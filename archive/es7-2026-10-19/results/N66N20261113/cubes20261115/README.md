# N66 level 14 (N66 ≤ 55): cube-and-conquer plan and pilot (15 November 2026)

**Status: N66 ≤ 55 is NOT decided. N66 ≤ 56 (level 13, CERTIFIED, parent README §9) remains the bound.**
A 64-cube split of the level-14 relaxation was designed and 4 cubes were timed: 1 UNSAT, 3 with no verdict at 240 s
(COMPUTED). The UNSAT cube's trimmed core is CERTIFIED (cake_lpr `s VERIFIED UNSAT`) **for that sub-CNF only**: it has
not been through row justification or p2_verify, so it is not yet a certified cube of the argument. All run-time
estimates are HEURISTIC. A critic review found the cover and the use of the CNF sound but the first write-up flawed
(a spliced hash, an estimate whose low end was already ruled out, a count error, costs left out). The corrections
are applied below (§6).

Written 05:40–05:45 KST, 15 November, by the stage-3 writer of the roadmap-20261115 night. Work directory
`/home/jay/research/data/roadmap-20261115/n66cubes/` (abbreviated C; not in Git). Parent work directory
`/home/jay/research/data/n66-20261113/` (abbreviated W). Units `esr-agx-r3-n66cube` (pilot) and
`esr-agx-r3-n66lratB` (cube B with a proof): 1 thread, MemoryMax 3G, MemorySwapMax 0; both finished, none running at
05:40. This folder holds only this README; the scripts and data stay in C (§7). Nothing is committed.

Labels: **CERTIFIED** = CaDiCaL 2.1.3 LRAT accepted by cake_lpr (`s VERIFIED UNSAT`, grepped) for the stated CNF;
**COMPUTED** = solver verdict only; **HEURISTIC** = timings and estimates.

## 1. Statement

Level L of the parent record's phase-2 relaxation asks for an assignment of the 70 states (W = range(70); states 0
and 1 fixed occupied) with at most L holes that satisfies the monolithic clauses (mono66, parent §6), the justified
rows (parent §2) and, with `--sb`, the mirror symmetry breaking of parent §6.7. UNSAT at level L means every set of
the class has at least L+1 holes, so N66 ≤ 69 − L. Level 13 is CERTIFIED (N66 ≤ 56). Level 14 would give
N66 ≤ 55. The two monolithic level-14 solves stopped undecided at 3 h 10 min (parent README, update of 15 Nov 02:05).

## 2. Model and soundness of the split

- **Base CNF** F_c = `W/p2/b14h2/it1/cert.cnf`: 1,647,808 variables, 9,436,582 clauses, L = 14, SB on, 660,810
  activated quadruples. The critic's audit of its parts: eager clauses (a sub-CNF of mono66.generate); 660,810 × 12
  = 7,929,720 quadruple clauses; the fixed units of states 0 and 1; 15,648 row clauses; a sequential counter
  "at most 14" over the 68 non-fixed hole literals; the 79 SB clauses of 27 fixed pairs; no blocking clauses. F_c is
  a subset of the full level-14 formula F_full, so a refutation of F_c plus a cube refutes F_full plus that cube
  (subset clause, parent §6.3).
- **Split literals.** sel_s = DIMACS variable 988541 + s (layout.json; the CNF's fixed units are 988541 = sel_0 and
  988542 = sel_1). Occupied = +sel_s, hole = −sel_s. p2_write.py and p2_verify.py use bit 1 = occupied, bit 0 = hole.
- **Cover argument.** Suppose the cubes cover every assignment of the split variables, and for every cube c some
  CNF ⊆ F_full ∪ {units of c} is refuted by cake_lpr. Then F_full is UNSAT, and N66 ≤ 55 by parent §6.3 and §6.7.
  Conditions:
  - all cube certificates share L = 14, W = range(70) and the same SB pair list (the §6.7 lex argument holds for one
    fixed pair list; mixing lists breaks the cover);
  - rows and activated quadruples may differ between cubes;
  - every cube certificate ends with p2_verify ALL_OK, with its own cube units declared in the layout's `cube` field.
