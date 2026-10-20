# F4 progress (seeds 4000000-4999999)

- 02:36 UTC start; env.txt recorded (4 cores, 15 GB).
- 02:40 built CaDiCaL (master, libcadical.a), tools/trackA/sat.c, brute26.c, brute.c, brute_kgon.c,
  ext_solve.cpp, prefix_server.cpp.  CNFs: gen_etv.py 26 5 7 7 (17,831 vars, 222,991 clauses),
  gen_cnf.py 33 7 (47,002 vars, 679,038 clauses).
- Reproduction: F2/s2 pipeline.sh on F22_106 gives the same sign hash 42629b224dde2249, brute26 OK,
  same 32-point deep-below set (D = 2^60, lcs 6), sat.c 109,337 faces = Euler count, 0 bad
  candidates, ext_solve 33/33 UNSAT; the same as F2/s2/data/run1.
- 02:41 launched on 4 cores: grow_guided.py (F2) seeds 4000001, 4000002; arm_f.py (F2/s2) seed
  4000003; gen_models.py seeds 4000004 (400 models) + 4000005 (2,600 models), 3,000 distinct,
  all OK under brute26 26 5 7 7, then realize_models.py (validated realizer, 4 CPU-s, ins-ff,lp).
