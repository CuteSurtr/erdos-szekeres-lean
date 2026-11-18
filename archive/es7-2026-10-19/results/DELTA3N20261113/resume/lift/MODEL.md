# Model, soundness, and an isolated-alignment obstruction

**PROVED:** the embedding clauses below express exactly an increasing copy of
the old signotope. Combined with the existing universal encoder, they search
all placements of k added points, rather than one chosen interleaving.
No geometric counterexample or universal exclusion is claimed by this note.

## Fixed orientation, free insertion gaps

Let r be the old size and m=r+k. Labels of the extension are in increasing x
order. For old label i, let d_i count inserted points preceding it. Its new
label is i+d_i, with 0≤d_i≤k and d_i≤d_(i+1). Conversely every such sequence
is exactly one increasing r-subset of [m], hence one insertion pattern.

The selector E(i,d) means d_i=d. Its row is exactly one, encoded by one
positive clause and pairwise negative clauses. For adjacent rows, clauses
¬E(i,a)∨¬E(i+1,b), a>b, impose monotonicity. For each i<j<l, and a≤b≤c, add

    ¬E(i,a) ∨ ¬E(j,b) ∨ ¬E(l,c) ∨ s(i,j,l)·t(i+a,j+b,l+c),

where a positive literal t means a positive integer determinant, and s is
the old sign. If selectors choose the embedding, exactly its old triple
constraint becomes active. Every old triple is covered. Conversely, a sign
assignment containing an increasing old copy satisfies all these clauses
by choosing its selectors. An optional fixed-positions list adds units;
without it every one of C(m,k) insertion patterns is included in one CNF.

`extension_cnf.cpp` includes `../../encoder/delta_cnf.cpp` as an unchanged
component, replacing only its executable entry point. That component supplies
signotope axioms, no 5-cap, no convex n-gon, and the full Delta-failure formula
on all 2^m subsets, with lattice witnesses and no symmetry restriction.
Its soundness proof and independent audit are `../../encoder/DESIGN.md` and
`../../encoder_audit/AUDIT.md`. This work does not claim to independently
reimplement or reprove that component. The new implication is the embedding
argument above; controls inspect the actual emitted clauses separately.

The default formula is SAT exactly when a signotope counterexample contains
an increasing copy of the old signotope. A genuine real extension of the
old integer points is included, even with secant alignments or nonlocal
insertions. Abstract SAT may be nonrealizable. A realization need only
preserve old signs; it need not retain the original metric coordinates.
`--embedding-only` and `--base-only` omit the counterexample condition and
must never be reported as counterexample searches. Full-sign pinning is
for controls or explicitly conditional searches.

## Why up to three insertions cannot refute the weak target

Let S have no convex hexagon and Q=S∪A, with |A|≤3. For n≥7, every convex
(n−1)-gon in Q meets A, since otherwise any six of its vertices would be a
convex hexagon in S. A contains no 4-cap by cardinality. Thus A itself is a
weak Delta, regardless of whether Q satisfies the validity assumptions.
The same proof works for signotopes with the hereditary four-subset notion
of convexity. This does not force a lower-chain intersection.

### Stronger n=8 obstruction: all extensions by at most five points

**PROVED.** If S has no convex hexagon, |A|≤5 and Q=S∪A has no 5-cap,
then Q has a weak Delta for n=8. No assumption excluding convex octagons
is needed for this conclusion.

Every convex heptagon in Q contains at least two points of A. It therefore
suffices to choose a 4-cap-free subset R of A omitting at most one point.
For |A|≤3 use all of A; for |A|=4 use any three points. For |A|=5 at least
one four-subset R is not a 4-cap: otherwise every triple of A belongs to a
four-cap and has negative orientation, so A itself is a forbidden 5-cap.
In each case R is 4-cap-free and meets every heptagon. The reasoning is
unchanged for signotopes. This completely removes weak n=8 from the 3–5
insertion search, even though the encoder supports it for general sources.

For weak n=7 with four insertions, two useful necessary conditions follow:
A must itself be a 4-cap, or A is already a weak Delta; and for each a∈A
there must be a hexagon consisting of a and five old points. Indeed the
three-set A\{a} is 4-cap-free, so failure requires a hexagon disjoint from it.
That hexagon cannot be entirely old. These are necessary conditions only;
the current complete formula does not need them as extra assumptions.

## Isolated secant ties do not escape the generic binary sign model

Here the precise hypothesis is an infinitesimal binary family: each old
point is a singleton or has two representatives converging to it, triples
from distinct fibers have the old nonzero signs, all new triple signs
eventually stabilize and are nonzero, and every doubled fiber has a limiting
unoriented pair-line direction. Assume fiber x-intervals are disjoint for
sufficiently small parameter. Orient each pair from its left to right member.

At p, a nonvertical limiting direction can equal the line pq for at most one
other old point q, because the old set is in general position. For every
other fiber, the pair/third-point sign is its strict limiting secant test.
If the direction equals pq and all representatives of q give the same
eventual sign with p's pair, choose one of the two adjacent generic slope
cells that gives that sign. Both cells agree on every other old fiber.
For a vertical limiting direction, no old secant is vertical, and one of
the unbounded cells reproduces all signs. Generic directions already belong
to a cell. Therefore, if no aligned doubled fiber splits the pair/third-point
sign across representatives of its aligned neighbor, every p can be assigned
a generic slope cell reproducing **all** orientation signs of the family.
There are no three-in-one-fiber triples, so these cases exhaust the triples.

In particular, if every secant alignment points to a singleton, the family
has a generic binary representative. To escape that sign model, some aligned
doubled fiber must point to another doubled fiber and distinguish its two
representatives by sign. This is a local necessary condition, not a new
nonexistence proof for all cup-side extensions. The earlier cluster certificates
also imposed their stated projection-transfer coverage; that restriction
must be retained whenever those certificates are invoked.

The sign split is possible. For ε>0 small, use

    p0=(0,0), p1=(ε,ε³), q0=(1,0), q1=(1+ε,ε).

The determinants det(p0,p1,q0)=−ε³ and
det(p0,p1,q1)=ε²−ε³−ε⁴ have opposite signs. The limiting p-pair direction
is the old secant, while the q-pair direction is transverse. Exact integer
versions and a corresponding source15 control are checked by the separate
control program. Their purpose is to demonstrate scope beyond the generic
model; they are not asserted to satisfy the Delta validity assumptions.

No literature novelty claim is made. These local statements are written
arguments and finite controls, with no Lean formalization. The separate
one-insertion CNF certificate is reported in `README.md`.

## Optional exact unit propagation

`unit_simplify.cpp` is an optional preprocessing tool, not used in the
one-insertion certificate. It repeatedly assigns the remaining literal of
an unsatisfied unit clause. Each assignment is entailed by the input plus
previously derived units, hence by the input inductively. At termination
it emits every assigned unit, omits satisfied clauses, and removes false
literals from the others. This preserves precisely the input models, with
variable IDs unchanged. An empty clause detected along the way means a unit
contradiction, but is not itself reported as a certified result.

The Python SAT auditor checks every clause of the **original** CNF even
when the solver used `solve.cnf`. An LRAT produced with this option belongs
to `solve.cnf`; checking it against `case.cnf` would be incorrect. The runner
records `proof_cnf` explicitly. Independent tiny truth-table controls compare
all 4,096 assignments across 64 formulas, including duplicate literals,
tautologies and empty clauses. A simplified copy of the original real cup15
control also passes the original-CNF and independent geometry audits.
