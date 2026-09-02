#!/usr/bin/env python3
"""
condition_lint.py: check a /goal condition before anyone pastes it.

goalify authors two artifacts. The brief is a file; the condition is a string. This lints
the string, mechanising the checkable half of the condition-lint checklist in
`skills/goalify/SKILL.md`.

It is a helper the skill may call, not a product. goalify remains a skill plugin with no
MCP server, no standalone CLI, no runtime dependency and no network call: this file is
standard library only and reads nothing but its own input.

Usage:
    python3 skills/goalify/scripts/condition_lint.py "<condition>"
    echo "<condition>" | python3 skills/goalify/scripts/condition_lint.py

Prints one line per rule, then a NOTE line if the condition is longer than a glance.
Exit 0 = every rule passed, 1 = at least one failed, 2 = no condition was supplied.

What it CANNOT check, and why the checklist in SKILL.md still needs a reader: whether the
named command actually proves the criterion, whether the sentinel is distinctive, whether a
clause is satisfied by the condition text itself, and whether every command in the condition
appears in the brief's definition of done. Those are judgment calls. A condition can pass
every rule here and still be a bad condition.
"""
import re
import sys

LIMIT = 4000
GLANCE = 150

# A token that begins like a filesystem path: POSIX absolute, home-relative, dot-relative,
# a Windows drive, or a UNC share.
PATH_START_RE = re.compile(r"^(?:~?/|\.{1,2}/|[A-Za-z]:[\\/]|\\\\)")
# "stop after", "or stop at", "stop once ..." all read as a stop rule.
STOP_RE = re.compile(r"\bstop(?:s|ping)?\s+(?:after|at|once|when)\b", re.IGNORECASE)
STOP_AFTER_RE = re.compile(r"\bstop\s+after\b", re.IGNORECASE)
# Matches the semantics tests/test_manifests.py already asserts on the shipped example:
# "bare" means unescaped.
BARE_DOLLAR_RE = re.compile(r"(?<!\\)\$")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def _strip_wrapping_quotes(text):
    text = text.strip()
    while len(text) >= 2 and text[0] == text[-1] and text[0] in "\"'":
        text = text[1:-1].strip()
    return text


def _last_sentence(condition):
    parts = [p for p in SENTENCE_SPLIT_RE.split(condition.strip()) if p.strip()]
    return parts[-1] if parts else ""


def lint(condition):
    """Return a list of (rule id, ok, detail). The caller decides how to report it."""
    cond = _strip_wrapping_quotes(condition)
    tokens = cond.split()
    results = []

    results.append((
        "length", len(cond) <= LIMIT,
        f"{len(cond):,} characters, limit {LIMIT:,}",
    ))

    results.append((
        "done-when", "done when" in cond.lower(),
        'the finish line has to be stated: say "done when ..."',
    ))

    # The v1 defect: a condition that IS a path. The evaluator has no file access, so a path
    # handed to /goal becomes a literal string it is asked about every turn. A path named
    # INSIDE a sentence is required, not banned: it is the first of the four teeth.
    leads_with_path = bool(tokens) and bool(PATH_START_RE.match(tokens[0]))
    whole_is_path = len(tokens) == 1 and bool(PATH_START_RE.match(cond))
    results.append((
        "path-as-condition", not (leads_with_path or whole_is_path),
        "the whole condition is a path" if whole_is_path
        else f"the condition leads with the path {tokens[0]!r}" if leads_with_path
        else "names the brief inside a sentence, not as the condition",
    ))

    unnumbered = [
        cond[m.start():m.end() + 18].strip()
        for m in STOP_AFTER_RE.finditer(cond)
        if not re.match(r"\s*\d", cond[m.end():m.end() + 20])
    ]
    results.append((
        "stop-after-number", not unnumbered,
        f'"stop after" needs a number: {unnumbered[:2]}' if unnumbered
        else "every stop-after clause carries a count",
    ))

    last = _last_sentence(cond)
    results.append((
        "stop-rule", bool(STOP_RE.search(last)),
        f"the last sentence must bound the loop, got {last[-60:]!r}",
    ))

    results.append((
        "bare-dollar", not BARE_DOLLAR_RE.search(cond),
        "a bare $ sequence can be rewritten by the hook prompt; escape or reword it",
    ))

    return results


def main(argv):
    if len(argv) > 1:
        condition = " ".join(argv[1:])
    else:
        condition = sys.stdin.read()
    if not condition.strip():
        print("FAIL: no condition supplied (pass it as an argument or on stdin)")
        return 2

    results = lint(condition)
    for rule, ok, detail in results:
        print(f"{'PASS' if ok else 'FAIL'}: {rule}  ({detail})")

    cond = _strip_wrapping_quotes(condition)
    if len(cond) > GLANCE:
        print(f"NOTE: {len(cond):,} characters. A condition reads best in one breath, around "
              f"{GLANCE}. Every clause past the four teeth is one more thing to score as unmet. "
              "This note does not fail the lint.")

    failed = [r for r, ok, _ in results if not ok]
    print("-" * 60)
    print(f"{len(results) - len(failed)}/{len(results)} rules passed")
    if failed:
        print("failed: " + ", ".join(failed))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
