# LO33N20261113: two-capacity thresholds on the residual catalog (F and Lo), 13 November 2026

**Status (phase 2, 20:52 KST): complete; every tree of this record is finished. Slice t = 20 (pair (64, 57))
closed at 20:28 KST with the certified coupled rows and was replayed twice. Over the Lean rows alone, slice 20 is
about half done (1,046 of 2,048 contexts, partial replay) and no job is running for it. Slice 21, the next open
slice, has been searched since 20:31:42 by the unit `nov13c-lo-tree-63-58`. That run was started by the phase-2
main loop and is not part of this record (§6).**
**No new bound on ES(8) is claimed.** Track B (LO33) of the 13 November afternoon session (16:55 KST until the
cut-off at about 19:40 KST), completed in phase 2.

> Phase-1 agent cut off at about 19:40 KST; completed from the work directory by a phase-2 agent at 20:52 KST
> (13 November 2026). The phase-2 agent filled every placeholder from W, recorded the end of slice 20 (closed by
> the unit the phase-1 agent had started; the phase-2 watcher `p2-watch-slice20` only re-ran its replay), and
> ran the read-only checks of §5 ("Phase-2 re-checks"). These were single checks under one minute each, and
> nothing was written in W. Statements about phase-1 runs that are not logged are marked as inferred.

**Headline (EXACT TREES; conditional statements; the trees are not Lean-checked, nothing is refereed):**

> **(i) N66 ≤ 56 ⇒ ES(8) ≤ 309, over the 2,650 Lean rows alone.** If every 57-point set (distinct x, general
> position) with no 6-cap and no 6-cup contains a convex octagon, then ES(8) ≤ 309.
> No coupled row and no bound on N5 is used. The certificate is two exact trees over the Lean rows plus
> capacity rows (3,815 nodes for slice 18 and 186,077 nodes for slice 19, each with minimum integer margin 1),
> glued by Lemma S below. Each of the two trees was replayed three times by `scripts/omission_tree.check_tree`
> (through `verify_stream.py`, §3): by the driver on completion, by a second run whose output files were written
> at 19:08:58–59 (inferred from file times; the command line is not logged), and by the phase-2 agent at 20:30
> from the archived tar files. All three replays gave identical counts and hashes.
>
> **(ii) N66 ≤ 57 ⇒ ES(8) ≤ 309, with the 578 cake_lpr-certified coupled rows.** These rows are certified CNFs
> of the coupled owner model, as in RES33N20261113, and are not Lean-checked. The proof uses the exact trees for
> slices 18 (3,611 nodes, replayed twice), 19 (167,509 nodes, replayed three times) and 20 (3,468,657 nodes,
> closed at 20:28 KST, replayed twice piecewise), glued by Lemma S. No bound on N5 is used.

- The trivial thresholds were N66 ≤ 54 without N5 and N66 ≤ 55 with N5 ≤ 65 (ETV5N20261113).
- **Over the Lean rows alone:** N66 ≤ 56 suffices and N66 ≤ 58 does not. An exact 33-hole vector over the Lean
  rows occupies 63 F-states and 58 Lo-states, i.e. it lies in slice 21; the phase-2 agent re-checked it exactly.
  N66 ≤ 57 is undecided there, because slice 20 over the Lean rows is half done.
- **With the certified coupled rows:** N66 ≤ 57 suffices. N66 ≤ 58 needs slice 21, which is undecided; the
  vector above violates 8 certified rows.
- Known bounds at the time of writing (other records, phase-1 certificates): N5 ≤ 65 is CERTIFIED (ETV5N20261113).
  In N66N20261113, N66 ≤ 59 is CERTIFIED and N66 ≤ 58 is COMPUTED, with its certification running in phase 2.
  Two consequences follow, both with the certified coupled rows:
  - **Slice 21 is the only open slice between "N66 ≤ 58" and ES(8) ≤ 309.**
  - **Slices 21 and 22 are the only open slices between the certified N66 ≤ 59 and ES(8) ≤ 309.** This holds
    with or without N5 ≤ 65.

  Over the Lean rows alone, slice 20 is still open as well, and slice 21 is OPEN (§4a).

Labels: **PROVED** (written proof), **CERTIFIED** (cake_lpr `s VERIFIED UNSAT` for a stated CNF),
**EXACT TREE** (branch-and-bound tree whose every leaf margin was recomputed in unbounded integers by
`scripts/omission_tree.check_tree`), **COMPUTED** (solver verdict only), **HEURISTIC** (statistics).

Work directory: `/home/jay/research/data/lo33-20261113` (not in Git; abbreviated W). Scripts were copied to
`tools/` and small data to `data/` at 18:15–19:09. Several scripts and all trees after 19:09 exist only in W;
they are listed with their SHA-256 in §6. Nothing is committed.

