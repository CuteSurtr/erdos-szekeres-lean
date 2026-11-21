# ETV7SAT20261113: SAT attack on the Erdős–Tuza–Valtr case (7; 5, 7) (13 November 2026)

Track E of the 13 November afternoon session, 16:53–21:00 KST. Work directory
`/home/jay/research/data/etv7sat-20261113/` (abbreviated W; not in Git). Tools are copied to `tools/`,
small data to `data/`. Nothing is committed. All jobs ran in `nov13c-e7-*` user units, at most 3 threads
(a fourth short job always ran with one of the three paused by SIGSTOP).

Labels: **PROVED** = written argument; **CERTIFIED** = an LRAT proof accepted by cake_lpr
(`s VERIFIED UNSAT`) for the stated CNF, hashes recorded; **COMPUTED** = solver verdict only;
**HEURISTIC** = statistics. "CERTIFIED" always means: the stated CNF is unsatisfiable. The step from
the CNF to the geometric statement is the written soundness argument of §2 plus the positive
controls of §5; it is not machine-checked.

> **Note (13 November, phase 2).** Phase-1 agent cut off at about 19:40 KST; completed from the work
> directory by a phase-2 agent at 20:48 KST. The runs still going at 19:40 (the two cases of rung N = 36,
> the colouring search at 28 and 30 vertices) ended by themselves by 20:10. The phase-2 agent rewrote this
> status block from their logs, filled §6.2 (rung N = 36), and added §9.1 (literature) and §13 (what was
> checked in phase 2). Everything else is the phase-1 text. The phase-2 agent could edit only this README, so
> the logs written after 19:33 are quoted here and stay in W (they are not in `data/`).

**STATUS (final).**

M(5; 7) = largest set (general position, distinct x) with no 5-cap and no convex heptagon.
ETV conjecture: 26. Before this record: M(5; 7) ≤ 41.

1. **The target ETV(7; 5, 7) = 26 is NOT decided.** Neither a proof nor a counterexample candidate
   (signotope or point set) was found at 27 points. Measured scaling (§6.3) puts a proof by the
   present method far outside this time box.
2. **M(5; 7) ≤ 36** (was 41). The owner-model CNFs "exactly N points" are **CERTIFIED** unsatisfiable
   for N = 41 (two different clause sets), 40, 38 and 37 (§6.2). The geometric statement follows by
   the written arguments of §2 (PROVED there, not machine-checked) and uses two lemmas that are
   themselves certified here (§5.1). The N = 38 and N = 37 certificates use no four-point axiom, so the
   bound 36 also holds for 2-colourings of triples (no 5-cap path, no weak heptagon).
   **36 is the final bound of this record; M(5; 7) ≤ 35 is NOT established.** Rung N = 36 was split into
   two cases (§6.2). Case B (at most 22 points end no 6-cup) is UNSAT by CaDiCaL (COMPUTED only): its LRAT
   proof (5.23 GB) is still in W, but cake_lpr ran out of its 2,600 MB heap at 19:53 and the check was not
   repeated. Case A (at most 13 points end a 6-cup) reached its 4,150 s time limit with no verdict.
   *Update 21 Nov 2026:* case B is now **CERTIFIED**. cake_lpr accepted the same 13 Nov proof at a 6,000 MB heap
   (§6.2). Case A is still open, so the bound stays at 36.
3. **Schroeder's M₇(5, 6) ≤ 25 re-proved by one CNF** (CERTIFIED, 59 s + 9 s check), and
   **strengthened to the colouring model** (CERTIFIED, 76 s + 56 s): every 2-colouring of the triples
   of 26 ordered vertices contains a 5-vertex cap path, a 6-vertex cup path or a weak heptagon
   (4-cap path and 5-cup path on common end-vertices). No four-point (signotope) axiom is used.
4. **The colouring version of ETV(7; 5, 7) is false**: an explicit 2-colouring of the triples of 27
   ordered vertices with no 5-vertex cap path, no 7-vertex cup path and no weak heptagon
   (`data/colouring27_nosig.json`; checked by two independent programs, §7). It violates 383 of the
   17,550 four-point packets, so it is not a signotope and says nothing about point sets. It shows that
   26 cannot be proved for (7; 5, 7) without four-point axioms — unlike (7; 5, 6) and Baek's a = 4.
   The largest such colouring has between 27 and 36 vertices. The search for colourings with 28 and 30
   vertices gave no verdict in 1,150 s each (§11).
5. **Conditional consequence** (§7.1): with M(5; 7) ≤ 36, weak Conj(8) of ETVTHY20261113 alone gives
   N5 ≤ 58 and hence, by RES33N20261113, ES(8) ≤ 309. Nothing unconditional about ES(8) follows.
6. **Method**: a state-indexed "owner model" CNF (§2). The position-indexed signotope encoder proposed
   for this track does not reach n = 26: no verdict in 16 minutes on the instance that the owner model
   refutes in one minute (§4).
