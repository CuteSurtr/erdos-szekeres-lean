// Cube worker: loads a DIMACS CNF once, then reads jobs "id limit lit1 ... litk 0" from stdin.
// Replies "U id" (unsat under the cube), "S id" (sat; model written to model-<id>.txt),
// or "K id lit" (conflict limit hit; lit = lookahead split literal under the cube).
#include "cadical.hpp"
#include <cstdio>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
int main(int argc, char **argv) {
  if (argc < 2) { std::fprintf(stderr, "usage: worker cnf [model-dir]\n"); return 2; }
  std::string dir = argc > 2 ? argv[2] : ".";
  CaDiCaL::Solver s;
  s.set("quiet", 1);
  int vars = 0;
  const char *err = s.read_dimacs(argv[1], vars, 1);
  if (err) { std::fprintf(stderr, "parse error: %s\n", err); return 2; }
  std::printf("READY %d\n", vars); std::fflush(stdout);
  std::string line;
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
      for (int l : cube) s.assume(l);
      int split = s.lookahead();
      std::printf("K %ld %d\n", id, split);
    }
    std::fflush(stdout);
  }
  return 0;
}
