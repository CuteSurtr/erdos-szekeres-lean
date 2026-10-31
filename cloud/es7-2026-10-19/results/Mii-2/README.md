# Task Mii-2: shard 2 of 8, mirror-symmetric 33-point instance, axis point interior (sub-case (ii))

**Result: shard not closed.** 9 of the 16 shard cubes are fully closed. The closed weight is
19/32 = 0.59375 of the shard. Every closed leaf is UNSAT with an LRAT proof that `lrat-check`
VERIFIED. No leaf was SAT, so there was nothing to decode or realize. Nothing here is a theorem:
the UNSAT claims are about one CNF (`m33k7int.sub.cnf`), whose encoding is tested but not
formally verified (`plan/es7_critique.md` item 4).

## Where it ran

Cloud container `vm` (`env.txt`): Linux 6.18.44 x86_64, 4 cores, 15 GB RAM, no swap. Wall time
was 02:36 to 06:12 UTC on 20 Oct 2026, with no restarts. During solving, 4 workers each ran
one CaDiCaL plus one streaming lrat-check.

## Tools (built from source; see `logs/provenance.txt`)

| tool | repository | commit |
|---|---|---|
| CaDiCaL 3.0.1 | arminbiere/cadical | c60730422e758ef1cebe7aeddf2dda31c996bf04 |
| drat-trim / lrat-check | marijnheule/drat-trim | 2e3b2dc0ecf938addbd779d42877b6ed69d9a985 |
| march_cu | marijnheule/CnC | 705b60c6491ef2b61988b3ce6ac674be1b90571d (`CFLAGS="-O3 -fcommon"`) |

## CNF

`m33k7int.sub.cnf` was regenerated with `../C/scripts/make_cnfs.sh` (`gen_etv.py` +
`mirgen.py --interior --yflip-unit`): `p cnf 47002 515121`, 2,736 orbit representatives.

- sha256 `69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d`
- `results/C` and `results/C2` record no sha256. Their variable, clause and orbit counts match
  (47,002 / 515,121 / 2,736).
- The same sha256 is recorded by sibling shards Mii-0, 1, 3, 4, 5, 6 and 7, and by Mi-0 and Mi-1.

## Validation and controls (passed)

- `logs/validate_report.json` (`../C/scripts/validate.py`, 1,000 sets, seed 1):
  - Orientation-only clauses: 1000/1000 for m33k7 and 500/500 for each of the other three CNFs.
  - Interior clause matches the geometry: 1000/1000.
  - Mirror identity: 0 violations. Projective map: 0 mismatches.
  - UNSAT iff 7-gon: 200/200. Hull frame UNSAT: 100/100.
  - Small-k equivalence: 2000/2000 on all 7 rows.
  - The figures match `../C/README.md` exactly, including the minimum 7-gon count, 25,411.
- `logs/part1_controls.log` (`../C/scripts/controls.sh`):
  - m8k5 is SAT.
  - m9k5, hm9k5, m9k5.sub, m17k6(.sub) and hm17k6(.sub) are UNSAT, each with LRAT VERIFIED.
  - The positive control at k = 7 holds: m32k7 and m32k7.sub are SAT under the classical mirror
    32-set.
- `scripts/verify_sat.py` (SAT-leaf checker) was tested on an m11k6 model. It found a signotope
  with 0 mirror violations, an interior axis point, and largest convex subset 5 (< 6), by two
  methods.

## Cubes (shard definition, unchanged)

`march_cu m33k7int.sub.cnf -d 7 -o cubes.icnf` (3 min 40 s):

- **128 cubes, 0 refuted leaves**; all cubes have depth 7.
- sha256 of `cubes.icnf`: `cb32d049e5e4249fd5b57c3ca900feb602ff444fde0873c3fe296fbaaacc8244`
  (copy in `logs/cubes_d7.icnf`). It matches the cube hashes recorded by Mii-0, 4, 6 and 7.
- Shard 2 is the cubes at 0-based line indices i with i mod 8 = 2: 2, 10, 18, …, 122 (16 cubes).

## Method (`scripts/shard.py`)

1. Each job is the CNF plus the cube literals as unit clauses, solved with
   `cadical --lrat --binary=false -t 300`.
2. The proof streams through a FIFO into `lrat-check`, which checks it against that same CNF, so
   no proof file is stored.
3. A leaf counts as closed only when the solver reports `s UNSATISFIABLE` and lrat-check prints
   `c VERIFIED`. lrat-check prints that only after it has checked a derivation of the empty
   clause.
4. A cube that times out is split with `march_cu <CNF+cube> -d 6`, and every child is solved the
   same way.
   - march_cu writes its look-ahead-refuted leaves to the cube file as well, so those are also
     solved with LRAT.
   - Each split was checked to be a complete binary decision tree.
   - Splits are recorded in `splits.jsonl`, and the run is resumable.
5. `scripts/status.py` recomputes the exact closed weight. It confirms that under every root, the
   closed leaves plus the open leaves form a complete binary tree.

## Results (`logs/status_final.json`, `leaves.jsonl`)

| quantity | value |
|---|---|
| shard root cubes | 16 |
| roots fully closed | **9** (indices 2, 10, 18, 26, 34, 42, 50, 58, 66) |
| roots partly closed | 1 (index 82: 32 of 64 children closed, weight 1/2) |
| roots open | 6 (indices 74, 90, 98, 106, 114, 122; split, 0 of 64 children done) |
| closed leaves | **545**, all UNSAT + LRAT VERIFIED (100 % LRAT coverage) |
| UNSAT without VERIFIED | 0 |
| SAT leaves | **0** |
| open leaves | 416 (all depth 13, never attempted) |
| closed weight of shard | **19/32 = 0.59375** |

Timing:

- Root 50 closed directly in 152 s.
- The other 15 roots hit the 300 s limit. Each was split into 64 depth-13 children; the
  march_cu splits took 356–646 s.
- No depth-13 child timed out. Their solve times have a median of about 60 s and a maximum of
  240 s.
- The total solve wall time over all leaves is about 36,100 s.
- The 416 open leaves were simply not reached before the time budget ran out. At the observed
  rate they need about 7 more core-hours.

## Is the shard closed?

**No.** 13/32 of the shard's weight is still open. No SAT leaf was found in the closed part, and
the open part has not been searched.

## Files

- `env.txt`: machine record.
- `leaves.jsonl`: one line per finished leaf (root index, cube, status, solve time, lrat).
- `splits.jsonl`: one line per split, with its children.
- `sat/`: empty, since there were no SAT leaves.
- `logs/`:
  - `provenance.txt` (tools, CNF and cube hashes), `make_cnfs.log`, `march_d7.log`, `cubes_d7.icnf`
  - `validate_report.json`, `part1_controls.log`
  - `run.log`, `status_final.json`
- `scripts/`: `shard.py` (driver), `status.py` (weights and tree check), `verify_sat.py` (SAT
  decoder and brute-force checker).
- No CNF or proof files are committed.

To resume:

```
python3 scripts/shard.py m33k7int.sub.cnf logs/cubes_d7.icnf 2 8 <bindir> <workdir> . 4 300 6
```

It skips finished leaves and reuses the recorded splits.
