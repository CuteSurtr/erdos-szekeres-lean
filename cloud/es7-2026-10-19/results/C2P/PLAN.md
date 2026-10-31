# C2P: the parallelogram cases of the central 34-point formula

**Goal.** Refute every second-layer subcase of the 8 canonical parallelogram cases of `results/C2C34`. Each case also
needs the certified cover of its split. Together with the hexagonal-hull result, this would exclude a centrally
symmetric 34-point set without a convex 7-gon. That is the last symmetric route to a counterexample to ES(7) = 33.

**List** (`lists/C2P.tsv`, made by `tools/mklist.py`). It has 2,236 units: 7 covers, 434 Q and 1,795 H.
- **Order.** Cases P8, P7, …, P1; within each case the cover first, then the orbit representatives, with Q and H
  interleaved.
- **Left out.**
  - For P8, the cover and 64 representatives are certified in `results/C2C34`.
  - P8_3-11, P8_2-11 and P8_1-9 gave no answer at 1,800 s. They need a third-layer split.
- **Cubes** (`cubes/`). Output of `results/C2C34/l2cubes.py`; the P8 file is identical to `results/C2C34/p8/P8_cubes.txt`.
- **Orbits** (`orbits/`). The P8 map is identical to `results/C2C34/p8/orbits.tsv`.

**Cost.** Estimated from the P8 pilot (Apple M5 Pro), including both checks:
- about 280 s per H unit and 900 s per Q unit;
- the covers took 550 s plus checks.

A cloud machine (4 vCPUs, 15 GB) runs one lane, because CaDiCaL needs up to about 12 GB on this formula. The list is
dealt round-robin to N machines, so all of them work through the cases in order.

**Trust base.**
- **Reviewed.** The encoding and the layer reduction (`results/C2C34/review/`) and the certified covers.
- **Not yet independently reviewed.**
  - The reduction of the 16 quadrilateral hull cases to the canonical 8 (`results/C2C34` §2).
  - The reflection that pairs the subcases of each case (§6).
  Both are arguments about real configurations, independent of the solver.
- **Records.** Each unit's record has the CNF sha256, the proof size and sha256, and both checker verdicts. Proofs are
  deleted after both checks.

**After this wave.**
- Units not reached.
- Q units that time out. They need a third-layer split, which is being developed separately.
- The other members of each orbit, if the reflection argument does not survive review.
