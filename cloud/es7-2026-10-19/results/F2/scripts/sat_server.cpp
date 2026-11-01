// Phase-guided model server for an ETV signotope CNF (gen_etv.py numbering, true = ccw).
// usage: sat_server CNF N SEED [MAXIT] ; then each stdin line of C(N,3) '0'/'1' chars is used as the
// decision phase of the X variables (forcephase), the CNF is solved, and the model's X values are
// printed as one line of '0'/'1'.  No blocking clauses: the same formula every call.
#include "cadical.hpp"
#include <cstdio>
#include <cstdlib>
#include <string>
#include <iostream>
#include <vector>
using namespace std;
int main(int argc, char** argv) {
  int N = atoi(argv[2]); int maxit = argc > 4 ? atoi(argv[4]) : 0; int nx = N*(N-1)*(N-2)/6;
  CaDiCaL::Solver S;
  S.set("quiet", 1); S.set("seed", atoi(argv[3])); S.set("lucky", 0); S.set("rephase", 0);
  S.set("forcephase", 1);
  int vars; const char* err = S.read_dimacs(argv[1], vars, 1);
  if (err) { fprintf(stderr, "%s\n", err); return 1; }
  string line;
  while (getline(cin, line)) {
    if ((int)line.size() < nx) continue;
    for (int v=0; v<nx; v++) S.phase(line[v]=='1' ? (v+1) : -(v+1));
    // assumption mode: assume every phase literal, drop the failed ones, repeat (keeps the model
    // close to the hint); after 'maxit' rounds fall back to phases only
    // optional second token: mask of the literals to assume ('1' = assume); default all
    bool hasmask = (int)line.size() >= 2*nx+1;
    vector<int> A; for (int v=0; v<nx; v++) if (!hasmask || line[nx+1+v]=='1') A.push_back(line[v]=='1' ? (v+1) : -(v+1));
    int r = 0, it = 0;
    for (; it < maxit; it++) {
      for (int l : A) S.assume(l);
      r = S.solve();
      if (r == 10) break;
      vector<int> B; for (int l : A) if (!S.failed(l)) B.push_back(l);
      if (B.size() == A.size()) break;
      A.swap(B);
    }
    if (r != 10) r = S.solve();
    if (r != 10) { printf("UNSAT %d\n", r); fflush(stdout); continue; }
    string out(nx, '0');
    for (int v=0; v<nx; v++) if (S.val(v+1) > 0) out[v] = '1';
    printf("%s\n", out.c_str()); fflush(stdout);
  }
}
