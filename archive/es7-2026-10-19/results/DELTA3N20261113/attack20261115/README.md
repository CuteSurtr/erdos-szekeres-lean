# Δ-reduction conjecture: eight-strategy attack (15 November 2026, 02:52-04:40 KST)

**Weak D(5,7) and weak D(5,8) remain OPEN. No proof and no counterexample was found.** Seven of the eight strategies
returned: two claimed lemmas (reductions and structure) and five obstructions that explain why a strategy cannot close
the conjecture as posed. The planned adversarial verification (three verifiers per claim) was cut short by the account's
weekly usage limit: only 9 of 21 verifications ran. No verifier refuted a lemma; two of three verifiers found that attack 7
overstates its headline. Every claim below is stated at the author agent's own label and is **not independently verified**
unless the table says so.

Source: workflow `es-overnight-extra` (run `wf_2deae7c5-405`), agents `delta:attack:1..8` and `delta:verify:*`. Their full
returns (statement, complete argument, checks run, gaps, files) are kept verbatim in
`/home/jay/research/data/roadmap-20261115/agent_results_extra.jsonl`; their own scripts and certificates are in the session
scratchpad (folders such as `rank/`, `lay/`, `sides.py`, `core15.py`, `rulecnf.py`, `certify_hit.py`), which is **not
durable** and must be copied before reuse. This file was written by the main session because the workflow's write-up step
failed on the same usage limit. Targets and definitions: ETVTHY20261113 §3, DELTA2N20261113, DELTA3N20261113 (and its
`resume/`, `selection/`, `boundary/` subrecords).

| # | Strategy | Outcome (author's label) | Verification |
|---|---|---|---|
| 1 | Induction by adding a rightmost point (Baek-style Δ removal) | **Lemma**: on 4-cap-free inputs, uniform-envelope selection (condition (U) of DELTA3N `boundary/envelope/theory.md` §1) is exactly the weak cup-transversal problem D(4,n) (PROVED); terminal-safe selection fails with longest cup n−2 (COMPUTED on a CERTIFIED witness); τ ≤ 3 at 2n−3 and rooted \|Δ\| ≤ 4 at 2n−2 for n = 6, 7 (CERTIFIED) | none ran |
| 2 | Minimal counterexample at the x-extremes | **Lemma**: minimality forces the rightmost point to end a 4-cap, and an r-independent selection statement CONJ-TS′(n) implies weak D(5,n) (PROVED, with forced-structure lemmas); terminal-safe selection fails on 28 trajectory sets including U18 (CERTIFIED, fresh LRAT + cake_lpr); exhaustive extension cells and an S19 sharpness example (COMPUTED) | 1 of 3: not refuted (confidence 0.93) |
| 3 | Cap/cup duality | **Obstruction**: what cap/cup-exchanging maps do to the three forms; the certified cup-side D(5,6) counterexample S15 analysed by exact cores (PROVED lemmas; CERTIFIED fixed-instance cores; COMPUTED scans) | 2 of 3: not refuted (0.86, 0.86) |
| 4 | Layer decomposition (union of 4-cap-free pieces) | **Obstruction**: explicit real sets at n = 7, 8 rule out every coarse cap-peeling, cap-length and cup-layer decomposition, and no pointwise rule exists (CERTIFIED); only near-discrete finest decompositions survive tests (COMPUTED) | none ran |
| 5 | Hitting sets and LP duality | **Obstruction**: reductions WD ⟹ FC ⟹ U ⟹ T and fractional vacuity (PROVED); exact integrality gaps (cup15 t* = 62/57, core 6/5, e13 ends 1; COMPUTED-exact); rank-monotone lemma (PROVED) with staircase failures at n = 6, 7 (COMPUTED) | 3 of 3: not refuted (0.90, 0.93, 0.90) |
| 6 | Rank-defined candidates Δ ⊆ Δ_R ∪ Δ_L | **Obstruction**: rank localisation R(4,7) is FALSE for 13-element signotopes (CERTIFIED fixed instance plus a hand proof) although D(4,7) itself is CERTIFIED true, and R(4,7) holds for m ≤ 12 (CERTIFIED); rank lemmas L1-L4 for a = 5 (PROVED); R(5,7), R(5,8) open; the failure was not realised by real points | none ran |
| 7 | Finite reduction plus certified computation | **Obstruction**: window lemma (PROVED, from CERTIFIED inputs), exact checks (COMPUTED), reach estimate (HEURISTIC) | 3 of 3: one not refuted (0.8); **two refuted the headline** (0.80, 0.75): "the strategy cannot settle weak D(5,7)/D(5,8)" is unsupported for the refutation direction; the window lemma itself was not challenged |
| 8 | Counterexample hunting | failed on the usage limit; no result | — |

