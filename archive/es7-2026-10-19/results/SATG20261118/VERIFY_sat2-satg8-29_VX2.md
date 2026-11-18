# VERIFY sat2-satg8-29 (verifier VX2) -- CONFIRMED

**Verdict: CONFIRMED.** Claim `sat2-satg8-29` (sat_g(8) <= 29): the 29-point set `data/SAT2_k8_n29.txt` is 8-gon-saturated in the
sense of Damasdi-Dong-Scheucher-Zeng (arXiv:2312.01223). Checked 2026-11-18 08:11 KST by VX2 with its own code
(`vx2sat.cpp`, written from the definitions; no code of SAT2, vx1118 or track L was run, imported or read).
Kind of evidence: exact computation (integer / GMP rational arithmetic), independent of the finder; not a written proof.

## Counts

| item | VX2 result |
|---|---|
| point file | `data/SAT2_k8_n29.txt`, SHA-256 `9baf0cd6bce4e896fe6cdd28561e1e0feb33faf3dc7445fef68c39fd6f494544` (equals the claim) |
| (a) general position | YES (all ordered triples, exact 64-bit orientations; max abs coordinate 1,267,379) |
| (a) largest convex subset | DP over convex chains: 7; exhaustive DFS over convex subsets: 7 (needed: 7) |
| (a) convex k-subsets (DFS) | k3=3654 k4=13381 k5=17728 k6=7196 k7=792 k8=0 |
| (a) brute force (hull of every k-subset) | k=7 convex_subsets 792 (dfs 792) AGREE; k=8 convex_subsets 0 (dfs 0) AGREE |
| lines L | 406 vertical_lines 0 parallel_pairs 0 vertices 71282 point_vertices 29 max_k 28 sum_k_minus_1 72036 |
| vertex multiplicities | k2:71253 k28:29 (every point of P is a vertex with k = N - 1) |
| F = 1 + L + sum_v (k_v - 1) | 72,443 |
| edges E = sum_l (m_l + 1), Euler | E = 143,724, V - E + F = 1 (and sum_l m_l = sum_v k_v) |
| sweep self-checks | blocks_checked 71282 breakpoints 71282 vertical_breakpoints 0 final_order OK |
| samples / distinct sign vectors / F | 72443 / 72443 / 72443: CELLS_COMPLETE; exact GMP fallbacks of the double filter: 4 |
| failing cells (method A, all cells) | **0** |
| method B cross-check | 3000 random cells, agree 3000; exact signs vs filtered signs mismatches 0; max DFS nodes 3924 |
| negative control: P minus point 0 | 62532 cells, 753 failing; deleted point's cell: FOUND FAIL; method B 3728 agree 3728 |
| runtime | 1.4 s wall (one thread, unit or foreground; see log) |

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
- logs `/home/jay/research/data/roadmap-20261115/pm1115/vx2/final_sat2-satg8-29.log`, `neg_sat2-satg8-29_drop0.log`,
  `ctrl_*.log`; control sets `ctrl4.txt`, `ctrl4_tri.txt`, `ctrl5.txt` (gen5.py), `ctrl_sym12.txt` (gensym.py)
- rerun: `./vx2sat2 /home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/SATG20261118/data/SAT2_k8_n29.txt 8 -1 K 1` (K = size of the method-B sample; negative control: drop index 0 as third argument;
  exact commands in `batchS.sh` / `batchA.sh`)

## Comparison with the record (read after the check)

SAT2's record states: cells 72,443; convex 5/6/7/8-subsets 17,728/7,196/792/0. VX2's counts are equal.
