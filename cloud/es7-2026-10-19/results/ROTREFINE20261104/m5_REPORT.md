# Fivefold algebraic refinement, 4 November 2026

The fivefold threshold remains unresolved: no upper-bound certificate was produced. The campaign retained an exactly verified obstruction beyond GP signs and directed product cycles: a twelve-layer abstract model passes every GP sign relation and the complete directed product-graph test, but violates an eight-bracket identity forced by geometric fivefold rotation. Six product families, four linear-identity families, a complete GP sign-template family, and sixteen GP-refinement batches were validated and tested. All SAT results are abstract assignments; no point realization is claimed.

## First retained abstract model and product contradiction

**Exact computation:** the twelve-layer base regenerated with SHA-256 `10d36965f5b50a30bb61895f5c82d4398cbbc71f0c2b94a45d8b863ecb8ab96a`. CaDiCaL returned SAT in 15.045 seconds wall time. A separate streaming assignment checker accepted every one of its 2,354,156 clauses. The retained positive-variable model has SHA-256 `81a0e98b89b621df2ca9f3a04b28eeeb85c3b8a4dc58d88f8dac8e5705abb321`. This is an abstract model, not a geometric construction.

**Exact computation:** all 66 two-orbit restrictions were searched, covering 16,632 rotation-representative GP identities. There was no GP sign violation or directed product cycle in that restricted search, including the union of its 33,024 product-comparison edges. A three-orbit scan found GP sign violations, so the model is not claimed to be a uniform chirotope. A second scan skipped invalid GP identities and used only valid minority-sign comparisons; it found a four-comparison product cycle on orbits 0, 1, and 8. Invalid identities supply no edge in this search.

**Written proof (reviewed, not refereed):** for signed area brackets, the determinant identity

`[abc][ade] - [abd][ace] + [abe][acd] = 0`

implies that a uniquely signed, nonzero summand has magnitude strictly larger than either other summand. General position supplies nonzero brackets. The specified rotation preserves determinant magnitudes, so brackets in one triple orbit have equal magnitude. These facts give the cycle `A > B > C > D > A`, where

| Product | Definition |
|---|---|
| `A` | `abs([0,1,44][0,2,9])` |
| `B` | `abs([0,1,7][0,2,41])` |
| `C` | `abs([0,2,6][0,1,42])` |
| `D` | `abs([0,1,9][0,2,44])` |

The four anchor quintuples are `(0,1,3,7,44)`, `(0,2,4,6,41)`, `(0,1,3,9,42)`, and `(0,1,2,9,44)`. The first three identities have signed-term pattern `(+,+,-)`; the fourth has `(+,-,+)`. Exact exponent cancellation verifies the contradiction. It excludes the model from realization with the prescribed fivefold action; it does not assert nonrealizability without that prescribed symmetry, and it is not asserted independent of every possible GP-sign consequence.

**Exact computation plus written determinant proof:** two distinct symbolic implementations accepted the witness. `m5_algebra.py` reconstructs signs with encoder A; `tests/check_product_symbolic.py` independently reconstructs the rotation orbits and variable numbering without importing the cycle-search implementation. See `m5_cycle00.json`, `m5_cycle00_verified.json`, and `logs/m5_product_independent.json`. The witness SHA-256 is `6ea08397ef94c6cc01bebb58331017385cd146fa11f42d56a4dc7f272e2320ae`.

## Sign pattern, map binding, and lifted family

**Exact computation:** all fourteen canonical brackets used by the first witness have positive signs in the source model. With twelve-layer variable numbers, their forbidden conjunction yields

```text
-1 -2 -5 -7 -40 -42 -59 -62 -94 -97 -201 -256 -355 -357 0
```

The same geometric point IDs in the thirteen-layer map give

```text
-1 -2 -5 -7 -40 -42 -64 -67 -99 -102 -216 -276 -385 -387 0
```

