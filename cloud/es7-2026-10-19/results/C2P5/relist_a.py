#!/usr/bin/env python3
"""Rewrite lists/C2P5A.tsv for the next K machines of list A (M<j0>..M<j0+K-1>, prompts with N = 37) when only some
cloud sandboxes are free: run mklist5.py with N = K on the current records, leaving out the units in the units.tsv of
every C2P5 machine that has started (and the P1-P3 quadrilateral units of exclude_AC.txt), and renumber the rows so that
shard j of the K-machine list becomes residue j0 + j modulo 37. Earlier machines keep the units they copied at start.
usage: relist_a.py RESULTS_DIR K J0 CASE...   (writes RESULTS_DIR/C2P5/lists/C2P5A.tsv; prints the mklist5 summary)"""
import glob, os, subprocess, sys
R, K, J0, cases = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4:]
here = os.path.dirname(os.path.abspath(__file__))
running = set()
for p in glob.glob(f"{R}/C2P5/M*/units.tsv"):
    running |= {l.split("\t")[1] for l in list(open(p))[1:] if l.strip()}
excl = f"{R}/C2P5/lists/exclude_next.txt"
with open(excl, "w") as f:
    for u in sorted(running | {l.strip() for l in open(f"{R}/C2P5/lists/exclude_AC.txt") if l.strip()}): f.write(u + "\n")
tmp = f"{R}/C2P5/lists/.next.tsv"
print(subprocess.run([sys.executable, f"{here}/mklist5.py", R, tmp, str(K), "--exclude", excl, *cases],
                     capture_output=True, text=True, check=True).stdout, end="")
rows = [l.rstrip("\n").split("\t") for l in list(open(tmp))[1:]]
with open(f"{R}/C2P5/lists/C2P5A.tsv", "w") as f:
    f.write("idx\tunit\tcase\tkind\tcap_s\n")
    for idx, u, c, k, cap in rows:
        j, m = int(idx) % K, int(idx) // K
        f.write(f"{J0 + j + 37 * m}\t{u}\t{c}\t{k}\t{cap}\n")
os.remove(tmp)
print(f"rewrote C2P5A.tsv for M{J0:02d}..M{J0 + K - 1:02d}: {len(rows)} rows, excluded {len(running)} units of started machines")
