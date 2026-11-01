// Diversified model generator for an ETV signotope CNF (tools/etv/gen_etv.py numbering:
// X(i,j,k), i<j<k, variables 1..C(N,3) lexicographic, true = ccw).
// usage: gen_models CNF N COUNT SEED MODE > models.txt
//   MODE 0: uniform random phases on X variables
//   MODE 1: phases = orientations of a random point set (mixture of families), so that the
//           solver starts from a realizable chirotope and repairs it
//   MODE 2: alternate 0/1
// Each model is printed as one line of C(N,3) chars '0'/'1' (X value), and a blocking clause on
// the X variables is added, so models from one process are pairwise distinct.
#include "cadical.hpp"
#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <vector>
#include <random>
#include <algorithm>
#include <array>
#include <string>
using namespace std;
int main(int argc, char** argv) {
  if (argc < 6) { fprintf(stderr, "usage\n"); return 1; }
  const char* cnf = argv[1]; int N = atoi(argv[2]); long cnt = atol(argv[3]);
  unsigned seed = atoi(argv[4]); int mode = atoi(argv[5]);
  CaDiCaL::Solver S;
  S.set("quiet", 1); S.set("seed", seed); S.set("lucky", 0); S.set("rephase", 0); S.set("shuffle", 1);
  S.set("shufflerandom", 1);
  int vars;
  const char* err = S.read_dimacs(cnf, vars, 1);
  if (err) { fprintf(stderr, "%s\n", err); return 1; }
  vector<int> T; int nx = N*(N-1)*(N-2)/6;
  vector<array<int,3>> tr;
  for (int i=0;i<N;i++) for (int j=i+1;j<N;j++) for (int k=j+1;k<N;k++) tr.push_back({i,j,k});
  mt19937_64 rng(seed * 7919ULL + 17);
  uniform_real_distribution<double> U(0,1);
  normal_distribution<double> G(0,1);
  for (long it = 0; it < cnt; it++) {
    int md = mode == 2 ? (it & 1) : mode;
    vector<int> ph(nx);
    if (md == 0) { for (int v=0; v<nx; v++) ph[v] = (rng()&1) ? 1 : -1; }
    else {
      vector<pair<double,double>> P(N);
      int fam = rng() % 4;
      for (int i=0;i<N;i++) {
        double x, y;
        if (fam == 0) { x = U(rng); y = U(rng); }
        else if (fam == 1) { // multiscale clusters
          int c = rng() % 4; double r = exp(-6*U(rng));
          x = c*0.3 + r*G(rng); y = (c*c%5)*0.2 + r*G(rng); }
        else if (fam == 2) { // noisy parabola-ish (both signs) -> long caps/cups get broken by the solver
          x = U(rng); double s = (rng()&1)?1:-1; y = s*x*x*0.5 + 0.2*G(rng); }
        else { x = G(rng); y = G(rng)*exp(2*G(rng)); }
        P[i] = {x, y};
      }
      sort(P.begin(), P.end());
      for (int v=0; v<nx; v++) { auto& t = tr[v];
        double d = (P[t[1]].first-P[t[0]].first)*(P[t[2]].second-P[t[0]].second)
                 - (P[t[1]].second-P[t[0]].second)*(P[t[2]].first-P[t[0]].first);
        ph[v] = d > 0 ? 1 : -1; }
    }
    for (int v=0; v<nx; v++) S.phase(ph[v]*(v+1));
    int r = S.solve();
    if (r != 10) { fprintf(stderr, "solve returned %d at %ld\n", r, it); break; }
    string line(nx, '0');
    for (int v=0; v<nx; v++) { if (S.val(v+1) > 0) line[v] = '1'; }
    printf("%s\n", line.c_str()); fflush(stdout);
    for (int v=0; v<nx; v++) S.add(line[v]=='1' ? -(v+1) : (v+1));
    S.add(0);
  }
  return 0;
}