## 1. Model

The residual catalog has 154 states; a hole vector h marks the unoccupied ones. F is the set of the 84
states with f₁ ≥ 5 and Lo the set of the 70 states with f₁ ≤ 4. By Lemma A of THEORY310N20261113 the
owners of F-states form a set with no 5-cap and no convex octagon, and the owners of Lo-states a set with
no 6-cap, no 6-cup and no convex octagon. So every residual hole vector satisfies

- h(F) ≥ 84 − N5, where N5 = N(cap ≤ 4) (N5 ≤ 65 is cake_lpr-certified in ETV5N20261113);
- h(Lo) ≥ 70 − N66, where N66 = N(cap ≤ 5, cup ≤ 5). The ETV value is 50. When this record was started only
  N66 ≤ 64 was known (COMPUTED); by 20:35 N66N20261113 reports N66 ≤ 59 CERTIFIED and N66 ≤ 58 COMPUTED.

**Pair (c, c2)** stands for the two rows h(F) ≥ 84 − c and h(Lo) ≥ 70 − c2. A pair is **CLOSED** if
every 0/1 vector with h₀ = 0, the 2,650 Lean rows, the cake_lpr-certified coupled rows and both capacity
rows has at least 34 holes. Then "N5 ≤ c and N66 ≤ c2" gives n_R ≤ 120 and ES(8) ≤ 309 (composition as
in THEORY310N20261113 §6). Pairs with c + c2 ≤ 120 are closed trivially.

Row system:
- base: `experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz`
  (SHA-256 `e800d5f8…`, pinned in `tools/common.py`), with state 0 occupied;
- coupled rows: the demand-one rows of `certified.jsonl` whose own CNF has a cake_lpr
  `s VERIFIED UNSAT` verdict: the 570 rows of RES33N20261113 plus 8 certified in this session (§4c).
  Their status is that of RES33N: certified CNFs of the coupled owner model, not Lean-checked;
- the two capacity rows of the pair.

"Over the Lean rows alone" means: no coupled row at all.

## 2. Slices (PROVED)

**Lemma S.** Let h be a 0/1 vector with h₀ = 0 that satisfies the 2,650 Lean rows.
1. Σh ≥ 33. This is the Lean theorem `Final313.residual_excludes_2650_zero : Excludes2650Zero 32`
   (`experiments/omission-final313-2026-10-11/Final313/Final.lean`), the residual half of ES(8) ≤ 310.
2. h(F) ≥ 18. Rows 973, 1165, 1167, 1171, 1175, 1179, 1183, 1186 and 2315 each have 28 states inside F
   and demand 6, and every F-state lies in exactly three of them; so 3·h(F) ≥ 54
   (`tools/check_f18.py`, exact).
3. Call **slice t** the pair (84 − t, 37 + t), i.e. the rows h(F) ≥ t and h(Lo) ≥ 33 − t. If Σh = 33
   then h satisfies slice t for t = h(F), with equality in both rows.
4. Hence a pair (c, c2) is closed **if and only if** every slice t with
   max(18, 84 − c) ≤ t ≤ c2 − 37 is closed.

*Proof of 4.* (⇐) Let h satisfy everything for (c, c2) with Σh ≤ 33. By 1, Σh = 33. Put t = h(F); then
t ≥ 84 − c, t ≥ 18, and h(Lo) = 33 − t ≥ 70 − c2 gives t ≤ c2 − 37. By 3, h is a 33-hole vector in
slice t, which is closed: contradiction. (⇒) A 33-hole vector of slice t has h(F) ≥ t ≥ 84 − c and
h(Lo) ≥ 33 − t ≥ 70 − c2, so it is a witness for (c, c2). ∎

So the frontier is a one-dimensional object: the set of closed slices. Slices t ≥ 25 are closed by
RES33N20261113 Result 3 ((59, 70) closed: h(F) ≥ 25 forces 34 holes). That left t = 18, …, 24. Slices 18, 19
and 20 are now closed (§4a), so slices 21–24 remain open.
Each slice is itself a pair, so a slice certificate is an ordinary single tree in the format of
`cert_c58/` and `cert_c59/`. A pair that needs two or more slices is closed by Lemma S, i.e. by several
replayed trees plus the Lean theorem of item 1; there is then no single `check_tree` file for it.

Reading the frontier: a bound N5 ≤ c removes the slices below 84 − c, a bound N66 ≤ c2 removes the
slices above c2 − 37. The low slices are the cheap ones, and they are closed from below. **An improvement of N5
therefore buys nothing until it skips an open slice.** (64, 57) and (66, 57) needed the same slice t = 20, which
is now closed, so both pairs are closed. (63, 58) and (66, 58) need the same open slice t = 21. With slices
18–20 closed, only N5 ≤ 62 helps, by removing slice 21 from the pairs with c2 = 59; N5 ≤ 59 would remove every
open slice.

