# resolve-20261126: the 96 sixfold cube proofs re-solved with the proofs kept (26 Nov 2026)

The 96 cube proofs of row D1 were deleted on 24 Nov after `../c6upper_proofs_20261124.tsv`:
- encoder B: 32 from `replay-2026-11-06/B` and 32 from `noty12-2026-11-06`;
- encoder A: 32 from `replay-2026-11-06/A`.

From 24 to 26 Nov they were recorded verdicts. They were re-solved by `run_queue.sh` (work directory
`~/research/data/resolve-queue-20261126/d1`; pre-registration `PLAN.md`, 26 Nov 00:22 KST): each kept CNF, re-hashed
against its receipt, went through `certify_cnf.sh` (CaDiCaL 2.1.3 `--lrat`, cake_lpr `c14ff498` at heap 8000 as on
24 Nov), counting a verdict only on the exact line. The proof is kept.

**Result** (`joins.txt`, from `joins.py`):
- **Verdicts:** all 96 cake_lpr outputs have the exact line `s VERIFIED UNSAT`, from 06:54:07 to 12:32:38 on 26 Nov
  (CaDiCaL 17.1 h, cake_lpr 1.2 h); one line per cube in `certify_all.jsonl`.
- **Formulas:** every formula's SHA-256 and path equal the receipt's.
- **Proofs:** the new proofs are **byte-identical to the deleted ones**, 96/96 LRAT SHA-256 equal to the receipt's
  recorded proof hash (CaDiCaL is deterministic here). So the hashes of formula and proof that row D1 cites are those
  of files on disk again.
- **Encoder B:** the 64 formulas equal, by cube name, the texts that the Lean printer of `CubesUnsat64` writes (ENCBLEAN
  M9 binding, `logs/m9_review_fix_hash_binding.log`, 64/64).
- **Encoder A:** the 32 formulas equal the encoder-A rows of `replay-2026-11-06/results.tsv` (encoder A has no Lean
  printer).
- **Shared proofs:** 15 proof files are each shared by 2 or 4 cubes, which have the same LRAT bytes. Each such cube was
  checked by cake_lpr against its own CNF, and the receipts record the same sharing.

**Proofs kept:** in the work directory's `out/` (41 GB zstd, 162.8 GB raw), not in git. `verify_zst.sh` decompressed
each `.lrat.zst` and compared its SHA-256 with the hash recorded before compression: 96/96 OK (`zst_roundtrip.tsv`).

**Deviation:** JOBS 3 → 4 at 12:10:19, after an advisor consult (`PLAN.md`; peak memory measured by `measure_mem.sh`
→ `mem_samples.tsv`).

**Not done:** no second LRAT check (Lean core's checker loads a whole proof); no review; nothing about encoder A's
written soundness proof (gaps G1–G4 in P1) changes.
