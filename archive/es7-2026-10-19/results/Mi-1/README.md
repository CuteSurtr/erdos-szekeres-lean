# Mi-1: shard 1 of 4, mirror-symmetric 33-point heptagon-free instance, sub-case (i)

Sub-case (i) = the axis point is a hull vertex (`hm33k7.sub.cnf`, see `../C/README.md`).
Shard = cubes with 0-based line index i, i mod 4 == 1, of `march_cu hm33k7.sub.cnf -d 7 -o cubes.icnf`.

## Where it ran
One cloud container (`env.txt`): Linux x86_64, 4 cores, 15 GB RAM, nothing else running.
Wall time 02:36–03:20 UTC, 20 Oct 2026. Solving itself took 02:53–03:13 UTC.

Tools built from source (`tools.txt`): CaDiCaL 3.0.1 `c60730422e758ef1cebe7aeddf2dda31c996bf04`,
drat-trim/lrat-check `2e3b2dc0ecf938addbd779d42877b6ed69d9a985`, CnC/march_cu
`705b60c6491ef2b61988b3ce6ac674be1b90571d`. march_cu needed `-fcommon` to link: built with
`make CFLAGS='-O3 -fno-strict-aliasing -Wall -DNDEBUG -fcommon'`.

## Inputs and checks
- I regenerated the CNFs with `../C/scripts/make_cnfs.sh`. `hm33k7.sub.cnf` has 47,002 vars and 535,454 clauses, as in the C README.
  Its sha256 is `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d`.
  Neither C nor C2 records a sha256 for this file. It **matches** the sha256 that sibling runs Mii-4 and Mii-7 recorded from their own regenerations (`cnf_sha256.txt`).
- `validate.py` (seed 1, 1000 sets) passed every check, with numbers identical to C's report (`logs/part1_validate.log`, `logs/validate_report.json`).
  `controls.sh` passed: m8k5 is SAT; the m9k5, hm9k5, m9k5.sub and the k=6 17-point instances are UNSAT with LRAT VERIFIED; the m32k7 and m32k7.sub positive controls are SAT (`logs/part1_controls.log`).
- march_cu `-d 7` took 6.5 min (`logs/march_d7.log`). It produced **128 cubes, 0 refuted leaves**, all of depth 7, forming a complete binary partition (`cubes_check.json`).
  The `cubes.icnf` sha256 is `2a1b47b50879f6f3b594ea412239ef2dfd20c69acf63e8fe2fab3ec62ac8764d`, which matches Mi-2's `provenance.txt`.

## Method (`shard.py`)
- Each leaf is the CNF plus the cube as unit clauses. It is solved with `cadical -q --lrat --binary=false -t 300`, and the proof is checked with `lrat-check` against that exact CNF, then deleted.
- A leaf that times out is split with `march_cu <CNF+cube> -d 6`. The children are the parent cube plus each child cube.
- Each split also gets a cover check: CNF + cube + the negation of every child cube must be UNSAT, LRAT-checked. This certifies any branches march_cu refutes by lookahead.
- Every record is in `leaves.jsonl`, which is also the resume state. `audit.py` re-derives coverage from it independently (`audit.json`).

## Result
- All 32 shard cubes closed. One cube timed out and was split: top-level index 93, `-1015 -525 2045 -1421 2030 -2014 1997`.
  march_cu gave 64 children with 0 refuted, and the cover check is UNSAT with LRAT VERIFIED.
- Leaves: 95 UNSAT, all 95 LRAT VERIFIED (31 top-level + 64 children); 0 SAT; 0 open; 0 LRAT failures.
- The longest leaf took 244 s; the largest proof was 0.17 GB. Total CaDiCaL time was about 3,659 s, including the 300 s timeout.
- **The entire Mi-1 shard is closed. Every leaf and the one split cover are LRAT-checked.**

What this means: for each of the 32 shard cubes, `hm33k7.sub.cnf` ∧ cube is UNSAT, and lrat-check certified it.
This is a claim about this CNF only. The encoding is not formally verified (`plan/es7_critique.md` item 4), and it is not a theorem.
Sub-case (i) as a whole is closed only if shards Mi-0, Mi-2 and Mi-3 also close. The 128 cubes partition the space with no refuted leaves, so nothing outside the four shards needs checking.

`check_sat.py` (SAT-leaf decoder and brute-force checker) was prepared but not needed.
