# Independent streaming Delta encoder (13 November 2026)

**PROVED (written argument below):** the new CNF is equisatisfiable with a
counterexample to D(5,n;weak), or its cup-side/cap-side variant, on m-point
signotopes. The implemented range is 5 <= n <= 8 and 4 <= m <= 20.
This is an encoding theorem, not a proof of the open Delta conjecture.

**CERTIFIED real counterexample (parent-scheduled discovery and verification):**
cup-side (5,6) fails on 15 integer-coordinate points, with 80 four-caps,
103 distinct lower-chain targets, no five-cap or convex hexagon,
**zero cup-side Delta** and **353 weak Delta**. The parent's
[realization](../coordinator/data/cup15/realized.json) matches all 455
orientation signs exactly; the smallest absolute determinant is
70,172,849,827,134. Its independent
[all-subset hull audit](../coordinator/data/cup15/independent_geometry.json)
confirms the geometric counts. The resulting 183-clause
[coloring CNF](../coordinator/data/cup15/cup15_coloring.cnf), with retained
[LRAT proof](../coordinator/data/cup15/cup15_coloring.lrat), has the exact
verdict `s VERIFIED UNSAT` in
[cake output](../coordinator/data/cup15/cup15_coloring.cake.out).
[Hashes](../coordinator/data/cup15/SHA256SUMS) are retained by the parent.
Thus Euclidean realizability is settled and the real cup-side hexagon
statement is false; the weak statement is not refuted.

The original abstract-search artifacts remain at
`/home/jay/research/data/delta3-codex-20261113/encoder/scheduled-cup-n6-m15/`;
the retained result snapshot is [frontier_n6m15.json](frontier_n6m15.json).
Its 2,395,813,802-byte LRAT trace is a SAT-search trace, **not an UNSAT
certificate**. Nothing has been deleted.

**COMPUTED controls:** the implementation passed 501,024 individual Delta-failure
comparisons with both the recorded encoders and direct geometric-sign
semantics. Small whole-instance proofs and cap-side negative controls are in
[CONTROLS.md](CONTROLS.md). All first scheduled frontier cases use `--sym none`.
Long jobs are exclusively the parent's responsibility.

The starting records, read without modification, are
`../../DELTA2N20261113/README.md`, `VERIFY_D1.md`, and the relevant definitions,
rank observations and conjecture sections of `../../ETVTHY20261113/README.md`.
In those relative references, `../../` from this directory is the results
directory. The old encoders are used only by the control script; the C++
encoder and the model checker do not import or invoke them.

## Files and intended use

- `delta_cnf.cpp`: C++17 streaming DIMACS encoder; no SAT library dependency.
- `run_case.py`: sequential encoder / CaDiCaL / cake_lpr pipeline, bounded by
  address space and time, preserving every CNF, proof and log with hashes.
- `check_model.py`: separate exact sign/coordinate verifier, including all
  subsets Delta via a full subset-zeta transform.
- `semantic_controls.py`: small exhaustive comparison against the old code
  and direct 4-subset convexity; it is not a frontier search.
- `control_report.json`: retained control outcomes, hashes and measured sizes.
- `COMMANDS.md`: reproducible build, scheduled runs and deferred checks.
- `frontier_n6m15.json`: snapshot of the parent's checked abstract SAT result.
- `FALLBACK.md`: exact flat counts and a bounded parent-scheduled alternative.
- `A4_REVIEW.md`: requested independent audit of a4 Sections 1 and 2 only.

Scratch is `/home/jay/research/data/delta3-codex-20261113/encoder/`. The compiled
binary is there, not in the repository. No commit, branch change, old-record
edit, web request or email was made by this track.

## 1. Semantics and base clauses

Points are labelled 0,...,m-1 in x order. The first C(m,3) variables are the
triples in lexicographic order, true = positive orientation = cup. A
signotope has at most one change in the four signs

    t(ijk), t(ijl), t(ikl), t(jkl),  i < j < k < l.

