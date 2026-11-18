# Forced16 product algebra — checked conditional theorem

**PROVED generic Lean algebra.** Five Init-only modules pass with 29 explicit
standard-only axiom audits. This packet does **not** claim a Lean refutation
of the fixed forced16 orientation model.

The main reusable theorem is
`Delta3.Forced16Algebra.cancelling_certificate_contradiction` in
[F16Cancellation.lean](F16Cancellation.lean). For a nonempty finite list of rows,
a finite list of variables with positive values x, positive natural weights w,
and natural exponent matrices small and large, it proves False from:

- every row's small monomial being strictly below its large monomial;
- equality, for each listed variable j, of the weighted totals
  `sum_i small(i,j)*w(i)` and `sum_i large(i,j)*w(i)`.

The proof raises each strict inequality to its positive natural weight,
multiplies the positive factors, and proves that multiplication of monomials
adds exponents. Exponent cancellation makes the two strictly ordered products
equal. Lists retain multiplicities; no finite-set enumeration, logarithm,
division, completeness, or fixed numeric certificate is hidden in the statement.

The algebraic assumptions are Lean's existing core `Lean.Grind.CommRing`,
`LE`, `LT`, `Std.LawfulOrderLT`, `Std.IsLinearOrder`, and
`Lean.Grind.OrderedRing` instances. These are standard ring and order laws,
not custom axiom declarations. A Mathlib-Real instantiation is not compiled
in this packet.

## GP and magnitude bridge

[F16GP.lean](F16GP.lean) proves the common-point Grassmann–Pluecker relation
for actual coordinate pairs using the determinant
`orient(a,b,c) = det(b-a,c-a)`.
For arbitrary five points it proves

`[a b c][a d e] - [a b d][a c e] + [a b e][a c d] = 0`.

It also proves `unique_sign_magnitude`: if A+B+C=0 and A has the unique
strict sign, then |A|=|B|+|C|, both latter magnitudes are positive, and
|B|<|A|. Here magnitude is explicitly defined as -x for x<0 and x otherwise.

[F16GPMagnitude.lean](F16GPMagnitude.lean) proves magnitude's negation and
multiplication laws and derives strict inequalities between products of
bracket magnitudes. [F16Certificate.lean](F16Certificate.lean) supplies:

- `coordinate_gp_inequality`, directly applying that result to coordinate
  determinants when the first GP term has the unique sign;
- `gp_certificate_contradiction`, a conditional finite-certificate theorem
  combining the GP rows with weighted exponent cancellation.

The latter explicitly assumes each row's zero-sum identity, unique-sign
condition, and the equality of its small/large monomials to the appropriate
term magnitudes. Selected GP terms may be reordered before applying the
generic unique-sign theorem. No row or sign binding from forced16 is
silently assumed checked.

## Fixed-model boundary

The context inputs are the frozen
[written forced16 verification](../forced16_realization/VERIFY_FORCED16.md),
its 387-row certificate, its 560-sign orientation pattern, and the parent's
independent exact replay. Their hashes are recorded in
[data/manifest.json](data/manifest.json). The certificate hash is
`cfe42cec6041709b2ed7ac18ee16b13e57f091239ac19b8e5257aac46d2a326d`;
the sign hash is
`b21664b06887c4019d75023025b1cd80582064a0b06f53698d2a70bc8fc49067`.

Those data were read as context but are not used as Lean premises or
evaluated inside the finished Lean sources. A complete fixed-model link
still requires kernel-checked encoding of all input signs, each selected
row and its factor-index/permutation bindings, the 387 positive weights,
and the 560 weighted exponent cancellations. A direct Mathlib real-point
instantiation would also need checking. The independent written/exact
forced16 nonrealizability proof remains separate.

## Checks and resources

| Replay order | Module | Axiom reports |
| --- | --- | ---: |
| 1 | F16Products | 10 |
| 2 | F16Cancellation | 7 |
| 3 | F16GP | 7 |
| 4 | F16GPMagnitude | 3 |
| 5 | F16Certificate | 2 |

[data/manifest.json](data/manifest.json) records every declaration's exact
axiom list, source/log/record hashes, resources, and input-context hashes.
All dependencies reported are among propext, Classical.choice, and
Quot.sound, with some declarations using none. All five finished checks
have no errors, warnings, guard stops or swap.
No finished source uses sorry, custom axioms, native_decide or
Lean.ofReduceBool.

The five successful checks took 1.129 seconds total, with peak kernel
RSS 382,488 KiB (373.523 MiB). Lean used -j1 -M200, AS3 GiB, a 480 MiB
RSS clean-stop guard and an 18-second inner deadline. The initial
Init-only probe measured 343,728 KiB RSS. Python/read work used AS150 MiB
and one CPU. No Mathlib imports, LSP, Lake build or long job was launched.
All Lean checks stopped for the parent's announced capacity hold and
resumed only on its explicit release.

The first product draft produced only an unused-section-variable warning;
that warning was fixed before the recorded final check. Its log is retained
in work/. `F16CoreProbe.lean` is an excluded import probe, not a sixth
finished module. The earlier algebra checkpoint is historical.
No frozen prior packet was edited.

## Fresh parent replay

Claim the permitted light slot first; do not run during a parent hold.
From the repository working directory:

```bash
f16_dir=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/protection_models/forced16_lean
/usr/bin/timeout --signal=TERM --kill-after=1 20s \
  /usr/bin/prlimit --as=157286400:3221225472 --core=0 \
  /usr/bin/taskset -c 4 python3 -B "$f16_dir/F16replay.py" \
  --prefix parent-f16-algebra-a
```

The parent Python process has a 150 MiB soft virtual limit, while its Lean
child may use the authorized 3 GiB virtual limit. Every check still has
the 480 MiB RSS guard, heap200 and deadline18s. The script validates source
hashes and all 29 axiom reports, exports only to this directory's work/,
and writes `work/parent-f16-algebra-a-DONE.json`.
Expected time is a few seconds; fresh parent replay is pending at freeze.
Archive replay evidence separately without changing the frozen sources.

