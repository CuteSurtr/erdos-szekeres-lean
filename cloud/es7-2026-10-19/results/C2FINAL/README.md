# C2FINAL: composition check of the central 34-point search

Local checks on an Apple M5 Pro, 1 November 2026 (UTC), over the run records on `es7-cloud` at a15dd2ce3. README revised
later the same day: the random sample is complete and the statement is claimed. Paths are relative to
`cloud/es7-2026-10-19/results`.

**Statement (claimed; computer-assisted).** Every centrally symmetric set of 34 points in general position contains a
convex 7-gon. Pairs can be deleted, so every centrally symmetric set of at least 34 points does, and the largest
centrally symmetric set without a convex 7-gon has exactly 32 points (`SYM2/sym7_32points.txt`).

**Status.**
- Every piece of the case split is accounted for, and every recorded CNF hash matches a rebuilt CNF (§2–§3). The orbit
  bookkeeping is Lean-checked (§6). An independent review (§8) found no blocking error.
- The random re-solve sample (§5) is complete: 24 of 24 units certified, 23 of them with byte-identical proofs;
  `P8_1-10` gave a different proof, accepted by both checkers. A second draw of 8 units: 8 of 8 reproduced.
- The encoder has a written soundness proof, refereed on 1 November: sound, with minor documentation gaps (§1).
- The hull cover and the 120 hexagonal hulls have retained proofs. Most parallelogram pieces rest on recorded verdicts:
  both checkers accepted the proof at solve time, and the proof was then deleted. The re-checks started on 1 November
  are in §9: by 1 November 2026, 19:43 UTC, 224 of the 2,304 cover and orbit facts had a re-solve on a hash-checked
  CNF with both checkers.

## 1. The chain being checked

1. **Base formula.** `SYMZ/zcnf.py rot 17 7 --m 2 --hull`. Soundness: written proof, refereed (below).
2. **Hull cover.** The 136 hull cubes cover the base (`WRITEUP/CERTIFICATES.md`, central34-cover).
3. **Hexagonal hulls.** All 120 cases are UNSAT with archived proofs (`C2C34` §3).
4. **Parallelogram hulls.** Case P_a and P_(17−a) are equivalent (reduction A, reviewed in `C2P/review`), so P1..P8
   suffice. Each case is split at the second layer into 560 subcases with a certified cover, and the reflection
   i ↦ (a − i) mod 17 (reduction B, same review) pairs the subcases into 287 orbits. `AUDIT3` (A5) checked both
   reductions at the CNF level: each relabelling maps every base clause into the base plus the hull clauses of the case.
5. **Relative covers** (added 1 November; referee finding R1). The cover CNF of case P_a is the base, the hull cube Q of
   P_a as units, and one clause ¬(L_i ∖ Q) per subcase (`C2C34/p8/mkunits.py`, `C2P/tools/lane.py`). Its
   unsatisfiability means that every labelled real configuration in the class of Q lies in the class of some Q ∧ L_i.
   This follows in one line from the base theorem below; dropping the literals of Q from each ¬L_i is equivalent under
   the units of Q.

**The encoder proof** (`C2ENC`; refereed versions `proof.md` `ae379b45…`, `perturbation.md` `28fbbd6a…`,
`class_table.md` `d7d7c9fc…`; revised versions in `C2ENC/SHA256SUMS`). Its base theorem: for every centrally symmetric set of 34 points in general position
without a convex 7-gon and every vertex p0 of its hull, the normal-form labelling from p0 exists and is unique, and its
real assignment satisfies every clause of the base `b0061e90…`. Hence an UNSAT cube has an empty class, and a certified
cover places every labelled configuration in the class of some cube. No perturbation of the centre is needed: by
general position the only collinear triples through c are {c, p, −p}. Evidence with it: a generator written from the
proof matches the base family by family, exact evaluation of real labellings, and mutation tests.

