# DELTA_PM_CHECK: literature check of the afternoon Δ-program statements (15 November 2026)

Track N1 of the afternoon team, 17:00-18:40 KST. **Status: complete (bounded search), 17:25 KST.**
**Rigor: evidence only (bounded literature search).** The verdict words are "found" (a source states the statement, a stronger one, or something that gives it in one step), "related"
(a source has a close analogue or the same device, but neither states nor implies the statement) and "not found in
this search". "Not found" is never "new" and never a priority claim. Statements are checked as worded in
DELTA3N20261113/attack20261115/THEORY_1115PM.md (v6, 16:55 KST) §0-§2 and ROUND6.md "Definitions". The earlier checks
NOVELTY20261113B (13 Nov) and NOVELTY20261115/README.md (15 Nov, 03:00-04:20) are not repeated; where they already
settled a point, this file only points to them. Nothing in the repository was changed except this new file; nothing was
committed, posted or sent.

## Verdict in brief

1. **None of today's Δ-program statements was found in the literature.** Not found in this search: the weak Δ in the
   project's sense (a 4-cap-free subset of a (5,n)-valid set meeting every convex (n−1)-gon) beyond what the earlier
   checks recorded, ROOT(n), CONJ-TS′(n), ENV#(n) and the related VE/(U)/AT_n forms, TS±(n), TWO-ENV#(n), LR(n) and its
   gluing form, LP0(n), DEPTH(n), CB(n), ONE(n), the transversal statement T(n) (and T₂₆(8), T₂₇(8)), the recursion
   M(5;n) ≤ C(n−1,2) + 1 + M(5;n−1), and the wave-2 statements H7 / H7U, C1-C3, Prop. R and Lemma A / Lemma G (the
   last are elementary one-step extension arguments in the style of the cups-caps proof; "caps are local" (F1) is
   standard: signotopes are transitive colourings in the sense of Fox–Pach–Sudakov–Suk). No source competes with or contradicts the day's computations (LR(6) and
   TWO-ENV#(6) true; ROOT(6), TS±(6), CONJ-TS′(6), ENV#(6), ROOT(7), CONJ-TS′(7), ENV#(7) false for real sets).
2. **One sub-statement is found, as a consequence of a public unproved conjecture.** Weak D(4,n) (a cup meeting every
   convex (n−1)-gon of a 4-cap-free set with no convex n-gon) follows from gotrevor's "transversal cup" conjecture
   L1(4,b) (public notes, 6-7 Oct 2026, unrefereed; for arbitrary 2-colourings of triples it is checked exhaustively at
   b = 5, 6 for every size, and sampled at b = 7, 8 (19 colourings, all split); no hand proof). NOVELTY20261113B already cited L1 for the split and quoted its "transversal cup" line (C5); what is added here is
   the explicit consequence for weak D(4,n), the notes' measurements on Baek's Δ, their "either side at each step"
   iterated Δ rules, and their ∃∀ (2QBF/CEGAR) method, which is the method the project uses for its Δ searches.
3. **Closest classical ancestors (related, not anticipations).**
   - Erdős–Szekeres 1935, cups-caps proof: the left ends of the (k−1)-cups form an (l−1)-cap-free set whose removal
     destroys every (k−1)-cup. This is the cup analogue of a weak Δ (gons replaced by cups). The polygon version is not
     in the source. P0/Q0 (points ending / starting no 4-cap) are the classical endpoint sets of this proof.
   - Baek (arXiv:2206.04260): his Δ (leftmost points of the β-rows 1..n−2) is removed so that S − Δ has no (n−1)-cup;
     the induction lowers the cup length, and mirror reflection supplies the one-sided WLOG at the extreme points. Δ
     hits cups, not gons (gotrevor measured that S − Δ keeps a gon on 21-67 % of samples).
   - Hitting or blocking sets for convex polygons exist in the literature only with blockers outside S, inside the
     polygons (k-hole blocking sets), which is a different notion.
4. **Background items asked for** (cups-caps decompositions, Suk and Holmsen–Mojarrad–Pach–Tardos, Szekeres–Peters,
   the SAT works, realizability tools): all related as context or method; none states or implies a Δ statement (§2).
   Heule–Scheucher already used biquadratic final polynomials to refute SAT models of an ES-type problem, so the
   project's SAT + BFP step is established practice.
