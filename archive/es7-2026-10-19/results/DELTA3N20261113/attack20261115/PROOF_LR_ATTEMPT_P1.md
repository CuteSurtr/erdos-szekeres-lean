# LR(n) proof attempt (track P1, 15 November 2026, 16:52-18:40 KST)

**Status (18:34 KST, final; all P1 units finished).** LR(7) remains OPEN; no proof of LR(n) for any n >= 7 is claimed, and no ES bound changes.
What this track adds:

- **PROVED** (complete proofs in §2; Lemmas G, G2, A1, Q and E also checked exactly on 164 instances, 0 failures):
  - Lemma G (a 4-cap ending at the leftmost point of a convex set extends its lower chain by one point), Corollary G2
    (every gon contains a point that ends no 4-cap or a point that ends an (n−2)-cup; a gon whose leftmost point ends a
    4-cap has an upper chain of 3 or 4 points and its rightmost point ends an (n−1)- resp. (n−2)-cup), Corollary SD
    (Lemma SD, both sides, as the case "no (n−2)-cup"), Lemma A1 (a point that starts an (n−1)-cup ends no 4-cap) and
    Proposition R (LR(n) follows from two one-sided statements C1(n), C2(n)): claim `p1-cupext`, **CONFIRMED by V2**.
  - Lemma Q (the top β-level starts no 4-cap): claim `p1-lemmaq`, **CONFIRMED by V3** (V3 noted that the proof gives
    T ⊆ Q0, so the filed wording "Q0 ∪ T is 4-cap-free" says no more than that).
  - Lemma E (a cup ending at a point that starts a 4-cap extends by one point) and C2\*(n) ⟹ C2(n), where C2\* = "r
    unrootable ⟹ some (3,n−2)-gon through l has its right end starting a 4-cap" (C2\* holds on all 14 known ROOT(7)
    failure types and fails on all 138 known ROOT(6) failure types): claim `p1-lemmae` (with Part B below),
    **CONFIRMED by V2** (`VERIFY_P1_LEMMAE.md`).
