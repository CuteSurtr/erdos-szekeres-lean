# LP0(7) for real point sets: BFP-CEGAR over block extensions (track D2, 15 November 2026, from 19:00 KST)

**Headline (21:13 KST): LP0(7) is FALSE for a REAL 20-point set (EXACT; claim `lp0-7-false-real`, filed 21:12,
**VS CONFIRMED 21:13** with own code: brute force over all 2^20 subsets, 0 weak Δs through r).**
A second, different real 20-point counterexample on T1's block (claim `lp0-7-false-real-2`, filed 22:00, **VS
CONFIRMED 22:02**).
No 2-point extension (19 points) of the five known real ROOT(7) blocks is a counterexample (CERTIFIED, 765/765
patterns; claims `lp0-7-real-2ext`, `lp0-7-real-2ext-onn`, both VB CONFIRMED).

## Status (final, 22:25 KST; all D2 units stopped)

- **A real LP0(7) counterexample: 20 integer points** (`d2/hit/lp0_7_real20.json`, SHA-256 dd729102…; |coordinates|
  ≤ 28,611). (5,7)-valid; r = 19 lies in no weak Δ (0 of 2^19 subsets); P0 = {0,1,2,3,5,6,11,12,17,18} misses 6
  convex hexagons, e.g. {7,8,9,13,15,16} with 4-caps (0,5,6,7), (0,2,7,8), (0,2,7,9), (1,5,12,13), (1,5,12,15),
  (0,2,15,16). Three independent exact checks from the coordinates agree (own `lp0_real_check.py`, P2's `p2lib`, T1's
  `indep_coords.py`). It is R7's real block `root7_real17` (points 0-4, 7-11, 13-19, same signs, checked) plus three
  new points 5, 6, 12 (pattern `ooooonnooooonooooooo`, gaps 5, 5, 10). Found 21:10:56 by the k = 3 BFP-CEGAR: the
  model's B + z sub-configurations and W itself had no BFP certificate, and `realize_sig.py` realized it in 1.2 s.
  Claim **`lp0-7-false-real`** filed 21:12; **VS CONFIRMED 21:13:53** from the coordinates alone with own code
  (`vslib.py`, `bf_delta.cpp`; 8,734 weak Δs in all, 0 through r, 4,040 through l;
  [VERIFY_LP0_7_FALSE_REAL.md](VERIFY_LP0_7_FALSE_REAL.md)).
- On this S, l = 0 lies in 4,040 weak Δs, so LR(7) and weak D(5,7) hold; ROOT(7) fails (r ends 165 4-caps).
  TWO-ENV#(7) holds on S: ENV#(S − r) = 0 (as it must, r being unrootable) but the mirror side ENV#(μ(S) − μ(l)) ≠ 0
  (P2's `envcount` logic, SAT branch for 19 points; l starts 34 4-caps; `d2/hit/twoenv_p2.json`; EXACT for this S,
  not filed). P2's H7U(7) fails for the real 19-point U = S − r (the hexagon above avoids r and so do its witness
  caps, while U has no ENV# Δ since r is unrootable) — a corollary, not filed separately.
- **S is minimal under single deletions**: none of the 20 sets S − p is an LP0(7) counterexample (own checker,
  `d2/hit/deletions.jsonl`): deleting a new point (5, 6 or 12) leaves r unrootable but no hexagon inside R¹; deleting
  any block point makes r rootable (12-340 weak Δs through r); deleting r gives 6,142 weak Δs through the new
  rightmost point.
- **2-point extensions (19 points): no counterexample** among the 765 position patterns of the five real blocks (713
  base-UNSAT, 52 closed by BFP cuts), **all 765 final CNFs CERTIFIED** by cake_lpr (`s VERIFIED UNSAT`, 765/765, by
  21:10). Claims `lp0-7-real-2ext` (VB CONFIRMED 20:39) and `lp0-7-real-2ext-onn` (VB CONFIRMED 20:48).