## 3. Method

**Exact search.** The search is the project's exact LP branch-and-bound
(`experiments/omission-final313-2026-10-11/search/pbb_strong.py`). It branches on a state (occupied or
missing). A leaf is a set of non-negative integer row weights with a capacity C, and the leaf is kept only if
its margin
Σ w_r·max(0, d_r − |S_r ∩ missing|) − C·(33 − |missing|) − Σ_free max(0, load_i − C) is a positive
integer. The tree is replayed by `scripts/omission_tree.check_tree`, which recomputes every margin in
unbounded integers. The root branches on state 0; the child "state 0 missing" stays pending and is
discharged by `OmissionResidualZeroState.zero_mem_residualOccupied`, exactly as in the 313 tree and in
`cert_c58/`, `cert_c59/` of RES33N20261113. **Soundness of a finished tree depends only on that replay
and on the validity of the rows**, never on how the tree was found.

**Why the production rule fails on slices, and the new branching score.** In a slice the two capacity
demands add up to the budget, so the LP "min Σh" equals exactly 33 on every live node and strong
branching sees zero gain everywhere. Knuth estimates with the production rule (K_TOP 16, D_TOP 8,
K_LOW 4) were 10^4.5, 10^6.6, 10^7.6, 10^7.8 nodes for t = 18, 19, 20, 21 (HEURISTIC). The slice engines
keep the same leaf format but choose the branching state with the score LP

    φ = min h(Lo)   subject to all rows, the node's fixings, and h(F) ≤ t.

A node is dead exactly when this LP is infeasible or φ > 33 − t, and φ rises smoothly towards that
threshold, so strong branching on φ is informative. (Covering rows are monotone, so this dead test is
equivalent to "min Σh > 33", up to the forced-row test done first.) With the same K parameters the
Knuth estimates drop to 10^3.3 (t = 18), 10^5.2 (t = 19), 10^6.4 (t = 20), about 10^7 (t = 21). The two
estimates that could be compared matched the trees actually built: t = 19 estimated about 170K nodes and the
tree has 167,509; t = 20 estimated 10^6.4 and the tree has 3,468,657 = 10^6.54.

Three engines, all producing the same kind of tree (`tools/`, and W for `pbb_fast2.py`):
- `pbb_lo.py`: pbb_strong with the score LP; about 18 nodes/s per process.
- `pbb_fast.py`: the same with lazy rows (a HiGHS model holds only rows that some optimum violated; one
  matrix–vector product checks all rows after each solve) and a vectorised forced-row scan; about
  55 nodes/s per process, essentially the same trees (t = 18: 3,635 nodes against 3,611).
- `pbb_fast2.py`: in addition (i) the leaf weights are read off the score LP's own dual (if α ≥ 0 is the
  multiplier of h(F) ≤ t and y the row duals, then y together with weight 1 − α on the row h(F) ≥ t if
  α ≤ 1, or y/α together with weight 1 − 1/α on the row h(Lo) ≥ 33 − t if α > 1, is a dual solution of
  the standard LP), and (ii) a branching candidate with a dead child is taken at once. On the same six
  contexts of slice 20: 4,830 nodes in 45.9 s against 4,516 nodes in 79.2 s for `pbb_fast.py`. The whole
  slice-20 tree: 3,466,608 context nodes in 45,775 process-seconds (sum of the logged context times), i.e.
  about 76 nodes/s per process.
- In every engine a leaf is kept only if `pbb_strong.margin` (exact integers, full row system) is
  positive; otherwise the node is handed to pbb_strong's own code or branched.
- HiGHS is used only as a heuristic source of branching decisions and dual weights. **No HiGHS status
  is evidence for anything in this record.**

**Driver** (`lotree.py`; the version that ran is W/lotree.py, see §6). It differs from `capcegar.py` of
RES33N in bookkeeping only:
- the extra rows are written in a stable order (capacity rows first, then certified rows in the order
  of `certified.jsonl`), so a context tree closed under a prefix of the rows remains a valid certificate
  after rows are appended (appended rows get weight 0);
- the master split is built once and stored with the context definitions, so after a restart, or after
  a witness is killed, only unfinished contexts are rerun;
- a witness (a 33-hole vector satisfying everything) is killed exactly as `capcegar.py` does: pooled
  transported rows that it violates are certified on the spot (own CNF, CaDiCaL LRAT, cake_lpr); if it
  violates none, its occupied set is probed for new coupled cores, which are certified and transported.
  A witness that cannot be killed is logged as STUCK (the obstruction). With `LO_NOCERT=1` (Lean rows
  only) a witness is reported as the obstruction at once.

