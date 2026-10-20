# V3A V03: first-pass v3 acceptance check, machine 3 of 16 (shard 3, nshards 16)

Run window 09:05 to 10:55 UTC 2026-10-20, 4 cores. v3_check ran from 09:06:56 until it was stopped at about 10:48.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). Details are in tools.txt.
- F = m33k7int.sub.cnf rebuilt from scratch, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Inputs at commit a033a13; verify/v3 at commit 7c6d70c.
- v3_jsonl_leaves: dirs 72, leaf lines 17942, skipped records 47. v3_manifest: 17989 leaves, 100 cases with leaves, 0 problems (same as the reference run).
- M.jsonl sha256 4282db60c19aa5cb61a3e27e12f25f134f788d112821fef0ca32ea428940f07e
- Mr.jsonl (40 ACCEPTED cases removed): 17632 leaves in 60 cases, sha256 5f114f4ea0b3f71682f08375dfe977e1bfec9e86142fb0f55eef7396f5825def

## Results (out.jsonl)
```
shard leaves 1102 shard cases 4 ['U10_L7', 'U4_L', 'U7_L4', 'U_L2-4']
leaf verdicts {'VERIFIED': 909}
cover verdicts {'VERIFIED': 3, 'NOT_COVERED': 1}
leaves without VERIFIED record 193
leaf solve_s: sum 20189.4 median 18.00 max 277.6
leaf check_s: sum 3822.1 median 3.02 max 23.4
cover NOT_COVERED U4_L nleaves 147 sources ['jtree/W29/U4_L']
```
- Leaves: 909 VERIFIED, 0 REJECTED, 0 SAT, 0 TIMEOUT. 193 of this shard's 1102 leaves are still unchecked and go to the second pass.
- Covers for this shard's cases (U10_L7, U4_L, U7_L4, U_L2-4): 3 VERIFIED, 1 NOT_COVERED.
- Times above are for leaf jobs. Solve time is CaDiCaL; check time is cake_lpr.

## NOT_COVERED
U4_L: the cover CNF ({case cube} + {not leaf} over its 147 leaves) is SAT (rc 10), so these leaves do not cover the case cube. The only source is jtree/W29/U4_L, made by v3_jsonl_leaves from results/WAVE1/W29/U4_L/leaves.jsonl. Most likely the wave had not closed U4_L by a033a13, so its leaves.jsonl was incomplete. This is a gap in the leaf set, not a SAT case. U4_L cannot be accepted from these inputs.
Record: `{"kind": "cover", "key": "U4_L", "nleaves": 147, "leaves_sha256": "5df1cb08b8c3c665561b57b4620bc45bc6abb99ed7c81c5ac1870e4db0284e9f", "cnf_sha256": "696fe585805ba6c5cf294cea3d1875564e52d87a1293537121bcacb3f9c711cf", "rc": 10, "solve_s": 0.04, "cake_lpr": "", "check_s": 0.0, "verdict": "NOT_COVERED"}`

No SAT, REJECTED or TIMEOUT leaves.
