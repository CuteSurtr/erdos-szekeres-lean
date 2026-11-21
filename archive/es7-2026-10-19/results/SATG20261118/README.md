# SATG20261118: small n-gon-saturated point sets (saturation numbers sat_g(n), DDSZ definition)

**Current best (22 Nov 2026): sat_g(6) ≤ 11, sat_g(7) ≤ 16, sat_g(8) ≤ 26, sat_g(9) ≤ 39, sat_g(10) ≤ 52, all EXACT for
the stated coordinates. The 11, 26 and 39 are in the SAT4 addendum at the end; the sections in between keep the
values of their own runs.**

Track SAT2, 18 Nov 2026, 04:45-07:40 KST (all SAT2 units stopped by 07:40; track L's units untouched). Builds on track L's item (1c) of
[LOWERBOUND_RUN_1118.md](../ROADMAP20261115/LOWERBOUND_RUN_1118.md) and on the verifier note
[VERIFY_LOWERBOUND_L18_SATG8_CELLS.md](../ROADMAP20261115/VERIFY_LOWERBOUND_L18_SATG8_CELLS.md). No existing record was
changed.

**Independent verification (added by the main session, 08:15 KST):** all 12 claims `sat2-*` were **CONFIRMED** by
verifier VX2 with its own code (`pm1115/vx2/vx2sat.cpp`, SHA-256 `9b243cd1…3a55d`; a vertical-sweep cell enumeration,
not the angular-sector method of the finder; exact signs with a proven float filter and GMP fallback; cells = Euler
count; every cell on a convex n-gon by a DP and, on samples and all control failures, by exhaustive search; for the
48-point set also brute force over all C(48,8) and C(48,9) subsets: 0 convex 9-subsets). Verify files
`VERIFY_<claim id>_VX2.md` in this folder; verdict files `pm1115/claims/<id>.verdict.json`. So each bound below rests
on two independent exact implementations.

## 1. Headline (status: final for this run, 07:40 KST; all labels below are for the stated integer coordinates)

| n | best set here | label of that set | DDSZ Thm 4 (n ≥ 7): 7/8 · 2^(n−2) | ES(n) − 1 = ram_g(n) |
|---|---|---|---|---|
| 6 | **12** (new tonight, track SAT2; 13 before) | **EXACT** (cell enumeration, finder + trusted replay); claims `sat2-satg6-12`, `sat2-satg6-13` | none (theorem is for n ≥ 7; their block method gives 16 at n = 6) | 16 (Szekeres–Peters) |
| 7 | **16** (track L's local search, 04:56, found unclaimed in `results3.jsonl` and checked here; SAT2's own best 18, then 19; 20 before) | **EXACT** (claim `sat2-satg7-16`, set by track L; SAT2's `sat2-satg7-18`, `-19`); the 20-point sets are CERTIFIED (`lb-l18-satg7-20`, VB CONFIRMED) + EXACT (re-run here) | 28 | ≥ 32 (= 32 if ES(7) = 33) |
| 8 | **27** (new tonight, track SAT2; then 28, 29, 30; 31 before, track L) | **EXACT** (claims `sat2-satg8-27`, `-28`, `-29`, `-30`); the 31-point set is CERTIFIED (`lb-l18-satg8-31`, VS CONFIRMED) + EXACT (vx1118) | 56 | ≥ 64 (= 64 if ES(8) = 65) |
| 9 | **48** (new tonight, track SAT2; then 51; 58 first) | **EXACT** (claims `sat2-satg9-48`, `-51`, `-58`; part (a) without the C(n,9) brute force, see section 5) | 112 | ≥ 128 (= 128 if ES(9) = 129) |

So, for these exact integer coordinates: **sat_g(6) ≤ 12**, **sat_g(7) ≤ 16**, **sat_g(8) ≤ 27**, **sat_g(9) ≤ 48**. The bounds are upper bounds
on sat_g by explicit sets. Nothing about ES(n) follows. "New" means only "not found in this search" (section 8).

## 2. Definitions (DDSZ, arXiv:2312.01223, SoCG 2024, EJC 2026)

- A finite planar set P in general position is **n-gon-saturated** if no n points of P are in convex position, while
  every point q ∉ P with P ∪ {q} in general position is a vertex of a convex n-gon contained in P ∪ {q}.
- sat_g(n) = the smallest size of an n-gon-saturated set; ram_g(n) = the largest size of an n-gon-free set in general
  position = ES(n) − 1. A maximum n-gon-free set is saturated, so sat_g(n) ≤ ram_g(n).
- DDSZ Thm 4: sat_g(n) ≤ 7/8 · 2^(n−2) for n ≥ 7 (28, 56, 112 for n = 7, 8, 9). Trivially sat_g(n) ≥ n − 1.
- Saturation is a property of the coordinates, not of the order type (track L, item (1b), claim
  `lb-l18-oct56-real`); every claim here is about the stated integer coordinates.

## 3. Model and soundness of the two checks

**(I) SAT certificate route (track L's sets only; CERTIFIED + PROVED soundness).** `l1enc S K` encodes "a new point p
with S ∪ {p} in general position and no convex K-gon through p" over the signs of orient(a, b, p) for all pairs of S;
realizability clauses (each forbids a sign pattern on three lines whose open half-planes have empty intersection,
checked exactly by Motzkin multipliers and by exact sampling) are added until UNSAT; cake_lpr prints exactly one
`s VERIFIED UNSAT`. Soundness: ABSAT8 sec. 3 and LOWERBOUND_RUN_1118 (1b)/(1c); claims confirmed by VS/VB (verdict
files in `pm1115/claims/`). Not re-run here.

**(II) Exact cell enumeration (all sets; EXACT, no SAT solver).**
- The admissible points q are exactly the points of the open cells (2-faces) of the arrangement of the L = C(|S|, 2)
  lines through two points of S: q ∪ S is in general position iff q is on none of these lines.
- **One sample per open cell suffices.** On an open cell C every orient(a, b, q) has a constant nonzero sign (C is
  connected and meets no line ab). The orientations inside S are fixed, so the order type of S ∪ {q} is constant on C.
  Convex position of a set in general position depends only on its orientation signs (a set is in convex position iff
  every 4-subset is; four points are in convex position iff none lies in the triangle of the other three). So "q is a
  vertex of a convex K-gon of S ∪ {q}" is constant on C, and one exact sample per cell decides saturation.
- **Completeness of the cell list.** The number of open cells is the Euler count F = 1 + L + Σ_v (k_v − 1) over the
  distinct vertices v of the arrangement, k_v = number of lines through v (insert the lines one by one: a line meeting
  earlier lines in m distinct points adds m + 1 cells). The trusted replay `check_cells.py` (Python integers and
  Fractions only) recomputes F from its own exact intersection points, recomputes for every sample all C(|S|, 2)
  orientations (all nonzero), checks that the F sign vectors are pairwise distinct (two samples with equal sign
  vectors lie in the same convex cell), so the F samples meet all F cells, and re-checks every claimed witness
  (T ∪ {q} has K hull vertices, exact monotone chain). It also recomputes general position and the largest convex
  subset of S (DP; must be K − 1).
- The finder `satcells.cpp` (C++, `__int128` + GMP; verifier vx1118's code, unchanged copy) produces the samples by
  sector enumeration at every vertex and tests each cell by two methods that must agree (cap regions of the convex
  (K−1)-gons of S, and a DP on S ∪ {q}). The replay alone proves the claim; the finder only supplies samples and
  witnesses.
- A set gets the label EXACT here only if: finder `cells = F_euler`, `fail = 0`, `mismatch = 0`, and replay
  `cells = F`, `fail = 0`, `bad = 0`, verdict SATURATED, for the file whose SHA-256 is listed.

## 4. Method of search (HEURISTIC; not part of any proof)

`tools/satls.cpp` (own code, track SAT2; finder only). Objective: the number of open cells whose sample is not a
vertex of a convex K-gon of S ∪ {q}.
- **Cells, one per cell, no deduplication.** With the symbolic "up" direction (ε, 1), every cell bounded below has a
  unique lowest vertex v and lies in one of the k_v − 1 upper sectors at v; the L + 1 cells unbounded below are
  sampled on a far line (long double). Each vertex is visited once, along the lowest-index line through it: the
  sign vector of all lines is updated combinatorially while walking along that line (crossings sorted exactly with
  `__int128` rationals; the line crossed flips its sign), and the signs of the lines through v are set from the
  sector direction w = d_j + d_{j+1} (exact integers). So the sign vector of every bounded-below cell is exact and
  the cell count equals the Euler count also for non-simple arrangements.
- **K-gon test per cell.** An exact DFS over convex chains from each lowest vertex lists the convex (K−1)-gons (and
  detects a K-gon). q fits between consecutive vertices a, b of such a polygon with predecessor p and successor r iff
  orient(a, b, q) < 0, orient(p, a, q) > 0, orient(b, r, q) > 0; these are indexed as bitsets over (a, b) → p → r.
- **Controls against vx1118's exact counts** (all equal): sl31 0 of 95,760; sl31 − p0 1,206 of 83,491; sl31 − p11 99
  of 83,491; s36 − centre 121 of 158,831; sat21 (K = 7) 0 of 18,565; sat14 (K = 6) 0 of 3,206 (non-simple); the two
  16-point hexagon-free sets 0 of 5,728 and 0 of 5,802 (non-simple); pentagon (K = 6) 33 of 38. Speed: 0.02 s for 31
  points at K = 8, 0.36 s for 58 points at K = 9.
- **search** (`satls search`): delete the point whose deletion leaves the fewest failing cells (ties random); then move
  one point at a time (integer Gaussian moves, log-uniform scale between diameter/3 and diameter/3,000; half the moves
  pick one of the 8 points nearest a random failing sample); accept if the set stays in general position and
  K-gon-free (exact) and the count does not grow (uphill with probability exp(−Δ/0.7)); after 1,500 iterations without
  progress either reset to the best state or **kick** (add the best of up to 8 valid rounded failing samples, then
  delete the best other point); after a hit, delete again (descend).
- **grow** (`satls grow`): add points one at a time into failing cells (best of up to 8 valid rounded candidates by
  the resulting count; coordinates multiplied by 4 when no rounded candidate is valid) until no cell fails; a valid
  added point never creates a K-gon, so the end state is a saturated (maximal K-gon-free) set.
- **multigrow** (`satls multigrow`): grow from random seeds of 2(K − 1) points; statistics only.
- Every hit is then checked by (II) before anything is claimed (`verify.sh`).

## 5. Results

### n = 6: sat_g(6) ≤ 12 (EXACT)

`data/SAT2_k6_n12.txt` (12 points, SHA-256 `61075bde…3ccc`), found 05:09 KST by satls (unit esr-sat-k6b, seed 25) from the
best 12-point state of the first run (L's 14-point set minus one point, then the 13-point set below minus one point):
(−1038, 2084), (−513, 821), (6199, −517), (−2935, 5475), (−12, −201), (905, 284), (−28, −3826), (827, −1718),
(−24552, −9847), (2646, −80), (−205, 107), (−253, −1974). Finder: general position, convex 3/4/5/6-subsets
220 / 216 / 48 / **0** (brute force and DP: largest 5); cells = F_euler = **1,672** (simple: 1 + 66 + 12·10 + 3·C(12,4));
pass 1,672, **fail 0**, mismatch 0. Replay: cells 1,672, pass 1,672, **fail 0, bad 0**, SATURATED. Claim `sat2-satg6-12`.

The first hit, 13 points (claim `sat2-satg6-13`, filed 05:06 although its JSON says 05:10):

`data/SAT2_k6_n13.txt` (13 integer points, |coordinates| < 4000), found at 04:52 KST by satls (seed 13) after 7 s
from L's 14-point set minus point 11 (61 failing cells at the start; points 4 and 11 tie): (−772, 1559), (−524, 905), (2556, 140),
(−1501, −85), (−1389, 2375), (72, −179), (200, 346), (345, −1977), (589, −877), (−3532, −49), (1862, 188),
(−245, 200), (−111, −502).

| check | result |
|---|---|
| finder satcells K = 6 | general position; convex 3/4/5/6-subsets 286 / 359 / 78 / **0** (brute force and DP: largest 5); cells = F_euler = **2,367** (simple arrangement: 1 + 78 + 13·11 + 3·C(13,4)); pass 2,367, **fail 0**, mismatch 0 |
| trusted replay check_cells.py | cells 2,367, pass 2,367, **fail 0, bad 0**, verdict SATURATED |

### n = 7: sat_g(7) ≤ 16 (EXACT; set found by track L)

Reading L's running units (as asked) showed `"result": "SATURATED", "n": 16` for tag `k7_20s8_d4` in
`l1118/satlocal/results3.jsonl` (04:56 KST, unit esr-agl-satlocal3b: L's 4-fold 20-point set `r6_g4_m5_f0_k7_s8`
minus orbit 4, then `satlocal.py` on the orbit representatives; L's geosat56 CEGAR returned UNSAT, nothing certified
and no claim filed by L; L's record does not mention it). The set `l1118/satlocal/k7_20s8_d4/hit515.txt` (= `cur.txt`),
copied as `data/L_k7_n16_satlocal_k7_20s8_d4.txt` (16 points, |coordinates| ≤ 979,301, SHA-256 `00b25ba9…a7f1`), passed
the exact check here (07:31): finder: convex 3/4/5/6/7-subsets 560 / 968 / 408 / 90 / **0** (DFS = brute force; DP
largest 6); cells = F_euler = **5,728** (non-simple: 56 parallel pairs and one point where 8 lines meet, the 4-fold structure); pass 5,728, **fail 0**,
mismatch 0. Replay: cells 5,728, pass 5,728, **fail 0, bad 0**, SATURATED. Filed as claim `sat2-satg7-16` (filed by
SAT2, crediting track L; it rests only on this exact check). Two 10-min SAT2 descents from it (units esr-sat-k7L1,
-k7L3, 07:33-07:43) are reported in section 9.

SAT2's own best at n = 7 is 18:


`data/SAT2_k7_n18.txt` (18 points, |coordinates| ≤ 47,486, SHA-256 `d1e26689…f4cd`), found 06:07 KST by unit esr-sat-k7f
(seed 42, with kicks) from the 19-point set below minus point 8 (best deletion), after about 50 min at 4 % CPU.
Finder: convex 3/4/5/6/7-subsets 816 / 1,708 / 1,062 / 167 / **0** (DFS = brute force; DP largest 6); cells = F_euler =
**9,622** (simple: 1 + 153 + 18·16 + 3·C(18,4)); pass 9,622, **fail 0**, mismatch 0. Replay: cells 9,622, pass 9,622,
**fail 0, bad 0**, SATURATED. Claim `sat2-satg7-18`.

The 19-point set (claim `sat2-satg7-19`):

`data/SAT2_k7_n19.txt` (19 points, |coordinates| ≤ 37,386, SHA-256 `47993354…34a8`), found 05:35 KST. How (HEURISTIC):
L's 20-point set `r6_g4_m5_f0_k7_s9` minus point 11 (58 failing cells; points 1, 6, 11, 16 tie; random tie break), satls seed 24 (unit
esr-sat-k7c) down to 2 failing cells, coordinates multiplied by 64 (finer integer moves), seed 31 (esr-sat-k7d), then
seed 42 with kicks (esr-sat-k7f): 0 failing cells 39 s after a kick (add a point in a failing cell, delete the best
other point). Finder: convex 3/4/5/6/7-subsets 969 / 2,158 / 1,495 / 291 / **0** (DFS = brute force; DP largest 6);
cells = F_euler = **12,123** (simple: 1 + 171 + 19·17 + 3·C(19,4)); pass 12,123, **fail 0**, mismatch 0. Replay: cells
12,123, pass 12,123, **fail 0, bad 0**, SATURATED. Claim `sat2-satg7-19`.

### n = 8: sat_g(8) ≤ 27 (EXACT)

`data/SAT2_k8_n27.txt` (27 points, |coordinates| ≤ 5,865,715 < 2^23, SHA-256 `a2116a7b…2097`), found 05:52 KST by unit
esr-sat-k8i (seed 91) from the 28-point set below minus point 10 (best deletion: 166 failing cells), 12.5 min at 4 %
CPU. Finder: convex 3/4/5/6/7/8-subsets 2,925 / 9,866 / 12,127 / 5,051 / 612 / **0** (DFS = brute force; DP largest 7);
cells = F_euler = **53,677** (simple: 1 + 351 + 27·25 + 3·C(27,4)); pass 53,677, **fail 0**, mismatch 0. Replay: cells
53,677, pass 53,677, **fail 0, bad 0**, SATURATED. Claim `sat2-satg8-27`.

The 28-point set (claim `sat2-satg8-28`):

`data/SAT2_k8_n28.txt` (28 points, |coordinates| ≤ 2,497,997 < 2^22, SHA-256 `074addb0…fcb4`), found 05:38 KST by unit
esr-sat-k8f (seed 41) from the 29-point set below minus one point (best deletion by scan: 198 failing cells). Finder: convex
3/4/5/6/7/8-subsets 3,276 / 11,417 / 14,250 / 5,699 / 666 / **0** (DFS = brute force; DP largest 7); cells = F_euler =
**62,532** (simple); pass 62,532, **fail 0**, mismatch 0. Replay: cells 62,532, pass 62,532, **fail 0, bad 0**, SATURATED.
Claim `sat2-satg8-28`.

The 29-point set (claim `sat2-satg8-29`):

`data/SAT2_k8_n29.txt` (29 points, |coordinates| ≤ 1,267,379 < 2^21, SHA-256 `9baf0cd6…4544`), found 05:24 KST by
unit esr-sat-k8f (seed 41) after deleting one point of the 30-point set below (scan of all 30 deletions; the best
left 165 failing cells) and 8.5 min of local search with kicks at 15 % CPU. Finder: convex 3/4/5/6/7/8-subsets
3,654 / 13,381 / 17,728 / 7,196 / 792 / **0** (DFS = brute force; DP largest 7); cells = F_euler = **72,443** (simple:
1 + 406 + 29·27 + 3·C(29,4)); pass 72,443, **fail 0**, mismatch 0. Replay: cells 72,443, pass 72,443, **fail 0, bad 0**,
SATURATED. Claim `sat2-satg8-29`.

The 30-point set (claim `sat2-satg8-30`):


`data/SAT2_k8_n30.txt` (30 points, |coordinates| ≤ 1,210,009 < 2^21, SHA-256 `4847c1f1…a52c`), found 05:16 KST (05:15:53).
How (HEURISTIC): L's sl31 minus point 1 (66 failing cells; points 1-5 tie), satls local search seeds 11 and 21
(units esr-sat-k8a, -k8b; 66 → 2 failing cells in about 10 min at 15-25 % CPU), then seed 41 (unit esr-sat-k8f)
from that 2-cell state: 0 failing cells after 61 s. Exact check (verify.sh, vx1118 binaries unchanged):

| check | result |
|---|---|
| finder satcells K = 8 | general position; convex 3/4/5/6/7/8-subsets 4,060 / 15,314 / 20,656 / 8,451 / 1,032 / **0** (DFS; brute force over all C(30,8) and C(30,7) agrees; DP largest 7); cells = F_euler = **83,491** (simple: 1 + 435 + 30·28 + 3·C(30,4)); pass 83,491, **fail 0**, method mismatches 0; 2.3 s |
| trusted replay check_cells.py | cells 83,491, pass 83,491, **fail 0, bad 0**, verdict SATURATED |

### Track L's sets (K = 6, 7, 8) re-checked with the same exact cell enumeration (04:53-04:55 KST, except the last two rows)

| set (`data/`) | K | cells = F | fail | replay |
|---|---|---|---|---|
| L_k6_n14 (14 points) | 6 | 3,206 | 0 | SATURATED |
| L_k7_n20_s8, _s6, _s9, _s20 (20 points each) | 7 | 14,960 each | 0 | SATURATED (all four) |
| L_k7_n21 (21 points) | 7 | 18,565 | 0 | SATURATED |
| L_k8_n31_sl31 | 8 | 95,760 | 0 | SATURATED (vx1118 run, 04:21 KST) |
| L_k8_n36 | 8 | 178,570 | 0 | SATURATED (vx1118 run) |

### n = 9: sat_g(9) ≤ 48 (EXACT)

- n = 9, **48 points (EXACT)**: `data/SAT2_k9_n48.txt` (|coordinates| ≤ 341,767, SHA-256 `843dfd16…244f`), found 06:45 KST
  by the same descent (esr-sat-k9g1, seed 26; 50 at 05:46, 49 at 06:04, 48 at 06:45; 10-15 % CPU). Exact check (unit
  esr-sat-v48, 06:47-06:59 at 20 % CPU): finder `satcells_nb` K = 9: convex 3/…/9-subsets 17,296 / 110,772 / 283,088 /
  307,751 / 142,859 / 23,101 / **0**, DP largest 8; 1,128 lines, 0 parallel pairs, 583,788 vertices (48 of multiplicity
  47, the rest simple); cells = F_euler = **587,077**; pass 587,077, **fail 0**, mismatches 0 (285 s wall). Replay: largest
  convex subset 8; own F = 587,077; 587,077 distinct samples; pass with verified witness 587,077, **fail 0, bad 0**,
  SATURATED (403 s wall). Claim `sat2-satg9-48`. (A check of the 49-point set, unit esr-sat-v49, was stopped after 4 min
  in favour of the 48-point set; no claim for 49.)
- n = 9, **51 points (EXACT)**: `data/SAT2_k9_n51.txt` (|coordinates| ≤ 374,088, SHA-256 `44710e41…33fb2`), found 05:42 KST
  by the descent (unit esr-sat-k9g1, seed 26: scan of all deletions, then local search with reset to the best state; this unit ran the binary
  from before the kick move was added) from the 58-point
  set, one point at a time (57, 56, 55, 54, 53, 52, 51 at 05:11-05:42). Exact check (unit esr-sat-v51, 05:46-06:03 at
  20 % CPU): finder `satcells_nb` K = 9: convex 3/…/9-subsets 20,825 / 143,994 / 406,983 / 499,653 / 259,837 / 45,480 /
  **0**, DP largest 8; 1,275 lines, 2 parallel pairs, 749,749 vertices (51 of multiplicity 50, the rest simple);
  cells = F_euler = **753,473**; 3,003,892 sector samples; pass 753,473, **fail 0**, mismatches 0 (399 s wall). Replay:
  largest convex subset 8; own F = 753,473; 753,473 distinct samples; pass with verified witness 753,473, **fail 0,
  bad 0**, SATURATED (568 s wall). Claim `sat2-satg9-51`.
- n = 9, **58 points (EXACT)**, the first 9-gon-saturated set (05:04; work file `k9/k9_n58_d16.txt`). Origin: SYMMAX/L `annealg 4 10 0 9 1 30 30000` (4-fold, 10 orbits, 9-gon-free, 40 points; 28,032 of
  275,920 cells failing), then `satls grow` (seed 5): 18 points added one at a time into failing cells (best of up to
  8 valid rounded candidates by the resulting failing count; coordinates multiplied by 4 when no candidate was
  valid), 0 failing cells at 58 points after 33 s; coordinates then divided by 16 and rounded (|x| < 2^23), still
  9-gon-free with 0 of 1,277,161 failing cells. `data/SAT2_k9_n58.txt` (SHA-256 `01d0cc93…b5c9`, |coordinates| ≤
  6,269,805 < 2^23). **Exact check (EXACT), unit `esr-sat-v58`, 05:05-05:45 KST at 10-20 % CPU:**

  | check | result |
  |---|---|
  | finder `satcells_nb` K = 9 (vx1118 satcells with one change: `SATCELLS_NO_BRUTE=1` skips the brute-force count over all C(58,9) ≈ 1.9·10^10 and C(58,8) subsets in part (a), infeasible here) | general position; convex 3/4/5/6/7/8/9-subsets by the pruned DFS (every 4-subset tested) 30,856 / 240,398 / 743,426 / 982,929 / 547,562 / 105,269 / **0**; DP largest 8; 1,653 lines, 380 parallel pairs, 1,272,299 vertices (58 of multiplicity 57, one of multiplicity 20 at the centre of the 4-fold seed, the rest simple); Σ(k_v − 1) = 1,275,507; cells = F_euler = **1,277,161**; 5,095,612 sector samples = Σ 2k_v; distinct cells 1,277,161; pass 1,277,161, **fail 0**, method mismatches 0; 1,196 s wall |
  | trusted replay check_cells.py (unchanged) | collinear triples 0, largest convex subset 8 (own DP); own vertex count 1,272,299 with the same histogram, F = 1,277,161; 1,277,161 samples, all distinct cells; pass with verified witness 1,277,161; **fail 0, bad 0**; SATURATED; 1,195 s wall; unit memory observed up to 1.26 GB |

Since the replay alone proves (a) (its DP) and (b) (cells = F, all distinct, every witness checked), skipping the
finder's brute force does not weaken the result; it removes only one of the finder's three cross-checks of (a).

## 6. Controls

- **Exact checker, negative** (vx1118 runs, same binary): sl31 minus the centre (1,206 failing cells), minus point 11
  (99), s36 minus the centre (121), convex pentagon at K = 6 (33 of 38): every failure confirmed by the replay's DP.
- **Exact checker, positive**: two 16-point hexagon-free sets (saturated because ES(6) = 17), and here L's 14-, 20-
  (four) and 21-point sets (section 5): all SATURATED with the Euler count matched.
- **Search objective vs. exact checker**: the satls counts equal vx1118's on all eight control sets (section 4), and
  every satls hit tonight (13, 12 at K = 6; 19, 18 at K = 7; 30, 29, 28, 27 at K = 8; 58, 51 at K = 9) passed the exact
  check with the same cell count; no hit failed it.
- **Deletion always breaks saturation**: for every saturated set scanned tonight, each single-point deletion left
  failing cells (minimum over deletions, failing cells: K = 6: L's 14-point 61, 13-point 46, 12-point 85; K = 7: L's s20 29,
  s9 58, 19-point 64, 18-point 203; K = 8: sl31 66, 30-point 165, 29-point 198, 28-point 166, 27-point 343; K = 9:
  58-point 13, 57: 15, 56: 12, 55: 81, 54: 24, 53: 36, 52: 116, 51: 20, 50: 183, 49: 167; the deleted point's own cell
  always fails). So each smaller set is a new
  configuration found by the search, not a subset of a known one.
- **`satcells_nb`**: identical to vx1118's satcells except that, with `SATCELLS_NO_BRUTE=1`, it skips the brute-force
  count of convex K- and (K−1)-subsets (it then compares the DFS count with itself). Used only for K = 9 (58 and 51
  points); all K ≤ 8 sets were run with the unchanged binary (`a0495961…`).

## 7. Files and hashes

Record files (`data/`: point sets, one "x y" integer pair per line; `L_*` are unchanged copies of track L's sets,
`SAT2_*` are tonight's; `L_k7_n16_satlocal_k7_20s8_d4.txt` is track L's 16-point set (section 5); `tools/`: `satcells.cpp`, `check_cells.py`, `run_all.sh` are unchanged copies of vx1118's
checker (hashes as in VERIFY_LOWERBOUND_L18_SATG8_CELLS.md), `satcells_nb.cpp` the K = 9 copy (one change, section 6),
`satls.cpp` the finder, `verify.sh` the check driver):

| file | SHA-256 |
|---|---|
| `data/L_k6_n14_r_g2_m7_f0_k6_s13.txt` | `1d09f5b4021e8fc380764f1bad79b97e3c9ddc8ac747d66266e46aedc731fb0a` |
| `data/L_k7_n16_satlocal_k7_20s8_d4.txt` | `00b25ba92a12112be05d31b832f95564fc299a6ecede57ca0eaae2d0f5c0a7f1` |
| `data/L_k7_n20_r6_g4_m5_f0_k7_s20.txt` | `324e1327ce44058cad0114d00d6977471a428b6f50a0579b57f29b439f100367` |
| `data/L_k7_n20_r6_g4_m5_f0_k7_s6.txt` | `e4ea53c0e44bf65257005a00b277c4f9da6f57af7cb8c96ecf7c249a513a095e` |
| `data/L_k7_n20_r6_g4_m5_f0_k7_s8.txt` | `5be6c81dbdcc7d69b35984497f29961db4fd9bec0f116b57e47caf8074779638` |
| `data/L_k7_n20_r6_g4_m5_f0_k7_s9.txt` | `3ace5c5c07695269b95cbf0f0aebcf2cd3699e43f0bf5ead45b62e4b2e190532` |
| `data/L_k7_n21_g5_m4_f1_k7_s2.txt` | `b03990878eca00e92467716afd2466725728c885fce39c1bd8f02b92253d0da0` |
| `data/L_k8_n31_sl31.txt` | `9982e59864204632c46eeec7ccd3860e471efd5c242e1d052c068717fb7a58f8` |
| `data/L_k8_n36_g5_m7_f1_k8_s1.txt` | `90ce329afdaa4f99784cf05a555db4e8014988d5b18f9be04b70ba12e2287eca` |
| `data/SAT2_k6_n12.txt` | `61075bde0c4658f4891d5f8ce299dc1759281619eafad86d727722543a383ccc` |
| `data/SAT2_k6_n13.txt` | `942701fa5ee646effcf7753905eac347e4c9c31a47bd50c6861752dddaac20b8` |
| `data/SAT2_k7_n18.txt` | `d1e26689a9f70ad9a90cba709ce43d1bc93b063f3cbca02b7cc601b4741df4cd` |
| `data/SAT2_k7_n19.txt` | `4799335463b7c1f93a78855a0beb28d5a5edba0700efab4d9b592e50576634a8` |
| `data/SAT2_k8_n27.txt` | `a2116a7b8a2128680363e76abb093cf05c988962fe9e08398229f5edb50b2097` |
| `data/SAT2_k8_n28.txt` | `074addb0c19ec3f0dd89bd67f1ade6bf18e459c8827753b1f48444c70dd1fcb4` |
| `data/SAT2_k8_n29.txt` | `9baf0cd6bce4e896fe6cdd28561e1e0feb33faf3dc7445fef68c39fd6f494544` |
| `data/SAT2_k8_n30.txt` | `4847c1f1373a273240409b502e21ac06cb50437aaebb39d4bead16c72ca9a52c` |
| `data/SAT2_k9_n48.txt` | `843dfd163796e84797e1c21ee2bc4660deabd6dbb600332a21b8a9b9b377244f` |
| `data/SAT2_k9_n51.txt` | `44710e41ebc85edecb2d15a03cf87ea8f3f3d5e8c4fc1f0ace38a397f9833fb2` |
| `data/SAT2_k9_n58.txt` | `01d0cc930f0ec2bdf3b2174fecea49d28fdb7a7f92ccd6cdc9e72adc3789b5c9` |
| `tools/check_cells.py` | `4b6cd648dcf88941238846842c86c9356b71589b992ab90afa449a15ca71072d` |
| `tools/run_all.sh` | `ee7a28551f1e117763060568503c6b7b8429b8d73ae88cd2f50efba5216a45f2` |
| `tools/satcells.cpp` | `9a7b4d9ef1dbff3cf0a7f7addefef88eed0779a4c54f25629727b2f0fad1d891` |
| `tools/satcells_nb.cpp` | `b7ec5bbd908fe07addc687f52623af207947f2fe237a809f3fb71f385e8720fb` |
| `tools/satls.cpp` | `001224afa6f78b8b48f0dbe6486cbdb4adda04480e16576cb8ec8d79ffe1d941` |
| `tools/verify.sh` | `a13cf7f7b3668aecddc0808fa85bc80795c96d2858c980f670d9cc5a2fe07e35` |

Work folder W = `/home/jay/research/data/roadmap-20261115/pm1115/sat2/` (samples with witnesses, read by the replay;
not copied into the repository):

| file | SHA-256 |
|---|---|
| `W/verify/samples/k6_n12.samples.txt` (72K) | `07d36a1d028fa5ec6b8c7b813171e2b7ec7766052cc4ad39e1527ab526b3e8ee` |
| `W/verify/samples/k6_n13.samples.txt` (96K) | `3ff09caa523a9d6422675baa5795159eae8f4d4f4bb6cb3048a7a73be7bbd7f9` |
| `W/verify/samples/k7_n18.samples.txt` (524K) | `3af9fd1984cb7ded11c12ad399cc3a93edf0e9044c1e5a2600e0985c316cebd3` |
| `W/verify/samples/k7_n19.samples.txt` (648K) | `c9a0098cbc819c8b7979d4a417aa4243454b86cebe7240ba76a71556b4ee58e2` |
| `W/verify/samples/k8_n27.samples.txt` (3.6M) | `f8bdeb94e3a5b3843398626ae6aa08e7d9ed86049b735867d50e830dd85bcfc9` |
| `W/verify/samples/k8_n28.samples.txt` (4.2M) | `7790cd7a1320b2b3a8c376a83fbae3123ba0de91ae172150f80eb347a0fd7953` |
| `W/verify/samples/k8_n29.samples.txt` (4.9M) | `0442b4696d8bab72f4d9b6ff3fa32e44fa1529e0770b71752284bacc9062a05a` |
| `W/verify/samples/k8_n30.samples.txt` (5.6M) | `0d610b4fa071311886683325c4dc154dcb83c8dba7160bb06529e744f53e3a95` |
| `W/verify/samples/k9_n48.samples.txt` (36M) | `10396329ee5057af9879a761a4727140416f13a9f00a9afa9decec1337046577` |
| `W/verify/samples/k9_n51.samples.txt` (47M) | `22778321fc1a40b016aab464fa5258b29799d1751b1fbb83541acd63350e9248` |
| `W/verify/samples/k9_n58.samples.txt` (79M) | `91fd1fdefcec5352ebf333789c264b62332d3197a45634f4c41723813767ed23` |
| `W/vx/satcells_nb` | `da8750d11c5bd6c2ea14436c22c905ffe68814a230b3a38a239cecaff9faf4c9` |
| `W/verify/samples/L_k7_n16.samples.txt` (360K) | `432ce8c1df82a70c4df8d184f1ade0e16423fd24b34c65da8a68d206b8769d76` |
| `W/verify/status.jsonl` | `6813d0a201254f92350a3df2708bda4579532d8cef3bf5066da17c08278ec92c` |

The vx1118 binary used for K ≤ 8 is `pm1115/vx1118/satcells` (`a0495961c2c86498…`). Logs: `W/verify/logs/<name>.{cpp,py}.log`,
one line per run in `W/verify/status.jsonl`; search logs `W/runs/<unit>/log.jsonl`, `W/k9/g1/log.jsonl`; claims as
filed in `pm1115/claims/sat2-*.claim.json` (copies of the JSON in `W/claims/`).

## 8. Literature status

From [WATCH_1118.md](../NOVELTY20261115/WATCH_1118.md) §2f (searches 03:18-03:21 KST, 18 Nov): "the only published
bounds are DDSZ's sat_g(n) ≤ 7/8 · 2^(n−2) for n ≥ 7 (28, 56); DDSZ have no citing works in OpenAlex or Semantic
Scholar"; DDSZ's final remarks: "Our current upper bounds on sat_c(k, ℓ) and sat_g(n) are exponential, while the
lower bounds are linear (sat_g(n) ≥ n − 1 is trivial). The obvious problem is to obtain better bounds." Verdict
there: sat_g(7) ≤ 20 and sat_g(8) ≤ 36 (now 31) "not found in this search". No new literature search was made for
this record (none was needed by the task); sat_g(6) ≤ 13 is likewise "not found in this search" (WATCH_1118 found only
the 16-point extremal hexagon-free sets in a web search for maximal hexagon-free sets with fewer than 16 points).

## 9. What remains

- **Independent verification** of the claims filed tonight (`sat2-satg6-12`, `-13`, `sat2-satg7-16` (track L's set), `-18`, `-19`,
  `sat2-satg8-27`, `-28`, `-29`, `-30`, `sat2-satg9-48`, `-51`, `-58`): own exact code, `VERIFY_SAT2_*.md` in this
  folder. Every check here used vx1118's code (finder + replay), not code independent of the record.
- **Smaller sets (negative so far, HEURISTIC):** when the units were stopped (07:31 KST) the searches were at
  - K = 6, 11 points: best 6 failing cells (esr-sat-k6b, about 68 min at 2-4 % CPU, about 680,000 moves); multigrow
    (1,054 random greedy growths): smallest saturated set 13 (32 times), never 12 or less;
  - K = 7, 15 points (from L's 16-point set; best deletion leaves 347 failing cells): best 57 and 60 after 7 min at
    30 % CPU each (esr-sat-k7L1, -k7L3, seeds 141, 143; 267,000 and 250,000 moves);
  - K = 7, 17 points: best 2 failing cells (esr-sat-k7f, from the 18-point set minus point 5; 203 at the start) and 20
    (esr-sat-k7i, minus point 0); multigrow (62 growths): smallest 21;
  - K = 8, 26 points: best 4 failing cells (esr-sat-k8j, from the 27-point set; 343 at the start) and 20 (esr-sat-k8i);
  - K = 9, 47 points: best 6 failing cells (esr-sat-k9g1); a second chain from the 49-point set (second-best deletion)
    reached 8 at 48 points before it was stopped.
  None of these is evidence that smaller sets do not exist; no lower bound beyond the trivial sat_g(n) ≥ n − 1 was
  attempted.
- **K = 9 from other seeds**: only one seed (a 4-fold 40-point anneal) was grown; the annealer itself was too slow at
  15 % CPU for K = 9 (all six configurations of `k9gen.sh` timed out, not kept). Other seeds or symmetric descents may
  give smaller 9-gon-saturated sets; K = 10 was not tried.
- **Order type vs. coordinates**: none of the new sets was tested for order-type saturation (`l1enc`); all claims are
  about the given integer coordinates.

## 10. Resume commands

```bash
W=/home/jay/research/data/roadmap-20261115/pm1115/sat2
cd $W && g++ -O2 -march=native -std=c++17 -o satls src/satls.cpp          # finder (HEURISTIC search)
g++ -O2 -std=c++17 -o vx/satcells_nb vx/satcells_nb.cpp -lgmpxx -lgmp     # K = 9 copy of the vx1118 finder
./satls eval <points.txt> <K>                    # failing-cell count of one set
./satls scan <points.txt> <K>                    # failing cells after each single deletion
./verify.sh <name> <points.txt> <K> [nb]         # EXACT: satcells (or satcells_nb with nb) + check_cells.py
# a descent chain as a capped unit (example: continue K = 8 from the 27-point set):
mkdir -p runs/k8x k9/gx
systemd-run --user --unit=esr-sat-k8x -p CPUQuota=15% -p MemoryMax=150M -p MemorySwapMax=0 -p RuntimeMaxSec=7200 \
  --nice=10 --working-directory=$W $W/satls search verify/k8_n27.txt 8 runs/k8x 7 7000 -2
# K = 9 grow from a seed, then descend (memory ~50 MB; the exact check of 48-58 points needs 0.8-1.4 GB):
$W/satls grow k9/a40.txt 9 k9/gx 5 3600
```

## SAT3 addendum (18 Nov, from 08:40 KST)

Track SAT3 (one agent, 08:40-12:30 KST; systemd user units `esr-sat-*`, at most 45 % CPU in total). Work folder
`/home/jay/research/data/roadmap-20261115/pm1115/sat3/` (notes `NOTES.md`). The text above this section is unchanged.
**Status: final for this run (11:50 KST; all SAT3 units stopped).**

### S1. Headline (labels for the stated integer coordinates)

| n | best set now | label | claim | before SAT3 | DDSZ Thm 4 |
|---|---|---|---|---|---|
| 8 | 27 (unchanged) | EXACT (SAT2) | – | 27 | 56 |
| 9 | **40** (also 44) | **EXACT, independent check by VX2's code** | `sat3-satg9-40`, `sat3-satg9-44` | 48 | 112 |
| 10 | **52** (also 56, 60, 64, 68) | **EXACT, independent check by VX2's code** | `sat3-satg10-52`, `-56`, `-60`, `-64`, `-68` | none | 224 |

So, for these coordinates: **sat_g(9) ≤ 40** and **sat_g(10) ≤ 52**. "EXACT, independent check" means: the sets were
found by SAT3's finder (HEURISTIC search, own code, derived from SAT2's `satls`), and each listed set was then checked by
VX2's exact checker `vx2sat2` (SHA-256 `3537f4936d2efd71005cc914cf75980ef3231e33870e4c76e6b95e017397d90b`, built from
`pm1115/vx2/vx2sat.cpp`, SHA-256 `9b243cd1…3a55d`), run **unchanged** by SAT3 with VX2's own arguments
(`vx2sat2 <file> <n> -1 1000 1`; negative control `vx2sat2 <file> <n> 0 300 1`). VX2's code was written independently of
SAT2's and SAT3's finders (vertical sweep, exact signs with a proven float filter and GMP fallback, cells = Euler count,
per-cell DP plus exhaustive DFS on samples). It has not yet been re-run by VX2 itself or by a verifier other than SAT3.
All new sets are invariant under the rotation (x, y) → (−y, x) about the origin. "New" only means not found in this
search; no literature search was made (section 8 above is the last one).

### S2. Results

Each line: VX2 `vx2sat2` run unchanged, full run (`… <n> -1 1000 1`) and negative control with point 0 deleted
(`… <n> 0 300 1`); logs in `sat3/vx/`.

- **n = 9, 40 points, claim `sat3-satg9-40` (EXACT, VX2):** `data/SAT3_k9_n40.txt`, 10 orbits of 4, |coordinates| ≤
  280,194. Part (a): general position; largest convex subset 8 by DP and by exhaustive DFS (convex 3..9-subsets 9,880 /
  50,134 / 89,404 / 62,912 / 15,748 / 1,227 / **0**); also VX2's brute force over all C(40,8) and C(40,9) subsets
  (`… 9 -1 0 1 3`, 34 s CPU): 1,227 convex 8-subsets and **0** convex 9-subsets, both agreeing with the DFS. Part (b): 780
  lines, 273,641 vertices; cells = distinct sign vectors = Euler count F = **275,920**, V − E + F = 1; method A **0 failing
  cells**; method B 1,000 samples agree; `VERDICT SATURATED_SET` (91 s wall, 9 s CPU). Negative control: 1,524 failing
  cells, `VERDICT NOT_CONFIRMED`.
- **n = 9, 44 points, claim `sat3-satg9-44` (EXACT, VX2):** `data/SAT3_k9_n44.txt`, 11 orbits of 4, |coordinates| ≤
  280,194. Part (a): general position; largest convex subset 8 (DP, DFS: convex 3..9-subsets 13,244 / 74,487 / 151,556 /
  130,996 / 47,720 / 6,168 / **0**; brute force skipped, C(44,8) > 6·10^6). Part (b): 946 lines, 406,605 vertices; cells =
  distinct = F = **409,376**, V − E + F = 1; method A **0 failing**; method B 1,000 agree; `VERDICT SATURATED_SET` (147 s
  wall, 18 s CPU). Negative control: 391 failing cells, `VERDICT NOT_CONFIRMED`.
- **n = 10, 52 points, claim `sat3-satg10-52` (EXACT, VX2):** `data/SAT3_k10_n52.txt`, 13 orbits of 4, |coordinates| ≤
  585,500. Part (a): general position; largest convex subset 9 (DP, DFS: convex 3..10-subsets 22,100 / 147,985 / 352,104 /
  341,850 / 141,132 / 23,926 / 1,412 / **0**; brute force skipped, C(52,9) > 6·10^6). Part (b): 1,326 lines (650 parallel
  pairs), 811,253 vertices (52 of multiplicity 51, one of multiplicity 26 at the centre); cells = distinct = F =
  **815,152**, V − E + F = 1; method A **0 failing**; method B 1,000 agree; `VERDICT SATURATED_SET` (277 s wall, 55 s CPU,
  213 MB). Negative control: 1,983 failing cells (method B confirms the 300 it checked), `VERDICT NOT_CONFIRMED` (158 s).
- **n = 10, 56 points, claim `sat3-satg10-56` (EXACT, VX2):** `data/SAT3_k10_n56.txt`, 14 orbits of 4, |coordinates| ≤
  582,283. Part (a): general position; largest convex subset 9 (DP, DFS: convex 3..10-subsets 27,720 / 201,274 / 524,260 /
  557,848 / 250,836 / 46,880 / 3,052 / **0**; brute force skipped, C(56,9) > 6·10^6). Part (b): 1,540 lines (756 parallel
  pairs), 1,100,793 vertices (56 of multiplicity 55, one of multiplicity 28 at the centre); cells = distinct = F =
  **1,105,328**, V − E + F = 1; method A **0 failing**; method B 1,000 agree; `VERDICT SATURATED_SET` (235 s wall, 82 s
  CPU, 330 MB). Negative control: 1,411 failing cells (method B confirms the 300 it checked), `VERDICT NOT_CONFIRMED` (289 s).
- **n = 10, 60 points, claim `sat3-satg10-60` (EXACT, VX2):** `data/SAT3_k10_n60.txt`, 15 orbits of 4, |coordinates| ≤
  608,307. Part (a): general position; largest convex subset 9 (DP, DFS: convex 3..10-subsets 34,220 / 268,619 / 772,936 /
  927,864 / 480,568 / 104,848 / 7,960 / **0**; brute force skipped, C(60,9) > 6·10^6). Part (b): 1,770 lines (870
  parallel pairs), 1,461,661 vertices (60 of multiplicity 59, one of multiplicity 30 at the centre); cells = distinct = F
  = **1,466,880**, V − E + F = 1; method A **0 failing**; method B 1,000 agree; `VERDICT SATURATED_SET` (426 s wall, 128 s
  CPU, 463 MB). Negative control: 2,620 failing cells (method B confirms the 300 it checked), `VERDICT NOT_CONFIRMED` (448 s).
- **n = 10, 64 points, claim `sat3-satg10-64` (EXACT, VX2):** `data/SAT3_k10_n64.txt`, 16 orbits of 4, |coordinates| ≤
  608,517. Part (a): general position; largest convex subset 9 (DP, DFS: convex 3..10-subsets 41,664 / 353,904 /
  1,133,072 / 1,519,060 / 863,060 / 200,597 / 15,156 / **0**; brute force skipped). Part (b): 2,016 lines (992 parallel
  pairs), 1,904,705 vertices (64 of multiplicity 63, one of multiplicity 32 at the centre); cells = distinct = F =
  **1,910,656**, V − E + F = 1; method A **0 failing**; method B 1,000 agree; `VERDICT SATURATED_SET` (727 s wall, 218 s
  CPU, 653 MB). Negative control: 3,355 failing cells (method B confirms the 301 it checked), `VERDICT NOT_CONFIRMED`.
- **n = 10, 68 points, claim `sat3-satg10-68` (EXACT, VX2):** `data/SAT3_k10_n68.txt`, 17 orbits of 4, |coordinates| ≤
  608,517. Part (a): general position; largest convex subset 9 (DP, DFS: convex 3..10-subsets 50,116 / 447,273 /
  1,493,176 / 2,101,648 / 1,308,412 / 344,976 / 27,628 / **0**). Part (b): 2,278 lines (1,122 parallel pairs), 2,441,541
  vertices (one of multiplicity 34 at the centre); cells = distinct = F = **2,448,272**, V − E + F = 1; method A **0
  failing**; method B 1,000 agree; `VERDICT SATURATED_SET` (942 s wall, 288 s CPU, 914 MB). Negative control: 603 failing
  cells (method B confirms the 300 it checked), `VERDICT NOT_CONFIRMED`.
- **n = 10, finder only (COMPUTED; N > 70, so VX2 cannot run):** 72 points (4-fold; 3,092,112 cells, 0 failing), 76
  points (4-fold; 3,855,328 cells), 83 points (no symmetry; lifted from SAT2's 48-point 9-gon-saturated set by greedy
  growth with K = 10, 09:02 KST; 5,522,987 cells). SAT2's `satls eval` and SAT3's copy agree on each.

### S3. Method (HEURISTIC; not part of any proof)

`tools/sat3ls.cpp` (work copy `src/sat3ls5.cpp`; produced the 44-, 40-, 72- and 68-point sets), `tools/sat3ls6.cpp`
(the same with the move bound 2^24 instead of 2^22 and the grown set written; produced the 76-, 64-, 60-, 56- and 52-point
sets) and `tools/sat3ls8.cpp` (sat3ls6 plus 3- and 6-fold rotations in the Eisenstein basis): copies of SAT2's
`satls.cpp` with
- **one-sweep deletion scan:** for every cap (a, b, p, r) of a convex (K−1)-gon, the AND of the vertex sets of all
  (K−1)-gons that give it; a covered cell is lost by deleting point x iff x lies in the AND over all caps covering the
  cell. One sweep gives, for every x, an upper bound on the old cells failing after deleting x (0 iff S − x is still
  saturated): 0.57 s instead of 6.5 s (48 points, K = 9). Used for descents and kicks.
- **symmetric search (`symgrow`, `symsearch`):** points stored as orbits of the rotation; growth adds the best of 4
  rounded failing-cell samples together with its 3 rotations; a move shifts one orbit (Gaussian step, log-uniform
  scale); after 150-300 moves without progress either a reset to the best state or a kick (add the best orbit, delete
  the orbit with the smallest deletion bound); after a hit, the orbit with the smallest deletion bound is deleted.
- **lifting** (grow K + 1 from a K-saturated set) and **destroy-and-repair** (`lns`: delete 2-3 low-cost points, regrow,
  prune free deletions); both gave no record here (S5).
- The chain behind all records: SAT2's 4-fold 9-gon-free 40-point seed `k9/a40.txt` (SYMMAX `annealg 4 10 0 9`).
  K = 9 (unit esr-sat-k9S, seed 72): growth to 52 (saturated) → 48 → 44 → 40 by orbit deletions and symmetric local
  search (09:15 KST: 44; 09:40: 40). K = 10 (esr-sat-k10S, seed 71, then esr-sat-k10S2, seed 78): growth to 76
  (saturated) → 72 (09:29) → 68 (09:45) → 64 (10:18; esr-sat-k10S2, from the 64-point state with 52 failing
  cells) → 60 (11:00; esr-sat-k10S3, seed 80: the 64-point set minus one orbit, 6,376 failing cells, to 0 in 100 s) → 56 (11:19; the 60 minus one orbit, 3,320 failing cells) → 52 (11:25; the 56 minus one orbit, 6,420
  failing cells). Before the VX2 runs the coordinates were divided by 256 (K = 9) or
  16 (K = 10) and rounded half away from zero (keeps the symmetry); the finder showed 0 failing cells after rounding.

### S4. Controls

- Every claimed set: VX2 negative control (point 0 deleted) fails as it must (numbers in S2).
- Finder vs. checker: SAT2's original `satls eval` and SAT3's copy give the same cell counts and 0 failing cells on
  every claimed set; these counts equal VX2's Euler counts (409,376; 275,920; 2,448,272; 1,910,656; 1,466,880; 1,105,328; 815,152).
- One-sweep deletion scan vs. n separate evaluations (SAT2's 48-point set, K = 9): same best point (37), every point
  positive in both (the bound counts old cells, so it is larger: 407 vs 73).

### S5. Negative results (HEURISTIC; none is evidence of non-existence)

- **K = 8, no set below 27.** (i) SAT2-type local search from SAT2's 27-point set minus its best point (esr-sat-k8a, seed
  31, 16 min at 5 % CPU): 26 points with 8 failing cells at best; continued (esr-sat-k8b, 8 min): still 8. (ii)
  Destroy-and-repair from SAT2's 27 (esr-sat-k8L, 20 min at 5 %): 200 iterations, 49 plateau moves (other 27-point
  saturated sets), no 26. (iii) 4-fold symmetry: SYMMAX `annealg 4 5 0 8` seed (20 points) → 32 → **28** (a new
  4-fold 28-point 8-gon-saturated set by the finder, not claimed, not better) → 24 points with 60 failing cells at best
  (esr-sat-k8S4, 35 min at 5 %); an asymmetric descent from that 28 (esr-sat-k8D) gave a 27-point set (finder, equal to
  the record, not claimed) and 26 points with 19 failing cells at best; 2-fold symmetric search from the 28: 26 points,
  130 failing; 3- and 6-fold growth from small annealed seeds: saturated at 30-42 points.
- **K = 9, nothing below 40.** Symmetric continuation (esr-sat-k9S, same chain as the 40): 36 points with 36
  failing cells at best (about 100 min at 3-10 % CPU); second seed from the 40 (esr-sat-k9S3, 25 min at 5 %): 36 points,
  944 failing. Before the symmetric chain: SAT2-type descent from SAT2's 48 (esr-sat-k9b, seed 22): 47 points, 6 failing
  (as SAT2); destroy-and-repair from SAT2's 48 (esr-sat-k9L): 25 iterations, 15 plateau moves, no 47; lifting (growth with
  K = 9 from SAT2's 27-point 8-gon-saturated set) gives a 54-point 9-gon-saturated set in 15 s, its descent (esr-sat-k9a):
  53 points, 8 failing; 3-fold symmetry (Eisenstein basis, annealed 18-point seed): saturated at 51, then 48 points with 72
  failing; asymmetric descent from the 44 (esr-sat-k9E): 43 points, 27 failing.
- **K = 10, nothing below 52.** Symmetric continuation (esr-sat-k10S3, from the 52): 48 points with 228 failing cells at
  best when the unit was stopped; the first 60-point attempt (esr-sat-k10S2, another orbit deleted from the 64-point state) stalled at 32 failing cells.
  Lifting from SAT2's 48-point set gave the 83-point set; destroy-and-repair from 83 (esr-sat-k10L, 6 min) and a
  fixed-size local search at 73 points (esr-sat-k10c: 383 → 245 failing) were stopped in favour of the symmetric chain;
  a 4-fold growth sweep from a40 with other seeds gave 84 (seed 1); 3-fold growth from an annealed 18-point seed reached
  78 points with 381 failing cells when that unit was stopped (see the memory note below).
- **Memory note (rule violation, no OOM kill):** unit esr-sat-k10G3 (3-fold K = 10 growth) peaked at 587.5 MB of its
  600 MB MemoryMax (above the 80 % rule) and was stopped cleanly by `esr-memguard-1118` at 09:44:29 KST ("memory 586 MB
  reached its limit"); no kernel OOM kill. All other SAT3 units stayed below 80 % (largest: the VX2 runs, 914 MB of 2 GB).
- **Units:** esr-sat-k10a, -k10b, -k10c, -k10L, -k10D, -k10S, -k10S2, -k10S3, -k10G3, -sw10, -k9a, -k9b, -k9c, -k9D, -k9E,
  -k9L, -k9L2, -k9S, -k9S2, -k9S3, -k9G3, -k8a, -k8b, -k8L, -k8D, -k8S2, -k8S4 (searches) and -vx44, -vx40, -vxb40, -vx68,
  -vx64, -vx60, -vx56, -vx52 (VX2 runs); total CPUQuota ≤ 45 % throughout, apart from a moment of 47 % between two consecutive
  `set-property` calls at about 09:41; all stopped by 11:50 KST.

### S6. Files and hashes (`data/`)

| file | n | K | points | SHA-256 | label |
|---|---|---|---|---|---|
| `SAT3_k9_n40.txt` | 40 | 9 | 4-fold | `3442c966e6adc9222664e159e85933194b747d8830c2f9fab39dd919307bd37a` | EXACT (VX2) |
| `SAT3_k9_n44.txt` | 44 | 9 | 4-fold | `e066b74696e67778cd5e88b1cd1ffa7599d1cfa46487178328fa7585693a7513` | EXACT (VX2) |
| `SAT3_k10_n52.txt` | 52 | 10 | 4-fold | `f03ef0b858630a93e06597243d86292d33718697e8a2986a2680b4e1d860696c` | EXACT (VX2) |
| `SAT3_k10_n56.txt` | 56 | 10 | 4-fold | `c2f2f5213128605915f255b05a88846fe0fd49cb929e024473bcfbd3720e55f2` | EXACT (VX2) |
| `SAT3_k10_n60.txt` | 60 | 10 | 4-fold | `7723af958b6e0e43b89acb6ced885cb6e35175d6050d63bf5fe3c3580e9850f2` | EXACT (VX2) |
| `SAT3_k10_n64.txt` | 64 | 10 | 4-fold | `f72127119f13030a26b0fe80ca290958f35e4ccd1f94fdb05c4ac23c22baf9fb` | EXACT (VX2) |
| `SAT3_k10_n68.txt` | 68 | 10 | 4-fold | `e3cff06e1bba8f980abca5516f567abf29a5e5b267f323eb1f4a0200505f79b5` | EXACT (VX2) |
| `SAT3_k10_n72.txt` | 72 | 10 | 4-fold | `7156bcaa1a59b2164d6f7e5e3e955fe64dc15dddc6c0743653dcb86f700ccc51` | COMPUTED (finder only; N > 70) |
| `SAT3_k10_n76.txt` | 76 | 10 | 4-fold | `30a44ac21b611b573ccaa96aeeb4524d9146ff7854db3ddb9b4caeaf9227b99b` | COMPUTED (finder only; N > 70) |
| `SAT3_k10_n83.txt` | 83 | 10 | none | `a25083dae6bda4d0e3ba2f157581438d2c0aaa74c8b4596810a889da188ea774` | COMPUTED (finder only; N > 70) |

VX2 cannot check sets with more than 70 points unchanged (`vx2sat.cpp` stops with `N out of range` for N > 70; it also
needs |coordinates| < 2^23). Tools: `tools/sat3ls.cpp` (SHA-256 `68d85171…020d`), `tools/sat3ls6.cpp`, `tools/sat3ls8.cpp`, `tools/sat3_launch.sh`,
`tools/sat3_vxcheck.sh`, `tools/sat3_mkclaim.py`. VX2 logs: `sat3/vx/{final,neg}_<claim id>.log` and `.time`;
brute-force log for the 40-point set `sat3/vx/brute_sat3-satg9-40.log`. Claims: `pm1115/claims/sat3-*.claim.json`.

### S7. What remains

- Independent re-runs of the seven claims (`sat3-satg9-40`, `-44`, `sat3-satg10-52`, `-56`, `-60`, `-64`, `-68`) by a verifier other than SAT3 (VX2 itself, or own code), `VERIFY_<id>.md`.
- The sets with more than 70 points (72, 76, 83 for K = 10) cannot be checked by VX2 unchanged.
- Smaller sets: K = 8 below 27; K = 9 below 40; K = 10 below 52 (S5).
  Other symmetry groups (3-, 6-fold, with a centre point) were tried only briefly.
- Order-type saturation of the new sets was not tested; all claims are about the given coordinates.

### S8. Resume commands

```bash
W=/home/jay/research/data/roadmap-20261115/pm1115/sat3; cd $W
g++ -O2 -march=native -std=c++17 -w -o sat3ls8 src/sat3ls8.cpp
./sat3ls8 eval <points> <K>                       # failing cells (finder)
BIN=sat3ls8 STALL=300 KICKP=0.6 ./launch.sh <job> <cpu%> <mem> symgrow seeds/a40.txt <K> <seed> 4   # symmetric chain
BIN=sat3ls8 STALL=150 KICKP=0.6 ./launch.sh <job> <cpu%> <mem> symsearch <state.txt> <K> <seed> 4 -1  # continue a state
vx/vxcheck.sh <claim id> <points> <K> 1000 300    # VX2 unchanged: full run + negative control (as a capped unit)
```

## Second implementation for the SAT3 sets (main session, 18 Nov 12:40 KST)

All seven SAT3 sets were re-checked with track vx1118's implementation. It is independent of SAT3's finder and of
VX2's checker. It consists of the finder `satcells` (in SAT2's copy `satcells_nb`, which skips only the C(n,K)
brute force) and the trusted Python replay `check_cells.py` (`4b6cd648…`). Every set was SATURATED in both programs,
with cells equal to the Euler count and 0 failures:

| set | cells | finder s | replay s |
|---|---|---|---|
| SAT3_k9_n40 | 275,920 | 14 | 21 |
| SAT3_k9_n44 | 409,376 | 23 | 36 |
| SAT3_k10_n52 | 815,152 | 101 | 105 |
| SAT3_k10_n56 | 1,105,328 | 159 | 155 |
| SAT3_k10_n60 | 1,466,880 | 238 | 229 |
| SAT3_k10_n64 | 1,910,656 | 392 | 343 |
| SAT3_k10_n68 | 2,448,272 | 561 | 484 |

So sat_g(9) ≤ 40 and sat_g(10) ≤ 52 each rest on two independent exact implementations.
- Logs: `/home/jay/research/data/roadmap-20261115/pm1115/main1118/vx1118sat3/`.
- The first unit (2.5 GB) was stopped cleanly by the memory guard on the 68-point set; it was rerun alone with 7 GB.
- Verdict files: `pm1115/claims/sat3-*.verdict.json` (verifier `MAIN-vx1118`).

## SAT4 addendum (Linux, 21 Nov 2026 20:16–23:25 KST; checks completed 22 Nov 00:40 KST)

Workflow `research-wave1-1121`, worker D (one thread at a time; units `esr-ag-satg-*`, CPUQuota 100 %, MemoryMax 600M,
nice 10). Work folder `/home/jay/research/data/lower-20261121/satg/` (worker README SHA-256 `01e1a3a5…9532`). The text
above this section is unchanged.

**Status: final for this run. Three new upper bounds, each EXACT for the stated integer coordinates.**

### T1. Headline

| n | best set now | before | label | DDSZ Thm 4 |
|---|---|---|---|---|
| 6 | **11** (three 11-point sets, at least two order types) | 12 (SAT2) | **EXACT** | none (n ≥ 7) |
| 8 | **26** | 27 (SAT2) | **EXACT** | 56 |
| 9 | **39** | 40 (SAT3) | **EXACT** | 112 |

Current best bounds from this record: **sat_g(6) ≤ 11, sat_g(7) ≤ 16, sat_g(8) ≤ 26, sat_g(9) ≤ 39, sat_g(10) ≤ 52.**
These are upper bounds given by explicit sets. Nothing about ES(n) follows. Lower bounds are still only the trivial
sat_g(n) ≥ n − 1.

### T2. Statement and checks

The sets `data/SAT4_k6_n11.txt`, `data/SAT4_k8_n26.txt` and `data/SAT4_k9_n39.txt` are in general position. They have no
convex 6-, 8- or 9-gon respectively, and they are 6-, 8- or 9-gon-saturated in the sense of section 2 (DDSZ).
Each verdict was reached by five exact implementations (model of section 3 (II): one decision per open cell of the
arrangement of the C(N,2) lines):

| implementation | author | 11 points | 26 points | 39 points |
|---|---|---|---|---|
| vx1118 `satcells` (K = 9: SAT2's `satcells_nb`) + trusted replay `check_cells.py`, unchanged | record | SATURATED, 1,145 cells | SATURATED, 45,800 | SATURATED, 248,938 |
| VX2 `vx2sat2`, unchanged (`<n> -1 1000 1`) | VX2 | SATURATED_SET; brute force 0 convex 6-subsets | SATURATED_SET; 0 convex 8-subsets | SATURATED_SET; brute force over all C(39,8) and C(39,9): 1,140 convex 8-subsets, 0 convex 9-subsets |
| `tools/sat4_satcheck.cpp` (new, exact `__int128`, cells from edge sign vectors) | worker D | SATURATED | SATURATED | SATURATED |
| `tools/sat4_satcheck_big.py` (pure Python integers, no coordinate bound) | worker D | SATURATED | – | – |
| `tools/sat4_vsat_verifier.cpp` (SHA-256 `5453cb48…8c0c`; own code, independent of all of the above: cells by Euler count, every cell decided from the definition, plus a replay of the finder's rational samples; plain brute force over all K- and (K−1)-subsets) | rebuild verifier | SATURATED, 1,145 cells; 0 convex 6-subsets, 22 convex 5-subsets | SATURATED, 45,800; 0 / 497 | SATURATED, 248,938; 0 / 1,140 |

- Verify files: `VERIFY_sat4_REBUILD.md` (own code, verdict **confirmed** for all three) and `VERIFY_sat4_SOUNDNESS.md`
  (convention and evidence review, **confirmed** for all three).
- Main-session check (22 Nov 00:40):
  - the five SHA-256 hashes below were recomputed;
  - the verifier's verdict lines were read;
  - every checker's cell count equals 1 + C(N,2) + N(N−2) + 3·C(N,4), the face count of the arrangement when no two
    lines are parallel and the only multiple points are the N points of S. That is 1,145, 45,800 and 248,938 for N = 11, 26, 39, so no cell
    was missed.
- The negative controls behaved as required. Each set minus point 0 is NOT saturated, with 166, 712 and 2,037
  failing cells in two implementations. The controls of the fresh checker reproduce the record's exact failure
  counts on nine vx1118 control sets.

Witness coordinates (one `x y` per line in the files):
- 11 points: (213881, 71368), (318, −1092), (−89750, 461390), (5440, 22606), (−2755, 54), (877, 1710),
  (56539, −45020), (−104159, 35280), (10577, 3446), (−53231, −35237), (−5619, 22356).
- 26 points: see `data/SAT4_k8_n26.txt`, |coordinates| ≤ 3,850,224.
- 39 points: see `data/SAT4_k9_n39.txt`, |coordinates| ≤ 621,645, no symmetry.
- Two further 11-point sets: `data/SAT4_k6_n11_b.txt` (same convex-subset counts as the first) and
  `data/SAT4_k6_n11_c.txt` (165 / 148 / 22 / 0 convex 3..6-subsets, so a different order type). Both are SATURATED in
  the record checker, VX2, satcheck, satcheck_big and the verifier's code.

### T3. Method (HEURISTIC; not part of any proof)

All four hits came from SAT3's local search at default settings: the unchanged `sat3ls8`, or its copy
`tools/satls9.cpp` with the new options off, whose trajectory then equals sat3ls8's.
- The 26-point set: SAT2's 27-point set minus point 1, then local search (73 s).
- The 11-point sets: SAT2's best 11-point state (6 failing cells), and SAT2's 12-point set minus point 0.
- The 39-point set: the first asymmetric descent from SAT3's 40-point set (second start, point 8 deleted; 534 s).

### T4. Negative results (HEURISTIC; none is evidence of non-existence)

- **K = 6 at 10 points:** eight full 150-s descents all ended at exactly 13 failing cells of 756. In each case these
  are 5 unbounded cells plus 4 antipodal pairs of point-adjacent sectors.
- **K = 8 at 25 points:** the best states have 2 failing cells, always one antipodal pair of thin sectors at the same
  point.
- **K = 9 at 38 points:** 27 failing cells after the 60-s tail of the hit run.
- **K = 7 below 16 and K = 10 below 52** were not tried in this run.

### T5. Lemma (PROVED, written argument, unrefereed)

A failing cell whose closure contains a point p of S is covered iff some convex (K−1)-gon through p lies, apart
from p, strictly on one side of a line through p in that sector. So such cells depend only on the order type. The
proof is in the worker README. The verifier checked it step by step and ran its own sector-by-sector machine check:
16 states, 0 mismatches.

### T6. Finder overflow (not a claim)

The finders `sat3ls8` and `satls` compute orientations in 64 bits and put no coordinate bound on kick points. In two
runs (k6g, k6h), kick points with |coordinate| up to 6·10¹² overflowed and produced false "FOUND" reports. Every exact
checker rejected them. `satls9` now skips kick candidates with |coordinate| ≥ 2^24. Past claims are unaffected,
because each was checked by exact code.

### T7. Literature (22 Nov 2026)

These searches found nothing on sat_g newer than DDSZ:
- two arXiv queries (saturated / convex / point set / Erdős–Szekeres / general position, from June 2023);
- a web search (DDSZ v3 of 6 Oct 2025, published in EJC 2025);
- the Semantic Scholar citation graph of DDSZ, from a cache of about 16 Nov, which lists 0 citing works.

The new bounds are "not found in this search", with that scope only.

### T8. Files and hashes

| file | SHA-256 |
|---|---|
| `data/SAT4_k6_n11.txt` | `0583fc7d58a7588ffb6bb0a7a0c269095b3c9ed2e836f3c9258615c4d2c0f35d` |
| `data/SAT4_k6_n11_b.txt` | `d11855a4c917d7ea6c8616ca87af389be76645e9432e4b84a7cfd3d581dbefb5` |
| `data/SAT4_k6_n11_c.txt` | `46e742ad3cb49bcde5677f76d632b8de67f47ee4860c81bf3dcf243eb3e075ea` |
| `data/SAT4_k8_n26.txt` | `123fcd3985fafc4c794fff982a008a1448e5dc14318289fe14d97ec62a3c057d` |
| `data/SAT4_k9_n39.txt` | `204a0744b0740d60c4a5278a03112cb0e598e8db9864b8541d3d6717dc28d50b` |
| `tools/satls9.cpp` (finder, fixed build) | `2171c0de0ed1d340848316f7952da17befb2db15fe16e999408dcbdb6df6b9a8` |
| `tools/satls9_v1.cpp` (finder that produced the 11-point hits) | `afb55e547f12da7e3da91342e6344ffe1f8ae98aa70201d61d6107a6e152e7d8` |
| `tools/sat4_satcheck.cpp` | `06cfa5fc02f0917174094a4e9d70b37ff65e27d14227832ec5eb174e38b5d120` |
| `tools/sat4_satcheck_big.py` | `521d11cf50cf4e8714e0816b49eeaaeed91dd72d0f30bb5c13d89d0d42572547` |
| `tools/sat4_vsat_verifier.cpp` | `5453cb48e5775c78edd619f72078192dc246cb087ca384e801544f3a348f8c0c` |
| `VERIFY_sat4_REBUILD.md` | `1ffd4b38c2d07b03abc78729f6d538bf4f453f03ee505eefb9a77368983f752c` |
| `VERIFY_sat4_SOUNDNESS.md` | `a21305edbde77c00e8037e465ada4bf138b4ae94784f863adb1641f31ea67edf` |

The logs (`vx/`, `logs/`, `verify/logs/`) are in the work folder, together with `SHA256SUMS`.

### T9. What remains

- K = 8 at 25 points: 2 failing cells, at one point.
- K = 7 below 16, K = 10 below 52 and K = 6 at 10 points, where the floor is 13 cells.
- Lower bounds beyond n − 1. Saturation depends on the coordinates; only point-adjacent cells are order-type data
  (T5).

### T10. Resume

```bash
W=/home/jay/research/data/lower-20261121/satg; cd $W
g++ -O2 -march=native -std=c++17 -w -o bin/satls9 src/satls9.cpp
# one descent as a capped unit (example: K = 8 from the 26-point set, delete point 25)
systemd-run --user --unit=esr-ag-satg-<job> -p CPUQuota=100% -p MemoryMax=600M -p MemorySwapMax=0 -p RuntimeMaxSec=3600 \
  --nice=10 --working-directory=$W ./driver4.sh <plan file>
bin/satcheck <points> <K>          # fresh exact check; verify/vsat check <points> <K> for the verifier's code
```
