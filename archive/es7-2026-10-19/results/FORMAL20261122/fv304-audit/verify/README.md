# fv304-audit / verify: independent review, slot rv4 (22 Nov 2026)

Status: DONE (18:50 KST). All five claims CONFIRMED at their stated labels. The full report is
`VERIFY_fv304-audit.md` in this directory. Nothing is running.

- Writes only here. Read only elsewhere; no git writes; no lake; nothing written into any olean store.
- Units, both finished; each ran with 1 thread, MemoryMax 4000M, MemorySwapMax 0, nice 10:
  - `esr-ag-rv4-fv304s`: the ONE compile, `src/RV.lean`, no olean written. 18:22–18:39, lean_rc 0, anon peak 516 MB.
  - `esr-ag-rv4-fv304h`: own closure re-hash, `tools/closure.py`. 18:41–18:43, `problems: []`.
- Repeat recipe: VERIFY_fv304-audit.md §9.
