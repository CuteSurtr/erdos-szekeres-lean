# M57R36N20261121: rung N = 36 of the M(5;7) owner model, cube campaign on the Mac (21 November 2026)

**Result: case B of rung N = 36 is CERTIFIED (modulo the written arguments of ETV7SAT §2): every set of 36 points in general position with distinct x, no 5-cap and no convex heptagon has at most 13 points that end a 6-cup, and the same holds for 2-colourings. Case A (the remaining case, r ≤ 13) is certified on 37/64 of its cube space, including the whole sub-case "state (5,1,1) occupied". M(5;7) ≤ 35 is NOT established.**

M(5;7) is the largest size of a point set in general position, with distinct x-coordinates, no 5-cap and no convex
heptagon. Before this record: 26 ≤ M(5;7) ≤ 36 (ETV7SAT20261113, CERTIFIED modulo the written arguments of its §2).
Rung N = 36 asks whether the owner-model CNF "exactly 36 points" is unsatisfiable. If it is, M(5;7) ≤ 35.

Labels as in ETV7SAT20261113. For a case or a cube region, **CERTIFIED** means three things:
- every leaf CNF has an LRAT proof accepted by cake_lpr (exact line `s VERIFIED UNSAT`);
- every leaf CNF equals the case CNF plus unit clauses (SHA-256 recomputed from the base);
- the certified leaves cover the region (EXACT).

The step from the CNF to geometry is the written argument of ETV7SAT §2 (PROVED there, not machine-checked).

## 1. What is claimed and what is not

Claimed:
- **Case B** (`c36_tle22`, t ≤ 22) is **CERTIFIED** UNSAT. The same written-argument status as ETV7SAT §6.2 applies.
  - Proof: the uncubed CNF, run once with CaDiCaL 3.0.1, UNSAT. 11,619,241 conflicts, 8,695 s wall (7,370 s solve),
    12:10:20–14:35:15 KST.
  - LRAT: 6,918,174,929 bytes, SHA-256 `99c81fa463e1f53257897943736d32f7744bda1cebfc3db3182234f3dc15d0af`.
  - cake_lpr: heap 9,000 MB, 202 s, exact line `s VERIFIED UNSAT` (`logs/mono.cake`, `logs/mono.cake.meta`).
  - Reading: in every 36-point set (or 2-colouring of triples) with no 5-cap and no (weak) heptagon, t ≥ 23, i.e.
    r = 36 − t ≤ 13. That is, at most 13 points end a 6-cup.
  - This supersedes the "COMPUTED only" status of case B in ETV7SAT §6.2. The 13 November proof (CaDiCaL 2.1.3) is
    not used; its only cake_lpr check ran out of heap at 2,600 MB and was not repeated.
  - Second route, redundant: 28 case-B cube leaves are also certified (45/64 of the case-B cube space), by the
    drivers' own checks (exact line; cube CNF hash computed when the cube was written). The end-of-campaign re-check
    of §6 covered case A only.
- **Case A** (`c36_rle13`, r ≤ 13): 38 leaves are certified; together they cover 37/64 of the case-A cube space (exact
  sum of 2^−|cube|).
  - They include every leaf with occ[26] = 1, so **case A with state 26 = (5,1,1) occupied is CERTIFIED UNSAT**.
    (State indices follow `cat_common.make(3, 5)`; f = (f₁, f₂, f₃).)
  - Of the half with state 26 empty, 5/64 of the case-A space is covered: 9/128 in the quarter with state 21 =
    (5,1,0) occupied (9/32 of that quarter) and 1/128 in the quarter with state 21 empty (1/32 of it).
- **Together** (modulo the written arguments of ETV7SAT §2): a 36-point set with no 5-cap and no convex heptagon (or
  such a colouring) has at most 13 points ending a 6-cup, leaves state (5,1,1) empty, and lies in one of the 46
  uncovered case-A cubes (`logs/state_2.json`, status queued or running; 27/64 of the case-A cube space).
  - Reading the last part requires the owner-model semantics of ETV7SAT §2.


Not claimed:
- **M(5;7) ≤ 35 is not established (27/64 of the case-A cube space is open).**
- ETV(7;5,7) = 26 is not decided.
- Nothing unconditional about ES(7) or ES(8).
- The CNF-to-geometry step, the lemma rows (ETV7SAT §2.3) and the case split are written arguments.
- No novelty claim. No matching prior result was found in the sources inspected (NOVELTY20261113B §§3, 6, 10; ETV7SAT §9;
  the web check of 21 Nov in ES8CHECK20261121 §5).

