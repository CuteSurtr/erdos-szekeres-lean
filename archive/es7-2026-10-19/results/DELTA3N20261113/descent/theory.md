# Saturated-endpoint exchange and its coverage obstruction

Theory/descent track, 13 November 2026. **No Delta conjecture is proved here.**
PROVED labels below mean written arguments, not Lean formalizations. The main
outputs are:

* **PROVED:** a complete-fan dichotomy for doubly hard type-4 cups, a cap-safe
  exchange under an explicit endpoint hypothesis, and an exact bounded
  obstruction criterion for one-point exchanges.
* **COMPUTED, exact integer witnesses:** the cap-safe exchange can lose an
  already hit type-2 cup, even with a unique helper. There are examples with
  10 points for n=7 and 11 points for n=8. An independent hull-based checker
  verifies every geometric hypothesis.
* **HEURISTIC as general evidence:** the more flexible conditional exchange
  E1 below survives the small checks made here. It is **OPEN**, not PROVED or
  CERTIFIED. The parent's 16-point minimum-transversal example has no eligible
  saturated right endpoints, so its E1 check is vacuous.

All new files of this track are in this directory. No old record, main README,
math.md, branch, commit, or remote was changed. No systemd job or long
computation was launched. Every search used the prescribed Python, one thread,
and a wall-time cap at most 20 seconds. The three solver calls had 8-second CPU
limits and 512 MiB address-space limits; all finished immediately. No UNSAT
result in this directory is labelled CERTIFIED.

## 1. Setting and precise target

Throughout, S is a finite **real** point set in general position with distinct
x-coordinates, no 5-cap, and no convex n-gon, with **n in {7,8}**. Indices and
inequalities are in increasing x-order. Both endpoints belong to every chain.

Write C(u,v), U(u,v) for maximum cap and cup lengths with endpoints u<v.
A cap and a cup with the same endpoints have disjoint interiors and their
union is in convex position. Consequently C(u,v)+U(u,v)<=n+1. Equality defines
a saturated pair; its longest cups are exactly the lower sides of convex
(n-1)-gons. Let F be the family of these lower sides, with duplicate cups
removed. A member D of F has type c=C(min D,max D), and |D|=n+1-c.
Here c is 2, 3, or 4. The type-2 members of F are exactly the (n-1)-cups.

Let Q be the points starting no 4-cap, and Q' the points ending no 4-cap.
Both are 4-cap-free. Put

    H(v) = {h : (v,h,y,z) is a 4-cap for some y,z},
    L(u) = {ell : (x,y,ell,u) is a 4-cap for some x,y}.

These are sets of **all** helpers, not a chosen helper per endpoint.

**E1_3 (OPEN, only n=7,8).** Suppose A is 4-cap-free, meets every type-2
member of F, D is a type-3 member of F disjoint from A, and v=max D starts
a 4-cap. There exist p in D and R contained in A, |R|<=1, such that

    B = (A minus R) union {p}

is 4-cap-free and meets every member of F already met by A.

The analogous **E1_4** has type 4 in place of type 3 and is a separate OPEN
statement. In particular its hypotheses do not silently include the extra
left-end saturation hypothesis of Lemma F4 below.

This is a global exchange statement allowing interior insertions, arbitrary
deletion positions, and cardinality increase when R is empty. It is not a
rule that prescribes a polygon endpoint. If E1 applies, the set of hit cups
strictly increases, because D becomes hit and none is lost.

**Scope limitation.** E1 only concerns cups whose right endpoints start
4-caps. Other missed cups need another argument. Replacing A by B need not
leave A inside Q or inside a single cap-free layer. Thus E1 alone would not
merge the three layers or prove the cup-side conjecture. No statement here
asserts E1 for n=6. The parent's newly reported abstract n=6 cup-side failure
is not contradicted by any proved result below; this track has not verified
or used that model.

## 2. What endpoint saturation really forces

The only geometric extension fact used is DELTA2N Lemma 1: if
(v,h,y,z) is a 4-cap, then (t,v,h) is a cup for every t<v. Otherwise
(t,v,h,y,z) would be a 5-cap. The reflected assertion applies to L(u).

### Lemma F3 — forced right fan, type 3 (PROVED)

Let D:u->v have type 3, let H(v) be nonempty, and suppose A misses D but
hits every (n-1)-cup. Then:

