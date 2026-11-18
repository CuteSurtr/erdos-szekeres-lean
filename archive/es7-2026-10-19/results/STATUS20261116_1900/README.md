# STATUS20261116_1900: short evening session, 16 November 2026 (18:19-18:51 KST)

**Status: STOPPED at the owner's request at 18:51 KST. Nothing runs.**
- The previous handoff, [STATUS20261115_2300](../STATUS20261115_2300/README.md), stays the reference for everything not
  changed here.
- **Nothing was committed, pushed, published, e-mailed or deleted.** The owner decisions listed there are still open.

The owner's messages:
- 18:07: "let's continue our research, please research as farthest as possible";
- then: "deploy many agents if necessary just like the last time";
- about 18:50: "can we save everything and stop? i need to study something".

The session was planned to run until 09:30 on 17 Nov and was stopped after 32 minutes. The results below are what
finished in that time. The agents' records are partial: each stops where its agent was stopped.

## What ran

| unit / workflow | job | ended |
|---|---|---|
| `esr-memguard-1116` | memory guard, 24,000 MB total (log `/home/jay/research/data/memguard-20261116.log`); one clean stop: `esr-ags-replaymem` at 18:29 (1,384 of 1,400 MB), no OOM kill | stopped 18:51 |
| `esr-n66-driver-r6` + 5 `esr-n66-cube-*` | N66 ≤ 55 cubes; `W/p2c14_driver_r6.py` = r5's rules with a new deadline and a 120 GB free-disk floor | stopped 18:51 |
| `esr-n66-zpart` | `W/n66_zpart_r6.py`, zstd of partial LRATs of cubes timing out after 18:30 | stopped 18:51 (nothing to do: no timeout) |
| `esr-lo-b35s20v11b` | (20,15) loop, `continue34_v11.py --start-version=148` | stopped 18:51 in finder slice c148s2 |
| workflow `wf_f37440ce-6fa` (wave A) | 8 agents: D, T, L, AN, AS (then R), VB, VS | stopped 18:50; R never ran |
| workflow `wf_97104ab7-3ce` (wave A2) | 5 agents: T2, T3, C (critic CN), P307, LIT | stopped 18:50 |

W = `/home/jay/research/data/n66-20261113`. At 18:51 every `esr-*` unit was stopped, and no research process was left
(checked with `ps`).

## Results

### N66 ≤ 55 (still not decided)

- **5 more cubes CERTIFIED**, each at the first attempt in 1,222-1,760 s, with the unchanged acceptance rules:
  - `oohhoo_23o_40o_52h`, `ohohoo_23o_40o_52h`, `ooohoo_40h_52o_46h`, `oooooo_40h_52o_46h` and `ooooho_40o_52o_46h`.
  - Now 110 of 132 leaves are certified, **482/512 = 94.1 % by measure** (93.2 % before). 22 leaves are queued.
  - No cube was SAT.
- **The 5 cubes running at the stop** had run 2-11 min, with no verdict. They were re-queued in `campaign_status.json`
  (backup `campaign_status.json.bak-20261116-1851`). Each cube's `requeued` field says what happened.
  - A re-run starts again at `it1` and rewrites `<id>.out`, so the stopped runs' files were moved aside, not deleted:
    `<id>/stopped1116-it1/` and `<id>.out.stopped1116`.
- No cube timed out, so `esr-n66-zpart` compressed nothing; its log `p2/c14/zpart_r6.jsonl` has only its start line.
- [STATUS_campaign.md](../N66N20261113/cubes20261115/STATUS_campaign.md) was regenerated (final). Its printed re-split
  order is now the one the driver uses (critic issue 6).
- **Independent check (VB, [VERIFY_N66CUBES_1116.md](../N66N20261113/cubes20261115/VERIFY_N66CUBES_1116.md)):**
  - 6 of 6 cubes taken pass U1's four checks;
  - the rest, including tonight's 5, are not yet checked.

### (20,15)

- The loop ran only its first finder slice and was stopped inside it, which is a safe point. Its events end with
  `FINISHED`, `stopped: True`, version 148.
- Closed-context files went from 1,505 to **1,652** of 8,065.
- No round was appended, so there is no batch to audit.

### Lower bounds (track L, [LOWERBOUND_RUN_1116.md](../ROADMAP20261115/LOWERBOUND_RUN_1116.md), partial)

| claim | statement | label | verdict |
|---|---|---|---|
| `lb-ln-ddsz28-real` | **Geometric 7-gon saturation is not an order-type invariant.** The 28-point DDSZ-type set S is geometrically saturated (claim `lb-e1-ddsz28`). Another realization S′ (integer points, same labelled order type, same x-order) plus the point p = (604, 510) is in general position and has no convex 7-gon. | EXACT (integer certificate) | VB CONFIRMED 18:37 ([VERIFY](../ROADMAP20261115/VERIFY_LOWERBOUND_LN_DDSZ28_REAL.md)) |
| `lb-ln-ddsz-block` | The cup-cap saturation of DDSZ's 8-point block depends on its coordinates, not on its signotope; this explains the claim above | EXACT / CERTIFIED parts | VB CONFIRMED 18:49 ([VERIFY](../ROADMAP20261115/VERIFY_LOWERBOUND_LN_DDSZ_BLOCK.md)) |
| `lb-ln-ddsz28-all34` | All abstract one-point extensions of that 28-point order type are realizable (44 integer certificates) | CERTIFIED + EXACT, as claimed | **not yet verified** |

