#!/usr/bin/env python3
"""Route one repository's Git and gh authentication to one GitHub.com account."""

from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


STATE_NAME = "multi-github-account-operate.json"
LOCK_NAME = "multi-github-account-operate.lock"
TOKEN_ENV_KEYS = {
    "GH_TOKEN",
    "GITHUB_TOKEN",
    "GH_ENTERPRISE_TOKEN",
    "GITHUB_ENTERPRISE_TOKEN",
}


class RouterError(RuntimeError):
    """Fail-closed operational error with no credential material."""


def run(
    command: list[str],
    *,
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
    capture: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        command,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
        check=False,
    )


def git(root: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = run(["git", "-C", str(root), *arguments])
    if check and result.returncode != 0:
        raise RouterError(f"git command failed with exit code {result.returncode}")
    return result


def decoded(value: bytes) -> str:
    return value.decode("utf-8", errors="replace").strip()


def repository_root(repository: str) -> Path:
    result = run(["git", "-C", repository, "rev-parse", "--show-toplevel"])
    if result.returncode != 0:
        raise RouterError("repository is not a Git worktree")
    return Path(decoded(result.stdout)).resolve()


def common_directory(root: Path) -> Path:
    result = git(root, "rev-parse", "--path-format=absolute", "--git-common-dir")
    return Path(decoded(result.stdout)).resolve()


def state_path(root: Path) -> Path:
    return common_directory(root) / STATE_NAME


@contextmanager
def operation_lock(root: Path):
    """Serialize this helper's bind/unbind mutations across linked worktrees."""
    path = common_directory(root) / LOCK_NAME
    try:
        stream = path.open("a+b")
        stream.seek(0, os.SEEK_END)
        if stream.tell() == 0:
            stream.write(b"\0")
            stream.flush()
        stream.seek(0)
        if os.name == "nt":
            import msvcrt

            msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except (OSError, ImportError) as error:
        try:
            stream.close()
        except (OSError, UnboundLocalError):
            pass
        raise RouterError("another bind or unbind operation is active") from error
    try:
        yield
    finally:
        try:
            stream.seek(0)
            if os.name == "nt":
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
        finally:
            stream.close()


def validate_name(value: str, label: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9_.-]*[A-Za-z0-9])?", value):
        raise RouterError(f"invalid {label}")
    return value


