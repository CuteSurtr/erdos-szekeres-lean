# Mii-1: shard 1 of 8, mirror-symmetric 33-point instance, axis point interior (sub-case (ii))

Run 20 Oct 2026, 02:36–06:20 UTC, one cloud VM. **The shard is not closed**: 7 of its 16 cubes
are fully closed with every leaf LRAT-checked, 2 are partly closed, 7 were never started. No SAT
leaf was found. Nothing here is a theorem or a counterexample.

## Machine and tools

`env.txt`: Linux x86_64 VM, 4 cores, 15 GB RAM, no swap. All work ran here, 4 workers.
Commits and build flags are in `logs/tools.txt`:

- CaDiCaL `c60730422e75` (3.0.1);
- drat-trim / lrat-check `2e3b2dc0ecf9`;
- CnC / march_cu `705b60c6491e`. march_cu needs `-fcommon` to link, so it was built with the
  Makefile's flags plus `-fcommon`.

## Instance

`m33k7int.sub.cnf` was regenerated with `results/C/scripts/make_cnfs.sh` (gen_etv.py + mirgen.py
`--interior --yflip-unit`). It has 47,002 variables and 515,121 clauses, the same as
`results/C/README.md`.

- sha256 `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`. results/C and
  results/C2 record no sha256 for this file, so there was nothing to compare there. It matches
  the sha256 recorded on this branch by shards Mii-0, Mii-2, Mii-3, Mii-4, Mii-6, Mii-7 and Mi-1.
- Validation (`logs/part1_validate.log`, `logs/validate_report.json`; validate.py, 1,000 sets,
  seed 1) passed, with every figure identical to results/C Part 1. For example:
  A1 1000/1000, A2 1000/1000, m33k7int.sub x-only 500/500, A4 200/200 and 100/100, and all
  B rows agree 2000/2000.
- Controls (`logs/part1_controls.log`, controls.sh) passed, identical to C/C2:
  - m8k5 SAT;
  - m9k5, hm9k5, m9k5.sub, m17k6(.sub) and hm17k6(.sub) UNSAT, each with lrat-check VERIFIED;
  - m32k7 and m32k7.sub SAT under the classical 32-point set's orientations.

## Shard definition (as specified)

`march_cu m33k7int.sub.cnf -d 7 -o cubes.icnf` (213 s) produced **128 cubes, including 0
refuted leaves**: a complete depth-7 binary tree.

- `cubes.icnf` sha256 `cb32d049e5e4249fd5b57c3ca900feb602ff444fde0873c3fe296fbaaacc8244`, the
  same as Mii-0, Mii-4 and Mii-7.
- The file is in `logs/cubes.icnf`.
- This shard is lines i with i mod 8 = 1: i = 1, 9, …, 121 (16 cubes).

## Method (`shard.py`)

- **Leaf.** A leaf is CNF + cube units, solved by `cadical --lrat --binary=false -t 300`.
  Every UNSAT proof is checked by `lrat-check` and then deleted.
- **Split.** A leaf that runs out its 300 s is split with `march_cu -d 6` on CNF + cube. Its
  children are the cube extended by each sub-cube. march_cu writes refuted leaves into the cube
  file too, so the children form a complete partition, and every child is solved like any other
  leaf.
- **Gap check.** For every split, a "gap" instance (CNF + cube + one clause ¬s for each
  sub-cube s) is solved with LRAT and checked. This gives a checked proof that the children
  cover the parent.
- **Records.** `leaves.jsonl` records every leaf, split and gap: cube literals, status, solve
  time, proof size, LRAT result and time. It is also the resume state: a restart skips finished
  nodes.
- **Summary.** `summarize.py leaves.jsonl` rebuilds the per-root tree. Its output is
  `status.json`.
- **SAT leaves.** `verify_sat.py` is the brute-force checker for a SAT leaf: signotope axiom on
  all 4-tuples, mirror identity, interior axis point, and exhaustive convex-7-gon search. It was
  tested on an m32k7.sub model (0 heptagons, and it finds the 6-gons when run with k = 6). It
  was not needed, because no leaf came back SAT.

## Results (final snapshot, `status.json`)

| root (line) | status | UNSAT leaves (all LRAT VERIFIED) | open |
|---|---|---|---|
| 1, 9, 17, 65 | closed | 64 each (one split) | 0 |
| 25 | closed | 126 (split + 1 deeper split) | 0 |
| 41 | closed | 252 (split + 3 deeper splits) | 0 |
| 49 | closed | 1 (solved directly at depth 7) | 0 |
| 33 | **open** | 126 | 1 depth-19 node that timed out and was not yet split (weight 1/4096 of the cube) |
| 57 | **open** | 39 | 25 sub-cubes (weight 25/64) |
| 73, 81, 89, 97, 105, 113, 121 | **not started** | 0 | whole cube |

Totals:

- 814 leaf solves: 800 UNSAT, 14 timeouts (each one split), 0 SAT.
- LRAT: 800/800 leaf proofs VERIFIED, and 13/13 gap proofs VERIFIED. 0 failures.
- Leaf depths 7–25. Largest proof 256 MB. Longest leaf solve 293 s.
- CPU: 42,913 s in CaDiCaL and 843 s in lrat-check. march_cu splits took 400–600 s each, on top
  of that.
- Closed weight inside the shard: 7 + 4095/4096 + 39/64 = 8.609 of 16 root cubes, about 53.8 %.
  In units of the whole instance that is 8.609/128, about 6.7 %.

**Certified part.** These 7 cubes are closed, with every leaf and every split's coverage
checked by lrat-check (line index : cube):

- line 1 : `-1651 -345 -1245 2029 -2380 2705 3005`;
- lines 9, 17, 25, 41, 49, 65 : the cubes on those lines of `logs/cubes.icnf`.

This is a statement about the CNF `m33k7int.sub.cnf` (sha256 above) under those cube
assumptions. The encoding itself is not formally verified (plan/es7_critique.md item 4), and
the result is not a theorem.

**Not closed.** Root 33 (one depth-19 node), root 57 (25 depth-13 sub-cubes) and roots 73–121.

## Notes

- Throughput, as observed:
  - every depth-7 cube except line 49 ran out the 300 s;
  - a depth-6 march_cu split then takes about 7–10 min;
  - most depth-13 leaves take 40–90 s.

  At that rate a cube costs about 20 min of wall time on 4 cores. The 9 unfinished cubes need
  roughly 3 more hours on this machine.
- Resuming: run `shard.py <cnf> logs/cubes.icnf <bindir> <workdir> leaves.jsonl 4 1 8` with
  this `leaves.jsonl`. It skips every finished leaf, split and gap, and re-runs only the
  unfinished nodes. A node that already timed out is not re-tried: its stored split is reused.
- Incident: at 02:44 a `git pull --rebase` replaced `leaves.jsonl` while the driver held it
  open, so the driver kept appending to the unlinked file. No record was lost. The live log was
  copied out through `/proc/<pid>/fd` for every checkpoint, and the committed file is that
  complete log.
- No CNF, LRAT or other file over 50 MB is committed.
