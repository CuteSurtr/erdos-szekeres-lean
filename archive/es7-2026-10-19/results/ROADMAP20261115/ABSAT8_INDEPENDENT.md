# ABSAT8_INDEPENDENT: independent encoder for the ABSAT8-core one-point-extension test (track L1, 15 Nov 2026)

## 1. Status (14:21 KST, final for this session)

- **CERTIFIED: all 28 CNFs of the new, independently written encoder are UNSAT.** CaDiCaL 2.1.3 produced an LRAT
  proof for each, and cake_lpr printed exactly one line `s VERIFIED UNSAT` for each (28/28). CNF and LRAT SHA-256
  are in §5, and the LRATs are kept as zstd.
- **PROVED: soundness.** If a real point can be added, the CNF has a satisfying assignment. "Can be added" means: in
  general position, with no convex octagon through it, to any realization of the order type. The written proof is
  in §3.
- **Geometric reading: CERTIFIED computation plus PROVED soundness** (computer-assisted, unrefereed). Take any of the
  28 order types, any realization of it and any point in general position. Adding that point always creates a convex
  octagon through it. So no 65-point octagon-free set in general position contains a 64-point subset of one of these
  order types. This replaces the COMPUTED label of ROADMAP20261115 §6 for these 28 order types.
- **Verifier V1 CONFIRMED claim `absat8-l1-indep` at 13:56 KST**
  (`/home/jay/research/data/roadmap-20261115/pm1115/claims/absat8-l1-indep.verdict.json`, report
  `VERIFY_ABSAT8_INDEPENDENT.md` in this folder).
  - V1 checked the §3 proof by hand.
  - V1 checked the hashes and the exact `s VERIFIED UNSAT` lines (28/28).
  - V1's own C++ regenerated R2 + AC + OCT, with convex 7-gons found by a different method (x-sorted cap/cup
    split). The result equals every certified CNF as a clause set (28/28).
  - V1 tested 32 exact real points and reproduced the comparison with absext.
  - V1 did not re-run cake_lpr, because heap 1000 MB exceeds its budget.
  - My second cake_lpr pass at heap 300 MB (unit `esr-abs-l1-heap`, 13:58 KST, `$L1/bin/heaptest.sh`,
    `$L1/logs/heaptest.log`, `$L1/heaptest/*.cake.out`) again printed exactly one `s VERIFIED UNSAT` per proof
    (28/28), with peak RSS about 310 MB. So an independent re-run fits in a 400M unit. It is not independent itself.
- **Verifier V3 CONFIRMED claim `absat8-l1-cake-rerun` at 14:01 KST.** V3 ran its own script in its own 400M unit
  (`VERIFY_ABSAT8_CAKE_RERUN.md`). cake_lpr at heap 300 printed exactly one `s VERIFIED UNSAT` per proof (28/28), and
  the CNF and LRAT hashes match. So the 28 LRATs have now been re-run independently.
- **Same model as the original probe, and the CNFs are equivalent to it.** On every one of the 28 sets the
  acyclicity and octagon clause families are identical as clause sets. The rotation families differ in their
  encoding but have the same solutions point by point, enumerated with a SAT solver (COMPUTED, reproduced by V1; §7
  says why they must agree). So the two CNFs have the same solutions on the pair variables.
- **Controls: 933/933 passed** (§6), including 1,098,381 exact real points on the 28 certified CNFs, every one of
  which lies on a convex octagon.
- **Scope.** The statement covers these 28 order types only. It says nothing about ES(8) = 65 beyond them.
- **Extension (§11): the seven 7-fold order types of `PRIMEFOLD` §3.**
  - All 8 CNFs (7 types) are UNSAT, CERTIFIED.
  - The chirotopes are exact, and the same soundness applies.
  - V3 CONFIRMED claim `absat8-l1-sevenfold` at 14:19, with its own exact chirotope, its own encoder and its own
    cake_lpr re-run.
  - So none of the 7-fold symmetric 64-point sets extends to a 65-point octagon-free set (for all realizations of
    these order types). [corrected 15 Nov pm (C1 issue 20): read "none of these seven order types", the seven listed
    in §11 (as §11 says "none of these 7-fold symmetric 64-point sets"); nothing is claimed for other 7-fold symmetric
    64-point sets]

Work dir: `/home/jay/research/data/roadmap-20261115/pm1115/l1/` (below `$L1`).

## 2. Statement

Let S be one of the 28 named 64-point sets of the ABSAT8-core probe. The sets are the 17 pilot sets, the walker end
sets w1-w3, and the 8 octagon-free vertex deletions `ae_d<v>` of AlphaEvolve's 65-point set. The files are
`probe1/absat/sets/*.txt`, copied to `$L1/sets/` with identical SHA-256. Each S has exact integer coordinates
(up to 57 bits) and no three collinear points (checked exactly).

**Theorem (CERTIFIED + PROVED).** Let S' be any point set with the same labelled order type as S, and let p be a
point such that S' ∪ {p} is in general position. Then S' ∪ {p} contains a convex octagon with p as a vertex.

## 3. Model, encoder and soundness

