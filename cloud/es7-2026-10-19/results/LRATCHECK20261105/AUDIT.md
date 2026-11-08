# lrat-check soundness audit, 5 Nov 2026

*This is the report of a read-only three-reader audit workflow plus a synthesis. Updates after it was written:*
- *`SIX10LINUX20261105` §5: all 94 proofs re-certified with cake_lpr.*
- *The 60 `ROT45CHORD20261105` transitivity patterns: re-certified with cake_lpr.*
- *The re-checks of §4 are in `recheck/README.md`. PRIMEFOLD Theorem E is now certified (7/7 accepted by cake_lpr),
  and so are the other cheap items, except two MIRRORETV encodings that have no committed generator.*
- *6 Nov: the defect was already public upstream before E2 (§5.1).*

## 1. Headline results

Every headline result except PRIMEFOLD Theorem E has a cake_lpr `s VERIFIED UNSAT` verdict for each SAT fact it needs. Every driver reads that verdict from cake_lpr's output line and none uses the exit code. Most C2 and C3 pieces are recorded verdicts: their proofs were deleted after both checkers passed, so they cannot be replayed now.

- **Theorem 1, threefold 33 (C3FINAL, C3LEAN): unaffected.** All 116,883 certified records in the 280 compose files carry cake_lpr `s VERIFIED UNSAT`. Both composers require that string (C3U2/tools/compose.py:151, C3AUDIT3/tools/mycompose.py:196). The 204 indispensable sigma pieces were re-solved with both checkers (C3PIECES/run/out.jsonl).
- **Theorem 2, mirror 33/34 (SYMZ, SYMLEAN): unaffected.** It is proved in Lean from Baek's theorem with no SAT, and cake_lpr accepted mirror33 and mirror34 (SYMZ/logs/chk_*_cake_lpr.out:1). The secondary 21-October Lean chain uses only cake_lpr facts:
  - 1,198 sub-case (i) leaves, checked in V1-0..3/V1-L and again in V1R;
  - 122 + 172 sub-case (ii) obligations, checked in Mii-S and again in Haudit;
  - 80,372 UNSAT records from WAVE1–4;
  - the V3 acceptance of 73,880 leaves and 278 covers.
- **Theorem 4, central 34 (C2FINAL): unaffected.** All 2,385 UNSAT records (2,320 wave + 65 pilot) have verdicts from both checkers. The hull cover has a solve-time cake_lpr verdict (C2FINAL/evidence/central34-cover/chk_hc34_cover_cake_lpr.out:1) and was accepted again in REPLAY §6. All 120 hexagonal hulls were re-checked with both checkers on hash-checked CNFs (C2RECHECK/hexcheck.jsonl).
- **Theorem 5, fivefold 35 (SYM5): unaffected.** cake_lpr accepted both P1 and L1 (SYM5/chk_P1_cake_lpr_heap30000.out:1, chk_L1_cake_lpr.out:1), and L1 also passed the hash-bound REPLAY. L2 is lrat-check only and is not needed.
- **Fourfold N(C4) = 28 (C4CUT, Fourfold32): unaffected.** cake_lpr accepted it (C4CUT/final.json:2), and so did the full replay of 1 Nov on hash-checked files. The six GP cuts are exact computation.
- **Threefold hexagon-free maximum 13 (SYMMAX, k = 6): unaffected.** cake_lpr accepted c3hex-15 and c3hex-16 in the hash-bound replay (REPLAY/out/replay_select.jsonl).
- **6-fold, k = 8, exactly 60 (C6UPPER, SIX60): unaffected.** Two encoders, each with 32/32 cubes accepted by cake_lpr (C6UPPER/logs/cake.txt, encb_cake.txt). The lower bound is exact computation.
- **7-fold, k = 8, exactly 64 (C7UPPER): unaffected.** cake_lpr accepted both encodings (logs/cake_A.out:1, cake_B.out:1), and they were replayed bound to their hashes (C6C7REVIEW/replay.py:134-145).
- **Mirror, k = 8, 46 (ES8SYM): unaffected.** cake_lpr accepted both encodings (mirror/encA_n23_cake.out:1, encB_r23_cake.out:1; input hashes in mirror/hashes.txt), and the bound is also proved in Lean from Baek's theorem.
- **N_mirror(7) ≤ 32 (MIRRORETV): unaffected as a bound.** It is proved in Lean from Baek's theorem. Its extra 17-point SAT certificate is not certified.
- **PRIMEFOLD Theorem E (note symmetric_extremal.tex): affected, not certified.** It is lrat-check only, and cake_lpr was never run on it (PRIMEFOLD/README.md:125-130). The note uses it in the abstract (l.50-51), thm:E (l.410-419), l.503-504 and the status table (l.653). Nothing shows it is false.

## 2. Affected claims

These rest on lrat-check alone, so they are **not certified**. None is shown false.

