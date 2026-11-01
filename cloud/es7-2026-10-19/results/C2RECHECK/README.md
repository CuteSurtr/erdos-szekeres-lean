# C2RECHECK: re-checks of the central 34-point records

Local runs on an Apple M5 Pro, 1–2 November 2026 (UTC). The records re-checked are those of `C2FINAL` (`es7-cloud` at
a15dd2ce3, unchanged since).

**Status.** §1–§3 are complete. §4 and §5 were still running when the table in §6 was made. This directory reports
re-checks only. Whether the 34-point statement is claimed is decided in `C2FINAL` and `WRITEUP`.

## What the re-checks close

The review in `C2FINAL` §8 and the audit of 1 November (`AUDIT3` §5) named four gaps:

1. **cake_lpr on unhashed CNFs.** This affected the 120 hexagonal cases (`C2C34/hchecker.sh`) and the 58 P8 orbits
   closed only by pilot records (`C2C34/p8/checker.sh`). cake_lpr ran on a CNF rebuilt by the same awk command as the
   lane but not hashed; lrat-check ran on the hashed file (`C2FINAL` §8, finding 2). Closed by §1 and §3.
2. **Unfinished sample.** The random sample of `C2FINAL` §5 stopped at 21 of 24 units (finding 1). Closed by §2.
3. **Mac-only facts.** 60 orbits and the covers of P1..P5 were closed only by records of the Mac lanes
   (`C2P2/LOCAL` to `C2P5/LOCAL`, `C2P/LOCAL_DEEP`). The sample excluded these lanes, and their records do not name the
   tools used (`AUDIT3` §5, row 2). Closed by §4 once it finishes.
4. **Lane-confined errors** (`AUDIT3` §5, row 8). An error confined to one lane would show only if a unit of that lane
   were re-solved. Examples are a wrong base file, solver or checker on one machine. The re-solves of `C2FINAL` §5 and
   of §4 here touch 38 of the 281 lanes with certified records (`lists_check.py`). Addressed by §5.

**Recount** (`lists_check.py`, from the records).
- The 2,296 orbits of P1..P8 (8 × 287) are closed as follows:
  - 2,117 by cloud records only;
  - 55 by both cloud and Mac records;
  - 60 by Mac records only;
  - 58 by pilot records only;
  - 6 by pilot records without a CNF hash, re-solved in `C2FINAL` §4.
- The covers of P1..P5 are Mac records and those of P6 and P7 are cloud records. The P8 cover was re-solved in
  `C2FINAL` §4.
- The pilot list holds exactly one unit per pilot-only orbit. The local list holds exactly one unit per Mac-only orbit,
  plus the five Mac covers.

## Method

**Re-solves** (`reproduce.py`, `reproduce_pilot.py`, `reproduce_local.py`; one unit at a time per process):
1. Rebuild the unit CNF as `C2P/tools/lane.py` does. This is the base `b0061e90…` (`C2FINAL` §3) with the header
   clause count raised by n, followed by n extra clauses: the subcase cube as units, or, for a cover, the hull cube as
   units and one clause per subcase. Require the SHA-256 recorded for that unit and lane.
2. Solve with CaDiCaL 3.0.1 `--lrat --binary=false`. Record whether the proof has the recorded size and SHA-256.
3. Run lrat-check and cake_lpr on exactly that CNF and that proof. cake_lpr gets an 8,000 MB heap and is retried with
   a larger heap if that is exhausted. The heap used is in `cake_heap_mb`; the records of `C2FINAL/sample/reproduce.py`
   lack that field, and that script always used 8,000 MB.
4. Compress the proof with zstd into a local archive (outside Git). Decompress it and require the proof's SHA-256
   (round trip).
5. Delete the CNF and the uncompressed proof, and append one JSON line.

**Hexagonal re-check** (`hexcheck.py`). It solves nothing.
1. Rebuild the case CNF as `C2C34/hlane.sh` does and require the CNF SHA-256 recorded in `C2C34/logs/hex_cases.tsv`.
2. Require the recorded archive SHA-256. Decompress the archived proof and require its recorded size and SHA-256.
3. Run both checkers on these two files.

