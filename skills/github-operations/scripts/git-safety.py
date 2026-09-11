#!/usr/bin/env python3
"""Fail-closed Git helpers for github-operations branch workflows."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse


class SafetyError(RuntimeError):
    pass


def git(repository: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", "-C", str(repository), *args],
        check=False,
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or f"git exited {result.returncode}"
        raise SafetyError(detail)
    return result


def repository_root(repository: str) -> Path:
    root = git(Path(repository), "rev-parse", "--show-toplevel").stdout.strip()
    return Path(root).resolve()


def normalize_remote_url(value: str) -> tuple[str, str]:
    value = value.strip()
    if not value:
        raise SafetyError("remote URL is empty")

    if value.startswith(("/", "./", "../", "~")):
        return ("file", str(Path(value).expanduser().resolve()))

    if "://" in value:
        parsed = urlparse(value)
        if parsed.scheme == "file":
            if parsed.netloc not in ("", "localhost"):
                raise SafetyError(f"unsupported file remote URL: {value}")
            return ("file", str(Path(unquote(parsed.path)).resolve()))
        if not parsed.hostname:
            raise SafetyError(f"remote URL has no host: {value}")
        scheme = parsed.scheme.lower()
        host = parsed.hostname.lower()
        try:
            port = parsed.port
        except ValueError as error:
            raise SafetyError(f"remote URL has an invalid port: {value}") from error
        default_port = {"git": 9418, "http": 80, "https": 443, "ssh": 22}.get(scheme)
        host = f"[{host}]" if ":" in host else host
        if port is not None and port != default_port:
            host = f"{host}:{port}"
        path = parsed.path
    else:
        match = re.fullmatch(r"(?:[^@/]+@)?([^:/]+):(.+)", value)
        if not match:
            raise SafetyError(f"unsupported remote URL: {value}")
        host = match.group(1).lower()
        path = match.group(2)

    normalized_path = path.strip("/")
    if normalized_path.endswith(".git"):
        normalized_path = normalized_path[:-4]
    parts = normalized_path.split("/")
    if len(parts) != 2 or not all(parts):
        raise SafetyError(f"remote URL must identify one owner/repository: {value}")
    return host, "/".join(part.lower() for part in parts)


def remote_urls(root: Path, remote: str) -> tuple[list[str], list[str]]:
    fetch = git(root, "remote", "get-url", "--all", remote).stdout.splitlines()
    push = git(root, "remote", "get-url", "--push", "--all", remote).stdout.splitlines()
    if not fetch or not push:
        raise SafetyError(f"remote has no fetch/push URL: {remote}")
    return fetch, push


def remote_matches(root: Path, remote: str, target: tuple[str, str]) -> bool:
    fetch, push = remote_urls(root, remote)
    return all(normalize_remote_url(url) == target for url in [*fetch, *push])


def resolve_remote(args: argparse.Namespace) -> None:
    root = repository_root(args.repository)
    target = normalize_remote_url(args.target_url)
    if args.remote:
        if not remote_matches(root, args.remote, target):
            raise SafetyError(f"remote {args.remote!r} does not match {args.target_url}")
        print(args.remote)
        return

    remotes = git(root, "remote").stdout.splitlines()
    matches = [remote for remote in remotes if remote_matches(root, remote, target)]
    if len(matches) != 1:
        raise SafetyError(
            f"expected exactly one remote matching {args.target_url}, found {len(matches)}: {matches}"
        )
    print(matches[0])


def switch_branch(args: argparse.Namespace) -> None:
    root = repository_root(args.repository)
    command = ["switch", "--no-overwrite-ignore"]
    if args.track_start_point:
        command.extend(["--track", "-c", args.branch, args.track_start_point])
    else:
        command.append(args.branch)
    git(root, *command)
    current = git(root, "branch", "--show-current").stdout.strip()
    if current != args.branch:
        raise SafetyError(f"expected branch {args.branch!r}, current branch is {current!r}")
    print(current)


def detach_worktree(args: argparse.Namespace) -> None:
    root = repository_root(args.repository)
    expected = git(root, "rev-parse", "--verify", f"{args.expected_sha}^{{commit}}").stdout.strip()
    current = git(root, "branch", "--show-current").stdout.strip()
    if current != args.expected_branch:
        raise SafetyError(f"expected branch {args.expected_branch!r}, current branch is {current!r}")

    head = git(root, "rev-parse", "HEAD").stdout.strip()
    if head != expected:
        raise SafetyError(f"HEAD changed: expected {expected}, found {head}")

    status = git(
        root,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--ignored",
    ).stdout
    if status:
        raise SafetyError(f"worktree contains tracked, untracked, or ignored files:\n{status.rstrip()}")

    git(root, "switch", "--detach", "--no-overwrite-ignore", expected)
    current_after = git(root, "branch", "--show-current").stdout.strip()
    head_after = git(root, "rev-parse", "HEAD").stdout.strip()
    if current_after or head_after != expected:
        raise SafetyError(
            f"detach verification failed: branch={current_after!r}, HEAD={head_after!r}"
        )

    print(
        json.dumps(
            {
                "detached_branch": args.expected_branch,
                "head": expected,
            },
            sort_keys=True,
        )
    )


def worktrees(root: Path) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] = {}
    for line in git(root, "worktree", "list", "--porcelain").stdout.splitlines():
        if not line:
            if current:
                entries.append(current)
                current = {}
            continue
        key, _, value = line.partition(" ")
        current[key] = value
    if current:
        entries.append(current)
    return entries


def ref_oid(root: Path, ref: str) -> str | None:
    result = git(root, "rev-parse", "--verify", ref, check=False)
    return result.stdout.strip() if result.returncode == 0 else None


def remote_oid(root: Path, remote: str, branch: str) -> str | None:
    ref = f"refs/heads/{branch}"
    result = git(root, "ls-remote", "--heads", remote, ref)
    rows = [line.split() for line in result.stdout.splitlines() if line.strip()]
    if not rows:
        return None
    if len(rows) != 1 or len(rows[0]) != 2 or rows[0][1] != ref:
        raise SafetyError(f"unexpected ls-remote result for {remote}/{branch}")
    return rows[0][0]


def verify_expected_refs(
    root: Path,
    local_branch: str | None,
    remote: str,
    remote_branch: str,
    expected: str,
) -> tuple[str | None, str | None]:
    local = ref_oid(root, f"refs/heads/{local_branch}") if local_branch else None
    remote_value = remote_oid(root, remote, remote_branch)
    if local is not None and local != expected:
        raise SafetyError(f"local branch advanced: expected {expected}, found {local}")
    if remote_value is not None and remote_value != expected:
        raise SafetyError(f"remote branch advanced: expected {expected}, found {remote_value}")
    return local, remote_value


def remove_worktree(root: Path, local_branch: str, worktree_path: str) -> None:
    target = Path(worktree_path).resolve()
    expected_ref = f"refs/heads/{local_branch}"
    holders = [entry for entry in worktrees(root) if entry.get("branch") == expected_ref]
    if len(holders) != 1 or Path(holders[0]["worktree"]).resolve() != target:
        raise SafetyError(f"worktree does not uniquely hold {expected_ref}: {target}")

    status = git(
        target,
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--ignored",
    ).stdout
    if status:
        raise SafetyError(f"worktree contains tracked, untracked, or ignored files:\n{status.rstrip()}")
    git(root, "worktree", "remove", str(target))


def cleanup(args: argparse.Namespace) -> None:
    root = repository_root(args.repository)
    target = normalize_remote_url(args.target_url)
    if not remote_matches(root, args.remote, target):
        raise SafetyError(f"remote {args.remote!r} does not match {args.target_url}")
    expected = git(root, "rev-parse", "--verify", f"{args.expected_sha}^{{commit}}").stdout.strip()

    local_before, remote_before = verify_expected_refs(
        root, args.local_branch, args.remote, args.remote_branch, expected
    )

    if args.worktree:
        if not args.local_branch:
            raise SafetyError("--worktree requires --local-branch")
        remove_worktree(root, args.local_branch, args.worktree)

    if args.local_branch:
        expected_ref = f"refs/heads/{args.local_branch}"
        holders = [entry for entry in worktrees(root) if entry.get("branch") == expected_ref]
        if holders:
            raise SafetyError(f"local branch is still checked out: {holders}")

    local_now, remote_now = verify_expected_refs(
        root, args.local_branch, args.remote, args.remote_branch, expected
    )

    if args.local_branch and local_now is not None:
        git(root, "update-ref", "-d", f"refs/heads/{args.local_branch}", expected)
    if remote_now is not None:
        lease = f"refs/heads/{args.remote_branch}:{expected}"
        refspec = f":refs/heads/{args.remote_branch}"
        git(root, "push", f"--force-with-lease={lease}", args.remote, refspec)

    local_after = ref_oid(root, f"refs/heads/{args.local_branch}") if args.local_branch else None
    remote_after = remote_oid(root, args.remote, args.remote_branch)
    if local_after is not None or remote_after is not None:
        raise SafetyError(
            f"cleanup incomplete: local={local_after!r}, remote={remote_after!r}"
        )

    print(
        json.dumps(
            {
                "expected_sha": expected,
                "local_deleted": local_before is not None,
                "remote_deleted": remote_before is not None,
            },
            sort_keys=True,
        )
    )


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(description=__doc__)
    commands = root.add_subparsers(dest="command", required=True)

    resolve = commands.add_parser("resolve-remote", help="resolve one remote matching a canonical repository URL")
    resolve.add_argument("--repository", default=".")
    resolve.add_argument("--target-url", required=True)
    resolve.add_argument("--remote")
    resolve.set_defaults(handler=resolve_remote)

    switch = commands.add_parser("switch", help="switch without overwriting ignored files")
    switch.add_argument("--repository", default=".")
    switch.add_argument("--branch", required=True)
    switch.add_argument("--track-start-point")
    switch.set_defaults(handler=switch_branch)

    detach = commands.add_parser("detach", help="detach a clean worktree at its verified branch HEAD")
    detach.add_argument("--repository", default=".")
    detach.add_argument("--expected-branch", required=True)
    detach.add_argument("--expected-sha", required=True)
    detach.set_defaults(handler=detach_worktree)

    clean = commands.add_parser("cleanup", help="delete verified local and remote branch refs")
    clean.add_argument("--repository", default=".")
    clean.add_argument("--local-branch")
    clean.add_argument("--remote", required=True)
    clean.add_argument("--remote-branch", required=True)
    clean.add_argument("--expected-sha", required=True)
    clean.add_argument("--worktree")
    clean.add_argument("--target-url", required=True)
    clean.set_defaults(handler=cleanup)
    return root


def main() -> int:
    args = parser().parse_args()
    try:
        args.handler(args)
    except SafetyError as error:
        print(f"git-safety: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
