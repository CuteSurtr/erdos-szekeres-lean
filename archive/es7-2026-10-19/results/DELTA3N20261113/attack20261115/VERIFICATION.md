# Δ-reduction attacks of 15 November 2026: verification record

Written 05:30-05:50 KST on 15 Nov 2026 by a write-up agent of the overnight workflow. For each of the eight attacks on the
Δ-reduction conjecture it gives the strategy, the outcome and the verifiers' verdict. Rule applied: **a claim counts only
if no verifier refuted it and every fatal objection is answered**; otherwise it is reported as refuted or open, with the
reason. This agent did not re-derive or re-run anything. Its only own checks are the greps of cake_lpr logs listed in §10.
Everything else is the verifiers' work as they reported it.

This file **supersedes the "Verification" column of `README.md`** in this folder. README.md was written at 04:45, when 9
of 21 verifications had run and attack 8 had no result. README.md itself is not modified.

## 0. Headline

**Weak D(5,7) and weak D(5,8) remain OPEN: no proof and no counterexample. No ES bound changes.**

- **Verifier returns:** 24, three per attack. 19 did not refute and 5 refuted: one for attack 2, two for attack 6, two for
  attack 7.
- **No verifier found a mathematical error in any part labelled PROVED.** The five refutations hit headlines and labels:
  - attack 7's headline "the strategy cannot settle weak D(5,7)/D(5,8)";
  - attack 6's "R(4,7) CERTIFIED for m ≤ 12, so 13 is the least size";
  - attack 2, one default-rule refutation ("cannot confirm every step"). A second verifier answered it, except for two
    cited items (§2).

### 0.1 What is now PROVED and survived verification (exact statements)

Conventions for the whole file. Points lie in the plane in general position, with distinct x, and are sorted by x.
- (p,q,s) is a **cap** if s lies below the line pq, and a **cup** otherwise.
- A **k-cap** (k-cup) is a k-chain all of whose consecutive triples are caps (cups).
- **(5,n)-valid** means: no 5-cap and no convex n-gon.
- A **gon** is a convex (n−1)-gon.
- A **weak Δ** is a 4-cap-free subset that meets every gon.

The two items that bear on a proof route:

- **P1, attack 1, Lemma U4.** Fix n ≥ 5 and a 4-cap-free set U. For A ⊆ U, conditions (i) and (ii) are equivalent.
  - (i) A is a weak Δ of U, and A ∪ {r} is a weak Δ of U ∪ {r} for every point r to the right of U such that U ∪ {r} is
    in general position and 5-cap-free. Here r may create a convex n-gon. This is condition (U) of
    `../resume/selection/boundary/envelope/theory.md` §1.
  - (ii) A is a cup that meets every gon of U.

  **Corollary.** If every (5,n)-valid set has a solution of (U), then D(4,n; weak) holds. So any r-independent invariant of
  this kind for weak D(5,8) must prove D(4,8; weak). The records leave that open from 14 to 22 points: DELTA2N20261113
  README §4.1 has "(4, 8) strong 7–13, open from m = 14", and Baek gives M(4;8) = 22.

  **Not shown:** the same reduction when only admissible insertions (U ∪ {r} with no n-gon) are required.
- **P2, attack 2, Theorem 3 (reduction).** Write h_U(b,c) for the length of the longest cap of U ending with the pair
  (b,c). A ⊆ U is *terminal-safe in U* if A has no 4-cap and every 3-cap a<b<c inside A has h_U(b,c) ≥ 4.
  - **CONJ-TS′(n):** if S is (5,n)-valid and its rightmost point r is the last point of a 4-cap of S, then S − r has a weak
    Δ that is terminal-safe in S − r.
  - **Theorem:** if CONJ-TS′(n) holds for all valid sets, then weak D(5,n) holds. Hence every minimal counterexample to
    weak D(5,n) is a counterexample to CONJ-TS′(n) and, by reflection, to its mirror form.
  - The proof also goes through with the r-dependent *rooted* hypothesis: a weak Δ A of S − r with A ∪ {r} 4-cap-free.
    It also works with the per-set disjunction "the left side or the right side works".
  - Verified with it:
    - Fact E: if S is 5-cap-free and A is terminal-safe in S − r, then A ∪ {r} has no 4-cap.
    - Lemma 1: a cup C ⊆ S − p that meets every gon of S − p gives the weak Δ C ∪ {p} of S.
    - Lemma 2: top extension.
    - Forced structure F1-F4.
    - F5, except its projective normal form.
    - F6 for n = 7, 8 only: |S| ≥ 16, from CERTIFIED inputs.

