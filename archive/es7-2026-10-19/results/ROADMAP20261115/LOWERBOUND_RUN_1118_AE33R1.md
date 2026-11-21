# E7-2 radius 1 around AE33: all 203 pairs UNSAT (draft record section for LOWERBOUND_RUN_1118, agent ae33, 21 Nov 2026)

**Filed by the main session, 22 Nov 2026 00:45 KST** (copied unchanged from the work folder below, apart from this note).
- Claim `lb-l18-e72-ae33` (`pm1115/claims/`).
- Workflow verifiers, each with its own code: rebuild verifier **CONFIRMED** all 7 items ([VERIFY_AE33R1_REBUILD.md](VERIFY_AE33R1_REBUILD.md); its own driver re-ran cake_lpr on all 203 pairs and its own C++ family checker `fam.cpp` re-derived every clause); soundness verifier **CONFIRMED** all 7 ([VERIFY_AE33R1_SOUNDNESS.md](VERIFY_AE33R1_SOUNDNESS.md)).
- Main-session check: the 203 worker cake outputs `cake/*.cake.out` each contain exactly one line `s VERIFIED UNSAT` (`grep -cx`, 203/203).
- `VERIFY_AE33R1.md` holds the worker's own item-by-item checks, not an independent verification.

**Status (21:06 KST, final): CERTIFIED + PROVED soundness for all 203 pairs.**
- Each CNF was regenerated bit for bit and its kept proof re-accepted by a fresh cake_lpr.
- An independent clause-family check (EXACT, own code `tools/indep.py`) found every one of the 223,165,944 clauses of
  the 203 CNFs equal to the families of the soundness note.

Computer-assisted, unrefereed. This is support evidence for ES(7) = 33 (class (S) of the lower-bound digest), not a
bound; nothing about ES(7) or ES(8) changes.

Track L's run (18 Nov; `L18` = `/home/jay/research/data/roadmap-20261115/pm1115/l1118`) finished on 18 Nov at 04:58.
- By its `summary.jsonl` and its 269 `cert/*.cake.out` files (my count of the verdict lines), all 269 targets were
  UNSAT.
- The 66 symmetric bases are claim `lb-l18-e72-sym`, CONFIRMED by VB.
- This directory re-checks the 203 AE33 targets with fresh tools and own code.

My item-by-item checks are in [VERIFY_AE33R1.md](VERIFY_AE33R1.md).

## 1. Statement

AE33 is AlphaEvolve's 33-point heptagon-free near miss: `archive/es7-2026-10-19/inputs/alphaevolve_pts.json`, key
`points_7` (SHA-256 `192c262f…`). It is used as the integer file `L18/e72/ae33.txt` (`cb6a5327…`), which equals the
JSON decimals × 10^17 exactly. It is in general position and has exactly one convex 7-gon,
H = {14, 15, 17, 20, 23, 25, 32} (ccw order 14, 15, 17, 20, 23, 32, 25). For a pair u < v, B = AE33 − {u, v} keeps
the other 31 points in their order.

**Theorem (CERTIFIED + PROVED soundness).** For each of the 203 pairs {u, v} that meet H, let B′ be any realization
of the labelled order type of B (or of its mirror image), and let p, q be points with B′ ∪ {p, q} in general position.
Then B′ ∪ {p, q} contains a convex 7-gon through p or q.

**Corollary (radius 1 around AE33 is empty at the order-type level).** No 33-point set in general position without
a convex 7-gon contains a 31-point subset with the order type (or mirror order type) of any 31-point subset of AE33.

- The 203 pairs that meet H are covered by the theorem. For the other C(26,2) = 325 pairs, B ⊇ H already contains a
  convex 7-gon, and convex position is an order-type property.
- In words: move any two points of AE33 to arbitrary positions, keeping the 33 points in general position, even
  letting the other 31 move without changing their order type. The result always has a convex heptagon: a new one, or
  H itself.
