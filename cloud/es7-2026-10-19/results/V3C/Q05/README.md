# V3C Q05: shard 5 of 16, third acceptance pass of mirror sub-case (ii)

Result: 774 of 774 leaves VERIFIED (cake_lpr printed `s VERIFIED UNSAT` for each). No REJECTED, SAT or TIMEOUT leaves, and none are left unchecked.

Tools (details in tools.txt):
- CaDiCaL 3.0.1, commit c60730422e758ef1cebe7aeddf2dda31c996bf04, built from source as /opt/bin/cadical
- cake_lpr, commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr`; its bundled example prints `s VERIFIED UNSAT`
- verify/v3 as of commit bdf319c

Inputs (details in inputs.txt):
- F.cnf was regenerated (gen_etv.py + mirgen.py). Its sha256 is 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d, which matches.
- Input commit 71bcca7. The work list results/V3C/worklist.jsonl has sha256 aeb4a3f19a5979e6d8fb9c4bc68b303de1332ea2a2677e1d4f69833fb6025abc and 12380 lines, both as expected.
- Cross-check at fdd0393 passed: Mfd.jsonl has sha256 34676b0c112438285b15a2cdb63291b9e63b242a98ac84b38d1d0d9c642afbfb and 47533 lines, and all 12380 work-list (case, lits) records occur in it.

Run: v3_check.py --shard 5 --nshards 16 --skip-covers --jobs 4 --cap 1800, from 13:52 to 15:05 UTC on 2026-10-20 (4 cores, 15 GB RAM). OUT was kept outside the checkout at /opt/work/out/out.jsonl and copied here (sha256 29ecb5df60c67d55260983f0d362849ba4dad69db25e71e180e8d368276c599a).

| verdict | count |
|---|---|
| VERIFIED | 774 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |
| unchecked | 0 |

Every record has rc 20 and cake_lpr `s VERIFIED UNSAT`. No REJECTED leaf had an empty cake_lpr field, so step 4 needed no rechecks.

Times (seconds):
| | sum | median | max |
|---|---|---|---|
| solve (CaDiCaL) | 13678.6 | 10.21 | 342.08 |
| check (cake_lpr) | 3271.0 | 3.12 | 26.91 |
