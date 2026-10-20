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
