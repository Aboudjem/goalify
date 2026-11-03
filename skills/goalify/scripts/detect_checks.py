#!/usr/bin/env python3
"""
detect_checks.py: propose candidate check commands from a repo so a goalify brief's
Definition of done never invents a command that does not exist.

Reads package.json, pyproject.toml, Cargo.toml, go.mod, Makefile, justfile,
deno.json, and .github/workflows/*.yml to surface test/lint/build/typecheck commands
that are actually defined in that repo.

Usage:
    python3 detect_checks.py <repo>          # human-readable list
    python3 detect_checks.py <repo> --json   # JSON array

Exit 0 on success (even when no candidates are found), 2 on a missing repo path.
Standard library only. It reads files and never writes, runs, or fetches anything.

Module API: detect(repo) -> list[dict]
Each dict has keys: command (str), source (str), kind (str), confidence (str).
kind is one of: test, lint, build, typecheck, check, other.
confidence is "high" for CI-sourced commands, "medium" for everything else.
"""

import json
import os
import re
import sys

# tomllib is in the stdlib since 3.11; fall back to regex for older Pythons.
try:
    import tomllib as _tomllib
except ImportError:
    _tomllib = None

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _read(path):
    """Read a text file, return None on any error."""
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return None


def _load_toml(path):
    """Return a parsed TOML dict if tomllib is available, else None."""
    if _tomllib is None:
        return None
    try:
        with open(path, "rb") as f:
            return _tomllib.load(f)
    except Exception:
        return None


def _toml_section_exists(text, dotted_key):
    """Regex fallback: True when the section header [dotted_key] appears in text."""
    pattern = re.compile(r"^\[" + re.escape(dotted_key) + r"\]", re.MULTILINE)
    return bool(pattern.search(text))


# ---------------------------------------------------------------------------
# Kind inference
# ---------------------------------------------------------------------------

def _kind_from_name(name):
    """Infer kind from a script/target/recipe name."""
    n = name.lower()
    if n == "test" or n.startswith("test:") or n.startswith("test-"):
        return "test"
    if n == "lint":
        return "lint"
    if n == "build":
        return "build"
    if n in ("typecheck", "type-check", "types"):
        return "typecheck"
    if n in ("check", "verify", "ci"):
        return "check"
    return "other"


def _kind_from_command(cmd):
    """Infer kind from a raw shell command string."""
    c = cmd.lower()

    test_markers = (
        "pytest", "jest", "vitest", "mocha", "ava ", "tap ",
        "deno test", "node --test", "python3 -m pytest", "python -m pytest",
        "cargo test", "go test", "npm test", "pnpm test", "yarn test", "bun run test",
    )
    if any(t in c for t in test_markers):
        return "test"

    lint_markers = ("eslint", "ruff check", "pylint", "flake8", "golangci-lint", "cargo clippy")
    if any(t in c for t in lint_markers):
        return "lint"

    tc_markers = ("tsc ", "tsc\n", "npx tsc", "mypy ", "pyright", "flow ")
    if any(t in c for t in tc_markers):
        return "typecheck"

    build_markers = ("cargo build", "go build", "vite build", "webpack ")
    if any(t in c for t in build_markers):
        return "build"

    m = re.search(r"\b(?:make|just|deno\s+task)\s+([A-Za-z0-9_.-]+)", c)
    if m:
        return _kind_from_name(m.group(1))

    if "test" in c:
        return "test"
    if "lint" in c:
        return "lint"
    if "build" in c:
        return "build"
    if "check" in c or "verify" in c:
        return "check"
    return "other"


# ---------------------------------------------------------------------------
# CI line filtering — allowlist approach
# ---------------------------------------------------------------------------

# Shell keywords and builtins whose presence as the first token means the line
# is control flow, not a runnable check command.
_SHELL_KEYWORDS = frozenset({
    "if", "then", "else", "elif", "fi",
    "for", "while", "until", "do", "done",
    "case", "esac", ";;",
    "exit", "return", "break", "continue",
    "set", "export", "unset",
    "echo", "printf", "cat", "read",
    "shopt", "local", "declare", "typeset",
    "[", "[[", "]]",
    "true", "false",
})


