// Cube worker for cnc2.py.
// usage: cnc_worker CNF NSPLIT OUTDIR
//   NSPLIT: variables 1..NSPLIT are the only split candidates (orientation variables X).
// The CNF is parsed once into memory. Jobs on stdin, one per line:
//   J id conflicts proof(0/1) lit1 ... litk 0
//     Fresh CaDiCaL solver reading (via its DIMACS parser) the base clauses in file order, then the cube literals as unit clauses
//     (so original clause ids are 1..m for the file and m+1..m+k for the cube units).
//     If proof=1, an ASCII LRAT proof is written to OUTDIR/p<id>.lrat.
//     Replies:
//       U id conflicts cpu            (UNSAT; proof file complete if requested)
//       S id conflicts cpu            (SAT; model in OUTDIR/model-<id>.txt)
//       K id conflicts cpu var score  (budget hit; var = split variable chosen by lookahead
//                                      on orientation variables; proof file deleted)
//       F id conflicts cpu var        (budget hit and unit propagation alone refutes the cube:
//                                      var=0; should not happen since the solver would close it)
//   L id lit1 ... litk 0
//     Lookahead only: reply "L id var score cpu" (var = 0 if unit propagation refutes the cube).
//   A id lit1 ... litk 0
//     Persistent incremental solver (no proof): solve under assumptions; reply "AU id"/"AS id".
// Lookahead: unit propagation (two watched literals) of cube; for each free orientation variable
// x, propagate x and -x; score = (t+1)*(f+1) with t,f = newly assigned variables; a failed
// literal (conflict on one side) is returned immediately (that child closes by propagation).
#include "cadical.hpp"
#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <ctime>
#include <iostream>
#include <sstream>
#include <string>
#include <vector>

static int nvars = 0, nsplit = 0;
static std::vector<std::vector<int>> clauses;
static std::string body;  // clause lines of the CNF, regenerated in canonical form

// ---------------- unit propagation engine for lookahead ----------------
struct UP {
  std::vector<std::vector<int>> cls;       // copies with watched literals at 0,1
  std::vector<std::vector<int>> watches;   // index by lit code
  std::vector<signed char> val;            // by var: 0 unassigned, 1 true, -1 false
  std::vector<int> trail;
  std::vector<int> units;                  // unit clauses of the CNF
  size_t qhead = 0;
  static int code(int lit) { return lit > 0 ? 2 * lit : 2 * (-lit) + 1; }
  int value(int lit) const { int v = val[std::abs(lit)]; return lit > 0 ? v : -v; }
  void init() {
    val.assign(nvars + 1, 0);
    watches.assign(2 * nvars + 2, {});
    for (auto &c : clauses) {
      if (c.size() == 1) { units.push_back(c[0]); continue; }
      if (c.empty()) continue;
      int idx = cls.size();
      cls.push_back(c);
      watches[code(-c[0])].push_back(idx);
      watches[code(-c[1])].push_back(idx);
    }
  }
  bool assign(int lit) {
    int v = value(lit);
    if (v == 1) return true;
    if (v == -1) return false;
    val[std::abs(lit)] = lit > 0 ? 1 : -1;
    trail.push_back(lit);
    return true;
  }
  // returns false on conflict
  bool propagate() {
    while (qhead < trail.size()) {
      int lit = trail[qhead++];
      auto &ws = watches[code(lit)];  // clauses watching -lit... we index by code(-watched)
      size_t i = 0, j = 0;
      bool conflict = false;
      for (; i < ws.size(); i++) {
        int ci = ws[i];
        if (conflict) { ws[j++] = ci; continue; }
        auto &c = cls[ci];
        if (c[0] == -lit) std::swap(c[0], c[1]);
        // now c[1] == -lit (false)
        if (value(c[0]) == 1) { ws[j++] = ci; continue; }
        bool moved = false;
        for (size_t k = 2; k < c.size(); k++) {
          if (value(c[k]) != -1) {
            std::swap(c[1], c[k]);
            watches[code(-c[1])].push_back(ci);
            moved = true;
            break;
          }
        }
        if (moved) continue;
        ws[j++] = ci;
        if (value(c[0]) == -1) { conflict = true; continue; }
        assign(c[0]);
      }
      ws.resize(j);
      if (conflict) return false;
    }
    return true;
  }
  void backtrack(size_t mark) {
    while (trail.size() > mark) { val[std::abs(trail.back())] = 0; trail.pop_back(); }
    qhead = mark;
  }
};

static UP up;

// returns split var (>0), or 0 if the cube is refuted by propagation
static int lookahead(const std::vector<int> &cube, double &best_score) {
  up.backtrack(0);
  bool ok = true;
  for (int u : up.units) ok = ok && up.assign(u);
  for (int l : cube) ok = ok && up.assign(l);
  ok = ok && up.propagate();
  if (!ok) { up.backtrack(0); best_score = -1; return 0; }
  size_t base = up.trail.size();
  int best = 0; best_score = -1;
  for (int x = 1; x <= nsplit; x++) {
    if (up.val[x] != 0) continue;
    up.assign(x);
    bool okp = up.propagate();
    long t = (long)(up.trail.size() - base);
    up.backtrack(base);
    if (!okp) { best_score = 1e18; best = x; break; }
    up.assign(-x);
    bool okn = up.propagate();
    long f = (long)(up.trail.size() - base);
    up.backtrack(base);
    if (!okn) { best_score = 1e18; best = x; break; }
    double s = (double)(t + 1) * (double)(f + 1);
    if (s > best_score) { best_score = s; best = x; }
  }
  up.backtrack(0);
  return best;
}

