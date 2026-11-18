# FLAYER20261113: the first-layer Erdős–Tuza–Valtr case (6,6;8) — structural capacity rows (13 November 2026)

Track D2 of the 13 November afternoon session, 16:53–21:00 KST. Work directory
`/home/jay/research/data/flayer-20261113/` (W; not in Git). One thread in total (units `nov13c-d2-*`).
Nothing is committed. All units of this track are stopped (§11). The last one, `nov13c-d2-ns17`, is an
annealing run started at 19:31, after this README was first written; it ended at about 19:38.

> **Note (13 November, phase 2).** Phase-1 agent cut off at about 19:40 KST; completed from the work
> directory by a phase-2 agent at 20:48 KST.
> - The README of 19:30 had no open block. Only the last annealing run (`run_ns17.sh`) finished later. It
>   raised the largest |E ∪ A| found in a real set from 31 to 32; the set was re-checked in phase 2 with
>   the record's pure-Python checker (§5, §11).
> - The 26-point instance of M₇(5, 6) was not decided by this track, and no log or proof of the attempt
>   survives. The statement was CERTIFIED the same afternoon with another encoder, in ETV7SAT20261113 §5.1
>   (§7.1, §11).
> - The phase-2 agent added §12 (literature) and §13 (what was checked in phase 2). It could edit only this
>   README, so `data/` and `SHA256SUMS` show the state of 19:29.

Labels: **PROVED** = written proof (plus exact checks as stated); **CERTIFIED** = CaDiCaL 2.1.3 LRAT proof accepted
by cake_lpr (`s VERIFIED UNSAT`) for the stated CNF; **COMPUTED** = solver verdict only (SAT verdicts are always
re-checked by an independent exact routine, UNSAT verdicts are not); **HEURISTIC** = search statistics.

## 0. Headline

**No capacity row beyond the cycle rows was proved. The exact hole minimum of the proved rows is unchanged:
6 holes, N66 ≤ 64 (COMPUTED, CP-SAT OPTIMAL over the 50 cycle rows).** What the track establishes instead:

1. **Small rows do not exist (COMPUTED, abstract model).** Every set of at most four states of the 70-state
   catalog is jointly occupied in some (6,6;8)-signotope with at most 14 points (70 singles, 2,415 pairs,
   54,740 triples, 916,895 quadruples; every witness re-checked by an independent exact DP). So every row that
   can be derived in the signotope model — in particular every coupled-CNF row — has support at least 5.
2. **Level-set capacities are false** (§5). Refuted by real point sets: "E has no (4,5)-gon", |X| ≤ 16,
   **|E| ≤ 25** and |E ∪ A| ≤ 30 (a real 35-point set in which 31 points end a 5-cup). |E ∪ A| ≤ 35, which
   would have given N66 ≤ 55 and ES(8) ≤ 309, is refuted by verified abstract configurations (36 on 40 points,
   40 on 44); the largest value found in real sets is 32 (31 when this README was first written; a
   36-point set found at 19:38, §5). The (5,5;6) analogues of all these statements are
   refuted by real point sets.
3. **PROVED lemmas** (§2): junction, level pairs, top-level structure, location of octagons, the composition
   formulas with the hole patterns of all one-step compositions, the small-witness principle, and two
   conditional reductions (|E ∪ A| ≤ 35 ⇒ N66 ≤ 55; Pascal split + Schroeder ⇒ N66 ≤ 50).
4. **CERTIFIED** (§7): every 15-point set with no 5-cap and no 5-cup contains a convex hexagon, i.e. the
   first-layer value N₁(5,5) = 14 (abstract signotope model, cake_lpr). The 26-point instance of Schroeder's
   M₇(5,6) = 25 was not decided by this track's encoder (one 6-minute run; no log or proof kept). The
   statement itself is CERTIFIED with another encoder in ETV7SAT20261113 §5.1 (§11). Both values were
   known before (§12).
5. **Which induction** (§8): the Pascal split PS(a,b) (S = S₁ ⊔ S₂ with S₁ ∈ FL(a−1,b), S₂ ∈ FL(a,b−1)) is the
   only induction matching the first-layer recursion; PS(6,6) with Schroeder's M₇(5,6) = 25 would give
   N66 ≤ 50. **PS(5,5) is false for real point sets**: seven explicit 14-point sets with no 5-cap, no 5-cup and
   no convex hexagon have no such split (exact brute force over all 16,384 partitions, pure Python), although
   every configuration with at most 13 points splits (complete search; CERTIFIED for n ≤ 11) and every
   sampled or randomly generated configuration did. PS(6,6) is open and has no real support. Only the
   one-sided split survives a complete test for (5,5;6); it would give N66 ≤ 60, not 55. *Literature
   (§12):* PS(a,b) is public, as gotrevor's L1(a,b) and as the first-diagonal case of GLitchfield's
   PASCAL-SPLIT; gotrevor reports L1(5,6) false for abstract 2-colourings.

## 1. Question, setting, notation

A **(6,6;8)-set** is a finite planar point set with distinct x-coordinates, in general position, with no
6-cap, no 6-cup and no convex octagon. N66 is its largest size. Points are indexed by increasing x; a cap
(cup) is a sequence whose consecutive triples are negatively (positively) oriented.

- E₋(u,v), E₊(u,v): largest number of points of a cap / cup ending with the pair (u,v); F₋, F₊: starting
  with the pair. Label d(u,v) = (E₋(u,v) − 1, E₊(u,v) − 1) ∈ [1..4]².
- Incoming state I(v): the down-set generated by {d(u,v) : u < v}, written as column heights
  f₁ ≥ f₂ ≥ f₃ ≥ f₄ (column = cap coordinate), 70 states, indexed as in `etv_common.py` with ETV_A=4, ETV_B=4.
  States are written as four digits, e.g. 4111. The owner map is injective (ETV5N20261113 §2, same proof).
- Outgoing state O(v): the same with F₋, F₊; it is the incoming state of v in the set reflected in a
  vertical line. Reflection in a horizontal line swaps caps and cups and transposes the diagram.
- Ranks: β(v) = 1 + f₁(v) (longest cup ending at v), c₋(v) = 1 + #{a : f_a(v) ≥ 1} (longest cap ending at v);
  ω(v), c₊(v): longest cup / cap starting at v.
- Level sets: **E** = {β = 5} = {f₁ = 4} (35 states), **A** = {c₋ = 5} = {f₄ ≥ 1} (35 states),
  **X** = E ∩ A (20 states), **Z** = S ∖ (E ∪ A) = {f₁ ≤ 3, f₄ = 0} (20 states); E′, A′, X′ are the
  corresponding sets of starting points (ω = 5, c₊ = 5, both).
- In a set with no 6-cap and no 6-cup a convex octagon is exactly a 5-cap and a 5-cup with common endpoints
  ("first layer", n = a + b − 4). FL(a,b) denotes the general class: no a-cap, no b-cup, no
  ((a−1)-cap, (b−1)-cup)-gon; N₁(a,b) = C(a+b−4, a−2) − C(a+b−6, a−3) is its conjectured maximum
  (Baek's theorem for a = 4; Schroeder's M₇(5,6) = 25 for (5,6)). N₁(6,6) = 70 − 20 = 50.

Known before: N66 ≤ 64 (cycle rows, 6 holes; COMPUTED); N66 ≤ 55 would give ES(8) ≤ 309.

## 2. PROVED statements

All statements are about a (6,6;8)-set S unless said otherwise. Exact checks on real sets: §2.8.

**2.1 Junction.** For an in-cell (a,b) ∈ I(v) and an out-cell (a′,b′) ∈ O(v): a + a′ ≤ 4 or b + b′ ≤ 4.
In particular E ∩ A′ = ∅ and A ∩ E′ = ∅: a point that ends a 5-cup starts no 5-cap, and the mirror.

*Proof.* Take u < v with a cap of a+1 points and a cup of b+1 points ending with (u,v), and w > v with a cap
of a′+1 points and a cup of b′+1 points starting with (v,w). If (u,v,w) is a cap, the caps concatenate to a
cap with a + a′ + 1 ≤ 5 points; if it is a cup, the cups give b + b′ + 1 ≤ 5. ∎

