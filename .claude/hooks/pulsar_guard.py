#!/usr/bin/env python3
# ruff: noqa
# fmt: off
# Vendored into many repos with different lint configs, so repo linters skip it; the kit lints it.
"""Shared Pulsar Claude Code hooks. Vendored into each repo by claude-kit/scripts/sync.sh; edit the kit,
not the copy. Standard library only. Reads the hook JSON on stdin.

  pulsar_guard.py pre-bash    PreToolUse/Bash: block force push, history rewrites on main, reading secrets
                              through the shell, and writes to protected paths
  pulsar_guard.py pre-file    PreToolUse/Read|Edit|Write|MultiEdit|NotebookEdit: block secrets and protected paths
  pulsar_guard.py post-edit   PostToolUse/Edit|Write|MultiEdit: fast lint of the one edited file

Exit 2 blocks a PreToolUse call (stderr is the reason) and shows lint findings to Claude on PostToolUse.
Repo-specific settings live in .claude/pulsar-guard.json (optional):
  {"protected": ["deploy/secrets/**"],           # never read or written by Claude
   "allow": ["test/**/fixtures/*.key"],          # secret-looking files that are safe test fixtures
   "lint": {".py": [["ruff", "check", "{file}"]]}} # replaces the default linter for that extension
"""

from __future__ import annotations

import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PROJECT = Path(
    os.environ.get("CLAUDE_PROJECT_DIR") or Path(__file__).resolve().parents[2]
)
CONFIG_FILE = PROJECT / ".claude" / "pulsar-guard.json"
LINT_TIMEOUT = 20  # seconds per command; the full suite belongs in CI, not here

SECRET_NAME_RE = re.compile(
    r"(?:^|[\\/])(?:\.env(?:\.[\w.-]+)?|[\w.-]*\.(?:pem|key|p12|pfx|kdbx)|id_(?:rsa|ed25519|ecdsa)|credentials\.json)$",
    re.IGNORECASE,
)
SAFE_ENV_RE = re.compile(r"\.env\.(?:example|sample|template|dist)$", re.IGNORECASE)
SECRET_DIR_RE = re.compile(
    r"(?:^|[\\/])(?:secrets?|\.secrets)(?:[\\/]|$)", re.IGNORECASE
)

FORCE_PUSH_RE = re.compile(
    r"\bgit\b[^;&|\n]*\bpush\b[^;&|\n]*(?:\s--force(?:-with-lease|-if-includes)?\b|\s-[a-zA-Z]*f\b|\s\+\S+)"
)
MAIN_REWRITE_RE = re.compile(
    r"\bgit\b[^;&|\n]*\bpush\b[^;&|\n]*\s(?:origin\s+)?:?(?:main|master)\b[^;&|\n]*--delete"
)
SHELL_READ_RE = re.compile(
    r"\b(?:cat|less|more|head|tail|bat|type|Get-Content|gc|source|\.)\s+[^;&|\n]*"
)
ENV_TOKEN_RE = re.compile(r"(?<![\w.-])(?:\S*[\\/])?\.env(?:\.[\w-]+)?(?![\w-])")
WRITE_OPS_RE = re.compile(
    r"(?:>>?|\btee\b|\bcp\b|\bmv\b|\brm\b|\bsed\s+-i|\bdd\b|\btruncate\b|Set-Content|Out-File|Remove-Item)"
)


def load_config() -> dict:
    try:
        return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def block(msg: str) -> None:
    print(f"Blocked by .claude/hooks/pulsar_guard.py: {msg}", file=sys.stderr)
    sys.exit(2)


def rel(p: str) -> str:
    path = Path(p)
    try:
        return path.resolve().relative_to(PROJECT.resolve()).as_posix()
    except (ValueError, OSError):
        return path.as_posix()


def is_secret(p: str) -> bool:
    p = p.replace("\\", "/")
    if SAFE_ENV_RE.search(p):
        return False
    return bool(SECRET_NAME_RE.search(p) or SECRET_DIR_RE.search(p))


def is_protected(p: str, cfg: dict) -> bool:
    r = rel(p)
    return any(fnmatch.fnmatch(r, pat) for pat in cfg.get("protected", []))


