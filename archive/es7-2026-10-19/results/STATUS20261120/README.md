# STATUS20261120: sessions of 19–20 November 2026 (handoff, written 20 Nov ~12:00 KST, updated 23:58)

**Status: STOPPED, 20 Nov 23:52 KST.** The owner asked at 23:50 to stop every job and to commit and push by 00:10. All runs are resumable (§6, "Stopped 20 Nov 23:52"); nothing is running, both memory guards are stopped. **ES(8) ≤ 304** is the current bound
([ES304N20261119](../ES304N20261119/README.md)): computer-assisted, Lean-checked composition, unrefereed, not
committed, and with no independent re-check by another person or agent yet.
- The previous handoff, [STATUS20261118](../STATUS20261118/README.md), stays the reference for everything not changed
  here. Its line "Nothing runs" is out of date.
- Nothing was committed, pushed, published or e-mailed between 18 Nov and the owner's commit-and-push request of 20 Nov 23:50 (records and tools of 19–20 Nov). Nothing has been published or e-mailed.

## 1. Results since 18 November

| result | label | record |
|---|---|---|
| ES(8) ≤ 306, then ≤ 305 (Z-row, Lemma Z), then **≤ 304** (balanced budget 67 with the Z-row) | EXACT TREE (two implementations) + CERTIFIED N66 ≤ 55 + PROVED lemmas; last step in Lean | ES306N20261119, ES305N20261119, **ES304N20261119** |
| Z*-row: Z* = {f(0) = 5, f(4) ≥ 1}, 70 states, h(Z*) ≥ 70 − N66 | PROVED (Lemma B both halves); Lean `LemmaZStar.lean`; exact controls | ES305N20261119 §8, ES303N20261120 |
| weak Conj(8) of Δ: no counterexample with ≤ 16 points | CERTIFIED (19 Nov 16:59) | DELTA2N20261113/VERIFY_DELTA2N_RECERT1119.md |
| all 358 DELTA2N proofs regenerated bit-identical to the deleted 13 Nov proofs | CERTIFIED, REPRODUCED | same |
| weak Conj(7) at 16 points | undecided (8 h limit) | same |
| weak Conj(8) at 17 points | undecided (16 h limit, 20 Nov 14:28) | same |
| budget-36 residual slice (18,18) | EXACT TREE; the other three slices are out of reach (2e10–3e11 nodes) | ES306N20261119 |
| N66 level 15, first 14 cube leaves | CERTIFIED per cube; independent check 14/14 | N66N20261113/cubes20261120 |

## 2. What runs (20 Nov, 19:15)

| unit | job | ends |
|---|---|---|
| `esr-bal-zbs68` | balanced budget 68 with the Z*-row → **ES(8) ≤ 303** ([ES303N20261120](../ES303N20261120/README.md)); launched at 22 threads at 17:41, pinned by `taskset` to cores 5–15 (logical 5–15, 21–31); runtime CPUQuota since then 2000 % / 1800 % (temperature, Tctl 86 °C), 1600 % from 19:10 (FV took 2 threads), 1800 % from 21:50 (Tctl 82.9 °C average), 1600 % again from 23:49 (Tctl 86.7 °C average at 1800 %, 83.9 °C at 1600 %); 14 until 11:01, 10 until 14:37, 11 until 17:41; resumable | earlier than the 11-thread window (22 Nov 01:30, range 21 Nov 13:00 – 23 Nov 03:00, HEURISTIC); new figure after the speed measurement; RuntimeMaxSec 24 Nov 05:01 |
| `esr-n66-drv15` + `esr-n66-c15-*` | **N66 ≤ 54** level-15 cube campaign ([cubes20261120](../N66N20261113/cubes20261120/README.md)); 4 cube slots (the n66 memory track binds) | driver deadline 23 Nov 12:00 (restartable) |
| `esr-vfy-drv15` + `esr-vfy-*` | progressive independent check of the level-15 leaves ([VERIFY_N66CUBES15.md](../N66N20261113/cubes20261120/VERIFY_N66CUBES15.md)) | 23 Nov 13:10 |
| `esr-memguard-1120e` + `esv-memguard-1120d` | memory guards: research 21,000 MB total (tracks bal=9500, dlt=7000, n66=17000, others 3000) + formal verification 3,000 MB (fv=3000) = 24,000 MB | stop them when nothing runs |
| `esv-fv-drv` + `esv-fv-*` | **Lean check of the ES(8) ≤ 304 tree** with the in-house compact checker (FV304; plan, pilot and launch command in `~/research/data/fv304-20261120/PLAN.md`): 2 jobs, pinned to cores 5–15; budget 68 gave up 2 threads (CPUQuota 1600 %, runtime) | about 55–90 CPU-h (HEURISTIC); resumable |