**2.2 Pairs inside a β-level.** Let u < v with β(u) = β(v) = k ≥ 2, and let t be the predecessor of u on a
k-cup ending at u. Then (t,u,v) is a cap; in particular E₋(u,v) ≥ 3. Hence a cap inside one β-level has at
most 4 points. Mirror: pairs inside a c₋-level have E₊ ≥ 3.

*Proof.* If (t,u,v) were a cup, the k-cup would extend by v and β(v) ≥ k + 1. Along a cap w₁…w_m inside
the level, E₋(w₁,w₂) ≥ 3 and E₋ grows by one at every step, so m + 1 ≤ 5. ∎

**2.3 The top level.** (i) E has no 5-cap. (ii) Every 4-cap u k₁ k₂ v with all points in E extends to a
5-cap t u k₁ k₂ v of S, so v ∈ X. (iii) E ∖ X has no 4-cap. The mirror statements hold for A.

*Proof.* (ii) is 2.2 for the pair (u,k₁). (i) the same extension of a 5-cap would be a 6-cap. (iii) follows
from (ii). ∎

Remark. (iii) gives nothing numerically: no 4-cap and no 6-cup allow C(6,2) = 15 points, the number of
states {f₁ = 4, f₄ = 0}; and E ∖ X is full (15 points) in the ETV set.

**2.4 Where octagons live.** In a set with no 6-cap and no 6-cup, every convex octagon is a 5-cap and a
5-cup from a point of X′ to a point of X. So a set with no 6-cap, no 6-cup and X = ∅ is automatically
octagon-free, and it has at most 50 points (the 20 states of X are holes). The first-layer statement
N66 = 50 says that points of X never pay.

**2.5 One-step compositions.** Let L and R be point sets, L to the left of R, such that R lies above every
line through two points of L and L lies below every line through two points of R ("R high above L").
Then, for S = L ∪ R,

- cap(S) = max(cap(L), cap(R) + 1), cup(S) = max(cup(L) + 1, cup(R)),
- gon(S) = max(gon(L), gon(R), cap(R) + cup(L)),

where cap, cup, gon are the largest cap, cup and convex polygon.

*Proof.* (l,l′,r) is a cup and (l,r,r′) is a cap for l,l′ ∈ L and r,r′ ∈ R. So a cap meeting both sides is
one point of L followed by a cap of R, and a cup meeting both sides is a cup of L followed by one point of R;
conversely all of these are caps / cups. A convex polygon meeting both sides has its leftmost vertex u in L
and its rightmost vertex v in R; its upper chain is u followed by a cap of R ending at v, its lower chain a
cup of L starting at u followed by v, so it has i + j vertices with i ≤ cap(R), j ≤ cup(L), and every such
pair of chains is a convex polygon. ∎

*Consequence.* S is a (6,6;8)-set iff cap(L) ≤ 5, cup(L) ≤ 4, cap(R) ≤ 4, cup(R) ≤ 5, both are octagon-free
and cap(R) + cup(L) ≤ 7. There are two maximal types, each with 50 points:

- type 1: cup(L) ≤ 3 (|L| ≤ 15) and cap(R) ≤ 4 (|R| ≤ 35, **any** 35-point set with no 5-cap and no 6-cup);
- type 2: cup(L) ≤ 4 (|L| ≤ 35, any 35-point set with no 6-cap and no 5-cup) and cap(R) ≤ 3 (|R| ≤ 15).

*Hole patterns.* With g the internal state of a point of R (cap coordinates 1..3 in type 1):
- type 1: points of L keep their states (all states with f₁ ≤ 2); a point of R gets (max(3, g₁), g₁, g₂, g₃),
  because pairs (l,r) have labels (1, β_L(l)) with β_L ≤ 3, and pairs inside R have labels (a+1, b). The
  occupied states are {f₁ ≤ 2} ∪ {f₁ = 3} ∪ {f₁ = f₂ = 4}: the holes are **H₂ = {f₁ = 4, f₂ ≤ 3}**.
- type 2: L occupies {f₁ ≤ 3}; a point of R gets (4, g₁, g₂, 0): the holes are **H₁ = {f₁ = 4, f₄ ≥ 1} = X**.
- The mirror operation ("R deep below L") transposes: H₁ᵀ = H₁ and H₂ᵀ = **H₃ = {f₄ = 1}**.

So this family of extremal sets is large (R is arbitrary among cup–cap extremal sets), but it has only the
three hole patterns H₁, H₂, H₃ (each 20 states). Their common part is the six states
4111, 4211, 4221, 4311, 4321, 4331. Checked exactly on constructed sets: §4.

**2.6 Small-witness principle.** Let T be a set of states that are all occupied in a (6,6;8)-set S. Then
there is a subset W ⊆ S with |W| ≤ nmax(T) := Σ_{s ∈ T} (1 + Σ_{corners (a,b) of s} (a + b − 1)) in which the
same points own the same states, and whose rightmost point is one of these owners. (A corner of a diagram is
a maximal cell.)

*Proof.* For each owner v and each corner (a,b) of I(v) choose u < v with d(u,v) ≥ (a,b), an (a+1)-cap and
a (b+1)-cup of S ending with (u,v): at most a + b − 1 points besides v. Let W be the owners and these points.
Labels computed in a subset do not exceed the labels in S, so I_W(v) ⊆ I_S(v); the corners are still
attained, so I_W(v) = I_S(v). W is again a (6,6;8)-set, and every chosen point lies to the left of its
owner. ∎

So the joint occupancy of a small set of states is a question about point sets of bounded size, with the
witnesses included. This is what the coupled owner CNF cannot see (it contains the owners only).

**2.7 Two conditional reductions.**
- |S| = |Z| + |E ∪ A| ≤ 20 + |E ∪ A|. So "|E ∪ A| ≤ 35" would give N66 ≤ 55 with no rows at all. It is
  **not provable in the signotope model** (§5: |E ∪ A| = 40 on 44 points).
- **Pascal split.** If S = S₁ ⊔ S₂ with S₁ free of 5-caps and of (4-cap, 5-cup)-gons and S₂ free of 5-cups and
  of (5-cap, 4-cup)-gons, then |S₁| ≤ 25 by Schroeder's M₇(5,6) = 25 and |S₂| ≤ 25 by its mirror image, so
  |S| ≤ 50. (N₁(a,b) = N₁(a−1,b) + N₁(a,b−1) is the Pascal recursion of the first-layer value.) §8.

**2.8 Exact checks.** `tools/lemma_check.py` tests 2.1 (cell form), 2.2, 2.3 (with the mirror statements), the
injectivity of in- and out-states and the rank identities on 41 real sets (26–50 points; all pools of §4) in
all four mirror images: 164 oriented sets, **0 violations** (`data/logs/lemma_check.log`). 2.5 is checked on
the constructed sets of §4.

## 3. The witness-complete abstract model (new encoder; soundness and controls)

`tools/wit.py` (the (6,6;8) row certifier), `tools/witg.py` (general FL(a,b), state indicators, used for
scans and enumeration) and `tools/fls.py` (general FL(a,b) with cardinality requirements) use the same model.

**Variables and clauses.**
1. o(i,j,k) for i < j < k: true iff the triple is positively oriented. *Signotope axioms*: on every 4-tuple
   the sequence (o_ijk, o_ijl, o_ikl, o_jkl) has at most one sign change (eight clauses of length 3).
2. pres(p): the first m points are present (prefix; `wit.py`, `witg.py`).
3. *Exact chain variables.* capE_k(u,v), k = 3, 4, 5, with capE_k(u,v) ⟺ ∃ t < u: (t,u,v) negative and
   capE_{k−1}(t,u) (capE₂ is true); cupE_k likewise. Both directions are encoded (Tseitin).
4. *No 6-cap, no 6-cup* ending at a present point: ¬(capE₅(t,u) ∧ (t,u,v) negative), and the mirror.
5. *No octagon*, one-directional: capF₄(u;p,q) ⇐ (u,t,p), (t,p,q) negative; cap5(u,v) ⇐ capF₄(u;p,q) ∧
   (p,q,v) negative; the same for cups; ¬(cap5(u,v) ∧ cup5(u,v)) for present v.
