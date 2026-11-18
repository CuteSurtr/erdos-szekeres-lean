# LFR20261113: a lazy full-support refuter for the coupled owner model (13 November 2026)

Track F of the 13 November evening session, 16:58 KST until the cut-off at about 19:40 KST. Work directory
`/home/jay/research/data/lfr-20261113/` (abbreviated W; not in Git, 1.4 GB). `tools/` and `data/` of this record
are **empty**: the copy step (`W/assemble.sh`) was never run, so every file named below is in W (§8). Nothing is
committed and no existing file was changed. Every job ran in a `nov13c-lfr-*` user unit with one thread.

**STATUS (phase 2, 20:52 KST): complete. No job of this track is running.**

> Phase-1 agent cut off at about 19:40 KST; completed from the work directory by a phase-2 agent at 20:52 KST
> (13 November 2026). Sections 1–3 and most of §4–§6 are the phase-1 agent's text. The phase-1 draft
> `W/README_sec4to8.md` (19:18) had placeholders, which were filled from W's logs, and a few of its statements
> were corrected against the logs (marked "corrected"). The phase-1 run `lazyall.py` (19:25–19:36) and its
> certificate were not in the draft and are described in §4.5. The phase-1 final chain (`W/final_chain.sh`) was
> never started. In its place the phase-2 agent ran the read-only checks marked "phase 2" (single checks under one
> minute each, outputs in the agent's scratch directory, nothing written in W). Some of them used a scratch copy
> of the tools, because the originals write work files into W.

Labels: **PROVED** = written argument; **CERTIFIED** = CaDiCaL 2.1.3 LRAT proof accepted by cake_lpr
(`s VERIFIED UNSAT`) for the stated CNF; **COMPUTED** = solver verdict or exact re-check only;
**HEURISTIC** = search statistics.

## 0. Summary

1. **The lazy full-support refuter works at the frontier.**
   - *18-hole witness of ETV5N (N5 catalog).* For its 66-owner occupied set the whole coupled CNF (62,920
     variables, 7.57 M clauses after pruning) is decided UNSAT in 3.7 s (COMPUTED). The full-support CNF is
     **CERTIFIED** UNSAT (cake_lpr, 10.2 s), and a 15-state core of it is **CERTIFIED**.
   - *19-hole vectors over the 305,090 rows of ETV5N.* All five vectors found were UNSAT on full support
     (COMPUTED, at most 6 s each). They gave five **CERTIFIED** cores (18–24 states), five **CERTIFIED**
     template CNFs and 64 transported rows. Level 19 of N5 was not closed, and nothing new is claimed for N5.
2. **N66 miniature CEGAR (COMPUTED).** Starting from 52 cycle rows, the full-support loop closed levels 6–10 by
   18:22 KST, i.e. at least 11 holes and **N66 ≤ 59, COMPUTED**. The level closures are plain or in-process
   CaDiCaL verdicts on the PB master and were never certified. Every row it added rests on a CERTIFIED core or
   template CNF (502 + 502 cake_lpr verdicts) plus the transport and mirror arguments of §2.4. Level 11 was
   undecided after 47 minutes (35,590 rows). N66 ≤ 59 had been CERTIFIED independently at 18:11 in
   N66N20261113.
3. **Single-CNF bounds with no rows, no transport and no PB arithmetic.** They are CERTIFIED for the stated CNFs;
   the bound follows modulo the encoder `lfr.Inst` and §2.5.
   - **N66 ≤ 62**: the monolithic optional-owner CNF "at most 7 holes" (9.95 M clauses), trimmed to 38,436
     clauses (§4.4).
   - **N66 ≤ 61**: the lazy monolithic CNF "at most 8 holes" (917,518 clauses), trimmed to 38,401 clauses
     (§4.5).
   - *Phase 2 re-checks.* The L = 7 trimmed pair was re-checked by cake_lpr. The kept L = 8 trimmed CNF was
     re-solved, and the fresh LRAT proof was accepted by cake_lpr. Every clause of both trimmed CNFs was shown
     to be a clause of the full L = 7 CNF of `monocert.py`, or of the regenerated totalizer, or the bound unit.
   - These bounds are weaker than the certified N66 ≤ 59 of N66N20261113. Their value is the independent
     trusted base.
   - COMPUTED only: "at most 9 holes" UNSAT (N66 ≤ 60, in-process CaDiCaL 1.9.5). "At most 10 holes" was
     undecided after 555 s.
4. **No gap seen between the coupled model and the ETV values (HEURISTIC).** The largest coupled-SAT sets
   found by greedy growth have exactly the ETV sizes, 42 (N5) and 50 (N66). The ETV occupied sets are saturated
   (COMPUTED). In the positive controls, the exact geometric assignments of the ETV sets violate none of the
   clauses, including all pool clauses inside their occupied sets (re-run in phase 2 with the final pools).
   Nothing is proved about larger SAT sets.
5. **Memory.** Three units were stopped by the session memory guard (18:31–18:37; §6). None was killed by the
   kernel. One of them (`f1`, 18:36) was itself an unchanged restart of a stopped cake_lpr check, made before the
   phase-1 agent had found the policy. After 18:37 nothing was restarted unchanged.
6. **Not done (cut off).** The final chain was never run: the certificate of the closed N66 level 10 over its
   rows (`pbcert2.py`), the transport of the w18 core, the certified saturation (`satcert.py`) and four more
   greedy runs. The copy into this record (`assemble.sh`) was not run either. Phase 2 replaced three of the
   final-chain controls (pool check, row soundness, cross-validation for N5 and N66) by short re-runs (§5).

For the ES(8) programme (see §7): LO33N20261113 now shows that **N66 ≤ 57 suffices for ES(8) ≤ 309 with the
certified coupled rows**, and that N66 ≤ 58 suffices together with slice 21. The N66 levels that matter are
therefore 11 (certified) and 12. This record's methods reached level 10 (row CEGAR, COMPUTED) and level 8
(single-CNF certificate).

## 1. Question

ETV5N20261113 refutes candidate hole vectors of the internal state catalog by demand-one rows that come from
UNSAT coupled owner CNFs on *small* supports (9–22 owners), because the "complete no-octagon" family of
`coupled5.py` has C(n, 8) clauses. At the frontier (18–19 holes for N5) small refutable subsets are rare
(probe yield about 1 in 1,500). Question of this track: can the coupled CNF be decided on the *whole* occupied
set O of a candidate vector (50–66 owners) at once, what does that cost, what cores come out, and where is the
limit of the coupled model?

## 2. Model and soundness (PROVED: written arguments; checks as stated)

Setting, labels, states, Growth, Lemma R, refined domains D′ and the six-order table TT are exactly those of
ETV5N20261113 §2 (catalog (A, B): caps ≤ A+1 points, cups ≤ B+1 points, no convex octagon; N5 is (3, 6) with
84 states, N66 is (4, 4) with 70 states). S is a real configuration of the class, T = (s₀, …, s_{n−1}) a
support of distinct states, all assumed occupied, v_i the owner of s_i.

### 2.1 Atoms and clause families (`lfr.py`, class `Inst`)

Atoms: before(i,j), cap_ge(i,j,k), cup_ge(i,j,k), orientation(i,j,k) with the meaning of `coupled5.py`
(orientation(i,j,k) for i<j<k is det(p_i,p_j,p_k) > 0; a permutation flips the sign by parity). There is no
convex_four atom. Each clause below is true for the owners of S:

1. **mono**: cap_ge(k+1) → cap_ge(k), cup_ge likewise (definitions; coupled5 family 1).
2. **trans**: ¬before(a,b) ∨ ¬before(b,c) ∨ before(a,c) (x-order is a strict total order; family 2). Because
   before(i,j) is one variable with a sign, the clauses of (a,b,c), (b,c,a), (c,a,b) coincide; one
   representative is kept, so the family forbids both cyclic tournaments on every triple.
3. **growth**: before(a,b) ∧ before(b,c) ∧ [abc] < 0 ∧ cap_ge(a,b,k) → cap_ge(b,c,k+1) with cap_ge(·,·,A+1)
   false, and the cup version with [abc] > 0 and ceiling B (Growth plus the ceilings; family 3).
4. **apex** (slope order). Let a be left of p, q, r, or right of all three. Then the signs
   ([apq], [aqr], [arp]) are neither (+,+,+) nor (−,−,−).
   *Proof.* det(a,p,q) = (p_x−a_x)(q_x−a_x)(m_q − m_p) with m_z the slope of the line a z. If p, q are on the
   same side of a the first two factors have a positive product, so [apq] > 0 ⇔ m_p < m_q. A cyclic pattern
   would give m_p < m_q < m_r < m_p. ∎
   Clause: ¬before(a,p) ∨ ¬before(a,q) ∨ ¬before(a,r) ∨ (the three orientation literals are not all true),
   the same with "not all false", and both again with a on the right.
5. **sig4**. For the x-order a<b<c<d the pattern ([abc],[abd],[acd],[bcd]) is neither (+,−,−,+) nor
   (−,+,+,−). *Proof.* math.md §2.1: (c_x−b_x)[abd] = (d_x−b_x)[abc] + (b_x−a_x)[bcd]; if [abc] and [bcd]
   have the same sign, [abd] has it too. ∎ (Two of the eight patterns of coupled5 family 4.)
   *Equivalence with family 4* (used only for SAT statements): in an x-ordered quadruple the other six
   forbidden patterns are (+,−,+,·), (−,+,−,·) (apex clause of the leftmost point a on b,c,d: [abc], [acd],
   [adb] all positive or all negative) and (·,+,−,+), (·,−,+,−) (apex clause of the rightmost point d, since
   [abd] = [dab], [acd] = [dac], [bcd] = [dbc]). So apex + sig4 + trans imply "at most one sign change" on
   every quadruple in the x-order of any model, and conversely each apex / sig4 clause follows from
   family 4 with transitivity.
6. **empty / domain / positive**: the state-dependent families 7, 8, 9 of coupled5, same tags
   ('empty', u, v), ('domain', u, v, a, b), ('positive', i, j, k), same clauses.
7. **poly** (lazy; replaces the complete no-octagon family 6). For owners c₁, …, c_a and u₁, …, u_b with
   c₁ = u₁, c_a = u_b, otherwise distinct, a + b = 10, the clause says: not (before(c_i, c_{i+1}) for all i,
   before(u_i, u_{i+1}) for all i, [c_i c_{i+1} c_{i+2}] < 0 for all i, [u_i u_{i+1} u_{i+2}] > 0 for all i).
   **Lemma P.** If all these literals held for points of S, the 8 points would be the vertices of a convex
   octagon. *Proof.* The chain c₁…c_a is x-monotone and every consecutive triple turns right, so its
   slopes strictly decrease: it is the graph of a strictly concave piecewise linear function f on
   [x(c₁), x(c_a)]. Likewise u₁…u_b is the graph of a strictly convex piecewise linear g on the same
   interval, and f = g at both ends. A concave function lies on or above its chord and a convex one on or
   below, so g ≤ f, and K = {g ≤ y ≤ f} is convex (hypograph of f ∩ epigraph of g). Every chain point is an
   extreme point of K: the two end points have the extreme x-coordinates, an interior point of the upper
   chain is a strict corner of the concave graph (slopes strictly decrease) and similarly below. Eight
   extreme points of a convex set are in convex position. ∎
   The class has no convex octagon, so the clause is true. Only the order *inside* each chain is used (8
   order literals), so one clause covers every interleaving of the two chains.
   *Which (a, b) are needed.* A chain of A+2 owners with all consecutive triples negative contradicts the
   growth clauses (they force cap_ge(c₂,c₃,2), …, cap_ge(c_{A+1},c_{A+2},A+1) = false); the same for cups
   with B+2 owners. So only a ≤ A+1, b ≤ B+1 remain: (4,6) and (3,7) for N5 (the 8-cup, a = 2, is excluded by
   growth), (5,5) for N66.

So if base clauses plus any set of poly clauses is unsatisfiable, the states of T are never all occupied:
**demand-one row on T**. This uses only that every clause is true for real owners; it does not depend on
how the poly clauses were found, nor on the pruning below, nor on the comparison with coupled5.

### 2.2 The lazy loop and what SAT means

`Lazy.solve`: solve; on SAT read the x-order π and the orientations of the model, compute by an O(n³) DP for
every pair L < R (in π) the longest chain from L to R whose consecutive triples are all negative, and the
longest with all positive (`chain_tables`); every pair with cap + cup ≥ 10 and every admissible split (a, b)
gives one violated poly clause (`find_polygons`); add them and repeat.

*Termination with SAT is a SAT answer for coupled5's CNF.* Let a model satisfy families 1–6 and contain no
pair (L, R) with cap + cup ≥ 10. By 4–5 its orientation is a signotope in the order π. Suppose 8 owners had
all 70 quadruples convex in the sense of coupled5 family 5 (in x-order the convex patterns are (+,+,+,+),
(−,−,−,−), (+,+,−,−), (−,−,+,+)). Let L, R be the first and last of them, U the others p with [LpR] < 0 and
D those with [LpR] > 0. For p < q in U the quadruple (L,p,q,R) has second and third sign negative, so it is
(−,−,−,−): [Lpq] < 0 and [pqR] < 0. For p < q < r in U the quadruple (L,p,q,r) has its first three signs
negative and is convex, so [pqr] < 0. Hence L, U, R is a chain with all triples negative, L, D, R one with
all triples positive, |U| + |D| + 4 = 10: the DP would have reported the pair (L, R). So no 8 owners have all
quadruples convex, and the model extends (by the definition clauses of convex_four) to a model of the
complete CNF of `coupled5.py`. In addition `verify_model` re-checks every reported model semantically and
independently of the clause generator: total order, labels in the refined domains, growth on every x-ordered
triple, forced orientations, at most one sign change on every x-ordered quadruple, no polygon, chain ceilings.

### 2.3 Pruning

A clause is omitted when one of its literals is true (i) under a unit clause of the same CNF on the clause's
own owners (empty-domain units, positive units), or (ii), for all families except trans and only in
`prune='closure'` mode, under the transitive closure of the forced order. Omitting clauses can never make an
UNSAT answer unsound. For SAT answers: with rule (i) the omitted clause is implied by a unit clause; with
rule (ii) every model satisfies the closure because trans is pruned only by rule (i), so the closure is
derivable from kept clauses (if b→a is derived from b→c, c→a, the clause of (b,c,a) is kept unless b→a is
itself a unit). Typical effect: for the 66 owners of the 18-hole witness 1,600 of 2,145 pairs are ordered by
units (the closure adds nothing), 6,427 of 45,760 orientations are units, and the CNF has 7.57 M clauses
instead of the 138 M of the unpruned signotope packets.
`prune='direct'` (rule (i) only) is used when owners are optional (§2.5).

### 2.4 Cores, certificates, transport

- *Selectors.* With `selectors=True` every clause carries ¬sel(o) for each of its owners. UNSAT under the
  assumptions {sel(o) : o ∈ T′} means the clauses whose owners all lie in T′ are contradictory. Deletion
  minimisation (`refute.deletion`) is discovery only.
- *Certificate of a row.* For a core T′ the CNF `Inst(T′)` + all pool poly clauses inside T′ is written
  without selectors, solved by CaDiCaL 2.1.3 `--lrat`, and checked by cake_lpr. Every clause of that CNF is
  true for real owners of T′ by §2.1, so `s VERIFIED UNSAT` certifies the demand-one row on T′, modulo the
  encoder.
- *Full-support certificate.* The same for the whole occupied set (7.57 M clauses for the 18-hole witness).
- *Trimmed certificates.* `lrat_trim2.py` traces the LRAT hints backwards from the empty clause with
  bounded memory, writes the used original clauses in their original order (a subset of the CNF) and the
  needed lemmas with renumbered clause ids; cake_lpr checks the trimmed pair. Unsatisfiability of a subset
  implies that of the whole CNF, and every clause of the subset is still one of the valid clauses. (Tested
  by the phase-1 agent: a trimmed pair is accepted; after removing one clause from the trimmed CNF cake_lpr
  rejects; the trimmed CNF equals the kept-index subset of the full CNF. No output of the negative test was
  kept. Phase 2: all 38,436 lines of the L = 7 trimmed CNF occur in the full CNF, §5.)
- *Transport.* The used original clauses are read off the proof; the state-dependent ones (tags) are
  shrunk while "non-state clauses + poly clauses + kept tests" stays UNSAT (`refute.shrink_tests`), that
  template CNF is certified by cake_lpr (`cegar.template_cert`), and `transport5.search` enumerates the
  injective maps σ for which every kept test holds. The non-state clauses and the poly clauses are true for
  the owners of *any* distinct states (they do not mention states), the kept tests are true for σ's states, so
  the template CNF refutes image(σ): demand-one row (the argument of ETV5N §2 "Transport"). For A = B the
  reflection y → −y maps the class to itself and every state to its transpose (`sym66.py`, checked there), so
  the mirror image of a row is a row.

### 2.5 Optional owners (monolithic CNF, `mono.py`, `monocert.py`)

All N states are owners, every clause carries its selectors, sel(s) is read as "state s is occupied", the two
fixed states are units, and a totalizer bounds the number of false selectors by L. For a real configuration
set sel(s) true exactly on its occupied states and give the present owners their geometric values: every
clause with an absent owner is satisfied by ¬sel, every other clause by §2.1 (rule (i) pruning only uses
units of the clause's own owners, so it is valid for every subset of present owners), and the totalizer
clauses with output L false are satisfiable whenever at most L inputs are true (brute-force self-test of
pysat's ITotalizer, 11,040 cases, `monocert.selftest`). Hence UNSAT under "at most L holes" means: every
configuration of the class has at least L + 1 holes. No rows, no transport and no pseudo-Boolean arithmetic
are involved.

### 2.6 What a SAT set is: the limit of the method

If the CNF of O is satisfiable, the model is an abstract x-ordered configuration (a signotope) on |O| points
with no chain of A+2 negative or B+2 positive consecutive triples and no cap/cup pair forming an octagon.
So a coupled-SAT set of m states exhibits an *abstract* configuration of the class with m points, and the
coupled model can never prove a bound below the largest such m. Every real configuration gives a SAT set
(soundness), so the limit is at least the ETV value (42 for N5, 50 for N66). (Remark, not written out: the
catalog lemmas only use triple signs and the signotope property, so conversely the occupied set of any
signotope of the class should be SAT; the limit of the method would then be exactly the extremal number of
the class for signotopes.)

## 3. Tool

| file | role |
|---|---|
| `lfr.py` | clause generator `Inst` (numpy; 1.3 s for 66 owners), lazy solver `Lazy` (pysat CaDiCaL 1.9.5, incremental, optional owner selectors), polygon DP, persistent `Pool` of poly clauses keyed by states, `verify_model`, LRAT helpers |
| `refute.py` | `refute` (full pipeline with full-support certificate), `refute_cores` (selector instance, deletion minimisation, several cores per vector), `certify_support`, `shrink_tests`, `transport` |
| `cegar.py` | miniature CEGAR: CaDiCaL 2.1.3 on the PB CNF (`pbcnf5.build`) → vector → cores → certified core and template → transported rows (+ mirrors when A = B); resumable |
| `cegar2.py` | the same with one persistent selector instance over all states and an in-process master (needs more than 4 GB for N66: stopped by the memory guard, §6) |
| `mono.py`, `monocert.py` | monolithic optional-owner CNF (in-process levels; single-CNF certificate) |
| `lazyall.py` | lazy monolithic CNF (§4.5); **edited at 19:28:36, after the run of 19:25 had started: the version that ran is not preserved** |
| `lrat_trim2.py` (`lrat_trim.py`) | bounded-memory backward trim of a CNF + LRAT pair (forward superset variant) |
| `grow.py`, `satcert.py` | greedy growth of SAT sets; certified saturation of the ETV occupied sets (`satcert.py` never run) |
| `posctl.py`, `soundness_lfr.py`, `xval.py` | controls (§5) |
| `pbcert.py`, `pbcert2.py` | LRAT + cake_lpr certificate of a closed level over the current rows (never run) |
| `final_chain.sh`, `assemble.sh`, `w18transport.py`, `trimcake.sh`, `cakeonly.py`, `trimstats.py` | final controls (never run), copy into this record (never run), w18 transport (never run), cake_lpr on a trimmed pair, cake_lpr alone (stopped, §6), trim statistics |
| `report.py`, `summ.py`, `quota.sh` | log summaries; CPU quota sum of the other tracks |
| `etv_common.py`, `coupled5.py`, `transport5.py`, `engine.py`, `geom.py`, `pbcnf5.py`, `sym66.py`, `etvcon.py`, `blocks5.py`, … | unchanged copies from ETV5N20261113 / ETVTHY20261113 / track A, so that the tools run on their own |

Sizes: 66 owners of N5 give 62,920 variables and 7,566,789 clauses (mono 10,725; trans 9,490; growth
705,810; apex 3,521,073; sig4 3,271,273; state-dependent 48,418). All 70 states of N66 with selectors give
71,645 variables and 9,822,279 clauses.

## 4. Measurements

All times are for one thread (CPUQuota 100 %). "Level L closed" means: the row system (or the monolithic CNF)
has no vector with at most L holes, i.e. at least L + 1 holes, i.e. N ≤ #states − L − 1.

### 4.1 N5 catalog (A, B) = (3, 6): the 18-hole witness and 19-hole vectors

**18-hole witness of ETV5N** (`witness18_final_rows.json`; 66 owners). It satisfies the 290,242 rows of 09:16.
In ETV5N it was refuted by density-grown supports: 6 UNSAT of 70 probes in a cube-driven round on 5 threads,
about ten minutes after it appeared.

| step | result |
|---|---|
| build / load | 1.3 s / 4.3 s; 62,920 variables, 7,566,789 clauses |
| lazy solve of the whole occupied set | **UNSAT in 3.7 s**, 6 lazy rounds, 4,717 poly clauses (COMPUTED) |
| full-support certificate | CNF of 7,571,506 clauses (298 MB, SHA-256 `5fa0dde6…`), CaDiCaL 2.1.3 2.7 s, LRAT 1.8 MB (`a883d38d…`), cake_lpr 10.2 s: **CERTIFIED UNSAT**. The proof uses 1,143 original clauses (589 state-dependent, 21 poly) |
| owners in the traced proof | 65 of 66 (the full-support trace is not selective) |
| selector minimisation | 34 solves, 10.1 s → **core of 15 states** [33, 40, 43, 47, 50, 57, 61, 63, 71, 73, 76, 77, 78, 79, 80] |
| core certificate | own CNF (15,432 clauses, `28998af8…`; LRAT `d86e6732…`), **CERTIFIED** |
| transported rows of the core | **not computed**: `w18transport.py` was part of the final chain, which was never run |
| total | 36.3 s (unit `nov13c-lfr-w18`, 17:11) |

**19-hole vectors.** `cegar.py` at level 19 over the 305,090 rows of `final19/rows_final.json` (read-only
copy): each vector satisfies all 305,090 rows and the rows added by the earlier rounds.

| vector | finder s | full-support solve s | lazy rounds | lazy clauses | core (states) | minimise s | tests used → kept | transported rows |
|---|---|---|---|---|---|---|---|---|
| 1 | 10.6 | 5.9 | 5 | 5,310 | 20 | 22.5 | 186 → 154 | 2 |
| 2 | 7.5 | 1.8 | 2 | 3,164 | 24 | 14.4 | 253 → 160 | 14 |
| 3 | 35.2 | 3.3 | 4 | 5,608 | 23 | 30.7 | 353 → 240 | 4 |
| 4 | 107.0 | 0.3 | 0 | 5,396 | 23 | 15.6 | 284 → 166 | 22 |
| 5 | 17.1 | 2.1 | 2 | 6,011 | 18 | 12.3 | 123 → 96 | 22 |

All five are UNSAT on full support (COMPUTED); the five cores and the five template CNFs are CERTIFIED;
"lazy clauses" includes the clauses taken over from the pool. The run was stopped after five rounds
(5.5 minutes, 17:15–17:20) to keep the thread for the other measurements; level 19 is not closed and nothing
is claimed for N5. Observations (HEURISTIC):
- At the frontier the refuter never failed and never needed more than 6 s.
- The minimal cores it returns are larger (18–24 states) than the 13–18-state cores that small-support probing
  finds. They also transport poorly: 2–22 rows, against the several thousand of a 13-state core.
- The vector finder (CaDiCaL on the PB CNF with 305 k rows) is now the slow step (7–107 s).

### 4.2 N66 catalog (A, B) = (4, 4): miniature CEGAR

Start: the 50 cycle rows of `cyc_base_A4B4.json` (track A; 6-hole optimum) closed under the mirror map (52
rows). Each round: vector with at most L holes → full-support refutation → core(s) by selector deletion →
core certificate → shrunk tests → template certificate → transported rows → mirrors. One core per vector
until 17:59, two per vector afterwards. Three runs:
- `cegar.py`, unit `nov13c-lfr-n66cegar`, 17:35:48–17:59:57: 114 rounds, stopped at level 10.
- `cegar2.py`, `nov13c-lfr-n66cegar2`, 18:13:17–18:31:26: 62 rounds, stopped by the memory guard.
- `cegar.py` again, `nov13c-lfr-f6`, 18:45:23–19:23:02: 132 rounds at level 11. The phase-1 agent stopped it to
  free the thread for §4.5.

| level closed (≥ L + 1 holes) | bound | at | rows then | wall s spent on the level | verdict (all COMPUTED) |
|---|---|---|---|---|---|
| 6 | N66 ≤ 63 | 17:36:07 | 58 | 19.1 | PB CNF "at most 6 holes" UNSAT, plain CaDiCaL |
| 7 | N66 ≤ 62 | 17:36:56 | 200 | 49.0 | same |
| 8 | N66 ≤ 61 | 17:39:00 | 690 | 124.1 | same |
| 9 | N66 ≤ 60 | 17:45:47 | 5,168 | 406.2 | same |
| 10 | N66 ≤ 59 | 18:22:12 | 14,475 | 1,385: 850 in `cegar.py` (68 rounds, 17:45:47–17:59:57) + 535 in `cegar2.py` (26 rounds) | in-process master "at most 10 holes" UNSAT (CaDiCaL 1.9.5) |
| 11 | – | not closed | 35,590 at 19:23:02 | 2,813 and undecided: 554 in `cegar2.py` (36 rounds, stopped by the guard at 18:31:26) + 2,259 in `cegar.py` (132 rounds) | – |

Every vector the finder produced was UNSAT on full support. Over 308 rounds (114 + 132 of `cegar.py`, 62 of
`cegar2.py`), the full-support solve took 0.34 s, 0.21 s and 0.03 s on average in the three runs, 0.9 s at most.
No vector was SAT and none timed out (no `MODEL_LIMIT` or `unknown` event in the logs).
- **Cores.** 502 cores: 114 + 264 from `cegar.py`, sizes 8–31 states; 124 from `cegar2.py`, sizes 11–33. Every
  core CNF and every template CNF carries a cake_lpr `s VERIFIED UNSAT` verdict, 502 + 502 in all, with CNF and
  LRAT SHA-256 in `cegar_n66_log.jsonl` and `cegar2_n66_log.jsonl`. The CNF and LRAT files themselves were not
  kept. Transport gave 15,436 + 3,444 rows before deduplication and mirrors.
  `cegar_n66_rows.jsonl` holds the 35,538 added rows; with the 52 base rows that makes 35,590.
- **Levels.** The levels are COMPUTED: plain CaDiCaL verdicts on the PB CNF, or the in-process master.
  **No level closure was certified.** `pbcert2.py` (CaDiCaL LRAT + cake_lpr of the PB CNF over the current
  rows) was written at 19:21 for the final chain and never run. N66 ≤ 59 is CERTIFIED elsewhere (N66N20261113,
  18:11).

Comparison (HEURISTIC; the phase-1 agent's read-only look at W of track A; only the 17:14 time is confirmed by
the N66N record): the ETV5N-style loop of track A (5 threads, face-union and density probing) reached level
10 at 17:14, 17 minutes after its start. It was still at level 10 at 18:16, with 645 cores and 7,273
transported rows. The full-support loop reached level 10 after 10 minutes on one thread. It closed level 10
after about 33 minutes of compute on one thread: 24 min of `cegar.py` and 9 min of `cegar2.py`. *(Corrected:
the draft said 45 minutes; the logs give 33.)*

Time per level grows by a factor of about 3: 19 s, 49 s, 124 s, 407 s and 1,385 s for levels 6–10. Level 11
was not closed after 2,813 s (47 minutes).

### 4.3 Limit of the method

**Positive control (first data point).** `posctl.py`: the exact ETV sets `etvcon.etv(8,5,8)` (42 points; and
its x-reflection) and `etvcon.etv(8,6,6)` (50 points; and three reflections) are in the class (exact integer
check), their 42 / 50 states are distinct, and the exact geometric assignment (x-order, labels E₋/E₊ of the
whole set, determinants) satisfies every clause of `Inst(occupied set)`: 0 violations in 1,249,686 and
967,387 clauses (N5), 2,701,413 / 2,117,281 / 2,701,413 / 2,117,281 clauses (N66), and in every lazy clause
generated up to then. The lazy solver answers SAT on all six occupied sets in 0.1–1.3 s (1–33 lazy rounds),
with verified models (17:14). **Pool check (phase 2, 20:39).** `posctl.py --poolonly` was re-run from a
scratch copy of the tools on W's final pools: 85,260 poly clauses for N5 (`pool_A3B6.jsonl`, SHA-256
`e307e180…`) and 191,828 for N66 (`pool_A4B4.jsonl`, `10a37284…`). The geometric assignments of all six sets
violate no clause of `Inst(occupied set)` and no pool clause inside the occupied sets. There are 0 and 2,707 such
pool clauses for the two N5 sets, and 0, 9,764, 0 and 7,745 for the four N66 sets.

**Saturation of the ETV occupied sets.** For each ETV set tested and each state s outside its occupied set
O, the full-support CNF of O ∪ {s} is UNSAT (COMPUTED, `grow.py`): N5, both reflections, 42 of 42 states
each (0.0–1.2 s per state); N66, the set and its x-reflection, 20 of 20 each (≤ 3.4 s). **These verdicts are
COMPUTED only:** `satcert.py`, which would certify them with cake_lpr, was never run.
In words: if these verdicts are right, no configuration of the class, and no abstract configuration in the
sense of §2.6, occupies the 42 (50) states of the ETV set together with any further state.

**Greedy growth.** Starting from the two fixed states, every other state is tried once in a given order and
kept iff the grown set stays SAT with a verified model (UNSAT is monotone, so one pass gives a maximal set):

| run | catalog | order | maximal set | states accepted (verified SAT) | states refused (UNSAT) | largest solve s | wall s |
|---|---|---|---|---|---|---|---|
| `n5_fix_asc` | N5 (84) | ascending | **42** | 40 | 42 | 0.4 | 49.1 |
| `n5_fix_r1` | N5 | random, seed 1 | **42** | 40 | 42 | 2.4 | 151.2 |
| `n5_fix_r2` | N5 | random, seed 2 | **42** | 40 | 42 | 0.8 | 88.5 |
| `n66_fix_r1` | N66 (70) | random, seed 1 | **50** | 48 | 20 | 1.8 | 84.2 |
| `n66_fix_r2` | N66 | random, seed 2 | 47 | 45 | 23 | 1.9 | 82.5 |
| `n66_fix_r3` | N66 | random, seed 3 | **50** | 48 | 20 | 0.7 | 64.3 |

No answer was "unknown" and every accepted state had a verified model. The largest coupled-SAT sets found have
**42 states (N5) and 50 states (N66), the ETV values**. No SAT set above the ETV value was found. For N5 every
maximal set found has exactly 42 states. For N66 one run stops at a maximal set of 47 states, so maximal SAT
sets do not all have the same size.

*Phase-2 observation (HEURISTIC).* The maximal sets are not all ETV occupied sets:
- `n5_fix_asc` ends exactly at the occupied set of etv(8,5,8).
- The other two N5 sets differ from the occupied sets of etv(8,5,8) and of its x-reflection in 36–44 states.
- The two 50-state N66 sets differ from those of etv(8,6,6) and of its x-reflection in 20–28 states. They were
  not compared with the y- and xy-reflections.
- Whether they are occupied sets of real configurations was not examined.

So the data give no gap between the coupled model and the ETV conjecture. The proved lower bound on what the
model can ever prove is the trivial one (42 and 50: the real sets), and the frontier vectors (65 and 59–60
states) are all UNSAT. (HEURISTIC as evidence; nothing is proved about larger SAT sets.)

### 4.4 Monolithic optional-owner CNF

`mono.py` (all 70 states of N66 as optional owners, 71,645 variables, 9,822,279 clauses with selectors, no
rows; the pool of 70,327 poly clauses known at 18:00 was preloaded and no new poly clause was needed):
"at most L holes" is UNSAT for L = 5, 6, 7, 8 after 11.9, 71.6, 92.5, 392.5 s (in-process CaDiCaL 1.9.5,
incremental; COMPUTED): N66 ≤ 61 from one CNF. L = 9 was undecided after 179 s (deadline). About three times
slower per level than the CEGAR, with the same growth factor.

**Single-CNF certificate: N66 ≤ 62 (CERTIFIED).** `monocert.py 7`: the monolithic CNF for L = 7
(71,979 variables, 9,948,111 clauses: 9,822,279 guarded coupled clauses, 125,057 guarded poly clauses,
2 fixed-state units, 772 totalizer clauses, 1 unit; 676 MB, SHA-256 `1e149253…`) is UNSAT for CaDiCaL 2.1.3
in 129 s (LRAT 713 MB, `c961fc89…`).
- *Trim and check.* The backward trim (`lrat_trim2.py`, 30 s) shows that the proof uses 38,436 of the 9,948,111
  clauses and 76,836 of the 6,429,664 lemmas. cake_lpr accepts the trimmed pair (CNF 2.0 MB, SHA-256
  `b7931c07…`; LRAT 23.7 MB, `0d921fef…`) in 0.5 s: **`s VERIFIED UNSAT`**.
- *Statement.* By §2.5 every configuration of the (4,4) class has at least 8 holes: **N66 ≤ 62**, with no rows,
  no transport and no PB arithmetic in the trusted base. *(Corrected: the draft called the previous proved
  bound 64. N66 ≤ 59 had already been CERTIFIED at 18:11 in N66N20261113 with rows and PB arithmetic; this
  certificate is weaker but independent of both.)*
- *Composition.* The 38,436 clauses are 9,331 apex/sig4, 9,625 growth, 9,697 domain, 1,363 empty units,
  3,824 positive units, 1,832 trans, 203 mono, 1,978 poly, 581 totalizer clauses and the 2 fixed units; all 70
  states occur (`monocert_A4B4_L7_trimstats.json`).
- *Phase 2 (20:27–20:38).* cake_lpr accepted the trimmed pair again (`s VERIFIED UNSAT`, 0.55 s, 1.0 GB). The
  full CNF still hashes to `1e149253…` and has 9,948,111 clause lines. Every one of the 38,436 trimmed clauses
  is a line of it.
- *L = 8.* The same was not run for L = 8 here: CaDiCaL needs 3.1 GB on the 9.9 M clause CNF within the first
  40 s, too close to the 4 GB budget of §6. L = 8 was certified by the lazy variant instead (§4.5).

### 4.5 Lazy monolithic CNF (`lazyall.py`, unit `nov13c-lfr-f7`, 19:25:02–19:36:03)

This is the CNF of §4.4 built lazily, to stay inside the memory budget.
- *Eager clauses*: the families mono, trans, growth and state-dependent, all guarded by selectors (877,677
  clauses); also the two fixed-state units and a pysat totalizer over the 68 hole literals −sel(s) with
  ubound 30 (1,985 clauses).
- *Seed* (37,853 clauses): the non-totalizer clauses of the L = 7 trimmed CNF of §4.4.
- *Lazy clauses*: apex and sig4 clauses are added only when a model violates them (at most 200,000 per round),
  and poly clauses when a model contains a polygon.

Command: `lazyall.py n66seed 5 <19:36:02> 8 200000 work_A4B4/mono_A4B4_L7_trim.cnf`.

| level | result | seconds | lazy rounds |
|---|---|---|---|
| 5, 6, 7, 8 | UNSAT (COMPUTED, in-process CaDiCaL 1.9.5) | 1.1, 5.1, 6.6, 10.4 | 0: eager + seed clauses were already UNSAT |
| 9 | UNSAT (COMPUTED): N66 ≤ 60 | 42.2 | 0 |
| 10 | undecided at the deadline | 555.1 | 169; 614,824 apex/sig4 and 336 poly clauses added |

**Certificate for L = 8: N66 ≤ 61 (CERTIFIED).**
- *The CNF.* It is the solver's clause set at level 8 plus the unit −rhs[8]: 72,088 variables, 917,518 clauses
  (877,677 eager, 37,853 seed, 1,985 totalizer, 2 fixed units, 1 unit), SHA-256 `1826f391…`.
- *Proof.* CaDiCaL 2.1.3 needed 24.0 s; its LRAT was 234 MB (`0abfa61a…`). The trim uses 38,401 clauses and
  282,716 of 1,752,390 lemmas. The trimmed CNF (1.8 MB, `54290773…`) and trimmed LRAT (84.7 MB, `a246f327…`) were
  accepted by cake_lpr in 1.6 s, `s VERIFIED UNSAT`. Statement logged at 19:26:06: "every configuration of the
  (A,B)=(4,4) class has at least 9 holes: at most 61 points".
- *What was kept.* By design, `lazyall.py` deleted the full CNF, the LRAT and the trimmed LRAT. Only the trimmed
  CNF `lazyall_A4B4_L8_trim.cnf` is kept (its SHA-256 still matches).
- **Phase-2 checks (20:27–20:38).**
  1. *Re-certification.* CaDiCaL 2.1.3 `--lrat` re-solved the kept trimmed CNF (UNSAT in 5.7 s; new LRAT
     102 MB, SHA-256 `d8c2471a46e1d00c…`, deleted after the check). cake_lpr accepted it: **`s VERIFIED UNSAT`**
     (2.3 s, 3.2 GB peak).
  2. *Origin of every clause.* 38,152 of the 38,401 trimmed clauses are lines of the full L = 7 CNF of
     `monocert.py` (SHA-256 `1e149253…`, re-verified). The other 249 are 248 clauses of pysat's ITotalizer,
     regenerated with the same inputs (−sel(s) for the 68 non-fixed states, ubound 30, top id 71,715,
     1,985 clauses, which matches the header's 72,088 variables), and the unit −rhs[8] = −72066 ("at most 8 holes").

  So the statement rests on the same encoder as the L = 7 certificate, `monocert.py` with `lfr.Inst`
  (prune='direct') and §2.5, plus the totalizer. It does not depend on `lazyall.py`, whose running version is
  not preserved (§3).

## 5. Controls and checks

- **Cross-validation with `coupled5.py`** (`xval.py`).
  - *N5 catalog.* 40 minimal cores of ETV5N are UNSAT. The same cores minus one owner are SAT in both tools, with
    models that pass `verify_model`. 60 random supports of 9–13 states agree (all SAT). The phase-1 agent's output
    was not kept. Phase 2 re-ran it at 20:39 with the same seed from a scratch copy (`coupled5.fast_solve` writes
    CNF files into the tools' directory) and got the same result in 8.0 s.
  - *N66 catalog (phase 2, 20:39; part of the final chain, never run in phase 1).* 40 cores of track A
    (`n66-20261113/cores.jsonl`, seed 2) are UNSAT. The same cores minus one owner are SAT in both tools with
    verified models. 60 random supports agree (all SAT). 7.6 s.
- **Geometric assignments** (§4.3): 0 violations on the ETV sets, including all pool clauses inside them.
  **Random real sets** (`soundness_lfr.py`, phase 2, 25 s per catalog from a scratch copy; part of the final
  chain, never run in phase 1). The script generates random point sets of the class (uniform, perturbed parabola,
  clusters, arcs), computes their exact states and labels, and evaluates every clause of `lfr.Inst` (both pruning
  modes) and every pool clause inside the support under the exact geometric assignment.

  | catalog | random sets | largest | CNFs | clauses evaluated | pool clauses | violations | states seen |
  |---|---|---|---|---|---|---|---|
  | N5 | 130 | 24 points | 390 | 8,814,145 | 94 | **0** | 77 of 84 |
  | N66 | 79 | 25 points | 237 | 6,683,229 | 129 | **0** | 69 of 70 |

  (HEURISTIC as evidence.)
- **Model verifier**: every SAT answer used anywhere (positive control, growth: accepted states, cross-
  validation) passed `verify_model`, which does not use the clause generator.
- **Pipeline on a known case** (phase-1 statement, 17:11; no output kept): a known 13-state core padded with 13
  random states is refuted, the LRAT trace returns exactly the 13 states, and the core equals the ETV5N core.
- **Trimmer**: positive and negative control of §2.4 (phase 1; outputs not kept). Phase 2: the L = 7 trimmed
  CNF is a subset of the full CNF, and the L = 8 trimmed CNF is a subset of the full L = 7 CNF plus the
  totalizer (§4.4, §4.5).
- **Totalizer**: brute-force self-test, 11,040 cases (§2.5; `monocert7.out`).
- **Rows against real sets** (phase 2, same runs as above): every row in the two row files is respected by the
  occupied sets of all the random real sets (0 row violations). The files are the 64 rows of the N5 level-19 run
  (`cegar_n5l19_rows.jsonl`) and the 35,538 rows added by the N66 loops (`cegar_n66_rows.jsonl`, including
  transported and mirrored rows). (HEURISTIC as evidence.)
- **Mirror symmetry** (`sym66.py`): cells, refined domains and the triple table transpose correctly; the 50
  base rows have valid mirrored cycle rows (phase-1 statement, output at 17:19 not kept).
- **State files after the forced stops** (§6): every line of the pool, row and log files parses, and the last
  lines are complete. Phase 2 confirmed this by reading them all (`report.py`, `posctl.py`, `soundness_lfr.py`).

## 6. Memory policy (rule 5 of `memguard-20261113/MEMORY_POLICY.txt`, in force from 18:25 KST)

The task text allowed MemoryMax 8 G per unit. From 18:25 a session guard enforced 4 GB for this track
(anonymous memory + swap over all its units). The phase-1 agent found the policy at 18:37 from the guard's log.
Stopped units (`MEMGUARD_STOPPED_*.txt` in W):

| time | unit | job | memory | change made |
|---|---|---|---|---|
| 18:31:26 | `nov13c-lfr-n66cegar2` | persistent CEGAR (`cegar2.py`: all 70 states with selectors in one solver, in-process master) | 4,350 MB | not restarted. Back to `cegar.py` (instance of the occupied set only, rebuilt per round), with the clause arrays freed after loading: peak 2.2 GB (systemd memory peak of `nov13c-lfr-f6`, 18:45–19:23) |
| 18:33:50 | `nov13c-lfr-monocert7` | cake_lpr on the 9.9 M clause monolithic CNF (after CaDiCaL had finished) | 4,306 MB | see next row |
| 18:36:42 | `nov13c-lfr-f1` | cake_lpr alone on the same pair (restarted before the phase-1 agent had found the policy; its error) | 4,116 MB | the proof is trimmed backwards with bounded memory (`lrat_trim2.py`, 0.6 GB) and cake_lpr checks the trimmed pair (1.0 GB) |

After 18:37 every unit was started with `MemorySwapMax=0` and a MemoryMax of at most 3,900 MB.
- *Peaks.* The systemd memory peaks of these units, which include page cache, were: f2 1.1 GB, f3 0.36 GB,
  f4 1.0 GB, f5 3.0 GB (the CaDiCaL probe), f6 2.2 GB and f7 3.4 GB (§4.5, MemoryMax 3,500 MB).
- *Correction.* The draft said "stayed below 2.5 GB". That is not true of these peaks for f5 and f7, although the
  guard's own measure (anonymous memory + swap) kept both units under their limits.
- *Guard.* The guard, which also stops units that swap, stopped none of them, and no unit of this track was killed
  by the kernel.
- *Probe.* The probe (`nov13c-lfr-f5`, 40 s) measured CaDiCaL at 3.13 GB RSS on the monolithic CNF, so the
  monolithic L = 8 certificate was not attempted; §4.5 did L = 8 with a 0.9 M clause CNF instead.
- *Phase 2.* The phase-2 checks peaked at 3.2 GB for 2 s (cake_lpr on the new L = 8 LRAT) and 1.0 GB for 0.5 s
  (cake_lpr on the L = 7 trimmed pair). All others stayed below 0.4 GB.

## 7. Recommendation (phase 2)

1. **The target has moved.** LO33N20261113 (phase 2) shows "N66 ≤ 57 ⇒ ES(8) ≤ 309" with the certified coupled
   rows. It also shows that N66 ≤ 58 suffices once slice 21 closes. The N66 work that matters is therefore:
   - certifying level 11 (N66 ≤ 58; COMPUTED in N66N20261113, certification running there);
   - deciding level 12 (N66 ≤ 57).

   Neither is in reach of this track's methods as measured. The row CEGAR grows by a factor of about 3 per level,
   so level 11 would take roughly 1–1.5 hours and level 12 roughly 3–4.5 hours of one thread (HEURISTIC
   extrapolation). The monolithic CNFs were still undecided when their deadlines ended: `mono` at level 9 after
   179 s, `lazyall` at level 10 after 555 s. Do not spend threads on this track's N66 loops tonight.
2. **Use the trim for certification under the memory policy.** Backward trimming (`lrat_trim2.py`, bounded memory)
   shrank a 713 MB LRAT for a 9.9 M clause CNF to 24 MB. cake_lpr then needed 1.0 GB instead of more than 4 GB.
   Any certification that is blocked by cake_lpr's heap (for example a monolithic N66 ≤ 58 proof) can be trimmed
   first; the soundness argument is the subset argument of §2.4.
3. **Seed with trimmed proofs.** The 37,853 clauses of the L = 7 trimmed proof made levels 5–9 UNSAT with no lazy
   clause at all (§4.5). Seeding the next level of any monolithic or lazy formulation with the trimmed clauses of
   the previous level is cheap and should be the default.
4. **The full-support refuter is a good refutation step, not a good row source for N5.** It never failed and
   needed at most 6 s on any frontier vector. For N5, though, its minimal cores (18–24 states) gave only 2–22
   transported rows each, against thousands for a 13-state core. For N66 the cores were 8–33 states, with a median
   of 10 (`cegar.py`) and 6 (`cegar2.py`) transported rows per core. Use it to kill vectors in a CEGAR, and take N5 rows from small-support
   probing.
5. **Housekeeping (needs the owner's permission or a task that allows it):**
   - run `W/assemble.sh`, which copies tools and small data into this record and writes `SHA256SUMS`;
   - archive the L = 7 trimmed pair and the L = 8 trimmed CNF;
   - optionally run the remaining final-chain items: `pbcert2.py` for level 10 is now redundant with N66N's
     certified N66 ≤ 59; the w18 transport; `satcert.py`; four greedy runs.

   The two big files `work_A4B4/mono_A4B4_L7.cnf` and `.lrat` (1.4 GB together) can then be deleted with the
   owner's approval.

## 8. Files and resumable state (all in W = `/home/jay/research/data/lfr-20261113`)

- **Certificates.**
  - L = 7 monolithic: `work_A4B4/mono_A4B4_L7.cnf` (676 MB, `1e14925350fc2669f481cd636fc900ceb869a14e8f676863fb36a4d948e23457`),
    `work_A4B4/mono_A4B4_L7.lrat` (713 MB, `c961fc897b2cbd2ed5ff2e23e92fa00ed4ceab15ab5dacb2a9ca73f6ef9ebad3`),
    trimmed pair `work_A4B4/mono_A4B4_L7_trim.cnf` (`b7931c07f2c61717362ce9aa65ebe84e31b5d43813a61ef8a78f6bd7fb4ba882`)
    and `work_A4B4/mono_A4B4_L7_trim.lrat` (`0d921fef4c488937ef4f41d7bfbab80b33e50e43300a575973dce12dda661402`),
    `work_A4B4/mono_A4B4_L7_kept.npy`, `monocert_A4B4_L7_trimstats.json`, `monocert7.out`, `trim7.out`,
    `trimcake7.out`.
  - L = 8 lazy monolithic: `lazyall_A4B4_L8_trim.cnf` (`542907739fbf268dcf49fae075293284fa32c0dcb89ee8e9cb6bf051ab3cb8b4`)
    and `lazyall_n66seed_log.jsonl`. Re-check: `cadical --lrat=true --binary=false lazyall_A4B4_L8_trim.cnf
    <out.lrat>`, then `cake_lpr lazyall_A4B4_L8_trim.cnf <out.lrat>` (8 s, 3.2 GB).
  - Core, template and full-support certificates: verdicts and SHA-256 in `refute_A3B6.jsonl`,
    `cegar_n5l19_log.jsonl`, `cegar_n66_log.jsonl` and `cegar2_n66_log.jsonl`. The CNF and LRAT files themselves
    were not kept; `work_A3B6/` is empty.
- **Rows and pools.** `cegar_n5l19_rows.jsonl` (64 rows), `cegar_n66_rows.jsonl` (35,538 rows), `pool_A3B6.jsonl`
  (85,260 poly clauses), `pool_A4B4.jsonl` (191,828).
- **Logs and data.** `cegar*_log.jsonl` / `.out`, `mono_n66pure_log.jsonl`, `lazyall_n66seed.out`,
  `refute_A3B6.jsonl`, `w18.out`, `grow_*.json` / `.out`, `posctl_A3B6.json`, `posctl_A4B4.json`, `memprobe.err`,
  `MEMGUARD_STOPPED_*.txt`, `witness18_final_rows.json`, `cyc_base_A4B4.json`. The phase-1 drafts
  `README_sec12.md` and `README_sec4to8.md` were merged into this record.
- **Resumable.**
  - The N66 CEGAR at level 11 reloads its rows and pool. The command that ran last, with `ETV_A=4 ETV_B=4`, was
    `$PY -u cegar.py n66 cyc_base_A4B4.json 11 <deadline> 15 600 2`.
  - `lazyall.py` from level 10 is not resumable as it ran: it saved no state, and the file was edited after its
    start.
  - `final_chain.sh <level>` and `assemble.sh` are ready but were never run.