**Local archives** (outside Git), one file `<unit>.lrat.zst` per unit. Each re-solve's JSON line gives its
`archive_sha256`.

| re-check | archive |
|---|---|
| §1 | `es7-symmetry`, folder `central34-hull` (written for `C2C34` §3; only read here) |
| §2 | `es7-central34-resample-2026-11-01` |
| §3 | `es7-central34-pilot-orbits-2026-11-01` |
| §4 | `es7-central34-local-2026-11-01` |
| §5 | `es7-central34-lanespot-2026-11-01` |

## 1. Hexagonal hulls (`hexcheck.py`, `hexcheck.jsonl`)

- **Result.** In all 120 cases the rebuilt CNF and the archive have the recorded SHA-256, and the decompressed proof
  has the recorded size and SHA-256. lrat-check (`c VERIFIED`) and cake_lpr (`s VERIFIED UNSAT`) both accept.
- **Times.** cake_lpr took 132 to 763 s per proof (median 227 s), with an 8,000 MB heap. lrat-check took 31 to 82 s.
- **Proofs.** 3.97 to 5.21 GB each, 524 GB in all.

## 2. Random sample (`sample_main.jsonl`, `sample_q3.jsonl`, `sample_extra.jsonl`)

**Units.** The 24 units of `C2FINAL/sample/sample.txt`: seed 20261101, drawn before any result was seen.
- `sample_main.jsonl` holds the 21 finished at the `C2FINAL` stop. It is `C2FINAL/sample/out.jsonl` without its two
  reproducibility lines.
- `sample_q3.jsonl` holds the other three: P6_9-11, P7_1-15 and P8_1-10.

**Result.** All 24 rebuild the recorded CNF hash and are accepted by both checkers. 23 reproduce the recorded proof.

**P8_1-10** (record `C2P2/M02`, CNF `163f52ea…`) gave a different proof, and both checkers accept it:

| | proof bytes | SHA-256 | solve |
|---|---|---|---|
| record | 9,984,634,396 | `d50827a7…` | 5,935 s |
| re-solve | 9,952,275,647 | `e98aa3ee…` | 2,978 s |

Proofs are not reproducible in general (`C2FINAL` §5, `P6_1-7`).

**Extra sample.** The 8 units of `C2FINAL/sample/extra_sample.txt` (seed 20261102). All 8 reproduce the recorded
proof and are accepted by both checkers. `sample_extra.jsonl` is `C2FINAL/sample/extra_out.jsonl`.

**Scripts.**
- The 21 + 8 records come from `C2FINAL/sample/reproduce.py`.
- The three in `sample_q3.jsonl` come from `reproduce.py` here. It adds an optional solve cap (`REPRO_CAP`) and the
  cake_lpr heap retry of `lane.py`.

## 3. P8 pilot orbits (`reproduce_pilot.py`, `pilot_orbits.jsonl`, `pilot_units_1.txt`, `pilot_units_2.txt`)

- **Units.** One unit for each of the 58 orbits, with its pilot record in `C2C34/logs/p8_units.tsv` (source
  `C2C34/p8`). The two lists ran as two processes.
- **Result.** All 58 rebuild the CNF hash recorded by the pilot and reproduce the recorded proof (same size and
  SHA-256). Both checkers accept each proof on the hash-checked CNF. So the pilot's recorded proofs have now been
  checked against hash-checked files.
- **Script.** `reproduce_pilot.py` is `reproduce.py` with the pilot rows added as records.

## 4. Mac-only orbits and covers (`reproduce_local.py`, `local.jsonl`, `local_units_1.txt`, `local_units_2.txt`)

- **Units.** 65, all from Mac records, in two lists run as two processes:
  - one unit for each of the 60 orbits: P5 20, P3 15, P6 7, P7 7, P2 5, P1 4, P8 2;
  - the covers of P1..P5.
- **Script.** `reproduce_local.py` extends `reproduce_pilot.py`. It builds cover CNFs as `lane.py` does (see Method),
  and it takes the case from the unit name, not from the record.
- **Effect.** A unit accepted here by both checkers no longer depends on the unrecorded tools of the Mac lanes.
- **Result.** See §6 (complete: 65 of 65).

