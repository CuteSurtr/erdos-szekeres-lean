# VERIFY_AUDIT_1118: verdicts on AU's (20,15) row-audit claims of 18 November 2026 (verifier VS)

## Claim agu-1118-v149 (taken 02:41, checked 02:43-02:45 KST)

**Verdict: CONFIRMED.** The 16 rows that the loop appended as `inputs/b35s20-v149` are each CERTIFIED:
- 8 rows from batch `v149w1u`, witness context 1765;
- 8 rows from batch `v149w2u`, witness context 1829.

Every row passed the following checks:
- a fresh cake_lpr run by VS printed exactly one line `s VERIFIED UNSAT`;
- the CNF is byte-identical to the house audit encoder's re-encoding;
- the row misses all 35 holes of its batch's witness.

The append is exact. The running total of **61 batches and 570 CERTIFIED rows** (v101-v149) is right. As the claim
says, these are additional rows only: no bound follows from them.

**Independence.** The byte identity was reproduced with the house audit encoder `audit/residual_encoder.py`
(`db7b2deb…`). That is the same encoder AU used, not an encoder written by VS. The geometric meaning of the CNFs rests on
the written soundness argument (VERIFY309N link (c)), which VS did not re-check. VS's own parts are:
- the fresh cake_lpr runs, in a separate unit on frozen copies;
- every set check: witness, catalog rows, v148 rows, row-witness disjointness, append.

### Checks (V = `/home/jay/research/data/roadmap-20261115/pm1115/vs1118/agu-v149/`; W = `/home/jay/research/data/es308-20261114`)

1. **Frozen copies.** For each of the 16 rows in `W/cuts-v149w{1,2}u/accepted.json`, VS copied `system.cnf`,
   `system.lrat`, `support.json`, `receipt.json` and `cake.log` to `V/v149w{1,2}/<k>/`.
   - The SHA-256 values of the copied CNF and LRAT equal the receipt's `files` entries and `generation.cnf_sha256`.
   - Each `receipt.json` equals its accepted.json entry, and each `support.json` equals the support.
   - Supports are sorted, have distinct entries and lie in 0..153.
   - The CNF and LRAT copies are now kept as zstd.
2. **Encoder identity.** `Geometry(states).chunks(support)` of the house audit encoder hashes to the CNF's SHA-256 for
   all 16 rows. The catalog `source-2650.json.gz` matches its raw SHA-256 `e800d5f8…`.
3. **Fresh cake_lpr** (unit `esr-agv-vs-agu149`, 02:43:49-02:44:37, CPUQuota 15 %, MemoryMax 400M).
   - Command: `cake_lpr --CML_HEAP_SIZE=280 --CML_STACK_SIZE=32 system.cnf system.lrat`, run on the copies.
   - **16/16 exit 0 with exactly one line `s VERIFIED UNSAT`** (`grep -cx`).
   - CNF and LRAT hashes were the same before and after each run.
   - Peak RSS 289,920 KiB; at most 2.9 s per row. The log is `V/cake.jsonl`.
4. **Witnesses (own code, `V/vs_rows.py`).** Holes were taken from the two `batch` events of
   `continuation-b35s20v11c/events.json`.

   | batch | context | holes | F / Lo | state 0 | = WITNESS file | satisfies 2,650 catalog rows | satisfies 1,576 v148 rows | rows missing all holes |
   |---|---|---|---|---|---|---|---|---|
   | v149w1 | 1765 | 35 distinct | 20 / 15 | occupied | yes (`WITNESS.json.r149w1`, e238d1d2…) | yes | yes | 8/8 |
   | v149w2 | 1829 | 35 distinct | 20 / 15 | occupied | yes (`WITNESS.json.r149w2`, 7853888d…) | yes | yes | 8/8 |

   - F = the 84 catalog states whose first coordinate is ≥ 5.
   - A row (support, rhs) is satisfied when |support ∩ H| ≥ rhs.
5. **Append.**
   - `inputs/b35s20-v149/extra.json` (1,592 rows, `10df12db…`) is `b35s20-v148/extra.json` (1,576 rows, `299ddc49…`)
     unchanged, followed by exactly the 16 rows: w1 then w2, in accepted.json order, as {support, rhs = 1}.
6. **Running total.**
   - The audit summaries `budget34/audit/cuts-v<101..149>*/summary.json` give 61 batches and 570 rows.
   - All of them have label CERTIFIED and rows = own-encoder matches = fresh acceptances.

### Files

- `V/vs_rows.py` (edbff41c…6e51), `V/run.sh` (f7839fbf…1cb2).
- `V/prep_summary.json` (7189da16…13ef31), `V/cake.jsonl` (47559819…ba5d), `V/prep.log`.
- `V/v149w*/<k>/vs_cake.out`.
