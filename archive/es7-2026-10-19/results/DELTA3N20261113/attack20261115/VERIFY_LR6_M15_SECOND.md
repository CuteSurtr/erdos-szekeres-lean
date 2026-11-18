**Verdict: CONFIRMED for the certificate** (claim `lr6-m15-second`, verifier V2; updated 15 November 2026, 16:55
KST). LR(6) at 15 points is CERTIFIED by T4's encoding. One part of the statement, "shares no code with T3's
lr_cnf.py", holds only partly; see below.

**Update 16:55: an independent cake_lpr re-run by the main session, checked by V2.** The folder is
`round6/mainsession/lr6secondrecake/`, made with `recake_generic.sh`.
- **Script:** `zstd -dc <kept .zst> | tee FIFO | sha256sum`, then `cake_lpr --CML_HEAP_SIZE=1500 <CNF> FIFO`.
- **Inputs:**
  - the CNF is **V2's regenerated** `pm1115/v2/lr6-m15-second/lr6_m15.cnf`, SHA-256 `cae7193d…399c`, equal to the
    claim;
  - archive SHA-256 `825adfdf9a562798…52f5`, which I recomputed on the kept file (equal);
  - streamed LRAT SHA-256 `fc824a77…e2fe`, equal to the claim and to V2's own stream hash.
- **Output:** `cake.out` is exactly `s VERIFIED UNSAT` (17 bytes, `grep -x` count 1). cake_lpr exited with status 0
  after 128 CPU s, with a peak RSS of 1.54 GB. It finished at 15:08:44.

**Correction to my 15:08 text.** I wrote that neither LR(6) certificate at 15 points had an independent cake_lpr
re-run. That was wrong even then: the main session had re-run `lrrcert/cert/lrr6_m15.lrat.zst` for claim
`lrr6-certified` at 14:21:41 (`round6/mainsession/lrr6recake/`, heap 1400). That run has exactly one verdict line and
exit status 0; its CNF `0555d770…` and streamed LRAT `625dffe5…` equal that claim. **Both LR(6) certificates at 15
points now have independent re-runs.**

**On "shares no code".** T3's `t3/tools/lr_cnf.py` (`8669a98b…`, 68 lines) imports nothing from round 6's
`root_cnf.py` or T4's `lr_cnf.py`, and it encodes the left side directly: L_abc → (l,a,b) and (a,b,c) are caps.
T4's encoding gets the left side by mirroring instead. But its base-clause block (signotope, no 5-cap, cv, no convex
n-set, Z, F, R) uses the same clause patterns as `root_cnf.py`. So the two encodings are independent in the left-side
construction and in code, but not in the form of the base clauses. Those base clauses were reviewed several times
today and passed every semantic control.

---

*Original verdict, 15:08:* NOT CONFIRMED (incomplete, not refuted), from 15:00-15:07 KST. The encoder review, the CNF regeneration, the proof-archive hash and 18 semantic controls of the
certified CNF all passed. The independent cake_lpr re-run of the 3.5 GB proof could not be completed: **"CakeML heap
space exhausted" at heap 300 MB**, the most V2's 0.4 GB budget allows. T3 used 1,500 MB. The CERTIFIED label for this
second certificate therefore still rests only on T3's own cake_lpr run.

# Independent check: second certificate of LR(6) at 15 points (T4's encoding)

**Claim (filed by T3).**
- CNF: `lr6_m15.cnf` = round 6's `root_cnf.py 6 15` plus T4's mirrored copy by `lr_cnf.py`, SHA-256 `cae7193d…`.
- T3's run: UNSAT, with an LRAT of 3,524,550,835 bytes (`fc824a77…`) and T3's cake_lpr exact line at heap 1500.
- Conclusion: LR(6) at 15 is CERTIFIED by two independent encodings. With ROOT(6) for |S| ≤ 14 and no valid 16-point
  signotope, LR(6) holds everywhere.

**Definitions.** candidates.md K1 and §0. LR(n): if S is (5,n)-valid, r ends a 4-cap and l starts a 4-cap, then S has a
weak Δ through r or a weak Δ through l.

## What passed

