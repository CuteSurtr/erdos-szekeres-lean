# Δ-reduction program: theory map and assessment (T4, 15 November 2026 afternoon; final v7 18:05 KST)

**Status.** Weak D(5,7) and weak D(5,8) remain OPEN; no ES bound changes. This file maps every statement of the
program, the implications among them, what the known counterexamples have in common, and how viable the route is after
today's results. It contains no proof of the conjecture. New exact computations are T4's own code
(`/home/jay/research/data/roadmap-20261115/pm1115/t4/`); the claims T4 filed are in §5 with their verifier status.
Labels are the house labels (PROVED / CERTIFIED / EXACT / COMPUTED / HEURISTIC); CONJECTURE marks an untested or
partly tested statement. Nothing is rounded up.

**The afternoon in one paragraph.** The one-sided rooted form behind Theorem 3 is dead for point sets at n = 6 and
n = 7: ROOT(6) is false for real 15-point sets (T1: 21 sets, claim root6-real-15, CONFIRMED [superseded 15 Nov pm: by
18:22 T1 had 177 distinct real 15-point ROOT(6) counterexamples (EXACT, T1's own checks, not filed; ROOT6_M15_REALIZE.md
items 18-19); the "21 real ROOT(6) sets" statistics of §3 describe the first 21 only (C1 issue 15b)]) at the extremal size,
with 16 points vacuous (claim root6-m16-vacuous, T4, CONFIRMED), so ROOT(6) is decided (true up to 14 points, false at
15); ROOT(7) is false for real 17-point sets (claims root7-real-17 by R7 and root7-real-17-t1 by T1, CONFIRMED). CONJ-TS′,
ENV#, VE and (U) fail with them (claims env6-real-14-15 and env7-real-16-17 by T4, CONFIRMED). The r-independent
two-sided form TS± also fails at n = 6 with 15 points, abstractly and for a real set (claims tspm6-m15-abstract and
tspm6-real-15, CONFIRMED). **What survives everywhere is the rooted two-sided form:** on all 27 rooted failures (22 at
n = 6, 5 at n = 7), on all 44 CEGAR models of rooted failures, and on every other counterexample set of the program, S
has a weak Δ through its leftmost point (LR), exactly one point (r) is unrootable, the explicit set P0 of points that
end no 4-cap is a weak Δ (LP0), and the mirror image of S − l has ENV# Δs (TWO-ENV#). [superseded 15 Nov pm (C1 issue
1): LP0 does not survive everywhere: it is false on P2's abstract 19-point W (claim lp0-7-false-abstract, V2 CONFIRMED;
§1.4 and finding 2). "Exactly one point (r) is unrootable" was checked on the 27 rooted failures only; the §3 table
shows 0 unrootable points on every other set. "P0 is a weak Δ" also fails on cup15 (finding 2). What holds on every set
T4 checked (the 27 rooted failures, the 44 CEGAR models, the other sets of the §3 table, and W) is LR and TWO-ENV#.]
**LR(6) holds for every signotope** [corrected 15 Nov pm (C1 issue 7): was "LR(6) is a theorem"; it is CERTIFIED plus a
PROVED combination, computer-assisted and unrefereed]: LR(6)
at 15 points is CERTIFIED on two separately written CNFs [corrected 15 Nov pm (C1 issue 7): was "two independent CNFs";
V2's verdict on lr6-m15-second: independent in code and in the left-side construction, but the base-clause block uses
the same clause patterns] (claims lrr6-certified and lr6-m15-second on T4's CNF, both CONFIRMED;
the main session re-ran cake_lpr on both proofs: exact line, hashes equal), with ROOT(6) below 15 and nothing above. All rooted failures share one mechanism: r caps
(almost) every pair it is allowed to cap, over a U whose 4-caps end in only 8-10 pairs and in 4-7 points (§3,
findings 2-3). The best surviving reductions are LR(n) and TWO-ENV#(n), both PROVED to imply weak D(5,n); the explanatory form
LP0(n) ("r lies in a weak Δ, or the points that end no 4-cap meet every gon") held on every searched failure but is
false at n = 7 for an abstract 19-point extension of a real hostile block (claim lp0-7-false-abstract); **TWO-ENV#(6), in its hypothesised form (r ends and l starts a 4-cap), also holds for every signotope** [corrected 15 Nov pm (C1 issues 3
and 7): was "TWO-ENV#(6) is also a theorem"; CERTIFIED plus a PROVED combination, computer-assisted and unrefereed, and
the certificates cover only the hypothesised form; weak D needs only that form] (T3
certified it at 15 points, claim twoenv6-m15, CONFIRMED): at n = 6 the r-independent two-sided uniform selection
holds although its terminal-safe version TS± fails. LP0(6) at 15 points is open (T4's SAT-mode probe found no
counterexample). Weak D(5,7) and weak D(5,8) themselves remain OPEN; T3 certified weak D(5,8) at 16 points (claim
wd58-m16; cake re-run by the main session), so it now holds for all sets with at most 16 points (open from 17). LR(7)
at 15 points is UNSAT by CaDiCaL (T1; COMPUTED, since cake_lpr ran out of heap at 1,150 MB on the 23.7 GB proof).

## 0. Definitions used throughout

- S is a signotope on labels 0..m−1 in increasing x; σ(i,j,k) for i<j<k is + (cup, orientation > 0) or − (cap); a point
  set gives σ by its orientation signs. k-cap / k-cup: every triple a cap / a cup. Convex set: every 4-subset x<y<z<w
  has σ(xyz) = σ(xyw) and σ(xzw) = σ(yzw) (for points this is convex position).
- (5,n)-valid: no 5-cap and no convex n-set. Gon: convex (n−1)-set. **Weak Δ**: 4-cap-free subset meeting every gon.
  **weak D(5,n)**: every (5,n)-valid S has a weak Δ. M(a;n): the largest (a,n)-valid point set (N5 = M(5;8)).
- r = m−1 (rightmost), l = 0 (leftmost), U = S − r, V = S − l; P4(U): pairs (c,d) that end a 4-cap (a,b,c,d) of U;
  ⊑ and ↑P4 as in ROUND6.md "Definitions"; C_r: pairs (b,c) of U with (b,c,r) a cap. The maximal 5-cap-free right
  extension r0 caps exactly the pairs outside ↑P4(U) (ROUND6 track 1, statements 2 and 4).
- **Rooted at p:** S has a weak Δ containing p (for p = r this is ROOT: A = Δ − r is a weak Δ of U with A + r
  4-cap-free; conversely). **Terminal-safe in U:** weak Δ A of U whose every 3-cap (a,b,c) has (b,c) ∈ P4(U).
  **Initial-safe in V:** mirror notion ((a,b) starts a 4-cap of V).
- P0 = points of S that end no 4-cap (l ∈ P0), Q0 = points that start no 4-cap (r ∈ Q0); both are 4-cap-free.
- End layers (mirror of DELTA2N Lemma 2): R⁰ = S, R^{i+1} = points of R^i that end a 4-cap inside R^i; depth(r) = i
  with r ∈ R^i − R^{i+1}. Start layers and depth(l) likewise (P0 = R⁰ − R¹, Q0 = first start layer).
- Mirror μ: i ↦ m−1−i; (i,j,k) ↦ (m−1−k, m−1−j, m−1−i) with the same sign (x ↦ −x keeps caps caps; self-tested against
  coordinates in `t4lib.py`).

## 1. (a) Map of the statements

"Fails at m (real)" = an exact real counterexample with m points is on record; "(abs)" = abstract signotope only;
"CERT ≤ m" = CERTIFIED for all signotopes up to m points. For n = 6 every size ≥ 16 is vacuous: no (5,6)-valid
signotope has 16 points (DELTA2N, base(5,6,16) CERTIFIED). Sources in the last column (R = this folder).

### 1.1 Targets and size statements

