# Frozen source provenance

`parent/` holds byte-identical snapshots of the reviewed parent sources,
with their relative include paths preserved. Origins and hashes are in
[source-provenance.json](../results/source-provenance.json). The two parent
Markdown files are documentation snapshots at freeze; the independent
arguments and final audit status are in the audit's own reports.

`check_rooted_fast_pre_tiny.py` is the exact checker used for the build and
two m16 controls. Only its `tiny` function changed in the final checker, to
add a valid n8 control with old heptagons. Each receipt identifies the
checker actually executed.

`replay_rooted_executed.py` preserves the exact wrapper used for all ten
successful replays. Its original allocation attribution is historical and
incorrect. The correct attribution is: **Parent reserved 800 MiB within
the owner's existing 6000 MiB track; owner-level caps were unchanged.**
The final wrapper and receipts contain that correction. Receipt execution
fields and raw outputs were not changed, and no proof was rerun. Both
wrapper hashes and the original receipt hashes are recorded in each
amended receipt.
