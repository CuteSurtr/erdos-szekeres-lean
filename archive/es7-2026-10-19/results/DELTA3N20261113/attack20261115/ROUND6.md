# Δ-reduction, round 6: ENV#/ROOT, AT_n and weak D(4,8) (15 November 2026, work 06:33-08:55 KST, record 08:59 KST)

## Status (exact)

- **Weak D(5,7) and weak D(5,8) remain OPEN. No ES(7) or ES(8) bound changes.**
- **Track 1, ENV#(7) and ROOT(7).**
  - ENV#(7) is CERTIFIED for every (5,7)-valid U with |U| ≤ 13. Each size 6-13 was certified by two encoders, and |U| ≤ 5
    is trivial. The verifier replayed all 16 proofs and regenerated every CNF byte for byte.
  - ROOT(7) is re-CERTIFIED at |S| = 13 and 14.
  - Both results re-imply only ranges that were already CERTIFIED: weak D(5,7) and ROOT(7) for |S| ≤ 14.
  - ENV# holds on every fixed set tested (EXACT). This includes U18, S19′, both real S19 realizations and all 302
    (5,7)-valid pool sets.
  - Undecided: ENV#(7) at |U| = 14 and 15, and ROOT(7) at |S| = 15 and 16.
- **Track 2, AT_n.**
  - AT_n is **FALSE for real point sets at n = 6, 7 and 8** (EXACT; confirmed by the verifier's own code). The integer
    counterexamples have |U| = 10, 12 and 14 = 2n − 2.
  - That size is the smallest possible: AT_n holds for every real valid U with |U| ≤ 2n − 3 (CERTIFIED; the verifier
    re-ran all 15 proofs).
  - AT_n is the antichain form of LT-cover_n (idea 39). The author's literal LT-cover check agrees on the n = 7
    instance; the verifier did not re-run it. So LT-cover_6, LT-cover_7 and LT-cover_8 of design:delta:1 fail as stated.
    That program's route to weak D(5,8), and through the ledger to ES(8) ≤ 303, loses its key lemma.
  - The repair AT2_n is CERTIFIED for |U| ≤ 12 at n = 6 and for |U| ≤ 13 at n = 7. It is FALSE for a real 13-point set at
    n = 6 (EXACT).
  - The "for every A0" form AT3_n is false on real pool prefixes (EXACT).
- **Track 3, weak D(4,8).**
  - Weak D(4,8) is CERTIFIED for every signotope, and so for every point set, with at most 15 points. 14 and 15 points are
    new.
  - At 16 points, cake_lpr accepted a trimmed copy of CaDiCaL's proof, and the verifier re-ran that check. Whether a
    trimmed proof meets the house wording of CERTIFIED is **the owner's call**. Until the owner rules, 16 points stands
    as "CERTIFIED via a trimmed LRAT".
  - Open: 17-22 points.

**Counting rule.** This record counts a statement only if the track's verifier confirmed it. A statement the verifier
did not confirm, or confirmed only in part, appears in the tables marked "not counted". Labels are the house labels
(PROVED / CERTIFIED / EXACT / COMPUTED / HEURISTIC). Each statement keeps its author's label; where a verifier's own
check supports a different label, the verdict column says so. Nothing is rounded up.

| track | statements | confirmed by the verifier, counted | not counted |
|---|---|---|---|
| 1. ENV#(7) / ROOT(7) | 13 | 13 | 0 |
| 2. AT_n | 12 | 11 | 1 (the 49,575 pool prefixes: not fully confirmed) |
| 3. weak D(4,8) at 14-22 points | 8 | 7 | 1 (the m = 17 cost estimate: the LRAT size is contradicted) |

**Sources.**
- Workflow round 6. Author folders: `/home/jay/research/data/roadmap-20261115/round6/{envroot,atn,d48}/`, each with its
  own README.md (envroot and atn also with a SHA256SUMS).
- Verifier folders: `round6/venvroot/`, `round6/vatn/` (`VERIFY_ATN.md`) and `round6/vd48/` (`VERIFY_D48.md`).
  - The envroot verifier wrote no `VERIFY_` file. Its verdicts reached this stage through the workflow. Its own scripts
    and logs are in `round6/venvroot/`: `replay.sh`, `regen.sh`, `sem_check.py`, `check_fixed.py`, `order_v.py`,
    `pool_v.py`, `n8_v.py` and `vlib.py`, with their `.log` / `replay/` / `regen/` outputs.
- This file was written by the workflow's write-up stage. Its tables of hashes were produced by code
  (`round6/writeup/gen_round6.py`), which:
  - read every hash from the agents' own `certify.jsonl`, `trim.jsonl` and replay records;
  - asserted that every certified proof archive exists;
  - asserted that every author cake_lpr output file contains the exact line `s VERIFIED UNSAT`;
  - asserted that every verifier re-run matches both hashes and has the exact line in the verifier's own output file;
  - computed the SHA-256 of the evidence files in §5.
- The writer ran no solver and no cake_lpr. No git action was taken, and no repository file other than this one was
  written.

Context known before round 6 (not re-checked here):
- CONJ-TS′(7) is CERTIFIED for |S| ≤ 14 (`ROUND2.md`).
- S19′ is a real 19-point counterexample to CONJ-TS′(7), EXACT and independently verified (`S19_REALIZABILITY.md`).
- Weak D(5,7) is CERTIFIED for |S| ≤ 15 (DELTA2N20261113). Weak D(4,7) and weak D(5,6) are CERTIFIED.
- The exact statements of ENV#, VE, RT*, ROOT, AT_n and weak D(4,8) are in `METHODS_SWEEP.md` §3.1-§3.3.

## Definitions used below (METHODS_SWEEP §3.1-§3.3; atn README §2, §10; d48 README §2)

- **Basics.**
  - (a,n)-valid: general position, distinct x, no a-cap and no convex n-gon.
  - Gon: a convex (n−1)-gon.
  - Weak Δ: a 4-cap-free subset that meets every gon.
- **The order ⊑ and ↑P4.**
  - P4(U) is the set of pairs (c,d) that end a 4-cap (a,b,c,d) of U.
  - For i < j < k: (j,k) ⊑ (i,k) ⊑ (i,j) when (i,j,k) is a cup, and (i,j) ⊑ (i,k) ⊑ (j,k) when it is a cap.
  - ↑P4 is the up-closure of P4 under ⊑.
- **ENV#(n):** every valid U has a weak Δ A in which every 3-cap a < b < c has (b,c) ∈ ↑P4(U).
- **ROOT(n):** if S is valid and its rightmost point r ends a 4-cap, then S − r has a weak Δ A with A ∪ {r} 4-cap-free.
- **Uniform.** A ⊆ W is uniform in W if:
  - A is a weak Δ of W;
  - no cap triple (a,b,c) ⊆ A has the line ℓ_bc exposed for W.
  - Exposed: above every 4-cap terminal line of W at some X > max_x W. Every line is exposed if W has no 4-cap.
- **AT_n.** For every valid U with rightmost point u, there are a uniform Δ A0 of U − u and an antichain I of (A0, <)
  that meets every gon H of U − u.
  - a < b iff a, b ∈ A0, x_a < x_b, b ∈ E and (a,b,u) is a cap.
  - E = {b ∈ A0 : h_U(b,u) = 3 and ℓ_bu is exposed for U}.
  - AT#_n is the order-type form, with "(b,c) ∈ ↑P4" in place of "not exposed". AT#_n ⟹ AT_n on real sets.
- **AT2_n:** some uniform A0 of U − u either has such an antichain, or meets every gon of U through u.
  **AT3_n** is the "for every A0" version.
- **Weak D(4,8) at m points:** every m-point set with no 4-cap and no convex octagon has a cup that meets every convex
  heptagon. It is form (ii) of attack 1's Lemma U4. On 4-cap-free inputs it is equivalent to uniform-envelope selection
  (U).

## 1. Track ENV#(7) / ROOT(7) (author `round6/envroot/`, verifier `round6/venvroot/`)

**Model and soundness.** envroot README §2 has written soundness notes for all three encoders:
- `env_cnf.py`:
  - pair variables u, with clauses for u ⊇ P4 and u up-closed under ⊑;
  - explicit 4-cap literals;
  - rows over |A| ≤ m − 5.
- `env2_cnf.py`, the extension form:
  - some 5-cap-free right extension r exists;
  - convex 7-gons through r are allowed;
  - no u variables.
- `root_cnf.py`: a gen.py-style base with the 4-cap hypothesis.

The verifier read each encoder against METHODS_SWEEP §3.1 and re-derived soundness itself. A counterexample with
u = ↑P4 satisfies every clause, and dropping rows keeps the CNF sound.

| # | statement | label | verifier's verdict | counted |
|---|---|---|---|---|
| 1 | **ENV#(7) holds for every (5,7)-valid signotope U with 6 ≤ \|U\| ≤ 13, hence for every valid point set** (encoder 1). \|U\| ≤ 5 is trivial: there is no hexagon, so A = ∅ works. | CERTIFIED | CONFIRMED. The verifier replayed all 8 proofs (env7_m6-m13) with its own FIFO script; each gave the exact line, and both hashes are equal. All 8 CNFs were regenerated byte-identical. Its own black-box semantic control on env7_m9/10/11 used 12 exact real subsets: the forced-violated rows equal its brute-force ENV# solutions (93-587 per sample) in 12/12. | yes |
| 2 | A second encoder (env2_cnf.py, extension form) gives UNSAT for \|U\| = 6..13. | CERTIFIED | CONFIRMED. 8 replays: exact line, hashes equal. The CNFs are identical on regeneration. The ⟹ direction was re-derived: the complement of ↑P4 is a down-set of ⊑, so U + r0 satisfies the axioms and has no 5-cap through r0. Own control with r fixed to its own r0: 12/12. **Caveat:** the same agent wrote both encoders, and they share the base clause pattern. | yes |
| 3 | Positive controls on real valid sets with exact integer coordinates: ENV# m = 9-13: 30/30; env2 m = 9-12: 20/20; ROOT m = 11-13: 18/18. | EXACT | CONFIRMED from the logs (12 PASS lines, no FAIL); the author's scripts were not re-run. The verifier's own separate control passed 32/32 (env m9-11, env2 m9-11, ROOT m11-12). It does not reproduce the m = 12/13 samples. | yes |
| 4 | Semantics of ⊑. On 400 random valid subsets, the r0 cap set derived from the 4-tuple axiom equals the complement of ↑P4 in 400/400. ↑P4 ⊋ P4 in 363, and the reversed order would differ in 392. | EXACT | CONFIRMED with its own code (order_v.py) on the same samples. Also, U + r0 is a 5-cap-free signotope in 400/400. Hand proof: the axiom on (i,j,k,r) holds iff the cap set is a down-set of ⊑. | yes |
| 5 | The explicit 4-cap literals are needed: of the 216,143 four-caps in the 1,123 valid pool sets, 113,191 have (b,c) ∈ ↑P4. | EXACT (count); "needed" is a reasoning claim | CONFIRMED by its own recount. Every one of the 1,123 sets has at least one such 4-cap. | yes |
| 6 | ENV#(7) at \|U\| = 14 and 15 is not decided. The m = 14 run was stopped because time grew from 12 s to 601 s between m = 12 and 13, which projects about 8 h. m = 15 was not run. | HEURISTIC | CONFIRMED. SIGTERM came after 11.06 s and 73,835 conflicts. m = 12 and 13 took 11.87 s and 601.08 s; growth of ×50 projects about 8.3 h. | yes |
| 7 | ENV# has a solution in every task-1 fixed set: the 124 TS-failing sets of expstar.py hard mode (including the 28 trajectory sets and U18), S19′ (abstract), both real S19 realizations and both real S19 − r. Every witness was re-checked by an independent exact path. | EXACT | CONFIRMED with its own code (157 coordinate witnesses plus the abstract S19′). **Correction:** the 124 sets have **18-22** points, not 17-22; 17 is only the minimum over the 1,090 candidates. The TS-failing classification itself is a pysat verdict (COMPUTED) and was not re-checked. | yes |
| 8 | U18 has exactly 4,057 ENV# solutions, 8,149 weak Δs and 0 terminal-safe weak Δs. S19′ as a U has 6,596, 9,601 and 0. S19′ − r has 4,057 rooted sets, the same sets as U18's ENV# solutions. | EXACT | CONFIRMED by its own enumeration of all subsets. U18 has 402 gons and 115 four-caps; S19′ has 424 and 126. The r of S19′ caps 37 pairs, all inside r0's 49. | yes |
| 9 | All 302 (5,7)-valid etvthy pool sets have an ENV# solution. pool_hept #75 (23 points) is the only one without a terminal-safe weak Δ, and its ENV# witness was checked. | EXACT for #75; COMPUTED for the 301 that rest on the finder | CONFIRMED. Its own validity filter over the 984 pool lines gives exactly 302. Its own pysat found a terminal-safe weak Δ for 301 sets, each re-checked exactly, so those 301 are EXACT by the verifier's check. "The only one" rests on an uncertified pysat UNSAT for #75 (COMPUTED). The #75 witness checks exactly (1,930 hexagons). | yes |
| 10 | ROOT(7) holds at \|S\| = 13 and 14 (new direct encoder root_cnf.py). Both sizes were already known from CONJ-TS′(7) plus Fact E. | CERTIFIED | CONFIRMED. 2 replays: exact line, hashes equal. The CNFs are identical on regeneration. The encoder was read against the ROOT statement. Own control on root7_m11/12: 8/8. | yes |
| 11 | ROOT(7) at \|S\| = 15 is undecided: CaDiCaL hit its time limit (3,417 CPU s, 9,610,308 conflicts; projected about 8 h). \|S\| = 16 was not run. | HEURISTIC | CONFIRMED. The log shows 3,416.92 s, no `s` line and exit 0; the regenerated CNF matches the record. No m = 16 files exist. | yes |
| 12 | Extra: ENV#(8) has a checked solution on ETV42 and on all 241 (5,8)-valid pool sets. All 242 also have a terminal-safe weak Δ, so nothing beyond TS is tested. | EXACT (witnesses) | CONFIRMED for the witness part, 242/242, by its own check: no 4-cap, every 3-cap in its own ↑P4, no convex 7-subset of U − A. Not re-checked: (5,8)-validity (only the 5-cap side) and terminal-safe existence (finder only, COMPUTED). r0 maximality was not checked for these sets. | yes |
| 13 | No ES(7) or ES(8) bound changes; weak D(5,7) and D(5,8) remain OPEN. ENV#(7) at \|U\| ≤ 13 re-implies weak D(5,7) and ROOT(7) only for \|S\| ≤ 14, and both were already CERTIFIED. | PROVED (the implication) | CONFIRMED. With Δ = A ∪ {r}, the cap set of a 5-cap-free extension r is a down-set that avoids P4, so it is disjoint from ↑P4. Hence ENV# at \|U\| = m gives weak D(5,7) and ROOT(7) at \|S\| = m + 1. The DELTA2N certificates themselves were not re-verified. | yes |

**Certificates, track 1** (CNFs under `envroot/cnf/`, proofs kept as zstd in `envroot/cert{,2,3}/*.lrat.zst`; LRAT
bytes and SHA-256 are those of the decompressed proof; verifier = `venvroot/replay/replay.jsonl`):

| CNF | vars / clauses | CNF SHA-256 | LRAT bytes | LRAT SHA-256 | author: cake_lpr | verifier |
|---|---|---|---|---|---|---|
| env7_m6 | 86 / 433 | `6afae24de31e71a084f6643e1611abef0ff62729c0f57f2f7e9fa095e68efa99` | 285 | `8a10eae11bf26ffbb539d63138eae2bd874091254dc9cd4778c568d75c1ecc13` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env7_m7 | 168 / 1,031 | `9a86c7f958c23d9cbb8a28488b44520e30590cde207f082920f120b9a576d045` | 986 | `f2f9a5744ce9d8a62e3f7efcd9a2a98d68b2771592d8b2c9054214a12e45321a` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env7_m8 | 308 / 2,243 | `09f9b9fd0eb26e185f59fe974f4d517c2b4cd877dfc635c60ea51a976b51ce6b` | 1,126 | `fec892da0a8697e48c3accebcfe8ff35f63ac85ed273ba58e1285f09296f26c0` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env7_m9 | 540 / 4,576 | `8be1c63436f0bfdbf15a7a3ea44b2785885a81b42b11594b4ae4431445eda73b` | 3,336 | `de02a5dc3e5ca829e12a61c1cd93bbc0fdf332d146c7c7bce1bf53f38542abe9` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env7_m10 | 915 / 8,870 | `da942eb2bb749b0e2c258850b05c75a7df1f402bb0cc5a8d968f9b5a28db472f` | 121,297 | `d45788da3c5a3a12715ed42c29bd4544268866fd46a50c92dbf1423c294c2914` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env7_m11 | 1,507 / 16,468 | `ca3b8e49aad5d3dea2358d4d4318f3cc6589ea8ee38b5f73172d57be3593b9d7` | 4,013,705 | `a4b56509809571c073412ade01e95998b057e11066741ea7a88bc19772e3262d` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env7_m12 | 2,420 / 29,471 | `0ec207e7504bcc3303235b2fda1cb07c99358f3b4cbed7d6c0b7b0738ed2c532` | 129,037,948 | `52d12a8bc6b66af5ebe7d2450f648bb4741dcf3fc60f89436016dd59513ba856` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env7_m13 | 3,796 / 51,143 | `14fe03381ba4d32007c2fa810cc317c20b741e19297c26a24b718a29ffa9188d` | 3,645,938,452 | `3f7247bd11ecdb99d4534f86d99e1a95934930c1b8eee2004a97f1ed06444df2` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env2_7_m6 | 86 / 513 | `df85783cb38c88fe441cfda6d6f37a7dd8bcbde79ca434eb34f0dd9108859177` | 285 | `7e7631e4b1ec4601f74a410186d4c3313a55852792ba11986c405ddbeddf3f8a` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env2_7_m7 | 168 / 1,171 | `c86919d0d648b49d470d6177047a268b6303ad336b4806889fe32bf270cc20d8` | 989 | `e3a48647dc9a0695b496eb9b5534e461fc86169ba9da2a1356bfdf1b56a313f0` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env2_7_m8 | 308 / 2,467 | `1665d667e9d17972870b472a910883f92bc5d4de53124c4a3ed9739d72b03dd9` | 1,134 | `d07580477068b0c842f52fa0b0aac11b6805c056f17e08ac70f1834a57fcc97e` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env2_7_m9 | 540 / 4,912 | `fd7e8ae53802fad3fb5d864e3e28c8bd0d918e379fee0a034853eca3e61c0ce3` | 4,790 | `73d7354a26b7c6e16d998317ddaf6837be61f12b711b05a6c2a8bd1dc9c18e0e` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env2_7_m10 | 915 / 9,350 | `9373bd32ff7ad84062c89e03cef04c0f4dfa848cf4149008d10e50bebc813e21` | 105,817 | `deb1069d443d0f0798191b32abef5500b945d6fcab2e310666d4082076a963b1` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env2_7_m11 | 1,507 / 17,128 | `7a8a1a3adddd44397cebfd9d118024bfeee1ced40be5c3457069b96ac87d6a41` | 3,825,046 | `343050178719dbfdbaaed877ecf9c8ec64b24c5bdce90689736792e8cdf83212` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env2_7_m12 | 2,420 / 30,351 | `6315ee214ba90ec2d47de4296b5074db86c3aeaad37e481f25cf5df169423e4e` | 103,758,589 | `5f9d5968677f6f788e64eb6d45b27f2b3a5024903ff046be3371087309d1e82f` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| env2_7_m13 | 3,796 / 52,287 | `7dbab6ef833d872cb6454b5ff3bbbf98417777d33310566f7f0645aee983ea43` | 3,819,593,912 | `3acd6007cbf144cee92c4edb04bce73e1804e2d4d39953b80eabe70f6cf2cbda` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| root7_m13 | 2,640 / 33,036 | `bd3ff096a6627e2ae62ebb05e7b6915b098e736e894051450a68d25eca83e420` | 116,548,792 | `dc4dec89b7b1d81bfc6927886f2c6a4692af09bccd7bf6f3d1c816dbb6e9bb60` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| root7_m14 | 4,082 / 56,292 | `4f41bb614b4b86d02f1209a6fbd14721e972ba5971ce73256b0d39307065126d` | 3,546,584,045 | `5722845357b501b75bce81c7900ff1e4964071e39623b622815ccadb363272db` | `s VERIFIED UNSAT` | replayed: exact line, CNF and LRAT hashes equal |
| root7_m15 | 6,188 / 93,967 | `063a839427c1ef3280f340ace269d6500745af33ff108e5a796d6206d09dccaf` | – | – | no verdict: CaDiCaL time limit (3426 s wall) | CNF regenerated, identical (regen.txt); no proof exists |
| env7_m14 | 5,824 / 86,595 | `8ce3b22d964b98a731911bc82ec0c6662df00623815d6249401f37bf0e452bb3` | – | – | no verdict: stopped after 11 s (projected about 8 h); partial LRAT deleted | not applicable |

**Not done or deleted.**
- The partial LRATs of the stopped env7_m14 run and the timed-out root7_m15 run were deleted by their author. They were
  that agent's own non-proof outputs; no proof was deleted.
- The verifier deleted nothing: it streamed every proof through a FIFO.

**What remains open (track 1).**
- **ENV#(7) at |U| = 14 and 15.** m = 14 is projected at about 8 CPU-h (HEURISTIC). |U| = 15 is the first size that
  would extend weak D(5,7), to |S| = 16.
- **ROOT(7) at |S| = 15 and 16.** 15 is UNKNOWN after 3,417 s and 9.6 M conflicts; 16 was not run. ROOT(7) at 16,
  together with the CERTIFIED weak D(5,7) for |S| ≤ 15, would give weak D(5,7) at 16.
- **ENV#(8)** is untested beyond TS: no (5,8)-valid fixed set without a terminal-safe weak Δ is known.
- **Process gap.** Both ENV# encoders come from one author. The independent part is the verifier's own semantic
  controls, its replays and its regeneration. A `VERIFY_` file in house format was not written for this track.

## 2. Track AT_n (author `round6/atn/`, verifier `round6/vatn/VERIFY_ATN.md`)

**Model and soundness.**
- atn README §2 proves the equivalent form of AT_n (statement 4). README §4 and §10 give the soundness notes for
  `atsharp_cnf.py` (AT#_n) and `at2_cnf.py` (AT2#_n).
- The verifier reviewed both encoders clause by clause:
  - the signotope axiom and no 5-cap;
  - the 4-set convexity criterion;
  - the closure directions, checked geometrically;
  - the B3/B2/Y semantics;
  - the exact row restrictions |I| ≤ |W| − (n−2) and |W| − (n−3).
- It confirmed the soundness direction: a real counterexample satisfies the CNF.
- Its own fixed-sign controls on 48 instances (8 SAT, 40 UNSAT) agree with its own evaluator.

| # | statement | label | verifier's verdict | counted |
|---|---|---|---|---|
| 1 | **AT_7 is false for real point sets.** S = (−539,−715) (−440,−548) (−303,−298) (−140,−142) (−139,−258) (−130,−109) (−105,−216) (−71,−140) (−43,30) (53,215) (193,500) (497,1187) (539,−104) is (5,7)-valid. At U = S − r (12 points, u = (497,1187)), no I ⊆ U − u is uniform in U − u with I + u uniform in U. Equivalently, for none of the 232 uniform Δs A0 of U − u does an antichain meet all hexagon traces. | EXACT | CONFIRMED by its own exhaustive exact code (vcheck.py). S has 0 five-caps and 0 convex 7-gons, 65 four-caps and 32 hexagons. U − u and U each have 232 uniform Δs, 0 containing u; E = {5,8,9,10}. S has 2,535 weak Δs, 0 through both u and r. The fixed CNF was rebuilt from the coordinates (89 clauses, equal), and cake_lpr re-accepted it. All 286 signs equal the abstract d7_13. | yes |
| 2 | **AT_8 is false for real point sets.** S8 = (−3177,1077) (−1790,771) (−1235,722) (−310,117) (−309,−676) (−275,−653) (−113,−488) (−35,−397) (3,166) (38,157) (167,157) (294,165) (505,249) (2437,1048) (3177,−6364) is (5,8)-valid. AT_8 fails at U = S8 − r (14 points): U has 600 uniform Δs, none containing u. | EXACT | CONFIRMED by its own exhaustive check. S8 has 114 four-caps, 30 convex 7-gons and no 8-gon. AT_8 fails in both forms; E = {5..12}. S8 has 12,176 weak Δs, 0 through u and r. The fixed CNF was rebuilt (141 clauses, equal) and re-accepted. All 455 signs equal d8_15.json. How the set was found (dr_cnf.py) was not checked. | yes |
| 3 | **AT_6 is false for real sets.** All 10 distinct abstract doubly-rooted failures of the DR-REAL probe (d6_11, d6_12 and 8 distinct m11_*) are realizable. Each refutes AT_6 at U = S − r (\|U\| = 10, or 11 for d6_12). | EXACT | CONFIRMED by its own exhaustive check of all 10 files: valid, AT_6 fails in both forms, 0 doubly-rooted weak Δs. The sign strings reproduce the probe exactly. The 12 m11 files fall into exactly 8 classes, and one realization was made per class. | yes |
| 4 | Lemma: AT_n(U,u) ⟺ some I ⊆ U − u is uniform in U − u with I + u uniform in U. Corollary: AT_n(S − r, u) implies that S has a weak Δ containing both of its rightmost points. | PROVED | CONFIRMED: both directions and the corollary were re-derived. The direct and equivalent forms agree on all 63 instances evaluated. | yes |
| 5 | **Thresholds:** AT_6 holds for real \|U\| ≤ 9, AT_7 for \|U\| ≤ 11 and AT_8 for \|U\| ≤ 13. So the smallest real counterexamples have exactly 2n − 2 = 10, 12 and 14 points. | CERTIFIED, via AT#_n ⟹ AT_n | CONFIRMED. cake_lpr was re-run on all 15 AT# proofs, including the 2.4 GB n8/m13 proof (77 s). The CNFs are byte-identical to fresh atsharp_cnf.py output. | yes |
| 6 | AT_n holds on every prefix of every real pool set, with 0 failures in 49,575 instances (n = 6, 7, 8, including the 124 and 28 sets, mirrors and 321 extra sets). | EXACT per instance; HEURISTIC as evidence for the general statement | **NOT FULLY CONFIRMED.** The counts are exact (1,844 + 32,962 + 10,209 + 4,560), with 0 recorded failures, and 440 random witnesses re-checked valid. The other ~49,100 witnesses were not re-checked, nor was membership of the 124 and the 28 sets. At n = 8 only 81 mirror sets are done. No discrepancy was found. | **no** |
| 7 | AT#_n is strictly stronger than AT_n on real sets: AT#_n fails on pool_a5n6[64] at prefix 13 and on two realizations of cup15_uniform (n = 7, k = 15), where AT_n holds. | COMPUTED | CONFIRMED by its own exhaustive exact evaluator. pool_a5n6[64][:13] has 0 AT# and 18 AT solutions; the cup15_uniform pair has 0 and 66; an extra instance, seed2_b, has 0 and 2. The verifier states that this supports EXACT. | yes |
| 8 | Round 2's UES* look-ahead (ROUND2 Task 4, listed OPEN) fails on d7_13_real at prefix 12. | COMPUTED | CONFIRMED. lookahead.py, run unchanged, prints `FAIL set 0 prefix 12 pairs 11`. The forcing argument (ROUND2 Lemma B, heredity H, Corollary C, plus its own count of 0 weak Δs through u and r) is valid. | yes |
| 9 | AT3_n is false on real pool prefixes: pool_hept[13] at k = 11 with A0 = {1,2}, and pool_hept[11] at k = 12 with A0 = {1,2,9}. | EXACT | CONFIRMED with its own code (at3_own.py). Both prefixes are valid. A0 is uniform and misses 3, respectively 9, hexagons through u, and there is no good antichain. The additional d7_13 k = 9 report was not checked. | yes |
| 10 | AT2_n is equivalent to: U has a uniform Δ D with D − u uniform in U − u (PROVED). AT2_6 holds for real \|U\| ≤ 12 and AT2_7 for \|U\| ≤ 13 (CERTIFIED). | PROVED; CERTIFIED | CONFIRMED. The equivalence was re-derived. All 14 AT2# proofs were re-run, including the 3.55 GB n7/m13 proof (111 s). The CNFs are byte-identical. Own controls: 3 SAT and 40 UNSAT. Not checked: the 4 unrealized abstract AT2#_6 models and the AT2#_7 m = 14 run (UNKNOWN). | yes |
| 11 | **AT2_6 is false for real sets.** V = (−810,745) (−698,596) (−511,−742) (−258,174) (−257,184) (−147,−18) (−141,−92) (−135,10) (−9,−287) (49,−179) (75,−150) (100,−482) (810,−341) is (5,6)-valid, with u = (810,−341). U − u has 7 uniform Δs, and none satisfies option (i) or (ii). U itself has 407 uniform Δs. A second counterexample is at2real/at2_n6_m13.seed5_b.json. | EXACT | CONFIRMED by its own exhaustive check. V has 62 four-caps and 114 pentagons; U has 407 uniform Δs, 174 of them containing u. seed5_b has 32 four-caps and 145 pentagons, 12 uniform Δs in U − u and 44 in U, and AT2 fails. Both fixed CNFs were rebuilt (202 and 219 clauses, equal) and re-accepted. All 286 signs match. | yes |
| 12 | Weak D(5,7) and weak D(5,8) remain OPEN. All counterexample sets above satisfy weak D, and UE holds on every counterexample U. | COMPUTED | CONFIRMED (computed part). The weak-Δ counts are 494 to 12,176 per set [corrected 15 Nov pm: **486** to 12,176; d6_12 has 486, see D6_12_NOTE.md]. The uniform-Δ counts are 34 to 600 for AT and 407 and 44 for AT2. | yes |

**What this changes** (author's reading in atn README §8, consistent with the confirmed statements):
- **Rooted uniformity fails.** In all three AT counterexamples, U has uniform Δs but none contains u. So every induction
  step that must keep the new rightmost point in the Δ fails.
- **LT-cover_6, LT-cover_7 and LT-cover_8 of design:delta:1 §5 are false as stated.**
  - AT_n is idea 39's antichain form of LT-cover_n.
  - The author's `ltcover_literal.py` also ran the literal vertex-cover form directly, for all 232 A0 of the n = 7
    instance, and it fails there too. The verifier did not re-run that literal check.
  - The roadmap route "LT-cover_8 ⟹ weak D(5,8) ⟹ ES(8) ≤ 303" therefore loses its key lemma. Weak D(5,8) itself is not
    refuted.
- **Deleting points or adding u is not enough at n = 6.** AT2_6 fails at 13 points and AT3 fails on pool prefixes. So a
  uniform Δ of U cannot always be obtained from a uniform Δ of U − u by deleting points and/or adding u. An inductive
  proof of UE_n needs a different step.
- **Not refuted by any of these sets:** weak D(5,n), UE_n, and ENV#/VE/RT*/ROOT. For ENV#/VE/RT*/ROOT this is the
  author's remark, not separately verified.

**Certificates, track 2** (CNFs under `atn/univ/`, proofs as zstd in `atn/univ/cert{,2}/`; the fixed_* rows are the
fixed-instance checks of the counterexamples; verifier = `vatn/cake/recake.jsonl`):

| CNF | vars / clauses | CNF SHA-256 | LRAT bytes | LRAT SHA-256 | author: cake_lpr | verifier |
|---|---|---|---|---|---|---|
| ats_n6_m6 | 86 / 448 | `523cd23c56b7b6ac5a392e62424ad96761c50b57411f6bed259d2c2b6bf212ef` | 95 | `277bc5783bd528636f20405f7c4d4765b6940b9d06dffafdafdcc520d8c1ad6c` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n6_m7 | 162 / 1,010 | `8c3ad98c6dd83289a055b1380ac395240453ebae3eab81d7a5a44c84d734fed0` | 429 | `419c9142b55585eb96f694c589ca6f59c54934b0d4ed6832d632674ed2faa9d1` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n6_m8 | 287 / 2,024 | `52d23bf94b146b98205c41fc2f4d7039db75d6a270b71b916ce0b8ea02c7bf84` | 18,263 | `154e8cf289c93c1e91edd50b42f642b631316db522783437db9ddf9bcc346375` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n6_m9 | 484 / 3,733 | `5f2859685698e4c8a6d448c9ac35affb878e6dd3e4f62e4f068800c2cda98ca7` | 402,399 | `721eb420b014385b0d9367be991d2419b21a1637732312e43e99d3c12dbc649c` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n7_m7 | 157 / 974 | `ac95bb370af9e70adebd873219f3253689a1287d8adeda21d757da7816bf6e93` | 285 | `43ff4896d4becc073b6223fb904cbe6e578d47a836f3da9ddf75b020cf5d8b74` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n7_m8 | 273 / 1,969 | `0d9cd4f86860dcd0afc936e7c79feeddf361dcf3d72eb34b172945b897697b91` | 1,036 | `de81777153360c1c760738124f2948c79875d70d35b81878ce294d61c98c9948` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n7_m9 | 456 / 3,755 | `973429bfb99a18f8ee314ebb2563bfcff6dc778eab81c8042344b1da10741aa5` | 72,246 | `6f171067d26bac7181090b7deb4b4b4e9e836d987813dd9dd0aa4bdc6009c8a4` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n7_m10 | 741 / 6,892 | `08f881907a5c4b2ab2be213cabd327dd6b11927bf971b0e9a92f08e8427d98d4` | 2,683,685 | `f8a3590e859730b3adc8d6168a642e7dc1c4d45bde1a91e2219d32288bafb125` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n7_m11 | 1,180 / 12,290 | `295818c4c7625ea69621144d51dd9482a27d22bba4fbacd266e72a9dae417d43` | 24,109,865 | `a5961a1c5828ba9eca841ae42358822696df438bab7b5ed1a6151524213dfa3c` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| fixed_d7_13_U12 | 11 / 89 | `56b2095730bd8ad9fc715dce8c6532006ea767fc05cc593962972a1365fa55cf` | 1,274 | `d27cf9e1956a585df74fa3b1057bcce5a9bbb71d76e22e5f1198b55a60d27e22` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| fixed_d8_15_U14 | 13 / 141 | `406c2032f5143a052b54a97be66c38d1f4f17b06ce240be5f253fb4854d24de4` | 1,240 | `745efdc4406f2329d03e2d718919ce45f50fccfeb9aad556bd8e0dccb69e0d9b` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n8_m8 | 267 / 1,871 | `55529c359dc0b17b5d9f3105e27d40d46970df149318f3249a8070ee5fb52f9b` | 779 | `43dad6c6d26c33cfc03fa35c393491d3f16fde9cf90ccda1fdfc3ea4d925fcbb` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n8_m9 | 436 / 3,532 | `382007907f9323c4364ea712ed3d15cef1a9aec9905a7ddac8561f01c56c6ba8` | 2,054 | `86467b2344f4687364f9a17cb33ee538c271d5a07ee34e25c5c98b05fc2ef951` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n8_m10 | 693 / 6,691 | `82493806935bf7f37ceb55658f5ac21bfbd2d0c1fb041071dfbb3e0be01d930a` | 212,016 | `025f0c9dc784a9854a93c8c66afaaa09420211162f839f539a1bb573b2cf0f20` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n8_m11 | 1,090 / 12,923 | `640860cd6da7516805a2561516ff912ea5690dd60aa300f5caf925445fe67ffd` | 4,742,507 | `c5bf92fa2ed5b240fb8bf7beb7d37d2391b98d1bdf0526850dcb589e6bde53da` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n8_m12 | 1,716 / 25,246 | `e8396ef41f74b1b9cdbd218cddab85552159b97e223d99239c6713ca30a213c9` | 120,386,202 | `688ef3edc1f868587d067a2602333215f7424349c498934bcd8ff231f5d5609c` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| ats_n8_m13 | 2,718 / 49,040 | `0c835892446587d47e6f5a4d79370a88ab42a40e15444e3eb4406040bb806d96` | 2,402,026,659 | `08d982ffb8e14af8e920339838357872e98fbeb47aa8bb2ceae8b4583940f1e7` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n6_m6 | 91 / 499 | `9b41afe074a2c20b589e78ab1f98df48529428939bbdebaadb5ad7500d270587` | 95 | `2ae49aa1d46b3e9938aeb7b85d2750222bb17100e0dc22ad90ccd4d1c16dec22` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n6_m7 | 177 / 1,147 | `af7d8c77f10ddae4aefc17f7cdab20af40cad71e8e990782805e78eada0eb05a` | 523 | `a9b8b6afb7f34c64d5d07405a18978f3e764a75201c5a16f99083f871a3806ad` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n6_m8 | 322 / 2,333 | `4a273255e2868627844e37f3272742940cf739f0bb9124b50fa618078fa4e2fc` | 2,132 | `1d87ad26b7abbcad37b1264a4ce5db367ce0668c3436b64b85a9f02cbcfeb14e` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n6_m9 | 554 / 4,358 | `200bd29705d355d54f2b1ba73377eaeb03c0cdab72d21bcf990f91b1b5223f00` | 189,642 | `39b1220d9b29e094361a34755376975abf47ddb10c8eae97f94d5b2249406f6b` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n6_m10 | 909 / 7,658 | `1127c265f5d6f7af7f3cb1b866f65c4cc38157a8804a0595d4acf7b37708d9db` | 3,552,841 | `944d758fac7f91063f2a08ff7179731d9a948b10418e4f32d6d0dab82c19cfb9` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n6_m11 | 1,432 / 12,880 | `2caccf9e620dd9b09080da46eac65c89ccd9bc991d4cca2cb19cb18bbdf2d17a` | 57,466,843 | `f0e1864f114b3edbd7b3d0f0eed49839098b931f4361bdc88a1988be72b11915` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n7_m7 | 163 / 1,101 | `e7b5a299724a7723aa382e12076822f6464254e28defec74bd39318aa4041da7` | 315 | `012566cea53c6563743181b97ec8db88d099bf2029a2bff27dbb54dc5c6f3a95` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n7_m8 | 294 / 2,383 | `4b9f7c5ef92e754adfee47650cf0d9f075a14e2de6cef87695908fb8efc36452` | 1,164 | `b70f443c68ee6fb26625aec2f8e7bcfb3d94babda880c87f92eef9410c9c40c6` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n7_m9 | 512 / 4,828 | `220aec95abf54a750a0b764f98ee02fe6cd721ef5404e23ce424f34f79ab9b9f` | 3,854 | `c68544a5d67e36d8e9845feb920a71f415a29ff8bb4844790f2401ecefc2d0fc` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n7_m10 | 867 / 9,290 | `3b8d0e7f47c3cf53e984c7043e4e274c7defbb2276826f04846b5c3100f69712` | 130,418 | `9b74cfd96f2139ea4e8be75d68c3d06545029bf764309cd501a77619f0c8a1c7` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n7_m11 | 1,432 / 17,128 | `54ffcc3e9b90934a37dbeb6e2d0d5ffff41d23df8757ec7dd2a8b3e3bfba497c` | 4,132,218 | `e50e4606f0364e8e8dc12f072bbb79d0c8d2f8f529d1c4cf48c410f43c34b1e1` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n7_m12 | 2,310 / 30,461 | `fa5288ae2c7baf1194b73a413e5c6ae7da64dcf713982a53f759edda0781ed4b` | 111,931,888 | `b1f83f1001f36129a5058cfede293cd05c155272afc7cd0618ef853a260a75c9` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n6_m12 | 2,178 / 21,023 | `ec08f72a694aa7dff2600118f10a4dffdfc85b2a3389635e335da76518131fa5` | 604,241,381 | `869b70217084ed47ae60ee17ed55db40be7ee31e3a444724f086a874568237c7` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| at2_n7_m13 | 3,642 / 52,573 | `8b76f4a79ba6d48a950a7967ac42591a6cfb26fcefef5e3617f80202aa277db3` | 3,551,739,524 | `05c81b590aaecaf3d00861b2f74c6a9f75cb8a59de8a2d15cfa1fb52b0680ed3` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| fixed_at2_6_13_opt1 | 12 / 202 | `249703f3001d55bb4b71e3d8f04ce1dab38edde1b48de0dade03f623f10b47ef` | 1,590 | `2dc83287f4ffc549e53d742395f0d609c8c34f4aa77510438df2b31fe27f198d` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |
| fixed_at2_6_13_opt2 | 12 / 219 | `fa42e08fef17a91e3de581fdcdaca48b4d1037852f11a9c353a777bbcaf0b7e9` | 2,291 | `848eb08c2c75189d540dac1b6ba1b0d3f0b33edf54e2fddadeea40d0f7ba3788` | `s VERIFIED UNSAT` | re-run: exact line, CNF and LRAT hashes equal |

**What remains open (track 2).**
- **AT2 beyond the certified sizes.** AT2_7 at |U| ≥ 14: the AT2#_7 m = 14 finder was UNKNOWN after about 1,860 s.
  AT2_8 was not run.
- **Unrealized AT2#_6 models.** The first model and seeds 3, 4 and 6 have not been tested for realizability.
- **UE_6, UE_7 and UE_8 in general.** They are not refuted, and they hold on every counterexample.
- **A general family.** Do doubly-rooted failures exist for every n ≥ 6? The three examples share one shape with 2n − 1
  points: a 3-point head, u at the end of an (n−1)-cup, and (a,u,r) a cap for every a. Not examined.
- **Statement 6 in full.** The n = 8 x-mirrors are 81 of 318 done (`run_n8.sh` resumes). The remaining ~49,100 recorded
  witnesses have not been re-checked.
- **Moot now.** The LP and Mirsky questions of METHODS_SWEEP §3.2 no longer matter, since AT_n is false.

## 3. Track weak D(4,8) at 14-22 points (author `round6/d48/`, verifier `round6/vd48/VERIFY_D48.md`)

**Model and soundness.**
- Lemma S48 is in d48 README §3 and §6. The candidates are the index sets of at most 7 points: a set with no 3-cap is a
  cup, and an octagon-free set has no cup longer than 7.
- The verifier's own clause-family checkers (`chk/famcheck.py`, `famcheck_c.py`) sort every clause of the eager CNFs
  (m = 14, 15, 16) and the chain CNFs (m = 14, 15) into families that are true under a counterexample's natural
  assignment. Nothing is left over, and both deliberate mutants are flagged.
- The verifier's own encoder (`vd48/enc/myenc.py`) has no 4-set helpers and lists all triples. It certified m = 7..14
  independently; its table is below.

| # | statement | label | verifier's verdict | counted |
|---|---|---|---|---|
| 1 | **Every (4,8)-valid signotope on 14 points, and so every 14-point set with no 4-cap and no convex octagon, has a cup that meets every convex 7-set.** | CERTIFIED | CONFIRMED. cake_lpr was re-run on d48_m14 and d48c_m14: exact line, hashes equal. Its own family check covers all 164,062 clauses (d48) and 170,538 (d48c). Its own encoder independently gives UNSAT at m = 14: CaDiCaL 65.7 s, cake_lpr exact line, with a positive control on 6 real 14-point subsets. | yes |
| 2 | **The same at 15 points.** | CERTIFIED | CONFIRMED. Both proofs (d48_m15, d48c_m15) were re-run: exact line, hashes equal. All 304,399 and 320,783 clauses lie in sound families. The verifier's own encoder reached no verdict at m = 15 (1,000 s limit, 1,650,897 conflicts), so m = 15 rests on the two d48 CNFs, both re-checked. | yes |
| 3 | **The same at 16 points.** cake_lpr accepted a trimmed copy of CaDiCaL's proof, not the original file. The original (12.45 GB) exhausted cake_lpr's heap at 1,200 and 1,500 MB. | CERTIFIED via a trimmed LRAT; **the owner rules whether this meets the house wording** | CONFIRMED. cake_lpr (heap 1,500 MB) was re-run on the trimmed proof: exact line, 359 s wall, peak 1.54 GB, and the CNF hash, LRAT hash and byte count all match. All 540,483 clauses pass the family check. The untrimmed stream re-hashes as recorded. The argument "a faulty trim could only be rejected" is correct, since cake_lpr re-checks against the same CNF. **Caveat:** the accepted file was derived by an untrusted trimmer (`tools/lrattrim.cpp`); CaDiCaL did not write it. | yes |
| 4 | Weak D(4,8) holds for every signotope and every point set with at most 16 points. | CERTIFIED (16 via the trimmed LRAT) | CONFIRMED. m ≤ 6 is trivial. For m = 7-13, DELTA2N's `cnf_hashes.tsv` lists the strong form as UNSAT with the exact line, but those proofs were not kept and could not be re-run. Independently, the verifier's own encoder certified m = 7..14; at m = 7, 8 the CNF contains the empty clause. m = 14-16 are statements 1-3. Baek's M(4;8) = 22 comes from the literature only. | yes |
| 5 | Lemma S48: if the CNF for m points is UNSAT, weak D(4,8) holds at m points for all signotopes and all point sets. The same holds for the chain encoding. | PROVED | CONFIRMED, with **two gaps in the write-up**. The short CAP4 / CUP8 / G37 clauses need two signotope facts: σ(ijk) = σ(jkl) = − forces a 4-cap, and a set whose consecutive triples are all cups is a cup. The verifier re-derived both, and they hold. | yes |
| 6 | The positive and structural controls on the 14-, 15- and 16-point CNFs all passed. | COMPUTED | CONFIRMED, with a **correction**. "66-790 heptagons each" holds only for the greedy subsets. Over all 72 configurations per size the ranges are 0-340, 0-540 and 0-790, and 3, 2 and 1 configurations have no heptagon. The chain encoder's controls cover 48 configurations (S1, S2, R1, R2), not "the same checks". | yes |
| 7 | Each of the 24 real (4,8)-valid pool sets (18-21 points) has a working cup. The smallest working cup has 3 points in 4 sets, 4 in 14 and 5 in 6. | COMPUTED | CONFIRMED by its own C++ program (`fullsets_v.cpp`, exact __int128 arithmetic). Brute force confirms the validity of all 24 sets, and the counts are equal; all five 21-point sets need 5. This is a fact about these 24 sets only. | yes |
| 8 | 17 points would need about 23 M conflicts, about 10 h on one thread and an LRAT of about 60 GB. | HEURISTIC | **NOT CONFIRMED.** The conflict part holds (×5.29, ×5.27 per point, giving about 23.3 M), and so does the time part (×10.9, ×12.4, giving about 8.4-9.6 h). The LRAT size does not: it grew ×9.7 and then ×11.8, which points to **about 120-150 GB**, not 60 GB. | **no** |

**Certificates, track 3** (CNFs under `d48/cnf/`, proofs as zstd in `d48/cert/`; verifier = `vd48/cake/recheck.jsonl`).
The SHA-256 of the zstd archives themselves is in `d48/cert/zst.sha256.final`.

| CNF | vars / clauses | CNF SHA-256 | LRAT bytes | LRAT SHA-256 | author: cake_lpr | verifier |
|---|---|---|---|---|---|---|
| d48_m14 | 4,797 / 164,062 | `ef1580665eeb9d45adec6fc0875c05243390ead78e47756d87f7174a21c09cec` | 108,455,438 | `5c2878af994df61b67aa083cd9b3859ecca99496907ba71f36aaba05ded0b906` | `s VERIFIED UNSAT` | re-run (heap 1200 MB): exact line, CNF and LRAT hashes equal |
| d48_m15 | 8,255 / 304,399 | `e6dc2f751daceea99532e2a468906347cedb2eeb4f361160a86e8feb356f36cc` | 1,055,101,030 | `b32b434e256ead8538153fa37368bd56c649df6290c3319546fdfd8a8e0f42db` | `s VERIFIED UNSAT` | re-run (heap 1200 MB): exact line, CNF and LRAT hashes equal |
| d48_m16 (CaDiCaL original) | 13,820 / 540,483 | `fcc31f0428a5ffceefaff5adbb96d503311a0dc5d1262a51280d4bc9b229e5a7` | 12,453,020,200 | `dc47342e18cd54fac1b1e1627d6275a955c6a475cd5df8152eca125b3beeef9f` | no verdict: "CakeML heap space exhausted." at 1,200 and 1,500 MB | not re-run; decompressed stream re-hashed: equal, same byte count |
| d48c_m14 | 11,273 / 170,538 | `167920bc801bd4fe8553298f7ad4c8555c43f5bec3ba36d8c624035026273790` | 116,663,473 | `0bf125299bd1bd24f003b6e969cac0a4af8c584089230e1133c8810fd3d3ebe8` | `s VERIFIED UNSAT` | re-run (heap 1200 MB): exact line, CNF and LRAT hashes equal |
| d48c_m15 | 24,639 / 320,783 | `7017220c16a99efdf97f739bcf70117c8e3493410c67133fd6341cef57a249ce` | 1,239,305,418 | `b0b65dc4bf1d3049373bd290d91f6bb73c94cc258599a2eb87a019a200cab9b0` | `s VERIFIED UNSAT` | re-run (heap 1200 MB): exact line, CNF and LRAT hashes equal |
| d48_m14 (trimmed by tools/lrattrim.cpp; heap 1200 MB) | 4,797 / 164,062 | `ef1580665eeb9d45adec6fc0875c05243390ead78e47756d87f7174a21c09cec` | 74,509,113 | `52b267fe6271b24999c1642c355c02c87df3228a2bedec56adbcd015bc8a3eaf` | `s VERIFIED UNSAT` | not re-run; archive passes zstd -t |
| d48_m16 (trimmed by tools/lrattrim.cpp; heap 1500 MB) | 13,820 / 540,483 | `fcc31f0428a5ffceefaff5adbb96d503311a0dc5d1262a51280d4bc9b229e5a7` | 9,108,287,846 | `1abf185657fb65096ffb16c3036985eafe910106811927413611dbbf0431d8b8` | `s VERIFIED UNSAT` | re-run (heap 1500 MB): exact line, CNF and LRAT hashes equal |

**Verifier's own encoder** (`vd48/enc/myenc.py`, certified with the house `certify_cnf.sh`; records in
`vd48/enc/cert/certify.jsonl`):

| verifier CNF (enc/myenc.py) | vars / clauses | CNF SHA-256 | LRAT bytes | LRAT SHA-256 | cake_lpr |
|---|---|---|---|---|---|
| my_m7 | 36 / 583 | `81183d1f47a529b9f149dec2dfbf3e0a465717e74cff413d8074f3e88ba8a0d2` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `s VERIFIED UNSAT` (CNF contains the empty clause) |
| my_m8 | 64 / 2,012 | `249bbf776e49ed5b463d541b75b03d9a4905f38c0f778df9671e4b0fdba2bfde` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | `s VERIFIED UNSAT` (CNF contains the empty clause) |
| my_m9 | 120 / 6,739 | `722054e77945a49636c35dce279a63495300aea04864f0e68d3c970a8edf858a` | 399 | `9c7c1e65b56920f40ce45644c17ef22d1e878b354fd63728d2809d4ccf3fdc2e` | `s VERIFIED UNSAT` |
| my_m10 | 240 / 19,973 | `0043f84ac677096c485f8a2c776804ec9d830a919336632f6f0756c590dfd147` | 1,444 | `a5d7ae4eeb0dfff59ab183913ee045c06e04845e560a20e421bd1495ba31c618` | `s VERIFIED UNSAT` |
| my_m11 | 495 / 52,141 | `eaec1d9f10eec265dcb71f2b3074bb0615d8b895f4dd8cb4b16533d739bcfa95` | 31,323 | `a649329a1158b437f60ad2200ced2da2db4f8dd0e8c08d36a0b8904c05aa00be` | `s VERIFIED UNSAT` |
| my_m12 | 1,012 / 122,102 | `fcadff64a19b35595c13b2aee8d0c16b4d52b90cbd49476988cdfe0fd81ed4da` | 658,381 | `dd91ba286b4902b203cc34149c85c08dc84944addaf08fec8be7218e4bc06a05` | `s VERIFIED UNSAT` |
| my_m13 | 2,002 / 261,496 | `053a8472e36a5b526b1a5eede4ef6ea27688e296a16097ada8348f9e9648592e` | 7,433,652 | `71b74b047f330be1031607e8770fc0f275212b0f7b5836888c5500c17c3d6d67` | `s VERIFIED UNSAT` |
| my_m14 | 3,796 / 520,418 | `25d31a405c5be3cda650ad1a1e5370c123871e82971326c5af0de98d92d8fb9b` | 172,619,411 | `b403e06f884a59cf094f0ea349f9b00cfe4899707edda9ece12bc0661426cc7b` | `s VERIFIED UNSAT` |
| my_m15 | 6,890 / 974,614 | `a41ca751389c4662f95d145d0972fc7c274638c9041213fcf2eae086938ef4b3` | – | – | no verdict: CaDiCaL stopped at 1000 s |

**What remains open (track 3).**
- **Weak D(4,8) at 17-22 points.**
  - 17 points extrapolates to about 23 M conflicts and about 8.4-10 h on one thread (HEURISTIC). Its LRAT would be about
    120-150 GB (verifier's extrapolation, HEURISTIC), so it needs a cube split or a stronger encoding, plus trimming or a
    cake_lpr heap of 4 GB or more.
  - A counterexample at 17-22 points would close the uniform-envelope routes at n = 8 (U4 corollary) without deciding
    weak D(5,8).
- **Owner's ruling.** Does a trimmed LRAT accepted by cake_lpr count as CERTIFIED? It has the same CNF and the same
  checker; unused lemmas were dropped and deletions moved. The untrimmed m = 16 proof is kept and needs a heap above
  1,500 MB.
- **Baek's M(4;8) = 22 for abstract signotopes.** It is not certified. For point sets the problem ends at 22 points
  by Baek's theorem; for signotopes this upper end is not established.
- **The hi = 3 question.** At 14 points, can every valid signotope's working cup be chosen with at most 3 points? It
  was UNKNOWN after 120 s.
- **The m = 7-13 strong-form proofs of DELTA2N** were not kept. The range is covered again by the verifier's own
  certificates (m = 7-14).

## 4. Records to correct (listed only; existing files are never modified here)

- **METHODS_SWEEP §1 item 3 and §3.2.** "AT_n not yet evaluated on any instance" is superseded: AT_n is false for real
  sets at n = 6, 7, 8 (track 2). "AT_n is equivalent to LT-cover_n, which implies weak D(5,n)" no longer gives a route.
- **METHODS_SWEEP §3.1 "Next" (b).** ENV#(7) at |U| = 13 is done (CERTIFIED), and |U| = 14, 15 are open. ROOT(7) at
  |S| = 15 is UNKNOWN and 16 is open. The risk line says VE(8) and ENV#(8) contain weak D(4,8). That obstacle is now
  certified away to 15 points, and to 16 via the trimmed proof.
- **METHODS_SWEEP §3.3.** The weak form is now certified at 14-15 points (16 via the trimmed proof). 17-22 are open.
- **ROADMAP20261115 SYNTHESIS §2.2.**
  - Item 2, the doubly-rooted realization test, is done: the failures are realizable at n = 6, 7 and 8.
  - Item 5, LT-cover written work, has no target any more.
- **design:delta:1.** §5 states LT-cover_n, and the atn author also lists its S4. LT-cover_6, LT-cover_7 and LT-cover_8
  fail as stated.
- **ROUND2 Task 4.** The UES* look-ahead, listed OPEN there, fails on d7_13_real at prefix 12 (COMPUTED by its own
  script; forced, verifier-confirmed).
- **envroot README §3.1.** The 124 TS-failing sets have 18-22 points, not 17-22.
- **d48 README.**
  - §3: add the two signotope facts behind the short clauses.
  - §6: the heptagon range of the controls.
  - §8: the m = 17 LRAT estimate is about 120-150 GB, not 60 GB.
- **attack folder `README.md`.** Its line "being worked on in round 6 (`ROUND6.md`, expected by 09:40)" now points to this
  file.
- **No novelty statement is made here.** Compare with the literature first; the last full check is
  NOVELTY20261113B.

## 5. Files and hashes

All paths are under `/home/jay/research/data/roadmap-20261115/round6/` (not in Git). envroot and atn have full
SHA256SUMS files (133 and 307 entries; envroot 3.0 GB). d48 records its hashes in README §7 and `cert/zst.sha256.final`.
- **Proofs kept, all as zstd:**
  - envroot `cert/`, `cert2/` and `cert3/`;
  - atn `univ/cert/` and `univ/cert2/`, about 1.9 GB;
  - d48 `cert/`, including the untrimmed and the trimmed m = 16 proofs;
  - vd48 `enc/cert/`.
- **Re-run by a second party:** all 18 envroot proofs, all 33 atn proofs, and d48_m14, d48c_m14, d48_m15, d48c_m15 and
  the trimmed d48_m16.
- **Not yet re-run by anyone other than their author:**
  - the untrimmed d48_m16, which needs a cake_lpr heap above 1,500 MB;
  - d48_m14.trim, which is redundant with the re-run untrimmed d48_m14;
  - the verifier's own vd48 proofs my_m7 to my_m14.

  The house rule keeps all of them. Deleting any proof directory needs the owner's OK.

Evidence files (SHA-256 computed by the writer at write-up time):

| file (under round6/) | content | SHA-256 |
|---|---|---|
| envroot/README.md | author record, track 1 | `1e94cd0a53227597ee15c7a17ddf778ecde9e296735499a000099989ae18be8d` |
| envroot/env_cnf.py | ENV#(7) encoder 1 | `94eb85691338b4ea7ca5e469e9074b00bec11c28e2f22f7c7fd23766225e61a8` |
| envroot/env2_cnf.py | ENV#(7) encoder 2 (extension form) | `cf977694406cd844e2b4d61982dbbb1b0598b168a4be5b6647e3b9e85804fe61` |
| envroot/root_cnf.py | ROOT(7) encoder | `aef1af7a5f63a7d5f9f0882bc246ad325bd9ec4ead7f3830bf8b5f6d74d09cec` |
| envroot/fixed_env.jsonl | ENV# witnesses on the task-1 fixed sets | `37a90488152215fda6d5ddc6a7ccf62199dff38489cfef1ae6a9b6b7145be5f2` |
| envroot/fixed_pool.jsonl | ENV# / TS on the 302 (5,7)-valid pool sets | `efbcc3135f7c28395319b665fc7305967e88d1d1d7e1e3e3c311a70a736d7d2b` |
| envroot/fixed_n8.jsonl | ENV#(8) witnesses (extra) | `1809702c2d0254d1d70152ea2ae7702174bcde224ee788b653631fa2faa430f1` |
| envroot/count_env.log | U18 / S19′ counts | `75214203749a88a8a1351202ffeaf8fadce288c7007cb582b05087a8f28f8fe8` |
| venvroot/replay/replay.jsonl | verifier: 18 cake_lpr replays | `ef736d2bfffb7e76260474bbe32fc22f9618f4017f0acfa972b5863b256d1cf5` |
| venvroot/regen/regen.txt | verifier: 19 regenerated CNFs | `6ad89876f2014113e90ddfb440bf80b168ba1b99fb84aedd4d2bf1525610a044` |
| atn/README.md | author record, track 2 | `149f73e15ac4d04a53305338483787a370b6cfd580a3c6694847a4e3f0f0500b` |
| atn/atsharp_cnf.py | AT#_n encoder | `86520990b4518178ee5b9f9d4cf91b5a7f6b3d6ec9c023ecc014688914a5da81` |
| atn/at2_cnf.py | AT2#_n encoder | `61236549ad59f3adda5993e7bbc07ac1e42cc3f7f201b216016935afa3a62c19` |
| atn/dr_cnf.py | doubly-rooted finder (found d8_15) | `667032e16dff0de4ec3921bb28b55e248010c9c228bdbdcbc72dcfa8a0d14adc` |
| atn/d7_13_real.json | AT_7 counterexample S (13 points) | `209f9f041196647a96651fdbf373dfd8c6321322eb9379f0abc5b504bbd7e705` |
| atn/d8_15_real.json | AT_8 counterexample S8 (15 points) | `416a1cdacc895e7d55e79a9f7cf5df67e30843e098b9ea1d3247ca44ea26e6ce` |
| atn/d6_11_real.json | AT_6 counterexample | `2aba56097efee08aa7c272976c6c5f71580550502381bc3049c8b57dd9434e1e` |
| atn/d6_12_real.json | AT_6 counterexample | `f97741da80a29f53bd640706b7b03fc639d3db16abb4f92623dcecddab559c90` |
| atn/m11_1_real.json | AT_6 counterexample | `219ff49fcd6ce8bb065951c779b9cb5ebb49239feb1e6fe5fb4ded1abb542048` |
| atn/m11_2_real.json | AT_6 counterexample | `f1faeb51809be56bc2e3720f785036547b11d2ba30562ad17d92a756d009ed6c` |
| atn/m11_3_real.json | AT_6 counterexample | `d719bf86d8a2b604d789421797d2c8afeee54aeb29ddaf5f811254ca8b74af2b` |
| atn/m11_5_real.json | AT_6 counterexample | `57617b89518f62f8232d157bb84e56164b9351b3e53541e83df74b9b10a8b9ca` |
| atn/m11_6_real.json | AT_6 counterexample | `0772a2ea658ad4594da18ac54385f8fd7bbd12a0bec6c466d6ae4a5eefc25a47` |
| atn/m11_7_real.json | AT_6 counterexample | `54b96876279113805d853c205f56f583911cb695eca68e74c9fd3c42d60dae9a` |
| atn/m11_8_real.json | AT_6 counterexample | `83049d4c02d7d34e6ec6804e3274aa8751c483db416b072ed1dd7b7c6b2044c0` |
| atn/m11_10_real.json | AT_6 counterexample | `3e3269ad5b1d4ad85b016eda63e9f8bdd6a444d718e93abcb45200b9d5c18e43` |
| atn/at2real/at2_n6_m13.seed1_b.json | AT2_6 counterexample V (13 points) | `02a0d09a555ee5e882b172239f76c0466f291c5c7c198ef0b4abfd88840342c5` |
| atn/at2real/at2_n6_m13.seed5_b.json | AT2_6 counterexample (second) | `c3e6f3df2dae1495953792d9838119395134c6a5c67098db928d035fe295ed78` |
| vatn/VERIFY_ATN.md | verifier record, track 2 | `f992596c16d253ac1963cd464153bbb0de5ef6444f5f3f810575f20052b56d3c` |
| vatn/cake/recake.jsonl | verifier: 33 cake_lpr re-runs | `f4c18f1ba6cf9de702b37a9f53f2cf45480ee323c2e279e3504915e014c99ff4` |
| d48/README.md | author record, track 3 | `a2586fa5fbfc8f9c09ff3ed8d15547b23de3d7dbbf329a45b98d68c49b4a3878` |
| d48/tools/build_d48.py | weak D(4,8) eager encoder | `07c6331facb408ceecd81b5c949fc347893e27670a9a4af7102fd5c199d56998` |
| d48/tools/build_d48c.py | weak D(4,8) chain encoder | `69fe2b5b987dbe333812dd50aacdccaf91624a86c06ab22e576d93431a86fae1` |
| d48/tools/lrattrim.cpp | LRAT trimmer (untrusted helper) | `9e08c5c5f0f6495e380a81bba616e088b48780f245a3235b904660698768f952` |
| d48/controls/fullsets.jsonl | the 24 real (4,8)-valid pool sets | `0031b3678b3a851ed5dd40cfe611ceb0769c48008309b4e3b20fce77f944e759` |
| vd48/VERIFY_D48.md | verifier record, track 3 | `a7abbac80f75c521c424b48077fa0df2493413cea9560dfe824574b2205175f1` |
| vd48/cake/recheck.jsonl | verifier: cake_lpr re-runs | `255c7a23b0f8e0bd46153353382ea02ebf99e66bfd9047312d32708d8ee9bc09` |
| vd48/enc/cert/certify.jsonl | verifier: own-encoder certificates | `5665703ecff521f72f67d924985d77e14611a4cbfbd5368089010492996b6b59` |

**House rules held.**
- **Units.** Every job longer than a minute ran as an `esr-agx-r6-*` unit with CPUQuota=100%, MemoryMax=2G,
  MemorySwapMax=0, nice 10 and a deadline by 08:45.
- **Overlaps and pauses, as reported by the agents:**
  - atn's chaining scripts caused two short overlaps of two units (23 s and 10 s), and the second unit was stopped each
    time;
  - envroot ran side jobs at 50 % quota while its main chain was lowered to 50 %;
  - d48 and vd48 paused their own unit (SIGSTOP/SIGCONT) for short foreground checks.
- **Thread budget.** At 08:10, vd48 saw `cpu_free.sh` report 0 free threads: the quotas of the running units added up to
  15.34 of 16. Each agent used its single thread.
- **Deletions.** Only non-proof files were deleted: two partial LRATs and `__pycache__` by envroot, and decompressed
  re-run copies by vatn.
- **Git.** No git action was taken.

## 6. Reproduce (each a single-thread job; the large replays as units)

```bash
R6=/home/jay/research/data/roadmap-20261115/round6
U="systemd-run --user -p CPUQuota=100% -p MemoryMax=2G -p MemorySwapMax=0 -p RuntimeMaxSec=1800 --nice=10"
# track 1: stream-replay kept proofs through a FIFO (heap 1400 MB, about 2.5 min each); appends to venvroot/replay/replay.jsonl
$U --unit=esr-agx-r6-replay1 bash $R6/venvroot/replay.sh 1400 cert/env7_m13 cert2/env2_7_m13 cert3/root7_m14
# track 2: re-run one proof (decompresses into vatn/cake and deletes the copy); appends to vatn/cake/recake.jsonl
$U --unit=esr-agx-r6-replay2 bash $R6/vatn/recake.sh cert ats_n8_m13 1500
# track 2: exhaustive exact check of the AT_7 counterexample (0.1 s, foreground)
cd $R6/atn && /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -I check_cex.py d7_13_real.json 7
# track 3: stream-check the trimmed m = 16 proof (heap 1500 MB, about 6 min; FIFO pattern of vd48/cake/recheck.sh)
W=/home/jay/research/data/<new work dir>; mkdir -p $W && mkfifo $W/f16
$U --unit=esr-agx-r6-replay3 bash -c "zstd -dc $R6/d48/cert/d48_m16.trim.lrat.zst > $W/f16 & \
  ~/.local/bin/cake_lpr --CML_HEAP_SIZE=1500 $R6/d48/cnf/d48_m16.cnf $W/f16 > $W/m16.cake.out; wait"
grep -x 's VERIFIED UNSAT' $W/m16.cake.out        # after the unit has finished
# next sizes: the authors' resume commands, envroot README §7 (ENV# 14, ROOT 15) and d48 README §9 (m = 17)
# regenerate this file's tables: python3 -I $R6/writeup/gen_round6.py $R6/writeup/ROUND6.tmpl.md $R6/writeup/ROUND6.md
```


## Correction, 15 November 2026 afternoon (main session)

- Statement 12 (§2): the weak-Δ count range over the 12 real AT_n sets is **486 to 12,176**, not 494 to 12,176. The
  set d6_12 has exactly 486 weak Δs. This was a summary slip: the round-6 verifier's own output `round6/vatn/out/d6_12.json`
  already says `weak_S = 486`. No conclusion changes: weak D holds on every set.
- Found by track T5 ([D6_12_NOTE.md](D6_12_NOTE.md)). Claim `d6-12-correction`, CONFIRMED by V3
  ([VERIFY_D6_12.md](VERIFY_D6_12.md)).
- The same wrong range is still in the work copies `round6/writeup/ROUND6.md` (line 193), `round6/writeup/ROUND6.tmpl.md`
  (line 172) and `round6/vatn/VERIFY_ATN.md` (line 136). Those were not edited.
