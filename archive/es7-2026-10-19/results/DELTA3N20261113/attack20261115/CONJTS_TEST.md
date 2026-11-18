# CONJ-TS′ certified test, round 4 (15 November 2026; runs 05:50–08:30 KST, verifier 08:35–08:47 KST)

## 1. Headline (exact status and labels)

- **CONJ-TS′(7) holds for every abstract signotope with |S| = 13 and with |S| = 14. CONJ-TS′(8) holds for every abstract
  signotope with |S| = 15. All three are CERTIFIED.**
  - Each rests on a CaDiCaL 2.1.3 LRAT proof that `~/.local/bin/cake_lpr` accepted with the exact line
    `s VERIFIED UNSAT`. The independent verifier re-ran cake_lpr on it and got the same line. Each also rests on the
    written soundness theorem of the encoding (PROVED, and checked by the verifier). All proofs are kept as zstd.
  - Each size is certified by two separately written encoders, `conjts_cnf.cpp` and `flat_cnf.py`. They are
    **independent in code only**: both rely on Lemma A, Lemma B and the 4-subset convexity rule (§3). The verifier's
    lemma-free encoder confirms n = 7 at 13 and n = 8 at 14. It was not run at n = 7, 14 or at n = 8, 15.
  - By the Corollary in §3, the same holds for every real point set of that size in general position with distinct x.
  - n = 7 at 13 and 14 re-certifies `ROUND2.md`, which certified CONJ-TS′(7) for |S| ≤ 14 with other encoders. For n = 8,
    a grep of `results/` for "CONJ-TS′(8)" (09:35 KST) finds it only in ROADMAP20261115 and STATUS20261115_1000, and
    both cite this round.
- **n = 7 at |S| = 15 is UNKNOWN.** Neither a proof nor a model was found before the time limit.
- **Side result: CONJ-TS′(6) is false for abstract signotopes at |S| = 13. EXACT.** There are three explicit 13-point
  signotopes, and two independent brute-force checkers checked each of them. Sizes |S| ≤ 12 are CERTIFIED, so 13 is the
  least failing size.
  - This run left realisability open, because its heuristic attempts failed. Afterwards the main session realised all
    three models with integer points and checked them exactly. That makes CONJ-TS′(6) false for real point sets at 13
    points (`VERIFY_ATN_MAIN.md`, 09:12 KST). Label: EXACT, from the main session's own code. No second party has checked
    it yet.
- **Weak D(5,7) and weak D(5,8) remain OPEN, and no ES bound changes.**
  - CONJ-TS′(7) is already false for real point sets at 19 points (S19′, `S19_REALIZABILITY.md`). So the certified
    n = 7 sizes only bound the smallest real counterexample to CONJ-TS′(7), which has 15–19 points. [superseded 15 Nov
    pm (STATUS20261115_1900, Corrections item 4): 15–17 points, by claim cts7-real-17 (V1 CONFIRMED, verdict file
    14:38:09): CONJ-TS′(7) fails on the two real 17-point ROOT(7) sets]
  - No counterexample to CONJ-TS′(8) is known. It holds for all abstract signotopes with |S| ≤ 15 (§5.3).
- **Independent verification gave the verdict "sound", and no size was refuted.** The verifier made one wording
  correction (the encoders are independent in code only) and noted minor process deviations (§7).

Counting rule: a size is listed as CERTIFIED only if the verifier did not refute it. Nothing is rounded up.

## 2. Statement

The labels 0, …, m−1 are in increasing x. r = m−1 is the last label, and U = S − r.

- (p,q,s) with p < q < s is a **cap** if s lies below the line pq, and a **cup** otherwise. A k-cap is a k-chain whose
  consecutive triples are all caps.
- **Valid** ((5,n)-valid) means no 5-cap and no convex n-gon. A **gon** is a convex (n−1)-gon of U.
- **Convexity.** The main encoder and the flat encoder call a set convex if every 4-subset is convex. The verifier's
  encoder uses the cap/cup split instead. For real point sets the two agree (Carathéodory).
- h_U(b,c) is the length of the longest cap of U ending with the pair (b,c).
- A ⊆ U is **terminal-safe in U** if A has no 4-cap and h_U(b,c) ≥ 4 for every 3-cap a<b<c inside A.
- A **weak Δ** of U is a 4-cap-free subset of U that meets every gon of U.
- **CONJ-TS′(n):** if S is valid and r is the last point of a 4-cap of S, then U has a weak Δ that is terminal-safe in U.

Source: attack 2 (`delta:attack:2`), Theorem 3 in `VERIFICATION.md` P2. If CONJ-TS′(n) holds for all valid sets, then
weak D(5,n) holds (PROVED there).

"At size m" means all S with |S| = m. Each size is a separate statement: a counterexample at one size does not give one
at the next.

Trivial sizes: if m ≤ n+1, every gon misses at most one point of U, so any two points of U form a terminal-safe weak Δ.
In the formulas this shows up as an empty clause: by the clause rule in §3 for the main encoder, and checked with grep
in the verifier's n = 6, m = 4–7 CNFs. The trivial sizes below are n6m7, n7m8 and n8m9.

