# WAVE3 task files

Each `G<k>.json` maps a case name to the list of open cubes (lists of literals over F's variables) that the WAVE3 machine G<k> must close.

Provenance:
- `gfrontier.py origin/es7-cloud` at commit c4f9367 (2026-10-20 10:35 UTC) computed, for every hull case, the cubes created by the wave-1 and wave-2 drivers (all top cubes in each directory's `top.icnf`, plus parent+sub for every SPLIT record in `leaves.jsonl`), minus the cubes split anywhere and the cubes covered by a verified leaf (a leaf whose literal set is a subset of the cube's). A case's whole cube `[]` counts as created and is split by any `top.icnf`.
- `wave3_tasks.py` dropped the cases already assigned elsewhere (U3_L to WAVE2 F1-F3, U4_L to F4-F5, U_L8 to F6-F7, U7_L still running on WAVE1 W26, and the 152 untouched small cases to WAVE2 S1-S5) and split the rest; a case given to k machines is split by position p mod k of its sorted open list.

These lists are a work plan only. Acceptance does not depend on them: every leaf is re-solved from scratch by `verify/v3/v3_check.py` and each case's cover is re-checked.
