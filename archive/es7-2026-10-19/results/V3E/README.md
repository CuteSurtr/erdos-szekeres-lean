# V3E: fifth acceptance pass of mirror sub-case (ii)

This pass checks every leaf of the final manifest, at Zf = 14447d0d5 (`results/FINAL/READY.json`), that had no VERIFIED record at Zf and that no running machine was checking.

`worklist.jsonl` (3801 records, sha256 5c10bc043fbacbd397ea5867207b2a3fedebeb0174f98d3590b18c6d564baac9) was made by `scripts/build_worklist_e.py REPO 14447d0d5 OUT --skip results/V3D/worklist.jsonl:0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23:24`:
- The manifest at Zf is built exactly as V3B step 2 does it (verify/v3 at bdf319c; `v3_jsonl_leaves.py` on `results/WAVE1` to `results/WAVE4`, then `v3_manifest.py` over the four pairs in order): 73880 lines, sha256 e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5, the values in READY.json. As a control the script rebuilds V3B's list at 066eaa9 and checks its sha256.
- verified keys at Z 54733 from 74 files. manifest at Z 73880 | without VERIFIED 19147 | left out (running machines) 15346 | work list 3801.
- Left out: the records of the work lists of machines still running at Zf (all 24 V3D machines, D00 to D23, were running: `--skip results/V3D/worklist.jsonl:0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23:24`); those machines are checking them.
- By case: U3_L 3204, U_L7 474, U_L8 81, U_L2 13, U_L6 12, U_L9 12, U_L5 5. By source: WAVE4 3665, WAVE2 81, WAVE3 55.

The machines are E00 to E07, machine i taking the records with idx = i mod 8 (`TASK.md`). Any leaf a V3D or V3E machine leaves unchecked is listed by the final acceptance table (`results/V3Z/`), which re-derives the manifest from the wave directories at Zf and needs a VERIFIED record for every leaf and a VERIFIED cover for every case; V3Z rechecks up to 3000 leftover leaves itself.
