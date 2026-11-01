# Mii-3: shard 3 of 8, mirror-symmetric 33-point heptagon-free instance, sub-case (ii)

**Status: shard NOT closed.** I stopped the run at the 4-hour budget (06:13 UTC) with 739
leaves still open. There are no SAT leaves. Every closed leaf is UNSAT, and lrat-check
verified each one.

## Where it ran
Claude Code cloud container (`env.txt`): Linux x86_64, 4 cores, 15 GB RAM. Run from
02:36 to 06:13 UTC on 20 Oct 2026. The container restarted once, at about 03:05; the
driver resumed from `leaves.jsonl`, and the 4 leaves that were in flight were redone.

## Tools (`logs/tools.txt`)
- CaDiCaL c60730422e758ef1cebe7aeddf2dda31c996bf04 (3.0.1).
- drat-trim / lrat-check 2e3b2dc0ecf938addbd779d42877b6ed69d9a985.
- CnC / march_cu 705b60c6491ef2b61988b3ce6ac674be1b90571d. It needed `-fcommon` to link.
- This CaDiCaL head rejects `-q`, so I ran `C/scripts/controls.sh` through a wrapper that
  only drops `-q`.

## CNF
I regenerated the CNF with `C/scripts/make_cnfs.sh` (gen_etv.py + mirgen.py).
- `m33k7int.sub.cnf`: `p cnf 47002 515121`.
- sha256 `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`.
- Neither `results/C` nor `results/C2` records a sha256, so there is no hash to compare
  against. The vars, clause count and orbit count (2,736) match `results/C/README.md`.
- Hashes of all generated CNFs are in `logs/cnf_sha256.txt`.

Validation and controls passed:
- `C/scripts/validate.py`, seed 1, 1000 sets (`logs/validate.log`,
  `logs/validate_report.json`). Every figure is identical to C's seed-1 report.
- `C/scripts/controls.sh` (`logs/controls.log`): m8k5 SAT; the m9k5/hm9k5/m17k6/hm17k6
  family and their `.sub` versions UNSAT, each LRAT VERIFIED; the m32k7 and m32k7.sub
  positive controls SAT.

## Shard definition (as specified)
- I ran `march_cu m33k7int.sub.cnf -d 7 -o cubes.icnf` (217 s).
- It reported "number of cubes 128, including 0 refuted leaves".
- `cubes.icnf` sha256 is `cb32d049e5e4249fd5b57c3ca900feb602ff444fde0873c3fe296fbaaacc8244`.
- All 128 cubes have depth 7. They form a complete binary partition with no gaps (checked).
- Shard 3 is the cube lines with 0-based index i, i mod 8 == 3. There are 16 of them,
  saved in `shard3_cubes.icnf`. My shard is 16/128 of the instance.

## Method (`shard_driver.py`)
- Each leaf is the CNF plus the cube literals as unit clauses. I solve it with
  `cadical -t 300 --lrat --binary=false`, then check every UNSAT with lrat-check against
  that exact file.
- A leaf that times out is split with `march_cu <CNF+cube> -d 6`.
- The children are the cube extended by each emitted sub-cube, plus any branch march_cu
  refuted itself (a "gap"). Each split is checked to be a binary partition.
- Across all 20 splits there were 0 gaps, so no part of my shard's closed weight rests on
  march_cu's own refutation.
- `leaves.jsonl` records every result: cube, status, solve time, LRAT result, proof size,
  and the children of each split. It is also the resume state.
- `verify_sat.py` is the SAT-leaf checker: signotope axioms, mirror identity, interior
  axis point, X(1,2,3), and an exhaustive convex 7-gon search. I tested it on one
  heptagon-free 32-point set (no 7-gon found) and on the AlphaEvolve 33-point set (finds
  its 7-gon). It was never needed.

## Results (`final_summary.json`)
- All 16 top-level depth-7 cubes timed out at 300 s and were split into 64 children each.
  4 of the depth-13 children were split again.
- **Closed:** 521 leaves UNSAT, **521/521 LRAT VERIFIED** (0 failed). That is 50.98% of
  the shard's weight, counting weight as 2^-depth.
  - 33,035 s of CaDiCaL time and 667 s of lrat-check time in total.
  - Slowest closed leaf: 276 s.
- **Open:** 739 leaves (498 at depth 13, 240 at depth 19, 1 at depth 15), 49.02% of the
  weight. Closed plus open adds up to exactly the shard.
- **SAT:** 0.
- No top-level cube is fully closed.

To resume, regenerate the CNF and `cubes.icnf` (check both sha256s), then run:
`shard_driver.py m33k7int.sub.cnf cubes.icnf <bindir> <workdir> leaves.jsonl 4 300`

## Caveats
Each UNSAT is a claim about one CNF, CNF + cube, and is LRAT-certified for that CNF only.
The encoding is not formally verified (critique item 4). Even a fully closed shard would
not be a theorem.