Variable numbers are not reused between dimensions. `m5_map_binding.json` records canonical-map fingerprints and both clauses. The twelve-layer generator metadata hash is `448e87642f0b2932441ed23f002df03e145e01f82326833a730bb2bed00400c1`; the thirteen-layer metadata hash is `28a9dd26ae7c74c9b58170284d50212d677c09a2750e26be178c15386167da10`. The generator hash is `4564e7f0ff1d3794917414002b4847cca6f0753420bd806af9d107f2a361bace`.

**Written proof (reviewed, not refereed):** an injective map of source orbits to target orbits, with an independent phase-index shift for each orbit and one common direction choice, sends rotation to rotation or its inverse. Consequently all GP identities and magnitude equalities in the proof persist. A simultaneous reversal of all bracket signs leaves the GP product signs unchanged. Negating each transformed impossible sign conjunction therefore gives a sound clause. One common phase shift can be fixed to zero because simultaneous rotation preserves orientations. No nesting, phase-order, or reflection-breaking assumption is used in this cut argument.

**Exact computation:** the first template gives 132,000 distinct clauses at twelve layers and 171,600 at thirteen layers, enumerating all orbit injections, all relative phase shifts, both common directions, and both bracket-sign reversals. The thirteen-layer clause-family SHA-256 is `acfb0a5499559fe0aa5629d4cc2ca352b7da4ede08389ecfd4e510590870952b`.

## Exact validation on the 56-point example

**Exact computation:** the certified fivefold example is evaluated in integer `Z[zeta_5]` arithmetic using the sign of `A+B sqrt(5)`, decided by integer squared comparisons. The centre is removed for the encoder comparison. All 26,235 triples of the remaining 55 points are noncollinear. The exact orientation table is bound to source hash `4cdd24bbeaa56d437420b1d1f63ca5ecb0fba64482ceb78ba6f1f7a496cf3387` and has table hash `2a780b6ce4bf794eee1893dc557260f53bff2c65e87027ab077c63a61ba0ffed`.

**Exact computation:** the first template was tested on every injection of its three source orbits into eleven actual orbits, all relative shifts, both directions, and both sign reversals: 99,000 tests, zero forbidden-pattern matches. Every emitted thirteen-layer clause was also tested directly on three actual orbit selections and both reflected signs: 1,029,600 direct clause tests, all passed. The twelve-layer family has analogous complete tests. The finite tests check implementation; the determinant and rotation argument supplies universal soundness.

## Experiment protocol and retained artifacts

**Written proof (reviewed, not refereed):** only the established odd-order reflection unit `H(1)` is used as a global symmetry-breaking unit. Reflection sends `theta_1` to `2pi/5-theta_1`, exchanging its two open half-sectors after generic perturbation. Its exact toggle on the 56-point example and mirror was checked in the preceding campaign. `d111111` is an explicitly identified phase-order cube, not an extra global assumption; conclusions from it alone do not cover all phase orders.

**Evidence only:** the initial matched experiment uses the same binary and 180-second real-time limits on `H1+d111111` with and without the verified family. A separate twelve-layer CEGAR lane seeks further product templates. Every accepted template must pass the independent symbolic checker, encoder-map checker, exact 56-point tests, and the declared family-lifting checks before insertion. SAT assignments are independently checked against their retained CNF; full GP consistency is not inferred from SAT. Every proof artifact, formula, and model is retained in the campaign archive with raw/compressed SHA-256 and a verified decompression round trip.

Commands are reproduced with local `ARCHIVE` and `BIN` variables; all computation uses one solver at a time and a 29 GB total-memory guard. No `cake_lpr` process is launched by this lane. An UNSAT pilot would be reported immediately for a retained LRAT rerun and both checkers before any certificate claim.

**Evidence only: matched first-family pilot.** Both runs reached their 180-second limits with UNKNOWN. The cut family did not yield a completion in this pilot. Conflict and propagation counts are activity measurements and do not establish a speedup or progress toward a contradiction.

| Thirteen-layer cube | Wall seconds | CPU seconds | Conflicts | Propagations | Peak RSS, decimal GB |
|---|---:|---:|---:|---:|---:|
| `H1+d111111` | 180.476 | 179.096 | 534,294 | 737,039,666 | 2.236 |
| Same cube + first product family | 180.518 | 178.841 | 549,013 | 746,585,449 | 2.495 |

