# VERIFY_LOWERBOUND_L18_SATG8_CELLS: SAT-free exhaustive cell check of claims `lb-l18-satg8-31` and `lb-l18-satg8-36` (verifier vx1118, 18 Nov 2026, 04:08-04:27 KST)

## Verdict

| claim | set (SHA-256) | (a) general position, no convex octagon | (b) geometrically octagon-saturated | label |
|---|---|---|---|---|
| lb-l18-satg8-31 | `l1118/sat31/sl31.txt` (`9982e598…7a58f8`), 31 points | **CONFIRMED** | **CONFIRMED**: 95,760 of 95,760 open cells pass | **EXACT** |
| lb-l18-satg8-36 | `l1118/sat36/g5_m7_f1_k8_s1.txt` (`90ce329a…87eca`), 36 points | **CONFIRMED** | **CONFIRMED**: 178,570 of 178,570 open cells pass | **EXACT** |

So **sat_g(8) ≤ 31** holds for these integer coordinates, by a second method that uses no SAT solver and no LRAT.
VS's CONFIRMED verdicts (SAT certificate, VERIFY_LOWERBOUND_L18_SATG8_VS1118.md and VERIFY_LOWERBOUND_L18_SATG8.md)
stand. This file is a supplement. For the 36-point set it is the third check, after VS (SAT) and VB (cells,
VERIFY_LOWERBOUND_L18_SATCELLS_VB1118.md). All code is my own. I did not read or run the claim's tools or VB's code.
I read VB's record only after my code was written and running, and used it only to compare the final counts.

The enumeration is complete and exact: integers, GMP and Python big integers / Fractions only, and no floating point
anywhere.

## Statement checked

S is a finite set of integer points and K = 8.
- (a) S is in general position and no K points of S are in convex position.
- (b) Take any point p of the plane on no line through two points of S, that is, with S ∪ {p} in general position.
  Then p is a vertex of a convex K-gon contained in S ∪ {p}.

This is DDSZ's "geometrically K-gon-saturated" (arXiv:2312.01223). Since S has no convex K-gon, a K-gon of S ∪ {p}
always has p as a vertex.

## Method

**Reduction to cells.** For each pair a < b, let L_ab(p) = orient(s_a, s_b, p). This is a linear function whose zero
set is the line ab. The points p allowed in (b) are exactly the points of the open cells (2-faces) of the arrangement
of the L = C(n,2) lines. The lines are pairwise distinct because S is in general position.

Inside one open cell, every sign of L_ab(p) is constant. The orientations inside S are fixed, so the order type of
S ∪ {p} is constant on the cell. Convex position of a set in general position is a function of its orientation signs:
a set is in convex position iff every 4-subset is (Carathéodory). Four points are in convex position iff none lies in
the triangle of the other three. Hence one exact sample per open cell decides (b).

**Number of cells.** For an arrangement of L distinct lines, not all parallel, the number of open cells is

> F = 1 + L + Σ_v (k_v − 1), where the sum runs over the vertices v (distinct intersection points) and k_v is the
> number of lines through v.

Derivation: insert the lines one at a time. A new line meets the earlier lines in m distinct points, so it is cut into
m + 1 pieces, and each piece splits one cell into two. Hence F = 1 + Σ (m_i + 1). A vertex where k_v lines meet is
counted as such a point once for each of its lines after the first, which gives k_v − 1. Parallel lines never meet and
contribute nothing; this is also correct for a line that meets no earlier line. The same value follows from Euler's
formula on the sphere with one extra vertex at infinity: E = L + Σ_v k_v and F = E − (V + 1) + 2. The k_v are computed
exactly by grouping all pairwise intersections, as reduced rationals, and each program checks Σ_v C(k_v, 2) +
(parallel pairs) = C(L, 2).

**Finder (`satcells.cpp`, C++ with `__int128` and GMP).**
1. *(a)*
   - All C(n,8) subsets are tested by brute force with the 4-subset criterion; the result is 0 in convex position.
   - All C(n,7) subsets are tested the same way, and the count equals the count of a separate pruned enumeration.
   - An O(n⁴) dynamic program finds the largest convex subset. It works from the lex-lowest vertex in angular order;
     the result is 7.
2. *Cells.* At every vertex v, the 2k_v rays of the lines through v are sorted exactly by angle. For each sector between
   consecutive rays r1 and r2 (angle < π), w = r1 + r2 lies strictly inside the sector. The cell in that sector has an
   exact sign vector:
   - for a line not through v, the nonzero sign of L(v);
   - for a line through v, the sign of ∇L·w, which is nonzero.

   Every open cell has a vertex on its boundary, because the lines are not all parallel. The deduplicated sign vectors
   must number F.
3. *Explicit sample per cell.* For each cell, the finder takes q = v + w/(D·M), where v = (X/D, Y/D) and D > 0.
   - It sets M = 1 + max ⌊|∇L·w| / |D·L(v)|⌋ over the lines whose two signs differ, so no line changes sign between v
     and q.
   - It then recomputes every orient(s_a, s_b, q) from the coordinates of q with GMP. Each must be nonzero and equal
     to the cell's sign vector.
