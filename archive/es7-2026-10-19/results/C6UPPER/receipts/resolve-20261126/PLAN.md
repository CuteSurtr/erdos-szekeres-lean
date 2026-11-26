# d1: re-solve of the 96 deleted sixfold cube proofs (PRE-REGISTRATION, 26 Nov 2026 00:22 KST: file birth time 00:22:19; first header said "00:3x", corrected 12:42 from stat)

Why: RESULTS row D1 (sixfold ES(8) = 65 case; Lean-checked modulo the 64 encoder-B verdicts CubesUnsat64) rests on
verdicts whose proofs were deleted on 24 Nov after a fresh cake_lpr re-check (receipts C6UPPER/receipts/
c6upper_proofs_20261124.tsv): they are recorded verdicts now. Owner 26 Nov: "fully utilize this pc to calculate what
we need". What: every receipt row (64 encoder B: 32 c6upper-replay/B + 32 c6upper-noty12; 32 encoder A), the kept CNF
re-hashed against the receipt (checked 26 Nov: 96/96 equal), then certify_cnf.sh (CaDiCaL 2.1.3 --lrat, cake_lpr
c14ff498 at heap 8000 as in the 24 Nov re-check, verdict only on the exact line), proof kept. Runs after the N66
re-solve (run_queue.sh d1 3 10: 3 at once, 10 GB units, guard track n66). Labels: none change before 96/96, then
the advisor. HEURISTIC: old proofs 43.3 GB zstd in total.

- 2026-11-26 12:10:19 (deviation, after an advisor consult): JOBS 3 -> 4. Measured over 2,622 samples (10:54:18-12:09:12,
  `measure_mem.sh`, `mem_samples.tsv`, memory.stat anon per unit): CaDiCaL phase 416-545 MB, cake_lpr phase 8,037-8,046 MB
  (heap 8000, unchanged), max total over the d1 units 16,583 MB. Rule: JOBS = floor(0.85 x track / 8,046 MB); the
  memguard n66 track was widened 26,000 -> 38,000 MB inside the unchanged esr total of 40,000 MB (guard
  esr-memguard-1126c; the other tracks are idle: b70 stopped by memguard at 07:46, part 3 done), so JOBS = 4. Only the
  driver was restarted (esr-vfy-d1drv: run_queue.sh d1 4 10); running jobs were not touched; the queue skips verified
  and active jobs. At the restart 33 of 96 were verified.
