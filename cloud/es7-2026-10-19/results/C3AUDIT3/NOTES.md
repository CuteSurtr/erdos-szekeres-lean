# C3AUDIT3 notes (work in progress)

Start 2026-10-21 05:37 UTC, branch head 712efc6b, H = 3.0.
Tools built here: CaDiCaL 3.0.1 c6073042, cake_lpr a36874a8, lrat-check 2e3b2dc + E2 patch
(sanity: `3 0 0` on {1},{-1} rejected, `3 0 1 2 0` accepted).

- tools/mycompose.py: own composer (grown from C3AUDIT/tools/mycompose.py, written from C3U/TASK.md only).
- tools/mydriver.py: own small-instance closer with sigma splits (deterministic conflict limits).
- tools/xcheck_tree.py: mycompose tree/units/cube children vs hullcase (C3U): 465 comparisons, 0 mismatches.
- t1 (m=7, k=6, root 0s0, --conf 3000,300,300,300,2000, K=2): 137 solves, 6 sigma splits (nested, |C| up to 4),
  4 cube layer splits, 104 dropped conflicting options; mycompose and C3U compose (41041780) both: covered, 126 certified.
