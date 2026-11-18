# Written equivalence argument for compact_cnf.cpp

**PROVED (written argument); finite implementation checks are COMPUTED.**
This note is not an independent author review, a Lean proof, or an m=16
certificate. Default options are `--convex recurrence --pool reduced
--containment witness`. The mode is weak D(5,n) only. No symmetry, orientation
fixing, cube, minimal-counterexample hypothesis, or geometric localization is
used. `--fix-signs` is explicitly conditional and is absent in the delivered
m=16 files.

## Orientation and four-point convexity

Variables 1,...,C(m,3) are lexicographically ordered increasing triples,
true for positive orientation (cup). For each i<j<k<l, let

    (a,b,c,d) = (t(ijk),t(ijl),t(ikl),t(jkl)).

The eight ternary signotope clauses forbid each alternating subsequence
of length three. A Boolean sequence has at most one change iff it has no
alternating subsequence of length three; hence these are exactly the old
encoder's eight forbidden four-bit packets, with shorter clauses.

Q4 is fully equivalent to `(a=b) AND (c=d)`, under the signotope clauses.
Four clauses give Q4 => both equalities. For the reverse direction, the
four clauses `(Q4 OR a OR d)`, `(Q4 OR -a OR -d)`,
`(Q4 OR b OR -c)`, `(Q4 OR -b OR c)` express that `(a=d) OR (b!=c)`
implies Q4. In a one-change packet, a=d forces all four signs equal,
and b!=c forces the pattern a=b!=c=d. Conversely, either convex pattern
has a=d or b!=c. Thus Q4 has its exact value in every model, not just
the canonical assignment.

The no-5-cap clause on each five-set requires some positive consecutive
triple. In a signotope, equal consecutive triple signs force every triple
of a chain to have that sign: on a four-vertex window the first and last
packet signs agree, forcing both middle signs; deleting an internal vertex
preserves the consecutive-sign condition. Repeated deletion proves the
claim. Thus this clause excludes exactly a five-cap.

For real x-ordered general-position points these packet axioms hold, and a
four-set is in convex position exactly when the two stated equalities hold.
A larger finite real set is in convex position iff every four-subset is:
an interior point otherwise lies in a triangle of other points. The existing
`../../encoder_audit/AUDIT.md` sections 3.1--3.4 give the detailed real-point
and abstract cap/cup equivalence arguments. This encoder uses the four-subset
definition directly, without enumerating cap/cup splits or restricting the
upper chain in its convexity clauses.

## Five-child convexity recurrence

For |S|>=5 choose the five smallest vertices E(S). Every four-subset T of S
omits at least one vertex v of E(S). Consequently

    Q(S) iff AND_{v in E(S)} Q(S minus {v}),

where Q means that every four-subset is convex. Both directions are exact:
convexity descends to all children, and every four-subset is tested in at
least one child. The deterministic choice of the five vertices is a cover,
not a symmetry restriction. Choosing only four would not cover the
four-subset consisting of those chosen vertices.

For every size 5,...,n-1, the source defines Q(S) with five binary forward
clauses and one six-literal reverse clause. For each n-set S it emits

    OR_{v in E(S)} -Q(S minus {v}).

Because the child flags are equivalences, this single five-literal clause
expresses exactly no convex n-gon. A merely one-way child definition would
be unsound here: false flags could conceal an actual n-gon. The same
size-(n-1) Q flags serve as weak targets. The optional `direct` version
uses every Q4 subset instead of five children, with the same full
conjunction equivalences.

## Containment witnesses and reduced Delta range

A(S) asserts that S contains a four-cap. At size four it implies the two
negative consecutive triple signs. At larger sizes it implies the OR of
the first five one-point-deletion children. A true node therefore descends
to a genuine cap leaf. Conversely, any four-cap in S avoids one of five
selected vertices, so the exact cap-containment truth values satisfy all
these one-way clauses simultaneously.

B(S) asserts that S contains a convex (n-1)-set. At size n-1 it aliases
the exact Q(S). At larger sizes it implies the OR of the first n deletion
children. Every witness of size n-1 avoids one of these n selected vertices.
The same decreasing-cardinality and canonical-assignment arguments apply.
Masks smaller than a witness size are constant false, never free variables.
The optional `containment exact` adds reverse implications; they follow from
subset containment and preserve the projection onto orientation variables.

The all-pool version requires A(Delta) OR B(V minus Delta) for every mask.
The default needs only 3 <= |Delta| <= m-n+2. To justify the omission:

* A Delta of size below three can be extended to size three. That extension
  contains no four-cap. If its pool clause holds, a target lies in the
  extension's complement, hence also in the original complement.
* A Delta larger than m-n+2 can be shrunk to size m-n+2. The latter's
  complement has size n-2, so its pool clause forces an actual four-cap
  inside the shrink, hence inside the original Delta.

Thus retained failure clauses imply every omitted failure clause at the
level of actual witnesses. Equivalently, any working omitted Delta can
be moved into the retained interval. If that interval is empty, m<n+1;
there is a Delta of size at most three with complement of size at most
n-2. It always works, so the source correctly emits an empty clause.
When m=n+1 the interval contains size three, whose pool clauses are empty.

Only needed A nodes of size <=m-n+2 and B nodes of size <=m-3 are allocated
in reduced mode. Their children remain in these bounds. At m=16 these
are A through size 11/10 for n=7/8, and B through size 13.

## Whole-formula equivalence and claim boundary

A model satisfies precisely the ambient premises. Each retained pool
clause has a true A or B witness, hence a genuine reason that its Delta
fails. The range argument extends that conclusion to every Delta. Thus
the orientation projection is an abstract weak counterexample.

Conversely, take any valid signotope with no working weak Delta. Assign
Q its exact four-subset convexity value and A/B exact witness-containment
truth. All full convexity definitions and ambient premises hold, all
containment implications hold by their cover identities, and every pool
clause holds. This gives a satisfying extension for every abstract or real
counterexample. Hence the unconditioned CNF is SAT iff an abstract weak
counterexample exists. SAT alone does not establish real realizability.

The controls in README check emitted clauses, real integer hulls, every
six-point signotope, and old/new projected Delta-failure queries. They
support implementation correctness but do not replace this argument or
certify either m=16 case. Only a retained matching proof accepted with
the literal cake line `s VERIFIED UNSAT` can certify a frontier CNF.