- So yesterday's "abstract extension exists" (E4) is realized geometrically.
- The literature check found DDSZ silent on order types and other realizations
  ([LOWERBOUND_EV_CHECK.md](../NOVELTY20261115/LOWERBOUND_EV_CHECK.md), E4). The first claim was not found there; it
  is not checked for novelty beyond that record.

### Other finished pieces

- **Route to 307** ([ROUTE307_1116.md](../ROADMAP20261115/ROUTE307_1116.md), first version).
  - Claim `p307-chain`: a written conditional chain from the ES(8) ≤ 308 inputs to ES(8) ≤ 307. No new computation.
    VS CONFIRMED 18:42 ([VERIFY_P307_CHAIN.md](../ROADMAP20261115/VERIFY_P307_CHAIN.md)).
  - What still has to happen for 307: (20,15) closed, including the high-cap pass, and N66 ≤ 55.
- **Literature watch** ([WATCH_1116.md](../NOVELTY20261115/WATCH_1116.md), complete): nothing found since the 16 Nov 03:10
  check changes a verdict.
- **Critic CN** (`/home/jay/research/data/roadmap-20261115/pm1115/cn/ISSUES_1116.md`, 8 issues, first pass).
  - Fixed tonight by the main session, as annotated edits:
    - issues 0, 3 and 4: wording in [STATUS20261115_2300](../STATUS20261115_2300/README.md) — TWO-ENV#(7) is also
      unrefuted; who checked the three LP0(7) sets; what the DDSZ calibration shows;
    - issue 6: the N66 status page.
  - Open:
    - issue 1: LP0_7_REAL_SEARCH.md says "at least 20 points", but 18 points were not covered. CN filed
      `cn-lp0-ext1-5blocks`, 85 certified CNFs for the 18-point case, not yet verified.
    - issue 2: THEORY_1115PM.md and the folder index are stale.
    - issue 5: VERIFY_RERUNS_1115EV.md says "two parties" for `v1_base_m16`, which is false.
    - issue 7: a note for track D.

### Started, not finished (records partial)

- **D:** LR(7) at 16 by certified cubes ([PROBES_1116.md](../DELTA3N20261113/attack20261115/PROBES_1116.md)). Nothing
  certified yet; work directory `pm1115/dn/` (2.0 GB).
- **T:** Δ lemmas. No record yet; work directory `pm1115/tn/`.
- **T2 and T3:** [THEORY_1116_SIZE.md](../DELTA3N20261113/attack20261115/THEORY_1116_SIZE.md) and
  [THEORY_1116_N6.md](../DELTA3N20261113/attack20261115/THEORY_1116_N6.md). Nothing proved yet; work directories
  `pm1115/t2size/` and `pm1115/t3n6/` (UNSAT-core tools).
- **AN:** N66 cost curves. No record yet; work directory `pm1115/agn1116/`.
- **AS:** the (20,15) high-cap pass and v12.
  - [V12_NOTES.md](../LO33N20261113/budget34/tools/V12_NOTES.md) is a draft. The new tools `run_tree_v7.py`,
    `continue34_v12.py` and `highcap_v1.py` were tested only in separate folders `runs/b35s20/bb-v12test-hc*`.
  - **Not reviewed (R never ran): do not use them before a review.**
  - Its claim `as-replay-mem-1116` is not yet verified.
- **Claims waiting for a verifier:** `as-replay-mem-1116`, `cn-lp0-ext1-5blocks` and `lb-ln-ddsz28-all34`.

## Saved

- **Session scratchpad**, copied in full to `/home/jay/research/data/roadmap-20261115/scratchpad-snapshot-20261116b/`
  (8,593 files, 1.6 GB).
  - Checked file by file against `scratchpad-snapshot-20261116b.MANIFEST.cksum`.
  - Task logs: `tasks-snapshot-20261116b/`.
- **Agents' work directories:** `/home/jay/research/data/roadmap-20261115/pm1115/{dn,tn,t2size,t3n6,ln,agn1116,ags1116,cn,p307,vb1116,vs1116}`.
- **Claims and verdicts:** `pm1115/claims/`.
- **Workflow journals:** `~/.claude/projects/-home-jay-research-lean-erdos-szekeres-lean/1e71bc06-5c09-4f54-ae48-3fca76aaa352/subagents/workflows/{wf_f37440ce-6fa,wf_97104ab7-3ce}/`.
- **Disk:** about 523 GB free at 18:50.

## Resume, in order of value

1. **N66:** copy `W/p2c14_driver_r6.py` and change only `DEADLINE` (`at(hm, day)` now takes the day of November).
   - Start a memory guard first; the driver will not start cubes without one.
   - The 22 queued leaves then run under r5's rules.
   - If a long run is planned, decide the partial-file question of STATUS20261115_2300 first. Otherwise start
     `n66_zpart_r6.py` with a new `SINCE`.
2. **(20,15):** `continue34_v11.py --start-version=148`, no receipt, with the v11 options of STATUS20261115_2300.
3. **Verification:**
   - the three claims waiting for a verifier;
   - U1's four checks on the cubes VB has not taken, which include tonight's 5.
4. **Review of AS's v12** (V12_NOTES.md) before any use; then the high-cap pass.
5. **Critic issues** 1, 2, 5 and 7.
6. **Unfinished tracks** (D, T, T2, T3, AN, L's E7-2): restart from their records and work directories.
