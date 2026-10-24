# Task A2: abstract neighbourhood search anchored on realizable sets (20 October 2026)

**Outcome: no SAT answer at 33 points, so nothing to decode or realize.** Every one of the
411,693 neighbourhood instances that finished (r = 3, 4, 5, 6 and a partial r = 7) was
UNSAT. These are solver answers about single CNFs. They are not theorems. A sample of 80 was
re-checked independently with DRAT proofs, and nothing else was proof-checked.

## Where it ran (`env.txt`)

- **Machine.** This was a cloud VM (a managed remote Claude Code session), not the local laptop.
  `uname`: Linux vm 6.18.44-fc-v139 x86_64. It has 4 cores, 15 GB RAM and no swap; the hostname is
  `vm`. The run started at 2026-10-20 00:21 UTC and stopped at about 03:40 UTC.
- **Load.** Nothing else ran on the VM. Every pool used 4 ext_solve workers. For the last ~15
  minutes of r = 7 there were 5, with 2 helper processes running the tails of 2 lagging workers'
  job lists in reverse; answers are de-duplicated per (label, tag).
- **Solver.** CaDiCaL 3.0.1, commit `c6073042` from GitHub (the same commit as task A). It was
  built as a library and a binary, with option `lucky=0`.
- **Proof checker.** drat-trim, commit `2e3b2dc`, built from GitHub.
- **Base CNFs.** These are `tools/trackB/gen_cnf.py 33 7` (47,002 variables, 679,038 clauses) and
  `gen_cnf.py 32 7` for the controls. They are identical in size to task A's.
- **Tester.** Task A's `ext_solve.cpp`, unchanged. It loads the base CNF once and fixes every kept
  triple through assumptions.

## 1. Rebuild and control C1 (`data/controls_A_rerun.json`)

The 32-point inputs were rebuilt from A's scripts on this machine (`convert.py`,
`make_extra_sets.py`). The output matched A's meta exactly:
- 8,537 pool sets, 1,492 of them sheared;
- AlphaEvolve 33-point set: exactly one convex 7-gon, at JSON indices {14, 15, 17, 20, 23, 25, 32};
- 273 near-full sets, each with exactly one convex 7-gon.

Then A's full `controls.py` was re-run. **It passed**, with the same numbers as task A:

| Control | Result |
|---|---|
| C1, required: delete one point q from 30 pool sets, then re-insert at p = 1..32 | own position SAT in **30/30**; 369 SAT and 591 UNSAT answers; all 369 SAT models pass brute force |
| C2: all 8,544 known heptagon-free 32-point signotopes, every triple fixed | 8,544/8,544 SAT |
| C3: 274 signotopes with a convex 7-gon, every triple fixed | 274/274 UNSAT |
| C3: 3 AlphaEvolve 32-point sets that keep the 7-gon, 33 positions each | 99/99 UNSAT |
| C3: pool set 0 with triple (1,2,4) flipped | brute_kgon finds 1 axiom violation; UNSAT |

**New neighbourhood positive controls** (`data/ctl_nb_*.json`). These use the 32-point CNF:
delete r points, then re-insert exactly r points with the `free` placement generator below. The
original placement is always among the placements tried, so every deletion set must give at least
one SAT answer, and every SAT model must pass brute force.

| Control | Bases | Deletion sets with a SAT answer | Answers (SAT) | SAT models passing brute force |
|---|---|---|---|---|
| r = 3; win, geo and rand | 67 (pool + AE) | **201 / 201** | 8,939 (6,361) | 6,361 / 6,361 |
| r = 5; win, geo and rand | 67 (pool + AE) | **201 / 201** | 11,770 (9,040) | 9,040 / 9,040 |
| r = 4; hv and hnear | 274 (near-miss) | **533 / 533** | 10,550 (9,939) | 9,939 / 9,939 |

"Passing brute force" means three things: the kept triples are exactly as assumed, the Python
signotope axiom check passes, and `brute_kgon` finds 0 violations and 0 convex 7-subsets.

