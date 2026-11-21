# STATUS20261121: Mac session of 21 November 2026, 12:00–15:00 KST (handoff)

**Status: all Mac jobs finished or stopped by 14:49 KST (solvers stopped 14:42; Lean rebuild done 14:48); nothing runs on Linux.** ES(8) ≤ 304 (ES304N20261119) is unchanged; nothing in this session changes a bound.
The Linux machine was not reachable from the Mac and was not touched. Its jobs are still stopped as at
STATUS20261120 §6 (budget 68 at 76 %, L15 campaign 51 leaves, FV304 379 modules).

## 1. Results of this session

| item | label | record |
|---|---|---|
| Rung N = 36 of the M(5;7) owner model (M(5;7) ≤ 35 if both cases close) | case B **CERTIFIED** (uncubed run + cake_lpr; geometry via the written arguments of ETV7SAT §2); case A 37/64 certified (all of state (5,1,1) occupied); M(5;7) ≤ 35 not established | M57R36N20261121 |
| Re-check of the written and Lean-source links of ES(8) ≤ 304 and of the Z*-row (303) | PROVED by re-derivation; no blocking or serious finding; 4 minor, 4 wording | ES8CHECK20261121 §1 |
| 3,131 catalog rows + Z-row + Z*-row on 8,419 real octagon-free sets (10–62 points) | EXACT computation, 0 violations (EVIDENCE for the rows) | ES8CHECK20261121 §2 |
| All 9 Lean files of the 305/304/303 composition (incl. `composition_304_z`, `composition_303_zzsf`) compiled on the Mac | Lean, standard axioms only; rebuilt chain311 modules and 4,952 pinned oleans byte-identical to Linux | ES8CHECK20261121 §4 |
| New balanced rows (58,950 (6,6)-chain rows, CG cuts, order rows) | PROVED rows, root LP unchanged at 66; chain rows enlarge the b68 Knuth estimate about 5.4× (HEURISTIC) | ES8CHECK20261121 §3 |
| Residual-side rows | none with LP gain; slice LPs are exactly 36 by the F/Lo partition; capacity thresholds tabulated | ES8CHECK20261121 §4b |
| N66 level-15 on the Mac | pipeline reproduced (UP cube trim.cnf byte-identical); blocked on Linux-only inputs | ES8CHECK20261121 §4c |
| Web literature check (18–21 Nov) | EVIDENCE: no competing ES(8) bound ≤ 319; no M(5;7) bound below 41 | ES8CHECK20261121 §5 |

## 2. Owner decisions pending

- Merge of branch `es-mac-2026-11-21` into main. The three records (M57R36N20261121, ES8CHECK20261121, this page) are
  committed on that branch, on top of origin/main 2d1cb6baa; main itself was not changed. If main has not moved, the
  merge is a fast-forward.
- Resume the rung-36 campaign (§3), and on which machine. The Linux machine (32 threads) would finish case A sooner.
- Copy the N66 level-15 inputs that exist only on Linux, so that the Mac can take part of the queue (ES8CHECK §4c):
  `p2/s15/q.json`, `mono/rows_1832.json`, the 27-pair SB list, the template_cert66 inputs, `c15_post.sh`.
- The elan toolchain leanprover/lean4 v4.36.0 that an `elan` auto-install added under `~/.elan/toolchains` today:
  keep or `elan toolchain uninstall leanprover/lean4:v4.36.0`.
- Unchanged from STATUS20261120: resume budget 68 (→ 303), the L15 campaign (→ N66 ≤ 54 → 302), FV304; deletions;
  e-mails and public wording.

## 3. Resume of the rung-36 campaign

M57R36N20261121 §8. Only case A remains: 46 open cubes in `cubes2/state.json`, all with state 26 empty. Proofs of the 67 certified leaves (66 cubes + the uncubed case B) are in `proof-archives/es7-r36-20261121/` on the Mac (16 GB, `SHA256SUMS`, `lrat_sha256.tsv`).
Everything else needed to resume is in git: the scripts in `M57R36N20261121/tools/`, the driver state in its
`logs/state_2.json` and the 66 per-leaf cake_lpr outputs in `logs/cake/`. The session's scratch area is not needed.
On Linux, `drive2.py` needs one change first (its memory check is macOS-only; M57R36N20261121 §8).

## 4. Lessons

- On macOS the Homebrew Python process is named `Python`. `pgrep -f 'python3 drive.py'` missed a running driver and
  let a second one start. Match on the script name (`drive\.py`), and check with `ps -Ao command -ww`.
- A wrapper that reacts to time (the 13:35 lane bump) must be stopped before the plan changes.
- cake_lpr heap for these 5.57 M-clause CNFs: 2,000 MB failed for 2 of 17 first checks, both with proofs under 1 GB;
  6,000 MB always sufficed. The CNF itself takes most of the heap.
- Under 20+ solver processes on 15 cores, the 1,500 s cube limit mostly produces splits. Fewer lanes, or a longer
  limit for the hard region, waste less.
