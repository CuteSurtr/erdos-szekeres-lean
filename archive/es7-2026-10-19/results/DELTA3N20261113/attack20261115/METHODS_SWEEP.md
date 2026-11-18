# Method sweep on the Δ-reduction conjecture (15 November 2026, 05:22-06:25 KST)

Written at 06:25 KST by the synthesis stage of workflow `es-methods-sweep` (run `wf_b43dabb6-560`, script
`/home/jay/.claude/projects/-home-jay-research-lean-erdos-szekeres-lean/1e71bc06-5c09-4f54-ae48-3fca76aaa352/workflows/scripts/es-methods-sweep-wf_b43dabb6-560.js`).
The input was the 75 lens returns relayed to this stage. No computation was run for this file, no other repository
file was written, and no git action was taken. Targets and definitions are those of ETVTHY20261113 §3, DELTA2N20261113,
DELTA3N20261113, and `README.md`, `VERIFICATION.md` and `ROUND2.md` in this folder.

Conventions:
- **(5,n)-valid:** no 5-cap and no convex n-gon. A **gon** is a convex (n−1)-gon. A **weak Δ** is a 4-cap-free set
  that meets every gon.
- **Sets used below:**
  - cup15 = S15 is the certified 15-point (5,6)-valid real set, `../coordinator/data/cup15/realized.json`;
  - minimum16 is the n = 7 witness of the same folder;
  - U18 is `../resume/selection/terminal/data/witness.json`;
  - S19′ is U18 plus the abstract point r of ROUND2;
  - ETV26 = ETV(7,5,7) and ETV42 = ETV(8,5,8).
- Idea numbers are positions in the list relayed to this stage. They need not match the workflow's `lens:<i>` labels.

## 1. Headline

**No method produced a verified result.** Weak D(5,7) and weak D(5,8) remain **OPEN**. No ES(7) or ES(8) bound
changes, and no upper- or lower-bound frontier moved.

- **What ran.** 75 lens groups, most with three methods, each returned one idea:
  - 72 on the Δ conjecture;
  - 3 on the ES(8) upper bound (ideas 54, 57, 58);
  - none on ES(7) or on the ES(8) lower bound.
- **No deep dive and no verification ran** (§2), so **0 claims are verified and 0 were refuted by a verifier**.
  - Every statement below is a lens agent's own claim, at the agent's own label. Each comes from a quick check of at
    most about 10 CPU-seconds on 1 thread.
  - Counting rule: a claim counts only if a verifier examined it and did not refute it. No verifier examined any
    claim, so nothing counts as verified.

What the sweep produced (**all unverified**):

1. **One closed question.** σ13, the 13-element signotope that refutes rank localisation R(4,7), is a real point set.
   - Ideas 11 and 52 found two different integer realizations and checked all 286 orientation signs exactly (EXACT by
     their own checks).
   - So R(4,7) is false for real point sets, not only for signotopes. Idea 20's EXACT result (no biquadratic final
     polynomial) is consistent with this.
   - This supersedes "the failure was not realised by real points" (`README.md`, attack 6) and "Open. Realisability
     of σ13" (`VERIFICATION.md` §6).
2. **About 30 proof principles or strengthenings were refuted or shown vacuous.** Almost all are at n = 6 or on fixed
   sets.
   - Existence through homology, Euler characteristic, parity, signed counts or topological Hall: ideas 3, 17, 18,
     22, 23, 24, 33, 35, 61, 62, 64, 66.
   - Existence through product measures, first moment, LLL or a canonical random Δ: ideas 26, 28, 29, 32, 53, 75.
   - F2-linear rules: idea 34.
   - Embedding-respecting rules at (5,6): idea 21.
   - The fractional staircase, FC_stair(6) = 457/528: idea 38.
   - Small and linear autarkies: ideas 44 (COMPUTED) and 14 (HEURISTIC: HiGHS output only).
   - The flip carry form: idea 13.
   - The window threshold Δ_t for weak D(4,n): idea 2.
   - The one-sided transversal library: idea 48, a 24-point set with |R| = 17 > 16 = b(7).
   - Two-sided Young-profile rules on the pools: idea 58. This also refutes idea 59.
3. **Candidate strengthenings that survive every known witness.** Each was tested on 1-3 instances or tiny random sets
   only:
   - ENV# (idea 8), RT* (42) and VE (55);
   - G-D (67) and CAPCLOSED-D (69);
   - SEED = E ⊆ Δ (1, 6) and WD-cup (10);
   - GT (37);
   - AT_n (39), not yet evaluated on any instance.
4. **A positive class statement.** Weak D(5,n) holds on every ES-separable set for n = 6, 7, 8 (idea 51).
   - COMPUTED by an exact finite closure.
   - Conditional on a composition lemma that has not yet been written out.
5. **Upper frontier.** Idea 57 made an EXACT finite check: the 84 F-states are the 3-subsets of [9], and the nine Baek
   rows are the point-stars.
   - Writer's remark: so every two Baek rows share exactly 7 states, which settles the overlap question that idea 54
     left open (§3.10).
   - No bound follows yet.
6. **Lower frontiers: a no-go only** (idea 19, PROVED by its author).
   - Index-shift-invariant signotopes are single cups or caps.
   - Finite projective symmetry groups of a set are conjugate into O(2).
   - So Lie-group orbit constructions add nothing beyond the C_m/D_m searches already run.

**Outside the sweep (same night; not a lens result).** The "Realize" task reports **S19′ realizable**:
`/home/jay/research/data/roadmap-20261115/s19/realize/README.md`, 05:50-06:10.
- The label is EXACT, from three of its own programs. By its own §8 no independent verifier has re-run it.
- Hence CONJ-TS′(7) is false for real point sets.
- Six sweep ideas (49, 60, 71, 72, 73, 74) aimed to decide S19′ and are now superseded.
- That real set still satisfies weak D, the mirror form and the rooted form.

## 2. Deep-dive outcomes and verdicts

**None.** No deep dive ran, so no deep-dive outcome and no verdict exists for any claim.
- **The gate.** The workflow script sends an idea to a deep dive only if its self-assessed promise is at least 7 of
  10, and it runs verifiers only on deep-dive outcomes.
- **The returns.** The highest promise among the 75 returns was 3, reached by ideas 8, 39, 40, 42, 49, 51, 54, 67 and
  72.

  | promise | 0 | 0.5 | 1 | 1.5 | 2 | 2.5 | 3 |
  |---|---|---|---|---|---|---|---|
  | ideas | 17 | 5 | 21 | 2 | 19 | 2 | 9 |
- **Consequence.** The ranking in §3 is the writer's judgment from the quick checks. It is not a deep-dive outcome.

