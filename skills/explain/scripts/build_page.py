#!/usr/bin/env python3
"""Build the explain learning page from a data file, checking every claim against the repo first.

    build_page.py --data data.json --repo /path/to/repo --out /path/to/page.html

Exits non-zero, writing nothing, if any evidence marked "verified" points at a
file, line range or snippet that is not really in the repo, or if a glossary
code name is not found in the repo. That is the mechanical guard against
AI-invented structure: fix the data (or mark the claim "unverified"), never
loosen the check.

Stdout is a single summary line on success; problems go to stderr.
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path

LEVEL_IDS = ["L0", "L1", "L2", "L3", "L4", "L5", "L6"]
SKIP_DIRS = {".git", "node_modules", "dist", "build", ".venv", "venv", "__pycache__",
             ".next", "coverage", "test-results", ".firebase", ".claude"}
# Never read files that commonly hold secrets, even to look for a name.
SECRET_FILE = re.compile(r"(^\.env)|\.pem$|\.key$|credential|secret", re.IGNORECASE)
MAX_FILE_BYTES = 2_000_000
MAX_FILES = 30_000
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")
WHERE = re.compile(r"^(?P<path>[^:]+?)(?::(?P<a>\d+)(?:-(?P<b>\d+))?)?$")
PATHLIKE = re.compile(r"[/\\]|\.(ts|tsx|js|jsx|mjs|py|go|rs|java|rb|json|md|yml|yaml|html|css)$")


def iter_repo_files(repo: Path):
    count = 0
    for path in repo.rglob("*"):
        if any(part in SKIP_DIRS for part in path.relative_to(repo).parts):
            continue
        if not path.is_file() or SECRET_FILE.search(path.name):
            continue
        count += 1
        if count > MAX_FILES:
            return
        yield path


def read_text(path: Path):
    try:
        if path.stat().st_size > MAX_FILE_BYTES:
            return None
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def build_token_index(repo: Path) -> set:
    tokens = set()
    for path in iter_repo_files(repo):
        text = read_text(path)
        if text is not None:
            tokens.update(IDENT.findall(text))
    return tokens


def check_evidence(repo: Path, where: str, contains):
    """Return an error string, or None if the pointer is real."""
    m = WHERE.match(where.strip())
    if not m:
        return f"cannot parse location {where!r} (use path, path:line or path:start-end)"
    rel = m.group("path").strip()
    target = (repo / rel).resolve()
    try:
        target.relative_to(repo.resolve())
    except ValueError:
        return f"{where!r} points outside the repo"
    if SECRET_FILE.search(target.name):
        return f"{where!r} points at a file that may hold secrets; cite something else"
    if not target.is_file():
        return f"{where!r}: file not found"
    text = read_text(target)
    if text is None:
        return f"{where!r}: file is not readable text"
    lines = text.splitlines()
    scope = text
    if m.group("a"):
        start = int(m.group("a"))
        end = int(m.group("b") or start)
        if start < 1 or end < start or end > len(lines):
            return f"{where!r}: line range is outside the file ({len(lines)} lines)"
        scope = "\n".join(lines[start - 1:end])
    if contains and contains not in scope:
        return f"{where!r}: expected text {contains!r} was not found there"
    return None


def code_names(code: str):
    """(is_path, names) for a glossary 'code' cell."""
    return (bool(PATHLIKE.search(code)), IDENT.findall(code))


def validate(data: dict, repo: Path):
    errors, warnings = [], []
    app = data.get("app")
    if not isinstance(app, dict) or not app.get("name"):
        errors.append("app.name is required")
    levels = data.get("levels")
    if not isinstance(levels, list) or not levels:
        errors.append("levels must be a non-empty list")
        return errors, warnings, 0, 0

    seen, verified, unverified = set(), 0, 0
    for lv in levels:
        lid = lv.get("id")
        if lid not in LEVEL_IDS:
            errors.append(f"unknown level id {lid!r} (expected one of {LEVEL_IDS})")
            continue
        if lid in seen:
            errors.append(f"{lid}: listed twice")
        seen.add(lid)
        if not (lv.get("answer") or {}).get("summary"):
            errors.append(f"{lid}: answer.summary is required")
        if not (lv.get("check") or {}).get("goodAnswerIncludes"):
            warnings.append(f"{lid}: check.goodAnswerIncludes is empty, so the pass check can't be self-graded")
        if not lv.get("evidence"):
            warnings.append(f"{lid}: no evidence listed")

        for ev in lv.get("evidence") or []:
            status = ev.get("status")
            if status not in ("verified", "unverified"):
                errors.append(f"{lid}: evidence status must be 'verified' or 'unverified': {ev.get('claim')!r}")
                continue
            if status == "unverified":
                unverified += 1
                continue
            verified += 1
            if not ev.get("where"):
                errors.append(f"{lid}: verified evidence needs 'where': {ev.get('claim')!r}")
                continue
            err = check_evidence(repo, ev["where"], ev.get("contains"))
            if err:
                errors.append(f"{lid}: {err} (claim: {ev.get('claim')!r})")

        answer = lv.get("answer") or {}
        sources = [answer.get("diagram", {}).get("source", "")] if answer.get("diagram") else []
        if ";" in "".join(sources):
            warnings.append(f"{lid}: diagram source contains ';' which Mermaid treats as a statement break")

    tokens = None
    for g in data.get("glossary") or []:
        code = g.get("code")
        if not code:
            continue
        is_path, names = code_names(code)
        if is_path:
            if not (repo / code.strip()).exists():
                errors.append(f"glossary: path {code!r} not found in the repo")
            continue
        if tokens is None:
            tokens = build_token_index(repo)
        missing = [n for n in names if n not in tokens]
        if missing:
            errors.append(f"glossary: {code!r} not found in the repo (missing: {', '.join(missing)})")
    return errors, warnings, verified, unverified


def render(template: str, data: dict) -> str:
    if template.count("__EXPLAIN_DATA__") != 1 or template.count("__EXPLAIN_TITLE__") != 1:
        raise SystemExit("template must contain each of __EXPLAIN_DATA__ and __EXPLAIN_TITLE__ exactly once")
    payload = json.dumps(data, ensure_ascii=False)
    # Keep the JSON inert inside a <script> element.
    payload = (payload.replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
               .replace("\u2028", "\\u2028").replace("\u2029", "\\u2029"))
    title = html.escape(f"{data['app']['name']} · explained")
    return template.replace("__EXPLAIN_TITLE__", title).replace("__EXPLAIN_DATA__", payload)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--data", required=True, help="path to the data JSON")
    parser.add_argument("--repo", required=True, help="path to the repo the claims are about")
    parser.add_argument("--out", required=True, help="where to write the HTML page")
    parser.add_argument("--template", help="override the template (default: ../references/template.html)")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    if not repo.is_dir():
        print(f"repo not found: {repo}", file=sys.stderr)
        return 2
    template_path = Path(args.template) if args.template else Path(__file__).resolve().parent.parent / "references" / "template.html"
    try:
        data = json.loads(Path(args.data).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read data file: {exc}", file=sys.stderr)
        return 2

    errors, warnings, verified, unverified = validate(data, repo)
    for w in warnings:
        print(f"warning: {w}", file=sys.stderr)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        print(f"not built: {len(errors)} problem(s). Fix the data or mark those claims 'unverified'.", file=sys.stderr)
        return 1

    out = Path(args.out).expanduser()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(template_path.read_text(encoding="utf-8"), data), encoding="utf-8")
    ids = ",".join(lv["id"] for lv in data["levels"])
    print(f"wrote {out} | levels {ids} | evidence {verified} verified, {unverified} unverified | {len(data.get('glossary') or [])} terms")
    return 0


if __name__ == "__main__":
    sys.exit(main())
