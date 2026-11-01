#!/usr/bin/env python3
"""Read-only scan for finding A1-F1 (assembled theorem missing; write-up stale on the central case).

Usage: python3 -I scan_docs.py <results_dir>

1. Prints the passages the finding cites, with line numbers, and asserts that the quoted stale phrases are there.
2. Searches every .md/.tex/.txt/.tsv file under <results_dir> for paragraphs that talk about symmetric sets of
   33-or-more points, so that a human can decide whether any of them states the assembled theorem
   ("every symmetric set of >= 33 points contains a convex 7-gon", with hypotheses C3-33, M33, M34, C5>=35, C2-34).
3. Lists every file that still calls the central 34-point case open / unsolved.
Nothing is written except to stdout.
"""
import os
import re
import sys

R = sys.argv[1]


def lines(rel):
    with open(os.path.join(R, rel), encoding="utf-8") as f:
        return f.read().split("\n")


def show(rel, a, b):
    L = lines(rel)
    print(f"--- {rel} lines {a}-{b}")
    for i in range(a, b + 1):
        print(f"{i:4d}: {L[i-1]}")


def must(rel, lineno_range, phrase):
    L = lines(rel)
    a, b = lineno_range
    text = " ".join(L[a - 1:b])
    ok = phrase in text
    print(f"[{'OK ' if ok else 'MISSING'}] {rel}:{a}-{b} contains {phrase!r}")
    return ok


print("=" * 100)
print("1. Passages cited by the finding")
print("=" * 100)
show("WRITEUP/SYMMETRIC.md", 59, 72)
show("WRITEUP/SYMMETRIC.md", 83, 83)
show("WRITEUP/SYMMETRIC.md", 181, 198)
show("WRITEUP/note/symmetric_es7.tex", 16, 27)
show("WRITEUP/note/symmetric_es7.tex", 121, 131)
show("WRITEUP/note/symmetric_es7.tex", 157, 161)
show("WRITEUP/note/symmetric_es7.tex", 242, 251)
show("C2FINAL/README.md", 5, 7)
show("C2FINAL/README.md", 163, 164)

print()
checks = [
    ("WRITEUP/SYMMETRIC.md", (59, 60), "published fourfold exclusion"),
    ("WRITEUP/SYMMETRIC.md", (63, 63), "exactly the half-turn group C2"),
    ("WRITEUP/SYMMETRIC.md", (83, 83), "at least 32; exactly 32 if ES(7) = 33"),
    ("WRITEUP/SYMMETRIC.md", (83, 83), "open (§4)"),
    ("WRITEUP/SYMMETRIC.md", (184, 185), "Excluding 34 points excludes all of them, since pairs can be deleted."),
    ("WRITEUP/SYMMETRIC.md", (194, 195), "The 8 canonical parallelogram cases are open."),
    ("WRITEUP/SYMMETRIC.md", (196, 198), "Neither closes the case."),
    ("WRITEUP/note/symmetric_es7.tex", (21, 24), "Combined with the fourfold result"),
    ("WRITEUP/note/symmetric_es7.tex", (22, 24), "centrally symmetric sets of even size at least $34$"),
    ("WRITEUP/note/symmetric_es7.tex", (122, 123), "the fourfold exclusion"),
    ("WRITEUP/note/symmetric_es7.tex", (160, 160), "$N(C_2)\\ge 32$, with $N(C_2)=32$ if $ES(7)=33$"),
    ("WRITEUP/note/symmetric_es7.tex", (244, 245), "excluding $34$ points would"),
    ("WRITEUP/note/symmetric_es7.tex", (248, 248), "The parallelogram cases are open"),
    ("C2FINAL/README.md", (6, 7), "**not yet claimed**"),
    ("C2FINAL/README.md", (163, 164), "`C2C34/README.md` and `WRITEUP/SYMMETRIC.md` still describe the parallelogram cases as open"),
]
allok = all([must(*c) for c in checks])
print("all quoted phrases present:", allok)

# What C2FINAL item 6 does NOT mention (to test the finding's 'already notes this').
item6 = " ".join(lines("C2FINAL/README.md")[162:164])
for word in ["symmetric_es7.tex", "note", "Corollary", "Cor.", "table", "N(C2)", "assembled", "theorem"]:
    print(f"C2FINAL item 6 mentions {word!r}: {word in item6}")

print()
print("=" * 100)
print("2. Paragraphs about symmetric sets of 33 or more points (candidates for an assembled theorem)")
print("=" * 100)
pat_sym = re.compile(r"symmetr", re.I)
pat_big = re.compile(r"(at least (\$)?33|33 or more|more than 33|\\ge ?33|>= ?33|of 33 points|33-point)", re.I)
pat_any = re.compile(r"(nontrivial symmetr|non-trivial symmetr|any symmetr|every symmetric|all symmetric|no symmetr|"
                     r"symmetric counterexample|symmetric route|has no symmetry|symmetric sets? of at least)", re.I)
skip_dirs = {"logs", "evidence", "cubes"}
cands = []
for root, dirs, files in os.walk(R):
    dirs[:] = sorted(d for d in dirs if d not in skip_dirs)
    for fn in sorted(files):
        if not fn.endswith((".md", ".tex", ".txt")):
            continue
        p = os.path.join(root, fn)
        try:
            txt = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
        if len(txt) > 2_000_000:
            continue
        # paragraphs = blocks separated by blank lines
        pos = 0
        for para in re.split(r"\n\s*\n", txt):
            start_line = txt.count("\n", 0, txt.find(para, pos)) + 1
            pos = txt.find(para, pos) + len(para)
            if pat_sym.search(para) and pat_any.search(para) and pat_big.search(para):
                cands.append((os.path.relpath(p, R), start_line, para))
for rel, ln, para in cands:
    print(f"### {rel}:{ln}")
    print(para.strip()[:1500])
    print()
print(f"candidate paragraphs: {len(cands)}")

print()
print("=" * 100)
print("3. Files that still call the central 34-point case open / unsolved")
print("=" * 100)
pat_open = re.compile(r"(central[^.\n]{0,60}(remains|stays|is) open|status: open|status \(open\)|"
                      r"parallelogram cases (are|is) (open|not solved)|"
                      r"centrally symmetric sets of (even size at least )?34( or more points)?[^.\n]{0,40}(open|not excluded)|"
                      r"Not excluded: centrally symmetric|N\(C_?2\)\s*\\?ge|at least 32, and exactly 32 if|"
                      r"at least 32; exactly 32 if|34-point set would refute ES\(7\) = 33; open)", re.I)
for root, dirs, files in os.walk(R):
    dirs[:] = sorted(d for d in dirs if d not in skip_dirs)
    for fn in sorted(files):
        if not fn.endswith((".md", ".tex")):
            continue
        p = os.path.join(root, fn)
        for i, line in enumerate(open(p, encoding="utf-8", errors="replace"), 1):
            if pat_open.search(line):
                print(f"{os.path.relpath(p, R)}:{i}: {line.strip()[:200]}")