6. *Exact cells.* cell(p,a,b) ⟺ ∃ u < p: capE_{a+1}(u,p) ∧ cupE_{b+1}(u,p).
7. *Owners* (`wit.py`): own(p,j) for each state s_j of the support T, exactly one p per j; own(p,j) implies
   pres(p), the corner cells of s_j true at p and the minimal cells outside s_j false at p (so I(p) = s_j
   exactly, because cell is monotone). The last present point is an owner.
   `witg.py` has indicators st(p,s) ⟺ (p present and I(p) = s) for all states and occ(s) ⟺ ∃p st(p,s).

**Soundness of UNSAT.** Let S be a real (6,6;8)-set in which all states of T are occupied. Take W from 2.6,
sorted by x, as the present points, |W| ≤ nmax(T); put the absent points far to the right in general
position. Orientation signs satisfy the signotope axioms (ETV5N20261113 §2, item 4). Give every defined
variable its true value: the chain equivalences are the recursion for the longest cap / cup ending with a
pair; clauses 4 and 5 hold because W has no 6-cap, no 6-cup and no octagon (for the one-directional
variables take "true iff such a chain exists"); the cell equivalences are the definition of I(p); the owners
keep their exact states by 2.6 and the last point of W is an owner. So the CNF with n = nmax(T) points is
satisfiable. Hence: **UNSAT at n = nmax(T) ⇒ the states of T are never all occupied** (a demand-one row).
For `fls.py` (no flags, no owners) the same argument shows: UNSAT at n ⇒ no real set of n points in FL(a,b).

**Meaning of SAT.** A model is a (6,6;8)-*signotope* (abstract configuration), not necessarily a real point
set. Every SAT model used in this record was decoded and re-checked by an independent pure-Python DP
(signotope axioms, longest caps and cups, the octagon test from every start point, the states). SAT
therefore shows that the statement in question **cannot be proved from the signotope axioms** — which covers
every SAT / coupled-CNF argument of this project — and it is labelled "abstract" below. It is a refutation
for real point sets only when a real set is given.

**State separation in the model.** d(u,v) ∉ I(u) holds for signotopes with the same proof (if a pair (t,u)
had a label ≥ d(u,v) in both coordinates, the triple (t,u,v) would raise E₋(u,v) or E₊(u,v)). So "at most
one point per state" is implied by the model and may be added as clauses (`cert.py`, mode `inj`).

**Controls** (`tools/wit_control.py`, 6 real sub-configurations of 8–20 points, orientations fixed by unit
clauses): the true states are accepted (6/6), also with two padded absent points (6/6); a state that is not
occupied is rejected (6/6); a set with a 6-cap, 6-cup or octagon is rejected (6/6). `fls.py` reproduces the
known first-layer maxima N₁(4,4) = 4, N₁(4,5) = 7, N₁(4,6) = 11, N₁(5,5) = 14 (SAT at the value, UNSAT one
above; §7) and finds 25-point configurations for (5,6). `witg.py` asserts for every enumerated model that the
occ variables agree with the independent DP.

## 4. Data: extremal sets and hole patterns

All real sets are integer point sets, checked by the exact C routine `esgeo` (128-bit orientation tests);
states by exact DP (`tools/fl.py`, `tools/fast.py`).

| family | sets | sizes | in-hole patterns |
|---|---|---|---|
| ETV block set `etvcon.etv(8,6,6)` (blocks of 15, 20, 15 points) and its three mirror images (`data/pool_etv.jsonl`) | 4 | 50 | H₁ (as built, y-mirror), H₂ (x-reversed), H₃ (rotated by 180°) |
| one-step compositions of 2.5, with the pieces as built or x-reversed (`data/pool_compose.jsonl`) | 8 | 50 | H₂ (type 1), H₁ (type 2), as predicted |
| largest (6,6)-subsets found in 12 of the 1,234 known 64-point octagon-free sets (greedy + swaps, `tools/sub64.py`, `data/pool_sub64.jsonl`) | 12 | 30 (2), 40 (5), 50 (5) | the five 50-point subsets: H₁ (in), H₂ (out) |
| simulated annealing, exact validity at every step (`tools/gen66.py`, `gen2.py`): 15 runs from scratch, 4 runs seeded with earlier sets | 19 | 26–40 | far from extremal: 33–40 points when maximizing the size |

- H₁ = {f₁ = 4, f₄ ≥ 1} = X, H₂ = {f₁ = 4, f₂ ≤ 3}, H₃ = {f₄ = 1}; 20 states each; H₁ ∩ H₂ ∩ H₃ =
  {4111, 4211, 4221, 4311, 4321, 4331}.
- (|E|, |A|, |X|) is (15, 15, 0) for H₁, (15, 25, 10) for the x-reversed ETV set and (25, 15, 10) for the
  rotated one; |Z| = 20 and |E ∪ A| = 30 in all of them.
- **Every real 50-point set found has one of the three patterns.** All of them are ETV-type (decomposable)
  sets; annealing from scratch did not come near 50 points.
- **Abstract 50-point configurations are different (COMPUTED, verified signotopes, `data/samples_50.jsonl`).**
  Two CaDiCaL runs (seeds 1, 2; about 150 s each) gave 50-point (6,6;8)-signotopes with
  (|E|, |A|, |E ∪ A|, |X|) = (16, 16, 30, 2) and (29, 30, 40, 19). Their four hole patterns (incoming and
  outgoing states) are none of H₁, H₂, H₃; the holes by class (X, E∖X, A∖X, Z) number (18, 1, 1, 0),
  (1, 2, 9, 8), (1, 5, 4, 10) and (16, 3, 0, 1). The hook state 4111 is the only state that is a hole in all
  seven patterns; 50 of the 70 states are holes in at least one of these four (`tools/holes50.py`).
  So the 20 holes of an extremal configuration are not confined to X or to any level set.
- No single state is a hole in general: all 70 states occur as incoming states in the real pool (47 sets), and
  69 of the 70 have an explicit real witness of at most 12 points (`data/singles_real.jsonl`; realized from
  the SAT witnesses by annealing on wrongly oriented triples, then re-checked exactly; the missing one, 4442,
  is occupied in pool sets).
- Abstract maximum: a 50-point configuration exists (SAT); the 51-point instance was not decided in 420 s
  (no claim). So nothing found here contradicts N66 = 50 even in the signotope model.

## 5. Candidate rows: ranking and status

Exact hole minimum of the 70-state system with the 50 cycle rows of
`/home/jay/research/data/n66-20261113/cyc_base_A4B4.json` plus the candidate rows (CP-SAT, one worker, OPTIMAL in
every line; `tools/rank.py`). "Abstract" = verified signotope (§3); such a candidate may still be true for real
point sets, but it cannot be proved by a signotope-level argument.

