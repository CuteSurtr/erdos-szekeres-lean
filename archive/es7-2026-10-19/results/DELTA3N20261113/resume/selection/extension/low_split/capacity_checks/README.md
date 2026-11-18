# Checked geometric capacity specializations

**PROVED, Lean.** Both unchanged draft sources compile successfully under
Lean4.24.0. All five axiom reports use only `propext`, `Classical.choice`
and `Quot.sound`, with no warning, error, resource stop or swap in the
successful run. The source comments describing their pre-check status
are historical; this separate receipt records their completed checks.

For every actual ordered real `Configuration n`, the conclusions are:

* no four-cap and no convex hexagon imply n<=11;
* no four-cap and no convex heptagon imply n<=16.

These specialize the existing Baek theorem, using parameters3 and4:
the thresholds are binomial(5,2)+2=12 and binomial(6,2)+2=17.
They are not new numerical bounds. The generic `hasNGon_real` bridge
reuses the existing boundary construction at arbitrary cardinality q,
so the conclusions use the repository's actual `HasConvexNGon` predicate.
`Configuration` requires strictly increasing x coordinates and nonzero
triple determinants; there is no extra realizability hypothesis.

| Source | SHA-256 | Axiom reports |
|---|---|---:|
| [Capacity16.lean](../Capacity16.lean) | `8d5ced5ab84da9ba9347bc4fd1f99952dfa876302c35a712e9e8fec284a003d3` | 3 |
| [Capacity11.lean](../Capacity11.lean) | `d34ad0ecbcba8a507e71c43b2d54e9a887e9362f1f9d265ae7fa8efcb9296156` | 2 |

The [successful receipt](pass/result.json) pins source/olean pairs for57
local transitive dependencies, the Lean binary, toolchain and checker.
It checks these dependencies before and after both sequential builds.
Capacity11 imports the Capacity16 olean freshly produced in the same
exclusive output directory. Both completed sources contain no sorry,
custom axiom, native_decide or ofReduceBool.

The complete checks took2.890s. Maximum sampled RSS was3,111,920KiB,
predominantly file-backed imports; swap was zero. The unit
`nov13c-vfy-delta6-capacity-b` used CPU100%, nominal MemoryMax6000M,
MemorySwapMax0, Runtime240s, AS6GiB and an independent4500MiB RSS guard.
Every child had a27-second CPU/wall deadline and one-core affinity.
The other verifier reservations were reduced before this allocation;
the shared6000MiB owner budget was not raised. The unit is now inactive.

The earlier3000MiB RSS attempt stopped itself cleanly before producing
a theorem. Its original driver, logs and receipt are retained in
[attempt-rss3000](attempt-rss3000/result.json). It is not a Lean rejection
or a kernel OOM. The successful allocation was made only after two other
solver reservations had ended.

Reproduction uses [capacity_check.py](../capacity_check.py) with a fresh
`--prefix` and `--rss-mib=4500`, after reserving that memory inside the
shared cap. The exact commands and logs are in the successful packet.

Together with the independently audited T6(L) coverage through left11,
the first capacity bound closes **T6(L) for every admissible left set**.
This composition uses written reductions and finite certificates; it is
not itself a fully Lean-formalized selector theorem. The second capacity
bound reduces universal T7(L) to left sizes through16; its left16 finite
obligation remains separate.
