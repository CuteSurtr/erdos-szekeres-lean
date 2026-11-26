# n66-resolve-20261125: restore re-checkable proofs for N66 <= 54 (PRE-REGISTRATION, 25 Nov 2026 ~20:45 KST)

**Why.** `N66Bound 54` (an input of ES(8) <= 302) rests on the cube leaves of the level-15 campaign. Each was accepted
by cake_lpr twice, and all their LRAT proofs were deleted on 24 Nov after the receipts were pushed
(`N66N20261113/receipts/n66_cube_proofs_20261124.tsv`), so today they are recorded verdicts: a referee who asks to
re-run them needs a re-solve. The certified trim formulas are all on disk. Re-solving them restores CERTIFIED with the
proofs kept, which the paper and any e-mail need.

**What.** For each of the 105 level-15 rows of the receipts (`level = L15`: 103 in `p2/c15/<id>/it1`, 2 in
`p2/cal15/<id>/it1`; checked 25 Nov 20:5x: all 105 `trim.cnf` present, 1.86 GB, every SHA-256 = the receipt):
1. `trim.cnf` must hash to the receipt's `trim_cnf_sha256_recorded` (mismatch: stop that leaf, report);
2. `.claude/skills/es-research/scripts/certify_cnf.sh trim.cnf OUT 4000 --keep` (CaDiCaL 2.1.3 `--lrat`, cake_lpr
   c14ff498, verdict only on the exact line `s VERIFIED UNSAT`; the new proof kept as `.lrat.zst`);
3. one JSON line per leaf (CNF hash, new LRAT hash, times, verdict) in `out/certify.jsonl`; the old proof hashes stay
   as recorded (a new solve need not reproduce the same proof file).

**Resources (HEURISTIC).** The campaign's recorded solve wall times sum to 104.2 h for the level-15 leaves (median
about 1 h, max about 2 h); the deleted proofs were 346.2 GB raw and 77.6 GB zstd in total (largest 9.8 GB raw), so about 78 GB of new
`.lrat.zst` stay on disk (1,115 GB free) and each job needs up to about 10 GB of transient raw proof. Each job:
unit `esr-vfy-n66-<id>`, 1 thread, MemoryMax 6G (CaDiCaL peaked at 2.6-3.3 GB in the campaign; cake_lpr runs after
it at heap 4000), RuntimeMaxSec 4 h. At most 6 jobs at once while Lean compiles run (memory guard esr total 36,000 MB), 10 when they have ended; yield
guard and Tctl gates as usual. About 11-17 h wall.

**Outcome.** (Labels: HEURISTIC above; the verdicts below are CERTIFIED only by cake_lpr's line.) Every leaf `s VERIFIED UNSAT` with its proof kept: N66 <= 54's cube leaves are CERTIFIED again (record
update in N66N20261113/cubes20261120 and REMAINS H-N66C after the advisor). Any leaf not accepted: stop, report, no
label change. Labels do not change before all 105 are done.

- 2026-11-26 04:12: unit esr-n66-hold-tctl (sleep, 8 h) holds one of the 7 slots, so the driver runs 6 cube jobs: Tctl read 86-88 °C at 78 % CPU and part 3 launches its next units only when Tctl < 86 °C.
- 2026-11-26 06:13: all 105 leaves CERTIFIED (tally.py: certified 105, not_accepted [], cadical 36.5 h, cake_lpr 4.9 h); the hold unit was stopped so the driver can end and chain_d1.sh can start D1.
