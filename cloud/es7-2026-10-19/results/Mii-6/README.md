# Task Mii-6: shard 6 of 8, mirror-symmetric 33-point instance, axis point interior (sub-case (ii))

Run of 20 Oct 2026, 02:36–06:15 UTC. **The shard is not closed.** 6 of its 16 cubes are closed,
and every one of their leaves was checked by lrat-check. 10 cubes are open. No SAT leaf was found.
Nothing here is a theorem or a counterexample. UNSAT is a claim about one CNF, and the encoding is
not formally verified (`plan/es7_critique.md` item 4).

## Machine

A cloud VM with 4 vCPUs, 15 GB RAM and no swap (`env.txt`). It was used only by this task, with
4 solver processes at a time. The container restarted once, at about 03:00 UTC, and about
14 minutes of solver work were lost (see "Incidents").

## Tools (`logs/tools.txt`)

All built from source in this session:

| tool | repository | commit |
|---|---|---|
| CaDiCaL 3.0.1 | arminbiere/cadical | `c60730422e758ef1cebe7aeddf2dda31c996bf04` |
| drat-trim / lrat-check | marijnheule/drat-trim | `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` |
| march_cu | marijnheule/CnC | `705b60c6491ef2b61988b3ce6ac674be1b90571d` |

march_cu was built with `CFLAGS="-O3 -fno-strict-aliasing -Wall -DNDEBUG -fcommon"`. Without
`-fcommon` it fails to link (multiple definition of `clause_red_depth`).

## CNF and validation

- `results/C/scripts/make_cnfs.sh` regenerated every CNF (`logs/make_cnfs.log`).
- `m33k7int.sub.cnf` has 47,002 variables and 515,121 clauses.
  sha256 `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`.
  All hashes are in `logs/cnf_sha256.txt`.
- `results/C` and `results/C2` record **no sha256**, so a hash comparison with them is not
  possible. The clause count does match `results/C/README.md` (515,121). The hash matches the
  hashes recorded by the sibling shards on this branch.
- `validate.py` (1000 sets, seed 1; `logs/part1_validate.log`, `logs/validate_report.json`)
  passed. Every figure equals the one in `results/C/README.md`.
- `controls.sh` (`logs/part1_controls.log`) passed:
  - m8k5 is SAT.
  - m9k5, hm9k5, m9k5.sub, m17k6(.sub) and hm17k6(.sub) are UNSAT, each with an LRAT proof that
    lrat-check VERIFIED.
  - The m32k7 and m32k7.sub positive controls are SAT under the classical set's orientations.

## Cubes (shard definition, unchanged)

- Command: `march_cu m33k7int.sub.cnf -d 7 -o cubes.icnf` (219.7 s; `logs/march_top_d7.log`).
- Result: **128 cubes, 0 refuted leaves.**
- `cubes.icnf` sha256: `cb32d049e5e4249fd5b57c3ca900feb602ff444fde0873c3fe296fbaaacc8244`.
  It is identical to the files of the sibling shards, and a copy is in this directory.
- Shard 6 is lines i ≡ 6 (mod 8), 0-based: 16 cubes, all of depth 7.

Note on march_cu: it **writes its refuted leaves to the cube file as well**. The count line
says "N cubes, including R refuted leaves", and if the whole formula is refuted it writes `a 0`.

## Method (`shard_driver.py`, resumable)

For each cube C, the driver writes the CNF plus C as unit clauses and runs
`cadical --lrat --binary=false -t 300`.

- **UNSAT:** `lrat-check <that CNF> <proof>` is run, then the proof is deleted.
- **Time limit reached:** the driver runs `march_cu <CNF+C> -d 6`. The children are C plus each
  subcube, and they are queued first in, first out.
- **Coverage check for each split:** the driver also solves a "gap" formula, CNF + C + ¬subcube_j
  for every j, with `cadical --lrat` and lrat-check. Its UNSAT certifies that the children cover
  every assignment that extends C, so coverage does not rely on trusting march's tree.
- **Records:** every job (cube, split, gap) appends one line to `leaves.jsonl`. Each line holds the
  literals, status, solve time, proof size, lrat-check result and check time.
- **Snapshot and resume:** `state.json` is the open-queue snapshot. A restart replays
  `leaves.jsonl` and does not repeat finished jobs.

`summarize.py` → `progress.json` counts a cube as **closed** only in two cases:
- it is UNSAT and lrat-check VERIFIED it; or
- it was split, its gap formula is VERIFIED, and every child is closed.

`decode_sat.py` and `tools/trackB/brute_kgon` were prepared for SAT leaves. They were not needed.

## Results (`progress.json`, `leaves.jsonl`)

| | count |
|---|---|
| cube jobs UNSAT, lrat-check VERIFIED | 384 (1 at depth 7, 383 at depth 13) |
| lrat-check FAILED | 0 |
| gap formulas UNSAT, VERIFIED | 7 |
| cubes that hit 300 s and were split | 16 (15 of the top cubes, plus one depth-13 cube) |
| SAT leaves | **0** |
| open (unsolved) leaves | 640, plus 9 gap formulas not yet run |
| CaDiCaL CPU time | 31,256 s |

The largest UNSAT leaf took 270.5 s and produced a 0.24 GB proof. The depth-13 leaves typically
took 20–120 s each. Each `march_cu -d 6` split took 165–843 s.

Per top cube (line index: status):

- **Closed (6), all LRAT-checked:**
  - 6, 14, 22, 30, 70: each split into 64 depth-13 children; all children are VERIFIED and the gap
    is VERIFIED.
  - 54: UNSAT directly in 115.7 s, VERIFIED.
- **Open (10):**
  - 62: 96.9 % of its weight is closed. One child, `… 3534 3765`, timed out and was re-split, and
    the gap for 62 has not been run.
  - 46: 1.6 % closed.
  - 38, 78, 86, 94, 102, 110, 118, 126: split into 64 children each, none solved yet.

Closed weight of the shard: **0.4365** (each of the 16 cubes weighs 1/16, and a child at local
depth d weighs 2^-d).

**LRAT coverage:** every leaf and gap counted as closed has a VERIFIED lrat-check, so coverage of
the closed part is 100 %. The open part has no claim.

**Is the entire shard closed? No.** Resuming `shard_driver.py` with the same arguments continues
from `leaves.jsonl`. Note that the split children of the open cubes are already recorded there.

## Incidents (affect only the bookkeeping, not any verdict)

1. **Container restart at about 03:00 UTC.**
   - The first driver run had written nothing yet. Its log is `driver_run1_lost.log`, which was not
     committed.
   - The driver was changed to log the timeout and the split as separate records.
   - It was then restarted from scratch at 03:05.
2. **Checkpoint overwrote the log at about 03:22–04:13 UTC.**
   - The checkpoint script ran `git pull --rebase` while the driver was appending to
     `leaves.jsonl` inside the repository. The rebase replaced the file, and the driver kept
     writing to the deleted inode.
   - Recovery came from the driver's stdout log (`logs/driver_run2.log`). Every record there is
     complete, but split records omit the children list.
   - The 4 splits whose children were in the committed file were kept.
   - The other 11 splits are marked `children_lost` and are ignored. They were re-run with the same
     deterministic `march_cu -d 6`.
   - Consistency check: all 312 solved depth-13 cubes appear in their parent's child list.
   - Since then the driver writes in scratch space, and the checkpoints copy it into the repository.
3. One depth-7 cube that was running at 04:13 was killed and re-solved. Its verdict was not
   affected.
