# LEDGER_1115PM: what the Δ-reduction route can give ES(8), after 15 November (track W1)

**Status (final, 17:13 KST, 15 November 2026).** No ES(8) bound changes. Weak
D(5,7) and weak D(5,8) remain OPEN. The project bound stays **ES(8) ≤ 308** (computer-assisted, unrefereed,
uncommitted; [budget34 README](../../LO33N20261113/budget34/README.md)).

This file does three things:
- it re-derives the arithmetic that turns each Δ-type statement into an ES(8) bound;
- it gives the status of each ingredient;
- it compares the Δ route with the omission route.

The only new computations are two short foreground scripts in `/home/jay/research/data/roadmap-20261115/pm1115/w1/`:
`ledger_calc.py` (exact integers, assert-checked) and `both_caps_lp.py` (an LP guide, HEURISTIC). Labels: PROVED /
CERTIFIED / EXACT TREE / COMPUTED / HEURISTIC; CONJECTURE marks an untested or partly tested statement. Nothing is
rounded up.

**In five lines.**
1. ES(8) ≤ 189 + N5 + N66 ≤ 245 + N5 (PROVED from Lean, CERTIFIED and PROVED inputs, §0). Weak D(5,8), LR(8) or T(8)
   would give N5 ≤ 58 and **ES(8) ≤ 303**. With weak D(5,7) as well: 298. CB(8): 302. CB(7) + CB(8): 296. Each is one
   less once N66 ≤ 55.
2. **Size relevance (§1.1, PROVED, elementary).** For ES(8), weak D(5,8) is needed only for 59-point sets, and there it is
   *equivalent* to N5 ≤ 58. The same holds for every row of the table without a hypothesis, at its own size; the
   hypothesised forms (LRR, TWO-ENV#, ROOT, CONJ-TS′) are needed at every size 17-59. Small-size certificates (today:
   up to 16 points) carry no ES(8) information by themselves.
3. **Windows (§2.2).** A vertex-critical counterexample to weak D(5,8) has 17-59 points: the lower end moved from 16 to
   17 today (claim wd58-m16, CONFIRMED 16:56). For weak D(5,7) the window is 16-32, unchanged today. For CB(8) it is
   16-58 and for CB(7) 14-31 (claim w1-cb-window, CONFIRMED by V3 at 17:10 with a wording fix).
4. **No computational path (§3).** The eager CNF has 2^m pool clauses, and the measured growth was ×17-20 from 15 to 16
   points. The frontier can move 1-2 points, but the size that matters is 59. The route pays only through a written
   proof that holds for every size. Subjective odds for n = 8 within a month: ≤ 0.05 (HEURISTIC).
5. **Omission route (§4).** For 307 it needs (20,15) EXACT TREE (987 of 8,065 contexts at 16:49) and N66 ≤ 55
   (65 of 88 cube leaves CERTIFIED at 16:56), or N66 ≤ 54 alone. It is the only route to 307 with a cost basis.

## 0. Definitions and inputs

**Definitions** are those of [THEORY_1115PM.md](THEORY_1115PM.md) §0:
- (5,n)-valid means no 5-cap and no convex n-gon; a gon is a convex (n−1)-gon.
- A weak Δ is a 4-cap-free subset meeting every gon.
- M(a;n) is the largest point set with no a-cap and no convex n-gon.
- **N5** = M(5;8) = N(cap ≤ 4). **N66** = N(cap ≤ 5, cup ≤ 5): no 6-cap, no 6-cup, no convex octagon.
- **ES(8)** is the least N such that every N points in general position contain a convex octagon.
- "X at m" means: X holds for every (5,n)-valid **point set** with exactly m points.

The Δ-type statements are:
- strong D(5,n): a weak Δ that contains no gon;
- **CB(n)**: a weak Δ with no (n−1)-cup;
- **T(n)**: the gons have a transversal of at most C(n−1,2)+1 points;
- **LR(n)**: a weak Δ through l or through r;
- **LP0(n)**: if r lies in no weak Δ, then the points that end no 4-cap form a weak Δ.

Four statements are *hypothesised*: they assume that r ends a 4-cap and l starts one. They are **LRR(n)** (rooted on one
side), **TWO-ENV#(n)**, **ROOT(n)** and **CONJ-TS′(n)**. All are as in THEORY §1.4 and PROBES_1115PM.md.

**Inputs.**