## Reading of the outcome (main session)

- The two lemmas give the clearest proof route: attack 2's reduction to the selection statement **CONJ-TS′**, and
  attack 1's identification of uniform-envelope selection with **D(4,n; weak)** on 4-cap-free inputs. The roadmap program
  "rooted 2n−3 theorem to all sizes via a vertex-cover lemma for lower tangents" (ROADMAP20261115) builds on the same
  objects.
- The obstructions close off coarse layer unions (4), rank localisation in its plain form (6), fractional/LP arguments
  alone (5) and naive cap/cup transfer (3). Any proof must use finer structure than these.
- **Before reuse:** copy the scratchpad scripts and certificates into this folder, rerun the CERTIFIED items through
  `certify_cnf.sh`, and run the missing verifications (attacks 1, 4, 6 and the remaining votes for 2 and 3).
- No ES(8) bound changes.

## Later files in this folder (15 Nov, 05:30-05:50 KST)

- `VERIFICATION.md` (workflow write-up after the usage limit was reset): 19 of 24 verifier returns do not refute; no math
  error found in any PROVED part. PROVED and kept: attack 1's Lemma U4 and attack 2's Theorem 3 (CONJ-TS′(n) ⟹ weak D(5,n)).
  Attack 5's chain ends in T(S): the convex (n−1)-gons have a transversal of at most b(n) points; T(8) gives M(5;8) ≤ 58
  (with M(5;7) ≤ 36 as recorded in ETV7SAT20261113), see ROADMAP20261115 §2.
- `ROUND2.md`: **CONJ-TS′(7) CERTIFIED for all valid S with |S| ≤ 14** (eight cake_lpr acceptances, one verifier replayed
  all eight); **S19′ (U18 + abstract r) is an EXACT 19-point signotope counterexample to CONJ-TS′(7)**, realizability open;
  UES*(7) ⟹ weak D(5,7) PROVED; the peel + D(4,n) scheme fails (CERTIFIED). Weak D(5,7), D(5,8) remain OPEN.
- Proof hazard fixed by the main session: `/home/jay/research/data/roadmap-20261115/delta-r2-tsprime7/ts7_m14.lrat.zst` is
  truncated (zstd -t: premature end; left untouched); a new archive `ts7_m14.lrat.zst.ok` (1,680,167,954 bytes, passes
  zstd -t) was made from the intact `ts7_m14.lrat` (5,713,648,952 bytes, SHA-256 in `ts7_m14.lrat.sha256`, prefix
  3a01ae023786…); the uncompressed proof is kept. `delta-r2-attacker/cert14` (4.5 GB) is a partial LRAT, not a proof;
  deleting it is the owner's decision.
- Running at 05:50: the realizability of S19′ (`S19_REALIZABILITY.md` expected by 09:45) and an independent certified
  CONJ-TS′ test at |S| = 13-15 (`CONJTS_TEST.md`); the method sweep (`METHODS_SWEEP.md`).
- `METHODS_SWEEP.md` (06:30): 75 lens agents over about 250 methods. **No verified result** (highest promise 3 < the
  deep-dive gate 7, so no deep dive or verifier ran); about 30 principles refuted or shown vacuous; σ13 (the R(4,7)
  counterexample) reported realizable by two independent integer realizations (each checked exactly by its finder;
  not independently verified). Top directions: ENV#/VE/RT*/ROOT certification at small sizes, the antichain form AT_n,
  weak D(4,8) at 14-22 points — being worked on in round 6 (`ROUND6.md`, expected by 09:40).
- **Pending verification (round 5):** S19′ is reported realizable by real points (EXACT by the finder's own three
  programs). If the independent verifier confirms it, CONJ-TS′(7) is false for real point sets (the reduction CONJ-TS′ ⟹
  weak D(5,7) stays valid but its premise fails), while S19′ itself satisfies weak D, the mirror and the rooted forms.
  [superseded 15 Nov pm: resolved at 06:30, next item]