- So a real LP0(7) counterexample that contains one of the five known real blocks with the same rightmost point has at
  least 20 points, and S shows 20 suffice. The least real counterexample overall has at most 20 points; whether one
  exists with 15-19 points is open (no single deletion of S is one, above).
- A third real counterexample (T1's block, pattern (5,5,7), its only R¹-hexagon {9,10,11,14,16,19} contains r):
  claim `lp0-7-false-real-3` (filed 22:21; **VS CONFIRMED 22:22**, own code, 2^20 brute force: 0 weak Δs through r,
  [VERIFY_LP0_7_FALSE_REAL_3.md](VERIFY_LP0_7_FALSE_REAL_3.md)). See the k = 3 results.
- All D2 units are stopped (last one 22:21); no unit is running. No memory-guard stop of a D2 unit (guard log
  `memguard-20261115ev.log`: only LIFT lines for `esr-age-*`).
## The real counterexample S (20 points, indices 0-19 in increasing x)

```
(-15537, -266), (-8403, -690), (-3735, 2710), (-3607, -968), (-3605, -1128), (563, 15010), (578, 14913), (583, 1396), (588, -1112), (803, -1226), (856, -1269), (860, 13590), (4070, 18359), (4083, 8416), (4105, -1297), (10248, -1438), (10324, -1565), (10348, 27827), (10804, 28611), (15537, -10027)
```

- New points (not in R7's block): 5, 6, 12. Block points: 0-4, 7-11, 13-19 (signs equal to `r7/root7_real17.json`).
- (5,7)-valid; 312 4-caps; 1,011 convex hexagons; r = 19 ends 165 4-caps and lies in no weak Δ; P0 =
  {0,1,2,3,5,6,11,12,17,18}; the 6 hexagons avoiding P0: {7,8,9,13,15,16}, {7,8,10,13,15,16}, {7,8,13,14,15,16} and
  three more (`d2/hit/check_p2lib.json` lists the first three). l = 0 lies in 4,040 weak Δs; S has 8,734 weak Δs in
  all (VS).
- P1's C2(7) holds on S (l starts 8 six-cups, e.g. (0,1,3,7,13,17)); C1(7) is not tested by S (r ends no 6-cup; it
  ends 4 five-cups). Longest cup: 6 (`d2/hit/cups_c1c2.json`).

## A second real counterexample S2 (T1's block, 20 points)

```
(-82222, 4108), (-39432, 90), (-18983, 12880), (-18786, -1835), (-18782, -2658), (-776, 63672), (-358, 60998), (-350, -2731), (-349, -3031), (444, -3633), (707, -3855), (713, 56391), (14898, 75167), (14917, 34097), (14946, -4366), (40334, -5663), (40545, -6291), (40576, 109378), (45688, 116317), (82222, -71926)
```

- Found 21:59:45 (`run_k3o`, pattern `ooooonnooooonooooooo` on T1's `m17_it4_real`; no BFP certificate on the model,
  realized by `realize_sig.py` in 1.5 s). `d2/hit/lp0_7_real20_t1it4.json`, SHA-256 3692cfc9…; |coordinates| ≤ 116,317.
- (5,7)-valid; 326 4-caps; 1,055 hexagons; r = 19 ends 159 4-caps and lies in no weak Δ; P0 =
  {0,1,2,3,5,6,11,12,17,18} misses 5 hexagons (e.g. {7,8,9,13,15,16}); l = 0 lies in 3,329 weak Δs. Three exact
  checks agree (own, P2's `p2lib`, T1's `indep_coords.py`); S2 − {5,6,12} has T1's block signs; S2 is a different
  order type from S (VS: 1,055 vs 1,011 hexagons; labelled signs differ in 10 triples). Claim
  **`lp0-7-false-real-2`** filed 22:00; **VS CONFIRMED 22:02** with own code (6,768 weak Δs in all, 0 through r,
  3,329 through l; [VERIFY_LP0_7_FALSE_REAL_2.md](VERIFY_LP0_7_FALSE_REAL_2.md)).

## Statement

LP0(n): for a (5,n)-valid set S with rightmost point r, either r lies in some weak Δ of S, or P0 (the points of S
that end no 4-cap) meets every gon (convex (n−1)-set). A counterexample is a (5,n)-valid S with r in no weak Δ and a
gon all of whose points end a 4-cap. P2 found 19-point abstract counterexamples at n = 7 (claim
`lp0-7-false-abstract`, CONFIRMED); R7 showed that all 108 models of P2's scan have no x-sorted realization (claims
`lp0-7-realblock-nonreal`, `lp0-7-scan-all-nonreal`, CONFIRMED). The question here: is LP0(7) false for some REAL
point set? This track searches the extensions W = B + 2 points of the five known real right-hostile 17-point blocks B
(order type of B fixed, coordinates free; no new point right of r), then W = B + 3 points.

