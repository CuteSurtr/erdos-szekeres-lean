# LP0 / LR by a counting-extremal route (track P2, 15 November 2026, 16:51-18:40 KST)

**Status (final, 17:50 KST).** No proof of LP0(6), LR(7) or weak D(5,7); **LP0(7) is FALSE for signotopes.** Results, each
with its claim and verifier verdict:

| # | result | label | claim / verdict |
|---|---|---|---|
| 1 | **LP0(7) fails at 19 points**: adding 2 points to any of the 10 known right-hostile 17-point blocks (108 position patterns) gives (5,7)-valid signotopes with r in no weak Δ (exhaustive count 0; also Lemma M) and up to 47 hexagons made of 4-cap end points, so P0 is not a weak Δ (§8). LR(7) and weak D hold on all of them (2,823-7,645 weak Δs through l). Realizability: R7's BFP run reports a non-realizability certificate for the example W (R7's work in `r7/lp0/`, not re-checked here); my LP placement over the two real blocks' own coordinates finds no realization of any model; point-set LP0(7) is open. | EXACT (abstract) | `lp0-7-false-abstract`, **CONFIRMED** (V2); correction note on the pattern count (108, not 45) |
| 2 | **Lemma A**: a gon whose first point ends a 4-cap has an upper chain of 3 or 4 points and (z, h2, h3) is a cup (z = third point of the 4-cap); every (n−1)-cup starts in P0 and ends in Q0; every gon inside R¹ has type (3, n−2) or (4, n−3) (§1-2). | PROVED (+ EXACT, 0 violations in 9,301 instances) | `p2-lemma-a`, **CONFIRMED** (V3) |
| 3 | Explicit witnesses for LP0 fail: P0 ∪ Q0 meets every gon (false, n = 8, real); Q0 plus points of P0 − Q0 (false, n = 7, real); a terminal-safe Δ of U (false, n = 6, real 15-point TS± set); a β-non-increasing Δ (false) (§4). | EXACT (real sets) | `p2-witness-refutations`, **CONFIRMED** (V2) |
| 4 | Conjecture H7 / H7U (*a gon made of 4-cap end points forces an ENV# Δ of U*) would have implied LP0; it held on 4,072 + 114 + 69 tested instances but **fails at n = 7** on the sets of item 1 (U = W − r, 18 points). **H7U(6) holds for |U| ≤ 12** (§3, §6). | CERTIFIED (12 points) / refuted at n = 7 | `h7u6-m12`, **CONFIRMED** (V2) |
| 5 | **The 10 known n = 7 right-hostile blocks are left-saturated**: no (5,7)-valid signotope contains a block and a point left of its leftmost point; so every valid superset keeps the block's leftmost point, and left-gluing tests on these blocks (T3's k ≤ 3 LR CNFs) are vacuous (§9). | CERTIFIED (10 CNFs) | `leftsat-r7blocks`, **CONFIRMED** (V3) |
| 6 | **LR(7) and TWO-ENV#(7) survive gluing near the known blocks**: CEGAR over every valid 2-point extension pattern of all 10 blocks for LR (1,360 patterns), of the two real blocks for TWO-ENV# (272), and the 56 early 3-point patterns of R7's block for both, finds no extension with l in no weak Δ, and none whose mirror side U′ = μ(W) − μ(l) lacks an ENV# Δ (every loop UNSAT after ≤ 19 resp. ≤ 10 cuts); on the 108 + 55 LP0 counterexample models the left ENV# side can be as thin as one Δ (§8). | COMPUTED (pysat verdicts; cuts sound, controls PASS) | — (not filed) |

What this means for the program: LP0 cannot serve as the induction statement for weak D(5,7) over signotopes (it may
still hold for point sets, or at 15-18 points); the end-point sparsity of the rooted failures is not forced by
hostility (adding two points makes R¹ large while r stays unrootable). LR and TWO-ENV# are untouched: every LP0(7)
counterexample found has l rootable. At n = 6 the construction has no room (15 = M(5;6) points), so LP0(6) stays open
only at 15 points.

Definitions as in THEORY_1115PM.md §0: signotope S on 0..m−1, σ(i,j,k) = + (cup) / − (cap), (5,n)-valid, gon = convex
(n−1)-set, weak Δ = 4-cap-free set meeting every gon, r = m−1, l = 0, U = S − r, P0 / Q0 = points ending / starting no
4-cap, R¹ = S − P0, L¹ = S − Q0, P4(U), ↑P4(U), ENV# Δ (ROUND6.md "Definitions"). Work directory (not in Git):
`/home/jay/research/data/roadmap-20261115/pm1115/p2/`.