4. *Octagon test, two methods that must agree on every cell.*
   - **Method 1, cap regions.** It enumerates all convex 7-gons T of S, in counter-clockwise order. q is placed
     between t_i and t_{i+1} iff three conditions hold: orient(t_i, t_{i+1}, q) < 0, orient(t_{i−1}, t_i, q) > 0 and
     orient(t_{i+1}, t_{i+2}, q) > 0. (Proof: these are the three new left turns, and the total turning of the
     octagon equals that of T, namely 2π.) The witness T ∪ {q} is then re-checked from the definition, with every
     4-subset in convex position.
   - **Method 2.** The same DP as in step 1, run on S ∪ {q}, using exact GMP comparisons for the position of q. The
     cell passes iff the largest convex subset has size ≥ 8.
   - A failing cell is re-checked against every convex 7-gon of S, from the definition. The first three failing
     cells of a run are also brute-forced against all C(n,7) subsets of S.

**Trusted replay (`check_cells.py`, separate code, Python integers and Fractions).** It reads only the point set, K
and the finder's sample file (QX QY QD plus the claimed witness). It then recomputes:
- general position of S, and the largest convex subset of S by its own DP (must be 7);
- F, from its own exact intersection points (Fractions);
- for every sample, all C(n,2) orientations with q, which must all be nonzero, so S ∪ {q} is in general position;
- that the sign vectors are pairwise distinct and that there are exactly F of them;
- for every sample marked "pass", the witness T ∪ {q}, by an exact monotone-chain convex hull that must have 8
  vertices;
- for samples marked "fail" (up to 300 per run), the largest convex subset of S ∪ {q} by the DP, which must be < 8.

Why this replay alone proves (b):
- Two points with the same nonzero sign vector lie in the same open cell. The cell is an intersection of open
  half-planes, hence convex, so the segment between the two points crosses no line.
- So F pairwise distinct, nonzero, realized sign vectors meet F distinct open cells. There are exactly F cells, so
  every cell contains a sample.
- Every sample has a verified convex octagon through it.

This argument does not depend on the finder's sector enumeration or on the cap lemma.

## Results

| set | n | lines | parallel pairs | vertices (at points of S, k) + (other, k) | Σ(k_v − 1) | F = Euler count | sector samples (Σ 2k_v) | distinct cells | pass | fail | convex 3/4/5/6/7/8-subsets | max sample bits / max M | C++ / Python (s, at 40 % CPU) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| sl31 | 31 | 465 | 0 | 31 (k=30) + 94,395 (k=2) = 94,426 | 95,294 | **95,760** | 379,440 | **95,760** | **95,760** | **0** | 4,495 / 17,915 / 26,021 / 11,050 / 1,295 / **0** | 61 / 8,031 | 7.3 / 15 |
| g5_m7_f1_k8_s1 | 36 | 630 | 0 | 36 (k=35) + 176,715 (k=2) = 176,751 | 177,939 | **178,570** | 709,380 | **178,570** | **178,570** | **0** | 7,140 / 33,270 / 58,922 / 36,140 / 6,065 / **0** | 73 / 4,280 | 19.1 / 40 |

- Both programs give identical numbers for both sets. The two methods of the finder agree on every cell (0
  mismatches). The Python replay verified all 95,760 and 178,570 witnesses, with 0 bad samples.
- The two arrangements are simple away from S. There are no parallel pairs and no point outside S on three lines, so
  F = 1 + L + n(n−2) + 3·C(n,4).
- The convex-subset counts equal VS's (4,495/17,915/26,021/11,050/1,295 and 7,140/33,270/58,922/36,140/6,065, with 0
  octagons). For the 36-point set, the cell and vertex counts equal VB's (178,570 cells, 176,751 vertices).

## Controls (same code, same unit)