**Exact computation:** baseline-cube SHA-256 is `ef4c7dad8109a760d6f07fe9b098c20394e2dc613607ad3536df8b60a1fb4b58`; strengthened-cube SHA-256 is `3df646b13a529555ea1af51254a9a1b17c7f5ce9c826a93218b8ee9489b419c2`. Fresh base, cube, family, and source-model hashes are retained in the archive manifests and assembly metadata. No memory guard fired in these two runs; their highest observed total active + wired + compressed memory was 28,055,617,536 bytes.

```sh
python3 -I ROTREFINE20261104/m5_lane.py --archive "$ARCHIVE" --generate 12
python3 -I ROTREFINE20261104/m5_lane.py --archive "$ARCHIVE" --bin "$BIN" \
  --file m5K8t12.cnf --name t12_plain --seconds 180
python3 -I ROTREFINE20261104/m5_product_cycles.py \
  --model "$ARCHIVE/t12_plain.model.json" --map "$ARCHIVE/m5K8t12.cnf.json" \
  --out "$ARCHIVE/m5_scan02" --max-layers 3 --max-seconds 120 --skip-invalid-gp
python3 -I ROTREFINE20261104/m5_algebra.py verify --archive "$ARCHIVE" \
  --model "$ARCHIVE/t12_plain.model.json" --witness ROTREFINE20261104/m5_cycle00.json \
  --output ROTREFINE20261104/m5_cycle00_verified.json
python3 -I ROTREFINE20261104/m5_algebra.py lift --archive "$ARCHIVE" \
  --verified ROTREFINE20261104/m5_cycle00_verified.json --layers 13 \
  --output "$ARCHIVE/m5_family00_t13.clauses"
```

## Further retained product templates and affine interiority

**Exact computation:** six product templates were retained. Each has a separate witness, encoder-map verification, independent symbolic verification, exhaustive template embeddings on the 55 noncentral example points, and a direct test of every emitted clause. The search uses only valid minority-sign GP identities for its product-comparison edges. Models may still violate other GP identities.

| Template | Comparisons | Literals | Source orbit support | Twelve-layer clauses | Thirteen-layer clauses |
|---|---:|---:|---|---:|---:|
| `00` | 4 | 14 | 0, 1, 8 | 132,000 | 171,600 |
| `01` | 5 | 15 | 0, 1, 2 | 132,000 | 171,600 |
| `02` | 3 | 11 | 0, 2 | 2,640 | 3,120 |
| `03` | 6 | 20 | 0, 1, 8 | 132,000 | 171,600 |
| `04` | 5 | 14 | 0, 1, 10 | 132,000 | 171,600 |
| `05` | 4 | 14 | 0, 1, 2 | 66,000 | 85,800 |

**Written proof (reviewed, not refereed):** the ordinary affine identity

`[abc] - [abd] + [acd] - [bcd] = 0`

forbids the two sign assignments in which its four nonzero signed terms have a common sign. This is a general affine constraint, not a consequence specific to fivefold symmetry. An exact rational-block diagnostic found the instance on points `(0,10,12,26)`, yielding the twelve-layer clause `-374 388 -483 2983`. That diagnostic motivated adding the complete standard family.

**Exact computation:** `m5_interiority.py` enumerates rotation representatives of every four-subset, emits both clauses, removes tautologies, and deduplicates. It produces 195,030 clauses at twelve layers and 270,790 at thirteen layers. Every emitted clause was tested on three orbit selections, three relative phase patterns, and both mirrored signs: respectively 3,510,540 and 4,874,220 direct tests. All 341,055 four-subsets of the actual 55 points also passed the sign relation. The thirteen-layer family hash is `65620047857e3dcd314c2779d6aeff3dffb5bd450a1944b5ce7ad66b222173ac`.

## Exact linear identities over the real pentagon field

