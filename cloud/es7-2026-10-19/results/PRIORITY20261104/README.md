# Priority check for the fivefold and sixfold obstructions

4 November 2026. Follow-up to `ROTREFINE20261104`, commit
`1e48cad8d7e7254a44a5104e3db4e9114032d9e4`.

## Assessment

**Evidence only — bounded literature inspection and research assessment.**
No matching prior result was found in the sources inspected for either exact
witness. This does not establish priority. Both belong to established methods
for disproving geometric realizability. The sixfold example remains the more
promising specific contribution; the fivefold identity has a short elementary
derivation, recorded and exactly checked in this review.

| Finding | Established antecedent | What remains unmatched here |
|---|---|---|
| Sixfold, sixteen signed areas on five orbits | Polynomial/semidefinite infeasibility certificates; geometric symmetry obstructions | This sparse prescribed-C6 witness, with its exact feasible linear lift and acyclic directed product graph |
| Fivefold, eight signed areas on four orbits | Linear combinations of determinant identities; elementary regular-pentagon relations | This particular forbidden sign pattern and its application to the retained candidate |

The comparison is limited to the precise relaxations actually tested. Neither
finding currently supports a claim of a distinct general method, a separation
from every biquadratic final-polynomial method, or an improved extremal bound.

## Sixfold: the broad idea has precedents

