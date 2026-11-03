# Beyond zero identities: a sixfold quadratic obstruction

**Exact computation plus written proof (independently reviewed, not
refereed).** Continuation model `model0033` is excluded from a realization
carrying the specified geometric sixfold rotation. Its SHA-256 is
`8b98f35bf949205a9270d94460b02a8e420e1607c5280db84c6f5588a621a9a8`.
This exclusion does not assert nonrealizability with the prescribed point
labels under every possible geometric action, and does not settle the
existence of another 60-point example.

## A verified limit of the linear-identity method

The model passes the full general-position sign check. It also admits an
exact rational lift satisfying all 5,710 strict orientation inequalities in
the dot/cross variables of `math.md`, with positive, strictly decreasing
squared radii. The minimum signed margin is

```text
11999999935581000083197553 / 9261999950281584064208027730 > 0.
```

The lift file has SHA-256
`011c9d9d13b15f37cacd786724880ec9eb7a99f80e3c46e2098945180f90f6e1`.
`tests/check_linear_primal.py` independently expands the seed-coordinate
triangle determinants, reconstructs their dot/cross coefficient forms, and
checks every rational inequality. Thus a positive zero combination of these
signed orientation forms cannot exclude this model: evaluating such a
combination on the displayed lift would be both positive and zero.

This rational lift itself is not a valid Gram matrix. For orbits 0 and 1,
its Hermitian principal minor is exactly

```text
D_00 D_11 - D_01^2 - 3 E_01^2
= -590506859853708478 / 20892261048855742161 < 0.
```

That calculation rejects this particular lift only. A different lift could
in principle satisfy the missing Gram conditions, so the negative minor
alone does not exclude the model.

## The exact quadratic certificate

For actual orbit seeds, `H_ij = D_ij + i sqrt(3) E_ij` is a Hermitian Gram
matrix. Positive semidefiniteness is a necessary condition; rank one is a
further condition that the numerical relaxation does not impose. A rational
congruence gives the equivalent real positive-semidefinite matrix

```text
[ D  -E  ]
[ E  D/3 ] .
```

`math_sdp.py` uses a numerical semidefinite optimization only to suggest
weights. After rounding to positive integers, it recomputes the quadratic
form exactly and accepts the candidate only if rational elimination proves
negative definiteness. Numerical solver warnings, objective values, and
status codes are not proofs.

For `model0033`, 75 positive integer weights, ranging from 1 to 84,513,
satisfy

```text
sum_r weight_r * required_sign_r * area_r(z) = Q(z),
```

where `Q` is negative definite in the twenty real coordinates of the ten
orbit seeds. If all required signs held, the left side would be strictly
positive. The right side is nonpositive for every seed vector, a
contradiction. This direct quadratic-form argument is the retained proof;
it does not require trusting the SDP solver or proving its numerical dual
optimality.

The witness is `math/model0033_sdp/sdp_witness.json` in the campaign archive,
SHA-256 `c07c0037b0ae71276cfabbdc4107c0d0b2b72ce72df6f2b02d0b55421b69ef6a`.
`tests/check_sdp_symbolic.py` independently reconstructs all variable IDs
and source-model signs, expands the actual determinants in the positively
oriented basis `(1,zeta_6)`, checks exact congruence to the advertised matrix,
and proves its negative definite sign by rational Schur complements. All
twenty pivots of the negated matrix are positive. The independent result is
`logs/m6_sdp0033_independent.json`.

This is a concrete strict separation between the zero-identity relaxation
and the geometric quadratic condition on one retained model. No claim of
mathematical priority is made. Smaller-support witnesses and the actual
inserted clauses are recorded separately by the refinement campaign.

**Exact computation.** Support reduction found a 16-row certificate on just
five orbits, `1,3,4,7,8`. Its positive integer weights range from 1,452 to
183,453; its ten-coordinate quadratic form is negative definite. The smaller
witness SHA-256 is
`85ff269f59fd263be8e11a37c015f94dccb88a2354888eb14b09bd5d26e2fe8d`.
The same independent direct-polynomial/congruence/Schur-complement checker
accepts it; see `logs/m6_sdp0033_five_orbit_independent.json`. Its source clause
is

```text
1635 -2026 2107 2162 -2320 2675 2737 3852 3888 -3911 -4039 4381 -4431 4564 4895 4977 0
```

The complete directed product-vertex graph of this same model is also
acyclic: 4,551,260 rotation-reduced GP identities produce 9,102,520 edges
(with multiplicity), and Kahn pruning removes all 9,848,610 used vertices.
The retained C implementation has three direct-Python crosschecks, including
a known cyclic example. This exhausts directed product-vertex cycles;
general weighted exponent cancellation, a broader final-polynomial method,
is not exhausted. See the full-product records in the `m6/` archive and
`logs/m6_full_product_review.json`.

## Correct transformations of an inequality cut

Orbit injections and independent index shifts substitute arbitrary rotated
seeds, preserving the quadratic bound. Direction reversal needs care.
Replacing the rotation by its inverse is conjugation of the plane, which
also reverses every oriented area. Therefore inverse direction and global
sign reversal must be coupled. For these nonzero quadratic inequalities,
the independent sign/direction choices used for a zero identity are not a
valid lifting rule. The permitted choices are `(direction, sign)=(+,+)`
and `(-,-)`.

The initial 75-row witness uses ten source orbits and was not inserted as a
family. The smaller five-orbit witness passed 100 deterministic finite
injective tests on the certified nine-orbit, 54-point configuration. These
are regression tests, not an exhaustive embedding enumeration.

The inserted `psd1006` family uses all 252 increasing injections into ten
orbits, 128 selected relative-shift patterns, and the two coupled
direction/sign choices. It has 64,512 clauses, SHA-256
`763bdd9da2e160230c006bea3c3659701f1b187c3a60bf37e32bfd79483cec05`.
Every emitted clause also passes exact tests on the original and mirrored
configuration with counterclockwise labels restored: 129,024 direct tests.
This is an explicitly bounded partial family. The source clause is included
and excludes the source model. The direct-polynomial check also confirms
why flipping signs alone fails: it turns the negative-definite form into a
positive-definite form.
