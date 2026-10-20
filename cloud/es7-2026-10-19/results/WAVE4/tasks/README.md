# WAVE4 task files

Each `H<k>.json` maps one case name to the list of open cubes (lists of literals over F's variables) that the WAVE4 machine H<k> must close.

Provenance:
- `scripts/gfrontier3.py` at commit 5192d6a7 (2026-10-20 12:42 UTC) computed, for every hull case, the cubes created by the wave-1, wave-2 and wave-3 drivers (all top cubes in each directory's `top.icnf`, plus parent+sub for every SPLIT record in `leaves.jsonl`), minus the cubes split anywhere and the cubes covered by a verified leaf (a leaf whose literal set is a subset of the cube's). 270 of the 278 wave cases had no open cube. Open cubes: U_L2 6466, U_L6 1074, U3_L 875, U_L7 526, U4_L 327, U_L5 30, U4_L8 1, U8_L2 1.
- `scripts/wave4_tasks.py` modelled the queue of every machine still running on U_L2 (WAVE3 G1-G3), U_L6 (G21), U3_L (WAVE2 F1, F3), U_L7 (G14) and U4_L (F4): the driver's frontier at its last resume record, then the children of its later SPLIT records in record order. It reserved for each running machine the first 0.8 x (its rate since the resume record) x (its minutes left) cubes of its queue, and gave every other open cube to the helpers: the cubes in no running queue first, then the unreserved queue tails from their far end, interleaved; position p of that list went to helper p mod k.
- Helpers: U_L2 H01-H18 (5842 cubes, 624 reserved for G1-G3), U_L6 H19-H23 (980; 94 reserved for G21), U3_L H24-H25 (635; 240 reserved for F1, F3), U_L7 H26-H27 (389; 137 reserved for G14), U4_L H28 (190; 137 reserved for F4). U_L5, U4_L8 and U8_L2 are left to the machines working on them (G22, S4, S1).

These lists are a work plan only. Acceptance does not depend on them: every leaf is re-solved from scratch by `verify/v3/v3_check.py` and each case's cover is re-checked. A cube closed twice (by a helper and by a running machine) is harmless.