| control | K | why | cells = Euler | pass | fail | check of the failures |
|---|---|---|---|---|---|---|
| sl31 minus point 0 (the centre (0,0)) | 8 | negative | 83,491 | 82,285 | **1,206** | C++: all 1,206 against all 875 convex 7-gons, 3 brute-forced over all C(30,7); both methods agree. Python DP: 300 of 1,206 confirmed (cap 300) |
| sl31 minus point 11 (−443467, −107068) | 8 | negative | 83,491 | 83,392 | **99** | Python DP: all 99 confirmed |
| g5_m7_f1_k8_s1 minus point 35 (the centre) | 8 | negative | 158,831 | 158,710 | **121** | Python DP: all 121 confirmed |
| convex pentagon (0,0),(10,0),(13,9),(5,15),(−3,9) | 6 | negative, known answer | 38 (3 parallel pairs, five 4-line points) | **5** (the five regions beyond one edge) | 33 | Python DP: all 33 confirmed |
| `F/data/sym16/m4/model1.pts`, 16 points, no convex hexagon | 6 | positive by theorem (ES(6) = 17, Szekeres-Peters) | 5,728 (56 parallel pairs, one 8-line point) | 5,728 | 0 | n/a |
| `F/data/sym16/m5/model239.pts`, 16 points, no convex hexagon | 6 | positive by theorem | 5,802 (1 parallel pair, two 3-line points) | 5,802 | 0 | n/a |
| `l1118/sat14/r_g2_m7_f0_k6_s13.txt` (claim lb-l18-satg6-14) | 6 | positive (confirmed claim) | 3,206 (42 parallel pairs, one 7-line point) = track L's 3,206 | 3,206 | 0 | n/a |
| `l1118/sat21/g5_m4_f1_k7_s2.txt` (claim lb-l18-satg7-21) | 7 | positive (confirmed claim) | 18,565 = VB's 18,565 | 18,565 | 0 | n/a |

What the controls show:
- The code finds failing cells when they exist. Deleting one point of either claimed set destroys saturation.
- The Euler formula, the sector enumeration and the replay also hold for arrangements with many parallel pairs and
  with points where many lines meet.

## Files and hashes

W = `/home/jay/research/data/roadmap-20261115/pm1115/vx1118/` (all SHA-256 in `W/SHA256SUMS`).

| file | SHA-256 |
|---|---|
| `W/satcells.cpp` (finder; `g++ -O2 -std=c++17 -o satcells satcells.cpp -lgmpxx -lgmp`, g++ 15.2) | `9a7b4d9ef1dbff3cf0a7f7addefef88eed0779a4c54f25629727b2f0fad1d891` |
| `W/satcells` (binary used) | `a0495961c2c86498427804d958b2d51ca1f65d110be866b469dfe0cdae36b09f` |
| `W/check_cells.py` (trusted replay) | `4b6cd648dcf88941238846842c86c9356b71589b992ab90afa449a15ca71072d` |
| `W/run_all.sh` (driver) | `ee7a28551f1e117763060568503c6b7b8429b8d73ae88cd2f50efba5216a45f2` |
| `W/sl31.txt` (copy of the claimed 31-point set) | `9982e59864204632c46eeec7ccd3860e471efd5c242e1d052c068717fb7a58f8` |
| `W/g5_m7_f1_k8_s1.txt` (copy of the claimed 36-point set) | `90ce329afdaa4f99784cf05a555db4e8014988d5b18f9be04b70ba12e2287eca` |
| `W/samples/main_sl31.samples.txt` (95,760 samples with witnesses, 6.6 MB) | `b4978f779b3217c54eccf5fedc11d617f81a65ed0757add1f4916dc5ff4a1206` |
| `W/samples/main_s36.samples.txt` (178,570 samples with witnesses, 14 MB) | `b56c5c07f69b19e51adca02c1695a2d31c0cba006af08d317d04e0b0221cb9ec` |
| `W/status.jsonl` (one line per run) | `3bff2a5f4e4e4fa07caf378633045025141bfa39256f20e69a5889d98e818cd4` |

Logs are in `W/logs/<run>.{cpp,py}.log`, control inputs in `W/ctl_*.txt` and control samples in `W/samples/`.

## Runtime

- One systemd user unit, `esr-mainv-sat31cells`, with CPUQuota 40 %, MemoryMax 1500M, MemorySwapMax 0 and
  RuntimeMaxSec 10800.
- It ran from 04:21:08 to 04:24:09 KST and stopped by itself: 72.5 s CPU in total, 191.7 MB memory peak.
- Earlier foreground tests on the 16-point and pentagon controls took under 1 s each.

## Not checked

- The SAT certificate, the l1enc encoding and the realizability clauses. VS checked them; I did not repeat that.
- How the sets were found: the local search, the Z[ζ₅] rounding and the symmetry statements. Saturation is claimed
  only for the integer coordinates, and that is what was checked.
- The claim's random-point sanity sampling. The exhaustive check supersedes it.
- Literature and novelty of sat_g(8) ≤ 31, including the comparison with DDSZ Thm 4's 56.
- Points p on a line through two points of S. The definition excludes them.

## Re-run

```bash
cd /home/jay/research/data/roadmap-20261115/pm1115/vx1118
g++ -O2 -std=c++17 -o satcells satcells.cpp -lgmpxx -lgmp
./satcells sl31.txt 8 samples/main_sl31.samples.txt            # ~7 s
~/research/data/six10-linux-20261105/venv.disk/bin/python -I check_cells.py sl31.txt 8 samples/main_sl31.samples.txt
# all ten runs (main sets and controls), about 3 min at 40 % CPU:
systemd-run --user --unit=esr-mainv-sat31cells -p CPUQuota=40% -p MemoryMax=1500M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=10800 --nice=10 --working-directory=$PWD /bin/bash run_all.sh
```