**Repair to the Lean rows** (`repair.py`, W only). This turns an exact slice tree that uses certified coupled
rows into a tree over the Lean rows alone. Every leaf whose weights touch a coupled row is re-opened and searched
again with `pbb_fast2` over the Lean rows plus the two capacity rows, and the subtree found replaces the leaf.
Leaves that use only Lean and capacity rows are kept. The capacity rows have the same indices 2650, 2651 in both
row systems. The result is an ordinary context-split tree with the same master split, replayed by
`verify_stream.py` against the Lean-only extra-row file, so its validity does not depend on `repair.py`. A
witness met during a repair is a 33-hole vector over the Lean rows inside the slice; the repair then stops and
the slice is OPEN over the Lean rows.

**Replay.**
- Small trees: `assemble.py` builds the single tree and replays it; `tools/verify_cert.py` replays the
  archived tree a second time from the archived files.
- Large trees: one assembled tree needs about 7 kB of Python objects per node, so
  `verify_stream.py` (W only) replays the same tree piecewise with the same checker. It runs `check_tree` on the
  top tree, with context placeholders as pending leaves. It also runs `check_tree` on every context subtree,
  wrapped under a chain of branch nodes fixing exactly the states on its master path (recomputed from the master
  tree by `omission_tree.contexts`). Validation: on slice 19 it reproduces the monolithic replay exactly
  (167,509 nodes, 83,755 leaves, minimum margin 1, one pending leaf). With missing contexts it reports PARTIAL
  and counts each missing context as a pending leaf.
- Both verifiers also check that the capacity rows are exactly (F, 84 − c) and (Lo, 70 − c2) and that
  every other extra row carries a cake_lpr `s VERIFIED UNSAT` verdict in `certified.jsonl`.

## 4. Results

### 4a. Slices at budget 33 (the ES(8) ≤ 309 frontier)

| slice t | pair (84 − t, 37 + t) | rows of the slice | with the certified coupled rows | over the Lean rows alone |
|---|---|---|---|---|
| ≤ 17 | – | – | empty: h(F) ≥ 18 (Lemma S.2, PROVED) | same |
| **18** | (66, 55) | h(F) ≥ 18, h(Lo) ≥ 15 | **CLOSED, EXACT TREE**: 3,611 nodes, 1,806 leaves, min margin 1 (578 rows available, 26 used) | **CLOSED, EXACT TREE**: 3,815 nodes, 1,908 leaves, min margin 1, 110 contexts; only the row h(Lo) ≥ 15 is used besides Lean rows (in 1,904 leaves; 1,227 Lean rows carry weight) |
| **19** | (65, 56) | h(F) ≥ 19, h(Lo) ≥ 14 | **CLOSED, EXACT TREE**: 167,509 nodes, 83,755 leaves, min margin 1 (578 available, 130 used; the F-row is used in 69 leaves) | **CLOSED, EXACT TREE**: 186,077 nodes, 93,039 leaves, min margin 1, 980 contexts (F-row used in 98 leaves, Lo-row in 92,647; 2,384 Lean rows carry weight). A second Lean-rows tree, made by repairing the certified-rows tree (§3), also closes it: 172,401 nodes, 86,201 leaves, min margin 1 |
| **20** | (64, 57) | h(F) ≥ 20, h(Lo) ≥ 13 | **CLOSED, EXACT TREE** (last context 20:28 KST): 3,468,657 nodes, 1,734,329 leaves, min margin 1, 2,048 contexts, no over-budget leaf (578 available, 180 used; certified rows carry weight in 512,613 leaves, the F-row in 92,030, the Lo-row in 1,616,173; 2,565 Lean rows carry weight) | **partial**: 1,046 of 2,048 contexts closed by repair (EXACT, partial replay: 2,026,813 nodes, 1,012,405 leaves, min margin 1, 1,003 pending leaves = state 0 plus 1,002 unrepaired contexts); nothing is running for the rest (§6). CP-SAT (2 workers, 480 s): no vector, no verdict |
| 21 | (63, 58) | h(F) ≥ 21, h(Lo) ≥ 12 | undecided; Knuth ≈ 10^7 (3 dives only, HEURISTIC); one witness found and killed (§4c). Searched since 20:31:42 by `nov13c-lo-tree-63-58` (phase-2 main loop, not this record; 8,184 contexts, 64 closed at 20:50) | **OPEN**: the §4c vector (h₀ = 0, h(F) = 21, h(Lo) = 12) satisfies all 2,650 Lean rows (exact re-check, phase 2) |
| 22, 23, 24 | (62, 59), (61, 60), (60, 61) | – | undecided; production-rule Knuth for t = 24: 10^8.0; the earlier 33-hole vectors of RES33N (60–62 F-states) lie here and are killed by certified rows | open: W0–W2 are 33-hole vectors over the Lean rows (`data/known_vectors_profile.json`) |
| ≥ 25 | (59, ·) | h(F) ≥ 25 | CLOSED (RES33N20261113 Result 3: 819,241 nodes) | t ≥ 27 closed (THEORY310N: capacity 57); t = 26 open (exact 33-hole vector with 58 F-states) |

