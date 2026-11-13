# ETVTHY20261113: theory track for M(5; 8) (13 November 2026, 06:40–10:25 KST)

M(5; 8) is the largest size of a planar set in general position with distinct x-coordinates, no 5-cap and
no convex octagon (Baek's N(8, 5, 8)). Known before this record: 42 ≤ M(5; 8) ≤ 71 (ETV construction;
internal omission, THEORY310N20261113 §4 L5). Cup–cap gives 84.

**No bound below 71 is proved here.** The main outputs are:

1. **The Δ-reduction conjecture** (§3, OPEN): every 5-cap-free octagon-free set S has a 4-cap-free subset Δ
   that meets every convex heptagon of S.
   - **Consequences.** With Baek's theorem and Schroeder's M₇(5,6) = 25 it gives **M(5; 8) ≤ 22 + 41 = 63**.
     With its level-7 analogue as well, **M(5; 8) ≤ 22 + 16 + 16 = 54**. That is below the capacities 57 and 56,
     which THEORY310N §3 certifies to give ES(8) ≤ 309 and ≤ 308.
   - **Strong form** (Δ also heptagon-free): this is the Erdős–Tuza–Valtr recursion
     M(5; n) ≤ M(4; n−1) + M(5; n−1). At every level it would give the ETV value 42.
   - **Evidence.** No violation was found.
     - 314 octagon-free real sets. A strong Δ was certified for each by an independent pure-Python check:
       - the ETV 42-point set, random and targeted sets (194, `data/conj8_certs.jsonl`);
       - greedy 5-cap-free subsets of 120 of the 64-point octagon-free sets, 69 of them with 42 points
         (`data/conj8_sub64_certs.jsonl`).
     - 121 heptagon-free sets at level 7 (`data/conj7_certs.jsonl`).
     - 31 random signotopes with 32–42 elements (`data/abstract_conj.log`). A 43-element sample (SAT for a signotope
       beating ETV's 42) was stopped unsolved after about 13 minutes.
     - Adversarial random walks with an exact test at every step: 570,485 octagon-free sets in all, mostly of
       16–30 points
       (§3.4, §8).
   - This is the natural extension of Baek's ∆-removal induction (lead 1). No pointwise rule produces Δ (§3.3).
   - Refinement: in all 187 sets tried, Δ could be taken inside Δ_R ∪ Δ_L, the rank-defined possible endpoints
     (§3.2).
2. **PROVED small results** (§2):
   - M(5; 7) ≤ 41 (Baek plus Schroeder; ETV value 26, cup–cap 56);
   - M(5; 8) ≤ 22 + N(8, 5, 7) (lead 2);
   - |S| ≤ 44 − |Z| + |M| for the natural cover by {c₋ ≤ 3}, {c₊ ≤ 3} and M, where M has no 6-cup;
   - a heptagon trichotomy (2.6): every heptagon ends in Q, starts in Q', or is a doubly hard (4,5)-gon nested
     under a 7-cup chord;
   - the identities linking the 84-state catalog to cap and cup ranks.
3. **LP sensitivity** (§4): which single capacity statement would push the omission bound below 71.
   - R7 ≤ 20 gives 70, and **R7 = 20 is attained**, so it would be sharp.
   - R6 ≤ 35, N(8,5,7) ≤ 48, R4 ≤ 48 and |Δ_R| ≤ 44 each give 70.
4. **Side observation (§3.5, OPEN).**
   - All 1,235 known 64-point octagon-free sets split into two 32-point heptagon-free sets.
   - So do 240 random gon-free sets at n = 8, 7, 6.
   - In general the split would give ES(8) ≤ 2·80 + 1 = 161, but already its n = 7 case is the open ES(7) = 33.
5. **REFUTED** (§5): fourteen natural lemmas or routes. The point sets are in `cex/`; each was re-verified by an
   independent pure-Python exact checker (`tools/verify_cex.py`, log `data/verify_cex.log`).

Notation (S is 5-cap-free and octagon-free; all ranks are computed in S):
- β(p) = longest cup ending at p, ω(p) = longest cup starting at p;
- c₋(p) = longest cap ending at p, c₊(p) = longest cap starting at p;
- B_k = {β = k} is the k-th β-level; R7 = B₇ (ends of 7-cups), R6 = B₆ ∪ B₇;
- Q = {c₊ ≤ 3}, Q' = {c₋ ≤ 3}, L4 = S∖Q (starts of 4-caps), R4 = S∖Q' (ends of 4-caps);
- M = L4 ∩ R4, Z = Q ∩ Q';
- T = S∖R7 (no 7-cup);
- N(8, 5, 7) = largest set with no 5-cap, no 7-cup and no convex octagon (ETV value 41).

f = (f₁, f₂, f₃) is the incoming state of the 84-state catalog (`theory310-20261113/cap5_omission.py`).

Work directory: `/home/jay/research/data/etvthy-20261113/` (W). Tools are copied to `tools/`, small data to `data/`.
All computations ran in systemd user units at one core each, at most two at a time. Nothing is committed.

## 1. Lead 1: Baek's proof and why it does not extend directly

Baek (arXiv:2206.04260v2) works in the configuration model: a 2-colouring of ordered triples, with weak gons.
- Slope labels s(e) = (longest cap starting with e) − 1 lie in {1, 2}.
- The (α, β)-statistic is injective into T₄,ₙ.
- Two interweaved laced (n−1)-cups give a (3, n−1)-gon (Lemma 5.2).
- Theorem 5.10 proves that C(n−1,2)+2 points contain such a pair. The induction removes ∆ = {leftmost point of
  rows 1..n−2}, so that S∖∆ is (n−1)-cup-free.

For a = 5 the labels are {1, 2, 3}.
- Label 1 extends cups to the left (for p q with s = 1 and any cup C starting at q, pC is a cup), and label 3
  extends cups to the right.
- **The middle label 2 does neither.** Every WLOG step of Baek's proof ("by mirror symmetry the label is 1")
  fails for it. The mirror maps 1 ↔ 3 and fixes 2.
- Concretely, Baek's Lemma 5.6 (left ends of (n−1)-cups precede right ends) fails for a = 5. In
  `cex/L7_R7_interleave.json` (33 points) a 7-cup starts to the right of the end of another 7-cup.
- Two interweaved 7-cups C₁ (p→r) and C₂ (q→s) force pqr cup, qrs cup, (p,q,q₂) cap and (r′,r,s) cap. We
  found no way to reach an octagon without a lacing condition, and Baek's lacing step uses the two-label
  symmetry.

What does generalize is the *shape* of Baek's induction: remove a small structured set and drop one polygon
size. §3 states the a = 5 version and tests it.
- For a = 4, the strong form says that every 4-cap-free n-gon-free set contains a cup Δ with at most n−2 points
  meeting every convex (n−1)-gon. It implies Baek's theorem by induction.
- It held in 24 of 24 random 4-cap-free octagon-free sets of 18–21 points (`tools/delta_strong_a.py`).

## 2. PROVED statements

**2.1 (lead 2).** R7 ⊆ Q, so R7 is 4-cap-free. Hence |R7| + |Q∖R7| ≤ 22 and M(5; 8) ≤ 22 + N(8, 5, 7).

*Proof.* Let c₁…c₆p be a 7-cup and p x y z a 4-cap. If (c₆, p, x) is a cup, c₁…c₆px is an 8-cup. Otherwise
c₆pxyz is a 5-cap. Q is 4-cap-free (a 4-cap inside Q starts at a point with c₊ = 4) and octagon-free, so Baek
gives |Q| ≤ 22. S∖R7 has no 7-cup. ∎

**2.2 (helpers).**
- If p ∈ L4 with a 4-cap p d e f, then (o, p, d) is a cup for every o < p (else o p d e f is a 5-cap). So
  every cup ending at p extends by d.
- Mirror: if p ∈ R4 with a 4-cap a b c p, then (c, p, q) is a cup for every q > p.
- Consequences:
  - L4 and R4 contain no 7-cup; β ≤ 6 on L4 and ω ≤ 6 on R4;
  - **M = L4 ∩ R4 contains no 6-cup**, because a cup in M extends at both ends;
  - every 4-cap of S starts in L4 and ends in R4.

**2.3 (natural 4-cap-free cover).** |S| ≤ |Q| + |Q'| − |Z| + |M| ≤ 44 − |Z| + |M|, since S = Q ∪ Q' ∪ M.
- Also |M| ≤ C(7,3) = 35 (no 5-cap, no 6-cup).
- So any bound |M| − |Z| ≤ 26 would give M(5; 8) ≤ 70.
- The largest value observed is |M| − |Z| = 19 (with |M| = 25 and |Z| = 6; §6).
- "M is heptagon-free" would give |M| ≤ 25 by Schroeder and hence 69, but it is **refuted** (§5).

**2.4 (M(5; 7) ≤ 41).** Let S′ be 5-cap-free and heptagon-free, and R6′ the ends of 6-cups of S′.
- A 4-cap starting at the end of a 6-cup gives a 7-cup (a heptagon) or a 5-cap. So R6′ is 4-cap-free and
  heptagon-free, and |R6′| ≤ C(6,2)+1 = 16 (Baek, n = 7).
- S′∖R6′ has no 6-cup, no 5-cap and no heptagon, so |S′∖R6′| ≤ 25 by Schroeder's Theorem 5.2 (M₇(5,6) = 25,
  computer-certified, unrefereed).
