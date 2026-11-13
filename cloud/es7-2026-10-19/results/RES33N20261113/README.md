# RES33N20261113: attacking residual budget 33 (the route to ES(8) ≤ 309), night of 13 November 2026

**No new bound is claimed.** This record documents a discovery run (13 Nov 2026, 02:00–05:40 KST) on the
residual side of the omission proof. Labels used below:
- **CERTIFIED**: a CaDiCaL LRAT proof accepted by cake_lpr ("s VERIFIED UNSAT") for the stated CNF.
- **COMPUTED**: a solver verdict only.
- **HEURISTIC**: search statistics.

Work directory: `/home/jay/research/data/res33-20261113` (not in Git). Tools are copied in `tools/`.

## Why the residual side

ES(8) ≤ 310 comes from (b_B, b_R) = (64, 32): balanced population ≤ 187, residual ≤ 121, and
F(B + R + 2, 8). Raising the residual exclusion to budget 33 (at least 34 holes, n_R ≤ 120) gives
**F(309, 8)**: every 309-point set in general position has a convex octagon.

ES8SLACK showed that the 2,650 proved residual rows admit 33-hole vectors (with h0 = 0). It also found
W0–W2 and a fourth vector V4, which survives the 2,322 instances of the eight existing coupled templates.
So budget 33 needs new geometric rows.

## Method

