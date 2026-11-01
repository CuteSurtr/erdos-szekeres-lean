// cnfeval: evaluate a symmetric no-K-gon CNF under a fixed assignment of the orientation
// variables 1..nX, without a SAT solver.
//
// The non-orientation ("aux") variables of symcnf.py / d3cnf.py CNFs only occur in
//   definitional clauses  (premises -> v), exactly one positive aux literal v, and
//   negative clauses      (all aux literals negative, no orientation literal) = K-set clauses.
// Under a fixed orientation assignment the aux part is Horn, so the least model (forward
// chaining of the definitional clauses from all-false) decides satisfiability exactly:
// the CNF restricted to the assignment is SAT iff the least model satisfies every clause.
//
// For each assignment line the tool prints
//   xonly_violated=<#clauses over orientation variables only that are false>
//   level counts of true aux variables in the least model (level r = r-subset convexity flag;
//     level 4 = defined from orientation literals, level r>4 = defined from r aux literals)
//   kfalse=<#negative aux clauses falsified by the least model>
//   sat=<0|1>
// It also checks the clause-shape assumptions above and reports violations.
//
// usage: cnfeval cnf nX assignments.txt   (one line of nX signed literals per sample)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <vector>
#include <string>
#include <fstream>
#include <sstream>
#include <iostream>

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: cnfeval cnf nX assignments\n"); return 2; }
  int nX = atoi(argv[2]);
  FILE *f = fopen(argv[1], "r");
  if (!f) { perror("cnf"); return 2; }
  int nv = 0; long nc = 0;
  std::vector<int> lits; std::vector<long> start;
  {
    char buf[1 << 16];
    // fast token reader
    int c; bool inComment = false; int sign = 1; long val = 0; bool inNum = false;
    bool header = false;
    std::string hdr;
    start.push_back(0);
    while ((c = fgetc(f)) != EOF) {
      if (inComment) { if (c == '\n') inComment = false; continue; }
      if (!inNum && (c == 'c')) { inComment = true; continue; }
      if (!inNum && c == 'p') {
        if (!fgets(buf, sizeof buf, f)) break;
        sscanf(buf, " cnf %d %ld", &nv, &nc);
        header = true; continue;
      }
      if (c == '-') { sign = -1; inNum = true; val = 0; continue; }
      if (c >= '0' && c <= '9') { val = val * 10 + (c - '0'); inNum = true; continue; }
      if (inNum) {
        int l = (int)(sign * val);
        if (l == 0) start.push_back((long)lits.size());
        else lits.push_back(l);
        sign = 1; val = 0; inNum = false;
      }
    }
    if (inNum) { int l = (int)(sign * val); if (l == 0) start.push_back((long)lits.size()); else lits.push_back(l); }
    (void)header;
  }
  fclose(f);
  long ncl = (long)start.size() - 1;
  fprintf(stderr, "parsed vars=%d clauses=%ld (header %ld)\n", nv, ncl, nc);
  // classify clauses
  std::vector<char> kind(ncl);  // 0 xonly, 1 definitional, 2 negative-aux (K-set), 3 other
  std::vector<int> head(ncl, 0);
  std::vector<int> level(nv + 1, 0);
  long shape_bad = 0, nK = 0, nDef = 0, nXo = 0;
  std::vector<std::vector<long>> occNeg(nv + 1);  // aux var -> definitional clauses where it is a premise
  for (long i = 0; i < ncl; i++) {
    int posAux = 0, negAux = 0, xl = 0, h = 0;
    for (long j = start[i]; j < start[i + 1]; j++) {
      int l = lits[j], v = abs(l);
      if (v <= nX) xl++;
      else if (l > 0) { posAux++; h = v; }
      else negAux++;
    }
    if (posAux == 0 && negAux == 0) { kind[i] = 0; nXo++; }
    else if (posAux == 1) {
      kind[i] = 1; head[i] = h; nDef++;
      int lev = (negAux == 0) ? 4 : negAux;
      if (negAux > 0 && xl > 0) shape_bad++;
      if (level[h] && level[h] != lev) shape_bad++;
      level[h] = lev;
      for (long j = start[i]; j < start[i + 1]; j++) if (lits[j] < 0 && -lits[j] > nX) occNeg[-lits[j]].push_back(i);
    } else if (posAux == 0 && xl == 0) { kind[i] = 2; nK++; }
    else { kind[i] = 3; shape_bad++; }
  }
  std::map<int, long> levCount;
  for (int v = nX + 1; v <= nv; v++) levCount[level[v]]++;
  fprintf(stderr, "xonly=%ld definitional=%ld kclauses=%ld shape_bad=%ld\n", nXo, nDef, nK, shape_bad);
  for (auto &p : levCount) fprintf(stderr, "  aux level %d: %ld vars\n", p.first, p.second);
  std::ifstream in(argv[3]);
  std::string line; int sample = 0;
  while (std::getline(in, line)) {
    if (line.empty()) continue;
    std::istringstream ss(line);
    std::vector<signed char> val(nv + 1, 0);  // 1 true, -1 false
    int l, cnt = 0;
    while (ss >> l) { if (l == 0) break; if (abs(l) <= nX) { val[abs(l)] = l > 0 ? 1 : -1; cnt++; } }
    long missing = 0; for (int v = 1; v <= nX; v++) if (!val[v]) missing++;
    auto litTrue = [&](int x) { return (x > 0) ? val[x] == 1 : val[-x] == 1 ? false : true; };
    // least model: aux false initially; forward chaining with counters
    std::vector<int> need(ncl, 0);
    std::vector<int> queue;
    for (int v = nX + 1; v <= nv; v++) val[v] = -1;
    for (long i = 0; i < ncl; i++) if (kind[i] == 1) {
      int n = 0; bool sat = false;
      for (long j = start[i]; j < start[i + 1]; j++) {
        int x = lits[j], v = abs(x);
        if (v <= nX) { if ((x > 0) == (val[v] == 1)) sat = true; }
        else if (x < 0) n++;  // premise aux var must become true
      }
      if (sat) { need[i] = -1; continue; }
      need[i] = n;
      if (n == 0 && val[head[i]] != 1) { val[head[i]] = 1; queue.push_back(head[i]); }
    }
    while (!queue.empty()) {
      int v = queue.back(); queue.pop_back();
      for (long i : occNeg[v]) if (need[i] > 0) {
        if (--need[i] == 0 && val[head[i]] != 1) { val[head[i]] = 1; queue.push_back(head[i]); }
      }
    }
    long xviol = 0, kfalse = 0, other = 0;
    for (long i = 0; i < ncl; i++) {
      bool sat = false;
      for (long j = start[i]; j < start[i + 1]; j++) { int x = lits[j]; if ((x > 0) == (val[abs(x)] == 1)) { sat = true; break; } }
      if (!sat) { if (kind[i] == 0) xviol++; else if (kind[i] == 2) kfalse++; else other++; }
    }
    std::map<int, long> tru;
    for (int v = nX + 1; v <= nv; v++) if (val[v] == 1) tru[level[v]]++;
    printf("sample=%d assigned=%d missing=%ld xonly_violated=%ld", sample, cnt, missing, xviol);
    for (auto &p : tru) printf(" true_level%d=%ld", p.first, p.second);
    printf(" kfalse=%ld other_false=%ld sat=%d\n", kfalse, other, (xviol == 0 && kfalse == 0 && other == 0) ? 1 : 0);
    fflush(stdout);
    sample++;
    (void)litTrue;
  }
  return 0;
}
