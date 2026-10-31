# Task Mii-7: shard 7 of 8, mirror-symmetric 33-point instance, axis point interior (sub-case (ii))

**Result: the shard is NOT closed.** 0 of its 16 top-level cubes are fully closed. No SAT
leaf appeared, and every UNSAT leaf (881 of 881) was checked VERIFIED by lrat-check. Nothing
here is a theorem or a counterexample.

## Where it ran

Cloud VM `vm` (`env.txt`): Linux 6.18.44 x86_64, 4 cores, 15 GB RAM, no swap. Run from
02:36 to 06:12 UTC on 20 Oct 2026, with 4 parallel workers throughout.

Tools were built from source (`logs/tools.txt`):

| tool | commit | build |
|---|---|---|
| CaDiCaL 3.0.1 | c60730422e758ef1cebe7aeddf2dda31c996bf04 | `./configure && make` |
| drat-trim / lrat-check | 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 | `make` |
| CnC march_cu | 705b60c6491ef2b61988b3ce6ac674be1b90571d | Makefile flags plus `-fcommon` |

## CNF

`m33k7int.sub.cnf` was regenerated with `../C/scripts/make_cnfs.sh` (which calls `gen_etv.py`
and `mirgen.py --interior --yflip-unit`). It has 47,002 vars and 515,121 clauses, the same
counts as `../C/README.md`. All sha256 values are in `logs/cnf_sha256.txt`.

- sha256 `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`
- Neither `results/C` nor `results/C2` records a sha256 for this file, so there was nothing
  there to compare against. It **matches** the sha256 that the sibling shard Mii-4 recorded
  (`../Mii-4/logs/cnf_sha256.txt`).

## Validation and controls (passed)

- `logs/part1_validate.log`: `validate.py`, seed 7, 1,000 random exact mirror sets.
  - All four CNFs: the orientation-only clauses are satisfied in every frame (1000/1000 and
    500/500).
  - Interior clause matches the geometry: 1000/1000.
  - Projective map: 0 orientation mismatches.
  - UNSAT iff a 7-gon is present: 200/200. Hull frame: 100/100 UNSAT.
  - Small-k equivalence: 2000/2000 on all 7 rows.
- `logs/part1_controls.log` (`controls.sh`):
  - m8k5 is SAT.
  - m9k5, hm9k5, m9k5.sub, m17k6(.sub) and hm17k6(.sub) are UNSAT, each LRAT VERIFIED.
  - Classical mirror 32-set: 0 identity violations. m32k7 and m32k7.sub are SAT under its
    orientations.

These are tests, not a proof: the encoding is unverified in the sense of
`plan/es7_critique.md` item 4.

## Shard definition (as specified, unchanged)

`march_cu m33k7int.sub.cnf -d 7 -o cubes.icnf` (log: `logs/march_top_d7.log`, 238 s):

- **128 cubes, 0 refuted leaves**
- cube-file sha256 `cb32d049e5e4249fd5b57c3ca900feb602ff444fde0873c3fe296fbaaacc8244`
  (file: `logs/cubes_top_d7.icnf`)
- `treecheck.py` confirms that the 128 cubes form a complete binary partition.

This shard is the cubes with 0-based index i ≡ 7 (mod 8): c7, c15, …, c127, 16 cubes
(`logs/shard7_cubes.txt`).

## Method (`shard.py`)

- **Solving a cube.** Each cube is solved as CNF + cube units with
  `cadical -q --lrat --binary=false -t 300`. Every UNSAT is checked with `lrat-check` against
  that exact CNF, and the proof is then deleted.
- **Splitting.** A cube that times out at 300 s is split with `march_cu -d 6` on CNF + cube.
  Each sub-cube (parent + sub-cube literals) is queued.
- **Gap task.** Each split also queues one *gap* task: CNF + parent units + the clauses
  ¬c_j over all sub-cubes. Its LRAT-verified UNSAT covers any branches march_cu refuted
  internally.
- **When a node counts as closed.** Only when every child and its gap are UNSAT + VERIFIED.
  Every split file (`logs/splits/`) also passes `treecheck.py` as a complete partition.
