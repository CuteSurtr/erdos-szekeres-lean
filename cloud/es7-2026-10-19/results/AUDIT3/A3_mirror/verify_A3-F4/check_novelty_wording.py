#!/usr/bin/env python3
"""Verify finding A3-F4 (bare novelty word in the Theorem 2b heading of SYMMETRIC.md).

Read-only: opens files under the repository worktree and git objects, writes nothing there.
Checks:
  1. SYMMETRIC.md line 53 is the Theorem 2b heading and contains the bare word "new".
  2. Every whole-word "new" in SYMMETRIC.md, classified by what it qualifies.
  3. The Scope paragraph's defined phrase ("No matching prior result found") is used
     anywhere else in the body of SYMMETRIC.md (if not, its disclaimer does not literally
     cover the heading's "new").
  4. The other statements of the same theorem (LaTeX note thm:M34, SYMZ/README.md) do or
     do not carry a novelty word.
  5. The project's own wording rules (LIT/TASK.md; MIRROR.md model phrasing) exist.
  6. The commit that introduced the heading, and whether the axis-free case was open before.
"""
import os
import re
import subprocess
import sys

R = os.path.abspath(os.environ.get("ES7_RESULTS", "."))
W = os.path.normpath(os.path.join(R, "..", "..", ".."))  # repository root
SYM = R + "/WRITEUP/SYMMETRIC.md"
TEX = R + "/WRITEUP/note/symmetric_es7.tex"
SYMZ = R + "/SYMZ/README.md"
LITTASK = R + "/LIT/TASK.md"
MIRROR = R + "/WRITEUP/MIRROR.md"

ok = True


def read_lines(p):
    with open(p, encoding="utf-8") as f:
        return f.read().split("\n")


def check(cond, msg):
    global ok
    print(("PASS " if cond else "FAIL ") + msg)
    ok = ok and cond


sym = read_lines(SYM)

# 1. line 53
l53 = sym[52]
print("line 53:", l53)
check(l53.startswith("**Theorem 2b"), "line 53 is the Theorem 2b heading")
check(re.search(r"\bnew\b", l53) is not None, "line 53 contains the bare word 'new'")
check("no matching" not in l53.lower(), "line 53 does not use the convention phrase")

# 2. every whole-word 'new' in SYMMETRIC.md
print("\nwhole-word 'new' in SYMMETRIC.md:")
for i, line in enumerate(sym, 1):
    if re.search(r"\bnew\b", line, re.I):
        print(f"  {i}: {line.strip()}")

# 3. uses of the defined phrase outside the Scope paragraph (lines 10-12)
uses = [i for i, line in enumerate(sym, 1)
        if "no matching" in line.lower() and not (10 <= i <= 12)]
print("\nuses of 'No matching ...' outside the Scope paragraph:", uses)
check(len(uses) == 0, "the defined phrase is never used in the body (disclaimer covers no actual statement)")
scope = " ".join(sym[9:12])
check("not a claim of priority" in scope, "Scope paragraph disclaims priority only for the defined phrase")
check(re.search(r"\bnew\b", scope, re.I) is None, "Scope paragraph does not mention the word 'new'")

# 4. other statements of the same theorem
tex = read_lines(TEX)
m34 = [i for i, line in enumerate(tex, 1) if "thm:M34" in line and "label" in line]
check(len(m34) == 1, f"LaTeX note has one thm:M34 statement (line {m34})")
if m34:
    block = " ".join(tex[m34[0] - 1:m34[0] + 2])
    check(re.search(r"\bnew\b", block, re.I) is None, "LaTeX thm:M34 statement carries no 'new'")
symz = read_lines(SYMZ)
t2b = [i for i, line in enumerate(symz, 1) if line.startswith("**Theorem 2b")]
check(len(t2b) == 1, f"SYMZ/README.md states Theorem 2b once (line {t2b})")
if t2b:
    check(re.search(r"\bnew\b", symz[t2b[0] - 1], re.I) is None, "SYMZ/README.md Theorem 2b carries no 'new'")

# 5. project wording rules
lit = "\n".join(read_lines(LITTASK))
check("never claim priority or novelty" in lit, "LIT/TASK.md contains the rule 'never claim priority or novelty'")
mir = "\n".join(read_lines(MIRROR))
check("No priority is claimed" in mir and "We did not find prior work stating" in mir,
      "MIRROR.md uses the model wording ('We did not find prior work stating ...; No priority is claimed')")

# 6. history
def git(*args):
    return subprocess.run(["git", "-C", W, "--no-pager", *args], capture_output=True, text=True).stdout

F = "cloud/es7-2026-10-19/results/WRITEUP/SYMMETRIC.md"
first = None
for line in reversed(git("log", "--format=%h", "--", F).split()):
    if "Theorem 2b (34 points" in git("show", f"{line}:{F}"):
        first = line
        break
print("\nfirst commit with the Theorem 2b heading:", first)
print("  subject:", git("log", "-1", "--format=%s", first).strip() if first else None)
if first:
    parent = git("rev-parse", f"{first}^").strip()
    before = git("show", f"{parent}:{F}")
    open_before = "That needs a mirror set of 34" in before or "mirror sets with no point on the axis" in before
    check(open_before, "before that commit the axis-free 34-point mirror case was listed as open")

print("\nALL CHECKS PASS" if ok else "\nSOME CHECKS FAILED")
sys.exit(0 if ok else 1)