**Written proof (reviewed, not refereed):** a linear identity whose coefficients are real algebraic numbers gives a forbidden orientation conjunction whenever the corresponding signed coefficients are all strictly positive. Formal expansion treats each orbit seed as two independent real variables. Thus it proves an identity for arbitrary seeds, with no geometric ordering or nesting assumption. Injective orbit substitutions and independent phase shifts remain valid; conjugation supplies the inverse-direction case and reverses every bracket sign. Global sign reversal also preserves a homogeneous zero identity.

**Exact computation:** the first retained identity is

`(5-sqrt(5))*[0,50,53] - 2*sqrt(5)*[0,51,52] + (5-sqrt(5))*[50,51,53] = 0`.

Its required source signs are `(+,-,+)` and its source-model cut is `-1555 1562 -6822`. Both weights are strictly positive. The same-orbit literal is retained in the family; no simplification from an unstated geometric fact is performed. The witness `m5_linear00.json` has hash `36b585fcd66266a3a0b03c0d53bb42faa403c8a56b8a303eefed88c18a9e9e8a` and is bound to model `40494397cc15b81e61ed8dacb2818e6377ab074c3ae97912dc906c67e505b028`.

**Exact computation:** two independent formal expansions verify this identity: a determinant expansion over `Q(sqrt(5))`, and `m5_linear_geometry.py`, which expands `conj(q-p)*(r-p) - (q-p)*conj(r-p)` over integer `Z[zeta_5]`. The second uses `sqrt(5)=1+2*zeta_5+2*zeta_5^4`, checks positive coefficients by integer comparisons, reconstructs variable IDs, and verifies the zero polynomial without trusting the first expansion's coefficient table. The exact example supplies all 2,200 two-orbit sign-pattern embeddings and all 11,000 weighted identities with absolute shifts, directions, and mirrors. All passed. The complete lifted family contains 1,320 clauses at twelve layers and 1,560 at thirteen layers; every emitted clause was directly tested six times. The thirteen-layer family hash is `11e6b7c78fab539a45a69cb95a2d54acd66f40d32633655ff20e591314483fd8`.

**Exact computation:** a second seven-row identity on source orbits `(0,2,5)` is retained as `m5_linear01.json`. It excludes the independently clause-checked model `cf56e1419dc19349bd16bc0cc875a830c8db9e703e92c57f1e386d84fc3a7355` by the cut `373 485 -577 -1004 -2926 -2986 3412`. Both formal polynomial implementations accepted the identity. The integer cyclotomic checker also accepted all 99,000 three-orbit sign-pattern embeddings and 1,500 weighted identities (three orbit selections, all shifts, both directions and mirrors). The weighted three-orbit test is sampled in its orbit selections; the symbolic identity is universal. Complete lifting gives 66,000 clauses at twelve layers and 85,800 at thirteen layers, whose family hash is `fcf7ec6a68328e0acfe500b5ae1969d5c89601be1f01e6ee40ff773b85b56de0`.

## GP refinement review

**Written proof (reviewed, not refereed):** `m5_gp_refine.py` correctly uses the six brackets in `[pbc][pde]-[pbd][pce]+[pbe][pcd]=0`. Its two choices of common signed-product sign and eight choices of first bracket signs enumerate exactly the sixteen forbidden assignments. Clause negation respects the signed encoder map, tautology removal is safe, and target variable numbers are reconstructed for each dimension. This review does not rely on the source violation file being complete: any retained actual violation yields sound clauses.

**Exact computation:** each emitted GP clause is tested on three injective orbit maps and both mirrored signs. These six tests per clause are finite implementation checks, not exhaustive orbit-injection tests. The universal argument is the determinant identity and exact literal substitution. Full GP status is checked separately on each retained abstract model; satisfying its current CNF alone is insufficient.

## Matched tiny-family experiment

**Evidence only:** the second matched comparison fixes all six product families, complete affine interiority, and the same `H1+d111111` cube. Its only input difference is the 1,560-clause `linear00` family. Both runs used the same binary and 180-second limit, without proof output. Both returned UNKNOWN; activity counts do not establish a speedup.