## Model and soundness

- **Blocks** (copied to `d2/blocks/`, SHA-256 in Files): R7's `root7_real17` (`r7real`), T1's `m17_it4_real`
  (`t1it4`), `m17_it5_real` (`t1it5`), `m17_it6_real` (`t1it6`), R7's `div17/real/m17_it3_s1` (`r7it3`). In each, r
  lies in no weak Δ. By Lemma M (claim `t4-lemmas`; it is immediate: a weak Δ of W meets B in a weak Δ of B) r stays
  unrootable in every (5,7)-valid W ⊇ B with max W = r. So such a W fails LP0(7) iff it has a convex hexagon made of
  4-cap end points.
- **Base CNF**: P2's `lp0ext.py` (copied): one variable per triple of W (true = cup), B's triples fixed, signotope
  axiom, no 5-cap and no convex 7-set on the subsets meeting a new point, and "some 6-subset is convex and each of its
  points ends a 4-cap" (one-way indicator variables). Every real x-sorted W of the stated form satisfies it.
- **BFP cuts**: for a model W, a biquadratic-final-polynomial certificate (three-term Grassmann–Plücker inequalities
  with positive integer multipliers summing to the zero form; with the vertical point at infinity V, [a,b,V] = + for
  a < b) on a sub-configuration shows that no x-sorted real configuration has those signs on the certificate's
  brackets. The cut forbids that partial sign pattern at every increasing placement and under the four reflections
  (identity; y ↦ −y: all point signs negated, V brackets unchanged, every GP relation keeps or flips all three terms
  together; x ↦ −x with reversed labels: s′(a,b,c) = s(m−1−c, m−1−b, m−1−a), every bracket including V brackets
  negates, so each term keeps its sign; and both). Brackets inside the fixed block are evaluated (placement skipped
  if they disagree, dropped if they agree). A pattern matching entirely inside a real block raises an error (never
  happened). Every certificate is verified exactly (`bfp.verify_certificate` and `t1lib.check_cert`) on its own
  sub-signature before its cut is used, and re-verified whenever the library is loaded.
- Hence: CEGAR UNSAT for a pattern = no real x-sorted W of that pattern over B's order type fails LP0(7) (label
  COMPUTED: pysat CaDiCaL verdict; the final CNF can be certified by cake_lpr, see Results).

## Method

- `tools/lp0cegar.py` (driver), `tools/d2lib.py` (HiGHS LP for the BFP search with greedy shrinking, exact
  certificate from the LP support, cut matching against the fixed block), `tools/lp0_real_check.py` (own exact LP0
  check from integer coordinates, for any realized model).
- Per model: BFP on B + z for each new point z (cached), then on W; a model without certificate goes to
  `realize_sig.py` (search only) and is then blocked by a HEURISTIC clause (an UNSAT after such a block is not a proof).
- Shared obstruction library `run_k2b/library.jsonl`: every certificate is cut in every later pattern.
- Calibration (search statistics only): the BFP LP on B + z (18 points + V, about 116,000 columns) takes 30-50 s;
  certificates found for B + z need 15-17 of the 18 points and V in most cases (9 points without V in two cases).

