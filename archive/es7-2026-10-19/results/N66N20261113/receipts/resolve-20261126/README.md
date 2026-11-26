# resolve-20261126: the 105 level-15 cube proofs re-solved with the proofs kept (25-26 Nov 2026)

The 105 level-15 cube proofs (p2/c15, p2/cal15) were deleted on 24 Nov after `../n66_cube_proofs_20261124.tsv`.
They were re-solved by `run_resolve.sh` (work directory `~/research/data/n66-resolve-20261125`; pre-registration
`PLAN.md`, 25 Nov 20:38 KST).

**Result:** 105/105 leaves with cake_lpr's exact line `s VERIFIED UNSAT`, the last at 06:13 on 26 Nov (`tally.json`:
CaDiCaL 36.5 h, cake_lpr 4.9 h).
- One line per leaf in `certify_all.jsonl`: CNF and new LRAT SHA-256, LRAT bytes, times, heap and verdict.
- The proofs are kept as `.lrat.zst` (121 GB) in the work directory's `out/`. They are not in git.
- The old proof hashes stay as recorded: a new solve need not reproduce the same proof file. 8 of the 105 new proofs
  are byte-identical to the deleted trim proofs (receipt `trim_lrat_sha256_recorded`); the other 97 differ.
- `verify_zst.sh` (26 Nov 12:44) decompressed every kept `.lrat.zst` and compared its SHA-256 with the hash recorded
  before compression: 105/105 OK (`zst_roundtrip.tsv`).

**Binding** (`m9_join.txt`):
- Each re-solved `trim.cnf` hashes to its receipt (`leaves.tsv`), and the leaf ids are the same 105.
- The multiset of the 105 CNF hashes (98 distinct texts) equals the multiset of the texts that the Lean printer of
  `N66R15Enc.CubesUnsat105R` writes (n66-l15-rows M9 binding, 105/105 MATCH).
- So every text that H-N66C of `Combined.es302_verdicts` depends on has a CERTIFIED proof on disk again.

**Incident** (`run.log`, 26 Nov 00:09): a driver restart relaunched c15_hoooho and c15_hooooo_40o while their first
runs were still going, so both copies wrote to one proof file. All four units were stopped, the partial proofs removed
and the two leaves re-solved; their certified runs are the lines in `certify_all.jsonl`. The aborted runs' CaDiCaL
logs are kept in `aborted-20261126/` in the work directory.

**Not done:**
- No second LRAT check: Lean core's checker (LEANLRAT20261125) loads a whole proof, and these are up to about 10 GB raw.
- No review.
