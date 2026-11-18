# Mixed hypergraphs and a closed four-state exchange obstruction

13 November 2026. Hypergraph theory track, DELTA3N20261113.

**PROVED:** the coloring formulations, singleton-clause elimination, a bounded
coherent local obstruction lemma, the exact one-hole move criterion, and the
isolated-cap obstruction theorem below. **COMPUTED:** the coordinate predicates
and finite checks in the accompanying JSON files, independently checked with
integer arithmetic. There is no new CERTIFIED/UNSAT claim in this directory.

**Main concrete result:** a 13-point real (5,7)-valid set has a proper partial
cup-side coloring trapped in a component of exactly four one-hole states.
There is also a valid four-point red set elsewhere. Consequently, even an
arbitrarily long sequence of the one-hole exchanges defined below need not
repair an arbitrary partial coloring. This is an exchange-connectivity
obstruction, not a counterexample to either Delta conjecture or a cardinality
gap. D(5,7;weak), D(5,8;weak), and their cup-side versions remain unresolved here.

Sources read: [DELTA2 README](../../DELTA2N20261113/README.md), especially
Sections 2, 4.2b, 6 (Lemma 4), and 7;
[VERIFY_D1](../../DELTA2N20261113/VERIFY_D1.md); and
[ETVTHY](../../ETVTHY20261113/README.md), Sections 1–3, 5, and 9.
The known failure of the strong version at (5,6) is respected throughout.
No saturated-endpoint descent argument is used.

## 1. Exact mixed-hypergraph formulation (PROVED)

Let S be a finite real planar set in general position, with distinct x
coordinates, no 5-cap, and no convex n-gon, where n is 7 or 8. Write:

- C(S): the four-point caps;
- G(S): the vertex sets of convex (n−1)-gons;
- L(S): the distinct lower cup chains of those gons, including both endpoints.

For each L in L(S), retain at least one **carrier** H in G(S) whose lower chain
is L. The carrier is evidence that the clause belongs to this instance.
It is not an additional clause. Duplicated lower chains give just one clause.

For P equal to G(S) or L(S), the required red set R is precisely a model of

    F(C,P) = AND_{K in C} (OR_{v in K} not x_v)
             AND AND_{E in P} (OR_{v in E} x_v),

where x_v means red. Thus no cap is all red, and every positive edge meets red.
P=G is the weak conjecture; P=L is the cup-side sharpening. The latter implies
the former because L is a subset of its carrier. We do not prohibit all-red
gons, which would introduce the different, strong conjecture.

An upper chain has c in {2,3,4} points. Its lower chain has n+1−c points:

| n | weak positive-edge size | cup-side positive-edge sizes |
|---|---|---|
| 7 | 6 | 4, 5, 6 |
| 8 | 7 | 5, 6, 7 |

For every cap K and lower chain L, **|K intersect L| <= 2**: three common
points would have both cap and cup orientation. This holds without any
assumption about endpoints. In the weak formulation a cap can intersect a
gon in three or four vertices, so this extra intersection restriction must
not be transferred to G.

The fractional constraints sum_{v in K} x_v <= 3 and sum_{v in E} x_v >= 1
admit x_v=1/2. Their integral feasibility is the issue.

### Geometric deletion versus deletion of a hypergraph variable

For the weak formula, the clauses on S−p are exactly the clauses of F(C,G)
whose edges avoid p. For the cup-side formula this can fail: a chain L avoiding
p can lose all its carriers when p is deleted as an upper-chain interior
vertex. Hence L may be a clause on S but not on S−p.

A coloring of S−p that hits its lower chains need not satisfy all original
lower-chain clauses avoiding p. Conversely, a proper partial coloring of the
**fixed** formula, in the sense of Section 4, does restrict to a valid geometric
coloring on S−p. We do not transplant Lemma 4's extension proof to cup-side
geometric deletions. Sections 2–3 use clauses of a fixed instance instead.

## 2. Singleton-intersection elimination and critical cores (PROVED)