| statement | n = 6 | n = 7 | n = 8 | source |
|---|---|---|---|---|
| weak D(5,n) | **true, all sizes** (CERT ≤ 15 + base 16) | CERT ≤ 15 (DELTA2N, proof not kept); ≤ 14 also via CONJ-TS′(7) + Theorem 3 (certificates replayed by a second party); open ≥ 16 | CERT ≤ 15 (DELTA2N, proof not kept); also via CONJ-TS′(8) ≤ 15 + Theorem 3 (replayed); **16 CERTIFIED by T3 (claim wd58-m16, DELTA2N's encoder, LRAT 5.6 GB; CONFIRMED by V2 after the main session's cake_lpr re-run, `round6/mainsession/wd58recake/`)**; open ≥ 17 | DELTA2N §4.1; R/ROUND2; R/CONJTS_TEST; claim wd58-m16 |
| vertex-critical counterexample window | — | 16-32 points | 16-59 (16-54 if weak D(5,7)); 17-59 once wd58-m16 is confirmed [superseded 15 Nov pm (C1 issue 4): wd58-m16 is CONFIRMED (V2, verdict file 16:53:54), so the window is 17-59] | R/VERIFICATION P6 (PROVED from CERTIFIED inputs) |
| T(n): gons have a transversal of ≤ C(n−1,2)+1 points | — | open | open; contains M(5;8) ≤ 58 | R/VERIFICATION P4 |
| weak D(4,n) (cup meeting every gon, 4-cap-free input) | complete | complete (strong form) | CERT ≤ 16; open 17-22 | DELTA2N §4.1; R/ROUND6 §3; R/VERIFY_ATN_MAIN |
| M(5;n) | 15 (signotopes CERT; points: ES(6) + ETV) | ≤ 36 (CERT, ETV7SAT); ETV value 26 (26-point signotopes exist, NOVELTY20261113B l.184) | ETV value 42; the N5 ≤ 65 ladder stalled and its LRATs were deleted | DELTA2N; NOVELTY20261113B; ROADMAP §6 |

### 1.2 Sharpenings of the partition (which Δ, which part of each gon)

