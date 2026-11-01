# V3D D12: shard 12 of 24

Fourth acceptance pass of mirror sub-case (ii). Run 2026-10-20, from 15:53:56 to about 17:20 UTC, on 4 cores with 15 GB RAM.

## Tools and inputs
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa. Its bundled example prints `s VERIFIED UNSAT`.
- F.cnf was regenerated with gen_etv.py and mirgen.py. sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches)
- input commit a71d30d, verify/v3 at commit bdf319c
- worklist.jsonl: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (matches)
- Cross-check against 3e4dbaae3: Mzd.jsonl has sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8 and 70215 lines (matches). All 22682 work-list (case, lits) pairs occur in it. PASS. See inputs.txt for details.

## Results (out.jsonl)
- Shard leaves: 945. Checked: 945. Still unchecked: 0.
- VERIFIED 945, REJECTED 0, SAT 0, TIMEOUT 0. Every record has cake_lpr = `s VERIFIED UNSAT`.
- No REJECTED records had an empty cake_lpr field, so no rechecks were needed.
- solve_s: sum 15499.32 s, median 9.91 s, max 231.92 s
- check_s: sum 3710.88 s, median 2.91 s, max 22.23 s
