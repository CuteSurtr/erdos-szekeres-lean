# Residual population tradeoff from the completed budget34 tree

14 November2026. **PROVED from the independently replayed EXACT TREE and
the certified geometric row system; not a complete Lean theorem;
unrefereed.** No N5 or N66 capacity theorem is an input to this lemma.

Let R be an actual residual configuration in the existing octagon-free
chart construction: distinct x-coordinates, general position, no6-cap,
no convex octagon, and no6-cup/5-cap junction. Its occupied states are an
injective image O in the154-state residual catalog. Define F by first
height at least5 and Lo by first height at most4. They have84 and70
states, partition the catalog, and state0 belongs to Lo.

**Tradeoff.** It is impossible that both

    |O intersect F| >=65   and   |O intersect Lo| >=55.

Equivalently, at least65 F owners force at most54 Lo owners; at least55
Lo owners force at most64 F owners.

**Proof.** The empty configuration is immediate. For nonempty R, let H
be its missing states. The owner/covering theorems give0 not in H and all
2,650 base inequalities. The812 sound coupled rows give their additional
demand-one inequalities. Every one is a lower bound on the number of
missing states in a fixed support, so remains true when H is enlarged.

The proposed populations imply |H intersect F|<=19 and
|H intersect Lo|<=15. Enlarge the first intersection to exactly19 and
the second to exactly15, without adding state0. This is possible because
F has84 states, and Lo without state0 has69 states. Call the enlarged
set H'. It still satisfies every covering inequality and excludes0.
It has exactly34 elements and satisfies F19 and Lo15. This contradicts
the independently checked slice19 exclusion. Therefore the proposed
populations cannot both hold. QED.

H' is used only as a Boolean assignment to a monotone finite row system.
It need not be the state image of a smaller geometric configuration;
no claim about recomputing labels after deleting points is made.

An independent mathematical review confirmed the padding argument and
checked the catalog partition, state0, and lower-bound form of every
input row; see [the follow-up review](../bridge-followup/README.md).

For any separately established capacities c5,c66 on these owner families,
the tradeoff gives the useful parametric consequence

    |R| <= min(c5+c66, max(64+c66,54+c5)).

Indeed either F has at most64 owners, or Lo has at most54; combine the
other coordinate with its separate capacity. The ordinary sum bound
gives the other term of the minimum. At(65,56) this gives120; at(65,55)
it gives119. The latter is conditional because55 is still unproved.

## Exact dependencies and scope

- Residual catalog, injective owner map, state0 occupancy and2,650
  covering inequalities: existing Lean components and their source
  correspondence audit, as listed in the [bridge memo](../bridge/README.md).
- Full geometric soundness of the coupled-owner encoder: the written
  audit in [VERIFY309, link(c)](../../../VERIFY309N20261113/README.md).
- All812 support CNFs independently reconstructed, retained LRAT hashes
  matched, and fresh literal cake acceptance obtained:
  [pool audit](../audit/pool_summary.json).
- The actual budget34 exclusion, with capacities exactly F19/Lo15:
  [slice19 replay](../audit/s19-summary.json),1,658,483 nodes,
  minimum margin1, all3,643 contexts covered, sole pending branch0missing.
- [Archived proof packet](../data/s19-archive.json), SHA-256
  `586793624172691d00a4c5f364ab29f6b4e4e3cb9e1e21458a93ab4232f3aeee`.

This lemma uses none of the new slice20 cuts, no N5<=65 proof, and no
N66<=56 or hypothetical55 proof. The separate conditional consequence
N66<=55 => ES(8)<=308 still uses the inherited N5<=65 theorem and the
balanced187 composition. With the presently established capacities,
the unresolved120-owner case is F64/Lo56. No improvement of ES(8)'s
upper bound or literature novelty is asserted here.
