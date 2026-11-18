# VERIFY_LP0_7_REAL_2EXT: verdict on claim lp0-7-real-2ext (verifier VB, 15 November 2026, 20:29-20:39 KST)

**Verdict: CONFIRMED at the claimed per-pattern labels.** Every check of the claim's "how to check" list was done with
VB's own code, and more: VB's **own, independently written base encoding** agrees with D2's verdicts on 89 patterns
(pysat) and is **CERTIFIED by CaDiCaL 2.1.3 + cake_lpr on 88 patterns** (with D2's cut clauses where needed, each cut
re-derived by VB). Status of the claim's labels at 20:38: D2's own cake_lpr verdicts (`cert_k2b/certify.jsonl`, 330 lines,
all exactly `s VERIFIED UNSAT`, 330 distinct patterns) cover r7real 142 + 10, t1it4 143 + 10, and the BFP-closed patterns
of r7it3 (10), t1it5 (10) and t1it6 (5 of 10); the other 433 closed patterns (r7it3, t1it5, t1it6 base-UNSAT; 5 t1it6
BFP-closed) are still COMPUTED on D2's side (certification running). The 2 'onn' patterns (r7real, r7it3) are open and
not claimed. Nothing about LP0(7) for point sets in general follows; only 2-point extensions of these 5 blocks.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vb/claims/lp0-7-real-2ext/`; D2 = `pm1115/d2/`)

1. **Blocks** (`V/vb_lp0.py` part A, exact integers): each of the 5 block files has exactly the coordinates of its
   stated source (T1's m17_it4/5/6_real, R7's root7_real17, R7's div17/real/m17_it3_s1); 17 points with increasing x;
   (5,7)-valid (no 5-cap, no convex 7-set); r ends a 4-cap; **r lies in no weak Δ** (0 of the 2^16 sets A ⊆ B − r make
   A + r 4-cap-free and meeting every convex hexagon; 328/328/328/306/277 hexagons).
2. **BFP certificates** (part B; own checker: χ from the `subsig` with V as element k and [a,b,V] = + for a < b; for each
   tag (a,b,c,d,e,odd,other) the three signed terms of [abc][ade] − [abd][ace] + [abe][acd], the odd term's sign differs
   from both others, multipliers positive integers, and the weighted sum of log|bracket| forms (odd term minus the other)
   is identically zero): **all entries valid** in every library file used — snapshots 195054 (10), 195140 (12), 201341
   (26), 201744 (28), 202006 (30), 203206 (34) and `claims/library_k2_2028.jsonl` (32).
3. **Cut clauses** (`V/vb_lp0_all.py`, all CEGAR patterns dumped by 20:38: 44 patterns, t1it4 10, t1it5 10, r7real 10,
   r7it3 10, t1it6 4; **5,656 cuts**). For each cut (entry in the snapshot named in `certify_jobs.jsonl`, rev, flip, Q),
   VB derived the justified clause itself: for every bracket of every GP relation of the certificate (all six brackets,
   since their signs decide the odd term) that does not contain V, map it through rev (t ↦ (k−1−t₂, k−1−t₁, k−1−t₀)) and Q,
   take the pattern sign (negated under flip); brackets inside B must agree with B's signs, the others give the literal
   "sign differs from the pattern". **In 5,656 of 5,656 cuts B agrees and D2's clause contains VB's justified clause**, so
   every cut is implied by a valid one; and each `.cnf`'s last `cut_clauses` clauses equal its `.cuts.jsonl`. Validity
   of the justified clause: a real x-sorted W satisfying the mapped pattern would contain the certified non-realizable
   x-sorted configuration (rev = reflection x ↦ −x with labels reversed, which keeps every sorted triple's sign and
   [a,b,V] = +; flip = reflection y ↦ −y, which negates every sign and keeps [a,b,V] = +).
4. **Own base encoding** (`V/vb_base.py`, written from THEORY_1115PM.md §0, not from P2's code): triple variables for W
   (19 points), old triples fixed to B's signs, signotope axiom on all 4-sets, no 5-cap in full form (not all 10 triples
   caps), cv ↔ convex 4-set, no convex 7-set, f_K → K a 4-cap, e_p → p ends a 4-cap, g_T → T a convex hexagon of 4-cap
   end points, ∨g_T. Sound by construction for "W is an x-sorted LP0(7) counterexample" (r unrootable is automatic by
   Lemma M, claim t4-lemmas). pysat (COMPUTED, `V/resultsD.jsonl`): 25 sampled base-UNSAT patterns (5 per block): own
   base UNSAT 25/25; 32 BFP-closed patterns: own base alone **SAT** 32/32 (as for D2: only the cuts close them) and own
   base + D2's cuts UNSAT 32/32.
5. **Own CNFs certified** (house `certify_cnf.sh`, units `esr-agv-vb-lp0cert` and `esr-agv-vb-lp0certE`, heap 2000 MB;
   LRATs kept as zstd in `V/owncert/`, CNFs as zstd in `V/owncnf/`): **88 of 88 `s VERIFIED UNSAT`** — base-UNSAT patterns
   r7it3 11, r7real 10, t1it4 10, t1it5 10, t1it6 10 (31 of them not yet certified by D2), and BFP-closed patterns with
   D2's re-derived cuts r7it3 10, r7real 10, t1it4 10, t1it5 7. All 37 own-certified BFP-closed patterns are among the 44
   whose cuts VB re-derived in check 3.
6. **D2's proofs, fresh cake_lpr** (unit `esr-agv-vb-lp0recake`, own FIFO wrapper): 6 random lines of
   `cert_k2b/certify.jsonl` (5 t1it4, 1 r7real): exactly one `s VERIFIED UNSAT` each; CNF hash, LRAT stream hash and
   bytes equal the recorded values.
7. **Counts** (`run_k2b/jobs.jsonl`): 765 = 5 blocks × 153 patterns (= C(18,2) positions of the two new points, r last):
   713 UNSAT (base), 50 UNSAT_CEGAR, 2 TIMEOUT (`onnoooooooooooooooo` of r7real and of r7it3), as claimed.

## Not done

- D2's controls (`d2/controls/`, `ctl_cuts.py`) and P2's `lp0ext.py` soundness were not re-run or read line by line; VB's
  own encoding replaces them for the sampled and certified patterns.
- VB did not re-derive cuts of patterns dumped after 20:38 (t1it6: 6 BFP-closed patterns pending at that time).

## Files (V as above)

| file | SHA-256 |
|---|---|
| `V/vb_lp0.py` / `V/vb_lp0_all.py` | `7cfb2cab34a016884484fb9b9b22598302918ba26b49475c26ca74cd3f122fea` / `6559422ed7f1dc687b6de585b31a836b8b1c5d31cf4cbc63895994313df27c14` |
| `V/vb_lp0_ABC_all2.out` (checks 1-3, 44 patterns) | `373802b4ef625d5bfd164695a10bf942c2fefc89636fdbd6996bfeff50455638` |
| `V/vb_base.py` | `cfd80fba566dfb9147b283164bcfb2b80a0aa6d3dcb8cb267ee7821ab11466e4` |
| `V/resultsD.jsonl` (check 4) | `f7e72f534bd50bd1cf0d1a5120f39a441dcfff893074bfcc204e1c7f2c13e3b1` |
| `V/owncert/certify.jsonl` (check 5, 88 lines) | `062045aa11af8a8743b3c17c90d9aa9cf8ff3f6631c8491494bd1ff5abffd291` |
| `V/d2recake/rerun.jsonl` (check 6) | `c8f3c783324cbaa0088831ed4d76555c946330f3013974796c5a8e14a9eb232b` |

D2's files were only read.

## Update 20:48 KST (VB)

The two 'onn' patterns were closed later by D2 (claim lp0-7-real-2ext-onn); VB's verdict on that claim is in
[VERIFY_LP0_7_REAL_2EXT_VB.md](VERIFY_LP0_7_REAL_2EXT_VB.md) (CONFIRMED). State at 20:47: all 765 patterns closed (713
base-UNSAT, 52 cut-closed); D2's CERTIFIED set 500 of 765; all 7,141 cuts of the 52 cut-closed patterns re-derived by VB;
VB's own encoding CERTIFIED on 103 patterns (all 52 cut-closed and 51 base-UNSAT samples).
