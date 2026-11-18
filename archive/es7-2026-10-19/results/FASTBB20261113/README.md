# FASTBB20261113: compiled branch-and-bound finders `fastbb` / `fastbb2`; slices 20 (second tree), 21, 22 and capacity 60 closed by exact trees (tracks G and G2, 13–14 November 2026)

## 0. Headline (status at 01:35 KST, 14 Nov; rewritten from the interim versions of 19:15 and 20:50–01:15)

- **Slice 21 (pair (63, 58)) is CLOSED — EXACT TREE** (22:22 KST, 13 Nov): 19,333,541 nodes, 9,666,771 leaves,
  minimum integer margin 1, one pending leaf (state 0 missing), over the 2,650 Lean rows, the slice's two capacity rows
  and 643 cake_lpr-CERTIFIED coupled rows; replayed twice by two wrappers around the unchanged `check_tree`
  (identical counts).
- **Slice 22 (pair (62, 59)) is CLOSED — EXACT TREE** (01:07 KST, 14 Nov): 32,328,319 nodes, 16,164,160 leaves,
  minimum margin 1, one pending leaf, over the Lean rows, its two capacity rows and 755 certified coupled rows; replayed
  twice by the two wrappers (identical counts, 01:12).
- Neither tree has been replayed by another track yet.
- **Capacity 60 is CLOSED — EXACT TREE** (phase-1 tree of 19:37, replayed in phase 2): every slice t ≥ 24 is closed.
- **Consequence (§1.5): a second route to ES(8) ≤ 309, one that needs neither N66 ≤ 58 nor 57 nor 56.** The write-up is
  ES309N20261113 (audited by VERIFY309N20261113; its simplest chain uses N66 ≤ 56 and slices 18–19 over the Lean rows
  alone). Here, with LO33N20261113's slices 19 and 20, the slices 21 and 22 close the pair (65, 59), so ES(8) ≤ 309
  also follows under the hypotheses (a)–(g) of §1.5 from **N5 ≤ 65 and N66 ≤ 59, both independently confirmed**
  (VERIFY_N5.md, VERIFY_N66.md), without N66 ≤ 58/57/56. Labels of the inputs: Lean theorems, written proofs,
  cake_lpr-CERTIFIED CNFs with written encoder arguments (the residual coupled encoder audited in VERIFY309N (c)),
  EXACT TREES. Beyond the Lean-checked ES(8) ≤ 310 nothing is Lean-checked; nothing is refereed; **the slice-21 and
  slice-22 trees have not been replayed by another track.** This record claims no bound of its own beyond the
  conditional statement of §1.5.
- **All 755 coupled rows of slices 21 and 22 have kept proofs** (CNF + LRAT, zstd): 705 re-certified 01:12–01:15 (705/705
  cake_lpr `s VERIFIED UNSAT`, regenerated CNF and LRAT SHA-256 equal to the recorded ones for all 705), 50 kept when
  they were certified (§3.3).