The encoder forbids each of the eight 4-bit assignments with two or more
changes, using eight 4-literal clauses. The old encoder instead forbids
alternating subsequences with eight ternary clauses; these conditions are
equivalent, but the emitted clause families differ.

For every 5-subset, a clause requires some consecutive triple to be positive.
For each n-subset and every split of its inner vertices into upper and lower
chains, with zero, one or two inner upper vertices, a clause forbids the
upper chain being a cap and the lower chain being a cup. Under no 5-cap, this
is exactly no convex n-set. No maximality, cardinality restriction on Delta,
minimum-counterexample assumption, fixed sign, or unproved localization is
used in the default model.

A target is:

- **weak:** all vertices of a convex (n-1)-set;
- **cup:** the lower cup chain of a convex (n-1)-set, including both ends;
- **cap:** the upper cap chain, including both ends (negative control).

The counterexample condition is: for every Delta, either Delta contains a
4-cap or a target is disjoint from Delta. Strong Delta is not implemented.

### Chain and convexity facts (PROVED)

First, all triples of a chain with equal consecutive signs have that sign.
On four consecutive vertices, the first and last entries of the signotope
sequence agree, so all four entries agree. Deleting any internal vertex
therefore preserves the consecutive-sign condition: the new consecutive
triples lie in such four-vertex windows. Repeated deletion gives any desired
subchain and in particular any triple.

Let U be a cap and L a cup with common endpoints u < v. Any interior x of U
has t(u,x,v) negative; an interior x of L has it positive. Thus their
interiors are disjoint. This justifies using an endpoint cap witness without
explicitly excluding the chosen lower chain's vertices.

Here is a full proof that U union L satisfies the recorded 4-subset convexity
test, addressing VERIFY_D1's noted gap in the earlier written argument.
Give each interior x its chord sign c(x)=t(u,x,v). For x < y:

- if x,y belong to the same chain, homogeneity gives
  t(u,x,y)=c(x) and t(x,y,v)=c(y);
- if they belong to different chains, the middle two entries of the
  signotope sequence on u,x,y,v are c(x),c(y), which differ. Having at most
  one change forces the first entry to be c(x) and the last to be c(y).

For internal x < y < z, if c(x) != c(y), use the sequence on u,x,y,z;
if c(y) != c(z), use x,y,z,v. Either forces t(x,y,z)=c(y).
If all three chord signs agree, they lie in one homogeneous chain, giving
the same conclusion. The endpoint cases were already proved. Consequently
the sign of every triple of U union L is the chord sign of its middle
vertex. For a < b < c < d in the union this gives

    t(abc) = t(abd),    t(acd) = t(bcd),

exactly the 4-subset convexity test.

Conversely, suppose every 4-subset of a set G passes that test. Partition
the internal vertices by t(u,x,v), where u=min(G), v=max(G). The 4-subset
test on u,x,y,v gives t(u,x,y)=c(x), t(x,y,v)=c(y). Its application on
u,x,y,z gives t(x,y,z)=t(u,y,z)=c(y). Thus the negative vertices with u,v
form a cap and the positive vertices with u,v form a cup. The 3-vertex
case is immediate. This proves both directions for every size, without a
finite enumeration assumption. For real points, the recorded convexity
test is equivalent to ordinary convex position.

## 2. Sharing seeds by an endpoint chain

Write Y_K for a 4-cap witness. It has one implication for each consecutive
triple of K. True Y_K therefore certifies a real 4-cap; false Y_K makes no
claim. These variables are also the size-four leaves of the cap lattice.

For u < v introduce one-way endpoint witnesses:

    H3(u,v) -> OR_{u<x<v} not t(u,x,v)
    H4(u,v) -> OR_{u<x<y<v} Y_{u,x,y,v}.

H3 asserts the existence of a 3-cap and H4 of a 4-cap. They are allocated
only where the interval has sufficient vertices. A 2-cap consists of the
endpoints and needs no variable.

