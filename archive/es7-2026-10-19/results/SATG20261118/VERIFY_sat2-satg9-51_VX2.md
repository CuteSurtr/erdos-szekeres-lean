# VERIFY sat2-satg9-51 (verifier VX2) -- CONFIRMED

**Verdict: CONFIRMED.** Claim `sat2-satg9-51` (sat_g(9) <= 51): the 51-point set `data/SAT2_k9_n51.txt` is 9-gon-saturated in the
sense of Damasdi-Dong-Scheucher-Zeng (arXiv:2312.01223). Checked 2026-11-18 08:11 KST by VX2 with its own code
(`vx2sat.cpp`, written from the definitions; no code of SAT2, vx1118 or track L was run, imported or read).
Kind of evidence: exact computation (integer / GMP rational arithmetic), independent of the finder; not a written proof.

## Counts

| item | VX2 result |
|---|---|
| point file | `data/SAT2_k9_n51.txt`, SHA-256 `44710e41ebc85edecb2d15a03cf87ea8f3f3d5e8c4fc1f0ace38a397f9833fb2` (equals the claim) |
| (a) general position | YES (all ordered triples, exact 64-bit orientations; max abs coordinate 374,088) |
| (a) largest convex subset | DP over convex chains: 8; exhaustive DFS over convex subsets: 8 (needed: 8) |
| (a) convex k-subsets (DFS) | k3=20825 k4=143994 k5=406983 k6=499653 k7=259837 k8=45480 k9=0 |
| (a) brute force (hull of every k-subset) | k=8 skipped C(N,k)=636763050; k=9 skipped C(N,k)=3042312350 |
| lines L | 1275 vertical_lines 0 parallel_pairs 2 vertices 749749 point_vertices 51 max_k 50 sum_k_minus_1 752197 |
| vertex multiplicities | k2:749698 k50:51 (every point of P is a vertex with k = N - 1) |
| F = 1 + L + sum_v (k_v - 1) | 753,473 |
| edges E = sum_l (m_l + 1), Euler | E = 1,503,221, V - E + F = 1 (and sum_l m_l = sum_v k_v) |
| sweep self-checks | blocks_checked 749749 breakpoints 749749 vertical_breakpoints 0 final_order OK |
| samples / distinct sign vectors / F | 753473 / 753473 / 753473: CELLS_COMPLETE; exact GMP fallbacks of the double filter: 5 |
| failing cells (method A, all cells) | **0** |
| method B cross-check | 1000 random cells, agree 1000; exact signs vs filtered signs mismatches 0; max DFS nodes 103281 |
| negative control: P minus point 0 | 694524 cells, 231 failing; deleted point's cell: FOUND FAIL; method B 531 agree 531 |
| runtime | 112.6 s wall (one thread, unit or foreground; see log) |

## Method

- Lines: for a < b, A x + B y + C = orient(P_a, P_b, (x, y)), exact 64-bit coefficients (|coord| < 2^23 asserted, so all
  `__int128` products stay below 2^123).
- Vertices: every pair of non-parallel lines is intersected exactly; points are reduced to a canonical triple
  (x_num, y_num, d) and grouped; each group must contain exactly C(k,2) line pairs (aborts otherwise). Parallel pairs are
  counted and contribute no vertex. F = 1 + L + sum_v (k_v - 1) follows from inserting the lines one by one (a line meeting
  the earlier lines in m distinct points adds m + 1 cells; parallels add 1); it holds with parallel lines.
- Edges: each line's own crossing points are sorted along it and counted (m_l); E = sum (m_l + 1); V - E + F = 1 checked.
- Cells (not by angular sectors): a vertical sweep keeps the bottom-to-top order of the non-vertical lines (initial order
  at x -> -infinity by slope and intercept). At each vertex the lines through it must be contiguous and in descending
  slope order; the block is reversed. The final order must equal the order at x -> +infinity. A cell's leftmost piece is
  a trapezoid of the slab right of its leftmost vertex (or of the first slab, or of a vertical line); for each one the
  sample is x* = midpoint of the two neighbouring breakpoints (exact rational), y* = midpoint of the two bounding lines at
  x* (or 1 below/above for unbounded pieces), with the exact check that the lower line is below the upper one.
