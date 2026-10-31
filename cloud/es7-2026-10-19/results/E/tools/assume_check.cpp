// assume_check: load a CNF once into CaDiCaL; for every line of signed literals in a file,
// solve under those literals as assumptions and print SAT/UNSAT (used to check that saved
// projected models extend to models of a CNF).
// usage: assume_check cnf lines.txt
#include "cadical.hpp"
#include <cstdio>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
int main(int argc, char **argv) {
  if (argc < 3) { std::fprintf(stderr, "usage: assume_check cnf lines\n"); return 2; }
  CaDiCaL::Solver s;
  s.set("quiet", 1);
  int vars = 0;
  const char *err = s.read_dimacs(argv[1], vars, 1);
  if (err) { std::fprintf(stderr, "parse error: %s\n", err); return 2; }
  std::ifstream in(argv[2]);
  std::string line;
  int n = 0, nsat = 0;
  while (std::getline(in, line)) {
    std::istringstream ss(line);
    std::vector<int> a; int l;
    while (ss >> l) if (l) a.push_back(l);
    if (a.empty()) continue;
    for (int x : a) s.assume(x);
    int r = s.solve();
    n++; nsat += (r == 10);
    std::printf("line %d lits %zu result %s\n", n, a.size(), r == 10 ? "SAT" : r == 20 ? "UNSAT" : "UNKNOWN");
  }
  std::printf("TOTAL lines=%d sat=%d\n", n, nsat);
  return 0;
}