- **Lazy activation** needs no extra argument: p2_verify matches every trimmed clause against the mono66 stream, the
  justified rows, the re-encoded counter and SB clauses and the declared units. A cube's counterexample loop only
  affects progress.
- If the level-14 relaxation is satisfiable, no split of it gives N66 ≤ 55.

## 3. Method

- **Split states** 25, 12, 16, 29, 17, 37: the six states that occur most often in the 6,775 rows of the level-13
  trimmed core (the designer's count, not rechecked). 2^6 = 64 cubes (C/full64.txt). Unit propagation on the 79 SB
  clauses (C/sb_clauses.cnf) refutes 8 of them, all with 25 hole, 29 occupied and 37 hole. 56 real cubes remain.
- **Pilot** (C/run_pilot.sh): each cube = F_c with its 6 units appended and the header count raised by 6, streamed
  into `/usr/bin/cadical` 2.1.3 with default options, `-n -t 240`, no proof. The monolithic runs used
  `--cadopts=--unsat`; the pilot did not.
- **Cube B with a proof** (C/run_lratB.sh): the same cube CNF written to disk;
  `cadical -n -t 360 --lrat=true --binary=false`; `W/p2_lrat_trim`; `cake_lpr --CML_HEAP_SIZE=2000 trim.cnf
  trim.lrat`; grep for the exact line; zstd both proofs; the 664 MB cube CNF deleted after hashing (§7).

## 4. Results (COMPUTED; read from the CaDiCaL logs at 05:41)

Split states in the order 25 12 16 29 17 37; o = occupied, h = hole.

| cube | pattern | verdict | wall | conflicts | conflicts/s | peak RSS |
|---|---|---|---|---|---|---|
| A | o o o o o o | none at 240 s | 240.2 s | 149,218 | 631 | 2,773.5 MB |
| B | h h h h h h | **UNSAT** | 138.8 s | 103,945 | 767 | 2,347.2 MB |
| C | h h h o o o | none at 240 s | 240.2 s | 207,893 | 878 | 2,530.5 MB |
| D | o h o h o h | none at 240 s | 240.2 s | 249,454 | 1,053 | 2,510.3 MB |

- In D the SB clauses also force state 32 to be a hole.
- From the logs (designer's reading): about 60–100 s of each run is parsing plus the first simplification (A: active
  variables 685k → 159k after about 58 s). The rate inside a cube rises from about 600/s to about 1,000/s within
  4 min. The monolithic level-14 runs averaged about 5,000/s (57.8M conflicts in 3 h 10 min).
- A fifth cube (A plus 23, 49, 44, 40 occupied) was queued and dropped for the LRAT re-run. Not run.

**Cube B with a proof.**
- UNSAT again: 113.9 s CPU, the same 103,945 conflicts, peak RSS 2,390.1 MB. LRAT 689,307,993 bytes (657 MiB;
  135 MiB as zstd).
- p2_lrat_trim kept 32,541 of 9,436,588 original clauses (C/cubeB/trim.json): the 6 cube units (ids
  9436583–9436588; all used), the 2 fixed units, 392 or 393 row clauses (the designer says 393, the critic counts 392;
  recheck with W/p2_used_rows.py), and the rest geometric, counter and SB clauses.
- cake_lpr printed `s VERIFIED UNSAT` (C/cubeB/cake.out, grepped).
- **CERTIFIED: trim.cnf (SHA-256 b1c42bb7…, §7) is unsatisfiable.** Not established: that every clause of trim.cnf
  holds for every set of the class. Of its rows, 273 are in the level-13 justification.json (critic's count), so
  about 119 need new template_cert66 justification. p2_verify would currently flag the 6 cube units as unclassified,
  because the layout says `cube = []`.

**Rule breach in the pilot.** Cube A reached 90 % of its 3 GiB MemoryMax, above the 80 % sizing rule (the guard
stops at 95 %). It ended at its time limit with normal CaDiCaL statistics (exit 0); no guard stop, no OOM kill.

## 5. Estimates (HEURISTIC; corrected after the critic)

- Monolithic conflicts (designer's numbers, not rechecked): level 11 3.23M, level 12 9.99M (×3.10), level 13 23.70M
  (×2.37). Level 14: b14h2 reached 57,791,366 and b14i2 57,055,359, with no verdict. These are different CNFs
  (664,235,085 vs 658,479,655 bytes), not replicates.
- So level 14 on the b14h2 CNF needs **more than 57.8M conflicts** if it is UNSAT at all. It needs at most about 95M
  only if the growth ratio stays at or below 4. There is no real upper bound, and the relaxation may be SAT. (The
  first write-up's low end of 57M was already ruled out.)
- Spread evenly over the 56 real cubes (an assumption; cube-and-conquer often costs more in total), that is
  1.03–1.69M conflicts per cube:
  - at the pilot rates, 630–1,050/s: about 18–47 min per cube including about 2 min parsing, **17–44 CPU-h** for 56
    cubes;
  - at about 5,000/s, the monolithic average: about 5–8 min per cube, 5–7 CPU-h. This is an assumption: no cube came
    near that rate in 4 min.
- The load is uneven: cubes with many holes are cheap (B: 2.3 min). **38** of the 56 real cubes (not 42; 4 of the 42
  are refuted by unit propagation) have 3 or fewer holes among the split states and carry most of the work.
- Not in these numbers: LRAT output (one data point: B took 114 s CPU with LRAT and 138 s without), trimming,
  cake_lpr (the p2_cake heap tiers go up to 5.5 GB), row justification, recheck, and p2_verify (about 35–40 s each
  at levels 12 and 13).
- **Memory.** Peaks: 2,773.5 MB (cube A) and 2,857 MB (monolithic level 14), that is 90 % and 93 % of 3 GiB. A long
  cube can be expected to grow toward the monolithic peak. Per-cube MemoryMax must be at least 3.6G (80 % rule).
  Five cubes at 3.6G plus one cake_lpr slot at 5.5G is 23.5 GB, inside the 24 GB total; six cubes leave no room for
  cake_lpr.
- **Disk.** Cube B's untrimmed LRAT was 657 MiB for 104k conflicts; the monolithic one 29.6 GB for 57.8M. Hard cubes
  may write several GB each, tens of GB over 56 cubes (zstd ratio about 4.9 on B). 943 GB were free on `/` at
  05:41. Proofs are kept until an independent check; deleting any needs the owner's OK.

## 6. Critic's verdict and fixes

Verdict: **flawed** (the write-up; not the cover or the soundness).

Checked by the critic and found correct:
- The cover is complete: the 64 cubes are the full 2^6 split; the cube literals in C/cubes.txt are numbered correctly;
  layout.json has W = range(70) in order.
- C/sb_clauses.cnf is byte-identical to the last 79 lines of cert.cnf. Unit propagation, re-run, gives exactly the 8
  refuted cubes and confirms that D forces 32 to be a hole.
- The CNF is sound as a relaxation, provided each cube ends with p2_verify ALL_OK (§2).
- Cube B is labelled correctly: CERTIFIED for trim.cnf only.

Re-run here at 05:43: `cover_check.py full64.txt` prints COVER_OK (64 cubes); `cover_check.py cubes.txt` prints
NOT_COVERED (the 4 pilot cubes alone), as expected.

| issue found by the critic | fix | status |
|---|---|---|
| cube-B CNF hash was spliced (first 8 hex digits of the CNF hash + the tail of the LRAT hash) | use the value in C/cubeB/cert.cnf.sha256 | applied (§7) |
| estimate's low end (57M conflicts) was below what b14h2 had already reached | "more than 57.8M, no upper bound" | applied (§5) |
| "passed 57.8M in both runs": different CNFs | give both counts; not replicates | applied (§5) |
| 3 CPU-h low end needs about 5,000/s in every cube; pilot cubes averaged 630–1,050/s | recompute from observed rates; 5,000/s only as an assumption | applied: 17–44 CPU-h (the critic's 18–28 CPU-h assumed about 1,000/s) |
| LRAT, trim, cake_lpr, row-justification and p2_verify costs left out | list them | applied (listed, not estimated) |
| "42 cubes with ≤ 3 holes" counted all 64 | 38 of the 56 real cubes | applied (§5) |
| memory over the 80 % rule (90 % and 93 % of 3 GiB) | MemoryMax ≥ 3.6G per cube; cake_lpr tiers inside 24 GB | next run (§8) |
| disk not budgeted | set a budget; ask the owner before deleting proofs | next run (§8) |
| cube B not a finished certified cube | p2_cert/p2_verify in its own cert dir with layout `cube = [[25,0],[12,0],[16,0],[29,0],[17,0],[37,0]]` (bit 0 = hole); justify the ~119 new rows; require ALL_OK | next run (§8, step 1) |
| cover acceptance not specified | accept a cube only if verify.json has ALL_OK; L = 14; W = range(70); sb_pairs identical to the 27-pair list of b14h2 layout.json; cube literals taken from the layout/verify `cube` field that p2_verify used (bit 1 = occupied = +sel), never from planning files such as full64.txt; no rows justified only under cube assumptions | next run (§8, step 4) |
| UP-refuted cubes have no certificate files | run all 8 through the same pipeline | next run (§8, step 2) |

Not checked by the critic or here: the level-11 to level-13 conflict counts, the 6,775-row frequency order, and the
soundness of p2_lrat_trim and mono66 themselves (the existing pipeline is relied on).

## 7. Files and hashes

C = `/home/jay/research/data/roadmap-20261115/n66cubes/`:
- `run_pilot.sh`, `cubes.txt` (the 4 pilot cubes), `pilot_results.jsonl`, `log_A_allocc.txt`, `log_B_allhole.txt`,
  `log_C_h25h12h16_o29o17o37.txt`, `log_D_o25h12o16h29o17h37.txt`;
- `full64.txt` (all 64 cubes; planning only), `sb_clauses.cnf`, `cover_check.py` (exact enumeration over at most 22
  split variables, with an assert self-check);
- `run_lratB.sh`, `cubeB/`: `STATUS`, `cadical.log`, `cake.out`, `trim.json`, `used_ids.txt`, `trim.cnf`,
  `trim.lrat.zst`, `cert.lrat.zst`, `sha256.txt`, `cert.cnf.sha256`.

SHA-256:
- F_c, `W/p2/b14h2/it1/cert.cnf` (664,235,085 bytes; hashed 05:41):
  `14f43bf4ac4306bc415298b88afd1ca77af022a00d7468fd9fce2dffe9e8cbf3`
- cube-B CNF (deleted; F_c with header `p cnf 1647808 9436588` and the units `-988566 -988553 -988557 -988570
  -988558 -988578` appended, one clause per line): `9c19503d355cc8bf61d376a0ea3ab35c2530560fcd0bf44d4d970b6d4099f6a9`
- untrimmed LRAT (kept as `cert.lrat.zst`): `938bdfdc541017dee5e03d5e112746557663f55c441fce308823ef11544955a9`
- `trim.cnf` (rehashed 05:41): `b1c42bb7b5834b01a3f2a88ae5b9ede73e8d91d851315b34d5d3ff688472f1a1`
- trimmed LRAT (kept as `trim.lrat.zst`): `debb07417a074c7be8d7388edbca9fe3577e99819499477ce760b92c0a257521`

Untouched: the partial monolithic LRATs `W/p2/b14h2/it1/cert.lrat` (29.6 GB) and `W/p2/b14i2/it1/cert.lrat`
(29.2 GB). Deleting them is the owner's decision.

## 8. What remains: the recommended next run

Owner decisions first:
- **Compute allocation.** At one thread the estimate means 17–44 h wall at pilot rates. The run needs about five
  cube slots plus one cake_lpr slot (§5 memory), inside the 16-thread and 24 GB caps.
- **Disk budget** for the untrimmed proofs.

Then, in order, each step a systemd user unit with a deadline and memguard running:
1. **Pipeline test on cube B.** Copy W/p2_batch.py to a new file with a `--cube s:bit,...` option. The only change
   is line 39, `'cube': []` → the parsed list; p2_write.py, p2_verify.py and p2_cert.sh already handle `cube`
   (checked by grep at 05:41). Run it with the parent record's level-14 options (`--warm p2/s14/c.json --tauclose
   --sb --cadopts=--unsat`, environment `ETV_A=4 ETV_B=4 P2_UNIT=<unit>`, the same SB pair list) and cube
   `[[25,0],[12,0],[16,0],[29,0],[17,0],[37,0]]`, then p2_cert.sh in its own cert directory. Justify the ~119 new
   rows and require p2_verify ALL_OK. If this fails, fix the pipeline before scaling.
2. **The 8 UP-refuted cubes** through the same pipeline (their proofs are immediate).
3. **The other 55 real cubes**, the 38 with ≤ 3 holes last:
   - limit 20 min per cube (a HEURISTIC choice);
   - a cube past its limit is split on the next state in the level-13 row-frequency order 23 (2,550 rows), 49, 44,
     40, 20, 32, 46, 45, 52, 35, 30, 39 (designer's order, not rechecked), mainly down the occupied side;
   - the same SB pair list everywhere;
   - MemoryMax 3.6G per cube, or pre-filter each cube CNF to drop the clauses its units satisfy (sound by the subset
     clause).
4. **A new cover script** that reads the cert.json/verify.json files with the acceptance rules of §6. The driver
   accepts only certificates without a cube, so it cannot do this step. cover_check.py's enumeration handles trees
   with up to 22 split variables.
5. **SAT cubes.** A cube that is SAT on its activated subset gets its violated quadruples added and is re-solved. A
   cube SAT on the full formula ends this route for level 14.

Not tried:
- march-style lookahead cubing (not installed; installing third-party code needs the owner's OK);
- the alternative SB-pair split: the first four SB pairs (32,37), (29,25), (39,45), (24,30) give 256 cubes, of which
  unit propagation refutes 120, leaving 136; the τ-pair set {32,37,29,25,23,17,16,12} leaves 160 real cubes. Counted,
  not timed.

## 9. Resume commands

```bash
C=/home/jay/research/data/roadmap-20261115/n66cubes
# 1. rebuild the cube-B CNF in a pipe and compare with the recorded hash (no solver; reads 664 MB)
SRC=/home/jay/research/data/n66-20261113/p2/b14h2/it1/cert.cnf
{ echo "p cnf 1647808 9436588"; tail -n +2 "$SRC"; for l in -988566 -988553 -988557 -988570 -988558 -988578; do echo "$l 0"; done; } | sha256sum
#    expect 9c19503d355cc8bf61d376a0ea3ab35c2530560fcd0bf44d4d970b6d4099f6a9
# 2. re-check the trimmed certificate; cake_lpr exits 0 on rejection, so grep the exact line (decompress on disk, not /tmp)
zstd -dc $C/cubeB/trim.lrat.zst > $C/cubeB/trim.lrat
systemd-run --user --unit=esr-n66cube-recheckB -p CPUQuota=100% -p MemoryMax=3G -p MemorySwapMax=0 \
  -p RuntimeMaxSec=1800 --nice=10 --working-directory=$C/cubeB \
  sh -c '/home/jay/.local/bin/cake_lpr --CML_HEAP_SIZE=2000 trim.cnf trim.lrat > cake2.out 2>&1'
grep -x 's VERIFIED UNSAT' $C/cubeB/cake2.out
# 3. cover check of the full 2^6 split (planning file; prints COVER_OK 64 cubes)
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -I $C/cover_check.py $C/full64.txt
```