- Radius 0 follows. A 32-point subset with the order type of AE33 − w contains a 31-point subset with the order type
  of AE33 − {w, t}.
  - Radius 0 was already CERTIFIED for the 7 heptagon-vertex deletions: LOWERBOUND_RUN_1115EV E7-1, claim
    `lb-e1-absat7`, VB CONFIRMED.
  - That is quoted from the record and not re-checked here; the corollary does not depend on it.

## 2. Model and soundness

**CNF.** `l2enc B 7` (source `L18/copied/l2enc.cpp`, `171a3e7c…`; binary `L18/bin/l2enc_l18` = `L18/bin/l2enc`,
`af75c610…`). For a < b in B, let r(a,b) be the lexicographic rank and N2 = n(n−1)/2 = 465. The variables are:
- X(a,b) = [orient(a,b,p) > 0], numbered 1 + r(a,b);
- Y(a,b) = [orient(a,b,q) > 0], numbered N2 + 1 + r(a,b);
- W(a) = [orient(a,p,q) > 0], numbered 2·N2 + 1 + a.

That is 961 variables. The 203 CNFs have 1,037,162 to 1,207,610 clauses (223,165,944 in all), in ten blocks: R2X,
R2Y, ACX, ACY, RAD, GPA, GPP∪GPQ, OCTX, OCTY, JK. GPP and GPQ are written interleaved, one triple at a time.

**Soundness (PROVED).** This is the note of LOWERBOUND_RUN_1118 §(2), reviewed by VB for `lb-l18-e72-sym` and again
here (VERIFY_AE33R1.md §2). Suppose B′ realizes B's labelled order type and B′ ∪ {p, q} is in general position with no
convex 7-gon through p or q. Then the real assignment satisfies every clause:

1. **R2X/R2Y, ACX/ACY, OCTX/OCTY:** ABSAT8_INDEPENDENT §3, applied to p and to q separately.
   - R2 is Cramer's rule, with the folding signs ε fixed from B. The three cone signs are ε-weighted orientations of B,
     so they hold in B′.
   - AC is the barycentric identity [abp] + [bcp] + [cap] = [abc].
   - OCT combines the visibility lemma and the slot lemma: a violated clause makes Q ∪ {p} a convex 7-gon through p.
2. **RAD:** [bpq] − [apq] + [abq] − [abp] = 0. The four terms are nonzero, so they are not all of one sign.
3. **GPA, GPP, GPQ:** the 3-term Grassmann–Plücker relation [efg][ehi] − [efh][egi] + [efi][egh] = 0, with pivot
   e = a ∈ B, p or q. The three products are nonzero, so they are not all of one sign.
4. **JK:** in a violated clause, p sees exactly edge Q_iQ_{i+1} of a convex pentagon Q of B.
   - By the slot lemma, Q1 = (…, Q_i, p, Q_{i+1}, …) is a ccw convex hexagon.
   - q then sees exactly one edge of Q1, so Q1 ∪ {q} is a convex 7-gon through p and q.
   - Edges through p use W literals: sees_q(x,p) = ¬W(x) and sees_q(p,y) = W(y).
5. **Order type and mirror:** every constant of the CNF depends only on B's labelled order type. These constants are
   the base orientations, the convex 5- and 6-gons with their ccw orders, and the R2 cone signs. A mirror realization
   is reflected.

So UNSAT gives the theorem. For the corollary, label a 31-point subset T ⊂ S by its order isomorphism with B.

## 3. Method

1. **Inputs** (own code `tools/prep.py`, `tools/geom.py`; unit `esr-ag-ae33-prep`):
   - The JSON is parsed with Decimal; × 10^17 it equals `ae33.txt` exactly. The repository's
     `results/D/calib/alphaevolve_int.txt` (`e332e971…`) has the same labelled order type.
   - Convex subsets of AE33 are enumerated exactly (4-point brute force, Python integers).
   - The 203 pairs that meet H are exactly the `ae_` names in `L18/e72/targets.txt`.
   - The own base files equal L18's `bases/ae_d<u>_<v>.txt` and `_pts.txt` byte for byte (203 + 203).
