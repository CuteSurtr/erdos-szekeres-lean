# Mii-4: shard 4 of 8, mirror-symmetric 33-point heptagon-free instance, sub-case (ii) (axis point interior)

Run from 20 Oct 2026, 02:36 to 06:15 UTC. **The shard is not closed.** The run found no SAT leaf.

## Where it ran

The run used one cloud VM ("vm", Linux 6.18 x86_64, 4 cores, 15 GB RAM; see `env.txt`). No other
jobs ran on it. All 4 cores ran the shard.

Tools were built from source (commits in `logs/tool_commits.txt`):

| tool | commit | build |
|---|---|---|
| CaDiCaL 3.0.1 | c60730422e758ef1cebe7aeddf2dda31c996bf04 | `./configure && make` |
| drat-trim / lrat-check | 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 | `make` |
| march_cu (CnC) | 705b60c6491ef2b61988b3ce6ac674be1b90571d | Makefile CFLAGS plus `-fcommon`, because the link failed on duplicate globals without it |

## The CNF and the validation

- `m33k7int.sub.cnf` was regenerated with `results/C/scripts/make_cnfs.sh`, which calls `gen_etv.py` and `mirgen.py --interior --yflip-unit`. It has 47,002 variables and 515,121 clauses.
- Its sha256 is `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`.
- `results/C` and `results/C2` record no sha256 for this file, so there was nothing there to compare against. The same hash appears in the committed logs of all 7 sibling shards (Mii-0…3, 5…7), so they match. The hashes of every generated CNF are in `logs/cnf_sha256.txt`.
- `validate.py` was run with 1000 sets and seed 1 (`logs/part1_validate_report.json`). Every field except the timings equals `results/C/logs/part1_validate_report.json`, for example `A_m33k7int.sub.xonly_SAT 500/500` and `A4_m33k7_full_unsat_iff_7gon 200/200`.
- `controls.sh` passed (`logs/part1_controls.log`):
  - m8k5 is SAT.
  - m9k5, hm9k5, m9k5.sub, m17k6(.sub) and hm17k6(.sub) are UNSAT, and lrat-check VERIFIED each one.
  - The m32k7 and m32k7.sub positive controls are SAT under the classical set's orientations.

## The shard definition

- I ran `march_cu m33k7int.sub.cnf -d 7 -o cubes.icnf` (212 s). It reported **128 cubes, including 0 refuted leaves**.
- The sha256 of `cubes.icnf` is `cb32d049e5e4249fd5b57c3ca900feb602ff444fde0873c3fe296fbaaacc8244`. It matches the hash in every sibling shard's committed logs.
- All 128 cubes have 7 literals. I checked that together they form a complete binary partition.
- A copy of the cube file is in `logs/cubes_d7.icnf`.
- Shard 4 is the 0-based lines i with i mod 8 = 4: lines 4, 12, …, 124, which is 16 cubes.

## Method (`shard.py`)

1. Each job is the CNF plus its cube as unit clauses. It runs with `cadical -q --lrat --binary=false -t 300`.
2. Every UNSAT result is checked with `lrat-check` against exactly that CNF file. The proof is deleted after the check.
3. If a job hits the 300 s limit, `march_cu -d 6` runs on CNF + cube. Each sub-cube (parent literals plus the new literals) becomes a new job, and so on recursively.
4. Each split also gets a **remainder** job: CNF + parent units + one clause ¬C for every sub-cube C. It covers the branches march_cu refuted by look-ahead, so a parent counts as closed only when every sub-cube and its remainder are UNSAT and LRAT-VERIFIED.
5. `leaves.jsonl` holds one record per finished job: cube literals, status, solve time, proof size, check time and lrat-check verdict. SPLIT records list their children.
6. `state.json` holds the job list for restarting.
7. `summary.json` is produced by the summary script (in `logs/`) and gives the closed weight per top cube. A sub-cube's weight is 2^-(its depth below the parent). A closed remainder counts for the parent's weight that no sub-cube covers.

## Results (at 06:15 UTC, when the run was stopped)

- 16 jobs were split: 15 of the 16 top cubes, plus one depth-13 sub-cube of top cube 44.
- 661 jobs finished UNSAT, and **all 661 are lrat-check VERIFIED (100% LRAT coverage)**. That count includes 10 remainder jobs.
- No job was SAT. No UNSAT result failed its LRAT check, and no remainder job timed out.
- Summed CaDiCaL solve time for these jobs was 38,107 s. The longest single solve took 278 s. About 43 GB of LRAT text was written and checked, then deleted.
- **Closed (all leaves VERIFIED), 9 of 16 top cubes:** lines 4, 12, 20, 28, 36, 52, 60, 68 and 76. Line 52 was solved directly in 77 s; the other 8 were each split into 64 sub-cubes plus a remainder.
- **Open, 7 of 16 top cubes** (split, with 379 jobs still pending):

  | line | closed weight | pending jobs |
  |---|---|---|
  | 44 | 63/64 | 65 (one depth-13 sub-cube was split again) |
  | 84 | 63/64 | 1 |
  | 100 | 0.1875 | 53 |
  | 92 | 0 | 65 |
  | 108 | 0 | 65 |
  | 116 | 0 | 65 |
  | 124 | 0 | 65 |

- The shard's closed weight is 0.697 (= 714/1024).

A restart can resume from `state.json` + `leaves.jsonl` with
`shard.py <cnf> <cubes.icnf> <this dir> <workdir> 4 300`. Finished jobs are skipped.

## What this does and does not mean

Each VERIFIED leaf certifies one statement: "this CNF plus these units (and clauses) is UNSAT." The encoding itself is not formally verified (`plan/es7_critique.md` item 4). It was only tested by the validation and controls above. So even a fully closed shard would be an LRAT-checked UNSAT claim about `m33k7int.sub.cnf`, not a theorem.

This shard is **not** fully closed. The run found no SAT leaf and therefore no signotope candidate. The decoder and brute-force check prepared for SAT leaves (`.sig` output followed by `tools/trackB/brute_kgon.c`) were never needed.