5. **Side observation (not literature; unverified).** Baek's theorem is Lean-checked for arbitrary 2-colourings with
   weak gons; with two signotope facts already in today's records (caps are local; cap ∪ cup with common ends is
   convex) it appears to give M(4;n) ≤ C(n−1,2)+1 for all signotopes. That would lift the "point sets only" caveat of
   LEDGER_1115PM input I6 and of the weak D(5,8) window. Details and the caveat in §2 under [Baek].

## 1. Statements checked, closest literature, verdict

Definitions as in THEORY_1115PM.md §0: S is (5,n)-valid (general position, distinct x, no 5-cap, no convex n-gon); a
gon is a convex (n−1)-subset; a weak Δ is a 4-cap-free subset meeting every gon; r / l are the right- / leftmost points;
U = S − r, V = S − l; P4(U) = pairs ending a 4-cap of U; ↑P4 its up-closure under the pair order ⊑.

| # | statement (project wording) | closest literature found (details in §2) | states or implies it? | verdict |
|---|---|---|---|---|
| 1 | **weak D(5,n)**: every (5,n)-valid set has a weak Δ (true at n = 6, CERTIFIED; open at n = 7 from 16 points, n = 8 from 17) | [ES35] cups-caps proof (cup analogue: left ends of (k−1)-cups, an (l−1)-cap-free set meeting every (k−1)-cup); [Baek] Δ meeting every (n−1)-cup; [GL-PS] PASCAL-SPLIT (strong form, prior); [HP756] transversal cup (a = 4 only) | no: the sources hit cups, or treat a = 4, or ask for the strong split; none asks for a 4-cap-free set meeting every convex (n−1)-gon when 5-caps are excluded | **not found in this search** (related: ES35, Baek, GL-PS, HP756). The earlier verdict "weak cap form not found verbatim" (NOVELTY20261113B C5) and the morning verdict stand; today's search used hitting-set / transversal wording instead of partition wording |
| 2 | **weak D(4,n)**: a 4-cap-free set with no convex n-gon has a cup meeting every gon (n = 8: CERTIFIED ≤ 16 points, open 17-22) | [HP756] L1(4,b): "a 4-cap-free, n-cup-free, (3,n−1)-gon-free colouring has a cup set `B` of ≤ n−2 points hitting every weak (n−1)-gon" (§6 of the notes; "transversal cup" in §4) | yes, for point sets: L1(4,n) gives a cup with at most n−2 points meeting every gon, hence weak D(4,n). L1(4,b) is open there for b ≥ 7 (exhaustive for all 2-colourings at b = 5, 6; sampled at b = 7, 8) | **found** (as a consequence of a public, unproved, unrefereed conjecture). DELTA2N §10 already notes that its complete (4,5), (4,6) strong results reproduce public claims |
| 3 | **T(n)**: the gons have a transversal of at most C(n−1,2)+1 points (and the weaker T₂₆(8), T₂₇(8) of LEDGER_1115PM §1.2); with weak D(5,n) for all sizes, M(5;n) ≤ M(4;n) + M(5;n−1) = C(n−1,2) + 1 + M(5;n−1), the input of the ES(8) ≤ 303 / 298 rows | [Baek] M(4;n) = C(n−1,2)+1 (main theorem, `thm:main` / `thm:main-thm` in arXiv v2; the earlier check cites it as Theorem 1.6; proved, and Lean-checked, for arbitrary 2-colourings with weak gons; for signotopes see the observation in §2); [ETV96] Pascal identity of the conjectured values; [Jav] endpoint split M_k(a,b) ≤ M_k(a−1,b) + M_k(a,b−1) (prior); [Sch] Lemma 5.3 (prior) | the bound on \|Δ\| is Baek's theorem (found); the recursion that lowers the polygon size n by paying M(4;n) was not found. The ETV values satisfy the sharper M(5;n) = M(4;n−1) + M(5;n−1) | **recursion: not found in this search**; ingredient M(4;n) = C(n−1,2)+1: found [Baek] |
| 4 | **CB(n)**: a weak Δ with no (n−1)-cup; gives M(5;n) ≤ C(n−1,2) + M(5;n−1) | [ES35] cups-caps theorem gives \|Δ\| ≤ C(n−1,2) (found, the counting step) | the existence statement: no | **not found in this search** |
| 5 | strong D(5,n) and cup-side D(5,n) | prior checks | — | not re-checked: strong form = PASCAL-SPLIT at u = k = n (found, NOVELTY20261113B C5); cup-side form not found (NOVELTY20261115 README) |
| 6 | **ROOT(n)**: if r ends a 4-cap, U has a weak Δ A with A + r 4-cap-free (false for real sets at n = 6, 15 points, and n = 7, 17 points) | [Baek] case split at the extreme cup endpoints p_S, q_S (both "hostile": handled directly; otherwise WLOG by reflection, then Δ-removal); [ES35] endpoint step | no | **not found in this search** |
| 7 | **CONJ-TS′(n)** (terminal-safe weak Δ of U), **ENV#(n)** (weak Δ whose 3-caps (a,b,c) have (b,c) ∈ ↑P4(U)), **VE, (U), uniform / exposed lines, AT_n, AT2_n, AT3_n** | [Valtr07] open caps and cups (no point above the chain): an emptiness condition on a cap/cup, only an analogy to "exposed"; [MS14]/[CK71] down-set (order ideal) technique, an analogy to the up-closure ↑P4 | no | **not found in this search** (related by analogy only) |
| 8 | **TS±(n)** and **TWO-ENV#(n)** (terminal-safe / ENV# on the right, or the mirror notion on the left) | [Baek] Lemma `lem:endpts` (p_S ≤ q_S: left ends of (n−1)-cups lie weakly left of right ends) and the left-or-right case split with mirror WLOG; [HP756] §14 iterated Δ rules "either side at each step" (`delta2`, `baek2`); [HMPT] left / right convex chains (a different dichotomy) | no | **not found in this search** (related: two-sided choice by reflection) |
| 9 | **LR(n)**: S has a weak Δ through l or through r (TRUE at n = 6, two certificates); the gluing form (an LR failure needs a right-hostile and a left-hostile block in one valid set); Lemma M (a weak Δ of W restricts to a weak Δ of any T ⊆ W) | [Baek], [HP756] as in row 8; Lemma M is the hereditary property of transversals under restriction, elementary, needs no source | no | **not found in this search** |
| 10 | **LP0(n)**: if r lies in no weak Δ, then P0 (the points ending no 4-cap) meets every gon; TRIV(n) (P0 or Q0 is a weak Δ); end layers R^i and DEPTH(n) | [ES35] (via [Jun]): P0 is the 4-cap-free complement of the right ends of 4-caps, the classical endpoint set; [Jav] Lemma 3 and [Sch] Lemma 5.3 use the same endpoint split (prior) | the objects P0, Q0, end layers: found (classical); the statements LP0, TRIV, DEPTH: no | **not found in this search** (P0 itself is classical) |
| 11 | **ONE(n)**: at most one point of a valid set lies in no weak Δ | — | no | **not found in this search** |
| 12 | Δ-reduction ⟹ ES(n)-type recursion as a programme (DELTA2N §1; THEORY §2.3) | [ETV96] (ES ⟺ ETV, Pascal identity); [GL-PS] (a Pascal split for general sets "would imply the Erdős–Szekeres conjecture", prior); [HP756] §10 refinement lattice of Pascal-type splits; [Baek] Δ-removal | the strong-split programme is public (prior); the weak-Δ programme is not | **not found in this search** for the weak form (related: GL-PS, HP756, ETV96) |
| 13 | Wave-2 lemmas (PROOF_LP0_ATTEMPT_P2 §1-2, PROOF_LR_ATTEMPT_P1 §2): F1 "caps are local" in signotopes; F2 convex = cap ∪ cup with common ends (4-subset definition); Lemma A / Lemma G (a gon whose leftmost point ends a 4-cap has an upper chain of 3 or 4 points; (z, g1, v) is a cup for every v > g1); A1 (every (n−1)-cup starts in P0 and ends in Q0); Cor. SD | F1: [FPSS] §"Transitive colorings" and [HMPT] ("transitive coloring"; signotopes are such colourings), [Baek] defines cups by consecutive triples; Lemma A/G, A1: the one-step extension argument of [ES35] (a cap ending at g1 plus a cap triple at g1 gives a longer cap); [HP756] §3 quotes Balko–Valtr's lemma "a vertex ending one (b−1)-cup and starting another forces a (3, b−1)-gon" (a = 4) | F1: found (standard); F2: standard for point sets, for signotopes with the 4-subset definition not located in a source here; Lemma A/G, A1: not stated in the sources found, but each step is a classical one-line extension argument | F1 **found**; F2 **related**; Lemma A/G, A1, SD **not found in this search** (elementary; cite [ES35] for the device) |
| 14 | H7(n) / H7U(n) (a gon made of 4-cap end points forces an ENV# Δ of U), C1(n) / C2(n) / C3(n) and Prop. R (C1 ∧ C2 ⟹ LR) | — | no | **not found in this search** |

## 2. Sources read or consulted today (new relative to the earlier checks unless marked "prior")

- **[ES35]** P. Erdős, G. Szekeres, "A combinatorial problem in geometry", Compositio Math. 2 (1935) 463-470
  (<http://www.numdam.org/item/CM_1935__2__463_0/>, record page checked; the paper itself was not read today). The cups-caps proof was read in **[Jun]** V. Jungić, *Introduction to Ramsey Theory:
  Lecture notes for undergraduate course*, Section 6.2 "Erdős-Szekeres Problem of Convex Polygons - Part Two"
  (<https://opentext.uleth.ca/Ramsey/sec_ES2.html>, read 15 Nov 2026): "Let L be the set of all points that are the
  left ends of (k−1)-cups in S"; "taking the set L out of S *destroys* all (k−1)-cups in S"; an (l−1)-cap in L is then
  extended to an l-cap or a k-cup. *Relevance:* the cup analogue of a weak Δ and the origin of the endpoint sets P0/Q0.
  It says nothing about convex polygons that are not cups or caps.
- **[Baek]** J. Baek, "On the Erdős-Tuza-Valtr conjecture", <https://arxiv.org/abs/2206.04260> (v2; LaTeX source read
  today, §2 and §5); journal version European J. Combin. (2024) according to Consensus (volume and pages not
  verified).
  "Define the set Δ = {x_1, x_2, ⋯, x_{n−2}} of size n−2", x_i the leftmost point of the row R_i(S) = {p : β(p) = i};
  "S' = S ∖ Δ"; "We will show later that S' is (n−1)-cup free, so that we can apply the induction hypothesis". The
  induction hypothesis is a cups-only statement (two interweaved laced (n−1)-cups in a 4-cap, n-cup free configuration
  of size C(n−1,2)+2); gon-freeness enters once, through the lemma that two interweaved laced (n−1)-cups force a
  (3, n−1)-gon (`lem:inter-gon`; Lemma 5.2 in gotrevor's numbering). Mirror reflection is used "extensively to exploit
  the symmetry without loss of generality". Lemma `lem:endpts`: with p_S the rightmost left end and q_S the leftmost
  right end of the (n−1)-cups, "we always have p_S ≤ q_S" (the mirror swaps them). The induction splits into cases at the extreme cup
  endpoints: configurations handled directly by lemmas (`lem:special`: an (n−1)-cup from x to y with an (n−2)-cup
  ending at x and one starting at y; in the Lean code the `JoinN2N3…` lemmas), and otherwise, after reflection if
  needed, "We assumed without loss of generality that q_S is not the starting point of an (n−2)-cup", where Δ is
  removed (Lean: `main_induction_wlog`, applied to the configuration or to its `Mirror`). This
  left-or-right case split at the two extreme cup endpoints is the closest literature device to LR / TWO-ENV#; it is
  about cups in a 4-cap-free set, not about weak Δs. The main theorem (`thm:main-thm`: "any configuration of size C(n−1,2)+2 contains either a 4-cap, n-cup or a
  (3, n−1)-gon") is proved for his configurations, which are arbitrary "bi-coloring[s] of a finite, complete 3-uniform
  hypergraph with a prescribed linear ordering" (§2; cups and caps defined by consecutive triples), so it covers
  signotopes as colourings. His n-gons are *weak*: "a pair of a-cap C1 and b-cup C2 sharing the same endpoints"
  (§2). The theorem is Lean-checked in this set form: <https://github.com/jcpaik/erdos-tuza-valtr>, `theorem main` in
  `ErdosTuzaValtr/Main/Main.lean` (statement read today, not built): for any `Config` (an arbitrary ternary relation
  `Cup3` on a linear order; `Cap`/`Cup` by consecutive triples, `Config/Defs.lean`) and any finset S with
  |S| ≥ C(n+2,2)+2, `C.HasNCap 4 S ∨ C.HasNGon (n+3) S`, an `NGon` being a cap list and a cup list with the same first
  and last points.
  **Observation for the project (not literature; this check's argument, not verified by a second party).** In a
  signotope a weak gon is strong: an interior point v of the cap lying on the cup would make (x, v, y) a cap and a cup
  at once, because caps and cups are local (F1 of PROOF_LP0_ATTEMPT_P2 §1; standard transitivity). A cap and a cup
  that meet only in their common end points form a convex set in the project's 4-subset sense (F2(⇐) there; the chain
  characterization was re-derived by the verifier of claim p1-cupext, CONFIRMED). So Baek's Lean-checked theorem
  appears to give M(4;n) ≤ C(n−1,2)+1 for **all signotopes**, not only point sets. That would remove the caveat of
  LEDGER_1115PM input I6 ("for signotopes CERTIFIED only for n ≤ 7") and make the upper end 59 of the weak D(5,8)
  window and T(n) hold for signotopes too. A verifier should check this before any record uses it. *Relevance:* Δ-removal ancestor (rows 1, 3, 6, 8, 9); the
  bound M(4;n) = C(n−1,2)+1 used in T(n).
- **[HP756]** gotrevor/es7-ladder, `docs/HUMAN-P756.md`
  (<https://raw.githubusercontent.com/gotrevor/es7-ladder/master/docs/HUMAN-P756.md>; public repository, last commit
  7 Oct 2026 by the GitHub API, unrefereed; prior for C5, re-read today for the Δ statements). Passages:
  - L1(a,b), the Pascal split (§4; the reformulation quoted next is in §6); "At `a = 4`, `B` is a cup of ≤ b−2 points meeting every (b−1)-cup and every
    (3, b−2)-gon, a 'transversal cup'. Baek's Δ has the same shape, but he avoids claiming that `S − Δ` is gon-free."
  - "Reformulated, L1(4,n) says: a 4-cap-free, n-cup-free, (3,n−1)-gon-free colouring has a cup set `B` of ≤ n−2
    points hitting every weak (n−1)-gon"; status table: L1 "Exhaustive (every colouring, 2QBF refinement
    `l1_verify.py`)" for (4,5) at every m ≤ 7 and (4,6) at every m ≤ 11 ("so all of it"); (4,7), (4,8) "Sampled"
    (12 colourings at m = 16, 7 at m = 22, all split); no hand proof. The model is arbitrary 2-colourings of triples
    ("no signotope axiom").
  - On Baek's Δ: "The gon half fails on 21-67% of these samples, and Δ is not even a cup set on 10-34%"; "Baek's
    induction hypothesis is not P(b−1,4,b−1) but his Theorem 5.10: a cups-only statement".
  - §10 "The targeted 2QBF": "a 2QBF for 'every (7,5,6)-free colouring on M vertices has a partition into parts free
    for the rungs P'. The outer solver proposes a colouring. The inner CEGAR (`partition`) finds a partition or proves
    there is none." Also a "CEGAR hitting set" (smallest subsets avoiding weak gons).
  - §14: iterated Δ rules, "Baek's Δ ... of S, then Δ of the rest, either side at each step" (`delta2`; `baek2` "is
    the member with Baek's own mirror choice"). The notes' verdict of 6 Oct 2026 (committed 7 Oct) closes the
    Pascal-split family "as a route to a hand proof" (estimate 0.5 %).
  *Relevance:* row 2 (found), rows 8, 9, 12 (related), and method prior art for the project's ∃∀ Δ searches. The
  model is 2-colourings of triples with weak gons, more general than signotopes.
- **[GL-RD]** GLitchfield/erdos-szekeres-convex-poly, `docs/research/archive-worktree-runs-20260908-to-20261003/
  sol-12h-20260913/runs/r20-sol-20261002/MATHEMATICAL-HANDOFF-root-deletion-2315.md`
  (<https://raw.githubusercontent.com/GLitchfield/erdos-szekeres-convex-poly/main/docs/research/archive-worktree-runs-20260908-to-20261003/sol-12h-20260913/runs/r20-sol-20261002/MATHEMATICAL-HANDOFF-root-deletion-2315.md>; head read today; agent notes of
  2 Oct 2026, unrefereed): "An ordered union of two cups with OneChange, no four-cap and no strong k-set has
  cardinality ≤ 2k−4 ... Deleting those two points lowers the forbidden strong size and permits induction." A
  two-point hitting set of the large strong (k−1)-sets in a special a = 4 class. *Relevance:* related to rows 1-2
  (Δ-removal for a special class); not a weak-Δ statement. Other files named "rooted" in that repository (experiments
  0028, 0084) use "rooted" for decomposition-tree states and rooted triangles, not for the project's ROOT.
  [GL-PS] PASCAL-SPLIT notes: prior (NOVELTY20261113B C5).
- **[Valtr07]** P. Valtr, "Open caps and cups in planar point sets", Discrete Comput. Geom. (2007) (abstract read
  through Consensus, <https://consensus.app/papers/details/w:9bef0559-4173-4725-9208-d467022757d4/>; volume and pages not
  verified): k-caps / k-cups with "no point of P vertically above the polygonal
  line". *Relevance:* an envelope-type emptiness condition; an analogy to the "exposed line" and ENV# conditions only.
- **[CGHSTU]** J. Cano, A. García, F. Hurtado, T. Sakai, J. Tejel, J. Urrutia, "Blocking the k-holes of point sets on
  the plane", XIV Spanish Meeting on Computational Geometry 2011, CRM Documents 8, p. 141 ff.
  (<https://www.matem.unam.mx/~urrutia/online_papers/BlockingHoles.pdf>, first pages read): "A set B of points blocks
  the k-holes of P if any k-hole of P contains an element of B in its interior"; cites Katchalski–Meir and
  Czyzowicz–Kranakis–Urrutia for blocking 3-holes. The journal version was not checked. *Relevance:* the nearest
  "hitting set of convex polygons" literature; blockers lie outside P and the polygons are empty, so it is a different
  notion (row 1). Czyzowicz–Kranakis–Urrutia, "Guarding the convex subsets of a point-set", CCCG 2000: bibliographic
  record only, not read.
- **[Suk]** A. Suk, "On the Erdős-Szekeres convex polygon problem", J. Amer. Math. Soc. 30 (2017) 1047-1053,
  <https://arxiv.org/abs/1604.08657> (abstract read): ES(n) = 2^{n+o(n)}. **[HMPT]** A. F. Holmsen, H. N. Mojarrad, J. Pach, G. Tardos,
  "Two extensions of the Erdős-Szekeres problem", <https://arxiv.org/abs/1710.11415> (abstract read; journal J. Eur. Math. Soc. 22 (2020)
  3981-3995, details not verified): Suk's theorem "generalizes to convexity structures induced by pseudoline
  arrangements" (the abstract setting that contains signotopes, by this check's reading) and improve the error term; for
  families of convex bodies c(n) ≤ c′(n) ≤ 2^{n+O(√(n log n))}. Their arXiv LaTeX sources were searched today for
  remov / delet / transversal / hitting / leftmost / rightmost: no hit in Suk's source; in HMPT only the proof device of
  "left convex chains" and "right convex chains" ("if |C| = 3, then C is either a left convex chain or a right convex
  chain, but not both"), a transitive colouring used to find cups and caps between separators. *Relevance:* context;
  asymptotic bounds; no decomposition, hitting-set or rooted statement found. The proofs were not read in full.
- **[SP06]** G. Szekeres, L. Peters, "Computer solution to the 17-point Erdős-Szekeres problem", ANZIAM J. 48 (2006)
  151-164, doi:10.1017/S144618110000300X (abstract read on the publisher page): "The proof makes use of a combinatorial
  model of planar configurations, expressed in terms of signature functions"; the model is larger than the realizable
  configurations. *Relevance:* the n = 6 background; the vacuity of (5,6)-valid signotopes at 16 points used today is the
  project's own certificate (DELTA2N base(5,6,16)), consistent with SP06 plus the ETV join argument and with GLitchfield
  experiment 0112 (prior).
- **SAT-based works** (methods only; none treats hitting sets or Δ-type ∀∃ statements, by abstract or prior reading):
  Balko–Valtr, "A SAT attack on the Erdős-Szekeres conjecture" (European J. Combin. 66 (2017) 13-23; prior);
  Scheucher, arXiv:1807.10848 and arXiv:2105.08406 (prior); Heule–Scheucher, "Happy ending: An empty hexagon in every
  set of 30 points", arXiv:2403.00737 (prior); Subercaseaux–Nawrocki–Gallicchio–Codel–Carneiro–Heule (formal
  verification of the empty hexagon number), arXiv:2403.17370 (prior); Subercaseaux–Mackey–Heule–Martins (minimizing
  pentagons), arXiv:2311.03645 (prior); Subercaseaux–Mackey–Qian–Heule, arXiv:2506.00224 (prior);
  **[KPH]** Krapivin–Przybocki–Heule, "Toward Satisfiability Modulo Realizability", <https://arxiv.org/abs/2607.02958>
  (abstract read today; its LaTeX source has no mention of final polynomials): SAT over abstract order types guided toward realizable ones by "partial realizability feedback". *Relevance:*
  [KPH] is the closest method analogue of the project's SAT + realizability (CEGAR/BFP) loop that produced the real
  ROOT(6)/ROOT(7) counterexamples; [HP756] §10 is the closest analogue of its ∃∀ encodings.
- **Realizability tools** (methods only): J. Bokowski, J. Richter, "On the finding of final polynomials", European J.
  Combin. 11 (1990) 21-34 (DBLP record <https://dblp1.uni-trier.de/rec/journals/ejc/BokowskiR90.html> seen; text not
  read); J. Bokowski, B. Sturmfels, *Computational Synthetic
  Geometry*, LNM 1355, Springer 1989 (not read; cited through the next two items); K. Fukuda, S. Moriyama,
  H. Nakayama, "Every non-Euclidean oriented matroid admits a biquadratic final polynomial", arXiv:math/0510500
  (abstract read: extends Richter-Gebert's theorem for uniform oriented matroids); M. Firsching, "Realizability and
  inscribability for simplicial polytopes via nonlinear optimization", arXiv:1508.02531 (abstract read: nonlinear
  optimization to realize; that it uses biquadratic final polynomials for non-realizability is known here only from a
  search-result summary); S. Felsner, H. Weil, "Sweeps, arrangements and
  signotopes", Discrete Appl. Math. 109 (2001) (author copy
  <https://page.math.tu-berlin.de/~felsner/Paper/sas-dam-rev.pdf> located, not read; venue details not verified).
  **Precedent in ES-type SAT work (read today in the LaTeX source of Heule–Scheucher, arXiv:2403.00737, extended
  version):** for 23-point signotopes with no 7-gon and no 6-hole, "all tested configurations are provably
  non-realizable using the method of bi-quadratic final polynomials [Bokowski–Richter 1990]". So the step "SAT model,
  then a BFP certificate of non-realizability" used today for the abstract ROOT(6) / ROOT(7) models (claims
  root6-m15-main-nonrealizable, root7-m17-nonreal-1, root7-m17-t3-nonrealizable: three-term Grassmann–Plücker
  inequalities with positive multipliers summing to zero) is established practice. *Relevance:* methods only; the
  project already cites Bokowski–Richter 1990 (C4CUT, FLAYER, ALGAN).
- **Cups-caps decompositions** (context; prior unless marked): Chvátal–Komlós 1971 **[CK71]**; Moshkovitz–Shapira,
  arXiv:1206.4001 **[MS14]**; **[FPSS]** Fox–Pach–Sudakov–Suk, "Erdős-Szekeres-type theorems for monotone paths and
  convex bodies", arXiv:1105.2097 (LaTeX source searched today: section "Transitive colorings": a q-colouring of the
  k-subsets is transitive if, whenever the consecutive k-subsets of i_1 < … < i_{k+1} lie in one colour class, all
  k-subsets do; HMPT recall the notion for triples, crediting FPSS and Hubard–Montejano–Mora–Suk); Baek–Balko, SoCG 2025 and JCTA 222 (2026) 106195 (split k-gons, decomposable
  sets); Damásdi–Dong–Scheucher–Zeng, "Saturation results around the Erdős-Szekeres problem", arXiv:2312.01223 (abstract
  read today; saturation by added points, not a hitting-set statement); D. Conlon et al., "Big line or
  big convex polygon", Comput. Geom. 2025 (Consensus abstract read; full author list not verified; an extension of the
  cups-caps theorem). None states a Δ-type statement.

- **Prior sources referred to by tag** (read in NOVELTY20261113B; links there): **[ETV96]** Erdős–Tuza–Valtr,
  "Ramsey-remainder", European J. Combin. 17 (1996) 519-532 (1993 report read there); **[Jav]** T. Javůrek, "Uncovered
  hull vertices and upper bounds for convex polygons", Figshare 34875984 (Lemma 3, the endpoint split); **[Sch]**
  M. Schroeder, "Erdős-Szekeres: upper bounds for convex heptagons and octagons", Zenodo 10.5281/zenodo.22842891
  (Lemma 5.3); **[GL-PS]** GLitchfield/erdos-szekeres-convex-poly, PASCAL-SPLIT notes (2-4 Oct 2026).

## 3. Search log

Queries (no personal name, e-mail address or repository name of the owner was put into any query; GitHub API calls
were unauthenticated, with a generic user agent):
- Web search (11): transversal of convex k-gons; removing points to destroy all convex (n−1)-gons with a cap-free
  subset; "guarding the convex subsets of a point-set"; hypergraph of convex k-subsets, transversal number; "4-cap free"
  subset meeting every convex polygon with "no 5-cap"; Bokowski–Richter final polynomials; Felsner–Weil signotopes;
  "rightmost point" induction with hitting cap/cup decompositions; ETV recursion N(a,b,n) ≤ N(a−1,b,n) + N(a,b,n−1);
  "biquadratic final polynomial" with Erdős–Szekeres / k-holes / signotopes; minimum number of points whose deletion
  destroys all convex k-gons. None returned a source stating a Δ-type statement.
- arXiv API (4): Erdős–Szekeres with transversal / hitting set / blocking set / piercing (1 hit, unrelated); date-sorted
  Erdős–Szekeres and convex-position listings (newest indexed items 11 Nov 2026: nothing on ES-type polygon bounds or
  decompositions; the morning check scanned to 15 Nov 03:00); abstracts of 2206.04260, 1710.11415, 1604.08657,
  2312.01223, 1505.07549, 2607.02958, math/0510500, 1508.02531.
- Consensus (2): subsets of a planar point set meeting every convex k-gon (3 results: Baek–Balko JCTA 2026, Conlon et
  al. 2025, Valtr 2007); removing a cap-free subset to destroy all convex (n−1)-gons (3 results: Baek–Balko 2026,
  Suk 2017, Baek 2024). Consensus returns 3 results per query on this plan.
- Pages and files read: the LaTeX sources of Baek, Suk, HMPT, FPSS, Heule–Scheucher (extended version) and KPH
  (keyword searches, plus Baek §2 and §5 in full); [HP756]; GitHub API commit lists and trees of gotrevor/es7-ladder (last
  commit 7 Oct 2026) and GLitchfield/erdos-szekeres-convex-poly (last commit 20 Oct 2026; 17,487 paths, file names
  filtered for transversal / hitting / root / delta / peel / envelope / terminal / split, five notes opened); [Jun];
  [CGHSTU]; [SP06] publisher page; the numdam record of [ES35]; erdosproblems.com forum (HTTP 403). One fetched PDF
  (<https://www.matem.unam.mx/~urrutia/online_papers/GuardConv.pdf>) turned out to be Czyzowicz–Rivera-Campo–Urrutia–
  Zaks, "Guarding Convex Sets" (guarding families of disjoint convex sets), unrelated.

## 4. Unread sources that could change a verdict

- erdosproblems.com/107 and its forum thread: HTTP 403 again (as on 13 Nov).
- Full texts of Suk 2017 and HMPT 2020 (abstracts read; LaTeX sources searched for a few words only); the journal versions of Balko–Valtr 2017 and
  Baek–Balko 2026 (still unread, as in the earlier checks); Erdős–Tuza–Valtr 1996 journal version.
- Erdős–Szekeres 1935 original (the endpoint argument was read in lecture notes); Czyzowicz–Kranakis–Urrutia 2000;
  the journal version of the k-hole blocking paper; Morris–Soltan surveys (2000, 2016), not opened.
- GLitchfield repository: only file names and five notes were checked; the tree listing is complete (17,487 paths),
  but notes whose names do not contain the filter words were not opened.
- MathOverflow / Math.StackExchange were not searched today (blocked or rate-limited in the earlier checks).
- arXiv has no full-text search; a paper that states a Δ-type lemma only in its body would be missed.

## 5. Wording advice if this is written up

- State weak D(5,n), LR, TWO-ENV#, LP0, CB and ONE as the project's conjectures, with "not found in this search"; cite
  [ES35] (cup analogue and endpoint sets), [Baek] (Δ-removal, M(4;n)), [GL-PS] and [HP756] (strong splits; the
  transversal cup; 2QBF/CEGAR), and the earlier checks' must-cite list (NOVELTY20261113B §7).
- Present weak D(4,n) as implied by gotrevor's L1(4,b) conjecture; do not present the a = 4 transversal-cup idea as the
  project's.
- Present the ROOT / CONJ-TS′ / ENV# / TS± refutations as refutations of the project's own induction schemes (no
  literature statement is refuted).
- Cite [KPH] and Bokowski–Richter 1990 for the realizability loop, and [HP756] §10 for ∃∀ split searches.