Every tree has exactly one pending leaf, "state 0 missing", as in the 313 tree. No witness was met in the
trees for t = 18, 19 and 20. This includes all 2,048 contexts of slice 20, searched with the certified rows. No
witness was met in the Lean-rows trees of slices 18 and 19 either, nor in the repairs (slice 19: all 502
contexts; slice 20: 1,046 contexts).

**Replays (which tree, how often).** Every replay below uses `scripts/omission_tree.check_tree`.

| tree (directory in W) | nodes | replays |
|---|---|---|
| slice 18, certified rows (`cert_66_55/`, built in `bb_66_55_lo/`) | 3,611 | 2: `assemble.py` in the driver (17:11:55); `verify_cert.py` on the archived tree (17:12:51) |
| slice 18, certified rows, `pbb_fast` (`bb_66_55_fast/`) | 3,635 | 1: `assemble.py` in the driver (17:17:02) |
| slice 18, Lean rows (`bb_66_55_leanrows/`, archived in `cert_66_55_leanrows/`) | 3,815 | 3: driver (18:35:56); `verify_stream.py` output written 19:08:59 (separate run, inferred from file times); phase 2 from the archived tar and extra file (20:30:30) |
| slice 19, certified rows (`bb_65_56/`, archived in `cert_65_56/`) | 167,509 | 3: `assemble.py` in the driver (17:30:53); `verify_cert.py` on the archived tree (17:34:25); `verify_stream.py` (18:33:16) |
| slice 19, Lean rows (`bb_65_56_leanrows/`, archived in `cert_65_56_leanrows/`) | 186,077 | 3: driver (19:08:33); `verify_stream.py` output written 19:08:58 (separate run, inferred); phase 2 from the archived tar and extra file (20:30:49, 15.5 s, one process) |
| slice 19, Lean rows by repair (`bb_65_56_repaired/`) | 172,401 | 1: phase 2 (20:31:05) |
| slice 20, certified rows (`bb_64_57/`, not archived) | 3,468,657 | 2, both piecewise from `bb_64_57/`: driver in `nov13c-lo-tree-64-57` (20:28:37, 5 processes); the resumed unit `nov13c-lo-tree-64-57b` found nothing left to search and replayed again (20:29:53, 4 processes). Identical counts and hashes: extra `d12f624f…`, master `15cd5892…`, contexts digest `709a345e…` |
| slice 20, Lean rows, partial (`bb_64_57_leanrows/`) | 2,026,813 in 1,046 contexts | 1 partial: phase 2 (20:31:41, 4 processes, 24 s); verdict PARTIAL, as it must be |

### 4b. Pairs (by Lemma S)

Status of (c, c2) for the ES(8) ≤ 309 question, with the certified coupled rows.
"trivial" = c + c2 ≤ 120. "needs t = …" lists the open slices in max(18, 84 − c) ≤ t ≤ c2 − 37.

| c \ c2 | 54 | 55 | 56 | 57 | 58 | 59 | 60 |
|---|---|---|---|---|---|---|---|
| **66** (no N5 input) | trivial | **CLOSED** (t = 18) | **CLOSED** (t = 18, 19) | **CLOSED** (t = 18–20) | needs 21 | needs 21, 22 | needs 21–23 |
| **65** (ETV5N) | trivial | trivial | **CLOSED** (t = 19) | **CLOSED** (t = 19, 20) | needs 21 | needs 21, 22 | needs 21–23 |
| 64 | trivial | trivial | trivial | **CLOSED** (t = 20) | needs 21 | needs 21, 22 | needs 21–23 |
| 63 | trivial | trivial | trivial | trivial | needs 21 | needs 21, 22 | needs 21–23 |
| 62 | trivial | trivial | trivial | trivial | trivial | needs 22 | needs 22, 23 |
| 61 | trivial | trivial | trivial | trivial | trivial | trivial | needs 23 |
| 60 | trivial | trivial | trivial | trivial | trivial | trivial | trivial ((60, 61) needs 24) |
| ≤ 59 | CLOSED for every c2 (RES33N Result 3) | | | | | | |

