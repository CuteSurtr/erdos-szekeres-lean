# Δ theory at n = 7: proved lemmas (track T, 18 November 2026, from 02:30 KST)

**Status (04:15 KST; work continues to 08:20).** Weak D(5,7) and LR(7) remain OPEN from 16 points; no ES bound
changes; nothing here moves the certified frontier at n = 7 or 8. What is new:
- **PROVED for all n ≥ 6** (§1): Lemma I(n) (n+1 points without a convex n-set: all convex (n−1)-subsets share a
  point) and **Theorem A** (a cup K with |S − K| ≤ n+1 extends by at most one point to a weak Δ; 5-caps allowed), with
  corollaries: every point on a b-cup is rootable when |S| ≤ n+1+b; C1(n) through 2n; weak D(5,n) through 2n − 1;
  **Theorem B: LR(n) through 2n − 2** (the written bounds were 2n − 3, one-sided). Claims `t1118-cupanchor`,
  `t1118-wd2n1`, `t1118-lr2n2`.
- **EXACT negative results** (§2): cup anchoring stops at 2n (a 13-point (5,6)-valid model); the obvious construction
  for ROOT at 2n − 2 fails (models at n = 6, 7).
- **LR(7) at 16** (§3): two sound add-ons in the numbering of `lc7_m16.cnf` (vertex criticality from the CERTIFIED
  15-point results; a mirror lex-leader for K1/K3 compatible with the D track's cube cover). Claims `t1118-vc16`,
  `t1118-lexmirror16`. Not solver-tested; expected effect small.
- **New conjectures with EXACT support** (§4): ANCHOR-L / STRONG ANCHOR-L — in all 614 known right-hostile sets every
  cup that starts at l and avoids r extends to a weak Δ; they imply C2 and LR, and at 16 points the 5-cup version would
  empty the pieces C1 and K2 of the LR(7) split. Claims `t1118-anchorl-data`, `-strong-data`, `-correction`. A complete
  CNF for ANCHOR-L(6) is being solved (unit `esr-agt-anchorl6full`).

Labels: PROVED (complete written proof here) / CERTIFIED / EXACT (own exhaustive code from the definitions) / COMPUTED
(solver verdict) / HEURISTIC / CONJECTURE. Nothing is rounded up. Work directory (not in Git):
`/home/jay/research/data/roadmap-20261115/pm1115/t1118/` (below `T/`). Compute: foreground checks under a minute;
longer exact checks as units `esr-agt-*` (CPUQuota ≤ 15 % in total, MemoryMax ≤ 600M).

## 0. Definitions

As in THEORY_1115PM.md §0 and PROOF_LR_ATTEMPT_P1.md §0. S is a signotope on 0..m−1 in x-order; '+' = cup
(orientation > 0), '−' = cap; k-cap / k-cup: every triple a cap / a cup; convex set: every 4-subset x<y<z<w has
σ(xyz) = σ(xyw) and σ(xzw) = σ(yzw); (5,n)-valid: no 5-cap and no convex n-set; gon: convex (n−1)-set; weak Δ:
4-cap-free set meeting every gon; l = 0, r = m−1, U = S − r, V = S − l; a point p is *rootable* in S if some weak Δ of S
contains p. β(v) / α(v): number of points of a longest cup ending / starting at v; γ(v): of a longest cup containing v.
A *bad quad* is a non-convex 4-subset; a set is convex iff it contains no bad quad. A sub-signotope (restriction to a
subset, relabelled in order) is a signotope.

## 1. Cup anchoring: Lemma I(n) and Theorem A (PROVED)

**Fact F5 (EXACT; `T/tools/local_lemmas 5`).** Every signotope on 5 points has 0, 2 or 4 bad quads, never exactly one
(all 62 signotopes: 8, 32 and 22 of them).

**Lemma I(n) (n ≥ 6).** Let W be a signotope on N = n+1 points with no convex n-subset. Then some w ∈ W is such that
W − w contains no convex (n−1)-subset.

*Proof.* Call a pair {x,y} ⊆ W an *edge* if it meets every bad quad (equivalently W − {x,y} is convex); E is the set of
edges. A point w lies in no edge iff W − w contains no convex (N−2)-subset, which is the claim. The hypothesis says
that for every point z some bad quad avoids z (else W − z would be a convex n-set). Write N(v) for the neighbours of v
in E and Δ for the largest degree.

- N = 7, 8: EXACT (`T/tools/sigenum 7`, `sigenum 8`: all 24,698 resp. 1,232,944 signotopes, enumerated from the
  signotope axiom; the counts equal the known numbers of rank-3 signotopes 8, 62, 908, 24,698, 1,232,944 for N = 4..8).
  Among the 22,402 resp. 1,221,504 without a convex (N−1)-subset, at most 6 points lie in edges; never all N.
- Let N ≥ 9 and suppose, for a contradiction, that every point lies in an edge.
  - (a) Every bad quad that avoids v contains N(v) (it meets each edge {v,b}).
  - (b) Δ ≤ 3. If deg v ≥ 4 with neighbours b1..b4, by (a) the only possible bad quad avoiding v is B4 = {b1,..,b4},
    and one exists, so B4 is bad. For y ∉ B4 + v, the 5-set B4 + y has a second bad quad (F5); it avoids v, so by (a)
    it contains B4: impossible.
  - (c) If N(v) = B with |B| = 3, then B + y is bad for every y ∉ B + v. (Some B + y0 is bad; F5 on B + y0 + y gives a
    second bad quad, which avoids v and so contains B; it is B + y.)
  - **Δ = 3.** Take v with N(v) = B = {b1,b2,b3}. A point y ∉ B + v in an edge {y,z}: z lies in B + y′ and in B + y″
    for two distinct y′, y″ ∉ B ∪ {v,y} (N − 5 ≥ 2), so z ∈ B. Each b ∈ B has at most two neighbours outside B + v.
    If b1 has two, y1 and y2, then N(b1) = {v,y1,y2} and (c) for b1 makes {v,y1,y2,b2} and {v,y1,y2,b3} bad; a third
    outside point y3 with an edge to b2 (to b3) misses the bad quad {v,y1,y2,b3} ({v,y1,y2,b2}), and an edge to b1
    contradicts Δ ≤ 3. So at most 2 outside points lie in edges, or at most 3 if every b has at most one outside
    neighbour. At most 1 + 3 + 3 = 7 < N points lie in edges.
  - **Δ = 2.** Take v with N(v) = {b1,b2}; R = W − {v,b1,b2} (|R| = N − 3 ≥ 6); 𝒫 = {{y,z} ⊆ R : {b1,b2,y,z} bad}.
    By (a) these are all bad quads avoiding v, so 𝒫 ≠ ∅. *Domination:* for {y,z} ∈ 𝒫 and w ∈ R − {y,z}, F5 on
    {b1,b2,y,z,w} gives a second bad quad avoiding v, so {y,w} ∈ 𝒫 or {z,w} ∈ 𝒫. A point x ∈ R in an edge {x,p}: p ≠ v
    (x ∉ N(v)); if p ∈ R, {x,p} meets every {b1,b2,y,z}, i.e. is a vertex cover of 𝒫; if p ∈ {b1,b2}: each b_i has at
    most one neighbour in R (degree ≤ 2, one neighbour is v), so at most 2 such x.
    - ν(𝒫) ≥ 3 (matching number): no 2-point cover; at most 3 + 2 = 5 points lie in edges.
    - ν(𝒫) = 2 with disjoint e1, e2 ∈ 𝒫: every R-partnered x lies in e1 ∪ e2; at most 3 + 4 + 2 = 9. Equality forces
      N = 9, R = e1 ∪ e2 ∪ {t1,t2} with edges {t1,b1}, {t2,b2}, and every point of e1 ∪ e2 joined by an edge to the
      other of e1, e2; a bipartite graph on 2 + 2 points with minimum degree ≥ 1 has a perfect matching, so E has two
      disjoint edges inside e1 ∪ e2. A bad quad avoiding b1 (exists) meets {v,b1}, {t1,b1}, {t2,b2} and those two
      edges: it has ≥ 5 points. So at most 8 < N.
    - ν(𝒫) = 1: the edges of 𝒫 pairwise meet, so 𝒫 is a triangle or a star. A triangle leaves a fourth point of R
      undominated. For a star with centre c, domination makes every w ∈ R − c a leaf (N − 4 ≥ 3 leaves), so every
      2-point cover contains c; R-partnered points are c and its ≤ 2 neighbours: at most 3 + 3 + 2 = 8 < N.
  - **Δ = 1.** Then E is a perfect matching: impossible for odd N, and for N ≥ 10 a bad quad would have to meet ≥ 5
    disjoint edges.
  - **Δ = 0** contradicts the assumption. ∎

*Reformulation.* W − w contains no gon iff every gon of W contains w. So Lemma I(n) says: **in a signotope on n+1
points without a convex n-subset, all convex (n−1)-subsets have a common point**; the proof gives at least N − 6
common points (all points outside V(E)), and the enumeration shows that 6 is attained for N = 7, 8, 9. For n+2 points
this fails: at n = 6 there are 8-point signotopes without a convex hexagon whose convex pentagons need 2 points to be
hit (261,428 of 912,128; `taugons 8 6`). Literature: not found in a short arXiv search (03:20; queries on
deletion/convex position/Erdős–Szekeres); "new" means only that.

**Theorem A (cup anchoring; PROVED).** Let n ≥ 6, S a signotope with no convex n-subset (5-caps are allowed), and K ⊆ S
a cup with |S − K| ≤ n + 1. Then K ∪ X is a weak Δ of S for some X ⊆ S − K with |X| ≤ 1.

*Proof.* K ∪ X has no 4-cap: a 4-subset contains at least three points of K (if |K| ≥ 3), and these form a cup triple;
if |K| ≤ 2 there is no 4-subset. A gon of S either meets K or lies in W = S − K. Choose X: |W| ≤ n − 2: X = ∅;
|W| = n − 1: X = {w} for any w ∈ W; |W| = n: W is not convex, take a bad quad Q ⊆ W and w ∈ W − Q, so W − w ⊇ Q is a
non-convex (n−1)-set; |W| = n + 1: w from Lemma I(n) applied to W (W has no convex n-subset). In each case W − X
contains no gon. ∎

**Corollaries (PROVED).**
- **A1.** If p lies on a b-cup and |S| ≤ n + 1 + b, then p lies in a weak Δ (any position of p, no 5-cap hypothesis).
  With b = 2 (any pair is a 2-cup): every point is rootable when |S| ≤ n + 3, which re-proves the parent's lemma of
  `resume/selection/structure/theory.md` §5 without its no-5-cap hypothesis.
- **A2 (C1(n) through 2n).** If |S| ≤ 2n and r ends an (n−1)-cup, r lies in a weak Δ. So P1's C1(n) holds for all
  (5,n)-valid S with |S| ≤ 2n, without its hypothesis "r ends a 4-cap". At n = 6 this is C1(6) for |S| ≤ 12 by hand
  (C1(6) is CERTIFIED for all sizes by `d1-c1six` + ROOT(6)).
- **A3.** In a (5,n)-valid S with m points every point p outside all weak Δs has γ(p) ≤ m − n − 2. So a ROOT(n) failure
  has β(r) ≤ m − n − 2 and an LR(n) failure has β(r), α(l) ≤ m − n − 2. At n = 7, m = 16 the bound is 7: **vacuous**
  (cups have at most 6 points), so Theorem A does not touch LR(7) at 16.
- **A4 (weak D(5,n) through 2n − 1; added 03:20).** Every (5,n)-valid S with |S| ≤ 2n − 1 has a weak Δ (n ≥ 6): if S
  has an (n−2)-cup K, then |S − K| ≤ n + 1 and Theorem A applies; otherwise P0 is a weak Δ by Corollary SD (P1, claim
  `p1-cupext`, CONFIRMED). At |S| = 2n the same argument works unless the longest cup has exactly n − 2 points. The
  previous written bound was 2n − 3 (ROOT(n) for |S| ≤ 2n − 3 plus induction). Nothing new at n = 7, 8 (weak D(5,7)
  and weak D(5,8) are CERTIFIED through 15 and 16 points). Claim `t1118-wd2n1`.
- **Theorem B (LR(n) through 2n − 2; PROVED, added 04:10).** For n ≥ 6, every (5,n)-valid S with |S| ≤ 2n − 2 has a
  weak Δ through l or through r (no hypothesis on 4-caps at the ends). *Proof.* For |S| ≤ 2n − 3, r lies in a weak Δ
  (Theorem 4 of `resume/selection/structure/theory.md`). Let |S| = 2n − 2 and suppose neither end lies in a weak Δ.
  By A3, α(l) ≤ γ(l) ≤ (2n − 2) − n − 2 = n − 4. Since r lies in no weak Δ, Corollary 5 of the same record gives an
  (n−2)-cup C of U = S − r such that U − C is a convex (n−1)-set. If l ∈ C, then C is a cup starting at l (l is the
  leftmost point), so α(l) ≥ n − 2. If l ∉ C, then l is the leftmost point of the gon U − C, whose lower chain is a cup
  starting at l with at least n − 3 points (its upper chain is a cap, so at most 4 points, and the two chains have
  n + 1 points together); so α(l) ≥ n − 3. Both contradict α(l) ≤ n − 4. ∎ This is the first written two-sided
  statement beyond the one-sided bound 2n − 3; nothing new at n = 7, 8 (LR is CERTIFIED through 15 points there).
  Claim `t1118-lr2n2`.
- **Sharpness.** For a prescribed (n−1)-cup ending at r the bound |S − K| ≤ n + 1 cannot be raised to n + 2 at n = 6:
  T3's anchored runs AC1(6; 13, K) (`pm1115/t3n6/anchor/ac1_6_13.jsonl`) give, for 488 of the 495 position patterns
  of K, a (5,6)-valid model in which K ∪ X is a weak Δ for no X (COMPUTED). (r is still rootable there by other sets.)
- **Comparison.** The written theorem of `resume/selection` gives ROOT(n) for |S| ≤ 2n − 3 by a different route (cup
  complement or a single β-level). Theorem A is anchored on a cup and holds for any point of the cup.

**Exact controls (own code `T/tools/t1lib.py`, self-test PASS; `ctl_thmA.py`, `ctl_thmA_rand.py`).**

| control | instances | result |
|---|---|---|
| Lemma I(n) by full enumeration, N = 7, 8 (`sigenum`) | 22,402 + 1,221,504 signotopes without a convex (N−1)-subset | 0 failures; at most 6 points lie in edges |
| Lemma I(8), N = 9 (`sigenum 9`, unit `esr-agt-sigenum9`, 02:54-03:11, 150 CPU-s) | all 112,018,190 signotopes (= the known count), 111,964,972 without a convex 8-subset | **0 failures**; at most 6 points lie in edges (independent check of the written N ≥ 9 argument at N = 9) |
| Theorem A construction + Lemma I witnesses on random subsets (n+3 .. 2n points) of T2's 1,440 collected sets (n = 6, 7; real and abstract; `T2/out/all_sets.jsonl`), 2 subsets per set | 2,880 subsets, 256,675 (cup, X) constructions, 146,115 Lemma I calls | 0 failures |
| A1 by brute force (every point p with γ(p) ≥ |T| − n − 1 lies in a weak Δ; all 2^|T| subsets) | 28,170 points | 0 failures |
| same on random integer point sets without a convex n-set (5-caps allowed; 245 of 450 sets have a 5-cap), n = 6, 7 | 450 sets, 46,269 constructions, 20,096 Lemma I calls, 4,314 points | 0 failures |
| τ of the gons (`taugons`): N = n+1 | n = 6 (24,698), n = 7 (1,232,944 signotopes) | τ ≤ 1 always (= Lemma I) |
| τ of the gons for N = n+2, n = 6 | 1,232,944 signotopes, 912,128 without a convex hexagon | τ ≤ 2 always (EXACT; a hint that "τ ≤ N − n" may hold more generally; not used) |

Claim: **`t1118-cupanchor`** (Lemma I(n), Theorem A, Corollaries A1-A3), verifier VS. (Filed 02:59 KST; the JSON
says 03:08 by mistake.)

## 2. Where cup anchoring stops (negative results)

| statement tested | result | label | evidence |
|---|---|---|---|
| "If r ends a 4-cap and an (n−1)-cup, some weak Δ contains a whole (n−1)-cup ending at r" (any choice of the cup), n = 6, \|S\| = 12 = 2n | holds (as Theorem A says) | COMPUTED (pysat CaDiCaL UNSAT of `T/tools/c1allcups.py 6 12`, 21,120 rows) | — |
| the same at \|S\| = 13 = 2n+1 | **false**: a 13-point (5,6)-valid signotope in which r ends a 4-cap and exactly one 5-cup (0,5,6,9,12), r lies in 65 weak Δs (smallest: {0,1,3,10,12}), none containing the whole cup | **EXACT** (model of `c1allcups.py 6 13`, re-checked by `check_c1allcups_model.py` from the definitions: signotope, valid, 672 weak Δs) | `T/models/c1allcups_6_13.json` |
| "at \|S\| = 2n−2, if U has an (n−2)-cup, some C + r or C + w + r (C an (n−2)-cup of U, w ∈ U − C) is a rooted weak Δ" (the obvious next step after Theorem 4 / Cor. 5 of `resume/selection/structure/theory.md`) | **false** at n = 6 (\|S\| = 10, U has six 4-cups) and n = 7 (\|S\| = 12) | EXACT (models of `root2n2.py`, re-checked by `check_root2n2_model.py`; r is rootable there by other sets) | `T/out/root2n2_6_10.json`, `root2n2_7_12.json` |
| the 2n−2 statement above with the extra hypothesis β(r) ≤ n − 4 (which A3 gives for an unrootable r at 2n − 2) | **holds at n = 6** (COMPUTED, pysat UNSAT); **false at n = 7** (12 points, β(r) = 3; EXACT re-check) and at n = 8 (14 points, β(r) = 4; COMPUTED model, validity re-checked) | as stated | `root2n2.py n m --a3`; `T/out/root2n2a3_7_12.json`, `root2n2a3_8_14.json` |
| "at \|S\| = 2n−1, with α(l), β(r) ≤ n−3 (A3) and an (n−2)-cup avoiding l and r (Theorem 2), some C + e or C + e + y (C an (n−2)-cup avoiding both ends, e ∈ {l, r}, y ∈ S − C) is a weak Δ" (the next step after Theorem B) | **holds at n = 6** (COMPUTED, `lr2n1.py 6 11` UNSAT); **false at n = 7** (13 points; EXACT re-check: valid, both ends rootable by other sets) and n = 8 (15 points, COMPUTED model) | as stated | `T/tools/lr2n1.py`, `T/out/lr2n1_7_13.json` |

So the cup-anchoring method ends exactly at 2n (it is sharp for prescribed and for freely chosen cups at n = 6), and
extending the written ROOT(n) theorem from 2n−3 to 2n−2 needs rooted Δs of another kind. Both are statements about
methods; no conjecture of the program is refuted.

## 3. LR(7) at 16: sound add-ons in the numbering of `d1ev/cnf/lc7_m16.cnf` (PROVED soundness; effect unknown)

Neither add-on has been run against a solver tonight; both are offered to the D track. Honest expectation: VC is weak
(it holds on almost every known 16-point set, see the control), the lex-leader halves only the 8 mirror-invariant top
cubes of K1 and K3 (8 of 36 top cubes each).

**Lemma VC (PROVED from CERTIFIED inputs).** Let S be a 16-point LR(7) failure (5,7)-valid, r = 15 ends a 4-cap,
l = 0 starts a 4-cap, no weak Δ contains l or r). Then
- (VC-a) every p ∈ {1..14} lies in a convex hexagon of S that avoids l or avoids r;
- (VC-b) every p ∈ {1..14} lies in a 4-cap of S;
- (VC-c) for every pair {p,q} ⊆ S − r some convex hexagon avoiding r meets {p,q}; mirror for S − l.

