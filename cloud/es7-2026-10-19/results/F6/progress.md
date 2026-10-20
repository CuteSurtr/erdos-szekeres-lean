# F6 progress (seeds 6000000-6999999)

- 02:36 UTC start; env.txt (4 cores, 15 GB). Built CaDiCaL (master c6073042) and sat.c, brute26.c,
  brute.c, brute_kgon.c, ext_solve.cpp, prefix_server.cpp, sat_server.cpp, gen_models.cpp (-O2).
  CNFs: gen_etv.py 26 5 7 7 (17,831 vars, 222,991 clauses); gen_cnf.py 33 7 (47,002 vars, 679,038 clauses).
- Reproduction: F2/s2 pipeline.sh on F22_106 and F22_162 with the rebuilt tools gives the same
  results as F2/s2/data/run1 (data/controls/repro_F2s2). F2's process26.py (direction-scan
  convention) on gg401_5 gives 5 cap-4 directions and 5 deep-below 32-sets, as F2 has.
- Fingerprint control: canonical_form fingerprint of gg401_5 is unchanged under a 90-degree
  rotation and under reflection; different F2 sets get different fingerprints (data/controls).
- 02:39 launched 4 workers (scripts/run_arms.sh): arm F defaults seeds 6000001..; arm F with
  --jitter 0.3 --extra-props 2 --bt-depth 4 seeds 6000101..; grow_guided seeds 6000201..;
  KPH-style: gen_models.py seed 6000301 (3,000 distinct models in 439 s) then the validated realizer
  (4 CPU-s per model, ins-ff,lp, seeds 6500000+index).
- 03:17 arm F defaults: 684 + 148 restarts, best 22/26 placed, 0 complete; jitter variant 437 + 95
  restarts, best 23, 0 complete. Reallocated (scripts/run_arms2.sh): those two cores now run
  grow_guided seeds 6000211.. and arm F --jitter 0.3 --extra-props 2 --smart-bt seeds 6000111..
  KPH-style at 377 models realized-attempted, 0 realized.
- 03:43 grow_guided seed 6000202 chain 1 completed a 26-point set, gg6000202_1 (via dfs, 916 s);
  03:50 chain 2 gave gg6000202_2 (358 s). Both: distinct x, general position, cap 4, cup 6, lcs 6,
  brute 0 axiom violations; canonical fingerprints 73018d566e82b37c and 7a99a99767186a46, not
  among F2's sets (data/sets26).
- s2 convention (pipeline.sh): both 32-point deep-below sets lcs 6, brute 0 convex 7-subsets,
  ext_solve 33/33 UNSAT (abstractly saturated). gg6000202_2: sat.c 0 bad faces (Euler count
  matches). gg6000202_1: compression below 2^27 failed in build32, so the face sweep is pending a
  recompression (scripts/geom_fill.py). (Note: the first gg6000202_1 run shared a scratch dir with
  the F2 reproduction, so its logs also list F22_106/F22_162; data/sets32/gg6000202_1 keeps only
  its own records. Later sets run in private dirs via scripts/handle26.sh.)