1. **Encoder soundness**, read line by line: `round6/envroot/root_cnf.py` (`aef1af7a…`) and `t4/lr_cnf.py`
   (`3e24db5b…`).
   - root_cnf.py has the same base clauses as reviewed in [VERIFY_CB6.md](VERIFY_CB6.md):
     - R_abc → (a,b,c) and (b,c,r) are caps, i.e. (a,b,c,r) is a 4-cap by the consecutive-caps fact, plus OR R (r ends a
       4-cap);
     - F_K → K is a 4-cap of U;
     - Z_T → T is a gon of U;
     - rows for A ⊆ U with |A| ≤ 10: F_K ∨ R_t (t ⊆ A) ∨ Z_T (T ⊆ U − A).
   - A + r is 4-cap-free iff A is 4-cap-free and no 3-cap of A forms a cap with r. So the rows say "A is not a rooted
     Δ", and a ROOT counterexample with canonical auxiliaries satisfies every clause.
   - A weak Δ of S through r is exactly A + r for such an A, so "no weak Δ through r" is the ROOT failure.
   - Copy 2 of lr_cnf.py is the same CNF evaluated at the mirror image S′ = μ(S):
     - S′ is valid;
     - r′ = μ(l) ends a 4-cap;
     - the weak Δs of S′ through r′ are the images of the weak Δs of S through l.
   - An LR counterexample therefore satisfies both copies. **Sound.**
2. **CNF regeneration.**
   - `root_cnf.py 6 15` gives `6bd7e8b9…be7`, byte-identical to `round6/mainsession/root6/cnf/root6_m15.cnf`.
   - `lr_cnf.py` writes its source path into the comment line, so I ran it on that file (absolute path, as T4 did).
   - Result: `cae7193d2722f37b6ddd395c8ea3d1088817a7bb7b8c64c76a3f0a02c083399c`, equal to the claim and to both copies on
     disk.
3. **Proof archive integrity.** `zstd -dc t3/cert/t4lr6/t4_lr6_m15.lrat.zst` streams exactly 3,524,550,835 bytes with
   SHA-256 `fc824a77e126c92a0732e7450f570bbfcf905baf3ef72270f8059bf3f879e2fe`, equal to T3's certify.jsonl.
4. **Semantic control of the certified CNF** (`control_lr.py`, `8c72e1c5…`). For each set, the signs were added as
   units on variables 1..455, and the result was compared with V2's own brute force over all 2^15 subsets: validity,
   both hypotheses, and the weak Δs through r and through l. **It agreed in 18 of 18 runs** (copy 1, copy 2 and full CNF
   each):
   - the abstract root6_m15 and 8 real ROOT(6) failures (m15_it10, 12-17, 19): 0 weak Δs through r and 220-260 through
     l, giving copy 1 **SAT**, copy 2 UNSAT, full UNSAT;
   - their 9 mirror images: copy 2 **SAT**, copy 1 UNSAT, full UNSAT.

## What failed (budget, not mathematics)

The run was `replay_lr.sh 300` in unit `esr-agy-v2-lr6rep` (CPUQuota 15 %, MemoryMax 400M): a FIFO stream into
`cake_lpr --CML_HEAP_SIZE=300` against the regenerated CNF.
- It printed `CakeML heap space exhausted.` and exited 1. No verdict line.
- The peak RSS was 313 MB. The output is in `cake_h300.time` (`2b6454f4…`).

**Requested re-run** (a verifier with ≥ 2 GB; T3 needed 122 s at heap 1500):
`zstd -dc …/t3/cert/t4lr6/t4_lr6_m15.lrat.zst > FIFO & ~/.local/bin/cake_lpr --CML_HEAP_SIZE=1500
/home/jay/research/data/roadmap-20261115/pm1115/v2/lr6-m15-second/lr6_m15.cnf FIFO | grep -x 's VERIFIED UNSAT'`

## The rest of the statement

- **"Shares no code with T3's lr_cnf.py".** I did not read T3's encoder, so I did not check this.
- **First certificate.** Claim `lrr6-certified` is V1 CONFIRMED. V1's summary says V1 did **not** re-run cake_lpr there,
  because its heap of 1150 MB exceeded V1's budget. So neither LR(6) certificate at 15 points has had an independent
  cake_lpr re-run yet.
- **The logical consequence is correct given its inputs:**
  - |S| ≤ 14: ROOT(6) is CERTIFIED (ROOT6_MAIN.md), and ROOT gives a weak Δ through r whenever r ends a 4-cap.
  - |S| = 15: the certificates.
  - |S| ≥ 16: vacuous (base(5,6,16) UNSAT; claim `root6-m16-vacuous`, V1 CONFIRMED).

## Files

- Folder: `/home/jay/research/data/roadmap-20261115/pm1115/v2/lr6-m15-second/`.
- Scripts: `replay_lr.sh` (`6a31faf2…`), `control_lr.py` (`8c72e1c5…`), `v2lib.py` (`7c8b1ee0…`).
- `results.jsonl` (`7e6f8c96…`).
- Regenerated CNFs: `lr6_m15.cnf`, `root6_m15_regen.cnf`.
