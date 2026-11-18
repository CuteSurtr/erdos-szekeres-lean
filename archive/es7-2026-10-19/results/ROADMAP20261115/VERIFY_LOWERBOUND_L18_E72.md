# VERIFY_LOWERBOUND_L18_E72: claim `lb-l18-e72-sym` (verifier VB, 18 Nov 2026, 03:30-03:50 KST)

**Verdict: CONFIRMED** at the claimed labels: CERTIFIED per CNF, and PROVED soundness, which I re-derived and checked
clause by clause with own code. For each of the 66 bases B (mirror32 − u and sym7_32 − u for u = 0..31, c3_31 and
c5_31), and for every realization B′ of B's labelled order type (or of its mirror image) and all p, q with
B′ ∪ {p, q} in general position, B′ ∪ {p, q} has a convex 7-gon through p or q.

So no 33-point set in general position without a convex 7-gon contains a 31-point subset with one of these 66 order
types. VS released this claim (note `lb-l18-e72-sym.note-from-VS.txt`: cake_lpr needs more than 300 MB of heap here)
and asked VB for the cake part and the review of the soundness note; both are below.

| check | result |
|---|---|
| bases = repository files: `SYMMAX/mirror_32points.txt` minus line u (32/32), `SYM2/sym7_32points.txt` minus line u (32/32), c3_31 = `SYMMAX/c3_31points.txt` (Eisenstein pairs as Cartesian integers, an orientation-preserving linear image), c5_31i = `l1118/absat_sym/c5_31i.txt` (orientations equal the exact Z[√5] signs, 0 of 4,495 differ; VERIFY_LOWERBOUND_L18_OTSAT.md) | all equal (`vb_bases.py`) |
| each base: no collinear triple, heptagon-free (own exact enumeration) | 66 / 66 |
| decompressed CNF SHA-256 = `summary_sym66.jsonl`; header `p cnf 961 <clauses>` | 66 / 66 |
| **fresh cake_lpr** (heap 1000 MB; LRAT streamed from the kept `cert/<name>.lrat.zst` through a FIFO): exactly one line `s VERIFIED UNSAT`; stream SHA-256 = `certify.jsonl` `lrat_sha256`; CNF SHA-256 = `cnf_sha256` | **66 / 66** (max RSS 1,003 MB) |
| **every clause justified by own code** (`vb_e72.py`): 70,967,624 clauses over the 66 CNFs | **66 / 66 CNFs, 0 unjustified** |
| — by own generated families (R2X, R2Y, ACX, ACY, OCTX, OCTY, JK) | 54,292,724 |
| — by exact semantic implication from RAD on {a, b, p, q} | 61,380 |
| — by exact semantic implication from a 3-term GP relation on {a, f, g, p, q}, pivot in B / p / q | 7,120,080 / 4,746,720 / 4,746,720 |
| own family counts and convex-set counts = l2enc's stats (r2x … jk, rad, gpa, gpp, gpq, convex4..7) | 66 / 66 equal |

## 1. Method (own code; l2enc.cpp, evalcnf2.py and ctrl_rand.py were not read)

`vb_e72.py` uses the claim's variable semantics:
- X(a,b) = [orient(a,b,p) > 0] = 1 + r(a,b);
- Y(a,b) = [orient(a,b,q) > 0] = N2 + 1 + r(a,b);
- W(a) = [orient(a,p,q) > 0] = 2·N2 + 1 + a.

Every clause of a CNF must be one of the following.

**(G) Own generated families**, built from the soundness note's definitions with VB's l1enc encoder code (it matched every
l1enc CNF in claims `lb-ln-ddsz28-all34`, `lb-l18-otsat-nonmax`, `lb-l18-satg6-14` and `lb-l18-satg7-20`).
- **R2X/R2Y, ACX/ACY, OCTX/OCTY:** l1enc's families for p and for q. OCT uses the chains of every convex 6-gon.
- **JK:** for every ccw convex 5-gon Q of B, every slot i and every edge (v, w) of Q1 = Q with p inserted after Q_i
  (neighbours u, z), the clause is ¬sees_p(Q_iQ_{i+1}) ∨ sees_p(Q_{i−1}Q_i) ∨ sees_p(Q_{i+1}Q_{i+2}) ∨ ¬sees_q(v,w) ∨
  sees_q(u,v) ∨ sees_q(w,z).
  - sees_p(x,y) = orient(x,y,p) < 0.
  - sees_q(x,p) = ¬W(x) and sees_q(p,y) = W(y), since orient(p,y,q) = −orient(y,p,q).
  - Duplicates are merged; there were no tautologies.

