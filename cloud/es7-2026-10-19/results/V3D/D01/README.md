# V3D D01: shard 1 of 24

Shard 1 is finished. All 946 leaves are VERIFIED (each with cake_lpr printing `s VERIFIED UNSAT`).

- Tools: CaDiCaL 3.0.1 at commit c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at commit a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (its bundled example printed `s VERIFIED UNSAT`). Both built from source. See tools.txt.
- F = m33k7int.sub.cnf, regenerated with gen_etv.py and mirgen.py: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit a71d30d; verify/v3 at commit bdf319c.
- Work list results/V3D/worklist.jsonl: sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9, 22682 lines (both match).
- Cross-check at 3e4dbaae3: the v3_manifest output Mzd.jsonl has sha256 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8 and 70215 lines (both match), with 0 problems. All 22682 work-list (case, lits) pairs occur in it. See inputs.txt.
- Run: v3_check.py --shard 1 --nshards 24 --skip-covers --jobs 4 --cap 1800, from 15:24 to 16:46 UTC on 4 cores with 15 GB RAM.

## Verdicts (946 leaves)

| VERIFIED | REJECTED | SAT | TIMEOUT | unchecked |
|---|---|---|---|---|
| 946 | 0 | 0 | 0 | 0 |

No REJECTED leaf had an empty cake_lpr field, so the step-4 recheck was not needed.

## Times (seconds)

| | sum | median | max |
|---|---|---|---|
| solve | 15924.1 | 9.91 | 322.25 |
| check | 3867.6 | 3.05 | 21.76 |

There were no SAT, REJECTED or TIMEOUT leaves. Per-leaf records are in out.jsonl.