- Sign vector of each sample against all L lines: double evaluation with a proven error bound (2^-45 times the absolute
  sum, i.e. 32 times the worst-case rounding error), GMP evaluation whenever the bound does not decide; an exact zero would
  abort. Samples are deduplicated by the full sign vector; distinct count = number of samples = F means every cell is hit
  exactly once (distinct sign vectors are distinct cells, and there are exactly F cells).
- Method A (every cell): orient(q, a, b) is read from the sign vector. For every first vertex v1 the points of the open
  half-plane left of q -> v1 are sorted by angle around q and a DP over pairs finds the longest chain v1, c1, ... with
  left turns; q, v1, c1, ... is then a convex polygon (angles span < pi, all turns left). q is a vertex of a convex n-gon
  iff some chain has n - 1 points.
- Method B (random cells and failing cells): all orientations with q recomputed from q's exact coordinates by GMP
  (compared with the sign vector), then an exhaustive DFS over subsets of P + q containing q, kept in convex position by
  the 4-point (Caratheodory) test, searching for n points.
- Part (a): DP over convex chains above each bottom point; exhaustive DFS over all convex subsets (4-point test);
  brute force over all k-subsets for k = n - 1, n with Andrew's monotone-chain hull when run.

## Controls (same binary)

- Positive controls with known answer (every set of ES(n) - 1 points without a convex n-gon is saturated, since ES(4) = 5 and ES(5) = 9): `ctrl4.txt` (triangle + interior point, n = 4): 18 cells, 0 failing, SATURATED_SET; `ctrl5.txt` (8 points, no convex pentagon, found by VX2 hill climbing and re-checked by DFS + brute force), n = 5: 287 cells, 0 failing, SATURATED_SET.
- Negative controls with known failing cells: a bare triangle (n = 4): 4 of 7 cells fail (inside + 3 vertex regions, as expected); `ctrl5` minus point 0 / minus point 3: 10 / 22 failing cells, the cell of the deleted point fails (FOUND FAIL / FOUND FAIL).
- Degenerate-arrangement control `ctrl_sym12.txt` (12 points, 4-fold rotation symmetry, general position; lines: 66 vertical_lines 4 parallel_pairs 38 vertices 1437 point_vertices 12 max_k 11 sum_k_minus_1 1553): cells 1620 (CELLS_COMPLETE), method A and method B agree on every cell (1620; n = 7: 1116 failing).

## Files

- code `/home/jay/research/data/roadmap-20261115/pm1115/vx2/vx2sat.cpp` SHA-256 `9b243cd156a6341f190240eb95960d1d51d4f3495678b63dfe8954bdccf3a55d`
  (binary `vx2sat2`, `g++ -O2 -std=c++17 ... -lgmp`, SHA-256 `3537f4936d2efd71005cc914cf75980ef3231e33870e4c76e6b95e017397d90b`)
- logs `/home/jay/research/data/roadmap-20261115/pm1115/vx2/final_sat2-satg9-51.log`, `neg_sat2-satg9-51_drop0.log`,
  `ctrl_*.log`; control sets `ctrl4.txt`, `ctrl4_tri.txt`, `ctrl5.txt` (gen5.py), `ctrl_sym12.txt` (gensym.py)
- rerun: `./vx2sat2 /home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/SATG20261118/data/SAT2_k9_n51.txt 9 -1 K 1` (K = size of the method-B sample; negative control: drop index 0 as third argument;
  exact commands in `batchS.sh` / `batchA.sh`)

## Comparison with the record (read after the check)

SAT2's record states: cells 753,473; 1,275 lines, 2 parallel pairs, 749,749 vertices; convex 3/.../9-subsets 20,825/143,994/406,983/499,653/259,837/45,480/0. VX2's counts are equal.