- **Records and restarts.** Every task is recorded in `leaves.jsonl`. Each record holds the
  cube literals, status, solve time, LRAT result, proof size, and the children if the task
  was split. `state.json` is a resumable snapshot. On restart, finished tasks are skipped and
  split children are re-queued.

### Operational notes

- **First start (02:43).** With `-q`, cadical reports a timeout as `c UNKNOWN`, so the first
  4 timeouts were recorded as ERROR. I fixed the parsing and restarted at 02:48. The aborted
  records are in `logs/leaves_aborted_first_start.jsonl` and are not used.
- **Queue order (04:42).** I changed the queue from FIFO to "top cubes with the fewest pending
  tasks first, depth-first inside a top cube", so that whole cubes would close sooner. This
  changes scheduling only, not the shard. The in-flight tasks were killed and redone. Driver
  logs: `logs/driver_run1.log` and `logs/driver_run2.log`.

## Results (snapshot 06:12 UTC; `logs/final_stats.json`, `logs/final_summary.json`)

| | count |
|---|---|
| top-level cubes in shard | 16 |
| top-level cubes fully closed | **0** |
| UNSAT leaves (sub-cubes 870 + gap tasks 11) | 881 |
| of these LRAT VERIFIED / FAILED | **881 / 0** |
| SAT leaves | **0** |
| splits (cube timed out at 300 s, march_cu -d 6) | 31 (1,980 children) |
| tasks still pending (open) | 1,084 |
| max cube length | 31 |

- **Closed weight** (fraction of each top cube covered by closed sub-cubes):
  - c15: 0.99798. Only part of the hard region c15.63 is still open; it needed splits down to
    four levels.
  - c23: 0.921875 (59/64 sub-cubes closed). c23.47 has been split. c23.59, .61, .62 and .63
    are pending: they timed out before the 04:42 restart, which interrupted their splits.
    The gap task c23.g is also pending.
  - The other 14 cubes: 0. Each was split into 64 sub-cubes, none of them solved yet.
  - **Whole shard: 0.1200.**
- **CPU spent:**
  - UNSAT solves: 25,455 s (max 291.6 s).
  - lrat-check: 515 s.
  - Timed-out solves that led to splits: 9,301 s.
  - march_cu splits: 11,519 s (up to 1,085 s each).
  - The LRAT proofs checked total 29.2 GB of text; all were deleted.
- **Rough estimate:** at the observed 30–60 s per depth-13 sub-cube, the ~900 unsolved
  depth-13 sub-cubes of c7 and c31–c127 would need roughly 8–15 more core-hours, plus the
  hard regions.

No SAT model was found, so nothing was decoded or passed to `tools/realizer/`.
`satcheck.py` was prepared and tested for that case: it decodes a model and brute-force checks
the signotope axioms, mirror consistency, the interior axis point and convex 7-gons. Its
self-test agrees 83/83 with exhaustive geometry, and it checks a real SAT model of m11k6.

## What can be claimed

The claims below are only about the CNF `m33k7int.sub.cnf` (sha256 above):

- **LRAT-checked UNSAT.** For each of the 870 cubes listed as UNSAT in `leaves.jsonl`,
  CNF ∧ cube is UNSAT, certified by lrat-check. The same holds for the 11 gap formulas.
- **Not closed.** No top-level cube, and therefore not the shard, is closed.

## Files

- **Scripts:** `shard.py` (driver), `summarize.py` (closure and weights), `finalstats.py`,
  `treecheck.py` (partition check), `satcheck.py` (SAT-model checker).
- **Records:** `leaves.jsonl` (all leaf records), `state.json` (resumable state; pending ids).
- **Logs:** `logs/` holds the CNF and cube hashes, top cubes, split cube files, validation
  and control logs, driver logs and final stats.
- **Not committed:** CNF and LRAT files.
- **To resume:** run `python3 shard.py <cnf> logs/cubes_top_d7.icnf 8 7 <workdir> leaves.jsonl
  state.json 4 300 6 3600`.