| Record | Claim | Why |
|---|---|---|
| PRIMEFOLD | Theorem E: ν(4..8) = 2, 3, 5, 9, ≤14, so one orbit of generic tiny clusters cannot reach 128 points for k = 9 | lrat-check only, with two encoders. cake_lpr never run. The binary hash is not logged. The note already labels it "lrat-check only". **This is the only headline-level item.** |
| SYM5 L2 (REPLAY now/lrat_small.jsonl:3) | c5-L2, a third proof (--unsat) of the fivefold CNF | lrat-check only (E2-patched build). cake_lpr never run. Redundant, because P1 and L1 settle Theorem 5. Listed in SYMMETRIC.md:233. |
| MIRRORETV | N(7,4,7) ≤ 16 by 17-point SAT, four encodings | lrat-check only (README.md:36, 124). Supplementary: the bound is proved in Lean from Baek's theorem. Cited in SYMMETRIC.md:102, 233; symmetric_es7.tex:200; symmetric_extremal.tex:260-261, 648. |
| ES8SYM single-orbit bound | m = 6, K = 8: cluster ≤ 9 (≤ 54 points); also m = 5 at n = 11 | lrat-check only (sets3/single_orbit_bounds/single_orbit_sat.log:4, 8). Appears only in the 2–3 Nov addendum. |
| SIX10LINUX20261105 §5 | The 54-, 52- and 56-point record sets do not extend by one layer (36/36, 26/26, 32/33 UNSAT) | lrat-check only, probably the unpatched Linux build. README.md:84 already says NOT certified. SIX60 does not use it. |
| C7UPPER calibration | (m,K) = (3,4)…(6,7) are UNSAT one layer past the known maximum | lrat-check only (logs/calib_unsat.log:1-4). Encoder validation only (k8_section.tex:118). |
| ROT456 | 40 transitivity patterns of m5K8t13 and 11 layer-5 patterns of d111111 are UNSAT | lrat-check only. For the 40, logs/cubes5_m5K8t13.txt records no checker verdict at all. The 5-fold case is open. |
| C, C2 controls | m9k5, hm9k5, m9k5.sub, m17k6, hm17k6, m17k6.sub, hm17k6.sub are UNSAT | lrat-check only, with pre-E2 builds from 19–20 Oct. Unpatched Mac builds from that date accept forged proofs (AUDIT3/A4_fivefold_layers/verify_A4-5/checker_controls.log:5-12). |
| E | n18k6m3 end-to-end control (3 cubes) | Unpatched 2e3b2dc only. ES(6) = 17 is known. E's three D3 results are certified through E2 and H2. |
| Mi-0..3 | Sub-case (i): 1,198 leaves, plus cover, gap and residual checks | Unpatched lrat-check only. Mi-2's parser would also accept `c NOT VERIFIED`. Superseded: cake_lpr re-checked the leaves (V1, V1R) and the cover is proved in Lean. |
| Mii-1..7 | Partial shards of sub-case (ii) | Unpatched lrat-check only. Superseded by Mii-S + WAVE + V3. |
| Mx | Independent re-encoding, partial closure | Unpatched lrat-check only. No sub-case is claimed. |
| B2 | (6,5,6)@16 pipeline control; 28 Knuth probe leaves | Unpatched lrat-check only. The value is known. |
| B3 | d14 cover of (7,5,7)@27; 17 spot checks | Unpatched lrat-check only. A cost estimate; the case is open. |
| G | k = 6 calibration at N = 17 | lrat-check only. The build is not recorded and no logs are committed. |

Some items look affected but are not:
- C's 12 spot cubes and C2's 4,535 + 749 mirror cubes were checked there by unpatched lrat-check only. H3 re-checked every one with cake_lpr on byte-identical CNFs (H3/logs/cube_lrat_*.jsonl, compare_mir.log:6-7).
- FOURPROBE's 20 patterns are refuted by an exact falsified-clause check (scripts/check_patterns.py).
- ROT45CHORD's 60 patterns were re-run in commit c3277920c, and cake_lpr accepted 60 of 60.

## 3. Unclear claims

| Item | Open question | What would settle it |
|---|---|---|
| ROT45CHORD20261105 threshold cubes | No result yet. The README says no cube finished under the v1 (lrat-check) supervisor between 04:46 and 12:59 KST, but the files in Git cannot confirm this. cubes4/o1234 was lost. | v1 supervisor logs showing no UNSAT verdict before 13:01 KST. Final results (due 16:00 KST) judged by v2's `^s VERIFIED UNSAT`. A re-run of o1234. |
| Patched lrat-check (2e3b2dc + E2) | AUDIT3 A2 item 11 argues it is sound, and SYMMETRIC.md §3 names it as trusted. The E2 patch closes only the empty-clause path. Reading lrat-check.c:154-162 suggests the remaining path with no conflict accepts only blocked clauses. That reading is untested. | No certified claim needs it. Reword both texts so that cake_lpr alone is the anchor. Otherwise, review the code and test forged proofs on the non-empty-lemma path. |
| Binary used for the Mac lrat-check-only runs (PRIMEFOLD, MIRRORETV, ES8SYM single orbit) | The logs do not say whether the patched build (f2046212…) or an unpatched one (bd7eb805…) ran. These claims are not certified either way. | A cake_lpr re-check (section 4) makes the question moot. |
| Binary used for the 5 Nov Linux runs (SIX10LINUX §5, first ROT45CHORD run) | The binary on PATH was not logged, and the only build on the host is unpatched. | A cake_lpr re-check of SIX10LINUX §5. The ROT45CHORD patterns are already re-checked. |
| <rot45-work-dir>/review_sup/lens_cutoff/lrat-check-strict | It lacks the E2 string and may carry a different fix. It is unknown whether any recorded verdict used it. | Diff it against 2e3b2dc and search the run logs for it. |

