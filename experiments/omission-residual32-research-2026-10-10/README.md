# Residual 32-hole search checkpoint — 2026-10-10

This is **unfinished computational research**, not a new planar Erdős–Szekeres bound or a Lean theorem. The 2,469-row Boolean relaxation has neither been proved infeasible with 32 holes nor supplied an exact 32-hole witness by these runs.

Two separate 40-minute searches processed the complementary cases in which state 43 is occupied or missing. Their disjoint subtrees were merged and every retained arithmetic leaf was independently replayed with unbounded integers. The merged tree has 701,979 nodes and 350,990 leaves, including **24 unclosed cases**: eight with state 43 occupied and sixteen with it missing. Neither entire root case is closed. These 24 cases can represent large unexplored subtrees; the number of closed leaves is not a completion percentage. The minimum margin of the retained weighted contradictions is one.

`checkpoint.json` records the input identities, search settings, result summaries, and the local resume path. The large partial tree remains in ignored cache; full replay requires that file with the recorded hash. `pending-contexts.json` lists every unclosed case. No solver is left running.

`source.json.gz` preserves the exact 2,469-row search input. It contains the 2,457-row research model followed by twelve independently replayed rounded arithmetic consequences. The individual new geometric inequalities have Lean proofs elsewhere in the library; **this full literal catalog and its arithmetic search have not been checked in Lean**. Historical pending-status metadata in the frozen source has deliberately been preserved rather than changing its identity.

The additional cut experiment found twelve valid integer consequences but did not improve the numerical root LP objective of approximately 27. `cover-cuts.json` and `cover-cuts-replay.json` preserve those derivations. A separate compaction pass tested all 17,848 eligible internal contexts in the earlier checkpoint containing the eleven-state inequality and collapsed no subtree; its result is in `compaction.json`.

`research-sources.json.gz` archives the exact scripts and the independent tree validator. The solver run used HiGHS 1.15.1 with one thread per partition. These scripts discover candidates; only exact integer replay certifies a retained arithmetic leaf, and unclosed leaves remain explicitly unproved.

For a future authorized continuation in the existing workspace, use the source and merged tree whose hashes match `checkpoint.json`, with a **new** output path:

```sh
.cache/solver-venv/bin/python -u .cache/stronger-budget32/search.py \
  .cache/recovery-residual32/source-2469.json \
  .cache/recovery-residual32/final-merged-tree.json.gz \
  .cache/recovery-residual32/resumed-tree.json.gz \
  --seconds 600 --budget 32 --strategy pseudocost \
  --max-scale 10000 --strong-candidates 4
```

The state catalog and original rows derive from Michael Schroeder's September 2026 companion archive, DOI [10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891). Attribution and upstream licensing are recorded in [THIRD_PARTY.md](../../docs/THIRD_PARTY.md). The later coupled geometric rows and arithmetic derivations are identified in the source provenance and the neighboring completed experiment bundles.
