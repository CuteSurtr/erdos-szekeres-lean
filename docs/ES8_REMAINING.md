# ES(8) ≤ 317: remaining work

**Status, 2026-10-09: ES(8) ≤ 317 remains unproved. The geometric reduction is
now complete, including all residual cycle and block constraints.** The
finished Suk and HMPT real-point theorems are independent of this research.

The proved steps are the balanced bound 192, the minimum-slope partition,
projective/root transfer, the residual 154-state encoding, and all 1,187
residual row implications. The last group comprises 1,164 cycles and 23 blocks.
For the blocks, the full relevant Baek combinatorial theorem is ported, and its
list boundary is proved to form a real convex polygon using supporting lines.
No geometric row assumption is hidden in `OmissionResidual.all_geometric_rows`.
See [the residual proof map](OMISSION_RESIDUAL.md) and
[check records](../experiments/omission-residual-geometry-2026-10-09/README.md).

| Remaining component | Exact work | Current uncertainty |
| --- | --- | --- |
| Residual arithmetic | Finish all 3,411 parts of the 145,474-leaf certificate, compose every branch, and audit the final exclusion of at most 30 holes. | Independent integer replays pass, but a partial Lean build is not a proof of the root. Part sizes and kernel memory/time vary. The current progress is recorded in the README and linked batch records. |
| Final artifact linking | Finish the fresh `BalancedProof` arithmetic and geometry checks, then compose the two population bounds and audit the closed global theorem. | Historical exports have colliding module names. The balanced exporter and geometry bridge now support a distinct prefix; the complete sources reproduce after import renaming, and fresh checks have begun. Real Lean integration controls pass. See the [assembly and reproduction guide](OMISSION_ASSEMBLY.md). |
| Final verification and review | Run the closed theorem's axiom audit, verify all generated-source bindings, publish reproduction commands, and inspect the resulting statement and provenance. | No closed `ForcesConvexNGon 317 8` theorem has yet passed. |

The exact remaining arithmetic proposition is `OmissionResidual.ExcludesThirtyHoles`
in [ResidualReduction.lean](../experiments/omission-residual-geometry-2026-10-09/ResidualReduction.lean):
there is no Boolean vector on the 154 states satisfying all literal row demands
with total at most 30. The proved `feasible_holes` theorem converts every actual
residual configuration into such a vector, with `sum holes + n = 154`.
`residual_bound_of_arithmetic` therefore proves that this arithmetic exclusion
implies `Partition.ResidualBound 123`.

The already checked balanced bound supplies the other part. The completed
conditional composition is `192 + 123 = 315` chart points, plus one deleted
root: at most 316 points in an avoiding set, hence a forcing threshold of 317.
The two extra units are one root and one strict forcing threshold. The
standalone `forces_317_of_arithmetic` keeps both the separately established
balanced bound and the still-unproved residual arithmetic argument explicit.

**Revised rough size:** the earlier estimate of thousands of further geometric
proof lines is obsolete. No unproved geometric lemma remains in this port of
the reduction. Remaining source work is expected to be certificate integration,
checks and documentation, plausibly hundreds of lines rather than another
geometric development. The dominant cost is generated-proof checking. At the
recent serial rate, the unfinished residual tree is on the order of **40–60
hours of checking on this Mac**, plus a fresh run for whichever family is
renamed for final linking. The recorded complete balanced run took about 6.7
hours; it is smaller than the full residual tree. These are low-confidence
planning estimates, not benchmarks or a completion promise. Kernel resource
failures or an integration bug could increase them. A few days of engineering
and sustained checking is a more appropriate current estimate than the earlier
weeks-to-months geometric port estimate.

The method and source comparison remain Michael Schroeder's
[version-1 archive, 19 September 2026](https://doi.org/10.5281/zenodo.22842891).
The stronger balanced and residual integer certificates target 192 and 123
instead of that archive's 193 and 124. The balanced improvement is fully proved
for its restricted geometric case; the stronger residual target is not yet
Lean-proved. No priority, currently-best-bound, or improvement of HMPT's
asymptotic coefficient is claimed.