## Results

### Structure of the problem (search statistics, exact SAT enumeration; R7's block)

- Valid 1-point extensions of R7's block (abstract sign vectors of the new point): gap 1: 204, gap 2: 332, gap 3: 166,
  gap 4: 110, gap 5: 115, gap 15: 242 (gap i = between old points i−1 and i).
- LP0 extension models per 2-point pattern (all models, distinct B + z vectors): `onn` 3,276 (204); `oonn` 204 (204);
  `oonon`, `oonoon`, `oonooon` 204 (205); `ooonn` 136 (136); `ooonon`, `ooonoon` 136 (137); `oooonn` 68 (68);
  `oooonon` 68 (69); `ooooonn` 68 (68). In the mixed patterns the point in the later gap has a single vector, so one
  obstruction for it closes the pattern. Union over the 11 patterns: 680 distinct B + z vectors.
- With the first 10 obstructions, 139 of the 204 valid gap-1 vectors and 317 of 332 gap-2 vectors survive the cuts.

### 2-point extensions: patterns closed (run `run_k2b`, 19:49-20:27)

Per block, 153 position patterns (two new points in gaps 0-16, gap i = just before old point i; none right of r).

| block | base CNF UNSAT (no abstract LP0 extension) | closed by BFP cuts | open |
|---|---|---|---|
| T1 `m17_it4_real` | 143 | 10 | 0 |
| T1 `m17_it5_real` | 143 | 10 | 0 |
| T1 `m17_it6_real` | 143 | 10 | 0 |
| R7 `root7_real17` | 142 | 10 | 1 (`onn`) |
| R7 `div17/real/m17_it3_s1` | 142 | 10 | 1 (`onn`) |

- The 10 cut-closed patterns are the same in every block: `oonon`, `oonoon`, `oonooon`, `ooonon`, `ooonoon`, `oooonon`,
  `ooooonn`, `oooonn`, `ooonn`, `oonn` (new points in gaps 2-5). Only 6 obstructions were needed for them: 2 for
  `oonn` and 2 for `oonoon` of R7's block, 2 for `oonon` of T1's it4 block; every other cut-closed pattern closed from
  the library at once (the matching maps a certificate found for one block and gap to other blocks and gaps). The
  library at 20:28 has 32 entries; the other 26 come from the open `onn` patterns (20 on R7's block over several
  restarts, 6 on the div17 block).
- The certificates: B + z sub-configurations (one new point) with 9-18 points, mostly with V. In the gap-1 pattern
  `onn` they need 15-18 points (block point 5 is the only one usually left out), so each cut excludes only one or two
  of the 204 valid gap-1 vectors of the new point; 600 s per block in pass 1 (3 iterations each, 2-4 minutes per
  iteration) did not close it; pass 2 (1,200 s each) is running.
  With the first 28 entries, 83 of the 204 valid gap-1 vectors of R7's block survive.
- No model reached the realizer: every model met a certificate (no BFP-feasible model at all).
- Label: COMPUTED for every closed pattern (pysat CaDiCaL), CERTIFIED where cake_lpr accepted the final CNF (base CNF
  for the base-UNSAT patterns, base + all library cuts for the cut-closed ones). **Final (21:10): 765 of 765 printed
  `s VERIFIED UNSAT`**, each `.cake.out` with exactly one such line; none rejected (`cert_k2b/certify_jobs.jsonl`).
  The two `onn` patterns closed later (20:38 and 20:43, with 8- and 13-point certificates for the second new point)
  and were certified at 20:40 and 20:44.

### 3-point extensions (20 points) of R7's block (from 20:47; in progress)

- Pattern scan (`scan_lib.py`, run_k3b/scan2.jsonl, 20:52-20:58, library of 43 entries): of the 969 position patterns
  (three new points in gaps 0-16), **765 have no abstract LP0 extension** (base CNF UNSAT) and **82 are closed by the
  library cuts alone**; **122 remain** (COMPUTED, pysat). The 122 are (1,1,x), (1,2,x), (1,3,x), (2,2,x), (2,3,x),
  (3,3,x) for many x, (a,b,7-10) with a,b in 1-5, and a new family with two or three points in gap 7: (x,7,7) for
  x = 2-7.
