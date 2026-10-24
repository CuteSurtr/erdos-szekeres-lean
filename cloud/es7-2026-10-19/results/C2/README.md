# Task C2: mirror-symmetric 33-point class, cloud run (20 Oct 2026)

Question: is there a set of 33 points in general position, symmetric under a reflection,
with no 7 in convex position? Such a set has exactly one point on the axis. Sub-case (i):
that point is a hull vertex. Sub-case (ii): it is interior. See `../C/README.md` for the
encodings (`hm33k7.sub.cnf` for (i), `m33k7int.sub.cnf` for (ii)).

**Nothing here is a theorem or a counterexample.** Neither sub-case was closed, and no SAT
model or 7-gon-free 33-point set was found.

## Where it ran

`env.txt`: cloud VM `vm`, Linux 6.18.44 x86_64, **4 cores**, 15 GB RAM, start 00:21:31 UTC.
The container restarted twice: about 02:53 UTC (all processes resumed from checkpoints at
02:53:49; `env.txt` records the same machine profile) and about 03:39 UTC (runs not resumed;
the remaining time went to verification). Core use: 2 CaDiCaL workers on (i), 1 on (ii),
1 annealer, plus the LRAT checker at nice 5 (oversubscribed).

Tools built from source: CaDiCaL 3.0.1 (commit c607304, 19 Jul 2026), drat-trim and
lrat-check (git head). All CNFs rebuilt with `../C/scripts/make_cnfs.sh`, and the clause and
variable counts match `../C/README.md` (`hm33k7.sub.cnf` 47,002 vars / 535,454 clauses,
`m33k7int.sub.cnf` 47,002 / 515,121).

## Controls (all passed)

- `logs/part1_controls.log`: m8k5 SAT. m9k5, hm9k5, m9k5.sub, m17k6, hm17k6, m17k6.sub and
  hm17k6.sub are UNSAT, each with an LRAT proof that lrat-check VERIFIED. The classical
  mirror 32-point set has 0 mirror-identity violations, and m32k7 and m32k7.sub are SAT under
  its orientations (positive control at k = 7).
- `logs/part1_k6_extra.log`: m11k6 and hm11k6 SAT (positive controls with one axis point;
  a mirror hexagon-free set has at most 5 pairs, see `../C/README.md`); m16k6 and hm16k6 UNSAT.
- `logs/part1_validate.log` (`validate.py`, **seed 2**, independent of the local seed 1):
  1,000 random exact mirror 33-sets. All satisfy the orientation-only clauses of all four CNFs
  in their frames. The interior clause matches the geometry 1000/1000. The projective map has
  0 orientation mismatches. UNSAT iff 7-gon 200/200; hull frame UNSAT 100/100. Small-k
  equivalence agrees 2000/2000 on all 7 rows (N = 7, 8, 9, 11; both frames).

The encodings remain **unverified** in the sense of `plan/es7_critique.md` item 4. They are
tested, not proved.

## Abstract side: cube-and-conquer (`../C/scripts/cnc2.py`, `cncw.cpp`)

Both runs **resumed** from the local run's checkpoints (`../C/logs/cnc_*/state.json`; the
regenerated CNFs have identical numbering). Settings: shallowest-first queue, exact Fraction
weights, `CNCW_CHAIN=1`, base 3000 conflicts, growth 1.05.

Open weight (= 1 − exact closed weight) every 30 min (`logs/cnc_progress_30min.jsonl`):

| UTC | (i) hull: open weight | open cubes (min depth) | (ii) interior: open weight | open cubes (min depth) |
|---|---|---|---|---|
| 00:24 | 0.2148 | 469 (11) | 0.6680 | 319 (8) |
| 00:54 | 0.0901 | 562 (12) | 0.5820 | 469 (9) |
| 01:24 | 0.0382 | 677 (13) | 0.4667 | 621 (10) |
| 01:54 | 0.0211 | 769 (14) | 0.4434 | 768 (10) |
| 02:24 | 0.0124 | 837 (15) | 0.4203 | 918 (10) |
| 02:54 | 0.0067 | 863 (16) | 0.3837 | 1060 (11) |
| 03:24 | 0.0042 | 958 (16) | 0.3792 | 1216 (11) |
| 03:39 (final) | **0.002722** | 1048 (17) | **0.3640** | 1340 (11) |

Exact final closed weights are in `logs/cnc_*/latest.json`. (i):
5178165469934777337811902522195967 / 2^112. (ii): 43706543615 / 2^36.

**Convergence assessment (honest):** neither sub-case is near closure.
- (i): the open weight shrank by a factor of about 0.42 per 30 min at first, but that factor
  has drifted up to about 0.65. Meanwhile the open cube count keeps growing (469 → 1048) and
  cubes get deeper. A geometric fit with a worsening ratio does not reach 0 in any predictable
  time. Closing (i) would need many more core-hours, likely with better cubing (e.g. march
  cubes off-line) rather than more of the same.
