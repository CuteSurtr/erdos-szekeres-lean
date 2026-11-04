# Sixfold 60-point model: exact rotation-specific obstruction and bounded refinement

4 November 2026, Asia/Seoul. The experiment began at 01:41:46 KST, with a hard deadline of 02:06:46 KST. The experiment finished at 02:04:45 KST, before the deadline. One compute process at a time; solver runs use one core, and the runner terminates its child if active + wired + compressed memory exceeds 29 GB. No certificate checker is launched by these scripts.

## Result on the archived model

**Exact computation + written proof (reviewed, not refereed).** The archived `gp_m6K8t10.cnf.model.json.zst` has no realization by a planar point set with the specified sixfold rotational action. A three-comparison biquadratic final polynomial already occurs on its two orbits numbered 0 and 3. This excludes that model, not all 60-point sixfold sets. It does not establish nonrealizability without the geometric rotation assumption.

**Exact computation.** Before reading the model, its compressed SHA-256 was checked against the archive's `SHA256SUMS`:

- Compressed model: `9365fc6c39e5b534c0712a1b9604b1c9b063121b2319ae3acc21c81c8309eb4c`.
- Decompressed model: `b0cde9d9e0ce5652211136d6443b91cbb7d261b601b5ff887a4273e834d14472`.
- Archived variable metadata: `f053fbdf5682ebb444f287ef52ec323d3e5d30214f17f8e12ef1f0087c921114`.
- Fresh base CNF: `ff10dafb31b009b50341d47edb3cdee2d6fd4d74b08b86285982867e8e4479ed`, 58,626 variables and 1,609,785 clauses.
- Initial accumulated GP clauses: `65010199babb8f6182004f89998b3bd35df917e05acab62b3cb1e71dbbc8ebbd`, 1,143,808 clauses. This file is not the complete GP family.

**Exact computation.** The search reconstructs all 5,710 triple-orbit IDs without importing the encoder, by lexicographically ordered minimal rotated triples. The separate verifier uses `C7UPPER/gen.py` and confirms every ID, the signs used in the witness, and the cancellation below. The search and verifier use integer arithmetic for these operations.

## The obstruction

**Written proof (reviewed, not refereed).** Write `[abc]` for the determinant orientation bracket and `a_v` for the absolute value of the canonical bracket represented by variable v. A Euclidean rotation preserves determinant values, hence identifies the magnitudes of rotated triples. Every bracket is nonzero in general position. For

`[abc][ade] − [abd][ace] + [abe][acd] = 0`,

the uniquely signed summand has greater absolute value than either of the other two. The archived model gives:

| Anchor quintuple `(a,b,c,d,e)` | Six signed orientation literals, in GP term order | Three summand signs | Strict comparison |
|---|---|---|---|
| `(0,2,4,22,23)` | `58,868,75,-72,76,-71` | `+,+,−` | `a71*a76 > a72*a75` |
| `(0,2,4,19,20)` | `58,751,72,-75,73,-74` | `−,+,−` | `a72*a75 > a73*a74` |
| `(0,2,4,18,21)` | `58,712,71,-76,74,-73` | `+,+,−` | `a73*a74 > a71*a76` |

Multiplying these three strict inequalities gives the same positive monomial on both sides, a contradiction. Equivalently the exponent vector of their product is exactly zero. The model assigns variables `58,71,72,73,74,75,76,712,868` true and `751` false, so the negation of this impossible pattern is the clause

```text
-58 -71 -72 -73 -74 -75 -76 -712 751 -868 0
```

**Scope.** This is a sound clause for configurations carrying the specified geometric rotation. A combinatorial automorphism of a chirotope alone need not preserve realizable bracket magnitudes; the clause must not be inserted into an unrestricted order-type encoding on this argument alone.

**Exact computation.** The witness is `m6_cycle_witness.json`, SHA-256 `e25599d3816e4d5ea94484633dde910afaa5f2a8404ec2c5ac164c0882689973`. `tests/verify_m6_cycle.py` checks it independently through encoder A, then tests every ordered pair of the certified 54-point set's nine orbits, all independent cyclic labels, and both mirrors: 5,184 tests, no forbidden pattern; 15,552 exact GP identities and 93,312 rotation-magnitude equalities. It also checks all triples of that point set are noncollinear. Arithmetic uses `(2 Re(z), 2 Im(z)/sqrt(3))`, which is an integer coordinate pair for the supplied cyclotomic weights; determinant signs therefore remain exact.

