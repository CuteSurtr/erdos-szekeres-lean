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
  - **6–7 November.** The cutoff was extended to 2026-11-16 17:00 KST.
    - Stopped at 00:06 KST, 7 November, at the author's request: 933 of 4,096 contexts closed (43.2% of the work).
    - Resumed at 03:31 KST with 30 workers, alongside the hourly ES(8) ≤ 310 Lean loop (`es310-incr`, 2 jobs).
    - **Stopped again at 18:26 KST, 7 November, at the author's request.** The screen had started to blink with
      all 32 threads busy, so the cap was first lowered to 26 and then the run was stopped.
      - **1,982 of 4,096 contexts closed** (71.8% of the work by budget-63 leaves; 10,214,522 budget-64 nodes, 9.11
        times the budget-63 record over the closed contexts).
      - No witness and no worker errors.
      - The 310 loop had compiled 1,074 chunks, none failed. 670 queued chunks were not started; the loop picks
        them up when it is restarted.
    - Nothing was deleted. The roughly 30 contexts in flight restart from scratch on resume, since each took under
      25 minutes. The steps to resume are in `campaign/SHUTDOWN-20261107.txt` in the work directory.
    - Choose the worker cap with the author before resuming. Full load (30 workers plus 2 Lean jobs) made the
      display blink.
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

## Mac share of the budget-64 search (started 21:39 KST, 7 November)

The Linux campaign is stopped (see above). The Mac continues it, at the author's request ("you can fully utilize
this mac"). **No bound below 311 is claimed**, and this section changes none of the claims above.

- **Same inputs.** The Mac's work directory is `<mac-b64-dir>`, outside git. Each input was regenerated there and
  matches the Linux record:
  - `contexts.jsonl`: regenerated with `tools/extract_contexts.py` from the tree parts (concatenated SHA-256
    `e5380cc6…`). Its SHA-256 `c16cc3da…` is the `contexts_sha256` of the es310 coverage record.
  - LP screen: `tools/lp_screen.py` gives the same minimum, median and maximum as
    `pilot/lp_screen.jsonl.summary.json`, and the same 20 lowest contexts in the same order. So the campaign order
    is reproduced exactly.
  - `pbb_strong.py`: `2aa90df2…`; the catalog: `acaf6323…`. HiGHS: `highspy` 1.15.1, the version Linux recorded.
    Also Python 3.14.10 and numpy 2.5.4.
  - **The driver is byte-identical to the one Linux ran** (`1937e9dc…`, the hash in the es310 coverage record).
    The committed `tools/run_context.py` differs only in its default repository path, written as a placeholder when
    it was committed. The Mac copy restores that default and points `ES_REPO` at a checkout of `e49379023`.
- **Check across platforms.** Two pilot contexts, run again on the Mac, both closed with exact replay:
  - ctx 840 gave 593 nodes against Linux's 611;
  - ctx 122 gave 1,211 against 1,209.

  The trees differ because HiGHS can return a different optimum of a degenerate LP on another platform, as the
  `run_context.py` docstring anticipates. Each tree is replayed exactly on its own, so this is not a soundness
  issue.
- **Scope.** Positions 2,040 to 4,096 of the campaign order, smallest first.
  - It skips the 10 pilot contexts in that range that the Linux campaign had closed, according to its export log
    (`experiments/omission-compact-checker-2026-11-05/logs/es310/export-full.err`, 1,744 contexts).
  - That leaves 2,047 contexts: an estimated 3.8 million budget-64 nodes, from 416,621 budget-63 record nodes at
    the pilot ratio.
  - Positions 1,733 to 2,039 are left out. The Linux campaign closed most of them after its last export, and its
    `runs/` directory says which; about 30 were in flight at the stop.
- **Driver.** `tools/mac_campaign.py` runs 15 workers at nice 10 under `caffeinate -i`, writes the Linux file layout
  (`runs/ctx-<k>-b64.result.json`, `.json.gz`), and stops starting jobs on a witness.
- **First measurement** (21:47 KST):
  - 45 contexts closed, all with exact replay ok;
  - ratio 8.64 against the budget-63 record (these are the smallest contexts);
  - 0.32 CPU-s per node with all 15 cores busy (0.21 with two busy).

  The projected wall time is about 22 hours.
- **To merge the two machines.**
  - Copy the Mac's `runs/ctx-*-b64.*` into the Linux work directory's `runs/` before resuming the Linux campaign.
    It never reruns a context with a closed result file.
  - Or copy the Linux results to the Mac, and lower `campaign/floor` to cover the gap.
  - The es310 coverage and export steps then see one `runs/` directory.

  *(10 Nov 2026: superseded. The Mac share finished on 8 November, 2,047 of 2,047 closed. The Mac result files
  record a Mac path for `pbb_strong.py`, which the frozen exporter and merge refuse on Linux, so a plain copy would
  stop the export. Import them with `ES8B64MAC20261110/tools/import_mac_runs.py`; see that record.)*

**10 November 2026: ES(8) ≤ 310 is Lean-checked** (compact checker, unrefereed). All 4,096 contexts are closed, 1,982 on Linux and 2,114 from the Mac (`ES8B64MAC20261110`). `assemble_final310.sh` reports VERIFIED in real mode with standard axioms only; see the section of 10 November 2026 in `experiments/omission-compact-checker-2026-11-05/README.md`.