1. **Coupled owner model as CNF** (`tools/coupled.py`). These are the clause families of the October
   rank-search encoder (`experiments/omission-residual32-rank-search-2026-10-10/cnf_export.py`): label
   thresholds, the source-cup rank bound, empty directions, label domains, order transitivity, cup/cap
   growth, forced triple signs (the six-order bounding-box check), signotope packets and four-point
   convexity. One change: the no-octagon constraint is complete (every 8-subset of owners gets "some
   4-subset is not convex").
   - The state-independent clauses depend only on the support size, so they are cached.
   - A probe takes 0.03–1 s with CaDiCaL 2.1.3, against 12–25 s for the October z3 model.
   - **Controls:** the known cores W1, W2, W4 and the Sixth obstruction are UNSAT; W1 minus one state is
     SAT; the fast and the full encodings give identical clause multisets on 3 random supports.
2. **Loop** (`tools/cegar.py`):
   - CP-SAT finds a vector with h0 = 0, at most 33 holes, satisfying catalog + templates + new rows. It
     searches neighbourhoods of the known vectors first (radius 4/8/12), then globally.
   - Subsets of the occupied set are probed: unions of the "faces" of tight cycle rows, sizes 10–17.
   - UNSAT supports are minimised by deletion to cores.
3. **Template transport** (`tools/transport.py`, `tools/shrink_tests.py`):
   - For each core, the LRAT proof is traced back to the original clauses it uses. The state-dependent ones
     (forced sign, empty direction, excluded label, source bound) are kept and shrunk greedily while the
     CNF stays UNSAT.
   - Every injective map σ from owners to states is then enumerated for which each kept clause is present
     in σ's CNF or implied by it. Implication covers two cases: an excluded label is implied by an empty
     direction, and a source bound by a smaller source height plus the threshold clauses.
   - The same refutation then refutes σ's CNF, so image(σ) is a valid demand-one row.
   - Checked edge case: no state triple has both orientations forced (0 such triples), and the triple
     table is cyclically invariant.
4. **Certification** (`tools/certify.py`): for each row checked, its full CNF is solved with `--lrat` and
   the proof is checked by cake_lpr.

## Results (filled in at the end of the run)

### Vectors refuted (CERTIFIED rows)

All four previously known 33-hole vectors that survive the 2,650 rows (W0–W2 via template rows, V4 via
new cores) are dead. The run found further 33-hole vectors and refuted each one. A vector is "refuted"
when at least one row whose own CNF cake_lpr verified is fully occupied in it:

| vector | origin | F-states occupied | new rows violated | cake_lpr-certified rows violated |
|---|---|---|---|---|
| W0 | ES8SLACK witness | 61 | 0 (killed by the existing template rows: Fourth/Nine instances) | – |
| W1 | ES8SLACK witness | 60 | 5 | 3 |
| W2 | ES8SLACK witness | 61 | 9 | 1 |
| V4 | ES8SLACK template-closure probe | 62 | 13 | 6 |
| N1 | found 02:15 (neighbourhood of V4) | 60 | 9 | 7 |
| N2 | found 02:27 (neighbourhood) | 61 | 12 | 8 |
| N3 | found 03:03 (global CP-SAT) | 62 | 13 | 8 |
| N4 | found 03:49 (global CP-SAT, optimisation mode) | 61 | 12 | 6 |
| N5 | found 04:07 (global CP-SAT, optimisation mode) | 62 | 8 | 8 |
| C59 | 2,650 rows + capacity 59 (HiGHS) | 59 | 7 | 1 |

The hole sets are in `vectors.json` and `capvec.jsonl` of the work directory. The counts are from
`final_summary.py`.

### Rows

- **New rows (all demand 1):** 50,568 in `newrows.json` (work directory).
  - Kinds: 43 minimal cores and 50,525 transported images, from 34 templates (`newtemplates.jsonl`).
  - Sizes: 2,211 rows of 9 states, 15,871 of 13 and 32,486 of 14.
- **CERTIFIED:** 497 rows, each with its own CNF and LRAT proof, all `s VERIFIED UNSAT`
  (`certified.jsonl`, with CNF and LRAT SHA-256). They are:
  - all 43 cores;
  - 449 sampled transported rows;
  - the 5 transported rows that refute the fork's capacity-59 witness (below).
- **Transport check:** 60 of 60 random transported rows were UNSAT when solved directly.
- **LP:** the relaxation over all rows is still 27.0.

### The 9-point order-type lemmas

Three of the cores have only 9 states. Their shrunk templates need no label or rank facts, only
18 forced orientations and 4 forced orders. Each is a statement about order types (signotopes): nine
points, x-ordered, in general position, with no six-cap and no convex octagon, cannot satisfy the listed
facts. The first one, for core [42, 56, 62, 68, 72, 83, 94, 106, 108]:
- p5, p6 lie left of p7, and p2, p3 lie left of p8;
- the triples (0,2,1), (0,2,4), (0,3,1), (1,2,3), (1,2,4), (1,7,3), (1,8,3), (2,4,3), (2,4,5), (2,5,7),
  (2,8,3), (3,4,5), (3,4,8), (3,5,8), (4,5,6), (4,5,8), (5,6,7), (5,6,8) are positively oriented.

That CNF (static clauses plus these 22 facts) is UNSAT, and without the facts it is SAT. The three
lemmas are pairwise non-isomorphic as test sets. Their transports give the 9-state rows.

### Global search for further 33-hole vectors (HEURISTIC)

- **Neighbourhoods:** after N1–N2 were refuted, no 33-hole vector existed within |H \ C| ≤ 12 of any
  of the 12 vectors then known (CP-SAT, 20 s per neighbourhood, so evidence only).
- **Global search:** N3, N4 and N5 each came from fresh random seeds, the last at 04:07 KST. From 04:07 to 05:33
  the finders ran 17 more rounds (400 s each, 2–3 workers). The best was 34 holes in
  every round; the CP-SAT bound stayed at 28.
- **Capacity-capped search:** 5+ rounds with all rows plus h(F) ≥ 25 found nothing below 34 (bound 31).
- **Rate:** a fresh 33-hole vector appeared roughly every 15–45 min of global search, and the loop
  refuted each in about 4 minutes. The integer optimum over the extended rows is unknown, but any
  remaining 33-hole vectors are now hard to find.
- **Size of an exact proof (Knuth estimate).** Random dives of the pbb_strong rule, with strong branching
  K = 8 on the top 8 levels (`knuth_res.py`).
  - Calibration on the 2,650 rows at budget 32 gives 10^7.18 nodes, against 875,159 for the actual 313
    tree built with strong branching K = 40/12. So the cheaper rule overestimates by about 17×.
  - Budget 33 over all rows gives 10^8.51 nodes (74 dives, none hit a 33-hole vector). With the same
    correction that is roughly 10^7.3 nodes (≈ 2·10^7), comparable to or above the 310 balanced tree
    (≈ 1.4·10^7 nodes).

### Capacity tests (COMPUTED, with THEORY310N20261113)

By Lemma A of THEORY310N20261113, the owners of the 84 residual states with f₁ ≥ 5 (the set F) form a
5-cap-free, octagon-free set, so |O ∩ F| ≤ N(cap ≤ 4).
- **Exact thresholds over the 2,650 Lean rows** (THEORY310N20261113 §7b: pbb_strong trees replayed
  in exact integers).
  - Capacity 57 forces ≥ 34 holes; capacity 56 forces ≥ 35.
  - Both are sharp: exact witnesses with 58 F-states and 33 holes, and with 57 F-states and 34 holes.
  - So "every 58-point 5-cap-free set has a convex octagon" implies ES(8) ≤ 309, and the 57-point
    version implies ES(8) ≤ 308.
- **Caveat on HiGHS.** The fork found that HiGHS reported a false optimum at c = 57. Every HiGHS status
  in this record (capacity runs, `hprove`, `lazycap`) is therefore at most COMPUTED, and an
  "infeasible" from HiGHS is not used as evidence.
- **2,650 rows + h(F) ≥ 25 (capacity 59).** HiGHS reports optimum 33 (the fork's
  `cap_mip.py 59`: 132,690 nodes, 1,111 s). Capacity 59 alone therefore does not give 309.
- **That optimum is not geometric.** The 33-hole vector found under capacity 59 (59 F-states occupied)
  violates 6 of the new rows (`capvec.jsonl`).
- **Capacity 59 with all rows.** No 33-hole vector was found by CP-SAT, restricted to h(F) ≥ 25 and
  using all rows. Details are in the search summary above. This is evidence, not proof, that
  N(cap ≤ 4) ≤ 59 together with the new rows would give residual budget 33, i.e. ES(8) ≤ 309.
- **LP side.** The LP-certified threshold is N(cap ≤ 4) ≤ 56 (exact rational dual 100/3 > 33).
- **All known 33-hole vectors** (W0–W2, V4 and the night's) occupy 60–62 of the 84 F-states.
- **Exact capacity 59 with certified rows** (THEORY310N20261113: pbb_strong over 2,650 rows + 492
  certified rows + h(F) ≥ 25).
  - It found an exact 33-hole witness with 59 F-states (`pbbcombo_c59_witness.json`).
  - That witness violates 5 transported rows. At 05:31 all 5 were certified here (`s VERIFIED UNSAT`),
    so it is refuted too.
  - Re-running that exact search with the 497 certified rows is the first step of the next session. If
    it closes, "N(cap ≤ 4) ≤ 59 ⇒ ES(8) ≤ 309" is exact, two points weaker than the Lean-rows-only
    threshold 57.

### Exact-proof attempts (negative)

- **Pure CDCL on the pseudo-Boolean problem.** Budget 32 and budget 33 were encoded with sequential
  counters and k-totalizers (`pbcnf.py`, brute-force self-test on 60 random instances). CaDiCaL ran
  about 11 minutes each and gave no verdict, even on budget 32, which is known UNSAT. Resolution is
  weak at this counting.
- **CP-SAT neighbourhood proofs.** CP-SAT did not settle even radius-6 neighbourhoods within 300 s.
- **HiGHS on all rows.** The dual bound was 28.0 after about 2,300 nodes (13 min).

## What this does and does not show

- Every new row is a valid omission row **if** the CNF encoding is sound. Each clause family is one the
  October Lean development (`CoupledSemantics`, the rank-attainment and template files) already proves for
  actual owners. The complete no-octagon clauses are instances of octagon avoidance. The rows themselves
  are not yet Lean-checked.
- No exhaustive exclusion of 33-hole vectors over the extended rows exists yet. Even if the integer optimum
  is now ≥ 34, ES(8) ≤ 309 needs a branch-and-bound certificate for budget 33 and its Lean check.
  - The LP bound stays at 27.0 with all new rows: demand-one rows of 9–14 states cannot lift a fractional
    optimum that spreads 27 holes thinly over 154 states.
  - So that certificate will be large, comparable to the 310 tree, unless capacity rows (high demand on
    large supports) are found. See THEORY310N20261113 for the ETV-type capacity lever.

## Next steps (ranked)

1. **Capacity route.** The cheapest way to ES(8) ≤ 309. Prove N(cap ≤ 4) ≤ c, the largest 5-cap-free
   octagon-free set, for some c ≥ 56 (THEORY310N20261113, (W1)).
   - At c = 56 the 2,650 proved rows already give LP 100/3 > 33, so a one-leaf certificate suffices.
   - With tonight's rows, c = 59 might suffice; the capacity-capped search is evidence only. Confirming
     it needs an exact MIP or branch-and-bound over all rows plus h(F) ≥ 25.
   - The fork suggests a whole-catalog coupled SAT on the 84 internal states, Schroeder-style.
2. **Residual loop.** Keep it running (`cegar.py` + `finder2.py`) until the global search stops finding
   33-hole vectors for many hours. Then attempt the exact exclusion at budget 33: pbb_strong over the
   extended catalog, cube-split into contexts, with the compact Lean checker. Estimated at about 10^7.3
   nodes.
   - The extended catalog can be thinned first: keep only rows that are ever tight in the tree.
3. **Lean.**
   - Export the 43 cores with the October RUP exporter (`experiments/omission-residual32-rank-search-2026-10-10/search/export_*.py`).
   - Extend the coupled-template Lean files with a `sourceTests` list (heights), because some shrunk
     templates use source-cup clauses. Then transport the template instances in Lean, the same way the
     Fourth/Sixth families were handled.
4. **Performance.** If the exclusion campaign is run, the per-node LP work should move to a compiled
   checker or solver driver (C++/Rust). The Python pbb_strong is the bottleneck at this size.

## Files (work directory `/home/jay/research/data/res33-20261113`)

- `newrows.json`, `newtemplates.jsonl`: the new rows and the templates they come from.
- `certified.jsonl`: per-row cake_lpr verdicts with CNF and LRAT hashes.
- `vectors.json`: the 33-hole vectors found tonight.
- `cegar.log`, `finder.jsonl`: event logs.
- `capvec.jsonl`, `capcond_*.log`: capacity tests.
- `knuth32_base.json`, `knuth33_all.json`: tree-size estimates.
- `static/`: cached clause files.

Large intermediate files (CNFs, LRATs) were deleted after checking, except the partial ones listed in
THEORY310N20261113 §7.

## Novelty check (13 November 2026, about 05:45–06:10 KST)

Sources read:
- Baek, arXiv:2206.04260 (ETV case a = 4).
- Schroeder's preprint v1 (19 Sep 2026, DOI 10.5281/zenodo.22842891), full text.
- Subercaseaux–Mackey–Qian–Heule, arXiv:2506.00224.
- Koshelev–Koshka, arXiv:2604.20120.
- Baek–Balko, "The Erdős–Szekeres conjecture revisited" (SoCG 2025 listing; the JCTA version was blocked).
- Dumitru, arXiv:2512.24061.
- Not read (access blocked): the 2013 DCG paper "Two upper bounds for the Erdős–Szekeres number with
  conditions".

Findings:
- **Capacity reduction.** "Every 58-point 5-cap-free set has a convex octagon ⇒ ES(8) ≤ 309" (and
  57 ⇒ 308) appears in none of these sources.
  - Only the ETV case a = 4 is proved (Baek). Schroeder proves the separate case M₇(5,6) = 25. No source
    bounds M₈(5,·).
  - Schroeder's §7.3 block compression is the same mechanism with two levels: no 4-cap, Baek capacity
    22. His §9 lists "further hereditary capacities" as an open task.
  - So the mechanism extends his. The quantitative reduction, its exact thresholds (57/56) and their
    sharpness are new as far as found.
- **Floor of the additive scheme.**
  - Schroeder §9: C₈ + D₈ + 2 ≥ 114 unconditionally (from D₈ ≥ 50), and in [114, 121] under ETV
    (D₈ ≤ 57).
  - THEORY310N's exact 57-point residual set gives D₈ ≥ 57, so the floor is **121 unconditionally**. This
    is the top of his conditional interval, i.e. it shows ETV's D₈ value is attained.
- **Bounds.** No ES(8) bound below Schroeder's 319 was found apart from this project's 310. The refereed
  bound is still 408 (Nassajian Mojarrad–Vlachos).
- **Symmetric sets.** arXiv:2506.00224 treats symmetric hexagon- and heptagon-free sets (symmetry orders
  2–5) and nothing for k = 8 or 9. So the symmetric k = 8/9 results lie outside it.
- **Small lemmas.** The 9-point lemmas and the coupled-row transport were not checked against
  literature beyond these sources.

## Session 2 (13 November 2026, from 06:35 KST): closing the capacity gap

### Result 1 (exact certificate): capacity 58 forces 34 residual holes

- **Statement.** Every 0/1 vector h on the 154 residual states with h₀ = 0, all 2,650 Lean rows, the 497
  cake_lpr-certified coupled rows (`certified.jsonl`), and h(F) ≥ 26 (at most 58 occupied F-states) has
  at least 34 holes.
- **Certificate.** pbb_strong at budget 33 (K_TOP 16, D_TOP 8, K_LOW 4, 4 processes, 32 contexts):
  60,191 nodes and 30,096 weighted leaves, minimum integer margin 1. It was replayed twice by
  `assemble.py` → `scripts/omission_tree.check_tree` in unbounded integers.
  - The single pending node is the "state 0 missing" branch, discharged by
    `OmissionResidualZeroState.zero_mem_residualOccupied`, as in the 313 tree.
- **Inputs (work directory `cert_c58/`).**
  - Extra rows `capx_c58_i1.json` (SHA-256 `25b9fa73…`): the 497 certified rows plus the capacity row.
  - Context trees `tree_c58_contexts.tar.xz` (SHA-256 `2673611d…`).
- **Check.** Every extra coupled row is a cake_lpr-verified support, and the capacity row is exactly F
  with demand 26.
- **Consequence.** By Lemma A of THEORY310N20261113 (|O ∩ F| ≤ N(cap ≤ 4)): **if every 59-point set in
  general position with no 5-cap contains a convex octagon, then ES(8) ≤ 309.**
  - This is one point weaker than the 58-point version, which used the Lean rows alone.
  - Status: arithmetic exact. The rows are cake_lpr-certified CNFs whose clause families are those of
    the Lean CoupledSemantics development. Not Lean-checked; not refereed.

### Result 2 (exact LP): why at most 66 F-states can be occupied, and why local cores cannot lower it

- **Rows inside F force h(F) ≥ 18, i.e. at most 66 occupied F-states.** This holds for the catalog
  alone and does not change with templates or 50K+ new rows (CP-SAT OPTIMAL; LP = IP = 18).
  - Rows reaching outside F can always be met by holes outside F, so only rows inside F matter.
- **The LP dual is supported on exactly 9 Baek block rows**, 28 states each with demand 6 (capacity
  22): rows 973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315, each with dual weight 1/3.
  - Hence F is exactly 3-covered by these 9 blocks, and 66 = 9 · 22 / 3.
- **Consequences.**
  - A demand-1 core of 9–14 states carries about 2–3 holes in the LP optimum, so cores cannot cut it.
    The F-occupancy loop (`fcegar.py`, 3 rounds, 34 certified cores, 60K transported rows) left the
    optimum at 18, as predicted.
  - Lowering the ceiling to the capacity threshold (≤ 59) would need an average block capacity of about
    19.7 instead of Baek's sharp 22. Since 22-owner abstract models exist for these blocks
    (ES8SLACK p11), the improvement must come from joint constraints across overlapping blocks.
  - That joint statement is in essence the ETV case N(cap ≤ 4) ≤ 59. The "meeting point" of the two
    loops is exactly that statement.
- **A new kind of row.** Demand-2 rows exist. Example:
  T = {25, 33, 43, 44, 53, 55, 67, 74, 77, 79, 85, 89, 91, 96, 107, 110, 111, 125}. Every 17-subset is
  coupled-UNSAT, so at most 16 are occupied. In the current LP optimum x(T) = 3.6, so the row does
  not bind.

### Tree-size estimates for the next capacities (Knuth, calibrated)

Knuth random-dive estimates use the production rule (K_TOP 16, D_TOP 8, K_LOW 4) over the 2,650 rows,
the certified rows (513–514) and the capacity row (`knuth_res.py`).
- **Calibration at c = 58:** estimate 10^4.76 ≈ 57K nodes, against an actual 60,191.
- **c = 59:** 10^5.83 ≈ 0.7M nodes (130 dives, none ending in a 33-hole vector). It was run from 07:11
  KST with 7 + 2 workers.
- **c = 60:** 10^6.66 ≈ 4.6M nodes (66 dives, none ending in a 33-hole vector). That is about 6–8 hours on
  7 workers: an overnight job. pbb_strong resumes per context, so it can run in pieces.
- Each step up in c weakens the hypothesis by one point. The unconditional result would be c = 66,
  because h(F) ≥ 18 is LP-provable. That is the full budget-33 tree, about 10^7.3 nodes.

### Result 3 (exact certificate): capacity 59 forces 34 residual holes

- **Statement.** Every 0/1 vector h with h₀ = 0, all 2,650 Lean rows, 513 cake_lpr-certified coupled rows
  (the 497 above plus 16 F-cores from `fcegar.py`) and h(F) ≥ 25 has at least 34 holes.
- **Certificate.** pbb_strong at budget 33 (same rule, 32 contexts): 819,241 nodes and 409,621 weighted
  leaves, minimum integer margin 1, one pending node (state 0 missing, discharged as before). The Knuth
  estimate had been 0.7M nodes.
  - Replayed twice by `assemble.py` → `check_tree` in exact integers.
  - The run used 7 + 2 workers. The two largest contexts were also split into sub-contexts
    (`pbb_split.py`), but the main run finished them first, so the files are the main run's.
- **Inputs (`cert_c59/`).** Extra rows `capx_c59_i2.json` (SHA-256 `e506e1bf…`; every coupled row
  cake_lpr-verified, the capacity row exactly F with demand 25) and context trees
  `tree_c59_contexts.tar.xz` (SHA-256 `54588936…`).
- **Consequence: if every 60-point set in general position with no 5-cap contains a convex octagon,
  then ES(8) ≤ 309.**
  - This is two points weaker than the 58-point hypothesis that the Lean rows alone need.
  - Status as for Result 1: exact arithmetic, certified rows, not Lean-checked, not refereed.

### c = 60 (in progress, resumable)

- **Witness kills.** The c = 60 region had several easy 33-hole witnesses, each occupying exactly 60
  F-states and each satisfying the certified rows at the time. Every one was killed by pooled
  transported rows that were certified on the spot: 3 by the exact loop and 2 by the CP-SAT pre-killer
  (`capfinder.py`). A final 15-minute pre-killer round on 7 workers (566 unique certified rows) found
  none.
- **Exact run.** Started 09:27 KST (`capcegar.py 60 … 7 128 20`, 128 contexts). At 09:41 a sixth
  witness appeared and was killed, and the run restarted with 570 certified rows (iteration 22). It was
  stopped at 10:16 with **15 of 128 contexts closed** in `capbb_c60_i22/`.
  - Extra-row file `capx_c60_i22.json`, SHA-256 `ad8b7363…`.
- **Resume** (from the repo root, unchanged rows):
  `K_TOP=16 D_TOP=8 K_LOW=4 python experiments/omission-final313-2026-10-11/search/pbb_strong.py 33 7 128 <work>/capbb_c60_i22 <work>/capx_c60_i22.json`,
  then `assemble.py <work>/capbb_c60_i22` for the exact replay.
  - Estimated about 4.6M nodes in all, roughly 6–8 hours on 7 workers.
  - On a WITNESS, kill it (`capcegar.py` does this) and restart with the new rows.


### Session 2 summary (06:35–10:20 KST)

- **Exact conditional results (with certified rows).** Capacity 58 and capacity 59 each force 34 residual
  holes. So **every 60-point 5-cap-free set having a convex octagon would give ES(8) ≤ 309**; the night
  before this needed 58 points.
- **New ETV-type bound (ETV5N20261113, parallel agent): N(cap ≤ 4) ≤ 65.** That is, every 66-point set in
  general position with no 5-cap contains a convex octagon. It improves the earlier internal bound of 71
  and the trivial cup–cap bound of 84; cake_lpr-verified, not Lean-checked.
- **The gap** between the proved bound and the threshold is now 65 vs 59 (6 points). It was 71 vs 57
  (14 points) at the start of the session.
- **Theory (ETVTHY20261113).**
  - PROVED: M(5;8) ≤ 22 + N(8,5,7) and M(5;7) ≤ 41.
  - OPEN, with strong evidence: the Δ-reduction conjecture (every 5-cap-free octagon-free set is a union
    of a 4-cap-free set and a heptagon-free set). It would give 63, and 54 with its level-7 version,
    which would yield ES(8) ≤ 308.
- **Structure.** The F-ceiling of 66 is exactly the 3-fold cover of F by 9 Baek blocks (LP dual), so local
  rows cannot close the gap.