## Complete embedding families

**Written proof (reviewed, not refereed).** An injection of the source orbits into the target orbits, followed by a cyclic offset on each orbit and one common direction `+1` or `−1`, commutes with the rotation or its inverse. Thus it preserves all magnitude identifications used by the polynomial. Simultaneously reversing all required bracket signs preserves every GP summand sign. Each resulting impossible sign pattern yields a sound clause. `m6_embed_cycle.py` verifies the minority signs and exact exponent cancellation for every embedding before writing the family.

**Exact computation.** The two-orbit template yields 2,160 checked embeddings and 1,080 unique clauses. The complete family passes 20,736 exact54 tests, covering both cyclic directions, both global sign choices, every ordered orbit pair, all cyclic labels and both mirrors. Its clause-file hash is `634d5ff71d178454007b8d9929b4797aba1d7bf977854948cd490aa7c2345e46`.

**Exact computation + written proof (reviewed, not refereed).** A successor model produces another three-comparison polynomial on orbits 0,1,3. Its negated pattern is

```text
-58 -59 -61 -63 -72 -74 -76 -154 -255 -358 0
```

The separate verifier checks its three original GP identities, all 217,728 labelled three-orbit embeddings/mirrors of the exact54 set, 653,184 determinant identities, and 3,919,104 magnitude equalities. The witness hash is `dc0ee57705319f792d5005ea20266a7fe529d045f7b74b58b9f1a43714bb9e9c`. The complete three-orbit embedding family has 103,680 checked embeddings and 17,280 unique clauses, with 870,912 exact54 tests and no forbidden pattern. Its hash is `d772a179248c3e1fd93c775f7d69d43ee07dce0b23cb4cde89fb6dd3d34fb9f5`.

## GP refinement and interpretation

**Exact computation.** All two-orbit GP identities were also generated, using all sixteen forbidden sign assignments of each identity, then exact literal substitution, tautology deletion and deduplication. This gives 421,720 distinct clauses. Every clause passes six direct exact54 embeddings (2,530,320 tests total); all 142,560 GP identities on five-point subsets of each pair of actual orbits are checked separately by integer determinants. The family hash is `7e562dfcf17e41f322dd0b9e0e298256f94e428a50a542e07d06d26b8abebebe`.

**Evidence only (solver experiments).** The initial 12-round pilot took 66.681 seconds, adding 11 checked polynomial cuts and one checked GP-sign cut; every solve remained SAT. The complete two-orbit polynomial family remained SAT in 2.040 seconds. Both polynomial families together remained SAT in 5.595 seconds. Adding complete two-orbit GP remained SAT in 14.511 seconds. These models concern relaxations. In particular, an exhaustive replay of all 27,307,560 GP relations found 5,904 violations in the last of these models, motivating the bounded full-GP refinement recorded in `M6_STATUS.json` and the archived logs.

**Written proof (reviewed, not refereed).** Subsequent GP clauses use only the determinant identity: three nonzero summands cannot share a sign. `m6_gp_refine.py` confirms the reported source-model violations, derives all sixteen forbidden sign patterns, and checks every distinct emitted clause on six concrete exact54 embeddings. These clauses do not depend on a final polynomial.

**Limitations.** A directed product cycle is only a special case of a nonnegative dependency among GP comparison rows. Failure to find one does not establish realizability. Checks of the archived model's magnitudes concern its stated rotational action. A SAT answer after partial GP refinement does not even establish full GP consistency. No exact sixfold maximum follows from the two model obstructions alone; the maximum remains 54 or 60 unless an upper-bound certificate or a realizable 60-point construction is obtained.

## Final status