## 3. Encoding and soundness (`CONJTS_SOUNDNESS.md`: PROVED in writing, checked by the verifier)

**Encoder.** `src/conjts_cnf.cpp` (`a9bb34d3fc6dd13dd42fd318f069eff8f1c67c2a148886722b46308a1303a121`) is a copy of the
reviewed DELTA3N `resume/compact/compact_cnf.cpp`.
- The original is kept as `src/compact_cnf.orig.cpp`
  (`1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553`), equal to the DELTA3N SHA256SUMS entry.
- `src/conjts_cnf.diff` (`43073d95478f01c4e9b0f0a08342b5ece41854d6abb18eaa193983f8097553fd`) adds only
  `--conjts hyp|nohyp`, and raises the m cap from 16 to 20 in that mode.
- Without `--conjts`, the copy writes byte-identical CNFs and maps in base and weak mode for (m,n) = (7,5), (9,6), (12,7),
  (13,8) and (15,7).

**Formula F_mode(n,m).**
- Base (unchanged):
  - orientation variables (true means cup) and the signotope axioms;
  - no 5-cap;
  - flags Q(X) for 4 ≤ |X| ≤ n−1, each exactly equivalent to "every 4-subset of X is convex";
  - no convex n-subset.
- New families. Every flag is a one-way witness:
  - nb(b,c) → t(u,v,b) ∨ t(v,b,c) for all u<v<b: no 4-cap ends with (b,c), so h_U(b,c) = 3;
  - bad(a,b,c) → ¬t(a,b,c) and bad(a,b,c) → nb(b,c): (a,b,c) is a 3-cap of U with h_U(b,c) = 3;
  - Bad(D) → ∨ Bad(D−v), over the 4 smallest v ∈ D, for 4 ≤ |D| ≤ m−n+1: D contains a bad triple;
  - B(X) = Q(X) if |X| = n−1, and B(X) → ∨ B(X−v) over the n smallest v ∈ X: X contains a gon of U;
  - hyp mode only: K(a,b,c) → ¬t(a,b,c) ∧ ¬t(b,c,r), plus one clause ∨ K(a,b,c): r ends a 4-cap;
  - for every D ⊆ U with 0 ≤ |D| ≤ m−n+1, the clause Bad(D) ∨ B(U−D). Absent terms are dropped, and an empty clause is
    intended.
- The main runs use no symmetry breaking, cubes or sign fixing.

**Lemma A.** If S has no 5-cap, then A ⊆ U is terminal-safe iff A contains no bad triple. Suppose A contained a 4-cap abcd
with abc not bad. Then some 4-cap wxbc lies in U, and wxbcd is a 5-cap.

**Lemma B.**
- Terminal-safety is hereditary.
- Take a terminal-safe weak Δ and a minimal subset D′ of it that still meets every gon. Each point of D′ has a private
  gon, so |D′| ≤ m−n+1. If U has no gon, then D′ = ∅.
- Every size from 0 to m−n+1 has its own clause, so small sets are never assumed to grow.

**Theorem.** F_hyp(n,m) is SAT iff some abstract signotope on m labels is a counterexample to CONJ-TS′(n).
- Model ⇒ counterexample: through the one-way witnesses and Lemma B.
- Counterexample ⇒ model: through the canonical assignment and the cover identities.
- F_nohyp is the same formula without the hypothesis.

**Corollary.** If cake_lpr prints `s VERIFIED UNSAT` for F_hyp(n,m), then CONJ-TS′(n) holds for every abstract signotope on
m labels. Hence it holds for every real set of m points in general position with distinct x: their orientations form a
signotope, and a real set is in convex position iff every 4-subset is.

**Second encoding.** `src/flat_cnf.py` (`a6f8223f3963a65b838e6f8b71cbb4e896081fe6cb45749af2db3b0ad935e3e2`) shares no code
with the main encoder. It uses:
- 8-pattern signotope clauses;
- 4-set convexity with an axiom-free equivalence;
- gon flags tied to all 4-subsets;
- bad flags tied to every 4-cap;
- flat failure clauses.

**It shares Lemma A (it checks bad triples only), Lemma B (sizes up to m−n+1) and 4-subset convexity with the main
encoder.** So it is an independent implementation, not an independent derivation.

**Third, lemma-free encoding.** The verifier wrote `conjts-verify/enc/my_conjts.py`
(`648176d9b3791fb90bbb1669794f28e0f6d7a9dc2251c52912903ca655a8ebd9`) from the statement alone. It uses cap/cup-split
convexity, one failure clause for each of the 2^(m−1) subsets of U, and a direct encoding of 4-caps. It needs neither
Lemma A nor Lemma B.

**SAT verdicts** give abstract signotopes only. Their models are checked by `src/check_conjts.py`
(`e859339301c708649fe5a9b4baae36ad6c55ddc37311f4e59c19e225cc1acc02`) and by the verifier's own checker. The first uses
cap/cup-split convexity and a brute-force subset search, without Lemma A.

## 4. Method

