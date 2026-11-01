# V3A V07: first pass of the v3 acceptance check of mirror sub-case (ii), shard 7 of 16

Run 2026-10-20 09:05–10:47Z on one cloud VM (4 cores, 15 GB RAM; see `env.txt`).

## Inputs and tools
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa
  (bundled example: `s VERIFIED UNSAT`). Binary sha256s are in `tools.txt`.
- F regenerated (gen_etv.py 33 7 7 7 --mirror, then mirgen.py --interior --yflip-unit):
  sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- verify/v3 scripts at commit 7c6d70c; inputs at commit a033a13.
- v3_jsonl_leaves.py: dirs 72, leaf lines 17942, skipped records 47.
- v3_manifest.py: 17,989 leaves in 100 cases, 0 problems (same as the reference machine).
  M.jsonl sha256 4282db60c19aa5cb61a3e27e12f25f134f788d112821fef0ca32ea428940f07e; C.jsonl 8724fba58ba65d45c331522be734f781199a55e7abaaec42fe0e60a77f89b82b.
- Mr.jsonl: I removed the 40 cases marked ACCEPTED in results/V3T/accepted.tsv (357 records) and renumbered the rest.
  It has n = 17,632 leaves in 60 cases, sha256 5f114f4ea0b3f71682f08375dfe977e1bfec9e86142fb0f55eef7396f5825def.
  This matches V00, V03, V09 and V14.
- Command: `v3_check.py --shard 7 --nshards 16 --jobs 4 --cap 1800`. OUT was kept at /opt/work/out/out.jsonl and copied to `out.jsonl` at each commit.

## Results (out.jsonl)
- leaf records 947: {'VERIFIED': 946, 'REJECTED': 1}
- my leaves 1102; VERIFIED 946; without a VERIFIED record 156 (of which 1 have a non-VERIFIED record, 155 were never checked)
- my cover cases (4): U11_L8, U5_L, U9_L, U_L2-9
- cover records 4: {'VERIFIED': 2, 'NOT_COVERED': 2}
- leaf solve (CaDiCaL): n 947, sum 20356.0 s (5.65 h), median 17.54 s, max 292.8 s
- leaf check (cake_lpr): n 947, sum 3447.2 s (0.96 h), median 2.74 s, max 52.0 s
- cover solve: n 3, sum 0.1 s (0.00 h), median 0.04 s, max 0.1 s; cover check: n 3, sum 0.0 s (0.00 h), median 0.00 s, max 0.0 s
- trivially VERIFIED leaves (contradict cube, no solve): 0

Non-VERIFIED records:

- leaf REJECTED: idx 2119, case U4_L, lits [-1014, -1040, 1065, -1112, 1134, 1155, -1245], rc 20, solve 216.27 s, proof 159754492 B, cake_lpr '', sources ['jtree/W29/U4_L']
- cover NOT_COVERED: case U9_L, 10 leaves, rc 10, cover CNF sha256 f64c7d8421b3756f53ae76d9b342c21ee2da6d275f37ef7d014bf4814701dde1, leaf source dirs ['jtree/W30/U9_L', 'results/WAVE1/W30/U9_L']
- cover NOT_COVERED: case U5_L, 525 leaves, rc 10, cover CNF sha256 85a3885240263484240911daeba99f9349a8c90dc32a12316958dc1a9ea96dc4, leaf source dirs ['jtree/W27/U5_L']
- cover VERIFIED: case U11_L8, 1 leaves (the empty cube is a leaf)
- cover VERIFIED: case U_L2-9, 122 leaves

## Notes
- **No SAT leaf.** No leaf TIMEOUT.
- **REJECTED leaf 2119 (U4_L)** comes from a memory-cgroup OOM kill of cake_lpr (anon RSS 4.2 GB) while 4 jobs ran at once.
  This is REVIEW.md RISK-3/RISK-5, a transient failure; it does not show a bad proof.
  A diagnostic re-run by hand reproduced the same CNF sha256 and proof size, and cake_lpr printed `s VERIFIED UNSAT` in 15 s.
  See `diag-leaf2119.txt`. That re-run was not done through v3_check, so it does not count.
  The second pass must re-check this leaf; for proofs this large it may need fewer parallel jobs.
- **NOT_COVERED U9_L and U5_L:** the leaf sets at a033a13 do not cover these cases. Their wave VMs were presumably still running (U5_L leaves come only from jtree/W27; U9_L leaves come from W30).
  A satisfying assignment of the cover CNF is an uncovered region; it says nothing about F.
  These cases cannot be accepted from this manifest.
- The run was stopped at 10:47Z, and 155 of my leaves have no record. Jobs that were running when the run stopped wrote no record.
  The second pass will pick up every leaf without a VERIFIED record: the 155 unchecked leaves plus idx 2119.