- **06:30 RESOLVED (`S19_REALIZABILITY.md`): S19′ is realizable by real points (EXACT, independently verified).** Two
  separately found integer realizations (`/home/jay/research/data/roadmap-20261115/s19/realize/s19_real_int_v1.json`,
  |coords| ≤ 2^16; `s19/nonreal/S19prime_realization_int.json`, ≤ 10^5) match all 969 signs; the round-5 verifier confirmed
  with its own Python and C++. **CONJ-TS′(7) is therefore false for real point sets** (19 points); the smallest real
  counterexample has 15-19 points [superseded 15 Nov pm (STATUS20261115_1900, Corrections item 4): 15-17 points, claim
  cts7-real-17, V1 CONFIRMED]. Theorem 3 (CONJ-TS′(n) ⟹ weak D(5,n)) remains valid but its premise fails at n = 7;
  the rooted and per-set left-or-right forms hold on S19′ and are open in general. Weak D(5,7) and D(5,8) stay OPEN.
  Main-session check with its own code (`s19/s19_own_check_mainsession.py`): both sets have 19 points in general position
  with distinct x, longest cap 4, **0 convex 7-gons among all 50,388 7-subsets**, and 11 four-caps ending at the last point
  (the terminal-safe failure itself was not re-checked by the main session).

## Round 6 and the certified CONJ-TS′ test (added by the main session, about 09:04 KST)

