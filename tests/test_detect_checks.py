#!/usr/bin/env python3
"""
Tests for skills/goalify/scripts/detect_checks.py.

Covers: one expected candidate list per fixture (command-set equality, order-insensitive),
the npm stub produces no test candidate, the empty fixture prints the exact no-checks message,
--json output parses cleanly, a missing repo path exits 2, and a read-only check (fixture
file mtimes are unchanged after running detect()).

Standard library only. Run: python3 tests/test_detect_checks.py
Exit 0 = all pass, 1 = at least one failed.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(ROOT, "skills", "goalify", "scripts")
sys.path.insert(0, SCRIPTS)
import detect_checks  # noqa: E402

FIX = os.path.join(ROOT, "tests", "fixtures", "detect")
SCRIPT = os.path.join(SCRIPTS, "detect_checks.py")

failures = []
_total = 0


def check(name, ok, detail=""):
    global _total
    _total += 1
    print(f"{'PASS' if ok else 'FAIL'}: {name}" + (f"  ({detail})" if detail and not ok else ""))
    if not ok:
        failures.append(name)


def commands(candidates):
    """Extract just the command strings from a candidate list."""
    return sorted(c["command"] for c in candidates)


# ---------------------------------------------------------------------------
# Snapshot fixture mtimes before any detect() call
# ---------------------------------------------------------------------------
def _all_mtimes(base):
    result = {}
    for dirpath, _, filenames in os.walk(base):
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            result[p] = os.stat(p).st_mtime_ns
    return result


before_mtimes = _all_mtimes(FIX)

# ---------------------------------------------------------------------------
# npm-real: two scripts, npm detected from package-lock.json
# ---------------------------------------------------------------------------
npm_real = detect_checks.detect(os.path.join(FIX, "npm-real"))
check(
    "npm-real: npm test and npm run lint",
    commands(npm_real) == sorted(["npm test", "npm run lint"]),
    f"{commands(npm_real)}",
)
check(
    "npm-real: all medium confidence",
    all(c["confidence"] == "medium" for c in npm_real),
)
check(
    "npm-real: test kind is 'test', lint kind is 'lint'",
    {c["command"]: c["kind"] for c in npm_real} == {"npm test": "test", "npm run lint": "lint"},
)

# ---------------------------------------------------------------------------
# npm-stub: default npm init stub — no test candidate, no package.json candidate at all
# ---------------------------------------------------------------------------
npm_stub = detect_checks.detect(os.path.join(FIX, "npm-stub"))
check(
    "npm-stub: produces no candidates at all",
    npm_stub == [],
    f"{npm_stub}",
)
check(
    "npm-stub: no candidate of kind 'test'",
    not any(c["kind"] == "test" for c in npm_stub),
)
check(
    "npm-stub: no candidate whose command contains 'test' from package.json",
    not any("test" in c["command"] for c in npm_stub if c["source"] == "package.json"),
)

# ---------------------------------------------------------------------------
# pnpm: pnpm-lock.yaml detected → pnpm commands
# ---------------------------------------------------------------------------
pnpm = detect_checks.detect(os.path.join(FIX, "pnpm"))
check(
    "pnpm: pnpm test and pnpm run build",
    commands(pnpm) == sorted(["pnpm test", "pnpm run build"]),
    f"{commands(pnpm)}",
)

# ---------------------------------------------------------------------------
# pyproject: [tool.pytest.ini_options] + [tool.ruff]
# ---------------------------------------------------------------------------
pyproject = detect_checks.detect(os.path.join(FIX, "pyproject"))
check(
    "pyproject: python3 -m pytest and ruff check .",
    commands(pyproject) == sorted(["python3 -m pytest", "ruff check ."]),
    f"{commands(pyproject)}",
)
check(
    "pyproject: no mypy candidate (not in toml)",
    not any("mypy" in c["command"] for c in pyproject),
)

# ---------------------------------------------------------------------------
# cargo: Cargo.toml → cargo test + cargo build
# ---------------------------------------------------------------------------
cargo = detect_checks.detect(os.path.join(FIX, "cargo"))
check(
    "cargo: cargo test and cargo build",
    commands(cargo) == sorted(["cargo test", "cargo build"]),
    f"{commands(cargo)}",
)

# ---------------------------------------------------------------------------
# go: go.mod → go test ./... + go vet ./...
# ---------------------------------------------------------------------------
go = detect_checks.detect(os.path.join(FIX, "go"))
check(
    "go: go test ./... and go vet ./...",
    commands(go) == sorted(["go test ./...", "go vet ./..."]),
    f"{commands(go)}",
)

# ---------------------------------------------------------------------------
# makefile: test + lint only (install excluded, pattern rule excluded)
# ---------------------------------------------------------------------------
makefile = detect_checks.detect(os.path.join(FIX, "makefile"))
check(
    "makefile: make test and make lint only",
    commands(makefile) == sorted(["make test", "make lint"]),
    f"{commands(makefile)}",
)
check(
    "makefile: make install not emitted",
    not any(c["command"] == "make install" for c in makefile),
)

# ---------------------------------------------------------------------------
# workflow: make check (single-line) + make test (block run, echo filtered)
# ---------------------------------------------------------------------------
workflow = detect_checks.detect(os.path.join(FIX, "workflow"))
check(
    "workflow: make check and make test from CI",
    commands(workflow) == sorted(["make check", "make test"]),
    f"{commands(workflow)}",
)
check(
    "workflow: both are high confidence",
    all(c["confidence"] == "high" for c in workflow),
    f"{[(c['command'], c['confidence']) for c in workflow]}",
)
check(
    "workflow: npm ci not emitted (noise)",
    not any("npm ci" in c["command"] for c in workflow),
)
check(
    "workflow: echo not emitted (noise)",
    not any(c["command"].startswith("echo") for c in workflow),
)

# ---------------------------------------------------------------------------
# messy: complex block run with control flow, heredoc, curl — only real cmds survive
# ---------------------------------------------------------------------------
messy = detect_checks.detect(os.path.join(FIX, "messy"))
check(
    "messy: only the three real commands survive",
    commands(messy) == sorted(["python3 tests/run_all.py", "npx tsc --noEmit", "make check"]),
    f"{commands(messy)}",
)
check(
    "messy: all high confidence (CI source)",
    all(c["confidence"] == "high" for c in messy),
)
check(
    "messy: curl/echo/if/heredoc body not emitted",
    not any(
        c["command"].startswith(("curl", "echo", "if ", "export", "import "))
        or "<<" in c["command"]
        or "hello from heredoc" in c["command"]
        for c in messy
    ),
)

# ---------------------------------------------------------------------------
# empty: no candidates, CLI prints exact message
# ---------------------------------------------------------------------------
empty = detect_checks.detect(os.path.join(FIX, "empty"))
check("empty: detect() returns []", empty == [], f"{empty}")

result = subprocess.run(
    [sys.executable, SCRIPT, os.path.join(FIX, "empty")],
    capture_output=True, text=True,
)
check(
    "empty: CLI exits 0",
    result.returncode == 0,
    result.stderr,
)
check(
    "empty: CLI prints exact no-checks message",
    result.stdout.strip() == "no runnable checks found, so the DoD must be written by hand",
    repr(result.stdout.strip()),
)

# ---------------------------------------------------------------------------
# --json output
# ---------------------------------------------------------------------------
json_result = subprocess.run(
    [sys.executable, SCRIPT, os.path.join(FIX, "npm-real"), "--json"],
    capture_output=True, text=True,
)
check("--json: exits 0", json_result.returncode == 0, json_result.stderr)
try:
    parsed = json.loads(json_result.stdout)
    check("--json: output is a list", isinstance(parsed, list), type(parsed).__name__)
    check(
        "--json: each entry has command/source/kind/confidence",
        all({"command", "source", "kind", "confidence"} <= set(e.keys()) for e in parsed),
        f"{parsed}",
    )
    check(
        "--json: commands match npm-real fixture",
        sorted(e["command"] for e in parsed) == sorted(["npm test", "npm run lint"]),
        f"{sorted(e['command'] for e in parsed)}",
    )
except json.JSONDecodeError as exc:
    check("--json: output is valid JSON", False, str(exc))

# ---------------------------------------------------------------------------
# Missing repo → exit 2
# ---------------------------------------------------------------------------
missing = subprocess.run(
    [sys.executable, SCRIPT, "/nonexistent-path-for-detect-checks-test"],
    capture_output=True, text=True,
)
check("missing repo: exits 2", missing.returncode == 2, f"exit={missing.returncode}")

# ---------------------------------------------------------------------------
# Read-only: no fixture file mtime changed after all detect() calls
# ---------------------------------------------------------------------------
after_mtimes = _all_mtimes(FIX)
changed = {p for p in before_mtimes if before_mtimes[p] != after_mtimes.get(p)}
new_files = set(after_mtimes) - set(before_mtimes)
check(
    "read-only: no fixture file was written or touched",
    not changed and not new_files,
    f"changed={changed}, new={new_files}",
)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print("-" * 60)
print(f"{_total - len(failures)}/{_total} checks passed")
print(f"{len(failures)} failed" if failures else "All checks passed.")
sys.exit(1 if failures else 0)
