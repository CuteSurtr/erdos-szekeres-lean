**Verdict: CONFIRMED** (claim `absat8-l1-indep`, verifier V1, 15 November 2026, 13:55 KST). (a) CERTIFIED as recorded:
verdict lines and all hashes check, but cake_lpr was not re-run by V1 (its 1000 MB heap exceeds V1's 400 MB budget while
another V1 unit runs). (b) PROVED: the §3 soundness proof and the order-type invariance argument are correct. (c) follows
from (a) and (b). (d) COMPUTED: reproduced on all 28 sets with V1's own code.

# VERIFY_ABSAT8_INDEPENDENT: independent check of the L1 encoder, its 28 certificates and its soundness proof

## Claim checked (filed by track L1)

(a) The 28 CNFs of `l1enc.cpp` (8 AlphaEvolve vertex deletions, 17 pilot sets, walker end sets w1-w3) are UNSAT, each
with a CaDiCaL 2.1.3 LRAT accepted by cake_lpr. (b) Soundness for real points (§3 of `ABSAT8_INDEPENDENT.md`).
(c) Hence, for each of the 28 order types, adding any point in general position to any realization creates a convex
octagon through it. (d) The AC and OCT families equal the original probe's absext clause sets, and the rotation
families have the same per-point solutions (126 each).

## 1. The soundness proof (§3), checked by hand

- **R2.** For an emitted triple (i, i+1, k) the three determinants det(u_i,u_{i+1}), det(u_{i+1},u_k), det(u_i,u_k)
  are > 0, so Cramer's rule gives u_{i+1} = λu_i + μu_k with λ = det(u_{i+1},u_k)/det(u_i,u_k) > 0 and
  μ = det(u_i,u_{i+1})/det(u_i,u_k) > 0. With w = p − a, det(u_x, w) = ε_x·det(x − a, p − a), so its sign is
  s_x = ε_x·orient(a,x,p), nonzero by general position. Then s_i = s_k forces s_{i+1} = s_i, which is exactly the
  clause pair. Correct. (The "2m solutions" remark concerns strength, not soundness.)
- **AC.** With barycentric p = λ_a a + λ_b b + λ_c c, det(c − b, p − b) = λ_a·det(c − b, a − b) and
  orient(b,c,a) = σ, so sign orient(b,c,p) = sign(λ_a)·σ; cyclically for the other edges. All three of sign −σ would
  give λ_a, λ_b, λ_c < 0 against λ_a + λ_b + λ_c = 1. Correct.
- **OCT.** (i) A = {u : ⟨u, p − q⟩ > 0 for all q ∈ Q} is the trace of an open convex cone with C ∩ −C = ∅, hence empty
  or an open arc shorter than π; edge e_j is visible iff n_j ∈ A; the normals of a convex polygon are in cyclic order,
  so the visible edges form a cyclic interval. (ii) A violated clause means e_i is visible and e_{i−1}, e_{i+1} are not,
  so by (i) e_i is the only visible edge. p is the unique maximiser of ⟨n_i, ·⟩, so a vertex. Every q_j has a
  non-visible incident edge, say e_j, so ⟨n_j, p⟩ < ⟨n_j, q_j⟩ (strict by general position); a direction u in the open
  normal cone of q_j close to n_j makes q_j the unique maximiser over Q ∪ {p}. So Q ∪ {p} is a convex octagon through p.
  "sees(x,y) ⟺ orient(x,y,p) < 0" is right for a ccw edge (interior to the left). Correct.
- **Order-type invariance.** AC uses σ only; OCT uses the convex 7-subsets and their ccw order, both decided by
  orientations. For R2 with S′, v_x = ε_x(x′ − a′) keeps the ε_x of S, and det(v_x, v_y) = ε_xε_y·orient(a′,x′,y′) has the
  sign of det(u_x, u_y); the proof only uses those three signs, not that the v_x are angle-sorted. Correct.
- So α_p satisfies every clause whenever S′ ∪ {p} (general position) has no convex octagon through p, and with UNSAT the
  §2 theorem follows. No gap found.

## 2. Certificates (`v1_certs.py`, output `v1_certs.out`)

For all 28 names in `names28.txt`: exactly one line equal to `s VERIFIED UNSAT` in `cert/<name>.cake.out`; the CNF SHA-256
equals `certify.jsonl`, `summary_l1.tsv` and the record table; `zstd -dc cert/<name>.lrat.zst | sha256sum` and the byte
count equal `certify.jsonl`, `summary_l1.tsv` and the record table; every CNF header has 2,016 variables and the recorded
clause count. **28/28, 0 mismatches.** The 28 inputs `sets/<name>.txt` equal the probe's
`lower8/probe1/absat/inputs.sha256` entries (28/28), and `sets.sha256` checks 29/29.
**Not done:** a cake_lpr re-run (see the verdict line). The author's run used heap 1000 MB with peak RSS 632-753 MB.

## 3. Independent regeneration of the clause families (`v1enc.cpp`, all 28 sets)

