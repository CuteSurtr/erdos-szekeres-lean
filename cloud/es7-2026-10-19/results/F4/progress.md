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
- 02:58 control: F4 process_new26.sh on F2's gg401_5 (fingerprint check bypassed) gives 5 direction-scan
  deep-below 32-sets + the s2-convention set (same order type as d4), 5 distinct order types,
  as F2 reported; all general position, lcs 6, brute_kgon 0 convex 7-sets, ext_solve 33/33 UNSAT
  on all 9 files; sat.c 0 bad candidates on the 3 files below 2^27 (2 order types).  Added a
  compression retry (2 x 150 CPU-s) so more order types get the geometric face sweep.
- ~03:00 container restart killed all runs (logs kept).  Before it: arm_f seed 4000003 558 restarts
  (max 22 of 26 placed), grow_guided 4000001/4000002 one finished chain (max 23), realizer 258
  models with 0 realized.  03:05 relaunched: grow_guided seeds 4000007, 4000008; arm_f seed
  4000006 with --jitter 0.3 --extra-props 2 --smart-bt; realizer resumed at model 258.
- 04:18 grow_guided seed 4000008 chain 5 produced gg4000008_5 (via the hybrid realizer step, so its
  x-order is the realizer's, not the model's).  Exact: distinct x, general position, lcs 6
  (heptagon-free), x-direction max cap 6 / cup 6.  Canonical fingerprint d336c15c... is new
  against F2's four 26-sets.  But it is NOT a (7,5,7) set in any direction: all 650 sweep
  directions have max cap >= 5 (process26.py: cap4_directions 0), and s2 build32.py finds neither
  a 4-cap nor a 4-cup frame.  So no deep-below 32-point set exists for it in either convention.
- 05:50 generators stopped; 06:00 realizer finished all 3,000 models on 4 cores (0 realized); README written.
