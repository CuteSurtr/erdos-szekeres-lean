// occfirst.cpp -- CaDiCaL (library, version printed at start) on a DIMACS CNF with a decision
// callback: the listed "priority" literals are decided first, in the listed order and phase; when
// all of them are assigned the solver's own heuristic decides.  No external clauses and no external
// propagation are ever added, so the LRAT proof written by the solver is a proof of the input CNF.
// usage: occfirst CNF PRIORITY_FILE PROOF_OR_- TIMELIMIT_SEC [opt=val ...]
#include "cadical.hpp"
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <fstream>
#include <string>
#include <vector>

using namespace std;

struct Prop : CaDiCaL::ExternalPropagator, CaDiCaL::FixedAssignmentListener {
  vector<int> order;          // signed literals in decision order
  vector<signed char> val;    // current value of observed variables
  vector<signed char> fixed;  // root-level fixed
  vector<vector<int>> trail;  // observed variables assigned per level
  long ext_decisions = 0;
  size_t scan_from = 0;
  Prop () { trail.emplace_back (); }
  void notify_assignment (const vector<int> &lits) override {
    for (int l : lits) {
      int v = abs (l);
      if ((size_t) v >= val.size ()) continue;
      if (!val[v]) { val[v] = l > 0 ? 1 : -1; trail.back ().push_back (v); }
    }
  }
  void notify_new_decision_level () override { trail.emplace_back (); }
  void notify_backtrack (size_t new_level) override {
    while (trail.size () > new_level + 1) {
      for (int v : trail.back ()) val[v] = 0;
      trail.pop_back ();
    }
  }
  void notify_fixed_assignment (int l) override {
    int v = abs (l);
    if ((size_t) v < fixed.size ()) fixed[v] = l > 0 ? 1 : -1;
  }
  bool cb_check_found_model (const vector<int> &) override { return true; }
  int cb_decide () override {
    for (size_t i = 0; i < order.size (); i++) {
      int v = abs (order[i]);
      if (!val[v] && !fixed[v]) { ext_decisions++; return order[i]; }
    }
    return 0;
  }
  int cb_propagate () override { return 0; }
  int cb_add_reason_clause_lit (int) override { return 0; }
  bool cb_has_external_clause (bool &f) override { f = false; return false; }
  int cb_add_external_clause_lit () override { return 0; }
};

struct Term : CaDiCaL::Terminator {
  chrono::steady_clock::time_point deadline;
  bool terminate () override { return chrono::steady_clock::now () > deadline; }
};

int main (int argc, char **argv) {
  if (argc < 5) { fprintf (stderr, "usage: occfirst CNF PRIO PROOF|- TLIM [opt=val ...]\n"); return 2; }
  CaDiCaL::Solver solver;
  printf ("c occfirst: CaDiCaL library version %s\n", CaDiCaL::Solver::version ());
  for (int i = 5; i < argc; i++) {
    string a = argv[i];
    size_t p = a.find ('=');
    if (p == string::npos) { fprintf (stderr, "bad option %s\n", argv[i]); return 2; }
    if (!solver.set (a.substr (0, p).c_str (), atoi (a.substr (p + 1).c_str ()))) {
      fprintf (stderr, "unknown option %s\n", argv[i]); return 2;
    }
    printf ("c option %s\n", argv[i]);
  }
  bool proof = strcmp (argv[3], "-") != 0;
  if (proof) {
    solver.set ("lrat", 1);
    solver.set ("binary", 0);
    if (!solver.trace_proof (argv[3])) { fprintf (stderr, "cannot open proof\n"); return 2; }
  }
  int vars = 0;
  const char *err = solver.read_dimacs (argv[1], vars, 1);
  if (err) { fprintf (stderr, "parse error: %s\n", err); return 2; }
  Prop prop;
  prop.val.assign (vars + 1, 0);
  prop.fixed.assign (vars + 1, 0);
  {
    ifstream f (argv[2]);
    int l;
    while (f >> l) if (l) prop.order.push_back (l);
  }
  printf ("c priority literals: %zu\n", prop.order.size ());
  if (!prop.order.empty ()) {
    solver.connect_fixed_listener (&prop);
    solver.connect_external_propagator (&prop);
    for (int l : prop.order) solver.add_observed_var (abs (l));
  }
  Term term;
  term.deadline = chrono::steady_clock::now () + chrono::seconds (atol (argv[4]));
  solver.connect_terminator (&term);
  auto t0 = chrono::steady_clock::now ();
  int res = solver.solve ();
  double dt = chrono::duration<double> (chrono::steady_clock::now () - t0).count ();
  solver.statistics ();
  printf ("c external decisions: %ld\n", prop.ext_decisions);
  printf ("c solve wall seconds: %.2f\n", dt);
  if (res == 10) {
    printf ("s SATISFIABLE\nv");
    for (int v = 1; v <= vars; v++) printf (" %d", solver.val (v) > 0 ? v : -v);
    printf (" 0\n");
  } else if (res == 20) printf ("s UNSATISFIABLE\n");
  else printf ("s UNKNOWN\n");
  fflush (stdout);
  if (!prop.order.empty ()) { solver.disconnect_external_propagator (); solver.disconnect_fixed_listener (); }
  if (proof) solver.close_proof_trace ();
  return res;
}
