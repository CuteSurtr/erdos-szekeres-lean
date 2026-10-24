# Tree checks of the wave leaves (analysis scripts)

Run in a checkout of es7-cloud: `python3 tree_stats.py REF OUT.json` and `python3 tree_cover_check.py REF` (both import the loader `tree_lib.py` from their own directory).

For every wave case they rebuild the cube tree from all directories of `results/WAVE1` to `results/WAVE4` at REF: the top cubes of `top.icnf`, the SPLIT records (`cube`, `subs`) of `leaves.jsonl`, and the closed cubes (UNSAT records whose `cake_lpr` is exactly `s VERIFIED UNSAT`, and `leaves.icnf`). The root children are the top cubes that are not `parent + sub` of a SPLIT record.

- `tree_stats.py` classifies every node as an exact leaf, split, subsumed (covered by a closed cube that is a proper subset, or the same set in another order) or open, and counts conflicting SPLIT records.
- `tree_cover_check.py` checks that the root children of each case, and the `subs` of each split node, are each a combinatorial cover (a Python transcription of `Mir.coverCheck`).

At commit 9639cfb45 (2026-10-20 15:08 UTC): 140 wave cases with a tree (the other 138 were closed by the empty cube) had 71,283 exact leaves, 897 split nodes, no subsumed node and no conflicting SPLIT record. All 140 root sets and all 897 split lists are covers. These are the facts the tree-shaped kernel proof of `results/V2-L/TREE_TASK.md` relies on.
