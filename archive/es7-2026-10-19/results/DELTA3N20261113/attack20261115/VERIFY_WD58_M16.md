**Verdict: CONFIRMED** (claim `wd58-m16`, verifier V2; updated 15 November 2026, 16:55 KST). Label CERTIFIED is
correct. Weak D(5,8) holds for every signotope, and hence every point set, with at most 16 points. The 16:26 verdict
below lacked only an independent cake_lpr re-run, and that re-run exists.

**Update 16:55: an independent cake_lpr re-run by the main session, checked by V2.** The folder is
`round6/mainsession/wd58recake/`, made with `recake_generic.sh`.
- **Script:** `zstd -dc <kept .zst> | tee FIFO | sha256sum`, then `cake_lpr --CML_HEAP_SIZE=2000 <CNF> FIFO`.
- **Inputs:**
  - CNF `t3/cnf/wd58_m16.cnf`, SHA-256 `d6d34086…f181`, equal to the claim and to V2's regeneration;
  - archive SHA-256 `5ba30ae7…5f7e`, equal to V2's own hash of the kept file;
  - streamed LRAT SHA-256 `68c70856…8168`, equal to the claim and to V2's own stream hash.
- **Output:** `cake.out` is exactly `s VERIFIED UNSAT` (17 bytes, `grep -x` count 1). cake_lpr exited with status 0
  after 216 CPU s, with a peak RSS of 2.06 GB. It finished at 16:23:21, three minutes before my original verdict, which
  did not know of it.

The re-run was made by the main session, not by the claim's author (T3) and not by V2.

---

*Original verdict, 16:26:* NOT CONFIRMED (incomplete, not refuted), from 16:19-16:25 KST. Three things passed: the encoder review, the byte-identical regeneration of both the m = 15 control
CNF and the m = 16 CNF, and the hashes of the proof archive and of the full decompressed proof stream. The
independent cake_lpr re-run was **not attempted**, because it needs about 2 GB (T3 used heap 1700 MB) and V2's budget
is 0.4 GB. Today V2's heap-300 attempts on proofs of 2.35 GB and 3.5 GB both ended in "CakeML heap space exhausted"
(VERIFY_TSPM6_14.md, VERIFY_LR6_M15_SECOND.md), and this proof (5.57 GB) and its CNF (about 13 M literals) are larger
still. The CERTIFIED label for m = 16 therefore rests only on T3's own cake_lpr run until a larger verifier re-runs it.

# Independent check: weak D(5,8) at 16 points

**Claim (filed by T3).** F(5,8,16;weak) is UNSAT:
- the CNF is DELTA2N's eager encoder `Enc(5,8,16,weak)` with all 2^16 subsets in the pool;
- the LRAT is 5,572,040,812 bytes, and T3's cake_lpr printed `s VERIFIED UNSAT` at heap 1700.

With DELTA2N's certificates for m ≤ 15, weak D(5,8) would then hold for every signotope and point set with at most
16 points.

**Definitions.** DELTA2N20261113 README §1-§2 (D(a,n;weak), (a,n)-valid, F(a,n,m;weak), Lemma S).

## What passed

1. **Encoder soundness.** I read `DELTA2N20261113/tools/eager_cert.py` (`055ea8ab…`, class `Enc`, lines 29-73 and
   199-219) against Lemma S, and T3's wrapper `t3/tools/gen_weakD.py` (`6733f027…`), which only calls
   `Enc(a,n,m,False).write(out,0,m)`.
   - **Base clauses.** Each holds for a valid signotope:
     - the signotope axioms (8 ternary clauses per 4-tuple);
     - for every 5-set, some consecutive triple is a cup. This is no 5-cap, because consecutive caps force all caps.
     - for every 8-set G and every split of its inner points into a cap part A (|A| ≤ 2) and a cup part B, "not (G₀+A+G₇
       a cap and G₀+B+G₇ a cup)". Such a cap–cup pair with common ends is a convex 8-set, and a cap part with ≥ 5
       points contains a 5-cap.
   - **Witnesses**, one direction only:
     - Y_K → K is a 4-cap (consecutive triples −);
     - Q4_Q → the 4-point rule (x_xyz = x_xyw and x_xzw = x_yzw);
     - Z_G → Q4 of all 4-subsets of the 7-set G.
   - **Pool.** For every D ⊆ [16] there is one clause: ∨Y_K (K ⊆ D) ∨ ∨Z_G (G ⊆ [16]∖D), meaning "D fails".
   - A counterexample with canonical witnesses satisfies every clause, so **sound**. The encoder was also reviewed in
     DELTA2N's VERIFY_D1.
2. **Regeneration**, in unit `esr-agy-v2-wd58` (CPUQuota 15 %, MemoryMax 400M; peak RSS 98 / 157 MB):
   - `gen_weakD.py 5 8 15` → `228120eefd868a689c0de199d2a9cee55e190150353fcd8dcdd6c1a044207dbb`, `p cnf 9620 421676`.
     This equals DELTA2N's `cnf_hashes.tsv` line 51, the certified m = 15 case with the exact verdict line.
   - `gen_weakD.py 5 8 16` → `d6d340863685d92eb9fdcdc1a7a46b957a39b085af5190c0330adc90aa51f181`, `p cnf 15640 778924`,
     equal to the claim.
3. **Proof integrity.**
   - `t3/cert/wd58/wd58_m16.lrat.zst` is 1,226,706,336 bytes with SHA-256 `5ba30ae75d958dfaaf02b8f0195173e0928ff9f87ea4c7d4b5f4254fe5bc5f7e`.
   - Its decompressed stream is **5,572,040,812 bytes**, SHA-256 `68c70856c1618ec85ab2151b484ba77ddc3b69462e52ddbaa51c65d5e11f8168`.
   - All values equal the claim. T3's `wd58_m16.cake.out` contains exactly `s VERIFIED UNSAT`.
4. **"All sets with at most 16 points".** DELTA2N certifies (5,8) weak for m = 7..15 (cnf_hashes.tsv lines 31-51, each
   with `s VERIFIED UNSAT`). m ≤ 6 is trivial, since there is no convex 7-set and Δ = ∅ works. So with m = 16 the range
   ≤ 16 is complete, given the certificate. "No ES(8) bound changes" is correct: the ledger needs all sizes.

## What was not done

- **No independent cake_lpr re-run** (budget; see the verdict line). Requested command, for a unit with MemoryMax ≥
  2.5G:
  `zstd -dc /home/jay/research/data/roadmap-20261115/pm1115/t3/cert/wd58/wd58_m16.lrat.zst > FIFO &
  ~/.local/bin/cake_lpr --CML_HEAP_SIZE=1700 /home/jay/research/data/roadmap-20261115/pm1115/v2/wd58-m16/wd58_m16.cnf FIFO | grep -x 's VERIFIED UNSAT'`.
  The CNF there is V2's regenerated copy, byte-identical to the claim's.
- No new semantic control. The encoder is the hash-identical DELTA2N encoder, whose controls (C1-C6) are on record.

## Files

- Folder: `/home/jay/research/data/roadmap-20261115/pm1115/v2/wd58-m16/`.
- `job.sh` (`3a42afc1…`), `results.txt` (`cd242a7b…`).
- Regenerated CNFs: `wd58_m15.cnf`, `wd58_m16.cnf`.