- **Solve and certify.** Each formula goes through CaDiCaL 2.1.3 (`/usr/bin/cadical --lrat=true --binary=false`,
  `src/solve.sh`) and then cake_lpr (`src/cake.sh`).
  - A verdict counts only on `grep -x "s VERIFIED UNSAT"`.
  - Each LRAT was compressed with zstd after cake. Each kept main `.zst` was decompressed again, and its SHA-256 matched
    the recorded LRAT hash.
- **Units.** The run used systemd user units `esr-agx-cts-*` with `--nice=10`, MemorySwapMax=0 and a RuntimeMaxSec
  ending by 08:30 KST. Its allocation was 2 threads and 3 GB of summed MemoryMax. The verifier used its own units, for
  example `esr-agx-cv-enc`.

## 5. Results

### 5.1 Main encoder, headline sizes (`cnf/`, `runs/<case>/`)

| n | \|S\| | vars / clauses | verdict | CaDiCaL s | cake s (heap MB) | verifier cake s |
|---|---:|---|---|---:|---:|---:|
| 7 | 13 | 9,078 / 41,718 | **CERTIFIED UNSAT** | 10.5 | 3 (1000) | 2.1 |
| 7 | 14 | 17,814 / 71,245 | **CERTIFIED UNSAT** | 763.8 | 97.5 (1800) | 103.2 |
| 8 | 15 | 35,974 / 152,210 | **CERTIFIED UNSAT** | 1,159.9 | 118.6 (1900) | 107.8 |
| 7 | 15 | 34,973 / 121,036 | **UNKNOWN** | see below | — | — |

Hashes, in the order CNF, then LRAT (uncompressed, with bytes), then kept `.zst` (with bytes):
- n7m13:
  - CNF `ae850264613f8e364be988da26cf486a07bdd47369cfeb35968bd896568ab671`
  - LRAT `f7588b212bca04bed83874654327527e7a764016a4f51bce43cfd77eeabc20c0` (106,846,918)
  - `runs/n7_m13/cts_n7_m13.lrat.zst` `138ee99423dcb787890c706c12fde15afbd48785169482d1056d5dee56f13b71` (31,947,274)
- n7m14:
  - CNF `146a4da17441962d4afa21132346cc248b5bf200c4a2a6d322f4685c06c3d446`
  - LRAT `38520a1d63f138e72442ab9caeb5f88cfbe33f342cd04138221cea938c46bb42` (3,275,982,795)
  - `runs/n7_m14/cts_n7_m14.lrat.zst` `abb6c7b0268e30e474f346da081b42579ae089a05d7a6156870cae8b25e4ce87` (982,119,689)
- n8m15:
  - CNF `7b39fd575508c47f88151bb9819bda24393d8e205a481f759964fe12161dff96`
  - LRAT `5efaeb863a15deef2d00bc94aa90af1e98041d96dc393bc723dc564177f9fc30` (3,795,269,378)
  - `runs/n8_m15/cts_n8_m15.lrat.zst` `9af06c3784bf268b7b517b0f4a60580edac078973ff81044d1c13242e4a1ec04` (1,131,994,153)
- n7m15 is UNKNOWN. CNF `364266614f9de4f91a55dabd24db89a6c19c6a6de475c424d21561dd38f0e643`.
  - The LRAT run went from 06:10 to 08:30 KST: 8,358.7 s and 18,380,879 conflicts. RuntimeMaxSec stopped it (SIGTERM),
    and `runs/n7_m15/cts_n7_m15.cadical.log` has no `s` line.
  - Two no-proof `--sat` runs, with seeds 1 and 2, took about 1,900 s and 2,502 s. Neither found a model.
  - The 22,867,943,424-byte `runs/n7_m15/cts_n7_m15.lrat` is a partial LRAT, not a proof.

### 5.2 Second encoding, headline sizes (`flat_cnf.py`, `runs/flat/`)

| n | \|S\| | vars / clauses | verdict | CaDiCaL s | cake s (heap MB) | verifier cake s |
|---|---:|---|---|---:|---:|---:|
| 7 | 13 | 2,365 / 35,632 | **CERTIFIED UNSAT** | 21.6 (50 % quota) | 5.3 (600) | 2.6 |
| 7 | 14 | 3,653 / 60,439 | **CERTIFIED UNSAT** | 1,316.7 | 169.8 (1900) | 163.5 |
| 8 | 15 | 5,980 / 173,410 | **CERTIFIED UNSAT** | 1,822.3 | 193.4 (1900) | 175.7 |

Hashes (CNF; LRAT with bytes; `.zst` with bytes):
- flat n7m13:
  - CNF `31c1a9c4e3201a1b6f5510dc3147492b1eb9bd215749637aea1b1f165b449cde`
  - LRAT `1252bd1bf06f6a00173fcc4b72c869bb1aee3d8039ae36f862f4e1e74aec7f75` (106,078,467)
  - `.zst` `23c47f9809ee1bcc465c99de549c9c9d065230d2b1c21bef8d2e8362acb1ae58` (32,124,929)
