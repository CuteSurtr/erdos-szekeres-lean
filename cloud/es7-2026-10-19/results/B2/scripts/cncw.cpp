// Cube worker for cnc2.py. Loads a DIMACS CNF once (incremental CaDiCaL), then serves jobs
//   "id limit lit1 ... litk 0"   (cube = assumptions, limit = conflict budget)
// Replies, one line each:
//   "U id secs"             cube refuted (UNSAT under the assumptions)
//   "S id secs"             satisfiable; model written to <dir>/model-<id>.txt
//   "K id lit secs nc"      budget exhausted; lit = split literal, an ORIENTATION variable
//                           (1 <= lit <= nX), among the nc orientation variables not assigned
//                           by unit propagation under the cube, maximizing (1+p)*(1+q) where
//                           p, q count positive / negative occurrences in clauses (size <= 40)
//                           learned while solving THIS cube (VSIDS-like activity, collected
//                           with CaDiCaL's Learner hook). Ties are broken by a march-style
//                           lookahead (1+n(+v))*(1+n(-v)), n = extra literals implied by unit
//                           propagation (a conflicting side counts 10^6).
//                           lit = 0 if no unassigned orientation variable remains.
// Only orientation variables are ever used for splitting.
#include "cadical.hpp"
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
struct Act : CaDiCaL::Learner {
  int nX; std::vector<long long> pos, neg; std::vector<int> buf;
  explicit Act(int n) : nX(n), pos(n + 1), neg(n + 1) {}
  bool learning(int size) override { return size <= 40; }
  void learn(int lit) override {
    if (lit) { buf.push_back(lit); return; }
    for (int l : buf) if (std::abs(l) <= nX) (l > 0 ? pos : neg)[std::abs(l)]++;
    buf.clear();
  }
  void reset() { std::fill(pos.begin(), pos.end(), 0); std::fill(neg.begin(), neg.end(), 0); buf.clear(); }
};
static double now() {
  using namespace std::chrono;
  return duration<double>(steady_clock::now().time_since_epoch()).count();
}
int main(int argc, char **argv) {
  if (argc < 4) { std::fprintf(stderr, "usage: cncw cnf nX model-dir\n"); return 2; }
  int nX = atoi(argv[2]);
  std::string dir = argv[3];
  CaDiCaL::Solver s;
  s.set("quiet", 1);
  int vars = 0;
  const char *err = s.read_dimacs(argv[1], vars, 1);
  if (err) { std::fprintf(stderr, "parse error: %s\n", err); return 2; }
  Act act(nX);
  s.connect_learner(&act);
  std::printf("READY %d\n", vars); std::fflush(stdout);
  std::string line;
  std::vector<int> implied, assigned(nX + 1);
  while (std::getline(std::cin, line)) {
    std::istringstream in(line);
    long id; long long limit; in >> id >> limit;
    std::vector<int> cube; int lit;
    while (in >> lit && lit != 0) cube.push_back(lit);
    double t0 = now();
    act.reset();
    for (int l : cube) s.assume(l);
    s.limit("conflicts", (int) std::min<long long>(limit, 2000000000LL));
    int res = s.solve();
    if (res == 20) { std::printf("U %ld %.3f\n", id, now() - t0); std::fflush(stdout); continue; }
    if (res == 10) {
      std::string path = dir + "/model-" + std::to_string(id) + ".txt";
      FILE *f = std::fopen(path.c_str(), "w");
      for (int v = 1; v <= vars; v++) std::fprintf(f, "%d\n", s.val(v) > 0 ? v : -v);
      std::fclose(f);
      std::printf("S %ld %.3f\n", id, now() - t0); std::fflush(stdout); continue;
    }
    for (int l : cube) s.assume(l);
    int r = s.propagate();
    if (r == 20) { std::printf("U %ld %.3f\n", id, now() - t0); std::fflush(stdout); continue; }
    implied.clear();
    if (r == 0) s.implied(implied);
    long long base = (long long) implied.size();
    std::fill(assigned.begin(), assigned.end(), 0);
    for (int l : implied) if (std::abs(l) <= nX) assigned[std::abs(l)] = 1;
    long long best = -1, bestla = -1; int bestv = 0, ncand = 0;
    for (int v = 1; v <= nX; v++) {
      if (assigned[v]) continue;
      ncand++;
      long long sa = (1 + act.pos[v]) * (1 + act.neg[v]);
      if (sa < best) continue;
      long long n[2];
      for (int side = 0; side < 2; side++) {
        for (int l : cube) s.assume(l);
        s.assume(side ? -v : v);
        int rr = s.propagate();
        if (rr == 20) n[side] = 1000000;
        else { implied.clear(); s.implied(implied); n[side] = (long long) implied.size() - base; }
      }
      long long sc = (1 + n[0]) * (1 + n[1]);
      if (sa > best || sc > bestla) { best = sa; bestla = sc; bestv = v; }
    }
    std::printf("K %ld %d %.3f %d\n", id, bestv, now() - t0, ncand);
    std::fflush(stdout);
  }
  return 0;
}
