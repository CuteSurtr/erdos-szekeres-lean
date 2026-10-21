# C3AUDIT3 notes (work in progress)

Start 2026-10-21 05:37 UTC, branch head 712efc6b, H = 3.0.
Tools built here: CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch
(sanity: `3 0 0` on {1},{-1} rejected, `3 0 1 2 0` accepted).

- tools/mycompose.py: own composer (grown from C3AUDIT/tools/mycompose.py, written from C3U/TASK.md only).
- tools/mydriver.py: own small-instance closer with sigma splits (deterministic conflict limits).
- tools/xcheck_tree.py: mycompose tree/units/cube children vs hullcase (C3U): 465 comparisons, 0 mismatches.
- t1 (m=7, k=6, root 0s0, --conf 3000,300,300,300,2000, K=2): 137 solves, 6 sigma splits (nested, |C| up to 4),
  4 cube layer splits, 104 dropped conflicting options; mycompose and C3U compose (41041780) both: covered, 126 certified.
- forge.py on t1 against C3U compose at 41041780: 18/18 pass (logs/forge_t1_c3u41041780.txt).
- m = 11 (base sha bf0e502e…, `p cnf 168399 4154921`), records at 712efc6b (/opt/work/snap):
  - C3SIG/G0..G3 out.jsonl: both composers 160 certified cube records, 20 sigma splits used (all 20 pilot nodes covered), frontier 143.
  - 116 wave files (all out.jsonl of C3WAVE1, C3WAVE2, C3S0, C3W3 + 5 recheck files + C04 out_reconstructed;
    summary and removed_records left out): mycompose, C3U compose, C3T compose all: 48,614 certified records,
    48,439 nodes, sha-checked, not covered, frontier 11,492.  Waves + SIG: 48,774 / 48,599, 20 sigma splits used,
    frontier 11,492 (the 20 pilot nodes were already layer-closed by the waves).