def pre_bash(data: dict, cfg: dict) -> None:
    cmd = str(data.get("tool_input", {}).get("command", ""))
    if FORCE_PUSH_RE.search(cmd):
        block("force pushes are not allowed (--force, -f, +refspec). Ask Adam.")
    if MAIN_REWRITE_RE.search(cmd):
        block("deleting main/master on the remote is not allowed.")
    for m in SHELL_READ_RE.finditer(cmd):
        for tok in ENV_TOKEN_RE.findall(m.group(0)):
            if not SAFE_ENV_RE.search(tok):
                block(
                    f"{tok} holds secrets. Read .env.example for variable names instead."
                )
    if WRITE_OPS_RE.search(cmd):
        for pat in cfg.get("protected", []):
            stem = pat.split("*")[0].rstrip("/")
            if stem and stem in cmd:
                block(
                    f"{pat} is protected in .claude/pulsar-guard.json; don't write there from Claude Code."
                )


def file_path(data: dict) -> str:
    ti = data.get("tool_input", {})
    return str(ti.get("file_path") or ti.get("notebook_path") or ti.get("path") or "")


def pre_file(data: dict, cfg: dict) -> None:
    p = file_path(data)
    if not p:
        return
    if is_secret(p) and not any(
        fnmatch.fnmatch(rel(p), pat) for pat in cfg.get("allow", [])
    ):
        block(
            f"{rel(p)} looks like a secret. Use .env.example for names; Adam handles real values."
        )
    if is_protected(p, cfg):
        block(f"{rel(p)} is protected in .claude/pulsar-guard.json.")


def default_linters(ext: str) -> list[list[str]]:
    node_bin = PROJECT / "node_modules" / ".bin"
    # Defaults report and never reformat, so a repo not already formatted doesn't get noisy diffs.
    # A repo that wants format-on-edit sets it in .claude/pulsar-guard.json.
    table: dict[str, list[list[str]]] = {
        ".py": [["ruff", "check", "--quiet", "{file}"]],
        ".sh": [["shellcheck", "-S", "warning", "{file}"]],
        ".go": [["gofmt", "-l", "{file}"]],
        ".kt": [["ktlint", "{file}"]],
        ".kts": [["ktlint", "{file}"]],
    }
    if ext in {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".astro"}:
        eslint = node_bin / ("eslint.cmd" if os.name == "nt" else "eslint")
        return [[str(eslint), "--no-warn-ignored", "{file}"]] if eslint.exists() else []
    return table.get(ext, [])


def post_edit(data: dict, cfg: dict) -> None:
    p = file_path(data)
    if not p or not Path(p).is_file():
        return
    ext = Path(p).suffix.lower()
    if ext == ".json":
        try:
            json.loads(Path(p).read_text(encoding="utf-8"))
        except ValueError as e:
            print(f"{rel(p)} is not valid JSON: {e}", file=sys.stderr)
            sys.exit(2)
        return
    commands = cfg.get("lint", {}).get(ext) or default_linters(ext)
    findings = []
    for cmd in commands:
        exe = cmd[0] if os.path.isabs(cmd[0]) else shutil.which(cmd[0])
        if not exe:
            continue  # tool not installed here; CI still runs it
        argv = [exe, *[a.replace("{file}", p) for a in cmd[1:]]]
        try:
            r = subprocess.run(
                argv,
                cwd=PROJECT,
                capture_output=True,
                text=True,
                timeout=LINT_TIMEOUT,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired) as e:
            print(f"pulsar_guard: {cmd[0]} skipped ({e})", file=sys.stderr)
            continue
        if r.returncode != 0:
            findings.append(f"$ {' '.join(cmd)}\n{(r.stdout + r.stderr)[-1500:]}")
    if findings:
        print(
            "Lint findings in the file you just edited:\n" + "\n".join(findings),
            file=sys.stderr,
        )
        sys.exit(2)


def main() -> None:
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        data = json.load(sys.stdin)
    except ValueError:
        data = {}
    handler = {"pre-bash": pre_bash, "pre-file": pre_file, "post-edit": post_edit}.get(
        mode
    )
    if handler:
        handler(data, load_config())


if __name__ == "__main__":
    main()