Elementary or obstruction-side items, also verified:

- **P3, attack 3.**
  - **Lemma SD.** Let n ≥ 6 and let S have no 5-cap and no (n−2)-cup (no n-gon hypothesis is needed). Then
    Q = {p : p starts no 4-cap} is at once a weak, a cup-side and a cap-side Δ. This is a special case of DELTA3N
    `resume/selection/structure/theory.md` Theorem 2.
  - **Chain-length lemma.** For n ≥ 7 every gon has cap part ≤ 4 ≤ cup part, so the cup-side D(5,n) is the longer-chain
    form L(5,n).
  - The reflection and projective-chart sign rule σ′(T) = (−1)^{|T∩A|} σ(T).
- **P4, attack 5.**
  - The chain WD ⟹ FC ⟹ U ⟹ T.
  - If T(n) holds for all valid sets, then M(5;n) ≤ C(n−1,2) + 1 + M(5;n−1). So T(8) gives M(5;8) ≤ 58 (using the
    CERTIFIED M(5;7) ≤ 36), T(7) gives M(5;7) ≤ 31, and both together give M(5;8) ≤ 53.
  - Fractional vacuity.
  - The rank-monotone lemma: a β-antitone or ω-isotone set has no 4-cap.
- **P5, attack 6.** Rank lemmas L1-L4 for a = 5. The cross-reference inside L3 is corrected in §6.
- **P6, attack 7.** Window lemma (a)-(d). Every vertex-critical counterexample has:
  - 16-32 points for n = 7 (point sets and signotopes);
  - 16-59 points for n = 8 (point sets, via Baek's M(4;8) = 22), or 16-54 if weak D(5,7) holds.
- **P7.**
  - Attack 4: Lemmas A-D (4-cap-free pieces, reformulation, mirror transfer, clause patterns T and K).
  - Attack 8: the trivial lemma "τ(S) ≤ 3 gives a weak Δ".

### 0.2 What was refuted

**By verifiers:**
- **Attack 7, headline (2 of 3 verifiers).** These sentences do not count:
  - "cannot settle / cannot prove or refute";
  - "[16,26] and [16,42] cannot be removed by computation alone";
  - "by (ii) such a theorem cannot follow from generic properties".

  What survives is a HEURISTIC obstruction to the *proof* direction only (§7).
- **Attack 6, the minimality claim (2 of 3).** Downgraded. The status is now:
  - R(4,7) for m ≤ 11: COMPUTED;
  - m = 12: CERTIFIED by one verifier's own re-run;
  - "13 is the least size": COMPUTED.
- **Attack 2 (1 of 3, default rule).** Answered by the third verifier, except for two items that stay unverified:
  - F5's projective normal form;
  - the r-dependent envelope variant of the corollary.

**Statements shown false by the attacks** (each verified):
- "No (n−1)-cup implies a terminal-safe weak Δ" is false at n = 7. Witness: U18, attacks 1 and 2.
- The 4-cap hypothesis cannot be dropped from CONJ-TS′. Witness: S19, attack 2.
- "minΔ ≤ τ + 1" is false at n = 7 with 18 points: sets A and B, CERTIFIED, attack 8.
- Rank localisation R(4,7) is false for a 13-element abstract signotope (attack 6), although D(4,7) is CERTIFIED.
- Every coarse layer union listed in §4 fails, and so does every pointwise 6-tuple rule (CERTIFIED).
- A β-antitone set plus an ω-isotone set does not cover all gons at n = 6 and n = 7 (attack 5).
- The generic principle "vertex-critical counterexamples are smaller than the largest valid set" is false for three
  related forms at n = 6 (attack 7).
- None of the cap/cup exchanges examined relates the cup-side form to the cap-side form on valid sets (attack 3).

### 0.3 Single most promising next step

**Test CONJ-TS′ for abstract signotopes at the first sizes the boundary record does not cover, and certify the result:**
n = 7 at |S| = 13, 14, 15, and n = 8 at |S| = 15.

How to build the CNF:
- Use attack 1's signotope base (sig.py style), plus "r = the last point ends a 4-cap".
- Add one clause per candidate Δ ⊆ S − r. The clause says that Δ contains a 4-cap, or contains a 3-cap whose last pair
  is the last pair of no 4-cap of S − r, or misses a gon.
- Subsets of terminal-safe sets are terminal-safe, so the shrinking argument of attack 7 (d) caps candidate sizes at
  |S| − n + 1.
- Write the soundness argument down. Run positive controls on U18, S19 and the 28 trajectory sets. Certify with
  `.claude/skills/es-research/scripts/certify_cnf.sh`.

Why this step:
- CONJ-TS′ ⟹ weak D(5,n) is the only reduction that all three verifiers accepted (P2), and ROADMAP20261115 (§2 and §5
  item 3) already ranks this route first.
- Attack 6 shows that a strengthened localisation can fail on small abstract signotopes even when the base statement is
  CERTIFIED (R(4,7) against D(4,7)). At these sizes weak D is already CERTIFIED (DELTA2N README §4.1, m ≤ 15), so the run
  tests only the strengthening.
- What each answer would mean:
  - UNSAT through 15 makes CONJ-TS′ a credible target for a written proof. Attack 2 §5 states what that proof must show.
  - A SAT model either is realised, which refutes CONJ-TS′ for point sets and moves the work to the rooted hypothesis of
    P2, or it shows that realisability has to enter the proof.

Caveat: (5,7) at m = 15 may exceed the light-compute cap, since the weak eager run took 1,737 s (DELTA2N README §4.1
line 210). Start at 13.

## 1. Attack 1: induction by adding a rightmost point (Baek-style Δ removal)

**Strategy.** Candidate invariants are sorted by when Δ(U) is chosen:
- (a) before r is seen, which means terminal-safe or uniform-envelope selection;
- (b) after r is seen, which means a rooted weak Δ containing r.

The tools were exact geometry, pysat, and CaDiCaL plus cake_lpr.

**Outcome (author).**
- (A) Lemma U4 and its corollary, PROVED (P1).
- (B) The 18-point (5,7)-witness U18 has no terminal-safe weak Δ (CERTIFIED in DELTA3N `resume/selection/terminal`). Its
  longest cup has exactly n − 2 = 5 points: 230 five-cups and no six-cup.
- (C) CERTIFIED:
  - τ ≤ 3 at m = 2n − 3 for n = 6, 7 (9 and 11 points);
  - a rooted weak Δ with |Δ| ≤ 4 exists at m = 2n − 2 for n = 6, 7 (10 and 12 points);
  - smaller m: COMPUTED.
- (D) COMPUTED on abstract signotopes, not realised:
  - 2 points do not suffice under the boundary premises (n = 6, 7, 8);
  - the bound 4 is attained at n = 6, m = 10;
  - 4 points do not suffice at n = 6, m = 11.
- (E) HEURISTIC: uniform-envelope solutions exist in 120/120 pool_hept, 120/120 pool_main and U18; walks made 49,361
  proposals with no failure.

**Verifiers.** 3 of 3 did not refute (confidence 0.82, 0.85, 0.80).
- The n = 6 instances and τ at n = 7, m = 11 were re-certified with independent encoders.
- root4_n7_m12 was replayed through cake_lpr on the author's hash-matched CNF and LRAT by two verifier runs. It was not
  re-encoded independently.
- Verifier 3 did not re-check the first bullet of (D).

**What counts.** (A)-(E) at the labels above, with these repairs:
- (B) reads "sharp at n = 7, one witness". The hypothesis "no (n−2)-cup" of structure Theorem 2 cannot be weakened to
  "no (n−1)-cup" at n = 7.
- The strategy consequence reads as in P1, including the admissible-insertion caveat.
- 2n − 2 is "the first size not covered by the written rooted proof", not an "open" size.

**Open.** The n = 8 cases of (C) were never finished: the τ run was stopped and the rooted m = 14 CNF never solved.
Weak D(5,7) and weak D(5,8) are not touched.

**Files.**
- Author's return: `/home/jay/research/data/roadmap-20261115/agent_results_extra.jsonl`, label `delta:attack:1`.
- Certificates: SP`/d1/cert/` (root4_n7_m12 and tau4_n7_m11 .cnf, .lrat.zst, .cake.out).
- Abstract models: SP`/d1/models.json`.
- Verifier replays: SP`/vfy_s1inv_l3/root4_n7_m12.cake.out`, SP`/s1inv_L1/root4_n7_m12.recake.out`.
- The verifier returns exist only in the workflow relay to this write-up.

## 2. Attack 2: minimal counterexample at the x-extremes

**Strategy.** A minimal counterexample forces structure at r and at l. Turn the rightmost deletion into the
r-independent statement CONJ-TS′, and test the known terminal-safe failures against the 4-cap hypothesis, by exact
enumeration of every rightward extension cell.

**Outcome (author).**
- (A) CONJ-TS′(n) ⟹ weak D(5,n), PROVED (P2).
- (B) Forced structure F1-F6.
- (C) S19 = U18 plus a top point r is valid; U18 has no terminal-safe weak Δ; r ends no 4-cap. So the 4-cap hypothesis
  cannot be dropped.
- (D) CONJ-TS′ holds for |S| ≤ 2n − 2 (n = 6, 7, 8).
- (E) COMPUTED: 124 of 1,090 candidate sets lack a terminal-safe weak Δ. None of them has a valid extension in which r
  ends a 4-cap. In the 65 that are extendable, the only valid cell is the top cell.

**Verifiers.** 2 did not refute (0.93, 0.88); 1 refuted (0.70).
- The refutation was explicitly "default rule, not a math error". Unconfirmed in that run:
  1. the CERTIFIED failure of 27 of the 28 trajectory sets;
  2. (E) beyond U18;
  3. F5's projective normal form;
  4. ETV7SAT's M(5;7) ≤ 36.
- How each was answered:
  - Items 1 and 2: the third verifier certified 28/28 trajectory failures on its own CNFs (cake_lpr "s VERIFIED UNSAT").
    It recomputed the 124/65 counts and 636/236/125/1 cells for U18, and the cell counts were also reproduced by the
    refuting verifier's own vertical sweep.
  - Item 4: answered by the citation. `../../ETV7SAT20261113/data/lad_ns37_N37.cake` contains the exact line once, which
    this agent checked.
  - Item 3: no verifier re-checked it.

**What counts.**
- (A) PROVED. Write "hence", not "equivalently".
- (B): F1 in the repaired form: for every p and every weak Δ′ of S − p there are a 4-cap K and a gon H through p,
  depending on Δ′, with K − p ⊆ Δ′, (H − p) ∩ Δ′ = ∅ and K ∩ H = {p}.
- (B): F2-F4 and F5 without the normal form.
- (B): F6 only for n = 7, 8 (|S| ≥ 16, DELTA2N §4.1). For n ≥ 9 the verifiers disagree (2n − 2 via structure Theorem 4
  against "no bound established"), so no bound is claimed.
- (C) EXACT, by independent integer recomputation.
- (D) PROVED + CERTIFIED, cited from the boundary record and not re-run.
- (E):
  - EXACT for U18;
  - CERTIFIED for the terminal-safe failure of the 28 trajectory sets;
  - COMPUTED for the rest;
  - pool statistics HEURISTIC.

**Open / unverified.**
- CONJ-TS′ itself.
- F5's projective normal form (cited from structure §7).
- The abscissa-envelope variant of the corollary.

**Files.**
- Author's return: `agent_results_extra.jsonl`, `delta:attack:2`. Verifier 1's return: `delta:verify:2:1`.
- S19: SP`/mc/S19.json`. Cell enumerator: SP`/mc/cells.py`. Certificates: SP`/mc/cert/`.
- U18: `../resume/selection/terminal/data/witness.json`.

## 3. Attack 3: cap/cup duality

**Strategy.** Compare the cup-side and cap-side sharpenings of weak D(5,n) under the reflections ρ and χ, the projective
charts that fix the vertical direction, and rotations. Analyse what the certified cup-side D(5,6) counterexample S15
obstructs, using exact cores, relaxations and its direction family.

**Outcome (author).**
- (1) PROVED: the maps fix each form, and none relates cup-side to cap-side on (5,n)-valid sets. Lemma SD.
- (2) CERTIFIED zero counts:
  - S15 has 0 cup-side and 87 cap-side Δ;
  - cap11 and cap13 have 0 cap-side Δ but 684 and 5,746 cup-side Δ.
- (3) The chain-length lemma.
- (4) Every unsatisfiable core of S15's cup-side system uses a (4,3)-pentagon cup clause. A CERTIFIED 55-clause core.
- (5) Direction scans: 4,256 valid cells with no cup-side failure. HEURISTIC.

**Verifiers.** 3 of 3 did not refute (0.78, 0.86, 0.86).

**What counts.** (1)-(5) at the labels above, with these repairs:
- The sentence "cap/cup duality cannot prove weak D(5,7)/D(5,8)" is an informal summary limited to ρ, χ, the
  vertical-fixing charts φ_c and rotations. It is HEURISTIC, not a proved impossibility.
- The pool total is 420, not 450 (1 + 89 + 91 + 90 + 89 + 7 + 53).
- Lemma SD needs no n-gon hypothesis, and its corollary holds for every n ≥ 6.
- "All 14 intermediate charts invalid" is specific to S15: a verifier found random (5,7)- and (5,8)-valid sets with valid
  intermediate charts.
- Positive counts are COMPUTED with explicit witnesses; one verifier re-enumerated all 2^15 subsets.

**Open.**
- Cup-side D(5,7) and D(5,8), which equal L(5,n) for n ≥ 7.
- L(5,6) for all signotopes.

**Files.**
- Author's return: `agent_results_extra.jsonl`, the DUALITY3 label. Verifier returns: `delta:verify:3:2` and `3:3`.
- SP`/dual/`, with `cert2/*.cake.out`: four logs, each with the exact line.
- S15: `../coordinator/data/cup15/realized.json`.

## 4. Attack 4: layer decomposition (unions of 4-cap-free pieces)

**Strategy.** Partition a valid set by vectors I of the invariants λ, ρ (4-cap peeling depths), c−, c+ (cap lengths) and
β, ω (cup lengths), and ask whether some union of I-classes is a weak Δ. Each failure was deletion-minimised and
re-checked by an independent brute-force program and by cake_lpr.

**Outcome (author).**
- (A) PROVED: pieces are 4-cap-free when I contains λ, ρ, β or ω.
- (B) CERTIFIED and EXACT: explicit real sets defeat every I contained in the listed vectors, at n = 7 and n = 8. Each
  obstruction set still has a weak Δ.
- (C) CERTIFIED: no pointwise 6-tuple rule works.
- (D) COMPUTED: the near-discrete vectors never failed.

**Verifiers.** 3 of 3 did not refute (0.82, 0.90, 0.90).

**What counts.** (A)-(D), with the headline narrowed:
- (β,ω) is obstructed at n = 7 only. At n = 8 it is not obstructed (0/334 failures).
- Also not obstructed at n = 8:
  - (λ,c−,β), (λ,c+,ω), (ρ,c−,β), (ρ,c+,ω), which were untested;
  - (c−,c+,β) and (c−,c+,ω).
- (C): both universal CNFs (n = 7 and n = 8) were regenerated independently and matched (EQUAL). This answers the
  author's gap "n = 8 encoding from one implementation".
- The median in (D) reads 0.55-0.91 classes per point.

**Open.** The finer vectors in (D) are tested only, and non-pointwise choices of the union were not studied.

**Files.**
- Author's return: `delta:attack:4`.
- SP`/lay/`: 30 of 30 `*.cake.log` contain the exact line; `SHA256SUMS` has 136 entries; for example
  `min_LR_n7.json` and `univmin_F_n8.cnf`.

## 5. Attack 5: hitting sets and LP duality

**Strategy.** Write down the basic LP and the strongest decoupled relaxation FC, and derive FC's dual. Compute exact FC
values on the known counterexamples to the sharpened forms. Test the rank-monotone (β-antitone, ω-isotone) families.

**Outcome (author).**
- (A), (B) PROVED (P4).
- (C) COMPUTED exact integrality gaps:
  - cup15 cup-side t* = 62/57;
  - a deletion-minimal 54-clause core with t* = 6/5;
  - e13 ends-restricted value 1.
- (D) The lemma is PROVED. No β-antitone plus ω-isotone pair covers all gons in:
  - a5n6 #6, 10, 49, 58, 64;
  - strong15;
  - pool_hept #1, 7, 12, 24, 28, 29, 31.
- (E) α_4(ETV42) = 22 and α_4(ETV26) = 16.

**Verifiers.** 3 of 3 did not refute (0.90, 0.90, 0.93).

**What counts.** (A)-(E), with these upgrades and precisions from the verifiers:
- (D) is now CERTIFIED by cake_lpr on independently generated CNFs (verifier 3).
  - Brute force confirms pool_a5n6 #6 and pool_hept #1 and #7.
  - strong15 is confirmed by 13 cake_lpr-accepted pair CNFs.
  - No n = 8 obstruction is known.
- (E) holds exactly from the witnesses plus Baek's bound (a 4-cap-free subset is 8-gon-free, so it has at most 22
  points).
