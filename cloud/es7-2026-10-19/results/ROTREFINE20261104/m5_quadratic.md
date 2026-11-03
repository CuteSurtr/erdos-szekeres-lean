# Exact fivefold linear separation

**Written proof (independently reviewed, not refereed).** For a configuration
carrying a specified rotation through 72 degrees, write each point as a rotated
orbit seed. Every signed triangle area is a homogeneous quadratic polynomial
in the seed coordinates. Equivalently, it is linear in seed dot products and
cross products, with coefficients in `Q(sqrt(5))`. If a positive linear
combination of the signed area forms is identically zero, the corresponding
strict sign conjunction cannot occur in a configuration in general position.
The negation of that conjunction is therefore a sound clause.

`m5_quadratic_scan.py` uses floating-point linear programming only to select a
candidate support. `quadratic_recovery.py` recovers its coefficients by exact
Gaussian elimination in `Q(sqrt(5))`, checks their positivity exactly, and
checks that the weighted form is zero. A numeric infeasibility or feasibility
verdict alone is not accepted as a geometric conclusion.

**Exact computation.** `tests/check_linear5_symbolic.py` supplies a separate
check that does not use the search coefficient table. In the positively
oriented basis `(1,zeta_5)`, rotation is

```text
R(u,v) = (-v, u + ((sqrt(5)-1)/2) v).
```

It checks `R^5 = I`, expands actual seed-coordinate triangle determinants,
reconstructs variable numbers and signs, checks the source-model hash, and
requires an identically zero polynomial with positive weights.
`m5_linear_geometry.py` supplies a further implementation using formal complex
polynomials in the integer cyclotomic ring `Z[zeta_5]`. Corrupting the first
witness's weight, model hash, or clause is rejected by the seed-polynomial
checker; see `logs/m5_quadratic_mutants.json`.

## The small pentagon identity

Let `b_0,...,b_4` be the vertices of a regular pentagon in rotation order,
and let `a` be any point. Write `[p,q,r]` for the oriented doubled area. The
parallel-chord equality

```text
b_3 - b_0 = ((1+sqrt(5))/2) (b_2 - b_1)
```

gives

```text
(5-sqrt(5)) [a,b_0,b_3]
- 2 sqrt(5) [a,b_1,b_2]
+ (5-sqrt(5)) [b_0,b_1,b_3] = 0.
```

All three displayed coefficient magnitudes are positive. Consequently the
area-sign pattern `(+,-,+)` is impossible. This is a standard geometric
relation of a regular pentagon, not a claim of mathematical priority. A short
independent derivation is in `math_pentagon.md`.

**Exact computation.** In the retained twelve-orbit model with SHA-256
`40494397cc15b81e61ed8dacb2818e6377ab074c3ae97912dc906c67e505b028`, choose
`a=0` and `b_j=50+j`. The forbidden conjunction gives the clause

```text
-1555 1562 -6822 0
```

The witness SHA-256 is
`36b585fcd66266a3a0b03c0d53bb42faa403c8a56b8a303eefed88c18a9e9e8a`.
Both independent polynomial implementations accept it. The exact certified
56-point example, with its centre removed, passes 2,200 complete sign-pattern
embedding tests and 11,000 weighted-identity embedding tests. The full lifted
families have 1,320 clauses at twelve orbits and 1,560 at thirteen. The latter
passes 9,360 additional direct clause tests and has SHA-256
`11e6b7c78fab539a45a69cb95a2d54acd66f40d32633655ff20e591314483fd8`.

The finite tests validate the implementation. The identity supplies the
universal argument. The exclusion concerns realizations with the prescribed
geometric rotation; it is not a claim about all realizations of an abstract
orientation pattern.

## Lifting and later experiments

Injective orbit relabelling, independent phase shifts, a common reversal of
rotation direction, and reflection preserve the real area identity. Applying
these transformations to an impossible sign conjunction gives sound clauses.
No arbitrary independent reversal of individual orbits is used. See
`m5_REPORT.md` for accepted families, exact tests, solver timings and final
status. Further witnesses are retained under the archive's `math5/` directory.
The seven-row successor witness was found in the first model surviving the
small pentagon family; it involves three orbits and also passes the independent
seed-polynomial check. These source models are not claimed to satisfy every
Grassmann–Plücker sign relation. The seven-row witness's source model, with
hash `cf56e1419dc19349bd16bc0cc875a830c8db9e703e92c57f1e386d84fc3a7355`,
fails 52,510 of the 27,307,560 relations in a subsequent complete check.
None of these exclusions by itself resolves the fivefold threshold.