## 1. Two signotope facts (PROVED)

Throughout, the signotope axiom: for every i < j < k < l the sequence σ(ijk), σ(ijl), σ(ikl), σ(jkl) changes sign at
most once. A 4-set is convex iff σ(ijk) = σ(ijl) and σ(ikl) = σ(jkl).

**F1 (caps are local).** p1 < … < pk is a cap iff every consecutive triple is a cap (same for cups).
*Proof.* If (a,b,c) and (b,c,d) are caps, the sequence σ(abc), σ(abd), σ(acd), σ(bcd) starts and ends with −, so with
at most one sign change it is constant: (a,b,d) and (a,c,d) are caps. Induction on the gap gives every triple. ∎

**F2 (convex = cap ∪ cup).** Let X = {x1 < … < xk}, k ≥ 3, and type(v) = σ(x1, v, xk) for x1 < v < xk.
(⇒) If X is convex, then H = {x1, xk} ∪ {type −} is a cap and K = {x1, xk} ∪ {type +} is a cup.
(⇐) If X = A ∪ B with A a cap, B a cup and A ∩ B = {x1, xk}, then σ(u,v,w) = type(v) for all u < v < w in X (with
type(x1), type(xk) never needed), so every 4-subset is convex.
*Proof.* (⇒) For interior u < v of the same type t, convexity of {x1, u, v, xk} gives σ(x1uv) = σ(x1uxk) = t and
σ(uvxk) = σ(x1vxk) = t; for interior u < v < w of type t, convexity of {u, v, w, xk} gives σ(uvw) = σ(uvxk) = t.
Together with σ(x1, v, xk) = t this covers every triple of H (t = −) and of K (t = +).
(⇐) For interior u < v the 4-set (x1, u, v, xk) has sequence (σ(x1uv), type(u), type(v), σ(uvxk)). If type(u) ≠
type(v) the single allowed change sits between places 2 and 3, so σ(x1uv) = type(u) and σ(uvxk) = type(v); if the types
agree, the same equalities hold because A is a cap and B a cup. For interior u < v < w the 4-sets (x1, u, v, w) and
(u, v, w, xk) have sequences (type(u), type(u), type(v), σ(uvw)) and (σ(uvw), type(v), type(w), type(w)); if type(u)
≠ type(v) the first forces σ(uvw) = type(v), if type(v) ≠ type(w) the second does, and if all three agree A or B gives
it. With the endpoint cases above, σ(u,v,w) = type(v) for every triple, so σ(pqs) = type(q) = σ(pqt) and σ(pst) =
type(s) = σ(qst) for every 4-subset p < q < s < t. ∎

For point sets both facts are elementary (a concave chain over a convex chain with common ends bounds a convex
polygon); the proofs above make Lemma A valid for abstract signotopes too.

## 2. Lemma A: gons whose first point ends a 4-cap (PROVED)

**Lemma A.** Let S be (5,n)-valid and G a gon with points g1 < … < g_{n−1}, upper chain H = (g1 = h1, h2, …, h_a =
g_{n−1}) and lower chain K = (g1 = k1, k2, …, k_b = g_{n−1}) as in F2(⇒), a + b = n + 1. Suppose g1 ends a 4-cap
(x, y, z, g1). Then
1. (z, g1, v) is a cup for every point v > g1 of S;
2. a ≥ 3, so G is not a cup; with no 5-cap, a ∈ {3, 4} and b ∈ {n−2, n−3};
3. (z, h2, h3) is a cup.

*Proof.* 1: if (z, g1, v) were a cap, (x, y, z, g1, v) would be a 5-cap by F1. 2 and 3: by 1, (z, g1, k2) is a cup
(k2 = g_{n−1} if b = 2), so B′ = (z, g1, k2, …, k_b) is a cup by F1. Let A′ = (z, h2, …, h_a). If a = 2, A′ = (z,
g_{n−1}); if a ≥ 3 and (z, h2, h3) is a cap, A′ is a cap by F1. In both cases A′ ∪ B′ = {z} ∪ G with A′ ∩ B′ = {z,
g_{n−1}}, so {z} ∪ G is convex by F2(⇐): a convex n-set, contradicting validity. Hence a ≥ 3 and (z, h2, h3) is a cup;
a ≤ 4 because H is a cap. ∎

**Mirror (A′).** If the last point g_{n−1} of a gon starts a 4-cap (g_{n−1}, x, y, z), then (v, g_{n−1}, x) is a cup
for all v < g_{n−1}, a ∈ {3, 4}, and (h_{a−2}, h_{a−1}, x) is a cup. (Apply Lemma A to the mirror image; μ keeps caps,
cups, convexity and upper chains.)