2. **Encoder and CNFs** (`tools/run_pairs.sh`; units `esr-ag-ae33-pilot` (3 pairs) and `esr-ag-ae33-all`; 1 thread):
   - `l2enc.cpp` rebuilt with g++ 15.2.0 `-O2 -std=c++17` is byte-identical to `af75c610…`.
   - Each CNF was regenerated from the own base file. Its SHA-256 was compared with `summary.jsonl`,
     `cert/certify.jsonl` and the kept `cnf/<name>.cnf.zst`.
3. **Fresh cake_lpr** (same units; cake_lpr `c14ff498…`):
   - Each kept `cert/<name>.lrat.zst` was decompressed into this directory, and its SHA-256 compared with
     `certify.jsonl`.
   - `cake_lpr --CML_HEAP_SIZE=600` was run on (regenerated CNF, LRAT), and lines equal to `s VERIFIED UNSAT` were
     counted (cake_lpr exits 0 even when it rejects).
   - The decompressed copies were then deleted. The `.zst` files in L18 are untouched.
4. **Independent clause-family check** (`tools/indep.py`; units `esr-ag-ae33-indep` for controls + 17 sample pairs,
   `esr-ag-ae33-indep2` for the other 186):
   - Every family is built from its definition: R2/AC/OCT from ABSAT8_INDEPENDENT §3, RAD/GP/JK from the note.
   - Convex 5- and 6-subsets come from a 4-point brute force, and ccw orders from the "all others to the left"
     successor test, not from l2enc's angular DFS.
   - Literals come from an explicit orientation-sign function. The GP relations are instantiated with an argument
     order different from l2enc's.
   - Each block of the kept CNF is compared with the own family as a multiset of clauses, with literals sorted.
   - In the same pass, the real pair is evaluated: exact orientations of B ∪ {u, v}, which is AE33 relabelled, plus an
     own enumeration of that set's convex 7-gons.

## 4. Results

The 203 pairs are 21 with both points on H, 57 with only u on H, and 125 with only v on H.

| check | result |
|---|---|
| CNF SHA-256: regenerated = kept `.cnf.zst` = `summary.jsonl` = `certify.jsonl` | **203 / 203** |
| encoder stats line = `summary.jsonl` stats (block sizes, convex counts) | 203 / 203 |
| decompressed LRAT SHA-256 and size = `certify.jsonl` | 203 / 203 (134,135 to 18,259,054 bytes) |
| fresh cake_lpr, heap 600 MB: exactly one line `s VERIFIED UNSAT` and no other output line | **203 / 203** (max RSS 617,656 kB; 647 s wall for all 203, regeneration included) |
| proofs from CaDiCaL 2.1.3, exit 20 (banners of `L18/e72/cert/<name>.cadical.log`; tied to the kept proofs only by the hash chain `certify.jsonl` → `.lrat.zst`; nothing was re-solved here) | 203 / 203 |
| own clause families = CNF blocks (all ten blocks; header `p cnf 961 <clauses>`; nothing after the last clause) | **203 / 203** (223,165,944 clauses: every clause of every CNF) |
| own convex 3- to 7-subset counts of B = encoder stats (convex7 = 0, so B is heptagon-free) | 203 / 203 |
| GP/RAD clauses that could be shortened (some implied shorter clause exists) | 0: all full length. The counts suggest this too: 930 = 2·C(31,2), 107,880 = 8·31·C(30,2), 143,840 = 2·16·C(31,3) |
| JK tautologies | 0 |
| real pair (u, v): convex 7-gons of B ∪ {u, v} (own enumeration) | exactly 1 per pair, namely H: through both new points (21), through p only (57), through q only (125), as the type says |
| real pair: violated clauses (own evaluator) | exactly 1 per pair: a JK clause (21 pairs, both on H), an OCTX clause (57, only u on H) or an OCTY clause (125, only v on H). 0 in R2/AC/RAD/GP for all 203 |

