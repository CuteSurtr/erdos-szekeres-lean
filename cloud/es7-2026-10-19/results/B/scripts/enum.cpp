// Count models of a CNF projected onto variables 1..nX (blocking clauses), and how many of
// them are fixed by the x-reflection rho(i,j,k) = (N+1-k, N+1-j, N+1-i).
// usage: enum cnf N [cap]   -> prints {"models": m, "fixed": f, "complete": bool}
#include "cadical.hpp"
#include <cstdio>
#include <cstdlib>
#include <map>
#include <tuple>
#include <vector>
int main(int argc, char **argv) {
  if (argc < 3) return 2;
  int N = atoi(argv[2]);
  long cap = argc > 3 ? atol(argv[3]) : 1000000;
  CaDiCaL::Solver s;
  int vars = 0;
  const char *err = s.read_dimacs(argv[1], vars, 1);
  if (err) { fprintf(stderr, "%s\n", err); return 2; }
  std::map<std::tuple<int, int, int>, int> idx;
  std::vector<std::tuple<int, int, int>> tri;
  int n = 0;
  for (int i = 1; i <= N; i++) for (int j = i + 1; j <= N; j++) for (int k = j + 1; k <= N; k++) {
    idx[{i, j, k}] = ++n; tri.push_back({i, j, k});
  }
  std::vector<int> rho(n + 1);
  for (int v = 1; v <= n; v++) { auto [i, j, k] = tri[v - 1]; rho[v] = idx[{N + 1 - k, N + 1 - j, N + 1 - i}]; }
  long models = 0, fixed = 0;
  bool complete = false;
  while (models < cap) {
    int r = s.solve();
    if (r == 20) { complete = true; break; }
    if (r != 10) break;
    models++;
    std::vector<int> val(n + 1);
    for (int v = 1; v <= n; v++) val[v] = s.val(v) > 0 ? 1 : 0;
    bool fx = true;
    for (int v = 1; v <= n && fx; v++) if (val[v] != val[rho[v]]) fx = false;
    fixed += fx;
    for (int v = 1; v <= n; v++) s.add(val[v] ? -v : v);
    s.add(0);
  }
  printf("{\"models\": %ld, \"fixed\": %ld, \"complete\": %s}\n", models, fixed, complete ? "true" : "false");
  return 0;
}
