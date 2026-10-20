// Incremental cube solver (iCaDiCaL style) for march_cu cube files.
//   iworker CNF CUBES.icnf WID NW TLIM_S NX OUTDIR [SEED]
// Loads CNF once into one CaDiCaL instance, then solves each assigned cube as assumptions,
// keeping learned clauses between cubes. Cube i (0-based, file order) goes to this worker iff
// perm[i] % NW == WID, where perm is a seeded random permutation, so every worker sees a
// uniform random sample of the cubes (makes the running projection unbiased).
// Per cube a wall-clock limit TLIM_S applies (0 = none); a cube that hits it is reported
// as UNKNOWN (censored). Log line per cube: "id res secs" with res in U/S/T.
// On SAT the orientation literals 1..NX are written to OUTDIR/model-<id>.txt.
#include "cadical.hpp"
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <random>
#include <sstream>
#include <string>
#include <vector>
static double now() {
  using namespace std::chrono;
  return duration<double>(steady_clock::now().time_since_epoch()).count();
}
struct Deadline : CaDiCaL::Terminator {
  double end = 0;
  bool terminate() override { return end > 0 && now() > end; }
};
int main(int argc, char **argv) {
  if (argc < 8) { fprintf(stderr, "usage\n"); return 1; }
  const char *cnf = argv[1], *cubes = argv[2];
  int wid = atoi(argv[3]), nw = atoi(argv[4]);
  double tlim = atof(argv[5]);
  int nX = atoi(argv[6]);
  std::string outdir = argv[7];
  unsigned seed = argc > 8 ? atoi(argv[8]) : 1;
  std::vector<std::vector<int>> C;
  std::ifstream in(cubes);
  std::string line;
  while (std::getline(in, line)) {
    if (line.empty() || line[0] != 'a') continue;
    std::istringstream ss(line.substr(1));
    std::vector<int> c; int l;
    while (ss >> l && l) c.push_back(l);
    C.push_back(c);
  }
  std::vector<int> perm(C.size());
  for (size_t i = 0; i < C.size(); i++) perm[i] = i;
  std::mt19937 rng(seed);
  std::shuffle(perm.begin(), perm.end(), rng);
  // perm is the processing order; worker takes positions p with p % nw == wid
  CaDiCaL::Solver S;
  int maxvar;
  const char *err = S.read_dimacs(cnf, maxvar);
  if (err) { fprintf(stderr, "parse: %s\n", err); return 1; }
  Deadline D; S.connect_terminator(&D);
  std::string logp = outdir + "/w" + std::to_string(wid) + ".log";
  FILE *log = fopen(logp.c_str(), "a");
  fprintf(log, "# start total_cubes=%zu wid=%d nw=%d tlim=%g t=%.3f\n", C.size(), wid, nw, tlim, now());
  fflush(log);
  for (size_t p = wid; p < perm.size(); p += nw) {
    int id = perm[p];
    for (int l : C[id]) S.assume(l);
    double t0 = now();
    D.end = tlim > 0 ? t0 + tlim : 0;
    int r = S.solve();
    double dt = now() - t0;
    char rc = r == 20 ? 'U' : r == 10 ? 'S' : 'T';
    if (r == 10) {
      std::string mp = outdir + "/model-" + std::to_string(id) + ".txt";
      FILE *m = fopen(mp.c_str(), "w");
      for (int v = 1; v <= nX; v++) fprintf(m, "%d ", S.val(v) > 0 ? v : -v);
      fprintf(m, "\n"); fclose(m);
    }
    fprintf(log, "%d %c %.3f %.3f\n", id, rc, dt, now());
    fflush(log);
  }
  fprintf(log, "# done t=%.3f\n", now());
  fclose(log);
  return 0;
}