| # | statement | label | source |
|---|---|---|---|
| I1 | An octagon-free S splits at a hull vertex a into {a} ∪ H ∪ R, so \|S\| ≤ 1 + n_H + n_R, and n_H ≤ 187 | Lean-checked (balanced 187; composition `Partition.forces_of_population_bounds`) | ROADMAP20261115 SYNTHESIS §1, §2.2; THEORY310N20261113 heading |
| I2 | **Lemma A.** R₆, the owners of the 84 F-states (f₁ ≥ 5), have no 5-cap. R ∖ R₆, the owners of the 70 Lo-states (f₁ ≤ 4), have no 6-cup and no 6-cap. Both are octagon-free. Hence \|O ∩ F\| ≤ N5, \|O ∩ Lo\| ≤ N66 and n_R ≤ N5 + N66 | PROVED | THEORY310N20261113 §2 |
| I3 | N66 ≤ 56 | CERTIFIED (level 13; in budget34's inherited trust boundary as "followup56") | N66N20261113 status line of 23:43, 13 Nov |
| I3′ | N66 ≥ 50 (ETV set); N66 ≤ 55 open | — | N66N20261113; cubes20261115/STATUS_campaign.md |
| I4 | M(5;7) ≤ 36 | CERTIFIED, modulo the written arguments of ETV7SAT §2 | ETV7SAT20261113 status item 2 |
| I4′ | M(5;7) ≤ 35 is not established. Rung 36: case B UNSAT by CaDiCaL (COMPUTED; 5.23 GB LRAT kept, cake_lpr ran out of heap at 2,600 MB); case A no verdict. ETV value 26 | — | same |
| I5 | M(5;6) = 15 | point sets: ES(6) = 17 plus the ETV gluing argument; signotopes: CERTIFIED (base(5,6,16)) | DELTA2N20261113 §4.1 notes |
| I6 | Baek: M(4;n) = C(n−1,2)+1 for point sets. So M(4;8) = 22, M(4;7) = 16, M(4;6) = 11 | PROVED (literature, arXiv:2206.04260; for signotopes CERTIFIED only for n ≤ 7, base(4,7,17)) | DELTA2N §3, §4.1 |
| I7 | Erdős–Szekeres cup–cap theorem: no k-cup and no l-cap gives at most C(k+l−4, k−2) points. So 4-cap-free with no 7-cup gives ≤ 21, and with no 6-cup ≤ 15 | PROVED (classical) | THEORY §2.1 |
| I8 | Omission chain: h(F) ≥ 18 (nine Lean rows), h(Lo) ≥ 70 − 56 = 14. The 34-hole cases (18,16), (19,15), (20,14) are EXACT TREE, so h(C) ≥ 35, n_R ≤ 154 − 35 = 119, \|S\| ≤ 307 and ES(8) ≤ 308. Budget 35: (18,17) and (19,16) EXACT TREE; (20,15) and (21,14) open | EXACT TREE + CERTIFIED rows + PROVED bridge | budget34 README headline; STATUS20261115_1000 |

**Master formula (PROVED from I1-I3).** For an octagon-free S, |S| ≤ 1 + 187 + N5 + N66. So

> **ES(8) ≤ 189 + N5 + N66 ≤ 245 + N5**, and ≤ 244 + N5 once N66 ≤ 55.

This is the reading that THEORY §2.3 used without re-deriving it ("arithmetic only, not re-derived"). It agrees with
SYNTHESIS §2.2 ("ES(8) ≤ 189 + c5 + c66"). Re-derived here, all five rows of THEORY §2.3 are correct.

**When an N5 bound matters.** The Lean rows already give |O ∩ F| ≤ 66 without any N5 input, so an N5 bound c matters only
for c ≤ 65. Against the budget-35 cases (`ledger_calc.py`):
- **c = 65 or 64** leaves (20,15) and (21,14): no gain over today. ETV5N's N5 ≤ 65 gives 189 + 65 + 56 = 310 by the master
  formula (its arithmetic LRATs were deleted anyway).
- **c = 63** removes (20,15) and leaves only (21,14). Then 307 follows with N66 ≤ 55 (189 + 63 + 55 = 307) or with a
  (21,14) tree.
- **c ≤ 62** gives ES(8) ≤ 189 + c + 56 ≤ 307 with no budget-35 tree at all.

**LP check (HEURISTIC; HiGHS values are never evidence).** `both_caps_lp.py` adds both capacity rows, h(F) ≥ 84 − c5 and
h(Lo) ≥ 70 − c66, to the 2,650 Lean rows with h₀ = 0. It uses the data and LP of THEORY310N `tools/cap_lp.py`.
- For every pair tested (c5 ∈ {65, 63, 62, 58, 57, 53, 52, 51, 42}, c66 ∈ {56, 55}) the LP optimum equals the trivial
  sum (84 − c5) + (70 − c66). For example, it is exactly 40.0 at (58, 56).
- So at the LP level the Lean rows add nothing to the master formula.
- Only integer trees with coupled rows could add holes. At budget 34 they added 3 holes over the N5-free sum 18 + 14 = 32.
  Such a gain on top of a Δ capacity row (40 holes and more) has not been measured, and trees at those budgets would be
  far larger than the budget-35 ones.

## 1. The ledger

### 1.1 Size relevance (PROVED, elementary; this ledger)

Let B7 = 36 be the proven bound for M(5;7), and b = M(4;8) + B7 = 58.

- **(a)** If weak D(5,8) holds at b + 1 = 59, then N5 ≤ 58.
  - *Proof.* If N5 ≥ 59, there is a (5,8)-valid set with ≥ 59 points, hence one W with exactly 59 points (validity is
    inherited by subsets).
  - A weak Δ of W is 4-cap-free and octagon-free, so |Δ| ≤ 22 (I6). W − Δ has no 5-cap and no convex heptagon, so
    |W − Δ| ≤ 36 (I4).
  - So |W| ≤ 58, a contradiction. ∎
- **(b)** Conversely, N5 ≤ 58 makes "weak D(5,8) at 59" vacuously true. So **at its relevant size the statement is
  equivalent to the extremal bound it yields.**
  - The same two-line argument applies to every row of §1.2 at the size in its "needed at" column.
  - Examples: T(8) or LR(8) at 59; CB(8) at 58 (21 + 36 + 1); weak D(5,7) at 32 (16 + 15 + 1), which is equivalent to
    M(5;7) ≤ 31.
- **(c)** The conjecture itself is more than ES(8) needs.
  - Every counterexample contains a vertex-critical one: delete points while no weak Δ exists. (Counterexamples are also
    upward closed among valid sets, by Lemma M, THEORY §2.2.) By P6 (VERIFICATION.md §0.1) a vertex-critical one has at
    most 59 points.
  - So weak D(5,8) for all sizes is equivalent to weak D(5,8) at every size in the window [17, 59].
  - ES(8) uses only the top size of the window.
- **(d)** The hypothesised forms LRR, TWO-ENV#, ROOT and CONJ-TS′ give weak D at m only together with weak D at m − 1:
  when r ends no 4-cap, a weak Δ of S − r plus r is used (THEORY §2.1; VERIFICATION P2). As ES(8) inputs they are
  therefore needed at **every** size 17..59, by induction from the CERTIFIED range ≤ 16. LR and LP0 without hypothesis
  give weak D at the same size directly, and T(8) at 59 gives N5 ≤ 58 directly (P4).

Consequence: the certified ranges (≤ 15-16 points) are evidence for the conjecture. They are not partial progress
toward an ES(8) bound. The bound appears all at once, when the statement is known at the size in the "needed at" column.

### 1.2 Statement → N5 → ES(8)

All arithmetic is recomputed by `ledger_calc.py` (exact integers, asserts). "Needed at" is the single size at which the
statement yields the N5 bound (§1.1). Hypothesised forms are needed at every size from 17 up to that size.

| statement | needed at | N5 bound (arithmetic, inputs) | ES(8), N66 ≤ 56 | ES(8), N66 ≤ 55 | status of the statement (n = 7, 8) |
|---|---|---|---|---|---|
| weak D(5,8); T(8) (P4); LR(8); LP0(8) | 59 | 22 + 36 = 58 (I6, I4) | **303** | 302 | OPEN. Weak D(5,8) CERTIFIED ≤ 16 (claim wd58-m16 CONFIRMED). LR(8) and LP0(8) are CONJECTURE (LR(8) CERT ≤ 15 per THEORY §1.4) |
| LRR(8), TWO-ENV#(8), ROOT(8), CONJ-TS′(8), TS±(8) (hypothesised) | every size 17-59 | via weak D(5,8): 58 | 303 | 302 | CONJECTURE; CERT ≤ 15 (through CONJ-TS′(8) ≤ 15). ROOT(8), CONJ-TS′(8) and TS±(8) are **not credible**: ROOT(6) and ROOT(7) are false for real sets (15, 17 points), CONJ-TS′(6) and CONJ-TS′(7) likewise (13, 17), TS±(6) at 15 |
| weak D(5,7) + weak D(5,8) (or LR(7) + LR(8)) | 32 and 54 | M(5;7) ≤ 16 + 15 = 31, N5 ≤ 22 + 31 = 53 (I6, I5) | **298** | 297 | weak D(5,7) CERTIFIED ≤ 15, undecided at 16-36 (vacuous above M(5;7) ≤ 36; minimal counterexamples in 16-32). LR(7) at 15: CaDiCaL UNSAT, cake_lpr out of heap, so COMPUTED |
| weak D(5,7) alone | 32 | M(5;7) ≤ 31; no N5 bound by itself | 308 (no change) | 308 | shrinks the weak D(5,8) window to 17-54 and lowers the weak D(5,8) row's size to 54 |
| CB(8) | 58 | 21 + 36 = 57 (I7, I4) | **302** | 301 | CONJECTURE; CERT ≤ 15 (≤ 14 twice, 15 by the DELTA2N record only) |
| CB(7) + CB(8) | 31 and 52 | 15 + 15 = 30, then 21 + 30 = 51 | **296** | 295 | CB(7) CERT ≤ 13 (twice) |
| weak D(5,8) + CB(7) | 31 and 53 | 22 + 30 = 52 | 297 | 296 | as above |
| CB(8) + weak D(5,7) | 32 and 53 | 21 + 31 = 52 | 297 | 296 | as above |
| strong D(5,8) | 53 | M(4;7) + 36 = 16 + 36 = 52 | 297 | 296 | CERT ≤ 15 (proofs deleted; ≤ 14 re-certified by V1). Not credible as a principle: strong D(5,6) fails for a real 15-point set (E4) and strong (6,6) at 16 |
| strong D(5,7) + strong D(5,8) (the Pascal chain) | 27 and 43 | M(5;7) ≤ M(4;6) + 15 = 26, N5 ≤ 16 + 26 = 42 (the ETV values) | 287 | 286 | refuted as a chain at n = 6; prior art GLitchfield PASCAL-SPLIT (SYNTHESIS §2.2) |
| T₂₆(8): the gons have a transversal of ≤ 26 points; or weak D(5,8) with ≤ 4 extra points (a 4-cap-free Δ plus ≤ 4 points meet every gon) | 63 | 26 + 36 = 22 + 4 + 36 = 62 | **307** | 306 | CONJECTURE, implied by weak D(5,8). A weaker Δ-type target that alone gives 307 (compare the "deletion form" row of SYNTHESIS §2.2, N5 ≤ 22 + M(5;7) + e) |
| T₂₇(8), or 5 extra points | 64 | 63 | 308; removes (20,15), leaving (21,14) | 307 | as above |
| the ETV value N5 = 42 (floor of the whole N5 lever) | — | 42 | 287 | 286 | with N66 at its lower bound 50: 281. The balanced 187 and N66 are outside the Δ program |
| *(Lo side, for comparison)* PS(6,6) + Schroeder's M₇(5,6) = 25, which gives N66 ≤ 50 | — | — | 304 with N5 ≤ 65 (LRATs deleted); 305 N5-free (h(F) ≥ 18 plus h(Lo) ≥ 20 = 38 holes) | — | open, "no real support" (FLAYER20261113 §8); PS(5,5) is false for real sets |

Superseded ledger lines elsewhere (older inputs; SYNTHESIS §2.2 already lists them):
- ETVTHY §3.1 and §9: N5 ≤ 63 and 54, and "54 would give ES(8) ≤ 308". With N66 ≤ 56, 54 would give 299.
- DELTA2N README l.83-84.
- ETV5N l.18/25: "N5 ≤ 57 would give ES(8) ≤ 309". By the master formula N5 ≤ 57 gives 302.

## 2. State of each ingredient (data as of 16:49-17:10 KST, 15 November)

### 2.1 Ingredients

| ingredient | certified / known | open | today's change | source |
|---|---|---|---|---|
| weak D(5,8) | CERTIFIED for every set with ≤ 16 points. At ≤ 15 there are two routes: DELTA2N (single cake_lpr run, proofs deleted) and CONJ-TS′(8) ≤ 15 + Theorem 3 (replayed). At 16: T3's run plus the main session's fresh cake_lpr re-run, hashes equal | 17-59 (window) | 16 added (claim wd58-m16, CONFIRMED by V2 at 16:56) | PROBES §4; MAINSESSION; VERIFY_WD58_M16.md |
| weak D(5,7) | CERTIFIED ≤ 15 (DELTA2N single run, proof deleted); ≤ 14 also via CONJ-TS′(7) + Theorem 3 (replayed) | 16-32 | none. LR(7) at 15 is COMPUTED: CaDiCaL UNSAT in 7,857 s, LRAT 23.7 GB kept as 5.3 GB zstd, cake_lpr "heap exhausted" at 1,150 MB (`t1/lrr7/cert15/`). TWO-ENV#(7) at 15 is running (T3: two encodings) | THEORY §1.4; PROBES status table |
| M(5;7) ≤ 36 | CERTIFIED | 26-36 | none | ETV7SAT |
| N66 ≤ 56 | CERTIFIED | N66 ≤ 55: cube campaign, **65 of 88 leaves CERTIFIED at 16:56** (33 of 70 at 09:29), 18 queued and 5 running, driver deadline 18:44 | +32 leaves | N66N20261113/cubes20261115/STATUS_campaign.md |
| CB(8) | CERTIFIED ≤ 14 twice (DELTA2N + V1's kept proofs); 15 by the DELTA2N record only (proof deleted) | 16-58 (window) | first stated today (claim cb78-from-strong, CONFIRMED) | VERIFY_CB78_FROM_STRONG.md |
| CB(7) | CERTIFIED ≤ 13 twice | 14-31 | same | same |
| CB(6) | CERTIFIED ≤ 13 | 14, 15 | new (claim cb6-le13, CONFIRMED) | THEORY §5 |
| LR(6), TWO-ENV#(6) | TRUE for every signotope (two certificates each at 15; m ≥ 16 vacuous) | — | new | claims lrr6-certified, lr6-m15-second, twoenv6-m15, twoenv6-13-14 |
| LR(8), TWO-ENV#(8), LP0(8) | LR(8) and TWO-ENV#(8): CERT ≤ 15 through CONJ-TS′(8) ≤ 15 (THEORY §1.4). LP0(8) holds vacuously wherever r is always rootable, which is the case at ≤ 15 (ROOT(8) CERT ≤ 15; r ending no 4-cap is rootable by weak D at m − 1); this step is W1's reading | from 16 up to the largest (5,8)-valid size (≤ 65 by ETV5N, whose arithmetic LRATs were deleted; ≤ 84 by cup–cap) | none | THEORY §1.4 |
| strong D(5,8) | CERT ≤ 15 (≤ 14 re-certified by V1) | from 16 up to the largest valid size; the n = 6 analogue is false | none | DELTA2N §4.1 |
| one-sided forms | false for real sets: ROOT(6) (15), ROOT(7) (17), CONJ-TS′(6) (13), CONJ-TS′(7) (17), ENV#(6) (\|U\| = 14), ENV#(7) (\|U\| = 16), TS±(6) (15), AT_n (n = 6, 7, 8) | ROOT(8) CERT ≤ 15; HEURISTIC guess of a first failure near 19 points (THEORY §3, finding 6) | all new today except AT_n | THEORY §1.4, §5; claims |

Note on n = 6: every n = 6 statement concerns M(5;6) = 15, which is already known. LR(6) and TWO-ENV#(6) therefore have
no ES(8) consequence. They are evidence that the two-sided forms are the right inductive targets for n = 7 and 8.

### 2.2 The counterexample windows (point sets)

A counterexample S to a hereditary statement X is **vertex-critical** if X fails for S but holds for every S − p. If
X(S − p) gives |S − p| ≤ β, then |S| ≤ β + 1.

| statement | window before today | window now | upper end from | what would shrink it next (HEURISTIC cost) |
|---|---|---|---|---|
| weak D(5,8) | 16-59 | **17-59** | 22 + 36 + 1 (P6; for point sets, because Baek's theorem is for point sets) | m = 17: about 20-28 CPU-h and an LRAT of about 95-110 GB (×17-20 growth from 16; PROBES §4 says about 20 CPU-h). m = 18: roughly 350-550 CPU-h and 1.6-2.2 TB of LRAT, beyond the 852 GB of free disk reported this morning. M(5;7) ≤ 35 would bring the top to 58, weak D(5,7) to 54 |
| weak D(5,7) | 16-32 | 16-32 | 16 + 15 + 1 (P6; also for signotopes) | LR(7), TWO-ENV#(7) or weak D(5,7) at 16. The direct eager run is estimated at about 11 h (VERIFICATION §7); a 600 s trial was UNKNOWN (DELTA3N) |
| CB(8) | — | **16-58** | 21 + 36 + 1 | CB(8) at 16 (THEORY §4 next step 3) |
| CB(7) | — | **14-31** | 15 + 15 + 1 | CB(7) at 14 |

How today's results act on the windows:
- Only wd58-m16 moved a window, by one size: 1 of the 44 sizes in 16-59.
- The n = 7 results concern sizes ≤ 15, where weak D(5,7) was already CERTIFIED. If certified, LR(7) at 15 or
  TWO-ENV#(7) at 15 would give a second, replayable route to the existing top size; they would not extend it.
- The refutations do not move any window. They remove candidate proof mechanisms: Theorem 3's premise CONJ-TS′, ROOT, and
  the uniform one-sided ENV#/VE/(U). The surviving inductive mechanisms for n = 7 and 8 are LR, TWO-ENV# and LP0, all
  CONJECTURE there.
- The top of each window is fixed by extremal bounds, not by the Δ certificates. Only an improvement of M(5;7), or
  weak D(5,7) itself, lowers the weak D(5,8) top.

Wording fixes for the records:
- THEORY §1.1 says "17-59 once wd58-m16 is confirmed". wd58-m16 is now CONFIRMED, so the window is 17-59. The upper
  end 59 holds for point sets (P6 states that qualifier; THEORY §1.1 drops it).
- Claim cb78-from-strong and VERIFY_CB78_FROM_STRONG.md say "CB(8) at 16-22 and CB(7) at 14-15 remain open". That
  understates the open ranges. CB(8) is undecided from 16 up to the largest possible (5,8)-valid size, and CB(7) at
  14-36; above those sizes they are vacuously true. By the window lemma both reduce to minimal counterexamples in
  16-58 and 14-31. Correction claim `w1-cb-window` (§5) is CONFIRMED by V3 with this wording. V3 refuted the claim's
  own sentence "open at every size ≥ 16 (≥ 14)", because it ignored the vacuous sizes.

## 3. The cheapest credible path to an actual ES(8) improvement through Δ

### 3.1 Why there is no computational path

- **Equivalence (§1.1).** At its relevant size each row is equivalent to the N5 bound it yields. A computer proof of
  "weak D(5,8) at 59" would be a computer proof of N5 ≤ 58, and harder: the Δ quantifier sits on top of the
  configuration search.
- **Encoding size.** DELTA2N's eager CNF has one pool clause for each of the 2^m candidate sets Δ, so at m = 59 it has
  2^59 ≈ 5.8·10^17 pool clauses. The DELTA3N streaming encoder shares witnesses on the subset lattice, but it is still
  exponential in m.
- **Measured growth** for weak (5,8) (DELTA2N §3; PROBES §4):

  | m | CaDiCaL | LRAT |
  |---|---|---|
  | 13 | 0.1 s | — |
  | 14 | 6 s | — |
  | 15 | 242 s | 0.56 GB |
  | 16 | 4,973 s | 5.6 GB |

  That is ×20 from 15 to 16 points by wall time (×17 by process time), and ×10-40 per point at 13-15 (DELTA2N §3). With
  cube-and-conquer and trimming the frontier moves 1-2 points (HEURISTIC), against 43 open sizes.
- **The direct N5 route** stalled at N5 ≤ 65 after 439 cores (ETV5N). SYNTHESIS §2.1 item 7 found no credible cost basis
  for N5 ≤ 63/62.

### 3.2 The cheapest credible sequence

Steps 1 and 2 change evidence, not bounds. Every cost is HEURISTIC.

1. **Make the existing frontier replayable** (about 1-3 CPU-h; cake_lpr needs a 4-6 GB heap, so it runs only when the
   memory budget allows).
   - Re-run cake_lpr on the kept LR(7) m = 15 proof (`t1/lrr7/cert15/lrr7_m15.lrat.zst`, 5.3 GB zstd).
   - Certify TWO-ENV#(7) at 15 (running, T3).
   - Re-certify DELTA2N's weak (5,7) and (5,8) at m = 15 with kept proofs (SYNTHESIS §2.2 item 3).
   - Value: the only computational support of the conjecture would no longer rest on deleted proofs. No window moves.
2. **Try to kill the route cheaply** (1-3 CPU-h per SAT-mode probe, plus a few CPU-h for realization or gluing).
   - Run SAT-mode searches for counterexamples to LR(7), TWO-ENV#(7) and weak D(5,7) at 16-18 points, with
     BFP/realize_sig realization of any model, as was done for ROOT(7).
   - Run gluing tests (Lemma M): known 17-point right-hostile blocks against left-hostile blocks with larger overlaps.
   - Today's data: ROOT(7) gave a model at 17 points in 1,599 s. LR(7) at 17 gave none in 2,496 s. Gluing with 1-2 extra
     points was UNSAT (COMPUTED).
   - A real LR(7) counterexample would remove the only inductive mechanism left. A weak D(5,7) counterexample would
     remove the 298 row.
3. **Prove the statement for every size** (the only step that can pay).
   - Target: a written proof of TWO-ENV#(n) or LR(n), or of weak D(5,n) directly, for n = 7 and 8 or for all n.
   - TWO-ENV# is the r-independent form: each side is a property of U = S − r (or V = S − l) alone, and it is true at
     n = 6 (THEORY §4).
   - Cost: research-level and unknown. The records name no mechanism ("No proof mechanism is known for TWO-ENV#, LR, LP0
     or CB beyond SAT", THEORY §4). DELTA2N §7 and T4's cores (THEORY §3, finding 5) show that the obstructions are
     global.
   - What a proof may use and must cover, from the records:
     - It may stay inside signotopes. No abstract counterexample to weak D is known: weak D(5,8) is CERTIFIED for all
       signotopes with ≤ 16 points, and 17 random abstract (5,8) samples with 24-36 points even have a cup-side Δ
       (DELTA2N §4.2b; HEURISTIC as evidence). The N5 consequence then still needs Baek's point-set theorem (I6).
     - An r-independent *one-sided* invariant would also have to prove weak D(4,8) (VERIFICATION P1, Lemma U4), which is
       open at 17-22 points. The two-sided TWO-ENV# is not known to contain weak D(4,8).
   - Subjective odds of a proof of the n = 8 case within a month: ≤ 0.05 (HEURISTIC).
   - Payoff: 308 → 303, or → 298 with n = 7 as well; one less with N66 ≤ 55.
   - A weaker target that still pays is T₂₆(8), or weak D(5,8) with ≤ 4 extra points, which gives 307. It needs a
     proof just as much. Its only advantage is slack: 26 transversal points against 22.

Cost summary (HEURISTIC; the bases are the measured runs quoted above):

| step | CPU | memory / disk | changes a bound? | probability / payoff |
|---|---|---|---|---|
| 1. cake_lpr re-run of LR(7) m = 15 | ≈ 0.2-0.5 CPU-h (LR(6) m = 15 re-runs took 2-5 min on 3.5 GB proofs; this proof is 23.7 GB) | heap 4-6 GB, in a unit with MemoryMax above the heap | no | high; the n = 7 frontier becomes replayable |
| 1. re-certify weak (5,7) and (5,8) at m = 15 | ≈ 1 CPU-h (DELTA2N: 1,737 s and 242 s of CaDiCaL plus cake_lpr) | 6 GB of LRAT for (5,7); keep as zstd | no | high |
| 2. SAT-mode falsification probes, LR(7)/TWO-ENV#(7)/weak D(5,7) at 16-18 | 1-3 CPU-h per probe (ROOT(7) at 17 gave a model in 1,599 s; LR(7) at 17 none in 2,496 s) | under 1 GB each | can remove rows (303, 298) | unknown; a model must then be realized (BFP) |
| 2. certified UNSAT of LR(7) or TWO-ENV#(7) at 16 | roughly 20-40 CPU-h (×10-20 over the 7,857 s at 15) | LRAT of roughly 0.2-0.5 TB | no (window 16-32 → 17-32) | evidence only |
| 3. written proof for n = 8 (or all n) | research-level, unknown | — | yes: 303 (298 with n = 7) | ≤ 0.05 within a month (subjective) |

Not credible as targets:
- ROOT(8), CONJ-TS′(8) and TS±(8): their n = 6 and 7 analogues are false for real sets.
- Strong D(5,8) and the Pascal chain: false at n = 6.
- Cup-side D(5,8): false at n = 6 (cup15).
- Rank and other explicit rules (DELTA2N §7; THEORY §1.3).

Rough expected value (HEURISTIC): the Δ route gives about 5 bound-points × ≤ 0.05 per month of research. The omission
route gives 1 bound-point (307) × about 0.2-0.35 within days, for about 130-510 CPU-h (§4: 110-450 for (20,15) plus
20-60 for the N66 cubes).

## 4. Comparison with the omission route

| route | what ES(8) ≤ 307 needs | status, 15 Nov afternoon | cost (HEURISTIC) | beyond 307 |
|---|---|---|---|---|
| omission, budget 35 | (20,15) EXACT TREE **and** (21,14) removed; **or** N66 ≤ 54 alone (then h(Lo) ≥ 16 leaves only (18,17) and (19,16), both EXACT TREE; SYNTHESIS §2.1 item 2, level 15, P ≈ 0.1 within 3 days) | (20,15): loop `esr-lo-b35s20v10b` running, **987 of 8,065 contexts closed at 16:49** (555 at 09:35); all 64 afternoon rows CERTIFIED by independent audit (ADDENDUM_1115PM.md). (21,14): N66 ≤ 55 cubes **65 of 88 leaves CERTIFIED at 16:56**, 23 open | (20,15): about 200 CPU-h (110-450), P(EXACT TREE within 48 h) ≈ 0.35. N66 cubes: 20-60 CPU-h, P ≈ 0.3 (SYNTHESIS §2.1, written before today's progress). (21,14) tree as fallback: 700-6,000 CPU-h | 306 needs h(C) ≥ 37: trees for the budget-36 cases (18,18) … (22,14), or better N66/N5 bounds; SYNTHESIS gives < 0.1 within two weeks |
| N5 directly | N5 ≤ 62 (no budget-35 tree), or N5 ≤ 63 together with N66 ≤ 55 | N5 ≤ 65 (ETV5N; arithmetic LRATs deleted) | no credible cost basis (SYNTHESIS §2.1 item 7) | 189 + N5 + N66 |
| Δ | weak D(5,8), LR(8) or T(8) (⟹ 303), or T₂₆(8) (⟹ 307), proved for every size up to 59 (63) | OPEN; CERTIFIED ≤ 16; no counterexample known | proof only (§3) | 298 with n = 7; floor 287 (ETV N5) |

Conclusions:
1. **For 307 the omission route is the only route with a cost basis.** The Δ route adds nothing to 307 unless a uniform
   statement is proved. Below 307 it would be worth 5 points (weak D(5,8)) or 10 points (with weak D(5,7)) if proved.
   Balanced-side statements such as THEORY310N's (W2) are separate levers.
2. **N66 ≤ 55 helps both routes.** It removes (21,14) and lowers every Δ row by one (third table column). It is the
   shared critical item.
3. **The routes do not add up.** Once any N5 ≤ 62 holds, the budget-35 trees become unnecessary. At the LP level the
   Lean rows add nothing to the two capacity rows (§0, HEURISTIC). Integer trees on top of a Δ capacity row are
   unmeasured.
4. **The ceiling of the N5 lever.** Even the ETV value N5 = 42 leaves ES(8) ≤ 287 with N66 ≤ 56. Further progress would
   have to come from the balanced bound n_H ≤ 187 (Lemma B route, n_H ≤ 2·N(cap ≤ 5, cup ≤ 6), THEORY310N) and from N66.
   These are outside the D(5,n) program.

## 5. Correction claim filed

`w1-cb-window`, filed at 17:07 KST. The claim's "time" field reads 17:50 by mistake. A verifier had locked the claim
before this could be fixed, so it was left unchanged.

It contains:
- **(a)** CB(n) is hereditary (the analogue of Lemma M).
- **(b)** A vertex-critical CB(n) counterexample has at most C(n−1,2) + M(5;n−1) + 1 points: 58 for n = 8, 31 for n = 7.
- **(c)** The open-range wording fix of §2.2.
- **(d)** CB(8) at 58 is equivalent to N5 ≤ 57, which gives ES(8) ≤ 302 by the master formula.

**Verdict: CONFIRMED by V3 at 17:10**, with one refuted part. Files:
`/home/jay/research/data/roadmap-20261115/pm1115/claims/w1-cb-window.verdict.json` and
[VERIFY_W1_CB_WINDOW.md](VERIFY_W1_CB_WINDOW.md); V3's code is `pm1115/v3/w1-cb-window/v3_w1_arith.py`.
- V3 re-derived (a), (b) and (d), the windows 16-58 and 14-31, and the arithmetic.
- V3 confirmed both quotations in (c) and that they understate the open ranges.
- **Refuted:** the claim's first sentence of (c), "CB(8) is open at every size ≥ 16 and CB(7) at every size ≥ 14".
  CB(7) is vacuously true at ≥ 37 because M(5;7) ≤ 36, and CB(8) above the best N5 bound.
- This ledger uses V3's wording (§2.2): undecided from 16 up to the largest valid size, and at 14-36.

No error was found in the arithmetic of THEORY §2.3, SYNTHESIS §2.2, VERIFICATION P4/P6 or DELTA2N §4.

## 6. Files

- This file: `archive/es7-2026-10-19/results/DELTA3N20261113/attack20261115/LEDGER_1115PM.md` (the only repository file
  written by W1).
- `/home/jay/research/data/roadmap-20261115/pm1115/w1/ledger_calc.py`: exact arithmetic of §0-§2 (asserts; under 1 s).
  Run with `python3 -I ledger_calc.py`.
- `/home/jay/research/data/roadmap-20261115/pm1115/w1/both_caps_lp.py`: the HEURISTIC LP guide of §0. It needs the venv
  (highspy) and takes about 10 s single-threaded.
- `/home/jay/research/data/roadmap-20261115/pm1115/w1/w1-cb-window.json`: the filed claim.