*Proof.* Every 15-point (5,7)-valid signotope T has a weak Δ through its leftmost or its rightmost point: if they end
resp. start a 4-cap this is LR(7) at 15 (CERTIFIED: main session's cake_lpr run of T1's proof, second run by VL;
STATUS20261115_2300); if, say, max T ends no 4-cap, it lies in no 4-cap of T and a weak Δ of T − max T (weak D(5,7) at
14, CERTIFIED with replayed certificates) plus max T is one. Apply this to T = S − p (its ends are l and r): a weak Δ D
of S − p contains l or r. In S, D is 4-cap-free and meets every hexagon avoiding p, but D is not a weak Δ of S, so it
misses a hexagon of S, which contains p and avoids the end in D (VC-a); D + p meets every hexagon, so it contains a
4-cap, which contains p (VC-b). For (VC-c) use T = S − {p,q} (14 points) and ROOT(7) at 14 (CERTIFIED; if r ends no
4-cap of T, weak D(5,7) at 13): a weak Δ of T through r misses a hexagon of S, which avoids r and meets {p,q}. ∎

**Clauses** (`T/tools/vc16.py`; `T/cnf/vc16_addon.cnf`, 238 clauses + 3,640 definitions, 1,820 new variables
108,259-110,078; merged `T/cnf/lc7_m16_vc.cnf`): (VC-a) ∨ B(X) over 6-sets X ∋ p not containing both 0 and 15; (VC-c)
∨ B(X) over 6-sets X ∌ r (resp. ∌ l) meeting {p,q}; (VC-b) ∨ y_K over 4-sets K ∋ p with new y_K → (abc cap) ∧ (bcd cap).
B(X) (|X| = 6) is lr_compact's one-way variable "X contains a gon" (B → cv(Q) for all 15 Q ⊆ X). The script
recomputes lr_compact's numbering and checks it against the CNF: all 7,007 B(X) and all 105,105 defining clauses
found (`numbering check OK`). Soundness: an LR failure satisfies the base CNF with canonical auxiliaries (D1's review,
`d1-lr7m16-split`), and with B(X) := [X convex], y_K := [K a 4-cap] it satisfies the add-on by Lemma VC.
**Control** (`ctl_vc16.py`, EXACT): on 20 sets (R7's real 16-point sets f4, f4b, f6 and the 17 one-point deletions of
R7's real 17-point block), the add-on clauses evaluated at the canonical assignment agree with the exact truth of
VC-a/b/c clause by clause (20/20); all three families are true on 19 of the 20 sets (VC-b fails on `root7_real17 − 16`),
so the add-on excludes little that these sets do not already satisfy.

**Mirror lex-leader for K1 and K3 (PROVED; `T/tools/lexmirror16.py`, `T/cnf/lexmirror16_K1.cnf`,
`lexmirror16_K3.cnf`, 839 clauses, 278 aux variables numbered after each base CNF).** The D track's trees use the
top variables V0 = (560, 1, 559, 2, 558, 15) = three mirror pairs and keep one assignment per mirror orbit (36 of
64); all 8 mirror-invariant assignments are kept (checked in `dn/cubes/K1_tree.json`, `K3_tree.json`). The add-on
says: if x560 = x1, x559 = x2 and x558 = x15, then (x_a) ≤lex (x_μ(a)) over the other 277 orbits {a, μ(a)}, a < μ(a), in
increasing a (false < true). *Soundness:* if S is a failure of K1 (K3) with an invariant V0 pattern, μS is a failure
of the same piece (PROBES_1116.md cover argument, part 2) with the same V0 pattern, and one of S, μS is lex-leader;
the auxiliaries e_i = [prefix equal through orbit i] satisfy all clauses. Non-invariant top cubes are unconstrained,
so the cover argument of PROBES_1116.md is unchanged. **Control** (`ctl_lexmirror16.py`, EXACT): 600 assignments
(300 random 16-point integer point sets and their mirror images, a third of them forced to an invariant V0 pattern):
the add-on with the 560 triple variables fixed is satisfiable exactly when the direct lexicographic test says so
(600/600; 280 invariant patterns). Not applicable to K2 or C1(7) (not mirror-invariant). The VC and lex-leader
add-ons both number their auxiliaries from 108,259 on K1; renumber before combining them.

Claims: **`t1118-vc16`** (Lemma VC and its clauses), **`t1118-lexmirror16`** (lex-leader add-on), verifier VS.

## 4. ANCHOR-L: in every known right-hostile set, l is rooted by a cup from l plus 1-3 points (CONJECTURE)

**ANCHOR-L(n) (new CONJECTURE).** If S is (5,n)-valid, r ends a 4-cap, l starts a 4-cap and r lies in no weak Δ, then
some weak Δ of S contains a whole (n−1)-cup K with min K = l.

- ANCHOR-L(n) ⟹ C2(n) (K is an (n−1)-cup starting at l) and ⟹ LR(n) (the Δ contains l). So it is a sharpening of
  the two-sided statements, of the same kind as Theorem A, and it names a mechanism: the hostile right end makes the
  left end rootable by anchoring on a long cup from l.
- It is not a consequence of Theorem A (|S − K| = n + 4 .. n + 7 in the data, beyond n + 1), and anchoring at l fails
  in general: the mirror image of the 13-point model of §2 has an (n−1)-cup from l and no anchored Δ (there r is
  rootable, so ANCHOR-L is not contradicted). The right-hostility is what makes it work.
- **EXACT data** (`T/tools/anchor_l.py`, own code; exhaustive search over X ⊆ S − K for every (n−1)-cup K from l): it
  holds on **all 614 right-hostile sets of T2's collection** (`pm1115/t2size/out/all_sets.jsonl`: every set with r in
  no weak Δ; 348 at n = 6, m = 15; 266 at n = 7, m = 17-20; real and abstract; outputs `T/out/anchor_l_*.out`).
  Smallest |X| needed: 2 or 3 at n = 6 (m = 15), 1 or 2 at n = 7 (m = 17: always 1; m = 19, 20: 1 or 2).
