# Residual 32-hole search resume — 2026-10-10

This bundle records **unfinished computational research**, not a new planar bound or a Lean proof of the 32-hole obstruction.

The exact 2,469-row input and the 701,979-node frozen tree were verified against their recorded hashes. The five previously discovered positive-integer-margin cuts were inserted into a new cache copy, leaving 19 pending contexts. A single-thread HiGHS 1.15.1 search then ran for 600 seconds. It processed 79,151 LP nodes and added 40,314 certified arithmetic leaves; every retained leaf in the resulting tree was independently replayed using unbounded integers. No 32-hole witness was found.

The resume fully closed **16 of those 19 original contexts**. The original cases numbered 7, 4, and 2 remain unresolved. Case 7 was partially explored and now contains six pending leaves; cases 4 and 2 are unchanged. Thus the resumed tree has eight pending leaves in total. These cases can represent large unexplored subtrees, so context counts are not a completion percentage. All cases in which state 43 is missing have been closed computationally; the state-43-occupied branch is still incomplete.

The full resumed tree has 782,585 nodes and 391,293 leaves, with minimum retained exact margin one. Its 109 MiB checkpoint stays in ignored cache at the path and SHA-256 recorded in `manifest.json`. The original checkpoint and all frozen inputs were left unchanged.

The sixteen `closed-context-*.json.gz` files contain complete conditional subtrees, totaling approximately 6.23 MB compressed. Each assumes its explicit list of missing and occupied states, the 32-hole budget, and every row in the frozen source. They can be independently replayed without the large cached tree:

```sh
python3 experiments/omission-residual32-resume-2026-10-10/check.py
python3 experiments/omission-residual32-resume-2026-10-10/test_check.py
```

The checker validates source and context hashes, all branch variables and tree edges, every nonnegative integer multiplier, and every strict weighted-capacity contradiction. Its six corruption controls include invalid row indices, erased weights, changed contexts, shared children, and unfinished leaves. This integer replay is **not Lean verification** of these sixteen subtrees. A separate [Lean bundle](../omission-residual32-resume-lean-2026-10-10/README.md) now checks the six smallest: 492357, 29, 485519, 492355, 485517 and 24. The [full geometric transfer](../omission-residual32-transfer-2026-10-10/README.md) is also complete. These additions do not close the remaining arithmetic cases.

`preparation.json`, `search-summary.json`, `full-tree-replay.json`, and `conditional-replay.json` record the separate verification stages. `pending-contexts.json` lists all eight remaining leaves. The three archived research scripts preserve the exact preparation, bounded search, and extraction used here; `check.py` is the portable certificate replay.

A future continuation must use a **new output path** and verify the source and resumed-tree hashes in `manifest.json` first. For example, in the current workspace:

```sh
.cache/solver-venv/bin/python -u \
  experiments/omission-residual32-resume-2026-10-10/search.py \
  .cache/residual32-resume-2026-10-10-b/source.json \
  .cache/residual32-resume-2026-10-10-b/resumed-tree.json.gz \
  .cache/residual32-resume-2026-10-10-b/future-resume.json.gz \
  --seconds 600 --budget 32 --strategy pseudocost \
  --max-scale 10000 --strong-candidates 4
```

The search process ended normally after saving and replay. No solver remains running from this chunk.

The state catalog and original rows derive from Michael Schroeder's September 2026 companion archive, DOI [10.5281/zenodo.22842891](https://doi.org/10.5281/zenodo.22842891). Attribution and licensing are recorded in [THIRD_PARTY.md](../../docs/THIRD_PARTY.md). Original source identities and subsequent row provenance are preserved in [the frozen research checkpoint](../omission-residual32-research-2026-10-10/README.md).
