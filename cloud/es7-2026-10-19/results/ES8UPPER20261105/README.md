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
- **Throttle** (added 19:48 KST, 5 November, at the author's request).
  - `campaign/max_running` caps the number of running workers. Extra workers are SIGSTOPped in place, so no work is
    lost, and resumed when the cap rises.
  - All workers run at nice 19 with idle I/O priority.
  - Set to 8 while the machine is needed for other work. The witness hunts were stopped then, after the 71-hole
    result.
  - **Paused completely at about 19:50 KST, 5 November** (cap 0, at the author's request). About 82 contexts were
    closed by then, about 4.9% of the work by budget-63 leaves. Their result files are on disk and are never redone.
    - The in-flight contexts are frozen in RAM. A reboot would lose only their partial work; they would restart from
      scratch.
    - The supervisor itself only wakes every 30 s.
    - Resume with `echo 28 > campaign/max_running`, or any smaller number, in the work directory. Extend
      `campaign/cutoff` (2026-11-09 17:00) if needed.
  - **Resumed at about 22:35 KST, 5 November, at about 20% of the machine** (at the author's request).
    - The cap is 6 workers, of 32 hardware threads.
    - A hard cgroup ceiling also applies:
      `systemctl --user set-property --runtime es8-b64-campaign CPUQuota=640% IOWeight=10`.
    - At this rate the remaining work takes about 10 days, so the 9 November cutoff will stop it partway unless it is
      extended.
- **After it finishes:**
  - if every context closes, assemble the full tree (master levels plus subtrees) and replay it exactly;
  - check it in Lean with the compact checker (`experiments/omission-compact-checker-2026-11-05`, once gate G2
    passes);
    *(6 Nov 2026: on the 64-leaf chunk the fused checker `checkF2` met G2's speed, size, corruption and axiom-audit
    criteria. G2's linearity criterion (64 to 1,000 to 10,000 leaves) cannot be shown on that chunk; linearity was
    measured later, on ES(8) ≤ 311 data, from 584 to 19,012 leaves per module. Its pipeline has since re-checked
    ES(8) ≤ 311 end to end, a second complete Lean check of that bound, in about 10 CPU-hours; see that
    experiment's README. A budget-64 tree would still need its own export, bridge and final file.)*
  - write `Bridge64` / `Final310` following Bridge63 / Final311, and audit the axioms.

  Only then can ES(8) <= 310 be claimed.
- A witness, if one turns up, would be exact evidence that the present catalogs cannot reach 310. The route would
  then switch to new rows (`MEMO.md` routes 2 and 5).