- **Slice 20 (pair (64, 57)), second tree with this engine: CLOSED — EXACT TREE** (01:32 KST): 3,044,395 nodes,
  1,522,198 leaves, minimum margin 1, one pending leaf, 755 certified coupled rows, no witness met; replayed twice,
  identical counts (LO33N's tree of the same slice: 3,468,657 nodes, 578 rows).
- **Still running** (autonomous unit `nov13c-g-chain9`, 5 threads, deadline 05:55 KST, 14 Nov): slice 23 (pair
  (61, 60), from 01:33). Results appear in `W/p2/runs/s<T>/` (`status.json`, `DONE.json` / `STUCK.json`,
  `replay2_compare.json`) and `W/p2/proofs/summary.json`, and **are summarized automatically in
  `data/AUTO_RESULTS.md`** (rewritten by the chain after every step and every 10 minutes); see §8. **Until
  `data/AUTO_RESULTS.md` says otherwise, slice 23 is open.**

Labels: **PROVED** (written proof), **CERTIFIED** (CaDiCaL 2.1.3 LRAT accepted by cake_lpr, `s VERIFIED UNSAT`, for a
stated CNF), **EXACT TREE** (every leaf margin recomputed in unbounded integers by the unchanged
`scripts/omission_tree.check_tree`), **COMPUTED** (a program's output that was not replayed), **HEURISTIC**
(statistics, estimates). The interim record of 19:15 called replayed trees "CERTIFIED"; they are EXACT TREES
(VERIFY_G.md §4.1).

W = `/home/jay/research/data/fastbb-20261113` (work directory, not in Git; phase-2 files in `W/p2/`).
W_lo = `/home/jay/research/data/lo33-20261113`. `tools/`: every script and source used here. `data/`: small result
files, frozen copies of the extra-row files, SHA-256 values.

---

## 1. Statements

### 1.1 Slice 21 — EXACT TREE

Every 0/1 vector h on the 154 residual states with h₀ = 0 that satisfies the 2,650 Lean rows, h(F) ≥ 21, h(Lo) ≥ 12 and
the 643 coupled rows of `data/s21_extra.json` has at least 34 holes. (F = the 84 states with f₁ ≥ 5, Lo = the other
70.) Tree in `W/p2/runs/s21/bb/`; numbers and hashes in §4.5 and §6.

### 1.1b Slice 22 — EXACT TREE

Every 0/1 vector h on the 154 residual states with h₀ = 0 that satisfies the 2,650 Lean rows, h(F) ≥ 22, h(Lo) ≥ 11 and
the 755 coupled rows of `data/s22_extra.json` has at least 34 holes. Tree in `W/p2/runs/s22/bb/`; numbers and hashes in
§4.6 and §6.

### 1.1c Slice 20 (second tree, this engine) — EXACT TREE

Every 0/1 vector h with h₀ = 0, the 2,650 Lean rows, h(F) ≥ 20, h(Lo) ≥ 13 and the 755 coupled rows of
`data/s20_extra.json` (the same coupled rows as slice 22) has at least 34 holes. Tree in `W/p2/runs/s20/bb/`.

### 1.2 Capacity 60 — EXACT TREE

Every 0/1 vector h with h₀ = 0, the 2,650 Lean rows, the 606 coupled rows of `data/capx_c60_i23.json` and h(F) ≥ 24 (at
most 60 occupied F-states) has at least 34 holes. Equivalently (LO33N Lemma S) every slice t ≥ 24 is closed.
Conditional consequence, same status as RES33N Results 1 and 3: **if every 61-point set in general position with no
5-cap contains a convex octagon (N5 ≤ 60), then ES(8) ≤ 309** — one point weaker than RES33N Result 3 (capacity 59).

### 1.3 Slices 18 and 19 again (validation of the slice engine) — EXACT TREES

On LO33N's own extra-row files (2 capacity rows + 578 coupled rows): slice 18, 3,891 nodes; slice 19, 180,241 nodes;
both minimum margin 1, one pending leaf (LO33N's trees: 3,611 and 167,509 nodes).

### 1.4 Phase 1: capacities 58 and 59 — EXACT TREES (confirmed by VERIFY_G.md)

V1: rows of `capx_c58_i1.json` (h(F) ≥ 26), 28,735 nodes, 14,368 leaves, minimum margin 1, 1 pending. V2: rows of
`capx_c59_i2.json` (h(F) ≥ 25), 407,101 nodes, 203,551 leaves, minimum margin 1, 1 pending. These reproduce RES33N's
Results 1 and 3 with smaller trees (RES33N: 60,191 and 819,241 nodes).

### 1.5 What follows for ES(8)

**Statement.** Every set of 309 points in general position in the plane contains 8 points in convex position:
**ES(8) ≤ 309** — under exactly the hypotheses (a)–(g). Status: the deduction is PROVED (written below); its inputs are
Lean theorems (a), written proofs (b), (e), cake_lpr-CERTIFIED computations whose encodings are written arguments in
their records (c), (d), (g), and EXACT TREES (f). Nothing beyond (a) is Lean-checked; nothing is refereed.

Two variants, both complete since 01:07 KST, 14 Nov:
- **Variant 59** (preferred: its capacity inputs are the independently verified ones): N5 ≤ 65 and **N66 ≤ 59**, pair
  (65, 59), slices **19, 20, 21, 22**.
- **Variant 58**: N5 ≤ 65 and N66 ≤ 58 (not yet independently checked), pair (65, 58), slices 19, 20, 21.
Below, (d), (e), (f) and the deduction are written for variant 58; for variant 59 replace 58 by 59, 21 by 22 and
h(Lo) ≥ 12 by h(Lo) ≥ 11.

- (a) **Lean-checked** (the ES(8) ≤ 310 development; compact checker `experiments/omission-compact-checker-2026-11-05`,
  commit 408c08856): an octagon-free set S in general position satisfies |S| ≤ 1 + n_H + n_R with n_H ≤ 187, and
  n_R ≤ 154 − Σh, where the residual hole vector h has h₀ = 0 (`OmissionResidualZeroState.zero_mem_residualOccupied`)
  and satisfies the 2,650 Lean rows; moreover Σh ≥ 33 (`Final313.residual_excludes_2650_zero`,
  `experiments/omission-final313-2026-10-11/Final313/Final.lean`).
- (b) **PROVED** (THEORY310N20261113 §2, Lemma A): the owners of the occupied F-states form a set with no 5-cap and no
  convex octagon, those of the occupied Lo-states a set with no 6-cap, no 6-cup and no convex octagon. Hence
  h(F) ≥ 84 − N5 and h(Lo) ≥ 70 − N66.
- (c) **N5 ≤ 65** (ETV5N20261113: "PROVED modulo the written arguments of §2 and the encoders; every computational step
  CERTIFIED by cake_lpr or re-checked exactly"; independently confirmed, VERIFY_N5.md).
- (d) **N66 ≤ 59** (N66N20261113 §4.1, CERTIFIED at 18:11 KST; **independently confirmed**, VERIFY_N66.md) for
  variant 59; **N66 ≤ 58** (N66N20261113 §7.2, CERTIFIED at 20:56 KST, trimmed CNF SHA-256 `424f3304…`, LRAT
  `8c80abac…`; not independently checked as far as this record knows) for variant 58. (N66 ≤ 57 and N66 ≤ 56 are
  also CERTIFIED and were independently confirmed in VERIFY309N20261113; with them slices 18–20, resp. 18–19, suffice:
  that is the chain of ES309N20261113.)
- (e) **PROVED** (LO33N20261113 §2, Lemma S, using (a); independently confirmed, VERIFY_LO.md): the pair (65, 58) is
  closed iff the slices t = 19, 20, 21 are closed (max(18, 84 − 65) = 19 ≤ t ≤ 58 − 37 = 21); the pair (65, 59) iff
  the slices 19–22 are closed.
- (f) **EXACT TREES**, each over the 2,650 Lean rows, the slice's two capacity rows and cake_lpr-certified coupled rows,
  each with one pending leaf (state 0 missing, covered by (a)):
  - slice 19: LO33N20261113 §4a, 167,509 nodes, minimum margin 1, 578 coupled rows (independently replayed,
    VERIFY_LO.md); also closed here on the same rows (180,241 nodes, §1.3);
  - slice 20: LO33N20261113 (`W_lo/bb_64_57`, replay at 20:29:53), 3,468,657 nodes, 1,734,329 leaves, minimum margin
    1, 578 coupled rows (independently replayed, VERIFY309N20261113 (b)); also a second tree here (§1.1c), 3,044,395
    nodes, 755 coupled rows;
  - slice 21: §1.1 of this record, 19,333,541 nodes, 9,666,771 leaves, minimum margin 1, 643 coupled rows (replayed
    twice here; not yet independently replayed);
  - slice 22 (variant 59 only): §1.1b of this record, 32,328,319 nodes, 16,164,160 leaves, minimum margin 1, 755
    coupled rows (replayed twice here, identical counts; not yet independently replayed).
- (g) **CERTIFIED rows**: every coupled row is a support S whose coupled owner-model CNF (RES33N20261113, Method 1: the
  clause families of the October rank-search encoder with a complete no-octagon constraint) has a CaDiCaL 2.1.3 LRAT
  proof accepted by cake_lpr; its meaning — no residual configuration occupies all of S, so h(S) ≥ 1 — rests on the
  soundness of that encoder: written argument of RES33N, **audited family by family in VERIFY309N20261113 (c): soundness
  CONFIRMED (written)**. The encoder copy used here (`W/killtools/coupled.py`) differs from RES33N's only in three
  work-directory paths.
  All coupled rows of slices 19–22 (LO33N's 578 rows of slices 19 and 20 are among the 755 rows of slice 22) now have
  kept proofs: 705 were re-certified on 14 Nov, 01:12–01:15 (regenerated CNF and LRAT hashes equal to the records,
  cake_lpr `s VERIFIED UNSAT` for each), the other 50 were certified after 23:26 with kept proofs (§3.3,
  `data/recert_summary.json`).

*Deduction.* Let S be octagon-free in general position (rotated so that x-coordinates are distinct) and h its residual
hole vector. By (a), (g) and (b)–(d), h satisfies h₀ = 0, the 2,650 Lean rows, every certified coupled row,
h(F) ≥ 19 and h(Lo) ≥ 12. Suppose Σh ≤ 33. By (a), Σh = 33; put t = h(F). Then t ≥ 19, and h(Lo) = 33 − t ≥ 12 gives
t ≤ 21, so h satisfies every row of slice t (its capacity rows hold with equality), and by (f) it has at least 34
holes — a contradiction. Hence Σh ≥ 34, n_R ≤ 120 and |S| ≤ 1 + 187 + 120 = 308: every 309-point set in general
position contains a convex octagon. ∎ (Lemma S applied to (65, 58).)

- Variant 59: with N66 ≤ 59, h(Lo) ≥ 11 and t ≤ 22, and slice 22 (§1.1b) covers the extra case t = 22.
- For published bounds see NOVELTY20261113B §3 (claim C1) and §10; this record makes no novelty claim.

---

## 2. Model and soundness

- **Residual model.** As in RES33N/LO33N: 154 residual states, hole vector h (h_i = 1 if state i is unoccupied).
  A row (S, d) says h(S) ≥ d. Rows: the 2,650 Lean rows of
  `experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz` (decompressed SHA-256 `e800d5f8…`,
  file `8c7fe9ef…`), capacity rows (F, ·) and (Lo, ·) (hypotheses, see §1.5), and demand-one coupled rows (CERTIFIED,
  §1.5(g)). Slices and Lemma S: LO33N20261113 §2.
- **Trees.** A tree branches on states (occupied / missing); a leaf is over-budget (|M| > 33) or a weighted leaf: integer
  row weights w and a capacity C with margin Σ_r w_r·max(0, d_r − |S_r ∩ M|) − C·(33 − |M|) − Σ_free max(0, load_i − C)
  > 0, which excludes every 0/1 vector below the leaf with at most 33 holes (inequality re-derived in VERIFY_G.md §2.7).
  The root branches on state 0; its "missing" child is the only pending leaf, discharged by the Lean lemma.
- **Trust.** `scripts/omission_tree.check_tree` (unchanged, unbounded Python integers) is the only trusted part. The
  finders `fastbb` / `fastbb2` (C++, double-precision dual simplex) only propose trees; every replay also checks that
  the capacity rows are exactly the stated ones, that every other extra row has a cake_lpr verdict, that the contexts
  cover the master frontier and that the only pending leaf is "state 0 missing".
- **Why the slice engine finds leaves (PROVED; not needed for soundness).** The score LP is φ = min h(Lo) over all rows
  except the two capacity rows, the node's fixings and h(F) ≤ t. With row duals y ≥ 0, side multiplier α ≥ 0 and
  g_φ = Σ y_r·rem_r⁺ + |M∩Lo| + α(|M∩F| − t) − Σ_free max(0, load_i − c_i) (c_i = α on F, 1 on Lo):
  if α ≤ 1, the vector y + (1 − α)·[h(F) ≥ t] has standard bound ≥ g_φ + t (identical free penalties,
  (1 − α)·rem⁺ ≥ (1 − α)(t − |M∩F|)); if α > 1, y/α + (1 − 1/α)·[h(Lo) ≥ b] has standard bound
  ≥ 33 + (g_φ − b)/α (penalties scale by 1/α), b = 33 − t. A Farkas ray (y, α), α > 0, of value g₀ > 0 gives
  y/α + 1·[h(Lo) ≥ b] with bound ≥ 33 + g₀/α; α = 0 gives a capacity-0 leaf. So g_φ > b yields a weighted leaf after
  rounding; the rounding is accepted only on a positive exact margin.

## 3. Method

### 3.1 `fastbb` (phase 1, `tools/fastbb.cpp`)

C++20, no third-party code except zlib. It finds trees for the same statements as
`experiments/omission-final313-2026-10-11/search/pbb_strong.py`, in the same file format (master.json, ctx-N.json.gz),
so that `assemble.py` / `replay_split.py` → `check_tree` replay them unchanged. Hand-written bounded dual simplex in
row-basis form, warm starts, strong branching on min Σh with pseudo-costs, a certificate pool and ancestors' dual
vectors; a leaf is written only if its margin is positive in exact 128-bit arithmetic. About 1,000–1,400 nodes/s per
thread on the capacity trees (HEURISTIC).

### 3.2 `fastbb2 --slice=1` (phase 2, `tools/fastbb2.cpp`)

`fastbb` plus LO33N's slice rule (`W_lo/pbb_fast2.py`):
- the score LP φ is solved by the same dual simplex; the side constraint h(F) ≤ t is an extra LP constraint (normal −1
  on F, right-hand side −t); the two capacity rows are kept out of the score LP; a node is dead iff the score LP is
  infeasible or φ > b;
- leaves from φ's dual through the conversion of §2, rounded at a list of capacities, accepted on a positive exact
  margin; otherwise the standard LP min Σh over all rows is solved from scratch; otherwise the node is branched;
- forced row (rem = avail > 0) → branch on its first free state before any LP (pbb_strong's rule);
- strong branching on φ over the K most fractional states (K_TOP 16 below 8 fixed states, K_LOW 4 deeper), score =
  product of the gains min(φ_child, b + 1) − φ (floor 10⁻³), **dead-child shortcut** (a candidate with a dead child is
  taken at once; that child becomes a cached leaf when its certificate exists);
- an integral score-LP optimum is completed to exactly t F-holes and b Lo-holes (rows are covering) and reported as a
  witness after an exact check against all rows.
About 640–760 nodes/s per thread on slices (LO33N's Python engine: 55–80).

### 3.3 Rows, driver, witness kills, proofs

- **Row pool `pool_v1.json`** (`W/p2/pool/`, `tools/build_pool.py`): union of the cake_lpr-verified demand-one rows of
  three snapshots (taken 20:25): `res33-20261113/certified.jsonl` (SHA-256 `81d27cb7…`, 581 lines, 570 supports),
  `lo33-20261113/certified.jsonl` (`2f065615…`, 589, 578), `W/killtools/certified.jsonl` (`1a59c275…`, 617, 606):
  **614 supports**. Kept only if a record carries `s VERIFIED UNSAT` and the CNF regenerated from the support by the
  unchanged encoder (`W/killtools/coupled.py`, `959072b1…`, identical to RES33N's except for work paths) has exactly
  the recorded SHA-256: 614 of 614 passed, 0 rejected. Stable order: res33's file order, then new rows of lo33's file,
  then of killtools'.
- **Slice row files** (`tools/make_slice_extra.py`): [h(F) ≥ t, h(Lo) ≥ 33 − t] + pool rows; rows certified later are
  only appended (fastbb2 checks this with a prefix hash), so closed contexts stay valid.
- **Driver** `tools/slicedrv.py`: rows file → `fastbb2 solve --slice=1 --on-witness=continue` (resumable per context) →
  on witnesses (a batch of 4, or one 15 minutes old) stop the search, kill them, resume → on completion replay with
  `tools/verify_slice.py` (piecewise `check_tree`, memory-aware) → `DONE.json`; a witness that cannot be killed →
  `STUCK.json`. The chain scripts `tools/run_chain*.sh` run the slices one after the other and replay each finished tree
  a second time with `tools/replay_split.py`.
- **Witness kills** (`tools/witness_kill.py`, from 21:24 `tools/witness_kill2.py`, which also keeps the transported
  images of new cores in `W/killtools/newrows_g2.json`): certify up to 12 pooled transported rows (RES33N's
  `newrows.json` + `fnewrows.json`) that the witness violates; if none, probe its occupied set for new coupled cores
  (as RES33N's capcegar.py), certify and transport them. Certification = coupled CNF → CaDiCaL `--lrat` → cake_lpr,
  verdict line `s VERIFIED UNSAT` only.
- **Proofs.** From 23:26 the private `W/killtools/certify.py` keeps CNF and LRAT (zstd) in `W/killtools/proofs/`
  (`tools/certify_keep.py`; before, as in RES33N/LO33N, they were deleted after the verdict). The chain re-certifies
  every coupled row of the slice-21/22 row files with kept proofs (`tools/recert_keep.py` → `W/p2/proofs/`), and checks
  that the regenerated CNF and LRAT have the recorded SHA-256 (CaDiCaL is deterministic). Result (01:12–01:15,
  `data/recert_summary.json`): of the 755 rows, 50 already had kept proofs; the other **705 were re-certified: 705
  cake_lpr `s VERIFIED UNSAT`, 705 CNF hashes and 705 LRAT hashes equal to the records**; 907 MB of proofs in
  `W/p2/proofs/` (`recert.jsonl` lists every file and hash).

## 4. Results

### 4.1 Phase 1 (track G, 16:50–19:40 KST)

| | Python `pbb_strong.py` (morning run) | `fastbb` (1 thread) | status |
|---|---|---|---|
| V1 capacity 58 | 60,191 nodes; 631 s wall on 4 processes | 28,735 nodes; 29.7 s | EXACT TREE (`assemble.py` → `check_tree`): 14,368 leaves, 1 pending (state 0 missing), minimum margin 1 |
| V2 capacity 59 | 819,241 nodes; 4,454 s wall on 7+2 workers | 407,101 nodes; 310 s | EXACT TREE (`replay_split.py`; also unchanged `assemble.py` piecewise, VERIFY_G): 203,551 leaves, 1 pending, minimum margin 1 |
| V5 same contexts | 24 of 24 random contexts closed, 1,100 nodes, 39.9 s | 866 nodes, 0.67 s | each Python tree replayed |
| V3 capacity 60 | stopped at 15 of 128 contexts | all 128 contexts closed at 19:37 after 4 witness kills | EXACT TREE (replayed in phase 2, §4.2) |

Knuth estimates of the production rule (`fastbb dive`, 4,000 dives each, rows of `capx_c60_i22.json`, HEURISTIC):
capacity 58: 10^4.72, 59: 10^5.75, 60: 10^6.54, 61: 10^7.10, 62: 10^7.50, 63: 10^7.49, 64: 10^7.63, 65: 10^7.50
(`W/logs/dive_c*.json`; one dive at capacity 62 ended in a 33-hole vector).

**Capacity-60 witnesses (reported as required).** At 18:51 KST the capacity-60 run (2,650 Lean rows + the 570
certified coupled rows of `capx_c60_i22.json` + h(F) ≥ 24, budget 33) stopped on an exact witness in context 17 after 17
closed contexts (478,891 nodes, 367 s):

    holes = [17, 25, 26, 30, 31, 36, 44, 50, 57, 62, 65, 66, 73, 74, 76, 78, 87, 88, 90, 94, 97, 98, 99,
             100, 101, 108, 109, 111, 126, 127, 130, 132, 139]

- Checked in exact integers by fastbb and by `tools/check_witness.py` (`scripts/omission_row_probe.valid_holes`):
  33 holes, all 3,221 rows satisfied, state 0 occupied, 60 of the 84 F-states occupied (also VERIFY_G §2.5).
- So the 570 certified rows of iteration 22 do not close capacity 60 (the morning run had not reached this region).
- It violates 2 pooled transported rows (9 states each). Both were certified at 19:01 (CaDiCaL LRAT, cake_lpr
  `s VERIFIED UNSAT`; re-certified by VERIFY_G §2.6) by `tools/witness_kill.py` on a private copy of the res33 tools and
  appended (`capx_c60_i23.json`, 573 rows). The run was resumed; the 17 closed contexts were kept.
- Three more witnesses (contexts 24, 56, 66, 19:10–19:31) were killed at 19:34 the same way: 11 + 11 + 12 pooled rows
  certified and appended (`W/logs/kill2.log`), 607 rows. Every witness occupied 60 F-states (slice 24). Hole sets:
  `W/runs/v3_c60/witnesses_killed_pass2/`. The run closed the last three contexts by 19:37.

### 4.2 Capacity 60: replay (phase 2)

`tools/replay_split.py W/runs/v3_c60 --jobs 1` (20:45–20:47, unchanged `check_tree`, one context at a time): 128 of 128
contexts, **2,621,661 nodes, 1,310,831 leaves, minimum margin 1**, one pending leaf; largest context 148,697 nodes; 1 min
40 s, peak 0.86 GB (`data/c60_replay.json`). Rows (`tools/check_cap_rows.py`): 607 extra rows, exactly one capacity
row (index 570, F with demand 24), 606 demand-one rows each with a cake_lpr `s VERIFIED UNSAT` record: OK. Rows were
only appended during the run, so contexts closed under 571 or 573 rows remain valid. All 606 rows are among the 755
rows re-certified with kept proofs (§3.3).

### 4.3 Validation of the slice engine (LO33N's extra-row files, 580 rows)

| slice | LO33N (Python, HiGHS) | fastbb2 | replay of the fastbb2 tree (`tools/verify_slice.py`) |
|---|---|---|---|
| 18 (66, 55) | 3,611 nodes (also 3,635 and 3,815 with other engines) | 3,891 nodes, 6.9 s on 1 thread | EXACT TREE: 3,891 nodes, 1,946 leaves, minimum margin 1, 1 pending; only capL used besides Lean/coupled rows |
| 19 (65, 56) | 167,509 nodes | 180,241 nodes, 69.7 s on 4 threads (+14.9 s master) | EXACT TREE: 180,241 nodes, 90,121 leaves, minimum margin 1, 1 pending; capF and capL used; 154 extra rows used |

### 4.4 Knuth estimates (pool_v1 rows, K_TOP 16 / D_TOP 8 / K_LOW 4, HEURISTIC; `data/dive_t*.final.json`)

| slice | dives | estimated nodes | std. error | actual tree |
|---|---|---|---|---|
| 19 | 2,000 | 1.77·10^5 | 0.09·10^5 | 180,241 (LO33N's rows) |
| 20 | 1,460 | 3.61·10^6 | 0.19·10^6 | LO33N's tree: 3,468,657 |
| 21 | 1,200 | 2.01·10^7 | 0.11·10^7 | **19,333,541** |
| 22 | 1,260 | 3.62·10^7 | 0.21·10^7 | **32,328,319** |

### 4.5 Slice 21 (pair (63, 58)) — CLOSED

- **Tree.** 8,175 contexts below a master split of 16,373 nodes; **19,333,541 nodes, 9,666,771 leaves, minimum margin
  1, one pending leaf**; largest context 32,731 nodes. Search 20:39–22:19 KST on 4–5 threads. Both capacity rows and 405
  of the 643 coupled rows carry positive weight in some leaf.
- **Replay 1** (`tools/verify_slice.py`, 22:19–22:22, 5 processes): these counts; semantic checks passed. **Replay 2**
  (`tools/replay_split.py`, 22:22–22:25): identical counts (`data/s21_replay2_compare.json`, agree = true).
- **Rows.** 614 of pool_v1 + 29 certified during the run. For all 643 the regenerated CNF has the SHA-256 of a
  cake_lpr-verified record (pool audit 20:34; the 29 audited at 22:27). Frozen copy: `data/s21_extra.json`.
- **Witnesses (reported as required): 11 distinct 33-hole vectors of slice 21 (63 F-states occupied) satisfied every row
  then in the file; all were killed by newly certified rows; none is stuck** (`data/s21_witnesses.jsonl`):
  - contexts 448, 1476 (killed 21:04 by 8 + 1 certified pooled rows, the chain stopped for 20 s and the kill step run by
    hand); 1891, 2876, 2885, 2937, 3003, 3026 (21:17–21:21: ctx 1891 violated no pooled row, so new cores were probed,
    certified and transported, 4 rows; ctx 2876 by 7 pooled rows; the others were already refuted); 6469, 6535, 7290
    (22:11–22:16: 6469 by probing, 4 rows; 7290 by 5 pooled rows; 6535 already refuted). Extra rows 616 → 645.

        ctx 448:  [7, 12, 13, 14, 27, 51, 54, 56, 58, 65, 66, 67, 68, 71, 72, 75, 76, 79, 93, 96, 97, 101, 102, 103, 107, 111, 119, 121, 126, 133, 139, 140, 144]
        ctx 1476: [12, 17, 18, 25, 27, 37, 46, 49, 50, 51, 59, 64, 66, 72, 75, 76, 78, 79, 84, 88, 96, 100, 101, 103, 106, 107, 116, 119, 124, 126, 133, 137, 139]

### 4.6 Slice 22 (pair (62, 59)) — CLOSED

- **Tree.** 4,096 contexts below a master split of 8,191 nodes; **32,328,319 nodes, 16,164,160 leaves, minimum margin
  1, one pending leaf**; largest context 208,551 nodes. Search 22:25 (13 Nov) – 01:03 (14 Nov) on 5 threads (Knuth
  estimate 3.62·10^7). Both capacity rows and 545 of the 755 coupled rows carry positive weight in some leaf.
- **Replay 1** (`tools/verify_slice.py`, 01:03–01:07, 5 processes): these counts; semantic checks passed (first two
  extra rows exactly (F, 22) and (Lo, 11); every other extra row demand 1 with a cake_lpr `s VERIFIED UNSAT` record).
  **Replay 2** (`tools/replay_split.py`, 01:07–01:12, 5 processes, peak 2.96 GB anonymous memory in the unit):
  identical counts (`data/s22_replay2_compare.json`, agree = true).
- **Rows.** 755 coupled rows = 614 of pool_v1 + the 29 of the slice-21 kills (appended by hand at 22:26, before any
  context was closed) + 112 certified during the run. Frozen copy `data/s22_extra.json`. All 755 re-certified or
  certified with kept proofs (§3.3).
- **Witnesses (reported as required): 34 distinct 33-hole vectors of slice 22 (62 F-states occupied) satisfied every row
  then in the file; all were killed by newly certified rows (4 of them by probing new cores, the others by certified
  pooled transported rows); none is stuck** (`data/s22_witnesses.jsonl`, 35 lines, one vector met twice).

### 4.7 Slice 20 (second tree) — CLOSED; slice 23 — running

- **Slice 20** (pair (64, 57)), row file = the two capacity rows + all 755 coupled rows of slice 22 (`data/s20_extra.json`,
  SHA-256 `cf6c7c967164f16f0085eb4b885cedfb33e5bbaf1f89b97e61bc605c1a946383`): 8,001 contexts, **3,044,395 nodes,
  1,522,198 leaves, minimum margin 1, one pending leaf**, largest context 8,071 nodes; search 01:15–01:31 on 5 threads,
  **no witness met**; replay 1 (`verify_slice.py`) and replay 2 (`replay_split.py`) identical (01:31–01:33);
  `master.json` `ba0434403c721cbe16eed3327401e63c5be94f240e4c78422fd830f910403f59`, contexts digest
  `4c70ca83cdbbdefad9ad4b26e99ff98b4b576cdcf093c8b70611f9cb433f8f53` (`data/s20_DONE.json`). An independent second
  tree for LO33N's slice 20 (different engine, different and larger row set).
- **Slice 23** (pair (61, 60); with slices 19–23 the pair (65, 60) would close): started 01:33 with the same 755 rows;
  no Knuth estimate was made (slices 21/22 needed 1.9·10^7 / 3.2·10^7 nodes); undecided at the time of writing.
  Result, or the state at the deadline 05:55 KST with the resume command of §8: `data/AUTO_RESULTS.md`.

## 5. Controls

- **Negative control (tree):** zeroing the weights of one leaf in a copy of the slice-18 tree makes `verify_slice.py`
  fail ("Nonpositive leaf margin").
- **Positive control (witness path):** rows = Lean + slice-24 capacity rows + the 570 rows of `capx_c60_i22.json` + 25
  singleton TEST rows forcing 25 of the 33 holes of the phase-1 capacity-60 witness. `fastbb2` met exactly that witness
  (exit 3); `check_witness.py` confirmed it (33 holes, 3,247 rows, 60 F-states occupied, 2 pooled rows violated); the
  driver certified those 2 rows, appended them, restarted, the region closed, and the replay **refused** the tree
  because the 25 test rows have no certificate (`W/p2/runs/pc24/`). (Slice 22 over the Lean rows alone met no witness
  in 2 minutes; stopped; not a result.)
- **Two replays per finished slice** with different wrappers (`verify_slice.py`, `replay_split.py`), same `check_tree`:
  identical counts for slice 21 and for slice 22.
- **Row audits:** regenerated CNF hashes for all 614 pool rows and the 29 slice-21 kill rows; full re-certification
  with kept proofs of all 755 rows of slices 21/22 (705 re-run tonight, all verified, all CNF and LRAT hashes equal to
  the records; 50 kept at certification).
- **Knuth calibration:** slice 19 estimate 176,905 vs tree 180,241; slice 20 3.61M vs LO33N's 3,468,657; slice 21
  2.01·10^7 vs 19,333,541; slice 22 3.62·10^7 vs 32,328,319.
- **Rule parameters** (40 fixed slice-21 contexts, 1 thread each, HEURISTIC; `data/tuning_s21_40ctx.json`): K_LOW 4
  (used) 129,118 nodes / 170 s; K_LOW 2: 235,084 / 180 s; K_LOW 3: 160,072 / 167 s; K_LOW 8: 85,980 / 203 s; K_LOW 4
  with known-closed children counted as dead (`--known=1`): 164,516 / 174 s.
- **VERIFY_G.md** (verifier, 20:20–20:45, on the 19:15 interim record): every phase-1 claim confirmed; corrections
  (labels, hashes, mutable row files, wording "finds trees for the same statements") are applied in this version:
  EXACT TREE labels, hashes in §6, frozen copies of the extra-row files in `data/`.

## 6. Files and hashes (SHA-256; 16-digit prefixes where the full value is in a JSON file in `data/`)

| item | SHA-256 |
|---|---|
| `source-2650.json.gz` (file / decompressed) | `8c7fe9ef5264182524095d46ef50ed6bc691cab425efa965756d1870112241aa` / `e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6` |
| `scripts/omission_tree.py` (check_tree) | `35cb30503c3b1eb8…` |
| `tools/fastbb.cpp` / binary `W/bin/fastbb` | `4713bd5ac85218ef4eab10522276b2e3ad9ef9d2e0afa47b5553fc3440036afa` / `0430b3655b9cd3f87e428afe14b114966b22b849fa62288c0cf9f6cb57360441` |
| `tools/fastbb2.cpp` / binary `W/p2/bin/fastbb2` | `2e7e0707b3cc40acd10806c03a8aabbbdb7a59ebd6e4d99d7a7035d5df9c1b18` / `39b724a2b5f5b08b56f3e9aedb24886c08ae2716301008410aaba9a1452b33b5` |
| V1 extra `data/capx_c58_i1.json` / master | `25b9fa73d476fdb78937bdcaca8505ccc96df5f5f753e051f57fe7903c25a820` / `70efcf24b384491fc30af5bc9fefa9759f763794fbea4029b79c852821bd22fe` |
| V2 extra `data/capx_c59_i2.json` / master | `e506e1bfc7ee68c62b4987d439ae84a759c767bbb55c0bc6bff6ccd4a49e4552` / `7d800a0eb34ff09a25dff493504dda1fa6ccae6de2655d289d878b8a632ff3c3` |
| V3 extra `capx_c60_i22.json` (571 rows, start) | `ad8b7363ca4495057fd6fcf85ece0e2ab629c6648103d772ad3fdf410c1fd5ce` |
| V3 extra `data/capx_c60_i23.json` (607 rows, final) / master.json / master.txt | `44ef8b22937b000be71d0743f59b676f7980758f9a6b3e2f1456f00e32e4cf89` / `d0c869fab190617a222736975bf81161d5b5a4e027d3acccdeca4b284d9d1bf2` / `7bfe4a05…` |
| V3 context files (digest of per-file digests, context order) | `dc7befa5653be9cd469f94681c8ac15d39b15e62742ebd59c93c404bf93d7865` |
| pool `W/p2/pool/pool_v1.json` / manifest `data/pool_v1_manifest.json` | `13c49a74da3620bdfa57e68cd16273f9ff302885cec008f1c1df91e1666adf24` / `3abcd7f3caa70aa8…` |
| encoder `W/killtools/coupled.py` | `959072b12004eec785bdc3ace47acdd23e41221848515e5c891b431a57ac17db` |
| slice 21 extra `data/s21_extra.json` (645 rows) | `7e7fc843d16b8e673924fd9a4fe060482d3cea3508699e7a3c7dd1ae58e90f69` |
| slice 21 rows file / master.json / master.txt | `a33eaecf888d974f…` / `63ea1915e70f2376c6d628af58b5799f0bf4309b23b5ed5d728ff64d547e6fac` / `1be33eb9ae3ecd1b…` |
| slice 21 context files (digest, context order) | `0715763257a108096a6f9722f7fc96bbed0457141f91dfcec106681924a95a62` |
| `W/killtools/certified.jsonl` at the slice-21 replay | `7ac2e0b2…` (full value in `data/s21_DONE.json`) |
| slice 22 extra `data/s22_extra.json` (757 rows) | `3add175a238f20fc295bc25cffde5fe6f7005c0b1e453892c8d14a3324fada51` |
| slice 22 rows file / master.json / master.txt | `a7266a312d417b87…` / `94137c06a58e0076bf8d512eecbac8df48c4e628f596be6c08a988cdad2cd038` / `f913ad0cda6f4e2f…` |
| slice 22 context files (digest, context order) | `a1e1ff34e0b619a9accb8a7dd3dd4b20431b990af4a015322f0f84e269623317` |
| `W/killtools/certified.jsonl` at the slice-22 replay | `8e7d920a…` (full value in `data/s22_DONE.json`) |
| slice 20 (second tree here) extra `data/s20_extra.json` (757 rows) / rows file | `cf6c7c967164f16f0085eb4b885cedfb33e5bbaf1f89b97e61bc605c1a946383` / `bfb0ecd62a0fd4fe…` |
| slice 20 (here) master.json / master.txt / context files digest | `ba0434403c721cbe16eed3327401e63c5be94f240e4c78422fd830f910403f59` / `def75aaebddb2d27…` / `4c70ca83cdbbdefad9ad4b26e99ff98b4b576cdcf093c8b70611f9cb433f8f53` |
| slice 20 (LO33N) extra / contexts digest | `d12f624f1858e8670988df864686accf1d35f4e02c7127b8c355bc918055ecee` / `709a345e…` |

`data/`: `s21_DONE.json`, `s21_replay2_compare.json`, `s21_witnesses.jsonl`, `s21_extra.json`, `s22_DONE.json`,
`s22_extra.json`, `s22_witnesses.jsonl`, `s22_replay2_compare.json`, `s20_DONE.json`, `s20_extra.json`,
`s20_replay2_compare.json`, `recert_summary.json`, `capx_c58_i1.json`, `capx_c59_i2.json`, `capx_c60_i23.json`,
`c60_replay.json`, `dive_t19..22.final.json`, `pool_v1_manifest.json`, `tuning_s21_40ctx.json`, and the files the chain
adds later (`AUTO_RESULTS.md`, `s<T>_*.json`, `recert_summary.json`). Large files (trees, rows files, proofs) stay in W.

## 7. What remains

- **Independent checks** (own code, another track): replays of the slice-21 and slice-22 trees (the other links of
  variant 59 are independently confirmed: N5 ≤ 65, N66 ≤ 59, Lemma A use, Lemma S, slices 19 and 20, the coupled
  encoder; see VERIFY_N5, VERIFY_N66, VERIFY_LO, VERIFY309N).
- **Slice 23** (pair (61, 60)): running from 01:33 (`data/AUTO_RESULTS.md`); with it the pair (65, 60) would close.
- **Proofs:** done for every row of slices 21/22 (`W/p2/proofs/`, `W/killtools/proofs/`); keep them until another
  track has re-run cake_lpr on them (house rule). Slices 19/20 (LO33N) use 578 rows, all among these 755.
- **Lean:** export the slice trees with the compact checker; LRAT-to-Lean for the coupled rows (STATUS20261113 §5).

## 8. Running jobs, resume and re-check commands

- Unit `nov13c-g-chain9` runs `W/p2/run_chain6.sh 5` (copy `tools/run_chain6.sh`): slice 22 (closed 01:07) → its second
  replay (01:12) → re-certification with kept proofs (01:15) → slice 20 (closed 01:32) → slice 23 (running from 01:33);
  deadline 05:55 KST, 14 Nov;
  MemoryMax 4G; log `W/p2/runs/chain.log`. Earlier units of the same chain (each replaced by hand, closed contexts kept):
  `nov13c-g-chain` 20:40–21:02 (4 threads), `-chain2` 21:02–21:04, `-chain3` 21:04–21:06, `-chain4` 21:06–21:16,
  `-chain5` 21:16–21:24, `-chain6` 21:24–22:26, `-chain7` 22:26–23:37, `-chain8` 23:37–00:30. **After every step and every 10
  minutes the chain rewrites `data/AUTO_RESULTS.md` in this record** (`tools/auto_results.py`: a table of the slice
  states read from DONE.json / STUCK.json / status.json / replay2_compare.json, the re-certification summary, and
  copies of those small files in `data/`); results that arrive after the G2 session ended appear there.
- Per slice T: `W/p2/runs/s<T>/`: `extra.json`, `rows.txt`, `bb/` (master and context trees), `fastbb.out`,
  `driver.log`, `status.json`, `witnesses.jsonl`, `kill.out`, and finally `DONE.json` (replay counts, minimum margin,
  SHA-256 of every input) or `STUCK.json` (a 33-hole vector that no certified row kills: the obstruction), then
  `replay2.json` / `replay2_compare.json`.
- **Resume** after any interruption (in a systemd unit with CPUQuota 500%, MemoryMax 4G):
  `bash W/p2/run_chain6.sh 5`. Closed contexts are kept, rows are only appended, finished steps are skipped.
- **Re-check a finished slice** (from the repository root; `PY` = the project venv python):
  `PY W/p2/tools/verify_slice.py W/p2/runs/s21/bb 21 5 W/p2/pool/pool_v1.json W/killtools/certified.jsonl` and
  `PY cloud/es7-2026-10-19/results/FASTBB20261113/tools/replay_split.py W/p2/runs/s21/bb --jobs 5` (a few minutes;
  under 0.3 GB per process for slice 21). For slice 22 use `s22` and `22`; its largest context (208,551 nodes) needs
  about 1.2 GB in one Python process, so use at most 3 processes with `replay_split.py` (`verify_slice.py` schedules by
  memory, `VERIFY_MEM_MB`, default 2,500).
- Build: `make -C cloud/es7-2026-10-19/results/FASTBB20261113/tools BUILD=<dir> fastbb2`.

## 9. Resources

- Track G2 used at most 5 threads at any time (`cpu_free.sh` before every unit; the short tests of 23:26 and 23:36
  ran while the chain was in a single-threaded kill phase). Memory: no unit of track G2 was stopped by the memory
  guard in phase 2; the capacity-60 replay peaked at 0.86 GB, the 5-thread search used about 0.24 GB (unit
  MemoryCurrent at 23:40); `verify_slice.py` schedules its replay to a 2.5 GB estimate; `replay_split.py` (no
  scheduler, 5 processes) peaked at 2.96 GB anonymous memory on slice 22 (unit MemoryMax 4 GB).
- Phase 1: `nov13c-g-v2asm` (the monolithic `assemble.py` replay of capacity 59) was stopped by the guard at 18:28
  (track over its then 2 GB budget); it was replaced by the piecewise `replay_split.py`, which V2 then used.