| statement | status | source |
|---|---|---|
| strong D(5,n): Δ also gon-free | (5,6) CERT ≤ 11, **fails at 15 (real, E4)** = extremal size; (5,7) CERT ≤ 13; (5,8) CERT ≤ 15; (6,6) fails at 16 (real) | DELTA2N §4.1; NOVELTY20261113B E4 |
| cup-side (lower-chain) D(5,n) | (5,6) CERT ≤ 13, **fails at 15 (real, cup15)** = extremal size; (5,7) CERT ≤ 13; (5,8) CERT ≤ 14; exact on 1,059 real sets | DELTA3N README; DELTA2N §4.2b |
| cap-side D(5,n) | fails: (5,6) 11 (real), (5,7) 12 (abs), (5,8) 13 (real) | DELTA2N §7 |
| **CB(n)**: weak Δ with no (n−1)-cup (between weak and strong) | CONJECTURE. **CB(6) CERTIFIED for \|S\| ≤ 13** (T4, claim cb6-le13, CONFIRMED); **CB(7) for \|S\| ≤ 13 and CB(8) for \|S\| ≤ 15 by citation**: the strong form implies CB and DELTA2N certified strong (5,7) ≤ 13 and strong (5,8) ≤ 15 (claim cb78-from-strong by T3, CONFIRMED [corrected 15 Nov pm (C1 issue 13): CB(8) at \|S\| = 15 rests on DELTA2N's record only; that proof was deleted and never re-run (V1's verdict on cb78-from-strong). CB(7) ≤ 13 and CB(8) ≤ 14 are CERTIFIED twice: DELTA2N, and V1's own encoder]); EXACT on every set of §3 (incl. strong15, cup15, the 22 ROOT(6) failures, root7_m17) and on the ETV extremal sets for n = 6, 7, 8 | §5 (T4) |
| CB2(n): weak Δ with no (n−2)-cup | fails: every 15-point (5,6)-valid set by counting (6 + 8 < 15); ETV42 at n = 8 (COMPUTED) | §5 (T4) |
| 5-cup-free transversal of the heptagons | fails on ETV42 (COMPUTED) | §5 (T4) |
| min transversal ≤ min weak Δ − 1 ("price ≤ 1") | fails at 18 (real, n = 7) | R/VERIFICATION §8 |
| a minimum lower-chain hitting set can be 4-cap-free | fails at 16 (real, n = 7) | DELTA3N README |

### 1.3 Localisations and explicit rules

| statement | status | source |
|---|---|---|
| Δ contains an end of every gon | fails (5,6) at 9 (real) | DELTA2N §7 |
| Δ ⊆ E_L ∪ E_R | fails (5,6) 12, (5,7) 12, (5,8) 13 (all real) | DELTA2N §7 |
| Δ ⊆ Δ_R ∪ Δ_L (rank, R(5,n)) | CERT (5,6) ≤ 13, (5,7) ≤ 12, (5,8) ≤ 13; open | DELTA2N §7 |
| R(4,7) | fails at 13 (real σ13) although D(4,7) is true | R/VERIFICATION §6; R/VERIFY_ATN_MAIN |
| Δ ⊆ ends ∪ interior cap vertices | CERT (5,6) ≤ 12, (5,8) 7-10 and 13 | DELTA2N §7 |
| TRIV(n): P0 or Q0 is a weak Δ (would give LR at once) | fails (abs) at n = 6 with 10 points (7-9 UNSAT, COMPUTED); fails for real sets at n = 7 (15 points) and n = 8 (18 points) (attack 4's min_LR sets); yet **P0 or Q0 works on every counterexample set of the program** (§3) [superseded 15 Nov pm (H1): not on P2's abstract 19-point W (claim lp0-7-false-abstract, V2 CONFIRMED): there P0 misses 47 hexagons, and Q0 contains r, which lies in no weak Δ of W, so Q0 is not a weak Δ either (Q0 misses 48 of the 714 hexagons; claim h1-pq0-w19, filed 19:09, EXACT + PROVED, VB CONFIRMED, verdict file 19:12:15, VERIFY_H1_PQ0_W19.md)] | §5 (T4); R/VERIFICATION §4 |
| threshold rule, must-contain rules, Q ∪ Q′ | fail at 8-11 (real) | DELTA2N §7 |
| on-line (left-to-right) rule | none for a = 4 (7 points n = 5, 8 points n = 6); (5,6) colourer survives 8 | DELTA2N §4.4 |
| coarse layer unions; pointwise 6-tuple rules | fail (real, n = 7, 8; CERT) | R/VERIFICATION §4 |
| "delete one point, extend any Δ′" | fails (5,6) at 10 (real) | DELTA2N §7 |
| repair with ≤ 1 newly selected old point | PROVED for \|S\| ≤ n+2; fails n = 7 at 14, n = 8 at 16 (real, CERT) | DELTA3N selection |
| peel the right 4-cap layer, then D(4,n) | fails (CERT fixed sets) | R/ROUND2 Task 3 |

### 1.4 Rooted and selection forms (the induction routes)

| statement | n = 6 | n = 7 | n = 8 | source |
|---|---|---|---|---|
| ROOT(n) (weak Δ through r) | PROVED for \|S\| ≤ 2n−3 (n ≥ 6); CERT ≤ 14; **fails at 15 (real, 21 sets; abs)**; 16 vacuous | CERT ≤ 14; 15, 16 open; **fails at 17 (real: R7's set and T1's 3 sets; abs)** | CERT ≤ 15 (CONJ-TS′(8) + Fact E; ≤ 14 directly) | DELTA3N selection; R/ROOT6_MAIN; claims root6-real-15, root6-m16-vacuous, root7-m17-abstract, root7-real-17, root7-real-17-t1 |
| CONJ-TS′(n) (terminal-safe weak Δ of U) | CERT ≤ 12; **fails at 13 (real)** and at 14 (real; V2, side observation in the tspm6-14 verdict [corrected 15 Nov pm (C1 issue 12): EXACT by V2's code only, not filed as a claim and not checked by a second party]) | CERT ≤ 14; **fails at 17 (real; claim cts7-real-17 by T3, CONFIRMED)** and at 19 (real S19); least real size now 15-17 | CERT ≤ 15 | R/CONJTS_TEST; R/S19_REALIZABILITY; claims cts6-real-13, root7-m17-abstract, root7-real-17, cts7-real-17 |
| no (n−2)-cup in U ⟹ rooted / terminal-safe | PROVED (structure Thm 2; Lemma SD) | same; "no (n−1)-cup" does not suffice (U18) | same | DELTA3N selection; R/VERIFICATION P3 |
| **LR(n)** (weak Δ through l or through r) | **TRUE for all signotopes** (LR at 15 CERTIFIED by T1 on T3's CNF, claim lrr6-certified, CONFIRMED by V1; and again on T4's independent CNF `lr6_m15.cnf` [corrected 15 Nov pm (C1 issue 7): independent in code and in the left-side construction, same base-clause patterns (V2)], run by T3, claim lr6-m15-second, CONFIRMED by V2; the main session re-ran cake_lpr on both proofs (exact line, hashes equal); ≤ 14 by ROOT(6); ≥ 16 vacuous) | CERT ≤ 14; **15: CaDiCaL UNSAT (T1, 7,857 s; LRAT 23.7 GB kept as zstd) but cake_lpr at heap 1,150 MB ran out of heap, so COMPUTED only until a larger-heap check**; holds on all 12 known ROOT(7) failure order types; 16 open | CERT ≤ 15; open | §5; candidates K1 |
| **TS±(n)** (terminal-safe on the right or initial-safe on the left) [corrected 15 Nov pm (C1 issue 3): the certificates cover the hypothesised form only, r ends and l starts a 4-cap (claims tspm6-le13, tspm6-14)] | CERT ≤ 13 (claim tspm6-le13, CONFIRMED); 14 CERTIFIED on T4's CNF (claim tspm6-14, CONFIRMED by V2 after the main session's cake re-run) [note 15 Nov pm (C1 issue 5): V3's verdict on tspm6-m15-abstract (file 16:33:57, unchanged at 19:10) still marks the sentence "TS±(6) is decided … true up to 14" NOT CONFIRMED; its stated reason, tspm6-14 NOT CONFIRMED, lapsed at 16:53:54 when V2 changed tspm6-14 to CONFIRMED]; **fails at 15: abstract (T3, model of T4's `tspm6_m15.cnf`, claim tspm6-m15-abstract, CONFIRMED by V3; that model is not realizable [corrected 15 Nov pm: it has no x-sorted realization, a BFP certificate on 9 points + V with 76 inequalities, V2 in VERIFY_TSPM6_REAL15.md]) and real (T1, a different model, claim tspm6-real-15, CONFIRMED by V2)**; on the abstract one r and l are both rootable | CERT ≤ 14; holds on the 5 ROOT(7) failures (3,263-3,825 left) and S19 (1,795 left) | CERT ≤ 15 | §5; candidates K2 |
| TWO-ENV#(n): ENV#(S − r) or mirror ENV#(S − l) | **TRUE for all signotopes** [corrected 15 Nov pm (C1 issue 3): in the hypothesised form only, r ends a 4-cap and l starts one, which is what claims twoenv6-m15, twoenv6-13-14 and twoenv6-m15-second certify; without the hypotheses only \|S\| ≤ 12 is covered (VERIFY_TWOENV6_13_14.md), and ENV#(6) is open at \|U\| = 12, 13 and false at 14; weak D needs only the hypothesised form (L2, then L1)] (15 points: T3's own CNF, claim twoenv6-m15, CONFIRMED by V1, cake re-run by the main session; 13-14 certified directly, claim twoenv6-13-14, and also via TS±(6) by L2; ≤ 12 from ENV#(6) ≤ 11; ≥ 16 vacuous); holds on every known set, including the TS±(6) failures | CERT ≤ 14 (ENV#(7) ≤ 13 applied to U); holds on all 12 known ROOT(7) failure order types (left ≥ 3,551); 15 open (CNF ready) | CERT ≤ 15 (CONJ-TS′(8) ≤ 15 implies it); holds on ETV42 | §3; claim twoenv6-m15; TS± ⟹ TWO-ENV# ⟹ LR |
| **ONE(n)** (≤ 1 unrootable point) | for \|S\| ≤ n+3 every prescribed root lies in a weak Δ (parent's argument, reviewed in the DELTA3N structure record); **n = 6: every point of every valid signotope with ≤ 12 points lies in a weak Δ** (T4 `one_cnf.py` variant, CaDiCaL UNSAT for m = 10, 11, 12: COMPUTED; rows validated semantically on d6_12), so unrootable points first appear at 13-15 points; exactly 1 unrootable point in all 27 rooted failures, 0 elsewhere | same | same | DELTA3N selection README; §3 |
| ENV#(n) | CERT \|U\| ≤ 11 (claim env6-le11 by T3); **fails at \|U\| = 14 and 15 (real; abs)**; 12, 13 open | CERT \|U\| ≤ 13; **fails at \|U\| = 16 and 17 (real; abs)**; 14-15 open | holds on ETV42 + 241 pool sets | R/ROUND6 §1; claims env6-fails-root6m15, env6-real-14-15, root7-m17-abstract, env7-real-16-17 |
| VE(n), (U) (uniform over real insertions) | **fail at \|U\| = 14 (real)** (corollary of root6-real-15) | **fail at \|U\| = 16 (real)** (corollary of root7-real-17); (U) contains weak D(4,7) (true) | open; contain weak D(4,8) (open 17-22) | R/METHODS_SWEEP §3.1; claims env6-real-14-15, env7-real-16-17 |
| RT*(n) | not refuted: for the actual r of a ROOT(6) set it only asks for a weak Δ of S inside U, which exists (all 409-600 weak Δs avoid r); other insertions not checked | open | open | R/METHODS_SWEEP §3.1 |
| UES*(7) | — | open; its look-ahead fails (COMPUTED) | — | R/ROUND2 Task 4; R/ROUND6 |
| AT_n / doubly rooted (weak Δ through r and r−1) | **fail at 2n−2 = 10, 12, 14 (real)**; CERT ≤ 2n−3 | | | R/ROUND6 §2 |
| AT2_n, AT3_n, LT-cover_n | AT2_6 fails at 13 (real); AT2_7 CERT ≤ 13; AT3 fails (real); LT-cover_6,7,8 false as stated | | | R/ROUND6 §2 |
| DEPTH(n): depth(r) ≤ 1 ⟹ ROOT | CONJECTURE; consistent with all data (§3); CNF at m = 15 ready | | | candidates K5′ |
| **LP0(n)**: r unrootable ⟹ P0 (points ending no 4-cap) is a weak Δ | CONJECTURE; holds in all 33 known ROOT(6) failure order types; holds for ≤ 14 points (r is always rootable there); m = 15 decides n = 6 (T4's CNF keeps the hypothesis "r ends a 4-cap", harmless given weak D(5,6); SAT-mode probe: no model in 221 CPU-s) | **FALSE at 19 (abs)**: P2 extended R7's real 17-point block by 2 points (r stays unrootable by Lemma M) so that P0 misses 47 hexagons, while l stays rootable (claim lp0-7-false-abstract, CONFIRMED by V2); that set and all 108 such 19-point extension models of P2's scan are not realizable (claims lp0-7-w19-nonreal, lp0-7-realblock-nonreal, lp0-7-scan-all-nonreal, BFP certificates, CONFIRMED) [corrected 15 Nov pm (C1 issue 20): none of the 108 has an x-sorted realization; 20 of them (W among them) have V-free certificates, i.e. no realization at all, and the other 88 only certificates with V (V2's verdicts)], so LP0(7) is open for point sets; holds in all 12 ROOT(7) failure types found by the SAT/CEGAR searches | — | candidates K6 |

### 1.5 The case n = 6 at a glance (all (5,6)-valid signotopes have at most 15 points)

| statement | holds for | fails at | status |
|---|---|---|---|
| weak D(5,6) | all sizes | — | **true** (CERTIFIED, DELTA2N) |
| LR(6) | all sizes | — | **true** (two certificates at 15; claims lrr6-certified, lr6-m15-second) |
| TWO-ENV#(6) | all sizes | — | **true** (claims twoenv6-m15, twoenv6-13-14; ≤ 12 via ENV#(6)) [corrected 15 Nov pm (C1 issue 3): hypothesised form, r ends and l starts a 4-cap] |
| LP0(6) | ≤ 14 | — | open at 15 only |
| CB(6) | ≤ 13 | — | open at 14, 15 |
| TS±(6) | ≤ 14 [corrected 15 Nov pm (C1 issue 3): hypothesised form] | 15 (real) | false |
| ROOT(6) | ≤ 14 | 15 (real) | false |
| CONJ-TS′(6) | ≤ 12 | 13 (real) | false |
| ENV#(6) (as a statement on U) | \|U\| ≤ 11 | \|U\| = 14 (real) | false; 12, 13 open |
| every point lies in a weak Δ | ≤ 12 (COMPUTED) | 15 (r in the ROOT(6) failures) | false; 13, 14 open |
| cup-side D(5,6) / strong D(5,6) | ≤ 13 / ≤ 11 | 15 / 15 (real) | false |
| TRIV(6) (P0 or Q0 is a weak Δ) | ≤ 9 (COMPUTED) | 10 (abs) | false |

So at n = 6 every one-sided or explicit selection fails, while the two two-sided forms LR and TWO-ENV# hold at every
size [corrected 15 Nov pm (C1 issue 3): TWO-ENV# in its hypothesised form], and LP0 is open only at the extremal size 15.

## 2. (b) Implications

### 2.1 Diagram (arrows are PROVED unless marked)

```
 CONJ-TS'(n) ──Fact E──► ROOT(n) ─────────────┐
      │                     │                 │ (per size: ROOT at m + weak D below m ⟹ weak D at m)
      ▼                     ▼                 ▼
   TS±(n) ──► TWO-ENV#(n) ──► LR(n) ──induction on |S|──► weak D(5,n) ──► T(n) ──► M(5;n) ≤ C(n-1,2)+1+M(5;n-1)
                              ▲  ▲               ▲  ▲          │
   ONE(n) ────────────────────┘  │               │  │          └──(n=8, with M(5;7) ≤ 36)──► N5 ≤ 58 ──► ES(8) ≤ 303
   LP0(n), TRIV(n) (false) ──────┘               │  │
   ENV#(n) at |U| = m ──► ROOT(n), weak D at m+1  │  │
   TS-selection ⟹ ENV# ⟹ (U) ⟹ UES*; UES*(7) ⟹ weak D(5,7)
   ENV# ⟹ VE ⟹ ROOT;  VE ⟹ RT* ⟹ weak D      │  │
   AT_n(S−r) ⟹ doubly rooted ⟹ ROOT            │  │
   strong D(5,n) ⟹ CB(n) ────────────────────────┘  │       CB(n) ⟹ M(5;n) ≤ C(n-1,2) + M(5;n-1)
   cup-side D(5,n) ─────────────────────────────────┘       strong D(5,n) ⟹ M(5;n) ≤ M(4;n-1) + M(5;n-1)
   (U) on 4-cap-free U ⟺ weak D(4,n)  (so ENV#, (U), VE, UES* each contain weak D(4,n))
```

Sources: Fact E, Theorem 3 and its rooted / left-or-right variants (R/VERIFICATION P2); ENV# ⟹ ROOT at +1 (R/ROUND6 §1
statement 13); TS ⟹ ENV# ⟹ (U) ⟹ UES* and VE ⟹ RT* (R/METHODS_SWEEP §3.1, ideas 8, 42, 55; L1-L2 read but not
verifier-run); UES*(7) ⟹ weak D(5,7) (R/ROUND2 Corollary C); AT_n ⟹ doubly rooted (R/ROUND6 statement 4); (U) ⟺ weak
D(4,n) (R/VERIFICATION P1, Lemma U4); weak D ⟹ T and T ⟹ the recursion (R/VERIFICATION P4).

**Short proofs of the arrows added here (T4; PROVED).**
- *LR(n) ⟹ weak D(5,n).* Induct on |S|. If r ends no 4-cap, then r lies in no 4-cap of S (it is rightmost), so a weak
  Δ of S − r plus r is 4-cap-free and meets every gon of S; likewise for l. Otherwise LR gives the weak Δ. ∎ (This is the
  per-set disjunction already noted in R/VERIFICATION P2.)
- *TS±(n) ⟹ TWO-ENV#(n) ⟹ LR(n).* P4(U) ⊆ ↑P4(U), so a terminal-safe weak Δ of U is an ENV# Δ of U. If A is an ENV# Δ
  of U, then A + r is 4-cap-free, because C_r is a down-set of ⊑ that avoids P4(U), hence is disjoint from ↑P4(U)
  (R/ROUND6 statement 13); so A + r is a weak Δ of S through r. Mirror for l. ∎
- *LP0(n) ⟹ LR(n) and weak D(5,n).* P0 (points ending no 4-cap) has no 4-cap (a 4-cap inside P0 would end at a
  point of P0) and contains l (l ends nothing). So if r lies in no weak Δ, LP0 makes P0 a weak Δ through l; and in
  either case S has a weak Δ. ∎
- *Rooted solutions versus ENV#.* For every valid S, the ENV# Δs of U are rooted at r, and **if C_r is the whole
  complement of ↑P4(U) (r = r0), the rooted Δs at r are exactly the ENV# Δs of U**: both say "A is a weak Δ of U with
  no 4-cap and no 3-cap (a,b,c) whose pair (b,c) lies outside ↑P4(U)". ∎ (This explains the equal counts 84 = 84,
  232 = 232, 600 = 600 in the AT sets and 0 = 0 in root7_m17.)
