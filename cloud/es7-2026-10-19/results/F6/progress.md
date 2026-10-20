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