- Structure behind |X| = 1 at n = 7, m = 17 (`anchor_l_stats.py`): for the cup K = (0,1,3,6,10,14) of the real
  17-point blocks, the 16-22 convex hexagons that avoid K all pass through the single point 9, so K + 9 is a weak Δ
  (the analogue of Lemma I far beyond n + 1 points). At n = 6, m = 15 and n = 7, m = 20 the hexagons avoiding the best
  cup have no common point (2-3 points needed).
- Smallest |X| over the 614 sets: n = 6: 2 (296 sets) or 3 (52); n = 7: 1 (160) or 2 (106) (`T/out/anchor_l_all_summary.txt`).
- **STRONG ANCHOR-L (stronger CONJECTURE, 03:45):** under the same hypotheses, *every* (n−1)-cup starting at l and
  not containing r extends to a weak Δ (a cup through r cannot extend, r being in no weak Δ; in the data no cup from l
  passes through r, as C1 predicts: such a cup would give β(r) = n−1). EXACT on the same 614 sets: all **5,182** (n−1)-cups from l (2,774 at n = 6; 2,408 at n = 7) extend
  (`anchor_l_which.py`, `T/out/anchor_which_*.out`). Caveat on the strength of this evidence: in the 150 sampled sets of
  the collection where r *is* rootable, all 216 cups from l extend as well (`anchor_l_general.py`), so the collection
  contains no non-extending cup at all, hostile or not; non-extending cups do exist in general: in §2's 13-point model
  the only 5-cup runs from l to r and lies in no weak Δ, and T3's anchored runs AC1(6; 13, K) give models for 323 position
  patterns of a 5-cup ending at r and avoiding l that extends to no weak Δ (COMPUTED; by the mirror, the same for cups
  from l avoiding r). The content of the conjecture is that a non-extending cup at one end never coexists with an
  unrootable point at the other end.