What M(5;7) ≤ 35 would give, from the audit (agents/r36_audit.json; arithmetic on the named records, not reviewed):
- the open ETV range becomes 27–35;
- the colouring version: the largest 2-colouring of triples with no 5-cap path, no 7-cup path and no weak heptagon has
  27–35 vertices;
- LEDGER_1115PM item I4 becomes 35, and the weak D(5,8) window 17–58;
- conditional ES(8) rows of that ledger: weak D(5,8) gives 302 (301 with N66 ≤ 55); CB(8) gives 301 (300);
- for 33-point ES(7) counterexamples nothing changes (ES7SPLIT: split-freeness needs N(7,5,7) ≤ 26).

## 2. Inputs (EXACT)

| case | CNF | rows | variables / clauses | SHA-256 |
|---|---|---|---|---|
| A, r ≤ 13 | `run/c36_rle13.cnf` | S1:25 S2:25 B1:16 **B2:13** ALL:36 | 457,857 / 5,569,648 | `aba65111d42151131a55e7596043721bd86fe94d05c8fea0b2750212d2808bbe` |
| B, t ≤ 22 | `run/c36_tle22.cnf` | **S1:22** S2:25 B1:16 B2:16 ALL:36 | 457,842 / 5,569,618 | `08b8ea9c9c588aa242485163a3d4836a0c79f8bd91c61ac25357010dc2bd9339` |

