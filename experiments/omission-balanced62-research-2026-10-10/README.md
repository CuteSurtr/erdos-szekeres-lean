# Balanced 62-hole search checkpoint — 10 October 2026

This bounded search is **inconclusive**. It found neither an exact 62-hole witness nor a proof that one is impossible in the 3,131-row balanced Boolean model. It establishes no new real-point bound.

The attempt used approximately 121 seconds of a single-worker swap search, followed by about 490 seconds of a single-threaded SCIP feasibility search. SCIP still had an open search tree when stopped. The diagnostics, exact input hash, original scripts and logs are preserved alongside this note. They are research records, not Lean proof certificates. No search remains running.

The exact input is the tracked [balanced V2 source](../omission-cover-certificates-2026-10-10/balanced-v2-source.json). Its 2,685 original geometric rows and 446 derived cuts belong to the completed proof route excluding at most 61 holes. That exclusion does not decide the 62-hole question. A feasible Boolean assignment would not itself establish a real-point realization.

Source catalogs and the omission method derive from Michael Schroeder's [version-1 archive](https://doi.org/10.5281/zenodo.22842891); see [third-party attribution](../../docs/THIRD_PARTY.md).
