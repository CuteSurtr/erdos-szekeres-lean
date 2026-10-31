# C2P4: fourth wave on the parallelogram cases of the central 34-point formula (2026-10-31)

**Closed in this wave: P6.** For this case, the cover of the 560-way second-layer split
and all 287 orbits are certified (lrat-check and cake_lpr). By the reflection pairing (B) every one of the 560 subcases
is excluded for real configurations, and by the case reduction (A) the mirror case
P11 is excluded too (`results/C2P/review/README.md`). Together with the earlier waves,
no centrally symmetric set of 34 points in general position without a convex 7-gon has a parallelogram hull of type
P8/P9, P7/P10, P6/P11. The other parallelogram cases remain open. The independent recount is below.

The setting, the encoding, the reductions (A) and (B) and the tools are those of `results/C2P` (README and `review/`);
P8 was closed in `results/C2P2` and P7 in `results/C2P3`. This wave ran `lists/C2P4.tsv` (made by `mklist4.py`) on 50
cloud machines (one CaDiCaL lane each, 4 vCPU and 15 GB) and one lane on a Mac:
- the open orbits of P6 and P5, then P4 and P3, placed greedily by expected load, quadrilateral subcases and covers
  first; cap 6,000 s for a quadrilateral subcase, 7,000 s if it timed out before, 1,800 s for a hexagonal one;
- for P6_1-7, which timed out at 5,938 s in the third wave, both members of its orbit (P6_1-7 and P6_5-16);
- on the Mac: P6_1-7 with a cap of 8,400 s, then the last rows of the list in reverse order; from 14:18Z first the
  five open hexagonal representatives of P6 that were queued behind fresh P5 quadrilateral units on the cloud; from
  14:46Z P6_8-9-12 (the last open orbit of P6), then hexagonal subcases of P3 in the reverse order of
  `C2P5/lists/C2P5B.tsv` (the Mac lane continues into the fifth wave; `LOCAL/out.jsonl` holds its records up to this
  collection).

Every UNSAT proof was checked by lrat-check and cake_lpr and then deleted; the records keep the CNF sha256 and the
proof's size and sha256.

## Results

- 324 unit records (320 of the 783 listed units reached); 303 certified (both checkers accepted).
- SAT answers: 0. Proofs rejected or unchecked: 0. Other outcomes: 0.
- Solve seconds of certified cloud units: 20–5,884 (median 366).
  Largest solver RSS: 10.9 GB.
- Units that timed out before (cap 7,000 s): P6_1-7 certified (5,818 s, M00); P6_8-13 certified (4,488 s, M01); P6_8-14 certified (4,246 s, M02); P6_9-14 certified (2,974 s, M03); P5_1-4 certified (1,207 s, M04); P5_1-6 certified (3,028 s, M05); P5_1-8 certified (4,312 s, M06); P5_1-10 certified (4,136 s, M07); P5_1-11 certified (3,070 s, M08); P5_1-12 certified (2,788 s, M09); P5_2-8 certified (2,512 s, M10); P5_2-9 certified (2,541 s, M11); P5_2-11 certified (3,786 s, M12); P5_6-9 certified (726 s, M13); P5_7-13 certified (3,023 s, M14).
- P6_1-7 and its partner: P6_1-7 certified (5,818 s, M00); P6_5-16 certified (5,884 s, M15).
- On the Mac: 34 records, 34 certified.
- By case, kind and outcome: P3 H certified: 30, P3 Q certified: 1, P4 H UNKNOWN: 1, P4 H certified: 50, P4 Q UNKNOWN: 15, P4 Q certified: 29, P5 H UNKNOWN: 3, P5 H certified: 123, P5 Q UNKNOWN: 2, P5 Q certified: 46, P6 H certified: 18, P6 Q certified: 6.

## All waves together

Per case, with all earlier waves and the P8 pilot; a certified reflection partner closes its orbit
(`C2P/tools/summary.py`):

```
case  cover  reps certified/287 (Q /56, H /231)  no answer yet (not certified)
P1    yes      0 ( 0 Q,   0 H)                  0: 
P2    yes      0 ( 0 Q,   0 H)                  0: 
P3    yes     31 ( 1 Q,  30 H)                  0: 
P4    yes     79 (29 Q,  50 H)                  16: P4_1-10 P4_1-11 P4_1-13 P4_1-5 P4_1-8 P4_1-9 P4_2-8 P4_5-15 ...
P5    yes    267 (54 Q, 213 H)                  5: P5_1-6-11 P5_2-6-9 P5_6-11-16 P5_6-16 P5_9-11
P6    yes    287 (56 Q, 231 H)                  0: 
P7    yes    287 (56 Q, 231 H)                  0: 
P8    yes    287 (56 Q, 231 H)                  0: 
total certified representatives: 1238 of 2296; covers: 8 of 8; third-layer units certified: 15, third-layer covers: 1
```

**Closed cases** (cover and all 287 orbits certified; with (A) the mirror case P(17−a) is excluded too). Independent recount by `C2P3/check_case.py`, which rebuilds the orbits from the subcase names and reads the raw records:
- P6 (and P11): subcases 560, orbits 287 (14 fixed), cover certified: True, orbits without a certified member: 0 [].
- P7 (and P10, closed in the third wave): subcases 560, orbits 287 (14 fixed), cover certified: True, orbits without a certified member: 0 [].
- P8 (and P9, closed in the second wave): subcases 560, orbits 287 (14 fixed), cover certified: True, orbits without a certified member: 0 [].

## Files

`TASK.md`, `mklist4.py`, `lists/C2P4.tsv`; per machine `M00`–`M49/` (`env.txt`, `tools.txt`, `units.tsv`, `run.sh`,
`out.jsonl`, `lane.log.tail`, `README.md`); `LOCAL/out.jsonl`: the Mac's records.
