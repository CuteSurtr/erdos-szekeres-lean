# VERIFY_C-ae33-radius1_rebuild (independent verifier, lens REBUILD, slot ae33, 21 Nov 2026, 21:15-22:05 KST)

**Verdict: all seven claims CONFIRMED.** The family and real-pair checks were rebuilt with my own code, the CNFs
regenerated, and the 203 kept proofs re-run with a fresh cake_lpr. No error was found in any claim. Labels as claimed:
- CERTIFIED: the 203 UNSAT verdicts;
- EXACT: inputs, regeneration, family equality, real pair;
- PROVED: soundness and corollary (written deduction).

The whole result is computer-assisted and unrefereed. It is support evidence for ES(7) = 33 and changes no bound.

| key | verdict | decisive evidence (own) |
|---|---|---|
| ae33-r1-203-certified | **confirmed** | fresh cake_lpr (heap 600 MB): output is exactly the one line `s VERIFIED UNSAT`, 203/203. The CNF is my regenerated file, whose SHA-256 equals 4 recorded hashes; the decompressed kept LRAT's SHA-256 and size equal `certify.jsonl` and `hashes_203.tsv` |
| ae33-r1-regen-exact | **confirmed** | `l2enc.cpp` rebuilt byte-identical. All 203 CNFs regenerated from my own base files hash-equal the 3 recorded sources (plus the worker's tsv). The stats line is equal except the working-directory path (§1.2) |
| ae33-r1-families-exact | **confirmed** | my own C++ generator `tools/fam.cpp`: all 10 blocks of all 203 CNFs are equal as multisets, as is the whole CNF. 223,165,944 clauses; convex7 = 0; 0 shortenable GP/RAD clauses; 0 JK tautologies |
| ae33-inputs-exact | **confirmed** | own `tools/inputs.py` (Decimal, exact): every listed fact reproduced; counts also by a C++ full brute force |
| ae33-realpair-exact | **confirmed** | own evaluator: exactly 1 violated clause per CNF (JK 21 / OCTX 57 / OCTY 125, none in R2..GP). Exactly one 7-gon in B ∪ {u, v}, and it maps back to H |
| ae33-r1-soundness-proved | **confirmed** | own family-by-family re-derivation (§2). Identities exact on 2,000 random tuples. Semantic controls that could fail: SAT direction 8/8, 8,600 + 6,097 random real configurations, 0 violations |
| ae33-r1-corollary | **confirmed** | written deduction (§2.8), as strong as its three inputs, all confirmed |

## 0. Independence: what I read, ran and wrote

- **Read:**
  - `L18/copied/l2enc.cpp` (all of it);
  - LOWERBOUND_RUN_1118.md (all of it, §(2) closely) and ABSAT8_INDEPENDENT.md §3;
  - `L18/bin/run_e72.sh`, `certify_cnf.sh`, VB's `run_own.sh` / `run_cake.sh` (read, not run);
  - from the worker:
    - README.md and VERIFY_AE33R1.md;
    - `hashes_203.tsv`, a comparison target in `drive.sh`;
    - the first row and the `cadical_version` column of `results.jsonl`;
    - its 203 `cake/*.cake.out` and one file `stats/ae_d0_14.stats`;
    - `logs/indep_selftest.json`, as data;
    - the stats and cadical lines of `tools/run_pairs.sh` (grep).
- **Not read:** the worker's `indep.py`, `geom.py`, `prep.py` (only hashed, to check the cited SHA-256) and
  `summarize.py` (neither read nor hashed); VB's `vb_e72.py`; L18's `src/`.
- **Integrity of cited worker artefacts (hashes only):** every SHA-256 in the claims matches the current file.
  - Files: `hashes_203.tsv`, `results.jsonl`, `summary.json`, `prep.json`, `VERIFY_AE33R1.md`, `README.md`,
    `logs/encoder_sha256.txt`, `tools/indep.py`, `tools/geom.py`, `tools/prep.py`, `logs/indep_selftest.json`,
    `indep/ae_d14_15.mutate.json`, `bin/l2enc_rebuilt`.
  - The concatenated `indep/*.json` gives `5040baf7…`.
  - My verdicts do not rest on these files.
- **Run of others' code:**
  - only the recorded encoder `l2enc`, rebuilt by me from `l2enc.cpp` (byte-identical to `af75c610…`). It was used to
    regenerate the target CNFs (needed for claim ae33-r1-regen-exact and to fix the exact bytes checked) and to make
    control CNFs;
  - the certifier cake_lpr (`c14ff498…`), `/usr/bin/cadical` 2.1.3 for the re-solve control, zstd and sha256sum.
  - The family check and cake_lpr ran on bytes whose SHA-256 equals the decompressed kept `.cnf.zst`. Those two
    verdicts therefore do not depend on having run l2enc: l2enc only reproduced the kept bytes.
  - Nothing from the worker's `tools/`, `bin/`, `stats/` or `bases/` was run or used as input.
- **My own code** (`V/tools`, hashes in `V/SHA256SUMS`):
  - `inputs.py` (inputs, base files);
  - `fam.cpp` (family generator, strict DIMACS parser, multiset comparison, real-configuration evaluator, brute-force
    k-gon oracle, comparator mutations);
  - `identities.py`, `mkctl.py`, `mktiny.py`, `summarize.py`, and the drivers `pilot.sh`, `drive.sh`, `controls.sh`,
    `extra.sh`.
- **Deliberate differences from l2enc:**
  - Convex subsets: brute force over **all** C(31, m) subsets (m = 3..7) with a monotone-chain hull test; the ccw
    order comes from the hull. l2enc uses an angular DFS from the lowest vertex; the worker used a 4-point test.
  - Orientation literals: explicit cyclic rotation plus one transposition. l2enc uses bubble-sort parity.
  - R2 angular order: by counting ranks, then checking that every pair i < j has det > 0.
  - GP and RAD: the full-length forbidden assignments are enumerated straight from the identities.
- **Compute:** units `esr-ag-ae33-v{inputs,build,pilot,ctl,all,extra}`, 1 thread, MemoryMax 1000M, one at a time.
  Peak was cake_lpr at 617,656 kB RSS (62 %). YIELD was never present.

## 1. Checks per claim

### 1.1 ae33-inputs-exact (own `inputs.py`, unit `esr-ag-ae33-vinputs`; `out/inputs.json`)

| fact | own result |
|---|---|
| `json.load(parse_float=Decimal)`, `points_7` × 10^17 integral and equal to `L18/e72/ae33.txt` (`cb6a5327…`) | true, 33 points, max abs coordinate 4.86·10^16 < 2^56 |
| `results/D/calib/alphaevolve_int.txt` (`e332e971…`; identical copy in D2) has the same labelled order type (all 5,456 signs) | true (not mirror) |
| collinear triples | 0 |
| convex m-subsets, m = 3..8: hereditary extension + hull test (Python) | 5,456 / 24,758 / 47,945 / 32,055 / **1** / 0 |
| the same, C++ full brute force over all C(33, m), m ≤ 8 (`bin/fam count`) | identical. All 5,456 orientation signs equal Python's (SHA-256 of the sign string `2c8fe702…` both ways) |
| the unique convex 7-subset and its ccw order | {14,15,17,20,23,25,32}; ccw 14, 15, 17, 20, 23, 32, 25 (both programs) |
| pairs u < v meeting H = the `ae_` names of `L18/e72/targets.txt` | 203 = 203, no duplicates; 21 both / 57 only u / 125 only v |
| own bases (AE33 minus lines u, v; `_pts` = base + line u + line v) = L18 `bases/` byte for byte | 203 / 203 and 203 / 203 |
| hull of AE33 | 5, 23, 32, 19, 21 (as the worker states) |

### 1.2 ae33-r1-regen-exact (`logs/build_l2enc.log`, `out/rows.jsonl`)

- `g++ 15.2.0 -O2 -std=c++17 L18/copied/l2enc.cpp` (`171a3e7c…`) is byte-identical (`cmp`) to `L18/bin/l2enc_l18` and
  `L18/bin/l2enc` (all `af75c610…`).
- For 203 / 203 pairs, the CNF regenerated from my own base file has one SHA-256, equal to all of:
  - the decompressed kept `L18/e72/cnf/<name>.cnf.zst`;
  - `summary.jsonl` `cnf_sha256`;
  - `cert/certify.jsonl` `cnf_sha256`;
  - the worker's `hashes_203.tsv`.
- The encoder stats line equals `summary.jsonl`'s stats in every field except `points`, 203 / 203.
  - `points` is the relative input path: `out/bases/…` in my run, `bases/…` in L18's.
  - The worker's line is byte-identical only because it ran with the same relative path. This is not a substantive
    difference.

### 1.3 ae33-r1-203-certified (unit `esr-ag-ae33-vall`; `out/rows.jsonl`, `cake/<name>.cake.out`)

For every pair, my driver did the following on exactly the regenerated file:
1. Decompress `L18/e72/cert/<name>.lrat.zst`.
2. Compare the LRAT's SHA-256 and size with `certify.jsonl` and `hashes_203.tsv`: equal 203 / 203 (134,135 to
   18,259,054 bytes). The `.lrat.zst` SHA-256 equals the tsv's, 203 / 203.