- Write "the weakest statement *in this chain* that yields the bounds: T(n)".
- strong15, strong form: the author established only t* ≤ 1. One verifier reports the exact value 1 (primal = dual).
- These gaps concern the false strengthenings, not weak D itself.

**Files.**
- Author's return: `delta:attack:5`. Verifier returns: `delta:verify:5:1` to `5:3`.
- SP`/lp5/`, for example `cup15_cup.json`. Verifier folder: SP`/vfy_lens2/`.

## 6. Attack 6: rank-defined candidates Δ ⊆ Δ_R ∪ Δ_L

**Strategy.** Use R(a,n): Δ must lie inside A = {c− + β ≥ n+1} ∪ {c+ + ω ≥ n+1} (ETVTHY20261113 §3.2). Test it on
real sets and universal CNFs, and prove structural lemmas.

**Outcome (author).**
- R(4,7) is false for the 13-element signotope σ13. Evidence: a CERTIFIED fixed-instance CNF and a hand proof from a
  20-clause core.
- R(4,7) is CERTIFIED for m ≤ 12, so 13 is the least size.
- L1-L4 are PROVED.
- R(5,7) and R(5,8) are open.

**Verifiers.** 1 did not refute (0.86); 2 refuted (0.85, 0.90).
- Both refutations name the same step and found no math error. The CNFs and LRATs for m = 6..12 (SHA prefixes
  d18ef14b…6dc35e9e) and the m = 13 CNF could not be found, so CERTIFIED for m ≤ 12, and with it minimality, cannot be
  confirmed.
