# Mi-3: shard 3 of 4, mirror-symmetric 33-point heptagon-free instance, sub-case (i)

Sub-case (i): the axis point is a hull vertex (`hm33k7.sub.cnf`, see `results/C/README.md`).
Shard = cubes of `march_cu hm33k7.sub.cnf -d 7` whose 0-based line index i has i % 4 == 3.

**Result: every one of the 32 cubes in this shard is closed. There are 799 UNSAT leaves, all
checked VERIFIED by lrat-check, and 0 SAT leaves.** This is a claim about one CNF. The
encoding is not formally verified (see `plan/es7_critique.md` item 4), so this is not a
theorem, and it covers only one quarter of sub-case (i).

## Where it ran

A cloud VM with 4 cores and 15 GB RAM (`env.txt`), from 02:36 to 04:20 UTC on 20 October 2026.
Tool commits are in `tools.txt`: CaDiCaL c607304 (3.0.1), drat-trim/lrat-check 2e3b2dc and
CnC/march_cu 705b60c (built with `-fcommon`).

## Setup (`setup.txt`)

- `hm33k7.sub.cnf` was regenerated with `results/C/scripts/make_cnfs.sh`: `p cnf 47002 535454`,
  sha256 `bfbc2d60…757d`. results/C and results/C2 record no sha256 for this file. The clause
  count matches C's README, and the sha256 matches the ones recorded by sibling runs Mi-1,
  Mi-2 and Mii-*.
- Validation (`validate.py`, 1000 sets, seed 1) and the controls (`controls.sh`) all passed,
  with the same figures as in results/C. The logs are in `logs/`.
- `march_cu -d 7` reported "number of cubes 128, including 0 refuted leaves". `cubes.icnf`
  has sha256 `2a1b47b5…764d`, which matches Mi-1/Mi-2.
- A shard-independent check: the CNF plus the negation of all 128 cubes is UNSAT, with LRAT
  VERIFIED. So the 128 cubes cover the whole instance.

## Method (`shard_solve.py`)

- Each cube is solved as CNF plus unit clauses with `cadical --lrat -t 300`, and every UNSAT
  is checked with `lrat-check`.
- A cube that times out is split with `march_cu -d 6` on CNF plus cube. Each child is the cube
  plus a subcube.
- For each split, a **residual** instance is also solved and LRAT-checked. The residual is CNF
  plus the cube plus one clause negating each subcube. It certifies the branches march_cu
  refuted, and that the children cover the node.
- So every closed node rests on LRAT-checked proofs only. `status.py` recomputes closure from
  `leaves.jsonl`.

## Numbers (`logs/final_status.json`)

- 32 of 32 top cubes are closed.
- 7 top cubes needed splitting: 31, 55, 63, 79, 91, 95 and 127. Splits went down to depth 25:
  12 split nodes in all, each with 63–64 children.
- 799 UNSAT records: 787 cube leaves and 12 residuals. All 799 are LRAT VERIFIED.
- There are 0 SAT leaves and 0 open leaves.
- CaDiCaL time was 15,563 s; the longest single solve hit the 300 s limit. The LRAT proofs
  totalled 13.9 GB, checked and then deleted.

## Incident

A checkpoint commit (git pull with autostash) ran while the solver was appending. It dropped
4 depth-19 leaf records under cube 79 from `leaves.jsonl`. They had been solved and VERIFIED
(see `logs/run.log`). They were then re-solved through the resume path; each was UNSAT and
LRAT VERIFIED again, and the new records are in `leaves.jsonl`.
