// cncw: persistent CaDiCaL cube worker with orientation-variable lookahead splitting.
// usage: cncw cnf candidates-file model-dir [maxcand]
// The candidates file lists the variables allowed as split variables (here: the mirror-orbit
// representatives of the orientation variables).  All candidates are frozen.
// stdin jobs:  "id limit lit1 ... litk 0"
// replies:     "U id"               cube refuted (solver claim, no proof log here)
//              "S id"               model written to <model-dir>/model-<id>.txt
//              "K id lit np nn"     conflict limit hit; lit = split literal chosen by a
//                                   march-style lookahead restricted to the candidates:
//                                   score (np+1)(nn+1), np/nn = literals implied by unit
//                                   propagation of cube+[lit] / cube+[-lit] beyond the cube.
//                                   A failed literal (propagation conflict on one side) is
//                                   returned at once with np or nn = -1.
//              "K id 0 0 0"         every candidate is assigned under the cube.
#include "cadical.hpp"
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
#include <algorithm>
static CaDiCaL::Solver s;
static long implied_count(const std::vector<int> &cube, int extra, bool &conflict) {
  for (int l : cube) s.assume(l);
  if (extra) s.assume(extra);
  int r = s.propagate();
  if (r == 20) { conflict = true; return 0; }
  conflict = false;
  std::vector<int> imp; s.implied(imp);
  return (long) imp.size();
}
int main(int argc, char **argv) {
  if (argc < 4) { std::fprintf(stderr, "usage: cncw cnf cands model-dir [maxcand]\n"); return 2; }
  std::string dir = argv[3];
  size_t maxcand = argc > 4 ? (size_t) atol(argv[4]) : 1000000;
  s.set("quiet", 1);
  int vars = 0;
  const char *err = s.read_dimacs(argv[1], vars, 1);
  if (err) { std::fprintf(stderr, "parse error: %s\n", err); return 2; }
  std::vector<int> cands; { std::ifstream f(argv[2]); int v; while (f >> v) cands.push_back(v); }
  for (int v : cands) s.freeze(v);
  std::printf("READY %d %zu\n", vars, cands.size()); std::fflush(stdout);
  std::string line;
  unsigned long long rng = 88172645463325252ULL;
  while (std::getline(std::cin, line)) {
    std::istringstream in(line);
    long id; long long limit; in >> id >> limit;
    std::vector<int> cube; int lit;
    while (in >> lit && lit != 0) cube.push_back(lit);
    for (int l : cube) s.assume(l);
    s.limit("conflicts", (int) std::min<long long>(limit, 2000000000LL));
    int res = s.solve();
    if (res == 20) { std::printf("U %ld\n", id); }
    else if (res == 10) {
      std::string path = dir + "/model-" + std::to_string(id) + ".txt";
      FILE *f = std::fopen(path.c_str(), "w");
      for (int v = 1; v <= vars; v++) std::fprintf(f, "%d\n", s.val(v) > 0 ? v : -v);
      std::fclose(f);
      std::printf("S %ld\n", id);
    } else {
      bool conf;
      long base = implied_count(cube, 0, conf);
      if (conf) { std::printf("U %ld\n", id); std::fflush(stdout); continue; }  // refuted by propagation
      std::vector<int> imp; s.implied(imp);
      std::vector<char> assigned(vars + 1, 0);
      for (int l : imp) assigned[std::abs(l)] = 1;
      std::vector<int> free;
      for (int v : cands) if (!assigned[v]) free.push_back(v);
      if (free.size() > maxcand) {  // random subset (deterministic xorshift)
        for (size_t i = 0; i < maxcand; i++) {
          rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
          size_t j = i + rng % (free.size() - i); std::swap(free[i], free[j]);
        }
        free.resize(maxcand);
      }
      int best = 0; double bestscore = -1; long bnp = 0, bnn = 0;
      for (int v : free) {
        bool cp, cn;
        long np = implied_count(cube, v, cp) - base;
        if (cp) { best = v; bnp = -1; bnn = 0; break; }
        long nn = implied_count(cube, -v, cn) - base;
        if (cn) { best = v; bnp = 0; bnn = -1; break; }
        double sc = (double) (np + 1) * (double) (nn + 1);
        if (sc > bestscore) { bestscore = sc; best = v; bnp = np; bnn = nn; }
      }
      std::printf("K %ld %d %ld %ld\n", id, best, bnp, bnn);
    }
    std::fflush(stdout);
  }
  return 0;
}