1. For every h in H(v), Dh is an (n-1)-cup and a type-2 member of F.
2. H(v) is contained in A intersect Q.
3. L(u) is empty, so u belongs to Q'.
4. For h<h' in H(v), (v,h,h') is a cap.

**Proof.** D has n-2 vertices. Extension gives the cup Dh of length n-1.
If C(u,h)>=3, its union with a 3-cap on the same endpoints would be a convex
n-gon; hence C(u,h)=2 and Dh is type 2. Since D misses A, hitting Dh forces
h into A. If h started a 4-cap, extending Dh once again would give an n-cup,
so h is in Q. If ell belonged to L(u), extending at both ends would give
the n-cup ell D h, a contradiction. Finally, a cup (v,h,h') would give the
n-cup Dhh'. General position therefore forces that triple to be a cap. End.

Items 1-3 sharpen the bookkeeping of DELTA2N Lemma 5; they do not say that
hits at helpers can be transferred to D.

### Lemma F4 — complete-fan dichotomy, type 4 (PROVED)

Let D:u->v have type 4, with L(u) and H(v) both nonempty. Suppose A misses
D and hits every (n-1)-cup. Then

    L(u) is contained in A  OR  H(v) is contained in A.

Moreover L(u) is contained in Q', H(v) is contained in Q, and every cup
ell D h, ell in L(u), h in H(v), is a type-2 saturated cup.

**Proof.** D has n-3 vertices. The extension fact at its two ends produces
ell D h, of length n-1, for every pair (ell,h). It is saturated of type 2
by the same no-n-gon argument as F3. Since D misses A, each pair satisfies
ell in A or h in A. If L(u) is not contained in A, choose one ell outside
A. This single ell forces every h into A. Otherwise the first alternative
already holds. A right helper h cannot start a 4-cap, since that would extend
ell D h to an n-cup. The assertion for a left helper is its reflection. End.

This is the bounded information available without assuming that a one-sided
type-4 extension remains saturated. For a merely right-extendible type-4
cup, Lemma 5 only gives C(u,h)<=3; equality is needed for Dh to be a
saturated type-3 cup. A drop to 2 can leave slack. F4 avoids that gap by
using both ends, and explains why whole helper sets in the two outer
cap-free layers become selected.

## 3. A cap-safe exchange, with its exact missing hypothesis

Say that A has the **right endpoint condition at v** when every 4-cap K
containing v with K minus {v} contained in A starts at v. A sufficient
condition is A contained in Q and v outside A: any other first vertex
would lie in Q and start a 4-cap, impossible.

### Lemma X — fan deletion is cap-safe (PROVED)

Let A be 4-cap-free, v outside A, and assume the right endpoint condition
at v. Then

    B = (A minus H(v)) union {v}

is 4-cap-free. If A misses a cup D ending at v, B hits D.

**Proof.** A hypothetical 4-cap in B must contain v, because A is
4-cap-free. By the endpoint condition it starts at v. Its second vertex
therefore belongs to H(v), but every such vertex was removed. Contradiction.
The final assertion follows from v in D intersect B. End.

The mirror exchanges L(u) for u. Lemmas F3/F4 identify cases in which the
whole deleted fan is already selected. Neither the endpoint condition nor
membership in one cap-free layer follows for arbitrary later exchange
states; it must be maintained or rechecked.

Coverage has a separate, exact condition. Define

    P_A(H) = {C in F : empty != C intersect A is contained in H}.

These are the cups whose entire current support is deleted. The exchange
of X preserves every previously hit cup **if and only if** every C in
P_A(H(v)) contains v. This equivalence follows directly by taking the
intersection of C with (A minus H(v)) union {v}. It is not supplied by
Lemma 5, even when H(v) has just one vertex.

## 4. Explicit obstruction to transferring coverage down the fan

**COMPUTED, exact integer witness; not a counterexample to E1 or Delta.**
The files `fan_obstruction_n7.json` and `fan_obstruction_n8.json` give the
following small examples. `verify_obstructions.py` independently checks
them with all-triple cap/cup tests and enumeration of convex hulls; it uses
neither the extraction DP nor a SAT solver. Its output is
`verify_obstructions.json`.

### n=7, ten points

In x-order the points are

    0=(-62,83)   1=(-37,17)  2=(-32,75)  3=(-11,-42)
    4=(19,-80)  5=(21,-80) 6=(31,-86)  7=(34,64)
    8=(56,92)   9=(70,95).

Set

    A = {7,8,9},             D = (0,1,3,4,5),
    upper cap = (0,2,5),     v = 5,
    H(5) = {7},              B = {5,8,9}.

The complete 4-cap list is (i,7,8,9), i in {3,4,5,6}. In particular
Q={0,1,2,7,8,9}, A is contained in Q, H(5) is exactly the displayed
singleton, and (5,7,8,9) supplies the required endpoint 4-cap.

The complete list of 6-cups consists of

    (0,1,3,4,5,h), (0,1,3,4,6,h), (0,1,3,5,6,h),
    for h in {7,8,9}.

Thus A hits every type-2 cup and misses D. But the type-2 cup

    C = (0,1,3,4,6,7)

has C intersect A={7} and C intersect B empty. The cap-safe exchange loses
an already hit cup of the very lowest cap type.

For an auditable validity certificate, the exact checker finds 120 nonzero
triple determinants, the four 4-caps above, no 5-cap, and no convex 7-gon.
The no-7-gon conclusion can also be reduced to the short chain lists:

* There is no 7-cup, since every 6-cup starts at 0, whereas deleting the first
  vertex of a 7-cup would yield a 6-cup with another start.
* The endpoints of every 6-cup are (0,h), h=7,8,9, with C(0,h)=2, so none
  can be the lower side of a (3,6)-gon.
* The only possible upper 4-caps have endpoints (i,9), i=3,4,5,6. The
  corresponding maximum cup lengths are respectively 4,3,3,2, all below 5.

These exclude all upper-chain types 2,3,4 of a 7-gon. The same exact signs
give C(0,5)=3 and U(0,5)=5, so the missed cup D has the required saturated
type 3, not merely the right number of vertices.

### n=8, eleven points

Insert (-50,50) between the old points 0 and 1 and relabel in x-order:

    0=(-62,83)  1=(-50,50)  2=(-37,17)  3=(-32,75)
    4=(-11,-42) 5=(19,-80) 6=(21,-80)  7=(31,-86)
    8=(34,64)   9=(56,92) 10=(70,95).

Now use

    A={8,9,10},              D=(0,1,2,4,5,6),
    upper cap=(0,3,6),       H(6)={8},
    B={6,9,10},              C=(0,1,2,4,5,7,8).

There are 165 nonzero triple determinants. The complete 4-cap list is
(i,8,9,10), i=4,5,6,7; there is no 5-cap. There is no convex 8-gon:
deleting the inserted point from one would leave a convex 7-gon in the
old ten-point set; an 8-gon not using it is impossible for the same reason.
The independent checker also enumerates this directly.

The nine 7-cups are the previous nine 6-cups with the inserted point
included and indices shifted. A meets all nine, while C meets A only at 8
and misses B. The cup D has saturated type 3. Thus the same coverage
obstruction applies at the second target size.

**What fails, exactly.** Even a forced, unique helper can support a different
longest cup using an alternative internal route. Hitting Dh at h says
nothing about whether the other cups hit only at h contain v. This prevents
the direct merging step based solely on endpoint saturation and cap safety.
In both examples E1 has the simple repair A union {0}: point 0 belongs to
D intersect Q, so the addition is cap-safe and loses no coverage.

The original 14-point examples before coordinate simplification are retained
in `fan_coverage_obstruction.json` and `fan_priority_obstruction.json`.

## 5. Exact bounded criterion for the flexible exchange

This section is combinatorial; it applies in particular to either E1_3 or
E1_4. A is 4-cap-free and disjoint from D in F. For p in D put

    B_A(p) = {K minus {p} : K is a 4-cap, p in K, K minus {p} contained in A}.

These are triples. If B_A(p) is nonempty, put I_A(p)=intersection B_A(p).
For r in A let

    P_A(r) = {C in F : C intersect A = {r}}.

### Lemma I — intersection/private-cup criterion (PROVED)

There is an exchange allowed by E1 for this A,D if and only if either

1. B_A(p) is empty for some p in D; or
2. for some p in D and r in I_A(p), every C in P_A(r) contains p.

**Proof.** An addition of p alone creates a 4-cap exactly when B_A(p) is
nonempty. When it is nonempty, deleting r removes all newly created
4-caps exactly when r belongs to every triple in B_A(p), that is, to I_A(p).
Old 4-caps do not occur because A is 4-cap-free. A previously hit cup can
become unhit after deleting just r and adding p exactly when it was hit
only at r and does not contain p. These are precisely the excluded members
of P_A(r). Since p belongs to the previously missed D, a successful move
also makes strict progress. End.

### Lemma W — bounded failure witnesses (PROVED)

If there is no exchange for A,D, then for each p in D its failure can be
witnessed by at most four blocking 4-caps and at most three private cups
with their upper chains. More precisely, if s=|I_A(p)|, one needs at most
4-s blocking caps and s private cups.

**Proof.** Choose one triple T0 in B_A(p). For each r in T0 minus I_A(p),
choose a triple T_r in B_A(p) not containing r. The intersection of T0 and
these chosen triples is exactly I_A(p): every point outside T0 is already
excluded, and every unwanted point of T0 has its own exclusion witness.
There are 1+(3-s)=4-s selected triples. For each r in I_A(p), failure of
condition 2 in Lemma I supplies a private cup C_r not containing p.
There are s<=3 such cups. Include an upper chain witnessing each C_r as
a member of F. No deletion outside I_A(p) clears all the selected caps;
a deletion inside it loses its designated private cup. End.

### Corollary — a finite size bound on a counterexample to E1 (PROVED)

If E1_c fails on a real S, c in {3,4}, then it fails on a subset S' with

    |S'| <= n+2 + 3(n-1)(n+1-c).

The bounds are 99 and 136 for E1_3 at n=7,8; 81 and 115 for E1_4.
This is a conditional bound on a counterexample to the exchange statement,
not on a counterexample to Delta, and it is not a claim that a bounded
verification has been carried out. These loose numbers are not claimed to
improve ambient point-set size bounds; the useful reduction is the bounded
number of cap and private-cup witnesses per proposed insertion.

**Proof.** Retain D, one upper chain for D, and one 4-cap starting at its
right endpoint. This uses at most (n-1)+3=n+2 points. For each p in D
retain the witnesses of W. T0 adds at most three points. Each of the
3-s additional blocker triples adds at most three more. Each of the s
private-cup gons adds at most n-2 points: its private selected point r
already belongs to T0. Thus this p adds at most

    3 + 3(3-s) + s(n-2) = 12+s(n-5) <= 3(n-1)

points, since n>=7 and 0<=s<=3. There are |D|=n+1-c choices of p.

Set A'=A intersect S'. Validity and cap-freeness are inherited. D retains
its cap type and saturated cup length because its upper-chain witness is
retained and ranks cannot increase in a subset. Its right endpoint still
starts a 4-cap. Every type-2 cup of S' is an (n-1)-cup of S and is hit by A;
its selected hit lies on the retained cup, hence is also in A'. The chosen
blocking caps and private-cup gons stay intact. Their privacy is unchanged,
and they still exclude every addition and every one-deletion exchange by
W. Thus S',A',D is again an E1 failure. End.

Unlike a direct induction for all saturated cups, the last proof only needs
heredity of the type-2 hitting condition. It explicitly retains upper chains
for every other cup whose saturation must survive restriction.

## 6. What was checked, and what remains open

`check_exchange.py` independently enumerates all 4-caps, n-gons, and lower
sides of (n-1)-gons on a supplied set of at most 16 points. It enumerates
every subset A and tests the E1 moves for eligible cups. It reports zero
eligible pairs separately from finding no failed exchange.

* `exchange_pool_samples.json`: 16 induced 14-point sets extracted around
  actual descents in `ETVTHY20261113` pool_hept record 3. Every subset A
  was checked; no eligible E1_3/E1_4 failure was found.
* `exchange_pool33_samples.json`: the same bounded check on 16 induced
  14-point sets from pool_hept record 33, the parent's 23-point example.
  Again no eligible exchange failure was found.
* `exchange_minimum16.json`: exhaustive subset check of the parent's
  deletion-minimal 16-point example. It has one type-2 cup, 84 type-3 cups,
  and 91 type-4 cups, but **zero right-extendible members of F**. Hence
  there are **zero E1 test pairs**, for either cap type.
* `exchange_etv_samples.json` and the early `exchange_n7.json` /
  `exchange_n8.json` are exploratory small-set records, not evidence of
  a general theorem. In particular the sampled ETV subsets had no eligible
  descents; their empty failure lists were not used as support for E1.

All per-set checks are **COMPUTED**. Their selection is neither exhaustive
over point sets nor random in any uniform model; as general evidence it is
only **HEURISTIC**.

`attack_exchange.py` builds a fixed-S, fixed-D counterexample CNF. The point
variables encode A. A positive blocker witness implies that its three
other cap vertices are selected. A positive private-cup witness implies
that its designated vertex is selected and all other cup vertices are
unselected. For every proposed insertion/deletion, a clause requires a
surviving cap or a lost private cup. This is Lemma I encoded with existential
witnesses. A SAT model is checked from coordinates against every actual
move before it can be reported as `SAT_RECHECKED`.

Two fixed cups of the full 23-point pool_hept record 33 were tried:

| cup D | type | variables | clauses | result |
|---|---:|---:|---:|---|
| (4,8,11,12,13) | 3 | 4158 | 20260 | COMPUTED `UNSAT_UNCERTIFIED` |
| (0,1,5,13) | 4 | 4038 | 20078 | COMPUTED `UNSAT_UNCERTIFIED` |

The CNFs, solver outputs, and coordinate records are `attack_pool33_c3.*`
and `attack_pool33_c4.*`. No proof was requested or checked, so these results
are **not certificates**. They do not assert E1 for other cups of that set.

**Positive control on real coordinates, outside E1's hypotheses.** Dropping
only the right-starter requirement, the 16-point example has the following
failed exchange:

    A={5,6,7,8,10},  D=(0,1,11,12),  upper cap=(0,4,10,12).

A is 4-cap-free and hits the unique type-2 cup; D is a missed saturated
type-4 cup. Its right endpoint 12 starts no 4-cap. Direct enumeration shows
that every addition p in D with zero or one deletion either creates a 4-cap
or loses a previously hit saturated cup. This is **not** a failure of E1_3
or E1_4, whose right-starter hypothesis is absent.

The encoder was rerun with the right-starter assertion explicitly disabled
and A pinned to these values. Its 576-variable, 2647-clause CNF returned
SAT; the model was independently rechecked against all actual moves. Files:
`control_no_starter16.json` (hull-based enumeration),
`control_no_starter16_sat.*` (CNF, solver output, and directly rechecked
SAT model). `control_no_starter16_kernel.json` extracts the cap/private-cup
witnesses of Lemma W for each of the four insertion positions. Thus the
encoder can return a genuine SAT exchange obstruction, not just UNSAT.
The control refutes a blanket one-exchange assertion and emphasizes why the
conditional endpoint hypothesis must stay in the candidate statement.

The parent may schedule broader attacks using this instrument. By default
it only builds a CNF; `--solve-seconds` explicitly enables a single solver
call and is limited to 8 seconds. The `--control-no-starter` and `--pin-a`
flags are explicitly marked as controls, not the default candidate. A long search or a batch should be
scheduled centrally, not implemented by repeated capped calls here.

Reproduce the independent coordinate checks from the repository root:

```sh
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  cloud/es7-2026-10-19/results/DELTA3N20261113/descent/verify_obstructions.py
```

A concrete build-only attack command for a new parent-chosen saturated cup:

```sh
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  cloud/es7-2026-10-19/results/DELTA3N20261113/descent/attack_exchange.py \
  INPUT.json --n 7 --cup U,I,J,K,V --out ASSIGNED_PATH/attack.json
```

For the tested 23-point inputs, construction and solving together took less
than a second and the fixed solver cap was 512 MiB, one thread. This does
not estimate the cost of quantifying over new order types. No further job
is running or proposed for unsupervised execution.

## 7. Relation to the preceding records

Read inputs: DELTA2N20261113 README (especially sections 4.2b and 6),
VERIFY_D1.md, and ETVTHY20261113 sections 1-3 and the exchange tools. The
three-layer cover and the failures of endpoint, online, and forced-layer
rules are taken as limitations, not reproposed as constructions.

The new proved step is F4's whole-fan alternative and the exact exchange
witness reduction. The new obstruction is loss of an already protected
longest cup under the cap-safe descent, at both target sizes. A proof that
merges the layers must control the private cups as well as the cap blockers;
Lemma 5 only controls the latter endpoint geometry. E1_3 and E1_4 remain
precise conditional targets for independent attack.
