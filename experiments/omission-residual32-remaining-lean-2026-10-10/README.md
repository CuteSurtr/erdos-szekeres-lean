# Stopped arithmetic compression experiment

This bundle contains exact Python replay and compression of ten already-closed
conditional arithmetic subtrees. **It contains no new Lean formalization.**
Work stopped before any large Lean export or compiler was started, after a
32-hole satisfying assignment was found for the complete 2,469-row system.
That witness prevents an unconditional 32-hole exclusion from these rows.

`prepare.py` tests each stored weighted dual at ancestor contexts, retaining a
replacement only while its exact integer margin is positive. It then tries
smaller integer multipliers and independently replays each resulting tree.
All initial missing/occupied contexts are retained. Original files are unchanged.

The 27,989 weighted leaves became 27,974: two leaves were removed in context
492346, one in context11, and twelve in context9. Other contexts retained the
same number of leaves. `compression.json` records individual hashes, margins,
and multiplier changes. These arithmetic checks are conditional and do not
improve a planar bound. The earlier six small Lean subtree proofs remain in
their separate frozen bundle.

`manifest.json` records this stopped status and pins every saved input, script,
report, and compressed output. Its identities were checked against the original
replay record; adding the manifest did not rerun or extend the research.