7. **Memory**: two units of this track were stopped by the session memory guard at 18:24 and 18:33
   (cake_lpr's default 4 GB heap); no result was lost; details and the changes made are in §12. The failed
   check of the N = 36 case-B proof was not a guard stop: CakeML reported heap exhaustion.
8. **Literature** (§9.1, from NOVELTY20261113B): the old bound 41 is one substitution into a printed lemma
   (Javůrek, Lemma 3). No public upper bound on M(5; 7) below 41 was found. Three public efforts leave the
   27-point case open. M₇(5, 6) = 25 already has two independent computer proofs: Schroeder's, and
   gotrevor's SAT run without a proof log. The colouring statements of items 3–4 have not been compared
   with Balko–Valtr's colourings.

## 1. Question

M(5; 7) is the largest size of a planar point set in general position with distinct x-coordinates,
with no 5-cap and no convex heptagon. ETV conjecture: 26 (attained: `data/pts/etv757.json`).
Known before this record: M(5; 7) ≤ 41 (ETVTHY20261113 §2.4: Baek's 16 plus Schroeder's 25).
Baek–Balko (SoCG 2025, §2.1) record the known ETV cases as k ≥ a + u − 3, a = 4 or u = 4; Schroeder's
v1 adds (7; 5, 6). The case (7; 5, 7) is outside all of these (literature check in §9).

## 2. The owner model (new encoder `owner.py`) and its soundness

### 2.1 Setting

S is a finite planar point set, in general position, with distinct x-coordinates, indexed by increasing
x. Cup / cap triples have positive / negative determinant. Parameters: CA, CB, G, N. Assume every cap
of S has at most CA + 1 points, every cup at most CB + 1 points, and S has no convex G-gon.
(Target: CA = 3, CB = 5, G = 7; a 7-cup is a convex heptagon. Schroeder's case: CA = 3, CB = 4, G = 7.)

- **Labels.** For u < v, d(u,v) = (E₋(u,v) − 1, E₊(u,v) − 1) ∈ [1..CA] × [1..CB], where E₋ / E₊ is the
  number of points of a longest cap / cup ending with the pair (u,v).
- **Growth.** For u < v < w: if (u,v,w) is a cap then d₁(v,w) ≥ d₁(u,v) + 1; if a cup then
  d₂(v,w) ≥ d₂(u,v) + 1 (extend an attaining chain).
- **States.** I(v) = the down-set of [1..CA] × [1..CB] generated by {d(u,v) : u < v}; it is given by
  column heights f₁ ≥ … ≥ f_CA (column a = cap coordinate a). There are C(CA+CB, CA) states
  (56 for the target, 35 for Schroeder's case).
- **State separation** (ETV5N20261113 §2; Schroeder Lemma 5.1): d(u,v) ∈ I(v) ∖ I(u). So v ↦ I(v) is
  injective: every state has at most one **owner**.
- **Lemma R** (ETV5N20261113 §2): d₂(u,v) ≤ cupH(u) + 1 and d₁(u,v) ≤ capH(u) + 1, with cupH = f₁ and
  capH = number of nonempty columns of I(u). Hence d(u,v) ∈ D′(I(u)→I(v)), where
  D′(s→t) = {(a,b) ∈ t ∖ s : a ≤ capH(s) + 1, b ≤ cupH(s) + 1}.
- **Exact predecessor.** If d₂(x,y) = b ≥ 2, an attaining cup has a predecessor t of x; its prefix
  gives E₊(t,x) ≥ b, and Growth on the cup (t,x,y) gives E₊(t,x) ≤ b. So d₂(t,x) = d₂(x,y) − 1.
  The cap statement is symmetric.
- **Corners.** Every maximal cell of I(v) is an actual label d(u,v) (a down-set is generated by its
  maximal cells, and I(v) is generated by actual labels).

**Colouring model.** All of the above uses only the signs of triples and "paths": sequences whose
consecutive triples have one sign. So it holds verbatim for an arbitrary 2-colouring of the triples of
an ordered set, with "k-cap" / "k-cup" read as monotone paths on k vertices (Baek–Balko's P³ₖ) and
"convex G-gon" read as a **weak G-gon**: a cap path and a cup path with common end-vertices and
a + b = G + 2 vertices. Only family S below needs more (signotopes or point sets).

### 2.2 Variables and clauses

The CNF has one block of variables **per state**, not per point. Semantic values (for a given S) are in
brackets; owner(s) is the point with state s.

| variable | semantic value |
|---|---|
| occ[s] | state s has an owner |
| P[s,t] (only if D′(s→t) ≠ ∅) | s and t are occupied and owner(s) is left of owner(t) |
| Lab[s,t,z], z ∈ D′(s→t) | P[s,t] and d(owner(s), owner(t)) = z |
| cupge[s,t,k], capge[s,t,k] | P[s,t] and the cup / cap coordinate of that label is ≥ k (constants folded) |
| ori[s,t,r], s<t<r as state indices | all three occupied and det(p_s, p_t, p_r) > 0 in index order |
| Wu[t,x,y], Wc[t,x,y] | P[t,x], P[x,y], (t,x,y) is a cup / cap triple and d(t,x) + 1 = d(x,y) in that coordinate |
| SU[b][s,j,k], SC[a][s,j,k] | P[s,j], P[j,k] and a b-cup / a-cap starts at owner(s) and ends with the pair (owner(j), owner(k)) |
| U[b][s,t], K[a][s,t] | P[s,t] and a b-cup / a-cap runs from owner(s) to owner(t) |
| cnt[i][j], rc[row][i][j] | counters: at least j holes (resp. occupied states of the row) among the first i |

A triple (x,y,z) of states in chronological order has orientation literal ori or ¬ori according to
the parity of the permutation that sorts it. A triple or 4-tuple of states is *feasible* if D′ is
nonempty for all its pairs in chronological direction (52,304 ordered triples and 1,145,667 ordered
4-tuples for the target).

Clause families (names as in the generator's statistics) and why the semantic assignment satisfies them:

| family | clauses | reason |
|---|---|---|
| P1 | P[s,t] → occ[s], occ[t] | definition |
| P2 | ¬P[s,t] ∨ ¬P[t,s] | x-order is strict |
| P3 | occ[s] ∧ occ[t] → P[s,t] ∨ P[t,s] (a missing P is the constant false) | owners are distinct points; the actual label lies in D′ of the actual direction |
| P4 | P[x,y] ∧ P[y,z] → P[x,z] | transitivity; if D′(x→z) = ∅ the conclusion is false, and that order is indeed impossible |
| L1–L3 | Lab → P; P → some Lab; at most one Lab | the label exists, is unique and lies in D′ (state separation, Lemma R) |
| T0–T2 | threshold variables agree with Lab | definition |
| Gcup, Gcap | cupge[x,y,k] ∧ P[y,z] ∧ cup(x,y,z) → cupge[y,z,k+1], k = 1..CB (k = CB: conclusion false); caps likewise | Growth and the ceilings (no (CB+2)-cup, no (CA+2)-cap) |
| A | occ[t] → ∨ₛ Lab[s,t,z] for every maximal cell z of t | Corners |
| W1–W3 | cupge[x,y,2] → ∨ₜ Wu[t,x,y]; Wu → P[t,x], P[x,y], cup(t,x,y); Wu ∧ cupge[x,y,k] → cupge[t,x,k−1]; caps likewise | Exact predecessor (Wu is true for every such t) |
| **S** | for a feasible chronological 4-tuple with P[x,y], P[y,z], P[z,w]: the signs of (xyz, xyw, xzw, yzw) change at most once | signotope packets of real points (ETV5N20261113 §2, family 4). **The only family that is not valid for arbitrary colourings.** |
| C1–C3 | SU[3] from a cup triple; SU[b−1][s,i,j] ∧ P[j,k] ∧ cup(i,j,k) → SU[b][s,j,k]; SU[b][s,j,t] → U[b][s,t]; caps likewise | a chain whose consecutive triples are cups is a cup (for colourings: a cup path, by definition) |
| C4 | ¬K[a][s,t] ∨ ¬U[b][s,t] for a + b = G + 2 | an a-cap and a b-cup on common endpoints are a + b − 2 = G points in convex position (colourings: a weak G-gon) |
| F | occ[∅], occ[(1,0,…,0)] | the first two points (N ≥ 2) |
| K | at most (number of states − N) holes, sequential counter | at least N points and injectivity; the counter variables are one-sided |

For G = 7 the polygon types are (a, b) = (3, 6) and (4, 5) (target), or (4, 5) only (CB = 4).

Generator options (each gives a CNF that the same semantic assignment satisfies):
- `--nosig`: family S omitted. The CNF is then sound for the **colouring model**.
- `--sigmax K`: family S only for 4-sets of states with at most K feasible chronological orders
  (K = 1: the 77,560 4-sets whose order is forced). A sub-family of S.
- `--link`: a chain variable SU[b][s,j,k] exists only if some label in D′(j→k) has cup coordinate
  ≥ b − 1, and implies that threshold (family CL: a b-cup ending with (j,k) gives E₊(j,k) ≥ b);
  clauses whose conclusion is a missing chain variable are dropped (they follow from CL and Gcup). Caps
  likewise. Valid for colourings too.

**Conclusion (PROVED, given the arguments above).** If S satisfies the hypotheses and has at least N
points, the semantic assignment satisfies every clause. Hence: *if the CNF is unsatisfiable, every such
S has at most N − 1 points.* Without family S the same holds for every 2-colouring of the triples of
an ordered N-set with no (CA+2)-cap path, no (CB+2)-cup path and no weak G-gon.

The design follows Schroeder's Appendix B (occupation, owner order, pair labels, corner attainment,
predecessor witnesses, four-point signs, common-endpoint paths) and the project's coupled owner CNF
(ETV5N20261113 §2). New here: all states at once, with occupancy variables and the cardinality counter
in **one CNF**, so that one solver run and one LRAT proof replace the hole-clause and coverage layers.

### 2.3 Lemma rows (`addrows.py`)

For a family F of states, "at most K states of F are occupied" may be added when the owners of F form
a set with a known extremal bound. For the target (CA = 3, CB = 5, G = 7):

| row | family | owners | why bounded |
|---|---|---|---|
| S1 ≤ 25 | f₁ ≤ 4 | points where no 6-cup ends | contain no 6-cup (it would end at one of them); (5,6) theorem |
| S2 ≤ 25 | f₃ ≥ 1 | points where a 4-cap ends | if a 4-cap a b c p ends at p, then (c,p,q) is a cup for every q > p (else a 5-cap); so a 6-cup starting at p would give the 7-cup c + cup. No 6-cup; (5,6) theorem |
| B1 ≤ 16 | f₃ = 0 | points where no 4-cap ends | contain no 4-cap; Baek, n = 7 |
| B2 ≤ 16 | f₁ = 5 | points where a 6-cup ends | a 4-cap starting at such a point gives a 7-cup or a 5-cap; no 4-cap; Baek, n = 7 |
| ALL ≤ N | all states | — | "exactly N": any N-subset of a valid set is valid, so it suffices to refute sets of exactly N points |

The owners of a family are a subset of S, so they inherit "no 5-cap, no heptagon"; the arguments in
the table are path arguments and hold for colourings. Both external theorems are certified here, in
the geometric and in the colouring form (§5.1). No other "coordinate-constant" family gives a
non-trivial row (checked by hand: every other one has at most as many states as its bound).
Cycle rows (lists of states whose triples are all forced convex: at most 6 occupied; own
implementation `cyc7.py`) do not lower the count: with the four block rows the exact minimum is still
15 holes, capacity 41 (CP-SAT OPTIMAL, 52 rows, no violated 7-list left: COMPUTED).

### 2.4 The position-indexed encoder (`etv7.py`, from `etv_sat2.py`)

Variables O(i,j,k) for the n points in x-order, signotope axioms on all 4-tuples, chains anchored at
their first point, the same polygon clauses. Without extras its clause set equals that of
`etv_sat2.py` (checked on the hexagon instance n = 16). Soundness for heptagons: a real 5-cap-free
heptagon-free set has no 7-cup (a 7-cup is a convex heptagon) and no (3,6)- or (4,5)-gon; the
remaining types (5,4), (6,3), (7,2) contain a 5-cap. The mirror clause O(0,1,2) → O(n−3,n−2,n−1) is
sound because x ↦ −x maps caps to caps, cups to cups and convex position to convex position, and
exchanges the first and last consecutive triples: of a set and its mirror image, at least one
satisfies the clause. This encoder is used here only for calibration, for the Baek lemma and for the
cross-check of §7.

## 3. Method

1. **Calibration of the position-indexed encoder** (§4): too slow at n = 26, 27; extra points do not
   help it; hull cubes do not help it.
2. **Owner model** (§2): the unknowns are attached to the 56 (or 35) *named* states. A learned clause
   then speaks about states and is valid for every placement of their owners; the position-indexed
   encoder has to rediscover the same fact for every placement.
3. **Certificates**: CaDiCaL 2.1.3 `--lrat --no-binary`, then cake_lpr; CNF and LRAT SHA-256 recorded
   (`solve_lrat2.sh`); LRAT files are deleted after the verdict.
4. **Lemma rows** (§2.3) and the exact-cardinality row.
5. **Ladder** (`ladder_g.sh`): the same CNF with "exactly N occupied" for N = 41, 40, …; each UNSAT
   certificate gives M(5; 7) ≤ N − 1.
6. **Model analysis**: when the signotope-free model turned out satisfiable at N = 27, the solution was
   decoded and checked independently (§7), and its occupancy pattern was refuted in the full model
   (one conflict). The trace of that refutation used only signotope clauses on inclusion chains of
   states, which led to the `--sigmax 1` variant.

## 4. Calibration and measurements

All times are single-thread seconds on this machine. "pos" = position-indexed signotope encoder,
"owner" = `owner.py`.

### 4.1 Position-indexed encoder

| instance | result |
|---|---|
| hexagon (6; 5, 6), n = 16, original `etv_sat2.py` | UNSAT, 45.6 s (COMPUTED) |
| hexagon (6; 5, 6), n = 15 | SAT (0.01 s) |
| the same, n = 16, with the mirror clause / plus backward chains / plus unanchored labels | UNSAT in 40.0 / 54.7 / 51.7 s (COMPUTED): no useful gain |
| the same with mirror clause, n = 17, 18, 19, 20, 22, 24 | UNSAT in 48.7, 59.6, 73.9, 78.0, 98.8, 146.7 s (COMPUTED): **more points do not make it easier** |
| the same, n = 16, upper-hull cubes (`cubes.py`, 57 cubes up to mirror) | the first cube alone (hull = the edge 0–15) took 43.9 s: **no gain from hull cubes** |
| the same, n = 16, signotope axioms removed | no verdict in 50 s |
| Baek (7; 4, 7), n = 17 | UNSAT, 0.57 s; without signotope axioms 0.41 s; both **CERTIFIED** (§5.1) |
| cup–cap (5, 5), n = 21 | UNSAT, 4.9 s (COMPUTED) |
| (7; 5, 6), n = 26, plain | no verdict in 600 s (3.0 M conflicts) |
| (7; 5, 6), n = 26, mirror clause, LRAT | no verdict in 960 s (3.8 M conflicts); stopped, partial proof deleted |
| (7; 5, 7), n = 27, plain | no verdict in 600 s (2.9 M conflicts) |

### 4.2 Owner model, 35-state catalog

| instance (CA, CB, G, N) | clauses | result |
|---|---|---|
| hexagon (3, 4, 6, 15) | 1.78 M | SAT in 0.8 s |
| hexagon (3, 4, 6, 16) | 1.78 M | no verdict in 55 s (default) and in 50 s (occupancy-first decisions): for hexagons the owner model is not better than the position-indexed encoder |
| **(3, 4, 7, 26)** = Schroeder's case | 1.75 M | **UNSAT in 63 s** (CaDiCaL 2.1.3, 291 k conflicts); 57 s with occupancy-first decisions (CaDiCaL 3.0.1 library, `occfirst.cpp`); 66 s without family W; 59 s with `--link`; **CERTIFIED** (§5.1) |
| (3, 4, 7, 26) `--nosig` | 0.61 M | **UNSAT in 76–84 s** (683 k conflicts); **CERTIFIED** (§5.1); 85 s with `--link` |
| (3, 4, 7, N), N = 34, 32, 30, 28, 27 | 1.75 M | UNSAT with 13; 104; 2,276; 31,431; 76,901 conflicts (0.5, 0.7, 1.6, 15.6, 30.0 s; COMPUTED). With N = 26: 291,485. **About ×3.5 per additional hole.** |
| (3, 4, 7, 25) | 1.75 M | positive control (§5.2) |

Occupancy-level CEGAR prototype (`cegar.py`, discovery only) on the hexagon instance: 44,772 candidate
patterns refuted in 50 s without closing; cores of about 20 literals. Random 16-subsets of states:
248 of 300 refuted by unit propagation alone (`rup_probe.py`).

## 5. Certificates and controls

### 5.1 CERTIFIED lemmas (CaDiCaL 2.1.3 → cake_lpr `s VERIFIED UNSAT`)

| statement | CNF | SHA-256 CNF / LRAT | times |
|---|---|---|---|
| **(5,6), geometric**: owner model (3, 4, 7, 26) is UNSAT. With §2: every set with no 5-cap, no 6-cup, no convex heptagon has ≤ 25 points (Schroeder's Theorem 5.2) | `owner_v1.py 3 4 7 26`: 89,318 variables, 1,754,143 clauses | `9646633ed38cbcc8740ae4aff903b832b8ab478e50cc2bc4f04523bae988167f` / `642b46600f29c87019f8d054623c94cc09afa52ce643b51265637f7a569bdef6` (321,528,931 bytes) | solve 59 s, check 9 s |
| **(5,6), colouring model**: owner model (3, 4, 7, 26) `--nosig` is UNSAT. With §2: every 2-colouring of the triples of 26 ordered vertices has a 5-cap path, a 6-cup path or a weak heptagon of type (4,5) | `owner_v1.py 3 4 7 26 --nosig`: 89,318 variables, 611,615 clauses | `df8ace7fb72d572191dd45b31a38018dc99898d0b7eac49acb52b07c63ab828c` / `7d40c2098956e10c4652764ab89c13353f5c7db5c8c01d2774971d743d97b0f0` (343,841,949 bytes) | solve 76 s, check 56 s |
| **Baek n = 7, geometric / signotope**: `etv_sat2.py`, n = 17, no 4-cap, no 7-cup, no (3,6)-gon: UNSAT | 4,760 variables, 35,836 clauses | `d76bf0e31451d46aa43490ae38cc45e5ed3aaaf950f4fb6005d876cce104ead5` / `3a2a1aba827a0832b4a1131395aaff6a3d63146477b10d94fc5b4b3b01a07c7b` (5,521,597 bytes) | 0.6 s |
| **Baek n = 7, colouring model**: the same CNF without its 19,040 signotope clauses: UNSAT | 4,760 variables, 16,796 clauses | `09136d731b9b08a991ef2fef3fd6e68c54239b8f1055ac6ef19da0132d1659a3` / `54638b1c81df01c552f9c5d46663a1a3f278c2621028ab150a73c25a5e88e6d6` (5,086,187 bytes) | 0.4 s |

Files: `data/*.cake`. Baek's theorem is published and is proved by him in the configuration model; the
two SAT certificates are a convenience, so that the rows B1, B2 rest on certified statements in both
models.

### 5.2 Positive controls on real point sets (exact integer arithmetic)

`owner_check.py` computes the semantic assignment of §2.2 from the coordinates (orientations, labels,
states, owners, chains; its own code, by variable name) and evaluates **every clause** of the CNF.

| CNF | point sets | clauses per set | violations |
|---|---|---|---|
| owner (3, 5, 7, 26) | ETV 26-point set `etv757.json` and its mirror image | 14,729,762 | 0 |
| owner (3, 5, 7, 26) + rows S1, S2, B1, B2 | the same two | 14,732,874 | 0 |
| owner (3, 5, 7, 26) + rows + ALL ≤ 26 | the same two | 14,735,140 | 0 |
| owner (3, 5, 7, 26) `--sigmax 1 --link` + rows + ALL ≤ 26 | the same two | 3,945,651 | 0 |
| owner (3, 5, 7, 2) `--sigmax 1 --link` + rows | 4 random sets (17–20 points) | 3,944,033 | 0 |
| owner (3, 4, 7, 25), also `--link` | ETV 25-point set `etv756.json` (no 5-cap, no 6-cup, no heptagon) | 1,754,193 / 1,552,705 | 0 |
| owner (3, 4, 6, 15) | ETV 15-point set `etv656.json` and its mirror image | 1,778,196 | 0 |
| owner (3, 4, 6, 2) | 24 random hexagon-free sets, caps ≤ 4, cups ≤ 5, 12–14 points, + `etv656.json` | 1.78 M | 0 |
| owner (3, 4, 7, 2) | 24 random heptagon-free sets, caps ≤ 4, cups ≤ 5, 14–19 points | 1.75 M | 0 |
| owner (3, 5, 7, 2) + rows | 16 random heptagon-free sets, caps ≤ 4, cups ≤ 6, 16–20 points, + `etv757.json`, `etv756.json`, `etv747.json` | 14.73 M | 0 |

The random sets (`randsets.py`; uniform, perturbed parabola, perturbed arc, clusters) are grown by
random insertion and re-validated by an independent brute-force convex-position test (`geom.py`:
Carathéodory on 4-subsets, no cap/cup logic). The ETV sets are built by `etvthy-20261113/etvcon.py`
and re-checked the same way (26 points: caps 4, cups 6, no convex heptagon). A `--nosig` CNF is a
sub-CNF of the corresponding full CNF with the same variable numbering, so these controls cover it.
The final `owner.py` without options produces the same named clause set as `owner_v1.py` (checked on
(3, 4, 7, 26): 1,749,352 distinct clauses in both).

### 5.3 Positive controls on abstract colourings that are not signotopes

`colcontrol.py`: colourings sampled with the original position-indexed encoder minus its signotope
clauses, re-checked by the independent path checker of `decode_check.py`; then every clause of the
`--nosig` owner CNF is evaluated under the semantic assignment computed from the colouring alone.

| CNF | colourings | violations |
|---|---|---|
| owner (3, 4, 7, 2) `--nosig` (612,263 clauses) | 21 colourings, n = 14–25 (three with 25 vertices), 10–540 violated signotope packets each | 0 |
| owner (3, 5, 7, 2) `--nosig` | 8 colourings, n = 16–26, 15–514 violated packets each | 0 |
| target variant v2 (`--nosig`, rows, exactly 27; 5,569,810 clauses) | the 27-vertex colouring of §7 (round trip: decoded, then re-encoded semantically) | 0 |

Logs: `data/ctl/`.

### 5.4 Reproducibility and known-answer checks of the generator

`repro.sh` regenerates certified CNFs from the generators and compares SHA-256 with the recorded
hashes; `extra_checks.sh` runs the owner model on other catalogs with known answers (COMPUTED).

```
(5,6) geometric: owner_v1.py 3 4 7 26 REPRODUCED 9646633ed38cbcc8740ae4aff903b832b8ab478e50cc2bc4f04523bae988167f
(5,6) colouring: owner_v1.py 3 4 7 26 --nosig REPRODUCED df8ace7fb72d572191dd45b31a38018dc99898d0b7eac49acb52b07c63ab828c
Baek n=7: etv_sat2.py 17 3 6 out 7 REPRODUCED d76bf0e31451d46aa43490ae38cc45e5ed3aaaf950f4fb6005d876cce104ead5
ladder N=38 [--nosig]: owner.py + addrows.py REPRODUCED d35b0c4f8ad8fe6c06c1c66ece6b9fc8b3d53e006b05c10af3ba0a80a24ca339
ladder N=40 [--sigmax 1 --link]: owner.py + addrows.py REPRODUCED d6fc98d836b0e4b103cdd49a19534fb44cfc0bfe95a37a6fb4890a2149cc200a
ladder N=41 [--sigmax 1 --link]: owner.py + addrows.py REPRODUCED 047fd3565378a9027a17c272eaff600a562c719bc7fa90dec118f1deda9399de
ladder N=41 [--nosig]: owner_v1.py + addrows.py REPRODUCED dafcc24c9f20326a01b3e28abce521c13a1df57fc25c3df370f5e28d1c265c58
owner(2,5,7,N=17): s UNSATISFIABLE (expected UNSAT) -- Baek n = 7: 17 points with no 4-cap contain a convex heptagon
owner(2,5,7,N=16): s SATISFIABLE (expected SAT) -- ETV 16-point set
{"points": "pts/etv747.json", "mirror": false, "n": 16, "occupied": 16, "cnf": "repro/x.cnf", "clauses": 170495, "violated": 0}
owner(2,4,6,N=12): s UNSATISFIABLE (expected UNSAT) -- Baek n = 6: 12 points with no 4-cap contain a convex hexagon
owner(2,4,6,N=11): s SATISFIABLE (expected SAT) -- ETV value 11
owner(3,3,6,N=15): s UNSATISFIABLE (expected UNSAT) -- ETV(6;5,5) = 14 (follows from ES(6) = 17 by the ETV extension)
owner(3,3,6,N=14): s SATISFIABLE (expected SAT) -- ETV value 14
owner(3,3,7,N=21): generator refused (N exceeds the number of states: trivially impossible) -- cup-cap: no 5-cap, no 5-cup: 20 states only
owner(3,3,7,N=20): s SATISFIABLE (expected SAT) -- cup-cap extremal set, all 20 states occupied
owner(2,6,8,N=23): s UNSATISFIABLE (expected UNSAT) -- Baek n = 8: 23 points with no 4-cap contain a convex octagon
owner(2,6,8,N=22): s SATISFIABLE (expected SAT) -- ETV value 22
```

## 6. Results for the target catalog (CA = 3, CB = 5, G = 7; 56 states)

### 6.1 Runs at N = 27 (the ETV case itself): no verdict

Target CNF: owner model (3, 5, 7, 27): 455,198 variables, 14,729,710 clauses (9.17 M of them signotope
packets, 4.58 M chain clauses). Variants: `v0` = plain; `v1` = + rows S1, S2, B1, B2; `v2` = `--nosig`,
rows, exactly 27 (5.57 M clauses); `v3` = full, rows, exactly 27 (14.74 M); `v4` = `--sigmax 1`, rows,
exactly 27 (6.19 M); `v6` = v4 with `--link` (3.95 M). All with LRAT output.

| time (KST) | run | outcome |
|---|---|---|
| 17:26–17:29 | v0, CaDiCaL 2.1.3 | stopped after 87 s (replaced by v1) |
| 17:27–17:37 | v1, CaDiCaL 2.1.3 | stopped after 581 s, 270 k conflicts, no verdict |
| 17:27–17:36 | v1, occupancy-first decisions (CaDiCaL 3.0.1) | stopped after 9 min, no verdict |
| 17:33–17:43 | **v2 (no signotope packets)** | **SATISFIABLE** after 599 s, 525 k conflicts: the colouring of §7 |
| 17:36–17:45, 17:50–18:06 | v3 (full model) | stopped twice (307 s; 927 s, 423 k conflicts), no verdict; about 450 conflicts/s |
| 17:55–18:15 | v4 | stopped after 1,174 s, 1.54 M conflicts, no verdict |
| 18:06–18:09 | v6 | stopped after 220 s, 97 k conflicts (thread given to the ladder) |

So at 27 points: **no proof, and no satisfying assignment of any model that contains signotope
packets**. Partial LRAT files of unfinished runs were deleted.

The v2 solution (which 27 states are occupied) is refuted by the full model with **one conflict**
(2.6 s). The refutation uses 241 original clauses, among them only 8 signotope clauses, all on 4-sets
of states that form an inclusion chain (forced chronological order). This is what `--sigmax 1` keeps.

### 6.2 Ladder: exactly N points, rows S1, S2, B1, B2

Each line is one CNF: owner model (3, 5, 7, N) with the stated generator flags, rows S1 ≤ 25, S2 ≤ 25,
B1 ≤ 16, B2 ≤ 16, ALL ≤ N. A CERTIFIED line proves (with §2 and §5.1) **M(5; 7) ≤ N − 1**; a
`--nosig` line proves the same bound for the colouring model.

| N | generator flags | variables / clauses | CaDiCaL 2.1.3 | conflicts | LRAT bytes | cake_lpr | status | SHA-256 CNF / LRAT |
|---|---|---|---|---|---|---|---|---|
| 41 | `--nosig` | 457,773 / 5,569,474 | UNSAT, 227 s | 293,228 | 796,941,967 | `s VERIFIED UNSAT`, 108 s | **CERTIFIED**: M(5; 7) ≤ 40 | `dafcc24c9f20326a01b3e28abce521c13a1df57fc25c3df370f5e28d1c265c58` / `a2aaa95d7b9496e97702815da1d75c0faa60414486231140776dc0b164f106c0` |
| 41 | `--sigmax 1 --link` | 353,529 / 3,945,321 | UNSAT, 461 s | 275,838 | 505,929,663 | `s VERIFIED UNSAT`, 58 s | **CERTIFIED**: M(5; 7) ≤ 40 | `047fd3565378a9027a17c272eaff600a562c719bc7fa90dec118f1deda9399de` / `b772b5f18547b184a53dbe6866b3979af033e4f05f450a107e854a07c3f9bc76` |
| 40 | `--sigmax 1 --link` | 353,554 / 3,945,371 | UNSAT, 686 s | 573,706 | 621,019,339 | `s VERIFIED UNSAT`, 20 s | **CERTIFIED**: M(5; 7) ≤ 39 | `d6fc98d836b0e4b103cdd49a19534fb44cfc0bfe95a37a6fb4890a2149cc200a` / `2f19525f18a36ba8b317ba7536fb10574b6326920286ff158f93839db98f3b5d` |
| 38 | `--nosig` | 457,842 / 5,569,612 | no verdict in 1500 s | 2,677,463 | — | — | no verdict | `f5fb9c7cb19439114020fb310702a2c48c3670e2fc724e3335ff319c3aadccf8` |
| 38 | `--nosig` | 457,842 / 5,569,612 | UNSAT, 1280 s | 3,086,289 | 2,228,107,748 | `s VERIFIED UNSAT`, 79 s | **CERTIFIED**: M(5; 7) ≤ 37 | `d35b0c4f8ad8fe6c06c1c66ece6b9fc8b3d53e006b05c10af3ba0a80a24ca339` / `a9327691747f587392d13fa95808fc6f67552fd49448b63f30c35ce05f2d2e70` |
| 37 | `--nosig` | 457,861 / 5,569,650 | UNSAT, 4144 s | 8,848,423 | 5,261,034,548 | `s VERIFIED UNSAT`, 148 s | **CERTIFIED**: M(5; 7) ≤ 36 | `8762b9f0f23456cca9f8fddeb3731100170e999128b1a5790f7e0730523996d5` / `d3205363dd75a3c6e101e3f61967d497b734e76be4061292641af56e2cb3f373` |

Generator versions: the `--nosig` line for N = 41 and the unfinished `--nosig` line for N = 38 (SHA
`f5fb…`) were generated by `owner_v1.py`, all other lines by the final `owner.py`. The two generators
give the same named clause set but number the chain variables differently, hence two hashes for
N = 38 `--nosig`. LRAT files were deleted after verification; the hashes are in `data/*.cake`.

Positive controls for exactly these flag combinations: §5.2 (`--sigmax 1 --link`; `--nosig` is a sub-CNF
of the controlled full CNF) and §5.3.

**Rung N = 36 as two cases** (`cube_n.sh`; coverage checked by `cube_cover.py`). With exactly 36
occupied states, let r be the number of occupied states with f₁ = 5 and t the number with f₁ ≤ 4;
r + t = 36, so r ≤ 13 or t ≤ 22. Case A replaces the row B2 ≤ 16 by B2 ≤ 13, case B replaces S1 ≤ 25
by S1 ≤ 22; a satisfying assignment of the uncubed CNF satisfies the rows of A or of B (the counters
are one-sided). Both cases UNSAT would give M(5; 7) ≤ 35.

Outcome (final). Both runs started at 18:43, one thread each, `--nosig`, time limit 4,150 s: case A in
unit `nov13c-e7-c36a`, case B in `nov13c-e7-c36b`. Logs: `W/run/c36_*.{log,out,cake}` and
`W/run/cubes.log`.

| case | rows | variables / clauses | CaDiCaL 2.1.3 | conflicts | LRAT bytes | cake_lpr | status | SHA-256 CNF / LRAT |
|---|---|---|---|---|---|---|---|---|
| A `c36_rle13` (r ≤ 13) | S1:25 S2:25 B1:16 **B2:13** ALL:36 | 457,857 / 5,569,648 | **no verdict**: time limit 4,150 s reached at 19:52:10 (`c UNKNOWN`, exit 0); peak RSS 1,425 MB | 7,786,400 | — (partial proof deleted by `cube_n.sh`) | — | no verdict | `aba65111d42151131a55e7596043721bd86fe94d05c8fea0b2750212d2808bbe` |
| B `c36_tle22` (t ≤ 22) | **S1:22** S2:25 B1:16 B2:16 ALL:36 | 457,842 / 5,569,618 | UNSAT, 4,074 s (19:50:54); peak RSS 1,427 MB | 8,233,969 | 5,233,911,342 | `CakeML heap space exhausted` after 153 s (heap 2,600 MB, unit `nov13c-vfy-e7-c36-tle22`, 19:53:30); not repeated | **COMPUTED only** | `08b8ea9c9c588aa242485163a3d4836a0c79f8bd91c61ac25357010dc2bd9339` / `a0d2cb92dee524757ceb1467e7eea6768e7a8453dc116bd69696e8f50ab9fc21` |

- **Rung N = 36 is not closed. M(5; 7) ≤ 35 is not established**, for point sets or for colourings.
- What case B says, if its proof is accepted later: in every set of exactly 36 points with no 5-cap and no
  convex heptagon, at most 13 points end a 6-cup (r ≤ 13). It is a `--nosig` CNF, so the same would hold for
  2-colourings. Every 36-point set would then fall under case A, and only case A would remain open.
  At present this statement is COMPUTED only.
- **The case-B proof is still unchecked.** The LRAT file is still on disk (`W/run/c36_tle22.lrat`). The
  phase-2 agent re-hashed the CNF and the LRAT in unit `nov13c-e7-f2sha`; both match the hashes above,
  which were recorded at 19:50. cake_lpr needs more than 2,600 MB of heap for this proof. The comparable
  N = 37 proof (5.26 GB) failed at 2,600 MB and passed at 4,200 MB, with about 4.4 GB resident. The phase-2
  share of this track is 2 GB, and the phase-2 verifier class has 4 GB, so the check was not attempted. It
  needs a verifier slot of about 4.5 GB. Delete the 5.2 GB file after the verdict.
- **Update 21 Nov 2026 (Linux): case B is now CERTIFIED.** cake_lpr accepted the 13 Nov CaDiCaL 2.1.3 proof:
  - run as unit `esr-r36-cakeB` at 19:51–19:55 KST with `--CML_HEAP_SIZE=6000 --CML_STACK_SIZE=200`;
  - output is the exact line `s VERIFIED UNSAT`, after 176 s;
  - before the check, the CNF was re-hashed and the proof decompressed from `W/run/c36_tle22.lrat.zst` and re-hashed;
    both match the hashes in the table above (`08b8ea9c…` and `a0d2cb92…`, 5,233,911,342 bytes);
  - the decompressed copy was deleted after the verdict; `W/run/c36_tle22.lrat.zst` is kept;
  - log and output are in `data/linux-20261121/` (`cakeB.log`, `c36_tle22.cake6000.out`), the script in
    `tools/cakeB_20261121.sh`.

  So in every 36-point set (or `--nosig` 2-colouring) with no 5-cap and no convex heptagon, at most 13 points end a
  6-cup. This rests on the written arguments of §2, as for every rung. The Mac record M57R36N20261121 (branch
  `es-mac-2026-11-21`) certified case B independently with a CaDiCaL 3.0.1 proof (cake_lpr, heap 9,000 MB); this
  Linux check uses the 2.1.3 proof named in SKILL.md §2. Rung N = 36 stays open in case A, so **M(5; 7) ≤ 35 is not
  established**.
- Coverage: `cube_cover.py` was run again in phase 2 (`COVER OK`). The two CNFs carry exactly the stated
  rows, and every assignment with exactly 36 occupied states satisfies the rows of case A or of case B.
- Case A stopped at 7.8 M conflicts with no verdict; case B needed 8.2 M to finish. Nothing in the log
  says how far case A was from a verdict, or whether it would be UNSAT. For comparison, the full rung
  N = 37 needed 8.8 M conflicts (§6.3).

### 6.3 Measured scaling and the cost of N = 27 (HEURISTIC)

Conflicts needed by CaDiCaL 2.1.3 (one thread):

| catalog, model | N → conflicts |
|---|---|
| 35 states, (3,4,7,N), full model, no rows | 34 → 13; 32 → 104; 30 → 2,276; 28 → 31,431; 27 → 76,901; 26 → 291,485 |
| 56 states, (3,5,7,N), `--sigmax 1 --link`, no rows, "at least N" | 54 → 34; 52 → 293; 50 → 1,220; 49 → 4,814; 48 → 5,520; 47 → 12,616; 46 → 10,816 |
| 56 states, with rows, "exactly N" | see §6.2 |

Observations:
- **Top of the ladder (with rows, exactly N).** `--nosig`: N = 41 → 293,228 conflicts (227 s);
  N = 38 → 3,086,289 (1,279 s); N = 37 → 8,848,423 (4,138 s). `--sigmax 1 --link`: N = 41 → 275,838 (397 s);
  N = 40 → 573,706 (685 s). So the signotope packets do not reduce the number of conflicts here, they
  only make each conflict more expensive (about 700 conflicts/s against 1,300–2,400), and the cost
  grows by a factor of about **2.2–2.9 per point** (41 → 38: ×10.5 in three steps; 38 → 37: ×2.9).
- **Near the threshold** the growth is steeper: in the 35-state catalog ×2.4 and ×3.8 for the last two
  steps (28 → 27 → 26), ×3.5 on average over the last four.
- **Extrapolation to N = 27** from N = 37: between 8.8 M × 2.2¹⁰ ≈ 2 × 10¹⁰ and 8.8 M × 3.5¹⁰ ≈ 2 × 10¹²
  conflicts. Below N = 37 the signotope-free model must become satisfiable somewhere (it is at N = 27,
  §7), so the geometric proof has to carry signotope packets, at 450–700 conflicts/s on one thread:
  roughly **1 to 170 CPU-years**, with an LRAT proof of about 15 TB to several PB at the measured
  0.7–2.7 kB per conflict. That is not a certificate anyone can check with cake_lpr.
  This is an extrapolation over 10 steps from 5 data points: HEURISTIC, the exponent is the whole
  uncertainty.
- The position-indexed encoder is worse: it does not solve the 35-state instance (n = 26) at all in
  16 minutes, and for hexagons its cost *increases* with the number of points (§4.1).

Conclusion: with the present model, ETV(7; 5, 7) = 26 needs a new idea, not more CPU. The rows S1–B2
only count; what is missing is structural information about near-extremal T (no 6-cup, 20–25 points)
and R (ends of 6-cups) and about their interaction (§11).

## 7. A 27-vertex colouring with no 5-cap path and no weak heptagon (side result)

The satisfying assignment of v2 decodes (`decode_check.py`) to a 2-colouring χ of the C(27,3) = 2,925
triples of the vertices 0 < 1 < … < 26 (the owners in chronological order). File
`data/colouring27_nosig.json` (SHA-256 `b42aebe4df5cb929fd8fbdba36c344e56773d6e129a7455c8e8c19fb9633d484`):
the list of positive (cup) triples, the 27 states in order, and the check results.

Checked properties of χ:

| property | value | how checked |
|---|---|---|
| longest cap path (consecutive triples negative) | 4 vertices | `decode_check.py`: position-indexed dynamic programme, independent of the CNF |
| longest cup path | 6 vertices | the same |
| largest weak polygon (cap path + cup path on common end-vertices, both with ≥ 3 vertices) | 6 vertices; so no weak heptagon | the same |
| the original encoder `etv_sat2.py` at n = 27 (no 5-cap, no 7-cup, no (3,6)-, (4,5)-gon), **without** its signotope clauses, plus the 2,925 unit clauses of χ | SATISFIABLE | second, independent encoder |
| the same **with** the signotope clauses | UNSATISFIABLE | as expected |
| violated four-point packets | 383 of 17,550 | `decode_check.py` |
| semantic re-encoding of χ in the v2 CNF | 0 of 5,569,810 clauses violated | `owner_check.py --coloring` |

So χ is a genuine 2-colouring of the triples of a 27-element ordered set with no monotone cap path on 5
vertices, no monotone cup path on 7 vertices and no weak 7-gon in the sense of Baek–Balko. It is not a
signotope, hence not a point set and not a pseudo-configuration. Consequences:

- The **colouring version of ETV(7; 5, 7) = 26 is false.** Together with §5.1 and §6.2 the largest
  such colouring has between 27 and 36 vertices.
- By contrast the colouring version of **ETV(7; 5, 6) = 25 is true** (§5.1, CERTIFIED), as are Baek's
  cases a = 4 (his proof is in the configuration model). So in the family (7; 5, b) the colouring
  version holds for b ≤ 6 and fails at b = 7: any proof of ETV(7; 5, 7) = 26 must use four-point
  (signotope / geometric) information. This refines the known failures of the colouring analogue of
  the full conjecture at k = 7 (Balko–Valtr: strong polygons; Baek–Balko: C_weak(7) > 33).
- For the search itself: any relaxation of the 27-point problem that only uses path growth and
  common-endpoint polygons is satisfiable. The signotope packets on inclusion chains of states already
  kill this particular colouring.

We did not find this colouring statement in the sources of §9; that is not a claim of priority.

### 7.1 What the new bound gives for ES(8) (conditional)

ETVTHY20261113 §3.1 proves: weak Conj(8) (every 5-cap-free octagon-free set has a 4-cap-free subset
meeting every convex heptagon; OPEN) implies N5 = M(5; 8) ≤ 22 + M(5; 7). With M(5; 7) ≤ 36 this reads
**N5 ≤ 58**. RES33N20261113 (exact trees over certified rows) proves that N5 ≤ 59 implies
ES(8) ≤ 309, and THEORY310N20261113 §3 that N5 ≤ 56 implies ES(8) ≤ 308. So:

- **weak Conj(8) alone now implies ES(8) ≤ 309.** With the old bound M(5; 7) ≤ 41 it gave only
  N5 ≤ 63, and 309 needed weak Conj(7) in addition.
- M(5; 7) ≤ 34 (rung N = 35) would give N5 ≤ 56 and ES(8) ≤ 308 under weak Conj(8).

This is an implication between statements of other records, quoted as they stand there; nothing
unconditional about ES(8) follows from this record.

## 8. Negative results and things that did not help

- Position-indexed signotope SAT: mirror clause, backward chains, unanchored labels, upper-hull cubes,
  more points (§4.1). None changes the picture; n = 26 is out of reach in 16 minutes.
- Owner model for hexagons: no better than the position-indexed encoder (§4.2).
- Occupancy-first decisions (`occfirst.cpp`): 57 s instead of 63 s on (3,4,7,26); no verdict on the
  target in 9 minutes. Not pursued (the driver prints no progress).
- `--link` (label-linked chain variables): fewer clauses (3.95 M instead of 6.19 M) but not faster per
  conflict (about 700 conflicts/s against 1,300 for `--nosig` at N = 41).
- Cycle rows in the 56-state catalog: no gain over the four block rows (capacity stays 41, §2.3).
- Dropping family W (predecessor witnesses) or family S changes the (3,4,7,26) time by less than 35 %.
- Unit clauses learned by the solver on the signotope-free target run are almost all on witness
  variables (23,529 of 23,822); no occupancy variable was fixed at top level in the first 10 minutes
  (`units_scan.py` on the partial proof).

## 9. Literature cross-check (13 November 2026)

- J. Baek, M. Balko, *The Erdős–Szekeres conjecture revisited*, SoCG 2025
  ([LIPIcs.SoCG.2025.13](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.13)):
  definitions of weak / strong k-gons and split polygons; "known to be true only in the trivial case
  k ≥ a + u − 3 and Baek proved it when a or u equals 4"; Theorem 7: C_weak(7) > 33; exact values of
  the split-polygon numbers C_split(a,u,k). Nothing on weak-polygon numbers with a cap restriction, and
  nothing on 26 or 27 vertices.
- J. Baek, *On the Erdős–Tuza–Valtr conjecture*, [arXiv:2206.04260](https://arxiv.org/abs/2206.04260).
- M. Schroeder, *Erdős–Szekeres: upper bounds for convex heptagons and octagons*, v1 (19 Sep 2026;
  local copy `session-scratch-20261113/lit/schroeder_v1.txt`): Theorem 5.2, M₇(5,6) = 25, by a
  state-indexed hole-clause certificate (91,720 hole clauses, a coverage CNF with 461 variables); says
  that the signotope reading of his proof has not been audited.
- A. Krapivin, B. Przybocki, M. J. H. Heule, *Toward Satisfiability Modulo Realizability*,
  [arXiv:2607.02958](https://arxiv.org/abs/2607.02958) (3 Jul 2026): their PointSAT *finds* a set of 26
  points with no 5-cap and no 7-gon (the known lower bound); no upper bound at 27 is claimed.
- M. Balko, P. Valtr, *A SAT attack on the Erdős–Szekeres conjecture*, European J. Combin. 66 (2017):
  refutation of the Peters–Szekeres colouring conjecture at k = 7.

We found no claim of ETV(7; 5, 7) = 26, of M(5; 7) ≤ 40 or better, or of the colouring statements of
§5.1 and §7. The search was short (one afternoon, the listed sources and two web searches).

### 9.1 Literature (from NOVELTY20261113B §§3, 6, 10; added in phase 2)

NOVELTY20261113B is the session's literature check. It read this record while the record still said
"M(5; 7) ≤ 37, in progress"; its comparison does not depend on that number (its §1). What it says about this
record's claims:

- **The starting bound 41 is not new as a statement** (claim C4: "prior art found, in the must-cite
  sense").
  - It is Javůrek's Lemma 3, M_k(a, b) ≤ M_k(a−1, b) + M_k(a, b−1), at (7; 5, 7), with Baek's 16 and
    Schroeder's 25. Source: T. Javůrek, "Uncovered hull vertices and upper bounds for convex polygons",
    Figshare, 1 Nov 2026, unrefereed.
  - The number 41 itself was not found in print.
  - Schroeder's D₇ baseline 41 (his Proposition 7.4) is a different quantity; do not confuse the two.
- **Javůrek isolates the same number.** His Lemma 2 is B₆ − 1 = M₇(5, 7), and his Theorem 5 is
  ES(n + 1) ≤ 3Bₙ − 3. He leaves the 27-point exclusion open. His conditional "B6 ≤ 27, hence ES(7) ≤ 78"
  is the target of this record.
  - Arithmetic added in phase 2: in his notation this record's bound reads B₆ ≤ 37. Through his Theorem 5
    that gives only ES(7) ≤ 3·37 − 3 = 108, not better than Schroeder's 81.
- **No source has an upper bound on N(7; 5, 7) = M(5; 7) below 41.** Refereed statements alone give
  16 + 35 = 51; cup–cap gives 56. Three public efforts leave the 27-point case open:
  - gotrevor/es7-ladder estimates P(7,5,7) at 27 points at ≥ 811 CPU h and did not run it;
  - Javůrek ran a 28-point pilot, with timeouts and one unchecked sub-case;
  - GLitchfield experiment 0112 left 27 points undecided after a three-hour CaDiCaL budget and writes "No
    upper bound is claimed".

  So the bounds 40, 39, 37 and 36 of §6.2 were not found in the literature. That is the result of a bounded
  search, not a priority claim.
- **M₇(5, 6) = 25 (status item 3) already has two independent computer proofs.**
  - Schroeder, Theorem 5.2: Lean with native evaluation, unrefereed.
  - gotrevor, 6 Oct 2026: SAT, 49,582 subcubes UNSAT, 82 CPU h; "no DRAT/LRAT proof was logged".

  The certificate of §5.1 is a third independent computation, by one CNF with a cake_lpr-checked LRAT
  proof. It is not a new theorem. gotrevor also reports that the rungs with k ≤ 6 and (7; 4, 7) hold for arbitrary 2-colourings
  of triples. That agrees with the colouring-model certificate for Baek's case in §5.1.
- **Colouring statements (status items 3 and 4; NOVELTY §10, "Outside the nine claims").**
  - Balko–Valtr's data page (`kam.mff.cuni.cz/~balko/ES_SAT`) lists colourings of 26 vertices (no red
    5-path, no blue 6-path, no 7-gon) and of 27 vertices (no red 5-path, no 7-gon), in their model.
  - Baek's Theorem 2.7 and Baek–Balko's Theorem 7 are weak-polygon statements, for a = 4 and for the
    diagonal.
  - NOVELTY did not compare the definitions. It says the comparison is needed before items 3–4 are written
    up.

  Remark (phase 2; reasoning only, nothing was run). The two abstract models must differ:
  - NOVELTY §6 (C4) quotes Balko–Valtr's abstract value N^(4, 7, 7) = 17.
  - §5.1 certifies that no 17-vertex colouring avoids a 4-cap path, a 7-cup path and a weak heptagon.
  - Likewise, §5.1 excludes a 26-vertex colouring with no 5-cap path, no 6-cup path and no weak heptagon.

  The difference may be the polygon notion (§7 assumes Balko–Valtr use "strong polygons") or something
  else. Running `decode_check.py` on their published colourings would show which. It would also show whether
  the 27-vertex colouring of §7 is new in the weak sense.
- **Methods (claim C9).** Every component of the owner model has precedent: the injective state map
  (Chvátal–Komlós 1971; Schroeder's Lemma 5.1) and SAT on signotopes or triple orientations (Balko–Valtr,
  Scheucher, Heule–Scheucher, Krapivin–Przybocki–Heule).

## 10. Files

Record directory `tools/` (copies of the scripts in W):

| file | purpose |
|---|---|
| `owner.py` (final), `owner_v1.py` (version that generated the CNFs before 17:42) | owner-model generator |
| `cat_common.py` | states, domains D′, corners |
| `addrows.py` | lemma rows S1, S2, B1, B2, ALL |
| `owner_check.py`, `states.py`, `geom.py` | semantic positive control (point sets and colourings), exact geometry |
| `decode_check.py`, `pattern_of.py`, `mkpat.py`, `refine.py` | decode a model into a colouring, independent check, pattern tests, lazy signotope refinement (prepared, not needed) |
| `colcontrol.py`, `randsets.py`, `controls.sh`, `ctl_flags.sh`, `colcontrol.sh` | positive controls |
| `solve_lrat2.sh`, `ladder_g.sh` (and earlier `ladder.sh`, `ladder_v1.sh`, `ladder_sm.sh`) | CaDiCaL → LRAT → cake_lpr |
| `occfirst.cpp`, `occ_lrat.sh`, `prio.py` | CaDiCaL 3.0.1 library driver with a decision callback (experiments only; no claim depends on it) |
| `etv7.py`, `etv_sat2_orig.py`, `cubes.py`, `cubebench.py`, `bench.sh` | position-indexed encoder and its calibration |
| `cyc7.py`, `cegar.py`, `rup_probe.py`, `units_scan.py`, `scale34.sh`, `scale35.sh`, `exp56.sh` | discovery tools and measurements |

`data/`: `*.cake`, `*.out` (certificates: hashes and cake_lpr lines), `ladder_*.log`,
`colouring27_nosig.json`, `t57_N27_v2.pattern.json`, `pts/` (ETV and random point sets), `ctl/`
(control logs and the sampled colourings), `scale34.log`, `scale35.log`, `bench*.log`, `exp56.log`,
`cyc7_357.json`, `SHA256SUMS`.

In W (not copied, large): `run/*.cnf` of the certified instances (reproducible from the generator;
hashes in `data/`), the four small certified LRAT files of §5.1, `om/` (base CNFs), `cal/`, `exp/`.

The record was assembled at 19:33, so `data/` and `data/SHA256SUMS` show that state. The following files
were written later and are only in W (quoted in §6.2 and §11):
- `run/c36_rle13.{log,out}`, `run/c36_tle22.{log,out,cake}`;
- the final `run/cubes.log` and `run/colhunt.log`;
- `run/hunt_N28.log`, `run/hunt_N30.log`;
- the unchecked case-B proof `run/c36_tle22.lrat`, 5.2 GB.

`data/c36_*.gen.log` are the generator logs of the two N = 36 cases.

Reproduce a certificate, e.g. the colouring-model (5,6) theorem:

```
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
$PY owner_v1.py 3 4 7 26 x.cnf --nosig          # sha256 df8ace7f…
cadical --lrat --no-binary x.cnf x.lrat          # s UNSATISFIABLE, about 76 s
cake_lpr x.cnf x.lrat                            # s VERIFIED UNSAT
```

and a ladder rung: `./ladder_g.sh TAG "41" 2100 "--nosig"` (or `"--sigmax 1 --link"`).

## 11. Next steps and resumable state

1. **More rungs** (straightforward, about ×2.2 per rung): N = 37, 36, 35 … with `--nosig` and rows; each
   also lowers the colouring-model bound. Split by the number r of occupied states with f₁ = 5
   (`cube_n.sh`, `cube_cover.py`): the two cases r ≤ 13 and r ≥ 14 at N = 36 are the first example.
   Budget: a `--nosig` rung needs about 1.1 GB for CaDiCaL and a 2.6 GB heap for cake_lpr
   (LRAT 2.2 GB at N = 38).
   *Outcome at N = 36 (§6.2).* r ≥ 14 (case B) is UNSAT, but its 5.2 GB proof is unchecked; the check needs
   a heap of more than 2.6 GB (4.2 GB was enough at N = 37). r ≤ 13 (case A) has no verdict after 4,150 s.
   Next: check the kept case-B proof, then run case A longer or split it further.
2. **Where does the colouring model stop?** Its maximum is between 27 and 36. `colhunt.sh` searches
   for colourings with 28, 30, 33 vertices (only a few minutes were spent). *Final run (19:32–20:10,
   `W/run/colhunt.log`):* N = 28 and N = 30 gave no verdict in 1,150 s each (2,007,870 and 2,666,570
   conflicts). N = 33 was not run. Below that maximum + 1 the
   ladder needs signotope packets (`--sigmax 1`, or lazy refinement with `refine.py`: add the packets of
   all 4-sets inside the occupied set of a spurious solution and repeat; prepared, not needed today).
3. **Structure instead of counting.** Ideas that were not tried:
   - *mirror information*: exact "starts a 6-cup" / "starts a 4-cap" variables (start ranks with
     successor witnesses) and the four mirrored rows (at most 25 points do not start a 6-cup, …), or a
     full two-sided model (incoming and outgoing state of every owner, both injective);
   - *internal catalogs*: give the owners with f₁ ≤ 4 their states inside T (35-state catalog, where
     the (5,6) theorem takes one minute) and the owners with f₁ = 5 their states inside R (Baek's
     catalog), coupled to the 56-state model, so that the solver can use the structure of
     near-extremal T and R instead of the bare counts 25 and 16;
   - *trade-off lemmas* "r points end a 6-cup ⟹ at most 26 − r points do not", proved for one r at a
     time (each is a slice of the 27-point problem; r = 16, 15, … may be easy).
4. **Octagons.** The same generator with G = 8 gives the (4,6)-gon catalog for N(8, 5, 7)
   (`owner.py 3 5 8 N`; no row applies, the trivial bound is 56, ETV value 41). By ETVTHY20261113 §2.1,
   N5 ≤ 22 + N(8,5,7); only N(8,5,7) ≤ 42 would beat the current N5 ≤ 65, i.e. 14 holes. Not run.
5. **Stretch (7; 6, 6)**: `owner.py 4 4 7 31` (70 states, 39 holes needed). Not run: by §6.3 it is
   harder than (7; 5, 7). The colouring question for it (is there a 31-vertex colouring with no 6-cap
   path, no 6-cup path and no weak heptagon?) is a cheap first step (`--nosig`).
6. **Lean / audit.** The owner-model soundness argument (§2) is short and uses only Growth, state
   separation, Lemma R, corner attainment and exact predecessors; the (5,6) certificate has 1.75 M
   clauses (0.61 M without signotope packets) and a 321 MB LRAT proof, so a Lean check along the lines
   of ES(8) ≤ 310 looks feasible. Until then every geometric statement here is "CNF certified +
   written argument".

**Resumable state.** Nothing is running; the last phase-1 job, the colouring search, ended at 20:10.
All generators are deterministic; every certified CNF is
reproduced by the command in the ladder table (flags, N) and matches the recorded SHA-256.
W keeps: `run/*.cnf` and `*.names.pkl` of the certified rungs, the four LRAT files of §5.1, the logs
(`run/*.log`, `run/ladder_*.log`, `run/cubes.log`), and `readme_parts/` + `mk_readme.py`. It also keeps
the two N = 36 CNFs with their `.names.pkl` and the unchecked case-B proof `run/c36_tle22.lrat` (§6.2).
Check it with
`cake_lpr --CML_HEAP_SIZE=4200 --CML_STACK_SIZE=200 run/c36_tle22.cnf run/c36_tle22.lrat`, in a unit with
about 4.5 GB.

Do not rerun `mk_readme.py`: it would overwrite the phase-2 additions with the 19:33 text.

## 12. Resources, memory guard, deviations

- **Threads**: at most 3 busy threads at any time. Short extra jobs (controls, generators, experiments)
  ran while one solver unit was paused with SIGSTOP. Idle watcher scripts (a sleep loop) are not counted.
- **Memory before 18:25**: the task share was 10 GB. Three solvers on the full 14.7 M-clause CNF used
  about 2.8 GB each (8.4 GB) between 17:27 and 17:37.
- **Memory policy of 18:25** (`/home/jay/research/data/memguard-20261113/MEMORY_POLICY.txt`: track
  budget 4 GB resident, no swap, verifiers in a separate 6 GB class). Units of this track stopped by the
  guard:

  | time | unit | what happened | consequence / change |
  |---|---|---|---|
  | 18:24:03 | `nov13c-e7-ladder4` | after CaDiCaL had refuted N = 40, cake_lpr started with its default heap (4 GB) and the unit reached 3,789 MB of its 4,096 MB limit | the LRAT file was complete (hashes already recorded); it was checked at 18:38 in a separate unit with `--CML_HEAP_SIZE=2600` (`s VERIFIED UNSAT`, 20 s). The queued rung N = 39 was lost; N = 38 made it redundant. |
  | 18:33:36 | `nov13c-e7-chain39` | the same check restarted with the default heap next to two CaDiCaL runs: track total 4,224 MB | as above |

  Changes: cake_lpr now runs only through `vfy.sh` (own unit `nov13c-vfy-e7-*`, `--CML_HEAP_SIZE=2600
  --CML_STACK_SIZE=200`, MemoryMax 3,500 MB, MemorySwapMax=0); CaDiCaL units are started with MemoryMax
  2,000 MB and MemorySwapMax=0 and use about 1.1 GB each on the `--nosig` CNF (three at a time: 3.3 GB);
  the wrapper scripts of the two runs already in progress were frozen with SIGSTOP so that they could
  not start a default-heap cake_lpr, and `watch_finish.sh` finished them; the full 14.7 M-clause model
  (2.8 GB per solver) was not run again.
- **Checker heap**: the N = 37 proof (5.26 GB) exhausted a 2,600 MB CakeML heap after 141 s (19:28,
  `CakeML heap space exhausted`, no verdict); it was accepted with `--CML_HEAP_SIZE=4200` (148 s). No
  other verifier unit was running at that time; the unit used at most 4.4 GB of the 6 GB verifier class.
  The N = 36 case-B proof (5.23 GB) failed in the same way at 19:53:30, after 153 s with 2,600 MB. That was
  after the phase-1 cut-off, so nobody restarted it with a larger heap (§6.2).
- **Solver versions**: every certificate is CaDiCaL 2.1.3 (`/usr/bin/cadical`) + cake_lpr. The CaDiCaL
  3.0.1 library (read-only use of `erdos810-20261106/cadical/build/libcadical.a`) was used only for the
  occupancy-first experiments; no claim depends on it.
- **Accident**: at 18:36 a `pgrep -f` pattern matched the shell that issued it and froze that shell
  for about two minutes (SIGSTOP, then SIGCONT). No unit and no file was affected.
- No Git state was changed. Nothing outside W and this record directory was written, except files
  under the session scratch that the tools created themselves (one downloaded PDF, copied into
  `W/lit/`).

## 13. Phase-2 completion (13 November, 20:20–20:48 KST)

Done by a phase-2 agent. It had a share of 1 thread and 2 GB, unit prefix `nov13c-e7`, and could edit this
README only.
- **Read**: the logs and outputs of the N = 36 cases, `cubes.log`, `colhunt.log`, the hunt logs, every
  `run/*.cake` file and the memory-guard log.
- **Checked against the tables above**:
  - every `run/*.cake` file: the nine certified CNF/LRAT hash pairs of §5.1 and §6.2 carry
    `s VERIFIED UNSAT`, with the hashes printed here;
  - `c36_tle22.cake` has no verdict line;
  - re-hashed in unit `nov13c-e7-f2sha` (1 thread, under one minute): `run/c36_tle22.cnf`,
    `run/c36_tle22.lrat` and `run/c36_rle13.cnf`, all equal to the recorded hashes;
  - `cube_cover.py`, re-run: `COVER OK`.
- **Not done**: the cake_lpr check of the case-B proof. It needs more than 2.6 GB of CakeML heap, and the
  phase-2 share is 2 GB (§6.2). Status: unchecked; the proof file is kept. No file was deleted. Nothing in
  `data/` or `tools/` was changed.
- **No new computation.** The only results added here come from logs that the phase-1 runs wrote after
  19:33. The arithmetic remark in §9.1 (B₆ ≤ 37 ⇒ ES(7) ≤ 108 through Javůrek's Theorem 5) and the
  comparison of abstract models there are reasoning, not computation.