def parse_target_url(value: str) -> dict[str, str]:
    parsed = urlparse(value)
    try:
        port = parsed.port
    except ValueError as error:
        raise RouterError("GitHub URL has an invalid port") from error
    if (
        parsed.scheme.lower() != "https"
        or parsed.hostname is None
        or parsed.hostname.lower() != "github.com"
        or port is not None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise RouterError("only credential-free GitHub.com HTTPS URLs are supported")
    parts = [unquote(part) for part in parsed.path.strip("/").split("/") if part]
    if len(parts) != 2:
        raise RouterError("URL must identify exactly one owner/repository")
    owner = validate_name(parts[0], "owner")
    repository = parts[1][:-4] if parts[1].lower().endswith(".git") else parts[1]
    repository = validate_name(repository, "repository name")
    return {
        "url": f"https://github.com/{owner}/{repository}",
        "host": "github.com",
        "owner": owner,
        "repository": repository,
    }


def remote_urls(root: Path, remote: str) -> list[str]:
    fetch = git(root, "remote", "get-url", "--all", remote)
    push = git(root, "remote", "get-url", "--push", "--all", remote)
    values = [line for line in decoded(fetch.stdout).splitlines() if line]
    values.extend(line for line in decoded(push.stdout).splitlines() if line)
    if not values:
        raise RouterError("remote has no fetch or push URL")
    return values


def remote_matches(root: Path, remote: str, target: dict[str, str]) -> bool:
    try:
        parsed = [parse_target_url(value) for value in remote_urls(root, remote)]
    except RouterError:
        return False
    expected = target["url"].casefold()
    return all(item["url"].casefold() == expected for item in parsed)


def config_values(root: Path, key: str) -> list[str]:
    result = git(root, "config", "--local", "--null", "--get-all", key, check=False)
    if result.returncode == 1:
        return []
    if result.returncode != 0:
        raise RouterError(f"cannot read local Git config key {key}")
    parts = result.stdout.split(b"\0")
    if parts and parts[-1] == b"":
        parts.pop()
    return [part.decode("utf-8", errors="strict") for part in parts]


def reject_worktree_config(root: Path) -> None:
    result = git(root, "config", "--local", "--bool", "--get", "extensions.worktreeConfig", check=False)
    if result.returncode not in (0, 1):
        raise RouterError("cannot inspect extensions.worktreeConfig")
    if result.returncode == 0 and decoded(result.stdout).casefold() == "true":
        common = common_directory(root)
        paths = [common / "config.worktree"]
        worktrees = common / "worktrees"
        if worktrees.is_dir():
            paths.extend(worktrees.glob("*/config.worktree"))
        found_codex_metadata = False
        for path in paths:
            if not path.exists():
                continue
            config = git(
                root, "config", "--file", str(path), "--no-includes",
                "--null", "--name-only", "--list", check=False,
            )
            if config.returncode != 0:
                raise RouterError("cannot inspect worktree configuration")
            keys = [key for key in config.stdout.split(b"\0") if key]
            if any(key.lower() != b"codex.localenvironmentconfigpath" for key in keys):
                raise RouterError("worktree configuration contains unsupported overrides")
            found_codex_metadata = found_codex_metadata or bool(keys)
        if not found_codex_metadata:
            raise RouterError("extensions.worktreeConfig requires metadata-only Codex configuration")


def set_config_values(root: Path, key: str, values: list[str]) -> None:
    if config_values(root, key):
        result = git(root, "config", "--local", "--unset-all", key, check=False)
        if result.returncode not in (0, 5):
            raise RouterError(f"cannot clear local Git config key {key}")
    for value in values:
        git(root, "config", "--local", "--add", key, value)


def assert_config_snapshot(root: Path, snapshot: dict[str, list[str]]) -> None:
    mismatches = [key for key, values in snapshot.items() if config_values(root, key) != values]
    if mismatches:
        raise RouterError(f"local Git config changed concurrently: {', '.join(mismatches)}")


def conditional_restore_config(
    root: Path,
    expected_current: dict[str, list[str]],
    restore_to: dict[str, list[str]],
) -> list[str]:
    """Restore only values still equal to this process's last verified snapshot."""
    failures: list[str] = []
    for key in reversed(list(expected_current)):
        try:
            current = config_values(root, key)
            if current == restore_to[key]:
                continue
            if current != expected_current[key]:
                failures.append(key)
                continue
            set_config_values(root, key, restore_to[key])
            if config_values(root, key) != restore_to[key]:
                failures.append(key)
        except RouterError:
            failures.append(key)
    return failures


def command_path(value: str) -> list[str]:
    candidate = Path(value)
    if candidate.exists():
        resolved = candidate.resolve()
    else:
        found = shutil.which(value)
        resolved = Path(found).resolve() if found else None
    if resolved is None or not resolved.is_file():
        raise RouterError("GitHub CLI executable was not found")
    if resolved.suffix.lower() == ".py":
        return [str(Path(sys.executable).resolve()), str(resolved)]
    return [str(resolved)]


def shell_command(arguments: list[str]) -> str:
    values = [Path(value).as_posix() if index < 2 else value for index, value in enumerate(arguments)]
    return " ".join(shlex.quote(value) for value in values)


def installed_config(state: dict[str, Any]) -> dict[str, list[str]]:
    python = state["python_executable"]
    script = state["script_path"]
    credential = "!" + shell_command([python, script, "credential", "--repository", "."])
    gh_alias = "!" + shell_command([python, script, "gh", "--repository", ".", "--"])
    prefix = f"credential.https://{state['target']['host']}"
    return {
        f"{prefix}.helper": ["", credential],
        f"{prefix}.username": [state["account"]],
        f"{prefix}.useHttpPath": ["true"],
        "alias.gh": [gh_alias],
    }


def read_state(root: Path, *, required: bool = True) -> dict[str, Any] | None:
    path = state_path(root)
    if not path.exists():
        if required:
            raise RouterError("repository is not bound")
        return None
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise RouterError("binding state is unreadable") from error
    required_keys = {
        "schema_version",
        "target",
        "account",
        "remote",
        "gh_command",
        "python_executable",
        "script_path",
        "installed_config",
        "previous_config",
    }
    try:
        if not isinstance(value, dict) or value.get("schema_version") != 1 or not required_keys.issubset(value):
            raise RouterError("binding state has an unsupported schema")
        target = value["target"]
        if not isinstance(target, dict):
            raise RouterError("binding state has an unsupported schema")
        normalized_target = parse_target_url(target["url"])
        if target != normalized_target:
            raise RouterError("binding state target is inconsistent")
        validate_name(value["account"], "account")
        validate_name(value["remote"], "remote")
        if (
            not isinstance(value["gh_command"], list)
            or not value["gh_command"]
            or not all(isinstance(item, str) and item for item in value["gh_command"])
            or not isinstance(value["python_executable"], str)
            or not value["python_executable"]
            or not isinstance(value["script_path"], str)
            or not value["script_path"]
        ):
            raise RouterError("binding state has an unsupported schema")
        for field in ("installed_config", "previous_config"):
            config = value[field]
            if not isinstance(config, dict) or not all(
                isinstance(key, str)
                and isinstance(items, list)
                and all(isinstance(item, str) for item in items)
                for key, items in config.items()
            ):
                raise RouterError("binding state has an unsupported schema")
        if value["installed_config"] != installed_config(value):
            raise RouterError("binding state config record is inconsistent")
        if set(value["previous_config"]) != set(value["installed_config"]):
            raise RouterError("binding state recovery record is inconsistent")
    except (AttributeError, KeyError, TypeError) as error:
        raise RouterError("binding state has an unsupported schema") from error
    return value


def atomic_write(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=f"{path.name}.", suffix=".tmp", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, sort_keys=True)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def config_report(root: Path, expected: dict[str, list[str]]) -> tuple[bool, list[str]]:
    mismatches = [key for key, values in expected.items() if config_values(root, key) != values]
    return not mismatches, mismatches


def status_payload(root: Path, state: dict[str, Any] | None) -> dict[str, Any]:
    if state is None:
        return {"bound": False, "common_directory": str(common_directory(root))}
    config_intact, mismatches = config_report(root, state["installed_config"])
    remote_intact = remote_matches(root, state["remote"], state["target"])
    return {
        "bound": True,
        "account": state["account"],
        "target_url": state["target"]["url"],
        "remote": state["remote"],
        "common_directory": str(common_directory(root)),
        "config_intact": config_intact,
        "remote_matches": remote_intact,
        "mismatched_keys": mismatches,
    }


def bind_locked(args: argparse.Namespace, root: Path) -> int:
    target = parse_target_url(args.url)
    account = validate_name(args.account, "account")
    remote = validate_name(args.remote, "remote")
    if not remote_matches(root, remote, target):
        raise RouterError("remote fetch and push URLs do not match the selected GitHub URL")

    existing = read_state(root, required=False)
    if existing is not None:
        same = (
            existing["target"]["url"].casefold() == target["url"].casefold()
            and existing["account"].casefold() == account.casefold()
            and existing["remote"] == remote
        )
        config_intact, _ = config_report(root, existing["installed_config"])
        remote_intact = remote_matches(root, existing["remote"], existing["target"])
        if same and config_intact and remote_intact:
            print(json.dumps(status_payload(root, existing), sort_keys=True))
            return 0
        raise RouterError("repository already has a different or modified binding")

    state: dict[str, Any] = {
        "schema_version": 1,
        "target": target,
        "account": account,
        "remote": remote,
        "gh_command": command_path(args.gh_executable),
        "python_executable": str(Path(sys.executable).resolve()),
        "script_path": str(Path(__file__).resolve()),
    }
    expected = installed_config(state)
    previous = {key: config_values(root, key) for key in expected}
    conflicts = [key for key, values in previous.items() if values]
    if conflicts:
        raise RouterError(f"existing local Git config would be overwritten: {', '.join(conflicts)}")
    state["installed_config"] = expected
    state["previous_config"] = previous

    current_snapshot = {key: list(values) for key, values in previous.items()}
    try:
        for key, values in expected.items():
            assert_config_snapshot(root, current_snapshot)
            set_config_values(root, key, values)
            current_snapshot[key] = values
            assert_config_snapshot(root, current_snapshot)
        config_intact, mismatches = config_report(root, expected)
        if not config_intact:
            raise RouterError(f"local Git config verification failed: {', '.join(mismatches)}")
        atomic_write(state_path(root), state)
    except (OSError, RouterError) as error:
        rollback_failures = conditional_restore_config(root, current_snapshot, previous)
        if rollback_failures:
            raise RouterError(
                "bind failed and changed config was preserved for manual recovery: "
                + ", ".join(rollback_failures)
            ) from error
        if isinstance(error, RouterError):
            raise
        raise RouterError("cannot write binding state") from error

    print(json.dumps(status_payload(root, state), sort_keys=True))
    return 0


def bind(args: argparse.Namespace) -> int:
    root = repository_root(args.repository)
    with operation_lock(root):
        reject_worktree_config(root)
        return bind_locked(args, root)


def status(args: argparse.Namespace) -> int:
    root = repository_root(args.repository)
    reject_worktree_config(root)
    state = read_state(root, required=False)
    payload = status_payload(root, state)
    print(json.dumps(payload, sort_keys=True))
    if state is None:
        return 1
    return 0 if payload["config_intact"] and payload["remote_matches"] else 2


def unbind_locked(root: Path) -> int:
    state = read_state(root)
    assert state is not None
    config_intact, mismatches = config_report(root, state["installed_config"])
    if not config_intact:
        raise RouterError(f"refusing to overwrite changed local Git config: {', '.join(mismatches)}")
    installed = {key: list(values) for key, values in state["installed_config"].items()}
    current_snapshot = {key: list(values) for key, values in installed.items()}
    try:
        for key, values in state["previous_config"].items():
            assert_config_snapshot(root, current_snapshot)
            set_config_values(root, key, values)
            current_snapshot[key] = values
            assert_config_snapshot(root, current_snapshot)
        if read_state(root) != state:
            raise RouterError("binding state changed concurrently")
        state_path(root).unlink()
    except (OSError, RouterError) as error:
        rollback_failures = conditional_restore_config(root, current_snapshot, installed)
        if rollback_failures:
            raise RouterError(
                "unbind failed and changed config was preserved for manual recovery: "
                + ", ".join(rollback_failures)
            ) from error
        if isinstance(error, RouterError):
            raise
        raise RouterError("cannot remove binding state") from error
    print(json.dumps({"bound": False, "common_directory": str(common_directory(root))}, sort_keys=True))
    return 0


def unbind(args: argparse.Namespace) -> int:
    root = repository_root(args.repository)
    with operation_lock(root):
        reject_worktree_config(root)
        return unbind_locked(root)


def clean_environment() -> dict[str, str]:
    environment = os.environ.copy()
    for key in list(environment):
        upper = key.upper()
        if (
            upper in TOKEN_ENV_KEYS
            or upper.startswith("GH_DEBUG")
            or upper.startswith("GIT_TRACE")
            or upper in {"DEBUG", "GIT_CURL_VERBOSE"}
        ):
            environment.pop(key, None)
    return environment


def selected_token(state: dict[str, Any]) -> str:
    command = [
        *state["gh_command"],
        "auth",
        "token",
        "--hostname",
        state["target"]["host"],
        "--user",
        state["account"],
    ]
    try:
        result = run(command, env=clean_environment())
    except OSError as error:
        raise RouterError("selected GitHub account token is unavailable") from error
    if result.returncode != 0:
        raise RouterError("selected GitHub account token is unavailable")
    token = decoded(result.stdout)
    if not token or any(character in token for character in "\r\n\0"):
        raise RouterError("selected GitHub account returned an invalid token")
    return token


def ensure_binding(root: Path) -> dict[str, Any]:
    reject_worktree_config(root)
    state = read_state(root)
    assert state is not None
    config_intact, mismatches = config_report(root, state["installed_config"])
    if not config_intact:
        raise RouterError(f"binding config changed: {', '.join(mismatches)}")
    if not remote_matches(root, state["remote"], state["target"]):
        raise RouterError("bound remote no longer matches the selected GitHub URL")
    return state


def parse_credential_input(stream: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in stream.splitlines():
        if not line:
            break
        key, separator, value = line.partition("=")
        if separator:
            values[key] = value
    if "url" in values:
        parsed = urlparse(values["url"])
        values.update(
            {
                "protocol": parsed.scheme,
                "host": parsed.netloc.split("@")[-1],
                "path": parsed.path.lstrip("/"),
                "username": parsed.username or values.get("username", ""),
            }
        )
    return values


def normalized_path(value: str) -> str:
    path = unquote(value).strip("/")
    if path.lower().endswith(".git"):
        path = path[:-4]
    return path.casefold()


def credential_matches(values: dict[str, str], state: dict[str, Any]) -> bool:
    expected_path = f"{state['target']['owner']}/{state['target']['repository']}".casefold()
    username = values.get("username", "")
    return (
        values.get("protocol", "").casefold() == "https"
        and values.get("host", "").casefold() == state["target"]["host"].casefold()
        and normalized_path(values.get("path", "")) == expected_path
        and (not username or username.casefold() == state["account"].casefold())
    )


def refuse_credential(message: str | None = None) -> int:
    if message:
        print(message, file=sys.stderr)
    print("quit=true")
    return 0


def credential(args: argparse.Namespace) -> int:
    if args.operation != "get":
        return 0
    try:
        root = repository_root(args.repository)
        state = ensure_binding(root)
        values = parse_credential_input(sys.stdin.read())
        if not credential_matches(values, state):
            return refuse_credential()
        if sys.stdout.isatty():
            return refuse_credential("credential output requires the Git credential protocol")
        token = selected_token(state)
    except (OSError, RouterError):
        return refuse_credential("repository account binding is unavailable")
    print(f"username={state['account']}")
    print(f"password={token}")
    return 0


def repository_argument(value: str, state: dict[str, Any]) -> bool:
    normalized = value.strip().strip("/")
    if normalized.lower().endswith(".git"):
        normalized = normalized[:-4]
    if normalized.casefold().startswith("github.com/"):
        normalized = normalized[len("github.com/") :]
    expected = f"{state['target']['owner']}/{state['target']['repository']}"
    return normalized.casefold() == expected.casefold()


def validate_gh_arguments(arguments: list[str], state: dict[str, Any]) -> None:
    if not arguments:
        raise RouterError("a gh command is required")
    if arguments[0] in {"auth", "alias", "config"}:
        raise RouterError("authentication and global gh configuration commands are not forwarded")
    index = 0
    while index < len(arguments):
        value = arguments[index]
        if value in {"--hostname", "--repo", "-R"}:
            if index + 1 >= len(arguments):
                raise RouterError(f"{value} requires a value")
            selected = arguments[index + 1]
            if value == "--hostname" and selected.casefold() != state["target"]["host"].casefold():
                raise RouterError("gh hostname does not match the repository binding")
            if value in {"--repo", "-R"} and not repository_argument(selected, state):
                raise RouterError("gh repository does not match the repository binding")
            index += 2
            continue
        if value.startswith("--hostname="):
            if value.split("=", 1)[1].casefold() != state["target"]["host"].casefold():
                raise RouterError("gh hostname does not match the repository binding")
        if value.startswith("--repo=") and not repository_argument(value.split("=", 1)[1], state):
            raise RouterError("gh repository does not match the repository binding")
        if value.startswith("-R="):
            if not repository_argument(value.split("=", 1)[1], state):
                raise RouterError("gh repository does not match the repository binding")
            index += 1
            continue
        if value.startswith("-R") and value != "-R" and not repository_argument(value[2:], state):
            raise RouterError("gh repository does not match the repository binding")
        index += 1


def gh_forward(args: argparse.Namespace) -> int:
    root = repository_root(args.repository)
    state = ensure_binding(root)
    arguments = list(args.arguments)
    if arguments and arguments[0] == "--":
        arguments.pop(0)
    validate_gh_arguments(arguments, state)
    token = selected_token(state)
    environment = clean_environment()
    environment["GH_TOKEN"] = token
    environment["GH_HOST"] = state["target"]["host"]
    environment["GH_REPO"] = f"{state['target']['owner']}/{state['target']['repository']}"
    result = run([*state["gh_command"], *arguments], cwd=root, env=environment, capture=False)
    return result.returncode


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    bind_parser = commands.add_parser("bind", help="bind this repository to one GitHub.com account")
    bind_parser.add_argument("--repository", default=".")
    bind_parser.add_argument("--remote", default="origin")
    bind_parser.add_argument("--url", required=True)
    bind_parser.add_argument("--account", required=True)
    bind_parser.add_argument("--gh-executable", default="gh")
    bind_parser.set_defaults(handler=bind)

    status_parser = commands.add_parser("status", help="inspect the secret-free binding state")
    status_parser.add_argument("--repository", default=".")
    status_parser.set_defaults(handler=status)

    unbind_parser = commands.add_parser("unbind", help="remove an unchanged binding")
    unbind_parser.add_argument("--repository", default=".")
    unbind_parser.set_defaults(handler=unbind)

    credential_parser = commands.add_parser("credential", help="implement the Git credential protocol")
    credential_parser.add_argument("--repository", default=".")
    credential_parser.add_argument("operation")
    credential_parser.set_defaults(handler=credential)

    gh_parser = commands.add_parser("gh", help="forward a gh command with the selected account")
    gh_parser.add_argument("--repository", default=".")
    gh_parser.add_argument("arguments", nargs=argparse.REMAINDER)
    gh_parser.set_defaults(handler=gh_forward)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        return int(args.handler(args))
    except RouterError as error:
        print(f"multi-github-account-operate: {error}", file=sys.stderr)
        return 1
    except OSError:
        print("multi-github-account-operate: operating system operation failed", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
