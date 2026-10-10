# Partial conditional case-7 search

This is an incomplete integer search, not a Lean theorem. Its assumptions
are missing states 54 and 67, occupied states 27, 43 and 88, all 2,469 frozen
rows, and at most 32 holes.

The initial subtree had 24,561 nodes and six pending leaves. The continuation
ran for 216.814 seconds and generated 15,287 new exact weighted leaves.
Independent integer replay checked a total of 55,137 nodes and 27,569 leaves,
with minimum accepted contradiction margin one. **Seven leaves remain pending.**
No case-7 witness or complete exclusion was established.

The process stopped gracefully after case 4 supplied a 32-hole witness for
the full old catalog. That witness makes a universal 33-hole conclusion from
the old rows impossible, irrespective of whether case 7 can be closed.

`preparation.json` binds the source, parent tree and extracted seed.
`search-summary.json`, `replay.json`, and `manifest.json` identify the results,
exact script and local checkpoint. The 8 MB partial tree is retained only in
ignored cache; it is not a portable proof artifact. `search.py` records the
search and exact conditional replay code and requires HiGHS and NumPy for
discovery. No solver from this chunk remains running.

The original catalog derives from Michael Schroeder's pinned September 2026
archive. See [THIRD_PARTY.md](../../docs/THIRD_PARTY.md) and the
[frozen source](../omission-residual32-research-2026-10-10/README.md) for
attribution, licensing and source identities.