Call a negative or positive clause E **removable at p in E** if no
opposite-sign clause D intersects E in exactly {p}.

**Lemma 1 (clause repair).** Deleting a removable clause preserves
satisfiability in both directions. Every model after deletion can be repaired
to satisfy the deleted clause by changing at most its chosen vertex p.

*Proof.* Only the direction restoring the clause requires proof. If the clause
already holds, do nothing. Otherwise all its vertices have the wrong color.
Change p to the clause's satisfying color. Same-sign clauses cannot be harmed.
If an opposite-sign clause D became false, p was its only previously satisfying
vertex. Every other vertex of E retained the old color and would satisfy D;
therefore D intersect E={p}, contrary to removability. This proves the claim
for either sign. ∎

Repeatedly delete such clauses. A model of the remaining formula extends to
one of the original formula by reversing the deletions and applying Lemma 1.
In particular, an empty remainder gives a constructive coloring.

The terminal clause family is independent of deletion order. Indeed, a family
in which every incidence (E,p) has an opposite singleton partner cannot lose
its first clause under this procedure. Every such family therefore survives
every deletion sequence; the terminal family itself has this property. It is
the unique largest such family. We call it the **singleton-supported core**.

**Corollary 1.** A counterexample must have a nonempty singleton-supported
core. In that core, each four-cap has four distinct positive singleton
partners, one for each vertex. Each positive edge E has |E| distinct cap
partners. In cup mode the degrees are at least (4,4) for n=7 and (4,5) for
n=8, and every cap/cup intersection still has size at most two.

This strengthens Lemma 4's existence of one singleton pair at each point to
a condition on **every incidence of every surviving clause**. It supplies
necessary conditions and a satisfiability-preserving reduction, not a
characterization of geometric counterexamples.

**Adversarial check (COMPUTED).** A nonempty core occurs in colorable valid
sets. On ETVTHY's 26-point `etv757.json`, exact geometry gives 2,001 four-caps,
9,632 hexagons, and 712 distinct lower chains. The terminal cores are:

| mode | deleted clauses | remaining caps | remaining positive edges |
|---|---|---|---|
| weak | 2 | 2,000 | 9,631 |
| cup | 502 | 1,500 | 711 |

See [etv757_peeling.json](etv757_peeling.json). Thus the proposed route
“every valid set peels to the empty formula” is false. These core counts are
one-program COMPUTED results, not part of the independent geometry audit.

## 3. A bounded coherent obstruction from positive-clause minimality (PROVED)

Keeping **all** geometric four-cap clauses is important in this lemma.

**Lemma 2 (coherent cap star).** If F(C(S),P) has no model, choose a nonempty
inclusion-minimal subfamily P0 of positive clauses for which F(C(S),P0) has
no model. For every E in P0 there are four-caps K_p, one for each p in E,
such that

1. K_p intersect E={p};
2. A=UNION_{p in E}(K_p−{p}) is disjoint from E and contains no four-cap;
3. A+{p} contains the cap K_p for every p in E.

Moreover, these witnesses, together with a carrier H of E in cup mode, lie
in a valid subconfiguration of at most 24 points for n=7 and 28 points for
n=8. The sharper cup-side bounds are in the table below.

*Proof.* By minimality, there is a red set R_E satisfying all cap clauses and
all clauses of P0−{E}. It must miss E. If R_E+{p} contained no four-cap for
some p in E, it would satisfy every clause of P0, a contradiction. Choose a
four-cap K_p in R_E+{p}. It contains p and its other three vertices lie in
R_E. Thus K_p intersect E={p}; their union A is a subset of the cap-free R_E.
For weak mode take H=E. For cup mode take any carrier H of E. The witness
ground set W=H union A has at most (n−1)+3|E| points. All the stated
geometry survives restriction to W, as do no 5-cap and no n-gon. ∎