static double cpu_now() { return (double)clock() / CLOCKS_PER_SEC; }

int main(int argc, char **argv) {
  if (argc < 4) { std::fprintf(stderr, "usage: cnc_worker CNF NSPLIT OUTDIR\n"); return 2; }
  std::string dir = argv[3];
  nsplit = std::atoi(argv[2]);
  // parse CNF
  FILE *f = std::fopen(argv[1], "r");
  if (!f) { std::perror("open cnf"); return 2; }
  {
    int c;
    std::vector<int> cur;
    long declared = -1;
    while ((c = std::getc(f)) != EOF) {
      if (c == 'c') { while ((c = std::getc(f)) != EOF && c != '\n'); continue; }
      if (c == 'p') {
        long a, b;
        if (std::fscanf(f, " cnf %ld %ld", &a, &b) != 2) { std::fprintf(stderr, "bad header\n"); return 2; }
        nvars = (int)a; declared = b; continue;
      }
      if (c == '-' || (c >= '0' && c <= '9')) {
        std::ungetc(c, f);
        int lit;
        if (std::fscanf(f, "%d", &lit) != 1) { std::fprintf(stderr, "parse\n"); return 2; }
        if (lit == 0) { clauses.push_back(cur); cur.clear(); }
        else cur.push_back(lit);
      }
    }
    std::fclose(f);
    if (declared != (long)clauses.size()) { std::fprintf(stderr, "clause count mismatch %ld %zu\n", declared, clauses.size()); return 2; }
  }
  for (auto &c : clauses) {
    for (int l : c) { body += std::to_string(l); body += ' '; }
    body += "0\n";
  }
  up.init();
  CaDiCaL::Solver *inc = nullptr;
  std::printf("READY %d %zu\n", nvars, clauses.size());
  std::fflush(stdout);
  std::string line;
  while (std::getline(std::cin, line)) {
    std::istringstream in(line);
    std::string kind; long id;
    in >> kind >> id;
    if (kind == "J") {
      long long conflicts; int proof;
      in >> conflicts >> proof;
      std::vector<int> cube; int lit;
      while (in >> lit && lit != 0) cube.push_back(lit);
      double t0 = cpu_now();
      CaDiCaL::Solver s;
      s.set("quiet", 1);
      std::string ppath = dir + "/p" + std::to_string(id) + ".lrat";
      if (proof) {
        s.set("lrat", 1);
        s.set("binary", 0);
        s.trace_proof(ppath.c_str());
      }
      // Feed the clauses through the DIMACS parser (from memory) so that CaDiCaL reserves the
      // original clause ids 1..m+k up front; adding them through 'add' would interleave ids of
      // clauses derived during root-level simplification and break LRAT numbering.
      {
        std::string text = "p cnf " + std::to_string(nvars) + " " + std::to_string(clauses.size() + cube.size()) + "\n";
        text.reserve(body.size() + 16 * cube.size() + 64);
        text += body;
        for (int l : cube) { text += std::to_string(l); text += " 0\n"; }
        FILE *mf = fmemopen((void *)text.data(), text.size(), "r");
        int vv = 0;
        const char *err = s.read_dimacs(mf, "job", vv, 1);
        std::fclose(mf);
        if (err) { std::fprintf(stderr, "dimacs error: %s\n", err); return 2; }
      }
      if (conflicts > 0) s.limit("conflicts", (int)std::min<long long>(conflicts, 2000000000LL));
      int res = s.solve();
      long long used = (long long)s.get_statistic_value("conflicts");
      if (proof) { s.flush_proof_trace(); s.close_proof_trace(); }
      double t1 = cpu_now();
      if (res == 20) {
        std::printf("U %ld %lld %.3f\n", id, used, t1 - t0);
      } else if (res == 10) {
        std::string path = dir + "/model-" + std::to_string(id) + ".txt";
        FILE *mf = std::fopen(path.c_str(), "w");
        for (int v = 1; v <= nvars; v++) std::fprintf(mf, "%d\n", s.val(v) > 0 ? v : -v);
        std::fclose(mf);
        if (proof) std::remove(ppath.c_str());
        std::printf("S %ld %lld %.3f\n", id, used, t1 - t0);
      } else {
        if (proof) std::remove(ppath.c_str());
        double score;
        int x = lookahead(cube, score);
        double t2 = cpu_now();
        if (x == 0) std::printf("F %ld %lld %.3f 0\n", id, used, t2 - t0);
        else std::printf("K %ld %lld %.3f %d %.6g %.3f\n", id, used, t2 - t0, x, score, t2 - t1);
      }
    } else if (kind == "L") {
      // lookahead only (no solving): "L id lit1 ... litk 0" -> "L id var score cpu" (var 0: UP refutes)
      std::vector<int> cube; int lit;
      while (in >> lit && lit != 0) cube.push_back(lit);
      double t0 = cpu_now();
      double score;
      int x = lookahead(cube, score);
      std::printf("L %ld %d %.6g %.3f\n", id, x, score, cpu_now() - t0);
    } else if (kind == "A") {
      std::vector<int> cube; int lit;
      while (in >> lit && lit != 0) cube.push_back(lit);
      if (!inc) {
        inc = new CaDiCaL::Solver;
        inc->set("quiet", 1);
        for (auto &c : clauses) { for (int l : c) inc->add(l); inc->add(0); }
      }
      for (int l : cube) inc->assume(l);
      int res = inc->solve();
      std::printf("%s %ld\n", res == 20 ? "AU" : (res == 10 ? "AS" : "A?"), id);
    } else {
      std::printf("E %ld unknown\n", id);
    }
    std::fflush(stdout);
  }
  return 0;
}
