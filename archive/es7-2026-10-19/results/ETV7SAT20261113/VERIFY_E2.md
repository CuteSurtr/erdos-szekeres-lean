# VERIFY_E2: re-check of the N = 37 certificate (13 November 2026, 21:38–22:46 KST)

VERIFY_E.md left M(5;7) ≤ 36 "not confirmed" only because the N = 37 LRAT had been deleted after its phase-1
check. The CNF was re-solved and the new proof checked with a heap large enough for it.

- CNF: `/home/jay/research/data/etv7sat-20261113/run/lad_ns37_N37.cnf`; SHA-256 begins `8762b9f0f23456cca9f8`,
  the hash recorded in §6.2 and regenerated independently in VERIFY_E.md.
- CaDiCaL 2.1.3 `--lrat=true --binary=false`: exit 20 (UNSAT) after 3,891 s.
- The new LRAT has SHA-256 `d3205363dd75a3c6e101e3f61967d497b734e76be4061292641af56e2cb3f373`, identical to the
  phase-1 proof hash quoted in VERIFY_E.md.
- cake_lpr `--CML_HEAP_SIZE=4200`: **`s VERIFIED UNSAT`** after 146 s.
- The proof is kept, zstd-compressed:
  - `/home/jay/research/data/verify-E2-20261113/n37.lrat.zst`;
  - script `recheck37.sh` and log `status.jsonl` in the same directory.

**Verdict.** Together with VERIFY_E.md, which confirms the soundness of the owner model, the CNF identity and the
controls, **M(5;7) ≤ 36 is confirmed: CERTIFIED and independently re-checked.** The other rungs (N = 38, 40, 41)
were not re-run and are logically not needed.