- **Relation to Theorem A (PROVED).** A k-cup K from l extends whenever |S| ≤ n + 1 + k, hostile or not (Theorem A);
  so STRONG ANCHOR-L for k-cups is a theorem for |S| ≤ n + 1 + k, and the conjecture concerns |S| ≥ n + 2 + k, where
  non-extending cups exist in general (above) and the right-hostility has to be used.
- **Shorter cups (03:55).** The same holds for shorter cups from l: in all 266 right-hostile n = 7 sets every
  **5-cup** from l extends (20,738 cups; `anchor_l_k2.py`, `T/out/anchor_k_n2_i7.jsonl`), and in 22 sampled n = 7 sets
  every 4-cup does (2,926 cups; `anchor_k_n3_i7.jsonl` and an earlier sample); at n = 6 every 4-cup extends in all 348
  right-hostile n = 6 sets (15,663 cups, 04:20; `T/out/anchor_k_n2_i6.jsonl`; first sample: 30 sets, 1,272 cups), and of 872 3-cups in 20 sampled sets exactly 8 do not extend — **all 8 are the cup (0,7,14),
  which contains r** (a cup through r can never extend; correction 04:05 of the first reading, which called this a
  failure of k = n−3). Even pairs: in 46 sampled hostile sets every point a ≠ r lies in a weak Δ together with l (593
  pairs; `anchor_pairs.py`). VB's independent check (`VERIFY_T1118_ANCHORL_DATA_VB1118.md`) extended this to the whole collection: all 266
  hostile n = 7 sets, 36,891 4-cups from l, the only 4 failures are the cup (0,1,4,16) through r; all 348 hostile n = 6
  sets, every 3-cup avoiding r extends (15,777; all 84 failures pass through r); in all 826 r-rootable sets the 6,168
  (n−1)-cups from l extend. So the data support the strongest form **ANCHOR-L_all: if r is unrootable, every cup that
  starts at l and avoids r extends to a weak Δ** (cups of every length 2..n−1), with no exception found.
