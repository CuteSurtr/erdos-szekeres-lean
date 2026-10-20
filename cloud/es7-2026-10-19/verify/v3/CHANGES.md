# Changes to verify/v3 after review V3-T (results/V3T/REVIEW.md)

## Fix 1 (BUG-1): unique work directory per job and process
`solve_check` used the fixed path `WORK/leaf-<idx>` or `WORK/cover-<case>`. Two v3_check.py
processes that share `--work` (default `/opt/work/v3`) and run manifests with overlapping idx
(for example two sub-manifests, both numbered 0..n-1) wrote, solved, checked and deleted the
same files, so a verdict for one leaf's CNF could be recorded for another leaf. Now each call
creates its own directory with `tempfile.mkdtemp(prefix="leaf-<idx>." or "cover-<case>.",
dir=WORK)`. Nothing else changes.
