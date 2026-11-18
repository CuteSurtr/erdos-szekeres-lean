# VERIFY_P307V_N66COMPLETE: claim `p307v-n66-cover-complete` (verifier VB, 18 Nov 2026, 04:36-04:40 KST)

**Verdict: CONFIRMED** at the claimed labels. The cover enumeration over the accepted certificates is EXACT; acceptance
is computed from the files. With own code (`vb_cover_accept.py`; n66_cover_check.py and vs_n66cover.py were not read):
- **All 132** certificate directories `W/p2/c14/<id>/it*/` that have a cert.json pass the stated acceptance rules;
  **0 are rejected**.
- Their cubes, taken from cert.json and equal to the ids, cover **all 16,384 assignments** of the 14 split states
  12, 16, 17, 23, 25, 29, 37, 39, 40, 44, 45, 46, 49, 52.
  - **0 assignments are uncovered.**
  - **0 are covered twice**, so the 132 leaves partition the split space.
- The four four-check lists (U1 76, VB 15 Nov 23, VB 16 Nov 6, VB 18 Nov 27) are disjoint, and their union is exactly
  the 132 accepted ids.

A second own computation from the certified formulas gives the same complete cover (VERIFY_N66CUBES_1118.md §8,
`vb_cover_trim.py`):
- It takes the selector units of each accepted `trim.cnf`.
- F_c's only selector units are +sel_0 and +sel_1, and the space is taken with sel_0 = sel_1 = true.
- The union of the 132 unit-cubes has measure exactly 1. The 8 cubes refuted by unit propagation even lack some id
  literal in their trimmed formulas.

As a cross-reference, the claimant's checker (`n66_cover_check.py`, SHA-256 `5087351e…` as claimed) was re-run read-only.
It printed `COVER COMPLETE: accepted 132 cert dirs, rejected 0; split states 14; uncovered 0/16384`, with exit 0. Its
output JSON has SHA-256 `15a38fb1…`, equal to the claim's `cover_complete_deep_0436.json`.

The consequence the claim states, **N66 ≤ 55** (CERTIFIED components plus written soundness, as for N66 ≤ 56), is also
the main session's claim `n66-le55-cubes-1118`, which VS CONFIRMED at 04:33. This verification agrees with it. The
written soundness of the relaxation and of the split (cubes README §2, parent README §6) was not re-proved here.

## Acceptance rules checked per directory (own code)

- cert.json `ALL_OK` and verify.json `ALL_OK` are true.
- `cake.out` is exactly the one line `s VERIFIED UNSAT`, and cert.json `cake_lpr` is that line.
- budget 14, holes_at_least 15, bound 55, W_size 70; layout L = 14, W = range(70), sel = [988541, 988610].
- The SB pair list in layout, cert and verify equals the 27-pair list of `p2/b14h2/it1/layout.json`.
- The cube is the same in cert, layout, verify and the parsed id (o = occupied = +sel, h = hole).
- verify `unclassified` is 0.
- The trim.cnf SHA-256 equals cert.json and verify.json `trim_cnf_sha256`.
- Every unit clause of trim.cnf is +sel_0, +sel_1 or a literal of the declared cube.
- Exactly one accepted directory per id.

## Files (`W = /home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/p307v-n66-cover-complete/`)

`vb_cover_accept.py` (`e5a5ff45…`), `cover_accept.json` (`9871af3a…`), `cover_accept.out`, `p307v_checker_rerun.json`
(`15a38fb1…`); SHA-256 in `W/SHA256SUMS`. Unit `esr-agv-vb-accept` (95 %, 1500M), under a minute. Re-run:
`python -I W/vb_cover_accept.py out.json`.