3. Run `~/.local/bin/cake_lpr --CML_HEAP_SIZE=600 cnf lrat`.
4. Delete the decompressed copies. The `.zst` files were not touched.

| check | result |
|---|---|
| `grep -cx 's VERIFIED UNSAT'` = 1, and the output is exactly one line (17 bytes) | **203 / 203** |
| header `p cnf 961 N`; N range | 203 / 203; 1,037,162 to 1,207,610 (as claimed); N equals the tsv's clause count, 203 / 203 |
| worker's `ae33/cake/*.cake.out` and L18's original `cert/ae_*.cake.out` (read only) | 203 / 203 exactly the one line; 203 / 203 one verdict line |
| CaDiCaL origin: `c Version 2.1.3` and `c exit 20` in all 203 `L18/e72/cert/ae_*.cadical.log` (own grep) | 203 / 203 |
| re-solve: `/usr/bin/cadical --lrat=true --binary=false` (2.1.3, `4acf5860…`) on 5 regenerated CNFs (ae_d1_32, ae_d20_23, ae_d14_15, ae_d17_27, ae_d5_32 = largest proof) | exit 20; LRAT SHA-256 **byte-identical** to `certify.jsonl`, 5 / 5 |
| cake_lpr negative controls (`ctl/negcake.jsonl`) | proof of ae_d0_14 vs CNF of ae_d14_16: 0 verdict lines ("Checking failed at line: 0"). Proof of ae_d14_16 cut to 1,115 of 1,594 lines: 0 ("empty clause not derived"). Positive twin, full proof: 1 |

