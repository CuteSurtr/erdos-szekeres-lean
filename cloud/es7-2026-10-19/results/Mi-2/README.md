# Mi-2: shard 2 of 4, mirror-symmetric 33-point heptagon-free instance, sub-case (i)

Sub-case (i): the axis point is a hull vertex (`hm33k7.sub.cnf`, see `results/C/README.md`).

## Where it ran
One cloud VM (`env.txt`): Linux x86_64, 4 cores, 15 GB RAM. Run 20 Oct 2026, 02:36–03:31 UTC.
Tools built from source; commits in `provenance.txt` (CaDiCaL 3.0.1 c6073042, drat-trim/lrat-check
2e3b2dc0, CnC/march_cu 705b60c6; march_cu needed `-fcommon`).

## CNF and validation
- `hm33k7.sub.cnf` regenerated with `results/C/scripts/make_cnfs.sh`:
  sha256 `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d`, header `p cnf 47002 535454`.
  No sha256 is recorded in `results/C` or `results/C2`; the header matches the counts in
  `results/C/README.md`, and sibling shards Mi-* report the same sha256.
- `validate.py` (1,000 sets, seed 1): every check passed, with the same numbers as Task C
  (`logs/validate_report.json`). `controls.sh`: all controls as expected (m8k5 SAT; m9k5, hm9k5,
  m9k5.sub, m17k6(.sub), hm17k6(.sub) UNSAT with lrat-check VERIFIED; the 32-point mirror set
  satisfies m32k7 and m32k7.sub) (`logs/part1_controls.log`).

## Cubes (shard definition, identical for all shards)
`march_cu hm33k7.sub.cnf -d 7 -o cubes.icnf`: 128 cubes, 0 refuted leaves (`logs/march_top.log`),
`cubes.icnf` sha256 `2a1b47b50879f6f3b594ea412239ef2dfd20c69acf63e8fe2fab3ec62ac8764d` (committed
here; 128 lines, all cubes). Shard 2 = lines with 0-based index i % 4 == 2: 32 cubes.

## Method (`scripts/shard.py`)
Each node: CNF + cube units, `cadical --lrat --binary=false -t 300`; every UNSAT proof checked with
`lrat-check` against that exact CNF, then deleted. A node over 300 s was split with
`march_cu -d 6` on CNF + cube, and its children (parent + child literals) queued. For every split
a gap check also ran: CNF + parent units + one clause blocking each child cube was UNSAT, LRAT
VERIFIED. That check shows the children cover the parent. `leaves.jsonl` holds every leaf and
split record and is also the resume state. `scripts/shard_check.py` re-checks coverage: each
root is a VERIFIED UNSAT leaf, or a split whose children form a complete binary partition with
every child closed (`logs/shard_check.json`).

## Result
- 32/32 shard cubes closed; 0 open; 0 SAT.
- 284 leaves, all UNSAT with lrat-check VERIFIED (100% LRAT coverage of leaves).
- 4 splits, each into 64 sub-cubes with 0 march-refuted leaves. Root 78 split at depths 7, 13
  and 19; root 94 split at depth 7. All 4 partitions passed the tree check and all 4 gap checks
  were VERIFIED. Leaf depths were 7, 13, 19 and 25.
- Total leaf solve time was 7,028 s of CPU on 4 workers; the longest leaf took 279 s.

Claim, scoped as `plan/es7_critique.md` item 4 requires: "CNF hm33k7.sub.cnf (sha above) together
with any of the 32 shard-2 cubes is UNSAT, LRAT-checked leaf by leaf." This is not a theorem. The
encoding (signotope axioms, cap/cup auxiliaries, mirror identification, hull projective step) is
validated only by tests, not formally verified. It covers only shard 2. Sub-case (i) is closed by
this CNF only when all 4 shards close.
