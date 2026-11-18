# Parent replay of the generic product/GP algebra

**PROVED, Lean; fresh parent replay PASS.** All five frozen modules and
their29 exact axiom reports were rebuilt and compared with the worker
manifest. Only standard axioms occur. Total child time was1.090s, maximum
RSS382808KiB; all exits were clean with no warning, guard stop or swap.

The checked statements are the generic weighted-product contradiction,
monomial exponent cancellation, the actual coordinate GP identity,
magnitude inequalities, and the conditional GP-certificate composition.
See [the frozen definitions and scope](../forced16_lean/README.md).
This does **not** instantiate the387-row forced16 certificate or its560
signs, and does not compile a Mathlib-Real adapter. The fixed-model written
and exact-arithmetic proof remains a separate result.

The command used a20-second outer timeout, AS150MiB soft/3GiB hard for
the Python wrapper, one-core affinity, and the worker's480MiB RSS guard
and200MiB Lean heap. The fresh prefix was `parent-f16-algebra-a`.
The worker sources and frozen manifest remain unchanged. Their manifest
SHA-256 is `c4e6e0dfc2d3ea417ad1a9c8969948a622d679a5e68899976f27896ba399c362`.
[data](data/) contains the ten fresh logs/receipts, completed replay result
and a snapshot of the checked worker manifest.