def _is_allowed_runner(cmd):
    """True when the first executable token of *cmd* is a known check runner.

    This is an allowlist: anything not listed here is silently dropped, which
    eliminates shell control flow, variable assignments, curl/git setup steps,
    and inline scripts without needing to enumerate every possible noise pattern.
    """
    # Strip leading env-var assignments like FOO=bar python3 ...
    tokens = cmd.split()
    while tokens and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", tokens[0]):
        tokens = tokens[1:]
    if not tokens:
        return False

    first = tokens[0]

    # python / python3: must run a named .py file or use -m <module>
    if first in ("python", "python3"):
        if "-m" in tokens:
            return True
        return any(t.endswith(".py") and not t.startswith("-") for t in tokens[1:])

    # Direct test/lint runners
    if first in ("pytest", "tox", "nox"):
        return True

    # npm: reject install/ci/uninstall; accept test/run/exec/...
    if first == "npm":
        if len(tokens) < 2:
            return False
        return tokens[1] not in ("ci", "install", "i", "update", "uninstall", "un")

    # pnpm: reject install family
    if first == "pnpm":
        if len(tokens) < 2:
            return False
        return tokens[1] not in ("install", "i", "add", "remove", "update", "up")

    # yarn: reject install/add/remove
    if first == "yarn":
        if len(tokens) < 2:
            return False
        return tokens[1] not in ("install", "add", "remove", "upgrade", "up")

    # bun: reject install/add/remove
    if first == "bun":
        if len(tokens) < 2:
            return False
        return tokens[1] not in ("install", "add", "remove", "update")

    # npx — any invocation is plausibly a check tool
    if first == "npx":
        return True

    # make / just — any target is potentially a check
    if first in ("make", "just"):
        return True

    # cargo: only test/build/clippy/check/fmt
    if first == "cargo":
        return len(tokens) >= 2 and tokens[1] in ("test", "build", "clippy", "check", "fmt")

    # go: only test/vet/build
    if first == "go":
        return len(tokens) >= 2 and tokens[1] in ("test", "vet", "build")

    # deno: test/task/lint/check
    if first == "deno":
        return len(tokens) >= 2 and tokens[1] in ("test", "task", "lint", "check")

    # Linters / formatters / typecheckers
    if first in ("ruff", "mypy", "tsc", "eslint"):
        return True
    if first == "prettier":
        return "--check" in tokens

    # Shell scripts (.sh or paths starting with ./)
    if first in ("bash", "sh"):
        return any(
            not t.startswith("-") and (t.endswith(".sh") or "/" in t)
            for t in tokens[1:]
        )
    if first.startswith("./"):
        return True

    return False


def _is_ci_candidate(cmd):
    """True when *cmd* looks like a runnable check command worth putting in a DoD.

    Rejects: GitHub Actions expressions (${{...}}), variable assignments,
    shell keywords/control flow, continuation-flag lines, and anything whose
    first token is not a known check runner.
    """
    if not cmd:
        return False
    # GitHub Actions template expressions
    if "${{" in cmd:
        return False
    # Variable assignment: FOO=... or FOO=$(...)
    if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", cmd):
        return False
    # Shell keyword as first token
    first_token = cmd.split()[0] if cmd.split() else ""
    if first_token in _SHELL_KEYWORDS:
        return False
    return _is_allowed_runner(cmd)


# ---------------------------------------------------------------------------
# Per-source detectors
# ---------------------------------------------------------------------------

