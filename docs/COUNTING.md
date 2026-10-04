# Counting experiments and the current benchmark

Research checkpoint: 2026-10-04. No new Erdős–Szekeres upper bound is claimed.

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
hypotheses explicitly. Their geometric justification is not proved here.

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
squared. The optimization over real x and the asymptotic geometric reduction
have not been formalized. This is not a lower bound on ES(n), nor an impossibility
result for other proof strategies. A stronger argument would have to exploit
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

Next computational priority: reproduce ordinary-polygon known cases with the
published Lean encoder, retain solver certificates, then measure the 33-point
instance. A solver's UNSAT verdict and a C proof check are still separate from
a complete Lean-checked geometric theorem in this repository.

## Precise 2020 target

`HMPT/Statement.lean` now defines the published leading coefficient through
an epsilon formulation: for every epsilon > 0, an eventual upper bound with
coefficient 8 sqrt(2)/3 + epsilon. `HMPT.StrictImprovement` asks for some smaller
nonnegative leading coefficient. These are unproved propositions. Reducing a
finite numerical surrogate or an unspecified term inside the published o(1)
does not establish this target.

The current formal work reaches the local geometric ingredients: the
four-point separated-pair test and same-cell replacement step in the proof of
Observation 3.5. The existence and geometry of the spike decomposition remain
unproved; the library does not yet prove either full Suk or full HMPT.
