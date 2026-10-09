# A uniform finite factorial saving

[`FactorialSaving.lean`](../../ErdosSzekeres/HMPT/FactorialSaving.lean) proves
that the factorial refinement is strictly stronger throughout an explicit
parameter regime, beyond the earlier single arithmetic example.

Write `K = 4m + 1`, `D = 3m - 6`, and let `E` denote the previous
`HMPT.twoScaleExponent m n d`. For every `m ≥ 3`, Lean proves

`floor(log₂((m+1)!)) ≥ D`.

Consequently, if `2K < E`, then
`HMPT.twoScaleFactorialExponent m n d < E`. The other auxiliary floor, `d`,
is automatically strictly below `E`. The completed theorem
`HMPT.integer_two_scale_bound_one_bit_smaller` says that, if also `n ≥ 4`,
`K ≤ 2^d`, and an auxiliary-polygon bound `ForcesConvexNGon (2^d) K` is available,
then `ForcesConvexNGon (2^(E-1)) n`. Thus the sufficient power-of-two population
threshold is at most half the previous one in this parameter regime.

The auxiliary-polygon input can be supplied by the already formalized Suk bound.
The conclusion concerns arbitrary finite real planar sets in general position.
The auxiliary-floor condition is essential to this strictness statement; the
factorial exponent is only known to be nonincreasing without it.

All six audited declarations use only `propext`, `Classical.choice`, and
`Quot.sound`. See [the audit](axiom-audit.txt) and
[source-bound validation](validation.json). This is an elementary finite
refinement of the repository's counting interface. It does not improve HMPT's
asymptotic leading coefficient or assert literature priority.