| candidate (support; demand) | holes | N66 ≤ | status |
|---|---|---|---|
| none (cycle rows only) | 6 | 64 | baseline reproduced |
| \|E\| ≤ 25 ({f₁ = 4}, 35 states; 10) | 10 | 60 | **REFUTED by a real set**: \|E\| = 31 on 35 points (`data/cex/E_31_n35.json`: \|A\| = \|X\| = 17; exact C check and the independent pure-Python check `tools/verify_levels.py`). Found by annealing at low temperature from a set with \|E\| = 25, after four runs from scratch had stopped at 24–25. Abstractly \|E\| = 33 on 40 points (`data/samples_lvl.jsonl`). The (5,5;6) analogue \|E\| ≤ 7 is refuted by real sets as well (9; `data/sets_fl55_E.jsonl`) |
| \|E\| ≤ 25 and \|A\| ≤ 25 | 11 | 59 | refuted (same set) |
| \|E\|, \|A\| ≤ 26 / 28 / 30 | 10 / 9 / 7 | 60 / 61 / 63 | refuted by the same real set |
| \|E ∪ A\| ≤ 30 (50 states; 20) | 20 | 50 | **REFUTED by the same real set** (\|E ∪ A\| = 31, with \|Z\| = 4); abstractly 36 on 40 points, 40 on 44 and on a 50-point configuration |
| \|E ∪ A\| ≤ 35 (50 states; 15) | 15 | 55 | **abstractly false** (same abstract witnesses); not refuted by a real set: the largest real value found is 32 (four seeded runs). The fourth run, after the first version of this README (19:31–19:38), found \|E ∪ A\| = 32 on 36 points, with \|E\| = \|A\| = 21 and \|X\| = 10; coordinates in §11. This was the cheapest route to ES(8) ≤ 309 (2.7) |
| \|X\| ≤ 16 (ES(6) = 17, if X were hexagon-free) / ≤ 14 (20 states; 4 / 6) | 8 / 9 | 62 / 61 | **REFUTED by real sets**: \|X\| = 17 and 19 on 29 points (`data/cex/X_19_n29.json`); abstractly \|X\| = 20 on 40 points |
| E has no (4,5)-gon (then \|E\| ≤ 25 by Schroeder) | – | – | **REFUTED by a real set** (40 points, \|E\| = 20, `data/cex/E_has_45_gon_n40.json`) |
| E ∖ X has no (3,5)-gon (then ≤ 11 by Baek) | – | – | false: E ∖ X has 15 points in the ETV set |
| in/out junction coupling: occupied in-states and out-states perfectly matched through the pairs allowed by 2.1 (1,764 of 4,900), both vectors satisfying the cycle rows (`tools/hall.py`) | 6 | 64 | valid (PROVED by 2.1) but **no cut**: CP-SAT OPTIMAL 64 |
| a single state is always a hole (the six common holes of §4) | – | – | REFUTED by real sets (§4) |

So no level-set statement survives: the top level E, the double level X and the union E ∪ A can all be almost
full, and the first-layer deficit of 20 is a global trade-off between levels (compare the 50-point
configurations with |E ∪ A| = 30 and 40). The exact (5,5;6) data of §7 show the same thing.

## 6. Small supports: there is no row with at most four states (abstract)

Method: `tools/witg.py` builds the model of §3 for 14 points with indicators occ(s) for all 70 states; a
support T is tested by solving under the assumptions occ(s), s ∈ T (incremental CaDiCaL 1.5.3 through pysat).
Every model is decoded and re-checked by the independent DP, and its whole set of occupied states is used to
skip later supports that it covers.

| supports | number | SAT queries needed | not realizable on ≤ 14 points |
|---|---|---|---|
| single states (`wit.py`, escalating n) | 70 | 70 | 0 (all within 12 points) |
| pairs (`wit.py`) | 2,415 | 2,415 | 0 (all within 12 points) |
| triples (`tools/scan3.py`) | 54,740 | 3,680 | 0 |
| quadruples (`tools/scan4.py`) | 916,895 | 36,348 | 0 |
| quadruples containing the hook state 4111 (separate run) | 52,394 | 10,971 | 0 |

Cross-check with the other encoder: 300 random quadruples and 100 random triples were decided again by `wit.py`
(owner variables, CaDiCaL 2.1.3) on 14 points: 400 of 400 SAT (`tools/crosscheck4.py`).

**Consequence (COMPUTED).** In the signotope model every set of at most four states is jointly occupiable.
A valid row for real point sets with support ≤ 4 would need all these abstract witnesses to be
non-realizable; for single states this is excluded by explicit real sets (§4). For pairs, a 5-minute run
realized 996 of 1,238 attempted pairs by explicit real sets of at most 12 points (`data/pairs_real.jsonl`,
exact re-check of the states); 242 attempts failed within the step limit (no evidence of non-realizability)
and 1,177 pairs were not attempted.

By contrast the small first-layer classes do have small circuits (§7): one state in FL(4,4), pairs in
FL(4,5), a triple in FL(5,5). The minimum circuit size grows with the class, and for (6,6;8) it is at least 5.
A circuit of five states needs a certificate at nmax(T) of roughly 40–60 points (2.6), i.e. an instance of
the size of the whole problem; this is why the witness-complete method produced no row today.

## 7. Small first-layer cases: exact and certified results (abstract model)

FL(a,b) and N₁(a,b) as in §1; `tools/fls.py`, `tools/cert.py`, `tools/witg.py`, `tools/circuits.py`.

**7.1 Values.** UNSAT at n means: no real point set of n points in the class (§3).

| class | states | N₁ | at n = N₁ | at n = N₁ + 1 |
|---|---|---|---|---|
| FL(4,4) | 6 | 4 | SAT | UNSAT, **CERTIFIED** (ES(4) = 5; control) |
| FL(4,5) | 10 | 7 | SAT | UNSAT, **CERTIFIED** (Baek, n = 5; control) |
| FL(4,6) | 15 | 11 | SAT | UNSAT, **CERTIFIED**, both modes (Baek, n = 6; control) |
| FL(4,7) | 21 | 16 | SAT | UNSAT, **CERTIFIED**, both modes, 1.1 s / 1.7 s (Baek, n = 7; control) |
| FL(4,8) | 28 | 22 | – | not decided in 400 s (Baek, n = 8; certified in THEORY310N with another encoder) |
| **FL(5,5)** | 20 | 14 | SAT | UNSAT, **CERTIFIED**, both modes (1.1 s / 1.6 s; LRAT 11.4 MB / 15.6 MB) |
| FL(5,6) | 35 | 25 | SAT (0.4 s) | not decided by this encoder: one run of 6 minutes (`inj`), then stopped; not repeated (§10.1). CERTIFIED with the owner-model encoder of ETV7SAT20261113 §5.1 (§11) |
| FL(6,6) | 70 | 50 | SAT (150 s) | not decided in 420 s |

**CERTIFIED statement: every set of 15 points in general position (distinct x) with no 5-cap and no 5-cup
contains a convex hexagon**; equivalently N₁(5,5) = 14, the first-layer Erdős–Tuza–Valtr value for
(a, b, n) = (5, 5, 6). The 14-point ETV set `etvcon.etv(6,5,5)` attains 14 (exact check: largest polygon 5,
caps 4, cups 4). Certificate: CNF
`fl_5_5_15_plain.cnf`, SHA-256 `9290bd1e…ffcd3`; LRAT SHA-256 `ae209678…ea72`; cake_lpr `s VERIFIED UNSAT`
(`data/certified.jsonl`; the CNFs are regenerated byte-identically by `cert.py`). We did not search the
literature for this case; it is weaker than ES(6) = 17 only in the sense that it needs the cap/cup hypothesis,
and it is the (5,5) instance of the ETV conjecture.

"Both modes": `plain` = `fls.FL` (signotope + exact chains + class clauses); `inj` = `witg.WitG` with all
points present plus "at most one point per state" (sound by state separation, §3).

**7.2 Level sets in FL(5,5)** (E = ends of 4-cups, 10 states; A = ends of 4-caps; X = E ∩ A, 6 states;
E ∪ A, 14 states; Z, 6 states). Exact maxima over abstract configurations with n points
(`tools/small_table.py`, `data/small_table_5_5.json`):

| n | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|
| max \|E\| (= max \|A\|) | 5 | 6 | 7 | 8 | 9 | 9 | 9 |
| max \|E ∪ A\| | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
| max \|X\| | 3 | 4 | 5 | 6 | 6 | 6 | 6 |

- The Pascal-type guesses \|E\| ≤ N₁(4,5) = 7 and \|E ∪ A\| ≤ 14 − 6 = 8 are false; the true maxima 9 and 11
  are **attained by real point sets** (annealing, four of four and two of two runs;
  `data/sets_fl55_E.jsonl`, `data/sets_fl55_EuA.jsonl`).
- For a = 4 the top-level bound does hold: \|E\| ≤ b − 2 in FL(4,5) and FL(4,6) for every n (UNSAT for all n,
  `tools/toplevel.py`), while \|A\| ≤ N₁(4,b−1) and the E ∪ A bound fail there too.

