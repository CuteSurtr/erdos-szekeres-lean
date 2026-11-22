# N66 level 15 (N66 ≤ 54): cube-and-conquer campaign (20 November 2026)

**Status (22 Nov 2026, 16:45 KST): COMPLETE. N66 ≤ 54 is CERTIFIED** (every leaf; cake_lpr) plus the written model
soundness of the level-14 record with L = 15. It has the same standard as N66 ≤ 55. Unrefereed.
- The campaign ended 22 Nov 13:07: 105 certified leaves, 41 split nodes, nothing queued; leaf cover and certified
  cover ok.
- Independent checks are in §8.

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


## 8. Acceptance (22 Nov 2026, main session, after the advisor's blocking checks)

| check | result | evidence |
|---|---|---|
| driver | final, 105 certified, 41 split, 0 queued/running; `leaf_cover_ok` and `certified_cover_ok` true | `p2/c15/campaign_status.json` (sha256 `4802dc9a946cefa3b855b8c495becc0fb33491a89e5472c9722ccb9d0c8138f5`) |
| independent verifier vfy15 (U1-style, own code), all 105 leaves | fresh cake_lpr `s VERIFIED UNSAT` 105/105; trim ⊆ cert 105; cert = F_c + cube units (own generator `genchk2`, K = 15) 105; rows justified (own check) 105; discrepancies none | `vfy15/summary.json` (sha256 `87b82b7a0029496176bdffdeabb87d95bd7f03eba844e576f31b826084927181`), `data/vfy15_tally.json`, `data/vfy15_summary_table.md` |
| exact partition, own code, on the campaign's cube literals | 105 leaves pairwise disjoint, total measure exactly 1; 64 roots; every one of the 41 split nodes has exactly its two children | `data/own_cover_check_20261122.txt` |
| exact partition on the REAL unit literals of the certified CNFs (vfy15 `units` read from each cert.cnf) | 0 overlapping pairs, total measure exactly 1; unit counts = cube literal counts | `data/acceptance_checks_20261122.txt` |
| join | status ids = vfy15 ids (105 = 105); trim.cnf/trim.lrat sha256 equal for every leaf; every leaf passes every vfy15 check | same |
| level | L = 15 throughout: driver `LEVEL = 15`; F_c built by `vfy15/bin/mkfc15.py` (asserts L = 15); vfy15 generator run with K = 15 (sequential counter "at most 15 holes") | F_c = `vfy15/fc/cert.cnf`, 684,497,868 bytes, sha256 `2f78368f5e00ba52dc04104bbfb66289212d3dbf05d1aa3e0c798a814c4fee29` |

**Statement.** N66 ≤ 54: every set of points in general position (distinct x) with no 6-cap, no 6-cup and no convex
octagon has at most 54 points.
- Label: CERTIFIED (all 105 leaves of an exact cover) + PROVED (the written soundness of the relaxation: level-14
  README §2 and §6, unchanged except L = 15).
- Not Lean-checked. The Lean encoder of `formalize-20261122/n66enc` covers level 14 (N66 ≤ 55) modulo its cube
  verdicts and RowsValid.

**Consequence.** `composition_302_n54 : ExcludesHoleBudgetZZsN 16 69 → N66Bound 54 → ResidualBound 118 →
ForcesConvexNGon 302 8` (ES303N20261120, Lean, standard axioms) now needs only the budget-69 tree with both extra rows
at rhs 16. That run starts after this record; see ES303N20261120 §7.