- flat n7m14:
  - CNF `2c21e961eed77944bf868b2fe31456708550cc9c1f71eb89532c15a80c6ad617`
  - LRAT `d226fff86c9e67d4666e0a2dbaec75dde812ed612b85ffb0d43833d5205e0d7b` (5,352,801,321)
  - `.zst` `948852c326f9379bc936851521f8d9cc68825f34fbf94a29b9487d92c4f5092c` (1,554,275,700)
- flat n8m15:
  - CNF `63a14b8fd77d80dc3676df8216f8a7ae02ee129d86cd3abde1b1a4e65918584b`
  - LRAT `2635218cc0f2399a2cfe982d1ebf92c2bc5efed30e9bfc751c9b4f2147317312` (5,626,002,566)
  - `.zst` `ae3e6b0bcb14f921cbbe7d3aaf9ccc562bdb3bf73294a8e9fd6cb40c43124187` (1,615,140,359)

### 5.3 Main encoder, smaller sizes (consistency; certified by the run's cake only)

The verifier did not re-run cake on these sizes. With its own encoder it certified n = 6 at 4–12 and n = 8 at 14 (§5.4).
n6m7, n7m8 and n8m9 are trivial (§2). The table was generated from `runs/{small,n6,n7_m12}/*.jsonl`. Each row asserts the
exact verdict line, and the `.zst` hashes come from `ZST_SHA256SUMS`.

| n | \|S\| | verdict | CNF SHA-256 | LRAT SHA-256 | .zst SHA-256 |
|---|---:|---|---|---|---|
| 6 | 7 | CERTIFIED UNSAT | `f3c374ed9c5cf836de5fd2502d4c92d627ac4e700a292fed5da0e5bb5cd2effb` | `35f52248c4b52c30b67952f279cd7d06e4f6ba846d857036a4b13bd708fe9b4d` | `d22ef300df16e7b82e3d961b5a7d3c509ac274a0af44d5a8b61264fd157414b5` |
| 6 | 8 | CERTIFIED UNSAT | `1d1345c2192fd1f666143289e46426c4d1dd576979cdd0f006b7b262815df732` | `969725a92947dcbfc3aec0e4e08a63f4059cd1f9f7d222fe9eb763b8f81265c8` | `20008cc47a6c611bee005f33677608cc21ac49dba09f499d3a310879c881bd66` |
| 6 | 9 | CERTIFIED UNSAT | `026b3c11fd8bec05ac2618987f029bea742b0a8e2d8152ccb2b5cbf9133c9772` | `f66713880cb673cd1a86f0ab8753122a0c9bc9c7e3f74437be08c7789e27b4b0` | `ad5250846c520187a9914bf264ce86a78397c9f375f7cea6e7f01a7534eafe9e` |
| 6 | 10 | CERTIFIED UNSAT | `d9ae63eba8a775d22ca41afd936614c8bff2df59fd126ff8988366b82e04da9b` | `7482ff9c125cf3a2a3648c8552bcc5d9aff903a20d82276a57159a20d871e463` | `a2652f4a315ce8f6692bdd27b6a18bf6175da8aad9a8a2a4b078184ba72ee3e6` |
| 6 | 11 | CERTIFIED UNSAT | `ad44e921892090021c4e60a28a83416c0045af798e34773530516474e63fde5d` | `ccc30274cc0d63a07d93f2bae35a31ddb3c142b8418ff5f33292b46937e99e7e` | `58ea418e1d47518f7d7c4fa8120fe324b6be2620a127fa933bfc2710945a2597` |
| 6 | 12 | CERTIFIED UNSAT | `edf390add68a6abd442295d261f078ce2fe8b19af3aab43cfcc54fc58446ab2a` | `c8fd0bfb933c1d72f94a603c786b89916b169b4ba5b168a7d0dac098ea1f286e` | `5e171bf821ce2c1321f9518aa96044cd8738ace472129ee9feea2627fe2bea60` |
| 7 | 8 | CERTIFIED UNSAT | `51e84247619a731d10e7dfd44d9708609f5d7320e09be41222581d9b1149bc75` | `19ac1f554126a6dd738af443d6f11510188056e8e028ca1bd0f3562bf02dd454` | `e8e4f1bae8e0cddbc91352b161fe465b83a2ddc1390162c19c8cf9ab5309f268` |
| 7 | 9 | CERTIFIED UNSAT | `f7ae051417dee4916c7d990e6d858a6b80524b71d8d05b73e376817c29595ec3` | `5923b5692d898c3a646d9d778de2eada2d6ce6047b5b24816f625e194b08ba1c` | `dc03000726144fec764dc460659c018836e19ad17959f69e321ffd56d3372b7c` |
| 7 | 10 | CERTIFIED UNSAT | `047983050a21c5e7d1c05fb1d4d8ec78b474c3b82432f9da791e576b396fd601` | `7248cf644d457700ca599fc7bad87c0a1a3d3788380db82b00e4d4265222b192` | `a866bdd274371aea2777d14a32ac9966c46ba369b2a1582e45338dbb89cf62ba` |
| 7 | 11 | CERTIFIED UNSAT | `9aa58a443eb01297b993b65fb18be85ceac3588231615bdf46e8bb1bc52fb143` | `a354e8fe3793e81069130f2c735010e856c886321723dfe00035fe019f48edc2` | `c7aa72a6fcbb366a8a3a3bead9b9bebd57dd5786eb419ccdf254665c0d7d6121` |
| 7 | 12 | CERTIFIED UNSAT | `89040466cdc3cba9153f91ff1b925756452bd8c3c6b263b15c96f5059a698f63` | `c381a89b56cb32eb5f69e5b55915872e93014de399574a306f7c55a614d756b9` | `a02ce2fcc959ba8f110a8a610fc4c5474a6539ef4f8a1b6fc7d91aebea954808` |
| 8 | 9 | CERTIFIED UNSAT | `df3a4cc6cbe2d65828230702c9d4801994c4e44111ab32ded0948f93bff164cd` | `f1f5d89db1a53758be5a3b2aa23e70437d9c6f073ce88a5d8cb6c0ea0015f76d` | `5e5c77142a111afdf00dc87b8921b1b02d74c23926c2dd3225f7d263b0f91089` |
| 8 | 10 | CERTIFIED UNSAT | `2e6a820e361a1abbc446a536841be85d65afbe3185f638b3ad7c55f7e45bf524` | `28d0d2530ee4285a8c856eedccd27d0b68bb20ec2b4d4089e06bb97fbd15afd2` | `22dc3c35c6b2b4962c2a57a0a829a63ab0b81dc22a97db5a510b1bed05ea04fb` |
| 8 | 11 | CERTIFIED UNSAT | `09ed2c46c8123c5c302365bb5f8856f5bb448fa3739f0ed0767454641bbcc59a` | `60b9cf562957b4bab97e2aadf4054b131252eefceb7d06da1ac5ecbf8b188dea` | `32bf631cdf1f6201b9f3c6485b6afc03aef045ba727a481d1294b0ed37ed1083` |
| 8 | 12 | CERTIFIED UNSAT | `e73d49d5e86b32c0bd577362c960cb36ee7f6866b2aa76de2c7fdf538185aa76` | `a0fb4f44cf01c94bff33ccab9ab0c67b4d9b2670357219e4cd7ba746400f12c8` | `471049e4b162230ebb592db38f2e62f7c3eafbe4366847df6908286e1546cc43` |
| 8 | 13 | CERTIFIED UNSAT | `6576b437565752b0f77becba28095c2a620f5dc7766b71e2f880c3471b00122a` | `9f71269971a7bc42dc9225171941f26158df59225ef6d8dfc2555b1ad5cc89c7` | `0049f688ab84af474ce712409e7e78c27fc0ef8e33a490085305a4ce2478423f` |
| 8 | 14 | CERTIFIED UNSAT | `046ba94a86baecfbe310ea095d5450de0440d13b7a76088531b2ea3d5a7e462c` | `e4fe0635fa088a10ba71620e2ed176197834f835376c880aa16ee87af7e9b67a` | `1b5e06e3923b4090480351c2c7e736c97120b1b87f5a037df62e1a02fbee111c` |

