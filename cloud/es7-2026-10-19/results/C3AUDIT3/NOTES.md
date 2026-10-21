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
