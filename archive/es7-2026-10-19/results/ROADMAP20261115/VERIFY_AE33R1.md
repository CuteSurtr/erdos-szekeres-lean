# VERIFY_AE33R1: E7-2 radius 1 around AE33, 203 pairs (verifier: agent ae33, 21 Nov 2026, 20:05-21:10 KST)

**Verdict: CONFIRMED at CERTIFIED + PROVED soundness, for all 203 pairs.**

**Claim checked.** AE33's heptagon is H = {14, 15, 17, 20, 23, 25, 32}. For each of the 203 pairs {u, v} of AE33 that
meet H, `l2enc (AE33 − {u, v}) 7` is UNSAT (CERTIFIED). With the soundness note of LOWERBOUND_RUN_1118 §(2) (PROVED),
this gives: no 33-point set in general position without a convex 7-gon contains a 31-point subset with the order type
(or mirror order type) of a 31-point subset of AE33.

**What supports the verdict:**
- every CNF regenerated bit for bit;
- every kept proof re-accepted by a fresh cake_lpr;
- every one of the 223,165,944 clauses matched by my own family generator;
- the soundness note re-derived (§2).

## 0. What I read, and what I did not

- **Read** (task step 1):
  - from L18: `copied/l2enc.cpp` (all of it), `bin/run_e72.sh`, `src/e72_summary.py`, and the first 60 lines of
    `src/evalcnf2.py`;
  - the records LOWERBOUND_RUN_1118 and ABSAT8_INDEPENDENT §3;
  - from VB: `run_own.sh`, `run_cake.sh`, `recake_vb.sh`, `verdict.json`, `own_summary.json` and
    VERIFY_LOWERBOUND_L18_E72.md.
- **Not read:** VB's `vb_e72.py` and `vb_bases.py`; L18's `ctrl_rand.py`, `ctrl_e72*.sh` and `geosat56.py`.
- **Own code** (`tools/`): `geom.py`, `prep.py`, `indep.py` and `summarize.py`, plus the drivers `prep.sh`,
  `run_pairs.sh` and `run_indep.sh`.
  - None of it imports or copies L18's or VB's code.
  - `indep.py` was written after reading `l2enc.cpp`, so its convex-set enumeration, ccw ordering, literal function and
    GP instantiation are deliberately different (§1.4).
- **Reused tools:**
  - `l2enc` itself, only to regenerate the CNFs and show hash equality with the recorded encoder;
  - cake_lpr (the certifier, `c14ff498…`);
  - zstd and sha256sum.

## 1. Checks

### 1.1 Inputs (own code `prep.py` + `geom.py`; unit `esr-ag-ae33-prep`)

| check | result |
|---|---|
| `geom.py` self-test: convex k-subsets equal a brute force from the definition (a point inside a triangle of three others); ccw orders are left-turn cycles; 60 random sets of 6-10 points | OK |
| repository JSON `points_7`, parsed with Decimal and multiplied by 10^17: all integral and equal to `L18/e72/ae33.txt` | equal (33 points) |
| `results/D/calib/alphaevolve_int.txt` (another integer version in the repository): same labelled order type, all C(33,3) signs | equal |
| AE33: collinear triples | 0 |
| AE33: convex m-subsets, m = 3..8 | 5,456 / 24,758 / 47,945 / 32,055 / **1** / 0 |
| the unique convex 7-subset, and its ccw order | {14,15,17,20,23,25,32}; 14, 15, 17, 20, 23, 32, 25 |
| pairs meeting H (u < v) = the 203 `ae_` names of `L18/e72/targets.txt` | equal, no duplicates; types: 21 both / 57 only u / 125 only v |
| own base files (AE33 without lines u, v; `_pts` = base + line u + line v) = L18's | 203 / 203 and 203 / 203, byte for byte |

Each base is heptagon-free: every convex 7-subset of B is one of AE33's, and H ⊄ B. `indep.py` also recounts
convex7 = 0 for every base.

### 1.2 Encoder and CNFs (units `esr-ag-ae33-pilot`, `esr-ag-ae33-all`)

- `g++ 15.2.0 -O2 -std=c++17 l2enc.cpp` builds `bin/l2enc_rebuilt`, byte-identical to `L18/bin/l2enc_l18` and
  `L18/bin/l2enc` (`af75c610…`).
- For 203 / 203 pairs, the CNF regenerated from my base file has the same SHA-256 as all three of:
  - the decompressed kept `cnf/<name>.cnf.zst`;
  - `summary.jsonl` `cnf_sha256`;
  - `cert/certify.jsonl` `cnf_sha256`.
- The encoder's stats line is identical to the one in `summary.jsonl`, 203 / 203.