The last row corrects LOWERBOUND_RUN_1118 §(2), which says "each real pair violates exactly one OCTY clause". Track
L's own `summary.jsonl` has the same split as here: 21 JK, 57 OCTX, 125 OCTY.

The check was run first on a sample of 17 pairs chosen by what the families exercise, then on the other 186:
- **Both on H, cyclic distance 1 along the heptagon** (the W literal is in the edge that q sees): d14_15, d23_32 (both
  points are hull vertices), d20_23 (fewest clauses).
- **Both on H, distance 2** (the W literal is in a neighbouring edge): d14_17, d20_32.
- **Both on H, distance 3** (no W literal): d14_20, d17_32.
- **Only v on H:** d5_32 (largest proof, 18.3 MB), d9_32 (most clauses), d1_32 (smallest proof), d0_17, d19_20, d2_23.
- **Only u on H:** d14_16, d15_21, d25_30, d17_27 (second-largest proof).

The hull of AE33 is 5, 23, 32, 19, 21.

## 5. Controls (each can fail)

- **Checker on tiny bases:** 40 random k-gon-free bases (k = 5, 6; n = 6–10). All ten blocks equal l2enc's output in
  40 / 40.
- **Identities:** RAD, 3-term GP and AC hold exactly on 2,000 random integer 5-tuples.
- **Mutation control:** on ae_d14_15, one literal was flipped in each of the blocks R2Y, GPP∪GPQ and JK. The checker
  reported exactly those three blocks (the same on a tiny base).