| mode / upper-chain size c | n=7: size of E; bound on W | n=8: size of E; bound on W |
|---|---|---|
| weak | 6; 24 | 7; 28 |
| cup, c=4 | 4; 18 | 5; 22 |
| cup, c=3 | 5; 21 | 6; 25 |
| cup, c=2 | 6; 24 | 7; 28 |

This is a finite local necessary obstruction, with named roles: one carrier,
one cap through each positive-edge vertex, and a common cap-free set of
the other cap vertices. Unlike arbitrary singleton partners, the cap
blockers must be **simultaneously compatible with one cap-free red set**.
They need not be disjoint, and no distinctness of the three-vertex red
blocks is assumed.

This does not say such stars are impossible, or that the occurrence of one
is a counterexample. It isolates a bounded geometric condition that every
positive-clause-minimal counterexample must realize. A clause-minimal
subformula obtained by also deleting cap clauses would not justify item 2:
its red witness might contain a geometric cap whose clause was deleted.

## 4. Minimum counterexamples and exact one-hole moves (PROVED)

A **proper one-hole state** (p,R,B) of a fixed formula has
S=R disjoint-union B disjoint-union {p}, no cap contained in R, and no
positive edge contained in B. Equivalently, every positive edge missing R
contains p. Constraints containing the hole are allowed to be unresolved.

Define the two blocker families

    A_p = { K−{p} : K is a four-cap contained in R+{p} },
    B_p = { E−{p} : E is a positive edge contained in B+{p} }.

If A_p is empty, filling p red works. If B_p is empty, filling p blue works.
Lemma 4 of DELTA2 states that, for a minimum weak geometric counterexample,
both families are nonempty for **every** proper coloring of every deletion.
Any chosen blockers then intersect in exactly p before that point is removed.

A **hole move** fills p with the color of another vertex q, and makes q the
new hole. No other color changes in that move.

**Lemma 3 (exact move criterion).** At a proper state with both blocker
families nonempty:

- a move to a red q is proper iff q lies in the intersection of A_p;
- a move to a blue q is proper iff q lies in the intersection of B_p.

*Proof.* For a red move, the new red set is R−{q}+{p}. Its only possible
new caps are the caps formerly blocking p, and all must contain q. Positive
clauses that previously missed R gain p; a clause losing its sole red q now
contains the hole q. Thus the negative condition is also sufficient. The
blue move leaves R unchanged and removes p from the blue-blocker clauses'
possible holes, so each such clause must contain the new hole q. ∎

Moves are reversible, and preserve |R|. Thus searching arbitrarily long
alternating sequences is a genuine reconfiguration problem, not automatically
an augmenting-path theorem. If a nonempty family of triple blockers has empty
intersection, at most four of them certify that fact: take one triple and
one further blocker omitting each of its three vertices. Similarly, at most
n−1 positive blockers certify an empty blue-move intersection, since each
residual positive edge has size at most n−2.

### Four-element transversals and a closed component

When |R|=3, write T=R+{p}. Proper states correspond exactly to four-element
positive transversals T with a distinguished hole p in T: three red points
cannot contain a four-cap. For each fixed T its four hole states form a
complete graph, using red hole moves. A blue hole move corresponds exactly
to a single exchange T -> T−{p}+{q} that remains a positive transversal.
Filling red is possible iff T is cap-free; filling blue is possible iff
T−{p} itself is a positive transversal. Both termination conditions matter.

**Theorem 4 (isolated-cap obstruction).** Suppose T is a four-cap meeting
every positive edge. For each p in T suppose there is a nonempty family
F_p of positive edges satisfying

    E intersect T = {p}  for E in F_p,
    INTERSECTION_{E in F_p} E = {p}.

Then the states (p,T−{p},S−T), p in T, form a closed connected component
of exactly four proper one-hole states. None can be completed, and there
is no blue hole move out of the component.