| Fixed input, plus indicated change | Wall seconds | CPU seconds | Conflicts | Propagations | Peak RSS, decimal GB |
|---|---:|---:|---:|---:|---:|
| Six product families + interiority | 180.672 | 179.948 | 383,423 | 749,194,740 | 2.576 |
| Same input + `linear00` | 180.656 | 179.817 | 346,048 | 769,384,774 | 2.444 |

**Exact computation:** the fixed input hash is `308e825a8acc312c3f27cea5b47733521ad95bdfb0e871ee3f5c3332f67c15a7`; with `linear00` it is `4f539746fb17bcd767bd7ae180fb93e5e67fe6bbb301cc22e1d31459d0bdb003`. Neither guard fired; the larger observed total memory was 27,810,332,672 bytes. Both children were reaped. Later runs use a native child-RSS guard at 3,000,000,000 bytes in addition to the system-memory guard; this does not alter the completed matched runs.

## Six-round GP refinement batch

**Exact computation:** starting from the twelve-layer model after both linear families, every round checks all 27,307,560 five-point GP sign relations. At most 100,000 violated relations are retained per round. The first round therefore uses a strict subset of its 198,660 violations; later rounds in this batch retain all their violations. Each retained relation contributes all sixteen forbidden assignments, followed by signed-variable substitution, tautology removal, and deduplication. Batches accumulate without inter-batch deduplication. The six batches below were each generated and exact-tested separately for twelve and thirteen layers.

| Batch | Violations before refinement | Relations retained | Clauses per dimension | Next SAT wall seconds |
|---|---:|---:|---:|---:|
| 01 | 198,660 | 100,000 | 354,144 | 6.027 |
| 02 | 75,960 | 75,960 | 243,072 | 18.081 |
| 03 | 25,020 | 25,020 | 80,064 | 24.103 |
| 04 | 21,930 | 21,930 | 70,176 | 36.136 |
| 05 | 16,660 | 16,660 | 53,312 | 9.044 |
| 06 | 22,060 | 22,060 | 70,592 | 18.078 |

**Exact computation:** all six replacement assignments passed complete checks against their retained CNFs. The last model, `cb7a94f2db9b19015f65d642afaee8f6538d43edecd18c610b05b198fda9cadd`, still has 7,040 GP violations. The decrease is not monotone, and these different SAT instances are not a speed comparison. None is a geometric construction or a GP-consistent survivor. The thirteen-layer rebinding preserves the specified point IDs and reconstructs its variable map; it does not claim to contain every GP identity on all thirteen orbits.

**Exact computation:** the retained C checker was also tested on every one of the 17,393,805 relations of the exact 55-point example, finding zero violations. Flipping one bracket sign produced 1,280 violations. The independent review and controls are recorded in `logs/m5_gp_controls.json`. These checks concern GP signs, not a realization algorithm.

## Longer proof-producing cube trial

**Evidence only:** the strengthened thirteen-layer `H1+d111111` formula contains the six product families, full affine interiority, both linear families, and GP batches `01`–`06`: 91,390 variables and 5,300,454 clauses. The input SHA-256 is `e7f785a44b40c3d1cfd94d752b057d038d2311703bda60f0435b7aad12544a10`. It ran with text LRAT enabled from the start and a 600-second limit. The outcome was UNKNOWN after 601.254 wall seconds and 599.194 CPU seconds, with 711,347 conflicts and 2,265,580,714 propagations. Peak process RSS was 2,560,475,136 bytes; peak observed total memory was 27,838,021,632 bytes. No guard fired, and the child was reaped.

**Exact computation:** the 1,243,456,719-byte partial proof stream was retained and compressed with verified decompression. Its raw SHA-256 is `849745909a02ecc7364f8d9c089c9e2d7ac3847b831a47893d84e946aa6417fe`, compressed hash `b5cf437c4db94c0d059c4579401ef691fd23c6df0be2aa0e952454294b6a86fe`. This is not a certificate: the run did not derive a contradiction. No proof checker was invoked on this partial stream. The trial concerns one explicitly named phase-order cube and establishes no fivefold threshold bound.

