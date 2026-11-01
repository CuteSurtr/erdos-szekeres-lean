# C2P: the parallelogram cases of the central 34-point formula (wave of 2026-10-31)

**What is open.** By `results/C2C34`, a centrally symmetric set of 34 points in general position with no convex 7-gon
would have a parallelogram hull. Its 8 canonical cases P1..P8 are open.

**This wave.**
- Each case is split at the second convex layer into 560 subcases (`results/C2C34/l2cubes.py`).
- A reflection pairs the subcases up, leaving 287 representatives per case.
- One CaDiCaL lane on each of 42 cloud machines, and one on a Mac, solved the representatives in order: P8, then P7, …
- Every UNSAT proof was checked by lrat-check and cake_lpr and then deleted. The records keep the CNF sha256 and the
  proof's size and sha256.

## Results

- **Records.**
  - 484 unit records from 42 cloud machines and the Mac (`M*/out.jsonl`, `LOCAL*/out.jsonl`).
  - 436 units certified (both checkers accepted).
  - 48 gave no answer: 35 at their full cap (2,400 s for quadrilateral second layers on the cloud;
    4,280 s on the Mac), and 13 cut short by the end of the wave with a smaller cap.
  - SAT answers: 0. Proofs rejected or unchecked: 0. Other outcomes: 0.
- **Cloud timings.** One lane per 4-vCPU, 15 GB machine; solve seconds:
  - hexagonal second layers (H): 17–688 (median 272) over 370 units;
  - quadrilateral second layers (Q): 492–2319 (median 941) over 47 units;
  - covers: 765 over 1 unit.
- **Checks.** lrat-check 9–93 (median 50) s; cake_lpr 79–525 (median 294) s.
- **Proofs.** 1325 GB in all, checked and deleted. Largest solver RSS: 11.8 GB.

Per case, together with the P8 pilot of `results/C2C34` (`tools/summary.py`):

```
case  cover  reps certified/287 (Q /56, H /231)  no answer yet (not certified)
P1    no       0 ( 0 Q,   0 H)                  0: 
P2    no       0 ( 0 Q,   0 H)                  0: 
P3    no       0 ( 0 Q,   0 H)                  0: 
P4    no       0 ( 0 Q,   0 H)                  0: 
P5    no       0 ( 0 Q,   0 H)                  0: 
P6    no      10 ( 0 Q,  10 H)                  3: P6_2-7 P6_3-11 P6_9-13
P7    yes    206 (24 Q, 182 H)                  25: P7_1-10 P7_1-12 P7_1-5 P7_1-6 P7_1-8 P7_1-9 P7_2-10 P7_2-11 ...
P8    yes    266 (35 Q, 231 H)                  21: P8_1-10 P8_1-11 P8_1-12 P8_1-6 P8_1-7 P8_1-9 P8_10-15 P8_2-10 ...
total certified representatives: 482 of 2296; covers: 2 of 8; third-layer units certified: 15, third-layer covers: 1
```

**Open representatives** (pilot and this wave together; a unit that timed out and was certified later counts as certified):
  - P1: not started (cover not run, all 287 representatives open).
  - P2: not started (cover not run, all 287 representatives open).
  - P3: not started (cover not run, all 287 representatives open).
  - P4: not started (cover not run, all 287 representatives open).
  - P5: not started (cover not run, all 287 representatives open).
  - P6: cover not run; 10 of 287 representatives certified; 274 not reached; 3 cut short by the end of the wave: P6_2-7, P6_3-11, P6_9-13; 0 timed out at the full cap.
  - P7: cover certified; 206 of 287 representatives certified; 56 not reached; 10 cut short by the end of the wave: P7_2-13, P7_3-10, P7_3-12, P7_3-8-16, P7_3-9-13, P7_8-13, P7_8-16, P7_9-10, P7_9-13, P7_9-14; 15 timed out at the full cap: P7_1-10, P7_1-12, P7_1-5, P7_1-6, P7_1-8, P7_1-9, P7_2-10, P7_2-11, P7_2-8, P7_3-11, P7_3-13, P7_3-9, P7_8-14, P7_8-15, P7_9-15.
  - P8: cover certified; 266 of 287 representatives certified; 0 not reached; 0 cut short by the end of the wave; 21 timed out at the full cap: P8_1-10, P8_1-11, P8_1-12, P8_1-6, P8_1-7, P8_1-9, P8_10-15, P8_2-10, P8_2-12, P8_2-9, P8_3-10, P8_3-11, P8_3-12, P8_3-13, P8_3-9, P8_4-10, P8_4-11, P8_4-12, P8_9-14, P8_9-15, P8_9-16.

## Trust base

- **Encoding, layer split and covers.** As in `results/C2C34`: encoder reviewed, covers certified. The P_a covers
  certified in this wave are in the records (unit `P<a>_cover`).
