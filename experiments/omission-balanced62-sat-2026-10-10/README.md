# Balanced 62-hole SAT search

This ten-minute search is **inconclusive**. CaDiCaL 3.0.1 returned `UNKNOWN`:
no 62-hole Boolean witness or complete infeasibility certificate was found.
It proves no new planar bound and no limitation of the mathematical problem.

The input is the unchanged 3,131-row balanced V2 catalog, whose geometric
transfer is already proved. `encoding.json` binds its SHA-256 and the generated
CNF. A positive primary variable means a missing state. Each row requires at
least its stated number of holes; the global constraint allows at most 62.
The encoding has 69,584 variables and 258,379 clauses. `encode.py` uses full
equivalences for sequential counting gates and checks their truth table and
all primary assignments up to six variables. This encoder is **not formalized
in Lean**; those checks are validation of the search implementation.

`result.json` and `search.log` record the solver, exact input identities, and
600-second limit. The unfinished DRAT trace is only in ignored cache and is
not an UNSAT certificate. No solver remains running.

A separate symmetry probe checked, with integer set comparisons, that
transposition and complementation permute the 2,685 original balanced rows.
Transforming the existing rounded cuts supplied 381 additional distinct rows.
The numerical LP objective remained approximately 55 before and after adding
them. `symmetry-probe.json` records the permutations and source row of every
addition. This is a numerical diagnostic and exact finite comparison, not a
Lean theorem; it was not included in the SAT run above.

To reproduce the encoding from the repository root:

```sh
python3 experiments/omission-balanced62-sat-2026-10-10/encode.py
```

It writes the CNF under `.cache/balanced62-sat-2026-10-10/`. The solver command
used is recorded in `result.json`; CaDiCaL is an external search tool, not a
trusted proof oracle or bundled dependency.

The original catalog and omission method derive from Michael Schroeder's
[version-1 archive](https://doi.org/10.5281/zenodo.22842891); see
[THIRD_PARTY.md](../../docs/THIRD_PARTY.md). The 446 existing rounded cuts
come from this repository's completed balanced61 proof route.