- Threads (cap 28 of 32 since 20 Nov 17:30, owner "80–90 %"): at 21:50 budget 68 18 + FV 2 + 4 cubes × 0.98 + drivers ≈ 24.5 (top: 72 % busy). Memory, not threads, limits the campaign (n66 track 4 × 3,800 MB reserved).
  The CPU has 16 cores × 2 threads: budget 68 runs on cores 5–15 (both threads of each); the cubes, the verifier and
  the drivers use cores 0–4 (96 MB L3), one thread per core. The campaign driver was restarted at 17:41 with its
  thread gate from `C15_CPU_CAP_MILLI=27500` (budget 68's 22 threads + 5.5). Formal verification (`esv-*` units, the
  compact Lean checker on the 304 tree) is being ported; it starts with its own memory guard so that the two guards'
  totals stay at 24,000 MB. Speed check of this step: `data/smt-20261120/rates.jsonl`.
- `esr-dlt-n8m17` (Δ weak (5,8) at 17 points) ended 14:28: undecided at its 16 h limit; its thread went to budget 68.
- Campaign at 14:30: 29 leaves certified, 4 running, 56 queued; one real time-out so far (`oohhoh`, split on state
  40). Independent check round 3: 28 / 28 leaves pass all four checks, no discrepancy.

## 3. What follows from what

- b68 EXACT TREE (both checks in `b68zs/steps.log`) + N66 ≤ 55 + ResidualBound 118 → **ES(8) ≤ 303**
  (`composition_303_zzsf`, compiled).
- N66 ≤ 54 (cover complete **and** VERIFY_N66CUBES15 confirmed) → the Z- and Z*-rows at rhs 16. Then a budget-69 tree
  on `balzs_n54.rows` → **ES(8) ≤ 302** (`composition_302_n54`, compiled; dives about 8.0e7 nodes, HEURISTIC).
  - The run script `zrow/zbs54_run0.sh` refuses to start until the marker `zrow/N66_LE_54_VERIFIED` exists.
  - The residual side does not gain from N66 ≤ 54 alone: (19,17) and (20,16) remain at budget 36.
- N66 ≤ 53 (level 16) would be worth about one more point (budget 71 at rhs 17: 4.1e9 dive nodes; HEURISTIC).

## 4. Owner decisions

Made on 20 Nov:
- L15 campaign alongside b68, with b68 at 10 threads.
- Level-15 disk policy: partial files of timed-out cube runs are deleted; certified leaves keep `trim.lrat.zst` and
  `cert.cnf.zst`, and the originals are removed only after the hash check (`c15_post.sh`).
- memguard n66 track 17 GB, with the total at 24 GB.
- Main model Opus, advisor Fable; consult points in `.claude/skills/es-research/SKILL.md` §7.