- Hence M(5; 7) ≤ 41. ETV says 26; cup–cap gives 56. ∎

The same split for octagons is 2.1. There the second piece is N(8, 5, 7), which is not known.

**2.5 (catalog identities).** For every point v except the leftmost:
- β(v) = f₁(v) + 1 and c₋(v) = 2 + [f₂(v) ≥ 1] + [f₃(v) ≥ 1].
- So the class {β = k, c₋ = 2} has 1 state, {β = k, c₋ = 3} has k−1 states and {β = k, c₋ = 4} has C(k,2)
  states.

These were checked on 187 sets, with the f-states injective in all of them.
- Every right endpoint v of a convex heptagon has c₋(v) + β(v) ≥ 9.
- So Δ_R := {c₋ + β ≥ 9} = {f₁ + [f₂≥1] + [f₃≥1] ≥ 6} (58 states) meets every heptagon.
- Its complement (26 states) is heptagon-free, so |S| ≤ 26 + |Δ_R|.
- In Baek's α-coordinates, Δ_R ⊆ {φ ≥ 7}, where φ = α₃ + [α₁ ≥ 2] + [α₂ ≥ 2]. In the ETV set, Δ_R is exactly
  {φ = 7} (16 points: the top row of each block).

**2.6 (heptagon trichotomy).** Every convex heptagon H = (cap K, cup D) of S, from u to v, falls into one of three
cases.
- (i) Its right end v starts no 4-cap (v ∈ Q).
- (ii) Its left end u ends no 4-cap (u ∈ Q').
- (iii) It is **doubly hard**: a (4,5)-gon u k₁ k₂ v + D with u ∈ R4 and v ∈ L4, whose cup extends at both ends
  to a 7-cup c_u D d_v (c_u, d_v the helpers of 2.2). Then:
  - H lies below the chord c_u d_v;
  - (k₁, k₂, d_v) and (c_u, k₁, k₂) are cups;
  - the 7-cup ends in R7 ⊆ Q and starts in L7 ⊆ Q'.

*Proof.* If v ∈ L4 and u ∈ R4, the cup D extends at both ends (2.2). So |D| + 2 ≤ 7, which forces |D| = 5 and
|K| = 4. The chord lemma (a 7-cup from x to y leaves no point above the chord xy between them, else a (3,7)-gon)
puts K below c_u d_v. If (k₁, k₂, d_v) were a cap, u k₁ k₂ d_v and the 6-cup D d_v would form a (4,6)-gon. The
case (c_u, k₁, k₂) is the mirror. ∎

*Consequence.* If every heptagon of S is of type (i), then Δ = {right ends of heptagons} ⊆ Q is 4-cap-free and
meets every heptagon, so weak Conj(8) holds for S; the mirror holds for type (ii). In 57 (resp. 63) of the 169 test sets, Δ_R ∩ Q
(resp. Δ_L ∩ Q') already meets every heptagon. A counterexample needs heptagons outside (i) and outside (ii). Even without type (iii), the union
of the two endpoint sets can contain 4-caps (§3.3).

**2.7 (exact ETV sets).** The ES/ETV block construction is built exactly (`tools/etvcon.py`):
- blocks T_i (caps ≤ i+1, cups ≤ n−1−i, C(n−2,i) points) are made steep and placed on a macro-cap;
- `data/etv858.json` has 42 points, largest polygon 7, caps ≤ 4, cups ≤ 7, 9,721 4-caps;
- `etv857.json` (41 points) and `etv757.json` (26 points) are the analogous sets;
- all were checked with the independent pure-Python checker.

## 3. The Δ-reduction conjecture (OPEN, strong evidence)

**Conj(n), weak form.** Every 5-cap-free set with no convex n-gon has a 4-cap-free subset Δ meeting every
convex (n−1)-gon.

**Conj(n), strong form.** The same, with Δ also free of convex (n−1)-gons.

**Equivalent phrasing.** S is the union of a 4-cap-free set and a heptagon-free set; in the strong form, the
first set is also heptagon-free.

The general (a, n) version: every set with no a-cap and no n-gon is the union of an (a−1)-cap-free set and an
(n−1)-gon-free set.
- In the strong form for all (a, n) it would give N(n,a,n) ≤ N(n−1,a−1,n−1) + N(n−1,a,n−1). That is the Pascal
  recursion of the ETV sum, so it would imply the full ETV conjecture, and with it Erdős–Szekeres. So only special
  cases can be expected to be easy.
- For a = 4 the strong form says the first set can be a cup with at most n−2 points. It implies Baek's theorem by
  induction; the converse is not clear.
- The strong form held for every random set tested at (a, n) = (5,6), (4,7), (6,7) and (6,8): 360 sets (§3.2).
- We did not search the literature for this formulation.

### 3.1 Consequences (PROVED implications)

- **Weak Conj(8):** Δ is 4-cap-free and octagon-free, so |Δ| ≤ 22, and S∖Δ is heptagon-free. Hence
  M(5; 8) ≤ 22 + M(5; 7) ≤ 22 + 41 = **63** by 2.4.
- **Weak Conj(8) and weak Conj(7):** M(5; 7) ≤ 16 + M(5; 6) ≤ 16 + 16 = 32, using ES(6) = 17
  (Szekeres–Peters). So M(5; 8) ≤ **54**. By the exact trees of THEORY310N20261113 §3, capacity 57 gives
  ES(8) ≤ 309 and capacity 56 gives ES(8) ≤ 308, so 54 would give ES(8) ≤ 308.
- **Strong Conj(n) for n = 5..8:** M(5; n) ≤ M(4; n−1) + M(5; n−1), giving 8, 15, 26, 42. These are exactly
  the ETV values.
  - This is the Pascal identity ETV(n,5,n) = ETV(n−1,5,n−1) + ETV(n−1,4,n−1).
  - The ETV construction realizes it: the removed set is the top row of each block.
  - So the strong form for n ≤ 8 implies the ETV values for a = 5 up to n = 8; the converse is not claimed. The
    weak form is much weaker, but still decisive.

### 3.2 Evidence

Exact checks were done with CP-SAT and lazy constraints. Every returned Δ was re-checked by the exact C checker:
4-cap-free, and S∖Δ (plus Δ itself for the strong form) without a convex heptagon.

| test | sets | result |
|---|---|---|
| **certificates**: strong Δ for every octagon-free test set (ETV, pool, all targeted searches), re-verified by `pyexact` (`data/conj8_certs.jsonl`; each record lists Δ) | 194 | 194 OK; \|Δ\| ≤ 16 |
| **certificates** for 5-cap-free subsets (greedy, n = 26–42) of 120 of the 1,234 known 64-point octagon-free sets (`tools/sub5cap.py`, `data/conj8_sub64_certs.jsonl`) | 120 | 120 OK (69 sets of 42 points) |
| **certificates** at level 7 (`data/conj7_certs.jsonl`) | 121 | 121 OK; \|Δ\| ≤ 11 |
| weak Conj(8), random pool (`gen_random.py`, four distributions, n = 28–37) | 120 | 120 OK |
| weak Conj(8), targeted extremes (sets maximizing R7, R6, L4, M, Y, size) | 48 | 48 OK |
| strong Conj(8): ETV(8,5,8) (Δ of size 16) + pool + targeted | 169 | 169 OK |
| weak and strong Conj(7): ETV(7,5,7) + 120 random heptagon-free sets (n = 22–26) | 121 | 121 OK (both) |
| strong a = 4 analogue at n = 8 (Δ a cup, heptagon-free) | 24 | 24 OK |
| **general (a, n), strong form** on random sets: (5,6) n = 14–15; (4,7) n = 14–16, including Baek-extremal 16-point sets; (6,7) n = 22–30; (6,8) n = 31–38 (`tools/run_general.sh`, `data/general_decomp.log`) | 4 × 90 | 360 OK |
| refined: Δ ⊆ Δ_R ∪ Δ_L, weak form (Δ_L = {c₊ + ω ≥ 9}, the possible left endpoints) | 121 + 66 | 187 OK |
| refined: Δ ⊆ Δ_R ∪ Δ_L, strong form | 121 | 121 OK |
| Δ ⊆ Δ_R alone / Δ ⊆ (Δ_R ∩ Q) ∪ (Δ_L ∩ Q′) | 121 | fails in 15 / 12 |
| random signotopes (SAT samples of the abstract relaxation: no 5-cap, no weak octagon), weak and strong Conj(8), `tools/abstract_conj.py` | 31 (n = 32–42) | 31 OK (two strong cases needed more lazy rounds, `abstract_recheck.py`) |
| adversarial random walks (§3.4) | see §3.4 | see §3.4 |

So the refined statement is: **Δ_R ∪ Δ_L contains a 4-cap-free subset that meets every heptagon** (and, strongly, is
heptagon-free). Δ_R and Δ_L are defined by ranks alone, so this localizes the search for a proof.

### 3.3 Why it is not proved: no canonical Δ

All of the following are exact computations over the 169 octagon-free test sets.
- Δ_R is 4-cap-free in only 12 sets. In the others its 4-caps start at points of L4 with β ∈ {5, 6},
  mostly in M.
- Δ_R ∩ Q (always 4-cap-free) meets every heptagon in 57 sets. Δ_L ∩ Q' does so in 63 sets.
- Left-to-right greedy (put p in Δ iff it closes a heptagon with the points kept so far) gives a 4-cap-free Δ in
  108 sets; trying both directions, in 147.
- Requiring Δ to contain an endpoint of every saturated pair (cap(u,v) + cup(u,v) = 9) is infeasible in 28 of
  121 sets. So Δ must sometimes cut heptagons in their interior.
- **No rule of the form Δ = {p : (c₋, c₊, β, ω)(p) ∈ F}, nor Δ = {p : α(p) ∈ F} with Baek's α, works for all
  sets.** This is a lazy CP-SAT over the rule space, INFEASIBLE after 20–22 rounds (`tools/rule_learn.py`).
  The weaker target "meet all 7-cups and all (4,5)-heptagons", which together with Schroeder would already give
  68, has no (c₋, c₊, β, ω)-rule either (`tools/rule_learn2.py`).
- Any proof therefore needs a global, Baek-style construction of Δ, not a pointwise rule.
- **How far Δ must leave Q** (`tools/min_l4.py`, 169 sets). The minimum of |Δ ∩ L4|:
  - is 0 in 76 sets, 1 in 28, 2 in 22, 3 in 26, and 4–8 in the remaining 17;
  - the forced L4 points are mostly in M with β ∈ {4, 5, 6}, or start both a 4-cap and a 6- or 7-cup.
- **The trichotomy (2.6) does not suffice either.** Take Δ_A = {right ends in Q} ∪ {left ends in Q' of saturated
  pairs whose right end is in L4}. Over 194 sets:
  - 145 have no doubly hard pair. There Δ_A always meets every heptagon, but it is 4-cap-free in only 80.
  - The other 49 have doubly hard pairs.
  - The 4-caps of Δ_A run from a left end in B4 = Q'∩L4 to a right end in Q∩R4 (`tools/trich.py`).
- **Partition (colouring) versions fail.** A splitting of S into c 4-cap-free sets would give |S| ≤ 22c.
  - The 4-cap hypergraph of the ETV 42-point set has chromatic number exactly 5 (CP-SAT: 3 and 4 colours
    INFEASIBLE, 5 feasible; `tools/colorable.py`).
  - 3-colourability fails in exactly 8 of 169 sets: the ETV set and its seven 42-point perturbations. It
    succeeds in every smaller set.
  - Δ_R splits into two 4-cap-free sets (which would give |S| ≤ 26 + 44 = 70) in only 163 of 169 sets.
  - So a covering argument must use weights (as in the coordinator's 9 blocks of capacity 22 with weight 1/3),
    not a partition.

### 3.4 Adversarial search

Every accepted step of each random walk was tested exactly. No violation of either form was found.

| walk | start | moves | accepted steps tested | result |
|---|---|---|---|---|
| v1 (`adv_search.py`), weak form | empty / pool | add, move, delete | 61,107 (drifted to n ≈ 16) | OK |
| v2 (`adv_search2.py`), strong form, seeds 11–12 | largest quarter of the pool | add, move, delete | 10,192 + 8,730 (drifted to n ≈ 28) | OK |
| v2, size-preserving, seeds 31–33 | 42-point sets | move, replace | 887 + 935 + 894 | OK, but the walks stay at the ETV configuration (191 saturated pairs throughout), so they add little diversity |
| v3 (`adv_search3.py`), maximizing doubly hard pairs (§2.6 (iii)) | sets with the most doubly hard pairs | add, move, replace | 36,272 (non-greedy) + 139,655 + 161,767 + 150,046 (greedy) | OK. Up to 38 doubly hard pairs per set, but the walks drift to 17–21 points |

### 3.5 The case a = n: splitting octagon-free sets into two heptagon-free sets (OPEN; side observation)

For a = n the strong decomposition says: every set with no convex n-gon is the union of two sets with no convex
(n−1)-gon. The (n−1)-cap condition is automatic.
- For n = 8 this would give ES(8) − 1 ≤ 2(ES(7) − 1) ≤ 160, using Schroeder's ES(7) ≤ 81. That is, ES(8) ≤ 161.
- The n = 7 case (every heptagon-free set is the union of two hexagon-free sets) would give ES(7) ≤ 2·16 + 1 = 33,
  the open Erdős–Szekeres value. So the split statement is at least as hard as ES(7) = 33. Only the evidence is
  recorded here; it is not a near-term route.
- **All 1,235 known 64-point octagon-free sets split into two 32-point heptagon-free sets.** These are the 1,234
  sets of `experiments/es8-lower-bound-search-2026-10-11/family/sets/` and `saturation/witness8.txt`. The split
  was found by lazy CP-SAT, and each class was checked heptagon-free by the exact C checker (`tools/split2.py`,
  `data/split2.log`, about 1 s per set).
- Since 64 = 2·32 and ES(7) = 33 is conjectured, both halves are (conjecturally) extremal heptagon-free sets.
- This is weak evidence: those sets come from Erdős–Szekeres-type block constructions, where such a split is
  built in (C(6,i) = C(5,i) + C(5,i−1)).
- Random sets with no cap restriction (`tools/run_split_gen.sh`, `data/split_gen.log`) also split every time:
  - 60 octagon-free sets (n = 37–49) into two heptagon-free sets;
  - 90 heptagon-free sets (n = 24–31) into two hexagon-free sets;
  - 90 hexagon-free sets (n = 15–16, i.e. up to the extremal 16 = ES(6) − 1) into two pentagon-free sets. At
    16 points both halves must be extremal 8-point pentagon-free sets.

## 4. LP sensitivity of the 84-state omission model (exploratory)

Base rows: `cap5_omission_out.json` (277 cycle rows, 2 Baek blocks), plus lazy cycle-row separation. Fixed:
states (0,0,0) and (1,0,0) occupied. Solver: HiGHS MIP (`tools/lptest.py`). **These values are not
certificates**; THEORY310N §3 documents a false HiGHS optimum. They only rank the targets.

| hypothetical capacity row | states | MIP bound | best example found (§6) |
|---|---|---|---|
| none (base) | – | 71 | – |
| R7 ≤ 21 | f₁ = 6 (28) | 71 (no gain) | – |
| R7 ≤ 20 / 19 | f₁ = 6 | 70 / 70 | **R7 = 20 attained** |
| R7 ≤ 18 / 16 / 10 | f₁ = 6 | 69 / 68 / 62 | false (R7 = 18, 19, 20 attained) |
| R6 ≤ 35 / 30 | f₁ ≥ 5 (49) | 70 / 65 | R6 = 23 |
| R5 ≤ 50 | f₁ ≥ 4 (64) | 70 | – |
| T ≤ 48, i.e. N(8,5,7) ≤ 48 | f₁ ≤ 5 (56) | 70 | – |
| T ≤ 41 (ETV value of N(8,5,7)) | f₁ ≤ 5 | 63 | – |
| R4 ≤ 48 / 40 | f₃ ≥ 1 (56) | 70 / 62 | R4 = L4 = 30 (mirror) |
| Δ_R ≤ 44 / 35 / 29 | f₁+[f₂≥1]+[f₃≥1] ≥ 6 (58) | 70 / 61 / 55 | Δ_R = 24 |
| B₆ ≤ 16 | f₁ = 5 (21) | 71 (no gain) | – |

The only R7 capacity that helps is **R7 ≤ 20** ("Baek minus 2" for the set of 7-cup ends), and it would be
**sharp**.
- `cex/R7_size_20.json` (26 points) is a 6-cup followed by 20 points, each extending it to a 7-cup.
- In that set Q = R7 ∪ {first two points}, so Q is Baek-extremal (22).
- By 2.1, |R7| ≥ 21 forces |Q∖R7| ≤ 1. In the 19- and 20-point examples, Q∖R7 is the leftmost one or two points
  of the base cup.
- **Proved for single-base sets.** Suppose S is a 6-cup c₁…c₆ together with points that each extend it to a
  7-cup. Then c₁ starts no 4-cap c₁ a b c:
  - if b extends the cup, the chord lemma puts a below c₁b, so (c₁, a, b) is not a cap;
  - if b lies on the cup, so does a, and (c₁, a, b) is a cup.
  So c₁ ∈ Q∖R7 and |R7| ≤ 21. Sets with several bases are not covered.
- R7 ≤ 20 in general is not proved.

## 5. REFUTED lemmas (explicit point sets in `cex/`, independently re-verified)

| candidate lemma | would give | counterexample |
|---|---|---|
| B₆ (β-level 6) has no (3,6)-gon, so ≤ 16 by Baek n = 7 | levels 22+16+35 | `B6_has_36_heptagon.json` (31 points). Levels B₂–B₅ contain (3,k)-gons even in the ETV set. |
| R7 has no (3,6)-gon, so |R7| ≤ 16; or |R7| ≤ 19 | 68 / 70 | `R7_has_36_heptagon.json`. |R7| = 18, 19 and 20 in `R7_size_18.json` (27 points), `R7_size_19.json` (31) and `R7_size_20.json` (26) |
| B4 = {c₊ = 4, c₋ ≤ 3} has no (3,6)-gon, so ≤ 16 | – | `B4_has_36_heptagon.json` |
| M = L4 ∩ R4 is heptagon-free, so ≤ 25 (Schroeder) and hence 69 | 69 | `M_has_45_heptagon.json` (a (4,5)-gon inside M) |
| M has no 5-cup, so ≤ 20 | 64 | `M_has_5cup.json` |
| R6 = B₆ ∪ B₇ is 4-cap-free, so ≤ 22 by Baek | 57 | `R6_has_4cap.json` |
| Baek Lemma 5.6 analogue: max L7 ≤ min R7 | – | `L7_R7_interleave.json` |
| Δ_R is 4-cap-free (would prove Conj(8) and give 63) | 63 | 157 of 169 test sets have a 4-cap in Δ_R |
| L4 or R4 is heptagon-free (Δ = Q or Q') | 63 | 49 of 180 sets have heptagons in both |
| a recolouring "cap (x,y,z) with s(xy)=3 → cup" makes S (or Δ_R) Baek-boundable | ≤ 67 | cups\* reach 31 in S, 18 in Δ_R |
| supersaturation by deletion (every 23-set has a 4-cap) | – | needs ≲ 240 4-caps at 70 points; the ETV set already has 9,721 |
| S splits into three 4-cap-free sets | 66 | the ETV 42-point set needs 5 (4-cap hypergraph chromatic number 5); 3 colours fail in 8 of 169 sets |
| Δ_R splits into two 4-cap-free sets | 70 | fails in 6 of 169 sets |
| Baek's own ∆ (leftmost point of each β-row) as the Δ of the a = 4 analogue | – | a cup that meets every heptagon in only 14 of 48 oriented tests (`tools/baek_delta_a4.py`) |

## 6. Largest pieces found by targeted search

Simulated annealing on integer point sets, exact validity at every step (`tools/maxpiece.py`).

| piece | max found | trivial / Baek bound |
|---|---|---|
| R7 (7-cup ends) | 20 | 22 |
| R6 = B₆ ∪ B₇ | 23 | 43 |
| L4 (≡ R4 by mirror) | 30 | 56 |
| M = L4 ∩ R4 | 25 | 35 |
| Y = B₆ ∩ L4 | 13 | 21 |
| Δ_R | 24 | 58 |
| Δ_R ∩ L4 | 18 | – |
| \|M\| − \|Z\| | 19 | – |
| \|S\| | 42 (only from ETV seeds) | – |

Random 5-cap-free octagon-free sets (greedy insertion plus swaps) reach 37 points. Their β-levels are far from
the ETV profile (1, 3, 6, 10, 15, 6, 1), which has levels 1–5 full and only 7 points in R6.

## 7. Leads 3 and 4

- **Supersaturation (lead 3).** Baek is equivalent to "the 4-cap hypergraph has independence number ≤ 22". The
  deletion method gives nothing useful (§5), and the Lovász Local Lemma fails because of huge dependencies.
- **SDP / flag (lead 4).** Not attempted beyond the LP of §4. Every new valid row must be non-local:
  - the omission model's cycle rows already encode every octagon forced by local triple orientations (they are
    convex-position rows, not only 8-cups);
  - (4,6)-octagons enter only through Baek-type global statements.

## 8. Status at stop time

- Every systemd unit of this record (`nov13b-thy-*`) was stopped by 08:38 KST. Each ran on one core; at most two
  ran at a time.
- The work directory W is about 1 MB. Nothing was committed.
- **Adversarial walks** (§3.4), steps with exact tests and no violation:
  - v1: 61,107;
  - v2: 21,638;
  - v3: 487,740 (one non-greedy seed of 36,272, then greedy seeds of 139,655, 161,767 and 150,046). The greedy
    walks reached up to 38 doubly hard pairs per set but drifted to 17–21 points.
  - Total 570,485.
- **Certificates** (strong Δ, pure-Python re-verified):
  - 314 octagon-free sets: `conj8_certs.jsonl` (194) and `conj8_sub64_certs.jsonl` (120);
  - 121 heptagon-free sets: `conj7_certs.jsonl`.
- **Abstract signotopes:** 31 samples, n = 32–42, all OK in both forms (`abstract_conj.log`,
  `abstract_recheck*.log`). One n = 43 SAT sample was stopped unsolved.
- **General (a, n):** 360 random sets, all OK (`general_decomp.log`).
- **Split test (§3.5):** 1,235 of 1,235 known 64-point sets and 240 of 240 random sets split (`split2.log`,
  `split_gen.log`).
- **Counterexamples:** 10 files in `cex/`, all re-verified (`data/verify_cex.log`).

## 9. Most promising next steps

1. **Prove weak Conj(8)**, which gives 63; with weak Conj(7) as well it gives 54 and hence ES(8) ≤ 308. Weaker
   intermediate targets:
   - "a 4-cap-free Δ meeting all 7-cups and all (4,5)-heptagons" gives 68 with Schroeder (§2.4 argument applied
     to S∖Δ).

   The data localize Δ to Δ_R ∪ Δ_L (rank-defined). By 2.6 every heptagon except the doubly hard (4,5)-gons
   under a 7-cup chord has its right end in Q or its left end in Q'. The difficulty is that Q-points and
   Q'-points together can form 4-caps (§3.3), and that Δ must sometimes use up to 8 points of L4. No pointwise
   rule works, so the proof must be a Baek-style global construction or an exchange argument. The natural
   invariant to try is a left-to-right sweep that repairs a red 4-cap ending at the new point.
2. **Compute N(8, 5, 7)** (no 5-cap, no 7-cup, no octagon; ETV 41) with the internal-omission/coupled-core
   machinery. It needs only (4,6)-octagons and 56 states (f₁ ≤ 5). Any N(8,5,7) ≤ 48 gives M(5; 8) ≤ 70 by the
   proved reduction 2.1; the ETV value 41 gives 63.
3. **Joint constraint for the coupled model.**
   - R7 ⊆ Q is a valid in/out coupling: in-state f₁ = 6 forces out-state "no outgoing 4-cap". So
     |R7| + |Q∖R7| ≤ 22 on the union of the in-block f₁ = 6 and the out-block c₊ ≤ 3. The mirror is L7 ⊆ Q'.
   - R7 ≤ 20 would give 70 in the omission MIP but is sharp (R7 = 20 attained), so it can only come from a joint
     argument.

## 10. Sources read tonight

- J. Baek, *On the Erdős–Tuza–Valtr conjecture*, [arXiv:2206.04260v2](https://arxiv.org/abs/2206.04260):
  §§3–5, Lemmas 5.1–5.9 and Theorem 5.10.
- M. Schroeder, *Erdős–Szekeres: upper bounds for convex heptagons and octagons*, v1, 19 Sep 2026
  ([michaelschroeder.ai](https://michaelschroeder.ai), PDF `research/ErdosSzekeres/erdos_szekeres_upper_bounds_v1.pdf`):
  Theorem 5.2 (M₇(5,6) = 25), §7.3 Lemma 7.5 (horizontal block compression).
- J. Baek and M. Balko, *The Erdős–Szekeres conjecture revisited*, SoCG 2025
  ([LIPIcs.SoCG.2025.13](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2025.13)).
  Their "decomposable sets" are recursive *deep-below* splits; that is a different decomposition from §3.
