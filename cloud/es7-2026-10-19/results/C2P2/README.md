# C2P2: second wave on the parallelogram cases of the central 34-point formula (2026-10-31)

**Closed in this wave: P8.** For this case, the cover of the 560-way second-layer split
and all 287 orbit representatives are certified (lrat-check and cake_lpr). By the reflection pairing (B) every one of
the 560 subcases is excluded for real configurations, and by the case reduction (A) the mirror case
P9 of the 16 parallelogram labellings is excluded too (`results/C2P/review/README.md`). So no
centrally symmetric set of 34 points in general position without a convex 7-gon has a parallelogram hull of type
P8/P9. The other parallelogram cases remain open.

Independent recount for P8 (`check_p8.py`, which rebuilds the orbits from the subcase names and reads the raw records,
without `C2P/orbits` or `summary.py`): subcases 560, orbits 287 (14 fixed), cover certified: True, orbits without a certified member: 0 [].

The setting, the encoding, the reductions and the tools are those of `results/C2P` (see its README and `review/`).
This wave ran `lists/C2P2.tsv` (made by `mklist2.py` from the first-wave records) on 42 cloud machines (one CaDiCaL lane
each, 4 vCPU and 15 GB) and one lane on a Mac:
- the 35 quadrilateral representatives that timed out at their full cap in the first wave or the pilot, again with a
  cap of 6,000 s, and P8_7-16, the reflection partner of P8_1-9 (refuting either member of a pair suffices);
- P8_1-9 itself on the Mac with a cap of 7,500 s;
- the rest of P7 and of P6 and the covers of P6..P1, with the caps of the first wave.

Every UNSAT proof was checked by lrat-check and cake_lpr and then deleted; the records keep the CNF sha256 and the
proof's size and sha256.

## Results

- 194 unit records; 176 certified (both checkers accepted).
- SAT answers: 0. Proofs rejected or unchecked: 0. Other outcomes: 0.
- Solve seconds of certified cloud units: 65–5,935 (median 391).
  Largest solver RSS: 11.5 GB.

**The hard quadrilateral subcases** (cap 6,000 s on the cloud, 7,500 s on the Mac):

| subcase | result | machine | solve s of cap | proof GB |
|---|---|---|---|---|
| P8_1-6 | certified | M00 | 3,717 of 6,000 | 8.0 |
| P8_1-7 | certified | M01 | 5,220 of 6,000 | 9.9 |
| P8_1-10 | certified | M02 | 5,935 of 6,000 | 10.0 |
| P8_1-11 | certified | M03 | 4,327 of 6,000 | 8.8 |
| P8_1-12 | certified | M04 | 3,404 of 6,000 | 7.4 |
| P8_2-9 | certified | M05 | 5,396 of 6,000 | 9.4 |
| P8_2-10 | certified | M06 | 5,505 of 6,000 | 8.9 |
| P8_2-12 | certified | M07 | 4,043 of 6,000 | 7.9 |
| P8_3-9 | certified | M08 | 3,403 of 6,000 | 7.6 |
| P8_3-10 | certified | M09 | 4,637 of 6,000 | 8.6 |
| P8_3-11 | certified | M10 | 4,718 of 6,000 | 8.8 |
| P8_3-12 | certified | M11 | 4,998 of 6,000 | 7.9 |
| P8_3-13 | certified | M12 | 3,347 of 6,000 | 6.9 |
| P8_4-10 | certified | M13 | 2,972 of 6,000 | 6.4 |
| P8_4-11 | certified | M14 | 3,433 of 6,000 | 7.2 |
| P8_4-12 | certified | M15 | 3,970 of 6,000 | 7.7 |
| P8_9-14 | certified | M16 | 3,286 of 6,000 | 7.2 |
| P8_9-15 | certified | M17 | 5,430 of 6,000 | 9.3 |
| P8_9-16 | certified | M18 | 5,844 of 6,000 | 9.7 |
| P8_10-15 | certified | M19 | 3,809 of 6,000 | 7.6 |
| P7_1-5 | certified | M20 | 2,075 of 6,000 | 6.0 |
| P7_1-6 | certified | M21 | 4,311 of 6,000 | 8.5 |
| P7_1-8 | certified | M22 | 5,389 of 6,000 | 10.1 |
| P7_1-9 | certified | M23 | 5,577 of 6,000 | 9.8 |
| P7_1-10 | certified | M24 | 5,331 of 6,000 | 9.4 |
| P7_1-12 | certified | M25 | 3,421 of 6,000 | 7.3 |
| P7_2-8 | certified | M26 | 3,610 of 6,000 | 8.1 |
| P7_2-10 | certified | M27 | 5,494 of 6,000 | 8.6 |
| P7_2-11 | certified | M28 | 4,515 of 6,000 | 8.3 |
| P7_3-9 | certified | M29 | 3,200 of 6,000 | 7.3 |
| P7_3-11 | certified | M30 | 4,168 of 6,000 | 7.9 |
| P7_3-13 | certified | M31 | 3,154 of 6,000 | 6.7 |
| P7_8-14 | certified | M32 | 3,438 of 6,000 | 7.7 |
| P7_8-15 | certified | M33 | 5,043 of 6,000 | 9.0 |
| P7_9-15 | certified | M34 | 4,285 of 6,000 | 8.2 |
| P8_7-16 | UNKNOWN | M35 | 5,946 of 6,000 | 0.0 |
| P8_1-9 | certified | Mac | 4,070 of 7,500 | 11.1 |

**Other units of this wave** (case, kind, outcome: count): P6 H UNKNOWN: 2, P6 H certified: 87, P6 Q UNKNOWN: 11, P6 Q certified: 3, P6 cover certified: 1, P7 H certified: 44, P7 Q UNKNOWN: 4, P7 Q certified: 5.

## All waves together

Per case, with the first wave (`results/C2P`) and the P8 pilot (`results/C2C34`); a certified reflection partner
closes its orbit (`C2P/tools/summary.py`):

```
case  cover  reps certified/287 (Q /56, H /231)  no answer yet (not certified)
P1    no       0 ( 0 Q,   0 H)                  0: 
P2    no       0 ( 0 Q,   0 H)                  0: 
P3    no       0 ( 0 Q,   0 H)                  0: 
P4    no       0 ( 0 Q,   0 H)                  0: 
P5    no       0 ( 0 Q,   0 H)                  0: 
P6    yes    100 ( 3 Q,  97 H)                  15: P6_1-10 P6_1-11 P6_1-16 P6_1-7-14 P6_1-8 P6_1-9 P6_1-9-14 P6_2-10 ...
P7    yes    270 (44 Q, 226 H)                  11: P7_1-11 P7_1-13 P7_2-13 P7_2-9 P7_3-10 P7_3-12 P7_3-8-16 P7_8-13 ...
P8    yes    287 (56 Q, 231 H)                  0: 
total certified representatives: 657 of 2296; covers: 3 of 8; third-layer units certified: 15, third-layer covers: 1
```

## Files

`TASK.md`, `mklist2.py`, `lists/C2P2.tsv`; per machine `M00`–`M41/` (`env.txt`, `tools.txt`, `units.tsv`, `run.sh`,
`out.jsonl`, `lane.log.tail`, `README.md`); `LOCAL/out.jsonl`: the Mac's records.