def _detect_package_json(repo):
    candidates = []
    pkg_path = os.path.join(repo, "package.json")
    text = _read(pkg_path)
    if not text:
        return candidates

    try:
        pkg = json.loads(text)
    except Exception:
        return candidates

    scripts = pkg.get("scripts", {})
    if not isinstance(scripts, dict):
        return candidates

    # Detect package manager from lockfile presence
    if os.path.exists(os.path.join(repo, "pnpm-lock.yaml")):
        pm = "pnpm"
    elif os.path.exists(os.path.join(repo, "yarn.lock")):
        pm = "yarn"
    elif (os.path.exists(os.path.join(repo, "bun.lockb"))
          or os.path.exists(os.path.join(repo, "bun.lock"))):
        pm = "bun"
    else:
        pm = "npm"  # package-lock.json or default

    TARGET_NAMES = {"test", "lint", "typecheck", "build", "check"}

    for name, cmd in scripts.items():
        if not isinstance(cmd, str) or not cmd.strip():
            continue
        if name not in TARGET_NAMES and not name.startswith("test:"):
            continue
        # Reject npm's default stub
        if "Error: no test specified" in cmd:
            continue

        if name == "test":
            command = {"npm": "npm test", "pnpm": "pnpm test",
                       "yarn": "yarn test", "bun": "bun run test"}[pm]
        else:
            command = {
                "npm":  f"npm run {name}",
                "pnpm": f"pnpm run {name}",
                "yarn": f"yarn {name}",
                "bun":  f"bun run {name}",
            }[pm]

        candidates.append({
            "command": command,
            "source": "package.json",
            "kind": _kind_from_name(name),
            "confidence": "medium",
        })

    return candidates


def _detect_python(repo):
    candidates = []

    pp_path = os.path.join(repo, "pyproject.toml")
    pp_text = _read(pp_path)
    if pp_text:
        has_pytest = False
        has_ruff = False
        has_mypy = False

        data = _load_toml(pp_path)
        if data is not None:
            tool = data.get("tool", {})
            has_pytest = "pytest" in tool
            has_ruff = "ruff" in tool
            has_mypy = "mypy" in tool
            if not has_pytest:
                project = data.get("project", {})
                deps = project.get("dependencies", [])
                opt = project.get("optional-dependencies", {})
                all_deps = list(deps) + [d for g in opt.values() for d in g
                                         if isinstance(d, str)]
                has_pytest = any(
                    isinstance(d, str) and "pytest" in d.lower() for d in all_deps
                )
        else:
            has_pytest = _toml_section_exists(pp_text, "tool.pytest.ini_options") or bool(
                re.search(r"pytest", pp_text)
            )
            has_ruff = _toml_section_exists(pp_text, "tool.ruff")
            has_mypy = _toml_section_exists(pp_text, "tool.mypy")

        if has_pytest:
            candidates.append({
                "command": "python3 -m pytest",
                "source": "pyproject.toml",
                "kind": "test",
                "confidence": "medium",
            })
        if has_ruff:
            candidates.append({
                "command": "ruff check .",
                "source": "pyproject.toml",
                "kind": "lint",
                "confidence": "medium",
            })
        if has_mypy:
            candidates.append({
                "command": "mypy .",
                "source": "pyproject.toml",
                "kind": "typecheck",
                "confidence": "medium",
            })

    if os.path.exists(os.path.join(repo, "pytest.ini")):
        if not any(c["command"] == "python3 -m pytest" for c in candidates):
            candidates.append({
                "command": "python3 -m pytest",
                "source": "pytest.ini",
                "kind": "test",
                "confidence": "medium",
            })

    tox_path = os.path.join(repo, "tox.ini")
    tox_text = _read(tox_path)
    if tox_text:
        if not any(c["command"] == "python3 -m pytest" for c in candidates):
            candidates.append({
                "command": "python3 -m pytest",
                "source": "tox.ini",
                "kind": "test",
                "confidence": "medium",
            })
        if re.search(r"^\[tox\]", tox_text, re.MULTILINE):
            candidates.append({
                "command": "tox",
                "source": "tox.ini",
                "kind": "test",
                "confidence": "medium",
            })

    return candidates


def _detect_cargo(repo):
    if not os.path.exists(os.path.join(repo, "Cargo.toml")):
        return []
    return [
        {"command": "cargo test",  "source": "Cargo.toml", "kind": "test",  "confidence": "medium"},
        {"command": "cargo build", "source": "Cargo.toml", "kind": "build", "confidence": "medium"},
    ]