- **Reductions — reviewed this wave** (independent adversarial review: literal-level checks, real-set checks and
  mutation tests; see `review/`).
  - **(A)** The 16 parallelogram cases reduce to the canonical 8.
  - **(B)** The reflection i → (a − i) mod 17 pairs subcases (P_a, V) and (P_a, V′), V′ = {(a − i) mod 17}.
  - The review found both sound, with 0 failures in 3 × 17,920 literal checks on the cube files and in
    17,920 + 17,920 checks on 8,960 real 34-point sets. Full clause evaluation on 1,628 real sets of small analogues
    also gave 0 failures, and the mutation tests show that the checks can fail (`review/README.md`).
  - (B) holds for real configurations only, not as a symmetry of the CNF. So the partner subcases are refuted by this
    argument, not by a solver.
- **Tools.** CaDiCaL 3.0.1, cake_lpr a36874a8 and lrat-check 2e3b2dc with the E2 patch, built from the sources vendored
  in `vendor/` (unmodified upstream files; `vendor/MANIFEST.sha256`). Six machines built from fresh clones of the
  same commits before the vendored build was added; their `tools.txt` records this.

## Subcases that need a deeper split

Some quadrilateral second layers did not close within the cap. For these, `tools/l3cubes.py` splits a subcase
(P_a, V2) at the third convex layer into 364 cubes, and the cover of that split is certified separately.
`tools/lane3.py` runs third-layer units, and `tools/mkl3.py` makes their work list.

**Third-layer pilot on P8_3-11 (Mac).**
- The cover of its 364-way third-layer split is certified: solve 274 s, both checks.
- 15 of the 364 units were run and certified, with solve times 29–211 (median 104) s.
- At that rate, the third-layer route costs about 11 Mac-hours per subcase.

**Direct runs with a long cap (Mac).**
- P8_2-11: UNSAT in 2,865 s (RSS 11.8 GB, proof 9.0 GB); lrat-check (86 s) and cake_lpr (353 s) both accepted.
- P8_1-9: UNKNOWN after 4,241 s of a 4,280 s cap (RSS 11.3 GB).

P8_2-11 was not answered within the 1,800 s cap of the pilot. It closed directly in under 48 minutes on the Mac.
P8_1-9 did not close within 71 minutes. The third-layer route projects to about 11 Mac-hours for P8_3-11. These are
different subcases, so this is only an indication, not a like-for-like comparison. Still, it suggests trying the
timed-out units directly with a cap of a few hours before splitting them further. The cloud machines are roughly half
as fast as the Mac.

## Real centrally symmetric sets in the hard region (`nestsets/`)

The hard core of the search is nested parallelograms: hull and second layer both quadrilaterals. A simulated annealing
search over real point sets (`nestsets/annealnest.c`) adds a penalty unless both layers are quadrilaterals.
`nestsets/verify_sets.py` checks every set exactly: symmetry, no collinear triple, layers, and the number of convex
7-gons and 8-gons by brute force over all subsets (`results/SYMMAX/brute.c`); see `nestsets/verify.log`.
- **30 and 32 points.** Centrally symmetric sets without a convex 7-gon whose first two layers are parallelograms
  (5 sets of 32 points, 2 of 30). The 32-point set of `results/SYM2` has a hexagonal second layer instead.
- **34 points.** A centrally symmetric set in general position with exactly 2 convex 7-gons (one antipodal pair) and
  no convex 8-gon (`central34_two_heptagons.txt`, layers 4,4,4,6,6,6,4). Convex 7-gons of a centrally symmetric set
  come in antipodal pairs, so 2 is the least nonzero count. If the central 34-point case is closed, the minimum
  number of convex 7-gons of a centrally symmetric 34-point set is exactly 2.
- **Search effort.** `annealnest` with G = 2, K = 7 and nest weight 50,
  one core per run, different seeds. 30 points: 2 runs, both found nested 7-gon-free sets. 32 points: 5 runs, all
  found such sets. 34 points: 14 runs from random starts; six reached 2 convex 7-gons, the other eight stopped at 6 to
  18, and none reached 0. Two more runs restarted from a 2-heptagon set found nothing better.

## Files

- `TASK.md`, `PLAN.md`, `lists/C2P.tsv`, `cubes/`, `orbits/`, `vendor/`, `tools/` (`lane.py`, `lane3.py`, `mklist.py`,
  `l3cubes.py`, `mkl3.py`, `summary.py`).
- `M00`–`M41/`: per machine `env.txt`, `tools.txt`, `units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`, `README.md`.
- Mac records: `LOCAL/` (test unit P7_2-10-13), `LOCAL_L3/` (third-layer pilot), `LOCAL_DEEP/` (direct runs with a long
  cap). `cubes3/`: the third-layer cubes of P8_3-11.
- `nestsets/`: the real sets and their checks. `review/`: the review scripts and logs (`review/README.md`).
