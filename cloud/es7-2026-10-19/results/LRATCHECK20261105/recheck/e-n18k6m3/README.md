# e-n18k6m3: cake_lpr re-check of E's n18k6m3 end-to-end control (5 Nov 2026)

**Result: the 3 LRAT spot-check cubes are UNSAT, and cake_lpr printed `s VERIFIED UNSAT` for all 3.**

Claim checked: `E/README.md` §2, "End-to-end test". 3 of 3 spot-checked cubes passed lrat-check
(`E/runs/test_n18/lrat.jsonl`), using the unpatched 2e3b2dc build only.

## Regeneration

- Base CNF: `python3 tools/symmetric/symcnf.py 18 6 3 -o gen/n18k6m3.cnf --map gen/n18k6m3.json`. It has 4,203
  variables and 335,648 clauses.
- Its SHA-256 `02c5ffc2bce862185b48a731a59a3006e708fa151584e9ae2d32f465d3790a6a` equals the full hash in
  `E/logs/cnf_sha256.txt`.
- Cube CNFs: `mkcubes.py` writes base + cube units byte for byte as `E/tools/lratcube.py` does. That means a new
  header, the text after the original header copied unchanged, and then the unit clauses in cube order.
- The cubes are taken in the order of `E/runs/test_n18/lrat.jsonl`:
  - cube1_d7: [-284, -324, -283, -91, -183, 269, 58];
  - cube2_d9: [-284, 324, 201, 275, 313, -127, 219, 94, 122];
  - cube3_d6: [284, -219, 109, -13, 8, 87].
- Their headers give 335,655, 335,657 and 335,654 clauses. These match the "parsed a formula with …" lines recorded
  in lrat.jsonl.
- No per-cube hash was recorded, so the binding is through the base CNF.

## Check

- `cadical --lrat --binary=false -q X.cnf X.lrat`, then `cake_lpr --CML_HEAP_SIZE=12000 X.cnf X.lrat > X.cake.log`.
- The verdict is `grep -qx 's VERIFIED UNSAT'`. lrat-check was not used.
- Proofs were 0.15, 6.0 and 4.6 MB. The runs took about 5 s in total (13:24 KST).

**Supplementary (beyond the claim):** the whole n18k6m3 CNF is also UNSAT, and cake_lpr printed `s VERIFIED UNSAT`
(`supplementary/`). Before this, only a plain solve had recorded it (`E/logs/controls.log`).

## Files

- `results.tsv`.
- `runs/X.*` and `supplementary/n18k6m3.*`: the artifacts, with `X.hashes.txt`.
- `gen/hashes.txt`.
- `aux_hashes.txt`: the scripts and logs.