- *CB(n) ⟹ the sharper recursion.* A CB Δ has no 4-cap and no (n−1)-cup, so |Δ| ≤ C(4+(n−1)−4, 2) = C(n−1,2) by the
  Erdős–Szekeres cup–cap theorem (f(k,l) = C(k+l−4, k−2)); S − Δ has no 5-cap and no gon, so |S − Δ| ≤ M(5;n−1). ∎

### 2.2 Monotonicity and the gluing form of LR (T4; PROVED)

**Lemma M.** Let W be (5,n)-valid and T ⊆ W. If D is a weak Δ of W, then D ∩ T is a weak Δ of T.
*Proof.* D ∩ T ⊆ D has no 4-cap. A gon G of T is a convex (n−1)-subset of W, hence a gon of W, so D meets G inside
G ⊆ T. ∎

**Corollaries.**
1. *Unrootability lifts.* If p ∈ T lies in no weak Δ of T, it lies in no weak Δ of any valid W ⊇ T. The unrootable
   points of T stay unrootable in every valid superset.
2. *ROOT failures are upward closed:* if S fails ROOT and W ⊇ S is valid with max W = max S, then W fails ROOT (r still
   ends a 4-cap). This does not hold for CONJ-TS′ or ENV#: their conditions refer to P4(U) and ↑P4(U), which grow with U.