- The non-refuting verifier re-ran the universal CNFs: m = 12 CERTIFIED, m = 6..11 COMPUTED. This is a partial answer.
- EXACT control: all 13 twelve-point subsignotopes of σ13 satisfy R(4,7).

**What counts.**
- σ13 facts, EXACT by independent recomputation:
  - 98 three-caps and 63 convex hexagons;
  - A = {0,1,2,3,8,9,10,11,12};
  - 215 working 3-cap-free sets, none inside A.
- The hand proof was checked against σ13.
- The fixed-instance obstruction is CERTIFIED, also by a verifier's own CNF (SHA-256 ffc4ebce…a327, LRAT
  7fada145…8377).
- So R(4,7) is false for abstract signotopes, while D(4,7) is CERTIFIED (DELTA2N §4.1).
- L1-L4 are PROVED. One correction to the remark in L3: E ∪ {r} lies inside A when r lies on a gon; otherwise E alone
  works inside A.

**Refuted / downgraded.**
- "R(4,7) CERTIFIED for m ≤ 12, 13 is least" becomes:
  - m = 6..11 COMPUTED;
  - m = 12 CERTIFIED by a verifier's re-run;
  - least size 13 COMPUTED.
- The author's certificates are unavailable.

**Open.** Realisability of σ13; R(5,7) and R(5,8). The a = 5 evidence (703 sets, walks) is COMPUTED/HEURISTIC and was not
re-run.