def _detect_go(repo):
    if not os.path.exists(os.path.join(repo, "go.mod")):
        return []
    return [
        {"command": "go test ./...", "source": "go.mod", "kind": "test",  "confidence": "medium"},
        {"command": "go vet ./...",  "source": "go.mod", "kind": "check", "confidence": "medium"},
    ]


_MAKE_ALLOWED = {"test", "check", "lint", "build", "verify", "ci", "typecheck"}
_MAKE_TARGET_RE = re.compile(r"^([A-Za-z0-9_.%-][A-Za-z0-9_.-]*)[ \t]*:", re.MULTILINE)


def _detect_makefile(repo):
    candidates = []
    text = _read(os.path.join(repo, "Makefile"))
    if not text:
        return candidates
    for m in _MAKE_TARGET_RE.finditer(text):
        name = m.group(1)
        if name == ".PHONY" or "%" in name:
            continue
        if name in _MAKE_ALLOWED:
            candidates.append({
                "command": f"make {name}",
                "source": "Makefile",
                "kind": _kind_from_name(name),
                "confidence": "medium",
            })
    return candidates


def _detect_justfile(repo):
    candidates = []
    for fname in ("justfile", "Justfile", ".justfile"):
        text = _read(os.path.join(repo, fname))
        if not text:
            continue
        for m in re.finditer(r"^([A-Za-z0-9_.-]+)\s*:", text, re.MULTILINE):
            name = m.group(1)
            if name in _MAKE_ALLOWED:
                candidates.append({
                    "command": f"just {name}",
                    "source": fname,
                    "kind": _kind_from_name(name),
                    "confidence": "medium",
                })
        break
    return candidates


def _detect_deno(repo):
    candidates = []
    for fname in ("deno.json", "deno.jsonc"):
        text = _read(os.path.join(repo, fname))
        if not text:
            continue
        stripped = re.sub(r"//[^\n]*", "", text)
        stripped = re.sub(r"/\*.*?\*/", "", stripped, flags=re.DOTALL)
        try:
            data = json.loads(stripped)
        except Exception:
            continue
        candidates.append({
            "command": "deno test",
            "source": fname,
            "kind": "test",
            "confidence": "medium",
        })
        for name in data.get("tasks", {}):
            if name in _MAKE_ALLOWED and name != "test":
                candidates.append({
                    "command": f"deno task {name}",
                    "source": fname,
                    "kind": _kind_from_name(name),
                    "confidence": "medium",
                })
        break
    return candidates


# Regex to detect a heredoc opener and capture its terminator word.
_HEREDOC_RE = re.compile(r"<<[-]?['\"]?([A-Za-z_][A-Za-z0-9_]*)['\"]?")