- **`ROUND6.md` (08:59)** replaces the line "being worked on in round 6" above. It counts a statement only if its track's
  verifier confirmed it (31 of 33).
  - ENV#(7) CERTIFIED for every valid U with |U| ≤ 13 (two encoders per size; the verifier replayed all 16 proofs and
    regenerated the CNFs byte for byte). ROOT(7) re-CERTIFIED at |S| = 13, 14. ENV# holds (EXACT) on U18, S19′, both real
    S19 and the 302 pool sets. This re-covers only |S| ≤ 14. Open: ENV#(7) at 14-15, ROOT(7) at 15 (UNKNOWN after
    3,417 s) and 16. The ENV#/ROOT verifier wrote no `VERIFY_` file (scripts and logs in `round6/venvroot/`).
  - **AT_n is FALSE for real point sets at n = 6, 7, 8 (EXACT, verifier's own code)**, with integer counterexamples of
    10, 12, 14 = 2n − 2 points, the smallest possible because AT_n is CERTIFIED for |U| ≤ 2n − 3. So LT-cover_6/7/8 of
    design:delta:1 fail as stated, and that program's route to weak D(5,8) (ROADMAP §2) loses its key lemma. The repair
    AT2_n is CERTIFIED for |U| ≤ 12 (n = 6) and ≤ 13 (n = 7) but FALSE for a real 13-point set at n = 6 (EXACT); AT3_n
    fails on real pool prefixes (EXACT).
  - Weak D(4,8) CERTIFIED for every signotope, hence every point set, with ≤ 15 points (14 and 15 new). At 16 points
    cake_lpr accepted a **trimmed** copy of CaDiCaL's LRAT (verifier re-ran it); whether that meets the house wording of
    CERTIFIED is the owner's call (superseded at 09:22 below: the untrimmed proof is accepted). Open: 17-22 points.
  - Not counted: the 49,575-prefix pool claim (partly confirmed) and the m = 17 cost estimate (LRAT about 120-150 GB).
  - ROUND6 §4 lists corrections to METHODS_SWEEP, SYNTHESIS §2.2, design:delta:1, ROUND2 Task 4 and the agents' own
    READMEs; those files were left unchanged, so read them together with ROUND6 §4.
- **Certified CONJ-TS′ test (round-4 workflow, author `/home/jay/research/data/roadmap-20261115/conjts/`, verifier
  `conjts-verify/`, verdict sound; record [CONJTS_TEST.md](CONJTS_TEST.md), written 09:42).** CONJ-TS′ holds on every abstract
  signotope at n = 7 with |S| = 13, 14 (already CERTIFIED in ROUND2, now by two further encodings) and **at n = 8 with
  |S| = 15 (new)**: CERTIFIED by two encodings each, and the verifier re-ran cake_lpr on all six (exact line). Its own
  lemma-free encoder certified n = 7 at 13 and n = 8 at 14. Caveat from the verifier: the second encoding is independent
  code but uses the same two written lemmas (Lemma A, Lemma B), which it checked and found correct. n = 7 at |S| = 15 is
  UNKNOWN (8,359 s, no verdict; the 22.9 GB partial `conjts/runs/n7_m15/cts_n7_m15.lrat` is not a proof, and deleting it
  is the owner's decision). Side result: **CONJ-TS′(6) is false for abstract signotopes at |S| = 13** (three models
  checked exactly by the verifier's brute force; 7-12 CERTIFIED, so 13 is the least failing size; realizability: see
  the 09:12 bullet below, all three are realizable).
- Weak D(5,7) and weak D(5,8) remain OPEN; no ES bound changes.
- **Main-session check of the AT_n counterexamples (09:08, [VERIFY_ATN_MAIN.md](VERIFY_ATN_MAIN.md)):** own exact code
  confirms all 12 realizations (n = 6, 7, 8) are valid and have no weak Δ through both rightmost points, which refutes AT_n
  via the corollary of ROUND6 track 2 statement 4. One side count differs: d6_12 has 486 weak Δs, below the "494 to 12,176"
  range stated in ROUND6 statement 12 (unresolved; the refutation does not depend on it). [superseded 15 Nov pm:
  resolved; d6_12 has exactly 486, and ROUND6 statement 12 now reads 486-12,176 (D6_12_NOTE.md; claim
  d6-12-correction, V3 CONFIRMED)]
- **σ13 realization checked (09:10, same file):** one of the two integer realizations of σ13 matches all 286 signs, and
  the σ13 facts of VERIFICATION.md §6 recompute exactly from the coordinates. So R(4,7) fails for a real 13-point set
  (A taken from VERIFICATION.md §6).
- **New (09:12, EXACT, main session; not yet checked by a second party [superseded 15 Nov pm: V1 CONFIRMED it, claim
  cts6-real-13, VERIFY_CTS6_REAL.md]): CONJ-TS′(6) is false for real point sets at 13
  points.** The three abstract round-4 models were realized with integer points. The main session's own exact code shows
  each is (5,6)-valid, r ends a 4-cap and U has 0 terminal-safe weak Δs. 13 is the least size (7-12 CERTIFIED). Details:
  [VERIFY_ATN_MAIN.md](VERIFY_ATN_MAIN.md). Weak D(5,6) is not affected.
- **ENV#(7) fixed-set check (09:17, same file):** own code confirms that ENV# holds on S19 (real v1), U18 and d7_13_real.
- **Weak D(4,8) at 16 points is CERTIFIED (09:22, main session; VERIFY_ATN_MAIN.md):** cake_lpr accepted CaDiCaL's own
  untrimmed 12.45 GB LRAT at a 6 GB heap (exact line; CNF and LRAT hashes equal to ROUND6). The trimmed-LRAT question for
  the owner is moot. Weak D(4,8) holds for all sets with at most 16 points; open: 17-22.
- **ROOT(6) CERTIFIED for |S| ≤ 14 (09:30, main session; [ROOT6_MAIN.md](ROOT6_MAIN.md)).** Round 6's ROOT encoder was
  run at n = 6 with a new positive control on the three real 13-point sets (PASS 3/3). Every m = 7..13 is accepted by
  cake_lpr, and m = 14 at 09:29 (480 s + 79 s). For point sets ES(6) = 17, so only sizes 15 and 16 remain (about 1 h and 10 h,
  HEURISTIC). [superseded 15 Nov pm: ROOT(6) is false at 15 (claim root6-real-15) and 16 is vacuous (claim
  root6-m16-vacuous), both CONFIRMED]

## Afternoon of 15 November (13:05-19:00 KST): agent team with independent verifiers

**Weak D(5,7) and weak D(5,8) remain OPEN. No ES bound changes.**

Every new result went through the claims folder `/home/jay/research/data/roadmap-20261115/pm1115/claims/` and got a
verdict from an independent verifier, who used its own code (`VERIFY_*.md` in this folder). The main session also
checked the central results itself and re-ran cake_lpr on every large proof the verifiers' memory budget could not hold
([MAINSESSION_1115PM.md](MAINSESSION_1115PM.md)).

[corrected 15 Nov pm (C1 issue 6): every filed claim got a verdict (45 claims, 45 CONFIRMED verdicts at 18:41; two
with one sentence excepted), but not every new result was filed: the ROOT(6) m = 7-14 certificates, T1's further real
15-point ROOT(6) sets (177 distinct by 18:22), R7's real `div17/real/m17_it3_s1.json` and V2's real 14-point CONJ-TS′(6)
sets rest on their authors' checks only. Not every large proof had a second-party cake_lpr run: T1's base(5,6,16) proof
`t1/base16/cert/valid56_m16.lrat.zst` and the ROOT(6) m = 7-14 proofs were not re-run (only their verdict lines and CNF
regeneration were checked; VERIFY_LRR6.md (c), VERIFY_ROOT6_M16_VACUOUS.md); V1's lemma-free base(5,6,16) LRAT and T1's
LRR(7) m = 15 LRAT have no cake_lpr verdict at all.]

- **One-sided forms refuted for real point sets** (EXACT, integer coordinates, each verified):
  - **ROOT(6)** at 15 points. It is completely decided: CERTIFIED for ≤ 14, false at 15, and ≥ 16 vacuous.
    [ROOT6_MAIN.md](ROOT6_MAIN.md), [ROOT6_M15_REALIZE.md](ROOT6_M15_REALIZE.md).
  - **ROOT(7)** at 17 points ([ROOT7_M17_REALIZE.md](ROOT7_M17_REALIZE.md)).
  - **CONJ-TS′(7)** at 17 points. The previous smallest real counterexample was S19′.
  - **ENV#(6)** at 14-15 points and **ENV#(7)** at 16-17, with the variants VE and (U).
  - **TS±(6)** at 15 points.
  - LP0(7) fails for an abstract 19-point signotope. Every one of the 108 extension models found by that scan is
    non-realizable (BFP certificates), so LP0(7) for real sets is open. [corrected 15 Nov pm (C1 issue 20): none of
    the 108 has an x-sorted realization; 20 have V-free certificates (no realization at all), the other 88 only
    certificates with V (claims lp0-7-realblock-nonreal, lp0-7-scan-all-nonreal, V2 CONFIRMED)]
- **What survives: the rooted two-sided form.**
  - **LR(6) holds for every (5,6)-valid signotope and point set.** It is CERTIFIED at 15 points on two encodings, each
    re-run by cake_lpr; ≤ 14 follows from ROOT(6), and ≥ 16 is vacuous.
  - **TWO-ENV#(6)** holds at every size. [corrected 15 Nov pm (C1 issue 3): in its hypothesised form, r ends a 4-cap
    and l starts one, which is what the certificates cover; weak D needs only this form]
  - On every known counterexample, LR(7) and weak D(5,7) hold.
