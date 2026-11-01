# W28: wave 1, mirror sub-case (ii), kind "cases"

Assigned (verify/ii_wave1.json, est_core_h 12.8): U11_L, U_L5, U_L6, U_L7.
Run 2026-10-20 06:56-10:35 UTC on one cloud VM, 4 cores, 15 GB (`env.txt`).

**Result: U11_L closed. U_L5, U_L6, U_L7 open** (partial leaves for U_L5 and U_L6). No SAT.

## Tools and hashes (`tools.txt`)
- CaDiCaL c6073042 (3.0.1); march_cu CnC 705b60c6 with -fcommon; cake_lpr a36874a8
  (bundled example: `s VERIFIED UNSAT`). Proofs checked only with cake_lpr.
- Base `m33k7int.sub.cnf` regenerated (gen_etv.py + mirgen.py as in make_cnfs.sh):
  sha256 69c1dc8f...f932d, matches. ii_wave1.json sha256 6df36dab...1c72e, matches.
- All four case CNFs from `hullsplit.py case` match their entry hashes (listed in tools.txt).

## Method (`scripts/close_w28.py`; `scripts/close_march.py` is the unchanged Mii-S copy)
Per case: plain `cadical --lrat -t 60` on the whole case (UNSAT accepted only with cake_lpr),
then the close_march recipe: `march_cu CASE -d 7 -o top.icnf`, each cube `cadical --lrat -t 300`
+ cake_lpr, a timeout split by `march_cu CASE+cube -d 6`. Differences from close_march.py:
one shared pool of 4 workers over all cases, by case priority; `leaves.icnf` holds only leaves
with cake_lpr `s VERIFIED UNSAT`; SPLIT records keep their children (`subs`) so the run resumes
from leaves.jsonl + top.icnf; `open.icnf` is written at the end; CPU time per call from wait4.
Cubes running at the deadline (10:30 UTC) were cut and left without a record; they are in open.icnf.

**Deviation from the listed order:** cases ran in the order U11_L, U_L5 until 09:13 UTC; then
U_L5 had 274 cubes left and growing, so I restarted the runner (resume) with priority
U11_L, U_L6, U_L7, U_L5 to try to close the two cheaper cases. U_L6 split further and did not close
either. Cubes in flight at the restart were lost (no records; they are still open).

## Per case
Plain 60 s CaDiCaL: UNKNOWN on all four. Top march -d 7: 128 cubes, 0 refuted, for each case.

| case | CNF sha256 | top.icnf sha256 | status | verified leaves | splits | open cubes | CPU h |
|---|---|---|---|---|---|---|---|
| U11_L | ccdd70bc...a11164 | 785e007f...42b9d8 | **CLOSED** | 309 | 3 | 0 | 2.36 |
| U_L5 | 84bf54f2...75ff6e | cdde9f11...17a66 | open | 609 | 12 | 274 | 6.00 |
| U_L6 | 741c7fe0...a105424 | a2e392c6...3872cc | open | 474 | 13 | 473 | 5.20 |
| U_L7 | c6d1c840...04f099 | c2d771b8...64c3 | open (not started) | 0 | 0 | 128 | 0.10 |

(Full top.icnf hashes: U_L6 a2e392c6d1071f505ffdcd0c5e95d3e3cb65de3f68452707e7540be5803872cc,
U_L7 c2d771b8b3f3b302634876481f22451d482d04f6138b39826b473872944e64c3,
U11_L 785e007fa80c372fdc33d059dc93c49809fb7124bbc1c5e5d44a04ed1642b9d8,
U_L5 cdde9f116d324e6ef8dc45ec12400aa7eeca59592c3cdcbf162310e427e17a66.)

CPU = cadical + cake_lpr + march, from leaves.jsonl. Every UNSAT answer got cake_lpr
`s VERIFIED UNSAT` (no unverified UNSAT). Leaf depths: U11_L 7:125, 11:2, 12:2, 13:180;
U_L5 7:125, 13:185, 18:1, 19:298; U_L6 7:126, 13:124, 19:224. Largest proof 266 MB; max leaf
solve 271 s.

## Cover check (`results/Mii-S/scripts/covercheck.py`)
- U11_L: `leaves.icnf` -> `s COVERED 309`. With the cake_lpr leaves this closes case U11_L
  (relative to the case CNF above); the verified check is still `lake exe cover_check` (H3).
- U_L5, U_L6, U_L7: leaves.icnf alone NOT COVERED; leaves.icnf + open.icnf -> COVERED
  (883, 947, 128 cubes), so open.icnf is exactly what is left.

## Resume
`BIN=<tools> python3 scripts/close_w28.py <this dir> <workdir> --cases U_L5=U_L5.cnf ...`
picks up the open cubes from leaves.jsonl + top.icnf (same case CNFs). Note U_L5 and U_L6 sit
in hard regions: depth-19 children still time out at 300 s, so estimates from est_core_s
(4.3 h and 0.33 h) were far too low for U_L5/U_L6; U11_L (est 7.9 h) took 2.4 h.