**Corollaries (PROVED).**
- A1. In a (5,n)-valid set every (n−1)-cup starts at a point of P0 and ends at a point of Q0.
- A2. Every gon contained in R¹ (or in L¹) has upper chain size 3 or 4: type (3, n−2) or (4, n−3).
- A3 (extension criterion used in the proof, PROVED the same way). For a gon G and a point v < g1, {v} ∪ G is convex
  iff [(v, g1, h2) cap and (v, k2, k3) cup] or [(v, g1, k2) cup and (v, h2, h3) cap] (a missing h3 or k3 makes that
  condition true). In a valid S neither holds for any v < g1.

**Checks (EXACT, own code `p2lib.py` with self-test against integer point-in-triangle convexity and the mirror;
`survey.py`).** Every one of the 58 distinct known sets (21 real ROOT(6) sets and their HIT models, the CEGAR models of
T1/R7 in `t4/cegarmodels/`, the real and abstract ROOT(7) sets, T3's models incl. tspm6_m15 and the AT/CONJ-TS′
controls, the TS± real set, attack 4's min_LR / min_LRB sets, R7's m16 seed), in both orientations (116 cases): every
pair (gon G, 4-cap ending at min G) satisfies 1-3. **0 violations in 9,301 instances.**

## 3. A sharper target: H7 and its U-only half H7U (refuted at n = 7 in §8)

*Written before §8. H7(7) and H7U(7) are false: the 19-point sets of §8 have 37 hexagons of U = W − r inside R¹(U)
and no ENV# Δ (r is unrootable). The tested instances below are all near the known hostile configurations, which is
why they missed it. H7U(6) is still open at 13-15 points (CERTIFIED for ≤ 12).*

**Lemma R (PROVED).** (a) If U has an ENV# Δ A, then A + r is a weak Δ of S (T4's L3, claim t4-lemmas, CONFIRMED).
(b) R¹(S) ∩ U = R¹(U), since a 4-cap ending at u < r lies in U. So a gon of S inside R¹(S) is either a gon of U inside
R¹(U) or contains r.

**H7(n) (CONJECTURE).** If some gon of a (5,n)-valid S lies inside R¹(S), then U = S − r has an ENV# Δ.
**H7U(n) (CONJECTURE).** If some gon of a (5,n)-valid set U lies inside R¹(U), then U has an ENV# Δ.