- CEGAR on the 122 (`jobs_k3_open.txt`, gap-7 family first; unit `esr-age-k3d` from 20:59): (7,7,7) closed with one
  11-point certificate (no V) for its last new point; the other (x,7,7) closed from the library at once. (Updated
  below.)
- One B + z sub-configuration had no BFP certificate: the gap-16 point of a (1,2,16) model (HiGHS found the LP
  infeasible, with and without V; search information only). It is cached as BFP-feasible; that model was excluded by
  a certificate for its gap-2 point instead.
- **(5,5,10), iteration 2 (21:00-21:10): the first BFP-feasible model.** Its three B + z sub-configurations (new
  points 12, 6, 5) and W itself (20 points + V, 297 s) had no BFP certificate; `realize_sig.py` (seed 1) realized it
  at once (start 0, 12-bit rounding, 1.2 s), and the driver's exact check (`lp0_real_check.py`) found LP0(7) false:
  **the real counterexample S of the Status section**. The model is then blocked by a heuristic clause and the run
  goes on (more real counterexamples may follow; they are listed below if found).
- **State of R7's block at 21:47 (k = 3 run stopped then; COMPUTED, nothing certified for k = 3):** of the 969
  patterns, 765 base-UNSAT + 82 closed by the library + 15 closed by the CEGAR = **862 closed**; **1 pattern has a real
  counterexample** ((5,5,10), the set S); 6 stopped without verdict at their time cap ((1,2,16), (3,3,14), (3,3,15),
  (3,3,16), (4,4,10), (4,5,10)); 100 of the 122 not reached. CEGAR-closed: (7,7,7), (x,7,7) for x = 2-6, (4,4,7-9),
  (4,5,7-9), (5,5,7-9). Library at the end: 63 entries (`run_k3b/library.jsonl`).
- From 21:15 to 21:36 a small unit (`esr-age-k3o`, 15 % CPU) tried the hit-like patterns (5,5,7-10), (4,5,9-10),
  (4,4,9-10) on the other four blocks; too slow at that quota (one iteration), stopped. From 21:47 to 22:21 the same
  job list ran at 100 % (`esr-age-k3o2`, library merged to 64 entries, 76 at the end) on T1's `m17_it4_real` only
  (the other three blocks were not reached):
  - (5,5,10): **real counterexample S2** at iteration 5 (21:59:45; claim `lp0-7-false-real-2`, VS CONFIRMED);
  - (5,5,9), (5,5,8): closed by the CEGAR (COMPUTED);
  - (5,5,7): **real counterexample S3** at iteration 1 (22:18-22:20; `d2/hit/lp0_7_real20_t1it4_b.json`, SHA-256
    9e5efcff…; (5,7)-valid, r unrootable (0 of 2^19), P0 misses exactly one hexagon {9,10,11,14,16,19}, which contains
    r; 295 4-caps, 1,042 hexagons; l in 3,655 weak Δs; three exact checks agree; claim `lp0-7-false-real-3` filed
    22:21, VS CONFIRMED 22:22);
  - (4,5,10): stopped without verdict (7 iterations, 7 obstructions).
- So real LP0(7) counterexamples arise from both R7's and T1's it4 block by three points in gaps 5, 5 and 7 or 10;
  in every one the two gap-5 points make block points end new 4-caps (witness caps (0,5,6,·), (1,5,12,·) or
  (0,5,12,·)).

## Controls

- `lp0_real_check.py` on R7's real block: 306 hexagons, 0 weak Δs through r, P0 meets every hexagon (LP0 holds);
  on its mirror: 48 hexagons avoid P0, 4,316 weak Δs through r (LP0 holds). Matches P2/R7.