Over the Lean rows alone, (66, 55), (66, 56) and (65, 56) are closed. The pairs (66, 57), (65, 57) and (64, 57)
need the Lean-rows slice 20, which is half done. Every pair that needs slice 21 is OPEN over the Lean rows alone,
because the §4c vector is a witness.

- (66, 55), (65, 56) and (64, 57) are single trees. (66, 56), (66, 57) and (65, 57) are closed by Lemma S from the
  slice trees and the Lean theorem Σh ≥ 33.
- **The most useful true sentences:**
  - "N66 ≤ 56 implies ES(8) ≤ 309" holds over the Lean rows alone (slices 18 and 19). It does not need
    N5 ≤ 65; with N5 ≤ 65 it is the single Lean-rows tree (65, 56).
  - "N66 ≤ 57 implies ES(8) ≤ 309" holds with the certified coupled rows (slices 18, 19 and 20). It does not
    need N5 ≤ 65; with N5 ≤ 65 it rests on the two trees (65, 56) and (64, 57).
- What an improvement of N5 would buy: with slices 18–20 closed, nothing until N5 ≤ 62 (§2).

### 4c. Witnesses and CP-SAT searches (COMPUTED / HEURISTIC)

| search | result |
|---|---|
| CP-SAT, pair (65, 58) (slices 19–21), 2 workers, 578 − 8 = 570 certified rows | one 33-hole vector after 218 s: **63 F-states and 58 Lo-states occupied** (h(F) = 21, slice 21). It violated 8 pooled transported rows; all 8 were certified by cake_lpr on the spot, so it is killed. Holes: `data/witnesses.jsonl`. Phase-2 exact re-check: 33 holes, state 0 occupied, 0 of the 2,650 Lean rows violated, 8 of the 578 certified rows violated |
| CP-SAT, pair (65, 56) (slice 19), 2 workers, about 10 min | no vector, no verdict (the exact tree then closed the slice) |
| exact trees t = 18, 19, 20 (with the certified rows), the Lean-rows trees t = 18, 19, and the repairs (slice 19 complete; slice 20, 1,046 contexts) | no witness met |
| CP-SAT, slice 20 over the Lean rows alone (`leanfind.py 20 480 2`, 19:09:54–19:17:54), 2 workers, 480 s | UNKNOWN: no vector, no verdict (`leanfind.jsonl`) |
| CP-SAT, budget 34, pair (65, 55), 1 worker, 150 s | no vector, no verdict |

No obstruction (a witness that cannot be killed) was found anywhere in this session.

### 4d. Budget 34 (the ES(8) ≤ 308 analogue), partial

For ES(8) ≤ 308 one needs 35 holes. With N5 ≤ 65 and N66 ≤ c2 the trivial threshold is c2 ≤ 54; the
first non-trivial pair is (65, 55): the single slice "h(F) ≥ 19, h(Lo) ≥ 15" at budget 34.
- Knuth estimate 10^6.2 nodes (77 dives, HEURISTIC); the first contexts suggest 3–4 million.
- Exact tree started and stopped: **24 of 3,792 contexts closed** (50,016 nodes, no witness), kept in
  `W/bb34_65_55/`. It ran 18:14:58–18:18:03 and was stopped to give its threads to slice 20. Undecided.
  Resume command in §6.

## 5. Controls

- **Row system.** `tools/common.py` pins the SHA-256 of `source-2650.json.gz`. `tools/check_f18.py`
  checks the nine-row identity behind h(F) ≥ 18 exactly.
- **Certified rows.** 570 rows come from RES33N20261113 (`certified.jsonl`, each with CNF and LRAT
  SHA-256 and the line `s VERIFIED UNSAT`); 8 more were certified in this session by the same
  `certify.py` (coupled CNF of the support → CaDiCaL 2.1.3 `--lrat` → cake_lpr). `lrat-check` is not
  used. The copy in W is `certified.jsonl` (589 lines, 578 distinct verified supports, 0 non-verified;
  unchanged since 17:01 and identical to `data/certified.jsonl`, SHA-256 `2f065615…`, at 20:41).
  The encoder `coupled.py` is byte-identical to RES33N's except for three work-directory paths.
- **Independent trees for the same slice.** Slice 18 was closed three times, by different engines and row
  systems: 3,611, 3,635 and 3,815 nodes, the last over the Lean rows only. Slice 19 over the Lean rows was
  closed twice: by direct search (186,077 nodes) and by repairing the certified-rows tree (172,401 nodes). Each
  tree replays exactly.
- **Monolithic against piecewise replay.** On slice 19 `verify_cert.py` (one assembled tree) and
  `verify_stream.py` (piecewise) return identical counts: 167,509 nodes, 83,755 leaves, one pending
  leaf, minimum margin 1.