- **What this would give at 16 points (implications PROVED; premises CONJECTURE).** Suppose that at m = 16, whenever
  r is unrootable, every 5-cup starting at l and avoiding r extends to a weak Δ (ANCHOR-L_5(7)), and the mirror
  statement holds. In an LR(7) failure both ends are unrootable, so no 5-cup from l avoids r and no 5-cup ending at r
  avoids l. Then α(l) ≤ 5 (a 6-cup from l contains a 5-cup from l avoiding r), β(r) ≤ 5, and if α(l) = 5 or β(r) = 5
  every such 5-cup runs from l to r (so α(l) = 5 ⟺ β(r) = 5). So the pieces C1 and K2 of `d1-lr7m16-split` are
  empty, K3 shrinks to the residual "every 5-cup at an end is a 5-cup from l to r" (364 position patterns
  (0,a,b,c,15)), and K1 remains. If also every
  4-cup from l avoiding r (and the mirror) extends, K1 shrinks to α(l), β(r) ≤ 3 plus residual 4-cups from l to r;
  with α(l), β(r) ≤ 3 no gon contains l (a gon through l has a lower chain of t ≤ α(l) ≤ 3 points, an upper chain of
  k ≤ 4 points, and k + t = n + 1 = 8 is impossible) and none contains r, so both ends lie in no gon and the problem
  lives on S − {l, r} (14 points) with two 4-cap-extension conditions. Each anchoring premise at 16 splits into
  pattern CNFs AC-L(7; 16, K) over cups K from l avoiding r (1,001 patterns for 5-cups, 364 for 4-cups), each a
  restriction of ROOT(7) at 16.