For cup mode and a lower-chain candidate L of size ell in {n-3,n-2,n-1},
let r=n+1-ell. The seed P_L implies every consecutive triple of L is
positive, and also H_r(min L,max L) when r is 3 or 4. For r=2 only the
cup conditions are needed. The interval from min L to max L must have at
least n-1 vertices; otherwise no seed is allocated.

If P_L is true, an r-cap U exists. The preceding lemma gives
U intersect L = {u,v} and convexity of their union, of size r+ell-2=n-1.
Thus P_L certifies exactly the required cup-side target. The upper chain
is allowed to meet Delta: only L must be disjoint from Delta. This is the
cup-side statement, not an accidental stronger restriction.

Conversely, any lower chain of an actual convex (n-1)-gon has this form:
its upper chain has 2, 3 or 4 vertices because the configuration has no
5-cap. Its true Y/H/P witnesses can all be set to their intended values.
The room test never deletes an actual seed.

For cap mode, swap the roles in the seed: enumerate a candidate upper
chain of size 2..4 and share an endpoint witness for a cup of the
complementary length. That endpoint witness implies a disjunction of
individual cup witnesses. The same proof applies. Weak mode instead uses
the recorded 4-subset convexity definition directly: a seed for G implies
convexity indicators for every 4-subset of G, each defined by the two sign
equalities above. The three modes consequently share the lattice engine
but have different target semantics.

## 3. The bounded-deletion lattice (PROVED exact)

For a family of subsets of size at most k, let E(S) mean that S contains
one member of the family. If |S| > k, choose **any k+1** vertices of S.
Every member of size at most k omits one chosen vertex, so

    E(S) iff OR_{v among those k+1 vertices} E(S minus {v}).

This is a pigeonhole argument, not a symmetry assumption. The implementation
chooses the smallest vertices deterministically.

### Cap nodes

For |S|=4, A(S) is Y_S. For |S|>4 the single clause is

    not A(S) OR A(S minus {v1}) OR ... OR A(S minus {v5}),

where v1,...,v5 are the first five vertices of S. For |S|<4, A(S) is
the compile-time constant false; **there is no free variable for it**.

Induction on |S| proves that a true A(S) entails an actual 4-cap in S:
at a non-leaf some smaller true child is required, eventually reaching a
true Y_K. Conversely, set A(S) true precisely when S actually contains a
4-cap. The pigeonhole identity makes every implication true. No reverse
implications are required for this existential encoding.

### Target nodes

Let k be the largest target size (n-1 for weak/cup, 4 for cap). At S, the
right-hand side contains its seed P_S if allocated, and the target nodes
of S minus {v} for the first min(|S|,k+1) vertices v. Its only defining
clause is

    not B(S) OR P_S OR OR_children B(S minus {v}).

Absent seeds and absent children mean false and are omitted, never replaced
by unconstrained variables. If the right-hand side has no literals, B(S)
is the compile-time false constant. If it has one, B(S) aliases that
literal; otherwise a fresh variable with the displayed clause is allocated.
All child sets have smaller size (and smaller integer bitmask), so this
definition is acyclic.

Induction now shows that any true B(S) has a genuine target seed contained
in S. In particular, nonexistent lower-level witnesses cannot provide a
false escape from a pool clause. Conversely, if a genuine target T lies
inside S, either T=S and its seed is present, or a selected deletion avoids
T. When |S|<=k all vertices are considered; when |S|>k the k+1 argument
applies. Repeating reaches P_T. Setting every B to actual target-existence
satisfies all defining clauses, including the aliases and false constants.

The clauses have at most six literals for internal cap nodes and at most
k+3 for target nodes with a seed. There is no list of clauses in memory.

## 4. Exactness of the whole counterexample CNF (PROVED)

For **all 2^m** masks Delta the encoder emits

    A(Delta) OR B([m] minus Delta).