- Both CNFs were regenerated on the Mac with the record's own tools: `python3 -B owner.py 3 5 7 36 base.cnf --names
  --nosig`, then `addrows.py` with the rows above. Both equal the recorded SHA-256.
- The tools' hashes equal ETV7SAT's `SHA256SUMS`.
- The 13 November proof of case B (CaDiCaL 2.1.3, 5.23 GB; its only cake_lpr check ran out of heap at 2,600 MB) is on
  the Linux machine and is not used.
- **Case split** (ETV7SAT §6.2; PROVED, elementary).
  - Row ALL:36 means at most 36 occupied states. The base family K means at least 36.
  - r = number of occupied states with f₁ = 5 (21 states); t = number with f₁ ≤ 4 (35 states).
  - r + t = 36, so r ≤ 13 (case A) or t ≤ 22 (case B).
  - Re-derived by the audit; `cube_cover.py` logic.

## 3. Method

- **Solver:** CaDiCaL 3.0.1 (`e12ecc8c…`) `--lrat --binary=false`. **Checker:** cake_lpr (`2fee767a…`); a leaf counts
  only on the exact line `s VERIFIED UNSAT`.
- **Cubes:** unit clauses on occupancy variables occ[s] = variable 32759 + s.
  - Case A splits on states 44, 39, 26, 21, 15, 33 (64 cubes), then 27, 37, 32, … These are the B2 states with the most
    occurrences (`occstat.py`).
  - Case B splits on states 34, 31, 16, 28, 22 (32 cubes), then 36, 29, … (S1 states).
  - A cube that hits the time limit is replaced by its two children on the next state of its order. The leaves
    therefore always cover the case. The limit was 1,500 s, except 600 s in the `drive.py` run from 13:07.
    `drive.py` and `drive_b.py` split on any exit code other than 10 or 20; `drive2.py` splits only on exit 0 with
    `c UNKNOWN` and marks other exit codes `error`.
- **Case B also ran uncubed:** one monolithic CaDiCaL run from 12:10 KST, UNSAT after 8,695 s wall (11,619,241 conflicts), LRAT 6.92 GB accepted by cake_lpr at heap 9,000 MB (case B CERTIFIED; §1).
- **Drivers:**
  - `drive.py` (case A, `cubes/`);
  - `drive_b.py` (case B, `cubes_b/`; started 12:46 so that case B got lanes);
  - `drive2.py` (both cases, `cubes2/`; from 13:40 it takes over the queued jobs of the other two through
    `handoff.py`, which never moves a job those drivers could still start);
  - `reverify.py` (re-checks leaves whose first cake_lpr ran out of heap).
- Each certified proof was compressed with zstd. The round trip is checked by hashing the decompressed stream, then the
  raw LRAT and the cube CNF are deleted. The CNF is regenerable from the base and the units; its hash is in
  `results.tsv`.
- **Machine:** Mac M5 Pro, 15 cores, 48 GB. Up to 23 solver processes ran at once (24 in the aborted window of §5), alongside the session's agents and one
  unrelated long-running single-thread job. All solver timings are wall times under that load (HEURISTIC).

## 4. Results

| case | route | certified leaves | covered | solver wall of certified leaves | conflicts | raw LRAT bytes | cake_lpr heaps (MB) |
|---|---|---|---|---|---|---|---|
| A | cubes (`drive.py`, `drive2.py`) | 38 | **37/64** (all of occ[26] = 1) | 12,900 s | 14,037,304 | 26,885,707,834 | 2,000–6,000 |
| B | uncubed run | 1 | **all** | 8,695 s | 11,619,241 | 6,918,174,929 | 9,000 |
| B | cubes (`drive_b.py`, `drive2.py`; redundant) | 28 | 45/64 | 33,266 s | 45,055,447 | 37,619,174,059 | 6,000 |

- **Effort, cube runs included in `results_*.tsv` (wall under load, HEURISTIC):**
  - case A: 58 runs, 33,931 s, 20 of them time-outs (10 at 1,500 s and 10 depth-7 cubes at 600 s, then split);
  - case B: 57 runs, 73,179 s, 24 time-outs. These totals include the 5 case-B cubes stopped at 14:40 once the
    uncubed certificate existed (status `error`, rc −15, 3,874 s; they are in `results_2.tsv`).
  - Not in these totals: the runs discarded at 12:12, 13:03 and 14:42 (§5).
- **Case-A difficulty.** With state 26 occupied, the 32 leaves closed in 72–388 s. With state 26 empty, 6 cubes closed
  in 758–1,408 s and the other 20 that ran reached their limit (9 depth-6 cubes at 1,500 s; 11 depth-7 cubes, 10 of
  them at 600 s). The quarter with state 21 also empty is the hardest (1/32 of it covered). The uncovered 27/64 is the
  hard core.
- **No cube returned SAT.** No accepted proof failed its round trip.


## 5. Incidents (none affects a counted leaf)

- **12:11–12:14, two drivers at once.**
  - A first driver was not detected by `pgrep` (its process name is `Python`), and a second one was started.
  - For about 2 minutes, two solvers wrote the same 11 proof files.
  - Both drivers and all 23 solvers were stopped by PID. Every file of those cubes was deleted, the state was reset,
    and a single driver was restarted at 12:14:33.
  - Nothing from that window is counted.
- **cake_lpr heap.**
  - The first driver's heap max(2000, 1200 + 0.9·LRAT MB) was too small for two leaves ("CakeML heap space
    exhausted").
  - `reverify.py` re-checked both at 6,000 MB, after verifying that the CNF and LRAT hashes equal the recorded ones;
    both were accepted.
  - From 12:24 every new driver uses min(12000, max(6000, 2000 + 0.8·MB)). Which heap applied is in the heap column
    of `results.tsv`. `reverify.py` covers only `cubes/`: a heap failure under `drive2.py` would stay `cake_failed`
    and not be re-queued (none occurred).
- **13:03, case-A driver paused** (STOP file) to give case B the lanes. Its 10 running cubes were discarded
  (re-queued, not split; partial LRATs deleted). `logs/paused-1303.txt` lists 9 of their 10 proof files
  (`A_h44h39h26h21h15h33h27` is missing); two lines naming a temporary file of the session were removed from it before
  the commit.
- **13:07, queue reorder.** Case-A queue reordered so that the cubes with state 26 occupied come first.
- **13:14, priority change.** The cube solvers running at 13:14 were reniced to 15 so that the monolithic case-B run
  (nice 10) got preference. Later solvers started at nice 5 (`drive.py`, `drive_b.py`) or 10 (`drive2.py`).
- **13:35–13:40, oversubscription.** An automatic lane increase restarted 10 case-A cubes before the hand-off, so up
  to 23 solvers (with the monolithic run) ran at once, more than 15 of them from 13:35 to 13:46 (memory stayed below
  20 GB RSS in all).
- **14:41–14:42, final stop.** `drive2.py` started 6 case-A cubes at 14:41:29; the STOP file ended them at 14:42:17.
  They are the 6 `running` jobs of `logs/state_2.json`, which `drive2.py` re-queues when it starts.
- The audit's liveness findings are fixed in `drive2.py`:
  - a dictionary race in the state save;
  - non-time-out exit codes treated as time-outs;
  - overwritten failed cake outputs.

## 6. Checks

- `verify_cover.py` (own code, stdlib): per case, it checks four things:
  - the base hash;
  - for every counted leaf, the exact cake_lpr line and the zstd round trip against the recorded LRAT hash;
  - the regenerated cube CNF hash;
  - exhaustive coverage of the sign patterns of the split variables.

  Output at the end of the session: 
```
case A: base run/c36_rle13.cnf sha aba65111d4215113... OK
case A: 38 verified leaves, 0 bad, variables [15, 21, 26, 27, 33, 39, 44], uncovered patterns 54 of 128
case A: NOT COVERED
case B: base run/c36_tle22.cnf sha 08b8ea9c9c588aa2... OK
case B: monolithic certificate c36_tle22.cake: exact line yes; meta names the base CNF hash: yes; base hash: OK
case B: COVERED (monolithic)
RUNG 36: NOT COMPLETE
```
- That run (14:43 KST) regenerated every case-A leaf CNF (38) from the base and checked its hash. It also
  decompressed every archived case-A proof and compared it with the recorded LRAT hash. Case B passed on the
  monolithic certificate, so the script did not re-check its 28 cube leaves (§1).
- The proofs were then moved to the archive. A re-run needs the session's layout: `cubes/`, `cubes_b/` and `cubes2/`
  with their `state.json` and `results.tsv` (`logs/state_*.json`, `logs/results_*.tsv`), the `.cake` files
  (`logs/cake/<dir>/`) and the archived `.lrat.zst` files; `run/c36_tle22.cake` and `.cake.meta` (`logs/mono.cake`,
  `logs/mono.cake.meta`); and both regenerated CNFs.
- `summarize_r36.py`: certified leaves and the exact covered fraction Σ 2^−|cube| per case.
- The independent audit (agent r36-audit, 12:15–12:31, `agents/r36_audit.json`): the case split and the cube cover are
  complete, and no path lets a leaf count without base + units and the exact line. Its liveness findings are listed
  in §5. Its reporting findings are in `agents/r36_audit.json`: stale `cake_failed` entries in `state_A.json` (the
  accounting reads `results.tsv`), naming both `drive.py` versions (§9), and the base hash on the monolithic path of
  `verify_cover.py` (fixed in the filed version).
- The audit's own scripts are in `tools/audit/`: `audit_static.py`, `cube_files_check.py` and its end-of-campaign
  checker `final_check.py`, which reads only `cubes/` (the jobs of `drive.py`) and was not updated after the hand-off
  to `drive2.py`.

## 7. Rung N = 35, prepared (agent rung35-prep; nothing solved)

- Four cases from the two partitions S1/B2 and B1/S2 (A: B2 ≤ 12, B1 ≤ 12; B: B2 ≤ 12, S2 ≤ 22; C: S1 ≤ 22, B1 ≤ 12;
  D: S1 ≤ 22, S2 ≤ 22).
- Coverage PROVED and script-checked: 329 block-count vectors, each in exactly one case; the check fails if case D is
  removed.
- CNF hashes in `agents/rung35.json`.
- Caveat: `--nosig` covers colourings. If a 35-vertex colouring exists, some cube is SAT and the rung needs the
  signotope packets.
- Scripts in `tools/rung35/` (session paths appear as the plain word SCRATCH):
  - `gen_cases.sh` builds the four case CNFs with `owner.py` and `addrows.py` of ETV7SAT20261113 (the copies used are
    byte-identical to the record's); `setup_r35.sh` prepares a run directory (not run);
  - `cover35.py`: the coverage check; `cube_cover.py`: the same check for the two cases of rung 36; `leafcover35.py`:
    the leaf cover of a driver state file;
  - `order35.py` and `order35.json`: the split orders; `drive35.py` is `tools/drive.py` plus `drive35.diff`;
  - `probe.sh` and `rates.txt`: a rate probe of at most 120 s per case; `SHA256_CNF.txt`, `SHA256_TOOLS.txt`;
    helpers `cat_common.py` and `states_of.py`.
  - `SHA256_TOOLS.txt` was written before the copy. `probe.sh` and `setup_r35.sh` no longer match it, because their
    paths were replaced.

## 8. Resume

Only case A remains. Its open cubes are the `queued` and `running` jobs of `cubes2/state.json` (40 + 6).
`drive2.py` re-queues `running` jobs when it starts. All jobs lie in the state-26-empty half.
```bash
cd <r36-dir>                      # needs run/c36_rle13.cnf (regenerate: owner.py 3 5 7 36 --names --nosig; addrows.py ...)
rm -f cubes2/STOP cubes2/NOSTART; echo B > cubes2/SKIP_CASES        # case B is closed
echo 13 > cubes2/LANES; echo 13 > cubes2/CAP; echo <epoch of last start> > cubes2/STOP_AT
TL=3600 nohup python3 -B drive2.py > cubes2_driver.out 2>&1 &       # a longer limit wastes less in the hard core
python3 -B summarize_r36.py; python3 -B verify_cover.py             # accounting; then archive_r36.py
```
- From git alone: put `tools/*.py` and `tools/helper.sh` in an empty `<r36-dir>`; create `cubes2/`, copy
  `logs/state_2.json` to `cubes2/state.json` (byte-identical to the live state at the stop) and `logs/results_2.tsv` to
  `cubes2/results.tsv`; link `bin/cadical` (CaDiCaL 3.0.1) and `bin/cake_lpr`; regenerate `run/c36_rle13.cnf` as in §2
  and check its SHA-256. That is enough to run `drive2.py`. The accounting scripts need the full layout of §6.
- `archive_r36.py` rewrites the archive's `SHA256SUMS` and `lrat_sha256.tsv` from `summary.json`, i.e. from the cube
  leaves only. A re-run would drop the two lines of the uncubed case-B proof (`mono/c36_tle22.lrat.zst`, SHA-256
  `91514fd8fd0d1972706e1f369d88ba180553d86bedde132b5f58105a67f5ce57`): re-add them. Set `ARC` first; the filed copy
  has the placeholder `<mac-repo>`.
- On Linux: the memory check `mem_used()` of `drive2.py` calls `vm_stat` (macOS only, 16 KiB pages). Replace it, for
  example by MemTotal − MemAvailable from `/proc/meminfo`, or drop it. Use Linux builds of `cadical` and `cake_lpr`,
  and raise `LANES` and `CAP`.
- A 32-thread Linux run is the natural place for the hard core. Copy the scripts and the state, regenerate the CNF and
  check its hash.
- Suggested split order there: keep 27, 37, 32, … as now, or test a cardinality split on r (r ∈ {11, 12, 13} is forced
  in case A by the rows S1 ≤ 25 and ALL = 36) before committing many CPU-hours.

## 9. Files

- `tools/`:
  - `drive.py`: this file (SHA-256 `093350926a16…`) ran from 13:07, with TL=600; the run from 12:14 differed only in
    line 100, the heap max(2000, 1200 + 0.9·LRAT MB);
  - `drive_b.py`, `drive2.py`, `handoff.py`, `helper.sh`, `reverify.py`, `verify_cover.py`, `summarize_r36.py`,
    `occstat.py`, `archive_r36.py`;
  - `audit/`: the audit's scripts (§6); `rung35/`: the rung-35 preparation (§7).
- `logs/`: the driver logs, the reverify log, `results.tsv` and `state.json` of each driver, `summary.json`. Machine
  paths are replaced by placeholders.
  - `logs/cake/<dir>/<id>.cake`: the cake_lpr output of each of the 66 certified cube leaves (each is the exact line);
  - `logs/mono.*`: the uncubed case-B run (solver tail, cake_lpr output and meta, zstd round trip);
  - `logs/paused-1303.txt`: proof files discarded at 13:03 (§5).
- `agents/`: the audit and the rung-35 returns (JSON).
- `SHA256SUMS`: every file of this directory except `README.md` and itself.
- Proofs: `proof-archives/es7-r36-20261121/` on the Mac (not in git):
  - `cubes/`, `cubes_b/`, `cubes2/`: every certified cube leaf as `<id>.lrat.zst` (37, 14 and 15 files);
  - `mono/c36_tle22.lrat.zst`: the uncubed case-B proof (SHA-256 `91514fd8…`; raw LRAT `99c81fa4…`);
  - `SHA256SUMS` (the 67 zst files) and `lrat_sha256.tsv` (raw LRAT hashes from `results.tsv`, plus the mono row).
