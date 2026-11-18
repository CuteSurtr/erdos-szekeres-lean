# WATCH_1118: literature watch and targeted checks of 18 November 2026 (track NOV)

**Status: COMPLETE for the scheduled scope (03:10 KST); may get small additions until 08:20 KST.** No unit was started
(compute-free track; the only computation is a sub-second exact check of public colourings, §2b). Work directory
`/home/jay/research/data/roadmap-20261115/pm1115/nov1118/` (abbreviated N below).
**Rigor: evidence only (bounded, read-only web check).** "Not found in this search" is the strongest positive wording;
it is never "new" in any other sense and never a priority claim.

Scope (wave A task, 18 Nov 02:30 KST):
1. Watch since [WATCH_1116.md](WATCH_1116.md) (16 Nov, 18:25-18:43 KST).
2. Targeted checks: (a) upper bounds for N(8; 6, 6) and for every Erdős–Tuza–Valtr (ETV) number with n = 8;
   (b) N(8; 5, 8) and N(7; 5, 7); (c) "geometric k-gon saturation is not an order-type invariant"; (d) ES(8) ≤ 307/308.
3. The consolidated map [NOVELTY_MAP_1118.md](NOVELTY_MAP_1118.md).

Notation: N(n; a, b) = largest size of a planar set in general position with distinct x, no a-cap, no b-cup and no
convex n-gon (Baek's N(n, a, b); Schroeder's M_n(a, b); Balko–Valtr's N(a, u, k) with k = n; ETV's m(k; l, l′) with
l = cup length, l′ = cap length). ETV value Σ_{i=n−b}^{a−2} C(n−2, i). Cup–cap bound C(a+b−4, a−2).

Privacy: no request contained the owner's name, e-mail, GitHub user or the repository name. GitHub and Stack Exchange
were queried unauthenticated with a generic client name.

## Verdicts in brief