- **Engine against engine.** `pbb_fast.py` and `pbb_fast2.py` with the direct-dual leaves switched on and
  dead-child picking off build the identical tree on six contexts of slice 20 (4,516 nodes each).
- **Witness detection is live.** The same driver, same rows, found the slice-21 vector by CP-SAT; the
  33-hole vectors of RES33N lie in slices 22–24 and violate certified rows (RES33N table). No
  positive-control witness run was made inside the exact engine at budget 33. Soundness of "CLOSED"
  does not rest on such a run, because it rests on the replay.
- **Knuth calibration.** For slice 19 the engine-exact estimate was 10^5.23 ≈ 170K nodes (60 dives) and
  the tree has 167,509 nodes. For slice 20 the estimate was 10^6.43 (25 dives) and the tree has 3,468,657
  nodes (10^6.54).
- **Source directory untouched.** `res33-20261113/certified.jsonl` and `newrows.json` have the same
  SHA-256 after the session as before (`81d27cb7…`, `6d97f3ae…`).
- **Phase-2 re-checks (20:30–20:39 KST).** Each check took under one minute. Outputs went to the phase-2
  agent's scratch directory, and nothing was written in W.
  - The slice-18 and slice-19 Lean-rows trees were extracted from `cert_66_55_leanrows/contexts_66_55_leanrows.tar`
    and `cert_65_56_leanrows/contexts_65_56_leanrows.tar` and replayed by `verify_stream.py` against the
    archived extra-row files (SHA-256 `1d6141af…`, `23134b33…`). The replays returned exactly the phase-1
    counts and the phase-1 master and context-digest hashes.
  - The repaired slice-19 tree and the 1,046 repaired contexts of slice 20 were replayed (§4a).
  - The §4c vector was re-checked exactly against the 2,650 Lean rows and the certified rows.
  - The row usage of the trees was counted by a read-only re-implementation of `rows_used.py` (the original
    writes `rows_used.json` into the tree directory).

## 6. Resumable state (all in W = `/home/jay/research/data/lo33-20261113`)

Run every command from the repository root; `PY` is the project venv python; `DL` is a deadline as a
Unix epoch. The driver keeps the master split, skips closed contexts, kills witnesses, and on completion
replays the tree (`LO_STREAM=1`: piecewise replay, needed above about one million nodes).

- **Slice 20 with the certified rows (pair (64, 57)): CLOSED.** The tree is `W/bb_64_57/`: `master.json`,
  `extra_v1.json` and 2,048 `ctx-*.json.gz`, 443 MB. Unlike slices 18 and 19, it was **not archived** into a
  `cert_64_57/` directory or into `data/`, because the phase-2 task allowed no new files. To archive it, copy
  `extra_v1.json` and a tar of `master.json` plus the contexts. Replay:
  `$PY W/verify_stream.py 64 57 W/bb_64_57 <procs>` (about 1 minute with 4 processes).
- **Slice 20 over the Lean rows alone: `W/bb_64_57_leanrows/`, 1,046 of 2,048 contexts.** These are the contexts
  that were closed in `bb_64_57` by 19:25, repaired by `nov13c-lo-repair20` (19:25:20–20:01:26, one process,
  248,691 leaves re-opened, 99,816 nodes added, no witness). No job is running for the rest. Next steps:
  1. Run `$PY -u W/repair.py 64 57 W/bb_64_57 W/bb_64_57_leanrows <procs> $DL`. It skips the repaired contexts
     and does the other 1,002, which contain 263,922 leaves that use certified rows. At the rate of the first
     part (8.7 ms per re-opened leaf) that is about 38 CPU-minutes (HEURISTIC).
  2. Run `$PY W/verify_stream.py 64 57 W/bb_64_57_leanrows <procs>`.

  If the result is CLOSED, then "N66 ≤ 57 ⇒ ES(8) ≤ 309" holds over the Lean rows alone. A witness would be a
  33-hole vector over the Lean rows in slice 20.
- **Slice 21 (pair (63, 58)), the next open slice.** At 20:31:42 the phase-2 main loop started
  `nov13c-lo-tree-63-58`: `LO_RULE=fast2 LO_STREAM=1 lotree.py 63 58 3 4096 <06:00 KST>`, 3 processes,
  `W/bb_63_58/`, log `W/logs/tree_63_58.log`. Its note in `phase2-20261113/main_loop_notes.log` reads
  "Python hedge … stop it if G2's C++ engine closes slice 21 first". Its master has 8,184 contexts and 3 master
  leaves; 12 contexts were closed at 20:41 and 64 at 20:50, with no witness so far. If it kills a witness, it appends rows to `W/certified.jsonl`; the
  copy in `data/` would then be out of date. At the Python rate of slice 20 (76 nodes/s per process), a tree of
  10^7 nodes needs about 36 process-hours. The C++ engine of FASTBB20261113 (same tree format) is the realistic
  route (HEURISTIC).