**7.3 Realizable occupancy sets and circuits** (`witg.py` enumeration with blocking clauses; every model
re-checked; `data/maximal_*.json`, `data/circuits_*.json`). A circuit is a minimal set of states that is not
jointly occupiable.

| class | maximal realizable occupancy sets | circuits |
|---|---|---|
| FL(4,4) | 3, all of size 4 | {21}, {11, 20, 22} |
| FL(4,5) | 13, all of size 7 | {20,31}, {21,31}, {30,31}, {11,22,30,32}, {21,22,30,32} and four of size 5: nine in all |
| FL(5,5) | 1,145, of sizes 11, 12, 13, 14 | sizes 3–9: 1, 4, 6, 43, 97, 166, 251 (568; larger sizes not enumerated). Smallest: {211, 310, 311}; {110,211,311,320}, {200,221,310,311}, {111,211,311,320}, {221,300,310,311} |
| (6,6;8) | – | none of size ≤ 4 (§6) |

The smallest circuits consist of the hook state (first row and first column full: 21, 31, 311) and
truncations of it; their size is 1, 2, 3 for (4,4), (4,5), (5,5) and at least 5 for (6,6). Already
for (5,5;6) the bound 14 needs hundreds of circuits of 6–9 states; it is not a consequence of a few
capacity rows.

## 8. Which induction for the first-layer bound 50?

**8.1 What fails on levels.** N₁(a,b) = N₁(a−1,b) + N₁(a,b−1), and unrolled N₁(6,6) = Σ_{j=1..5} N₁(5, j+1) =
1 + 3 + 7 + 14 + 25. The rotated ETV set has exactly these β-level sizes, but the ETV set itself has
(1, 4, 10, 20, 15). So there is no level-by-level bound \|B_j\| ≤ N₁(5, j+1), and by §5 not even the top-level
bound \|B₅\| ≤ 25 is available. The induction cannot be run on rank levels.

**8.2 The Pascal split statement PS(a,b).** Every FL(a,b)-configuration S is a disjoint union S₁ ⊔ S₂ with
S₁ ∈ FL(a−1,b) (no (a−1)-cap, no ((a−2)-cap, (b−1)-cup)-gon) and S₂ ∈ FL(a,b−1) (no (b−1)-cup, no
((a−1)-cap, (b−2)-cup)-gon). PS(a,b) for all smaller classes would give N₁(a,b) by induction; PS(6,6) with
Schroeder's M₇(5,6) = 25 alone would give N66 ≤ 50 (2.7). For a = 4, S₁ is a cup with at most b − 2 points,
the shape of Baek's ∆-removal. It is a symmetric (cap/cup) strengthening of the strong Δ-reduction of
ETVTHY20261113 §3 inside the first-layer classes (§8.4), and the only induction that matches the Pascal
recursion of the first-layer value.

**8.3 PS(5,5) is FALSE, also for real point sets (explicit 14-point sets, exact verification).**

*Complete search in the signotope model.* `tools/cegar_split.py`: (1) SAT for an FL(5,5)-signotope on n points
for which none of the partitions collected so far is a valid split; (2) find a valid split of it (`split.py`);
(3) add a clause saying that this partition is not a valid split (some 4-cap or (3,4)-gon inside S₁, or some
4-cup or (4,3)-gon inside S₂; auxiliary variables with the implication "variable ⇒ the chain is there" only).
UNSAT in (1) means that every FL(5,5)-signotope on n points has one of the collected partitions as a valid
split: if a signotope had none, setting each auxiliary variable to "the chain is there" would satisfy the CNF.

| n | 1–5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
|---|---|---|---|---|---|---|---|---|---|---|
| outcome | all split | all split | all split | all split | all split | all split | all split | all split | all split | **counterexamples** |
| partitions needed | ≤ 4 | 5 | 8 | 14 | 24 | 52 | 136 | 410 | 993 | – |
| status | CERTIFIED | CERTIFIED | CERTIFIED | CERTIFIED | CERTIFIED | CERTIFIED | CERTIFIED | COMPUTED | COMPUTED | brute force |

- n ≤ 11: the final CNF of each loop is **CERTIFIED** UNSAT (CaDiCaL 2.1.3 LRAT + cake_lpr,
  `data/cert_split.log`), and `tools/regen_split_cnf.py` rebuilds each CNF byte-identically from its list of
  partitions alone (`data/regen.log`, `data/split_partitions/`). n = 12, 13: UNSAT verdict of the
  incremental loop only; the CNFs are also rebuilt byte-identically, but their cake_lpr runs were stopped by
  the session memory guard (§10.1) and were not repeated.
- n = 14: the first abstract counterexample is `data/cex/split_counterexample_5_5_14.json`, a valid
  FL(5,5)-signotope none of whose 16,384 partitions is a strong split (`tools/verify_nosplit.py`: pure-Python
  brute force, no SAT solver). `tools/cegar_more.py` then listed **17,358 distinct** abstract counterexamples
  in 300 s without exhausting them (each with a brute-force count of 0 valid splits;
  `data/nosplit_all.jsonl.gz`). 40 of them, chosen at random, were re-verified from scratch by
  `verify_nosplit.py` (40 of 40).

*Which of them are point sets?* A random sample of 120 of the 17,358 (`data/nosplit_sample.jsonl`):
- **66 are PROVED non-realizable**: `tools/bfp.py` finds a bi-quadratic final polynomial. From the three-term
  Grassmann–Plücker relations [abc][ade] − [abd][ace] + [abe][acd] = 0 the sign pattern gives strict
  inequalities between products of two brackets; an integer combination with positive multipliers that
  cancels identically is a contradiction 0 > 0. The LP (HiGHS) only proposes the support; the multipliers
  are recomputed in exact rational arithmetic and the certificate is checked by a separate exact routine
  (241–258 inequalities per certificate; `data/nosplit_sample_bfp.jsonl`). A separately written checker,
  `tools/bfp_verify.py`, re-verified all stored certificates (66 of the sample and 4 of the first 12
  counterexamples; 71 records, one configuration is stored twice). Control: no certificate for 6 of 6 real order types; the self-test of `bfp.py` checks the
  identity and the inequalities on real points.
- **7 are realized by integer point sets** (`tools/realize_uncert.py`: annealing on wrongly oriented triples,
  2 attempts of 250,000 steps for each of the 54 configurations without certificate). The 7 real sets are in
  `data/cex/real_nosplit_5_5_14.jsonl`. Each was verified by `tools/verify_real_nosplit.py` (pure Python,
  integers only, no SAT solver, no C code): distinct x, no collinear triple, no 5-cap, no 5-cup, no
  (4,4)-gon, and **0 valid strong splits among all 16,384 partitions**; `tools/describe_real.py` repeats the
  count with separate code. One of them:

  (−3520165, −167974), (−972295, −164013), (−645607, 138116), (−225123, 1735740), (−108417, −343932),
  (−102960, 815076), (−69070, −5872830), (−2218, −143005), (7408, 724785), (12822, −147274),
  (1022170, −2053838), (1282213, 1939600), (1465729, −750589), (3951279, 4262718).

  They have |E| = 6, |A| = 6 or 8, |X| = 2 or 4.
- 47 remain undecided (no certificate, not realized).

So **every FL(5,5) set with at most 13 points has a strong split, and some 14-point sets (the extremal size)
have none.** The bound N₁(5,5) = 14 is true (§7.1) but it is not a consequence of a Pascal split.

**8.4 What survives.**
- *One-sided split* WS(a,b): S has a subset S₁ ∈ FL(a−1,b) that meets every (b−1)-cup. The same complete loop
  with the one-sided condition ends UNSAT for every n ≤ 14 (201, 412 and 740 partitions for n = 12, 13, 14;
  `data/logs/cegar55_weak.log`; CNFs rebuilt byte-identically, not certified). So WS(5,5) holds for every
  FL(5,5)-signotope, hence for every real FL(5,5) set (COMPUTED); the seven real counterexamples have between
  9 and 94 one-sided splits of the first kind and between 11 and 103 of the mirror kind. WS(6,6) with
  Schroeder would give only N66 ≤ 25 + 35 = 60.