**Files.**
- Author's return: `delta:attack:6`.
- SP`/rank/`, SP`/cert/` (fixed13.*). Verifier folder: SP`/r47verify_lens2/`.

## 7. Attack 7: finite reduction plus certified computation

**Strategy.** Bound vertex-critical counterexamples by the certified frontier and extremal numbers. Compare that window
with SAT reach, and add a sound vertex-criticality layer to the CNF.

**Outcome (author).**
- (A) The window lemma (P6).
- (B) The headline "OBSTRUCTION":
  - (i) certifying the window would also give M(5;7) ≤ 31 (M(5;8) ≤ 58);
  - (ii) cup15, E4 and E1 are vertex-critical counterexamples of the maximum valid size (15, 15, 16) for related forms;
  - (iii) SAT reach ends near m = 16-17; the VC layer changes only constant factors.
- Conclusion: "cannot prove or refute".

**Verifiers.** 1 did not refute (0.80); 2 refuted (0.80, 0.75).
- "Cannot refute" is unsupported. One SAT model at m = 16-17 would refute the conjecture. The author's own extrapolation
  puts (5,7) m = 16 at about 11 h and (5,8) m = 16 at about 2.7 h (242.3 s × 40). Cup-side n6 m15 was refuted this way
  (DELTA3N README).
