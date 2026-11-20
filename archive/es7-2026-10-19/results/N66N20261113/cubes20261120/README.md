# N66 level 15 (N66 ≤ 54): cube-and-conquer campaign (20 November 2026)

**Status: RUNNING. N66 ≤ 54 is NOT decided. N66 ≤ 55 (level-14 cube campaign, `../cubes20261115/`, CERTIFIED) remains
the bound.** The live status table is `STATUS_campaign.md` in this folder, written by the driver.

Labels: **CERTIFIED** = CaDiCaL 2.1.3 LRAT accepted by cake_lpr (`s VERIFIED UNSAT`, grepped) for the stated CNF, with
row justification and p2_verify (all inside `p2_cert.sh`); **COMPUTED** = solver verdict only; **HEURISTIC** =
timings and estimates.

## 1. Statement and soundness

- Same relaxation, split and acceptance rules as level 14 (`../cubes20261115/README.md` §1–§2 and §6), with L = 15.
  UNSAT at level L means every set of the class has at least L + 1 holes, so N66 ≤ 69 − L = 54.
- Split states 25 12 16 29 17 37 (64 cubes), re-split order as in level-14 driver r7 (A1 order). A cube whose
  CaDiCaL run reaches its time limit is replaced by its two children; the leaves always cover the 2^6 split, and
  the driver checks the cover exactly (`covered()`) over the cube literals read from each `verify.json`.
- N66 ≤ 54 follows only when every leaf has an accepted certificate, and it needs an independent check before it is
  stated.

## 2. What changed from level 14

| item | level 14 (r7) | level 15 (`W/p2c15_driver.py`) |
|---|---|---|
| L | 14 | 15 |
| warm quadruples | `p2/s14/...` (660,810) | `p2/s15/q.json` (676,907; 683,670 after τ) |
| CaDiCaL limit per cube | 1,200 / 2,400 s by band | 3,600 / 7,200 s by band |
| MemoryMax per cube | 4.1G / 5G | 6500M (memguard stops at 95 %) |
| reservation per running cube | 3,300 MB | 3,800 MB |
| units | `esr-n66-cube-<id>` | `esr-n66-c15-<id>`, driver `esr-n66-drv15` |
| partial files of timed-out runs | kept | **deleted** (owner OK, 20 Nov ~11:00) |
| certified leaf | trim.lrat → trim.lrat.zst | `c15_post.sh`: trim.lrat and cert.cnf → zstd, originals removed only after the decompressed SHA-256 matches cert.json (owner OK) |

- Calibration leaves `hhhhhh` and `hohhhh` (W/cal15.sh, same options and warm file) are adopted only through the
  same `accept()` rules.

## 3. Calibration (HEURISTIC timing; both leaves CERTIFIED for their cube)

| cube | L14 CaDiCaL s | L15 CaDiCaL s | ratio | L15 conflicts | L15 trimmed LRAT |
|---|---|---|---|---|---|
| hhhhhh | 124.1 | 289.6 | 2.3 | 487,146 | 188.0 MB |
| hohhhh | 238.9 | 537.7 | 2.25 | 1,358,563 | 506.1 MB |

- Both were UNSAT at the first solve with the warm set (no CEGAR iteration).
- Level 14 cost 43.7 process-h and 60.3 slot-h over 200 cubes (68 split, 132 leaves). At 2.2–4.5× that is roughly
  100–200 process-h and 140–270 slot-h.

## 4. Allocation (owner approved 20 Nov ~11:00 KST: run alongside budget 68)

- Budget 68 (`ES303N20261120`) restarted at 10 threads at 11:01 (resumed: 7,257 contexts kept, 25,498 to do).
- Memory guard restarted as `esr-memguard-1120b`: total 24,000 MB, n66 track 17,000 MB (was 6,000).
- Cube slots: up to 5, gated by free threads under the 16-thread cap and by memory room. While the Δ unit runs,
  about 4 slots fit.
- Driver deadline: 23 Nov 12:00 KST (restartable; the state is kept in `W/p2/c15/campaign_status.json`).

## 5. Files

- Work directory W = `/home/jay/research/data/n66-20261113/`: `p2c15_driver.py`, `c15_post.sh`, `cal15.sh`,
  `p2/c15/` (cubes), `p2/cal15/` (calibration leaves). Copies of the scripts are in
  `ES303N20261120/tools/`.

## 6. Resume

```bash
cd /home/jay/research/data/n66-20261113
systemd-run --user --unit=esr-n66-drv15 -p CPUQuota=6% -p MemoryMax=300M -p MemorySwapMax=0 --nice=10 \
  --working-directory=$PWD -E C15_DEADLINE_DAY=23 -E C15_DEADLINE_HM=12:00 -E C15_SLOTS=5 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u p2c15_driver.py
```

## 7. Independent check (progressive)

`VERIFY_N66CUBES15.md` (status NOT CONFIRMED until the campaign is complete). U1/VB's four checks and the exact cover,
re-run with L = 15 and the level-15 F_c (`vfy15/fc/cert.cnf`, `2f78368f…`), by unit `esr-vfy-drv15` (child units
`esr-vfy-<step>`, 65 % CPU, one at a time) while the campaign runs. Smoke test on the first 14 leaves: 14/14 pass all
four checks; negative controls (level-14 F_c; genchk2 at L = 14) fail as they must.
