# V3E E00: shard 0 of 8

- Tools: CaDiCaL 3.0.1 at c60730422e758ef1cebe7aeddf2dda31c996bf04; cake_lpr at a36874a8b750b43fe4b385b8ddbf5b033e46a3fa (bundled example: `s VERIFIED UNSAT`). See tools.txt.
- F.cnf regenerated from source: sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (matches).
- Input commit d0456ff; verify/v3 from commit bdf319c.
- worklist.jsonl: sha256 5c10bc043fbacbd397ea5867207b2a3fedebeb0174f98d3590b18c6d564baac9, 3801 lines (matches).
- Cross-check at 14447d0d5: v3_manifest.py gives 73880 leaves, 278 cases, 0 problems; Mzd.jsonl sha256 e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5 (matches). All 3801 work-list (case, lits) pairs occur in it. See inputs.txt.

## Results (out.jsonl)

Shard 0 holds 476 leaves (`--skip-covers`, `--jobs 4`, `--cap 1800`). All 476 were checked, so none are left unchecked.

| verdict | count |
|---|---|
| VERIFIED | 476 |
| REJECTED | 0 |
| SAT | 0 |
| TIMEOUT | 0 |

Every record has solver rc 20 and cake_lpr `s VERIFIED UNSAT`. No leaves needed a step-4 re-check, because there were no REJECTED records with an empty cake_lpr field.

| time (s) | sum | median | max |
|---|---|---|---|
| solve | 6839.1 | 8.57 | 202.38 |
| check | 1885.2 | 3.17 | 21.14 |

Wall time of the run: 16:38:56 to about 17:17 UTC on 2026-10-20.
