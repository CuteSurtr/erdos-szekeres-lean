// iCaDiCaL-style conquer worker for march_cu cubes.
// usage: icube CNF CUBES.icnf W w TLIM OUT.tsv [MODELDIR] [SKIPFILE]
// Loads CNF once into one incremental CaDiCaL solver and solves every cube with index
// idx = w (mod W) (idx = 0-based line number among "a ... 0" lines) as assumptions, with a
// wall-clock limit of TLIM seconds per cube (0 = none). Learned clauses are kept across cubes.
// Writes one line per cube:  idx <tab> U|S|T <tab> seconds <tab> conflicts
// (U = refuted, S = satisfiable (model to MODELDIR/model-idx.txt), T = time limit hit).
// SKIPFILE: optional file of indices already done (first column), skipped.
#include "cadical.hpp"
#include <chrono>
#include <cstdio>
#include <fstream>
#include <set>
#include <sstream>
#include <string>
#include <vector>
using clk = std::chrono::steady_clock;
struct Tim : CaDiCaL::Terminator {
  clk::time_point t0; double lim = 0;
  bool terminate() override {
    return lim > 0 && std::chrono::duration<double>(clk::now() - t0).count() > lim;
  }
};
int main(int argc, char **argv) {
  if (argc < 7) { std::fprintf(stderr, "usage: icube CNF CUBES W w TLIM OUT [MODELDIR] [SKIP]\n"); return 2; }
  int W = atoi(argv[3]), w = atoi(argv[4]); double tlim = atof(argv[5]);
  std::string mdir = argc > 7 ? argv[7] : ".";
  std::set<long> skip;
  if (argc > 8) { std::ifstream sf(argv[8]); long x; std::string rest;
    while (sf >> x) { skip.insert(x); std::getline(sf, rest); } }
  CaDiCaL::Solver s; s.set("quiet", 1);
  int vars = 0; const char *err = s.read_dimacs(argv[1], vars, 1);
  if (err) { std::fprintf(stderr, "parse error: %s\n", err); return 2; }
  Tim tm; tm.lim = tlim; s.connect_terminator(&tm);
  std::ifstream cf(argv[2]); FILE *out = std::fopen(argv[6], "a");
  std::string line; long idx = -1;
  while (std::getline(cf, line)) {
    if (line.empty() || line[0] != 'a') continue;
    idx++;
    if (idx % W != w || skip.count(idx)) continue;
    std::istringstream in(line.substr(1)); int lit; std::vector<int> cube;
    while (in >> lit && lit) cube.push_back(lit);
    for (int l : cube) s.assume(l);
    int64_t c0 = s.get_statistic_value("conflicts");
    tm.t0 = clk::now();
    int res = s.solve();
    double dt = std::chrono::duration<double>(clk::now() - tm.t0).count();
    int64_t c1 = s.get_statistic_value("conflicts");
    char r = res == 20 ? 'U' : res == 10 ? 'S' : 'T';
    if (res == 10) {
      std::string p = mdir + "/model-" + std::to_string(idx) + ".txt";
      FILE *f = std::fopen(p.c_str(), "w");
      for (int v = 1; v <= vars; v++) std::fprintf(f, "%d\n", s.val(v) > 0 ? v : -v);
      std::fclose(f);
    }
    std::fprintf(out, "%ld\t%c\t%.3f\t%lld\n", idx, r, dt, (long long)(c1 - c0)); std::fflush(out);
  }
  std::fclose(out); return 0;
}