```sh
python3 -B -I ROTREFINE20261104/m5_gp_cegar.py --archive "$ARCHIVE" \
  --bin "$BIN" --checker "$GPCHECK" \
  --model "$ARCHIVE/t12_linear01_families06_180.model.json" --rounds 6 --seconds 180 --linear-through 1
python3 -B -I ROTREFINE20261104/m5_proof_lane.py --archive "$ARCHIVE" \
  --bin "$BIN" --file t13_gp06_linear01_families06_cube.cnf \
  --name t13_gp06_linear01_families06_cube_600 --seconds 600
```

## Third pentagon identity

**Exact computation:** after twelve GP batches, the model `22884512a1a0056cf8a9441b98e06daee014cc814079da01d8acd4a8804f8cb9` still has 4,920 GP violations. A further exact five-row identity on source orbits `(1,9,10)` excludes it by `2820 2849 2851 2852 -2859`. Its witness hash is `20b1586b152375ae4ff12e0eb39f7bb1df59c5e8c760a4fe2614fd8c97df9ca1`. Independent polynomial implementations, all 99,000 exact sign-template embeddings, and 1,500 weighted identities passed. Complete lifting produces 66,000 twelve-layer clauses and 85,800 thirteen-layer clauses, with respectively 396,000 and 514,800 direct clause tests. Their hashes are `7963f449b0483538adeebf13f6ac28ce4db3b10d8e46f37d6de3892db10eea1e` and `d39da6843ffdc4dcad7d7b7ec4e3fba3e8037baccc7583a06be24b345d1fdbc7`.

**Written proof (reviewed, not refereed):** [the shared-centre pentagon derivation](m5_linear02_proof.md) proves the five-row identity directly from two pentagons about the same centre. It uses neither layer ordering nor phase inequalities and supplies an independently readable explanation of the sign contradiction.

## Second GP-refinement batch

**Exact computation:** batches `07`–`12` again retained every detected violation, generated both dimensional maps, directly tested every emitted clause six times, and independently checked every returned SAT assignment against its entire CNF.

| Batch | Violations before refinement | Clauses per dimension | Next SAT wall seconds |
|---|---:|---:|---:|
| 07 | 7,040 | 22,528 | 39.153 |
| 08 | 6,670 | 21,344 | 27.089 |
| 09 | 6,560 | 20,992 | 33.156 |
| 10 | 6,620 | 21,184 | 69.284 |
| 11 | 7,540 | 24,128 | 9.048 |
| 12 | 3,280 | 10,496 | 12.055 |

The twelve accumulated GP batches contribute 992,032 clauses per dimension before inter-batch deduplication. The final model has 4,920 GP violations and is the source of the third pentagon identity described above. This batch again demonstrates only exact refinement of abstract models, with no realization or upper-bound conclusion.

## All-phase threshold pilot and complete GP-template lifting

**Evidence only:** the thirteen-layer `H1`-only formula uses the same six product families, affine interiority, `linear00` and `linear01`, and all twelve observed-GP batches. It has 5,421,120 clauses and no phase-order cube. With text LRAT enabled from the start, the 600-second run returned UNKNOWN after 601.366 wall seconds and 598.729 CPU seconds, with 634,754 conflicts and 2,022,069,130 propagations. Peak process RSS was 2,793,472,000 bytes; peak observed total memory was 27,790,016,512 bytes. No guard fired. This is a broader input than the preceding cube experiment, not a matched timing comparison.

**Exact computation:** the input hash is `1b2a2a0072ad475a27e22e8c7733b145a4bb597d5ad4b430560b7806b42de765`. The 1,181,192,432-byte partial LRAT stream has raw hash `513c67c06ac577af47dffa33575d49a5fac9ee1e7fe9ff2ffac455b907132093`, compressed hash `163292ac078a93c9478c55c0e8da93c80ed964a02b75ee1dd8fdaee35eea5d72`, and a verified decompression round trip. It is not a certificate and was not proof-checked. The child was reaped before the next solve.

