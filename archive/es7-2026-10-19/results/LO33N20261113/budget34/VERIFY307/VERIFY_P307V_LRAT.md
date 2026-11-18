# VERIFY_P307V_LRAT: verdict on claim p307v-lrat-v148 (verifier VS, 18 November 2026, 03:22-04:20 KST)

**Verdict: CONFIRMED at the claimed label (CERTIFIED for the stated CNFs).**
- Every one of the 1,574 rhs-1 rows of `inputs/b35s20-v148/extra.json` (extra indices 2..1575) has a retained CNF+LRAT
  pair whose content hashes equal the recorded ones.
- **A fresh cake_lpr run by VS printed exactly one line `s VERIFIED UNSAT` for each: 1,574/1,574.**

VS's matcher and runner are its own code, not `lrat_recheck_b35.py`. As the claim says, whether each CNF encodes its
row's geometric statement rests on the written encoder argument and the batch audits; that is not covered here.

## Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/p307v-lrat/`)

1. **Matching** (`V/vs_lrat_jobs.py`, c400f65f…; `V/match_summary.json`). VS collected for each row every retained pair
   whose record names that support:
   - pool rows from `audit/pool_verified.tsv`, at `<retained_directory>/<cnf_sha[:16]>.{cnf,lrat}.zst`;
   - batch rows from every `W/cuts-*/accepted.json` ('files' map), with the test namespaces v5xx-v7xx excluded.

   Result: **1,574 rows, 0 unmatched**. By source: 812 pool, 128 cuts-near9, 80 cuts-v2..v13, and 554 from the 59
   folders cuts-v101 .. cuts-v148w1u. 72 batch folders were used in all.
2. **Fresh cake_lpr** (unit `esr-agv-vs-lrat148`, 03:22:37-04:16:13, CPUQuota 15 %, MemoryMax 400M; `V/run_cake.sh`
   ba718c27…; results `V/results.tsv` f13a318a…).
   - Per job:
     - decompress into a work copy;
     - SHA-256 of CNF and LRAT content against the record;
     - `cake_lpr --CML_HEAP_SIZE=280 --CML_STACK_SIZE=32`;
     - `grep -cx 's VERIFIED UNSAT'`.
   - **1,574/1,574: both hashes equal, exit 0, exactly one verdict line.** Every `out/<job>.out` has exactly one such
     line.
   - Peak RSS 290 MB; 2,827 s of cake time in all.
3. **Comparison with the claim's `data/lrat-b35s20-v148/lrat-results.tsv`.**
   - Its 1,576 jobs (all ACCEPTED) are exactly VS's 1,574 distinct (row, CNF hash, LRAT hash) triples.
   - The two "rows with two retained pairs" (extra indices 1054 and 1375) are byte-identical copies of one pair, kept in
     both `cuts-v14` and `cuts-v105` / `cuts-v134u`, not two different proofs. VS deduplicated them by hash.

## Not checked

- The encoder argument per row. It is covered by the batch audits (e.g. VERIFY_AUDIT_1118.md for v149) and by
  VERIFY309N link (c).
- The claimant's `rows_stated.py` append-only check over v100..v150.