Per n, this gives:
- **n = 6:** |S| ≤ 12 holds (CERTIFIED; sizes ≤ 7 are trivial). |S| = 13 fails (§5.5).
- **n = 7:** |S| ≤ 14 holds (CERTIFIED here, and in `ROUND2.md`). |S| = 15 is UNKNOWN.
- **n = 8:** |S| ≤ 15 holds (CERTIFIED; sizes ≤ 9 are trivial).

### 5.4 Verifier's lemma-free encoding (`conjts-verify/enc/`)

| case | vars / clauses | verdict | CaDiCaL s | CNF SHA-256 | LRAT SHA-256 | .zst SHA-256 |
|---|---|---|---:|---|---|---|
| n6 m12 hyp | 5,093 / 34,785 | **CERTIFIED UNSAT** | 5.2 | `65179926f3edef2dee85e226b705808aaf8d667b715ae8001579f846892b0c6f` | `4719f525355dd005fa7473e2185df67beec21def9821e49d13fb520b047c503a` | `8edf59e9b741d8407ae1cdf63f4b465e05a3a3fd8168bfd16a007c83c69593f4` |
| n7 m13 hyp | 16,995 / 128,441 | **CERTIFIED UNSAT** | 33.4 | `5369e5e9d9aad5052c98ee3cfcf2f25bb5552e1be6367377b967f9763c78871f` | `e8788d1914d66437da1dd90a79d875bab9dada1dd47609025777c0d99aeaae58` | `2aaa292e7f4dbe6398bbe4b92b1c0dce71e78caaeb0b6d363951929678df34bd` |
| n8 m14 hyp | 58,357 / 489,960 | **CERTIFIED UNSAT** | 192.5 | `2f66fb4b2f29a0056188f97177ff11a74f83e9698eaa7f4952d0a29103b2b140` | `9b9bf638c5a8d672119285f562631882ada82eab794d5845cb6bda8e774ab467` | `04951c0589a4fc7c38dddca13f170f2951ac5ad10107f680dd1ed44068bfa77b` |
| n6 m13 hyp | 8,415 / 60,725 | SAT; the model is a counterexample by brute force (gons_U 114) | 4.6 | `9d0d79a89f0e2346a68e344b1fbab4ba22dd690bab5cc9fc878006a48facb22e` | — | — |
| n6 m13 nohyp | 8,195 / 60,284 | SAT; the model is a counterexample by brute force (gons_U 69) | 3.3 | `6f12ec869e64e7eb8d28e3ba3b6c3b0c923c477fe4137841d72fed4b356cab18` | — | — |

