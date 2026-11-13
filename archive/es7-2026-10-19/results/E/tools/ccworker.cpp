// ccworker: persistent CaDiCaL cube worker for cnc2.py.
//
// Loads a DIMACS CNF once, freezes the orientation variables 1..nX (so they are never
// eliminated and can always be assumed or split on), then serves jobs from stdin:
//   "<id> <conflict_limit> <lit_1> ... <lit_k> 0"
// and answers on stdout with one line:
//   "U <id> <solve_ms>"            the CNF is UNSAT under the cube (solver claim)
//   "S <id> <solve_ms>"            SAT; the full model is written to <dir>/model-<id>.txt
//   "K <id> <solve_ms> <lit> <score> <ncand>"
//                                   budget exhausted; <lit> is an orientation variable chosen
//                                   by a restricted look-ahead (see below), 0 if none is free
//
// Split heuristic (orientation variables only): under the cube, unit-propagate; every free
// orientation variable x (not implied) is a candidate, or a deterministic pseudo-random sample
// of at most <max_cand> of them weighted toward frequent variables.  For each candidate,
// propagate cube+[x] and cube+[-x] and count newly implied literals n+ and n-.  A failed
// literal (conflict) wins immediately.  Otherwise pick the maximum of (n+ + 1)*(n- + 1).
//
// usage: ccworker cnf nX model_dir [max_cand] [--cadical-option=value ...]
#include "cadical.hpp"
#include <algorithm>
#include <cmath>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

static long long now_ms() {
  return std::chrono::duration_cast<std::chrono::milliseconds>(std::chrono::steady_clock::now().time_since_epoch()).count();
}

int main(int argc, char **argv) {
  if (argc < 4) { std::fprintf(stderr, "usage: ccworker cnf nX model_dir [max_cand]\n"); return 2; }
  int nX = std::atoi(argv[2]);
  std::string dir = argv[3];
  int max_cand = argc > 4 ? std::atoi(argv[4]) : 400;
  CaDiCaL::Solver s;
  s.set("quiet", 1);
  for (int i = 5; i < argc; i++)  // extra CaDiCaL options "--name=value"
    if (!s.set_long_option(argv[i])) { std::fprintf(stderr, "bad option %s\n", argv[i]); return 2; }
  int vars = 0;
  const char *err = s.read_dimacs(argv[1], vars, 1);
  if (err) { std::fprintf(stderr, "parse error: %s\n", err); return 2; }
  for (int v = 1; v <= nX; v++) s.freeze(v);
  // static occurrence counts of orientation variables (cheap re-read of the file)
  std::vector<long> occ(nX + 1, 0);
  {
    FILE *f = std::fopen(argv[1], "r");
    int c, sign = 1; long val = 0; bool num = false, comment = false;
    while ((c = std::fgetc(f)) != EOF) {
      if (comment) { if (c == '\n') comment = false; continue; }
      if (!num && (c == 'c' || c == 'p')) { comment = true; continue; }
      if (c == '-') { sign = -1; num = true; val = 0; continue; }
      if (c >= '0' && c <= '9') { val = val * 10 + (c - '0'); num = true; continue; }
      if (num) { long l = val; if (l && l <= nX) occ[l]++; sign = 1; val = 0; num = false; }
    }
    std::fclose(f);
    (void)sign;
  }
  std::printf("READY %d\n", vars); std::fflush(stdout);
  std::string line;
  unsigned long long rng = 0x9E3779B97F4A7C15ULL;
  while (std::getline(std::cin, line)) {
    std::istringstream in(line);
    long id; long long limit; in >> id >> limit;
    std::vector<int> cube; int lit;
    while (in >> lit && lit != 0) cube.push_back(lit);
    long long c0 = now_ms();
    for (int l : cube) s.assume(l);
    s.limit("conflicts", (int) std::min<long long>(limit, 2000000000LL));
    int res = s.solve();
    long long used = now_ms() - c0;  // solve wall time in ms
    if (res == 20) { std::printf("U %ld %lld\n", id, used); std::fflush(stdout); continue; }
    if (res == 10) {
      std::string path = dir + "/model-" + std::to_string(id) + ".txt";
      FILE *f = std::fopen(path.c_str(), "w");
      for (int v = 1; v <= vars; v++) std::fprintf(f, "%d\n", s.val(v) > 0 ? v : -v);
      std::fclose(f);
      std::printf("S %ld %lld\n", id, used); std::fflush(stdout);
      continue;
    }
    // restricted look-ahead on orientation variables
    for (int l : cube) s.assume(l);
    int pr = s.propagate();
    if (pr == 20) { std::printf("U %ld %lld\n", id, used); std::fflush(stdout); continue; }
    std::vector<int> base;
    if (pr == 0) s.implied(base);
    std::vector<char> assigned(nX + 1, 0);
    for (int l : base) if (std::abs(l) <= nX) assigned[std::abs(l)] = 1;
    for (int l : cube) if (std::abs(l) <= nX) assigned[std::abs(l)] = 1;
    std::vector<int> cand;
    for (int v = 1; v <= nX; v++) if (!assigned[v]) cand.push_back(v);
    int ncand_all = (int) cand.size();
    if ((int) cand.size() > max_cand) {
      // weighted sample without replacement: key = u^(1/w) (Efraimidis-Spirakis), top max_cand
      std::vector<std::pair<double, int>> key;
      for (int v : cand) {
        rng ^= rng << 13; rng ^= rng >> 7; rng ^= rng << 17;
        double u = ((rng >> 11) + 0.5) / 9007199254740992.0;
        key.push_back({std::pow(u, 1.0 / (double) (occ[v] + 1)), v});
      }
      std::partial_sort(key.begin(), key.begin() + max_cand, key.end(),
                        [](const std::pair<double, int> &a, const std::pair<double, int> &b) { return a.first > b.first; });
      cand.clear();
      for (int i = 0; i < max_cand; i++) cand.push_back(key[i].second);
    }
    size_t nb = base.size();
    int best = 0; double bestScore = -1;
    for (int v : cand) {
      long long n[2];
      bool failed = false;
      for (int side = 0; side < 2; side++) {
        int x = side ? -v : v;
        for (int l : cube) s.assume(l);
        s.assume(x);
        int r = s.propagate();
        if (r == 20) { failed = true; best = x; break; }
        std::vector<int> imp;
        if (r == 0) s.implied(imp);
        n[side] = (long long) imp.size() - (long long) nb;
      }
      if (failed) { bestScore = 1e300; break; }
      double sc = (double) (n[0] + 1) * (double) (n[1] + 1);
      if (sc > bestScore) { bestScore = sc; best = v; }
    }
    std::printf("K %ld %lld %d %.6g %d\n", id, used, best, bestScore, ncand_all);
    std::fflush(stdout);
  }
  return 0;
}
