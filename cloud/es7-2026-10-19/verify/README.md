# Leaf list for the mirror sub-case (i) instance

`hull_leaves.icnf` lists the 1,198 leaf cubes with which the shard runs Mi-0..Mi-3 closed
`hm33k7.sub.cnf` (sha256 `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d`,
the file that `results/H3`'s Lean generator writes byte for byte).

- Source: `results/Mi-{0,1,2,3}/leaves.jsonl` at commit d74db44. A leaf is a record with a
  `cube`, status UNSAT/UNSATISFIABLE and an lrat-check verdict; split nodes, cover/gap checks and
  residual checks are not leaves. Each cube keeps the decision order of its record (root first).
- Lines are sorted by (length, literals); format `a l1 ... lk 0`.
- sha256 of the file: `cc11270a57ebe85ad1d5c83b15da0a3439521cc7ebd50432f16c223a1b2478b6`.
- Depths: 118 leaves of depth 7, 635 of 13, 1 of 18, 316 of 19, 128 of 25.
- Partition check (`extract_hull_leaves.py`): in the trie of the cubes every internal node has
  exactly two children, x and -x, and no leaf is a prefix of another, so the cubes form a complete
  binary partition of the assignments; the weights 2^-depth sum to exactly 1.

The shards checked their proofs with drat-trim's `lrat-check` at 2e3b2dc. results/E2 found that
this build accepts an unjustified empty clause (`logs/lrat_check_soundness.md` there), so those
verdicts do not certify UNSAT. The leaves have to be re-checked with a sound checker
(`cake_lpr`, and lrat-check with `results/E2/tools/lrat-check-E2.patch`) before sub-case (i)
counts as closed, and the cover must be re-checked with `lake exe cover_check` from results/H3.

# Wave 1 for mirror sub-case (ii): `ii_wave1.json`

Deterministic assignment of the 278 open hull cases of `results/Mii-S` (cases.jsonl at commit afb4a45)
to 36 cloud machines W00..W35 (sha256 of the file:
`6df36dab6dc93cec474ee7a795b38716bc19bf2d6064468b9c5e38e00901c72e`).

- The six most expensive 4-gon-hull cases are split by top cube: case CNF from
  `results/Mii-S/scripts/hullsplit.py case`, top cubes from `march_cu CASE -d 7`, shard s of k takes the
  cubes with 0-based line index i, i mod k == s. U_L2 gets 12 machines, U_L11 4, U_L4 3, U10_L, U6_L and
  U12_L 2 each. Every shard of a case must record the same top-cube file sha256.
- The other 22 open 4-gon cases are packed onto 7 machines and the 250 open 6-gon cases onto 4,
  longest estimate first (cases without an estimate counted as 600 s).
- Leaves are closed only by cake_lpr `s VERIFIED UNSAT`; results go to `results/WAVE1/<vm>/<case>/`
  (`leaves.jsonl`, `leaves.icnf`, and `open.icnf` for anything left).
