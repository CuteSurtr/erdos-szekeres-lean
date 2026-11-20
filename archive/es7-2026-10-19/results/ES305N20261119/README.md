# ES305N20261119: ES(8) ≤ 305 (computer-assisted, unrefereed; 19 November 2026)

**Superseded for the bound (20:55): ES(8) ≤ 304, see ES304N20261119.** That bound uses the budget-67 tree with the
same method and tools. This record keeps the method, Lemma Z, the Lean files and the tools.

**Status (17:50 KST).** ES(8) ≤ 305 follows from four links:
- the balanced budget-66 **EXACT TREE**, checked by two implementations;
- **Lemma Z**: written proof, with exact controls on 300 point sets;
- **N66 ≤ 55** (CERTIFIED, N66N20261113; already an input of ES(8) ≤ 307);
- the residual half of the ES(8) ≤ 307 chain (ES307N20261118).

The last composition step is Lean-checked (`Composition305.lean`). Not refereed, not committed, no independent
re-check by another person or agent yet.

**Update 19:30: Lean now checks everything except the three computational inputs.** `BalancedBudgetsZ.lean` proves
`composition_305_z : ExcludesHoleBudgetZ 66 → N66Bound 55 → ResidualBound 118 → ForcesConvexNGon 305 8`, with
standard axioms only. Lemma Z is a Lean theorem (`LemmaZ.lean`; §3), and the 3,131 rows are Lean's own rows (§5). The
inputs that remain outside Lean:
- the budget-66 tree, which is exactly `ExcludesHoleBudgetZ 66` (EXACT TREE, two implementations, §4);
- N66 ≤ 55 (CERTIFIED by cake_lpr);
- `ResidualBound 118` (the 307 chain).

**Every 305-point set in general position contains 8 points in convex position.** The previous bound was 307 (18 Nov).

## 1. Statement

ES(8) ≤ 305. The new ingredient is a single extra row on the balanced side, the **Z-row**, which no earlier record used
(searched 19 Nov: no record applies N66 to the balanced states).

## 2. Model (the 310/307 decomposition, unchanged)

- Lean `Partition.forces_of_population_bounds`: `BalancedBound B` and `ResidualBound R` give `ForcesConvexNGon
  (B + R + 2) 8`.
- `ResidualBound 118` is the residual half of ES307N20261118 (h(C) ≥ 36; not Lean).
- `BalancedBound B` concerns the balanced part H: no 7-cap, no 7-cup, no convex octagon.
- Lean (`BalancedStates.lean`, `BalancedBudgets.lean`):
  - every point v of H gets a Ferrers state f_v : {0..4} → {0..5} (antitone; 252 states);
  - v ↦ f_v is injective;
  - the hole vector h (h_s = 1 if no point has state s) satisfies the 3,131 catalog rows (`feasible_holes`), and
    Σ h = 252 − |H|.

## 3. Lemma Z (PROVED, written; new here)

- **Definitions.** capLabel(u, v) + 1 and cupLabel(u, v) + 1 are the numbers of points of the longest cap and cup in H
  ending with the edge (u, v) (`ActualRanks.labels` = (rank cap − 1, rank cup − 1), both in [1, 5]). The state is
  f_v(i) = max{cupLabel(u, v) : u < v, capLabel(u, v) ≥ i + 1}, or 0 if there is none (`BalancedStates.column`).
- **The class.** Z = {f : f(0) ≤ 4, f(4) = 0}. These are the antitone f(0..3) ∈ [0, 4] with f(4) = 0: C(8, 4) = **70
  states**, state 0 included.
- **Lemma Z.** The owners Z_H = {v ∈ H : f_v ∈ Z} contain no 6-cap and no 6-cup. Hence Z_H is a point set in general
  position with distinct x-coordinates, no 6-cap, no 6-cup and no convex octagon, so |Z_H| ≤ N66 ≤ 55. By
  injectivity at most 55 states of Z are occupied, which gives the **Z-row**: Σ_{s∈Z} h_s ≥ 70 − 55 = 15.
