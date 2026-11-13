# V3Z: covers and final acceptance table of mirror sub-case (ii)

Task `TASK.md` with H = 4.5, Z = d0456ff. Run 2026-10-20, 16:37 to about 18:35 UTC, on one 4-core 15 GB machine (`env.txt`).

**SAT: none.** No SAT record in any leaf or cover file of V3T, V3A, V3B, V3C, V3D, V3E or V3Z.

- Tools (`tools.txt`): CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (`make cake_lpr`, bundled example prints `s VERIFIED UNSAT`). F regenerated, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- verify/v3 at bdf319c. Inputs pinned at Zf = 14447d0d56c891a89a07a8141b50eae0ebfd44a7 (from `results/FINAL/READY.json`).
- Manifest (`inputs.txt`): jtree1..4 leaf lines 30151 / 12429 / 8850 / 28871 (WAVE1 skipped records 71, others 0); `v3_manifest.py`: leaves 73880, cases with leaves 278, problems 0. M.jsonl sha256 e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5, 73880 lines: both equal READY.json. C.jsonl (450 lines, sha256 3fff4486…f44411) committed as `cases_final.jsonl`.
- Covers (`covers.jsonl`, `--skip-leaves --jobs 4 --cap 3600`): 278 records, **278 VERIFIED** (140 by cake_lpr `s VERIFIED UNSAT`, 138 whose leaf list is the empty cube), no other verdict.
- Step 4: waited until every machine directory under V3B, V3C, V3D and V3E with an env.txt had a README.md (last one, V3D/D21, at 18:24 UTC), then built the table at branch head ff29bc68 with `scripts/aggregate_final.py` (a copy of `results/V3T/scripts/aggregate.py` changed only as step 4 (a) and (b) allow; run by `scripts/run_aggregate.sh`; the 78 input files are listed in `aggregate_inputs.txt`). Records read: 75459 leaf VERIFIED, 1 leaf REJECTED, 377 cover VERIFIED, 9 cover NOT_COVERED (the 9 NOT_COVERED are for leaf lists of older manifests; none matches a final leaf list).
- **Result (`accepted_final.tsv`, `problems.txt`): 278 of 278 wave cases ACCEPTED; 73880 of 73880 leaves have a VERIFIED record with matching cnf_sha256; every cover VERIFIED.** Per solved leaf: solve median 10.9 s, max 730.0 s; check median 3.0 s, max 52.0 s.
- Listed only (step 4 (a)): one REJECTED record next to a VERIFIED one, U4_L [-1014, -1040, 1065, -1112, 1134, 1155, -1245] in `results/V3A/V07/out.jsonl`.
- Step 5: no leaf without a VERIFIED record, so nothing to check (`leaves.jsonl` not created).
- Cases not accepted: **none**.

Summary (`summary.md`): 122 split obligations verified (Haudit task 3); 172 direct cases, 172 records `s VERIFIED UNSAT` with sha256 matching cases.jsonl (Haudit `t5_all172.jsonl`); 278 wave cases accepted here. Direct and wave cases are disjoint and make up all 450 cases. **All 450 cases of sub-case (ii) are covered.**
