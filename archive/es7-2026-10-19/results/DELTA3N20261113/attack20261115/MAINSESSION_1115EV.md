# Main-session checks, 15 November 2026 evening (18:50-23:00 KST)

## LRR(7) = LR(7) (rooted left-or-right form) at m = 15: cake_lpr accepts T1's proof (18:52-19:04)

- CNF `/home/jay/research/data/roadmap-20261115/pm1115/t1/lrr7/lrr7_m15.cnf` (SHA-256
  `651241dbc65d664730eb4f33e4d6f2c08a9e7c0c9c4918d2e076839749cda7f4`). It is T3's encoder `pm1115/t3/tools/lr_cnf.py` run
  at n = 7, m = 15 through T1's streaming copy. T1: CaDiCaL 2.1.3 UNSAT after 7,857 s.
  - Proof: `pm1115/t1/lrr7/cert15/lrr7_m15.lrat.zst` (LRAT 23,709,710,423 bytes, SHA-256 `99c38ea8…d32c`).
  - T1's own cake_lpr run at a 1,150 MB heap ran out of heap, so the result stood as COMPUTED.
- Main-session run: the proof was streamed through a FIFO into cake_lpr (heap 4500 MB) in unit `esr-mainv-lrr7m15`
  (MemoryMax 5800M). Script `round6/mainsession/recake_generic.sh`; outputs in `round6/mainsession/lrr7m15cake/`.
- Result: **`s VERIFIED UNSAT`** (1 line; exit status 0).
  - LRAT SHA-256 recomputed while streaming: `99c38ea8e322246b3af60e2a8f04161f6fff5b5c7674462a1fe4a1896679d32c`, equal
    to T1's record. CNF SHA-256 equal.
  - Wall time 11 min 43 s; peak RSS 4.62 GB.
- With ROOT(7) CERTIFIED for |S| ≤ 14 (ROOT implies LRR at each size): **LRR(7), hence LR(7), holds for every
  (5,7)-valid signotope with at most 15 points** (CERTIFIED; computer-assisted).
- Caveats:
  - The CNF's correspondence to LRR(7) rests on lr_cnf.py. V1 reviewed that encoder at n = 6 (VERIFY_LRR6.md). The n = 7
    regeneration and controls are filed as claim `lrr7-m15-certified` for a verifier.
  - Weak D(5,7) was already CERTIFIED to 15 points (DELTA2N), so this extends the LR route, not weak D(5,7).
- **Verifier verdict, 19:41: CONFIRMED** at the label CERTIFIED ([VERIFY_LRR7_M15.md](VERIFY_LRR7_M15.md)). The
  verifier regenerated the CNF from T3's original `lr_cnf.py 7 15` (`8669a98b…`) byte for byte (`651241db…`) and
  reviewed the encoder at n = 7.

## LP0(7) is false for a REAL 20-point set (EXACT; main session's own C++ check, 21:14)

- Set: `/home/jay/research/data/roadmap-20261115/pm1115/d2/hit/lp0_7_real20.json` (SHA-256 `dd7291027c456978…`). Agent
  D2 found it with a BFP-CEGAR over two- and three-point extensions of R7's real block, and realize_sig.py realized it.
  Claim: `lp0-7-false-real`.
- The set (x strictly increasing; r = the last point):
  `[[-15537, -266], [-8403, -690], [-3735, 2710], [-3607, -968], [-3605, -1128], [563, 15010], [578, 14913], [583, 1396], [588, -1112], [803, -1226], [856, -1269], [860, 13590], [4070, 18359], [4083, 8416], [4105, -1297], [10248, -1438], [10324, -1565], [10348, 27827], [10804, 28611], [15537, -10027]]`
- Check: `round6/mainsession/root15/lp0_real_check.cpp` (SHA-256 `40173a3488d299b3…`), compiled with g++ -O2.
  - Integer orientations; no collinear triple; caps by all triples; convexity by exact point-in-triangle tests on
    4-subsets.
  - Exhaustive over all 2^20 subsets for the weak Δs through r and through l.
- Output (`lp0_real20_check.out`):
  - 312 four-caps, 165 ending at r.
  - **0 five-caps and 0 convex 7-gons**, so the set is (5,7)-valid. 1,011 convex hexagons.
  - **P0** (the points that end no 4-cap) has 10 points and **misses 6 convex hexagons**.
  - **Weak Δs containing r: 0.** Weak Δs containing l: 4,040.
- So **LP0(7) fails for this real set**: r lies in no weak Δ, and P0 is not a weak Δ.
- On the same set ROOT(7) also fails at r. LR(7) and weak D(5,7) hold (4,040 weak Δs through l). All numbers equal the
  claim.
- Consequence: of the three reductions T4 PROVED to imply weak D(5,n) (LR, TWO-ENV#, LP0), LP0 is now false for point
  sets at n = 7. LR(7) is CERTIFIED for |S| ≤ 15 and open above. No ES bound changes.

## LRR(7) m = 15: independent second cake_lpr run (verifier agent VL, 21:05-21:19)

- **CONFIRMED** ([VERIFY_LRR7_M15_RERUN.md](VERIFY_LRR7_M15_RERUN.md)). VL wrote its own streaming script
  (`pm1115/vl/cake_stream.sh`, `cbf2abf4…`). The run printed exactly one line, `s VERIFIED UNSAT`, with an empty
  `cake.err`.
  - CNF `651241db…`; streamed LRAT `99c38ea8…`, 23,709,710,423 bytes. Both equal the record.
  - Heap 4500; wall time 13 min 55 s; peak RSS 4.5 GiB.
  - Unit `esr-mainv-vl-lrr7m15`, moved to the `mainv` track by the main session so that it stayed out of the
    verifiers' 3 GB track. Result success.
- Both cake_lpr runs used the same cake_lpr binary. So the LRR(7) ≤ 15 certificate now has two separate runs with
  separate scripts, plus VB's check of the CNF.
- **Second, different real counterexample (22:01, claim `lp0-7-false-real-2`).** File
  `pm1115/d2/hit/lp0_7_real20_t1it4.json` (SHA-256 `3692cfc9969620f6…`; |coordinates| ≤ 116,317), built on T1's
  block. The same `lp0_real_check.cpp` gives `LP0_7_real_counterexample: YES` (output `lp0_real20b_check.out`):
  - 326 four-caps, 159 ending at r; 0 five-caps, 0 convex 7-gons; 1,055 convex hexagons;
  - P0 has 10 points and misses 5 hexagons;
  - 0 weak Δs through r, and 3,329 weak Δs through l.