- **Proof.** Let p1 < … < p6 lie in Z_H.
  - If they form a 6-cup, it is a 6-cup of H ending with the edge (p5, p6), so cupLabel(p5, p6) ≥ 5. Every edge has
    capLabel ≥ 1, so f_{p6}(0) ≥ 5: a contradiction.
  - If they form a 6-cap, then capLabel(p5, p6) ≥ 5 = 4 + 1, so f_{p6}(4) ≥ cupLabel(p5, p6) ≥ 1: a contradiction. □
- It is the exact analogue of the residual Lemma A (THEORY310N; capacity row (Lo, 70 − N66)), now on the balanced
  states.
- **Lean (19:25, `LemmaZ.lean`, namespace `OmissionZRow`).**
  - `Z` is defined from the Lean `catalog` by f(0) ≤ 4 ∧ f(4) = 0.
  - `Z_eq` (by `decide +kernel`) pins it to the 70 indices of `zrow.json`.
  - `zOwners_no_cup` and `zOwners_no_cap` are the two halves of the proof above, on `column` and `labels`.
  - `z_row : N66Bound 55 → … → 15 ≤ (Z \ c.occupied).card` is the Z-row in the form of
    `OmissionBalanced.all_geometric_rows`.
  - `N66Bound B` says that every `Configuration` with no 6-cap, no 6-cup and no convex octagon has at most B points.
  - Compiled with `lake env lean` in 6 s: no `sorry`, axioms propext, Classical.choice and Quot.sound.
- **Exact controls** (`bal186-20261119/zrow/lemmaz_control.py`, own code from the Lean definitions):
  - 300 random integer point sets (12–40 points, no 7-cap, no 7-cup): the states are pairwise distinct, and Z_H
    never contains a 6-cap or a 6-cup;
  - negative control: the wider class f(0) ≤ 5 contains a 6-cup in 191 of the 300 sets.

## 4. The budget-66 tree (EXACT TREE, two implementations)

- **Rows.** The 3,131 rows of `balanced-v2-source.json` (Lean catalog, SHA-256 `acaf6323…`), then the Z-row
  (support Z, rhs 15). Files: `balz.rows`, and `zrow.json` for the checkers.
- **State 0 is free.**
  - The tree branches on state 0. The zero side (0 occupied) is a fastbb256 packet on `balz.rows` at budget 66.
  - The one side (0 missing) is a packet on `balz_m0.rows` at budget 65. That file has state 0 removed from every
    support, every rhs containing 0 lowered by one (the Z-row becomes 14 on 69 states), and row indices kept, so the
    margins are equal in the original instance.
  - fastbb256 fixes state 0 occupied internally. That is the identity on the zero side and has no effect on the one
    side, where 0 is in no row.
- **Finder.** `zb_run.sh 66 10 1024` (fastbb256 `--ktop=16 --klow=4 --dtop=0 --dmid=0 --on-witness=stop`), 17:25-17:40.
  Both sides closed: rc 0, no witness, 1,024 contexts each.
- **Check A.** `balz_assemble.py` v2 writes one file per master leaf, its path starting with the state-0 literal.
  Each file is replayed by `scripts/omission_tree.check_tree` on the original rows plus the Z-row at budget 66,
  prefixed by its path (pending == path length).
  - Result: **EXACT TREE**: 2,048 files, 1,285,734 nodes, 643,891 leaves, minimum margin 1, no bad file.
- **Check B.** `balcheck` (own C++, independent of check_tree and of fastbb; leaf rule derived in its header; exact
  `__int128`), with the Z-row through `BALCHECK_EXTRA_ROWS`.
  - Result: **"EXACT TREE (balcheck)"**: 2,048 contexts, same nodes and leaves, minimum margin 1, and the path
    cover is **complete** (the 2,048 paths are the leaves of one complete binary decision tree).
- **Conclusion.** No 0/1 vector on the 252 states with at most 66 holes satisfies the catalog rows and the Z-row. The
  actual hole vector of H satisfies both (Lean, Lemma Z) and has 252 − |H| holes. So 252 − |H| ≥ 67:
  **BalancedBound 185**.

## 5. Composition (Lean-checked)

`Composition305.lean`: `composition_305 : BalancedBound 185 → ResidualBound 118 → ForcesConvexNGon 305 8` and
`avoiding_304`. `lake env lean` gives rc 0; axioms only propext, Classical.choice and Quot.sound.