- "Cannot prove" rests only on a HEURISTIC fit over 3-4 sizes.
- The step from (ii) is a non sequitur. Examples of at most 16 points at n = 6 do not exclude a generic bound near 17 at
  n = 7. Also, Lemma 2(b) is itself a generic bound.

**What counts.**
- (A) PROVED, from the CERTIFIED frontier (no counterexample with ≤ 15 points), base(4,7,17), base(5,6,16), M(5;7) ≤ 36
  and Baek's M(4;8) = 22.
- (B)(i) is a PROVED implication.
- (B)(ii) is COMPUTED exact and reproduced independently. It refutes only the generic principle. All three examples
  violate the weak-form Lemma 4 (DELTA2N §6), so they do not obstruct arguments that use it.
- (B)(iii) HEURISTIC: an obstruction to *proving* weak D(5,7) or D(5,8) with these encoders alone. Refutation remains
  within estimated reach if a counterexample with about 16-17 points exists.

**Refuted.** The headline sentences listed in §0.2.

**Files.**
- Author's return: `delta:attack:7`. Verifier returns: `delta:verify:7:1` to `7:3`.
- SP`/s7/`: `vc_cnf.py`, `window.py`.

## 8. Attack 8: counterexample hunting for weak D(5,7) at m ≥ 16