- **PROVED, with written proofs checked by verifiers:**
  - LR(n) ⟹ weak D(5,n);
  - TS±(n) ⟹ TWO-ENV#(n) ⟹ LR(n);
  - Lemma M (monotonicity and the gluing form of LR) — all four in [THEORY_1115PM.md](THEORY_1115PM.md);
  - the cup lemmas G, G2, A1, E and Q, and Prop. R: C1(n) ∧ C2(n) ⟹ LR(n)
    ([PROOF_LR_ATTEMPT_P1.md](PROOF_LR_ATTEMPT_P1.md));
  - Lemma A ([PROOF_LP0_ATTEMPT_P2.md](PROOF_LP0_ATTEMPT_P2.md));
  - strong form ⟹ CB(n);
  - CB(n) is hereditary, with the counterexample window lemma ([LEDGER_1115PM.md](LEDGER_1115PM.md)).
- **CERTIFIED:**
  - **weak D(5,8) at 16 points**, so it holds for all sets with ≤ 16 points, open from 17;
  - TS±(6) ≤ 14 [corrected 15 Nov pm (C1 issue 3): hypothesised form]; CB(6) ≤ 13; ENV#(6) ≤ 11; H7U(6) at 12;
  - CB(8) ≤ 15 and CB(7) ≤ 13 (cited from DELTA2N) [note 15 Nov pm (as C1 issue 13): CB(8) at 15 rests on DELTA2N's
    record only, a proof deleted and never re-run; CB(7) ≤ 13 and CB(8) ≤ 14 are certified twice (V1's verdict on
    cb78-from-strong)];
  - the 10 known right-hostile 17-point ROOT(7) blocks are left-saturated. [corrected 15 Nov pm (C1 issue 7b): the 10
    tested blocks named in claim leftsat-r7blocks; T1's real m17_it5 and m17_it6 and R7's real div17 m17_it3_s1 were
    not tested]
  - SAT probes and their sizes: [PROBES_1115PM.md](PROBES_1115PM.md).
- **Ledger** ([LEDGER_1115PM.md](LEDGER_1115PM.md)). CB(8) for all sizes 16-58 would give ES(8) ≤ 302 through
  N5 ≤ 57 (arithmetic PROVED, claim `w1-cb-window`, CONFIRMED).
- **The next statement to settle is LR(7)**, for example through P1's conjectures C1(7) and C2(7). LR(7) at 17 points
  ran out of time with no verdict.
- **Superseded lines above:**
  - the d6_12 discrepancy is resolved: ROUND6 statement 12 is now corrected to 486-12,176
    ([D6_12_NOTE.md](D6_12_NOTE.md));
  - "not yet checked by a second party" for the real 13-point CONJ-TS′(6) sets: V1 CONFIRMED them
    ([VERIFY_CTS6_REAL.md](VERIFY_CTS6_REAL.md));
  - "only sizes 15 and 16 remain" for ROOT(6): false at 15, and 16 is vacuous.