- *a = 4:* PS(4,5) for every n ≤ 7 and PS(4,6) for every n ≤ 11 hold in the signotope model (COMPUTED,
  complete; `data/logs/cegar45.log`, `cegar46.log`), in line with Baek's ∆-removal. (5,5) is the first class
  where the split fails.
- *The Δ-reduction of ETVTHY20261113 §3 is not affected.* Its second part only has to be free of convex
  (n−1)-gons, it may contain (b−1)-cups. At (a, n) = (5, 6) the seven real sets above have between 131 and
  386 weak Δ-reductions (Δ free of 4-caps, the rest pentagon-free) and between 28 and 106 strong ones (Δ also
  pentagon-free), by brute force over all partitions with two independent pentagon enumerations
  (`tools/etvthy_check.py`, `data/logs/etvthy_check.log`). So the failure is specific to the symmetric
  cap/cup form. For the (6,6;8) class the Δ-reduction would read S = Δ ⊔ R with Δ ∈ FL(5,6) (≤ 25, Schroeder)
  and R heptagon-free with no 6-cap and no 6-cup; the ETV value of that second-layer class is 30, so the
  Δ-reduction together with "second layer ≤ 30" would give N66 ≤ 55 — but no bound near 30 is known for it.

**8.5 Tests that did not see the failure** (`tools/split.py`: all chains are enumerated, one SAT call; every
split found is re-checked by an independent DP on the two classes). They show how weak sampling evidence is
for statements of this kind, including PS(6,6):

| configurations | number | result |
|---|---|---|
| FL(5,5): the witnesses of all maximal realizable occupancy sets (n ≤ 14; 770 of them with 14 points, which have 9 to 109 valid splits, median 35) | 1,145 | all split |
| real FL(5,5) sets on 14 points: random walks, every new order type tested (`tools/real_nosplit_search.py`) | 8,501 order types | all split |
| real FL(5,5) sets on 14 points: annealing that minimizes the exact number of valid splits (`tools/real_nosplit_anneal.py`) | 3 long and 4 short runs | minimum 7 in each long run, never 0 |
| the first 12 abstract counterexamples, annealing on wrongly oriented triples (2 to 6 attempts of 300,000–400,000 steps) | 12 | none realized (4 of them are certified non-realizable) |
| FL(4,5) witnesses (n ≤ 7) | 13 | all split |
| real (6,6;8)-sets: 4 ETV images, 12 subsets of 64-point sets (five with 50 points), 15 annealed sets | 31 | all split; every 50-point set splits 25 + 25 |
| abstract (6,6;8)-configurations: \|E\| = 26 on 30 points (2), \|E\| = 30, 33, \|E ∪ A\| = 36, 40, \|X\| = 20 on 38–44 points, two 50-point configurations | 9 | all split (the 50-point ones 25 + 25) |
| abstract FL(5,6) configurations on 25 points (CaDiCaL with ten random unit clauses each, `tools/sample56.py`) | 60 | all split |

PS(6,6) itself is therefore **open, with no real support**: its tests are of the kind that failed to see the
(5,5) counterexamples, which exist only at the extremal size. The complete loop for FL(5,6) on 25 points was
tried once and stopped by its own memory limit (850 MB) after 87 partitions and 80 s, without a result
(`data/logs/cegar56.log`); in this form it does not fit the memory budget of §10.1.

**8.6 No canonical choice of S₁** (`tools/canon.py`). On the 1,145 FL(5,5) witnesses:
- S₁ = E (all ends of 4-cups): E ∈ FL(4,5) in 685 cases only, and (E, S ∖ E) is a strong split in 213;
- S₁ = the left-to-right greedy transversal of the 4-cups (v ∈ S₁ iff a 4-cup ends at v with its other points
  outside S₁): in FL(4,5) in 766 cases, strong split in 169.
For (6,6;8), E contains (4,5)-gons already in a real 40-point set (§5). ETVTHY20261113 §3.3 found the same
for a = 5: no pointwise rule in the ranks works.

**8.7 Assessment.** A human proof of N66 ≤ 50 does not look plausible, and no induction is available.
- The only induction that matches the Pascal recursion of the first-layer value is the split PS(a,b), and it
  is false for point sets already at (5,5;6), exactly at the extremal size.
- Baek's proof for a = 4 depends on the two-label dichotomy of 4-cap-free sets, which fails for a ≥ 5
  (ETVTHY20261113 §1); the base case M₇(5,6) = 25 has only a computer proof (Schroeder), and N₁(5,5) = 14 has
  the SAT certificate of §7.1.
- Counting on the catalog cannot replace an induction: there are no small rows (§6), no level-set
  capacities (§5), and the (5,5;6) bound already needs hundreds of circuits (§7.3).
- What remains is a direct computer proof in the signotope model, where the bound (unlike the split) may
  well hold: the 51-point instance for the value 50, or the **56-point instance for ES(8) ≤ 309**. Neither
  was within reach of one thread today (51 points undecided after 420 s; 50 points took 150 s to satisfy).
- The one-sided split is the only structural statement of this kind that survived a complete test; it is
  too weak for ES(8) (60 instead of 55).

## 9. Deliverable summary

- **Proved capacity rows beyond the cycle rows: none.** With the 50 cycle rows the exact hole minimum is 6
  (N66 ≤ 64; COMPUTED, CP-SAT OPTIMAL, reproduced by `tools/rank.py`).
- **Proved but not cutting:** the junction coupling of in- and out-states (2.1; no cut, §5); the structure
  lemmas 2.2–2.4 (they reproduce the catalog counts).
- **Proved descriptions:** the composition formulas and the three hole patterns H₁, H₂, H₃ of all one-step
  compositions (2.5, checked on 8 + 4 + 5 real 50-point sets); the small-witness principle (2.6).
- **Refuted candidates:** §5 (real sets in `data/cex/`, abstract configurations in `data/samples_*.jsonl`).
- **Conditional statements:** |E ∪ A| ≤ 35 ⇒ N66 ≤ 55 (false in the signotope model); PS(6,6) + Schroeder ⇒
  N66 ≤ 50 (PS(6,6) open; PS(5,5) is false for real point sets, §8.3).
- **Human proof of 50:** not plausible; the natural induction is false at (5,5;6) (§8.7).
- **Certified side results:** N₁(5,5) = 14 (§7.1); the Pascal split for all abstract FL(5,5) configurations
  with at most 11 points (§8.3); control instances of Baek's theorem for n = 5, 6, 7 (§7.1).
- **Exactly verified side results:** real 14-point FL(5,5) sets without a Pascal split (§8.3); bi-quadratic
  non-realizability certificates for 66 abstract configurations (§8.3).

## 10. Files

Record `tools/` (all scripts; run from W, or from a copy of `tools/` with `libesgeo.so` built by
`gcc -O2 -shared -fPIC -o libesgeo.so esgeo.c` and the Python of
`/home/jay/research/data/six10-linux-20261105/venv.disk`):
- geometry and states: `esgeo.c`, `esgeo.py` (from ETVTHY20261113), `etv_common.py` (from ETV5N20261113; use
  ETV_A=4, ETV_B=4), `fl.py`, `fast.py`, `etvcon.py` (from ETVTHY20261113);
- data: `gen66.py`, `gen2.py`, `gen4.py`, `sub64.py`, `compose.py`, `anneal_ab.py`, `an1.py`–`an3.py`,
  `holes50.py`, `lemma_check.py`;
- catalog experiments: `rank.py`, `hall.py`;
- abstract model: `wit.py`, `wit_control.py`, `rows_small.py`, `witg.py`, `scan3.py`, `scan4.py`,
  `crosscheck4.py`, `fls.py`, `toplevel.py`, `small_table.py`, `circuits.py`, `sample_fl.py`, `sample56.py`,
  `cert.py`, `cert_cnf.py`;
- splits: `split.py`, `canon.py`, `cegar_split.py`, `cegar_more.py`, `regen_split_cnf.py`, `verify_nosplit.py`,
  `verify_nosplit_many.py`, `weak_split.py`, `splitcount.py`, `describe_cex.py`, `real_nosplit_search.py`,
  `real_nosplit_anneal.py`, `verify_real_nosplit.py`, `describe_real.py`, `etvthy_check.py`;