### 1.3 Fresh cake_lpr (same units)

- 203 / 203: the decompressed kept LRAT has the SHA-256 and size recorded in `certify.jsonl`.
- `cake_lpr --CML_HEAP_SIZE=600 <regenerated CNF> <LRAT>` printed exactly one line, `s VERIFIED UNSAT`, 203 / 203.
  - Max RSS was 617,656 kB, within the 1000M slot (the guard counts anon memory only, here about 62 %).
- The L18 CaDiCaL logs show `c Version 2.1.3` and `c exit 20`, 203 / 203. These logs are tied to the kept proofs only
  by the hash chain `certify.jsonl` → `.lrat.zst`; I did not re-solve.
- **Negative controls**, each 0 verdict lines:
  - the proof of ae_d14_15 run against the CNF of ae_d14_17;
  - that proof truncated to 75 % of its lines.

### 1.4 Own clause-family check (`indep.py`; units `esr-ag-ae33-indep` and `esr-ag-ae33-indep2`)

Every family was built from its definition, independently of l2enc:

- **R2X/R2Y** (ABSAT8 §3):
  - folding signs ε_x come from B;
  - the folded vectors are sorted by exact determinant;
  - for each i and each k ≥ i+2, the clauses (¬S_i ∨ S_{i+1} ∨ ¬S_k) and (S_i ∨ ¬S_{i+1} ∨ S_k), where
    S_x = ε_x·[orient(a,x,new) > 0];
  - all three cone determinants are asserted > 0 for every emitted clause.
- **ACX/ACY:** one clause per triangle, σ·[orient(e,new) > 0] over its three edges e, with σ = orient(a,b,c).
- **RAD, GPA, GPP, GPQ:** generated directly from the identities, which were re-tested exactly on random integers.
  - Every assignment of the involved variables under which all signed terms have one sign gets the clause that
    excludes the full assignment.
  - The GP relations are instantiated as (a, p, q, x, y), (p, q, x, y, z) and (q, p, x, y, z). l2enc uses
    (a, x, y, p, q), (p, x, y, z, q) and (q, x, y, z, p). The forbidden pattern set of a 3-term GP relation does not
    depend on this order, and the equality with l2enc confirms it.
  - Also checked: none of these clauses can be shortened (flipping any one variable leaves the forbidden pattern).
- **OCTX/OCTY:**
  - convex 6-subsets come from a 4-point brute force, not l2enc's angular DFS;
  - the ccw order comes from the successor test (every other member strictly to the left);
  - one clause per distinct cyclic 4-chain.
- **JK:** for every convex 5-subset Q in ccw order, every slot i, and every edge (v, w) of Q1 with neighbours u and z:
  lit(Q_i,Q_{i+1},p), ¬lit(Q_{i−1},Q_i,p), ¬lit(Q_{i+1},Q_{i+2},p), lit(v,w,q), ¬lit(u,v,q), ¬lit(w,z,q).
  - lit(x,p,q) = W(x) and lit(p,y,q) = ¬W(y), from an explicit permutation-parity orientation function.
  - Duplicates are merged and tautologies counted.

Each block of the kept CNF was compared with my family as a multiset of literal-sorted clauses.
- Block positions come from the encoder's block sizes. GPP and GPQ form one block, because l2enc interleaves them.
- The header must be `p cnf 961 <total>`, with nothing after the last clause.

| check | result |
|---|---|
| all ten blocks equal, header OK, nothing trailing | **203 / 203 pairs** (223,165,944 clauses) |
| own convex 3- to 7-subset counts = encoder stats | 203 / 203 |
| GP/RAD clauses that could be shortened; JK tautologies | 0; 0 |
| real pair, own evaluator: violated clauses | exactly 1 per pair: a JK clause for the 21 pairs with both points on H, an OCTX clause for the 57 with only u on H, an OCTY clause for the 125 with only v on H; 0 in R2/AC/RAD/GP |
| real pair, own enumeration: convex 7-subsets of B ∪ {u, v} | exactly 1 per pair, through both points / p only / q only, as the type says |
| tiny bases vs l2enc (40 random k-gon-free sets, k = 5, 6, n = 6-10) | 40 / 40 equal |
| mutation control (one literal flipped in each of R2Y, GPP∪GPQ, JK of ae_d14_15) | exactly those three blocks reported |

## 2. Soundness review (own, as requested): PROVED

I re-derived the note of LOWERBOUND_RUN_1118 §(2) for exactly the families that §1.4 found in the CNFs, and no
others. Assume B′ realizes the labelled order type of B, and B′ ∪ {p, q} is in general position (all orientations
nonzero) with no convex 7-gon through p or q.

