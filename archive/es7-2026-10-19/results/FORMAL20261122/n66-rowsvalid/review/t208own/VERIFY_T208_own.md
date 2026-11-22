# T208 sub-list print: independent reproduction (main session, 22 Nov 2026 21:00 KST)

Closes the reviewer's "not confirmed" item "binding: RowCertsUnsat, T208 trimmed sub-list (849f8a5e23a1fc77)",
which was blocked only by the reviewer's 3.5 GB unit cap.

- Script: `t208_own.sh` (own code; not tools/m9.sh). Unit `esr-ag-t208own`, MemoryMax 6G, 1 thread.
- Frozen exe `rowprint` sha256 `7140a6ffffb0e34b3074673c858e5584b7f2f31e482cd6e57490fa1e86e46344`, the same before and
  after, equal to the hash in `logs/m9_summary.txt`.
- `rowprint st 208 data/trim208.idx` printed `349b6c6c7b95d396e578ace1196cadff1cea0071387fad68b10ea20155057a12`. This equals
  VB's recorded `.trimmed.sha256` and the sha256 of VB's decompressed `.trimmed.cnf.zst`. VB's `.trimmed.cake.out` has
  exactly 1 line `s VERIFIED UNSAT`.
- Control: the full text `rowprint t 208` printed `243fa74ce2220fa3ee5e9c739541dac4005cb0967f8897083140be2bdfd606d3`,
  equal to the sha256 of VB's decompressed full `.cnf.zst`.
- Resources: 12.9 s wall; max RSS 3,303,704 kB (3.30 GB).

Verdict: **confirmed** (the trimmed print matches the certified trimmed CNF). Not re-run: cake_lpr on the trimmed pair.
The reviewer already accepted it with their own run.
