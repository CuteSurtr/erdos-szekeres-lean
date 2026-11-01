"""Check the k = 10 instance (../k10_points.txt) with the review's own code only; the file is read as data.

- (H0)-(H5) of Lemma 3 and general position: rhyp.check (exact integers and fractions).
- Largest convex subset (cup+cap DP and angular DP) and the number of convex subsets of each size (cup x cap
  counting DP): refdp.c, run on an exact orientation-sign table written by refdp_io.write_table.
Written when the directory was assembled (1 November 2026, UTC); the same checks as check_author_files.py, which
covers k = 6 and k = 8, with the C port in place of the Python DPs because of the size.
Usage: python3 check_author_k10.py PATH_TO_k10_points.txt   (needs ./refdp compiled from refdp.c)
"""
import os
import sys
from rg import read_points
from rhyp import check
from rconstruct import base_abscissae
from refdp_io import run_c

HERE = os.path.dirname(os.path.abspath(__file__))
path = sys.argv[1]
k = 10
n = k - 2
rows = read_points(path)
cl = [[] for _ in range(n + 1)]
for (x, y, j) in rows:
    cl[j].append((x, y))
pts = [(x, y) for (x, y, j) in rows]
S = set(pts)
sym = all((-x, -y) in S for (x, y) in pts)
csym = all(set((-x, -y) for (x, y) in cl[j]) == set(cl[n - j]) for j in range(n + 1))
rep = check(cl, k, base_abscissae(k))
print("%s k=%d N=%d distinct=%s sym=%s clustersym=%s sizes=%s 0notin=%s" %
      (os.path.basename(path), k, len(pts), len(S) == len(pts), sym, csym, [len(B) for B in cl], (0, 0) not in S))
print("   hyp:", {h: rep[h] for h in ['H0', 'H1', 'H2', 'H3', 'H4', 'H5', 'GP', 'ALL']},
      "H3cnt", rep['H3_count'], "H4cnt", rep['H4_count'], "H5", rep['H5_detail'])
sys.stdout.flush()
tab = os.path.join(HERE, "k10_author_tab.bin")
print("   refdp:", run_c(pts, tab, counts=True))
os.remove(tab)