*Proof.* T meets all positive edges, so all four states are proper.
Filling red creates T. Filling blue leaves any member of F_p all blue.
A red move to any other element of T gives another of the four states.
For a blue q outside T, some E in F_p omits q, by the intersection condition.
After the proposed move that E is all blue and avoids the new hole q, so
the move is improper. These exhaust all moves. ∎

This theorem does not require T to be globally minimum or unique among
transversals. It only requires the explicitly checkable local families F_p
and that T hits all positive edges.

## 5. A real 13-point obstruction, with a compatible solution elsewhere

**COMPUTED exact data:** [four_state_obstruction_small.json](four_state_obstruction_small.json).
Indices below are zero-based and sorted by x:

```text
0  (-924533,  889269)     1  (-862616,  406191)
2  (-810776, -115118)     3  (-756115, -685015)
4  (-619844,  832856)     5  (-409931, -758551)
6  (-387999, -847162)     7  (-379015, -936157)
8  (-284232,  210113)     9  (-111157, -424156)
10 (  65971, -578715)     11 ( 342593,  642694)
12 ( 800385,  970806)
```

There are 17 four-caps, no five-cap, 90 convex hexagons, no convex heptagon,
and 90 distinct lower chains. The minimum absolute triple determinant is
596,334,752, so general position is exact. Put T={1,5,6,7}. It meets every
lower chain. Its four increasing triple determinants are

    -14567748991, -44390408438, -30978416563, -1155757116,

so T is a four-cap. The following eleven lower-chain/carrier pairs establish
the local hypotheses of Theorem 4. In the last three rows p ranges over
5,6,7, giving nine pairs.

| pivot | lower chain E | hexagon carrier H |
|---|---|---|
| 1 | {0,1,9,10} | {0,1,4,8,9,10} |
| 1 | {1,2,8,11,12} | {1,2,4,8,11,12} |
| p in {5,6,7} | {0,2,p,9} | {0,2,4,p,8,9} |
| p in {5,6,7} | {0,3,p,10} | {0,3,4,p,8,10} |
| p in {5,6,7} | {2,3,p,9} | {2,3,4,p,8,9} |

For pivot 1 the two chains intersect only in 1. For the other pivots, the
three chains intersect only in p. Each chain meets T only at its pivot.
Thus, for example, the initial state

    hole = 1; red = {5,6,7}; blue = S−{1,5,6,7}

can move its hole only to 5,6,7, and from those states only to another
member of T. It can never terminate, irrespective of path length.

Nevertheless **{0,1,2,4} is a four-cap-free transversal of all 90 lower
chains**. A full coloring of a size compatible with the three-red hole
states therefore exists. The failure is the inability of these moves to
reach it. We make no minimum-transversal claim for this 13-point example.

Provenance: the coordinates are the subset of coordinator's 16-point
counterexample at original indices

    0,1,2,3,4,5,6,7,10,11,12,14,15.

The source file and its SHA-256 are embedded in the JSON. Vertices were
deleted preserving the **isolated-cap condition**, not a minimum-cardinality
gap. The final set is deletion-minimal for that condition with this fixed T
under the performed deletion check; no globally smallest-size claim is made.
The initial 16-point local certificate is also retained in
[four_state_obstruction.json](four_state_obstruction.json).

### Exact scope

Refuted: “every proper partial coloring of the fixed cup-side mixed
hypergraph can be completed by repeatedly exchanging the hole with one
colored vertex, keeping every intermediate state proper.” This fails
already for a real (5,7)-valid set with 13 points.

Not refuted: either Delta conjecture; a proof that selects a favorable
partial coloring; repairs that change the number of red points while the
hole remains; multiple-hole or simultaneous exchanges; an argument exploiting
additional global properties of a minimum counterexample; or a cup-side
geometric-deletion algorithm that recomputes carriers and thereby uses a
different state space. In particular, no analogous arbitrarily-long-path
barrier for the weak-gon state space is claimed here.

The parent reported a different result on the original 16 points:
unconstrained cup-transversal size 4 and cap-free size 5, with the unique
four-point transversal T. That suggested the obstruction but is not used
to verify the 13-point certificate. No minimization over transversal size
was repeated here. No result relies on the now-refuted cardinality-equality
strengthening.

