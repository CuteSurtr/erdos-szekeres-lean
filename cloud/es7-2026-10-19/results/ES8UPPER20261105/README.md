# ES8UPPER20261105: towards ES(8) <= 310 (balanced budget 64)

Started 5 November 2026. **No bound below 311 is claimed.** `MEMO.md` is the scoping memo: a read-only workflow of
5 readers, 3 proposals and a judge.

## The route

The omission bound is T = 406 − b_B − b_R, with b_B and b_R the largest excluded hole budgets over the balanced and
residual catalogs. Currently (b_B, b_R) = (63, 32), so T = 311.
- **The residual side is tight.** Over the present 2,650 rows, assignments with 33 holes exist, so b_R = 32 cannot
  improve without new rows.
- **The balanced side is open.** Excluding every balanced assignment with at most 64 holes, over the present 3,131
  rows, gives (64, 32) and **ES(8) <= 310**. This needs no new mathematics, only a branch-and-bound certificate and
  its Lean check.

## Exact result of 5 November: a 71-hole balanced vector

The CP-SAT hunt (`tools/witness_hunt.py`, minimising from the known 72-hole vector) found a 0/1 hole vector with
**71 holes** that satisfies all 3,131 balanced constraints. It is the second line of `pilot/witness_solutions.jsonl`.
- The coordinator re-checked it directly against
  `experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json` (SHA-256 `acaf6323…`): 71 distinct
  states and 0 of 3,131 constraints violated.
- **Consequence.** The balanced optimum h_B^min lies in [64, 71], down from [64, 72]. The present catalogs can
  therefore never prove better than **ES(8) <= 304** (= 375 − 71). That is a statement about this proof method, not
  about ES(8).

## Pilot (5 November, 16:02–17:23 KST; evidence for the cost estimate)

- **Setup.**
  - 4,096 depth-12 contexts were extracted from the budget-63 tree of the 311 record
    (`tools/extract_contexts.py`). Their subtree sizes sum to the recorded 782,437 leaves.
  - 28 contexts were stratified by size (`tools/select_pilot.py`), and the 4 lowest-LP contexts were added.
  - The driver `tools/run_context.py` imports `pbb_strong.Solver.expand` unchanged, with the production rule, and
    replays every subtree exactly. It reproduced the recorded budget-63 subtrees exactly on 4 of 5 checked contexts;
    on the fifth, a different HiGHS optimum gave a different tree.
- **Result** (`pilot/pilot_ratios.tsv`).
  - All 32 budget-64 contexts closed, including the largest (883 budget-63 leaves).
  - Node ratio against the recorded budget-63 subtree: **pooled 9.34**, range 7.4–10.6.
  - Paired against this machine's own budget-63 runs: 8.1–9.6.
  - The memo's gate ("ratio <= about 10: launch") is passed.
  - No context produced a witness, and the budget-64 CP-SAT hunt has found none.
- **Projection.** About 1.46e7 nodes and about 1,500 CPU-h at about 0.38 s per node, so 2–3 days on 28 workers.

## Full budget-64 search (launched 17:24 KST, 5 November)

- `tools/campaign.py` runs as the systemd user unit `es8-b64-campaign`, with 28 workers. Its cutoff is
  2026-11-09 17:00 KST (editable in `campaign/cutoff` in the work directory).
- **Order.** The 64 lowest-LP contexts first, then the rest by decreasing size.
- **Restart-safe.** A context with a closed result file is never rerun.
- **Health.** The youngest worker is paused on heat or memory pressure.
- **Witness.** On a witness, no new jobs start and an alert is raised.
- **After it finishes:**
  - if every context closes, assemble the full tree (master levels plus subtrees) and replay it exactly;
  - check it in Lean with the compact checker (`experiments/omission-compact-checker-2026-11-05`, once gate G2
    passes);
  - write `Bridge64` / `Final310` following Bridge63 / Final311, and audit the axioms.

  Only then can ES(8) <= 310 be claimed.
- A witness, if one turns up, would be exact evidence that the present catalogs cannot reach 310. The route would
  then switch to new rows (`MEMO.md` routes 2 and 5).