`v1enc.cpp` was written from §3's definitions before reading `l1enc.cpp`, `l1check.cpp` or `compare_orig.py` (none of
them was read). Exact arithmetic: coordinates in int64, determinants in __int128 (inputs up to 57 bits).
- R2 and AC follow the §3 definitions (sort by exact determinant comparison, then assert det(u_i,u_k) > 0 for all
  i < k; ε_x from the half-open upper half-plane; literal "orient(a,b,p) > 0" = X(a,b) for a < b, ¬X(b,a) for a > b).
- **Convex 7-gons by a different method from the author's angular sweep:** sort the points lexicographically by (x, y)
  (a tiny rotation of the x-direction, which preserves orientations), enumerate every cap (orient < 0 on consecutive
  triples) and every cup between each leftmost/rightmost pair, and join a c-point cap with a (9 − c)-point cup. Every
  polygon is asserted ccw-convex on all 7 consecutive triples; for the first 2,000 polygons of each set no point lies
  in a triangle of three others (brute force). OCT = (¬sees(q_i,q_{i+1}) ∨ sees(q_{i−1},q_i) ∨ sees(q_{i+1},q_{i+2})),
  deduplicated.
- The input is also checked for collinear triples (none).

Result (`v1enc_all.out`, SHA-256 `905e26be…ecde0`): on **all 28 sets my R2 ∪ AC ∪ OCT equals the certified CNF as a
clause set: 0 clauses only in mine, 0 only in theirs**; every CNF clause has 3 literals and none is repeated; R2 has
242,048 clauses (3,782 per point), AC 41,664, and my convex 7-gon and OCT counts equal `summary_l1.tsv` on every set
(for example ae_d0: 1,766,547 seven-gons, 100,609 OCT clauses; ot0000: 4,720,996 and 154,836). So each certified CNF is
exactly the formula whose soundness §1 checks.

## 4. Exact real-point samples (`v1enc SET CNF k seed`)

Random integer points p in the bounding box enlarged by half its size on each side, kept only if S ∪ {p} is in general
position. For each p: evaluate every clause under α_p, and independently count the convex 7-gons Q of S for which the
exact convex hull of Q ∪ {p} has 8 vertices.
- 32 samples (8 on ae_d0, 12 on ot0000, 12 on c2_64points_k8_bb): **R2 and AC violated 0 times; "some OCT clause is
  violated" equals "an octagon through p exists" in 32/32**; every sampled p lies on at least one octagon (1 to
  2,121,441), as the theorem says. One ae_d0 sample has exactly one violated OCT clause and exactly one octagon.
- Outputs `v1_samples_ae_d0.out` (`788a6f59…`), `v1_samples_ot0000.out` (`478c493d…`), `v1_samples_c2bb.out`
  (`8623453a…`).

## 5. Part (d) against the original absext CNFs (`v1_lv_compare.py`, all 28 sets)

Inputs: `lower8/probe1/absat/cnf/<name>.cnf` and my dumped families. For each set: the absext clauses without a type
variable (variables ≤ 2,016) equal my AC ∪ OCT as clause sets; each typed clause contains exactly one type variable; and
for each point a, the block with type variable 2,017 + a uses only X(a,·) and that type variable, and its solutions
projected onto the 63 variables X(a,·) (enumerated with Glucose4 and blocking clauses) equal those of my R2 block for a.
**28/28 sets: identical AC ∪ OCT; 64/64 points each with 126 = 126 projected solutions and equal sets** (outputs
`v1_lv_compare.out`, `v1_lv_compare_all.out`). This reproduces (d) with V1's own code (label COMPUTED, as claimed).

## 6. Remarks

- The record's §6 "Controls" is still the placeholder `CONTROLS_PLACEHOLDER` (C1/C3 were running at filing time). Nothing
  in (a)-(d) depends on it.
- (c) covers exactly these 28 labelled order types (and, by reflecting everything, their mirror images); nothing beyond.
- The "abstract reading" remark of §3 (Goodman-Pollack) was not checked; it is not part of the claim.

## Code and outputs (`/home/jay/research/data/roadmap-20261115/pm1115/v1/absat8-l1-indep/`)

| file | SHA-256 |
|---|---|
| v1enc.cpp | `0ac24dde1c9bfba301df38d5bc7213b95dbfb33cc37b77e92935d7c94e488b05` |
| v1_certs.py | `29eaa51317f7742fbcfc063911c72df594496ea68c4fed17ed27063f6f4062c6` |
| v1_lv_compare.py | `020d4c745bb80bc4e2c1dbcbdfb7324d31873a8d9658a8677800e6490f60afbf` |
| v1_certs.out | `6759807933ddd9a616f98669cdb06e51b5825fec98211510d98cdb4d102bef64` |
| v1enc_all.out | `905e26befafdd84f5863ebaa12cd88f0c80c0a91073042f1a06121da622ecde0` |
| v1_lv_compare.out / _all.out | `c699da90…546014a` / `083db6dd…733895` |

Rerun: `g++ -O2 -std=c++17 -o v1enc v1enc.cpp; ./v1enc $L1/sets/<name>.txt $L1/cnf/<name>.cnf [k seed]`
(about 1 s per set); `python3 -I v1_certs.py`; `v1enc ... <prefix>` then `v1_lv_compare.py <absext.cnf> <prefix>` (venv
python with pysat). All foreground, single thread, under a minute each. No git action, no other repository file written.
