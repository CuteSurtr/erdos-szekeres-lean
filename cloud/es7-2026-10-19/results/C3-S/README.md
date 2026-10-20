# Task C3-S: a sound decomposition of the 3-fold class, measured

Class: 33 points in general position, invariant under a rotation by 120°, no convex 7-gon
(m = 11, k = 7 in the C3a/C3b centre-pencil normal form).

Nothing here is a theorem. "UNSAT" is a claim about one CNF, and it counts only when both
lrat-check (with the E2 patch) and cake_lpr accept the LRAT proof. The cover argument is a
paper proof (`soundness.md`) backed by exact-coordinate tests, not a formal proof.

## Summary

STATUS_PLACEHOLDER

## What ran where

One cloud VM: 4 cores, 15 GB RAM, no swap (`env.txt`), from 04:49 to about 08:45 UTC on
2026-10-20. Up to 6 solver processes shared the 4 cores at times, so wall-clock numbers are
upper bounds on single-core times (about 1–1.5× inflated). Tools were built from source:

- CaDiCaL 3.0.1 (c6073042)
- march_cu (CnC 705b60c, `-fcommon`, `mem_max = 600000000` as in C3a)
- cake_lpr (built from the repository's `cake_lpr.S`)
- drat-trim lrat-check (2e3b2dc) with `results/E2/tools/lrat-check-E2.patch`
- pysat 1.x (cadical195) for incremental probes only. Its results are never used as closures.

## The decomposition (details and proofs: `soundness.md`)

1. **Hull normalization (the task's idea; the argument holds).** The line l can be turned so that
   any point gets label 0, and the point reflection keeps labels, so label 0 is a hull vertex
   and σ_0 = 0. The hull H is a union of R-orbits with |H| ≤ 6, so |H| is 3 or 6. Moving label 0
   to the other hull orbit maps residue a to m − a, so a ≤ 5 can be assumed. Splitting on
   σ_a gives **11 top cases: H3, H6(a, s) for a = 1..5 and s = 0, 1.** The hull order is the
   angular order about c, given by the key (σ_i, i). Each case adds unit clauses
   ccw(u, v, w) for every hull edge (u, v) and every other point w (93 units for H3, 187 for
   H6), plus σ_a = s.
2. **Convex layers (generalization).** The same argument applies to every convex layer: each
   layer is one or two R-orbits, its order is the (σ, label) order, and its edges have the rest
   strictly to the left. A node of the layer tree fixes L_1..L_j. Its children are every one-orbit
   choice and every two-orbit choice with both σ values for the next layer (`tree_children`).
3. **Mirror reduction below H3 (new).** The reflection in l maps an H3 configuration to an H3
   configuration with (residue r, σ) ↦ (m − r, 1 − σ). Below H3 we keep one layer-2 option of
   each mirror pair: 100 of 190.
4. **Composition.** The class is empty if the set of certified nodes is a cut of the tree.
   `tools/compose.py` checks the cut and recomputes every certified node's CNF sha256 from the
   base CNF and the node name.

Case CNF = base CNF (`gen_case.py 11 7 none`, byte-identical to C3a's chain CNF, sha256
`bf0e502e…`) + the node's unit clauses. Both C3a and C3b encoders are supported
(`--enc c3b`).

## Validation (all passed)

- **Hull cover on random sets** (`tools/validate_hull.py`, `logs/validate_hull.jsonl`,
  `logs/validate_layers_m11.jsonl`): 2,950 random C3-symmetric sets with exact Z[√3]
  coordinates, m = 3..11, shapes chosen so the hull is often 3 or 6. 2,379 had hull size 3 or 6
  and were canonically relabelled. For each, every clause of its case CNF was evaluated on the
  true assignment, with 0 failures: core clauses true, hull units true, and 7-gon clauses true
  exactly when the brute-force `convk` finds no convex k-gon. All 11 m = 11 cases occurred
  (H3: 500; H6 cases: 49–202 each). The sets with hull ≥ 9 all had a k-gon, as they must.
  The convex layers were also peeled from the coordinates, and the layer units of every prefix
  were true: 5,808 layers checked. The hull clauses of every other case were false in every
  set ("other_case_hull_ok": 0).
  One run first reported a failure, "no canonical l found": random integer directions missed
  a very narrow angular gap. An exact constructive choice of l was added. The same set then
  passed, with 0 failures (`logs/validate_layers_m11_v1_randomdir_only.jsonl` is the first run).
- **Mutations are caught** (`tools/mutation_hull.py`, `logs/mutation_hull.jsonl`): the swapped
  σ orders, the reversed orientation and the wrong rotation direction fail on 30/30 H6 sets.
- **Mirror map** (`tools/validate_mirror.py`, `logs/validate_mirror.jsonl`): 900 H3 sets
  (m = 7, 9, 11) and their mirror images were canonicalized independently. All layer paths
  matched the predicted map (3,270 layers). Dropping the σ flip fails 23/30.
- **Controls with the case clauses** (`tools/controls.py`, `logs/controls.jsonl`): for each
  (m, k) in m = 2..9, k = 5..7, the no-case CNF and every case CNF were run in both encodings.
  Same answer in every case. m = 3, k = 5 and m = 6, k = 6 are UNSAT for every case, and the
  proofs are accepted by both checkers (k = 5, 6 have only the H3 case). m = 8 and m = 9 with
  k = 7: every case is SAT.
- **Per-case agreement of C3a and C3b, stronger than SAT/UNSAT** (`tools/projcount.py`,
  `logs/projcount.jsonl`): all models were enumerated, projected to (chi_S on all triples,
  σ). The model sets are identical for every case at m = 2 (k = 5, 6, 7) and m = 3
  (k = 5, 6, 7; up to 588 models), and for m = 4, k = 7 without a case (180,712 models).

## Measurements at m = 11, k = 7

MEASUREMENTS_PLACEHOLDER

## Files

- `soundness.md`: the WLOG argument, the case cover, layers, mirror lemma, composition.
- `shard_plan.md`: the deterministic plan for N machines.
- `cases.jsonl`: per top case: CNF sha256, sizes, short-run result, and closure status.
- `manifest_depth2.tsv`: every node at depth ≤ 2 (11 + 1,630) with units and CNF sha256.
- `tools/`: `hullcase.py` (cases, layers, mirror), `gen_case.py`, `validate_hull.py`,
  `validate_mirror.py`, `mutation_hull.py`, `controls.py`, `projcount.py`, `probe.py`,
  `knuth_layers.py`, `knuth_pruned.py`, `knuth_adaptive.py`, `summarize_walks.py`,
  `close_node.py`, `close_tree.py`, `compose.py`, `manifest.py`.
- `logs/`: all raw records (short runs, probes, closures, validation).
