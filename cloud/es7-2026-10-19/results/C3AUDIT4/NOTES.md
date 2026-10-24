# C3AUDIT4 working notes

Task `TASK.md` at 3fd8a4d8, H = 2.5 h, started 2026-10-24 11:31 UTC (deadline 14:01; report by 13:51; fallback report
at 13:31 if C3U2 has no README). Bases rebuilt with `C3U/tools/gen_case.py m k none` (m = 11: `p cnf 168399 4154921`,
sha256 bf0e502e…dd6da, equal to the task's value).

## Tools (all mine, in `tools/`)
- `runcomp.py`: runs one composer in-process at any (m, k) (C3U-style compose.py with M, K, BASE_SHA rebound like
  C3AUDIT3's `c3u_small.py`, or C3AUDIT3's fixed `mycompose.py`) and reads its full `missing` list and `memo` from
  its locals when it prints: verdict, full frontier set, open depth-1 and depth-2 nodes.
- `myh6.py`: own Lemma H6M reduction (from PLAN.md 3a text) patched into mycompose for `--mirror-h6`.
  Kept-option sets equal `hullcase.tree_children(..., mirror_h6=True)` for every H6(a, s) at m = 7, 9, 11
  (150, 392, 810 roots).
- `adv.py`: 98 targeted adversarial record sets (step 1 list), each with the required outcome; true cnf_sha256
  values (so forgeries are structural unless the case forges the sha); own brute-force cover check with an own tree.
- `fuzz.py`: random close_tree-like runs (rules 2-4, random timeouts, K in 0..3, S in 1..2, sigma_cubes format
  sometimes) plus 9 mutation kinds; own brute force; soundness = "covered implies 0 brute holes".

## Pre-fix results (C3U 95cafa93 vs C3AUDIT3 mycompose)
- adv.py: mycompose 98/98; C3U 90/98. C3U fails c01 (childless plain FULL with one cube; union happens to cover, but
  no route is complete) and c04 (FULL with all but one of its cubes certified) at (5,6), (6,6), (7,6), (7,5):
  **c04 is unsound for C3U** (says covered, brute force finds the hole) = C3AUDIT3 finding 1, reached at m = 6, 7 too.
- Frontier conventions differ between C3U-family and mycompose (not soundness):
  * C3U lists a sigma-split node whose route failed in addition to its missing children; mycompose lists only leaves.
  * mycompose omits an uncertified childless cube node that carries an old `split, children 0` record (it is in
    lsplit), so its frontier under-reports such leaves (still not covered).
  * mycompose canonicalizes residue order inside a layer (`0s0_3s1-2s0` == `0s0_2s0-3s1`); C3U does not
    (an unsorted name is never a tree node there). Both are sound: the CNF of the unsorted name is the same clause
    set (ring order is sorted by key, sigma units only reordered).

## C3U2 (seen at cad4e050, before its README)
- Diff vs 95cafa93: compose.py covered2 plain branch: `if not ch: missing; return False` (finding 1); sigma loop and
  implied split guarded against empty child sets (cannot happen, defensive). close_tree.py: restart maps
  sigma_cubes records to node__C (finding 3); childless timed-out node -> "unsplittable", stays open (finding 2);
  an old split record with 0 children is treated as no split.
- adv.py at cad4e050: C3U2 98/98, 0 unsound.
