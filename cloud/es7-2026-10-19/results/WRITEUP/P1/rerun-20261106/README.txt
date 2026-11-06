Re-run of the lower-bound checkers for preprint P1 (WRITEUP/P1/p1.tex, Section 7, "Re-run for this draft").

When and where: 6 November 2026, 04:58-04:59 KST (start 2026-11-05T19:58:05Z, end 19:58:57Z, see timing.txt), on
the project's Linux workstation (32 hardware threads, about 64 GB of memory), on copies, under the session's
resource caps.  Archived on 6 November 2026 from the session scratch directory where it ran.

What ran (run_lower.sh):
  1. sh check64/run_all.sh on copies of PRIMEFOLD/check64 and PRIMEFOLD/sets/k8 (kept here as check64/ and
     sets/k8/; every script and .pts file is byte-identical to the repository version).  It rewrote check64.log
     in place; that log equals PRIMEFOLD/check64/check64.log except two timing lines ("computed in 0.1s" vs 0.0s).
  2. gcc -O2 of SIX60/verify/dfs_convex.c (six60/dfs_convex), then for each of the five sixfold sets
     SIX60/sets/c6_60pts_{A,B,C,C2,D}.pts: SIX60/verify/verify60.py (six60/verify60_X.log), a conversion of the
     file to oblique integer pairs (six60/X_ab.txt), and dfs_convex on it (six60/dfs_X.log).
  timing.txt: 35.162 s for step 1; 3.142, 3.129, 2.562, 2.575, 3.510 s for dfs_convex on A, B, C, C2, D.

The binaries check64/cvxenum and six60/dfs_convex of that run are not kept (rebuild from the .c files).
run_lower.sh is kept as run: its SCR=/tmp/claude-1000/... path was a temporary session directory that is not kept,
and R= is the repository's results directory on that host.

To rerun from a checkout (from cloud/es7-2026-10-19/results):
  cp -r PRIMEFOLD/check64 PRIMEFOLD/sets <dir>/          # run_all.sh reads ../sets/k8 and rewrites check64.log
  sh <dir>/check64/run_all.sh
  gcc -O2 -o <dir>/dfs_convex SIX60/verify/dfs_convex.c
  python3 -I SIX60/verify/verify60.py SIX60/sets/c6_60pts_A.pts        # likewise B, C, C2, D
  # dfs_convex input: the oblique integer pairs; run_lower.sh shows the one-line conversion from the .pts rows
  # (w0-w2-w3+w5, w1+w2-w4-w5).