**Referee (1 November).** Sound, with minor documentation gaps; no blocking or major finding. The referee listed the
clause families from the code before reading the proof (they add up to the header's 16,653,336 clauses), re-derived
every lemma, re-ran the tests, added nine mutants (every unsound one caught; one equivalent mutant explained) and two
evaluators of its own, one of them on the full base. Findings: R1 (minor), relative covers, now step 5; notes R2–R8: a
test description claims clause identity where the script compares counts (R2), an incomplete reason in Lemma 8 (R3),
the specification script shows coverage, not an independent derivation (R4), a union-find branch that is dead at these
sizes (R5), two small slips (R6), an informal identification of the Lean notions (R7), and a count that can be misread
(R8). The fixes are applied in `C2ENC` (its §4): R1 as Corollary 3′, R2, R3, R4, R6 and R8 by text changes; R5 and R7
need none.

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
- **Local records.** 60 orbit facts and the covers of P1–P5 rest only on records of the local Mac lanes
  (`C2P*/LOCAL*`), which keep no record of the tools used (`AUDIT3`, A8). Their re-solve on hash-checked CNFs is in §9
  (44 of 65 by 1 November 2026, 19:43 UTC).

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
  - The case of each record is read from its unit name, not from the record. `hashmatch.json` lists, per unit, the
    recorded hashes that were rebuilt and matched.
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
accepted it. Reproduction is not guaranteed in general: `P6_1-7` has the same CNF (`11dbd566…`) in `C2P4/M00` and
`C2P4/LOCAL` but two different proofs (5,818 s on the cloud, 3,989 s on the Mac), both accepted by both checkers. A
re-solve whose proof differs from its record is still checked afresh by both checkers.

**Random sample.** `sample/sample.txt` lists 24 units drawn before any result was seen:
- seed 20261101;
- two hexagonal (H) units and one quadrilateral (Q) unit per case;
- cloud records only (the local Mac records are covered in §9).

`sample/reproduce.py` re-solves each unit (CNF hash checked, proof compared with the record, both checkers, archived
proof). `sample/out.jsonl` holds the results, the first two lines being the reproducibility test.

**Result (complete on 1 November, 12:58 UTC).**
- Main sample: 24 of 24 units finished (16 H, 8 Q). In all 24 the rebuilt CNF has the recorded hash and both checkers
  accept the re-solved proof. 23 proofs have the recorded size and SHA-256. `P8_1-10` (record `C2P2/M02`, CNF
  `163f52ea…`) gave a different proof, 9,952,275,647 bytes, SHA-256 `e98aa3ee…` (solve 2,978 s against 5,935 s
  recorded).
- The units `P6_9-11`, `P7_1-15` and `P8_1-10` were not reached at a first stop at 09:10 UTC and were finished later the
  same day; their lines are the last three of `sample/out.jsonl`. They were run with the present `sample/reproduce.py`,
  which adds two options to the first version: `REPRO_CAP` overrides the 3,600 s solve cap, and cake_lpr is retried with
  an 11,000 MiB heap if 8,000 MiB is exhausted. Neither changed these runs: all three solved within 3,600 s, and
  cake_lpr passed at 8,000 MiB (the extra field `cake_heap_mb`).
- Extra sample (`extra_sample.txt`, seed 20261102, one more H unit per case, drawn before any result was seen): 8 of
  8 finished, all reproduced and accepted by both checkers (`extra_out.jsonl`).
- Proofs are archived with zstd round trips in the local archive `es7-central34-resample-2026-11-01`.

## 6. Lean check of the bookkeeping (`Central34Orbits.lean`, `gen_lean.py`)

**The data.** `gen_lean.py` writes the closed subcases of each case as Lean lists. A subcase is included only through a
certified record whose (unit, CNF hash) pair `hashmatch.py` rebuilt and matched, or through a §4 re-solve whose CNF hash
equals the hash `hashmatch.py` computed for that unit. The case is read from the unit name.

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
- B. C. Dumitru, arXiv:2512.24061v1: no symmetric point-set results ("symmetry" there means symmetry breaking). It has
  only v1; his homepage announces a second version.
- The Mackey thesis (CMU-CS-25-108), read in part (abstract, contents, §3.1, §3.2.4, chapter 4, full-text search):
  searches for 16-point hexagon-free sets with 3-, 4- and 5-fold rotation (the threefold formula is unsatisfiable,
  §3.2.4), and a fourfold 32-point attempt that reached realizations with at most 24 points.
- Krapivin–Przybocki–Heule, "Toward Satisfiability Modulo Realizability", arXiv:2607.02958v1 (July 2026): no symmetry
  imposed, no nonrealizability certificates, no 34-point case; its 32-point search found no realization among 200,000
  abstract solutions.
- Koshelev–Koshka, arXiv:2604.20120v1 (April 2026): other Erdős–Szekeres variants, no symmetric 7-gon results.
- Zeng–Liu–Ratnavelu–Ong, SSRN 7334758 (August 2026, read through a cached copy): a SAT encoding for 33 points, no
  symmetric construction. Schroeder, Zenodo 22842891 (September 2026, text search): upper bounds only.
  Georgiev–Gómez-Serrano–Tao–Wagner, arXiv:2511.02864 (Problem 6.58): 2^(k−2)-point constructions for k ≤ 8, no
  symmetry stated. Baek, Eur. J. Combin. 124 (2025) 104085: no symmetric sets.
- The survey `LIT/RELATED.md` with its 42 searches, four further searches, the arXiv full-text search for
  "Erdős–Szekeres" (2026 entries), the 2025–2026 publication list of B. Subercaseaux, the 2025–2026 files of M. Heule,
  and citation searches (OpenAlex, Semantic Scholar). The Morris–Soltan survey does not mention symmetry (an earlier
  version of this list said it records symmetric constructions).
- Not inspected: the CICM proceedings version of arXiv:2506.00224, the journal version of Baek–Balko, journal databases
  behind paywalls, and sources not in English.

The 32-point example follows from Valtr's construction as described by Baek and Balko (SoCG 2025, Lemma 14, §6.1).
This is not a novelty claim.

## 8. Independent review (1 November 2026)

An adversarial review, run separately and given the code and claims but not the authors' reasoning, used its own
scripts (`review/`). It ran no solver or checker. **No blocking error.**

**Checked and found correct.**
- Completeness of steps 1–5: hull and second layer have 4 or 6 vertices; the centre is not in the set; P_a and P_(17−a)
  pair without fixed points; 34 points imply all larger sizes. Exact tests on 1,500 real sets and 6,000 labellings:
  hull cubes, reduction A, second-layer cubes (1,704/1,704) and reduction B (1,704/1,704) agree with the geometry.
- Cover shape: every subcase cube contains its hull cube and has 53 or 78 further literals.
- Own recount of all 2,492 records, own regeneration of all 136 hull cubes and the eight cube files (byte-identical),
  own rebuild of all 2,589 + 7 CNF hashes, and 35 hashes rebuilt with the lanes' own awk and `shasum` pipeline.
- The Lean file: theorems as stated, not vacuous (`uncovered a []` has 560 entries), controls fail as they should.
- Encoder sanity: 13,012,616 base clauses over triple variables hold on 160 real labellings.

**Findings and their resolution.**
1. *Major*: the claim waits for the random sample (§5). Resolved: the sample is complete (24 of 24), and the
   statement is claimed.
2. *Minor*: for the 120 hexagonal cases and 58 P8 orbits, cake_lpr ran on a CNF rebuilt by the same awk command but not
   hashed (`C2C34/hchecker.sh`, `C2C34/p8/checker.sh`); lrat-check ran on the hashed file. Both sets were re-checked on
   hash-checked files (§9): 120 of 120 and 58 of 58.
3. *Minor*: proofs are not always reproducible (`P6_1-7`). §5 corrected.
4. *Minor*: `gen_lean.py` treated any record with a hash as matched, took the case from the record and had a no-op
   assertion; `hashmatch.py` took the case from the record. Both fixed; the regenerated Lean file is byte-identical.
5. *Minor*: the raw hull-cover logs were not in the repository. They are now in `evidence/central34-cover/` (build-host
   line removed). The raw hexagonal lane records were not kept; only `C2C34/logs/hex_cases.tsv` and the proofs exist.
6. *Minor*: `C2C34/README.md` and `WRITEUP/SYMMETRIC.md` described the parallelogram cases as open. Updated on
   1 November.

## 9. Re-checks started on 1 November

Counts as of 1 November 2026, 19:43 UTC; two jobs were still running. Scripts and records: `C2RECHECK`.

| check | units | method | result |
|---|---|---|---|
| hexagonal hulls on hash-checked files | 120 | rebuild each case CNF; require the recorded CNF, archive and proof SHA-256; lrat-check and cake_lpr on exactly these files | 120 of 120: all hashes equal, both checkers accept (cake_lpr heap 8,000 MiB); finished 17:59 UTC |
| P8 pilot orbits | 58 | re-solve on a CNF with the recorded hash; compare the proof with the record; both checkers; archive `es7-central34-pilot-orbits-2026-11-01` | 58 of 58 certified, all 58 proofs byte-identical to the records; finished 17:33 UTC |
| orbits and covers on local records only | 60 + 5 | as for the pilot orbits; archive `es7-central34-local-2026-11-01` | 44 of 65 (running): all certified, all byte-identical to the records |
| lane spot check (`AUDIT3` §5 row 8) | 242, one per lane not already reached by a re-solve (`C2RECHECK` §5) | as for the pilot orbits; archive `es7-central34-lanespot-2026-11-01` | 81 of 242 (running), from 81 lanes: all certified, all byte-identical to the records |
| retained certificates (cover and others) | | replay with hash-bound logs (`WRITEUP/CERTIFICATES.md`, `REPLAY`) | both checkers accepted L1, the C4CUT proof and the two c3hex proofs; not run on the cover, `mirror33`, `mirror34`, P1 or L2 |
| independent pass over these outputs | | own hashes of the archives written in these re-checks; orbit closure split into re-verified and recorded-only facts | closure split counted from the run records (below); the new archives were hashed only by the jobs' own round trips |

**Closure split** (by 1 November 2026, 19:43 UTC). Of the 2,304 facts the case split needs (8 covers and 8 × 287
orbits), 224 (9.7%) have a re-solve on a CNF with the recorded hash, accepted by both checkers, with an archived proof:
6 covers (P1–P5, P8) and 218 orbits (P1 18, P2 19, P3 23, P4 20, P5 28, P6 17, P7 16, P8 77). They come from the
pilot re-solve (7 units, §4), the reproducibility test and the samples (34, §5), the pilot orbits (58), the
local-record units (44) and the lane spot check (81); each unit closes a different fact. The other 2,080 rest on
recorded verdicts. `closure_split.py` maps unit names to orbits as `recount.py` does and counts the facts.

## Reproduction

From `cloud/es7-2026-10-19/results`, with the base written by `zcnf.py` as in `C2P/TASK.md`:

```sh
python3 C2FINAL/recount.py . recount.json
python3 C2FINAL/hashmatch.py /path/to/base.cnf . hashmatch.json
python3 C2FINAL/gen_lean.py . hashmatch.json Central34Orbits.lean a15dd2ce3 C2FINAL/pilot/out.jsonl
lean Central34Orbits.lean      # Lean 4.24.0, no Mathlib needed
python3 C2FINAL/sample/reproduce.py <work dir holding base.cnf> <dir with cadical, lrat-check, cake_lpr> . out.jsonl P6_9-11@C2P3/M31
python3 C2FINAL/closure_split.py --until 2026-11-01T19:43:14Z C2FINAL/pilot/out.jsonl C2FINAL/sample/*out.jsonl <C2RECHECK records>
```

The last line re-solves one sample unit; set `REPRO_ARCHIVE=<dir>` to keep the proof.