- (ii): on one core it went from 0.668 to 0.364 in 3.3 h, with the per-30-min factor now at
  0.96–0.99. It is far from closure.

**Coverage:** `scripts/check_tree2.py` confirms that the closed cubes plus the open cubes form
a complete binary partition of the root for both runs (`logs/check_tree2_*.json`).
`../C/scripts/check_tree.py` passes for (ii) but reports false for (i). After the 02:53
resume, some cubes processed after the last checkpoint were re-split on a different variable,
which leaves stale closed entries that the single-variable rule rejects. check_tree2 accepts
any branching variable whose two children are both covered, which is still a sound partition.

**LRAT:** every distinct closed cube, those inherited from the local run included, was
re-solved from scratch with `cadical --lrat`, and the proof was checked with `lrat-check`
against CNF + cube units. Results are in `logs/cnc_*/lrat_*.jsonl`; see "Final LRAT tally"
below. No cube came back as anything other than UNSAT + VERIFIED. This certifies "CNF + cube
is UNSAT" for each closed cube only. Since the open cubes remain, neither sub-case CNF is
certified UNSAT.

No SAT model appeared in either run, so there was nothing to realize with `tools/realizer/`.

## Realizable side: mirror annealer (`../C/scripts/mirann.c`, `scripts/anneal_loop.sh`)

One core; alternating runs of 1,000,000 iterations each, T 0.5 → 0.01, log-energy
acceptance, energy = exact number of convex 7-gons (integer orientation arithmetic).

- **33 points (16 pairs + 1 axis point)**: 31 runs (`logs/anneal/m33_K7_P16_A1.log`). Minimum
  energy reached: **1** (21 runs), 2 (5 runs), 3 (5 runs). **No run reached 0.** The final
  best state of each of 26 runs was re-verified by `exact_tools.py verify` (brute force over
  all 7-subsets with `brute_kgon`): all are in general position, mirror-symmetric, with one
  axis point and convex 7-gon counts exactly as the annealer reported (17 × 1, 5 × 2, 4 × 3;
  `logs/anneal33_best_exact_verify.jsonl`, `sets/anneal33_best_states.txt`). Whenever the 32
  pair points alone were heptagon-free, the annealer scanned the axis exactly; the minimum
  found was 1.
- **32 points (16 pairs, no axis point)**: 31 runs; 24 reached a heptagon-free mirror 32-set
  (`sets/heptagon_free_mirror32_found.txt`). All 24 were brute-force verified (general
  position, mirror-symmetric, 0 convex 7-gons). **Exact axis scan** (every interval between
  consecutive intersections of lines with the axis, rational arithmetic, independent Python
  scan in `../C/scripts/exact_tools.py`, matching mirann and brute-force rechecked at the best
  t): the minimum number of 7-gons after adding an axis point is **1** for 9 sets, then 18, 36,
  49, … up to 961; there are **0 zero intervals**
  (`logs/axis_scan_new_heptfree32_exact.jsonl`).
- The 21 heptagon-free mirror 32-sets from the local run were re-scanned the same way:
  minimum 1 (5 sets), 0 zero intervals (`logs/rescan_prev_heptfree32_*`).
- The local near-miss `../C/sets/near_miss_mirror33_one_heptagon.txt` was re-verified:
  general position, mirror-symmetric, 1 axis point, exactly 1 convex 7-gon.

So the realizable side repeatedly gets to exactly one convex heptagon and no further.

## Candidates

None. No SAT model, no 7-gon-free 33-point set, and no axis interval with zero 7-gons.

## Files

- `scripts/`: `anneal_loop.sh`, `lrat_loop.sh`, `reconcile.py` (finds closed cubes without a
  VERIFIED record), `check_tree2.py`, `collect.sh`. Everything else is reused from `../C/scripts/`.
- `logs/cnc_i_hull/`, `logs/cnc_ii_interior/`: `cnc.log`, `latest.json`, `state.json` (open
  cubes), `closed.txt`, and the LRAT records.
- No CNF or proof files are committed.

## Final LRAT tally

Output of `scripts/reconcile.py` on all LRAT records at 04:03 UTC:

| run | distinct closed cubes | LRAT VERIFIED | unchecked | other outcomes |
|---|---|---|---|---|
| (i) hull | 4,535 | 4,535 | 0 | 0 |
| (ii) interior | 749 | 749 | 0 | 0 |

That is 5,289 proof checks in all. The longest from-scratch solve took 57.9 s, the largest
proof was 22 MB, and the solves took 3.1 h of CPU in total. Proofs were deleted after
checking. Every closed cube is certified in the sense that CNF + cube is UNSAT by a checked
LRAT proof. The open cubes (1,048 for (i), 1,340 for (ii); listed in `state.json`) are
unresolved, so **neither sub-case is certified**.