A later five-row identity excludes the model surviving twelve GP-refinement
rounds, SHA-256
`22884512a1a0056cf8a9441b98e06daee014cc814079da01d8acd4a8804f8cb9`.
It involves orbits `1,9,10` and gives the source clause
`2820 2849 2851 2852 -2859`. Its witness SHA-256 is
`20b1586b152375ae4ff12e0eb39f7bb1df59c5e8c760a4fe2614fd8c97df9ca1`.
Independent seed-polynomial and cyclotomic checks pass, along with 99,000
complete sign-pattern embeddings and 1,500 weighted geometric checks on the
certified example. The full twelve- and thirteen-orbit families have 66,000
and 85,800 clauses, respectively; every emitted clause receives six direct
exact tests. See `m5_linear02_proof.md` for a separate shared-centre pentagon
derivation. This source still has 4,920 full-GP violations, which are recorded
separately; no uniform-chirotope claim is made for it.

An earlier rational-block relaxation, which cancelled rational and radical
coefficients separately while allowing only rational positive weights, missed
the three-sign identity. Its negative search outcomes therefore cannot be
read as evidence of realizability. One 191-row witness on all twelve orbits
passed exact symbolic checks but was not inserted: the smaller witnesses give
tractable lifting and direct tests against the eleven-orbit example.

## A fully GP-consistent source excluded by eight areas

**Exact computation.** After fourteen GP-refinement batches, model
`t12_gp14_linear02_families06_180` satisfies all 4,413,866 retained CNF clauses
and all 27,307,560 GP sign relations. Its SHA-256 is
`7e75a43e3b4c5028ad8edb17fe31a67e86f74ff2f2173615c53fc3d2f5977c49`.
Its complete directed product-vertex graph is acyclic: 5,461,512
rotation-reduced relations and 10,923,024 edges, with direct Python controls.
This does not exhaust general weighted exponent cancellation.

**Written proof plus exact computation.** Set `A=13-3 sqrt(5)`,
`B=13 sqrt(5)-15`, and `C=5 sqrt(5)-1`, all strictly positive. For the
specified fivefold rotation and arbitrary orbit seeds, the identity is

```text
A*(-[5,35,39] -[5,36,37] +[5,40,45] +[5,41,47]
   -[35,45,49] -[35,46,47])
- B*[5,38,46] + C*[5,43,46] = 0.
```

The source model makes every displayed signed term positive, a contradiction.
The witness involves only orbits `1,7,8,9` and has SHA-256
`29b9ed9cfdc2d3637fffd4ccb33d547e52476c1efd3d4f277883f6bc4b45ed19`.
Both independent seed-coordinate and cyclotomic polynomial checks pass. The
source clause is `2628 2649 2701 -2739 -2759 -2791 6515 6526`.

**Exact computation.** The source pattern passes all 3,960,000 injective
sign-pattern embeddings in the certified eleven-orbit example and 7,500
weighted geometric tests. The lifted families deliberately use only
order-preserving target-orbit injections, with all relative shifts and both
independent direction/sign choices justified for a zero identity. They are
bounded partial families, with 123,750 distinct clauses at twelve orbits
and 178,750 at thirteen. Every emitted clause also passes six exact tests.
The thirteen-orbit family SHA-256 is
`f2607c58f8b573d35e44d368200057455ff9d39a1b1343a7b9a08c8bfeacde75`.
The universal identity supplies soundness; finite configuration tests validate
implementation. This excludes the prescribed rotational realization of this
model, not every 60-point fivefold configuration.

## General-position refinement

**Written proof (independently reviewed, not refereed).** The identity
`[pbc][pde]-[pbd][pce]+[pbe][pcd]=0` excludes exactly sixteen of the 64
assignments of nonzero signs to the six brackets. `m5_gp_refine.py` verifies
each reported violation against its source model, enumerates these sixteen
forbidden sign assignments, and translates their negations through the target
encoder's signed literal map. It rebuilds variable IDs when the target orbit
count differs. Duplicate clauses and tautologies may be discarded safely.
The identity supplies universal soundness without any rotation assumption.

**Exact computation.** Every emitted GP clause is additionally tested on six
embeddings in the certified 55 noncentral points (three injective orbit maps
and both global signs). These are implementation tests, not an exhaustive
orbit-injection enumeration. The retained metadata states that distinction.
For the model above, 52,510 violations give 168,032 unique clauses and
1,008,192 direct tests. This reference batch was generated; the adaptive lane
records separately which batches were actually inserted.

The complete GP checker also passes two controls: all 17,393,805 relations on
the exact 55-point table pass; flipping one bracket and its antisymmetric
copies produces 1,280 violations. See `logs/m5_gp_controls.json`.

Reproduction uses an isolated Python environment only for numerical search:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 "$PYTHON" -I -B \
  m5_quadratic_scan.py --model "$MODEL" --out "$SEARCH" --max-layers 3
python3 -I -B tests/check_linear5_symbolic.py \
  --witness "$SEARCH/linear_witness.json" --model "$MODEL"
python3 -I -B m5_full_gp.py --model "$MODEL" --checker "$GP_CHECKER" \
  --layers 12 --out "$GP_OUTPUT"
python3 -I -B m5_gp_refine.py --model "$MODEL" \
  --violations "$GP_OUTPUT/full_gp_violations.txt" --archive "$M5_ARCHIVE" \
  --target-layers 12 --output "$M5_ARCHIVE/selected_gp.clauses"
```