- **Refuted (EXACT):** ISO-ROOT, a normal form proposed here at 17:31 ("a rootable r lies in a weak Δ whose β-values
  are nondecreasing"), fails for a real 17-point (5,8)-valid set (claim `p1-lemmae`, Part B, CONFIRMED by V2 with its own code). The unrooted form ISO
  survives all 2,566 tested instances (CONJECTURE).
- **C2(6) holds for every signotope (CERTIFIED at 15 points by my own cake_lpr run; claim `p1-c2six` filed 18:19,
  independent re-run pending):**
  CaDiCaL proved `c2_nolcup6_m15.cnf` UNSAT (T3's compact ROOT(6) CNF at 15 points, which regenerates byte-identically,
  plus "l starts no 5-cup"; 329 CPU-s, LRAT kept as zstd, `p1/c2_nolcup6_m15.lrat.zst`). So every 15-point ROOT(6)
  failure has α(l) = 5 (even without assuming that l starts a 4-cap); with ROOT(6) CERTIFIED ≤ 14 and 16 points vacuous,
  C2(6) holds for all signotopes (the cake_lpr check below passed). C1(6) is not yet decided (SAT mode only, no model in
  180 CPU-s), so the n = 6 instance of Proposition R is half done.
  cake_lpr (heap 480 MB, the most my 600 MB unit allows; unit `esr-agq-p1-cake`, 18:17-, output `p1/c2cake/`):
  **`s VERIFIED UNSAT`** (exactly one line), 18:21:15, wall 3 min 54 s, max RSS 495 MB; LRAT SHA-256 recomputed while
  streaming `0b5745db…` and CNF SHA-256 `1d703c4c…`, both equal to the recorded values. The proof stays kept as zstd.
- **CONJECTURE** (new, explicit): **STAIR-LR(n)**: "a β-staircase through r or an α-staircase through l is a weak Δ"
  (a staircase takes whole intervals of β-levels in increasing order; §1). It implies LR(n), is checkable without subset
  enumeration, and holds on every tested set: all 738 (n, type) pairs of the broad scan (152 rooted failures included)
  and 2,721 prefix instances of real (5,7)- and (5,8)-valid pool sets (EXACT). Its one-sided half STAIR-C1 (§1) is the
  explicit form of C1.
- **CONJECTURE** (new, tested): **C1(n)** "if r ends a 4-cap and an (n−1)-cup, r lies in a weak Δ" and **C2(n)** "if
  r ends a 4-cap, l starts a 4-cap and r lies in no weak Δ, then l starts an (n−1)-cup". Together they give LR(n)
  (Proposition R). **EXACT: both hold on all 110 distinct known order types** (n = 6, 7; real and abstract; every
  set and its mirror image), including all 34 ROOT(6) and 12 ROOT(7) failure types, and in a broad scan of all 531 set
  files of the team (738 distinct (n, type) pairs, 152 distinct r-unrootable types: 138 at n = 6, 14 at n = 7). **COMPUTED: no counterexample in
  the neighbourhood of any known rooted failure** (re-signing every triple through the moved end point and up to three
  further points (four at n = 6 for C2): 75,740 SAT calls, all UNSAT; 4,090 positive controls, all SAT and re-checked
  exactly; §4). **HEURISTIC:** CaDiCaL in SAT mode found no C2(6) and no C1(6) counterexample at 15 points in 180 CPU-s
  each (plain ROOT(6) at 15: a model in 13 s).
- **The gap** (§5): no mechanism is known that produces a weak Δ through an end point that starts (ends) an
  (n−1)-cup (C1), nor one that forces an (n−1)-cup at l from the unrootability of r (C2; C2(6) is now known by a
  certificate, not by an argument). The only structural
  rooting theorem (DELTA3N Theorem 2) works in the opposite regime (no (n−2)-cup), and the explicit candidates (Q0,
  β-levels plus r, β-antitone sets) fail to explain C1 on 4 of the 58 known order types with an (n−1)-cup at r.
  Staircases (β-isotone unions of whole level intervals) do work on every tested set, so the open core is a combinatorial
  statement: for a suitable choice of n−2 cut points the staircase is 4-cap-free and meets every gon (STAIR-C1 on one
  side, STAIR-LR two-sided). No argument for the existence of a good cut vector is known, and no canonical cut rule
  works on all sets.

Labels: PROVED (complete written proof here), EXACT (own exhaustive code on the named sets), COMPUTED (solver verdict),
HEURISTIC, CONJECTURE. Work directory (not in Git): `/home/jay/research/data/roadmap-20261115/pm1115/p1/`.

## 0. Definitions

As in THEORY_1115PM.md §0. S is a signotope on 0..m−1 (increasing x); '+' = cup, '−' = cap; k-cap / k-cup: every
triple a cap / cup. Convex set: every 4-subset x<y<z<w has σ(xyz) = σ(xyw) and σ(xzw) = σ(yzw). (5,n)-valid: no 5-cap
and no convex n-set. Gon: convex (n−1)-set. Weak Δ: 4-cap-free set meeting every gon. r = m−1, l = 0, U = S − r,
V = S − l. "p is rootable": some weak Δ of S contains p.

- R¹ = points that end a 4-cap, P0 = S − R¹ (l ∈ P0); L¹ = points that start a 4-cap, Q0 = S − L¹ (r ∈ Q0). P0 and Q0
  are 4-cap-free.
- β(v) = number of points of a longest cup ending at v (β ≥ 1); α(v) = same for cups starting at v. B_j = {β = j},
  A_j = {α = j}, E2 = {β ≥ n−2}, F2 = {α ≥ n−2}. Since S has no n-cup (an n-cup is a convex n-set), β, α ≤ n−1.
- Mirror μ: i ↦ m−1−i, keeps caps, cups, convexity, hence weak Δs; it swaps (r, β, R¹, P0) with (l, α, L¹, Q0).
- **Chains of a convex set.** For a convex set H with leftmost h and rightmost e, the upper chain is
  {h, e} ∪ {u : σ(h,u,e) = −} and the lower chain is {h, e} ∪ {w : σ(h,w,e) = +}; the upper chain is a cap and the
  lower chain a cup (standard characterization of convex sets in signotopes; also checked exactly on all 47,832 gons of
  the sets in §3). k = |upper chain|, t = |lower chain|, k + t = |H| + 2. No 5-cap gives k ≤ 4.
- **Consecutive rule.** In a signotope, a sequence x_1 < ... < x_s whose consecutive triples (x_i, x_{i+1}, x_{i+2})
  are all caps (all cups) is a cap (a cup). (For a 4-tuple p<q<s<t the sign sequence σ(pqs), σ(pqt), σ(pst), σ(qst)
  changes sign at most once, so σ(pqs) = σ(qst) forces all four equal; induct on the gap.)

## 1. Results at a glance

| item | statement | label | evidence |
|---|---|---|---|
| Lemma G | 4-cap (a,b,c,h) at the leftmost point h of a convex set H ⟹ (c) + lower chain of H is a cup, and (c, h, u₂) is a cup | PROVED | §2; EXACT on 11,300 (gon, 4-cap) pairs, 0 failures |
| Cor. G2 | in a (5,n)-valid S, a gon H ⊆ R¹ has k ∈ {3,4} and its rightmost point e has β(e) ≥ n+2−k (= n−1 if k = 3); hence every gon meets P0 ∪ (E2 ∩ R¹); mirror: every gon meets Q0 ∪ (F2 ∩ L¹) | PROVED | §2; EXACT on all 47,832 gons of 164 sets (S and mirrors), 0 failures |
| Cor. SD | no (n−2)-cup ⟹ P0 and Q0 are weak Δs (Lemma SD of VERIFICATION P3, both sides) | PROVED (new short proof) | special case of G2 |
| Lemma A1 | a point starting an (n−1)-cup ends no 4-cap (A_{n−1} ⊆ P0); mirror B_{n−1} ⊆ Q0 | PROVED | §2; EXACT on 164 instances (1,046 points with α or β = n−1), 0 violations |
| Prop. R | C1(n) ∧ C2(n) ⟹ LR(n) (⟹ weak D(5,n) by T4's L1) | PROVED | §2 |
| Lemma Q | no 5-cap ⟹ the top β-level T starts no 4-cap (T ⊆ Q0; V3's sharpening of the filed wording "Q0 ∪ T is 4-cap-free"); so if S has no (n−1)-cup, B_{n−2} ⊆ Q0 and A_{n−2} ⊆ P0 | PROVED (claim p1-lemmaq CONFIRMED by V3) | §2; EXACT on 164 instances (`qe_check.py`); it adds nothing to Q0 / P0 as witnesses: on `triv6_m10` (no 5-cup) Q0 = Q0 ∪ B_4 and P0 = P0 ∪ A_4 both miss a gon |
| Lemma E | a cup ending at a point that starts a 4-cap extends by one point; longest cups from any point end in Q0 | PROVED | §2; EXACT on 164 instances, 0 failures (`qe_check.py`) |
| C2\* ⟹ C2 | C2\*: r unrootable ⟹ a (3,n−2)-gon through l has its right end in L¹ | PROVED (implication); C2\* holds on all 14 ROOT(7) failure types and is false on all 138 ROOT(6) failure types of the broad scan (EXACT) | §2, `c2star.py` |
| C1(n) | r ends a 4-cap and an (n−1)-cup ⟹ r rootable | CONJECTURE | EXACT on 110 types: 58 types have β(r) = n−1, r rootable in all; no violation in the broad scan (738 (n, type) pairs) |
| C2(n) | r unrootable (r ends, l starts a 4-cap) ⟹ l starts an (n−1)-cup | CONJECTURE | EXACT on 110 types: r unrootable in 46 types (34 at n = 6, 12 at n = 7), α(l) = n−1 in all; broad scan: all 152 r-unrootable types (138 at n = 6, 14 at n = 7) |
| C3(n) | S has no (n−1)-cup ⟹ r rootable (consequence of C2) | CONJECTURE | only 2 known sets lack an (n−1)-cup |
| **STAIR-C1(n)** (new; explicit form of C1) | if r ends a 4-cap and an (n−1)-cup, then for some cut points −1 = c₀ ≤ c₁ ≤ ... ≤ c_{n−2} ≤ c_{n−1} = r the **staircase** D = ⋃_j {v : β(v) = j, c_{j−1} < v ≤ c_j} (a β-isotone union of whole level intervals; it contains r) is a weak Δ | CONJECTURE | EXACT (`stair.py`, `stair2.py`, `stairpool.py`): holds in all 58 known types and all 219 broad-scan types with β(r) = n−1, in all 719 instances (prefixes of 13-22 points, both sides) of the real (5,7)-valid pool and all 154 instances (14-24 points) of the real (5,8)-valid pool with β(r) = n−1 and r ending a 4-cap. A working staircase never needs more than 4 levels (2 in 120 of the 219 scan types, `stair3.py`); cutting at the points of an (n−1)-cup ending at r works in only 30 of the 219, the canonical choices "B_{n−1} plus the part of B_{n−2} left of min B_{n−1}" in 98 and "each level up to the first point of the next" in 12 (`cupstair.py`, `stair4.py`): the cut vector has to be searched. The two envelope staircases (left-to-right β-records; right-to-left β-minima) meet every gon in all 219 types but contain a 4-cap in 207 resp. 219 of them (`stair5.py`): meeting the gons is easy, 4-cap-freeness is the binding constraint. With β(r) < n−1 the staircase rule can fail (min_LRB_n7, β(r) = n−2, r rootable) |
| ISO-ROOT(n) (new, **refuted at n = 8**) | if r lies in a weak Δ, it lies in a **β-isotone** weak Δ (β nondecreasing from left to right); mirror: l in an α-antitone one | **FALSE** for n = 8 (EXACT; claim p1-lemmae Part B, CONFIRMED by V2) | Counterexample: a real 17-point (5,8)-valid set (independent check `verify_isocex.py`: prefix of pool set 2 of DELTA3N `real_pool/full-n8.pool`, saved as `p1/isoroot8_cex_2_17_prefix.json`; β(r) = 3, r lies in the weak Δ {8, 15, 16} (β = 4, 6, 3), but no subset of {β ≤ 3} = {0,1,2,4,6,7,16} containing r is a weak Δ); 7 of the 776 prefix instances of that pool fail (`isopool8.py`), all with β(r) ∈ {2, 3, 4} (`isofind8.py`), so the restriction of ISO-ROOT to β(r) = n−1 (a strengthening of C1 with a β-isotone witness) survives. No failure at n = 6, 7 in the sets below; positive data at n = 6, 7: EXACT (`iso.py`, `iso2.py`): holds in all 64 types where r is rootable, although β-isotone sets are only 2-16 % of the rooted weak Δs (median 15 %); also on 1,680 instances from real (5,7)-valid pool sets (15- and 16-point prefixes and mirrored suffixes of 480 sets of `round6/envroot/pool_valid.jsonl`; `isopool.py`), all rootable |
| **STAIR-LR(n)** (new; explicit two-sided rule, implies LR(n)) | some β-staircase through r (cuts −1 = c₀ ≤ ... ≤ c_{β(r)} = r, D = ⋃_{j ≤ β(r)} {v : β(v) = j, c_{j−1} < v ≤ c_j}) or some α-staircase through l (the same in the mirror image) is a weak Δ; at most C(m+n−3, n−2) candidates per side, so it is checkable without subset enumeration | CONJECTURE | EXACT (`stairlr.py`, `stairlrpool.py`): holds on all 738 broad-scan (n, type) pairs (the β-staircase through r alone fails on 180 of them: the 152 rooted failures and 28 sets in which r lies only in non-staircase weak Δs), on 1,945 prefix instances (13-18 points) of the real (5,7)-valid pool (β-staircase through r works in all) and on 776 prefix instances (14-17 points) of the real (5,8)-valid pool (β-staircase through r fails in 4, the α-staircase through l works there); also on attack 4's two n = 8 TRIV-failure sets `min_LR_n8` (18 points) and `min_LRB_n8` (25 points), where the β-staircase through r works (`stairone.py`). Also on 1,408 random (5,6)-valid 10-point sets and 1,343 random (5,7)-valid 12-point sets (integer coordinates, LR hypothesis; `stairrand.py`; weak evidence, random sets are easy). Not tested on the ETV extremal sets (their coordinates were not at hand in `t4/etv/`, and 26-42 points need a faster checker) |
| **ISO(n)** (new) | every (5,n)-valid set has a β-isotone weak Δ (a sharpening of weak D) | CONJECTURE | EXACT (`iso3.py`, `isopool.py`, `isopool8.py`): all 110 types (β-isotone: 2.8-17 % of all weak Δs, median 17 %), the 1,680 n = 7 pool instances and all 776 n = 8 pool prefix instances (16 and 17 points, both sides) |
| neighbourhoods | no C1/C2 counterexample agrees with a known rooted failure outside the triples through the moved end point and k ≤ 3 further points (k ≤ 4 for C2 at n = 6) | COMPUTED | §4 (75,740 UNSAT calls) |
| C2(6) at 15 points, SAT mode | no model in 180 CPU-s | HEURISTIC | §4 |
| **C2(6)** (all signotopes) | UNSAT at 15 points (default mode), ≤ 14 by ROOT(6), 16 vacuous | **CERTIFIED** (cake_lpr exact line, own run; claim p1-c2six, independent re-run pending) | §4, `p1/c2cake/` |
| C1(6) at 15 points, SAT mode | no model in 180 CPU-s | HEURISTIC | §4 |
| blockers | in every rooted failure (46 types) r becomes rootable once the gons containing l are ignored; ignoring only the (n−1)-cups at l is not enough in 30 of the 46 types (all 12 at n = 7), ignoring only the (3,n−2)- and (4,n−3)-gons at l is | EXACT | `blockers.py` |

Supporting EXACT facts on the known rooted failures (from `prof_all.jsonl` and the broad scan): β(r) = 4 in all 152
rooted-failure types (= n−2 at n = 6, = n−3 at n = 7), α(l) = n−1, and at n = 7 every 6-cup of R7's real set starts at
l (8 of 8); in all 21 real ROOT(6) sets l starts exactly 9 five-cups, all ending at r − 1. Whether "r unrootable ⟹
β(r) = 4" has a reason (or is an artefact of the sizes 15 and 17 reached so far) is open; no n = 8 rooted failure is known.

## 2. Lemmas and proofs

**Lemma G (cup extension at a 4-cap end).** Let S be a signotope with no 5-cap, H ⊆ S convex with |H| ≥ 3, leftmost
point h, rightmost point e, lower chain h = w₁ < ... < w_t = e and upper chain h = u₁ < ... < u_k = e. If (a,b,c,h) is a
4-cap of S, then (i) c, w₁, ..., w_t is a (t+1)-cup ending at e, and (ii) (c, h, u₂) is a cup.

*Proof.* (i) t ≥ 2. If (c, h, w₂) were a cap, the consecutive triples (a,b,c), (b,c,h), (c,h,w₂) would all be caps, so
(a,b,c,h,w₂) would be a 5-cap by the consecutive rule. So (c, w₁, w₂) is a cup; every other consecutive triple of
(c, w₁, ..., w_t) lies in the cup (w₁, ..., w_t). By the consecutive rule the sequence is a cup. (ii) The same argument
with u₂ in place of w₂ (k ≥ 2). ∎

The mirror statement: if (e, x, y, z) is a 4-cap starting at the rightmost point e of H, then w₁, ..., w_t, x is a
(t+1)-cup starting at h, and (u_{k−1}, e, x) is a cup.

**Corollary G2.** Let S be (5,n)-valid and H a gon (k + t = n + 1). If every point of H ends a 4-cap (H ⊆ R¹), then
k ∈ {3, 4} and β(e) ≥ t + 1 = n + 2 − k for the rightmost point e of H; in particular β(e) = n − 1 if k = 3 and
β(e) ≥ n − 2 if k = 4. Consequently every gon meets P0 ∪ (E2 ∩ R¹). Mirror: if every point of H starts a 4-cap, then
k ∈ {3,4} and α(h) ≥ n + 2 − k for the leftmost point h; every gon meets Q0 ∪ (F2 ∩ L¹).

*Proof.* The leftmost point h of H ends a 4-cap (a,b,c,h). By Lemma G(i), (c, w₁, ..., w_t) is a (t+1)-cup ending at
e. (Only this is used, so the first sentence holds for every gon whose leftmost point ends a 4-cap; V2's remark.) S has no n-cup, so t + 1 ≤ n − 1, i.e. t ≤ n − 2 and k = n + 1 − t ≥ 3; k ≤ 4 because the upper chain is a cap. And
β(e) ≥ t + 1. If H misses P0 then H ⊆ R¹, so e ∈ R¹ and β(e) ≥ n − 2: H meets E2 ∩ R¹. The mirror statement is the same
proof applied to μS. ∎

**Corollary SD.** If a (5,n)-valid S has no (n−2)-cup, then P0 and Q0 are weak Δs (P0 through l, Q0 through r).

*Proof.* E2 = F2 = ∅, so by G2 every gon meets P0 and every gon meets Q0; both sets are 4-cap-free (a 4-cap inside
P0 would end at a point of P0; a 4-cap inside Q0 would start at a point of Q0). ∎ (This is Lemma SD of VERIFICATION P3
with both sides and a two-line proof; no n-gon hypothesis is used beyond "no n-cup".)

**Lemma A1.** In a (5,n)-valid S, a point v that starts an (n−1)-cup ends no 4-cap; a point that ends an (n−1)-cup
starts no 4-cap.

*Proof.* If (a,b,c,v) is a 4-cap and (v, d₂, ..., d_{n−1}) a cup, Lemma G(i) applied to H = {v, d₂, ..., d_{n−1}}
(a cup, so H is its own lower chain) makes (c, v, d₂, ..., d_{n−1}) an n-cup, a convex n-set. Mirror for the second
claim. ∎

More generally, a point that ends a 4-cap has α ≤ n − 2, and every cup that starts at it extends one point to the left.

**Lemma Q (the top β-level starts no 4-cap).** Let S have no 5-cap and let T = {v : β(v) = max_w β(w)} be the top
β-level. Then no point of T starts a 4-cap, i.e. T ⊆ Q0 (as filed: "Q0 ∪ T is 4-cap-free"; V3 pointed out that the
proof gives T ⊆ Q0, which makes the filed wording trivial). Mirror: the top α-level lies in P0. In particular, if a
(5,n)-valid S has no (n−1)-cup and has an (n−2)-cup, then B_{n−2} ⊆ Q0 and A_{n−2} ⊆ P0; with an (n−1)-cup this is
Lemma A1.

*Proof.* Let (d,x,y,z) be a 4-cap with d ∈ T. Then β(d) ≥ β(x) ≥ 2 (x ends the 2-point cup (d,x)); hence a longest
cup ending at d has a last edge (p,d). If (p,d,x) were a
cup, appending x would give β(x) ≥ β(d) + 1 > β(d), contradicting the choice of T; so (p,d,x) is a cap (this is
DELTA3N Lemma 1). Then (p,d,x), (d,x,y), (x,y,z) are consecutive caps and (p,d,x,y,z) is a 5-cap. ∎

**Lemma E (pushing a cup to Q0).** In a (5,n)-valid S, if a cup K = (k₁, ..., k_s), s ≥ 2, ends at a point of L¹
(a 4-cap (k_s, x, y, z) starts there), then (k₁, ..., k_s, x) is a cup. Hence every cup is the prefix of a cup that ends
in Q0 (repeat; lengths are at most n−1, and an (n−1)-cup ends in Q0 by Lemma A1), and a longest cup starting at any
point ends in Q0. Mirror: a longest cup ending at any point starts in P0.

*Proof.* Mirror Lemma G with H = K (a cup is its own lower chain): (k_{s−1}, k_s, x) is a cup, else
(k_{s−1}, k_s, x, y, z) is a 5-cap. ∎

**C2\* ⟹ C2 (PROVED).** Call C2\*(n) the statement "if r is unrootable, some (3,n−2)-gon H containing l has its
rightmost point in L¹". By mirror Lemma G, the lower chain of such an H (n−2 points, starting at l) extends by one
point to an (n−1)-cup starting at l; so C2\*(n) ⟹ C2(n). EXACT: C2\* holds on all 12 ROOT(7) failure types (8-10
such gons each) but **fails on all 34 ROOT(6) failure types** (there the gons through l ending in L¹ are (4,3)-gons,
which give only α(l) ≥ 4 = n−2, while α(l) = 5 for other reasons); in the broad scan of §3 the same holds for all
14 ROOT(7) and all 138 ROOT(6) failure types. So at n = 7 the observed long cup at l is explained by (3,5)-gons through
l whose right end starts a 4-cap (these gons are present, but they are not the gons that block rooting at r: §3,
`blockers2.py`); at n = 6 (the extremal size 15) it is not explained (`c2star.py`). The weaker witness C2′ "some (n−2)-cup from l ends at a point of L¹" (⟹ C2 by Lemma E) behaves the
same way: present in all 12 ROOT(7) failure types, absent in all 34 ROOT(6) failure types (`c2prime.py`); at n = 6 the
5-cups from l (9 of them in T1's real sets, all ending at r − 1) have 4-cup prefixes ending in Q0. Being an extremal
set does not explain it either: the mirror images of the real ROOT(6) sets are 15-point (5,6)-valid sets with
α(l) = 4.

When S has an (n−1)-cup the top level is B_{n−1} ⊆ Q0 (Lemma A1) and Lemma Q says nothing new; Q0 ∪ B_{n−2} can then
contain 4-caps (d,x,y,z) with β(d) = n−2, β(x) = n−1 (it does in 75 of the 110 known types, `dq.py`). Without an
(n−1)-cup, Q0 ∪ B_{n−2} = Q0.

**Proposition R (reduction of LR to two one-sided statements).** Fix n ≥ 6. Define

- **C1(n):** for every (5,n)-valid S whose rightmost point r ends a 4-cap: if r ends an (n−1)-cup, r is rootable.
- **C2(n):** for every (5,n)-valid S in which r ends a 4-cap and l starts a 4-cap: if r is unrootable, l starts an
  (n−1)-cup.

Then C1(n) ∧ C2(n) ⟹ LR(n), and hence (T4's L1, claim t4-lemmas) weak D(5,n).

*Proof.* Let S be (5,n)-valid with r ending and l starting a 4-cap, and suppose r is unrootable. By C2(n), l starts an
(n−1)-cup. In the mirror image μS, the rightmost point μ(l) ends a 4-cap and an (n−1)-cup (μ keeps caps and cups and
reverses the order), so by C1(n) applied to μS it lies in a weak Δ D of μS; μ⁻¹(D) is a weak Δ of S containing l. ∎

Remarks. (1) C2 alone implies C3(n): a valid S without an (n−1)-cup (with r ending, l starting a 4-cap) has r rootable;
C3 is the natural next step after DELTA3N Theorem 2 ("U has no (n−2)-cup ⟹ r rootable"). (2) C1 alone already says an
LR counterexample has β(r) ≤ n−2 and α(l) ≤ n−2. (3) By Lemma M (T4), C2 implies: if S is right-hostile (r unrootable)
and W ⊇ S is valid with max W = r, then l(W) starts an (n−1)-cup in W. All three known 17-point right-hostile blocks
admit no new leftmost point at all (T3's glue probes), so this consequence is untested beyond them.

## 3. Exact checks (own code, `p1/`)

Sets: T1's 21 real ROOT(6) sets and `root6_real15`, T3's `root6_m15`, `rc6_m15_fg`, `tspm6_m15`, the three CONJ-TS′(6)
sets, T1's `tspm6_real15`, the 32 CEGAR models `cg15_it*`, T4's TRIV(6) model `triv6_m10`; at n = 7 R7's and T1's real
17-point sets (also T3's copies `blk_*`), `root7_m17_s1`, `d7_13_real`, the 12 CEGAR models `r7c17_it*`, `r7cg17_it*`,
attack 4's `min_LR_n7` (15) and `min_LRB_n7` (20). Every set and its mirror: 164 instances, **110 distinct order
types**, all valid, all with r ending and l starting a 4-cap.

| check | result |
|---|---|
| validity, rootability of r and l, β(r), α(l), R¹, L¹ (`p1prof.py`, output `prof_all.jsonl`) | LR holds in all 164; r unrootable in 73 instances = 46 types (34 at n = 6, 12 at n = 7) |
| Lemma G and G2, both sides (`lemmaG_check.py`) | 47,832 gons, 11,300 (gon, 4-cap at its left end) pairs: 0 failures of G, 0 of G2, 0 of mirror G2, 0 of "gon in R¹ has right end in E2" |
| C1 (`distinct.py`, `p1prof.py`) | 58 types with β(r) = n−1: r rootable in all 58 |
| C2 (`distinct.py`) | 46 types with r unrootable: α(l) = n−1 in all 46 |
| explicit witnesses for C1 (`c1cands.py`) | Q0 is a weak Δ in 53 of 58; some β-level of U plus r in 15; a β-antitone weak Δ of U in 15; none of the three in 4 (tspm6_m15 both sides, ctl_lattice-hyp, mirror of tspm6_real15), where r is rootable by other sets |
| LP0 split (`lp0parts.py`) | P0(S) = P0(U) whenever r ends a 4-cap (asserted on all 164); in every rooted failure P0 meets every gon of U and every gon through r; where P0 fails, the gons inside R¹ are (4,n−3)-gons and, through r, also (3,n−2)-gons (consistent with G2) |
| **broad scan** (`scanall.py`, `scanall2.py`) | all 531 set files (json with points or signs, 10-18 points) in the team work directories `pm1115/{r7,t1,t3,t4,u2,v1,v2,v3,l1,t5}` (excluding claim, forms and status files), each with its mirror, for n = 6 and 7 where valid: 738 distinct (n, order type) pairs with r ending and l starting a 4-cap, among them **152 distinct r-unrootable types (138 at n = 6, 14 at n = 7)**; **no violation of C1, C2 or LR**; all 738 satisfy the signotope axioms; on all 152 r-unrootable types T4's LP0 holds (P0 meets every gon) and β(r) = 4 (n = 6: 15 points, n = 7: 17 points) |
| semantic control of the SAT add-on (`addcup_ctl.py`) | 328 of 328: the added block is satisfiable with the triples fixed exactly when β(r) = n−1 (mode `rcup`) resp. α(l) ≠ n−1 (mode `nolcup`) |
| two-level rule D_r = Q0 ∪ E2 (∋ r), D_l = P0 ∪ F2 (∋ l) (`dq.py`) | a weak Δ in only 46 of 110 types (P0 or Q0: 102 of 110); D_r is 4-cap-free in 35 types (always when there is no (n−1)-cup, by Lemma Q) and contains a 4-cap in 75; on `triv6_m10` (no 5-cup, TRIV failure) D_r = Q0 and D_l = P0 (Lemma Q) and both miss a gon. Negative result: this explicit rule is not a route to LR |
| localisation (`loc.py`) | a weak Δ through r inside Q0 ∪ E2 exists in 55 of the 64 types where r is rootable; not in 9 (5 of them with β(r) = n−1: tspm6_m15 both sides, ctl_lattice-hyp, mirror of tspm6_real15, mirror of min_LR_n7). So rooted weak Δs can need points of lower β-levels that start 4-caps; no rank-localised proof of C1 is possible along these lines |
| blockers of rooting at r (`blockers.py`, 46 rooted-failure types) | ignoring all gons that contain l makes r rootable in all 46 (14-319 rooted sets); ignoring only the (3,n−2)- and (4,n−3)-gons containing l also suffices in all 46 (11-193); ignoring only the (n−1)-cups at l does not suffice in 30 (18 at n = 6, all 12 at n = 7). So the (n−1)-cups that C2 predicts at l are not themselves the obstruction. Finer split in the next row |
| blockers by type (`blockers2.py`) | n = 7 (12 types): ignoring all (4,n−3)-gons through l makes r rootable in all 12, ignoring all (3,n−2)-gons through l (in particular the C2\* witnesses) in none; n = 6 (34 types): ignoring the (3,n−2)-gons through l suffices in all 34, ignoring the (4,n−3)-gons in 24. So at n = 7 the C2\* witnesses (which force the 6-cup at l) are present but are not what blocks rooting; the blockers are (4,4)-gons through l |

## 4. SAT probes at n = 6, m = 15, and neighbourhood tests (COMPUTED / HEURISTIC)

At n = 6 every (5,6)-valid signotope has at most 15 points and r is rootable for m ≤ 14 (ROOT(6) CERTIFIED ≤ 14), so
C1(6) and C2(6) are each decided by one CNF at m = 15: T3's compact ROOT encoder `t3/cnf/rc6_m15.cnf` (SHA-256
`152d8a20…`; its soundness is in `t3/tools/root_compact.py`; it gave a ROOT(6) model in 13 s) plus the add-on of
`p1/addcup.py` (each block is the literal definition of the cup condition over the triple variables, true = cup; the
aux y_T are one-way witnesses). The C2 CNF does not add "l starts a 4-cap", so an UNSAT verdict would prove the
stronger statement "every ROOT(6) failure has α(l) = 5"; a model would have to be checked for that hypothesis.

| CNF | asks for | SHA-256 | run (unit `esr-agq-p1-cup6`, CPUQuota 15 %, CaDiCaL `--sat --seed=1 -t 1200` wall) | verdict |
|---|---|---|---|---|
| `c2_nolcup6_m15.cnf` | ROOT(6) failure with l starting no 5-cup (C2(6) counterexample) | `1d703c4c…` | 16:59-17:19, 180 CPU-s | **UNKNOWN** (no model; the base CNF gave a ROOT(6) model in 13.3 s, `t3/runs/rc6_m15.fg.log`): HEURISTIC support for C2(6) |
| `c1_rcup6_m15.cnf` | ROOT(6) failure with r ending a 5-cup (C1(6) counterexample) | `078f207e…` | 17:19-17:39, 180 CPU-s | **UNKNOWN** (no model): HEURISTIC support for C1(6) |
| `c2_nolcup6_m15.cnf` again, default mode with LRAT (`run_c2unsat.sh`, unit `esr-agq-p1-c2u`, CaDiCaL 2.1.3 `--seed=2 -t 2400 --lrat`) | an UNSAT verdict for C2(6) | same (`1d703c4c…`) | 17:39:43-18:16:18; 329 CPU-s, 1,551,940 conflicts, max RSS 116 MB | **`s UNSATISFIABLE`**; LRAT kept: `p1/c2_nolcup6_m15.lrat.zst` (429,401,302 B, SHA-256 `ab9b0b0b…`; decompressed LRAT SHA-256 `0b5745db…`); **cake_lpr `s VERIFIED UNSAT`** (heap 480 MB, unit `esr-agq-p1-cake`, `p1/c2cake/`, hashes equal): CERTIFIED |
| `c1_rcup6_m15.cnf`, default mode, no proof output (unit `esr-agq-p1-c1u`, CaDiCaL `--seed=2`, wall limit to 18:33) | an UNSAT verdict for C1(6) | `078f207e…` | 18:22-18:33, 100 CPU-s | **UNKNOWN** (wall limit; no verdict) |

**Neighbourhood tests (COMPUTED, `nbhd.py`; each model re-checked exactly).** For every known set S with r unrootable,
fix the signs of all triples that avoid the moved end point (l for C2, r for C1) and k further points, leave the rest
free, and ask T3's compact ROOT CNF (n = 6: `rc6_m15.cnf`; n = 7: `t3/cnf/rc7_m17.cnf`) plus the cup block for a C2
(resp. C1) counterexample. Positive control: the same calls without the cup block (mode `ctl0`) must be SAT, and every
model is decoded and re-checked with T4's exact code (valid, signotope, r unrootable).

| n | instances | k | C2 calls (SAT) | C1 calls (SAT) | controls moving l / moving r (SAT, exact r unrootable) |
|---|---|---|---|---|---|
| 6 | 56 (all r-unrootable instances) | 0 | 56 (0) | 56 (0) | — |
| 6 | 35 (CEGAR models, T3's two abstract models, T1's root6_real15) | 1 | 455 (0) | 455 (0) | 455 (455, 455) / 455 (455, 455) |
| 6 | 35 | 2 | 2,730 (0) | 2,730 (0) | 2,730 (2,730, 2,730) |
| 6 | 35 | 3 | 10,010 (0) | 10,010 (0) | — |
| 6 | 35 | 4 | 25,025 (0) | 12,199 of 25,025 run (0) (chunks stopped at the 57-s limit) | — |
| 7 | 15 (R7's and T1's real sets, root7_m17_s1, 12 CEGAR models) | 1 | 225 (0) | 225 (0) | 225 (225, 225) / 225 (225, 225) |
| 7 | 15 | 2 | 1,575 (0) | 1,575 (0) | — |
| 7 | 15 | 3 | 6,825 (0) | 1,589 of 6,825 run (0) (five chunks, each stopped at the 57-s limit) | — |

So no C1 or C2 counterexample differs from a known rooted failure only in the triples through the moved end point and
at most three other points (four for C2 at n = 6; for C1 at n = 7 with k = 3 only 1,589 of the 6,825 cases were run). These are UNSAT verdicts of pysat's CaDiCaL 1.5.3,
not certified.

## 5. What blocks a proof (the gap)

1. **Nothing constructs a rooted weak Δ in the long-cup regime.** DELTA3N Theorem 2 roots r when U has no (n−2)-cup;
   Theorem 4 and Corollary 5 handle |S| ≤ 2n−3 and localise |S| = 2n−2. Every hostile set has (n−1)-cups (finding 1
   of THEORY), and C1 asks exactly for rooting in the presence of an (n−1)-cup at the root. The rank tools (β-levels
   are terminal-safe; β-antitone sets are 4-cap-free) do not suffice: on 4 of the 58 known types with β(r) = n−1, no
   β-level plus r, no β-antitone set and not Q0 works, yet r is rootable.
2. **C2 is global.** It asserts that a hostile right end forces a long cup at the far left end. T4's deletion-minimal
   cores use every point of U, and the known 17-point right-hostile blocks are vertex-critical including l (finding 8),
   so no local gadget proof is in sight. The obstruction does run through l: in all 46 rooted-failure types r becomes
   rootable once the gons containing l are ignored. But the gons that carry it are not the ones that force the long cup:
   at n = 7 the blockers are the (4,4)-gons through l (Lemma G turns their right ends in L¹ only into 5-cups from l),
   while the 6-cup at l comes from (3,5)-gons through l (the C2\* witnesses), which are not needed for the obstruction;
   at n = 6 no C2\* witness exists at all.
3. **What Lemma G gives.** Local cup extensions at 4-cap ends: the gons that P0 misses are (3,n−2)- or (4,n−3)-gons
   ending in E2 ∩ R¹ (Cor. G2). This explains part of LP0 for free: if β(r) ≤ n−3 (as in all 14 ROOT(7) failure types),
   every gon through r meets P0 (a gon inside R¹ that contains r has r as its rightmost point, so β(r) ≥ n−2); at n = 6
   (β(r) = n−2 in all 138 ROOT(6) failure types) G2 does not give this, although it holds there (EXACT). The remaining
   part (gons of U inside R¹) is not reached by these arguments.
4. **A normal form that fails.** The existing rank tools all use β-antitone (terminal-safe) sets. In every set of
   §3 where r is rootable, some rooted weak Δ is β-isotone (ISO-ROOT), which would have confined rooted Δs to
   {β ≤ β(r)} and explained why r with small β(r) is hard to root (β(r) = 4 in all 152 rooted-failure types). It is
   false at n = 8 for a real 17-point set (β(r) = 3, rooted only by non-isotone sets). The unrooted form ISO (every valid
   set has a β-isotone weak Δ) survives every test (2,566 instances) but is not rooted, so it does not feed an induction.
5. **What a proof along these lines would need.** (a) C1(n): a construction of a weak Δ through an end point that
   ends (starts) an (n−1)-cup, valid for all set sizes; STAIR-C1 says where to look: a staircase of whole β-level
   intervals, i.e. a choice of n−2 cut points, works on every tested set (219 scan types plus 873 pool instances with β(r) = n−1, n = 6, 7, 8),
   so a proof would have to show that some cut vector gives a 4-cap-free set meeting every gon. Equivalently: find a
   nondecreasing h : {0, ..., r} → {1, ..., n−1} with h(r) = n−1 such that D_h = {v : β(v) = h(v)} is 4-cap-free and
   meets every gon of U (gons through r are met by r). Envelope choices of h meet every gon on all tested sets but
   contain 4-caps. Every 4-cap (a,b,c,d) of S has β(a) < β(b) (else DELTA3N Lemma 1 gives a 4-cap (p,a,b,c) and with d
   a 5-cap), so inside a staircase its first two points lie in different level intervals; no further restriction on
   these 4-caps was found; (b) C2(n), e.g. through C2\*(n) for n ≥ 7: "if r is unrootable,
   some (3,n−2)-gon through l has its rightmost point in L¹". (a) and (b) are one-sided, so each can be probed by SAT more
   cheaply than LR (one copy of the ROOT encoding plus a cup block), but neither has a proof idea; for n = 6 (where both
   hold on all known sets) the C2 mechanism is different and unexplained.
6. **No size reduction.** By Lemma M an LR(7) counterexample needs a right- and a left-hostile block, each with at least
   15 points (ROOT(7) CERTIFIED ≤ 14); with M(5;7) ≤ 36 (CERTIFIED) the problem is finite (15-36 points) but far beyond
   SAT reach, and no argument bounds a minimal counterexample below 36.

## 5a. Next steps (in order of cost)

1. Decide C1(6) and C2(6) at 15 points in default (UNSAT) mode, with LRAT: one CNF each (`p1/c1_rcup6_m15.cnf`,
   `p1/c2_nolcup6_m15.cnf`); expected cost similar to LR(6) at 15 (1,225-1,402 CPU-s). If both are UNSAT and certified,
   the n = 6 case of the reduction is a theorem for all signotopes (≤ 14 points follow from ROOT(6), ≥ 16 vacuous).
2. One-sided SAT-mode probes at n = 7, 17 points (`addcup.py` on `t3/cnf/rc7_m17.cnf`): a model would refute C1(7) or
   C2(7); ROOT(7) itself gave a model at 17 points in 1,599 s.
3. A CNF for STAIR-LR (needs order-encoded β-level variables and cut variables) at n = 6 (≤ 15 points) and n = 7 (15-17
   points); STAIR-LR is stronger than LR, so a model would not refute LR but would retire the explicit rule.
4. Theory: prove that a good cut vector exists (STAIR-C1), starting from the facts that envelope staircases meet every
   gon and that the 4-caps they contain start with a β-increase.

## 6. Files

Work directory `/home/jay/research/data/roadmap-20261115/pm1115/p1/` (all scripts single-threaded, each under a
minute): `sets.py` (the set list), `p1prof.py` (profiles; output `prof_all.jsonl`), `lemmaG_check.py`, `distinct.py`,
`c1cands.py`, `lp0parts.py` (`lp0parts.jsonl`), `gl1.py`, `detail.py`, `dq.py` (`dq.jsonl`), `blockers.py`
(`blockers.jsonl`), `blockers2.py` (`blockers2.jsonl`), `c2star.py`, `c2prime.py`, `triv_detail.py`, `loc.py`,
`qe_check.py`, `nbhd.py` (neighbourhood tests; outputs `nb6*.jsonl`, `nb7*.jsonl`), `scanall.py`, `scanall2.py`
(`scanlist.txt`, `scan_*.json`: the broad scan), `iso.py`, `iso2.py`, `iso3.py`, `isopool.py`, `isopool8.py`,
`isofind8.py`, `verify_isocex.py`, `isoroot8_cex_2_17_prefix.json` (the ISO-ROOT(8) counterexample), `stair.py`,
`stair2.py`, `stair3.py`, `stairpool.py`, `cupstair.py`, `c1look.py`, `addcup.py` (CNF add-on), `addcup_ctl.py`
(semantic control), `run_cup6.sh`, `run_c2unsat.sh`, `cnf.sha256`, the two probe CNFs and their logs (`*.out`,
`run_cup6.status`, `run_c2unsat.status`, `c2u.out`, `c1u.out`), the C2(6) proof `c2_nolcup6_m15.lrat.zst` with
`c2_nolcup6_m15.lrat.sha256` and its cake_lpr run `c2cake/`, `decode_c2u.py`, `stairone.py`, `stairrand.py`, `stair5.py`,
claim files `claim_p1-*.json` (filed as `pm1115/claims/p1-cupext`, `p1-lemmaq`, `p1-lemmae`, `p1-c2six`; note
`p1-c2six.note-from-P1.txt`).
Uses T4's `t4lib.py` (exact signotope toolkit, self-test) for loading and weak-Δ enumeration.

Reproduce:

```bash
P1=/home/jay/research/data/roadmap-20261115/pm1115/p1; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd $P1 && OPENBLAS_NUM_THREADS=1 $PY -I lemmaG_check.py     # Lemma G / G2 on 164 instances
OPENBLAS_NUM_THREADS=1 $PY -I distinct.py                  # C1, C2 on the 110 distinct order types
OPENBLAS_NUM_THREADS=1 $PY -I addcup_ctl.py                # semantic control of the SAT add-on
OPENBLAS_NUM_THREADS=1 $PY -I stair2.py                    # STAIR-C1 on the broad-scan types (needs scan_*.json)
OPENBLAS_NUM_THREADS=1 $PY -I verify_isocex.py isoroot8_cex_2_17_prefix.json   # ISO-ROOT(8) counterexample
for st in 0 120 240 360 480; do OPENBLAS_NUM_THREADS=1 $PY -I scanall.py scanlist.txt $st 120; done   # broad scan
```
