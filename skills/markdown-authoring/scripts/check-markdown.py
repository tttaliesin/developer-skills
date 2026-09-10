#!/usr/bin/env python3

"""Check portable Markdown invariants without third-party dependencies."""

from __future__ import annotations

import argparse
import html
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote


FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^(#{1,6})\s+\S")
REFERENCE_LINK_RE = re.compile(r"^ {0,3}\[(?:\\.|[^\]\\])+\]:[ \t]*")
SCHEME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
PATH_LINE_RE = re.compile(r"(?:^|/)[^/#?]+\.(?:md|mdx):\d+(?:$|[?#])", re.IGNORECASE)
HOME_PATH_RE = re.compile(
    r"(?:/home/[A-Za-z0-9._-]+/|/Users/[A-Za-z0-9._-]+/|[A-Za-z]:\\Users\\[^\\\s]+\\)"
)


@dataclass(frozen=True)
class Diagnostic:
    path: Path
    line: int
    code: str
    message: str
    severity: str = "error"

    def render(self) -> str:
        return f"{self.path}:{self.line}: {self.code} {self.severity}: {self.message}"


def normalize_destination(raw: str) -> str:
    destination = raw[1:-1] if raw.startswith("<") and raw.endswith(">") else raw
    # Markdown escapes/entities precede URL parsing. Percent escapes belong to
    # the path and must not become fragment/query separators before splitting.
    return html.unescape(re.sub(r"\\([!\"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])", r"\1", destination))


def escaped(text: str, index: int) -> bool:
    start = index
    while start > 0 and text[start - 1] == "\\":
        start -= 1
    return (index - start) % 2 == 1


def mask_literals(text: str, mdx: bool) -> tuple[str, bool]:
    """Mask recognized literals, preserving offsets and newlines.

    This is deliberately a scanner, not a full CommonMark/JSX parser. Unknown
    MDX regions are excluded and returned as an advisory coverage limit.
    """
    chars = list(text)
    limited = False

    def hide(start: int, end: int) -> None:
        chars[start:end] = ["\n" if c == "\n" else " " for c in text[start:end]]

    i = 0
    while i < len(text):
        if text.startswith("<!--", i):
            end = text.find("-->", i + 4)
            end = len(text) if end < 0 else end + 3
            hide(i, end)
            i = end
        elif text[i] == "`" and not escaped(text, i):
            run = re.match(r"`+", text[i:]).group()
            end = i + len(run)
            closing = None
            for match in re.finditer(r"`+", text[end:]):
                if len(match.group()) == len(run):
                    closing = end + match.end()
                    break
            if closing is None:
                i = end
            else:
                hide(i, closing)
                i = closing
        elif ((mdx and text[i] == "{") or re.match(r"</?[A-Za-z][\w.-]*(?=[\s/>])|<>", text[i:])) and not re.search(r"(?:\]\(|\]:)[ \t]*$", text[:i]):
            limited = True
            start = i
            expression = text[i] == "{"
            depth = 0
            quote = None
            i += 1
            while i < len(text):
                c = text[i]
                if quote:
                    if c == quote and not escaped(text, i):
                        quote = None
                elif c in "\"'`":
                    quote = c
                elif c == "{":
                    depth += 1
                elif c == "}":
                    if expression and depth == 0:
                        i += 1
                        break
                    depth -= 1
                elif c == ">" and not expression and depth == 0:
                    i += 1
                    break
                i += 1
            hide(start, i)
        else:
            i += 1
    return "".join(chars), limited


def destination_at(text: str, start: int) -> tuple[str, int] | None:
    """Read an angle destination or balanced bare destination."""
    i = start
    while i < len(text) and text[i].isspace():
        i += 1
    start = i
    if i == len(text):
        return None
    if text[i] == "<":
        i += 1
        while i < len(text) and text[i] != "\n":
            if text[i] == ">" and not escaped(text, i):
                return text[start:i + 1], i + 1
            i += 1
        return None
    depth = 0
    while i < len(text):
        c = text[i]
        if c == "\\" and i + 1 < len(text):
            i += 2
            continue
        if c.isspace():
            break
        if c == "(":
            depth += 1
        elif c == ")":
            if depth == 0:
                break
            depth -= 1
        i += 1
    if depth:
        return None
    return text[start:i], i


def link_destinations(line: str) -> list[str]:
    reference = REFERENCE_LINK_RE.match(line)
    if reference:
        parsed = destination_at(line, reference.end())
        return [parsed[0]] if parsed else []
    results = []
    i = 0
    while i < len(line):
        if line[i] != "[" or escaped(line, i):
            i += 1
            continue
        depth = 1
        j = i + 1
        while j < len(line) and depth:
            if not escaped(line, j):
                if line[j] == "[":
                    depth += 1
                elif line[j] == "]":
                    depth -= 1
            j += 1
        if depth or j == len(line) or line[j] != "(":
            i += 1
            continue
        parsed = destination_at(line, j + 1)
        if parsed:
            destination, end = parsed
            # Accept an outer close, optionally after a quoted title. Do not
            # diagnose an incomplete example as a real link.
            tail = line[end:]
            if re.match(r'''^(?:\s+(?:["'][^\n]*?["']|\([^\n)]*\))\s*)?\s*\)''', tail):
                results.append(destination)
            i = max(end, i + 1)
        else:
            i += 1
    return results


def check_relative_link(path: Path, line_number: int, destination: str) -> Diagnostic | None:
    if not destination or destination.startswith(("#", "//", "/")):
        return None
    if SCHEME_RE.match(destination) or any(char in destination for char in "{}$*"):
        return None

    target_text = unquote(destination.split("#", 1)[0].split("?", 1)[0])
    if not target_text:
        return None

    target = path.parent / target_text
    if not target.exists():
        return Diagnostic(
            path,
            line_number,
            "MA003",
            f"relative link target does not exist: {destination}",
        )
    return None


def check_file(path: Path) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except (OSError, UnicodeError) as error:
        return [Diagnostic(path, 1, "MA000", f"cannot read UTF-8 Markdown: {error}")]

    fence_character: str | None = None
    fence_length = 0
    fence_line = 0
    previous_heading_level: int | None = None

    prose = []
    html_block = False
    block_limited = False
    list_indents: list[int] = []
    for line_number, line in enumerate(lines, start=1):
        # Quote containers do not turn code examples into executable links.
        line = re.sub(r"^(?: {0,3}>[ \t]?)+", "", line)
        item = re.match(r"^( *)(?:[-+*]|\d+[.)])[ \t]+", line)
        if item and (len(item.group(1)) <= 3 or list_indents):
            indent = len(item.group(1))
            while list_indents and indent < list_indents[-1]:
                list_indents.pop()
            list_indents.append(item.end())
            line = line[item.end():]
        elif list_indents and line.strip():
            continuation = next((n for n in reversed(list_indents) if line.startswith(" " * n)), None)
            if continuation is not None:
                line = line[continuation:]
            else:
                list_indents.clear()
        fence = FENCE_RE.match(line)
        if fence:
            marker = fence.group(1)
            remainder = fence.group(2)
            if fence_character is None:
                fence_character = marker[0]
                fence_length = len(marker)
                fence_line = line_number
            elif (
                marker[0] == fence_character
                and len(marker) >= fence_length
                and not remainder.strip()
            ):
                fence_character = None
                fence_length = 0
                fence_line = 0
            prose.append("")
            continue

        if fence_character is not None:
            prose.append("")
            continue

        if re.match(r"^ {0,3}</?[A-Za-z][\w.-]*(?=[\s/>])", line):
            html_block = True
            block_limited = True
        if html_block:
            if not line.strip():
                html_block = False
            prose.append("")
            continue
        if line.startswith(("    ", "\t")):
            prose.append("")
            continue
        prose.append(line)

    visible, limited = mask_literals("\n".join(prose), path.suffix.lower() == ".mdx")
    if limited or block_limited:
        diagnostics.append(Diagnostic(path, 1, "MA006", "HTML/MDX regions excluded; use renderer-aware validation for those regions", "warning"))

    for line_number, line in enumerate(visible.splitlines(), start=1):

        heading = HEADING_RE.match(line)
        if heading:
            level = len(heading.group(1))
            if previous_heading_level is not None and level > previous_heading_level + 1:
                diagnostics.append(
                    Diagnostic(
                        path,
                        line_number,
                        "MA001",
                        f"heading level jumps from H{previous_heading_level} to H{level}",
                    )
                )
            previous_heading_level = level

        home_path = HOME_PATH_RE.search(prose[line_number - 1])
        if home_path:
            diagnostics.append(
                Diagnostic(
                    path,
                    line_number,
                    "MA002",
                    f"machine-specific home path: {home_path.group(0)}",
                )
            )

        for raw_destination in link_destinations(line):
            destination = normalize_destination(raw_destination)
            if PATH_LINE_RE.search(unquote(destination.split("#", 1)[0].split("?", 1)[0])):
                diagnostics.append(
                    Diagnostic(
                        path,
                        line_number,
                        "MA004",
                        f"non-portable path:line link: {destination}",
                    )
                )
                continue
            broken_link = check_relative_link(path, line_number, destination)
            if broken_link:
                diagnostics.append(broken_link)

    if fence_character is not None:
        diagnostics.append(Diagnostic(path, fence_line, "MA005", "fenced code block is not closed"))

    return diagnostics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check portable Markdown structure and repository-local link targets."
    )
    parser.add_argument("files", nargs="+", type=Path, metavar="FILE")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    diagnostics: list[Diagnostic] = []

    for path in args.files:
        if path.suffix.lower() not in {".md", ".mdx"}:
            diagnostics.append(Diagnostic(path, 1, "MA000", "expected a .md or .mdx file"))
            continue
        diagnostics.extend(check_file(path))

    for diagnostic in diagnostics:
        print(diagnostic.render(), file=sys.stderr)
    return 1 if any(item.severity == "error" for item in diagnostics) else 0


if __name__ == "__main__":
    raise SystemExit(main())
