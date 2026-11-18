# STATUS20261115_0450: handoff after the 14-15 November night (written 04:50 KST)

Read first: [ROADMAP20261115](../ROADMAP20261115/README.md) (research program and recommended order), the headline of
[budget34](../LO33N20261113/budget34/README.md), [CHAIN_REVIEW](../LO33N20261113/budget34/VERIFY308/CHAIN_REVIEW.md),
[the Δ attack](../DELTA3N20261113/attack20261115/README.md), [NOVELTY20261115](../NOVELTY20261115/README.md) and the
15 Nov addendum of [SATOPEN20261113](../SATOPEN20261113/README.md).

## Results of the night (labels as in the records)

- **ES(8) ≤ 308** (computer-assisted, unrefereed, uncommitted): budget-34 slices 18, 19, 20 EXACT TREE + budget-33
  baseline, N5-free. Trees and all 1,020 coupled-row LRATs independently re-checked (VERIFY308); all five written links
  confirmed by two independent reviewers each (CHAIN_REVIEW); no competing result found (NOVELTY20261115).
- Budget 35: (18,17) and (19,16) EXACT TREE (fresh replay + independent C++ checker each); 314 new coupled rows CERTIFIED
  and batch-audited (35 for (19,16), 279+ for (20,15)). (20,15) and (21,14) open: HEURISTIC estimates 3.3e8 and 1.85e9
  nodes with all certified rows.
- N66 ≤ 55: undecided (two 3h10m monolithic solves; partial LRATs `n66-20261113/p2/b14h2|b14i2/it1/cert.lrat`, about
  29 GB each, kept: deleting them is the owner's decision).
- k = 9 ring "two displaced layers": exact list `SATOPEN20261113/tools/k9/ring_cases.py` (95 linear, 175 cyclic); 79+
  cyclic cases CERTIFIED by 03:27, no model.
- Δ conjecture: still open; two lemmas and five obstructions (most of them not independently verified because of the
  usage limit).

## Jobs still running at 04:50 (all with deadlines; they stop by themselves)

| unit | job | ends |
|---|---|---|
| `esr-lo-b35s20h` | (20,15) finder + loop v8 (12 threads), from version 132, `continuation-b35s20h` | 05:50 |
| `esr-k9-sched2` | k = 9 ring scheduler (2 jobs) | soft 05:35, hard 05:45 |
| `esr-memguard4` | memory guard (24 GB; tracks lo, vfy, n66, k9, agx) | about 06:27 |

After they stop: audit the (20,15) batches after v128u with `audit/audit_followup_rows_v4.py` **one process per batch**;
run `verify_cycx.py` on the k9 cases certified after 02:12 (`k9/verify_cycx_20261115a.txt` covers the first 30); then
update the budget34 and SATOPEN records.

## Notes for the next session

- The account's weekly usage limit (resets 18 Nov 11:00 KST) stopped all agents at about 03:50; workflow outputs are in
  `/home/jay/research/data/roadmap-20261115/agent_results_*.jsonl`.
- Agent scratch scripts and certificates from the Δ attack live in the session scratchpad, which is not durable; copy what
  is needed into the records before relying on it.
- Owner preferences voiced tonight: compiled code (C/C++) for heavy computation; more agents when useful; work to 06:00.
- Nothing was committed or pushed after the 21:01 snapshot push of 14 Nov; the repository cleanup is still paused at the
  question of who the cleaned repository is for.

## Update 05:55 KST (the owner reset the usage limit and extended the session to 10:00)

- Workflows finished since 04:50: roadmap synthesis (`ROADMAP20261115/SYNTHESIS.md`, reconciled in README §6), Δ verification
  (`DELTA3N20261113/attack20261115/VERIFICATION.md`), round 2 (`ROUND2.md`: CONJ-TS′(7) CERTIFIED for |S| ≤ 14; S19′ an
  EXACT 19-point signotope counterexample; `budget34/BAEK973.md`: row-973 route blocked), round 3
  (`N66N20261113/cubes20261115/README.md`: 64-cube plan, cover checked; `ROADMAP20261115/ES7_FEASIBILITY.md`).
- Correction to the line "Trees ... independently re-checked (VERIFY308)": VERIFY308 covers the budget-34 and budget-35
  packets; the budget-33 baseline trees rest on their earlier replays (VERIFY_LO, check_tree).
- Running until about 09:45 (all with deadlines): k = 9 ring scheduler `esr-k9-sched4` (MAXJOBS 2, MEMB 9.2; 114/175 cyclic
  certified at 05:39); (20,15) loop `esr-lo-b35s20j` (4 threads, from b35s20-v133); round-4 workflow launching the N66 cube
  campaign (`esr-n66-*`) and a certified CONJ-TS′ test; round-5 workflow on the realizability of S19′; the v9 batch-loop
  build; the method sweep. Memory guard `esr-memguard5` until about 08:30 (to be extended); scratch area synced to
  `/home/jay/research/data/roadmap-20261115/scratchpad-snapshot-20261115/` every 30 minutes.
- **07:28 load incident:** the load reached 30 of 32 threads for about a minute. Cause: an agent ran `realize_sig.py`
  directly in the session's terminal scope (not in a capped unit), and its numerical library used about 19 cores. The main
  session stopped the process at 07:29 and capped the terminal scope at runtime (`systemctl --user set-property --runtime
  ptyxis-spawn-…scope CPUQuota=800%`; not persistent) so that agent-side scripts cannot take the machine again; the research
  units (`esr-*`) are unaffected. No memory or OOM event (memory guard total about 11-15 GB).