**Model (the original probe's, determined from its README and code).** The model is a general order-type extension,
not a signotope with a fixed x-position:

- the unknowns are the orientations χ(a,b,p) for all pairs a<b of S, with no x-order constraint on p;
- the constraints are the necessary conditions R2, AC and OCT below.

By Las Vergnas' characterization of single-element extensions, the solutions of R2 + AC are exactly the acyclic
uniform one-element extensions of the oriented matroid of S. That is a remark and not needed for the theorem.

**Variables.** X(a,b) for 0 ≤ a < b < 64 is true iff orient(a,b,p) > 0, and it is numbered 1 + its
lexicographic rank, so there are 2,016 variables and no auxiliary variables. orient(a,b,c) is the sign of
det(b−a, c−a), with '+' meaning counterclockwise. The literal "orient(a,b,p) > 0" is X(a,b) for a<b and ¬X(b,a)
for a>b.

**Clause families of `l1enc` (`$L1/src/l1enc.cpp`).** These are written from the definitions. The original
`absext.cpp` was read only after these CNFs were certified.

- **R2 (rotation at each point a; 3,782 clauses per point, 242,048 in all).**
  - For x ≠ a, let d_x = x − a and ε_x = +1 if d_x lies in the half-open upper half-plane (y > 0, or y = 0 and
    x > 0), else −1. Let u_x = ε_x d_x.
  - Sort the 63 vectors u_x by angle in [0, π), comparing by the exact sign of det(u_x, u_y).
  - Let S_x be the literal "s_x = +", where s_x = ε_x·orient(a,x,p).
  - For each i and each k ≥ i+2 the encoder emits two clauses, (¬S_i ∨ S_{i+1} ∨ ¬S_k) and
    (S_i ∨ ¬S_{i+1} ∨ S_k). Before emitting them it checks exactly that det(u_i,u_{i+1}), det(u_{i+1},u_k) and
    det(u_i,u_k) are all > 0.
  - The clauses say that s_i = s_k forces s_{i+1} = s_i. On a sequence of m signs this pattern has exactly the 2m
    solutions with at most one switch (brute-force self-test, m = 1..16). Proof: two switches at the first two
    switch positions i < l give s_i = s_{l+1} ≠ s_{i+1}.
- **AC (acyclicity; one clause per triangle, 41,664 in all).** For a<b<c with σ = orient(a,b,c), the clause says
  that orient(x,y,p) has sign σ for at least one of the edges (a,b), (b,c), (c,a). In words: p is on the side of
  the third vertex for at least one edge line.
- **OCT (no convex octagon through p).**
  - `l1enc` enumerates every convex 7-gon Q of S once: from its lowest vertex, in increasing angle, with left
    turns, and with the "closable" pruning, which is valid because every prefix of a convex polygon closes to a
    convex polygon. A brute-force self-test on 200 random 6-11-point sets checks the counts.
  - For each cyclic 4-chain (q_{i−1}, q_i, q_{i+1}, q_{i+2}) of each Q in ccw order, it emits
    (¬sees(q_i,q_{i+1}) ∨ sees(q_{i−1},q_i) ∨ sees(q_{i+1},q_{i+2})), where sees(x,y) means orient(x,y,p) < 0.
  - The clause depends only on the chain, so chains are deduplicated with a bitset.
  - The encoder aborts if S itself contains a convex octagon (except with `--allow-kgon`, used for one control).

**Soundness theorem (PROVED).** Let p be a real point with S ∪ {p} in general position, and let α_p be the
assignment X(a,b) = [orient(a,b,p) > 0]. If S ∪ {p} has no convex octagon through p, then α_p satisfies every
clause. So if the CNF is UNSAT, every such p lies on a convex octagon.

*Proof.* The three families are treated in turn.

- **R2.**
  - Fix a and an emitted triple (i, i+1, k). The exactly checked signs give u_{i+1} = λu_i + μu_k with
    λ = det(u_{i+1},u_k)/det(u_i,u_k) > 0 and μ = det(u_i,u_{i+1})/det(u_i,u_k) > 0 (Cramer's rule).
  - With w = p − a, linearity gives det(u_{i+1}, w) = λ·det(u_i, w) + μ·det(u_k, w).
  - Also det(u_x, w) = ε_x·det(x − a, p − a), so sign det(u_x, w) = ε_x·orient(a,x,p) = s_x.
  - So if s_i = s_k, then s_{i+1} has the same sign. The two clauses state exactly this, for '+' and for '−'.
- **AC.**
  - Write p = λ_a a + λ_b b + λ_c c with λ_a + λ_b + λ_c = 1 (barycentric coordinates).
  - Then p − b = λ_a(a − b) + λ_c(c − b), so det(c − b, p − b) = λ_a·det(c − b, a − b). This means
    sign orient(b,c,p) = sign(λ_a)·σ, and likewise for the other two edges.
  - If p were on the opposite side from the third vertex for all three edges, then λ_a, λ_b, λ_c < 0, which
    contradicts λ_a + λ_b + λ_c = 1.
- **OCT.** Let Q = (q_0..q_6) be a convex 7-gon in ccw order, with edges e_j = q_j q_{j+1}, outward unit normals
  n_j and support function h(u) = max_{q∈Q} ⟨u, q⟩. Then "p sees e_j" ⟺ ⟨n_j, p⟩ > h(n_j).
  - *(i) Visibility lemma: the visible edges form a cyclic interval.*
    - The set A = {u ∈ S¹ : ⟨u, p − q⟩ > 0 for all q ∈ Q} is the trace on the circle of an open convex cone C.
    - C ∩ −C = ∅, so A is empty or an open arc.
    - Edge e_j is visible ⟺ n_j ∈ A.
    - The normals n_0, …, n_6 of a convex polygon go once around the circle in this cyclic order, so the j with
      n_j ∈ A form a cyclic interval.
  - *(ii) Slot lemma.* Suppose the clause for (Q, i) is violated: p sees e_i but not e_{i−1} and not e_{i+1}. By
    (i), e_i is the only visible edge.
    - p is the unique maximizer of ⟨n_i, ·⟩ over Q ∪ {p}, so p is a vertex of conv(Q ∪ {p}).
    - For each q_j, at least one incident edge is not visible; say e_j (the case e_{j−1} is symmetric). Then
      ⟨n_j, p⟩ < h(n_j) = ⟨n_j, q_j⟩, with strict inequality by general position.
    - Take a direction u in the open normal cone of q_j (the arc between n_{j−1} and n_j) close enough to n_j.
      Then ⟨u, q_j⟩ exceeds ⟨u, q⟩ for every other q ∈ Q, and by continuity it also exceeds ⟨u, p⟩.
    - So every q_j is a vertex of conv(Q ∪ {p}), and Q ∪ {p} is a convex octagon through p.
  - Hence when there is no octagon through p, no OCT clause is violated. ∎

**Order-type invariance (PROVED).** The CNF is computed from the coordinates of S, but every clause stays valid for
any realization S' of the same labelled order type.

- **AC** depends only on σ = orient(a,b,c).
- **OCT** depends only on which 7-subsets are in convex position and on their ccw cyclic order. Both are decided by
  orientation signs, through the 4-point test and orient(q_i, q_j, q_k) > 0 for i < j < k.
- **R2** uses the numbers ε_x, which depend on coordinates. For S', put v_x = ε_x(x' − a') with the same ε_x.
  - Then det(v_x, v_y) = ε_x ε_y orient(a', x', y') has the same sign as det(u_x, u_y).
  - So Cramer's rule again gives positive λ', μ', and the R2 proof goes through unchanged for any p' in general
    position with respect to S'.

So α_{p'} (computed in S') satisfies the CNF of S whenever S' ∪ {p'} has no octagon through p'. With the
certified UNSAT this proves the theorem of §2. ∎

**Abstract reading (remark, not checked here).** In the abstract model the OCT clauses are also implied by "no
abstract convex octagon through p". The reason: a violated clause involves the 8 elements Q ∪ {p}, and every uniform
acyclic rank-3 oriented matroid on 8 elements is realizable (Goodman–Pollack). So UNSAT also excludes abstract
(pseudo-configuration) extensions, as the original probe stated.

## 4. Method

- **Encoding:** `$L1/bin/l1enc sets/<name>.txt 8 cnf/<name>.cnf`, about 0.13 s per set; the stats are in
  `$L1/logs/encode_stats.jsonl`.
- **Certification:**
  - Ran in unit `esr-abs-l1-cert` (CPUQuota 60 %, MemoryMax 1500M, MemorySwapMax=0), 13:33:17-13:33:36 KST.
  - `$L1/bin/driver_cert.sh 1000` runs, for each set, `certify_cnf.sh cnf/<name>.cnf cert 1000 --keep`. That is the
    house script (sha256 `a5ff0d8f…`, unchanged), with CaDiCaL 2.1.3 (sha `4acf5860…`) and cake_lpr (sha
    `c14ff498…`) at heap 1000 MB. The AE deletions ran first.
  - The driver itself greps `^s VERIFIED UNSAT$` in each `cake.out`. Peak RSS was 632-753 MB, under 51 % of the
    unit's limit.

## 5. Results (28/28 CERTIFIED)

Every CNF has 2,016 variables, 242,048 R2 clauses and 41,664 AC clauses. The table gives the total clause count,
the OCT clauses, the original absext CNF's clause count, the LRAT size, and the SHA-256 of the CNF and of the raw
LRAT. "lines" is the count of exact `s VERIFIED UNSAT` lines in `cert/<name>.cake.out`. My OCT count equals absext's
slot count and my convex 7-gon count equals the probe's on all 28 sets (`$L1/summary_l1.tsv`).

| set | group | clauses | OCT | orig clauses | LRAT bytes | CNF SHA-256 | LRAT SHA-256 | lines |
|---|---|---|---|---|---|---|---|---|
| ae_d0 | AE deletion | 384321 | 100609 | 150209 | 80695 | `6f1e5dc2ca828fdd10b15d78ec814a377d775d8e79e4f0fa86d12c3e3db82d50` | `4fb3751c410ddb0561265353b1cd62aa97f4db93118c6b82040ac276a95b904d` | 1 |
| ae_d1 | AE deletion | 384321 | 100609 | 150209 | 79583 | `0483afa145d75bbdf339db0f65f875fa5b1f13a1daed538823c699ecf01aaed8` | `39af4a54e79ee0cad83ec98b67d1edb7838beec30febb94bf9da3c1c309bcbff` | 1 |
| ae_d15 | AE deletion | 384718 | 101006 | 150606 | 58635 | `00653e693ee82310bd238724634da4fd44dbc50a44d67579b48efe7d77be8797` | `464c40e8bc08dd094fa2632bc73c7d471a6fe1948f5da7fb2d9ee45a3adb4931` | 1 |
| ae_d23 | AE deletion | 384197 | 100485 | 150085 | 49370 | `8419ae3098f4cf8bf92ed3d5acb6b49cb3047cf6e5dd154aaab6f2b30ccf57e1` | `8c7ae07457d1a2fd310aa9a9fe88c28393e01cad156e4bf837c251c6644bc388` | 1 |
| ae_d27 | AE deletion | 384321 | 100609 | 150209 | 53802 | `c7349210af75411b61989c880db18f03dc3be37fcb934ccba7002fa240355f20` | `b3edf12a19eb808a0834234bc64f38fdd02012f3e03d7d4556e07ec247b1959b` | 1 |
| ae_d29 | AE deletion | 384197 | 100485 | 150085 | 49270 | `dd98c56d819b93b983b3d84a5825c20a704eacdff4ce768eed297f079fde3002` | `f81b568cc6b4f92bb6766fd72040376c188959f87664430c91e73d382ef67237` | 1 |
| ae_d30 | AE deletion | 384321 | 100609 | 150209 | 108556 | `6fe0739761c23617db61bf7706bf0a344263d6e3a6003a9416aeffa836d73209` | `22b107e8bea4177ba028a5a1a03807dd3b2a15d94a12cf746f963f2bdecff244` | 1 |
| ae_d57 | AE deletion | 384718 | 101006 | 150606 | 39027 | `9225447e9b0102ded6245db565a03e3afe92c4aa46b5f95db0198c4007ec79e3` | `7555c581638e5e10519eac3ac08438ecbecea945638ee8883aa453760a6aa0db` | 1 |
| c2_64points_k8 | pilot | 373076 | 89364 | 138964 | 80160 | `00ed93fa217f459e90f2e835ddaf848e5df057adcb96f4f6c3d767fee332226e` | `62b9d689e64d51d20fcf7752c5dd0e1f117153ca73fb5d7705d646eb3b33ede7` | 1 |
| c2_64points_k8_bb | pilot | 357630 | 73918 | 123518 | 126356 | `e06887637335716b97f3f7a8d4e0c3ac7f02200a2252d66ba242fb20527440e4` | `8dc6438b17b4f4b55193520f81fcbe9a56506880beed0efe0b37c302f26aa235` | 1 |
| ot0000 | pilot | 438548 | 154836 | 204436 | 44927 | `2d5768ff89bfd0ae1dc12609b1472d6e5b4c1df8c29e09b59e3ce86d559af325` | `f3feff5e6082dee7eecacb15acc5eb4c8441dce2df6584448b92df42014baace` | 1 |
| ot0174m | pilot | 376520 | 92808 | 142408 | 52205 | `d1be012f5e2887b9578e80a3a757a54384dbc5a6ae0933bc8591d42fa75e69c8` | `b6f154a0f3bc54850a631c8bc4027f863e261fcdc2edce9745bb79ffc535099c` | 1 |
| ot0341 | pilot | 433364 | 149652 | 199252 | 108120 | `e0515a6df015c405999e5746e6675ea52673d2bf26ff104164abd888be9a5ed1` | `d0c8b7d458af44fdb74ff0d1bfe1c0d5dacc17fc96ffe072045d3ccaa4de825a` | 1 |
| ot0550 | pilot | 383744 | 100032 | 149632 | 29388 | `4adc4710f3900a449c554acd7ae4b67803efd8b4ec73634822dff464009ec8f7` | `2cb66221b84bcc7ec89532886a64dd11e05959595d6c81294232d25b8325f1d4` | 1 |
| ot0682 | pilot | 431853 | 148141 | 197741 | 74515 | `c3ebe11d8e6ef3d46950e62537dce4ee830d0f23bbfdf92c1ade3c5b79de8903` | `67833a5f1f585a94c6da5361e114fb99f07f2c4987b45c463c83379f427b967d` | 1 |
| ot0822 | pilot | 417733 | 134021 | 183621 | 42389 | `9d9653c2fee9e88e7f2d5f58bdf99a688ce4dba3975d785dc750a671afb72f1b` | `152a086558e8afede57d76bd2beed60a66dfd94cf869c78b28399146f48f1011` | 1 |
| ot0977 | pilot | 388096 | 104384 | 153984 | 98234 | `f3d60c4a26ee2db446c3ab928598f5dba15bf02fb7041d25b807d2b85bb1ac55` | `2a6995606a2bc221c0e4652a820aba44eb53e206d6805ba478130e2f85719d1d` | 1 |
| ot1150 | pilot | 411675 | 127963 | 177563 | 38972 | `6dbc6a0496e94079beb7420ffe50fb743b25caf5ab651cf2ecabf11195e6e7b2` | `d199701b3b01aca759c3855dac419cf559d50ccdefd12c19efe9ca945e86afab` | 1 |
| ot1313 | pilot | 386328 | 102616 | 152216 | 61281 | `0f7540075d5653123b90ac5ecdbc594583908c80cb24e03c0f36f83cd2a51c15` | `400b0667ef8ad59812690d75add52cb70f7c5d05c4bc9526b33d071451b6c585` | 1 |
| ot1451 | pilot | 420579 | 136867 | 186467 | 104103 | `98ccbb05d55988e23d688dc45ee3aae6b1df8e8fd7d783a61c062bc174262733` | `9ac209d57b184931b10e5e667d317f9e419f32d70a4a0e3b2718b1d44ec4734b` | 1 |
| ot1588 | pilot | 407380 | 123668 | 173268 | 85848 | `792f3be5087063e443daca9ff05523c635d8c7b96589301a04c8aaed647ea39e` | `696859c83d86de7559da66a7536c44af5d85220e8491d463c4dcae5cc5cd7f0d` | 1 |
| v2w21_last_set | pilot | 388790 | 105078 | 154678 | 50827 | `7917865a728e24c6ce8ae76cafdbe8fa7081d7cf38fc4325496aff77c3688392` | `aa62fca8c0236d8cd2001aa3856ac46a839bce6f4ab9887d7ebe9b75665f1ad1` | 1 |
| v2w22_last_set | pilot | 401219 | 117507 | 167107 | 102205 | `a0d7493ac55e54885a80cbebb54989d98b6cb36f6307ecd64eaeca24efc75492` | `649551aac1342e4f964b5a3802a0603834c71c66c6e914d0490e638c7e9c76ce` | 1 |
| v3w31_last_set | pilot | 397441 | 113729 | 163329 | 41113 | `6b564a06a88b441e7734009b32c58a7ced07a040ab8f54d6c102063ce848e0b7` | `28ca6f212493e74b9f3f90b1d331f23006cd19bab55ba53c97c4ade35d3b034a` | 1 |
| v3w32_last_set | pilot | 382786 | 99074 | 148674 | 95881 | `9b081e303ec46cdf7dd499188c8baccf34a7a2947b1c83e55478e4b19d182a36` | `a5509ae252b539652f0ef9216878fc18f2aac89451e92f79aa876b464c799e4b` | 1 |
| w1_last_set | walker end set | 391836 | 108124 | 157724 | 124102 | `0f16134681a8988d44adeae06c06fb07326b0db155668c34bdeae95d370d5ce5` | `dcf5a19afb4fc7d3f0a0edafb9bc6dd6ef308d263e0a6dfce7faf864f6d377f9` | 1 |
| w2_last_set | walker end set | 404816 | 121104 | 170704 | 105190 | `771d3dedef463a4445eaad4f8307d2e3c3289a37de25532487fbd5ebac173f34` | `5e9aaf0b624e52e245f060628b3c47c1c2b929907dcee210e2ee977092747fe5` | 1 |
| w3_last_set | walker end set | 415977 | 132265 | 181865 | 56993 | `4ce78bdc63388ff64d0a46891b920eab0cec7deae19b0bfd1e2f267d634816e8` | `8d2b4ccdc545313131e1f52f9acddfe58259233c420656419665ed4d9459b40a` | 1 |

## 6. Controls

All controls passed, with 0 failures. `$L1/controls/controls.jsonl` (final sha256 `5e24f6a6…`) has 1,003 lines: 933
for the 28 sets (this section) and 70 for the 7-fold sets (§11). The 28-set controls ran in
units `esr-abs-l1-ctrl` (13:40-13:47) and `esr-abs-l1-ctrl2` (13:47-13:57), both at CPUQuota 100 % and MemoryMax
1500M. Every point is evaluated in exact arithmetic (GMP in `l1check`).

`l1check` decides "convex octagon through p" by its own dynamic program over convex chains around p, without using
the CNF or `l1enc`'s polygon enumeration. A self-test checks it against brute force on 600 random cases: 446 with a
K-gon through p, 154 without.

- **C2: the sets are octagon-free (EXACT, 28/28).**
  - The dynamic program finds no convex octagon in any of the 28 sets, and `l1enc`'s own count agrees (convex8 = 0).
  - On `ae65` it finds exactly the octagon vertices {0, 1, 15, 23, 27, 29, 30, 57}, as the probe reported, and no
    9-gon.
- **C5: octagon clauses dropped (28/28 SAT).** With R2 + AC only, CaDiCaL says SAT on every set.
- **C4: AlphaEvolve's 65-point set (65/65).** For each vertex v, the CNF of ae65 − v is evaluated at the real point
  v.
  - *v on the octagon (8 cases).* The CNF is byte-identical to `cnf/ae_d<v>.cnf`. v violates no R2 or AC clause and
    exactly 1 OCT clause, and the dynamic program finds the octagon through v.
  - *v off the octagon (57 cases).* ae65 − v contains the one octagon (convex8 = 1, encoded with `--allow-kgon`). v
    violates no clause at all, so a real point satisfies the CNF (EXACT). The dynamic program finds no octagon
    through v, and CaDiCaL says SAT.
  - These are full-size 64-point positive controls with the same structure as the AE deletions.
- **C3: delete and re-extend (672/672).** S − w is re-encoded and evaluated at the real point w.
  - The cases are 8 deletions per set (w = 0, 8, …, 56) and all 64 deletions for the 8 AE sets.
  - In every case w satisfies every clause (EXACT), the dynamic program finds no octagon through w, and CaDiCaL says
    SAT.
- **C1 and C1b: real points on the 28 certified CNFs (each point EXACT; coverage HEURISTIC).**
  - C1, per set: 1,000 random points in the bounding box enlarged by half its size on each side, 100 far points,
    and one point in each of the 126 wedges at each vertex (p = q + (u+v)/2^40 for angularly consecutive rays u, v).
  - C1b uses new seeds with 20,000 random and 2,000 far points plus the wedge points.
  - Together: 1,098,381 points with 3 degenerate points skipped.
  - None violates an R2 or AC clause. Every one has a convex octagon through it and violates at least 1 OCT clause
    (between 1 and 46,189), and there are 0 mismatches between "OCT violated" and the dynamic program.
  - This agrees with the certified UNSAT. A point with no octagon would have been a counterexample.
- **C7: both directions of OCT (56/56).** On the subsets S[:40] and S[:48] of each set (octagon-free), 2,000 random
  points, 200 far points and all wedge points were tested.
  - 336,863 points were tested and 33 degenerate ones skipped.
  - 280,006 points have an octagon through p, and each violates at least 1 OCT clause.
  - 56,857 have none, and each satisfies every clause.
  - There are 0 mismatches and 0 R2 or AC violations, and all 56 subsets show both outcomes.
- **Encoder self-tests.** `l1enc --selftest` checks that the R2 pattern is exactly "at most one switch" (m = 1..16,
  brute force) and that the convex k-gon counts match brute force on 200 random 6-11-point sets.
- **LRAT cores (COMPUTED, information only).** The 28 proofs reference 1,792-5,640 original clauses each:
  935-3,021 R2, 104-1,194 AC and 734-2,130 OCT (`$L1/logs/lrat_core.tsv`). So the obstruction uses about 1-2 % of the
  octagon clauses.

## 7. Comparison with the original encoding (`absext.cpp`, read after certification)

| item | original `absext` | `l1enc` (this record) |
|---|---|---|
| model | general order-type extension (acyclic uniform one-element extension) | same |
| pair variables | X(a,b), lexicographic, orient(a,b,p) > 0 | same numbering |
| auxiliary variables | 64 (one "type" variable per point) | none |
| rotation family | "Las Vergnas" monotone chain: 2 × 62 clauses per point, signs normalised against the first other point b0 (chirotope only), the type variable picks the direction | 3,782 clauses per point (i, i+1, k pattern), normalised against the x-axis, no auxiliary variable |
| acyclicity | 41,664 clauses | 41,664, **identical clause set** |
| octagon clauses | slot clause per 4-chain of a convex 7-gon | same family, **identical clause set** (built by separate enumeration code) |
| size, e.g. ae_d0 | 2,080 vars, 150,209 clauses, 2.5 MB | 2,016 vars, 384,321 clauses, 6.5 MB |

`$L1/src/compare_orig.py` makes the following comparisons on all 28 sets (lines `C6_compare_orig` in
`controls/controls.jsonl`):

- the AC blocks are equal as clause sets: **28/28**;
- the OCT blocks are equal as clause sets, with 0 clauses only in mine and 0 only in theirs: **28/28**;
- for every point a, my R2 block and their LV block, with its type variable projected out, have the same solutions
  on the 63 variables X(a,·). Each block has exactly 126 = 2·63 projected solutions, enumerated with Glucose4 and
  blocking clauses: **64/64 points on 28/28 sets** (COMPUTED). It is also clear why: both encode "the '+' signs form
  an arc of 63 consecutive signed directions around a", cut at different reference directions;
- each type variable occurs only in its own block (asserted).

So the two CNFs have the same solutions on the pair variables. This explains why both are UNSAT. It also means the
independence lies in the code (convex-polygon enumeration, slot generation, rotation encoding, numbering) and in the
proof, not in a different mathematical model.

## 8. Files and hashes

- `$L1/src/l1enc.cpp` `410375484c709b16c51b6ed0f90110908238018679a64e883df59b2b1d3cd41e` (binary
  `60fee0ce…`), `$L1/src/l1check.cpp` `0f5a03e9933d88311bbb6c15ea47d97e30a6d47a2cef9a10608bcdf8d09df019`,
  `$L1/src/compare_orig.py` `6389c5cc…`, `$L1/src/controls.py` `b979c727…`, `$L1/src/controls2.py` `991c609e…`,
  `$L1/bin/driver_cert.sh` `fb0dcb96…`, `$L1/bin/l1check` `12a7d6f4…`.
- `$L1/cnf/<name>.cnf` (28, 179 MB), `$L1/cert/<name>.lrat.zst`, `.cake.out`, `.cadical.log`,
  `cert/certify.jsonl` (sha256 `7e43cc43…`), `summary_l1.tsv` (`5dc9455d…`), `sets/sets.sha256` (`0c1ddada…`).
  The 29 input files are identical to the probe's `inputs.sha256` entries.
- Control CNFs: `$L1/controls/{nooct,ae65,del,sub,del7}/*.cnf.zst` (680 MB in all); results
  `$L1/controls/controls.jsonl`; logs `$L1/logs/`.

## 9. What remains

- Done: the independent cake_lpr re-run of the 28 LRATs (V3, CONFIRMED 14:01). The house rule allows the proofs to
  be deleted now, but that is the owner's call. They are small (29-126 KB each), and nothing was deleted.
- Outside this track:
  - the 7 seven-fold types: done in §11 (CONFIRMED by V3);
  - the walker end sets beyond w1-w3 and v2w21-v3w32 do not exist on this machine. ES8SAT kept the last sets of the
    Mac walkers only, and all 7 of those are among the 28;
  - the value check on a DDSZ saturated set of non-maximum size (arXiv:2312.01223). DDSZ's construction is a limit
    construction ("sufficiently small" ε and δ). It needs an explicit instance first, then an exhaustive exact
    geometric saturation check over the faces of the line arrangement, then this encoder at the matching k. A
    starting point is n = 7: 28 points, built from DDSZ's explicit 8-point (4,5)-cup-cap-saturated set. This was not
    attempted here, as it is outside this track;
  - radius 1 (delete one point, add two);
  - a literature check before any "new" wording.

## 10. Resume

```
cd /home/jay/research/data/roadmap-20261115/pm1115/l1
g++ -O2 -std=c++17 -o bin/l1enc src/l1enc.cpp && ./bin/l1enc --selftest
g++ -O2 -std=c++17 -o bin/l1check src/l1check.cpp -lgmpxx -lgmp && ./bin/l1check --selftest
for n in $(cat names28.txt); do ./bin/l1enc sets/$n.txt 8 cnf/$n.cnf; done     # byte-identical CNFs (hashes §5)
systemd-run --user --unit=esr-abs-l1-cert -p CPUQuota=60% -p MemoryMax=1500M -p MemorySwapMax=0 -p RuntimeMaxSec=3600 \
  --working-directory=$PWD $PWD/bin/driver_cert.sh 1000
systemd-run --user --unit=esr-abs-l1-ctrl -p CPUQuota=100% -p MemoryMax=1500M -p MemorySwapMax=0 -p RuntimeMaxSec=10800 \
  --working-directory=$PWD /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -u src/controls.py
```

## 11. Extension (14:10 KST): the seven 7-fold order types

ROADMAP SYNTHESIS §2.4 listed these as the untested ABSAT8 item. They are `PRIMEFOLD` §3's sets, the P1 objects.

**Status:**

- **CERTIFIED: all 8 CNFs (7 order types) are UNSAT.** Each `cake.out` has exactly one `s VERIFIED UNSAT` line.
- **The order types were identified exactly** by interval arithmetic plus exact integer checks.
- **The same PROVED soundness of §3 applies.**
- **Verifier V3 CONFIRMED claim `absat8-l1-sevenfold` at 14:19 KST** (`VERIFY_ABSAT8_SEVENFOLD.md`; verdict file
  `/home/jay/research/data/roadmap-20261115/pm1115/claims/absat8-l1-sevenfold.verdict.json`).
  - V3 computed its own exact Z[ζ7] chirotope (group ring plus a rigorous integer enclosure of 2cos(2π/7)). It
    equals all 8 `.chi` files, and every integer realization, including the 80-bit one, has the same signs.
  - V3's own encoder reproduces all 8 CNFs as equal clause multisets. Its convex 7-gon counts equal `PRIMEFOLD` §3.
  - V3's own cake_lpr run at heap 300 printed exactly one `s VERIFIED UNSAT` per proof (8/8).
  - V3 re-derived §3. It did not re-run controls S1-S3.
  - V3 also noted that the 14:08 version of this section said "V1 CONFIRMED" before any verdict existed. The author
    corrected that at 14:12.

**Statement.** The theorem of §2 holds for each of the following order types, all in `PRIMEFOLD/sets/k8/` (SHA-256
equal to `PRIMEFOLD/SHA256SUMS`):

- `c7_64pts_small`;
- `c7_64pts_9layers_centre`;
- `c7_64_own_s1000`;
- `c7_64pts_9layers_centre_own`;
- `p7_compound_64`. `p7_two_orbit_64` has the identical labelled chirotope, checked with `cmp`, and was certified
  separately;
- `rule_p7_64pts`;
- `m7_x2_G9s_centre`.

In particular, none of these 7-fold symmetric 64-point sets (Z[ζ7] coordinates) extends to a 65-point set in general
position without a convex octagon.

**Method.**

1. **Exact chirotope (`$L1/src/z7chi.py`).**
   - Points are Σ_j w_j ζ^j with ζ = e^{2πi/7}.
   - All 41,664 signs of det(b−a, c−a) are computed with mpmath interval arithmetic (`mpmath.iv`, 300 bits). Each
     interval excludes 0, and plain 600-bit `mpf` gives the same sign every time.
   - The lower bounds on min |det| are 1.46, 2.16e17, 2.64, 3.07e4, 1.00e9, 9.99e9, 2.36e13 and 1.13e22. They agree
     with the 200-digit values of `K8EXACT20261106`.
2. **Integer realizations.** The 600-bit coordinates are rounded at scale 2^s:
   - s = 7 for `c7_64pts_small` and `c7_64_own_s1000`;
   - s = 0 for the other five 44-bit-or-smaller sets;
   - s = −20 for `m7_x2_G9s_centre` (`$L1/src/z7int_big.py`), which gives 80-bit coordinates.

   Every rounded set has exactly the interval chirotope. This was checked twice: with Python integers in the scripts,
   and by `$L1/src/chi_of_int.cpp` (GMP), whose output is byte-equal to the `.chi` files.
3. **Encoding.**
   - The six sets with ≤ 44-bit coordinates were encoded with the unchanged `l1enc`.
   - `m7_x2_G9s_centre` was encoded with `$L1/src/l1enc_big.cpp`. This is `l1enc` with GMP coordinates and the same
     algorithm. Its output is byte-identical to `l1enc`'s on all 35 integer sets of this record
     (`$L1/logs/big_vs_small.txt`).
4. **Certification.** `certify_cnf.sh` at heap 1000 MB, in units `esr-abs-l1-cert7` (14:03) and
   `esr-abs-l1-cert7b` (14:04), with peak RSS 671-896 MB.

**Why the result holds for the real 7-fold sets.** The CNF depends only on the labelled chirotope (§3, invariance).
Each integer realization has the same labelled chirotope as its Z[ζ7] set (exact). So every point that could be added
to a Z[ζ7] set gives a model of the certified-UNSAT CNF, and there is none.

**Results.** Each CNF has 2,016 variables, 242,048 R2 clauses and 41,664 AC clauses. My convex 4-gon and 7-gon counts
equal `PRIMEFOLD` §3's table, which was computed from exact algebraic signs, for all 7 types. The convex 8-gon count
is 0 in every set.

| set | clauses | OCT | convex 4-gons | convex 7-gons | CNF SHA-256 | LRAT SHA-256 | lines |
|---|---|---|---|---|---|---|---|
| c7_64pts_small | 401,718 | 118,006 | 416,052 | 4,688,763 | `d71670fd65a7162f17e7d56c3d9892548d06a62728a07c0c02dcca9863367615` | `666eda8317dbe80364249496722db88fdf670cbb62c6526bc9bd43ae5510379e` | 1 |
| c7_64pts_9layers_centre | 402,614 | 118,902 | 416,220 | 4,691,381 | `c1bbddfd4a82868f761447456aeb2e4322037d35b6fcf1aa4791cdcf27ad915c` | `c8baa25cac30bd7b231404bc270b3558decf50cd7885d65d429e14b6e58d60f2` | 1 |
| c7_64_own_s1000 | 389,524 | 105,812 | 392,966 | 3,328,145 | `8037c8ce91ac57ca853f46e22388a47474f4561b3806e2bf5458edf292c3f0e6` | `3575dce40e932778adaed760849da21d87a0c186d0ae62598d2652c7591d13d2` | 1 |
| c7_64pts_9layers_centre_own | 387,872 | 104,160 | 392,553 | 3,252,475 | `78dd444fcd7a08c1584a4bc4309f1549994847d804dd6f549db9e12545efcd47` | `f317f3c7a983d1629fa3719140bf562ce2904952a621401cccd1ae334457a061` | 1 |
| p7_compound_64 | 459,545 | 175,833 | 470,764 | 18,396,499 | `b18115606184170a5a4fbb674ee6a1cb244e1c406bf65b0f3b0e53851d44c305` | `5af25b0990aefdf92b81377c95f1f81dc2fd53bd055e6bc5df17aab6138fbc68` | 1 |
| p7_two_orbit_64 | 459,545 | 175,833 | 470,764 | 18,396,499 | `38102de02e10bd1054d89f813d75e48b2d07ab1179d66f70cea16fdcb26355cc` | `c3e82e824ddb46a6bd2156f974207690f75d02df3fd3931f279b12929a9bc1ee` | 1 |
| rule_p7_64pts | 528,075 | 244,363 | 487,711 | 30,031,745 | `c3c793113f8a62c5296d4d78328e08156e9c13fae5a9519d57b62a82131c6875` | `b40182ddbac0f81627a7783da421aa544edefcefbc17e5994b009d44be4410c7` | 1 |
| m7_x2_G9s_centre | 466,748 | 183,036 | 462,581 | 14,719,287 | `8b55f59cb43c3f47c90aa003f4a1fa16bc8aa1cc3407e27ea984fae31b93d38e` | `e623edf168a1d783cc88f243993296d7207a7f71b0b903fed9a0048143f06f8a` | 1 |

**Controls (`controls/controls.jsonl`, lines S1-S3, unit `esr-abs-l1-ctrl7`): 70/70 passed.**

- **S2: octagon-free.** The dynamic program finds no octagon in any of the 7 integer realizations with ≤ 44-bit
  coordinates.
- **S1: real points.** 94,948 real points were tested (13,564 per set: 5,000 random, 500 far and all wedge points).
  Every one lies on a convex octagon. There are 0 R2 or AC violations and 0 mismatches between "OCT violated" and the
  dynamic program.
- **S3: delete and re-extend.** 56 cases (w = 0, 8, …, 56). Each deleted point satisfies every clause of its CNF
  (EXACT), and CaDiCaL says SAT.
- **Not sampled.** The 80-bit realization of `m7_x2_G9s_centre` is beyond `l1check`'s 64-bit input. Its encoder is
  covered by the byte-identity check.

**Files.**

- `$L1/sets7/*.pts` (copies), `.chi`, `.int.txt` and `m7_x2_G9s_centre.bigint.txt`;
- `$L1/cnf7/*.cnf`, and `$L1/cert7/*.lrat.zst`, `*.cake.out`, `certify.jsonl`;
- hashes of every new file in `$L1/logs/sevenfold_hashes.txt`;
- `$L1/logs/z7chi.log`.
