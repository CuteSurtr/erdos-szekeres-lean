# C2FINAL: composition check of the central 34-point search

Local checks on an Apple M5 Pro, 1 November 2026 (UTC), over the run records on `es7-cloud` at a15dd2ce3.

**Status.** Every piece of the case split is accounted for and every recorded CNF hash matches a rebuilt CNF. The
statement "every centrally symmetric set of 34 points in general position contains a convex 7-gon" is **not yet
claimed**: an independent review and the random re-solve sample (§5) are still open.

## 1. The chain being checked

1. **Base formula.** `SYMZ/zcnf.py rot 17 7 --m 2 --hull` (the encoder was reviewed in `C2C34` §5).
2. **Hull cover.** The 136 hull cubes cover the base (`WRITEUP/CERTIFICATES.md`, central34-cover).
3. **Hexagonal hulls.** All 120 cases are UNSAT with archived proofs (`C2C34` §3).
4. **Parallelogram hulls.** Case P_a and P_(17−a) are equivalent (reduction A, reviewed in `C2P/review`), so P1..P8
   suffice. Each case is split at the second layer into 560 subcases with a certified cover, and the reflection
   i ↦ (a − i) mod 17 (reduction B, same review) pairs the subcases into 287 orbits.

## 2. Independent recount (`recount.py`, `recount.json`)

- **Records.** 2,492: 2,424 from the waves `C2P`..`C2P5` and 68 from the P8 pilot (`C2C34/logs/p8_units.tsv`).
  - 2,385 UNSAT, 107 UNKNOWN (time limit), 0 SAT, 0 errors.
  - No record's `certified` field disagrees with its verdict strings.
- **Cases.** For each of P1..P8, the script derives the 560 subcases and the orbits itself:
  - 287 orbits, 14 of them fixed;
  - 287 closed, where an orbit counts as closed only through a record with status UNSAT, lrat-check `c VERIFIED` and
    cake_lpr `s VERIFIED UNSAT`;
  - the cover of the 560-way split is certified.
- **Not used.** The script does not read `C2P3/check_case.py` or the `certified` field.

## 3. Regeneration and hash matching (`hashmatch.py`, `hashmatch.json`)

- **Inputs rebuilt.**
  - Base: `p cnf 838032 16653336`, SHA-256 `b0061e90…`, map `2476faff…` (23 s).
  - `C2C34/cubes.txt` (136 hull cubes): byte-identical.
  - `C2P/cubes/P1..P8_cubes.txt`: byte-identical.
  - The pilot's P8 cube file: byte-identical.
  - The hull cover CNF: SHA-256 `bb60facb…`, as recorded in `WRITEUP/CERTIFICATES.md`.
- **Unit CNFs.** Every lane builds a unit CNF as the base with the header clause count raised by n, followed by n
  extra clauses. The script rebuilds the SHA-256 of each record's CNF in this way.
  - Result: **2,589 of 2,589 recorded hashes match** (120 hexagonal cases, 61 pilot rows, 2,408 wave rows), 0
    mismatches.
  - Third-layer pieces (16 records) are skipped; they close no orbit.
- **Controls.**
  - A unit CNF written to disk and hashed with `shasum` gives the recorded hash.
  - Flipping one literal, or dropping one clause, changes the hash.

## 4. The pilot gap and its re-solve (`pilot/`)

**The gap.** Seven pilot records had no CNF hash: `P8_cover` and the subcases `P8_1-3`, `P8_2-4-11`, `P8_2-12-15`,
`P8_3-4-5`, `P8_3-4-15` and `P8_9-13-15`. Six P8 orbits and the P8 cover rested only on them, and their proofs had been
deleted.

**The re-solve.** `pilot/resolve.py` handled all seven, one process at a time.
- It rebuilds each CNF exactly as `C2P/tools/lane.py` does, and requires the expected hash.
- It solves with CaDiCaL 3.0.1 `--lrat` and checks the proof with lrat-check and cake_lpr.
- It archives the proof with zstd (local archive `es7-central34-pilot-resolve-2026-11-01`, outside Git), checking that
  decompression reproduces the proof hash.