Open:
- Deletions:
  - Δ partials `delta-recert-20261119/cert/a5_n7_m16_weak.partial.lrat.zst` (14.9 GB) and
    `a5_n8_m17_weak.partial.lrat.zst` (13.7 GB, since 20 Nov 14:28); neither is a proof;
  - the old Z-row-only b68 finder directory `zrow/b68z` (about 12 GB);
  - (decided 20 Nov ~12:25: the L15 pilot partial `p2/b15q/it3/cert.lrat`, 13.7 GB, was deleted with the owner's OK; its 0.68 GB `cert.cnf` is kept.)
- Commit and push of the records since 18 Nov. Untracked: ES303–ES306, STATUS20261120, VERIFY_DELTA2N_RECERT1119,
  cubes20261120, LO33 tools.
- E-mails, public wording, and an independent re-check of 305/304/303 by another person or agent.
- Formal verification plan for the three computational inputs (literature check 20 Nov): [FORMAL_OPTIONS.md](FORMAL_OPTIONS.md).

## 5. Lessons (20 Nov)

- The first b68 finish estimate was wrong by 2–3×. Per-context cost rises along the context order within each class.
  Holdout-test a projection before quoting it.
- Check the memguard track budget before launching on a track: the L15 pilot was stopped at the 3,000 MB default.
- The first start of the L15 driver crashed because its output folder did not exist (fixed: makedirs).
- The verifier copy kept the level-14 F_c hash constant in `summarize.py`. The advisor's pre-launch review caught it.

- **OOM kill at 18:21 (my error).** The first formal-verification helper (`esv-fv-ctx`, MemoryMax 1G) was started
  before any memory guard covered `esv-*` units, and a full JSON parse of the large tree files reached the limit: the
  kernel OOM-killed it (the owner's GNOME alarm). Fix: `esv-memguard-1120` (total 3,000 MB) now runs, the research
  guard was restarted as `esr-memguard-1120c` with total 21,000 MB (sum 24,000), and the helper parses headers only.
  Rule: start the guard for a prefix before the first unit of that prefix.

## 6. Resume

### Stopped 20 Nov 23:52 (owner: stop everything and commit by 00:10)

State at the stop (all jobs stopped with `systemctl --user stop`; drivers first, then the job units, then the guards):
- **b68** (ES(8) ≤ 303): 24,938 of 32,755 contexts closed (76 %), `b68zs/occ.out` ends with a complete line; no
  check has run yet. Last runtime CPUQuota 1600 % (Tctl 83.9 °C average; 86.7 °C at 1800 %).
- **L15 campaign** (N66 ≤ 54): 51 leaves certified, 29 split, 42 queued. The 4 cubes running at the stop
  (`ohohoo`, `ohhooo`, `hoooho`, `oohhoo_40h`) were set back to `queued` in `p2/c15/campaign_status.json` (copy before
  the edit: `campaign_status.before-sunset-20261121.json`); their partial run files were renamed
  `p2/c15/<id>*.stopped-20261121` (nothing certified there; delete with the owner's OK). Driver deadline 23 Nov 12:00
  (`C15_DEADLINE_DAY/HM`); move it if the stop lasts long.
- **FV304** (Lean check of the 304 tree): export complete (8,192 contexts); 379 chunk modules compiled, all lean_rc 0
  with the standard axioms; the two compiles running at the stop left no olean (written only on rc 0). Rerun the
  driver command below; it skips finished modules.
- **Verifier** (`vfy15`): stopped idle between rounds; rerun the command below.

Restart order: the two memory guards first (sum 24,000 MB), then b68, the campaign driver, the verifier, FV.

```bash
# memory guards (start before any unit of their prefix)
systemd-run --user --unit=esr-memguard-1121 -p CPUQuota=30% -p MemoryMax=200M -p MemorySwapMax=0 --nice=5 \
  -E LOG=/home/jay/research/data/memguard-20261119.log \
  /home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/memguard.sh esr 21000 bal=9500 dlt=7000 n66=17000
systemd-run --user --unit=esv-memguard-1121 -p CPUQuota=20% -p MemoryMax=200M -p MemorySwapMax=0 --nice=5 \
  -E LOG=/home/jay/research/data/memguard-20261119.log \
  /home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/memguard.sh esv 3000 fv=3000
# FV304 driver (resumable; STOP file in the work dir stops new steps)
systemd-run --user --unit=esv-fv-drv -p CPUQuota=20% -p MemoryMax=300M -p MemorySwapMax=0 -p RuntimeMaxSec=432000 \
  --nice=10 --working-directory=/home/jay/research/data/fv304-20261120 -E FV_JOBS=2 -E FV_MEM=2800 -E FV_TMAX=90 \
  taskset -c 5-15,21-31 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u \
  /home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05/drive_es304z.py
```
(b68 at 16 threads: use `CPUQuota=1600%` in the b68 line below. The commands below are the earlier ones.)

```bash
# b68 (resumes from closed contexts; runs both checks at the end)
cd /home/jay/research/data/bal186-20261119/zrow
systemd-run --user --unit=esr-bal-zbs68 -p CPUQuota=2200% -p MemoryMax=8G -p MemoryHigh=7G -p MemorySwapMax=0 \
  -p RuntimeMaxSec=300000 --nice=10 --working-directory=$PWD taskset -c 5-15,21-31 ./zbs_run0.sh 68 22 16384
# L15 campaign driver (state in W/p2/c15/campaign_status.json)
cd /home/jay/research/data/n66-20261113
systemd-run --user --unit=esr-n66-drv15 -p CPUQuota=6% -p MemoryMax=300M -p MemorySwapMax=0 --nice=10 \
  --working-directory=$PWD -E C15_DEADLINE_DAY=23 -E C15_DEADLINE_HM=12:00 -E C15_SLOTS=5 -E C15_RES_MB=3800 \
  -E C15_CPU_CAP_MILLI=27500 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u p2c15_driver.py
# verifier
systemd-run --user --unit=esr-vfy-drv15 -p CPUQuota=5% -p MemoryMax=200M -p MemorySwapMax=0 --nice=10 \
  --working-directory=/home/jay/research/data/n66-20261113/vfy15 /bin/bash /home/jay/research/data/n66-20261113/vfy15/bin/driver15.sh
# memory guard
systemd-run --user --unit=esr-memguard-1120b -p CPUQuota=30% -p MemoryMax=200M -p MemorySwapMax=0 --nice=5 \
  -E LOG=/home/jay/research/data/memguard-20261119.log \
  /home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/memguard.sh esr 21000 bal=9500 dlt=7000 n66=17000
# (unit name esr-memguard-1120c since 18:22) and the formal-verification guard (start it before any esv-* unit):
systemd-run --user --unit=esv-memguard-1120 -p CPUQuota=20% -p MemoryMax=200M -p MemorySwapMax=0 --nice=5 \
  -E LOG=/home/jay/research/data/memguard-20261119.log \
  /home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/memguard.sh esv 3000
```