False constants are omitted. A clause with both sides false is emitted
as the empty clause, which is necessary, for example in small trivial
cases. No subset-size window or sampling is used.

**From a CNF model to a counterexample.** Its orientation part satisfies
the base, so is a valid signotope. Every pool clause contains a true A
or B witness. The induction above gives a 4-cap inside Delta or a target
disjoint from Delta. Consequently no Delta works. A SAT model can still
be nonrealizable; this does not automatically refute the real-point
conjecture. `check_model.py` checks the signs by the independent 4-subset
definition and enumerates all Delta outcomes before accepting SAT.

**From a counterexample to a CNF model.** Assign orientation variables the
counterexample's signs, every Y/Q4/endpoint/seed variable its exact
mathematical truth value, and A(S),B(S) actual containment truth. Each
base clause holds; each one-way witness clause holds; every recursion
holds by the deletion identity; and every pool clause holds because
Delta fails. Aliased B nodes have the same truth value as their only
possible source; false B nodes have no actual target. This is an explicit
canonical satisfying assignment. It applies in particular to every real
point counterexample, with its actual upper/lower chains.

Thus the unconditioned CNF is SAT iff an abstract counterexample exists.
An accepted UNSAT proof establishes the stated m-point theorem, subject
to this written encoder argument. The `--base` option omits witnesses
and the pool and instead tests existence of a valid configuration.

## 5. Optional symmetry and exhaustive cubes

Neither option is used for the first frontier runs.

Reversing x order maps t(i,j,k) to t(m-1-k,m-1-j,m-1-i), **without sign
complementation**. Geometrically x reflection reverses orientation once
and reversing the triple order reverses it again. Caps, cups, validity,
targets and the existence of Delta are all preserved.

`--sym mirror` enforces lexicographic t <= reversed(t), false < true.
It considers the smaller index of each two-element reversal orbit in
increasing order; fixed variables need no comparison. A prefix flag is
initially true. At a pair x,y it requires prefix -> (not x or y), and
equality with a true prefix forces the next prefix true. After the first
strictly smaller pair, remaining prefixes may be false. These one-way
prefix clauses express exactly the lex condition: a first greater pair
is impossible, and every lex-small assignment has a flag extension.
At least one member of every reflection orbit satisfies the condition.
No justification exists for fixing t(0,1,2) to a chosen sign alone.

`--cube 010` adds units fixing the first three orientation variables.
For any fixed q, all 2^q prefixes partition all assignments. Certification
of **every** cube is required for a full theorem; one cube establishes
only a conditional statement. This remains a covering scheme with
mirror enabled, using the orbit argument first. No cube pruning beyond
explicitly certified UNSAT is implemented. Cube arguments are a ready
fallback, not a claim of a search speedup.

## 6. Size and resource estimates

Exact counts below are for lattice, **sym none**, no cube and no fixed
signs. The CNF sizes in parentheses are measured with the small optional
mirror clauses included; they are conservative rounded sizes for either
setting. Generation of all six files together took under one second.

| target | variables | clauses | literals | measured disk, approx. |
|---|---:|---:|---:|---:|
| cup (5,6), m14 | 35,647 | 102,025 | 426,471 | 2.44 MB |
| cup (5,6), m15 | 69,770 | 181,556 | 781,297 | 4.60 MB |
| cup (5,7), m14 | 37,280 | 136,128 | 601,868 | 3.32 MB |
| cup (5,8), m14 | 37,706 | 162,375 | 752,797 | 4.08 MB |
| weak (5,7), m16 | 125,870 | 512,206 | 2,162,652 | 12.86 MB |
| weak (5,8), m16 | 117,862 | 881,146 | 3,446,527 | 20.40 MB |

The source streams each clause directly and rewrites a fixed-width DIMACS
header at completion. It keeps five integer arrays indexed by subset,
orientation IDs, small endpoint support data and the current clause. For
cup mode the five arrays occupy 20*2^m bytes: 0.3125 MiB at m14 and 0.625
MiB at m15. Observed whole-process generator RSS was 4.3--5.3 MiB on these
six cases. A single-thread optimized build used 166.4 MiB RSS and 1.33 s.

