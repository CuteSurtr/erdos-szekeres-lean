# CHAIN_REVIEW: adversarial review of the written links of ES(8) ≤ 308 (15 November 2026, 02:52-03:40 KST)

**All five links CONFIRMED by both of their two independent reviewers (10/10). No gap, no refutation.** The chain stays
computer-assisted, not Lean-checked as a whole, and unrefereed. The Lean facts rest on the recorded kernel receipts, whose
source hashes the reviewers matched against the current files (Lean was not re-run tonight).

Ten reviewer agents of the workflow `es-overnight-extra` (run `wf_2deae7c5-405`); reviewer 1 of each link worked from the
written argument down, reviewer 2 from the Lean/CNF artefacts up. Their full reports (verdict, details, the checks they ran,
files) are kept verbatim in `/home/jay/research/data/roadmap-20261115/agent_results_extra.jsonl` (labels `chain:*`); their
own scripts are in the session scratchpad (`rev1/f18_gluing.py`, `mytree.py`, `check_catalog_state0.py`, `catcheck.py`,
`myreplay.py`, `myreplay_b33.py`, `s20scan.py`, `lemmaA_control.py`, …). This file was written by the main session from those
reports because the workflow's own write-up step failed on the account's usage limit.

| Link | What was checked | Reviewer 1 | Reviewer 2 |
|---|---|---|---|
| population composition | \|S\| ≤ 1 + \|H\| + \|R\|, balanced 187 (`Compact310.balanced_population_187`), forcing threshold 187 + 119 + 2 = 308 via `Partition.forces_of_population_bounds`; the bridge uses the Lean statements exactly as written (reviewer 2 re-elaborated them) | confirmed | confirmed |
| residual catalog and state 0 | `all_rows_2650` for the hole vector of every actual nonempty R, h₀ = 0 (`zero_mem_residualOccupied`), \|R\| + h(C) = 154, budget-32 exclusion; slice rows 0-2649 identical to source-2650 (hash e800d5f8…); the only pending branch of each slice tree is state 0 missing (reviewer 1 re-replayed with own code) | confirmed | confirmed |
| capacity transfer (Lemma A) and N66 | F/Lo owners, h(Lo) ≥ 70 − N66 from the ambient no-6-cap/no-6-cup/no-octagon property, ambient-vs-subset subtlety, general position and distinct x; N66 ≤ 56 used with the same definition as VERIFY_N66_56 (own controls `lemmaA_control.py`) | confirmed | confirmed |
| h(F) ≥ 18, baseline and gluing | the nine rows 973, 1165, 1167, 1171, 1175, 1179, 1183, 1186, 2315 give 3h(F) ≥ 54 (recounted with own script); budget-33 baseline h(C) ≥ 34; the 34-hole cases are exactly (18,16), (19,15), (20,14), each excluded by its packet; no off-by-one, no uncovered case | confirmed | confirmed |
| coupled-row soundness | every coupled row is implied for every actual residual configuration by the written encoder-soundness argument (VERIFY309N link (c), re-derived against the Lean definitions); tonight's non-pool rows were built with the same pinned encoder and independently re-encoded; nothing in the encoder depends on slice, budget or witness | confirmed | confirmed |

**Trust boundary (inherited, as both reviewers of the relevant links list it):** the Lean build receipts; the written
encoder-soundness argument for the coupled rows (CERTIFIED for their stated CNFs, the CNF-to-geometry step is written);
N66 ≤ 56 (CERTIFIED components with written soundness, not Lean-checked); the budget-33 slice trees (EXACT TREE, VERIFY_LO).