1. **R2.** Fix a and an emitted triple (i, i+1, k), and set v_x = ε_x(x′ − a′) with ε_x taken from B.
   - Then det(v_x, v_y) = ε_x ε_y orient(a′,x′,y′) = ε_x ε_y orient(a,x,y). So the three determinants asserted > 0 in
     B are also > 0 in B′.
   - Cramer's rule gives v_{i+1} = λ v_i + μ v_k with λ, μ > 0.
   - With w = p − a′, det(v_x, w) = ε_x orient(a′,x′,p). So if S_i = S_k, then S_{i+1} has the same value. These are
     exactly the two clauses.
2. **AC.** For any four points, [abp] + [bcp] + [cap] = [abc]. So σ times at least one of the three terms on the left
   is positive.
3. **RAD.** Take the 4 × 4 matrix with rows (x, y, 1, 1) for a, b, p, q.
   - It has two equal columns, so its determinant is 0.
   - Laplace expansion along the last column gives [bpq] − [apq] + [abq] − [abp] = 0 (also re-tested exactly).
   - Four nonzero terms that sum to 0 are not all of one sign.
4. **GP.** Project from the pivot e: each bracket [exy] becomes a 2 × 2 determinant of the images.
   - The relation det(f,g)det(h,i) − det(f,h)det(g,i) + det(f,i)det(g,h) = 0 is the 2-D Plücker identity (re-tested
     exactly).
   - With all three products nonzero, the signed terms are not all of one sign.
   - Permuting f, g, h, i maps the three signed terms to ± a permutation of themselves, so the forbidden set does not
     depend on the argument order (used in §1.4).
5. **OCT** (ABSAT8 §3 (i), (ii)).
   - For a convex polygon Q in ccw order and a point outside it, the visible edges (orient < 0) form a nonempty cyclic
     interval.
   - If p sees e_i but neither e_{i−1} nor e_{i+1}, then e_i is the only visible edge (m ≥ 3, so the three edges are
     distinct).
   - Then p and every vertex of Q are vertices of conv(Q ∪ {p}). For a convex hexagon Q of B′, this is a convex 7-gon
     through p.
   - Convex position of a 6-subset, and its ccw order, are determined by orientations. So Q is a convex hexagon of B′,
     with the same order.
6. **JK.** Suppose the clause is violated.
   - Step 5 for the pentagon Q (m = 5) shows that Q ∪ {p} is in convex position with p between Q_i and Q_{i+1}. So Q1
     is a ccw convex hexagon of B′ ∪ {p}.
   - The q-part of the clause states that q sees edge (v, w) of Q1 but neither neighbouring edge. For edges through p
     the literals are correct: orient(x,p,q) < 0 ⟺ ¬W(x), and orient(p,y,q) < 0 ⟺ W(y), since
     orient(p,y,q) = −orient(y,p,q).
   - Step 5 again (m = 6) makes Q1 ∪ {q} a convex 7-gon through p and q.
7. **Order type and mirror.**
   - Every constant used depends only on B's labelled order type: the signs of base triples, the convex 5- and
     6-subsets with their ccw orders, and the signs of the R2 cone determinants.
   - For a mirror realization, reflect B′ ∪ {p, q}. This keeps general position and convexity.
8. **Corollary.** Let S be a 33-point set in general position, and T ⊂ S a 31-point subset order-isomorphic (or
   anti-isomorphic) to AE33 − {u, v}.
   - If {u, v} ∩ H = ∅, then T contains the image of H, which is a convex 7-gon.
   - Otherwise B = AE33 − {u, v} is one of the 203. Labelled through the isomorphism, T realizes B's labelled order type
     (or its mirror), and the UNSAT CNF gives a convex 7-gon through one of the two other points of S.

Conclusion: the soundness argument is correct. JK's completeness remark is not needed, and I did not check it.

## 3. Not checked

- Track L's controls C1–C4, `l2enc --selftest` and the random-pair controls were not re-run; they remain track L's
  evidence only.
  - My real-pair evaluation covers only the violating direction: for each of the 203 CNFs, the real pair (which lies
    on H) violates exactly one k-gon clause, as expected, and no consistency clause.
  - No SAT-direction control (a real heptagon-free extension satisfying every clause) was run here.
- Novelty: not judged.
- The 66 symmetric bases (claim `lb-l18-e72-sym`, already CONFIRMED by VB): not re-checked here.

## 4. Re-run

See README §8.
- Results: `results.jsonl`, `indep/<name>.json`, `negctl/negctl.jsonl`, `logs/indep_selftest.json`, `summary.json`.
- Hashes: `hashes_203.tsv` and `SHA256SUMS`.