## 4. Recommended cake_lpr re-checks, smallest first

Where proof sizes are not recorded, the order goes by instance count and point count. Each re-check should solve again from the hash-recorded CNF and bind the cake_lpr log to the CNF and proof hashes.

1. **E n18k6m3:** 3 cubes, 18 points. Optional, since the value is known.
2. **C/C2 encoding controls:** 7 instances at 9 and 17 points. The proofs were deleted, so they must be solved again.
3. **C7UPPER calibration:** 4 instances, (m,K) = (3,4)…(6,7).
4. **ES8SYM single-orbit bound:** 2 instances (m = 6 at n = 10; m = 5 at n = 11).
5. **MIRRORETV n17_K7:** 4 encodings at 17 points.
6. **PRIMEFOLD Theorem E:** ν(4..8) with both encoders. The largest proof was 25,378,109 bytes and is not in Git; the CNF hashes are recorded. **This is the only re-check a headline needs. It is cheap, so do it first if priority beats size.**
7. **ROT456:** 11 layer-5 patterns and 40 transitivity patterns. Optional, since no 5-fold bound is claimed. For the 40, an exact falsified-clause check like FOURPROBE's may also work.
8. **SIX10LINUX §5:** 94 instances at 52–56 points. Not used by any theorem.
9. **SYM5 L2:** the 35-point fivefold CNF (P1 needed a heap of 30000, and 12000 ran out). Redundant.

No re-check is needed for Mi-0..3, Mii-1..7 or Mx, which cake_lpr routes supersede. B2 and B3 are controls and cost estimates, and G has no records to re-check.

## 5. Other findings

1. **The defect itself was already known.** E2 found the empty-clause hole on 20 Oct and patched it (E2/logs/lrat_check_soundness.md; tools/lrat-check-E2.patch, sha256 52721abd…). CERTIFICATES.md:38-40 already pins the patched binary (f2046212…). Commit c3277920c records the defect again without citing E2.
   - *Added 6 Nov:* it was also public upstream before E2 (`marijnheule/drat-trim`). Issue #31 (2022-07-22) reported it; commit cbd2915 (2022-10-19) fixed it; commit 5cd8ac3 (2024-04-21) brought it back, and it is still on master 2e3b2dc. Issue #42 and PR #43 (both 2026-09-29) report the regression with the same `p cnf 1 1 / 1 0` + `2 0 0` reproduction and a one-line fix. So E2's 20 Oct finding was an independent rediscovery of a publicly known defect; the credit for finding and patching it locally stays with E2.
2. **New: the Linux setup builds the unsound checker.** The host's only drat-trim (<drat-trim-src>, 2e3b2dc, built 4 Nov 21:42) is unpatched: lrat-check.c:161 is commented out and there is no E2 line. The "Setting up on Linux" section of STATUS20261104/README.md does not mention the patch.
3. **New: the hole is narrower than the coordinator described.** This comes from reading the source, not from a test. For a non-empty lemma, acceptance with no RAT candidates also requires `intro[-pivot] == 0`, which means no clause contains the negated pivot. Such a lemma is a blocked clause, which preserves satisfiability. The unsound path is the empty clause, and that is the path E2 closes.
4. **New: two lrat-check drivers parse verdicts incorrectly.**
   - Mi-2/scripts/shard.py:65 accepts output that contains "VERIFIED" and no "FAIL", so it also accepts `c NOT VERIFIED` and the lowercase lemma-failure line. Its 284 records do not show even an lrat-check acceptance.
   - ROT45CHORD tools/implane.sh:5 has the same problem; that record is already marked UNRELIABLE.
   - No cake_lpr driver has this problem: all compare the exact output line.
5. **New: a README claims more than its log shows.** ROT456/README.md:78 says lrat-check accepted the 40 patterns, but the log has no verdict lines for them.
6. **Cross-group closure.** Group 1 left open that FINAL's sub-case (ii) closure rests on WAVE1–4 records it did not audit. Group 2's tally closes this: 80,372 UNSAT records, all accepted by cake_lpr, with no lrat-check fields. The 2 UNSAT_UNVERIFIED records are excluded downstream.
7. **Record fixes:**
   - Reword SYMMETRIC.md §3 and AUDIT3 A2 item 11 so that cake_lpr alone is the anchor.
   - Add a pointer in E/README.md to the E2 and H2 re-checks.
   - Add the cake_lpr line to C2C34/logs/central34_status.txt (the log exists in C2FINAL/evidence).
   - Log the checker binary's sha256 in every future run.