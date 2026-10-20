# Changes to verify/v3 after review V3-T (results/V3T/REVIEW.md)

## Fix 1 (BUG-1): unique work directory per job and process
`solve_check` used the fixed path `WORK/leaf-<idx>` or `WORK/cover-<case>`. Two v3_check.py
processes that share `--work` (default `/opt/work/v3`) and run manifests with overlapping idx
(for example two sub-manifests, both numbered 0..n-1) wrote, solved, checked and deleted the
same files, so a verdict for one leaf's CNF could be recorded for another leaf. Now each call
creates its own directory with `tempfile.mkdtemp(prefix="leaf-<idx>." or "cover-<case>.",
dir=WORK)`. Nothing else changes.

## Fix 2 (BUG-2): resume and output records identify the leaf or leaf set, not just the index
A rerun skipped any (kind, key) already in OUT, where key is the manifest idx for a leaf and the
case name for a cover. If OUT was reused with a different manifest (rebuilt at a newer commit,
or a renumbered sub-manifest), the old verdict for idx k (a different leaf) or for a cover of an
older leaf set was kept, and the new leaf or cover was never checked. Leaf records also carried
no literals, so records from different machines could only be joined by idx.
Now leaf records carry `"lits"` and cover records carry `"leaves_sha256"` (sha256 of the JSON
list of the case's leaves in manifest order); a record is skipped on resume only if kind, key,
case and lits (leaf) or leaves_sha256 (cover) all match. Old records without these fields are
re-checked. Nothing else changes.