def _detect_ci(repo):
    """Extract runnable check commands from GitHub Actions workflow run: steps.

    For block run: | steps, each line passes through a strict allowlist filter:
    - heredoc bodies are skipped entirely (tracked by terminator word)
    - GitHub Actions expressions (${{...}}) are rejected
    - variable assignments, shell keywords, and control flow are rejected
    - continuation backslash lines are skipped
    - only lines whose first token is a known check runner are kept
    """
    candidates = []
    wf_dir = os.path.join(repo, ".github", "workflows")
    if not os.path.isdir(wf_dir):
        return candidates

    try:
        names = sorted(os.listdir(wf_dir))
    except OSError:
        return candidates

    for name in names:
        if not name.endswith((".yml", ".yaml")):
            continue
        text = _read(os.path.join(wf_dir, name))
        if not text:
            continue

        rel = os.path.join(".github", "workflows", name)
        source = f"ci:{rel}"
        lines = text.split("\n")
        i = 0

        while i < len(lines):
            line = lines[i]

            # ---- Block run: | (checked first so "run: |" is not captured as cmd "|") ----
            mb = re.match(r"^(\s+)run:\s*\|", line)
            if mb:
                indent = len(mb.group(1))
                i += 1
                heredoc_term = None
                prev_backslash = False
                while i < len(lines):
                    bline = lines[i]
                    # End of block: non-blank line at or shallower than run:'s indent
                    if bline.strip() and (len(bline) - len(bline.lstrip()) <= indent):
                        break
                    i += 1
                    cmd_full = bline.strip()
                    if not cmd_full:
                        prev_backslash = False
                        continue

                    # Inside a heredoc: skip until terminator line
                    if heredoc_term:
                        if cmd_full == heredoc_term:
                            heredoc_term = None
                        prev_backslash = False
                        continue

                    # Skip lines that continue the previous backslash-terminated line
                    if prev_backslash:
                        prev_backslash = cmd_full.endswith("\\")
                        continue

                    # Skip bare continuation-flag lines like -H, -d, -e
                    if re.match(r"^-[a-zA-Z]", cmd_full) and not cmd_full.startswith("--"):
                        prev_backslash = cmd_full.endswith("\\")
                        continue

                    # Detect heredoc opener (set term BEFORE candidate check so we
                    # still skip the body even when the opening line is not emitted)
                    hm = _HEREDOC_RE.search(cmd_full)
                    if hm:
                        heredoc_term = hm.group(1)

                    bare = cmd_full.rstrip("\\").strip()
                    prev_backslash = cmd_full.endswith("\\")

                    if _is_ci_candidate(bare):
                        candidates.append({
                            "command": bare,
                            "source": source,
                            "kind": _kind_from_command(bare),
                            "confidence": "high",
                        })
                continue  # skip the final i += 1 for the outer loop

            # ---- Single-line run: cmd ----
            m = re.match(r"^(\s+)run:\s+(.+)$", line)
            if m:
                cmd = m.group(2).strip()
                if _is_ci_candidate(cmd):
                    candidates.append({
                        "command": cmd,
                        "source": source,
                        "kind": _kind_from_command(cmd),
                        "confidence": "high",
                    })
                i += 1
                continue

            i += 1

    return candidates


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------

def _dedup(candidates):
    """Deduplicate by command string, keeping CI (high-confidence) entries first."""
    ordered = sorted(
        range(len(candidates)),
        key=lambda idx: (0 if candidates[idx]["confidence"] == "high" else 1, idx),
    )
    seen = set()
    result = []
    for idx in ordered:
        c = candidates[idx]
        if c["command"] not in seen:
            seen.add(c["command"])
            result.append(c)
    return result


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def detect(repo):
    """Return candidate check commands for the repo at *repo*.

    Returns an empty list (not an error) when *repo* has no recognised build
    files.  Raises no exceptions.  Never writes, runs, or fetches anything.
    """
    if not os.path.isdir(repo):
        return []

    candidates = []
    # CI first so its entries win deduplication
    candidates.extend(_detect_ci(repo))
    candidates.extend(_detect_package_json(repo))
    candidates.extend(_detect_python(repo))
    candidates.extend(_detect_cargo(repo))
    candidates.extend(_detect_go(repo))
    candidates.extend(_detect_makefile(repo))
    candidates.extend(_detect_justfile(repo))
    candidates.extend(_detect_deno(repo))

    return _dedup(candidates)


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def _format_human(candidates):
    if not candidates:
        return "no runnable checks found, so the DoD must be written by hand"

    kind_w = max(len(c["kind"]) for c in candidates) + 2  # brackets
    cmd_w = max(len(c["command"]) for c in candidates)

    lines = []
    for c in candidates:
        kind_col = f"[{c['kind']}]".ljust(kind_w)
        cmd_col = c["command"].ljust(cmd_w)
        lines.append(f"  {kind_col}  {cmd_col}  ({c['source']})")
    lines.append(f"{len(candidates)} candidate check command(s) found.")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv):
    args = argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if args else 2

    repo = args[0]
    use_json = "--json" in args

    if not os.path.isdir(repo):
        print(f"no such repo: {repo}", file=sys.stderr)
        return 2

    candidates = detect(repo)

    if use_json:
        print(json.dumps(candidates, indent=2, ensure_ascii=False))
    else:
        print(_format_human(candidates))

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
