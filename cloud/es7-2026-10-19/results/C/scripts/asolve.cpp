// asolve: load a DIMACS CNF once, then solve it under each line of assumptions read
// from stdin ("lit lit ... 0" or just literals per line).  Prints "<lineno> SAT|UNSAT".
// With argv[2] given, the model of every SAT answer is appended to that file
// (one line of signed literals per model).  Used for the encoding validations.
#include "cadical.hpp"
#include <cstdio>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
int main(int argc, char **argv) {
  if (argc < 2) { std::fprintf(stderr, "usage: asolve cnf [models-out] < assumptions\n"); return 2; }
  CaDiCaL::Solver s;
  s.set("quiet", 1);
  int vars = 0;
  const char *err = s.read_dimacs(argv[1], vars, 1);
  if (err) { std::fprintf(stderr, "parse error: %s\n", err); return 2; }
  FILE *mf = argc > 2 ? std::fopen(argv[2], "a") : nullptr;
  std::string line; long n = 0;
  while (std::getline(std::cin, line)) {
    n++;
    std::istringstream in(line); int lit;
    while (in >> lit && lit != 0) s.assume(lit);
    int res = s.solve();
    std::printf("%ld %s\n", n, res == 10 ? "SAT" : res == 20 ? "UNSAT" : "UNKNOWN");
    if (res == 10 && mf) {
      for (int v = 1; v <= vars; v++) std::fprintf(mf, "%d ", s.val(v) > 0 ? v : -v);
      std::fprintf(mf, "0\n");
    }
    std::fflush(stdout);
  }
  if (mf) std::fclose(mf);
  return 0;
}