**Exact computation + written proof (reviewed, not refereed).** The original archived model was freshly checked against all 27,307,560 GP relations with zero violations. After nine additional GP-refinement solves, a successor model also passed all those relations and every one of its 3,277,941 CNF clauses. That model, hash `7d52dd0f74bbeb1f1ccf11a0777f8c02dcd8be8dda50f8540d9465e75b6c4e76`, nevertheless has a five-comparison rotation-specific polynomial on orbits 1,8,9. Its witness is `logs/m6_final_cycle_witness.json`, hash `7a72eaf9220fae89b4a98f460d1c09b4dab550897573fc884fc4a698db7f32c7`. Verification includes all 217,728 exact54 three-orbit embeddings, 1,088,640 determinant identities and 6,531,840 magnitude equalities. Thus two fully GP-consistent models were explicitly excluded by rotation-specific polynomial arguments in this experiment.

**Exact computation.** The five-comparison template yields 103,680 distinct clauses, with every embedding verified and 870,912 exact54 tests passing. Its family hash is `cdba6006a76c32009c439badc1d94878180a1dd8e237f32cc5901147e1303a50`. Across the three polynomial templates there are 122,040 family clauses. The final formula retains these, the complete two-orbit GP family, 84,256 additional GP-refinement clauses, and the 12 pilot clauses, along with the fresh base and original accumulated GP clauses.

**Exact computation; solver timing is evidence only.** The last solve remained SAT in 10.436 seconds. `m6_verify_assignment.py` independently verifies its assignment against all 3,381,621 clauses. The final model hash is `437144235bdaf2045f30767432d7453a2199bb608fee49257dfb51554db9789d`; its exhaustive GP replay has 2,640 violations. Refinement stopped at this point. There were 25 SAT solves, zero UNSAT verdicts, and no LRAT proof generated by this pilot. No realizable 60-point set or stronger upper bound was established. `M6_STATUS.json` contains the final formula/model hashes and exact check results.

**Resource record.** Peak observed active + wired + compressed memory across the monitored commands was 27.259 GB. The 29 GB termination guard never fired. Individual solver peak RSS was not separately recorded. All subprocess handles were waited to completion; each runner terminates and reaps its child on a limit. No process started by this subtask remains running.

## Reproduction and retention

**Exact computation.** The retained archive is `proof-archives/es8-c6c7-review-2026-11-04/m6/`. It contains all generated full CNFs, SAT models, polynomial witnesses, cut prefixes, complete embedding families, and exact-test metadata. Raw and zstd hashes, with decompression round-trip checks, are recorded in the manifest files. `archive_events.json` preserves the chronological prefix-cut archival events; `archive_manifest.json` identifies the final retained files and separate per-round cut prefixes.

From the results directory, with `MODEL`, `MAP`, `SCRATCH`, `ARCHIVE`, `BIN` and `GP_CHECKER` set to the intended local files:

```sh
python3 -I C6C7REVIEW/m6_product_cycles.py --model "$MODEL" --map "$MAP" --out "$SCRATCH" --max-layers 3 --max-seconds 90
python3 -I C6C7REVIEW/tests/verify_m6_cycle.py --model "$MODEL" --witness "$SCRATCH/m6_cycle_witness.json" --output "$SCRATCH/verified.json"
python3 -I C6C7REVIEW/m6_embed_cycle.py --model "$MODEL" --witness "$SCRATCH/m6_cycle_witness.json" --out "$ARCHIVE/embedding_family"
python3 -I C6C7REVIEW/m6_two_orbit_gp.py --out "$ARCHIVE/two_orbit_gp"
python3 -I C6C7REVIEW/m6_full_gp.py --model "$MODEL" --checker "$GP_CHECKER" --out "$SCRATCH/gpcheck" --max-output 100000
```

**Exact computation.** The full-GP checker is compiled from the unchanged `ROT456/tools/gpcheck.c`; source SHA-256 `2e425efed9e072963b36552e2565846d5ecc05952ce5b91e3cf065cd5be98ee9`. The default SDK caused a linker architecture error; selecting the installed 26.5 SDK allowed compilation. Checker binary SHA-256 is `7bb2e1535755438daeedb3dc68561abed94458945d87c2dedce9c53917a03c6c`. This is an ordinary exhaustive computation, not an LRAT certificate.
