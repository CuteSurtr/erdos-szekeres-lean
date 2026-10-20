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
- CORRECTION: probe.sh used `shuf --random-source=<(yes SEED)`, which is NOT random: it picks
  line 63 of 64 for every seed (checked). So probe_757_seed1/2/3 and probe_es6 followed ONE
  deterministic path (the same cubes, timing noise only). They describe one hard path, not a
  random sample; their "est_nodes" figures are not Knuth estimates. Replaced by descend.sh /
  sample_node.sh (python random.seed(seed*1000+step)).
- 01:57 node30 (descend seed 7, depth 30): march -d 10 -> 109 cubes + 73 refuted leaves (68 s);
  all 109 cubes UNSAT in 2.65 s total.
- 02:00 samples_d30.txt: 12 random depth-30 nodes (5 descents of march -d 6), plain CaDiCaL,
  300 s cap: 10 UNSAT in 0.13-0.92 s, 2 (seeds 102, 106) TIMEOUT at 300 s. Heavy-tailed.
  Product of surviving-cube counts along the paths: 1.7e7 to 1.07e9 (mostly 64^5 = 1.07e9).
- 02:10 hard node 102 (depth 30): march -d 10 -> 945 cubes + 28 refuted leaves (336 s); conquer
  with 3 incremental CaDiCaL workers, 600 s/cube cap (hard102/progress.txt).
- 02:13 LRAT spot-check (lrat/summary.txt): 4 hard102 cubes at the 20/50/80/95th percentile of
  solved-cube time (0.2-6 s): CaDiCaL --lrat, lrat-check "c VERIFIED" on node CNF + cube units; proofs
  0.4-17 MB, checked in 0.1-0.3 s. Negative test: same proof against the CNF with the last cube unit
  removed -> lrat-check ERROR (not verified).
- 02:15 glue pipeline on the (7,5,7)@26 control models (ours+lexx, bb+lexx): glue.py 757 -> 32-element
  signotopes, sigcheckB: no 7-gon (both tests), max cap 6, max cup 6, no signotope violation.
- 02:17 realize.py (methods ins-ff,lp,free; 150 CPU s) on the 26-point control model: not realized,
  211 violated triples at best (proves nothing; KPH report ~1.6e-4 realization rate at this size).
- 02:23 hard102 interim: 496/945 cubes done (493 UNSAT, 3 hit 600 s), summed cube time 4,525 s;
  solve-time histogram <1 s: 331, 1-10 s: 130, 10-60 s: 23, 60-600 s: 9, >=600 s: 3.
- 03:06 hard102 finished its pass (hard102/cubes.tsv: idx, result, seconds, conflicts): 945 cubes,
  931 UNSAT, 14 hit the 600 s cap, 0 SAT. Wall 72 min on 3 cores; summed cube time 12,611 s
  (censored: lower bound). UNSAT cube times: median 0.43 s, p90 5.7 s, p99 61 s, max 487 s.
  So this one depth-30 node is NOT closed: 14 depth-40 cubes remain open after 600 s each.
- 03:07 sampling shallower random nodes (depth 24 x9, 18 x6, 12 x3), plain CaDiCaL, 300 s cap.
- 03:07-03:45 Knuth samples: samples_d24.txt (57 random depth-24 nodes; 54 UNSAT 0.4-175 s, 3 capped
  at 300/400 s) and samples_d18.txt (2 depth-18 nodes, both >300 s). estimate.py: depth-24 cutoff
  >= 8.9e8 s ~ 2.5e5 core-h (lower bound, censored).
- 03:45 three depth-18 nodes with a 1500 s cap running.