- n = 6 at m = 4–11 is CERTIFIED UNSAT as well (`enc/small_run.jsonl`, with each CNF and LRAT hash).
  - m = 4–7 are trivial: those CNFs contain the empty clause (checked by grep).
  - The LRATs for m = 5–7 are empty (SHA-256 `e3b0c442…`).
- The verifier recorded only the uncompressed LRAT hashes. The writer of this file computed the `.zst` hashes in the
  table at 09:33 KST.

### 5.5 n = 6 at |S| = 13 (side result; EXACT for abstract signotopes)

- **Models.** The main encoder is SAT in hyp and in nohyp mode, and so is the flat encoding. The three models are
  lattice-hyp, lattice-nohyp and flat-hyp.
  - Their names are in `analysis/n6_models.txt`. The sign strings are in `controls/controls.jsonl` and
    `runs/flat/flat.jsonl`.
  - Their pairwise Hamming distances are 85, 5 and 88.
- **Checks.** In each model:
  - S is a signotope with 0 five-caps and 0 convex hexagons;
  - r ends a 4-cap;
  - none of the 4,096 subsets of U is a terminal-safe weak Δ.

  `src/check_conjts.py` checked this, and the verifier's own checker checked it independently. The gons_U counts are
  117, 108 and 92 for lattice-hyp, lattice-nohyp and flat-hyp. The 4-subset and cap/cup convexity definitions agree on
  every subset of size 4–7 of all three models (`analysis/convex_agree.py`).
- **More models.** The verifier's own encoder found two more 13-point counterexamples, one in hyp and one in nohyp mode.
  The sign strings are in `enc/enc_run.jsonl`, and its brute force confirms both.
- **What still holds.** In the two main-encoding models, U still has a rooted weak Δ: {0,2,3,5,6} in lattice-hyp and
  {0,1,3,4,6} in lattice-nohyp. A rooted weak Δ is a weak Δ A of U with A + r 4-cap-free. S also has a weak Δ. Only
  the r-independent terminal-safe form fails.
- **Least failing size.** 13 is the least failing size:
  - sizes 7–12 are CERTIFIED (§5.3);
  - sizes 4–12 are also CERTIFIED by the lemma-free encoder (§5.4);
  - every signotope on ≤ 7 labels agrees with the brute force (control 1).
- **Realisation.**
  - Here: five heuristic runs failed (DELTA2N `tools/realize.py`; `analysis/realize_n6.jsonl`). This is not evidence
    either way.
  - Later, the main session found integer realisations of all three models and checked them exactly
    (`VERIFY_ATN_MAIN.md`, 09:12 KST). Label: EXACT, own code. No second party has checked them yet.

## 6. Controls (`controls/controls.jsonl`: COMPUTED solver verdicts compared with an exact brute force)

1. **Every signotope on 6 and 7 labels** (908 and 24,698, own enumeration), for n = 5, 6, 7 and both modes. The CNF under
   the orientation assumptions agrees with the brute force in 908/908 and 24,698/24,698 cases for every n. No
   counterexample exists at these sizes.
2. **S19** is the record's U18 plus attack 2's top point r, with the signs fixed.
   - The nohyp formula is SAT. The decoded model equals S19's signs, and U = U18 has no terminal-safe weak Δ.
   - The hyp formula is UNSAT, because r ends no 4-cap.
   - The verifier confirmed S19 independently: it is valid, r ends no 4-cap, there are 402 gons and 0 terminal-safe weak
     Δs (`enc/s19_check.json`).
3. **Real point sets at the main sizes, run against the exact main CNFs.** The sets are 160 random m-subsets of the real
   valid pools (DELTA3N `resume/selection/data/real_pool/full-n7.pool` and `full-n8.pool`), 40 each at (13,7), (14,7),
   (15,7) and (15,8). In 34–37 of each 40, r ends a 4-cap. Every set has a terminal-safe weak Δ, and both CNFs are UNSAT
   under its orientations: 160/160 agree.
4. **SAT side.**
   - The n = 6, |S| = 13 models of §5.5 are SAT instances that the checkers confirm.
   - The universal formulas for n = 5 (m = 8) and n = 6 (m = 9–12) are UNSAT in both modes.
5. **Verifier's cross-test** (`xtest/xtest.jsonl`).
   - With orientations fixed, the main encoder agrees with the verifier's brute force on 101 of 101 13-point signotopes
     at n = 6, in both modes. These are the 5 models plus every single-flip neighbour that is still a signotope; 28 of
     them are counterexamples. So the encoder is neither too weak nor too strong where both outcomes occur.
   - The verifier's own encoder passed its self-test, 58 of 58 in both modes, with 19 counterexamples.

## 7. Independent verification (`/home/jay/research/data/roadmap-20261115/conjts-verify/`): verdict **sound**