- **Budget 34, pair (65, 55)** (ES(8) ≤ 308 analogue): `W/bb34_65_55/`, 24 of 3,792 contexts closed.
  `LO_BUDGET=34 LO_OUT=bb34_65_55 LO_RULE=fast2 LO_STREAM=1 $PY -u W/lotree.py 65 55 <procs> 2048 $DL`
- A new slice t: `lotree.py <84 − t> <37 + t> …` (add `LO_NOCERT=1 LO_OUT=<dir>` for Lean rows only).
  The engines `fast`/`fast2` are for slices only (the two capacity demands must add up to the budget).
- `W/certified.jsonl` is this track's copy of the certified rows (RES33N's file is untouched).
- **Files that exist only in W** (the copies in `tools/` were made at 18:15–18:40). `tools/lotree.py` is an older
  version without `fast2`, `LO_NOCERT` and `LO_STREAM`; the version that ran is `W/lotree.py`. SHA-256 of the W
  versions:

  | file | SHA-256 |
  |---|---|
  | `lotree.py` | `b8125ee87517018363ad978ae3a737ebe8a2de72bc12bd6d34f5195728ae0685` |
  | `pbb_fast2.py` | `1fa2e0489b1d5ed0b56873958645bf8f39ad9bb1e36a39379b0ae7ae5b74bf64` |
  | `verify_stream.py` | `54ea1b34a896adfc105c9d3609dc029cf0aa548f2f5f9282f89558d46033ae1c` |
  | `repair.py` | `f1dc54aa149f8280c1c81bfcd17e07d252702c84252fbd07e561687b5342944f` |
  | `leanfind.py` | `520545c54c5432b16ae6335b158164f31f03583dc99e56a48c7f42261180488a` |
  | `rows_used.py` | `573eb6c4d51426971d4ededbf45fe96c96e8218d115495e880c0a5819103015b` |

  `ctxbench.py` also differs from its copy. These are in W only: the 24.5 MB tree `cert_65_56/tree_65_56.json.gz`,
  the context archives `cert_66_55/contexts_66_55.tar.xz`, `cert_65_56/contexts_65_56.tar.xz` and
  `cert_65_56_leanrows/contexts_65_56_leanrows.tar`, and all of `bb_*`. `data/` holds the extra-row files and
  verifier outputs of slices 18 and 19, the slice-18 tree, the slice-18 Lean-rows tar, and small tables.

## 7. Negative results and things that did not help

- **Production branching on slices** (zero strong-branching gains): 10 to 40 times larger trees (§3).
- **Score "min s"** (s = common slack of both capacity rows): Knuth 10^6.5 for t = 19, no better than
  the production rule. The one-sided score min h(Lo) is the one that works for small t.
- **Pseudo-cost preselection** of strong-branching candidates: 10^5.33 against 10^5.23 (t = 19, 60
  dives each): no gain.
- **Iteration-limited strong branching** (15 dual simplex iterations per child) doubles the node rate
  but also doubles the trees; K_LOW = 8 gives 28% fewer nodes for 25% more time. Parent-basis restore
  before each child LP: slightly slower. HiGHS Devex / Dantzig pricing, no scaling, primal simplex:
  all slower than the defaults.
- **Sub-slicing by block counts.** Fixing h(B_j) for the nine Baek blocks (Σ_j h(B_j) = 3t) splits
  slice 19 into 165 and slice 20 into 3,003 sub-slices. None is dead at the root LP; the slack
  histograms (`data/fine_lp_t19.json`, `data/fine_lp_t20.json`) predict a larger total than the single
  tree. Sub-slicing by h({f₁ = 6}) alone: the sub-slice h = 6 has the same LP value as the whole slice.
  Not pursued.
- **F-patterns are not few.** There are at least 4,915 hole sets inside F with exactly 18 holes that
  satisfy all rows inside F (CP-SAT enumeration stopped at 240 s, COMPUTED lower bound), so "enumerate
  the rigid F-side, then solve Lo" is not a shortcut.
- **CP-SAT** did not decide slice 19 in about 10 minutes on 2 workers; the exact tree needed about
  8 CPU-minutes × 5. CP-SAT did not decide slice 20 over the Lean rows in 480 s on 2 workers either.
- A path bug in `knuth3.py` (relative output path after `chdir`) wrote eight small estimate files into
  the repository root; they were moved to W at 18:40 and the script was fixed. The repository contains
  nothing from this track outside this record directory.
