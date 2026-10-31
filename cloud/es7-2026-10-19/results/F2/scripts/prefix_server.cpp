// Prefix-extendability oracle for an ETV signotope CNF on N points (gen_etv.py numbering).
// usage: prefix_server CNF N SEED CONFLICT_LIMIT
// stdin lines: "k i_1 .. i_k bits": realized points at positions i_1 < .. < i_k of 1..N, bits =
// C(k,3) chars '0'/'1' for their triples (lex order over the k points, '1' = ccw).  Those triples
// are assumed (as X(i_a, i_b, i_c)), the CNF is
// solved under the conflict limit, and one line is printed: SAT, UNSAT or UNKNOWN.  Learned
// clauses stay valid because the prefix is passed only as assumptions.
#include "cadical.hpp"
#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
int main(int argc, char** argv) {
  int N = atoi(argv[2]); long climit = atol(argv[4]);
  vector<int> idx((N+1)*(N+1)*(N+1), 0); int nx = 0;
  for (int i=1;i<=N;i++) for (int j=i+1;j<=N;j++) for (int k=j+1;k<=N;k++) idx[(i*(N+1)+j)*(N+1)+k] = ++nx;
  CaDiCaL::Solver S; S.set("quiet", 1); S.set("seed", atoi(argv[3])); S.set("lucky", 0); srand(atoi(argv[3]));
  int vars; const char* err = S.read_dimacs(argv[1], vars, 1);
  if (err) { fprintf(stderr, "%s\n", err); return 1; }
  string line;
  while (getline(cin, line)) {
    // a line starting with "M " additionally randomises the decision phases of the X variables and
    // prints the model's X values (C(N,3) chars) after SAT
    bool wantm = line.size() > 2 && line[0] == 'M' && line[1] == ' ';
    if (wantm) { line = line.substr(2); for (int x = 1; x <= nx; x++) S.phase((rand() & 1) ? x : -x); }
    istringstream is(line); int k; is >> k; vector<int> P(k); for (int& p : P) is >> p;
    string bits; is >> bits;
    int v = 0;
    for (int a=0;a<k;a++) for (int b=a+1;b<k;b++) for (int c=b+1;c<k;c++) {
      int x = idx[(P[a]*(N+1)+P[b])*(N+1)+P[c]]; S.assume(bits[v++]=='1' ? x : -x); }
    if (climit > 0) S.limit("conflicts", climit);
    int r = S.solve();
    printf("%s\n", r == 10 ? "SAT" : r == 20 ? "UNSAT" : "UNKNOWN");
    if (wantm && r == 10) { string m(nx, '0'); for (int x = 1; x <= nx; x++) if (S.val(x) > 0) m[x-1] = '1'; printf("%s\n", m.c_str()); }
    fflush(stdout);
  }
}