- **cake_lpr re-run** (`cake/cake_rerun.jsonl`). cake_lpr printed the exact line `s VERIFIED UNSAT`, checked with
  `grep -x`, on all six headline certificates. Each CNF SHA-256, and each SHA-256 of the decompressed LRAT, equals §5.1
  and §5.2. Times: 2.1, 103.2 and 107.8 s for the main proofs; 2.6, 163.5 and 175.7 s for the flat ones.
- **Regeneration.** The three main headline CNFs regenerate byte for byte from the recorded source (`xtest/xtest.jsonl`).
- **Soundness note and encoder.** Lemma A, Lemma B (including the D = ∅ case) and both directions of the Theorem are
  correct.
  - The diff is exactly the stated one, and `compact_cnf.orig.cpp` equals the DELTA3N file.
  - In conjts mode the Q flags exist for all subsets, and `children()` throws if a child flag is missing.
  - The A and B flags are filled only by the new families.
  - The Q4 clauses are exact under the signotope axioms.
- **Lemma-free re-derivation** (§5.4). CERTIFIED at n = 6 for m = 4–12, at n = 7 for m = 13 and at n = 8 for m = 14. SAT at
  n = 6, m = 13 in both modes. This confirms n7m13 and the n = 6 boundary (12 holds, 13 fails) without Lemma A or
  Lemma B.
- **Models.** The verifier's own brute force confirms all three n = 6 models and the S19 control (§5.5, §6).
- **Issues raised.**
  - Wording, minor: "two independent encodings" means independent code only. At n7m14 and n8m15 the result rests on the
    written Lemma A, Lemma B and 4-subset convexity, which the verifier checked and found correct. It does not rest on a
    second, lemma-free derivation. This file uses the corrected wording.
  - Process, minor, with no effect on the evidence: see §10.
- **Not checked by the verifier:**
  - realisability of the n = 6 models;
  - the n7m15 UNKNOWN;
  - n = 7 at m = 8–11 and n = 8 at m = 9–13 with its own encoder. cake_lpr was not re-run on these either.

**Checks by the writer of this file** (09:33–09:36 KST, hash checks and greps only, no solver):
- All 40 cake output files of the run and the verifier contain the exact line `s VERIFIED UNSAT` once (`grep -cx`).
- `sha256sum -c` against `ZST_SHA256SUMS` passed for the 9 kept archives in `runs/n7_m12`, `runs/n7_m13`, `runs/n7_m14`,
  `runs/n8_m15`, `runs/n6` and `runs/flat`. The `runs/small` archives were not re-hashed.
- The n7m15 CaDiCaL log has no `s` line and ends with SIGTERM.

## 8. Files and hashes

The run's work dir is `/home/jay/research/data/roadmap-20261115/conjts/`, and the verifier's is
`/home/jay/research/data/roadmap-20261115/conjts-verify/`. Neither has been copied into the repository yet.

| file | SHA-256 |
|---|---|
| `conjts/README.md` (run report) | `dd4cf3a937b34e47b2c7b0f26277c44a1ae2df783387dcdaedf7431490bdb7d0` |
| `conjts/CONJTS_SOUNDNESS.md` | `b9a2ea3c9ccf129d460dcff7b20fc7c9530baf709896bdcf9f59e94288178d3d` |
| `conjts/SHA256SUMS` (all small files) | `49f4fd1fe63174a699e0305b610f19044aa5929568e8188902e74f2a381fee28` |
| `conjts/ZST_SHA256SUMS` | `067da7807192f63ee1436f2830c8dbcd000deb9a82465ce8d4f44ef45874a39f` |
| `conjts/src/conjts_cnf.cpp` | `a9bb34d3fc6dd13dd42fd318f069eff8f1c67c2a148886722b46308a1303a121` |
| `conjts/src/conjts_cnf.diff` | `43073d95478f01c4e9b0f0a08342b5ece41854d6abb18eaa193983f8097553fd` |
| `conjts/src/compact_cnf.orig.cpp` | `1964e17b777fd7b7a973f12b2911c003a050047f13a621f523a9f98c6e31d553` |
| `conjts/src/flat_cnf.py` | `a6f8223f3963a65b838e6f8b71cbb4e896081fe6cb45749af2db3b0ad935e3e2` |
| `conjts/src/check_conjts.py` | `e859339301c708649fe5a9b4baae36ad6c55ddc37311f4e59c19e225cc1acc02` |
| `conjts/src/controls.py` | `560fe28a5c6608389ea39ca3c08acb1f626081b64ffc6432c811c97c4735af60` |
| `conjts/controls/controls.jsonl` | `431da3d16f033ed117f27f26e0656a46e8c34470b077b8407a6e0a41d063440f` |
| `conjts/runs/flat/flat.jsonl` | `cbce29951fd9358df2b69ef5cf6cff7390d02a382a2f13da36a8e4e65923521f` |
| `conjts/analysis/n6_models.txt` | `1573b8afbf806c2c1df3633acee7c7cab5d6396a5b644a3c060955dfabc3566d` |
| `conjts-verify/enc/my_conjts.py` | `648176d9b3791fb90bbb1669794f28e0f6d7a9dc2251c52912903ca655a8ebd9` |
| `conjts-verify/cake/cake_rerun.jsonl` | `8b994514cde5f8c940fc96e34b0f8836cec78e05e6b5506cda9a89a2c810771f` |
| `conjts-verify/enc/enc_run.jsonl` | `1853e7de9c0d20b725cb06cdb55f750effbc830d832d3d03c7272d5bf0162c6b` |
| `conjts-verify/enc/small_run.jsonl` | `aeaa03e3657ef3f7f64766308842c619d27520d3376174349161e23851b40b1c` |
| `conjts-verify/xtest/xtest.jsonl` | `11b29b2063df93a3c8ada013455ee4ccd4c1436a908f79dfa17e57d7c9255a54` |
| `conjts-verify/enc/s19_check.json` | `7ed290795c64c221968734dfd4cea43031d6b85f8607fa2485cdd6a6ee75ee30` |