3. *Gluing form of LR.* LR(n) fails exactly when some valid W has both l(W) and r(W) unrootable (if r(W) ends no
   4-cap, or l(W) starts none, then W − r or W − l has no weak Δ at all, so weak D fails and LR fails by L1; wording
   fixed after V2's review, claim t4-lemmas); by 1 this happens as soon as W contains a set T_r with max T_r = r(W) in which r(W) is unrootable and a set T_l with min T_l = l(W) in which
   l(W) is unrootable. So **LR(n) says that a right-hostile and a left-hostile configuration can never be glued into one
   valid set with these extreme points.**
4. *Room.* ROOT is CERTIFIED for |T| ≤ 14 (n = 6, 7) and ≤ 15 (n = 8), so hostile blocks have at least 15 (16) points.
   For n = 6 every valid set has at most 15 points, so an LR(6) failure must be one 15-point set hostile at both ends
   (T_l = T_r = W); the single LR(6) CNF at 15 points decides exactly this. For n = 7 two hostile blocks of at least 15
   points each must share at least 30 − M(5;7) points: at least 4 if M(5;7) equals the ETV value 26, none under the
   proven bound 36; the known minimal right-hostile blocks at n = 7 have 17 points (finding 8), which would push the
   overlap to at least 8 under the ETV value. In every known rooted failure the opposite end is not hostile at all
   (finding 2), and the hostile
   side brings many 4-cap start pairs into the other side (finding 3, item 5 of §4), which is what large overlaps would
   have to overcome (HEURISTIC).

### 2.3 What each surviving statement would give for ES(8)

The ledger rows of ROADMAP20261115 SYNTHESIS §2.2 (weak Conj(8) → 303, weak Conj(7)+(8) → 298, strong Conj(8) → 297,
N5 ≤ 62 → 307) all fit ES(8) ≤ 245 + N5 in this range; the rows below use that reading (arithmetic only, not re-derived).

| statement assumed for all sizes | N5 = M(5;8) bound | ES(8) bound |
|---|---|---|
| T(8), or weak D(5,8), or LR(8), TWO-ENV#(8), LP0(8) | 22 + 36 = 58 | 303 |
| weak D(5,7) and weak D(5,8) (or LR(7) and LR(8)) | 22 + (16 + 15) = 53 | 298 |
| CB(8) (CONJECTURE) | 21 + 36 = 57 | 302 (reading) |
| CB(7) and CB(8) (CONJECTURE) | 21 + (15 + 15) = 51 | 296 (reading) |
| strong D(5,8) (fails at n = 6 at the extremal size) | 16 + 36 = 52 | 297 |

For comparison the Erdős–Tuza–Valtr values are M(5;6) = 15, M(5;7) = 26, M(5;8) = 42 (Σ_{i≤3} C(n−2,i); 26 is attained
by signotopes per NOVELTY20261113B).

## 3. (c) What the counterexamples have in common

All numbers EXACT (T4's own exhaustive code from coordinates or sign strings; `t4/table.py`, `t4/analyze.py`,
`t4/tsboth.py`, `t4/rcaps.py`, `t4/core.py`, `t4/twins.py`, `t4/rules.py`). Columns: 4-caps at r = 4-caps of S ending
at r; C_r / outside ↑P4 = pairs capped by r against the pairs of U outside ↑P4(U) (the most any 5-cap-free extension
can cap); through r / l = weak Δs of S containing r / l; TS right = terminal-safe weak Δs of U; IS left = initial-safe
weak Δs of V; ENV#(U) = ENV# Δs of U = S − r. cup15 is a real set (coordinates in its file; its signs were used).

| set | n | m | longest cup | 4-caps | gons | 4-caps at r | P4(U) | ↑P4(U) | C_r / outside ↑P4 | depth r | depth l | τ | weak Δs | through r | through l | unrootable | TS right | IS left | ENV#(U) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 21 real ROOT(6) sets (T1) | 6 | 15 | 5 | 78-88 | 289-317 | 29-39 | 10 | 20 | 62-68 / 71 | 2 | 2 | 7 | 409-600 | **0** | 220-268 | 1 | 0 | 179-211 | 0 |
| root6_m15 (abstract) | 6 | 15 | 5 | 98 | 329 | 43 | 9 | 19 | 69 / 72 | 2 | 2 | 7 | 467 | **0** | 231 | 1 | 0 | 206 | 0 |
| root7_m17 (T3, abstract, non-realizable) | 7 | 17 | 6 | 163 | 229 | 109 | 9 | 16 | **104 / 104** | 2 | 3 | 4 | 7,736 | **0** | 3,741 | 1 | 0 | 3,263 | 0 |
| real ROOT(7) set of R7 (root7_real17) | 7 | 17 | 6 | 170 | 306 | 117 | 8 | 14 | **106 / 106** | 2 | 3 | 5 | 8,435 | **0** | 4,316 | 1 | 0 | 3,825 | 0 |
| 3 real ROOT(7) sets of T1 (m17_it4-6, one U type) | 7 | 17 | 6 | 168-169 | 328 | 110-111 | 8 | 13 | 104-106 / 107 | 2 | 3 | 4 | 8,195 | **0** | 4,129 | 1 | 0 | 3,683 | 0 |
| CONJ-TS′(6) lattice-nohyp | 6 | 13 | 5 | 6 | 154 | 2 | 3 | 36 | 10 / 30 | 1 | 1 | 5 | 1,997 | 1,094 | 1,191 | 0 | **0** | 78 | 508 |
| CONJ-TS′(6) lattice-hyp | 6 | 13 | 5 | 18 | 150 | 6 | 4 | 39 | 20 / 27 | 1 | 2 | 5 | 1,074 | 462 | 609 | 0 | **0** | 354 | 208 |
| CONJ-TS′(6) flat-hyp | 6 | 13 | 5 | 6 | 133 | 2 | 3 | 30 | 11 / 36 | 1 | 1 | 5 | 2,062 | 1,124 | 1,201 | 0 | **0** | 63 | 467 |
| AT_6 d6_11 | 6 | 11 | 5 | 40 | 33 | 28 | 4 | 4 | 41 / 41 | 1 | 2 | 3 | 494 | 84 | 189 | 0 | 84 | 177 | 84 |
| AT_6 d6_12 | 6 | 12 | 5 | 68 | 55 | 42 | 4 | 5 | 49 / 50 | 1 | 2 | 4 | 486 | 34 | 240 | 0 | 30 | 214 | 32 |
| AT_7 d7_13 | 7 | 13 | 6 | 65 | 32 | 50 | 5 | 5 | 61 / 61 | 1 | 2 | 2 | 2,535 | 232 | 970 | 0 | 232 | 924 | 232 |
| AT_8 d8_15 | 8 | 15 | 7 | 114 | 30 | 102 | 4 | 4 | 87 / 87 | 1 | 2 | 2 | 12,176 | 600 | 5,112 | 0 | 600 | 5,082 | 600 |
| AT2_6 seed1_b | 6 | 13 | 5 | 62 | 114 | 1 | 8 | 14 | 15 / 52 | 1 | 2 | 5 | 653 | 378 | 432 | 0 | 7 | 236 | 7 |
| AT2_6 seed5_b | 6 | 13 | 5 | 32 | 145 | 14 | 3 | 5 | 42 / 61 | 1 | 2 | 5 | 696 | 130 | 433 | 0 | 10 | 145 | 12 |
| cup-side D(5,6) cup15 | 6 | 15 | 5 | 80 | 216 | 6 | 21 | 59 | 25 / 32 | 3 | 2 | 7 | 353 | 219 | 139 | 0 | 53 | 1 | 203 |
| strong D(5,6) strong15 (E4) | 6 | 15 | 5 | 72 | 220 | 7 | 17 | 57 | 19 / 34 | 2 | 2 | 7 | 316 | 228 | 157 | 0 | 101 | 24 | 202 |
| CONJ-TS′(7) S19 (real v1) | 7 | 19 | 6 | 126 | 424 | 11 | 16 | 104 | 37 / 49 | 2 | 2 | 5 | 9,601 | 4,057 | 5,726 | 0 | **0** | 1,795 | 4,057 |
| TS±(6) counterexample (T3, abstract) | 6 | 15 | 5 | 25 | 282 | 3 | 9 | 61 | 22 / 30 | 2 | 2 | 7 | 1,607 | 914 | 717 | 0 | **0** | **0** | 526 |
| real TS±(6) counterexample (T1, tspm6_real15) | 6 | 15 | 5 | 24 | 265 | 4 | 9 | 57 | 28 / 34 | 2 | 1 | 7 | 2,219 | 1,211 | 978 | 0 | **0** | **0** | 730 |
| ETV extremal etv656 (control) | 6 | 15 | 5 | 281 | 521 | 71 | 18 | 18 | 58 / 73 | 2 | 2 | 7 | 441 | 168 | 231 | 0 | 150 | 185 | 150 |

[note 15 Nov pm (C1 issue 15b): the row "21 real ROOT(6) sets" and the statistics drawn from it below (29-39 four-caps
at r, P4(U) = 10, ↑P4(U) = 20, 2 distinct U types, layers 10 + 4 + 1) describe T1's first 21 real sets only. By 18:22
T1 had 177 distinct real 15-point ROOT(6) counterexamples (EXACT by T1's coordinate checks, not filed;
ROOT6_M15_REALIZE.md items 18-19), with 66-112 four-caps, 25-57 of them at r, and 205-308 convex pentagons in U; T4's
other statistics were not recomputed on them.]

**Findings.**
1. **Every counterexample has a longest cup of exactly n − 1** (the maximum: an n-cup is an n-gon); σ13 (a = 4, n = 7)
   too (longest cup 6). This matches the PROVED positive side: if U has no (n−2)-cup, the right ends of its gons plus r
   form a rooted Δ (DELTA3N structure Thm 2), and Q0 is a weak Δ when S has no (n−2)-cup (Lemma SD).
2. **The failures are one-sided, and the other side is trivially fine.** In every set the failing side (r for
   ROOT/TS/ENV#, the pair (r−1, r) for AT) is the least rootable side; the other side has many solutions (through l:
   139-5,112; initial-safe: 1-5,082). More: **P0 (points ending no 4-cap) is itself a weak Δ in every set of the table
   (all 27 rooted failures included) except cup15, where Q0 is** (`t4/rules.py`; also on all of DELTA2N's small cex sets).
   The same holds for **every rooted failure produced today: 33 distinct ROOT(6) order types (the 32 CEGAR models of
   T1's cg15 run and the main session's model; 9 distinct U) and 12 distinct ROOT(7) order types (T3's model, the CEGAR
   models of T1's r7c17 and R7's cg17 runs, the real sets; 10 distinct U)**: in each, r lies in no weak Δ, l lies in
   one, P0 is a weak Δ, and the mirror image of S − l has ENV# Δs (at least 179 at n = 6, 3,551 at n = 7), so LR, LP0
   and TWO-ENV# hold (`t4/lp0check.py`, `t4/twoenvcheck.py`, EXACT per set). But P0 is not forced: P2 added 2 points to
   R7's real block (r stays unrootable by Lemma M) and obtained a 19-point abstract W in which P0 misses 47 hexagons
   while l still lies in 5,833 weak Δs (claim lp0-7-false-abstract). The searches simply never produced such sets.
   T4's own check of W (`t4/lp0check.py`, `t4/twoenvcheck.py`): valid, r unrootable, l rootable, P0 not a weak Δ, and
   TWO-ENV# still holds (the mirror image of W − l has 4,401 ENV# Δs). The SAT searches built sets
   hostile at r and found the left side open in the most trivial way. A two-sided failure needs more: the two-layer rule
   TRIV fails at 10 points (abs, n = 6) and for real sets at n = 7, 8, but no set is known where both l and r are
   unrootable. The asymmetry is visible in the 4-cap end and start points (`t4/endpoints.py`): in the rooted failures
   the set R¹ of points that end a 4-cap is tiny (4-5 of 15 points at n = 6, 7 of 17 at n = 7) and contains no gon,
   so P0 = S − R¹ meets every gon; the start points L¹ are spread (8-13 points) and contain 1-48 gons, which is why Q0
   (∋ r) fails. cup15 is the mirror case (|R¹| = 9 with 10 gons inside, |L¹| = 6 with none).
3. **The rooted failures share one mechanism: r is a near-universal capper over a U with few 4-cap ends.** In
   R7's real ROOT(7) set, root7_m17 and the AT sets r caps every pair of U outside ↑P4(U) (C_r = 106/106, 104/104,
   41/41, 61/61, 87/87: r is exactly r0, and R7's set shows that a real r0 can occur) [corrected 15 Nov pm (C1 issue
   15): among the AT sets this holds for d6_11, d7_13 and d8_15 only; d6_12 has 49 of 50 (table above)], so by §2.1 the rooted Δs are
   exactly the ENV# Δs of U. In the other rooted failures r caps 62-69 of 71-72 (n = 6) and 104-106 of 107 (n = 7)
   pairs. In all 27 rooted failures P4(U) has only 8-10 pairs and ↑P4(U) 13-20 (of 91-120 pairs), and ENV#(U) = 0: a rooted Δ must avoid almost every 3-cap of U, i.e. be nearly a cup, while meeting every gon of U. This is the
   4-cap-ful analogue of Lemma U4 (a universal capper forces a cup, so (U) contains weak D(4,n)). The 21 real ROOT(6)
   sets [note 15 Nov pm (C1 issue 15b): T1's first 21; not recomputed on the 177 of 18:22, see the note under the
   table] have only **2 distinct U = S − r order types** (14 + 7 sets; T4's count agrees with V3), sharing the same 10
   P4 pairs and 20 ↑P4 pairs, and 14 distinct V = S − l types: they are different near-universal cappers r over two
   ENV#-hostile 14-point sets; likewise T1's three real ROOT(7) sets share one U = S − r. The terminal-safe failures (CONJ-TS′(6) sets, S19) are different: P4(U) is tiny (3-16
   pairs) but r caps few pairs; there the r-independent condition fails while ROOT holds. The gon shapes differ too:
   in the rooted failures 26-42 % of the gons have a 4-point cap part (the doubly hard (4, n−3)-gons of ETVTHY 2.6),
   in the CONJ-TS′(6) sets only 1-12 % (they are cup-heavy: 23-38 % of their gons are (n−1)-cups). The two TS±(6)
   counterexamples (T3's abstract and T1's real 15-point sets) push this to both sides: only 24-25 four-caps, so few
   4-cap end and start pairs (P4 = 9 on each side) that no terminal-safe or initial-safe set exists, while both ends are
   rootable (914/717 and 1,211/978 weak Δs through r/l) and ENV# holds on both sides (526/124 and 730/86). So the
   r-independent "pair ends a 4-cap" condition fails when 4-caps are scarce, the rooted conditions fail when they are
   plentiful at r; only the rooted two-sided forms (LR, LP0) and TWO-ENV# survive all known sets [superseded 15 Nov pm
   (C1 issue 1): LP0 fails on P2's abstract 19-point W (claim lp0-7-false-abstract); LR and TWO-ENV# hold there].
