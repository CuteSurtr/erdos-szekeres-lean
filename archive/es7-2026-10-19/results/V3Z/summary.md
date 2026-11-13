# Sub-case (ii) of the mirror split: final statement (V3Z)

F = `m33k7int.sub.cnf`, sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d (regenerated here, matches), split into 450 hull cases (`results/Mii-S/cases.jsonl`, `results/Mii-S/cases.icnf`, argument in `results/Mii-S/soundness.md`). The only trusted checker is cake_lpr (a36874a8); every count below is of records whose cake_lpr verdict is `s VERIFIED UNSAT` (or, for a cover whose leaf list is the empty cube, the trivial cover noted by `v3_check.py`).

1. **The split (122 obligations).** `results/Haudit/t3_cover_lrat.jsonl`: 122 records (root plus 121 up:U), 122 distinct obligations, all `s VERIFIED UNSAT`; all 122 CNF sha256 equal those in `results/Mii-S/cover_lrat.jsonl`.
2. **172 direct cases.** `results/Haudit/t5_all172.jsonl`: 172 records for 172 distinct cases; 172 have `cake_lpr` = `s VERIFIED UNSAT` and a `cnf_sha256` equal to that case's `cnf_sha256` in `results/Mii-S/cases.jsonl`. They are exactly the 172 cases with method `direct` in `cases_final.jsonl`.
3. **278 wave cases.** Manifest at Zf = 14447d0d56c891a89a07a8141b50eae0ebfd44a7 (73880 leaves, sha256 e01af167266dc044078798355f76f9f8d36c74d1b8843aeab90072b644ea83b5, equal to `results/FINAL/READY.json`). All 278 covers VERIFIED here (`covers.jsonl`). `accepted_final.tsv` (built by `scripts/aggregate_final.py` over the 78 record files in `aggregate_inputs.txt`, at branch head ff29bc68): 278 of 278 wave cases ACCEPTED, 73880 of 73880 leaves with a VERIFIED record whose CNF sha256 matches the CNF rebuilt from F + case cube + leaf. No SAT record anywhere. They are exactly the 278 cases that are OPEN in `cases.jsonl`.
4. **Cases not accepted:** none.

The 172 direct cases and the 278 accepted wave cases are disjoint and together are all 450 cases of `results/Mii-S/cases.jsonl`.

**Statement:** all 450 cases of sub-case (ii) are covered: each is UNSAT with a cake_lpr-verified proof (directly, or by leaves whose cover is verified), and the 450-case split is certified by the 122 verified obligations. By the argument in `results/Mii-S/soundness.md`, F is unsatisfiable.
