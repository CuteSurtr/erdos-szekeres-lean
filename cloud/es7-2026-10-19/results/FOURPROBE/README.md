# FOURPROBE: hardness of the fourfold threshold for convex octagons (4 November 2026)

**Context.** The best fourfold octagon-free set has 52 points (13 layers); the threshold instance is m4K8t17 (68 points).

**Results.** Every solver run hit its time limit, so all of these are evidence only.

| Instance | Limit | Result | Conflicts | Conflicts/s |
|---|---|---|---:|---:|
| m4K8t15, plain | 600 s | unknown | 2.11M | 3,831 |
| m4K8t16, plain | 600 s | unknown | 2.10M | 3,569 |
| m4K8t17 cube c11111 (1<2<3<4) | 2,140 s | unknown | 6.97M | 3,385 |
| m4K8t17 cube c11100 (1<4<2<3) | 955 s | unknown | 3.77M | 4,023 |

- **Where the plain encoding stops.** It switches from SAT (t = 14, abstract model) to unknown between 14 and 15.
- **Comparison with 6-fold.** Every 6-fold cube finished within 2,068 s. c11111 was still open at 2,140 s with no visible
  progress, so a 4-fold cube likely needs well over an hour with this split.

**Exact computation.**
- **Cover.** The t = 17 split (Y(1,2) plus 32 cubes on the phase order of layers 1–4) passes `verify_cover.py`, and all 4
  mutant tests are rejected.
- **Impossible patterns.** The 20 patterns that violate transitivity each falsify a base transitivity clause. Their
  one-step LRAT refutations pass lrat-check; cake_lpr was not run.

**Reflection unit for m = 4 (evidence only).** The 52-point set and its mirror satisfy all clauses of m4K8t13, and Y(1,2)
toggles. This uses 90-digit arithmetic; the argument is `C6UPPER` §2, which covers every even m.

**Next step.** Finer splits, for example also on the order of ψ₅, with the cover check extended to match.

The CNFs regenerate from `C7UPPER/gen.py` (t17 `4843a9e9…`). The timed-out proofs were deleted.