### 2.1 Agreement between independent lens computations

Separate agents wrote separate code, and the results below agree. This is the closest substitute for verification,
but it is **not verification** in the house sense: no `VERIFY_` file exists, and no verifier re-ran anything.

| Claim | Agreeing computations | Reading |
|---|---|---|
| cup15 has 80 four-caps, 216 pentagons and 353 weak Δs (of sizes 7/8/9: 108/189/56) | about 20 scripts reproduce all or part of this, e.g. ideas 1, 3, 4, 10, 12, 21, 24, 28, 29, 34, 38, 47, 63, 67, 69, 70 | the geometry codes agree with DELTA3N |
| minimum16 has 71 four-caps, 279 hexagons and 7,835 weak Δs | 8, 34, 38, 40, 67, 69 | control |
| ETV26 has 2,001 four-caps and 9,632 hexagons | 14, 44, 56 | control |
| U18 has 115 four-caps, 402 hexagons and 8,149 weak Δs | 8; the s19 task's `check_cex.py`; ROUND2 | control |
| 4,057 is the same count in three places: the ↑P4-safe weak Δs of U18 (idea 8), the record's real envelope Δs, and the rooted Δs of the real S19 (s19 task) | three separate computations | consistent with idea 8's L2: the canonical extension r0 is the worst 5-cap-free extension |
| σ13 is realizable | 11 and 52, with different coordinates | EXACT by each author |
| σ13 has no biquadratic final polynomial | 20 and 11 checked a feasible point exactly; 16 and 52 rely on HiGHS only | consistent with realizability |
| For the pair (4-cap-free complex, its gon-missing subcomplex) on cup15: relative Betti numbers 16 and 41, and Σ(−1)^\|Δ\| = 25 | 3, 23, 24 | agree |
| On cup15 the first-moment sum 80p^4 + 216(1−p)^5 has minimum about 11.25, at p ≈ 0.537 | 29, 32; idea 28 gives the exact Bernstein form | agree |

### 2.2 Internal refutations and inconsistencies found by the writer

- **Idea 24.** Its HRel(5,6) (nonzero relative homology on reduced sets) is refuted by idea 23's 9-point instance.
  That instance is reduced (its core is all 9 points) and acyclic over F2. COMPUTED by one script, not cross-checked.
- **Idea 59.** Its profile rule PR(5,7), PR(5,8) is idea 58's two-sided (f,g) state rule, built from the same
  Moshkovitz-Shapira profiles. Idea 58 found that rule UNSAT on 120 heptagon-free and 186 octagon-free pool sets
  (COMPUTED with pysat; no LRAT).
- **Ideas 31, 45, 46: off-by-one arithmetic.**
  - Ideas 31 and 45 write "weak D(5,7) ⟹ M(5;7) ≤ 16 + 16 = 32". Idea 46 writes "1 + M(4;7) + M(5;6) = 33".
  - With M(4;7) = 16 and M(5;6) = 15, both complete in DELTA2N §4.1, the values are 31 and 32 (`VERIFICATION.md` P4
    and P6).
  - Their thresholds remain valid; they are only not sharp.
- **Ideas 36, 65, 68.** Idea 36 reports one x-interval module of cup15, the points {11,12,13}. Ideas 65 and 68 report
  none. The definitions of a module differ and were not reconciled.
- **Idea 72.** Its sub-chirotope tests leave out the vertical point at infinity, so they test order types, not
  signotopes (idea 73). This is moot now that S19′ is realizable.

## 3. The ten most promising directions (ranked)

Criteria, which are the writer's judgment (HEURISTIC):
1. the statement implies weak D(5,n) or an ES bound;
2. it survives every known witness, including the real S19;
3. a cheap exact test can kill it;
4. it is not superseded.

Self-assessed promise is in brackets.

### 3.1 Uniform and rooted selection below CONJ-TS′ (ideas 8, 42, 55; `VERIFICATION.md` P2; s19/realize) [3, 3, 2]

**Notation.**
- U is (5,n)-valid.
- P4(U) is the set of pairs (b,c) that end a 4-cap of U.
- ⊑ is idea 8's order on pairs:
  - (j,k) ⊑ (i,k) ⊑ (i,j) when (i,j,k) is a cup;
  - (i,j) ⊑ (i,k) ⊑ (j,k) when it is a cap.
- ↑P4 is the up-closure of P4 under ⊑.

**Statements.**
- **ENV#(n):** every valid U has a weak Δ A in which every 3-cap a<b<c has (b,c) ∈ ↑P4(U).
  - Equivalent form, by idea 8's L1-L2: A ∪ {r} has no 4-cap for every 5-cap-free one-point right extension r of U,
    abstract extensions included.
  - Status of L1-L2: PROVED by the author. The writer re-derived both by hand from the 4-element signotope axiom;
    that is a reading check, not a verifier run.
  - ENV#(n) gives weak D(5,n) with no induction: put U = S − r and Δ = A ∪ {r}.
- **VE(n)** (idea 55): the same as ENV#, but with r ranging only over valid real insertions.
- **RT*(n)** (idea 42): U has one weak Δ A such that, for every valid real insertion r, either A ∪ {r} is 4-cap-free
  or A meets every gon through r.
- **ROOT(n):** if S is valid and its rightmost point r ends a 4-cap, then S − r has a weak Δ A with A ∪ {r}
  4-cap-free.

**Chain of implications.**
- TS selection ⟹ ENV# ⟹ (U) ⟹ UES* (idea 8; ROUND2 Task 4).
- UES* ⟹ VE, from ROUND2's Lemma B (writer's remark).
- VE ⟹ RT* ⟹ weak D(5,n) (ideas 55, 42).
- VE ⟹ ROOT, and ROOT at all sizes ⟹ weak D(5,n) by the rooted variant of Theorem 3.

**Next.**
- (a) Test ENV# with one SAT call per set, which needs only order-type data. Run it on the 124 sets that lack a
  terminal-safe weak Δ, on the 28 trajectory sets and on the pools.
- (b) Universal CNFs at the first open sizes:
  - **ENV#(7) for |U| = 13, 14, 15.** Drop r and use gen.py's rows with "some bad triple lies in A" replaced by "A
    contains a 4-cap, or some 3-cap (a,b,c) ⊆ A has ¬u(b,c)". Clauses force u ⊇ P4 and u up-closed under ⊑. This is
    sound because any such u contains ↑P4.
  - The explicit 4-cap literal is needed: unlike "bad", ¬u(b,c) is not forced by a 4-cap inside A. The same holds
    for ROOT below.
  - **ROOT(7) at |S| = 15, 16.** Keep gen.py's base and 4-cap hypothesis. The rows become "A contains a 4-cap, or
    some 3-cap (a,b,c) ⊆ A has (b,c,r) a cap, or some gon of U avoids A".
  - Both keep gen.py's restriction to |A| ≤ |U| − 5. It stays sound: a subset of a solution whose complement in U has
    five points is again a solution, since no hexagon fits in five points.
