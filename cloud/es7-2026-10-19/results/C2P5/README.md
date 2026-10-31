# C2P5: fifth wave on the parallelogram cases of the central 34-point formula (2026-10-31)

**Closed in this wave: P5.** For this case, the cover of the 560-way second-layer split
and all 287 orbits are certified (lrat-check and cake_lpr). By the reflection pairing (B) every one of the 560 subcases
is excluded for real configurations, and by the case reduction (A) the mirror case
P12 is excluded too (`results/C2P/review/README.md`). Together with the earlier waves,
no centrally symmetric set of 34 points in general position without a convex 7-gon has a parallelogram hull of type
P8/P9, P7/P10, P6/P11, P5/P12. The other parallelogram cases remain open. The independent recount is below.

The setting, the encoding, the reductions (A) and (B) and the tools are those of `results/C2P` (README and `review/`);
P8 was closed in `results/C2P2`, P7 in `results/C2P3` and P6 in `results/C2P4`. This wave ran three lists made by
`mklist5.py` on up to 100 cloud routines (one CaDiCaL lane each, 4 vCPU and 15 GB) and one lane on a Mac:
- `lists/C2P5B.tsv` on M50–M99 (from about 15:10Z, 5.25 h): the cases P2 and P1, then P3, placed greedily by expected
  load, quadrilateral subcases first;
- `lists/C2P5A.tsv` on M00–M36 (5 4 3 r2, 659 rows): the 20 open orbits of P5, then P4 and hexagonal subcases of P3 and
  P2. These routines fired at 15:32Z but the cloud gave no sandbox while the 49 machines of list B ran (about 50
  sandboxes at a time); only M00 started (15:58Z). At 17:55Z the list was rewritten for the machines that had not
  started (`relist_a.py`: the open orbits of P4 and the last hexagonal subcases of P3, without the units of every started
  machine, residues 1..36 modulo 37), and M01–M16 started as machines of list B finished. Machines of list A that were
  still running at this collection keep pushing their records into their directories;
- `lists/C2P5C.tsv` on M37–M49 (first a backup: hexagonal subcases of P1 and P2 in reverse order) obtained no sandbox
  at 15:36Z. At 20:05Z it was rewritten (`relist_c.py`) for the 10 open orbits that no running machine held (M98 of
  list B never started; some machines ended with rows left), and M37–M41 were started on it;
- caps: 8,000 s for a quadrilateral subcase, 10,000 s if it timed out before at 5,000 s or more (then both members of
  its orbit run), 2,400 s for a hexagonal one;
- on the Mac (records after the fourth-wave collection): hexagonal subcases of P3 in the reverse order of
  `C2P5B.tsv`; from 15:44Z the 18 open hexagonal representatives of P5, then P5_9-11 and P5_6-16 (the last orbit of P5),
  then hexagonal representatives of P4.

Every UNSAT proof was checked by lrat-check and cake_lpr and then deleted; the records keep the CNF sha256 and the
proof's size and sha256.

## Results

- 995 unit records (945 of the 1057 listed units reached); 995 certified (both checkers accepted).
- SAT answers: 0. Proofs rejected or unchecked: 0. Other outcomes: 0.
- Solve seconds of certified cloud units: 18–6,645 (median 290).
  Largest solver RSS: 10.7 GB.
- Units that timed out before (cap 10,000 s): none.
- On the Mac: 54 records, 54 certified.
- By case, kind and outcome: P1 H certified: 231, P1 Q certified: 55, P2 H certified: 237, P2 Q certified: 55, P3 H certified: 216, P3 Q certified: 55, P4 H certified: 101, P4 Q certified: 24, P5 H certified: 18, P5 Q certified: 3.

## All waves together

Per case, with all earlier waves and the P8 pilot; a certified reflection partner closes its orbit
(`C2P/tools/summary.py`):

```
case  cover  reps certified/287 (Q /56, H /231)  no answer yet (not certified)
P1    yes    286 (55 Q, 231 H)                  0: 
P2    yes    286 (55 Q, 231 H)                  0: 
P3    yes    275 (55 Q, 220 H)                  0: 
P4    yes    191 (53 Q, 138 H)                  1: P4_8-13
P5    yes    287 (56 Q, 231 H)                  0: 
P6    yes    287 (56 Q, 231 H)                  0: 
P7    yes    287 (56 Q, 231 H)                  0: 
P8    yes    287 (56 Q, 231 H)                  0: 
total certified representatives: 2186 of 2296; covers: 8 of 8; third-layer units certified: 15, third-layer covers: 1
```

**Closed cases** (cover and all 287 orbits certified; with (A) the mirror case P(17−a) is excluded too). Independent recount by `C2P3/check_case.py`, which rebuilds the orbits from the subcase names and reads the raw records:
- P5 (and P12): subcases 560, orbits 287 (14 fixed), cover certified: True, orbits without a certified member: 0 [].
- P6 (and P11, closed in the fourth wave): subcases 560, orbits 287 (14 fixed), cover certified: True, orbits without a certified member: 0 [].
- P7 (and P10, closed in the third wave): subcases 560, orbits 287 (14 fixed), cover certified: True, orbits without a certified member: 0 [].
- P8 (and P9, closed in the second wave): subcases 560, orbits 287 (14 fixed), cover certified: True, orbits without a certified member: 0 [].

## Files

`TASK.md`, `mklist5.py`, `relist_a.py`, `relist_c.py`, `lists/C2P5B.tsv`, `lists/C2P5A.tsv` and `lists/C2P5C.tsv` (as
last rewritten; earlier versions in the git history), `lists/exclude_*.txt`; per machine `M00`–`M99/` (`env.txt`, `tools.txt`,
`units.tsv`, `run.sh`, `out.jsonl`, `lane.log.tail`, `README.md`); `LOCAL/out.jsonl`: the Mac's records after the
fourth-wave collection.