## 5. Lane spot check (`lanespot.jsonl`, `lanespot_units.txt`, run with `reproduce_local.py`)

- **Units.** One certified unit from each of the 242 lanes with no unit among the re-solves of `C2FINAL` §5 and §2
  here or in the list of §4: 241 cloud lanes and the Mac lane `C2P/LOCAL`. The third-layer lane `C2P/LOCAL_L3` is
  left out, since its pieces close no orbit.
- **Choice.** Each lane contributes its unit with the shortest recorded solve time, except `C2P4/M06`. There the list
  has the second shortest, P4_1-6-12 (670 s), instead of P4_7-9 (546 s).
- **Order.** The units run by recorded solve time, from 17.8 s to 5,884 s.
- **Scope.** This checks lanes, not a random sample of units: it detects a fault that affects a whole lane.
- **Result.** See §6: 145 of 242 lanes when the run was stopped at the end of the session; the remaining lanes rest on their records.

## 6. Results (`summarize.py`, `summary.json`)

**Final totals** (last record finished 2026-11-01 20:54:18 UTC). The other documents of 1 November quote an earlier snapshot
(records finished by 19:43:14 UTC: 44 of 65 for §4 and 81 of 242 for §5); these totals supersede it.

| Re-check | done | CNF hash = record | proof = record | both checkers | archive round trip |
|---|---|---|---|---|---|
| Hexagonal hulls (§1) | 120 of 120 | 120 | 120 | 120 | 120 |
| Random sample, main (§2) | 24 of 24 | 24 | 23 | 24 | 24 |
| Random sample, extra (§2) | 8 of 8 | 8 | 8 | 8 | 8 |
| P8 pilot orbits (§3) | 58 of 58 | 58 | 58 | 58 | 58 |
| Mac-only orbits and covers (§4) | 65 of 65 | 65 | 65 | 65 | 65 |
| Lane spot check (§5) | 145 of 242 | 145 | 145 | 145 | 145 |

Proofs that differ from the record: P8_1-10 (random sample, main). Not accepted by both checkers: none. The five
covers are among the 65 units of §4, and the 145 units of §5 come from 145 lanes.

**Columns.**
- "proof = record": for a re-solve, the new proof has the recorded size and SHA-256. For §1, the decompressed
  archived proof does.
- "archive round trip": for a re-solve, decompressing the new archive gives the proof's SHA-256. For §1, the archive
  has its recorded SHA-256 and decompresses to the recorded proof.

**Refresh.** `summarize.py` regenerates `summary.json` and these totals from the JSON-lines files. The rows above are the
final state of both runs.

## Scope

- Units not re-checked here or in `C2FINAL` §4–§5 rest on their records, as do the units of §4 and §5 not yet done.
  Each such record has a CNF hash that was rebuilt and matched (`C2FINAL` §3) and recorded verdicts of both checkers;
  its proof was deleted.
- Not re-checked here:
  - the encoder (`C2C34` §5);
  - the hull cover (`WRITEUP/CERTIFICATES.md`, central34-cover);
  - reductions A and B (`C2P/review`);
  - the Lean bookkeeping (`C2FINAL` §6).
- The split of the orbit closure into re-verified and recorded-only facts is in `C2FINAL` §9 (`AUDIT3` §5, row 3d).

## Reproduction

From `cloud/es7-2026-10-19/results`:

```sh
python3 C2RECHECK/summarize.py C2RECHECK/summary.json
python3 C2RECHECK/lists_check.py .
python3 C2RECHECK/hexcheck.py BASE C2C34/cubes.txt C2C34/logs/hex_cases.tsv ARCHIVE BIN WORK out.jsonl
REPRO_ARCHIVE=ARCHIVE python3 C2RECHECK/reproduce_local.py WORK BIN . out.jsonl $(cat C2RECHECK/local_units_1.txt)
```

- `BASE` is the base CNF written by `zcnf.py` as in `C2P/TASK.md`. The `reproduce*.py` scripts expect it as
  `WORK/base.cnf`.
- `BIN` holds `cadical`, `lrat-check` and `cake_lpr`, and `ARCHIVE` is a directory of `<unit>.lrat.zst` files.
- `summarize.py` and `lists_check.py` need only Python 3.