The kept proofs are the `.zst` files listed in §5. Keep every one until an outside re-run.

## 9. What remains

- **n = 7 at |S| = 15 is UNKNOWN.**
  - The runtime grew ×73 from 13 to 14 points. That suggests roughly 15 h or more of one thread for an UNSAT proof
    (HEURISTIC), so a cube split would be needed.
  - Real counterexamples to CONJ-TS′(7) have 15–19 points (S19′) [superseded 15 Nov pm (STATUS20261115_1900,
    Corrections item 4): the least real counterexample has 15–17 points (claim cts7-real-17, V1 CONFIRMED)]. By analogy with n = 6, whose first failure is at
    2n+1, a counterexample at 15 points is plausible (HEURISTIC).
- **Lemma-free certificates at n7m14 and n8m15** with the verifier's `my_conjts.py`. Expect hours per instance on one
  thread.
- **Outside re-run and copy.** The m = 14 and m = 15 LRATs need an outside re-run. Then copy `conjts/` and
  `conjts-verify/` (tools, jsonl logs and kept `.zst`) into a repo record.
- **Second-party check** of the n = 6 realisations in `VERIFY_ATN_MAIN.md`.
- **Rooted form.** "S valid and r ends a 4-cap ⇒ U has a weak Δ A with A + r 4-cap-free" is being tested elsewhere
  (`ROOT6_MAIN.md`, `ROUND6.md`). The n = 6 counterexamples here satisfy it.
- **Partial LRAT.** Deleting the 22.9 GB `runs/n7_m15/cts_n7_m15.lrat` needs the owner's OK.

## 10. Process notes

**Run.**
- The memory guard stopped `esr-agx-cts-flat` at 1001 MB. cake had run at heap 1000 inside a 1000M unit, a sizing error
  against the 80 % rule. It was a clean stop, not an OOM kill. The cake was redone as `flatcake` at heap 600 and was
  accepted.
- From 06:13:40 to 06:15:55 the summed MemoryMax was 3064M, over the 3 GB allocation, because of the 64M watcher.
- To fit short extra units, the run changed its own units' limits at runtime: `sathunt` to 50 % CPUQuota, and `chainA`
  MemoryMax to 600M and then 530M.
- Short foreground checks of a few seconds each briefly put one thread over the allocation.
- No git action, no repo write, no foreign unit touched, no web request.

**Verifier.**
- `esr-agx-cv-enc` ran at 100 % CPUQuota for about a minute while the summed quotas were 16.2 threads. It was lowered to
  80 % at runtime, and raised again once threads were free.
- One foreground check of about 1 s ran outside a unit.
- The peak was 2 cake units of 2600M each.
- No git action, no repo write, no foreign unit touched.

**Writer of this file.**
- Ran only greps and hash checks, about 10 s on one thread at nice 10, while `cpu_free.sh` reported 6 free threads.
- Wrote only this new file. No git action.

## 11. Resume commands

```bash
cd /home/jay/research/data/roadmap-20261115/conjts
g++ -std=c++17 -O2 -Wall -Wextra -pedantic src/conjts_cnf.cpp -o src/conjts_cnf
./src/conjts_cnf --m 15 --n 7 --conjts hyp --out cnf/cts_n7_m15.cnf --map cnf/cts_n7_m15.map   # deterministic
systemd-run --user --unit=esr-<track>-<job> -p CPUQuota=100% -p MemoryMax=600M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=<s> --nice=10 --working-directory=$PWD /bin/bash src/solve.sh cnf/cts_n7_m15.cnf runs/n7_m15
# cake: heap 1900 sufficed for the 3.3-5.6 GB proofs; give the unit MemoryMax >= heap/0.8 (e.g. 2400M)
bash src/cake.sh cnf/<f>.cnf runs/<case>/<f>.lrat runs/<case> 1900
# lemma-free encoder (n7m14 and n8m15 not yet run): python my_conjts.py enc <m> <n> hyp|nohyp <out.cnf>
cd /home/jay/research/data/roadmap-20261115/conjts-verify/enc
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python my_conjts.py enc 14 7 hyp my_n7_m14_hyp.cnf
```