**(S) Exact semantic implication by an identity that real orientations satisfy.**
- **RAD:** [bpq] − [apq] + [abq] − [abp] = 0, so the four signs are not all equal.
- **3-term Grassmann–Plücker:** [efg][ehi] − [efh][egi] + [efi][egh] = 0 on the 5-set {a, f, g, p, q}, for each of
  its five pivots.
- The test: the clause's variables lie among the relation's (at most 6), and every completion of the assignment that
  falsifies the clause violates the relation (all assignments enumerated).

## 2. Review of the soundness note (LOWERBOUND_RUN_1118 §(2)), as VS asked

- **R2X/R2Y, ACX/ACY, OCTX/OCTY:** ABSAT8_INDEPENDENT §3, per new point. The hypothesis "no convex 7-gon containing p
  or q" includes "none through p" and "none through q". Order-type invariance holds as in ABSAT8 §3; the folding signs
  are fixed from B.
- **RAD:** take the 3×3 minors of the homogeneous coordinates v_i = (x_i, y_i, 1). Laplace expansion of the singular
  4×4 matrix with a repeated row of ones gives Σ (−1)^{i+1} [v₁..v̂_i..v₄] = 0. In general position all four terms are
  nonzero, so the clauses that forbid the two all-equal patterns are valid. My semantic check confirms that each of the
  930 RAD clauses per CNF is implied by this identity.
- **GP:** this is the 3-term Grassmann–Plücker relation for 3×3 minors sharing the column e. With all products nonzero,
  (T₁, −T₂, T₃) cannot all have one sign. Each GPA/GPP/GPQ clause was checked to be implied by its relation instance.
  The clauses are full-length, with 8 per base-pivot instance and 16 per p- or q-pivot instance.
- **JK:**
  - Suppose the clause is violated. Then p sees edge Q_iQ_{i+1} of the convex pentagon Q but neither neighbouring edge.
    The visible edges form a cyclic interval (visibility lemma), so this is the only visible edge. By the slot lemma,
    Q ∪ {p} is in convex position with p between Q_i and Q_{i+1}, so Q1 in this cyclic order is a ccw convex hexagon.
  - In Q1, q sees (v, w) but not its neighbours, so by the slot lemma again Q1 ∪ {q} is a convex 7-gon through p and q.
    That contradicts the hypothesis.
  - The orientation literals for edges through p are the W literals above, consistent with the ccw order (…, Q_i, p,
    Q_{i+1}, …).
- **Conclusion:** if l2enc(B, 7) is UNSAT, the statement follows for every realization and its mirror. Every clause
  used is one of the above, as checked in §1, so the 66 UNSAT certificates prove the claim for these 66 order types.
  The note's completeness remark (every 7-gon through both points is caught by JK) is not needed and was not checked.

## 3. Not checked

- The claim's controls (`l2enc --selftest`, C1/C2/C4, the random pairs), the encoder review by the claimant, and
  the remaining 203 AE33 targets (not part of this claim).
- The remark about c3_31/c5_31 following from the one-point certificates is consistent with VERIFY_LOWERBOUND_L18_OTSAT.md:
  there `l1enc(S, 7)` is UNSAT for c3_31 and c5_31i, and l1enc's families are a subset of l2enc's.
- Novelty is not judged.

## 4. Files (`W = /home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/lb-l18-e72-sym/`)

`vb_e72.py` (`e4fd4025…`), `vb_bases.py` (`73dd7e44…`), `run_cake.sh` (`6d311352…`), `run_own.sh` (`ca4f3ffc…`); results
`bases_check.json`, `cnf_hash_check.txt`, `cake/rerun.jsonl` + `cake/<name>.cake.out` (66), `own/<name>.json` (66),
`own_summary.json`; SHA-256 in `W/SHA256SUMS`.
- Units `esr-agv-vb-e72cake` (95 %, 2700M, 1.5 min for all 66) and `esr-agv-vb-e72own` (95 %, 1500M, about 9 s per
  CNF, max RSS about 650 MB).
- Re-run: `bash W/run_cake.sh; bash W/run_own.sh`.