**Strategy.** Simulated annealing on real coordinates, with an exact C++ engine (hunt.cpp), under two objectives: the
weak-Δ count W and the price minΔ − τ. A one-point extension scan. An independent Python re-check and cake_lpr.

**Outcome (author).**
- (1) Two explicit 18-point valid sets, A and B (coordinates in SP`/hunt8/price2.txt` and `price2b.txt`). In each:
  - τ = 4, attained only by a 4-cap: A {9,10,11,13}, B {3,5,6,8};
  - every 5-point transversal contains a 4-cap;
  - minΔ = 6, with 47 and 46 such sets;
  - W = 3,254 and 1,304.
  So weak D(5,7) holds for both, but the price is 2. "No 4-cap-free transversal with ≤ 5 points" is CERTIFIED.
- (2) Near-misses with W = 456 (16 points) and W = 433 (17 points). COMPUTED, but each has τ = 3 and so is far from a
  counterexample.
- (3) HEURISTIC: 2,056,697 proposals with no W = 0.

**Verifiers.** 3 of 3 did not refute (0.93 each).
- Exact recomputation by independent programs.
- A fresh cake_lpr re-run of both certificates.
- Independent 18-variable CNFs, also "s VERIFIED UNSAT": SHA-256 8f12f8e3… (A) and fca5046b… (B).
- τ ≥ 4 certified for both sets.