**`BalancedBudgetsZ.lean` (19:30): the balanced half in Lean, down to the tree.**
- `ExcludesHoleBudgetZ b`: no 0/1 vector on the 252 states with at most b holes satisfies:
  - the 2,685 rows of `OmissionBalanced.all_geometric_rows`;
  - the 446 cuts of `BalancedCoverCutsV2.all_rows`;
  - the Z-row.
- `feasible_holes_z` (from `OmissionBalanced.feasible_holes`, with the cuts and `z_row` added): the actual hole vector
  satisfies all of them, and Σ h = 252 − n.
- `balanced_bound_of_hole_budget_z : N66Bound 55 → ExcludesHoleBudgetZ b → BalancedBound (251 − b)`.
- `composition_305_z : ExcludesHoleBudgetZ 66 → N66Bound 55 → ResidualBound 118 → ForcesConvexNGon 305 8`, and the
  analogous `composition_304_z` with budget 67 (a statement about inputs, not a claim).
- **Build.** `tools/build.sh` (unit `esr-lean-z`) compiles against the chain311 oleans of the ES(8) ≤ 310/311 compact
  pipeline (`BalancedRows`, `BalancedCoverCutsV2`; built 5–6 Nov, against the main-library oleans of 4 Nov, which are
  still the current ones). LemmaZ takes 5.2 s and 3.8 GB RSS; BalancedBudgetsZ takes 2.7 s and 3.2 GB.
  - All three theorems print only propext, Classical.choice and Quot.sound.
- **Rows.** `tools/rows_match.py` parses `BalancedProof/Catalog.lean` (2,685 rows in `rowChunks` order) and
  `BalancedCoverCutsV2.lean` (446 cuts), and compares them with the 3,131 constraints of `balanced-v2-source.json`.
  - Result: 0 mismatches in support or demand, same order.
  - So the trees' rows (`balz.rows`: JSON rows + Z-row) are exactly the rows of `ExcludesHoleBudgetZ`.

## 5b. Fixed states and zero-side-only trees (19:45; for budget 68)

- **Lean (`FixedStatesZ.lean`, namespace `OmissionBalancedZF`; `tools/build_fixed.sh`; 5.0 s, 3.6 GB RSS).**
  - `owner_zero`: the first point of a balanced configuration has state 0 (`column_zero`: no incoming pair).
  - `owner_one`: the second point has state 1 (`labels_zero_one`: the pair (0, 1) has labels (1, 1); `column_one`).
  - Hence `zero_mem_occupied` (n ≥ 1) and `one_mem_occupied` (n ≥ 2).
  - `ExcludesHoleBudgetZF b` is `ExcludesHoleBudgetZ b` restricted to h_0 = h_1 = 0, and
    `balanced_bound_of_hole_budget_zf : b ≤ 249 → N66Bound 55 → ExcludesHoleBudgetZF b → BalancedBound (251 − b)`.
    The case n ≤ 1 is trivial.
  - `composition_304_zf` and `composition_303_zf` (budgets 67 and 68) are statements about inputs.
  - Axioms: propext, Classical.choice and Quot.sound only.
- **Consequence.** A tree for budget B needs only the zero side (state 0 occupied). The "state 0 missing" side, about
  40 % of the work at budgets 66 and 67, is excluded in Lean.
- **Fixing state 1 as well does not help** (Knuth dives at budget 68, HEURISTIC, 200 dives each, seed 1, default
  options, `fix/`; state 1, and state 3, removed from every support):

  | fixed occupied | estimate (nodes) |
  |---|---|
  | {0} (reference `dz_b68`) | 6.5e7 ± 0.8e7 |
  | {0, 1} | 1.10e8 ± 0.19e8 |
  | {0, 1, 3} | 9.5e7 ± 1.2e7 |

  The LP keeps these states occupied anyway, and the finder's branching changes. The budget-68 plan therefore fixes
  only state 0 (state 3 would have come from the mirror symmetry).
- **Tools (work dir `zrow/`).**
  - `balz_assemble_v3.py`: v2 plus MIS = "-", meaning zero side only.
  - `../balcheck/balcheck2.cpp`: v2 of balcheck. The environment variable `BALCHECK_LEMMA_PATHS` lists paths that
    count as cover leaves without a file, and the verdict names them.
  - `zb_run0.sh B T C`: the zero-side-only driver, output in `b<B>z/`.