- **Use for LR(7) at 16 (proposal, not run).** In an LR(7) failure r is unrootable, so STRONG ANCHOR-L(7) at 16 would
  exclude α(l) = 6 with a 6-cup from l avoiding r, and by the mirror β(r) = 6 with a 6-cup ending at r avoiding l; what
  is left of the piece `c1_rcup7_m16` of `d1-lr7m16-split` are the failures whose 6-cups from l all end at r (a 6-cup
  through both ends; 1,001 position patterns). The anchoring part splits into
  C(14,5) = 2,002 pattern CNFs AC-L(7; 16, K) (6-cups from l avoiding r) (`T/tools/acl.py`: compact ROOT(7) failure CNF + "l starts a 4-cap" +
  "K is a cup" + the 2^10-ish anchored rows of the fixed K), each a restriction of ROOT(7) at 16. Timing at n = 6,
  m = 15: with pysat's CaDiCaL 1.9.5, pattern (0,1,2,5,13) UNSAT in 20.6 s, (0,1,11,12,13) no verdict in 55 s; with
  CaDiCaL 2.1.3 through the driver `T/tools/acl_driver.sh` (resumable, one JSON line per pattern, modes fast/cert)
  the first 8 of the 715 patterns of 5-cups from l avoiding r ((0,1,2,3,x), x = 4..11) are all **UNSAT in 5-9 s each**
  (COMPUTED, `T/out/acl6_test/acl.jsonl`); in cert mode the first 4 of them ((0,1,2,3,x), x = 4..7) are **CERTIFIED**
  (CaDiCaL 2.1.3 LRAT kept as zstd, cake_lpr exactly one `s VERIFIED UNSAT`, stream hash = proof hash; 7-10 s each
  including cake_lpr; `T/out/acl6_certtest/acl.jsonl`, `runs/*/certify.jsonl`). So the complete n = 6 sweep (715 patterns, about 1.5 CPU-hours) would
  establish STRONG ANCHOR-L(6) for 5-cups (with C1(6), C2(6): ANCHOR-L(6)), and is the natural test bed before the
  n = 7, m = 16 patterns; one n = 7 pattern ((0,1,3,6,10), 5-cup) gave no verdict in 50 s, and the n = 6 pattern
  (0,1,11,12,13) none in 45 s with CaDiCaL 2.1.3 either (cups ending next to r are the hard ones). Not run tonight
  beyond that (CPU budget).