By Lemma R: H7(n) ⟹ LP0(n) ⟹ LR(n) ⟹ weak D(5,n), and H7(n) ⟺ H7U(n) ∧ H7-case-2(n), where case 2 = every gon
inside R¹(S) contains r. H7U is a statement about one set with no extension point in it. Contrapositive: *an
ENV#-hostile U has no gon made of 4-cap end points* — the end-point sparsity seen in all 45 rooted-failure order types
(there ENV#(U) = 0 and R¹(U) has 4 points at n = 6, 6 at n = 7). Since an ENV# Δ is rooted for every 5-cap-free
extension, H7U says the hostile configurations of THEORY §3 finding 3 can only occur over a U whose 4-cap end points
contain no gon. H7U(6) holds for |U| ≤ 11 because ENV#(6) does (claim env6-le11); 12-15 are open.

**Evidence (EXACT, own code; ENV# counts by exhaustive enumeration of subsets of U for |U| ≤ 17, pysat witness
otherwise, gons and caps from integer coordinates or sign strings).**

| test | instances with a gon inside R¹ | H7 / H7U violations | LP0 violations | script |
|---|---|---|---|---|
| H7 on the known sets and mirrors (m ≤ 17) | 54 | 0 | 0 | `h7sub.py 0` |
| H7 on all 1-point deletions (never r) | 681 (96 in case 2) | 0 | 0 | `h7run.py 1` → `h7k1.jsonl` |
| H7 on all 2-point deletions (never r) | 3,337 (1,147 in case 2) | 0 | 0 | `h7run.py 2` → `h7k2.jsonl` |
| H7U with U = S and U = S − r, all known sets incl. m = 18-25 | 114 (n = 6: 75, n = 7: 32, n = 8: 7) | 0 | — | `h7.py` → `h7_full.out` |

All these sets are subsets or mirrors of the program's counterexample sets, so the evidence is concentrated near the
known hostile configurations (HEURISTIC as evidence for the general statement).

**SAT test of H7U(6) (in progress).** CNF = round 6's universal ENV#(6)-failure CNF `env_cnf.py 6 m` plus T4's
"some gon consists of 4-cap end points" clauses (`t4/lp0_cnf.py`, applied with the triple variables of U; soundness: a
counterexample U satisfies the ENV# rows with canonical auxiliaries, and the added clauses with c4 = "is a 4-cap", e =
"ends a 4-cap", g = "is a gon inside R¹(U)"). Files `p2/h7u/h7u6_m{12,13,14}.cnf` (SHA-256 `2d7d8b04…`, `5f6f8db8…`,
`aa445fbf…`; ENV# parts `env6_m*.cnf`: `803a364d…`, `140b1cf0…`, `654d5705…`). **Controls PASS** (`h7u_control.py`,
`h7u_control2.py`): on all 72 distinct 14-point U from the known n = 6 sets (S − r, S − l, mirrors), the ENV# part with
fixed signs is SAT exactly when ENV#(U) = 0 (10 cases), the full CNF is SAT exactly when ENV#(U) = 0 and a gon lies in
R¹(U) (0 cases), and the CNF without the ENV# rows is SAT exactly when a gon lies in R¹(U) (25 cases). Run: unit
`esr-agq-p2-h7u6` (CPUQuota 15 %, MemoryMax 600 MB, until 18:28 at the latest), `certify_cnf.sh` with heap 400 MB, m =
12, 13, 14 in turn; results in `p2/h7u/cert/certify.jsonl`. Result: see §6.

## 4. Natural explicit witnesses that fail (EXACT; refuting sets are real point sets unless noted)

Each would have given LP0 (or LR) with an explicit Δ through r; each is false. Re-checked by plain enumeration in
`refute_check.py` → `refute_check.out.json`.

| statement | refuted by | detail |
|---|---|---|
| H4: P0 ∪ Q0 meets every gon (no gon consists of points that end and start a 4-cap) | min_LRB_n8 (attack 4, real, 25 points, n = 8), both orientations | 3 heptagons inside R¹ ∩ L¹, e.g. {8, 9, 12, 14, 16, 20, 21} with explicit witnesses; holds on all n = 6, 7 sets tested |
| H2: if P0 misses a gon, then Q0 ∪ X is a weak Δ for some X ⊆ P0 − Q0 | mirror of min_LR_n7 (real, 15 points, n = 7); also min_LRB_n7 (20 points) and min_LR_n8 / min_LRB_n8 | B = P0 − Q0 = {0, 2, 6}, Q0 = {1, 3, 8, …, 14}: none of the 8 sets Q0 ∪ X is a weak Δ; r is rooted, e.g. by {4, 12, 14} |
| H5 / H5U: a gon inside R¹(S) (or R¹(U)) gives a terminal-safe weak Δ of U | tspm6_real15 (T1's real TS± counterexample, 15 points, n = 6): U = S − r has the pentagon {3, 5, 6, 8, 12} inside R¹(U) and **0** terminal-safe weak Δs | so even the U-only form needs ENV# (here 730 ENV# Δs) rather than terminal safety; 473 other instances pass |
| H6: … gives a weak Δ of U whose cup ranks β are non-increasing (Lemma 1 / Theorem 2 of the DELTA3N structure record) | the mirrors of all 21 real ROOT(6) sets (and most mirrored CEGAR models) | β-non-increasing Δs: 0 |
| case 2 (every gon inside R¹ contains r): P0 + r or Q0 is a weak Δ | min_LR_n7, min_LRB_n7, min_LR_n8 (orientation 0) | neither works; H7 still holds there |
| TRIV (P0 or Q0 is a weak Δ) | already refuted (THEORY §1.3) | Q0 ∪ {l} also fails on the min_LR_n7 mirror (it is one of the 8 sets above) |

Also observed (EXACT): no simple rule built from the end layers works — L1 = R¹ − R², R¹, Q0 ∪ L1, Q0 ∪ R¹ are ENV#
Δs in 0/114 H7U instances; Q0 in 98/114; Q0 ∩ R¹ in 27/114.

## 5. Where the counting / extremal route stands (the gap)

- The Erdős–Szekeres cup–cap bound gives |P0| ≤ C(n, 2) (P0 is 4-cap-free with no n-cup) and Lemma A bounds the shape
  of R¹-gons, but no count of 4-caps, gons or layers forces a weak Δ through r: the obstruction sets of THEORY §3 are
  global (finding 5) and the tests of §4 show that every witness built from P0, Q0, end layers, cup ranks or terminal
  safety fails on some real set.
- The ENV# alternative (H7) looked like the surviving mechanism on 4,255 tested instances, but it is false at n = 7
  (§8), and so is LP0(7) itself. The reason a counting proof could not work: both "r unrootable" and "some gon lies
  inside R¹" are upward closed in valid supersets with the same r (Lemma M and monotonicity of R¹), so any hostile
  block with room for two well-placed early points becomes an LP0 counterexample. No statement of the form "hostility
  at r forces few 4-cap end points" can hold once the block can be extended.
- Lemma A survives (it does not involve r): it pins the shape of R¹-gons. In the 19-point counterexamples the R¹-gons
  are created by 4-caps starting at the two new early points ((1,2,3,·), (0,2,7,·)), consistent with Lemma A (the
  4-caps enter each gon's first point from below).
- n = 6 by hand: not reached. LP0(6) is open only at 15 points (ROOT(6) is CERTIFIED below); a hand proof would need a
  structure theory of 15-point (5,6)-valid sets that I do not have. LR(6) (CERTIFIED) was used only as a sanity target:
  every tested set satisfies LR.
- n = 7: LP0(7) is false for signotopes (§8); for point sets it is open (the example W is non-realizable by R7's BFP
  certificate; the other 107 models are being tested by R7). LR(7): every LP0(7) counterexample found has l rootable,
  and the hostile blocks are left-saturated (§9), so a two-sided failure built on a known block must keep the block's
  leftmost point. LR(7) at 15 remains COMPUTED (T1).

## 6. SAT run results

| CNF | vars / clauses | CaDiCaL | proof | cake_lpr (heap 400 MB) | label | claim |
|---|---|---|---|---|---|---|
| `h7u6_m12.cnf` (`2d7d8b04…`) | 3,587 / 41,001 | UNSAT, 117 s at 15 % quota | LRAT 200,796,177 B, `d5a10f6c…`, kept as `cert/h7u6_m12.lrat.zst` | **`s VERIFIED UNSAT`** (exactly one line), 46 s | **CERTIFIED** | `h7u6-m12` |
| `h7u6_m13.cnf` (`5f6f8db8…`) | 5,382 / 66,172 | **no verdict**: stopped by me at 17:37 after about 205 CPU-s (1.28 M conflicts) once H7U was refuted at n = 7 | partial LRAT `cert/h7u6_m13.lrat` (1.46 GB) is **not a proof**; left in place for the owner to delete | — | open | — |
| `h7u6_m14.cnf` (`aa445fbf…`) | 7,840 / 104,199 | not run | | | open | — |

So **H7U(6) holds for every (5,6)-valid signotope with at most 12 points** (≤ 11 from ENV#(6), claim env6-le11; 12
CERTIFIED here). Controls at 12 points: 60 random 12-point subsets of the known n = 6 sets, all three CNF parts agree
with the exact ENV# and R¹-gon computations (`h7u_control12.py`; none of them is ENV#-hostile, 7 have an R¹-gon).

Extra evidence for H7 (EXACT, `extra.py`): 77 further distinct sets of other tracks (R7's LNS / anneal / move / deletion
sets, T1's ext16 sets; 154 orientations): 69 instances with a gon inside R¹, H7 and LP0 hold in all (11 in case 2).

## 7. Order of events (KST)

16:51 start; 17:00-17:10 Lemma A, survey, refutations of explicit witnesses, H7/H7U data; 17:11-17:14 H7U(6) at 12
certified; 17:15-17:18 claims `p2-lemma-a`, `p2-witness-refutations`, `h7u6-m12` filed (all CONFIRMED by 17:26);
17:18-17:22 extension scan (written to look for LP0(7) counterexamples near the hostile blocks, after the H7 data
were all positive) finds the 19-point counterexamples; 17:25 claim `lp0-7-false-abstract` (CONFIRMED 17:26 by V2);
17:27 scan completed (108 patterns); 17:28-17:31 realization attempts over the real blocks' coordinates (none);
17:32-17:36 left-saturation certified, claim `leftsat-r7blocks` (CONFIRMED 17:38 by V3); 17:37 H7U(6) m = 13 run
stopped; 17:39-18:02 LR and TWO-ENV# CEGARs over the extensions (all UNSAT). Sections 3-5 were written before 17:20 and are kept
with the refutation marked.

## 8. LP0(7) is false for signotopes: 19-point counterexamples (EXACT; claim `lp0-7-false-abstract`)

**Idea.** Both properties in an LP0 failure are upward closed in valid supersets with the same rightmost point: r
unrootable (Lemma M) and "some gon lies inside R¹" (R¹ only grows when points are added, and gons stay gons). So a
right-hostile block B can be turned into an LP0 counterexample by adding points that create 4-caps ending at enough
old points, as long as the result stays (5,n)-valid. At n = 6 there is no room (every valid set has ≤ 15 points and
the blocks have 15), at n = 7 the blocks have 17 points and M(5;7) ≥ 26.

**Search** (`lp0ext.py`, `lp0scan.py`; pysat CaDiCaL): the 10 known n = 7 right-hostile blocks (R7's real
root7_real17, T1's real m17_it4_real, T3's root7_m17 and 7 CEGAR models; r unrootable re-checked by exhaustive count
before each scan), every position pattern of k new points (none right of r), CNF = signotope axiom, no 5-cap and no
convex 7-set on subsets meeting a new point, old triples fixed, plus "some 6-subset is convex and consists of 4-cap end
points". Controls: k = 0 gives UNSAT on the block and SAT on its mirror (48 R¹-hexagons, as in §2's survey).

| k | patterns | patterns with a valid extension | patterns with an LP0 counterexample |
|---|---|---|---|
| 1 | 170 (10 × 17) | 160 (no block can be extended to the left of l) | **0** |
| 2 | 1,530 (10 × 153) | 1,360 | **108** (10-13 per block, every block) |

Every one of the 108 models was re-checked exactly (`p2lib`: signotope axiom, no 5-cap, no convex 7-set, a hexagon
inside R¹, **0 weak Δs through r by exhaustive enumeration of 2^18 subsets**); LR holds on all of them (2,823-7,645
weak Δs through l, `lrcheck.py`), so weak D(5,7) holds on them too.

**Example W** (`lp0cex/w19_real17_oonn.json`, SHA-256 `834da5f8…`; independent brute-force check `verify_ext.py`):
R7's real block with two new points inserted after its second point (pattern `oonnooooooooooooooo`, new points 2, 3).
19 points, signotope axiom violations 0, 5-caps 0, convex 7-sets 0, 213 four-caps, 714 hexagons. P0(W) = {0, 1, 2, 3,
16, 17}; **47 hexagons lie inside R¹**, e.g. {4, 5, 9, 11, 12, 13} with 4-caps (1,2,3,4), (1,2,3,5), (0,2,7,9),
(1,2,3,11), (1,2,3,12), (0,2,7,13) ending at its points. Weak Δs through r = 18: **0**; through l: 5,833. The
sub-signotope on {0, 1, 4, …, 18} equals root7_real17. Two more patterns re-checked the same way:
`onnoooooooooooooooo` (2 R¹-hexagons, both avoiding r) and `oononoooooooooooooo` (21; 16 avoid r).

**Consequences.**
- **LP0(7) fails at 19 points** (abstract). LP0 cannot be the induction statement for weak D(5,7) for signotopes; it
  survives at n = 7 only if restricted to point sets (realizability open, below) or to |S| ≤ 18 (sizes 15-18 open; 17
  had T4's SAT probe without a model).
- **H7 and H7U fail at n = 7**: 37 of the 47 R¹-hexagons of the example avoid r, so U = W − r (18 points) has a gon
  inside R¹(U) and no ENV# Δ (an ENV# Δ would root r). §3's conjecture is refuted at n = 7; H7U(6) ≤ 12 (CERTIFIED,
  claim h7u6-m12) is unaffected.
- The mechanism: two points placed early (between the block's first old points) become the first points of many new
  4-caps ((1,2,3,·), (0,2,7,·)), which turns most of the block into 4-cap end points without creating a 5-cap or a
  convex heptagon. The hostility at r (Lemma M) is untouched. LR survives because l stays rootable.
- At n = 6 the construction has no room (blocks have M(5;6) = 15 points), so LP0(6) remains open at 15 and the n = 6
  picture of THEORY §1.5 is unchanged.

**Further checks on the counterexamples (EXACT for the listed models).**
- TWO-ENV#(7) holds on all 108 models: ENV#(W − r) = 0 (as it must) but the mirror side ENV#(μ(W) − μ(l)) ≥ 1 — and
  the minimum is exactly 1 (`twoenv_check.py`), so the left side is thin on some of them.
- k = 3, new points in the early gaps 1-6 of R7's real block (`GAPMAX=6`, `lp0scan_k3_early.jsonl`): 55 of 56 patterns
  give 20-point LP0(7) counterexamples; on these 55 models the left-side ENV# count is again ≥ 1 (minimum 1) and LR
  holds (`twoenv_k3.py`). 165 further sampled 20-point valid extensions (`lrsample.py`, not required to be LP0
  counterexamples; 27 of them are): fewest weak Δs through l 3,426, fewest left ENV# Δs 1 — no LR or TWO-ENV#
  failure (HEURISTIC as a search: sampled models only).

**LR CEGAR (COMPUTED; `lrcegar.py`).** For W = block + new points (pattern fixed, block signs fixed, validity
clauses as in `lp0ext.py`), the loop asks the solver for W, finds a weak Δ D through l in W (pysat), shrinks D
greedily, and adds the cut "some 4-subset of D is a 4-cap, or some 6-subset of W − D is convex" (one-way indicator
variables; every W′ in which D is not a weak Δ satisfies it, so the cuts are sound and UNSAT means no W with l
unrootable). Controls: with the root set to r the loop reports the hostile block's extensions as failures at once,
and from R7's block minus point 5 (r rootable) it re-creates an r-hostile 17-point set after 2 cuts. Results: all 136
extendable 2-point patterns of each real block (272 runs, ≤ 9 cuts) and all 56 early 3-point patterns of R7's block
(≤ 19 cuts) are UNSAT, and so are all 1,088 extendable 2-point patterns of the 8 abstract blocks (≤ 11 cuts,
`cegar_batch.py` → `lrcegar_abs_k2.jsonl`): **no LR(7) failure among the 2-point extensions of any known block** (`lrcegar_k2.jsonl`, `lrcegar_k3.jsonl`).

**TWO-ENV# CEGAR (COMPUTED; `twoenvcegar.py`).** Same loop with the left side of TWO-ENV#: for the model W it computes
an ENV# Δ A of U′ = μ(W) − μ(l) exactly (4-caps, 3-caps ending outside ↑P4(U′), gons), shrinks it and adds the cut
"some 4-subset of A is a 4-cap, or some 6-subset of U′ − A is convex, or some 3-cap (a,b,c) of A has (b,c) outside u′",
with u′ ⊇ P4(U′) and u′ up-closed under the pair order (the canonical u′ = ↑P4(U′) satisfies them, so the cut is sound;
ENV#(W − r) is empty automatically since r is unrootable). Controls: on the mirrored real block the empty left side
is reported at once (right side 3,826 ENV# Δs), and from the mirrored block minus point 10 the loop re-creates an empty
left side after 4 cuts. Results: all 272 two-point patterns of the real blocks (≤ 7 cuts) and the 56 early three-point
patterns (≤ 10 cuts) are UNSAT: **no TWO-ENV#(7) failure among these extensions** (`twoenvcegar_k2.jsonl`,
`twoenvcegar_k3.jsonl`).

**Realizability (search only; nothing claimed).** For the two real blocks, every model of every one of their 21
counterexample patterns was enumerated (77-3,276 models per pattern, blocking the signs of triples with a new point)
and the new points were placed one at a time by an LP on the orientation constraints over the block's own
coordinates (`realize_lp.py`; HiGHS as a guide; any hit re-checked in integers). In **no** model does the first new
point fit into the line arrangement of the block (positive control: removing two points of the mirrored real set and
re-placing them succeeds after 176 models). So these extensions are not realizable **over these two coordinate
realizations of the blocks**; other realizations of the same order types are not excluded. R7's
`r7/tools/lp0_bfp_batch.py` (BFP non-realizability certificates for these models) was started by R7 on my scan file;
its outcome decides whether LP0(7) can still hold for point sets. At 17:29 R7's run reported a BFP certificate
without the point at infinity for the example W (`r7/lp0/bfp_oonn_full_noV.json`, model SHA `a0e6cecd…`, which is
the model V2 checked): if R7's exact re-verification confirms it, W is not realizable at all; I did not re-check it.
Two more heuristics from my side: (i) the 3-point early patterns behave the same over the real block (6 patterns,
2,443-3,282 models each, first new point never placeable); (ii) random real single-point insertions into R7's real
block keep (5,7)-validity only in its gap 15 (3 of 40 samples; 0 of 40 in each of gaps 1-5, 7-14 and 16; gap 6 has no integer x; `gapmap.py`), so
the real realization is almost saturated although every gap 1-16 admits an abstract valid insertion.

## 9. Left-saturation of the known n = 7 hostile blocks (CERTIFIED; claim `leftsat-r7blocks`)

The k = 1 and k = 2 scans of §8 showed that exactly the position patterns with a new point to the left of l admit no
valid extension (10/10 and 170/170; every other pattern is extendable). Certified directly: for each of the 10 blocks
the CNF "block + one point left of min B, (5,7)-valid" (`leftsat_cnf.py`, the validity part of `lp0ext.py`) is UNSAT,
CaDiCaL LRAT + cake_lpr **`s VERIFIED UNSAT`** (10/10, proofs about 0.2 MB each, kept in `p2/leftsat/cert/`, hashes in
`certify.jsonl`). Controls: the mirror image of root7_real17 (left-hostile) and root7_real17 minus its leftmost point
both give SAT.

Consequences (PROVED from the certificates): every (5,7)-valid superset W of one of these blocks B has min W = min B
(else B plus that point would be a valid subset of W). Hence (a) T3's gluing CNFs that add k ≤ 3 points to the left of
the three 17-point blocks were UNSAT for this reason alone and say nothing about LR; (b) an LR(7) failure containing a
known block has l(W) = l(B), where l is rooted by thousands of weak Δs inside B. CONJECTURE (tested only on these 10
blocks, which share one mechanism): every right-hostile (5,n)-valid set is left-saturated. Even if true it does not
give LR by itself (in an LR failure W it only forces r to be rootable in W − l and l in W − r).

## 10. Files (work directory `/home/jay/research/data/roadmap-20261115/pm1115/p2/`, not in Git)

`p2lib.py` (exact toolkit + self-test), `survey.py` (LP0 data, Lemma A check) → `survey.jsonl`; `hyp.py` (H2, H4),
`h5.py` (H5, H6), `h5u.py` (H5U), `h7.py`, `h7sub.py`, `h7run.py`, `extra.py` (H7, H7U) → `h7_full.out`, `h7k1.jsonl`,
`h7k2.jsonl`; `envcand.py`, `case2.py`, `classes.py`, `gonstats.py`, `wtest.py` (explicit-witness and shape tests);
`refute_check.py` → `refute_check.out.json`; `h7u/` (CNFs, `drive.sh`, `cert/`; controls `h7u_control.py`,
`h7u_control2.py`, `h7u_control12.py`); **LP0(7) counterexamples**: `lp0ext.py` (extension CNF), `lp0scan.py` →
`lp0scan_k1.jsonl`, `lp0scan_k2.jsonl` (every model's sign string is in the SAT rows), `verify_ext.py` (brute-force
re-check) → `lp0cex/w19_real17_*.json`, `lrcheck.py` (LR on the 108 models), `realize_lp.py` (LP placement over the real
blocks; control output `lp0cex/control_realized_mirror_block15_oonn*.json`), `real_sat_patterns.txt`, `real_sat_k3.txt`,
`lp0scan_k3_early.jsonl`, `twoenv_check.py`, `twoenv_k3.py`, `lrsample.py`, `gapmap.py`; LR CEGAR `lrcegar.py` →
`lrcegar_k2.jsonl`, `lrcegar_k3.jsonl`; TWO-ENV# CEGAR `twoenvcegar.py` → `twoenvcegar_k2.jsonl`, `twoenvcegar_k3.jsonl`; batch driver `cegar_batch.py` →
`lrcegar_abs_k2.jsonl` (`abs_patterns_k2.txt`) (pattern lists `lr_patterns_k*.txt`; controls `lp0cex/control_rootr_*.json`); **left
saturation**: `leftsat_cnf.py`, `leftsat/` (CNFs, controls, `cert/certify.jsonl`, proofs); claim JSONs in `claims/`.

Reproduce (one thread, each under a minute):

```bash
P2=/home/jay/research/data/roadmap-20261115/pm1115/p2; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd $P2 && OPENBLAS_NUM_THREADS=1 $PY p2lib.py                 # self-test
OPENBLAS_NUM_THREADS=1 $PY -I survey.py /tmp/s.jsonl            # Lemma A on all known sets (prints 'A 0 N' per case)
OPENBLAS_NUM_THREADS=1 $PY -I refute_check.py                   # the refutations of section 4
OPENBLAS_NUM_THREADS=1 $PY -I h7u_control.py 14                 # CNF controls
OPENBLAS_NUM_THREADS=1 $PY -I verify_ext.py $B/r7/root7_real17.json 7 oonnooooooooooooooo /tmp/w.json  # LP0(7) cex
OPENBLAS_NUM_THREADS=1 $PY -I lp0scan.py 2 /tmp/k2.jsonl 50     # resumable scan (about 5 x 50 s for all 10 blocks)
OPENBLAS_NUM_THREADS=1 $PY -I leftsat_cnf.py $B/r7/root7_real17.json 7 /tmp/ls.cnf && cadical -q /tmp/ls.cnf; echo $?  # 20
```
(`B=/home/jay/research/data/roadmap-20261115/pm1115`.)
