// Incremental abstract-extension tester on top of the CaDiCaL library.
//
// The base CNF (tools/trackB/gen_cnf.py M K, no symmetry breaking) is loaded once. Variables
// X(i,j,k), 1<=i<j<k<=M, are 1..C(M,3) in lexicographic order (true = counterclockwise).
// Every job fixes the triples of an "old" signotope on N points, mapped into 1..M, through
// assumptions only, so learned clauses stay valid for every later job.
//
// usage: ext_solve BASE.cnf M CONFLICT_LIMIT [option=value ...] < jobs > results
//   jobs:
//     S <label> <N> <signs>   current old signotope (signs: C(N,3) chars '+'/'-', lex order)
//     P <p>                   one-point insertion at x-position p (needs M == N+1); old point a
//                             goes to the a-th index of 1..M other than p (as in ext_cnf.py)
//     J <tag> m_1 ... m_N     general map: old point a -> new index m_a (strictly increasing)
//   output (one R line per solve, plus a W line with the full M-point model when SAT):
//     R <label> <tag> SAT|UNSAT|UNKNOWN <conflicts> <decisions> <milliseconds>
//     W <label> <tag> <signs of the C(M,3) triples of the model>
#include "cadical.hpp"

#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

static int M;
static std::vector<int> tidx;  // (i,j,k) -> var, flattened (M+1)^3

static inline int &T(int i, int j, int k) { return tidx[((size_t)i * (M + 1) + j) * (M + 1) + k]; }

int main(int argc, char **argv) {
  if (argc < 4) {
    std::fprintf(stderr, "usage: ext_solve BASE.cnf M CONFLICT_LIMIT [option=value ...] < jobs\n");
    return 2;
  }
  const char *cnf = argv[1];
  M = std::atoi(argv[2]);
  int climit = std::atoi(argv[3]);
  tidx.assign((size_t)(M + 1) * (M + 1) * (M + 1), 0);
  int nX = 0;
  for (int i = 1; i <= M; i++)
    for (int j = i + 1; j <= M; j++)
      for (int k = j + 1; k <= M; k++) T(i, j, k) = ++nX;

  CaDiCaL::Solver solver;
  solver.set("quiet", 1);
  for (int a = 4; a < argc; a++) {  // optional CaDiCaL options, e.g. lucky=0
    std::string kv = argv[a];
    size_t eq = kv.find('=');
    if (eq == std::string::npos || !solver.set(kv.substr(0, eq).c_str(), std::atoi(kv.c_str() + eq + 1))) {
      std::fprintf(stderr, "bad option %s\n", argv[a]);
      return 2;
    }
  }
  int vars = 0;
  const char *err = solver.read_dimacs(cnf, vars, 1);
  if (err) {
    std::fprintf(stderr, "read_dimacs: %s\n", err);
    return 2;
  }
  if (vars < nX) {
    std::fprintf(stderr, "CNF has %d vars < C(M,3) = %d\n", vars, nX);
    return 2;
  }
  for (int v = 1; v <= nX; v++) solver.freeze(v);  // keep X variables out of elimination
  std::fprintf(stderr, "loaded %s: %d vars, C(M,3)=%d\n", cnf, vars, nX);

  std::string label, signs;
  int N = 0;
  std::vector<int> oi, oj, ok;  // old triples in lex order
  std::string line;
  std::ios::sync_with_stdio(false);
  while (std::getline(std::cin, line)) {
    if (line.empty()) continue;
    std::istringstream in(line);
    std::string cmd;
    in >> cmd;
    if (cmd == "S") {
      in >> label >> N >> signs;
      size_t expect = (size_t)N * (N - 1) * (N - 2) / 6;
      if (signs.size() != expect || N > M) {
        std::fprintf(stderr, "bad S line for %s\n", label.c_str());
        return 2;
      }
      oi.clear(); oj.clear(); ok.clear();
      for (int i = 1; i <= N; i++)
        for (int j = i + 1; j <= N; j++)
          for (int k = j + 1; k <= N; k++) { oi.push_back(i); oj.push_back(j); ok.push_back(k); }
      continue;
    }
    std::vector<int> map(N + 1, 0);
    std::string tag;
    if (cmd == "P") {
      int p;
      in >> p;
      if (M != N + 1 || p < 1 || p > M) { std::fprintf(stderr, "bad P\n"); return 2; }
      int a = 0;
      for (int t = 1; t <= M; t++) if (t != p) map[++a] = t;
      tag = "p" + std::to_string(p);
    } else if (cmd == "J") {
      in >> tag;
      for (int a = 1; a <= N; a++) in >> map[a];
      for (int a = 1; a <= N; a++)
        if (map[a] < 1 || map[a] > M || (a > 1 && map[a] <= map[a - 1])) {
          std::fprintf(stderr, "bad J map\n");
          return 2;
        }
    } else {
      std::fprintf(stderr, "unknown command %s\n", cmd.c_str());
      return 2;
    }
    for (size_t t = 0; t < signs.size(); t++) {
      int v = T(map[oi[t]], map[oj[t]], map[ok[t]]);
      solver.assume(signs[t] == '+' ? v : -v);
    }
    int64_t c0 = solver.get_statistic_value("conflicts");
    int64_t d0 = solver.get_statistic_value("decisions");
    if (climit > 0) solver.limit("conflicts", climit);
    auto t0 = std::chrono::steady_clock::now();
    int res = solver.solve();
    double ms = std::chrono::duration<double, std::milli>(std::chrono::steady_clock::now() - t0).count();
    int64_t c1 = solver.get_statistic_value("conflicts");
    int64_t d1 = solver.get_statistic_value("decisions");
    const char *st = res == 10 ? "SAT" : res == 20 ? "UNSAT" : "UNKNOWN";
    std::printf("R %s %s %s %lld %lld %.1f\n", label.c_str(), tag.c_str(), st, (long long)(c1 - c0),
                (long long)(d1 - d0), ms);
    if (res == 10) {
      std::string w(nX, '?');
      for (int v = 1; v <= nX; v++) w[v - 1] = solver.val(v) > 0 ? '+' : '-';
      // the old triples must come back exactly as assumed
      for (size_t t = 0; t < signs.size(); t++) {
        int v = T(map[oi[t]], map[oj[t]], map[ok[t]]);
        if (w[v - 1] != signs[t]) { std::fprintf(stderr, "model disagrees with assumption\n"); return 3; }
      }
      std::printf("W %s %s %s\n", label.c_str(), tag.c_str(), w.c_str());
    }
    std::fflush(stdout);
  }
  return 0;
}