- Cut soundness on real configurations (`ctl_cuts.py`): every library cut for the layout is evaluated on the exact
  sign vector of (a) a real block with two of its own points re-placed as the "new" points (all adjacent pairs in gaps
  1-7 plus random pairs) and (b) random real 2-point extensions of each real block. Final 41-entry library: 17,945
  clauses on 120 real configurations, **0 falsified** (`d2/controls/ctl_cuts_final41.json`). Earlier libraries: 561
  clauses / 92 configurations and 9,143 / 205, 0 falsified.
- Positive control (`ctl_positive.py`): 3 real (5,7)-valid insertions into gap 15 of R7's block (random integer
  points, exact checks) all satisfy P2's validity CNF plus the library cuts for that layout (pysat with the real signs
  as assumptions).
- The two placement enumerations agree: `dump_cnf.py` (plain loop over all placements) produces the same number of cut
  clauses per pattern as the driver's backtracking matcher in every certified cut-closed pattern checked (e.g. 115,
  206, 226, 110, 92, 100, 82, 114, 119, 212 for R7's ten).
- A pattern matching entirely inside a real block would raise an error in the matcher: never happened (every
  library entry is matched against all five real blocks in every job).
- Independent check by VB (claim `lp0-7-real-2ext`, CONFIRMED 20:39): own block checks, own exact certificate checks
  (32/32), all 5,656 cut clauses of 44 cut-closed patterns re-derived, own base encoding (25/25 sampled base-UNSAT
  patterns UNSAT; 32/32 cut-closed patterns SAT without cuts and UNSAT with them), 88 own CNFs certified, fresh
  cake_lpr on 6 of D2's proofs ([VERIFY_LP0_7_REAL_2EXT.md](VERIFY_LP0_7_REAL_2EXT.md)).

## Files (work directory `/home/jay/research/data/roadmap-20261115/pm1115/d2/`, not in Git)

- `blocks/{r7real,t1it4,t1it5,t1it6,r7it3}.json` (copies; SHA-256 d9b5e6c4…, 86b97e77…, c77245a1…, 729a343f…,
  194dbdef…; full hashes in `claims/SHA256SUMS_tools_blocks.txt`).
- `tools/`: `lp0ext.py`, `p2lib.py` (P2's, unmodified copies), `t1lib.py`, `bfp.py` (T1's, unmodified), `realize_sig.py`
  (round6, unmodified), own: `d2lib.py`, `lp0cegar.py` (driver; edited during the run for search speed only: shrink
  settings, conflict-guided small tests, R1-witness test, one new point per iteration; evidence never depends on the
  driver version, since every CNF is regenerated by `dump_cnf.py` from the exactly re-verified library),
  `dump_cnf.py`, `certify_jobs.py`, `lp0_real_check.py`, `ctl_cuts.py`, `ctl_positive.py`, `count*.py`, `scan_lib.py`,
  `summ.py`. Hashes: `claims/SHA256SUMS_all.txt`.
- `run_k2b/`: `jobs.jsonl` (765 patterns: state, iterations, obstructions), `library.jsonl` (41 entries at the end of
  k = 2), `models.jsonl`, `cegar.log`. Frozen copies: `claims/library_k2_2028.jsonl` (32 entries, SHA-256 26d01658…),
  `claims/library_k2_final_2044.jsonl` (41 entries, SHA-256 93682c97…).
- `cert_k2b/`: per pattern `<block>_<pattern>.cnf`, `.cuts.jsonl` (provenance), `.lrat.zst`, `.cake.out`, `.cadical.log`;
  `certify.jsonl` (CNF and LRAT SHA-256, verdict lines) and `certify_jobs.jsonl`; `library_snapshot_*.jsonl` (the
  library each CNF was generated from).
- Earlier, superseded attempts (kept, not evidence): `test1/`, `run_k2_try1/`, `run_k2_try2/`, `run_k2/` (slower
  settings; their obstructions were merged into `run_k2b/library.jsonl` after re-verification), `run_k3/` (aborted k = 3
  start and a partial pattern scan `scan.jsonl`), `run_sat1/` (aborted gap-2 saturation attempt, 1 obstruction).
