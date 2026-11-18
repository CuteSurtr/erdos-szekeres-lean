# A finite test for one Delta chosen before every rightward X

**PROVED** below means written proofs, not Lean formalization. Coordinate
controls are separate COMPUTED results. No universal existence theorem or
counterexample to weak D(5,7), D(5,8), or uniform-envelope selection is claimed.
The breakpoint test was already used in `../../terminal/SOUNDNESS.md`;
the interval formulation, two-line certificates and quantifier accounting
below make the exact finite selection problem explicit.

## 1. Order of quantifiers

Fix a nonempty finite point set U with distinct x-coordinates and no
collinear triples. Put M=max_x(U), k=n-1, and let H be all convex k-subsets.
For an ordered pair b<c write its line as

    ell_bc(M+t) = s_bc t + z_bc,       t>0.

Let L be the finite set of terminal lines of ambient four-caps and
F(t)=max_{l in L} l(t), with max(empty)=-infinity. A uniform solution means

    exists A subset U: A is a weak Delta in U AND
                      for every t>0, F3(A;M+t) <= F(t).                 (U)

Here A is chosen after U and before t. This differs from
`for every t>0 there exists A_t`, and from choosing A after the entire
insertion r=(M+t,Y). Neither quantifier interchange is licensed by an
existence result for individual rooted instances.

If U has no five-cap, (U) is equivalent to the existence of one old weak
Delta A such that A+r is a weak Delta for **every** general-position
rightmost insertion preserving five-cap-freeness. Sufficiency is the prior
threshold lemma. Conversely, if some triple line q of A exceeds F(t),
choose Y strictly between them, avoiding the finitely many old secants.
Then U+r has no five-cap but this triple extends to a four-cap. If L is
empty choose any sufficiently low Y<q(t), again avoiding the secants.
There is no no-n-gon restriction on these test insertions. Restricting r
to preserve no-n-gon can destroy this necessity; the envelope remains a
sufficient condition for those restricted insertions.

## 2. Line-dominance reduction and exact exposure intervals

Call a cap triple T=(a,b,c) **exposed** when its terminal line q=ell_bc
exceeds F somewhere on t>0. Its exposure set is

    I(q) = {t>0 : q(t)>l(t) for EVERY l in L}.

**Lemma 1.** I(q) is an open interval (possibly empty or unbounded).
Write q=(s,z) and each l=(u,w). If u=s and w>=z for some l, I(q) is empty.
Otherwise put

    alpha = max({0} union {(w-z)/(s-u) : u<s}),
    beta  = min({+infinity} union {(w-z)/(s-u) : u>s}).

Then I(q)=(alpha,beta) if alpha<beta, and is empty otherwise. A pair
supporting several cap triples is tested only once. If L is empty every
cap triple is exposed, with interval (0,+infinity).

**Proof.** Each strict inequality is `(s-u)t> w-z`. A smaller ambient
slope imposes the stated strict lower bound; a larger slope imposes a
strict upper bound; an equal slope either forbids all t or imposes no
restriction. Intersect these bounds with t>0. QED.

For rational coordinates all finite endpoints are rational. A nonempty
interval gives a small exact counter-witness: its midpoint if bounded,
or alpha+1 otherwise. Equality at an interval endpoint is not exposure.

Equivalently, q is safe on the entire half-line iff q(0)<=F(0), q(t)<=F(t)
at every positive breakpoint of the upper envelope F, and s is at most
the largest ambient slope. On each intervening interval F-q is affine;
on the last ray the slope condition is necessary and sufficient once its
initial value is nonnegative. Continuity justifies testing t=0 although
the domain is open. If L is empty use the separate convention above.
Testing only t=0 and the final slope is generally insufficient when F has
interior breakpoints.

**Lemma 2 (at most two supporting lines).** For nonempty L, q is safe iff
one of the following holds:

1. Some ambient line has u>=s and w>=z.
2. There are ambient lines l_-=(u_-,w_-), l_+=(u_+,w_+) with
   u_-<s<u_+ and a rational weight (for rational inputs)

       lambda=(u_+-s)/(u_+-u_-)

   such that lambda*w_-+(1-lambda)*w_+ >= z.

Thus safety has a certificate of one line, or a convex combination of two
lines, whose slope and height at M dominate those of q.

**Proof.** Either certificate dominates q for every t>=0, and its convex
combination never exceeds max(l_-,l_+)<=F. Conversely assume I(q) empty.
An equal-slope obstruction is case 1. A larger-slope line producing
beta<=0 is also case 1. In the remaining case beta>0, and alpha>=beta
must be attained by a smaller-slope line and a larger-slope line. Set
a=s-u_->0, b=u_+-s>0. Their bound endpoints are
alpha=(w_--z)/a, beta=(z-w_+)/b. At the displayed weight,

    lambda*w_-+(1-lambda)*w_+ - z = ab/(a+b)*(alpha-beta) >= 0.