- realizability: `bfp.py`, `bfp_verify.py` (non-realizability certificates), `realize_small.py`,
  `realize_uncert.py`, `realize_control.py`, `nosplit_real.py` (annealing on wrongly oriented triples; used),
  `realize_lp.py` (x by annealing, y by an LP; weaker here: 5 of 6 control order types, 1 of the 7 realizable
  no-split configurations), `realize.py`, `realize_samples.py` (alternating LPs; failed on the 30-point
  configurations, kept for the record);
- `run_*.sh`: the unit scripts as run; `assemble.py`: builds this record's `tools/`, `data/`, `SHA256SUMS`.

Record `data/` (4 MB; SHA-256 of every file of `tools/` and `data/` in `SHA256SUMS`): the files referred to in
the text. `data/cex/` holds the counterexamples (real sets: `E_31_n35.json`, `X_19_n29.json`,
`E_has_45_gon_n40.json`, `real_nosplit_5_5_14.jsonl`; abstract: `split_counterexample_5_5_14.json`;
`nosplit_best_*.json` are the best real sets of the directed search, with 7 or more valid splits);
`data/split_partitions/` the partition lists of the complete split loops; `data/logs/` the unit logs and the
three notes of the memory guard.

Work directory W: everything above plus the occupancy masks of the annealing runs (`masks_*.json`), the
CNFs of the certified instances (`cert/*.cnf`; all LRAT files were deleted after cake_lpr's verdict) and
temporary files.

### 10.1 Memory policy and stopped jobs

From 18:25 KST the session memory policy (`/home/jay/research/data/memguard-20261113/MEMORY_POLICY.txt`) gives
this track 2 GB (resident memory + swap over all its units). Three units were stopped by the session guard,
all at the same step: cake_lpr on the proof of the 12-point split CNF of §8.3 (LRAT 85 MB) reached 2.0–2.2 GB.
- `nov13c-d2-ns5` (18:32:47, 2,201 MB) and `nov13c-d2-ns6` (18:42:23, 2,069 MB): launched before the policy
  had been read; the stops looked like unexplained terminations, and the second launch was the same batch
  in another order.
- `nov13c-d2-c12` (18:45:20, 2,025 MB): a retry with CML_HEAP_SIZE=1300 in the environment, which did not
  reduce the checker's memory.
What was changed: no further cake_lpr run on that proof or on the 13-point one (both statements stay
COMPUTED, §8.3); every later unit was started with MemoryMax ≤ 1.5 GB and MemorySwapMax=0 and ran small jobs
(searches and loops on at most 25 points); the long attempt on the 26-point (5,6) instance was dropped,
because the cake_lpr check of a multi-GB proof cannot fit the budget (the 6-minute attempt before the policy
had 1.1 GB of solver memory and a 1 GB LRAT). Before 18:25 the largest unit peak was 1.7 GB (the 51-point
probe).

## 11. Next steps and resumable state

1. **For the row tracks.** High-demand structural rows for the 70-state catalog are not available: there
   is no level-set capacity (§5), and in the signotope model no row with fewer than five states (§6). What
   this track can offer instead:
   - *attainment*: by 2.6 the owners of a support T keep their exact states once their witnesses are added.
     A coupled CNF may therefore add up to nmax(T) − |T| free points and require the exact states of the
     owners (`wit.py` does this with point-indexed variables); in a whole-catalog model the clause is
     "an occupied state has every corner attained by a pair whose first point is an owner";
   - *state separation* is implied in point-indexed models and may be added as clauses (`cert.py`, mode `inj`);
   - *conditional rows* "the states of T are occupied and the states of H′ are holes" are the natural output
     of such a model once most states are holes; they are still clauses for the hole-vector problem.
2. **The direct instance.** A (6,6;8)-signotope on 56 points does not exist ⇒ N66 ≤ 55 ⇒ ES(8) ≤ 309 with
   no residual rows. `fls.py` / `cert.py` write the instance (about 4–5 million clauses). It needs
   cube-and-conquer and a proof check that respects the memory policy (cube by cube). Calibration with these
   encoders, one thread: Baek's 23-point instance undecided in 400 s (`plain`), the 26-point (5,6) instance
   undecided in 6 minutes (`inj`), the 51-point (6,6) instance undecided in 420 s; 50 points satisfiable in
   150 s.
3. **Pascal split.** Settled negatively for (5,5;6) (§8.3). Open: PS(5,6) and PS(6,6); a lift of the 14-point
   counterexamples to these classes; how many of the 17,358+ abstract counterexamples are point sets (the
   sample has 66 non-realizable, 7 realizable, 47 undecided of 120).
4. **One-sided split.** WS holds for every abstract FL(5,5) configuration; WS(6,6) would give N66 ≤ 60.
   Test it on (6,6;8) configurations (`split.py`, `weak=True`) and look for a canonical S₁.
5. **Independent certificate of M₇(5,6) = 25.** `cert.py 5 6 26 inj` (4.1 MB CNF) needs cubes and a
   memory-bounded checker; not attempted beyond 6 minutes.
   *Final state (phase 2).*
   - This track's CNF is `W/cert/fl_5_6_26_inj.cnf` (4,099,130 bytes, 17:49), with no verdict.
   - No log, no LRAT and no `certified.jsonl` line of the 6-minute attempt survive in W, so nothing was
     left to check.
   - The same statement, FL(5,6) at 26 points, i.e. no 5-cap, no 6-cup and no (4,5)-gon (the only convex
     heptagon in such a set), was CERTIFIED the same afternoon in ETV7SAT20261113 §5.1:
     - owner-model CNF `owner_v1.py 3 4 7 26`, SHA-256
       `9646633ed38cbcc8740ae4aff903b832b8ab478e50cc2bc4f04523bae988167f`;
     - CaDiCaL 59 s; LRAT 321,528,931 bytes, SHA-256
       `642b46600f29c87019f8d054623c94cc09afa52ce643b51265637f7a569bdef6`;
     - cake_lpr `s VERIFIED UNSAT` in 9 s;
     - the same holds in the colouring model there;
     - like this record, it rests on a written soundness argument (ETV7SAT §2).
   - So the conditional statements of 2.7, 8.2 and 8.4 that use M₇(5,6) = 25 can now cite a project
     certificate as well as Schroeder's unrefereed proof. A certificate in this record's encoder would only
     cross-check the two encoders.
6. **A real counterexample to |E ∪ A| ≤ 35** is missing (abstract ones exist; the largest real value found is
   31 as of 19:30, and 32 at the end, see below). Since 2.7 would turn this statement into ES(8) ≤ 309,
   it is the one level-set statement still worth a real refutation or a second look.
   *Final state (phase 2).* The last annealing run raised the largest real value to **32**.
   - Run: `run_ns17.sh`, unit `nov13c-d2-ns17`, 19:31–19:38, seeded with the best |E| set; log `W/ns17.log`.
   - The set: line 4 of `W/sets_pEuA.jsonl` (seed 72), not in `data/`. A real (6,6;8)-set with n = 36,
     |E| = 21, |A| = 21, |X| = 10, |E ∪ A| = 32 (so |Z| = 4).
   - Checks: by the C routine during the run, and again in phase 2 by `tools/verify_levels.py` (pure Python,
     integers only), which confirmed validity and all four counts.
   - The same run's |E| leg stayed at |E| = 31 on 35 points.

   The 36 points, sorted by x. Python's `json.dumps` of this list of [x, y] pairs, with its default
   separators, has SHA-256 `b2f2e160a1e7069793bb46c0ae206a0c054c47c43b7650914dfbff7e07e1c300`; that is the
   `P` field of the jsonl line:

       (-24390462, -15364407), (-7194786, -3245934), (-4676014, -1169611), (-3914075, -493980),
       (-2273462, 4264396), (-1794272, 2874550), (-1357112, 2191252), (-1282540, 1911118),
       (-1260407, -1176110), (-1111891, -931520), (-835906, -626417), (-824337, -651210),
       (-809067, -712493), (-742436, -246850), (-731018, 1546678), (-729071, -283744),
       (-723194, 2116692), (-714318, -337736), (-710411, 154004), (-691671, 177946),
       (-622704, -157060), (-268967, 904428), (-211714, 832058), (-151431, -1025523),
       (-146651, -924487), (-142425, -955994), (-63395, -1463398), (-60862, -1284382),
       (-11108, -259094), (-2545, -288009), (27835, -352892), (479224, 682581),
       (494801, 512087), (511797, 449454), (658057, 234274), (1219173, -440182)

   It is still 4 short of a counterexample (36 needed), and the gain from 31 to 32 came from one more seeded
   run of 1.5 M steps. This says nothing either way about |E ∪ A| ≤ 35 for real sets.

**Resumable state.** All units `nov13c-d2-*` are stopped; nothing is committed; no file outside this record
and W was created or changed. W holds all scripts, logs, pools, the SAT witnesses (`singles.jsonl`,
`pairs.jsonl`, `samples_*.jsonl`, `maximal_*.json`), the certified CNFs (`cert/`) and the partition lists of
the split loops. Every experiment is re-run by the command line given in the head of its script; the unit
scripts `run_*.sh` show the exact invocations.

## 12. Literature (from NOVELTY20261113B §§3, 6, 10; added in phase 2)

NOVELTY20261113B is the session's literature check. Its points that concern this record (claims C4, C5
and C8 there):