**Note (a defect in the worker's artefact, not in the claim).** The worker's `results.jsonl` has
`"cadical_version":""` in all 203 rows: its grep pattern `CaDiCaL Version` does not match the log line
`c Version 2.1.3`. Its README nevertheless cites "203 / 203" banners. The fact is true (my grep, plus the re-solve
byte equality), but that field of `results.jsonl` is not evidence for it.

### 1.4 ae33-r1-families-exact (own `bin/fam check`, on the same regenerated bytes; `fam/<name>.json`)

- **Generator:** every family is generated from the definitions in LOWERBOUND_RUN_1118 §(2) and ABSAT8 §3, as
  restated in the claim's recipe. Variables: X = 1 + r, Y = 466 + r, W = 931 + a; r is the lexicographic pair rank,
  built by enumeration.
- **Parser:** the CNF is parsed strictly: header `p cnf V N`, exactly N clauses of the form `l … l 0\n`, single
  spaces, no leading zeros, |l| ≤ V, no comments, nothing after the last clause. Eleven malformed variants were
  rejected (`logs/parsetest.out`).
- **Block split:** the CNF is split into blocks using **my own** family sizes, in l2enc's emission order (r2x, r2y,
  acx, acy, rad, gpa, gpp∪gpq, octx, octy, jk).