| unit | solve s | proof GB | lrat-check | cake_lpr | same proof as pilot |
|---|---|---|---|---|---|
| P8_3-4-5 | 17.3 | 1.11 | VERIFIED | VERIFIED UNSAT | yes |
| P8_cover | 242.0 | 4.65 | VERIFIED | VERIFIED UNSAT | no (clause order, below) |
| P8_9-13-15 | 31.4 | 1.97 | VERIFIED | VERIFIED UNSAT | yes |
| P8_3-4-15 | 60.9 | 3.18 | VERIFIED | VERIFIED UNSAT | yes |
| P8_2-12-15 | 82.9 | 3.30 | VERIFIED | VERIFIED UNSAT | yes |
| P8_2-4-11 | 99.8 | 3.35 | VERIFIED | VERIFIED UNSAT | yes |
| P8_1-3 | 213.5 | 3.93 | VERIFIED | VERIFIED UNSAT | yes |

- **Identical proofs.** For the six subcases the proof SHA-256 equals the one recorded by the pilot. CaDiCaL is
  deterministic, so this ties those pilot records to the rebuilt CNFs.
- **The cover.** The pilot's `p8/mkunits.py` wrote the 560 subcase clauses in sorted name order, while `lane.py` writes
  them in cube-file order. The clauses are the same, the bytes differ. The re-solved cover (CNF `8851e2ac…`) now has a
  hash and an archived proof.

## 5. Proof reproducibility and the random re-solve sample (`sample/`)

**Reproducibility.** Two units solved on the x86_64 cloud machines were re-solved on the ARM Mac: `P6_7-8-9` (record
`C2P/M02`) and `P2_7-9-10` (`C2P5/M97`). Both gave a proof with the recorded size and SHA-256, and both checkers
accepted it. Every deleted proof can therefore be regenerated from its CNF and recognized by its recorded hash.

**Random sample.** `sample/sample.txt` lists 24 units drawn before any result was seen:
- seed 20261101;
- two hexagonal (H) units and one quadrilateral (Q) unit per case;
- cloud records only.

`sample/reproduce.py` re-solves each unit (CNF hash checked, proof compared with the record, both checkers, archived
proof). `sample/out.jsonl` holds the results, the first two lines being the reproducibility test. **This sample was
still running at the time of this commit.**

## 6. Lean check of the bookkeeping (`Central34Orbits.lean`, `gen_lean.py`)

**The data.** `gen_lean.py` writes the closed subcases of each case as Lean lists. A subcase is included only through a
record that is certified and hash-matched, or through a §4 re-solve whose CNF hash equals the expected one.

**The theorems.** Core Lean 4.24.0, `decide +kernel`, axioms `propext` only, about 6 s:
- `subcases_reflection`: each case has 560 subcases, and the reflection maps subcases to subcases and is an
  involution, giving 287 orbits with 14 fixed;
- `closed_are_subcases`: every listed subcase is a genuine subcase of its case;
- `all_cases_closed`: every orbit of P1..P8 has a closed member.

**Control.** Removing one entry of a case's list makes `decide` fail.

**Scope.** The file checks the combinatorics only. It does not check the SAT records, the encoding, the covers, or
reductions A and B themselves.

## 7. Literature (1 November 2026)

No matching prior result was found in the sources inspected:
- Subercaseaux–Mackey–Qian–Heule, arXiv:2506.00224v1. It searched only 4-fold symmetry at 32 points, its conclusion
  lists a 2-fold 32-point realization as open, and it makes no claim about 34 points.
- Bogdan, arXiv:2512.24061v1: no symmetric point-set results ("symmetry" there means symmetry breaking).
- The Mackey thesis listing (CMU-CS-25-108; abstract only, the PDF was unreachable): 16-point hexagon-free sets with 3-,
  4- and 5-fold rotation.
- The survey `LIT/RELATED.md` with its 42 searches, and four new searches.

This is not a novelty claim.

## Reproduction

From `cloud/es7-2026-10-19/results`, with the base written by `zcnf.py` as in `C2P/TASK.md`:

```sh
python3 C2FINAL/recount.py . recount.json
python3 C2FINAL/hashmatch.py /path/to/base.cnf . hashmatch.json
python3 C2FINAL/gen_lean.py . hashmatch.json Central34Orbits.lean a15dd2ce3 C2FINAL/pilot/out.jsonl
lean Central34Orbits.lean      # Lean 4.24.0, no Mathlib needed
```