**What counts.** (1)-(3) as stated. This refutes "minΔ ≤ τ + 1" at n = 7 with 18 points. It is the whole-hexagon
analogue of minimum16 (lower chains, price 1); no earlier real example was found in the records.
- Corrections:
  - the random-hypergraph estimate for A is about 1.2 × 10⁻⁵, not 10⁻⁴;
  - the amplification condition reads: for each k in K, every X ⊆ S − {k} that meets the hexagons H with H ∩ K = {k}
    gives a 4-cap in (K − {k}) ∪ X.
- This attack ran after README.md was written; it supersedes README's "failed on the usage limit; no result".

**Files.**
- Author's return: workflow relay only.
- SP`/hunt8/` (cert/ with price2_k5 and price2b_k5 .cnf, .lrat.zst, .cake.out).
- Verifier folder: SP`/vprice2_lens3/` (`orig/*.recheck.out`).

## 9. Process notes the agents reported

These are the agents' own statements; this agent did not audit them.
- **Attack 1:**
  - pysat solves of up to about 50 s ran outside systemd units;
  - for about 2 minutes, three solvers ran outside units;
  - about 17.3 threads were in use for under a minute;
  - memguard stopped unit esr-agx-x-cert7 at its 1 GB limit, which was not an OOM kill.
- **Attack 3:** certify_cnf.sh failed to allocate under a 1.5 GB address-space cap, so certification was redone with an
  explicit heap and stack. The failed logs in SP`/dual/cert/` are not rejections.
- **Attack 5:** the n = 8 staircase run was stopped after 5 sets because the 16-thread cap was over-subscribed.
- **Attack 8:**
  - it started at 04:52, after its 04:20 stage deadline, and read the relayed "no, i reset." as a restart;
  - about 7.1 CPU-minutes ran in foreground runs outside units, at times one thread over the cap;
  - BLAS threads ran for about 1 s.
- No agent reports a repo write, a git action or a touched foreign unit.

## 10. Durability and own checks

- **SP** is `/tmp/claude-1000/-home-jay-research-lean-erdos-szekeres-lean/1e71bc06-5c09-4f54-ae48-3fca76aaa352/scratchpad`.
  It is RAM-backed, cleared at reboot, and **not durable**.
  - **16 Nov 00:55 KST (main session):** all of SP was copied, with the same relative paths, to
    `/home/jay/research/data/roadmap-20261115/scratchpad-snapshot-20261116/`. The copy was checked against
    `scratchpad-snapshot-20261116.MANIFEST.cksum`. Use that copy.
- Every certificate and script named above exists only there. House rule (SKILL.md §2): keep the proofs, zstd, until an
  independent re-run. The main session must copy them into this record before reuse. This agent was allowed to write only
  this file.
- Own checks, a grep for the exact line `s VERIFIED UNSAT`:
  - one match in each of SP`/d1/cert/root4_n7_m12.cake.out`, SP`/d1/cert/tau4_n7_m11.cake.out`,
    SP`/vfy_s1inv_l3/root4_n7_m12.cake.out` and SP`/s1inv_L1/root4_n7_m12.recake.out`;
  - one match in each of SP`/vprice2_lens3/orig/price2_k5.recheck.out` and `price2b_k5.recheck.out`;
  - one match in each of the four SP`/dual/cert2/*.cake.out`;
  - 30 of 30 SP`/lay/*.cake.log`;
  - `../../ETV7SAT20261113/data/lad_ns37_N37.cake`.
- The verifier returns for attacks 1, 4, 6 and 8, and for verifications 2:2, 2:3 and 3:1, are not in
  `agent_results_extra.jsonl`. They exist only in the workflow relay to this agent. Folder names such as SP`/vfy_*`,
  SP`/vts/`, SP`/vlay3/` and SP`/r47/` suggest their working files, but that mapping is by name only.
- **Not reconciled:** ROADMAP20261115 §2 says weak D(5,8) "would give M(5;8) ≤ 63". Attacks 5 and 7 derive ≤ 58 from
  Baek's 22 plus the CERTIFIED M(5;7) ≤ 36 (ETV7SAT20261113 README item 2).