4. **ROOT failures sit at end-layer depth ≥ 2.** In all 22 ROOT(6) failures r is the only point of depth 2 (layers
   10 + 4 + 1) [note 15 Nov pm (C1 issue 15b): the first 21 real sets and root6_m15; not checked on T1's later real
   sets (177 distinct by 18:22)]; in the 5 ROOT(7) failures r has depth 2 (with one or two other points; layers 10 + 5 + 2 in the real
   ones). Of the 4-caps ending at r most have all three other points ending no 4-cap (20 of 37 in m15_it8_real, 29 of
   109 in root7_m17); one (n = 6) or a few (n = 7) have all three in R¹, which is what puts r at depth 2. Every set where ROOT holds has depth(r) = 1, except
   strong15, S19 and etv656 (depth 2) and cup15 (depth 3). So depth(r) ≥ 2 looks necessary for a ROOT failure
   (CONJECTURE DEPTH(n), candidates K5′) and is not sufficient.
5. **The obstructions are global.** Deletion-minimal unsatisfiable cores (`t4/cores.jsonl`) use every point of U: 76
   clauses (34 pentagons, 10 four-caps, 32 r-caps) for root6_m15; 57-59 for the three CONJ-TS′(6) sets; 95 for S19
   (29 hexagons, 66 bad triples). No small gadget explains a failure; this repeats DELTA2N's conclusion that every local
   rule breaks.