| # | item | verdict |
|---|---|---|
| 1 | Watch since 16 Nov 18:43 KST: arXiv (Tue 17 Nov announcement, all four categories), arXiv API, Zenodo, Schroeder's site, erdosproblems.com/107 and forum, GitHub, Figshare, MathOverflow/Math.SE, zbMATH Open, Wikipedia | **nothing new** that bears on any project claim |
| 1a | Public ES(8) upper bound | still **319** (Schroeder, Zenodo 22842891, v1 only; versions API total = 1; v2/v3 PDF URLs 404; sitemap unchanged since 9 Nov). Refereed: 408 |
| 2a | Published upper bound for N(8; 6, 6) below the cup–cap 70 | **not found in this search** (ETV 1993/96, Balko–Valtr ENDM 2015 + data, Szekeres–Peters 2006, Scheucher's SAT papers, Heule–Scheucher, SMQH, KPH, Koshelev–Koshka, Dumitru, Baek, Baek–Balko SoCG, Mojarrad–Vlachos, Schroeder v1 read in full text or LaTeX source). Published n = 8 ETV upper bounds that **do** exist: (4, 8) = 22 [Baek]; (7, 8) ≤ 406 [Mojarrad–Vlachos]; (8, 8) ≤ 407 [Mojarrad–Vlachos]; unrefereed (7, 7) ≤ 193 and (8, 8) ≤ 318 [Schroeder]; trivially every N(8; a, b) ≤ ES(8) − 1 (≤ 318 unrefereed, ≤ 407 refereed) |
| 2b | N(8; 5, 8) ≤ 65 and N(7; 5, 7) ≤ 36 | **not found in this search** (no public bound below 78 resp. 41 derivable, 84 resp. 56 cup–cap); nothing new since 13 Nov. **Definition check:** Balko–Valtr's abstract values are for *strong* gons, the project's colouring statements for *weak* gons; exact check of all eight published Balko–Valtr colourings (claim `nov-bv-weak-strong`, CONFIRMED by VS 02:48) |
| 2c | "Geometric k-gon saturation is not an order-type invariant" (`lb-ln-ddsz28-real`) | the **mechanism is known** ("well known" in Aichholzer–Krasser, EWCG 2005 / CGTA 2006: a fixed realization does not yield all one-point extensions, with a 5-point example); the **saturation statement itself was not found in this search** (DDSZ, Damásdi et al. 2021 and the saturation literature do not state it) |
| 2d | ES(8) ≤ 307/308 or anything below 319 in public | **not found in this search**; the only public page with a figure below 319 is the project's own public repository (a self-hit, README still at 314) |
| 2e | Three items no novelty record covered (ES7SPLIT, Catalan rule, 49 vs 46) | C6 related (Javůrek, Baek–Balko), the z-split statement not found; Catalan rule and the 49-vs-46 correction **not found in this search** |
| 2f | Today's saturation results (track L): sat_g(6) ≤ 14, sat_g(7) ≤ 20, sat_g(8) ≤ 31, order-type saturation without maximality | **not found in this search**; the only published bounds are DDSZ's sat_g(n) ≤ 7/8 · 2^(n−2) for n ≥ 7 (28, 56); DDSZ have no citing works in OpenAlex or Semantic Scholar |

## 1. Watch since 16 Nov 18:43 KST

- **arXiv announcements.** The newest listing is "Tuesday, 17 November 2026" (announced 17 Nov 10:00 KST); the
  Wed 18 Nov listing appears at 10:00 KST, after this track. `/list/<cat>/new` fetched 02:32 KST
  (N/arxiv-new/): math.CO 70 new + 27 cross + 53 replacements; cs.CG 2 + 5 + 4; cs.DM 5 + 13 + 8; math.MG 5 + 5 + 5.
  Keyword scan of every title and abstract (parser `N/tools/parse_list.py`, copy of WATCH_1116's) gave 38 hits (33
  distinct entries), none relevant. The closest:
  - arXiv:2611.21416 (Milojević–Morawski–Sudakov–Tomon, "Polynomial bounds for quasiplanar graphs"): uses
    "Erdős–Szekeres type combinatorial arguments" for k-quasiplanar graphs. Not relevant.
  - arXiv:2611.19433 (bicoloured point sets, order types), 2611.19600 (deepest pairs, convex position),
    2611.19543 (caps in F_3^n), 2611.21470 (Reinhardt conjecture; "octagon" = smoothed octagon). Not relevant.
  - Also scanned (03:20 KST): cs.LO (8 + 10 + 21 entries) and cs.AI (135 + 293 + 289) for Szekeres, convex position,
    happy ending, signotope, order type, k-gon/hexagon/heptagon/octagon, Ramsey: no hit.
- **arXiv API**, newest first (N/arxiv-api/q1-q8): Szekeres; "happy ending"; "convex position"; signotope(s);
  "order type" AND points; Tuza AND Valtr; saturation AND convex; cups and caps. Newest Erdős–Szekeres-type items:
  2611.21416 (above) and 2610.28305 (permutation patterns, 20 Oct, known). Nothing new on convex polygons.
  Version check (N/arxiv-api/idl2.xml): 2604.20120 v1, 2512.24061 v1, 2607.02958 v1, 2506.00224 v1, 2312.01223 v3,
  2511.02864 v3, 2206.04260 v2, 2403.00737 v1, 1510.06255 v2: no new version.
- **Zenodo.** Versions API of record 22842891: total = 1 (v1, 19 Sep 2026; files md5 f05d6b63… and a3376908…, as on
  16 Nov). Searches by title/description (Szekeres, "Erdos-Szekeres", "happy ending", "convex octagon", "convex
  heptagon", signotope), newest first: nothing after 19 Oct 2026 (23485633, known).
- **Schroeder's site.** Companion page: "Preprint · Version 1 · 19 September 2026", "We prove ES(7) ≤ 81 and
  ES(8) ≤ 319". `_v2.pdf`, `_v3.pdf`: HTTP 404. Sitemap lastmod 2026-11-09 (unchanged).
- **erdosproblems.com/107** (02:34 KST): "This page was last edited 11 April 2026", Comments (2), Proof claims (0);
  forum thread: same two comments of December 2025, "The ability to post new comments has been suspended."
- **GitHub** (unauthenticated): gotrevor/es7-ladder last push 7 Oct; GLitchfield/erdos-szekeres-convex-poly last push
  20 Oct; teorth/erdosproblems last push 12 Nov; jcpaik/erdos-tuza-valtr 24 May; jcpaik/erdos-szekeres-sat Aug 2025;
  bsubercaseaux/automatic-symmetries May 2025. Repository search ("erdos szekeres", "happy ending problem", "convex
  octagon"): one new repository since 16 Nov, sebastian-hanisch/erdos-szekeres-demo (17 Nov), a Streamlit demo on
  monotone subsequences and Greene's theorem (not the polygon problem); plus the project's own repository (self-hit).
- **Figshare**: Javůrek's 34875984 still version 1 (1 Nov 2026).
- **MathOverflow and Math.SE** (Stack Exchange API, since 10 Nov): no question on Erdős–Szekeres, happy ending,
  convex position (one unrelated hit) or convex octagons.
- **zbMATH Open** (2025-2026 "Erdős-Szekeres" documents; "Tuza Valtr conjecture"; "Ramsey-remainder"; saturation and
  convex position): only known items. The zbMATH review of Baek (EJC 124 (2025) 104085) calls P(n, 4, n) "the first
  result on the strengthened conjecture".
- **Wikipedia** "Happy ending problem": only a bot edit since 11 Aug (15 Nov, archive links); still "The value of f(N)
  is unknown for all N > 6".
- **MathWorld** "Happy End Problem" (03:34 KST): no ES(7) or ES(8) bound on the page (the site-wide stamp reads "Last
  Updated: Mon Nov 16 2026").

## 2. Targeted checks

### 2a. Upper bounds for N(8; 6, 6) and for the ETV numbers with n = 8

Project: 50 ≤ N66 = N(8; 6, 6) ≤ 56 CERTIFIED; N66 ≤ 55 reached at 04:28 (all 132 level-14 cubes accepted, cover
complete; claim `n66-le55-cubes-1118`, filed 04:33 by the main session, CONFIRMED by VS 04:33); ETV value 50; cup–cap
70.

Sources read (full text or LaTeX source unless stated) and what they state:
- **Erdős–Tuza–Valtr**, "Ramsey-remainder" (FU Berlin report B 93-01, Feb. 1993, read in full from the archived
  PostScript, N/papers/etv93/; the journal version EJC 17 (1996) was not read). They define m(k; l, l′) ("no convex
  k-set, no convex l-sequence, no concave l′-sequence"), prove only the **lower** bound "Claim 17 … m(k; l, l′) ≥
  Σ_{i=k−l′}^{l−2} C(k−2, i)" and state "Conjecture A′: The bound in Claim 17 is exact" (formulas transcribed from
  the PostScript text). Upper bounds: only the cup–cap case ("[ES 35] proved m(k; l, l′) = C(l+l′−4, l−2)" when
  k = l + l′ − 2) and "Conjecture A is known to be true for n ≤ 5". **No upper bound for any nontrivial n = 8 case.**
- **Balko–Valtr**, ENDM 49 (2015) 425-431 (the EJC 66 (2017) full text is still unread: ScienceDirect blocks automated
  clients; zbMATH has no review text "due to conflicting licenses"): "The best known upper bound for N(a, u, k) is
  N(a, u, k) ≤ C(a+u−4, a−2), which is obtained from the trivial estimate"; "Proposition 3.2 For every integer k ≥ 3,
  we have N(4, k, k) ≤ C(k, 2) − 1"; pseudolinear SAT: "we have N(4, 7, 7) = 16 and N(4, 8, 8) = 22".
- **Szekeres–Peters**, ANZIAM J. 48 (2006) 151-164 (full PDF, open on Cambridge Core): n = 6 only; no ETV numbers;
  "It would be of great interest to also verify (P_{σ,6}), but at present this seems to be out of reach." (the
  subscript is garbled in the PDF text and was read from the context)
- **Scheucher's SAT papers** (arXiv:1807.10848, 2105.08406, 2504.02650, 2409.01723, abstracts): holes, higher
  dimensions, drawings; no ETV numbers (2105.08406 source: "for the planar k-gons g^(2)(5)=9, g^(2)(6)=17 … and
  g^(2)(k) ≤ C(2k−5, k−2)+1 are known"). **Heule–Scheucher** (2403.00737, extended-version source): empty hexagons;
  "we are optimistic that we can determine the 7th Erdős–Szekeres number g(7) on a computing cluster with some further
  engineering"; the only octagon mention is "A set of 29 points with no 6-hole and no 8-gon [Overmars]". **SMQH**
  (2506.00224, source): "The only further values known are g(5) = 9 and g(6) = 17"; "we suspect that there are symmetric
  constructions for all k ≥ 7". **KPH** (2607.02958, source): "PointSAT can find a set of 26 points with no 5-cap or
  7-gon. The existence of such a set follows from a theorem of Erdős, Tuza, and Valtr". **Koshelev–Koshka**
  (2604.20120), **Dumitru** (2512.24061), **Balko–Scheucher–Valtr** (2203.07518): no ETV upper bound.
- **Baek** (2206.04260 source; EJC 124 (2025) 104085): "Theorem (Main Theorem). For any n ≥ 3, the statement
  P(n, 4, n) holds. That is, C(n−1, 2) + 2 points on a plane in general position determine either a 4-cap or a
  n-gon"; "this is the first new instance of Conjecture [ETV] proven so far since the original 1935 paper". At n = 8:
  **N(8; 4, 8) = 22**.
- **Mojarrad–Vlachos** (1510.06255 source; DCG 2016): "Let n ≥ 6 … the set S of f(n−1, n−1) + g(n, n−2) + 1 points
  … Then S contains an (n−1)-cap or a convex n-gon", g(m, l) = C(m+l−4, l−2) − C(m+l−6, l−3). At n = 8: 252 + 154 + 1 =
  407 points, so **N(8; 7, 8) ≤ 406** (cup–cap 462, ETV value 63), and ES(8) ≤ 408.
- **Schroeder** v1 (PDF, md5 f05d6b63…): "Write M_n(a, b) for the maximum size of a set avoiding a convex n-gon, an
  a-cap, and a b-cup"; "Proposition 7.2 (Balanced octagon bound). C8 = M8(7, 7) ≤ 193"; "Proposition 7.6 (Residual
  octagon bound). D8 ≤ 124"; §9: "M8(6, 6) ≥ 50" and the table "D8 ≥ 50 … ≤ 124 … ≤ 57" under ETV. **No upper bound
  on M8(6, 6) is stated.** Unrefereed. His proof archive (Zenodo zip, 240 MB, 323 members; the central directory and
  five text members read by HTTP range requests, tool `N/tools/zip_range_get.py`) has certificates only for C8 ≤ 193,
  D8 ≤ 124, the restricted 25-point and the residual 26-point examples; its `literature/REVIEW.md` says: "The Baek–Balko
  conference text, §2.1, states the known ETV ranges n≥a+b−3 or a=4 or b=4", and repeats "M8(6,6)≥50" as a lower
  construction only.
- **Baek–Balko** (SoCG 2025, LIPIcs 332:13; JCTA full text unread): Theorem 4/6 give ES_split(6, 6, 8) = 51 for
  *split* 8-gons ("a split k-gon can contain k or k + 1 points"), which are not necessarily convex, so no bound on N66;
  Theorem 8 gives 50 for **decomposable** sets only ("The proof of Theorem 8 is omitted" in SoCG).
- **Strunk**, "Two upper bounds for the Erdős–Szekeres number with conditions", DCG 49 (2013): the Springer PDF is
  behind a JavaScript challenge; the zbMATH review (L. A. Székely) says the conditions are on the convex hull ("no point
  inside a triangle determined by three consecutive vertices of its convex hull"; "convex hull is an (n−1)-gon"). Not
  an ETV result.
- Background re-confirmed: Chung–Graham, Kleitman–Pachter, Tóth–Valtr bound only ES(n) (the case a = b = n).
- **Citation sweep** (OpenAlex, 03:15 KST, `N/openalex/`): all 16 works citing ETV 1996, all 10 citing Balko–Valtr
  2017 and all 3 citing Baek (EJC 2025), newest first. Besides the papers above they are: Krapivin–Przybocki–Heule (LNCS
  2026), "A Survey on Ordered Ramsey Numbers" (2026; arXiv 2502.02155, source read: "It is only known that the
  conjecture is true for n ≤ 6", no ETV values), Lean Pool (arXiv 2026), Scheucher's and others' SAT papers, and
  older surveys and Ramsey-remainder papers (Károlyi 2001, Pór–Valtr 2002, Rosta 2004, Gerken's 2006 thesis, behind an
  anti-bot page and not read). None has an upper bound for an ETV number with n ≥ 7 beyond those listed.

**Verdict (2a).** No upper bound for N(8; 6, 6) below 70 was found, in refereed or unrefereed sources; the project's
N66 ≤ 64 (13 Nov), ≤ 57, ≤ 56 (CERTIFIED) and ≤ 55 (04:28) are **not found in this search**. The only published
n = 8 ETV upper bounds found: (8; 4, 8) = 22 and its mirror (Baek; Lean-checked by Baek), (8; 7, 8) ≤ 406 and its
mirror (Mojarrad–Vlachos), (8; 8, 8) = ES(8) − 1 ≤ 407 (Mojarrad–Vlachos), and, unrefereed, (8; 7, 7) ≤ 193 and
ES(8) ≤ 319 (Schroeder). The trivial cases a + b ≤ 11 follow from cup–cap. So **N(8; 6, 6), N(8; 5, 7), N(8; 5, 8),
N(8; 6, 7), N(8; 6, 8) have no published bound below cup–cap** (70, 56, 84, 126, 210), as far as found. Printed lemmas
give two derivable improvements that nobody states: N(8; 5, 8) ≤ 22 + 56 = 78 (NOVELTY20261113B C3) and
N(8; 6, 8) ≤ 78 + 126 = 204 (endpoint split, below).

**Remark (corollaries of the project's bounds; claim `nov-etv8-corollaries`, filed 03:08, CONFIRMED by VB 03:15;
corrected by claim `nov-etv8-corollaries-correction`, filed 03:17, CONFIRMED by VS 03:25).** The classical endpoint split
N(k; a, b) ≤ N(k; a−1, b) + N(k; a, b−1) (right ends of (a−1)-caps; printed as Javůrek's Lemma 3) turns B1 and B2 of
the map into N(8; 6, 7) ≤ 56 + 56 = 112 (cup–cap 126) and N(8; 6, 8) ≤ 65 + 112 = 177 (cup–cap 210, derivable 204);
also N(8; 7, 7) ≤ 224, which Schroeder's unrefereed 193 beats. **Correction:** the claim's item (iv),
N(8; 7, 8) ≤ 401 < 406, is true but empty: every N(8; a, b) is at most ES(8) − 1, so the project's Lean-checked
ES(8) ≤ 310 already gives N(8; 7, 8) ≤ 309 (Schroeder's unrefereed 319 gives 318). Do not quote 401. With N66 ≤ 55
the two useful numbers become 111 and 176. These are one-line corollaries of low value. Nothing follows for ES(8).

**The trivial bound N(8; a, b) ≤ ES(8) − 1.** It makes Schroeder's unrefereed 319 an upper bound of 318 for every
N(8; a, b), the refereed 408 one of 407. It improves on the bounds listed above only for (8; 7, 8): the best public
bound there is 318 (unrefereed), and 406 among refereed statements.

### 2b. N(8; 5, 8) ≤ 65 and N(7; 5, 7) ≤ 36; the colouring statements

- No new source since the 13 Nov and 16 Nov checks (§1). The public baselines stay: N(8; 5, 8) ≤ 78 derivable from
  printed lemmas (cup–cap 84; ETV 42); N(7; 5, 7) ≤ 41 derivable (Javůrek Lemma 3 with Baek and Schroeder), 51 from
  refereed statements alone (cup–cap 56; ETV 26). GLitchfield experiment 0112, gotrevor's PLAN.md and Javůrek still
  list (7; 5, 7) at 27 points as open (repositories unchanged since October). **Verdict: not found in this search.**
- **The open definition comparison** (NOVELTY20261113B §10; ETV7SAT20261113 §9.1, phase-2 remark "the two abstract
  models must differ") is now settled from the sources:
  - Balko–Valtr (ENDM 2015): a k-gon in a colouring is "a red and a blue monotone path that are vertex disjoint
    except for the common end-vertices"; their `generator.cpp` (`findGons`) splits the interior vertices of each
    k-subset between the two paths, so only such gons are forbidden.
  - Szekeres–Peters 2006: a convex k-subset is "the union of a cup-cap pair with common endpoints", of k points.
  - Baek–Balko (SoCG 2025 §2.3): "a weak k-gon … Note that the red and the blue monotone path can share other
    vertices … If we exclude this possibility … we call such ordered subhypergraph a strong k-gon … Balko and Valtr [4]
    proved C_strong(7) > 33 … ▶ Theorem 7. We have C_weak(7) > 33."
  - The project's colouring model (ETV7SAT §2.1, clause C4) and Baek's Lean theorem use **weak** gons.
- **Exact check (own code; claim `nov-bv-weak-strong`, filed 02:43, CONFIRMED by VS at 02:48 with its own code and a
  C++ brute force over all k-subsets, [VERIFY_NOV_BV_WEAK_STRONG.md](VERIFY_NOV_BV_WEAK_STRONG.md)):** all eight
  colourings on Balko–Valtr's data page satisfy their stated path restrictions and contain **no strong** k-gon, but **each contains a weak k-gon** (1, 1, 6,
  2, 7, 10, 2, 1 witnesses for the files 7Gon4Red_17, 7Gon5Red6Blue_26, 7Gon5Red_27, 7Gon6Red6Blue_31, 7Gon6Red_32,
  7Gon_33, 8Gon4Red_23, 9Gon4Red_30; e.g. in the 26-vertex colouring the red path (18, 22, 23, 25) and the blue path
  (18, 19, 23, 24, 25) share vertex 23). The 27-vertex colouring of ETV7SAT item 4 has **no weak heptagon**, longest
  cap path 4, longest cup path 6 (third independent check). Controls: 10 realizable colourings (6 random 11-point sets
  checked at k = 5 and 6, 4 pentagon-free 8-point sets at k = 4 and 5; 20 comparisons with brute-force convex position,
  all agreeing; the claim text says "12 realizable colourings", which counts the first group's comparisons) and a
  4-vertex weak-but-not-strong example; VS ran 300 further controls. Files: N/tools/weakgon_check.py, N/weakgon_report.json.
- **Consequences for wording.**
  - Balko–Valtr's N̂(5, 6, 7) ≥ 26, N̂(5, 7, 7) ≥ 27, N̂(4, 7, 7) = 17, N̂(4, 8, 8) ≥ 23 are strong-gon statements.
    They do not contradict ETV7SAT item 3 (every 26-vertex colouring has a 5-cap path, a 6-cup path or a weak
    heptagon, CERTIFIED) nor Baek's weak-gon theorem; the colourings they publish contain the weak gons those
    statements require.
  - ETV7SAT item 3 (weak colouring (5, 6, 7) = 25): **not found in this search**; it shows that the weak and strong
    abstract models differ at (5, 6, 7) (Balko–Valtr's 26-vertex colouring is strong-free, weak-not-free).
  - ETV7SAT item 4 (a 27-vertex weak-heptagon-free colouring with no 5-cap path and no 7-cup path): **related, must
    cite** Balko–Valtr N̂(5, 7, 7) ≥ 27 (the strong version) and Baek–Balko Theorem 7 (C_weak(7) > 33, the diagonal
    weak case). The weak (5, 7, 7) instance itself was **not found in this search**; whether the JCTA version of
    Baek–Balko states it is unknown (full text unread).

### 2c. Saturation is not an order-type invariant (`lb-ln-ddsz28-real`, `lb-ln-ddsz-block`)

- **Mechanism: known.** Aichholzer–Krasser, "Abstract order type extension and new results on the rectilinear crossing
  number", EWCG 2005 extended abstract (TU Graz PDF, sha256 858cb25f…; journal version CGTA 36 (2006) 2-15, not
  read): "It is well known that an extension technique relying only on the geometric realizations of the data base
  cannot guarantee completeness of the extension, see Figure 1. For a specific n-point realization of an order type
  we cannot derive all required n + 1 order types just by adding a new point to this realization." Figure 1: "Two
  realizations of the order type of five points in convex position. Only the right point set can be extended in a way
  such that the resulting point set has three points on its convex hull."
- **The saturation statement: not found in this search.** DDSZ (arXiv v3 source, re-read): saturation is checked
  cell by cell in the arrangement of lines spanned by a fixed P ("These lines cut the plane into polygonal cells …");
  their hand check of the 8-point (4, 5) block uses a coordinate fact ("the intersection between the lines p1p3 and
  p6p8 are outside Δ"), and Proposition 14 assumes "very generic" blocks; no sentence says that another realization
  of the same order type may fail to be saturated. Damásdi–Keszegh–Malec–Tompkins–Wang–Zamora, "Saturation problems in
  the Ramsey theory of graphs, posets and point sets" (EJC 2021; arXiv 2004.06097 source): semisaturation of convex
  k-sets; no order-type statement. Web and zbMATH searches: nothing else.
- **Verdict.** State `lb-ln-ddsz28-real` as an instance, for k-gon saturation, of the known realization dependence of
  one-point extensions (cite Aichholzer–Krasser), with DDSZ's 28-point set as the explicit example: the instance was
  not found in this search; the phenomenon is not new.
- **Remark (reasoning only, not literature).** For the other Ramsey-type saturation problem on point sets in this
  literature, monotone point sets (Damásdi et al. 2021: "A sequence S of distinct numbers (resp. point set with
  distinct x- and y-coordinates) is called (k,l)-saturated if …"), saturation *is* a combinatorial invariant: a new
  point's type is fixed by the x-interval and the y-interval it falls into, and every realization of the same permutation offers all of them. The difference for
  cups, caps and convex k-gons is that the possible new points are the cells of the arrangement of lines spanned by the
  set, which the order type does not determine. A write-up could use this contrast in one sentence.

### 2d. ES(8) ≤ 307/308

Nothing below 319 in public (§1): Zenodo, Schroeder's site, arXiv, erdosproblems.com, Wikipedia, MathWorld-type pages
(not re-opened), GitHub, web search. The web search surfaced the project's own public repository (README at 314) as
the only page with a lower figure; it is a self-hit. ES(8) ≤ 310 (Lean-checked), ≤ 309 and ≤ 308 (computer-assisted
chains, unrefereed) remain **not found in this search** as public statements by others.

### 2e. Three results that no earlier novelty record covered (for NOVELTY_MAP rows C6, D6, D7)

- **ES7SPLIT (RESULTS C9): z-splits of 33-point heptagon-free sets exist iff N(7, 5, 7) ≥ 27.** Javůrek's draft (Figshare
  34875984 v1, PDF md5 e2fadb21…, read): "Lemma 2. For n ≥ 4, B_n − 1 = M_{n+1}(n − 1, n + 1)", where B_n is "the largest
  size of a planar point set with no convex (n + 1) polygon and with a hull vertex on no convex n polygon"; "a certified
  exclusion of 28 points with an uncovered hull vertex at size six would imply ES(7) ≤ 78". This ties the same ETV case
  (7; 5, 7) to ES(7) by a projective map, through a different structure (an uncovered hull vertex, not a split).
  Baek–Balko's decomposable sets ("A is deep below B") are the nearest notion of split; their Theorem 8 is recursive
  and gives no statement about one split. **Verdict: related (cite both); the z-split statement not found in this
  search.**
- **CATALAN20261110 (RESULTS D7): m-fold sets of m(Cat(h+1) − Cat(h)) + 1 points, m = 2h + 1.** Web search (rotational
  symmetry, Catalan numbers, convex position): nothing; OEIS has no sequence matching 16, 64, 253, 991 (the sizes for
  h = 2..5; `N/oeis/`). **Verdict: not found in this search.**
- **SYM16FIVE20261110 (RESULTS D8): at least 49 fivefold 16-point hexagon-free order types, against SMQH's 46.** No
  public correction: SMQH arXiv:2506.00224 is still v1; its repository bsubercaseaux/automatic-symmetries (27 files,
  last push May 2025) holds encoders and helper files, no list of classes; Mackey's thesis CMU-CS-25-108 (read) gives
  one 5-fold realization and no count. The CICM 2025 chapter (LNCS 16136, 29-47) is behind a login and zbMATH shows no
  review text. **Verdict: no correction found in this search.**

### 2f. Today's saturation results of track L (claims filed 02:43-03:20; record [LOWERBOUND_RUN_1118.md](../ROADMAP20261115/LOWERBOUND_RUN_1118.md))

Results checked (as filed): sat_g(6) ≤ 14 (`lb-l18-satg6-14`), sat_g(7) ≤ 21 and ≤ 20 (`lb-l18-satg7-21`,
`lb-l18-satg7-20`), sat_g(8) ≤ 36 (`lb-l18-satg8-36`), order-type saturation without maximality incl. sat_g(8) ≤ 51
(`lb-l18-otsat-nonmax`), and the octagon analogue of the realization dependence (`lb-l18-oct56-real`). Here sat_g(n) is
DDSZ's saturation number (the smallest n-gon-free set in general position to which no point can be added in general
position without creating a convex n-gon).

- **What the literature has.** DDSZ (arXiv:2312.01223 v3 source; SoCG 2024; EJC 131 (2026)): "A planar point set P is
  n-gon-saturated if it is n-gon-free while any q ∉ P with P ∪ {q} being in general position is part of an n-gon in
  P ∪ {q}. Denote by sat_g(n) the smallest size of an n-gon-saturated set" (the claims use this definition); "Theorem. For any integer
  n ≥ 7, we have sat_g(n) ≤ 7/8 · 2^{n−2} ≤ 7/8 · ram_g(n)", i.e. 28 for n = 7 and 56 for n = 8; nothing for n ≤ 6;
  "Our current upper bounds on sat_c(k, ℓ) and sat_g(n) are exponential, while the lower bounds are linear
  (sat_g(n) ≥ n − 1 is trivial). The obvious problem is to obtain better bounds." Damásdi–Keszegh–Malec–Tompkins–Wang–
  Zamora (EJC 2021): "While we were not able to obtain non-trivial bounds for the saturation problem [for convex
  k-sets], for the semisaturation problem we have the following result."
- **Searches** (03:18-03:21 KST): OpenAlex (the three DDSZ versions are one work, W4414265473, cited by 0); Semantic
  Scholar citations of arXiv:2312.01223: 0 (both indexes are known to be incomplete); arXiv API (saturated/saturation
  with "convex position", "Erdos-Szekeres", gon, "saturation number", "point set"): only DDSZ, Damásdi et al. 2021,
  "Saturation Problems in Convex Geometric Hypergraphs" (2109.09931, graphs, a different notion) and "Saturated
  Drawings of Geometric Thickness k" (2503.03577, drawings); web search: DDSZ only. A repository copy of DDSZ
  (real.mtak.hu/224104) is arXiv v2. arXiv author listings of Damásdi, Z. Dong, J. Zeng and Scheucher (newest first):
  no follow-up on saturation after DDSZ. A web search for maximal (non-extendable) hexagon-free sets with fewer than 16
  points found only the 16-point extremal sets.
- **Verdicts.**
  - sat_g(7) ≤ 20 and sat_g(8) ≤ 36: **not found in this search**; the only published upper bounds are DDSZ's 28
    and 56.
  - sat_g(6) ≤ 14 < 16 = ram_g(6): **not found in this search**; DDSZ show sat_g(n) < ram_g(n) only for n ≥ 7.
  - Order-type (every-realization) saturation of non-maximum sets, k = 7 and 8: **not found in this search**.
    Related: DDSZ Theorem 5 (for monotone paths in arbitrary 2-colourings the saturation number equals the Ramsey
    number, "in contrast to the geometric setting") and their final problem for transitive colourings ("Is the
    saturation number equal to C(k+ℓ−4, k−2) again for monotone paths in 3-uniform complete ordered hypergraphs with
    transitive 2-colorings?"), which concerns cups and caps, not k-gons; and the commented-out remark in the DDSZ source
    ("It would be interesting to consider saturation problems for strong or weak n-gons").
  - `lb-l18-oct56-real` (octagon analogue of `lb-ln-ddsz28-real`): as in §2c, the mechanism is known
    (Aichholzer–Krasser), the instance was not found.
- **Value (one line).** The saturation bounds are the clearest "not found" results of the night: concrete improvements
  of a recent SoCG/EJC theorem at n = 7, 8 and its first instance at n = 6, though only small cases of a problem whose
  interest is asymptotic. All four saturation claims were CONFIRMED by independent verifiers by 03:27 (VB: 14 and 20;
  VS: 21 and 36). Before any public statement: a second independent look at the realizability-clause soundness
  (Motzkin certificates), a reading of the DDSZ journal version, and a write-up. Added 03:43: `lb-l18-sat14-realdep`
  (all 56 abstract one-point extensions of the 14-point set are realized by some realization), the k = 6 instance of
  the realization dependence (§2c). Added 03:50: `lb-l18-satg8-31` (sat_g(8) ≤ 31; CONFIRMED by VS 03:49); the verdict for
  31 is the same as for 36: not found in this search. `lb-l18-sat14-realdep` CONFIRMED by VS 03:44.

### 2g. Sources tried and not read

- Balko–Valtr, EJC 66 (2017) 13-23: ScienceDirect only (OpenAlex: bronze OA at ScienceDirect, no repository copy;
  Semantic Scholar has no record); no arXiv version. Balko's thesis "Ramsey-type results for ordered hypergraphs"
  (Charles University, 2017; its abstract includes the refutation of the Peters–Szekeres conjecture, so it probably
  contains the full SAT chapter): dspace.cuni.cz timed out twice (60 s), as on 15 Nov.
- Baek–Balko, JCTA 222 (2026) 106195: still ScienceDirect only; Balko's homepage unchanged since 16 Nov.
- Strunk, DCG 49 (2013): Springer JavaScript challenge; content known from the zbMATH review (§2a).
- Schroeder's proof archive: only its directory and four text members were read (§2a); the Lean modules and the
  certificate data were not opened.
- Gerken's 2006 thesis (mediaTUM): an anti-bot proof-of-work page; not read (it concerns empty hexagons).
- The KNU seminar page found by web search (webbuild.knu.ac.kr/~mhs/seminars/S89): host does not resolve; the Wayback
  Machine CDX service was temporarily offline. The search snippet describes Baek's a = 4 talk.
- Unpaywall (03:42 KST, generic e-mail parameter) lists no other open copy of Baek–Balko JCTA, DDSZ EJC, Balko–Valtr
  EJC 2017 or ETV 1996 than the SoCG, arXiv and publisher locations already used or blocked.
- No CAPTCHA or JavaScript challenge was attempted, and no browser was started.

## Files

Work directory N = `/home/jay/research/data/roadmap-20261115/pm1115/nov1118/` (20 MB; everything fetched read-only on
18 Nov 2026, 02:30-03:20 KST). Downloaded sources are kept as fetched; only TeX files were extracted from arXiv sources.

| file | what | SHA-256 |
|---|---|---|
| `arxiv-new/new_math.CO.html` | arXiv math.CO /new, Tue 17 Nov | `6f555107af79db879d6e4b1d78801bd8ac2b114ec58d4c07c06401970b57dd4c` |
| `arxiv-new/new_cs.CG.html` | arXiv cs.CG /new | `e4a50ff4dbbbedd9052bbbafad55548371d90655a1f05b263497fb1d3f69fb5a` |
| `arxiv-new/new_cs.DM.html` | arXiv cs.DM /new | `1c8e6634a4bc2660d4f7afc90b0657a0577481ecccb7ca519d6aeecb9b6fa7e7` |
| `arxiv-new/new_math.MG.html` | arXiv math.MG /new | `d27cc036234016f4b0cf5ab96499449a7753f7f208cafe9988c475fdbeeaf8f3` |
| `zenodo/versions.json` | Zenodo versions API, record 22842891 (total 1) | `60b7a3e1546fb9518b63b1143f6468b578ed8551b78976e706ccc500fa333e56` |
| `schroeder/companion.html` | Schroeder's companion page (byte-identical to the 16 Nov copy) | `62cfbd5bf63d077987dc43dad637c5239afd039e22da33e5e2a92eeec4909b42` |
| `erdosproblems/p107.html`, `t107.html` | problem 107 and its forum thread | `c549dae6…5e25`, `a08c236f…671b` |
| `papers/etv93/tr-b-93-01.ps.gz` | Erdős–Tuza–Valtr, FU Berlin report B 93-01 (zip archive with PostScript, from the Wayback Machine) | `fd767b072a3a7cf094e42f67246d2a770cd0dc027147b419f99f1c3c3f868aed` |
| `papers/sp06/sp06.pdf` | Szekeres–Peters 2006 (Cambridge Core) | `d8bf83d80433bca1ad09f02576c5eaacb5589f2b279ae3ec34ae54a2942d5240` |
| `papers/schroeder_v1/v1.pdf` | Schroeder v1 (md5 f05d6b63…, as on Zenodo) | `f47c8cc16d4a1d8a5d483b79aa98f97c57919822dcd37dac1b17a757e919f4c5` |
| `papers/ak05/ak05.pdf` | Aichholzer–Krasser, EWCG 2005 extended abstract | `858cb25fcac4d6fb60d10d7560e044c67ffc32968d5dbb93e946976f2ea84730` |
| `papers/javurek/jav.pdf` | Javůrek, Figshare 34875984 v1 | `258641b6f5ab95385b31e598c182bd3931fbefa3f44e3631bbf8895e727ecd29` |
| `papers/mackey/mackey.pdf` | Mackey, CMU-CS-25-108 | `d797a1e7bb6078aa665aed7e03b33b45f2b3eb637023adca547d3142a35772af` |
| `papers/bv_data/` | Balko–Valtr data page files (hashes in claim `nov-bv-weak-strong`); `generator.cpp` | `a56a2dfbd68cb4d182418be82556c4057002339b70aac312b0d7917c7dd4f3e3` |
| `papers/src/<arXiv id>/` | LaTeX sources: 1505.07549, 1510.06255, 1807.10848, 2004.06097, 2105.08406, 2203.07518, 2206.04260, 2403.00737, 2506.00224, 2512.24061, 2604.20120, 2607.02958 | e.g. 1510.06255 `c9d5c3ce…d0fe0`, 2206.04260 `924b89ad…8bfd`, 2004.06097 `15ceead9…e7c` |
| `weakgon_report.json` | all weak/strong gon witnesses (claim `nov-bv-weak-strong`) | `d4bc75d73dd75e7bd0ff8eeb49730a9fa7b2375e8ca04ddf74a1599f80839e81` |
| `tools/weakgon_check.py`, `tools/weakgon_report.py` | own checker and report | `d0666217…5b50`, `05c6b280…fc92` |
| `tools/count_map.py` | row counter for NOVELTY_MAP_1118.md | `e6e10087782850745e82dc97c2516a450e5c79ea2912e1ef34a4d1d42c094ae1` |
| `tools/parse_list.py` | arXiv listing parser (copy of WATCH_1116's) | `5894310ee8ac2a78f19835cda3d906a4ad3b6a3a80573aeb5db32a7a42280db9` |
| `papers/schroeder_zip/entries.json`, `x/` | central directory of Schroeder's archive and four text members (REVIEW.md, BACKGROUND_MACHINERY_2026_09_15.md, RELEASE_NOTES.md, paper/octagons.tex) | `b2ff3870…49bd1`; REVIEW.md `75b9a29d…f0f6` |
| `tools/zip_range_get.py` | reads single members of a remote zip by range requests | `7d2823b8dd35c24b78972840787af69f20cb4f134a21f8b7a2dacc3cbd997c3f` |
| `openalex/c_W2912850616.json` | the 16 works citing ETV 1996 (and `c_*.json` for Balko–Valtr 2017, Baek 2025) | `3e08481a87327361ba83076964e1e9b6fdd9ea01ae0c1331f0b55ea812f12f9b` |

Claims filed: `nov-bv-weak-strong` (CONFIRMED by VS, 02:48), `nov-etv8-corollaries` (CONFIRMED by VB, 03:15) and its
correction `nov-etv8-corollaries-correction` (filed 03:17, CONFIRMED by VS 03:25; item (iv) is empty, see §2a).

## Resume

If this file still says RUNNING, the track was cut off; the verdicts above stand. To repeat the watch:

```bash
N=/home/jay/research/data/roadmap-20261115/pm1115/nov1118
for c in math.CO cs.CG cs.DM math.MG; do
  curl -sS -A "Mozilla/5.0 (literature-watch)" -o $N/arxiv-new/new_${c}_$(date +%m%d).html "https://arxiv.org/list/$c/new?skip=0&show=2000"
  python3 -I $N/tools/parse_list.py $N/arxiv-new/new_${c}_$(date +%m%d).html | grep -v 'hits=\[\]'
done
curl -sS "https://zenodo.org/api/records/22842891/versions?allversions=true&size=25" | python3 -I -c 'import json,sys; print(json.load(sys.stdin)["hits"]["total"])'
cd $N/papers/bv_data && for f in 7Gon4Red_17.txt:7 7Gon5Red6Blue_26:7 8Gon4Red_23:8; do python3 -I $N/tools/weakgon_check.py ${f%%:*} ${f##*:}; done
```
