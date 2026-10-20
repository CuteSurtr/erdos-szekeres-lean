# V3A V06: first pass, shard 6 of 16, from-scratch acceptance check of mirror sub-case (ii)

Run 2026-10-20, 09:07:46Z to 10:48Z (stopped at the time limit). 4 cores, 15 GB RAM (env.txt).

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04 (/opt/bin/cadical)
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr`; the bundled example prints `s VERIFIED UNSAT`
- F regenerated (gen_etv.py 33 7 7 7 --mirror, then mirgen.py --interior --yflip-unit): sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d, which matches
- verify/v3 at commit 7c6d70c (worktree /opt/v3src); inputs at commit a033a13 (worktree /opt/in)
- v3_jsonl_leaves.py: dirs 72, leaf lines 17942, skipped records 47
- v3_manifest.py: 17,989 leaves in 100 cases, 0 problems (same as the reference machine)
  - M.jsonl sha256 4282db60c19aa5cb61a3e27e12f25f134f788d112821fef0ca32ea428940f07e
  - C.jsonl sha256 8724fba58ba65d45c331522be734f781199a55e7abaaec42fe0e60a77f89b82b
- Mr.jsonl (M minus the 40 cases ACCEPTED in results/V3T/accepted.tsv, which removes 357 records; idx renumbered): n = 17,632 leaves in 60 cases,
  sha256 5f114f4ea0b3f71682f08375dfe977e1bfec9e86142fb0f55eef7396f5825def
- Details are in tools.txt and inputs.txt.

## Run
`v3_check.py --root /opt/in/cloud/es7-2026-10-19 --base /opt/work/F.cnf --manifest /opt/work/Mr.jsonl --shard 6 --nshards 16 --out /opt/work/out/out.jsonl --work /opt/work/v3w --jobs 4 --cap 1800`
(OUT kept outside the checkout; out.jsonl here is a copy.)

## Results (out.jsonl, 1023 records)
```
leaf 1019 {'VERIFIED': 1019}
 solve_s: sum 19588.8 median 16.28 max 225.08
 check_s: sum 4238.2 median 3.26 max 22.82
cover 4 {'VERIFIED': 4}
 solve_s: sum 0.1 median 0.03 max 0.03
 check_s: sum 0.0 median 0.00 max 0.02
my leaves 1102 verified 1019 unchecked/unverified 83
```
- Leaves: 1019 VERIFIED, 0 REJECTED, 0 SAT, 0 TIMEOUT. Of the 1102 leaves in this shard (idx ≡ 6 mod 16), **83 are still unchecked**; the second pass will pick them up.
  When the run was stopped, the 4 leaves in flight (including idx 15926, 16262, 16358) were killed without writing a record.
- Covers: 4 of 4 VERIFIED (U11_L13 with 1 leaf, U4_L9 with 114, U8_L5 with 116, U_L2-7 with 377), 0 NOT_COVERED.
- Every verdict comes from cake_lpr printing exactly `s VERIFIED UNSAT`. The largest text LRAT proof was 200 MB.
- No SAT, REJECTED, TIMEOUT or NOT_COVERED record.