**Evidence only — source inspection.** Parrilo's semidefinite hierarchy already
provides polynomial infeasibility certificates based on sums of squares.
The campaign's positive weighted sum of required signed areas equalling a
negative-definite quadratic form fits this established certificate framework.
This classification is an inference from the form of our proof, not a claim
that the paper contains our coefficients. [Parrilo (2003), DOI
10.1007/s10107-003-0387-5](https://doi.org/10.1007/s10107-003-0387-5).

**Evidence only — source inspection.** SDP nonrealizability testing was already
applied to oriented matroids by Miyata, Moriyama and Imai in 2009. Fukuda,
Miyata and Moriyama review that work and compare methods; their complete small
classifications show that all nonrealizable members of the three classes they
classify admit biquadratic final polynomials. Those finite classifications do
not imply a universal dominance result for all SDP formulations, and do not
classify our sixty-point example. [Fukuda–Miyata–Moriyama,
arXiv:1204.0645v2, introduction, Theorem 1.1 and reference 36](https://arxiv.org/html/1204.0645v2).

**Evidence only — source inspection.** Richter-Gebert exhibited a realizable
rank-three oriented matroid with a combinatorial symmetry admitting no metric
realization, and a related nonrealizable matroid with no biquadratic final
polynomial. Thus both broad phenomena were already established in 1996.
[Richter-Gebert, DOI 10.4171/DM/7](https://ems.press/journals/dm/articles/8964949).
Miyata gives further symmetry theory and antecedent credit in
[arXiv:1301.6451v5, introduction and Section 3](https://arxiv.org/html/1301.6451v5).

**Exact computation plus written proof — previously checked, not replayed in
this literature pass.** Our retained model0033 has a strictly feasible exact
rational lift for every signed-area linear inequality, while sixteen positive
weights produce a negative-definite seed-coordinate quadratic form. Hence the
specific linear relaxation cannot exclude it and the quadratic test does.
The complete directed product-vertex graph is acyclic. See
[the retained argument](../ROTREFINE20261104/quadratic_bounds.md).

**Written proof — reviewed, not refereed.** Acyclicity is weaker than absence
of all biquadratic final polynomials. In the full method, products can cancel
by balancing exponents of individual bracket variables; cancellation need not
follow a cycle of identical two-bracket product vertices. The general LP
method and its symmetry reduction already appear in
[Bokowski–Richter (1990), DOI 10.1016/S0195-6698(13)80052-2](https://www.sciencedirect.com/science/article/pii/S0195669813800522).
We have not run that complete comparison on this model.

Furthermore, the campaign has not proved an asymmetric realization of the
same abstract order type. Its exclusion therefore does not itself establish
a symmetry gap within the class of realizable oriented matroids. The proved
statement concerns the prescribed Euclidean rotational action.

## Fivefold: the identity simplifies to elementary relations

**Written proof plus exact computation — independently checked, not refereed.**
The weights in the eight-area witness normalize from
`A=13-3 sqrt(5)`, `B=13 sqrt(5)-15`, `C=5 sqrt(5)-1` to
`B/A=sqrt(5)` and `C/A=(1+sqrt(5))/2`. Three short identities for a regular
pentagon's rotation matrix, followed by determinant bilinearity, derive the
entire formula. The [derivation](FIVEFOLD_DERIVATION.md) includes the actual
eight triangles. An independent formal expansion over `Q(sqrt(5))` passes
all eleven checks; see `check_fivefold.py` and `check_fivefold.json`.

**Evidence only — research assessment.** This elementary derivation weakens a
claim of substantial standalone theoretical novelty. It does not demonstrate
that the exact formula was previously published, or that the earlier short
clause families already imply its sign clause. Selecting a useful support,
binding its signs to an abstract candidate, and deriving its rotation lifts
remain concrete contributions to this computation. The retained source
passes all GP relations and the directed cycle test, but this does not resolve
the broader BFP comparison.

## Recent application literature

**Evidence only — source inspection.** The following primary texts were
checked for matching methods or witnesses:

- Subercaseaux, Mackey, Qian and Heule, **arXiv:2506.00224v1**, Sections 3–6:
  rotational SAT encodings, local-search realizations and exclusions via small
  unrealizable subconfigurations already occur. No matching eight-area or
  sixteen-area witness was located. [Primary text](https://arxiv.org/html/2506.00224v1).
- Krapivin, Przybocki and Heule, **arXiv:2607.02958v1**, Sections 4 and 7:
  SAT–realizability interaction and prior SAT+CAS theory-lemma learning are
  described. The generic refinement pipeline is established practice.
  [Primary text](https://arxiv.org/html/2607.02958v1).
- Dumitru, **arXiv:2512.24061v1**, methods and Table 1: layer-template SAT
  experiments, without a matching cyclic area or Gram obstruction in the
  inspected text. [Primary text](https://arxiv.org/html/2512.24061v1).
- Koshelev and Koshka, **arXiv:2604.20120v1**, Section 5.2: fixing abscissae
  gives a different linearization. No matching rotational witness was located.
  [Primary text](https://arxiv.org/html/2604.20120v1).

## Search limits and next discriminating checks

**Evidence only.** Searches combined oriented matroids, realizability,
rotational/cyclic symmetry, signed areas, pentagons, sixfold octagon avoidance,
semidefinite programming, Gram matrices, sums of squares and final
polynomials. Exact titles, authors and references were followed. No exhaustive
isomorphism/minor comparison with published obstruction databases was made.
An arbitrary relabelling or algebraic reformulation will not necessarily be
found by text search.

The full 2025 Mackey thesis was not obtained. It is identified in reference 13
of arXiv:2506.00224; its absence remains a priority-check gap. The full Pacific
Journal of Optimization 2009 article cited in arXiv:1204.0645 was not obtained.
A particularly close inspected lead is Miyata, Moriyama and Imai,
“Analyzing automorphism groups of oriented matroids by semidefinite programming,”
RIMS Kokyuroku 1641 (2009), 8–15. It explicitly treats symmetric-realization
SDP and studies Richter-Gebert's example. Kyoto's authoritative metadata lists
Handle `2433/140589`, with no DOI field. No arXiv identifier was found. Its
location is retained in `SEARCH_RECORD.json`; it is separated from the formal
DOI/arXiv bibliography to respect the requested citation rule. The broad-method
assessment above is independently supported by the DOI/arXiv sources.

The most discriminating mathematical follow-up is a complete BFP comparison
on the sixfold witness, followed by comparison of its reduced support with
known obstructions. A general structural family, a smaller conceptual proof,
or a proved extremal improvement would establish significance more clearly
than the existence of one additional certificate. These are recommendations,
not computations performed in this review.

The appropriate current description is: **explicit, independently checked
rotational obstructions using established algebraic methods; no matching
published instances found in the inspected sources; priority unresolved.**