## 2. Design (`scripts/make_bases.py`, `scripts/nbhd2.py`)

**Bases** (`data/bases.jsonl.gz`, index in `data/bases_index.tsv`). There are 341 heptagon-free
32-point sets, each with an exact integer signotope:
- 60 pool sets: 6 seeded-random sets from each of the 10 source tags (A7n, A7n2c, A7n2d, A7r,
  A7r2a, A7r2b, A7sv, A7sv2, A7w and A7w2e). They avoid A's `sample107.txt`, so these bases are
  new.
- The 7 AlphaEvolve-derived 32-point sets (a heptagon vertex deleted).
- 274 near-miss sets. Each of the 273 `nearfull_p2c/p2d` 33-point sets and AlphaEvolve's 33-point
  set loses one seeded-random vertex of its unique convex 7-gon. Every one of the 274 remainders
  was re-checked by brute_kgon: 0 convex 7-subsets and 0 violations.
- For each near-miss base we record the 6 surviving heptagon vertices and the deleted vertex
  (in the base's own sheared frame where a shear was needed). An exact test confirmed that these
  7 points are in convex position for all 274 bases.

**Deletion kinds** (r points deleted, one deletion set per kind per base, de-duplicated across
kinds):
- `win`: r consecutive points in x-order.
- `geo`: a random point and its r − 1 nearest points.
- `rand`: r uniformly random points.
- `hv` (near-miss bases only, r ≤ 6): r of the 6 surviving heptagon vertices.
- `hnear` (near-miss bases only): the r points nearest to the deleted heptagon vertex. This
  usually includes heptagon vertices. Where it coincided with the `hv` set, it was dropped as a
  duplicate, which is why its count is below 274.

**Insertion of r + 1 new points.** The gap e is the number of kept points to a new point's left.
- `slot`: task A's scheme. One new point goes in each deleted point's gap, plus one extra point
  in every gap e = 0..32 − r, giving 33 − r placements.
- `free` (the freer insertion order): every multiset of r + 1 gaps inside the window from
  (min deleted gap − 2) to (max deleted gap + 2). The new points' x-ranks are free in that window,
  and several new points may share a gap; they are still ordered by x, and their mutual
  orientations are free. If there are more multisets than `cap`, a seeded random sample of `cap`
  is taken. Placements that `slot` already tried are skipped.
  - cap = 100 / 60 / 30 / 20 for r = 3 / 4 / 5 / 6.
  - The window was enumerated completely for at least 821 / 181 / 78 / 0 of the deletion sets at
    r = 3 / 4 / 5 / 6.

Conflict limit: 300,000 per call for r ≤ 5 and 200,000 for r ≥ 6. It was never reached
(UNKNOWN = 0 everywhere).

## 3. Results (`data/m_r*.json`, raw answer lines in `data/raw/m_r*_R.txt.gz`)

Totals per run, then per deletion kind and placement mode, then per base source. The r = 7 run was stopped by the time budget with 5,208 of its 5,226 jobs answered; the other 18 were never answered and are not counted. Its wall time includes the helper processes.

| Run | r | Bases | Deletion sets | Answers | SAT | UNSAT | UNKNOWN | Conflicts mean / max | ms mean / max | Wall s |
|---|---|---|---|---|---|---|---|---|---|---|
| m_r3 | 3 | 341 | 1,543 | 165,533 | 0 | 165,533 | 0 | 8.5 / 491 | 13.5 / 6,429.7 | 579.0 |
| m_r4 | 4 | 341 | 1,538 | 132,952 | 0 | 132,952 | 0 | 28.3 / 1,299 | 31.9 / 6,639.0 | 1094.3 |
| m_r5 | 5 | 341 | 1,509 | 87,132 | 0 | 87,132 | 0 | 129.7 / 6,651 | 100.9 / 8,990.5 | 2390.5 |
| m_r6a | 6 | 67 | 201 | 9,447 | 0 | 9,447 | 0 | 473.0 / 16,092 | 357.8 / 14,897.9 | 1099.7 |
| m_r6b | 6 | 274 | 423 | 11,421 | 0 | 11,421 | 0 | 277.3 / 14,097 | 190.8 / 10,039.9 | 613.3 |
| m_r7 | 7 | 67 | 201 | 5,208 | 0 | 5,208 | 0 | 2972.0 / 158,356 | 2686.9 / 139,642.2 | 3880 |

| Run | Kind | Mode | Deletion sets | Answers | SAT | UNSAT | UNKNOWN | Conflicts mean / max |
|---|---|---|---|---|---|---|---|---|
| m_r3 | geo | free | 341 | 24,171 | 0 | 24,171 | 0 | 9.9 / 247 |
| m_r3 | geo | slot | 341 | 10,230 | 0 | 10,230 | 0 | 7.4 / 491 |
| m_r3 | hnear | free | 246 | 17,394 | 0 | 17,394 | 0 | 7.1 / 108 |
| m_r3 | hnear | slot | 246 | 7,380 | 0 | 7,380 | 0 | 5.8 / 96 |
| m_r3 | hv | free | 274 | 23,621 | 0 | 23,621 | 0 | 7.9 / 196 |
| m_r3 | hv | slot | 274 | 8,220 | 0 | 8,220 | 0 | 5.7 / 96 |
| m_r3 | rand | free | 341 | 33,889 | 0 | 33,889 | 0 | 7.1 / 241 |
| m_r3 | rand | slot | 341 | 10,230 | 0 | 10,230 | 0 | 5.5 / 161 |
| m_r3 | win | free | 341 | 20,168 | 0 | 20,168 | 0 | 14.2 / 240 |
| m_r3 | win | slot | 341 | 10,230 | 0 | 10,230 | 0 | 11.0 / 375 |
| m_r4 | geo | free | 341 | 19,602 | 0 | 19,602 | 0 | 34.6 / 926 |
| m_r4 | geo | slot | 341 | 9,889 | 0 | 9,889 | 0 | 26.3 / 1,299 |
| m_r4 | hnear | free | 241 | 13,362 | 0 | 13,362 | 0 | 23.1 / 457 |
| m_r4 | hnear | slot | 241 | 6,989 | 0 | 6,989 | 0 | 13.6 / 431 |
| m_r4 | hv | free | 274 | 15,682 | 0 | 15,682 | 0 | 23.6 / 384 |
| m_r4 | hv | slot | 274 | 7,946 | 0 | 7,946 | 0 | 11.8 / 498 |
| m_r4 | rand | free | 341 | 20,460 | 0 | 20,460 | 0 | 15.6 / 607 |
| m_r4 | rand | slot | 341 | 9,889 | 0 | 9,889 | 0 | 10.9 / 378 |
| m_r4 | win | free | 341 | 19,244 | 0 | 19,244 | 0 | 55.0 / 923 |
| m_r4 | win | slot | 341 | 9,889 | 0 | 9,889 | 0 | 47.7 / 1,296 |
| m_r5 | geo | free | 341 | 10,155 | 0 | 10,155 | 0 | 151.9 / 6,651 |
| m_r5 | geo | slot | 341 | 9,548 | 0 | 9,548 | 0 | 119.6 / 5,754 |
| m_r5 | hnear | free | 212 | 6,280 | 0 | 6,280 | 0 | 148.3 / 6,328 |
| m_r5 | hnear | slot | 212 | 5,936 | 0 | 5,936 | 0 | 75.1 / 3,018 |
| m_r5 | hv | free | 274 | 8,115 | 0 | 8,115 | 0 | 179.2 / 4,706 |
| m_r5 | hv | slot | 274 | 7,672 | 0 | 7,672 | 0 | 79.0 / 2,484 |
| m_r5 | rand | free | 341 | 10,230 | 0 | 10,230 | 0 | 41.3 / 1,515 |
| m_r5 | rand | slot | 341 | 9,548 | 0 | 9,548 | 0 | 33.2 / 1,578 |
| m_r5 | win | free | 341 | 10,100 | 0 | 10,100 | 0 | 241.6 / 3,919 |
| m_r5 | win | slot | 341 | 9,548 | 0 | 9,548 | 0 | 208.9 / 6,479 |
| m_r6a | geo | free | 67 | 1,340 | 0 | 1,340 | 0 | 598.1 / 15,757 |
| m_r6a | geo | slot | 67 | 1,809 | 0 | 1,809 | 0 | 447.1 / 10,650 |
| m_r6a | rand | free | 67 | 1,340 | 0 | 1,340 | 0 | 61.5 / 3,720 |
| m_r6a | rand | slot | 67 | 1,809 | 0 | 1,809 | 0 | 71.2 / 1,847 |
| m_r6a | win | free | 67 | 1,340 | 0 | 1,340 | 0 | 893.0 / 12,351 |
| m_r6a | win | slot | 67 | 1,809 | 0 | 1,809 | 0 | 802.0 / 16,092 |
| m_r6b | hnear | slot | 149 | 4,023 | 0 | 4,023 | 0 | 420.2 / 14,097 |
| m_r6b | hv | slot | 274 | 7,398 | 0 | 7,398 | 0 | 199.6 / 7,571 |
| m_r7 | geo | slot | 67 | 1,742 | 0 | 1,742 | 0 | 3777.0 / 90,043 |
| m_r7 | rand | slot | 67 | 1,742 | 0 | 1,742 | 0 | 132.0 / 4,989 |
| m_r7 | win | slot | 67 | 1,724 | 0 | 1,724 | 0 | 5028.3 / 158,356 |

| Run | Source group | Deletion sets | Answers | SAT | UNKNOWN |
|---|---|---|---|---|---|
| m_r3 | A7n2c | 18 | 1,991 | 0 | 0 |
| m_r3 | A7n2d | 18 | 1,815 | 0 | 0 |
| m_r3 | A7n | 18 | 1,922 | 0 | 0 |
| m_r3 | A7r2a | 18 | 1,919 | 0 | 0 |
| m_r3 | A7r2b | 18 | 1,902 | 0 | 0 |
| m_r3 | A7r | 18 | 2,060 | 0 | 0 |
| m_r3 | A7sv2 | 18 | 1,955 | 0 | 0 |
| m_r3 | A7sv | 18 | 2,025 | 0 | 0 |
| m_r3 | A7w2e | 18 | 1,833 | 0 | 0 |
| m_r3 | A7w | 18 | 1,833 | 0 | 0 |
| m_r3 | AEdel | 21 | 2,345 | 0 | 0 |
| m_r3 | NM_AE33 | 5 | 527 | 0 | 0 |
| m_r3 | NM_p2c | 718 | 77,151 | 0 | 0 |
| m_r3 | NM_p2d | 619 | 66,255 | 0 | 0 |
| m_r4 | A7n2c | 18 | 1,594 | 0 | 0 |
| m_r4 | A7n2d | 18 | 1,594 | 0 | 0 |
| m_r4 | A7n | 18 | 1,594 | 0 | 0 |
| m_r4 | A7r2a | 18 | 1,586 | 0 | 0 |
| m_r4 | A7r2b | 18 | 1,502 | 0 | 0 |
| m_r4 | A7r | 18 | 1,560 | 0 | 0 |
| m_r4 | A7sv2 | 18 | 1,544 | 0 | 0 |
| m_r4 | A7sv | 18 | 1,602 | 0 | 0 |
| m_r4 | A7w2e | 18 | 1,602 | 0 | 0 |
| m_r4 | A7w | 18 | 1,594 | 0 | 0 |
| m_r4 | AEdel | 21 | 1,861 | 0 | 0 |
| m_r4 | NM_AE33 | 5 | 445 | 0 | 0 |
| m_r4 | NM_p2c | 715 | 61,741 | 0 | 0 |
| m_r4 | NM_p2d | 617 | 53,133 | 0 | 0 |
| m_r5 | A7n2c | 18 | 1,044 | 0 | 0 |
| m_r5 | A7n2d | 18 | 1,044 | 0 | 0 |
| m_r5 | A7n | 18 | 1,044 | 0 | 0 |
| m_r5 | A7r2a | 18 | 1,034 | 0 | 0 |
| m_r5 | A7r2b | 18 | 1,034 | 0 | 0 |
| m_r5 | A7r | 18 | 1,044 | 0 | 0 |
| m_r5 | A7sv2 | 18 | 1,044 | 0 | 0 |
| m_r5 | A7sv | 18 | 1,044 | 0 | 0 |
| m_r5 | A7w2e | 18 | 1,039 | 0 | 0 |
| m_r5 | A7w | 18 | 1,044 | 0 | 0 |
| m_r5 | AEdel | 21 | 1,213 | 0 | 0 |
| m_r5 | NM_AE33 | 4 | 232 | 0 | 0 |
| m_r5 | NM_p2c | 709 | 40,947 | 0 | 0 |
| m_r5 | NM_p2d | 595 | 34,325 | 0 | 0 |
| m_r6a | A7n2c | 18 | 846 | 0 | 0 |
| m_r6a | A7n2d | 18 | 846 | 0 | 0 |
| m_r6a | A7n | 18 | 846 | 0 | 0 |
| m_r6a | A7r2a | 18 | 846 | 0 | 0 |
| m_r6a | A7r2b | 18 | 846 | 0 | 0 |
| m_r6a | A7r | 18 | 846 | 0 | 0 |
| m_r6a | A7sv2 | 18 | 846 | 0 | 0 |
| m_r6a | A7sv | 18 | 846 | 0 | 0 |
| m_r6a | A7w2e | 18 | 846 | 0 | 0 |
| m_r6a | A7w | 18 | 846 | 0 | 0 |
| m_r6a | AEdel | 21 | 987 | 0 | 0 |
| m_r6b | NM_AE33 | 2 | 54 | 0 | 0 |
| m_r6b | NM_p2c | 227 | 6,129 | 0 | 0 |
| m_r6b | NM_p2d | 194 | 5,238 | 0 | 0 |
| m_r7 | A7n2c | 18 | 468 | 0 | 0 |
| m_r7 | A7n2d | 18 | 468 | 0 | 0 |
| m_r7 | A7n | 18 | 468 | 0 | 0 |
| m_r7 | A7r2a | 18 | 450 | 0 | 0 |
| m_r7 | A7r2b | 18 | 468 | 0 | 0 |
| m_r7 | A7r | 18 | 468 | 0 | 0 |
| m_r7 | A7sv2 | 18 | 468 | 0 | 0 |
| m_r7 | A7sv | 18 | 468 | 0 | 0 |
| m_r7 | A7w2e | 18 | 468 | 0 | 0 |
| m_r7 | A7w | 18 | 468 | 0 | 0 |
| m_r7 | AEdel | 21 | 546 | 0 | 0 |

**Scaling with r** (mean conflicts per call; win and geo deletions cost more than rand):
- 8.5 at r = 3;
- 28 at r = 4;
- 130 at r = 5;
- 280–470 at r = 6;
- about 3,000 at r = 7 (win 5,000, rand 130).

The largest single call was 158,356 conflicts (r = 7, win), which is close to the 200,000 limit; a larger r will need a higher limit or cubing.

Every answer was UNSAT. No answer was UNKNOWN, and no SAT model came up at any r, kind,
placement mode or source.

## 4. Independent re-check (`scripts/cert2.py`, `data/cert_drat_sample.jsonl`)

80 random jobs were re-checked: 20 each from r = 3, 4 and 5, and 10 each from the two r = 6 runs.
For each job:
- the kept signotope was rebuilt from `bases.jsonl` and the deleted set in the label, not from the
  job file;
- the index map was rebuilt from the tag's new indices and compared with the job's map;
- a stand-alone CNF was written (the base CNF plus unit clauses) and solved by the CaDiCaL binary
  with a DRAT proof, which drat-trim then checked.

**80/80:** every map matched, every job was UNSAT, and every proof was DRAT-VERIFIED.

## 5. Realization (`scripts/realize2.py`)

**No SAT model came up at 33 points, so nothing was decoded or realized.** The pipeline is ready:
1. `summ2.py` decodes and brute-force checks every W model.
2. `realize2.py` runs task A's near-original LP/nonlinear realizer.
3. If that fails, it runs `tools/realizer/realize.py`, seeded with the base's coordinates.
4. Any candidate is re-checked exactly: every labelled orientation is recomputed with integers,
   general position is checked, and brute_kgon is run on the recomputed signotope.

**A bug was caught and fixed in calibration.** `tools/realizer`'s LP method sends one point to
infinity, so its output is a correct *labelled* realization that is not in x-order. The first
version of the check compared x-sorted signotopes and wrongly rejected it. The check now compares
labelled orientations.

**Calibration: 1/12.** The calibration set was 12 random r = 3 control models (32 points),
realized under full CPU contention with a 60 s budget each. These models are not guaranteed to be
realizable, so this is weak calibration. Task A's 24/30 and 107/369 figures for the same stage-1
code stand. A "not realized" verdict would have been weak evidence.

## Not tested

- r = 7 is partial (pool and AE bases only, win/geo/rand, slot placements only); see the table.
  r ≥ 8 was not run.
- Free placement is a capped random sample for most deletion sets with r ≥ 4. At r = 6 the near-miss
  bases got slot placements only, and only the hv/hnear kinds. Insertion outside the ±2-gap window
  was tested only through slot mode's single extra point.
- Only one deletion set per kind per base (per-kind 1), and only one heptagon vertex deleted per
  near-miss set.
- Only the original sweep direction was used (no rotated signotopes), and the 168 31-point starts
  were not covered.
- Certification: only the 80 DRAT samples are proof-checked. The assumption-based encoding is not
  verified in Lean.

## Files

- `scripts/`: `make_bases.py`, `nbhd2.py` (deletion and placement generator, and driver),
  `summ2.py` (summary and model checks), `cert2.py` (DRAT sample), `realize2.py`, `tables.py`.
  They reuse `results/A/scripts/` (`ext_solve.cpp`, `run_ext.py`, `sigutil.py`,
  `realize_models.py`, `controls.py`).
- `data/`: per-run summaries (`m_r*.json`), controls, `cert_drat_sample.jsonl`,
  `realizer_calib_r3.jsonl`, bases, and raw R lines plus deletion sets (gzipped).

Reproduce from `cloud/es7-2026-10-19/`, with A's build steps in `results/A/scripts/run_all.sh`
followed by:

```
python3 results/A2/scripts/make_bases.py WORK inputs 6 2026102 WORK/bases.jsonl
python3 results/A2/scripts/nbhd2.py --wd WORK --bases WORK/bases.jsonl --r 3 --out WORK/m_r3 --cap 100 --seed 11
python3 results/A2/scripts/nbhd2.py ... --r 4 --cap 60 --seed 12;  --r 5 --cap 30 --seed 13
python3 results/A2/scripts/nbhd2.py ... --r 6 --src A7,AE --kinds win,geo,rand --cap 20 --seed 16 --climit 200000
python3 results/A2/scripts/nbhd2.py ... --r 6 --src NM --kinds hv,hnear --modes slot --seed 17 --climit 200000
python3 results/A2/scripts/nbhd2.py ... --r 7 --src A7,AE --kinds win,geo,rand --modes slot --seed 18 --climit 200000
python3 results/A2/scripts/summ2.py WORK WORK/bases.jsonl WORK/m_r3 m_r3.json models.jsonl
```

(nbhd2.py and run_ext resolve `ext_solve` and `n33k7.cnf` relative to `--wd`; the runs here used
WORK as the current directory.)