**Written proof (reviewed, not refereed), with exact implementation tests:** `gp_template00` takes the GP identity at anchor quintuple `(25,0,3,28,34)` from the last twelve-layer model. Its three signed products are all positive, contradicting their zero sum. The source-map clause is `-80 1004 -1005 -1011 1073 -5569`. The template was selected for fewest distinct variables among 110 violations supported on at most three orbits; no frequency-optimality claim is made. Its source supports are `(0,5,6)`.

**Exact computation:** independent canonical-map verification and all 99,000 certified-set template embeddings passed. Complete orbit, phase, direction, and sign-reversal lifting yields 132,000 twelve-layer clauses (hash `b0af045f489da4c7760569f1c4cb67a6a519b4d0badd56779e5cb50efb3129f7`) and 171,600 thirteen-layer clauses (hash `f94ed62e7cc03a1424aa3da516dfee5bb3bea14d0dfa7e6acc2e432e85ce842a`). Every emitted clause passed six direct exact tests, respectively 792,000 and 1,029,600. This complete template family supplements the batches of individually retained relations; it is a GP-sign consequence, not a rotation-specific identity.

## GP-consistent survivor and complete product-graph check

**Exact computation:** with `linear02` and `gp_template00` added, the next twelve-layer assignment satisfied all 4,403,178 clauses, but still had 2,220 GP violations. GP batch `13` added 7,104 clauses per dimension and produced an assignment with 1,120 violations; batch `14` added 3,584 clauses and produced a survivor with zero violations among all 27,307,560 GP relations. The latter model hash is `7e75a43e3b4c5028ad8edb17fe31a67e86f74ff2f2173615c53fc3d2f5977c49`; a separate checker accepted all 4,413,866 clauses of its input, hash `af9abe4c07d94c11ce7db3cadc62b0661d5e9025a352d04abf0d9f54d0755722`.

**Exact computation:** `m5_full_products.py` supplies the retained generic C graph core with fivefold signed canonical IDs, all 60 points, and the twelve phase-zero anchors. A common rotation carries any anchored GP relation to one of those anchors, preserving the product vertices. The core enumerated all 5,461,512 reduced identities and 10,923,024 directed edges with multiplicity. The complete directed product-vertex graph was acyclic. This exhausts directed cycles in that graph; it does not test arbitrary positive dependencies of logarithmic inequalities or certify realizability.

**Exact computation:** two small restrictions were independently enumerated in Python: 252 and 3,003 identities, all 6,510 directed edges agreeing exactly with the C dump, and independent DFS agreeing on acyclicity. The unchanged C binary hash is `466bd2e013655758e24342c8f5fffd41f3068957d9951e213d1b1f444ce1003a`; source hash `8aefa45b0e53a768de328b10e2a8ec6dfd1554366a299848ad8cf6712ac6aa05`. The full C check used 558,235,648 bytes peak RSS and 0.229 seconds wall time; its process was reaped. Inputs, full counts, and controls are retained under `m5_full_products_gp14`, with the compact public log `logs/m5_full_products_gp14.jsonl`.

## Exclusion beyond GP signs and directed product cycles

**Exact computation with a written algebraic proof:** the GP-consistent, product-graph-acyclic model above violates the eight-row identity retained as `m5_linear03.json`, on source orbits `(1,7,8,9)`. The source-model clause is `2628 2649 2701 -2739 -2759 -2791 6515 6526`. Witness hash `29b9ed9cfdc2d3637fffd4ccb33d547e52476c1efd3d4f277883f6bc4b45ed19` binds it to the immutable model. Two independent formal polynomial calculations verify a zero identity over `Q(sqrt(5))`, with all weights strictly positive against the required orientation signs. Thus no point configuration carrying the prescribed geometric fivefold rotation realizes this model.

**Exact computation:** all 3,960,000 four-orbit source-template embeddings into the exact example passed, as did 7,500 weighted identity checks (three orbit selections, every absolute phase choice, both directions and mirrors). The formal identity supplies universal soundness; the finite tests check implementation. `m5_linear_geometry.py` records the exact polynomial residual and scope explicitly.