- What is already known and what a result would give:
  - ROOT(7) already holds for |S| ≤ 14, from the CERTIFIED CONJ-TS′(7) for m ≤ 14 plus Fact E.
  - ENV#(7) at |U| = 15 alone would give weak D(5,7) at |S| = 16.
  - ROOT(7) at |S| = 16 would give it as well, together with the CERTIFIED weak D(5,7) for |S| ≤ 15.
  - This is a milestone only; it changes no ES bound.

**Why.**
- Theorem 3 and its rooted variant form the only reduction that all three verifiers accepted.
- S19′, now real, kills CONJ-TS′(7) but none of these statements. ENV# holds on U18's order type (4,057 ↑P4-safe weak
  Δs), so the real S19 satisfies ENV#, (U), VE, RT* and ROOT.
- ENV# replaces the terminal-safe condition (b,c) ∈ P4 by the exact invariant (b,c) ∈ ↑P4, with one canonical
  extension r0. That makes it a single SAT instance per set.

**Risk.**
- All of these strengthen weak D for U, and no proof mechanism is known yet.
- At n = 8, VE contains weak D(4,8) on 4-cap-free inputs (writer's remark, unverified).
  - Reason: the point r_inf of idea 42 (4) is a valid insertion that caps every pair, so A must be a cup.
  - So ENV#, (U) and UES*, which each imply VE, contain it too. For ENV#, idea 8 shows this directly; for (U), it is
    the P1 corollary.
- Weak D(4,8) is open from 14 to 22 points (§3.3).
- RT* avoids this obstacle through r_inf (idea 42). Other extensions were not checked.

### 3.2 Antichain form AT_n of the LT-cover lemma (idea 39; ROADMAP20261115 §2, program delta:1) [3]

**Setting.** U is valid with rightmost point u.
- A0 is a uniform Δ of U − u (design:delta:1 §4).
- E = {b ∈ A0 : h_U(b,u) = 3 and line(b,u) is exposed}.
- a < b iff a, b ∈ A0, x_a < x_b, b ∈ E, and (a,b,u) is a cap.

**Statement AT_n.** For every valid (U,u), some uniform A0 has an antichain of (A0, <) that meets H ∩ A0 for every
convex (n−1)-gon H of U − u.

The author proves the following; none of it is verified:
- < is a strict partial order whose chains are cups.
- So the exposure graph is a comparability graph, and the conflict side of the polytope is the integral antichain
  polytope.
- AT_n is equivalent to LT-cover_n, which implies weak D(5,n).

**Next.** Compute exactly on U18, the real S19, pool_hept and pool_main:
- A0, the exposure test and the order;
- the polytope Q(U,u,A0), with primal and dual rechecked in exact rationals (HiGHS only proposes);
- integer feasibility, by brute force or SAT;
- whether one Mirsky level of (A0, <) already works.

**Why.**
- It is the exact missing lemma of the roadmap's first-ranked Δ program.
- Unlike attack 5's relaxation, any 3-chain cuts off x = 1/2.
- Nothing on record refutes it or supports it.

**Risk.**
- It has never been evaluated on a single instance.
- Deletion-only repairs of other selections failed at 9-10 points.
- The covering rows are unstructured, so the relaxation is vacuous whenever every trace has at least height(<) points.
- If "uniform" means condition (U), the n = 8 case presupposes weak D(4,8) (§3.3).

### 3.3 Weak D(4,8) at 14-22 points (ideas 2, 8; `VERIFICATION.md` P1) [0.5, 3]

**Statement.** Every 4-cap-free set U with no convex octagon and 14 ≤ |U| ≤ 22 has a cup that meets every convex
heptagon of U.
- The problem is finite: Baek gives M(4;8) = 22.
- DELTA2N §4.1 certified the strong form for 7-13 points; it timed out at 14.

**Next.**
- Write an encoding whose candidates are the cups of U. A cup has at most 7 points here, so there are at most
  Σ_{k≤7} C(m,k) candidates instead of 2^m.
- Give it a written soundness note.
- Run positive controls on the 24 (4,8) pool sets of DELTA2N §4.2b and on idea 2's two real a = 4 (n = 6) sets.

**Why.**
- It is necessary for every r-independent route of uniform-envelope type at n = 8:
  - (U), by the P1 corollary;
  - ENV#(8), UES*(8) and VE(8), as in §3.1;
  - the uniform A0 of §3.2, if "uniform" means (U).
- Idea 2 refuted the natural construction: on two real a = 4 sets, every endpoint set Δ_t contains a 3-cap (COMPUTED).
  So a proof must use vertices that are not gon endpoints.

**Risk.**
- SAT reach: the strong form stalled at 14 points.
- A counterexample would close those routes at n = 8 without deciding weak D(5,8).

### 3.4 Composition calculus: weak D(5,n) on all decomposable sets (ideas 51, 36, 65, 68; idea 60's lemma) [3, 1, 1, 1, 2]

**Statement (a): idea 51's composition lemma.** In A ⊕hi B, where B is flattened far to the upper right:
- a crossing cap is one point of A followed by a cap of B;
- a crossing cup is a cup of A followed by one point of B;
- a crossing convex polygon is a cup of A that starts at A's left end, joined to a cap of B that ends at B's right end.

So validity and the minimal weak profiles compose by explicit maps F_hi and F_lo, and the mirror case is the same.

**Statement (b): DB(n) for n = 7, 8 (idea 36).** Suppose S = A ⊔ B with B deep below A, where the x-ranges may
interleave. If S is (5,n)-valid and A and B each have a weak Δ, then S has one.
- Each split can be decided by one CNF on |A| + |B| variables, using idea 36's L1-L2.
- L1-L2 were checked on 28,812 subsets of 3 random instances.

**Next.**
1. Write (a) out.
2. Check F_hi and F_lo against brute-force profiles of explicit separable point sets, in exact integers.
3. Extend the profile calculus to interleaved deep-below splits.
4. Recompute the closure for n = 7, 8.

**Why.**
- Idea 51's exact closure already gives weak D(5,n) on every ES-separable set, conditional on (a):
  - 97, 263 and 510 types for n = 6, 7, 8, none with an empty profile set;
  - the largest separable valid sets have 15, 26 and 42 points, the ETV values.
- That would be the first all-size positive statement at n = 7, 8 on an infinite class containing the ETV extremal
  sets.
- With DB(n), every minimal counterexample would be prime.
- Idea 60's tropical-limit lemma (PROVED by the author) is the one-point case. A point that dominates all heights lies
  in no 4-cap or in no gon, so it can be added to Δ or kept out of it.

**Risk.**
- The known hard (5,6) instance S15 is prime (ideas 36, 65, 68), so the reduction does not reach the hard cases.
- No bound changes.
- General substitution needs a fat-point hypothesis that is stronger than weak D (idea 65).

### 3.5 Graph and closure forms: G-D(5,n) and CAPCLOSED-D(5,n) (ideas 67, 69) [3, 2]

**Statements.** Each implies weak D(5,n).
- **G-D(5,n):** S has a set Δ that meets every gon and contains no middle pair {p2, p3} of a 4-cap p1p2p3p4 of S.
- **CAPCLOSED-D(5,n):** S has a set Δ that:
  - meets every gon;
  - contains the middle point of every 3-cap whose two ends it contains;
  - contains no two ends of a 4-cap.

**Next.**
- Universal CNFs at (5,6) for 5 ≤ m ≤ 15. This covers all sizes, because base(5,6,16) is CERTIFIED UNSAT (DELTA2N
  §4.1).
  - G-D: the weak (5,6) encoder with the 4-cap clauses replaced by binary middle-pair clauses.
  - CAPCLOSED: the same encoder with the Horn clauses (¬a ∨ ¬c ∨ b) and the binary clauses (¬a ∨ ¬d) added.
  - Cost: the weak (5,6) run at m = 15 took 1,267 s.
- Then U18, the real S19, ETV26, ETV42 and the pools of 121 and 194 sets.

**Why.**
- Each turns 4-cap-freeness into a graph or closure condition:
  - G-D asks for a vertex cover of the middle-pair graph that contains no gon;
  - CAPCLOSED asks for a convex up-island indexed by a cup Γ of S.
- No failed strategy had this structure.
- Both survive cup15 and minimum16.

**Risk.**
- Both are very tight on cup15: only 4 (G-D) and 5 (CAPCLOSED) of the 353 weak Δs qualify.
- Idea 69 expects CAPCLOSED to fail on ETV-type sets.
- The middle-pair graph is not hereditary under adding a rightmost point, so attack 2's induction does not transfer.

### 3.6 Seeded and localised forms: SEED(n) = E_{n−1} ⊆ Δ, WD-cup(n) (ideas 1, 6, 10) [2, 1, 2]

**Statements.**
- **SEED(n):** S has a weak Δ that contains every right end of an (n−1)-cup, or one that contains every left end.
- **WD-cup(n):** S has a weak Δ whose intersection with Q = {points that start no 4-cap} is a cup of at most n − 2
  points.

**Next.**
- The same universal (5,6) runs (all sizes), then the n = 7, 8 pools, U18 and S19.
- SEED adds unit clauses; WD-cup adds a 3-cap ban and a cardinality bound on Δ ∩ Q.

**Why.**
- Two lenses proposed SEED independently.
- Its seed is 4-cap-free and settles every pure-cup gon by the classical Pascal-split step (PROVED, ideas 1 and 6).
  Only saturated pairs of types (3, n−2) and (4, n−3) remain.
- Both forms are looser than §3.5 on cup15, so they are more likely to survive: 107 of the 353 weak Δs contain R, and
  46 of 353 satisfy WD-cup.

**Risk.**
- Earlier seeded or localised strengthenings held at small sizes and then failed at 9-15 points: terminal-rank
  selection, one-old-blue repair, Δ inside the gon ends.
- The leftover (4, n−3) pairs are the original difficulty.

### 3.7 Natural Δ rules at n = 7, 8 (idea 21) [2]

**Statement.** Is there a choice function c on the gon types such that
Δ_c(S) = {the c(type)-th vertex of every convex (n−1)-gon of S} is 4-cap-free for every set in the pool, U18 and S19?
- n = 7: 11 gon types, on the 121 heptagon-free sets.
- n = 8: 16 gon types, on the 194 octagon-free sets.
- By idea 21's lemma (A), PROVED by the author and unverified, these are exactly the Δ rules that respect embeddings.
  The classical cups-caps proof uses a rule of this class.

**Next.**
- Copy `natrule.py` out of the scratchpad and run it on the pools; it takes seconds.
- Certify every UNSAT answer with CaDiCaL LRAT and cake_lpr, including the (5,6) answer on cup15.

**Why.** It is decisive either way at negligible cost.
- UNSAT gives a clean no-go for every embedding-respecting construction.
- SAT would reduce weak D(5,n) to excluding one configuration of at most 4 + 4(n−2) points: 24 for n = 7, 28 for
  n = 8.

**Risk.** The failure at (5,6) makes SAT unlikely. The expected result is one more obstruction.

### 3.8 Size surrogates of T(n): GT, CTL, RMU (ideas 37, 48, 27) [2, 1, 2]

**Statements.**
- **GT(n):** min(|T→(S)|, |T←(S)|) ≤ C(n−1,2) + 1. Here T→ is the set of points rejected by the left-to-right sweep
  that keeps a point unless it closes a convex (n−1)-gon with points already kept; T← is the same for the
  right-to-left sweep.
- **RMU(n):** τ(gons of S) ≤ α_rm(S), the size of the largest β-antitone or ω-isotone set.
- Each implies T(n), hence M(5;7) ≤ 31 for n = 7 and M(5;8) ≤ 58 for n = 8.

**Next.**
- Run idea 48's climbers (`climb.c`, `climb2.c`) with the objective min(|T→|, |T←|), starting from pool_hept and from
  w24.
- Compute τ(ETV42) exactly, to see whether RMU has zero slack there (α_rm(ETV42) = 16).
- Re-validate every hit in exact integers.

**Why.**
- These are the only proposals that bypass 4-cap-freeness.
- The one-sided library bound fell within seconds: w24 has |R| = 17 > 16 at n = 7 (EXACT by two programs). The
  two-sided bound reached equality (16) in 4 s.
- GT has slack 6, 5 and 4 at n = 8, 7, 6 on every pool set, so a targeted search should decide GT(7) quickly.

**Risk.** Any proof of GT(8) or RMU(8) contains M(5;8) ≤ 58 (the caution in ROADMAP20261115 §2). These are targets for
refutation, not shortcuts.

### 3.9 Counterexample hunting in the window (ideas 30, 31, 4) [1.5, 2, 2]

**Statement.** Find a (5,7)-valid set or signotope of 16-32 points that has no weak Δ. A valid set of 32 or more
points would be such a counterexample automatically, because weak D(5,7) gives M(5;7) ≤ 31.

**Next.**
- Search 17-26-point sets with one of two drivers:
  - multilevel splitting on −log P_S, where P_S is the success probability of random-order greedy (idea 30);
  - soft-constraint replica exchange (idea 31).
- Test each candidate exactly with SAT.
- Send any hit through CNF → CaDiCaL LRAT → cake_lpr, then through the realizability oracle of ideas 11 and 52.
- Idea 4's forced-trace census is a cheap filter for gadget pieces.

**Why.**
- The refutation direction is open (attack 7's verifiers, `VERIFICATION.md` §7).
- These scores aim at hardness, unlike the 570,485 plain random walks.
- Idea 31 shows that hard-constraint flip chains are disconnected even at 5-6 points. That may explain why earlier
  walks stayed trapped in ETV basins.

**Risk.** A null result is HEURISTIC only, and the evidence leans towards the conjecture being true.

### 3.10 Upper frontier: pair rows on the nine Baek blocks (ideas 54, 57) [3, 0.5]

**Statement PAIR(i,j,c).** Every configuration of the coupled omission semantics (no 5-cap, no convex octagon) has
occ(B_i) + occ(B_j) ≤ c. The B_i are the nine Baek rows, catalog rows 973, 1165, 1167, 1171, 1175, 1179, 1183, 1186
and 2315.

**Next.**
- One CNF per pair: the coupled clauses plus occ(B_i) ≥ 22 and occ(B_j) ≥ c + 1 − 22.
- Certify each with cake_lpr.
- Start at c = 43.

**Why.**
- Idea 57's exact check identifies the 84 F-states with the 3-subsets of [9] and the nine rows with the point-stars.
- So every two rows share exactly 7 states, and the overlap graph is K9.
- Hence idea 54's fractional-matching step holds, with weight 1/8 on each edge:
  - PAIR(·,·,43) for all 36 pairs gives occ(F) ≤ 64, i.e. h(F) ≥ 20;
  - c = 42 gives h(F) ≥ 21.

**Risk.**
- ROADMAP20261115 §6 marks this F-side lever as stalled: row 973 is blocked in the coupled encoder (BAEK973).
- c = 42 is a per-block capacity of 21 in disguise.
- Idea 57 found no symmetry beyond the identity, so all 36 pairs need their own runs. The cost is close to that of the
  stalled N5 ladders.

### Next in line, outside the top ten

- **Rule synthesis with cheap a = 4 gates** (ideas 40, 43, 45, 47): CEGIS over rank-class weights, row-extreme
  selectors or Skolem rules. Drop a rule language if it cannot produce certified rules for (4,6), (4,7) and weak
  (5,6), where the truth is CERTIFIED.
- The recourse hierarchy k*(a,n) (ideas 41, 64).
- The flip / down-locked reduction (ideas 13, 25).
- The frame relaxations (ideas 9, 50).
- OH(8,t) (idea 58).

## 4. Every lens group

Columns:
- **P** is the agent's self-assessed promise (0-10), given after its own objection.
- **T** is the target: Δ for the conjecture, U for the ES(8) upper bound.
- The last column is the agent's own check and objection, all unverified, unless it says otherwise.

| # | Methods | T | Idea | P | Objection / decisive fact |
|---|---|---|---|---|---|
| 1 | extremal comb. (Pascal split) / saturated pairs / enumerative comb. | Δ | SEED(n): weak Δ containing all right (or all left) ends of (n−1)-cups | 2 | Seeded strengthenings failed before; the leftover (4,n−3) pairs are the core. Holds on cup15 (107/353 contain R). |
| 2 | geometric / algebraic / probabilistic comb. | Δ | Window threshold Δ_t for weak D(4,n) | 0.5 | Refuted (COMPUTED, exact): every Δ_t contains a 3-cap on two real a = 4 sets; covering lemma (i) unverified. |
| 3 | topological / analytic / additive comb. | Δ | Homology, Euler char., parity of (4-cap-free, non-transversal) | 0 | Homology zero on 15-22 % of random valid sets that have a Δ (n = 6, 7; float orientations). |
| 4 | Ramsey (forcing gadgets) / computational comb. / arithmetic comb. | Δ | Gadget amalgamation over flat-block substitutions | 2 | Size cap leaves little room; S15 has no forced point; at best a falsification test. |
| 5 | graph / hypergraph / extremal graph theory | Δ | Balanced-hypergraph (Berge) route | 0 | Needs a 2-colourable 4-cap hypergraph; χ = 5 on ETV42 (recorded). |
| 6 | structural / spectral / random graph theory | Δ | Forcing E_{n−1} ⊆ Δ (LPX type) | 1 | Same statement as idea 1; forcing a rank level failed before; untested. |
| 7 | matroids / geometric graph theory / graph limits | Δ | Permutation version false; grid lemma G_n | 1 | G_n is far weaker than weak D; part (A) is folklore pigeonhole. |
| 8 | oriented matroids / order theory / lattices | Δ | ENV#(n): ↑P4-safe weak Δ, canonical extension r0 | 3 | Stronger than weak D; contains weak D(4,n) on 4-cap-free inputs. Holds on U18 (4,057), cup15 (251), minimum16 (1,823). |
| 9 | discrete geometry / design theory / finite geometry | Δ | DirD(8): Δ 4-cap-free in some admissible viewpoint | 1 | Far viewpoints make S cap-rich; no mechanism; untested. |
| 10 | combinatorial / convex / incidence geometry | Δ | WD-cup(n): Δ ∩ Q a cup of ≤ n−2 points | 2 | A localisation like those that failed at 9-15 points; holds on cup15 (46/353). |
| 11 | real / convex / classical algebraic geometry | Δ | Realizability oracle; σ13 realized | 1.5 | Closes a loophole (R(4,7) false for real sets); nothing toward weak D. |
| 12 | projective / affine / Euclidean geometry | Δ | Pencil-sweep greedy PS(5,n) | 1 | On cup15 pencil orders are no better than random ones (20.5 % vs 21.8 %). |
| 13 | polyhedral B(m,2) / discrete differential / differential geometry | Δ | Repair along cap-to-cup flips | 1 | Carry form false (3 of 68 pairs, m = 9); the adaptive form is a global selection again. |
| 14 | linear algebra / tropical / symplectic geometry | Δ | Linear-autarky induction LA(n) | 1 | ETV26 looks linearly lean (HiGHS and numpy only: HEURISTIC), so the induction cannot start. |
| 15 | abstract / group / finite group theory | Δ | Only symmetry is the x-mirror (Z/2) | 0 | No-go; symmetries of auxiliary models unchecked. |
| 16 | invariant / representation theory / commutative algebra | Δ | BFP cuts to rescue R(4,7) for real sets | 1 | No BFP (HiGHS only); superseded: σ13 is realizable (11, 52). |
| 17 | homological / noncommutative / multilinear algebra | Δ | Relative homology (K, K′), Mayer-Vietoris | 0.5 | χ = 0 on 185 of 757 essential cores. |
| 18 | exterior / tensor / Lie algebra | Δ | Signed count (supertrace) | 0 | Zero by a toggling involution (PROVED) and on 10 sampled sets with every point on a 4-cap. |
| 19 | Lie theory / algebraic groups / ring theory | Δ | Higher-Bruhat / total-positivity dictionary | 0 | Renaming; flip induction blocked; orbit constructions for L7/L8 add nothing (N2, N3). |
| 20 | field theory / Galois theory / module theory | Δ | BFP test on σ13 | 1 | No BFP (EXACT integer check); moot since σ13 is realizable. |
| 21 | category theory / sheaves / algebraic topology | Δ | Natural (embedding-respecting) Δ rules | 2 | None at (5,6) on cup15 (pysat UNSAT, no LRAT); n = 7, 8 untested. |
| 22 | combinatorial / geometric / differential topology | Δ | Topological Hall criterion TH | 1 | Fails on cup15 at W = S: η sum 12 < 15. |
| 23 | equivariant topology / homotopy / homology | Δ | HD(5,n): relative homology nonzero | 0.5 | False on a reduced 9-point (5,6)-set with 304 weak Δs. |
| 24 | cohomology / simplicial homology / discrete Morse | Δ | HRel(5,n) on reduced sets, rightmost Morse matching | 2 | Refuted at n = 6 by idea 23's instance; the induction leaves the class. |
| 25 | real / functional / complex analysis | Δ | Convexifying sweep LF(n); reduction to down-locked sets | 2 | Moves the difficulty to the down-locked class; tested only at 10 points (393/393). |
| 26 | harmonic / Fourier / higher-order Fourier | Δ | Harris-FKG obstruction to product-measure proofs | 0 | Folklore; rules out averaging only. |
| 27 | measure / integration / asymptotic analysis | Δ | RMU(n): τ(gons) ≤ α_rm(S) | 2 | Possibly zero slack at ETV42 (α_rm = 16, τ not computed); no mechanism. |
| 28 | probability / operator / spectral theory | Δ | Density criterion on cup15 | 0 | EXACT: μ_p(D) + μ_p(U) < 1 for every p (all Bernstein coefficients ≤ 0). |
| 29 | discrete / geometric probability / random matrices | Δ | Canonical random Δ, CRD(n) | 0 | CRD(6) false on S15: best minimum coverage 0.8729. |
| 30 | concentration / martingales / stochastic processes | Δ | Random-order greedy: P_S and SWEEP(n) | 1.5 | A restatement plus a search score; P_S falls with N. |
| 31 | statistical mechanics / ergodic theory / percolation | Δ | Soft-constraint replica-exchange search | 2 | A null result is HEURISTIC; mixing is likely exponential. |
| 32 | dynamical systems / symbolic dynamics / information theory | Δ | Switching injection SW(n) | 1 | A fixed one-half fraction is very likely false; weaker forms are weak D itself. |
| 33 | entropy / coding / algebraic coding theory | Δ | GF(2) parity (Reed-Muller) existence | 0 | Both parities at m = 9-11; signed count 0 on 10 of 51 sets. |
| 34 | combinatorial coding / number theory / elementary NT | Δ | F2-linear Δ rules; ODD(n) | 0 | Linear system inconsistent on cup15 and minimum16; only Δ ⊆ Q survives, refuted at n = 8 in the records. |
| 35 | additive / analytic / algebraic number theory | Δ | Mod-p counting (Chevalley-Warning) | 0 | Residues vary (PROVED at a = 3; COMPUTED at (4,5), (5,6)). |
| 36 | arithmetic geometry / Diophantine geometry / multiplicative NT | Δ | Deep-below (valuative) splits, DB(n) | 1 | Baek-Balko calculus already known; S15 has no deep-below split. |
| 37 | combinatorial optimization / optimization / Diophantine approx. | Δ | GT(n): greedy-sweep transversal count | 2 | One direction reaches 20 of 22; the min of two sweeps is ad hoc; a proof contains M(5;8) ≤ 58. |
| 38 | convex / discrete optimization / integer programming | Δ | FC_stair(n); local search LS(n,k) | 1 | FC_stair(6) = 457/528 < 1 on cup15 (exact primal and dual); LS needs growing neighbourhoods. |
| 39 | LP / Farkas certificates / SDP / NLP | Δ | Antichain form AT_n of the LT-cover lemma | 3 | Never evaluated on an instance; the covering rows are unstructured. |
| 40 | constraint programming / global / polynomial optimization | Δ | Inverse optimization: weights W(n) on rank classes | 3 | Per-instance fits are expected; a shared w is likely infeasible; no exchange lemma. |
| 41 | mathematical logic / operations research / propositional logic | Δ | Bounded-recourse inductive invariant | 2 | The recourse needed may be unbounded. |
| 42 | first-order logic / model theory / finite model theory | Δ | RT*: one A good for every extension type; amalgamation lemma | 3 | Strengthening of weak D; the induction step needs pairs of new points. |
| 43 | proof theory / computability / recursion theory | Δ | Mine Skolem functions from LRAT refutations | 1 | Witnesses exist only where the conjecture is already certified (m ≤ 14). |
| 44 | set theory / descriptive set theory / reverse mathematics | Δ | Autarky local-to-global BA(n,k) | 1 | BA(7,3) false on ETV26. |
| 45 | formal methods / verification / theorem proving | Δ | Skolemize ∃Δ: rule language plus certification for m ≤ 36 | 2.5 | Evidence says Δ is a global choice; the a = 4 gates may fail. |
| 46 | interactive theorem proving / proof complexity / complexity | Δ | Lean-checkable kernel; window obstruction | 1 | Relabels easy steps; the obstruction is attack 7's window lemma. |
| 47 | algorithm design / parameterized complexity / analysis | Δ | Row-extreme (Baek-type) selection RX(n) | 2 | Likely a fast INFEASIBLE; label rules are too weak. |
| 48 | randomized / approximation / exponential algorithms | Δ | CTL: explicit transversal library | 1 | One-sided bound false: w24 has \|R\| = 17 > 16 (EXACT, two programs); two-sided at equality. |
| 49 | exact algorithms / SAT / SMT | Δ | Decide S19′ realizability; CEGAR for CONJ-TS′(7) | 3 | Superseded: S19′ is realizable (s19/realize). |
| 50 | computational geometry / constraint satisfaction | Δ | Frame-relaxed D^proj(5,n) | 2 | The extra freedom does not help a proof and cannot be settled finitely. |
| 51 | symbolic computation / computer algebra / experimental math | Δ | Profile algebra over ES compositions | 3 | Covers a nice class only (S15 is prime); its requirement system W_8 is ETV-hard. |
| 52 | real algebraic computation / computer-assisted proof / interval arithmetic | Δ | σ13 is a real 13-point set | 1 | Realizability is not the missing ingredient. |
| 53 | probabilistic / entropy / polynomial method | Δ | No-go for averaging and polynomial methods | 0 | First moment ≥ 55.5 on ETV42, counting only 191 heptagons. |
| 54 | discharging / flag algebras / spectral method | U | PAIR(i,j,c) rows across the nine Baek blocks | 3 | c = 42 is capacity 21 in disguise; the F-side lever is stalled (ROADMAP §6); SAT cost near the N5 ladders. |
| 55 | absorption / containers / regularity | Δ | VE(n): valid-envelope absorber | 2 | A reformulation; it contains weak D(U). |
| 56 | extremal set theory / set systems / intersection theorems | Δ | Pinch lemma plus Bollobás set pairs | 1 | Every point of ETV26 is a pinch point; no finite reduction. |
| 57 | association schemes / Boolean function analysis | U | 84 F-states = J(9,3); Baek rows = point-stars | 0.5 | The scheme structure is bookkeeping and does not see the geometry. |
| 58 | Young tableaux / partitions / symmetric functions | U | Hook split: \|S\| ≤ 42 + min(\|O\|, \|O′\|); OH(8,t) | 2 | OH is not easier than the bound; O is not 4-cap-free. Two-sided state rules UNSAT on the pools. |
| 59 | Schubert calculus / comb. representation theory / comb. commutative algebra | Δ | Profile rule PR(5,n) on (λ_L, λ_R) | 2 | Pointwise; already refuted on the pools by idea 58 (COMPUTED). |
| 60 | tropical comb. / cluster algebras / incidence algebras | Δ | Log-Plücker gate for S19′; tropical-limit lemma | 2 | Superseded (S19′ realizable); per-witness gates cannot reach all sizes. |
| 61 | finite fields / discrete harmonic analysis / enumerative geometry | Δ | F2 polynomial, Walsh and Sauer-Shelah readings | 0 | Degree 1.7 million against 42 variables on ETV42; parity vacuous. |
| 62 | topological / geometric / arithmetic Ramsey theory | Δ | Topological Hall with gons as colour classes | 0.5 | Hypothesis fails on 4 stored (5,6)-sets, one of them real. |
| 63 | infinite / infinitary / transfinite comb. | Δ | Null result: the valid class is bounded | 0 | Compactness collapses to finite induction; the derivative does nothing on cup15. |
| 64 | comb. game theory / algorithmic game theory / descriptive comb. | Δ | Recourse hierarchy k*(a,n) of the online game | 1 | Bounded recourse only fails more often; a diagnostic. |
| 65 | species / symbolic comb. / discrete dynamical systems | Δ | Flat-module substitution reduction | 1 | Removes only decomposable sets; cup15 has no module; the induction hypothesis gets stronger. |
| 66 | generating functions / analytic NT methods / sieves | Δ | Signed count SC(5,n) on reduced cores | 0 | Zero on 6 of 40 random real sets with a good Δ (float orientations). |
| 67 | graph colouring / homomorphisms / additive energy | Δ | G-D(5,n): Δ independent in the 4-cap middle-pair graph | 3 | Very tight (4/353 on cup15); may be false; the graph is not hereditary. |
| 68 | hypergraph regularity / containers / graph minors | Δ | Substitution closure SC(n) for modules | 1 | Hard instances are prime (cup15 has 0 modules). |
| 69 | convexity / geometric transversals / discrete convex analysis | Δ | CAPCLOSED-D(5,n): Δ an up-island | 2 | Likely fails on ETV-type sets; the line-separable form is already false on cup15. |
| 70 | polytopes / face enumeration / rigidity | Δ | Matroid sandwich (Edmonds) | 0 | Equivalent to weak D via free matroids; the 4-cap-free complex is not a matroid. |
| 71 | oriented-matroid realizability / order types | Δ | BFP19 for S19′; BFP-CEGAR | 2.5 | Superseded (S19′ realizable); its LP timed out. |
| 72 | chirotopes / semialgebraic geometry / pseudoline arrangements | Δ | Realizability gate for the CONJ-TS′ route; Helly reduction | 3 | Superseded (S19′ realizable). |
| 73 | real algebraic sets / quantifier elimination / CAD | Δ | Bi-order normalization; bilinear LP for S19′ | 2 | Superseded; the normalization is classical. Flags ROUND2's "at most 8" (§6). |
| 74 | Positivstellensatz / SOS / SDP relaxations | Δ | Positivstellensatz test for S19′ | 2 | Superseded; narrow payoff. |
| 75 | moment methods (first/second moment, LLL, Sherali-Adams, Lasserre) | Δ | No route; negative result recorded | 0 | First moment ≥ 55.5 on ETV42; the relaxations can only refute. |

## 5. Methods that gave nothing concrete

### (a) Groups whose whole output is a no-go or a refuted existence principle (promise 0)

| idea | methods |
|---|---|
| 3 | topological, analytic and additive combinatorics |
| 5 | graph, hypergraph and extremal graph theory |
| 15 | abstract, group and finite group theory |
| 18 | exterior, tensor and Lie algebra |
| 19 | Lie theory, algebraic groups, ring theory |
| 26 | harmonic, Fourier and higher-order Fourier analysis |
| 28 | probability, operator and spectral theory |
| 29 | discrete probability, geometric probability, random matrices |
| 33 | entropy methods, coding theory, algebraic coding theory |
| 34 | combinatorial coding theory, number theory, elementary number theory |
| 35 | additive, analytic and algebraic number theory |
| 53 | probabilistic, entropy and polynomial method |
| 61 | finite field methods, discrete harmonic analysis, enumerative geometry |
| 63 | infinite, infinitary and transfinite combinatorics |
| 66 | generating functions, analytic number theory methods, sieve theory |
| 70 | polytope theory, face enumeration, rigidity theory |
| 75 | moment methods |

The shared reason: existence by counting, averaging, parity or topology needs an invariant that is nonzero on every
valid set. On small valid sets that have many Δs these invariants vanish, and the tight extremal sets leave no slack
for averaging.

### (b) Groups that report only a restatement or a weak lemma

| idea | methods | what it gave |
|---|---|---|
| 12 | projective, affine and Euclidean geometry | a restatement plus a greedy |
| 32 | dynamical systems, symbolic dynamics, information theory | no new leverage |
| 44 | set theory, descriptive set theory, reverse mathematics | autarky reduction, "gains nothing" |
| 46 | interactive theorem proving, proof complexity, complexity theory | no real leverage |
| 56 | extremal set theory | the pinch lemma, no leverage |
| 57 | association schemes, Boolean function analysis | bookkeeping only |

### (c) Single methods reported as no fit inside otherwise productive groups

| method | idea |
|---|---|
| arithmetic combinatorics | 4 |
| spectral graph theory; random graph theory | 6 |
| graph limit theory | 7 |
| incidence geometry | 10 |
| tropical geometry; symplectic geometry | 14 |
| representation theory; commutative algebra | 16 |
| Galois theory; module theory | 20 |
| algebraic topology | 21 |
| functional analysis (reproduces the vacuous fractional relaxation); complex analysis | 25 |
| asymptotic analysis | 27 |
| Diophantine geometry (negative only); multiplicative number theory | 36 |
| Diophantine approximation | 37 |
| semidefinite programming (θ equals the clique LP on perfect graphs); nonlinear programming | 39 |
| interval arithmetic | 52 |
| flag algebras (LP averaging only); spectral method | 54 |
| container method; regularity method | 55 |
| symmetric functions | 58 |
| cluster algebras; incidence algebras | 60 |
| arithmetic Ramsey theory | 62 |
| algorithmic game theory; descriptive combinatorics (obstructions only) | 64 |
| discrete dynamical systems | 65 |
| additive energy | 67 |
| hypergraph containers (asymptotic only); graph minor theory (vacuous) | 68 |
| SDP relaxations and finite flag-algebra SDP (refutation direction only) | 74 |

## 6. Corrections suggested for other records

These are not applied here: this file changes nothing else.

- **`README.md` (attack 6 row) and `VERIFICATION.md` §6.**
  - σ13 is realizable (ideas 11 and 52; unverified), so R(4,7) also fails for real point sets.
  - This supersedes "the failure was not realised by real points" and "Open. Realisability of σ13".
  - Coordinates: `/home/jay/research/data/roadmap-20261115/sweep/lens-ag-rag-cag/w13_realization.json`. Idea 52's
    points are listed in its return.
- **`ROUND2.md`, S19′ realizability.** "S19′ realizable ... OPEN" and "CONJ-TS′(7) for real sets with |S| ≥ 15 is
  OPEN" should become:
  - false at |S| = 19 (s19/realize, pending an independent check);
  - open at |S| = 15-18.
- **`ROUND2.md`, writer's remark.** "every signotope on at most 8 elements is realizable" should read "at most 7".
  - Reason: an m-element signotope is an arrangement of m + 1 pseudolines once the line at infinity is counted.
    Arrangements of at most 8 pseudolines are stretchable (Goodman-Pollack), while the simple non-Pappus arrangement has
    9.
  - Source: idea 73, a literature remark. The writer re-derived the correspondence by hand; it was not checked by
    computation.
  - The remark's use, for 6- and 7-point sub-signotopes, is unaffected.

## 7. Files and hazards

**Durable scripts** live in `/home/jay/research/data/roadmap-20261115/sweep/<label>/`:

| label | idea | notes |
|---|---|---|
| `lens-om-order-lattice` | 8 | |
| `lens-ag-rag-cag` | 11 | `w13_realization.json` only |
| `lens-dg-polyhedral` | 13 | |
| `lenses-trop-sympl-linalg` | 14 | |
| `lenses-rep-inv-commalg` | 16 | |
| `lie-alggroups-ring` | 19 | |
| `lenses-field-galois-module` | 20 | |
| `eqtop-homology` | 23 | `instance6.txt` is the HD counterexample |
| `lens-asym-measure` | 27 | |
| `lens-prob-geomprob-rmt` | 29 | |
| `lens-conc-mart-stoch` | 30 | |
| `lens-percolation-statmech-ergodic` | 31 | |
| `coding-nt` | 34 | |
| `nt-lenses` | 35 | |
| `lens-dioph-optim-combopt` | 37 | |
| `lens-convex-discrete-ip` | 38 | |
| `lens-polyopt-cp` | 40 | |
| `itp-proofcx` | 46 | |
| `lens-rand-approx-exp` | 48 | `w24.txt`, with `SHA256SUMS` |
| `lens-csp-cg-ca` | 50 | |
| `symcomp-profile` | 51 | |
| `symfun-tableaux` | 58 | |
| `ramsey-lenses` | 62 | |
| `lens-coloring-homomorphism` | 67 | |
| `minor-regularity-containers` | 68 | |
| `lens-gtt-convexity-dca` | 69 | |
| `lens-tgt-om-ot` | 71 | |
| `lens-pseudoline-chirotope-semialg` | 72 | |
| `lens-rag-qe-cad` | 73 | |

**Not durable: the session scratchpad** `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/1e71bc06-5c09-4f54-ae48-3fca76aaa352/scratchpad/`.
Since 16 Nov 00:55 KST a durable copy with the same relative paths is at
`/home/jay/research/data/roadmap-20261115/scratchpad-snapshot-20261116/`.
Copy these files before reuse:

| idea | files |
|---|---|
| 1 | `pairchk.py` |
| 2 | `thr_ends.py` |
| 4 | `lens/forced.py` |
| 7 | `shadow.py` |
| 10 | `wdcup.py` |
| 12 | `pencil/pencil.py` |
| 15 | `sym.py`, `rho.py`, `rhoall.py` |
| 18 | `ext/sigma.py` |
| 21 | `natrule.py` |
| 24 | `relhom.py` |
| 33 | `parity.py`, `parity2.py` |
| 44 | `aut.py` |
| 47 | `rowx2.py` |
| 61 | `cnt.py` |
| 63 | `inf/cb.py` |
| 64 | `parity.py` |
| 66 | `signed.py` |

**Hazard:** `parity.py` was written in turn by ideas 33, 34 and 64 (idea 34 reports that its own version was replaced).
The current file, dated 05:51, belongs to the last writer.

**No files at all** (inline runs or hand checks only): ideas 3, 5, 6, 9, 17, 22, 25, 26, 28, 32, 36, 39, 41, 42, 43,
45, 49, 52, 53, 54, 55, 56, 57, 59, 60, 65, 70, 74, 75. The full lens returns exist only in the workflow relay to this
stage, and in the run file `wf_b43dabb6-560.json` once the workflow writes it. This file is their durable summary.

**Other notes.**
- The sweep produced **no LRAT proofs**, so nothing in it is newly CERTIFIED. Its UNSAT answers are pysat verdicts
  (ideas 21, 58).
- Budget: idea 58's full-pool run used 33 CPU-s and a peak of 1.46 GB, over the 10 CPU-s cap; idea 71 used about
  15 CPU-s. All lens work ran on one thread.