- **Comparison:** each block is compared with my family as a multiset of literal-sorted clauses, and the whole CNF
  with the union.

| check | result |
|---|---|
| all 10 blocks: 0 clauses only in the CNF, 0 only in my family; whole CNF likewise; header vars 961 = mine; header N = my total | **203 / 203**, 223,165,944 clauses in all |
| my counts per family (r2x, r2y, acx, acy, rad, gpa, gpp, gpq, octx, octy, jk) and convex3..7 equal `summary.jsonl` stats; jkq = 0 | 203 / 203 |
| own convex7 of B (brute force over all C(31,7) subsets) | 0, 203 / 203 (each base heptagon-free) |
| GP/RAD clauses where some single flip keeps the pattern forbidden (shortenable) | 0 (all full length) |
| JK tautologies; duplicates merged in JK; duplicates in any other family | 0; 232,808 to 302,206 per base (by l2enc's dedup rule, from pentagons sharing a 4-chain); 0 |
| R2: every pair i < j in each angular order has det > 0 | 203 / 203 |
| comparator controls (3 pilot pairs plus 36 tiny bases): one literal flipped, one clause dropped, one clause appended, in each non-empty block | 1,152 / 1,152 detected; all 384 flips flagged in their own block (count unchanged, so only the block comparison could catch them) |
| tiny bases vs l2enc, k-gon-free, k = 5, 6, 7 (12 each), plus 9 earlier ones | 45 / 45 equal |

### 1.5 ae33-realpair-exact (own evaluator in `fam.cpp`; `fam/<name>.json`)

For each pair the assignment was computed from exact orientations of AE33's own coordinates: X(a,b) =
[orient(b_a,b_b,u) > 0], Y with v, W(a) = [orient(b_a,u,v) > 0]. Every clause of the CNF was evaluated.
- **Violations:** exactly 1 violated clause per CNF:
  - JK for the 21 pairs with both points on H;
  - OCTX for the 57 with only u on H;
  - OCTY for the 125 with only v on H;
  - 0 in R2X/R2Y/ACX/ACY/RAD/GPA/GPP∪GPQ.
  The same counts come out on my own families.
- **7-gons:** the convex 7-subsets of B ∪ {u, v} were enumerated exhaustively, as convex7(B) plus hexagon + one new
  point plus pentagon + both. There is exactly 1 per pair, of the type above, and mapped back to AE33 labels it is H,
  203 / 203.
- **Record correction confirmed:** the LOWERBOUND_RUN_1118 sentence "each real pair violates exactly one OCTY clause"
  holds only for the 125 pairs with only v on H. L18's own `summary.jsonl` has the same 21 / 57 / 125 split.

### 1.6 ae33-r1-soundness-proved and ae33-r1-corollary: see §2. Semantic controls (each could fail)

- **Identities** (`tools/identities.py`, `logs/identities.json`): AC, RAD and the 3-term GP identity hold exactly on
  2,000 random integer 5-tuples (coordinates up to 10^17).
  - The claim's own citation, the worker's `logs/indep_selftest.json`, contains only a summary sentence.
  - So my confirmation of "checked by machine on 2,000 random tuples" rests on my own run, not on that file.
  - The 16 forbidden GP sign patterns do not depend on the order of (f, g, h, i).
  - No realized sign vector was forbidden.
- **SAT direction** (`ctl/sat.jsonl`): B = AE33 − {h, u, v} with h ∈ H, 30 points, 8 cases (pairs inside H, mixed, and
  off H).
  - B ∪ {u, v} = AE33 − h has no 7-gon.
  - My families equal `l2enc B 7` (n = 30, 900 variables).
  - The real (u, v) violates **0** clauses in all blocks, 8 / 8; the 7-gon oracle finds none.
- **Random real (p, q)**, exact integers: uniform, near (u, v), near base points, and far points.
  - On the 203 target CNFs: 8,600 configurations. 0 consistency-family violations, and OCTX / OCTY / JK violated
    exactly when the brute-force oracle finds a 7-gon through p only / q only / both (0 mismatches). Every
    configuration had such a 7-gon, as the theorem says (that part is HEURISTIC, a sample).
  - On the SAT-direction and tiny bases: 1,600 + 900 + 3,597 more, 0 violations and 0 mismatches. Among them, 310 +
    611 + 1,534 configurations without a k-gon through p or q satisfied every clause.

## 2. Soundness, re-derived (own)

Let B′ realize the labelled order type of B, and let p, q be points with B′ ∪ {p, q} in general position (all
orientations nonzero; in particular p, q ∉ B′ and p ≠ q) and no convex 7-gon through p or q. Let α be the real
assignment. The literal of "orient(i,j,k) > 0" uses only that orient is alternating, which is true of the determinant:
- for x < y it is X(x,y) / Y(x,y), and ¬X / ¬Y for the reversed pair;
- orient(x,p,q) > 0 ⟺ W(x);
- orient(p,y,q) = −orient(y,p,q), so it is ¬W(y);
- cyclic shifts keep the sign.

1. **R2.** Set v_x = ε_x(x′ − a′), with ε_x taken from B's coordinates.
   - det(v_x, v_y) = ε_xε_y·orient(a′,x′,y′) = ε_xε_y·orient(a,x,y). So the three cone determinants of every emitted
     triple, which are > 0 in B, are > 0 in B′.
   - Cramer: v_{i+1} = λv_i + μv_k with λ = det(v_{i+1},v_k)/det(v_i,v_k) > 0 and μ = det(v_i,v_{i+1})/det(v_i,v_k) > 0.
   - With w = t − a′ and sign det(v_x, w) = ε_x·orient(a′,x′,t), which is S_x: if S_i = S_k, then S_{i+1} has the same
     value. These are exactly the two clauses.
2. **AC.** [abt] + [bct] + [cat] = [abc] (exact). If all three terms on the left had sign −σ, with σ = sign[abc] (an
   order-type constant), the sum would have sign −σ.
3. **RAD.** [bpq] − [apq] + [abq] − [abp] = 0 (exact). Four nonzero terms with sum 0 are not all of one sign. The two
   clauses forbid exactly the two one-sign patterns.
4. **GP.** [efg][ehi] − [efh][egi] + [efi][egh] = 0 for any five points (2-D Plücker identity after translating e to
   0; exact).
   - The three products are nonzero, so the signed terms are not all of one sign.
   - Each clause forbids one full assignment with all signed terms equal.
   - The constant bracket [axy] of GPA is an order-type constant.
5. **OCT** (t = p or q), for a ccw convex hexagon Q of B.
   - Convex position and ccw order are decided by orientations: a point lies inside a triangle by three signs, and
     every consecutive edge has all other points on its left. So Q is a ccw convex hexagon of B′.
   - **Visibility lemma.** C = {u : ⟨u,t⟩ > h_Q(u)} is an open convex cone, since h_Q is sublinear, and C ∩ −C = ∅.
     So its trace on S¹ is empty or an open arc, and the visible edges (those with n_j ∈ C) form a cyclic interval.
   - A violated clause means t sees e_i but not e_{i±1}. These are three distinct edges, so e_i is the only visible
     edge.
   - **Slot lemma.** t is the unique maximizer of ⟨n_i,·⟩. Each q_j has an incident edge that t does not see, and
     strictly so by general position; a direction in q_j's normal cone near that edge's normal makes q_j the unique
     maximizer over Q ∪ {t}.
   - So Q ∪ {t} is a convex 7-gon through t, which is excluded.
6. **JK** (checked most closely).
   - The p-part of a violated clause means p sees exactly edge Q_iQ_{i+1} of the ccw convex pentagon Q (step 5 with
     m = 5). So Q ∪ {p} is in convex position.
   - Its ccw order is Q1 = (…, Q_i, p, Q_{i+1}, …). For j ≠ i, p is strictly inside the line of e_j, so the four edges
     e_j remain hull edges with the same direction. The two missing hull edges must join the only vertices of degree
     < 2, namely Q_i–p and p–Q_{i+1}.
   - The record note (LOWERBOUND_RUN_1118 §(2) item 5) and the worker's §2.6 state this cyclic position without an
     argument; the bullet above supplies it. That is a small gap in the cited texts, not in the result.
   - The q-part means q sees edge (v,w) of the ccw hexagon Q1 and neither neighbour. For edges through p the literals
     are right: sees_q(Q_i,p) ⟺ orient(Q_i,p,q) < 0 ⟺ ¬W(Q_i), and sees_q(p,Q_{i+1}) ⟺ orient(p,Q_{i+1},q) < 0 ⟺
     W(Q_{i+1}). The clause holds the negations, lit(Q_i,p,q) = W(Q_i) and lit(p,Q_{i+1},q) = ¬W(Q_{i+1}), as
     generated.
   - Step 5 with m = 6 for Q1 and q gives a convex 7-gon through p and q, which is excluded.
   - The SAT-direction control exercises exactly these W literals next to a former heptagon, and is clean.
7. **Order type and mirror.** Every constant is a function of B's labelled order type:
   - base signs;
   - convex 5- and 6-subsets with their ccw orders;
   - the R2 cone signs, via ε_xε_y·orient.

   A mirror realization becomes a realization of B's order type by reflecting B′ ∪ {p, q}, which keeps general
   position and convexity.
8. **Corollary.** Let S be a 33-point set in general position, and T ⊂ S a 31-point subset with a bijection
   φ: AE33 − {u,v} → T that preserves (or reverses) every orientation.
   - If {u,v} ∩ H = ∅ (C(26,2) = 325 pairs), φ(H) ⊂ S is a convex 7-gon.
   - Otherwise (203 pairs), T labelled by φ realizes B's labelled order type (or its mirror). Since S is in general
     position, the CERTIFIED UNSAT, the EXACT family equality and steps 1-7 give a convex 7-gon through one of the two
     points of S − T.
   - Radius 0: a 32-subset of type AE33 − w contains a 31-subset of type AE33 − {w,t} for any t ≠ w.

   The deduction is correct. Its strength is that of its inputs: CERTIFIED + PROVED soundness, computer-assisted,
   unrefereed.

The note's completeness remark (every k-gon through p or q violates some OCT or JK clause) is not needed for UNSAT.
The random and real-pair controls are consistent with it, but I did not prove it.

## 3. Not checked / limits

- Track L's own controls C1-C4, `l2enc --selftest`, and the 66 symmetric bases (claim `lb-l18-e72-sym`, VB
  CONFIRMED): not re-run.
- The re-solve shows CaDiCaL provenance by byte equality for 5 of the 203 proofs only. For the other 198 it rests on
  the logs and the `certify.jsonl` hash chain, as the claim says. cake_lpr acceptance does not depend on it.
- The random-configuration counts are HEURISTIC samples. They support, but do not prove, the semantics.
- Novelty: not judged.

## 4. Files

`V=/home/jay/research/data/lower-20261121/ae33/verify`. `SHA256SUMS` covers the tools, binaries, results, logs and
controls. Main results: `out/rows.jsonl` (`7063859a…`), `out/summary.json` (`4b7de8d1…`), `fam/<name>.json`
(concatenated `ec5a5cc6…`), `cake/<name>.cake.out` (concatenated `96a8ffe4…`), `out/inputs.json` (`d61b04c1…`).
Resume commands: README.md §9.