- **Test at n = 6 for all signotopes (running).** A first CEGAR (`anchorl_cegar.py`: T3's compact ROOT(6) CNF
  `d1ev/cnf/rc6_m15.cnf`, SHA-256 `152d8a20…`, plus lazily added rows) was too slow at 15 % (1 iteration in 14 min;
  stopped 03:38). Replaced by a **complete compact CNF** (`T/tools/anchorl_cnf.py 6 15` → `T/cnf/anchorl6_m15.cnf`,
  72,894 variables, 234,826 clauses, SHA-256 `cbb00e49e1a9edab0fddb8816271e6edc4c32be9bcb55a1ea56c9f2a7578317a`):
  T3's lr_compact scheme with the left rows made conditional, `¬A(D) ∨ BadL(D) ∨ B(Ul − D)`, where A(D) ("D + l
  contains an (n−1)-cup from l") is forced by A(D) ← [D + l is a cup] (|D| = n−2) and A(D) ← A(D − v). Soundness in
  the encoder's docstring (an ANCHOR-L counterexample satisfies every clause with canonical auxiliaries). UNSAT proves
  ANCHOR-L(6) at 15 points, hence for all signotopes (r is rootable below 15 points by ROOT(6) ≤ 14, CERTIFIED; no
  (5,6)-valid signotope has 16 points); a model would be an ANCHOR-L(6) counterexample, i.e. a right-hostile 15-point
  set in which no weak Δ through l contains a whole 5-cup from l.
  - Controls (`ctl_anchorl.py`, EXACT, own code): on 39 right-hostile and 10 r-rootable 15-point sets of T2's
    collection, with every variable at its defining value, the only falsified clauses of the hostile sets are
    conditional left rows, each one a D whose D + l is an anchored weak Δ (91-148 per set); the CNF with the 455
    triple variables fixed is UNSAT for all 49 sets, and without the conditional left rows it is SAT for every hostile
    set and UNSAT for every r-rootable set. The refactored encoder regenerates the CNF byte-identically.
  - Run: unit `esr-agt-anchorl6full` (15 %, MemoryMax 600M, from 03:38:57), `T/tools/cad_stream_cert.sh`: CaDiCaL
    2.1.3 with LRAT streamed through zstd (kept as `T/cert/anchorl6_m15/anchorl6_m15.lrat.zst`, SHA-256 of the
    uncompressed stream recorded), wall limit 07:58, then cake_lpr (heap 500 MB) on the decompressed stream (tested on
    a small CNF: `s VERIFIED UNSAT`, hashes equal). Status: see "What remains".

**Probe (stopped).** C2(7) counterexample at 17 points in SAT mode (`d1ev/cnf/c2_nolcup7_m17.cnf`, SHA-256
`0b755f7e…`, CaDiCaL 2.1.3 `--sat --seed=7`, unit `esr-agt-c2m17`, 03:13-03:22, about 80 CPU-s at 15 %): **no model**
(UNKNOWN; stopped to give the CPU to the ANCHOR-L test). HEURISTIC only.

## Claims and verdicts (as of 04:31)

| claim | statement (short) | label | verdict |
|---|---|---|---|
| `t1118-cupanchor` | F5; Lemma I(n); Theorem A; A1-A3 | PROVED (+ EXACT N = 7, 8) | VS CONFIRMED 03:13 (own enumeration, own controls) |
| `t1118-wd2n1` | weak D(5,n) through 2n − 1 | PROVED | VS CONFIRMED 03:21 |
| `t1118-lr2n2` | Theorem B: LR(n) through 2n − 2 | PROVED | VS CONFIRMED 04:02 |
| `t1118-vc16` | Lemma VC + add-on clauses for lc7_m16 | PROVED from CERTIFIED inputs | VB CONFIRMED 03:19 |
| `t1118-lexmirror16` | mirror lex-leader add-on for K1/K3 | PROVED | VS CONFIRMED 03:20 |
| `t1118-anchorl-data` | ANCHOR-L on all 614 hostile sets | EXACT | VS CONFIRMED 03:42 |
| `t1118-anchorl-strong-data` | STRONG ANCHOR-L and shorter cups; LR(7)@16 implication | EXACT + PROVED | VB CONFIRMED WITH CORRECTION 04:01 (item (d): the failing 3-cups pass through r; already corrected) |
| `t1118-anchorl-correction` | correction of item (d) | EXACT | VS CONFIRMED 04:00 |

## What remains (ranked for the next wave)

1. **ANCHOR-L(6) at 15 points** (`T/cnf/anchorl6_m15.cnf`): unit `esr-agt-anchorl6full` from 03:38:57 (CaDiCaL wall
   limit 07:58, then cake_lpr with a 500 MB heap). UNSAT + `s VERIFIED UNSAT` would CERTIFY ANCHOR-L(6) for all
   signotopes; if cake_lpr runs out of heap, re-run it on the kept proof with a larger heap (resume commands). At the
   wall limit the partial proof is kept as `*.partial.lrat.zst` (not a proof). Outcome: see the last status line.
2. **STRONG ANCHOR-L(6) sweep**: `T/tools/acl_driver.sh 6 15 5 …` over the 715 patterns (fast mode about 1.5-3
   CPU-hours; 8 done, all UNSAT), then the 286 patterns of 4-cups; then cert mode. A SAT pattern is a counterexample.
3. **n = 7, m = 16 patterns** (1,001 of 5-cups from l avoiding r): if they are UNSAT, the pieces C1 and K2 of the
   LR(7)-at-16 split are empty and K3 shrinks to 364 patterns (§4); feasibility unknown (no verdict in 50 s for one).
4. Proof ideas for anchoring (none yet); LR(n) at 2n − 1 by hand (the 2n − 2 argument of Theorem B does not extend
   directly: at 2n − 1 the A3 bound is n − 3 and Cor. 5 is not available).
5. Weak D(5,n) at |S| = 2n with longest cup n − 2 by hand (COMPUTED true at n = 6 by `anchor2n.py 6 12`).
6. Add-ons of §3 (VC, lex-leader) are ready for the D track; expected gain small.

## Resume

