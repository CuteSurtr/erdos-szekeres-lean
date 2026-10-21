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

## FINDING 1 (breaks soundness of compose.py): childless plain nodes covered vacuously
C3U/tools/compose.py at 79a3f3c1: line 198 puts the layer name L itself into `prefixes` for every
certified cube record L__C (C3T only put proper prefixes there); line 238 covers a plain node in
`prefixes` by `for c in children(layers)` with no check that there are children.  A fully layered node
L' (every residue in a layer; tree_children = []) that has one certified cube L'__C (which rule 3
generates legitimately: a layer split of a cube node whose newest layer uses the last residues) is then
covered as a plain node without any proof of L' itself (only of the part with sigma = C).
The 79a3f3c1 guard ("never vacuously covered") covers only cube nodes, not this plain path.
Evidence (real proofs, both checkers, sha re-derived): m = 5, k = 6, logs/childless_real_m5k6.jsonl
(tools/forge_childless.py + tools/real_childless.py): every depth-2 node certified except P = 0s0_1s0-2s0,
every child of P certified except A = P_3, and of A's only child FULL = P_3_4 only FULL__3s0-4s0 (one
quarter of FULL) certified.  C3U compose: class_covered true.  Correct: not covered (FULL itself is
never solved; with logs + a real FULL record both say covered).
My composer had the same hole (same prefix idea); fixed in tools/mycompose.py (a node with no children
is never covered unless certified): now not covered.
Fix suggested for C3U: in covered2's plain branch, `if not ch: missing; return False` (as C3T's
`covered`), or keep prefixes to proper prefixes.

- Re-solved 3 C3SIG/G0 cubes (cheapest) with my own CNF (tools/resolve.py; CaDiCaL --sat -t 600 --lrat --binary=false,
  lrat-check E2 + cake_lpr): cnf_sha256 equal to G0's records 3/3, UNSAT, both checkers accept, proof_bytes equal
  to G0's records to the byte (208478098, 212743975, 235203589).  logs/resolve_sig_G0.jsonl.
- Wave records at 712efc6b use at most 7 of the 11 residues (no fully layered node), so finding 1 is latent
  for current records; it becomes reachable once rule-3 layer splits below cubes run 4+ layers deeper.
- close_tree.py (C3U, and C3T before it): a timed-out node with no children (fully layered) gets a split record
  with "children": 0 and leaves the frontier, so the run prints open_frontier 0 without a proof of that node.
  compose.py catches it for cube nodes (79a3f3c1 guard) and, for plain nodes, only if finding 1 is fixed.
  Cosmetic for soundness (compose is the judge) but misleading.
- close_tree.py reading OUT on restart: a sigma_cubes.py-format record ("node" = parent, "cube") that is
  certified would mark the PARENT done.  Only if such a file is used as close_tree OUT; compose is unaffected.
- t2 (m=7, k=6, K=3, --conf 3000,300,200,200,200,2000): 401 solves, 3 sigma splits, 16 cube layer splits, 312 dropped;
  t3 (m=6, k=6, K=2, --conf 1000,150,150,150,3000): 316 solves, 15 sigma splits (nested, |C| = 4), 23 cube layer splits,
  414 dropped.  Both composers: covered, same certified counts (381 / 277).  forge.py: 18/18 on t1, t2, t3.
- Re-solved 3 cubes of C3U's m = 11 records (C3U/tests/logs/m11/tree_*.jsonl at 0181991c; the 3 cheapest):
  cnf_sha256 3/3 equal, UNSAT 3/3, proof_sha256 and proof_bytes 3/3 equal to C3U's records (CaDiCaL is
  deterministic), lrat-check 3/3 c VERIFIED, cake_lpr s VERIFIED UNSAT 3/3 (first run: 2 empty cake_lpr outputs
  under memory pressure from a parallel m = 8 run; re-run alone: accepted).  logs/resolve_c3u_m11.jsonl
  (lines 1-3 first run, 4-5 re-run).
- Both composers on C3U's m = 11 records: 16 certified cubes, 2 sigma splits used, frontier 161 (agree).
