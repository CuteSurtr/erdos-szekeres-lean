# Independent geometry tests — 4 November 2026

## Results and limits

**Exact computation.** Both encoders passed 68 separately generated hexagon configurations with two or three layers. Integer orientations and exhaustive eight-subset hull tests found no unsound non-chain clause and no disagreement between the chain family and existence of a convex octagon. The 54-point certified set and its mirror also satisfy all 1,040,348 clauses of each nine-layer encoder, checked in exact integer/rational arithmetic.

**Evidence only.** Both encoders passed 64 floating-point heptagon configurations. These tests use a nonzero-determinant guard, but no rigorous interval error bound, so they do not qualify as exact computation.

**Scope.** These are finite validation results, not universal encoder soundness proofs. The 54-point check does not enumerate its eight-subsets; it verifies the full CNF under the geometrical assignment and the least chain assignment. No SAT solver or proof checker is used here, and no certified source directory is changed.

## Independent oracle

`tests/adversarial.py` imports the encoder A generator and executes encoder B with in-memory output streams. It does not import any existing validation module. Its separate implementations provide:

- all triple orientation signs from the actual coordinates;
- strict nesting checks against every edge of every outer layer;
- a monotone-chain convex hull of every eight-subset, stopping at the first convex octagon;
- generic Horn closure of the residual CNF after all orientation and phase variables are fixed, without reproducing either encoder's chain-building recurrence;
- negative controls that add an orientation unit with the wrong sign and delete the entire chain family on an octagon-containing configuration.

**Exact computation.** For hexagons, a stored point `(x,y)` represents `(x,sqrt(3)*y)`. Rotation by 60 degrees is the rational map `((x-3y)/2,(x+y)/2)`. After all denominators are cleared, orientation is the sign of an integer determinant, since the omitted factor `sqrt(3)` is positive. Phase order within the sector is the exact order of `y/x`. The generated layers are placed using exact edge bounds, including a factor `999999/1000000` below the nesting limit. Mirror images are relabelled by the same rational rotation rule.

**Evidence only.** For heptagons, points use binary floating-point trigonometry; configurations with any absolute triple determinant below `1e-10` are rejected. None of the final 64 cases was rejected. No certified numerical error analysis is claimed.

The fixed seed is `202611040731`. Targeted cases include phases near zero, near the sector boundary, near coincident phases, both sides of the odd-order half-sector boundary, tight nesting, reverse phase order, and reflections. Random cases use the same independently implemented geometry.

| Geometry | Layers | Cases | Octagon-free | Contain an octagon | Eight-subsets examined |
|---|---:|---:|---:|---:|---:|
| 6-fold, exact computation | 2 | 36 | 29 | 7 | 15,097 |
| 6-fold, exact computation | 3 | 32 | 17 | 15 | 816,981 |
| 7-fold, evidence only | 2 | 34 | 26 | 8 | 82,510 |
| 7-fold, evidence only | 3 | 30 | 15 | 15 | 3,250,307 |

**Exact computation / evidence only, respectively.** All 4,164,895 examined eight-subsets agreed with both formulas. The 12 exact three-layer reflection pairs reversed `Y(1,2)`; the 24 heptagon reflection pairs reversed `H(1)`. All eight formula instances detected the wrong orientation unit, and removing their chains made the evaluator miss an octagon that the independent hull oracle found, as intended by the negative control.

## Exact certified 54-point check

`tests/certified54.py` reads `ES8SYM/sets/c6_54pts_9layers.pts`. For a cyclotomic weight vector `w`, it converts exactly to

```
X = 2*w0 + w1 - w2 - 2*w3 - w4 + w5
Y = w1 + w2 - w4 - w5
```

The real point is `(X/2,sqrt(3)*Y/2)`. The common positive factor `1/2` is omitted. Each input block is independently checked to be a full regular hexagon. Blocks are ordered by the exact squared radius `X*X + 3*Y*Y`.

For the chosen outer representative `(u,v)`, multiplication by its complex conjugate sends `(x,y)` to `(x*u+3*y*v,y*u-x*v)`. This is a rotation and a positive uniform scale, so it preserves orientations. The unique sector representative is selected by `x>0` and `0<=y<x`; inner representatives satisfy strict inequalities. All phases are distinct, and their rational slopes determine the phase order. The mirror check conjugates the original coordinates before repeating the entire normalization. No trigonometry, Decimal arithmetic, or tolerance is used.

**Exact computation.** For each of the original and mirror configurations, every one of the 24,804 triple orientations is nonzero and every later orbit is strictly inside every earlier orbit. Results:

| Configuration | Encoder | Clauses | Non-chain violations | Chain violations | Y(1,2) |
|---|---|---:|---:|---:|---|
| Original | A | 1,040,348 | 0 | 0 | false |
| Original | B | 1,040,348 | 0 | 0 | false |
| Mirror | A | 1,040,348 | 0 | 0 | true |
| Mirror | B | 1,040,348 | 0 | 0 | true |

The exact phase orders are `[0,3,8,7,2,6,5,4,1]` and `[0,1,4,5,6,2,7,8,3]`.

This supplies an actual exact-arithmetic replacement for the finite-precision checks described as “exact” in `ROT456/tests/test_reflect.py` and the related encoder B test. It does not relabel those historical runs as exact.

## Reproduction, resources, and hashes

Run from the parent results directory:

```sh
python3 -I C6C7REVIEW/tests/adversarial.py > C6C7REVIEW/logs/adversarial.jsonl
python3 -I C6C7REVIEW/tests/certified54.py > C6C7REVIEW/logs/certified54.jsonl
```

**Evidence only (observed resource use).** The final small-instance run took 5.77 seconds. The final 54-point run took 6.28 seconds and reported peak resident memory of 733,347,840 bytes through `resource.getrusage`, within the one-core/approximately 1 GB allocation. All test processes exited. An earlier `/usr/bin/time -l` wrapper could not read `kern.clockrate` in the restricted environment after the test itself passed; the final run records resources directly in Python and exits successfully.

**Exact computation.** SHA-256 of retained artifacts:

| Artifact | SHA-256 |
|---|---|
| `tests/adversarial.py` | `76cc273b5f96f23d9679da6c9c36f7c5a83fe73458efb5843e5d38a4a27b01ac` |
| `logs/adversarial.jsonl` | `9d1910a51cf4dfd6e792b795664cd08569cbda25b8184d270d9671d559378684` |
| `tests/certified54.py` | `92ac5a8623f65f052b3e8799af9c0119ed3f37a30751ecad42874b49fd5f745e` |
| `logs/certified54.jsonl` | `04a9821103812be2bbc6b40cc2550a51223749821f37fc55199074e789236837` |
| Source 54-point file | `235472b5c604421d11458865e2035b9977a8aa628f699f82bfad74536bf12c95` |
| In-memory encoder A, 6-fold/9 layers | `467e71194ffd0c2c6a629191fd5d86d33a30a61995e0227eac144649b5ba6782` |
| In-memory encoder B, 6-fold/9 layers | `9f63854369a76998e13217e1f4208e365d0821b07f253decca2b9aed1ba1d350` |

Formula fingerprints for all eight small-instance formulas are included in the JSONL log. Formulas were held in memory; no CNF or proof file was left in scratch storage. Log hashes identify this retained run, including measured elapsed times, so later runs need not reproduce the log bytes.