**Written proof (reviewed, not refereed):** the bounded target family uses only strictly increasing injections of the four source orbit labels into target orbit labels. This is a sound subset of all injective substitutions. It includes every relative phase choice, both directions, and both global sign reversals, but is not the complete family of arbitrary target-orbit injections. Metadata records this restriction explicitly.

**Exact computation:** deduplication leaves 123,750 twelve-layer clauses, hash `a787c8d7743f91e93ac8616aa06c590a8fa42fce453097cfcf6d9d29b154e4cd`, and 178,750 thirteen-layer clauses, hash `f2607c58f8b573d35e44d368200057455ff9d39a1b1343a7b9a08c8bfeacde75`. Every emitted clause passed six direct exact tests, respectively 742,500 and 1,072,500. This model supplies a concrete separation between the tested sign/product-cycle relaxation and genuine fivefold geometry. No claim is made about arbitrary positive logarithmic dependencies or independent novelty of the identity.

## Final bounded trials and cleanup

**Exact computation:** after `linear03`, the twelve-layer formula remained SAT (22.132 wall seconds; all 4,537,616 clauses checked), with 1,640 GP violations. GP batch `15` adds 5,248 clauses per dimension; its next SAT assignment (24.149 seconds, all 4,542,864 clauses checked) has 5,450 violations. Batch `16` adds 17,440 clauses per dimension; its next SAT assignment (20.117 seconds, all 4,560,304 clauses checked) has 4,300 violations. Each batch passed six direct exact tests per emitted clause. The final twelve-layer model hash is `180102dad8e9f688cf8948402fbe13e0d2d4cb93d0df9b75854b03c3901463ed`; it is not GP-consistent. These three runs retained proof traces from the start, but SAT traces are not refutation certificates.

**Evidence only:** the final thirteen-layer `H1`-only formula contains all 28 accepted families/batches, 91,390 variables, and 5,890,646 clauses. Its sole extra unit is `H1`; no phase-order cube is imposed. The input hash is `3ca0d9429daa4495b4336f9236334f093ab3d854efd0cdbdee9aa72537baf80f`. The 600-second proof-producing run returned UNKNOWN after 601.261 wall seconds and 598.339 CPU seconds, with 585,071 conflicts and 1,973,661,338 propagations. Peak process RSS was 2,825,060,352 bytes; peak observed total memory was 27,760,066,560 bytes. No guard fired. This final bounded search establishes no threshold exclusion.

**Exact computation:** the final 1,149,235,438-byte partial LRAT stream has raw hash `3d9c637f58f3e61e9f77c90463f4e120767ea55a4f5d28eefe081fee0de411d2` and compressed hash `62c2dcf93153f8ba1ecb0e4fbeb509e59bd8ee2506820708dfe09f916cafa6f6`; decompression matched the raw hash. It is not a certificate, and no checker was invoked on it.

**Exact resource accounting:** 35 solver jobs completed: 26 SAT abstract assignments and 9 UNKNOWN results, with no UNSAT result. Aggregate solver wall time was 3,691.367 seconds and aggregate CPU time 3,632.547 seconds. Peak process RSS across the solver jobs was 2,825,060,352 bytes; peak observed total active + wired + compressed memory was 28,068,118,528 bytes. No guard fired. All solver and verification children in this lane were reaped, and no owned computation remains running. No `cake_lpr` or other refutation checker was launched by this lane. The six retained partial LRAT streams total 3,887,153,254 bytes before compression.

`m5_campaign_summary.json` records each job, its input/model/proof hashes, resources, and cleanup state. The durable archive contains raw formulas, models, accepted witnesses and families, all assembly metadata, proof streams, sanitized logs, and content-addressed source snapshots. Mutable archive-index files are compressed only after their last update by the final archive audit. The lane wrappers retain this campaign's hard deadline; a later authorized campaign must explicitly reset its deadline before rerunning them.

The useful retained result is the exact model obstruction and the tested refinement machinery. The measured UNKNOWN runs do not establish a speedup, a realizability result, or an upper bound.