6. **Where the failures sit in size.** n = 6: strong D, cup-side D and ROOT fail exactly at 15 = M(5;6), the extremal
   size, and ROOT holds below it; CONJ-TS′(6) (13), AT_6 (11-12) and AT2_6 (13) fail below it. n = 7: CONJ-TS′(7) and
   ROOT(7) fail for real sets at 17, far below the ETV value 26. Both first rooted failures sit at 2n + 3 points (15 is
   exact for n = 6; for n = 7, 15 and 16 are open, and T3's 2,100 s SAT-mode search at 16 found no model). If the
   pattern held, ROOT(8) would first fail at 19 points (HEURISTIC, from 1.5 data points). The 21 real ROOT(6) sets have no twin points; the AT sets are
   cup blow-ups of 6-8 point configurations (d8_15 = {0,1,2} 3 {4..7} {8..12} 13 14, each cluster a cup).
7. **The ETV extremal constructions are easy.** etv656 (15 points, n = 6; table), etv757 (26 points, n = 7) and etv858
   (42 points, n = 8) all have weak Δs through r and through l, terminal-safe, initial-safe, ENV# and CB solutions
   (for 26 and 42 points by pysat with every witness re-checked exactly: EXACT for these positive answers;
   `t4/etv/`). ROOT and its mirror also hold on all 90 real (5,6)-valid pool sets with 14-15 points
   (`t4/poolroot.py`). The rooted failures are special configurations, not typical extremal ones.
8. **The rooted failures are minimal hostile blocks.** At n = 6 this is automatic (ROOT(6) holds at 14 points). At
   n = 7 both real 17-point order types (R7's and T1's) and T3's abstract model are vertex-critical: deleting any one
   point, l included, makes r rootable (`t4/essential.py`, EXACT). So the smallest known right-hostile blocks have 17
   points; by Lemma M an LR(7) failure needs a right- and a left-hostile block inside one valid set (§2.2, Cor. 4).
9. **A counting lens (HEURISTIC).** A split statement "Δ of type X, S − Δ gon-free" can hold at an extremal set only if
   (max size of X) + M(5;n−1) ≥ M(5;n). Against the ETV values: strong D has slack 0 for n = 6, 7, 8 (Pascal's rule is
   tight), CB has slack 3, 4, 5, weak D has slack 4, 5, 6, CB2 is negative (fails by counting at n = 6, as observed).
   The strong form failed exactly where it is tight; weak D and CB have room.

## 4. (d) Assessment

**Is the Δ route still viable?** As a research program: yes, with a sharper target than this morning. As a route to an
ES(8) bound in the near term: no.
- *Solid.* Weak D(5,6) is true; weak D(5,7) holds for every set with at most 15 points and weak D(5,8) for every set
  with at most 16 (CERTIFIED; ≤ 14 / ≤ 15 also through replayed CONJ-TS′ certificates; 16 is T3's claim wd58-m16); no counterexample to weak D is known for any n, abstract or real. The
  reductions LR(n), TS±(n), TWO-ENV#(n), LP0(n) ⟹ weak D(5,n) are PROVED (claim t4-lemmas for the first three; the LP0
  step in §2.1).
- *Fell today.* Every one-sided induction statement. At n = 6 and at n = 7, ROOT, CONJ-TS′, ENV#, VE and (U) are false
  for real point sets (15 and 17 points). So no proof of weak D(5,6) or weak D(5,7) by the one-sided rooted induction
  exists, even for point sets, and by Lemma M every valid superset with the same rightmost point fails ROOT too. AT_n
  (double rooting) failed this morning. The a = 4 side (weak D(4,8) at 17-22) is open and is contained in every
  uniform (r-independent, one-sided) route at n = 8.
- *Survives, and gained two theorems* [corrected 15 Nov pm (C1 issue 7): two CERTIFIED results with a PROVED
  combination, computer-assisted and unrefereed, not written proofs]. **LR(6) and TWO-ENV#(6) are true for every signotope** (claims lrr6-certified
  and lr6-m15-second; twoenv6-m15; all CONFIRMED) [corrected 15 Nov pm (C1 issue 3): TWO-ENV#(6) in its hypothesised
  form, r ends and l starts a 4-cap]: at n = 6 the two-sided forms hold although the
  one-sided ones fail for real sets. LR, TWO-ENV#, CB and ONE hold on all 27 rooted failures (22 at n = 6, 5 at
  n = 7) and on every other counterexample of the program [corrected 15 Nov pm (C1 issue 1): on P2's W T4 checked
  only LR, LP0 and TWO-ENV#; CB and ONE were not checked there]; LP0 held on all of them too but fails on P2's 19-point
  abstract extension at n = 7. TS± also held on
  all of them but **fails at n = 6 with 15 points** (abstract; a set with only 25 four-caps on which both ends are
  rootable): the r-independent terminal-safe condition is too strong even in its two-sided form, while TWO-ENV#
  (526 ENV# Δs of U on that set) survives. CB(6) is CERTIFIED up to 13 points, CB(7) to 13 and CB(8) to 15 (the last
  two from the strong-form certificates) [corrected 15 Nov pm (C1 issue 13): CB(8) at 15 rests on DELTA2N's record only,
  a proof that was deleted and never re-run; CB(8) ≤ 14 is CERTIFIED twice (V1's verdict on cb78-from-strong)].
- *Caveats.* No proof mechanism is known for TWO-ENV#, LR, LP0 or CB beyond SAT. Every known counterexample is hostile at one
  end only (finding 2), so the data say little about sets hostile at both ends; the gluing view (Lemma M) shows what a
  two-sided failure would need: two hostile blocks, each with at least 15 points (17 in all known n = 7 examples),
  inside one valid set.
- *The gap is large.* Certification reaches 15-16 points; the vertex-critical window is 16-32 (n = 7) and 17-59 (n = 8,
  given weak D(5,8) at 16),
  and the one-sided forms failed at 15 (n = 6) and 17 (n = 7), just above the certified ranges. A certificate of a
  strengthening at small sizes is weak evidence for the sizes that matter.
- *The gain is modest.* Weak D(5,8) gives ES(8) ≤ 303 against the current ≤ 308; with weak D(5,7), 298; CB would add one
  or two. The upper-bound machinery of ROADMAP20261115 (budget-35 trees, N66 ≤ 55) remains the near-term path.

**Most promising next statements.** Two statements survive everything and are true at n = 6; each implies weak D(5,n)
(PROVED):
- **TWO-ENV#(n)** — U = S − r has an ENV# Δ or the mirror image of V = S − l has one. Each side is a property of U (resp.
  V) alone, so this is the r-independent, uniform form a structural proof could aim at. TRUE at n = 6 (claim
  twoenv6-m15) [corrected 15 Nov pm (C1 issue 3): in the hypothesised form, r ends and l starts a 4-cap; without the
  hypotheses only \|S\| ≤ 12 is covered], strictly weaker than the refuted TS±(6). n = 7: holds for |S| ≤ 14 by ENV#(7) ≤ 13 (CERTIFIED); first
  open size 15 (`t4/twoenv/twoenv7_m15.cnf`, controls PASS; T4's SAT-mode probe found no model in 1,540 CPU-s).
- **LR(n)** — S has a weak Δ through l or through r. TRUE at n = 6 (two certificates). LR(7) at 15: T1's CaDiCaL run
  ended UNSAT (7,857 s, LRAT 23.7 GB, kept), but cake_lpr at heap 1,150 MB ran out of heap, so it is COMPUTED until a
  larger-heap check (about 4-6 GB) is run; the 16-point run was stopped; LR(7) at 16 would extend weak
  D(5,7) to 16 points. At 17, where ROOT(7) fails, T3's SAT-mode search of an LR(7) CNF found no model in 2,500 s of wall
  time (ROOT(7) at 17 gave one after 1,599 s): HEURISTIC support only.
- *Demoted:* **LP0(n)** (r lies in a weak Δ, or the points that end no 4-cap meet every gon) held in every rooted
  failure the searches produced (45 order types) but is false at n = 7 for abstract 19-point sets built by extending
  hostile blocks (claim lp0-7-false-abstract; all 108 such models are non-realizable [corrected 15 Nov pm (C1 issue
  20): none has an x-sorted realization; 20 have none at all, 88 only certificates with V], so LP0(7) is open for point
  sets); LP0(6) at 15 is still open (T4's SAT-mode probe: no model in 221
  CPU-s). It stays useful as a sufficient condition (whenever P0 is a weak Δ, l is rootable), not as a target.

Next steps, in order of cost:
1. Done during the afternoon: the main session re-ran cake_lpr (heap 1,500 MB) on the LR(6) proofs of both encodings,
   the TS±(6)-at-14 proof, the TWO-ENV#(6) proofs (13-15) and the weak D(5,8)-at-16 proof: exact line, CNF and LRAT
   hashes equal (`round6/mainsession/*recake/`); V2 then confirmed lr6-m15-second, tspm6-14 and wd58-m16 (16:55).
2. TWO-ENV#(7) and LR(7) at 15, 16 (LR(7) at 16 or TWO-ENV#(7) at 16 would extend weak D(5,7) to 16 points).
3. CB(6) at 14, 15, CB(7) at 14, 15, CB(8) at 16: the one sharpening with a better bound (≤ 13 / ≤ 13 / ≤ 15 are known).
4. Gluing (Lemma M): T3's first test (k ≤ 3 points added to the left of the 17-point blocks: 9 CNFs UNSAT) was vacuous:
   P2 showed that all 10 known right-hostile 17-point blocks are left-saturated, i.e. no (5,7)-valid signotope adds a
   point to the left of their leftmost point (claim leftsat-r7blocks, CONFIRMED). So an LR(7) failure containing a known
   block must keep the block's own l, which is rootable in every known block; new points can only go between or to the
   right. [corrected 15 Nov pm (C1 issue 7b): "the 10 tested blocks" named in claim leftsat-r7blocks, not all known
   ones: T1's real m17_it5 and m17_it6 (`t1/r7c17/feasible/m17_it5_real.json`, `m17_it6_real.json`) and R7's real
   `r7/div17/real/m17_it3_s1.json` were not tested, so the sentence before holds for the 10 tested blocks.] [note 15 Nov
   pm (C1 issue 11): T3 ran two gluing tests. `glue.py` adds k = 1..3 points left of l (the 9 CNFs above; vacuous by
   leftsat-r7blocks). `glue2.py` inserts k = 1, 2 points anywhere left of r: 16 of 17 and 136 of 153 patterns admit a
   valid W, and none gives an LR(7) failure (COMPUTED; PROBES_1115PM.md status table). That second test is not vacuous.] Block extension remains the productive search (it produced P2's LP0 counterexample).
5. Theory: prove a special case of TWO-ENV# or LR, e.g. when r is the maximal capper r0 (then rooted Δs = ENV# Δs of
   U, §2.1), and explain why the left side stays open when the right side is hostile (finding 2; P2's 19-point set shows
   the witness need not be P0).

**What would kill it.**
- A counterexample to weak D(5,8) (kills the 303 route outright) or to weak D(5,7) (kills 298). There is none with at
  most 16 points for n = 8 (claim wd58-m16) or 15 for n = 7; T3's direct weak D(5,7) CNF at 16 (`t3/cnf/wd57_m16.cnf`) is
  the next test, and ROOT(7) failed at 17 in SAT mode, so a weak-D failure near 17-18 points is within reach of the
  same kind of search.
- An LR failure at n = 7 or 8 (a valid set with both extreme points in no weak Δ): weak D would survive, but without any
  known induction scheme. (LP0's failure at n = 7 removed only the explanation, as expected.) Lemma M makes block
  extension a productive search: P2's LP0 counterexample came from extending a known hostile block by two points.
- For CB: a failure at n = 6 (decidable at 14, 15) would remove the only sharpening with a better bound.

## 5. T4's results today (with claim status)

| item | label | claim / status |
|---|---|---|
| ROOT(6) at 16 points is vacuous (no (5,6)-valid signotope on 16 points), so ROOT(6) is completely decided for signotopes; same for every n = 6 statement at ≥ 16 points | CERTIFIED by citation (DELTA2N base(5,6,16); its LRAT not kept) + PROVED | root6-m16-vacuous, filed 13:38, **CONFIRMED by V1** (T1 re-certified base(5,6,16) with its own encoder) |
| ENV#(6) fails for real 14- and 15-point sets (21 real sets: 0 ENV# Δs for U = S and U = S − r); corollaries VE(6), (U) fail at U = S − r | EXACT (own code) + PROVED | env6-real-14-15, filed 13:47, **CONFIRMED by V3** |
| ENV#(7) fails for real 16- and 17-point sets (R7's and T1's real ROOT(7) sets: 0 ENV# Δs for U = S and S − r); VE(7), (U) fail at U = S − r | EXACT (own code) + PROVED | env7-real-16-17, filed 14:15, **CONFIRMED** (verdict 14:21) |
| TS±(6) holds for every signotope with at most 13 points (13 is where CONJ-TS′(6) fails) | CERTIFIED (T4's CNF `tspm6_m13.cnf`, certified by T3: CaDiCaL 71 s, LRAT 520 MB, cake exact line) + citation of CONJ-TS′(6) ≤ 12 | tspm6-le13, filed 14:18, **CONFIRMED by V3** (own cake re-run, 162 semantic controls); extended to 14 points by T3's claim tspm6-14 on T4's `tspm6_m14.cnf` (CONFIRMED by V2 at 16:55 after the main session's cake re-run, `round6/mainsession/tspm6recake/`) |
| CB(6) holds for every signotope with at most 13 points | CERTIFIED (cake_lpr exact line, m = 7..13; m ≤ 6 trivial; m = 13: CaDiCaL 567 s at 20 % quota, LRAT 846 MB, cake 151 s at heap 340 MB) | cb6-le13, filed 14:12, **CONFIRMED by V2** (cake re-run 7/7; V2's own encoder certified m = 7..13 [corrected 15 Nov pm (C1 issue 13): was "m = 7..12"; V2's 15:27 addendum in the cb6-le13 verdict adds m = 13]) |
| Four short lemmas: LR ⟹ weak D; TS± ⟹ TWO-ENV# ⟹ LR; rooted Δs = ENV# Δs when r = r0; Lemma M (monotonicity, gluing form of LR) | PROVED | t4-lemmas, filed 14:09, **CONFIRMED by V2** (with the wording fix now in §2.2, Cor. 3; Cor. 4 not checked) |
| LR, TS±, TWO-ENV#, CB, ONE hold on the 21 real ROOT(6) sets, root6_m15, root7_m17 and the real ROOT(7) sets; LR, LP0 and TWO-ENV# hold on all 44 CEGAR models of rooted failures (45 distinct order types with the others); the rooted-failure mechanism (finding 3); minimal-block property (finding 8) | EXACT (own code) | §3; no new statement refuted |
| TRIV(6) fails for an abstract 10-point signotope (7-9 UNSAT) | COMPUTED (CaDiCaL verdicts; model re-checked exactly) | not filed (a T4 candidate, refuted by T4) |
| CB2(8) and the 5-cup-free transversal fail on ETV42 (42 points, 235,288 heptagons) | COMPUTED (pysat UNSAT on a 42-variable CNF; not certified) | — |
| ETV extremal sets (15, 26, 42 points) satisfy ROOT, mirror ROOT, TS, IS, ENV#, CB; 90 real (5,6) pool sets satisfy ROOT and mirror ROOT | EXACT (positive answers with re-checked witnesses) | — |
| d6_12 has 486 weak Δs | EXACT (own code) | agrees with claim d6-12-correction (CONFIRMED) |
| LR(6) at 15 points: T4's SAT-mode probe of `lr6_m15.cnf` | no model in 266 CPU-s, stopped at 13:50 to avoid duplicating T1's certification run (ROOT(6) at 15 gave a model in 26 s) | HEURISTIC |
| LP0(6) at 15 points: T4's SAT-mode probe of `lp0_6_m15.cnf` (unit esr-agy-t4-lp06) | no model in 221 CPU-s (CaDiCaL `-t 1400` is a wall-clock limit; the unit ran at 20 %, then 10 %) | HEURISTIC; open |
| Every point of every (5,6)-valid signotope with ≤ 12 points lies in a weak Δ (so ONE(6) holds there) | COMPUTED (CaDiCaL UNSAT, m = 10, 11, 12; m ≤ 9 PROVED in the DELTA3N structure record; row semantics checked on d6_12) | m = 13: no verdict in 300 CPU-s (unit esr-agy-t4-all6, wall-clock limit at 10 % quota) |
| DEPTH(6) at 15 points: SAT-mode probe of `depth6_m15.cnf` (unit esr-agy-t4-depth6) | no model in 190 CPU-s; stopped 15:07 to make room for the TWO-ENV# probe | HEURISTIC; open |
| TWO-ENV#(6) at 15 points: `twoenv6_m15.cnf` (T4's `twoenv_cnf.py` over round 6's `env_cnf.py`), controls PASS; SAT-mode probe (unit esr-agy-t4-twoenv6) | no model in 472 CPU-s; stopped 15:51 when T3 certified UNSAT with its own encoder (claim twoenv6-m15) | T4's CNF is a ready second encoding for a second certificate |
| TWO-ENV#(7) at 15 points: `twoenv7_m15.cnf` (sha `c2ce861c…`; copies = round 6's env7_m14.cnf, regenerated byte-identical), controls PASS on two 15-point subsets of R7's real set; SAT-mode probe (unit esr-agy-t4-twoenv7, 20 %) | no model in 1,540 CPU-s (wall-clock limit 7,700 s reached at 18:01) | HEURISTIC; open; a certified run is free for T3 |

Encoder notes. `lr_cnf.py` builds F(x) ∧ F(x∘μ) from any CNF whose first C(m,3) variables are the triples (round 6's
root_cnf.py, T4's ts_cnf.py); soundness: an LR (TS±) counterexample satisfies F with canonical auxiliaries and so does
its mirror. `cb_cnf.py`, `triv_cnf.py`, `depth_cnf.py` carry their soundness arguments in their docstrings. Controls
(`lr_control.py`, `ts_control.py`, `cb_control.py`): fixed signs of root6_m15 make copy 1 of LR SAT, copy 2 SAT on the
mirror and UNSAT on S, the full LR CNF UNSAT; the three CONJ-TS′(6) models make copy 1 of TS± SAT and the full CNF
UNSAT; AT2 seed1_b and seed5_b make copy 1 UNSAT; the CB CNF at 15 is UNSAT on root6_m15 and a real ROOT(6) set and
its CB2 variant SAT on both; the DEPTH CNF is UNSAT on root6_m15 and two real ROOT(6) sets (depth 2). All PASS.

## 6. Files

All under `/home/jay/research/data/roadmap-20261115/pm1115/t4/` (not in Git): `t4lib.py` (exact signotope toolkit with
self-test), `analyze.py`, `tsboth.py`, `rcaps.py`, `twins.py`, `core.py`, `table.py`, `envS.py`, `rules.py`,
`poolroot.py`, `utypes.py`, `upairs.py`, `sigma13.py`, `extremal_test.py`, `cb_test.py`, `cupfree_test.py`,
`lr_cnf.py`, `ts_cnf.py`, `cb_cnf.py`, `triv_cnf.py`, `depth_cnf.py`, `lr_control.py`, `ts_control.py`,
`cb_control.py`, `decode.py`, `lp0_cnf.py`, `lp0_control.py`, `lp0check.py`, `one_cnf.py` (and the variant
`one/one_single_cnf.py`), `one_semctl.py`, `twoenv_cnf.py`, `twoenv_control.py`, `endpoints.py`, `essential.py`,
`rcapsites.py`; outputs `profiles_*.jsonl`, `root15.profile.json`, `root7_m17.profile.json`, `real15/` (21 real ROOT(6)
sets: profiles, TS±, ENV#, input SHA-256), `real17/` (real ROOT(7) sets), `cegarmodels/` (the 44 CEGAR models of T1 and
R7 as sign strings), `table_rows*.jsonl`, `table_real15.jsonl`, `table_real17.jsonl`, `table_tspm.jsonl`, `cores.jsonl`,
`etv/`; CNFs `lr/lr6_m15.cnf` (`cae7193d…`), `ts/tspm6_m13.cnf` (`0bbee2d5…`), `ts/tspm6_m14.cnf` (`921018d6…`),
`ts/tspm6_m15.cnf` (`1467209f…`), `twoenv/twoenv7_m15.cnf` (`c2ce861c…`), `lp0/lp0_6_m15.cnf` (`bc8745fe…`), `depth/depth6_m15.cnf` (`8f15cba6…`), `cb/cb6_m13.cnf`
(`2dbe9c4c…`), `cb/cb6_m14.cnf` (`845547e1…`), `cb/cb6_m15.cnf` (`5e9fbf06…`), `twoenv/twoenv6_m15.cnf` (`b48d3fac…`),
`one/one6_m*.cnf`, `one/single6_m*.cnf`, `triv/triv6_m10.cnf` (`ab25227b…`); CB certificates `cb/cert/`
(`certify.jsonl`, proofs kept as zstd; the partial m = 14 LRAT of the stopped run was not a proof and was deleted);
candidate list `candidates.md`; claim files `claims/`.

Reproduce (each under a minute, one thread):

```bash
T4=/home/jay/research/data/roadmap-20261115/pm1115/t4; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd $T4 && OPENBLAS_NUM_THREADS=1 $PY t4lib.py                       # self-test
OPENBLAS_NUM_THREADS=1 $PY -I analyze.py ../t1/root6_real15.json 6   # one profile (rootability, layers, ENV#, ...)
OPENBLAS_NUM_THREADS=1 $PY -I rules.py 6 ../t1/real/m15_it8_real.json  # P0 / Q0 rule
OPENBLAS_NUM_THREADS=1 $PY -I lr_control.py lr/lr6_m15.cnf ../../round6/mainsession/root15/root6_m15.json
bash /home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/certify_cnf.sh cb/cb6_m12.cnf $T4/repro 300 --keep  # CB(6) m = 12 (about 12 s, 0.3 GB RSS)
```