This is case 2. The sets are finite, so finite extrema are attained. QED.

No LP solver is needed. This statement is for arbitrary finite line
families; no claim is made that every algebraic example is realizable by
the cap terminal lines of a valid point set.

## 3. Exact finite combinatorial characterization

Let B be the cap triples with nonempty I, and C the ambient four-caps.

**Theorem 3.** A uniform old weak Delta exists iff this finite Boolean
formula is satisfiable, with z_v meaning v belongs to A:

    AND_{H in H} ( OR_{v in H} z_v )
    AND_{C in C} ( OR_{v in C} not z_v )
    AND_{T in B} ( OR_{v in T} not z_v ).

**Proof.** The first two families say precisely that A is a weak Delta.
The third forbids every cap triple whose terminal line exceeds F at any
rightward abscissa. Since F3(A) is the maximum of these triple lines,
this is equivalent to its domination at every abscissa, with the same A.
The empty-family conventions include an empty A and an empty L. QED.

Equivalently the blue complement B0=U minus A must hit every four-cap and
every exposed triple, while containing no entire target polygon. This is
a finite colored-hypergraph condition once coordinates are fixed. The
line comparisons require more than simply identifying terminal ranks;
no claim is made that the extra data depend only on triple orientations.

For five-cap-free U every exposed triple ends on a pair of ambient cap
rank exactly three: rank four would put its own line in L and preclude
exposure. The converse fails on the prior 18-point terminal fixture.
In particular, substituting ALL rank-three triples for B changes the
problem to the already refuted terminal-safe selection rule.

The four-cap family must be retained. For example take the seven points

    (0,0),(1,3),(2,5),(3,6),(4,100),(5,120),(6,130).

The first four form a cap. No five-cap exists: every mixed cap has at most
one point in the first block, because its internal slopes are <=3 whereas
every cross-block slope is >20; the last block has only three points.
The last edge (5,120),(6,130) ends a four-cap obtained by prepending any
first-block point to the last three. Its line has slope 10 and value 130
at M=6. Every terminal line of a triple in the first four has slope <=5/2
and value <=31/2 there. Thus that four-cap itself passes the envelope
test. Its complement has three points, so it even meets every target of
size >=4; failure is exactly its old four-cap. The construction is in
general position by the same strict slope separation and direct within-
block turns. Envelope domination alone does not remove old four-caps.

## 4. A finite set of common tests and a useful repair condition

**Lemma 4 (common tests).** For each exposed terminal pair choose one
abscissa M+t inside I(q). A fixed A is uniform iff it is a weak Delta and
passes the envelope inequality at every one of these chosen abscissae.
At most binomial(|U|,2) tests are needed; if B is empty none are needed.

**Proof.** A uniform A passes every test. If A contains an exposed triple,
the test chosen for its terminal pair fails. QED.

This is `exists A, for every test`, a single simultaneous selection
problem. Solving the tests separately only establishes `for every test,
exists A_test`. For a complete **pointwise** assessment, the finite
endpoints of all exposure intervals partition the half-line into cells;
the forbidden-triple set is constant on each open cell. Test one point
per cell and, if desired, the finite endpoints separately. This does not
replace the union B used by Theorem 3.

**Lemma 5 (uniform deletion repair).** Let A be any old weak Delta, and
let B[A]={T in B:T subset A}. For R subset A, A minus R is uniform iff

    R hits every T in B[A], and
    no H intersect A, H in H, is contained in R.

Consequently it suffices to find a transversal R of B[A] of size t such
that every old target has at least t+1 selected vertices in A.

**Proof.** Deletion preserves four-cap-freeness. It removes all exposed
triples precisely when R hits B[A], and preserves old target coverage
precisely when no old support is deleted entirely. The numerical condition
ensures the latter. Apply Theorem 3. QED.

This is a useful next selection condition: obtain an ordinary weak Delta
whose **union of actual exposure blockers over all X** has a small
transversal compared with its polygon-hit multiplicities. It is strictly
less restrictive than demanding ambient rank four for every terminal
pair and needs no promise that a particular rightmost insertion preserves
no-n-gon. A private-hit exposed triple blocks deletion-only repair of
that A; it does not rule out another old Delta or old-point recoloring.
The lemma generalizes the prior fixed-insertion repair test by taking
the union of blockers BEFORE choosing the repair. No theorem asserting
that this condition can always be achieved is claimed.

## 5. Scope and remaining work

The new boundary fixtures refute the parent's cup/complement shortcut,
not weak Delta. That separate result is not used in the proofs above.
The useful output here is the exact union-of-exposures hypergraph, small
rational certificates for each allowed or forbidden pair, and the
simultaneous repair condition. Finite positive fixtures cannot establish
universal favorable selection. A negative SAT status would still need a
retained cake_lpr proof with exactly `s VERIFIED UNSAT` and a geometry/
clause audit before being called CERTIFIED. UNKNOWN is not evidence.