- **Controls (`fix/t66/run.sh`, on the budget-66 zero side alone, 1,024 files).**

  | run | result |
  |---|---|
  | check_tree | EXACT TREE: 771,030 nodes, 386,027 leaves, minimum margin 1 |
  | balcheck2 with lemma path "0:1" | "EXACT TREE (balcheck)", cover "complete with 1 lemma path(s) 0:1" |
  | without the lemma path | rejected, "incomplete cover" |
  | wrong lemma path "0:0" | rejected |
  | one file left out | rejected |

  - The budget-66 zero side plus `zero_mem_occupied` is therefore a second proof of `BalancedBound 185`, through
    `ExcludesHoleBudgetZF 66`.
- **Budget-68 cost (HEURISTIC).** The b66 and b67 zero sides were 2.6× and 3.0× their dive estimates, so expect about
  2e8 nodes.
  - Finder: b67 ran at 169 nodes per thread-second, so about 27 h with 12 threads.
  - check_tree: about 3 h. Disk: about 60 GB of finder files plus about 60 GB of assembled files.
  - **Owner OK at about 20:15: 14 threads.** The chain unit `esr-bal-chain68` (`zrow/chain68.sh`) waits for budget 67.
    It starts `esr-bal-zb68` (`zb_run0.sh 68 14 16384`, output `b68z/`) only if budget 67 passes check_tree and
    balcheck with a complete cover. Log: `zrow/chain68.log`.

## 6. Controls of the checkers

- `balcheck`, on the budget-64 trees behind 310:
  - B = 64: EXACT TREE, 4,096 contexts, 7,048,218 leaves, cover complete;
  - B = 65 with the header check off: all 4,096 rejected ("leaf margin < 1");
  - 4,095 contexts: "incomplete cover".
- `balcheck` and `check_tree` agree on every pilot tree of ES306N20261119 §6.1. At B = 66 those budget-65 pilot trees
  are rejected by `balcheck`.

## 7. Files and hashes (work dir `/home/jay/research/data/bal186-20261119/zrow`, 1.1 GB for b66)

