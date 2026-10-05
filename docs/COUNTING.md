# Counting experiments and the current benchmark

> Status notice, 2026-10-05: this is a historical research log. New research and
> certificate batches are stopped at the user's request. The current proved
> scope is in [README](../README.md), the [paper map](PAPER_MAP.md), and
> [VALIDATION](VALIDATION.md). Any forward-looking steps below are unexecuted.

Research checkpoint: 2026-10-05. No improvement over the published bound is claimed.

## Read the final versions

[Suk, arXiv:1604.08657v2](https://arxiv.org/pdf/1604.08657)
gives an exponent of the form n + 6 n^(2/3) log₂ n for sufficiently large n.
[Holmsen–Mojarrad–Pach–Tardos, arXiv:1710.11415v3](https://arxiv.org/pdf/1710.11415)
improves this to n + (8√2/3 + o(1))√(n log₂ n).
The coefficient 8√2/3 is approximately 3.771236. An older author-hosted draft
does not contain the final two-scale improvement; optimizing against that draft
alone would misidentify an already published improvement as new.

## Exact arithmetic interface

`ErdosSzekeres/Counting.lean` proves a product form of Vandermonde's inequality:

    ∏ choose(aᵢ,bᵢ) ≤ choose(Σaᵢ,Σbᵢ).

In the horizontal-chain budget, put mᵢ = cᵢ−1, d = n−2 and
M = 2(n−1)−k. If Σmᵢ ≤ M, the product is bounded by choose(M+kd,M).
The Lean theorem `combine_budgets` exposes the extraction, part-size, and budget
hypotheses explicitly. The newer `HMPT/` modules derive geometric part-size and
cap budgets for horizontal support paths, with explicit endpoint and padding
losses, and combine them with extraction into a complete finite bound. See
[`HMPT.md`](HMPT.md). Projective normalization also provides a checked one-scale
bridge from general convex-subset counts, allowing the existing Suk theorem to
supply the input density. The sharper two-scale ratio, entropy estimates, and
eventual optimization are now proved in `HMPT.theorem2020` for ordinary point sets.

`scripts/counting_experiments.py` compares this compression with coarser
arithmetic bounds and with balanced allocations under parity budgets. Binomial
products are exact integers; logarithms and numerical minimizers are approximate.
An independent dynamic program checks the balancing formula on small cases.
The beta=4 experiment deliberately drops an asymptotic bootstrap error and is
not a finite-n upper bound. None of these experiments beats the final HMPT result.

## Why simply adding doublings is insufficient

This is our analysis of a restricted leading-order model. Let f_m count convex
m-subsets and D(m)=m log₂N−log₂f_m. Set S=√(n log₂n), m=xS and
log₂N=n+CS. Ignoring lower-order terms, a hypothetical failure to find an n-gon
suggests step constraints of the form

    dᵢ₊₁ − dᵢ ≥ Cx2ⁱ − 1,
    d₀ ≥ 0,  dₜ ≤ (2ᵗx)².

We study these inequalities as explicit assumptions, not established geometric
theorems. Telescoping implies Cx(2ᵗ−1) ≤ 4ᵗx²+t. Minimizing the resulting
coefficient over x>0 gives

    Cₜ² = 4·4ᵗ·t / (2ᵗ−1)².

`ErdosSzekeres/DyadicModel.lean` proves the telescoping inequality and, for every
integer t≥1, 128(2ᵗ−1)² ≤ 36·4ᵗ·t, with equality at t=2. Thus the minimum
squared coefficient in this model is 128/9, exactly the published coefficient
squared. The actual two-scale geometric reduction and its optimal real parameter
are now formalized in `HMPT/Asymptotic.lean`. The all-scale inequality above is
still a restricted model, not a lower bound on ES(n) or an impossibility result
for other proof strategies. A stronger argument would have to exploit
information discarded by this model, or change the counting framework.

## Frontier directions under investigation

- [Baek–Balko, SoCG 2025](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.13):
  the conjectured threshold works for split polygons. The endpoint compatibility
  needed to obtain an ordinary convex polygon is a remaining obstacle; the
  split result does not resolve the original conjecture.
- [Dumitru, December 2025](https://arxiv.org/abs/2512.24061): SAT experiments for
  selected 33-point families. Its suggested coarse four-set indicators and
  shorter seven-set clauses are concrete encoding experiments, not completed proofs.
- [Koshelev–Koshka, April 2026](https://arxiv.org/abs/2604.20120): combine Boolean
  orientation constraints with linear arithmetic after fixing x-coordinates.
  This can produce exact witnesses. UNSAT for one fixed x-grid does not cover
  all realizable configurations.

Known ordinary-polygon cases have now been reproduced and the unrestricted
33-point SAT runs ended UNKNOWN; see `SAT.md`. Current searches include joint
coordinate moves and finite omission constraints. A solver's UNSAT verdict and
a C proof check are still separate from a complete Lean-checked geometric
theorem in this repository.

## Formalized 2020 benchmark

`HMPT/Statement.lean` now defines the published leading coefficient through
an epsilon formulation: for every epsilon > 0, an eventual upper bound with
coefficient 8 sqrt(2)/3 + epsilon. `HMPT.theorem2020` proves that statement for
ordinary real point sets. `HMPT.StrictImprovement` asks for some smaller
nonnegative leading coefficient and remains unproved. Reducing a
finite numerical surrogate or an unspecified term inside the published o(1)
does not establish this target.

The library now proves Suk's 2016 upper bound end to end in
`Suk/Asymptotic.lean`, including global extraction, both geometric cases,
rounding, and the eventual estimate. The four-point separated-pair test and
same-cell replacement step also provide local ingredients relevant to HMPT's
Observation 3.5. The geometric product method, convex-subset ratios, entropy
bound, rounding, and eventual optimization now complete the ordinary-point-set
HMPT bound. The pseudo-configuration and convex-body extensions are outside
this development. A strict improvement remains unproved. See `SUK.md` and
`HMPT.md` for the completed theorems' dependencies and exact scope.

## Mixed-cap strengthening: a checked counterexample

The attempted unconditional addition of a vertical cap and a nonadjacent inner
cap fails. `MixedCap.mixed_cap_budget_counterexample` gives a 22-point real
configuration in general position containing all six support anchors, an
eight-point vertical cap, and an eight-point inner cap. Its largest convex
subset has exactly 15 vertices. The theorem is checked in Lean; an independent
Python replay also exhausts all 74,613 sixteen-point subsets. See
[`MIXED_CAPS.md`](MIXED_CAPS.md) for the coordinates, the 672 triangle certificates,
and the precise geometric hypotheses. Further mixed constraints would need
additional compatibility hypotheses beyond these cap sizes and memberships.

## Simultaneous local product sharpness (2026-10-05)

`scripts/region_blowup.py` constructs small copies of classical cups-caps sets
around the points of another cups-caps set. Exact integer predicates verify
spike membership and the triangle order: distinct clusters are ordered, and
each cluster is an antichain. Thus the region size equals height times width.
On a selected maximum chain and maximum antichain, the measured cap maxima
also attain both local binomials:

    height = choose(a+b−2,a−1), width = choose(c+d−2,c−1).

Here a,b are the left/right cap sizes on that chain, and c,d are the inner/outer
cap sizes on that antichain. These are actual geometric checks on the recorded
examples, not a claim about every maximum chain or antichain in the region.

| a,b,c,d | Region size | Height × width | Largest local convex subset | Largest including anchors |
| --- | --- | --- | --- | --- |
| 2,2,2,2 | 4 | 2 × 2 | 4 | 6 |
| 3,3,2,2 | 12 | 6 × 2 | 6 | 6 |
| 3,3,2,3 | 18 | 6 × 3 | 7 | 7 |
| 3,3,3,3 | 36 | 6 × 6 | 8 | 8 |
| 3,3,2,5 | 30 | 6 × 5 | 9 | 9 |
| 4,4,2,2 | 40 | 20 × 2 | 8 | 8 |
| 4,4,2,3 | 60 | 20 × 3 | 9 | 9 |
| 4,4,3,3 | 120 | 20 × 6 | 10 | 10 |
| 4,4,2,5 | 100 | 20 × 5 | 11 | 11 |

The data are in `experiments/region-blowup-2026-10-05.json`. Maximum convex
sizes use the exact dynamic program; configurations with at most 22 ambient
points also exhaust all subsets one larger than the reported maximum. All
three local product factors can be attained simultaneously in these examples,
but larger polygons also appear. This rules out a strict factor saving from
those local assumptions alone. It does not establish sharpness of the complete
HMPT bound, which also uses global avoidance and replaces some local parameters
by n-dependent bounds. The observed local size a+b+c+d−4 holds for these nine
profiles only; no uniform theorem or stability estimate has been proved.