```bash
T=/home/jay/research/data/roadmap-20261115/pm1115/t1118; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
# §1 Lemma I / Theorem A (seconds; N = 9 about 150 CPU-s)
cd $T/tools && g++ -O2 -o sigenum sigenum.cpp && g++ -O2 -o local_lemmas local_lemmas.cpp && g++ -O2 -o taugons taugons.cpp
./local_lemmas 5; ./sigenum 7; ./sigenum 8; ./taugons 8 6; ./sigenum 9      # F5, Lemma I(6..8), tau for N = n+2
cd $T && $PY -I tools/t1lib.py && $PY -I tools/ctl_thmA.py ../t2size/out/all_sets.jsonl 2 7
$PY -I tools/ctl_thmA_rand.py 6 300 1; $PY -I tools/ctl_thmA_rand.py 7 150 2
# §2 negative results (models re-checked exactly)
$PY -I tools/c1allcups.py 6 13 60; $PY -I tools/check_c1allcups_model.py 6 13 "$(python3 -c "import json;print(json.load(open('models/c1allcups_6_13.json'))['signs'])")"
$PY -I tools/root2n2.py 6 10 > out/root2n2_6_10.json; $PY -I tools/check_root2n2_model.py out/root2n2_6_10.json
# §3 add-ons for LR(7) at 16 (numbering check inside vc16.py)
$PY -I tools/vc16.py ../d1ev/cnf/lc7_m16.cnf cnf/vc16_addon.cnf cnf/lc7_m16_vc.cnf
$PY -I tools/ctl_vc16.py cnf/vc16_addon.cnf ../r7/lns/f4.json ../r7/lns/f4b.json ../r7/lns/f6.json ../r7/root7_real17.json
for k in K1 K3; do $PY -I tools/lexmirror16.py ../dn/cnf/lr${k}_m16.cnf cnf/lexmirror16_${k}.cnf; done
$PY -I tools/ctl_lexmirror16.py cnf/lexmirror16_K3.cnf
# §4 anchoring data (each chunk < 1 min)
for st in 0 100 200 300 400 500 600; do $PY -I tools/anchor_l.py ../t2size/out/all_sets.jsonl $st 100; done
$PY -I tools/anchor_l_k2.py ../t2size/out/all_sets.jsonl out/hostile_idx.json i7 0 45 1 out/x.jsonl   # 5-cups, n = 7
# §4 ANCHOR-L(6) CNF, controls, solve + certificate (several CPU-hours at 15 %)
$PY -I tools/anchorl_cnf.py 6 15 > cnf/anchorl6_m15.cnf   # SHA-256 cbb00e49e1a9edab0fddb8816271e6edc4c32be9bcb55a1ea56c9f2a7578317a
$PY -I tools/ctl_anchorl.py 6 15 ../t2size/out/all_sets.jsonl 0,1,2 hostile
systemd-run --user --unit=esr-agt-anchorl6full -p CPUQuota=15% -p MemoryMax=600M -p MemorySwapMax=0 -p RuntimeMaxSec=<s> \
  --nice=10 --working-directory=$T -E OPENBLAS_NUM_THREADS=1 /bin/bash tools/cad_stream_cert.sh cnf/anchorl6_m15.cnf cert/anchorl6_m15b <wall_s> 500
# cake_lpr again on a kept proof with a larger heap (MemoryMax must exceed the heap):
#   f=cert/anchorl6_m15/anchorl6_m15; mkfifo $f.f2; (zstd -dc $f.lrat.zst | tee $f.f2 | sha256sum > $f.stream2.sha256) &
#   ~/.local/bin/cake_lpr --CML_HEAP_SIZE=2000 cnf/anchorl6_m15.cnf $f.f2 > $f.cake2.out; grep -cx 's VERIFIED UNSAT' $f.cake2.out
# pattern CNFs for STRONG ANCHOR-L: one K per call, e.g.
$PY -I tools/acl.py 6 15 ../d1ev/cnf/rc6_m15.cnf 1,2,5,13            # UNSAT in about 20 s at full CPU
$PY -I tools/acl.py 7 16 ../t3/cnf/rc7_m16.cnf 1,3,6,10 --write cnf/acl7_16_K0_1_3_6_10.cnf   # a 5-cup pattern at n = 7
# the n = 6 sweep (resumable; fast = no proof, cert = LRAT + cake_lpr; last argument = stop time as epoch seconds)
systemd-run --user --unit=esr-agt-acl6 -p CPUQuota=100% -p MemoryMax=600M -p MemorySwapMax=0 -p RuntimeMaxSec=<s> --nice=10 \
  --working-directory=$T /bin/bash tools/acl_driver.sh 6 15 5 ../d1ev/cnf/rc6_m15.cnf out/acl6_k5 300 fast 500 <stop_epoch>
# decode a model if the ANCHOR-L(6) run ends SAT
$PY -I tools/decode_anchorl_model.py 6 15 cert/anchorl6_m15/anchorl6_m15.cadical.log
```

## Addendum (main session, 18 Nov 10:57 KST): `anchorl6_m15.cnf` CERTIFIED

Track T's run `esr-agt-anchorl6full` ended with CaDiCaL UNSAT (7,470 s) and its LRAT kept, but its cake_lpr step failed
on heap exhaustion at the track's 500 MB heap ("CakeML heap space exhausted"). The main session re-ran cake_lpr on the
kept proof: unit `esr-vf-cakeanchor`, `--CML_HEAP_SIZE=4000`, the proof streamed from `anchorl6_m15.lrat.zst` through a
FIFO and re-hashed. Result: exactly one line `s VERIFIED UNSAT`, stream SHA-256 `137e155ac75f6ec7…` = the recorded
`anchorl6_m15.lrat.sha256`, CNF SHA-256 `cbb00e49e1a9edab0fddb8816271e6edc4c32be9bcb55a1ea56c9f2a7578317a`, 81 s, peak
RSS 4.1 GB (files `pm1115/t1118/cert/anchorl6_m15/recake1118/`). **Label: CERTIFIED for that CNF.** That the CNF encodes
ANCHOR-L(6) at 15 points rests on this record's encoding note and controls (claim `t1118-anchorl-data`, VS CONFIRMED);
no separate verifier has read the encoding.