| file | SHA-256 |
|---|---|
| `balz.rows` (3,132 rows) | `7076dd8212c382caf19b7fe39fca9b81de9ae8fba9150727efa1997d54f6288f` |
| `balz_m0.rows` | `6fb2337976f23ffd328f3704d6905af57441009ff5d469316e264b816250f055` |
| `zrow.json` | `b43ba5f80582f7754fe6acf04cbbf81fc7822a5f784fb8c5ddedf643cce51258` |
| `b66/occ/master.json` | `6354a5cae50247679b07600a771b2e046e171372959c371e088706ffc98daf13` |
| `b66/mis/master.json` | `537241fa44429ad8aac71c94ffe4c0129a72a2473d2e21afd0ab84858741209d` |
| `balz_assemble.py` (v2) | `ae0411c1c7503792a4ee9dd39919611609dbe72b0939375328f252af858d63a2` |
| `zb_run.sh` | `aa7350f11d220eadd7b0de465c6a63d9ac398757ca8311768e03acb7b7bbd781` |
| `zb_check.sh` | `3c5f32d65ff05a3703be2d03f6e376fe8655a6daf78b2b6c42090549269acb46` |
| `../balcheck/balcheck.cpp` | `554814faf9336b2d7a4e7ec2c236fcb6ceaead3dd640f2cacdeef10c64e4cde3` |
| `../balcheck/balcheck` (g++ 15) | `bd55b6a63908fc215df72fd6b614ea6848cc4bbd25ef2b4deb7b6b5757278f48` |
| `lemmaz_control.py` | `ae317cefd6c707d8977dd0b647a25cf1bd7b3c286153774bc7680609e25ae578` |
| `../fastbb256` (finder) | `df17fa7471f27ab80afe34363d4945b324ac1e007e27e1f8dbadd2d342c4cc90` |
| `LemmaZ.lean` (record) | `e6b28efaa80cb2158180daf12dd4ce76cf2b86cc833ae9d79b1c08ffca005d65` |
| `BalancedBudgetsZ.lean` (record) | `3e0651a023a58df5a9a0fff4c7d0fc1c5859dfe40b67e9a4e17cdc313224ab1a` |
| `Composition305.lean` (record) | `d7d1b2c30d6986ab5104630054e663bb5639e0f67fb3fa03ab1ef5c82b05eeae` |
| `tools/rows_match.py` | `136ecaabe05390ac4617f1d28c628711da9eed84cefe06e21f467ef65a25e743` |
| `tools/build.sh` | `f24290195536c3e55d3b7d195db198a6db17cd204814f38b1d3a5a63588b8899` |
| `leanz/olean/LemmaZ.olean` (work dir) | `ef249ba167372ac31f995027299efa1eeddac251ff73e4ef093a990ab02c353c` |
| `FixedStatesZ.lean` (record) | `20945f03e3c2ea7623f8cebcfd92622a3b13cf49c01bb20c863d71d2a2818988` |
| `tools/build_fixed.sh` | `b5745752e831466f88cb8d8e104b0c8a82bc93fbb7c365fc57e784d17077165d` |
| `zb_run0.sh` | `fe9f5e18082e708061b5753152b7e79d1c256ff362e873a1e636db21a9d87b0b` |
| `balz_assemble_v3.py` | `eddc2b9837d60cc2a46731646a2d7a9c77c734979d001ae32686b0be3df174f5` |
| `../balcheck/balcheck2.cpp` | `83d14a9f89aedcbbefaee48cdf4ec02210140450e0c6e506e722ecc127408af2` |
| `../balcheck/balcheck2` (g++ 15, -O2) | `951b90dc19c8b54c3f65871481f300dc6678338dbd2c76a80147e5feed984661` |
| `fix/mkfix.py` | `2cdb78b51f6faccb634a9bd1a829ea081a486a178d7b784e592a77e8244099a5` |
| `fix/t66/run.sh` | `7755dd09ff09909cbc95b2cbf3b42b841197108ffb44a5bf3802d3e3962e2fde` |

## 8. What remains

- An independent re-check by another reader or agent: Lemma Z (now also in Lean), and both tree checks re-run.
- Done 19:30: the Lean proof of Lemma Z and the Lean composition down to `ExcludesHoleBudgetZ 66` (§3, §5).
- A literature check before any public wording (last full check: R/NOVELTY20261113B).
  - Quick re-check, 19 Nov 19:50: three web searches plus the Zenodo versions API for record 22842891.
    - No planar ES(8) bound newer than this project's was found.
    - Schroeder's record (ES(8) ≤ 319) is still version 1 only (total = 1).
    - The other hits (arXiv 2604.20120, 2607.02958, 2512.24061; Baek–Balko, JCTA) are all in NOVELTY20261113B.
  - "New" means only "not found in this search". This is not a full check.
- Budget 67 (gives 304): started 17:42 (unit `esr-bal-zb67`, 12 threads, 4,096 contexts per side). Budget 68 (gives
  303): Knuth estimate 6.5e7 nodes for the zero side alone. The budget-66 actual tree was about 4× its estimate, both
  sides together.
- **The next lever (HEURISTIC LP, `zrow/lp_n67.py`).** Only N66 among the certified octagon bounds goes below its
  class's cups–caps count. Checked: N5 ≤ 65 against 56 states, Baek's 22 against 21, and ETV(5-cap, 6-cup) = 35 =
  cups–caps.
  - A bound on **N67** (no 6-cap, no 7-cup, no octagon; mirror-equal to N76) would give capacity rows on the classes
    {f(4) = 0} and {f(0) ≤ 4} (126 states each).
  - Root LP with the Z-row: 60.2. Adding N67 ≤ 100: 60.2; ≤ 90: 62.2; **≤ 80: 71.4**; ≤ 70: 80.7; ≤ 60: 90.0.
  - ETV predicts N67 = 56. **N67 ≤ 80** would be about 24 above the predicted truth (N66 ≤ 55 was within 5) and would
    move the balanced side by about 11 holes at the root.
