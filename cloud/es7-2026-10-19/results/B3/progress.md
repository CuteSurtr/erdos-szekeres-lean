# B3 progress log (UTC)
- 00:29 start; 4 cores, 15 GB (env.txt).
- 00:40 built CaDiCaL, Kissat, drat-trim+lrat-check, march_cu (CnC; needed -fcommon), Baek-Balko encoder.
- 00:41 controls (controls.json): (7,4,7)@16 SAT, @17 UNSAT, (7,5,7)@26 SAT, (6,5,6)@16 UNSAT
  (CaDiCaL: ours 126.8 s, bb 111.8 s, ours+lexx 105.8 s, bb+lexx 73.4 s); all four encodings agree,
  every SAT model brute-force checked by sigcheckB.
- main CNF: gen_etv.py 27 5 7 7 + lexx.py (x-reflection lex-leader): 21,533 vars, 265,448 clauses.
- 00:42 plain Kissat baseline started on 1 core (ours_sb.cnf).
- march_cu -d 8: 256 cubes in 18 s; -d 12: 4096 cubes in 578 s, 0 refuted leaves.
- 3 random depth-12 cubes: all hit 120 s limit (incremental CaDiCaL). 3 random depth-20 cubes
  (one depth-12 cube refined by march -d 8): all hit 120 s.
- 00:57-01:08 Knuth probe (probe_757_seed1.log): random descent, march_cu -d 6 per step, 3 random
  cubes per level, 60 s limit. Every level up to depth 30 has 64/64 surviving cubes (no lookahead
  refutation) and all sampled cubes time out; depth 36: 31 s, 37 s, >60 s; depth 42: 4-11 s; depth 48:
  0.1-3.5 s (59/64 survive); depth 54: 23/64 survive. Path estimate of leaves at depth 42: 4.4e12.
- 01:00-01:25 ES(6) calibration, (6,5,6)@16 + lexx (monolithic CaDiCaL 106 s):
  march_cu -d 8: 254 cubes, 1.7 s cubing, 271 s total conquer (incremental CaDiCaL, 2 workers);
  march_cu dynamic (default): 27,173 cubes (329 refuted leaves), 694 s cubing, 1,208 s conquer.
  So CnC costs 2.6x (d=8) to 18x (dynamic) the monolithic CPU time on ES(6).
  Knuth probe on ES(6) (probe_es6_seed1.log): depth 4: 16 cubes x 2.5-5.3 s -> estimate ~60 s, same
  order as the true 106-271 s.