- **cake_lpr negative controls:**
  - The proof of ae_d14_15 run against the CNF of ae_d14_17 gives 0 verdict lines ("Checking failed at line: 0").
  - The same proof truncated to 7,614 of its 10,152 lines, run against its own CNF, gives 0 verdict lines ("empty
    clause not derived at end of proof").
- **Real pairs:** see §4. Track L's controls C1–C4 (LOWERBOUND_RUN_1118 §(2)) were not re-run here.

## 6. Files and SHA-256 (work dir `/home/jay/research/data/lower-20261121/ae33`)

- **Per-pair hashes:** `hashes_203.tsv` gives each CNF's SHA-256 and clause count, the LRAT SHA-256 and size, and the
  `.lrat.zst` SHA-256. Its own hash is in `SHA256SUMS`.
- **Proofs and CNFs:** the proofs stay in `L18/e72/cert/ae_*.lrat.zst` (unchanged; 51 MB including the logs). The
  CNFs in `L18/e72/cnf/ae_*.cnf.zst` (1.2 GB) are regenerable bit for bit.
- **Results:** `prep.json`, `results.jsonl` (one line per pair), `indep/<name>.json` (203, plus
  `ae_d14_15.mutate.json`), `negctl/negctl.jsonl`, `logs/indep_selftest.json`, `summary.json`.
- **Tools:**

  | file | SHA-256 |
  |---|---|
  | `tools/geom.py` | `cb7face7…` |
  | `tools/prep.py` | `a32ee3c3…` |
  | `tools/indep.py` | `affe63fa…` |
  | `tools/summarize.py` | `7f4cd777…` |
  | `tools/prep.sh` | `e7c2b958…` |
  | `tools/run_pairs.sh` | `654c9af7…` |
  | `tools/run_indep.sh` | `63d4a927…` |
  | rebuilt encoder `bin/l2enc_rebuilt` | `af75c610…` |

- **Inputs and binaries:**

  | file | SHA-256 |
  |---|---|
  | `alphaevolve_pts.json` | `192c262fd9889d176ce8410de18f0627d42fd8207a88f5d098ad658adabcd09a` |
  | `ae33.txt` | `cb6a5327b26b869ab39baadf0ade737882f8473dc1ccfbd377d06405a59eb54d` |
  | `l2enc.cpp` | `171a3e7c32f3e9fb03843aa3fc9f253df15c51068b06d5be79c8b3b01332ab2b` |
  | `l2enc_l18` | `af75c610d590db10ca377dd8468d387e810c0d5b31e5e5ea413631c2927d6ce1` |
  | cake_lpr | `c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54` |
  | `/usr/bin/cadical` (2.1.3) | `4acf586001aa286dff6e1a390a273023c3160f0175aba2693e3e6a0065089e70` |

- `SHA256SUMS` covers the tools, the results and the two documents.

## 7. What remains

- **Main session:** file the result as a claim (e.g. `lb-l18-e72-ae33`) and paste this section into LOWERBOUND_RUN_1118
  (Appendix A lists the edits to its existing text).
- **Not checked:**
  - track L's controls C1–C4 and `l2enc --selftest` (not re-run);
  - novelty (none claimed).
- **Scope:** AE33 is one near miss. The 273 near-full sets (LOWERBOUND_PLAN E7-1, item 3) have no radius-1 run.
- **Proof retention:** an independent check has now re-run the 203 kept LRATs. Deleting them is the owner's decision.

## 8. Resume

```
W=/home/jay/research/data/lower-20261121/ae33
U="-p CPUQuota=100% -p MemoryMax=1000M -p MemorySwapMax=0 --nice=10 --working-directory=$W"
systemd-run --user --unit=esr-ag-ae33-prep  $U -p RuntimeMaxSec=900  bash $W/tools/prep.sh
systemd-run --user --unit=esr-ag-ae33-all   $U -p RuntimeMaxSec=5400 bash $W/tools/run_pairs.sh $W/bin/l2enc_rebuilt
systemd-run --user --unit=esr-ag-ae33-indep $U -p RuntimeMaxSec=7200 bash $W/tools/run_indep.sh $W/pairs.txt
python -I $W/tools/summarize.py     # writes summary.json
```

Both drivers skip finished pairs and stop when `/home/jay/research/data/agents-20261121/YIELD` exists. A full re-run
takes about 11 min for regeneration + cake_lpr and about 32 min for the family check (1 thread, at most 620 MB anon).

## Appendix A. Edits to the existing text of LOWERBOUND_RUN_1118.md (for the main session)

1. **Line 3** ("Status: IN PROGRESS … last update 04:00"): track L's run finished on 18 Nov at 04:58
   (`L18/e72/summary.log`), with all 269 E7-2 targets UNSAT.
   - Source: `summary.jsonl` and one verdict line in each of the 269 `cert/*.cake.out` files.
   - The 66 symmetric bases were verified by VB (`lb-l18-e72-sym`).
   - The 203 AE33 targets were re-checked on 21 Nov (this section and VERIFY_AE33R1.md).
2. **Table row (2)** ("203 AE33 pairs running"): all 203 are UNSAT, so the radius-1 neighbourhood of AE33 is empty at
   the order-type level (CERTIFIED + PROVED soundness).
3. **§(2), "Results so far (03:20)"**:
   - The final count is 269 / 269, each with one verdict line in L18's `cert/*.cake.out`. The 203 AE33 targets were
     re-checked with a fresh cake_lpr here, and the 66 symmetric bases by VB.
   - The sentence "each real pair violates exactly one OCTY clause and nothing else" should read: one clause each and
     nothing else, namely 57 OCTX (only u on H), 125 OCTY (only v on H) and 21 JK (both on H). This is the split in
     track L's own `summary.jsonl`, and the own evaluator reproduces it on all 203 pairs.
4. **Claims table:** add the AE33 claim once it is filed. Suggested name `lb-l18-e72-ae33`, label CERTIFIED + PROVED
   soundness, verifier note VERIFY_AE33R1.md.
5. **"What remains":**
   - The E7-2 bullet is done.
   - The first bullet ("Verification of all six claims") is stale: the claims table shows nine claims CONFIRMED
     (lower-bound digest §5, item 8).
