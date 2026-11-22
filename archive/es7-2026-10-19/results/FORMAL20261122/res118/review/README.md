# res118-lean statement-fidelity review (slot lrev), 22 Nov 2026

This is the reviewer's work directory and the only place this review wrote to. The deliverable is
**`VERIFY_res118-lean_fidelity.md`**.

**Status: DONE (07:05 KST, `date`).** Statement fidelity is CONFIRMED for `Res118.residual_bound_118_of_slices` and
`Res118.forces_304_of_slices`.
- The correct label is "Lean-checked modulo" its hypotheses.
- No bound changes and no label changes.

What was done:

1. **Own read-only data checks**, all ok:
   - `data/rev_check_data.json`: row files, capacity rows, rhs, budgets, nesting, and that the Lean blocks equal the
     JSON.
   - `data/rev_check_rows_cert.json`: every block row has an accepted, hash-matched cake_lpr job.
2. **Positive control** (HEURISTIC), `data/rev_realsets.json`: 1,302 real residual configurations, with 0 row
   violations.
3. **One Lean compile**, unit `esr-ag-lrev-ax1`:
   - rc 0, 23 s, cgroup peak 437 MB.
   - Every axiom audit is standard.
   - The kernel-checked restatement (`Rev.rev_residual_118`, `Rev.rev_304`) compiled.
   - `data/rev_cmp_dumps.json`: the data dumped from the oleans equal the JSON (F/Lo, the catalog, the 2,650 base rows
     and the four blocks).
4. **Five documentation corrections** to the worker's README are listed in VERIFY §7. None of them affects the Lean
   result.