- `hit/`: the three real counterexamples (`lp0_7_real20.json` = S, `lp0_7_real20_t1it4.json` = S2,
  `lp0_7_real20_t1it4_b.json` = S3) with the exact check outputs `check_own*.json`, `check_p2lib*.json`,
  `check_t1indep*.json`, plus `deletions.jsonl` (S), `twoenv_p2.json`, `cups_c1c2.json` (S).
- `run_k3b/` (k = 3 on R7's block: `scan2.jsonl` pattern scan, `jobs.jsonl`, `library.jsonl` 63 entries, `HIT_*.json`,
  `feasible/` model + realization), `run_k3o/` (k = 3 hit-like patterns on T1's it4 block; library 76 entries; two
  `HIT_*.json`).
- `claims/`: the filed claim JSONs (`lp0-7-real-2ext`, `lp0-7-real-2ext-onn`, `lp0-7-false-real`, `-2`, `-3`).

## What remains

- k = 3 (20 points): R7's block has 862 of 969 patterns closed (COMPUTED), 1 with a real counterexample, 6 without
  verdict, 100 not reached; T1's it4 block: only 5 hit-like patterns tried (2 real counterexamples, 2 closed, 1 open);
  T1's it5, it6 and R7's div17 block not tried at k = 3. Nothing at k = 3 is certified (not needed for the
  counterexamples, which are EXACT from coordinates).
- Larger extensions (k ≥ 4), new points to the right of r (then Lemma M does not apply), and hostile blocks other than
  these five real ones were not searched. A real LP0(7) counterexample need not contain any of the five blocks.
- Gap saturation (no realizable (5,7)-valid insertion at a gap) was tried for gap 2 of R7's block and stopped (one
  obstruction in 3 minutes; 281 of 332 valid gap-2 vectors survived the 28-entry library). With the final library 33
  of R7's 204 valid gap-1 vectors and 3 of the second point's vectors were left when `onn` closed; a full saturation
  statement would need every valid vector excluded.
- Certification: done for k = 2 (765/765). The smallest real LP0(7) counterexample size (15-20) is open; the
  counterexamples found are minimal under single deletions (S checked; S2, S3 not checked).

## Resume

```bash
D2=/home/jay/research/data/roadmap-20261115/pm1115/d2; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd $D2
U="systemd-run --user -p CPUQuota=85% -p MemoryMax=1700M -p MemorySwapMax=0 -p RuntimeMaxSec=<s> --nice=10 --working-directory=$D2 -E OPENBLAS_NUM_THREADS=1 -E OMP_NUM_THREADS=1 -E MKL_NUM_THREADS=1"
# CEGAR (resumable: finished jobs, library, B+z cache and heuristic blocks are reloaded)
$U --unit=esr-<prefix>-k3 $PY -u tools/lp0cegar.py jobs_k3_r7real_b.txt run_k3b <deadline_epoch> 240 45 2
$U --unit=esr-<prefix>-k3r $PY -u tools/lp0cegar.py jobs_k3_rest.txt run_k3r <deadline_epoch> 240 45 2   # copy run_k3b/library.jsonl first
# certification of closed patterns (ALL=1 also certifies base-UNSAT patterns, with an empty library)
systemd-run --user --unit=esr-<prefix>-cert -p CPUQuota=15% -p MemoryMax=300M -p MemorySwapMax=0 -p RuntimeMaxSec=<s> --nice=10 --working-directory=$D2 -E ALL=1 $PY -u tools/certify_jobs.py run_k2b cert_k2b <deadline_epoch> 150
$PY tools/summ.py run_k2b                                       # states per block
$PY tools/count_onn.py blocks/r7real.json <pattern> run_k3b/library.jsonl   # models left under the cuts
$PY tools/ctl_cuts.py <library> 8 10 3 blocks/*.json            # cut soundness control
```