In the old expanded pool alone, each 4-cap variable occurs 2^(m-4) times:
C(m,4)*2^(m-4) cap literals before counting targets. The new pool has at
most 2^(m+1) literals; its sharing adds O(2^m) variables and O(k*2^m)
literals, rather than one repeated list per Delta. Cup witnesses also
share endpoint caps instead of enumerating a separate variable for every
upper/lower-chain pair. The optional `--pool flat` retains the new seeds
but expands containment directly, providing an exact performance/control
baseline. It also streams, without retaining Python clause lists.

Solver and checker working sets are not bounded by CNF size alone. Planning
estimates for initial cup m14/m15 solver state are tens of MiB; learned
clauses may grow substantially. The parent's measured m15 SAT runtime is
reported below; generation counts do not predict search time or guarantee
900/1800-second termination. These are the parent-controlled
limits, not achieved resource bounds:

- single process at a time inside each pipeline;
- current proposed/scheduled setting: `RLIMIT_AS=1300 MiB`, unit
  `MemoryMax=1800M`, one CPU, cake heap 1100 and stack 32;
- lower-memory fallback: AS 900 MiB, heap 650, stack 32;
- local controls: AS <=350 MiB, <=18-second outer timeout, heap 96/stack 16;
- a checker heap failure or time limit is **UNSAT_UNCERTIFIED**, never
  CERTIFIED. Proofs stay available for a separately scheduled larger check.

The runner chooses the smallest CPU in its inherited affinity mask. The
parent should provide distinct per-unit CPU masks (as it has arranged),
otherwise multiple runners may select the same CPU. The runner does not
start units, reserve resources, or launch a queue itself.

## 7. Priority and claim boundary

The original plan prioritized cup (5,6) at m14 and m15 to complete a
universal-signotope theorem using the existing m<=13 and base-m16 results.
The parent's m15 result supersedes that plan: the cup-side statement is
false for real point sets, with exact integer realization and the
183-clause coloring obstruction certified by cake_lpr. The model still
has 353 weak Delta, so it is not a weak-Delta counterexample. The geometry,
CNF, LRAT, exact cake verdict and hashes are linked at the top of this note.

**COMPUTED (parent's deletion audit):** all 15 single-point deletions have
a working cup-side Delta, with explicit witnesses in
[deletions.json](/home/jay/research/data/delta3-codex-20261113/coordinator/cup15/deletions.json).
This makes the particular example minimal under single-point deletion;
it does not establish that no different 14-point counterexample exists.

The retained SAT case is unconditioned: sym none, no cube, no fixed signs.
CaDiCaL reported SAT after 668.641 seconds; the independent exact checker
completed in 0.114 seconds. CNF SHA-256:
`f0b94d902933799f9222b12619fd3bd5b17c05ea59fc11719e076ceaaa98d631`.
The trace hash and complete sign string are in `frontier_n6m15.json`.

The m14 n6 case can still locate the smaller frontier, while n7/n8 m14
remain their own questions. After the m14 lattice cases ended UNKNOWN
at their 900-second limits, the parent launched flat m14 cases for n6,
n7 and n8, each with a 300-second solver budget. The flat estimates and
reproduction command are in [FALLBACK.md](FALLBACK.md). No such job was
launched by this encoder track.
Weak m16 files remain available. No solver speed advantage of the compact
lattice is claimed, and no numerical Erdős--Szekeres bound changes here.

The six small UNSAT controls do not extend a universal frontier. The new
certified real cup-side obstruction comes from the parent's separate
scheduled m15 solve, exact realization and geometric/coloring checks,
not from those controls. The original `frontier_n6m15.json` remains an
unchanged historical abstract-SAT snapshot; the linked parent artifacts
provide the subsequent real realization and certificate.