## 6. Smaller-radius barriers at both target parameters

**COMPUTED, independently rechecked:** two previously recorded real sets
refute the simpler repair rule allowing at most one old vertex to change
color while the deleted point receives either color. The minimum number
of old recolorings is exactly two in each row: all zero/one-change extensions
fail and the displayed two-change extension succeeds.

| n, points, mode | deleted p | initial red set | valid full red set after two old changes |
|---|---|---|---|
| 7, 12, weak | 0 | {1,2,3,9,10,11} | {1,2,3,4,9,10} |
| 7, 12, cup | 0 | {1,2,3,9,10,11} | {1,2,3,5,9,10} |
| 8, 13, weak | 3 | {0,1,2} | {1,2,4} |
| 8, 13, cup | 3 | {0,1,2} | {0,1,3,4} |

The sources are DELTA2's `restr_ends_weak_a5_n7_m12_real.json` and
`restr_ends_weak_a5_n8_m13_real.json`; their coordinates, blocker lists, and
one failing clause for every zero/one-change extension are frozen in
[one_recolor_obstructions.json](one_recolor_obstructions.json).
Deletion validity in these checks uses the surviving **whole gons** as
carriers, including in cup mode.

As a control, exhaustive one-hole state enumeration on these two particular
fixtures found no trapped component in either fixed hypergraph. Those
statistics are in [vacancy_small_controls.json](vacancy_small_controls.json).
They are single-program COMPUTED results, not evidence that the universal
one-hole repair assertion holds. Section 5 supplies an explicit negative
instance for cup mode on a different 13-point set.

## 7. Checks, reproducibility, and changed files

[independent_audit.py](independent_audit.py) imports none of the extraction or
search programs. It reconstructs convexity using four-subset point-in-triangle
tests, instead of monotone hulls; caps use consecutive determinants, instead
of all triples; lower chains use the signs relative to the extreme chord.
It verifies both four-state certificates, every proposed move and completion,
the compatible full coloring, and all four two-recolor barriers. Result:
[independent_audit.json](independent_audit.json). It does not claim to
independently reproduce the ETV core or the exhaustive control-state counts.

All scripts use the Python standard library. All computational invocations
were single-threaded, with a 20-second external timeout where research was
performed. The longest was the fixed 26-point ETV check: 4.37 seconds and
50,308 KiB maximum RSS. Script limits are 18 CPU seconds and 512 MiB address
space. No long job, solver queue, systemd unit, agent, or web request was
launched. No SAT/UNSAT result is being promoted to CERTIFIED.

From the repository root, the complete independent certificate audit is:

```sh
timeout 20s env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python \
  cloud/es7-2026-10-19/results/DELTA3N20261113/hypergraph/independent_audit.py
```

The audit rewrites only its own JSON report, whose timing field varies.
`SHA256SUMS` records the delivered snapshot; it excludes itself. No further
probe is proposed or pending from this track.

New repository files, all in `R/DELTA3N20261113/hypergraph/`:

- `theory.md`: this record;
- `obstruction_check.py`: exact geometry, clause peeling, one-recolor barriers;
- `vacancy_probe.py`: enumeration of the fixed-formula one-hole state graph;
- `extract_four_state.py`: local fan extraction and support deletion;
- `independent_audit.py`: separate exact checker;
- `four_state_obstruction.json`, `four_state_obstruction_small.json`;
- `one_recolor_obstructions.json`, `independent_audit.json`;
- `etv757_peeling.json`, `vacancy_small_controls.json`;
- `SHA256SUMS`.

Scratch writes only in
`/home/jay/research/data/delta3-codex-20261113/hypergraph/`:
`first_check.json`, `etv757_input.json`, `etv757_peeling.json`, and
`vacancy_check.json`. No existing research record, main README/math file,
branch, commit, or remote was changed by this track.
