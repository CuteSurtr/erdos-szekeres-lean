# Task Mi-0: shard 0 of 4, mirror-symmetric 33-point heptagon-free instance, sub-case (i)

Sub-case (i): the axis point is a hull vertex (`hm33k7.sub.cnf`, see `results/C/README.md`).
This shard is cubes whose 0-based line index i in `cubes.icnf` has i mod 4 == 0.

**Result: all 32 cubes in this shard are UNSAT, and lrat-check VERIFIED every one of them.
None was split, no leaf was SAT, and none is open.** This is a claim about one CNF. The
encoding is not formally verified (see `plan/es7_critique.md` item 4), so this is not a
theorem. It also covers only a quarter of the cube file; the other shards are Mi-1..Mi-3.

## Where it ran

One cloud VM: 4 cores, 15 GB RAM, Linux 6.18 x86_64 (`env.txt`). Wall time from start to
the last leaf was 02:36 to 02:57 UTC on 20 Oct 2026. Tool commits are in `tools.txt`:
- CaDiCaL 3.0.1 at `c6073042`;
- drat-trim/lrat-check at `2e3b2dc0`;
- CnC/march_cu at `705b60c6`, built with `-fcommon` added to the Makefile's flags.

## CNF

`results/C/scripts/make_cnfs.sh` (with `mirgen.py`) regenerated all CNFs (`logs/make_cnfs.log`).
- `hm33k7.sub.cnf` has sha256 `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d`,
  with 47,002 variables and 535,454 clauses.
- `results/C` and `results/C2` record no sha256. The variable and clause counts match
  `results/C/README.md`.
- The same sha256 appears in Mi-1, Mi-2, Mi-3, H3 and Mii-* (all sha256s are in `logs/cnf_sha256.txt`).

Validation passed. `validate.py` (1000 sets, seed 1) gave `logs/validate_report.json`, and
every non-timing field is identical to `results/C/logs/part1_validate_report.json`.
`controls.sh` passed too (`logs/controls.log`): m8k5 is SAT, while m9k5, hm9k5, m9k5.sub,
m17k6(.sub) and hm17k6(.sub) are UNSAT with lrat-check VERIFIED. The 32-point positive
control is SAT for m32k7 and m32k7.sub.

## Cubes

`march_cu hm33k7.sub.cnf -d 7 -o cubes.icnf` took 386 s (`logs/march_d7.log`).
- It reported "number of cubes 128, including 0 refuted leaves".
- `cubes.icnf` has 128 lines, sha256 `2a1b47b50879f6f3b594ea412239ef2dfd20c69acf63e8fe2fab3ec62ac8764d`,
  and this matches Mi-1, Mi-2 and Mi-3.
- Note that march_cu's count includes the refuted leaves, and it writes them to the cube file too (`cube.c`).
- This shard is the 32 cubes at lines 0, 4, ..., 124, each with 7 literals.

## Solving

The driver is `scripts/shard.py`. For each cube it writes CNF + cube units and runs
`cadical --lrat --binary=false -t 300`. The proof is streamed through a FIFO into
`lrat-check <CNF+cube> <fifo>`, which checks it clause by clause and prints VERIFIED only
after it derives the empty clause.

The split path (march_cu -d 6 on CNF+cube) was never needed: the slowest cube took 230 s.
I tested that path on small instances, where it splits and checks that the child cubes
form an exact binary partition. `leaves.jsonl` (one record per leaf) is also the resume
state. `logs/leaves_table.txt` is the same data as a table.

- Solve times: min 1.2 s, median 53 s, max 230 s; 2,245 CPU seconds of cadical in total.
- Five of the 32 leaves come from a first driver instance that I restarted after 1 minute
  to move its output out of the git tree. Those leaves were solved and checked the same way.
- Cross-check (`logs/xcheck_file_lrat.json`): I re-solved two cubes (origins 24 and 100)
  with the proof written to a file. lrat-check VERIFIED both, and the same proofs minus
  their last line gave NOT VERIFIED.

## SAT handling (unused)

`scripts/decode.py` maps a model back to all X(i,j,k) via the orbit representatives. It
then checks the CNF, the hull units, mirror consistency, and runs `scripts/sigverify.c`,
which checks the signotope axioms and does an exact convex-7-subset count by triangle
containment. On 3 random top-axis mirror sets in the hull frame, the decoded orientations
matched exactly, and sigverify's 7-gon count equalled `cgon` on the original Euclidean
points (187,631 / 110,349 / 61,499). No SAT leaf occurred.

## Counts

| shard cubes | closed (UNSAT, LRAT VERIFIED) | open | SAT | split |
|---|---|---|---|---|
| 32 | 32 | 0 | 0 | 0 |
