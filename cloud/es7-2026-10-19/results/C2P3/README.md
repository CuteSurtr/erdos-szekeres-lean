# C2P3: third wave on the parallelogram cases of the central 34-point formula (2026-10-31)

**Closed in this wave: P7.** For this case, the cover of the 560-way second-layer split
and all 287 orbits are certified (lrat-check and cake_lpr). By the reflection pairing (B) every one of the 560 subcases
is excluded for real configurations, and by the case reduction (A) the mirror case
P10 is excluded too (`results/C2P/review/README.md`). With P8 and P9 (`results/C2P2`),
no centrally symmetric set of 34 points in general position without a convex 7-gon has a parallelogram hull of type
P8/P9, P7/P10. The other parallelogram cases remain open. The independent recount is below.

The setting, the encoding, the reductions (A) and (B) and the tools are those of `results/C2P` (README and `review/`); the
second wave and the closure of P8 are in `results/C2P2`. This wave ran `lists/C2P3.tsv` (made by `mklist3.py`) on 50
cloud machines (one CaDiCaL lane each, 4 vCPU and 15 GB) and one lane on a Mac:
- on every machine first a quadrilateral subcase of P7 or P6 with a cap of 6,000 s (15 machines then a second one with
  4,800 s): all open quadrilateral representatives of P7 and P6;
- then the open hexagonal representatives of P7 and P6, then representatives of P5;
- on the Mac: the covers of P5..P1 and 2 quadrilateral representatives of P5; then (from 10:54Z) the three
  open hexagonal representatives of P7 that were queued behind long units on the cloud, and after them open hexagonal
  representatives of P6 in the same position.

Every UNSAT proof was checked by lrat-check and cake_lpr and then deleted; the records keep the CNF sha256 and the
proof's size and sha256.

## Results

- 314 unit records; 297 certified (both checkers accepted).
- SAT answers: 0. Proofs rejected or unchecked: 0. Other outcomes: 0.
- Solve seconds of certified cloud units: 19–5,463 (median 386).
  Largest solver RSS: 13.4 GB.
- The 65 quadrilateral units with long caps: certified 61, no answer 4.
  Open: P6_1-7 (5,938 s of a lane cap of 6,000 s), P6_8-13 (1,314 s of a lane cap of 1,328 s), P6_8-14 (2,907 s of a lane cap of 2,936 s), P6_9-14 (2,914 s of a lane cap of 2,945 s).
- By case, kind and outcome: P1 cover certified: 1, P2 cover certified: 1, P3 cover certified: 1, P4 cover certified: 1, P5 H UNKNOWN: 2, P5 H certified: 90, P5 Q UNKNOWN: 11, P5 Q certified: 9, P5 cover certified: 1, P6 H certified: 124, P6 Q UNKNOWN: 4, P6 Q certified: 49, P7 H certified: 8, P7 Q certified: 12.

## All waves together

Per case, with the first and second waves and the P8 pilot; a certified reflection partner closes its orbit
(`C2P/tools/summary.py`):

```
case  cover  reps certified/287 (Q /56, H /231)  no answer yet (not certified)
P1    yes      0 ( 0 Q,   0 H)                  0: 
P2    yes      0 ( 0 Q,   0 H)                  0: 
P3    yes      0 ( 0 Q,   0 H)                  0: 
P4    yes      0 ( 0 Q,   0 H)                  0: 
P5    yes     98 ( 8 Q,  90 H)                  13: P5_1-10 P5_1-11 P5_1-12 P5_1-4 P5_1-6 P5_1-8 P5_2-11 P5_2-11-16 ...
P6    yes    268 (52 Q, 216 H)                  4: P6_1-7 P6_8-13 P6_8-14 P6_9-14
P7    yes    287 (56 Q, 231 H)                  0: 
P8    yes    287 (56 Q, 231 H)                  0: 
total certified representatives: 940 of 2296; covers: 8 of 8; third-layer units certified: 15, third-layer covers: 1
```

**Closed cases** (cover and all 287 orbits certified; with (A) the mirror case P(17−a) is excluded too). Independent recount by `check_case.py`, which rebuilds the orbits from the subcase names and reads the raw records:
- P7 (and P10): subcases 560, orbits 287 (14 fixed), cover certified: True, orbits without a certified member: 0 [].
- P8 (and P9, closed in the second wave): subcases 560, orbits 287 (14 fixed), cover certified: True, orbits without a certified member: 0 [].

## Files

`TASK.md`, `mklist3.py`, `lists/C2P3.tsv`, `check_case.py`; per machine `M00`–`M49/` (`env.txt`, `tools.txt`, `units.tsv`,
`run.sh`, `out.jsonl`, `lane.log.tail`, `README.md`); `LOCAL/out.jsonl`: the Mac's records.