- **The Pascal split PS(a, b) of §8.2 is public** (NOVELTY §10).
  - It is the statement L1(a, b) of gotrevor/es7-ladder (`docs/HUMAN-P756.md`, 5–7 Oct 2026, unrefereed)
    and the first-diagonal case of GLitchfield's PASCAL-SPLIT (notes of 2–4 Oct 2026, unproved). Cite both.
  - gotrevor reports L1(5, 6) false for abstract 2-colourings (49 colourings on 23–25 vertices), with no
    failure on 40 signotope samples. So PS(5, 6) cannot be proved from path and colouring axioms alone. For
    signotopes and point sets it is open; §8.5 found no failure on 60 abstract FL(5,6) configurations.
  - Other first-layer strategies in gotrevor's note: a three-part split L2(5, 6) (unrefuted), and hole
    injection through Baek's α-statistic ("Step 3 fails at a = 5"). NOVELTY found no others besides Baek's
    Conjecture 5 for a = 4.
- **PS(5, 5) and PASCAL-SPLIT.** NOVELTY was not asked about PS(5, 5). It did not examine whether the
  14-point sets of §8.3 bear on PASCAL-SPLIT as tested in that repository.
  - Phase-2 reading of the wording quoted in NOVELTY §6 (C5): "A has no a-cap, no (u−1)-cup and no
    (k−1)-gon; E has no (a−1)-cap, no u-cup and no (k−1)-gon". At (a, u, k) = (5, 5, 6), A and E are the
    classes FL(5, 4) and FL(4, 5) of §8.2: in a set with no 4-cap and no 5-cup the only convex pentagons are
    (3,4)-gons, and the mirror holds.
  - So the seven real 14-point sets of §8.3 look like counterexamples to that case of PASCAL-SPLIT for real
    point sets.
  - The repository reports PASCAL-SPLIT exhaustive for all signotopes up to 8 points and "never failed, even
    on general signotopes". It reports a stronger "peel" variant false at 14 and 11 points in (5, 5, 6).
    Neither contradicts §8.3, where every FL(5,5) signotope with at most 13 points splits.
  - This is a reading of quoted text only, not checked against the repository's own definitions. Compare
    the definitions before stating it anywhere.
- **The first-layer formula of §1 is public** (C8): N₁(a, b) = C(a+b−4, a−2) − C(a+b−6, a−3).
  - Explicit in gotrevor's note, as Lean lemma `d1N_add_holes`: an identity for the conjectured value, not
    a proof that the value holds.
  - Implicit in Baek–Balko's Lemma 9.
  - The same expression appears for other quantities in Mojarrad–Vlachos, Theorem 3.6, and in Schroeder's
    Proposition 7.4.
  - Balko–Valtr (EuroComb 2015) call k = a + u − 4 "this first nontrivial case". Their colourings
    (N^(5,6,7) ≥ 26, N^(6,6,7) ≥ 31) show that the abstract colouring analogue fails on the first layer,
    which agrees with this record's use of the signotope model.
- **Bounds on N66 = N(8; 6, 6)** (C8: "no prior art found; 'partially anticipated' stands").
  - The literature has only the cup–cap bound 70 and the lower bound 50. No bound below 70 for general point
    sets was found, so this record's baseline N66 ≤ 64 (COMPUTED) is not in the literature (bounded search).
  - Baek–Balko's Theorem 8 makes 50 exact for (6, 6, 8) on decomposable sets. NOVELTY §6 C3 notes that its
    proof is omitted in the SoCG version and that GLitchfield's notes assert a gap in it (their claim, not
    verified). This bears on the observation of §4 that every real 50-point set found is decomposable
    (ETV-type).
  - Their Theorems 4 and 6 give the forcing number 51 for split 8-gons.
  - Schroeder's Lemma 5.3 splits his balanced heptagon part into a 5-cap-free and a 5-cup-free part, each
    at most 25 by his Theorem 5.2. Phase-2 remark: the Pascal split of 2.7 bounds the same two classes by
    25 each, in another setting.
- **N₁(5, 5) = 14 (§7.1) is known.**
  - For point sets, all ETV cases with n ≤ 6 follow from ES(6) = 17 and Baek's Theorem 1.5. NOVELTY §6 C4
    marks this as an inference, not a printed sentence.
  - MathOverflow question 277192 (2017) has computed values that match the first-layer ETV values for
    n ≤ 6, "for example 14 for 5-cap, 5-cup, (4,4)-hexagon".
  - Balko–Valtr verified the abstract statement for k = 6, for all a and u except a = u = k.

  The certificate of §7.1 is a re-derivation in the signotope model. Its "we did not search the
  literature for this case" is answered by these points.
- **M₇(5, 6) = 25 (§7.1, §11)** (C4). Schroeder, Theorem 5.2 (Lean with native evaluation; unrefereed). Then
  gotrevor (SAT, 82 CPU h, no proof log). Now also ETV7SAT20261113 §5.1, with a cake_lpr-checked certificate.

## 13. Phase-2 completion (13 November, 20:20–20:48 KST)

Done by a phase-2 agent (unit prefix `nov13c-e7`, 1 thread, 2 GB; it could edit only this README).
- **Read.** Every file in W newer than the README of 19:30: `run_ns17.sh`, `ns17.log`, `sets_pE.jsonl`,
  `sets_pEuA.jsonl`, `init_Ebest2.json`, `masks_pE_71.json`, `masks_pEuA_72.json`. Also `cert/` and all
  queue scripts and logs, searched for the 26-point (5,6) attempt: there is no trace of it besides the CNF.
- **Checked.** The seed-72 set of `sets_pEuA.jsonl`, by `tools/verify_levels.py` (pure Python, integers;
  about 0.01 s): valid (6,6;8)-set, n = 36, |E| = 21, |A| = 21, |X| = 10, |E ∪ A| = 32.
- **Pending proof checks.** No LRAT file is left in W, so there was nothing to check. The cake_lpr checks of
  the 12- and 13-point split CNFs of §8.3 stay undone; their proofs were deleted, and those statements
  remain COMPUTED.
- **Nothing else.** No unit was started for this record. No file was deleted. `data/`, `tools/` and
  `SHA256SUMS` are unchanged; they show the state of 19:29.
- **Context** (other records, read at about 20:35 KST, not re-checked here):
  - N66N20261113 reports N66 ≤ 59 CERTIFIED; N66 ≤ 58 is COMPUTED there, with its certification running.
  - LO33N20261113 shows N66 ≤ 56 ⇒ ES(8) ≤ 309 by exact trees.

  So "N66 ≤ 55 would give ES(8) ≤ 309" (§1, 2.7) is still true but no longer the sharpest threshold.
  "N66 ≤ 64" in §0 is the baseline this track started from.