- **Other levers checked 19:30–19:40 (HEURISTIC, `zrow/cuts/`; negative results).**
  - **Rounding cuts at the root** (`sep_z.py`): rounded cover cuts with capacity 2 from pairs and triples of tight
    rows, the Lean `rounded_cover_cut` family, found **no violated cut**. That covers 16,020 pairs and 1.8 M triples
    on the 321 tight rows.
    - The root LP point with the Z-row is very spread out: 233 of the 252 values are fractional, all ≤ 0.5.
  - **Z-row sensitivity** (`lp_zsens.py`): root LP 60.23, 61.05, 61.88, 62.71 and 64.37 for Z-row rhs 15, 16, 17, 18
    and 20, i.e. N66 ≤ 55, 54, 53, 52 and 50. **Each unit of N66 is worth 0.83 at the root**, about one budget
    step. N66 ≤ 54 would make budget 68 cost about what budget 67 does now. N66 ≤ 55 needed a cube campaign of
    several days at 16 threads (N66N20261113).
  - **Classes Y = {f(3) = 0} and Y′ = {f(0) ≤ 3}** (56 states each; owners have no 5-cap and no 7-cup, resp. the
    mirror; ETV value 41) (`lp_y75.py`):
    - LP min h(Y) is 3.5 and LP min h(Y′) is 3.0;
    - but even h(Y), h(Y′) ≥ 15 (the ETV truth) leave the root LP at 60.226;
    - the optimum already has those holes. No lever.
  - **N67** (§8 above): ETV5N20261113 §6 set up the 4 × 5 box (126 states) and reached at most "≥ 18 holes" from
    cycle rows. The lever starts only at ≥ 36 holes (N67 ≤ 90). Not pursued.
  - **N67 revisited (20 Nov 00:32–00:47; HEURISTIC LP/MIP unless stated; scripts in `zrow/lift/`).** This corrects the
    two bullets above.
    - **Four classes, not two.** THEORY310N Lemma B adds K3 = {f(0) = 5} (a 6-cup ends, so no 6-cap) and K4 =
      {f(4) ≥ 1} (mirror) to K1 = {f(4) = 0} and K2 = {f(0) ≤ 4}. All four have 126 states and occupancy ≤ N67, and
      K2 ∪ K3 is all 252 states. So Lemma B alone gives h ≥ 252 − 2·N67.
    - **Root LP with all four rows** (`lp_n67.py`):

      | N67 ≤ | 100 | 98 | 96 | 95 | 94 | 93 | 92 | 91 | 90 |
      |---|---|---|---|---|---|---|---|---|---|
      | root LP | 60.2 | 61.6 | 63.3 | 64.2 | 65.1 | 66.0 | 68 | 70 | 72 |

      The lever starts at N67 ≤ 98, not 90. N67 ≤ 96 would make budget 71 cost about what budget 68 does now
      (ES(8) ≤ 300). From N67 ≤ 92 down, Lemma B alone decides (n_H ≤ 2·N67).
    - **What the existing rows give** (`n67_restricted.py`). An N67-class set is an H-class set whose states lie in
      K1, so the 3,131 rows plus the Z-row restricted to K1 bound N67: LP 19.69 holes, MIP optimum 23 (incumbent =
      bound), so **N67 ≤ 103** (HEURISTIC until an exact tree replays it). An integer vector attains the optimum, so
      no cut on these rows helps.
    - **A second Z-type row inside the N67 class (PROVED, written).** In an N67-class set T, let P be the points where
      a 5-cap ends (f(3) ≥ 1, 70 states). If r1 … r6 in P form a 6-cup and c1 … c4 r1 is a 5-cap, then (c4, r1, r2)
      is a cap, which gives a 6-cap c1 … c4 r1 r2, or a cup, which gives a 7-cup c4 r1 … r6. So |P| ≤ N66 ≤ 55 and
      h(P) ≥ 15. Likewise the points where a 6-cup ends (f(0) = 5) have no 5-cap (N75 class).
    - **These recursions do not reach the lever** (`n67_restricted2.py`). The P-row moves the LP to 20.47 holes but
      leaves the MIP at 23. Even N75 ≤ 46 would give only N67 ≤ 101, and N75 ≤ 41 (the ETV value, i.e. the conjectured
      truth) only N67 ≤ 96.
    - **Lifted N66 rows: no gain** (`lift_probe.py`). For a down-set D within Z, the owners of D form an N66-class set
      whose own states lie in D, so h(D) ≥ |D| − M(D). The bound M(D) from the 15,648 certified N66 demand-one rows
      (`n66-20261113/mono/rows_1832.json`) falls short of the root LP's occupancy for all 89 candidate down-sets
      tested (best gap −0.99). On D = Z the row store gives only M ≤ 63 against the campaign's 55.
    - **Conclusion.** N67 ≤ 96 needs N67-specific geometry: coupled rows, monolithic families and cubes, as N66 did,
      now on 126 states and 126-owner configurations. N66 needed 9 holes beyond its cycle-row bound and N67 needs 7
      beyond its row bound, but the instance is much larger. No cost basis yet. It is the largest lever found.
  - **Z*-row: valid, Lean-checked, about one budget step (20 Nov 00:40–01:35).** First read as useless from
    default-option dives; the real budget-66 tree and the production-option dives below correct that.
    - **Lemma (PROVED, written; Lemma B both halves).** Let Z* = {f(0) = 5, f(4) ≥ 1}: 70 states, transpose-closed,
      disjoint from Z. Its owners are the points where both a 6-cup and a 6-cap of H end. Let y1 … y6 be a 6-cap among
      them, and c1 … c5 y1 a 6-cup. Then (c5, y1, y2) is a cup, which gives a 7-cup, or a cap, which gives a 7-cap.
      The 6-cup case is the mirror. So the owners form an N66-class set, and N66 ≤ 55 gives h(Z*) ≥ 15.
    - **Exact control** (`lift/zstar_control.py`, own code): the cup–cap construction X(7,7) (252 points, all 252
      states occupied, 70 Z*-owners) and 150 random subsets. Injectivity, Lemma Z and the Z*-lemma hold on all 151.
      Negative controls: owners of {f(0) = 5} alone contain a 6-cup in 151 of 151, owners of {f(4) ≥ 1} alone a
      6-cap in 137.
    - **Root LP** (`lift/lp_zstar.py`): 60.23 → **66.00** with the Z*-row; rhs r gives 54 + 0.8 r.
    - **But the dives get worse** (`zrow/dives_zs.sh`, fastbb256 dive, 200 dives, seed 1; `balzs.rows` = balz.rows +
      the Z*-row):

      | budget | rows | mean | median | max |
      |---|---|---|---|---|
      | 68 | catalog + Z | 6.5e7 | 2.5e7 | 8.1e8 |
      | 68 | catalog + Z + Z* | 5.7e8 | 4.2e6 | 6.9e10 |
      | 70 | catalog + Z | 3.2e10 | 8.6e9 | 1.1e12 |
      | 70 | catalog + Z + Z* | 5.4e11 | 1.7e10 | 5.3e13 |

      A valid row cannot enlarge a tree with fixed branching. Here the finder's branching follows an LP point that
      spreads the 15 Z* holes thinly, and the dives run deeper (median depth 33 against 31 at budget 70). Z* states
      (long cups and caps ending) are rarely occupied, so near-budget integer vectors probably have many Z* holes
      already; the row cuts off fractional points only. Compare Z, whose states are usually occupied.
      Those were default-option dives. The production runs use `--ktop=16 --klow=4 --dtop=0 --dmid=0`.
    - **Real tree, budget 66, zero side** (`zrow/zs66/`, 1 thread): the master phase closed everything, **5,151
      nodes** in 93 s, against **771,030** nodes without the Z*-row (b66). Replayed by the v4 pipeline: check_tree
      EXACT TREE (2,576 files, 3,133 rows, minimum margin 1) and balcheck2 EXACT TREE, cover complete with the lemma
      path 0:1.
    - **Production-option dives** (200 each, seed 1; mean, median):

      | budget | without Z* | with Z* |
      |---|---|---|
      | 67 | 2.2e7, 8.4e6 (real tree 1.37e7) | not run |
      | 68 | 9.0e8, 2.7e8 | **1.05e8, 8.4e6** |
      | 69 | 8.4e9, 2.2e9 | 8.9e9, 1.1e9 |
      | 70 | not run | 1.4e11, 4.3e9 |

      The Z*-row cuts budget 68 by about 9× (mean) and 32× (median) and does nothing measurable at 69. With the
      budget-67 ratio of real tree to estimate (0.62): about 5.6e8 nodes for budget 68 without Z* (about 2.5 days at
      14 threads; the running job's nodes per context were rising) and about 6.5e7 with it (about 7 h).
    - **MIP check** (`lift/mip_zstar.py`, HEURISTIC): the best integer vectors found (76 holes) have 9–11 Z* holes, so
      the row cuts off integer vectors too.
    - **Lean (20 Nov 01:20, `zrow/leanzs/`, build_zs.sh; all standard axioms).**
      - `LemmaZStar.lean`: `Zs_eq` (decide +kernel, pins `zstar.json`), `zsOwners_no_cap`, `zsOwners_no_cup` (the
        Lemma B argument via `rank_attained`, `rank_lt_of_avoids` and one `EndingPath` extension), and `zs_row :
        N66Bound 55 → … → 15 ≤ (Zs \ c.occupied).card`. 6.7 s.
      - `BalancedBudgetsZZs.lean`: `ExcludesHoleBudgetZZsF b` (catalog + Z-row + Z*-row, h_0 = h_1 = 0),
        `balanced_bound_of_hole_budget_zzsf` and `composition_303_zzsf` … `composition_300_zzsf`
        (budgets 68–71). 2.5 s.
    - **Switch (01:33).** The budget-68 job without Z* (`esr-bal-zb68`, 2,754 of 16,384 contexts after 4.5 h) was
      stopped. Its closed contexts stay in `zrow/b68z/` (2,774 files), so `zb_run0.sh 68 14 16384` resumes it.
      Budget 68 restarted as `esr-bal-zbs68` (`zbs_run0.sh 68 14 16384`: `balzs.rows`, `balz_assemble_v4.py`,
      balcheck2 with `zzs_rows.json`; output `zrow/b68zs/`), on the same 14 threads and limits.
- **Rounding cuts inside the tree (22:00, HEURISTIC, `zrow/cuts/node_cuts.py`, `add_cuts.py`, `node_lpgain.py`).**
  - Random dives at budget 68 (seed 1): 132 of the 134 nodes within 3 of the pruning threshold carry violated
    capacity-2 cuts. That gave 313 distinct cuts, each re-derived exactly from its parent rows (`add_cuts.py`).
  - Fresh dives (seed 2) with that pool appended: median LP gain 0.025, 90th percentile 0.07, 4 of 132 nodes
    pruned.
  - Knuth estimate at budget 68 with the pool: 1.08e8 ± 0.17e8, against 6.5e7 for the reference.
  - The cuts are node-specific, so this is no lever.
- **Residual side (22:10, `zrow/resid/lp_n5.py`).**
  - In the b36 slice model the capacity classes F (84 states, the N5 class) and Lo (70 states, the N66 class) are
    disjoint and cover all 154 residual states. So h(C) = h(F) + h(Lo), and the root LP is exactly
    (84 − N5) + (70 − N66): 33 for 66 + 55.
  - Hence |R| ≤ N5 + N66, as in THEORY310N Lemma A. With N66 ≤ 55, the first useful step is **N5 ≤ 62 → ResidualBound
    117** (no tree needed). Each further unit of N5 is one point of ES(8).
  - N5 ≤ 65 is the record (ETV5N20261113; ETV value 42), and ROADMAP20261115/SYNTHESIS §2.1 item 7 found "no credible
    cost basis" for N5 ≤ 63/62 (stalled after 439 cores). Not scheduled. N66 ≤ 54 is not scheduled either: the level
    13 → 14 step cost about 3 days of cubes.
- The Lean-rows-only budget-65 campaign (ES306N20261119 §6.1) is stopped, with 40 contexts kept. It is superseded
  for 306, but would give a 306 that does not depend on Lemma Z.

## 9. Resume

```bash
cd /home/jay/research/data/bal186-20261119/zrow
./zb_run.sh <B> <threads> <contexts>     # finder both sides + assembly + check_tree + balcheck
./zb_check.sh <B> <threads>              # assembly + both checks on existing packets
```
