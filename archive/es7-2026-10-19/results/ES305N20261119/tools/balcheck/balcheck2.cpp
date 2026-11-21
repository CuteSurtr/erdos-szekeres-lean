// balcheck2.cpp (v2 of balcheck.cpp, 19 Nov 19:45: optional lemma leaves in the cover) -- independent checker for the balanced budget-B omission trees (route to ES(8) <= 306).
// Own code (main session, 19 Nov 2026), written from the defining inequality, not from scripts/omission_tree.py.
//
// Claim checked: no 0/1 hole vector h on the 252 balanced states with sum(h) <= B satisfies every catalog row
// "sum_{s in support} h_s >= rhs".  Evidence: K context files ctx-<k>-b<B>.json.gz, each a binary decision tree
// below the literals of its context path, plus the requirement that the K paths form a complete binary decision tree.
//
// Leaf rule (derivation).  Let M, O be the states fixed missing (h=1) / occupied (h=0) on the way to a leaf, F the
// free states.  A weighted leaf carries an integer capacity c >= 0 and integer weights w_r >= 0 on distinct rows.
// For a feasible h: for each row, sum_{s in supp_r & F} h_s >= rhs_r - |supp_r & M| and >= 0, so with
// d_r = max(0, rhs_r - |supp_r & M|) and load_s = sum_{r : s in supp_r} w_r:
//     sum_{s in F} load_s h_s >= D := sum_r w_r d_r.
// Also load_s h_s <= c h_s + max(0, load_s - c) and sum_{s in F} h_s <= B - |M|, so
//     sum_{s in F} load_s h_s <= U := c (B - |M|) + sum_{s in F} max(0, load_s - c).
// Hence D - U >= 1 excludes every feasible h below the leaf.  (If B - |M| < 0 no h exists either; an over_budget
// leaf is accepted iff |M| > B.)  All sums in __int128; weights must fit in int64 and be < 2^40.
//
// usage: balcheck CATALOG.json BUDGET K THREADS FILE_PATTERN OUT.tsv
//   FILE_PATTERN contains "%d" for the context number, e.g. /path/runs/ctx-%d-b65.json.gz
// Exit 0 iff every file passes, the path cover is complete and exactly K contexts were read.
// v2: env BALCHECK_LEMMA_PATHS="v:b,v:b;v:b..." lists paths (literal lists, ";"-separated) that count as leaves of the
// cover without a file, because a Lean lemma excludes them (e.g. "0:1" = state 0 missing, FixedStatesZ.zero_mem_occupied).
// They are inserted into the cover trie like context paths; the verdict then names them.
#include <zlib.h>
#include <atomic>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <mutex>
#include <set>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>
using namespace std;
typedef __int128 i128;
static const int NS = 252;

// ---------- minimal JSON reader for the two file kinds used here ----------
struct P {
  const char *s, *e;
  explicit P(const string &t) : s(t.data()), e(t.data() + t.size()) {}
  void ws() { while (s < e && (*s == ' ' || *s == '\n' || *s == '\r' || *s == '\t')) s++; }
  [[noreturn]] void fail(const char *m) { throw runtime_error(string("json: ") + m); }
  void expect(char c) { ws(); if (s >= e || *s != c) fail("unexpected character"); s++; }
  bool peek(char c) { ws(); return s < e && *s == c; }
  string str() {
    expect('"'); string r;
    while (s < e && *s != '"') { if (*s == '\\') fail("escapes not supported"); r += *s++; }
    if (s >= e) fail("unterminated string");
    s++; return r;
  }
  long long integer() {
    ws(); bool neg = false; if (s < e && *s == '-') { neg = true; s++; }
    if (s >= e || *s < '0' || *s > '9') fail("integer expected");
    long long v = 0; int digits = 0;
    while (s < e && *s >= '0' && *s <= '9') { v = v * 10 + (*s - '0'); s++; if (++digits > 17) fail("integer too long"); }
    if (s < e && (*s == '.' || *s == 'e' || *s == 'E')) fail("non-integer number");
    return neg ? -v : v;
  }
  void skip() {  // skip any value
    ws(); if (s >= e) fail("eof");
    if (*s == '"') { str(); return; }
    if (*s == '{') { s++; if (peek('}')) { s++; return; } do { str(); expect(':'); skip(); } while (peek(',') && (s++, true)); expect('}'); return; }
    if (*s == '[') { s++; if (peek(']')) { s++; return; } do { skip(); } while (peek(',') && (s++, true)); expect(']'); return; }
    if (!strncmp(s, "true", 4)) { s += 4; return; }
    if (!strncmp(s, "false", 5)) { s += 5; return; }
    if (!strncmp(s, "null", 4)) { s += 4; return; }
    if (*s == '-' || (*s >= '0' && *s <= '9')) { while (s < e && (strchr("+-.eE", *s) || (*s >= '0' && *s <= '9'))) s++; return; }
    fail("bad value");
  }
  vector<long long> intlist() {
    vector<long long> v; expect('[');
    if (peek(']')) { s++; return v; }
    do { v.push_back(integer()); } while (peek(',') && (s++, true));
    expect(']'); return v;
  }
};

static string readfile(const string &fn) {
  gzFile f = gzopen(fn.c_str(), "rb");
  if (!f) throw runtime_error("cannot open " + fn);
  string out; char buf[1 << 16]; int k;
  while ((k = gzread(f, buf, sizeof buf)) > 0) out.append(buf, k);
  int err; const char *m = gzerror(f, &err);
  gzclose(f);
  if (k < 0 || (err != Z_OK && err != Z_STREAM_END)) throw runtime_error(string("gz error ") + m + " in " + fn);
  return out;
}

struct Row { vector<int> sup; long long rhs; };
static vector<Row> ROWS;
static vector<vector<int>> ROWS_OF_STATE;  // not needed for the rule; kept for the support sanity check

static void read_catalog(const string &fn) {
  string t = readfile(fn); P p(t);
  p.expect('{'); bool have = false; int nstates = -1;
  do {
    string k = p.str(); p.expect(':');
    if (k == "constraints") {
      have = true; p.expect('[');
      do {
        p.expect('{'); Row r; r.rhs = -1; bool hs = false;
        do {
          string kk = p.str(); p.expect(':');
          if (kk == "support") { auto v = p.intlist(); for (auto x : v) r.sup.push_back((int)x); hs = true; }
          else if (kk == "rhs") r.rhs = p.integer();
          else p.skip();
        } while (p.peek(',') && (p.s++, true));
        p.expect('}');
        if (!hs || r.rhs < 0) throw runtime_error("catalog row without support or rhs");
        ROWS.push_back(r);
      } while (p.peek(',') && (p.s++, true));
      p.expect(']');
    } else if (k == "states") {
      p.expect('['); nstates = 0;
      if (!p.peek(']')) { do { p.skip(); nstates++; } while (p.peek(',') && (p.s++, true)); }
      p.expect(']');
    } else p.skip();
  } while (p.peek(',') && (p.s++, true));
  p.expect('}');
  if (!have || nstates != NS) throw runtime_error("catalog: expected 252 states and a constraints list");
  if (const char *ex = getenv("BALCHECK_EXTRA_ROWS")) {   // extra rows appended after the catalog rows (e.g. the Z-row)
    string t2 = readfile(ex); P q(t2); q.expect('[');
    if (!q.peek(']')) do {
      q.expect('{'); Row r; r.rhs = -1; bool hs = false;
      do {
        string kk = q.str(); q.expect(':');
        if (kk == "support") { auto v = q.intlist(); for (auto x : v) r.sup.push_back((int)x); hs = true; }
        else if (kk == "rhs") r.rhs = q.integer();
        else q.skip();
      } while (q.peek(',') && (q.s++, true));
      q.expect('}');
      if (!hs || r.rhs < 0) throw runtime_error("extra row without support or rhs");
      ROWS.push_back(r);
    } while (q.peek(',') && (q.s++, true));
    q.expect(']');
  }
  for (auto &r : ROWS) {
    set<int> u(r.sup.begin(), r.sup.end());
    if ((int)u.size() != (int)r.sup.size()) throw runtime_error("catalog: repeated state in a support");
    for (int x : r.sup) if (x < 0 || x >= NS) throw runtime_error("catalog: state out of range");
    if (r.rhs > (long long)r.sup.size()) throw runtime_error("catalog: rhs > |support|");
  }
}

// ---------- one context file ----------
struct Node { int type = -1; int vertex = -1, zero = -1, one = -1; long long cap = -1; vector<pair<int, long long>> w; };
enum { BRANCH = 0, WEIGHTED = 1, OVER = 2, PENDING = 3 };

struct CtxResult { int k = -1; bool ok = false; string err; long long nodes = 0, leaves = 0; i128 minm = -1; vector<pair<int,int>> path; };

static CtxResult check_file(const string &fn, int expect_k, int B) {
  CtxResult R; R.k = expect_k;
  try {
    string t = readfile(fn); P p(t);
    long long ctx = -1, budget = -1, root = -1; string status; vector<long long> mis, occ; vector<Node> nodes; bool hp = false;
    p.expect('{');
    do {
      string k = p.str(); p.expect(':');
      if (k == "context") ctx = p.integer();
      else if (k == "budget") budget = p.integer();
      else if (k == "root") root = p.integer();
      else if (k == "status") status = p.str();
      else if (k == "missing") mis = p.intlist();
      else if (k == "occupied") occ = p.intlist();
      else if (k == "path") {
        hp = true; p.expect('[');
        if (!p.peek(']')) do { auto v = p.intlist(); if (v.size() != 2) throw runtime_error("path entry not a pair"); R.path.push_back({(int)v[0], (int)v[1]}); } while (p.peek(',') && (p.s++, true));
        p.expect(']');
      } else if (k == "nodes") {
        p.expect('[');
        if (!p.peek(']')) do {
          Node nd; p.expect('{');
          do {
            string kk = p.str(); p.expect(':');
            if (kk == "type") {
              string ty = p.str();
              nd.type = ty == "branch" ? BRANCH : ty == "weighted" ? WEIGHTED : ty == "over_budget" ? OVER : ty == "pending" ? PENDING : -2;
            } else if (kk == "vertex") nd.vertex = (int)p.integer();
            else if (kk == "zero") nd.zero = (int)p.integer();
            else if (kk == "one") nd.one = (int)p.integer();
            else if (kk == "capacity") nd.cap = p.integer();
            else if (kk == "weights") {
              p.expect('[');
              if (!p.peek(']')) do { auto v = p.intlist(); if (v.size() != 2) throw runtime_error("weight entry not a pair"); nd.w.push_back({(int)v[0], v[1]}); } while (p.peek(',') && (p.s++, true));
              p.expect(']');
            } else p.skip();
          } while (p.peek(',') && (p.s++, true));
          p.expect('}'); nodes.push_back(move(nd));
        } while (p.peek(',') && (p.s++, true));
        p.expect(']');
      } else p.skip();
    } while (p.peek(',') && (p.s++, true));
    p.expect('}');
    if (ctx != expect_k) throw runtime_error("context field != file number");
    if (budget != B && !getenv("BALCHECK_CONTROL_IGNORE_BUDGET_FIELD")) throw runtime_error("budget field != B");  // env switch: negative controls only
    if (status != "closed") throw runtime_error("status != closed");
    if (!hp || root < 0 || root >= (long long)nodes.size()) throw runtime_error("missing path or bad root");
    // context literals from the path: b = 1 -> missing, b = 0 -> occupied; must equal the stated lists
    vector<char> fixed(NS, 0);  // 0 free, 1 missing, 2 occupied
    set<long long> pm, po;
    for (auto &pr : R.path) {
      if (pr.first < 0 || pr.first >= NS || (pr.second != 0 && pr.second != 1)) throw runtime_error("bad path literal");
      if (fixed[pr.first]) throw runtime_error("repeated path vertex");
      fixed[pr.first] = pr.second ? 1 : 2; (pr.second ? pm : po).insert(pr.first);
    }
    if (set<long long>(mis.begin(), mis.end()) != pm || set<long long>(occ.begin(), occ.end()) != po || mis.size() != pm.size() || occ.size() != po.size())
      throw runtime_error("missing/occupied lists differ from the path");
    // walk
    vector<char> seen(nodes.size(), 0);
    struct Fr { int i; vector<char> fx; int nm; };
    vector<Fr> st; st.push_back({(int)root, fixed, (int)pm.size()});
    i128 minm = -1; long long leaves = 0;
    vector<i128> load(NS);
    while (!st.empty()) {
      Fr f = move(st.back()); st.pop_back();
      if (f.i < 0 || f.i >= (int)nodes.size()) throw runtime_error("child index out of range");
      if (seen[f.i]) throw runtime_error("node reached twice");
      seen[f.i] = 1;
      const Node &nd = nodes[f.i];
      if (nd.type == BRANCH) {
        int v = nd.vertex;
        if (v < 0 || v >= NS || f.fx[v]) throw runtime_error("branch on a fixed or invalid state");
        Fr z{nd.zero, f.fx, f.nm}; z.fx[v] = 2;            // zero child: occupied
        Fr o{nd.one, move(f.fx), f.nm + 1}; o.fx[v] = 1;    // one child: missing
        st.push_back(move(z)); st.push_back(move(o));
        continue;
      }
      leaves++;
      if (nd.type == OVER) { if (f.nm <= B) throw runtime_error("unjustified over_budget leaf"); continue; }
      if (nd.type != WEIGHTED) throw runtime_error("leaf is neither weighted nor over_budget");
      if (nd.cap < 0) throw runtime_error("negative capacity");
      for (int s = 0; s < NS; s++) load[s] = 0;
      i128 D = 0; set<int> used;
      for (auto &pr : nd.w) {
        int r = pr.first; long long w = pr.second;
        if (r < 0 || r >= (int)ROWS.size()) throw runtime_error("weight on an unknown row");
        if (!used.insert(r).second) throw runtime_error("row weighted twice");
        if (w < 0 || w >= (1LL << 40)) throw runtime_error("weight out of range");
        long long inM = 0;
        for (int s : ROWS[r].sup) { if (f.fx[s] == 1) inM++; load[s] += w; }
        long long dr = ROWS[r].rhs - inM; if (dr < 0) dr = 0;
        D += (i128)w * dr;
      }
      i128 U = (i128)nd.cap * (i128)(B - f.nm);
      for (int s = 0; s < NS; s++) if (f.fx[s] == 0 && load[s] > nd.cap) U += load[s] - nd.cap;
      i128 m = D - U;
      if (m < 1) throw runtime_error("leaf margin < 1");
      if (minm < 0 || m < minm) minm = m;
    }
    for (size_t i = 0; i < nodes.size(); i++) if (!seen[i]) throw runtime_error("unreachable node");
    R.nodes = (long long)nodes.size(); R.leaves = leaves; R.minm = minm; R.ok = true;
  } catch (exception &ex) { R.ok = false; R.err = ex.what(); }
  return R;
}

// ---------- the path cover: the K paths must be the leaves of one complete binary decision tree ----------
struct Trie { int vertex = -1; int child[2] = {-1, -1}; bool leaf = false; };
static vector<vector<pair<int,int>>> LEMMA;
static string cover_check(const vector<CtxResult> &res0) {
  vector<Trie> T(1);
  vector<CtxResult> res(res0);
  for (auto &lp : LEMMA) { CtxResult x; x.path = lp; x.k = -1; res.push_back(x); }
  for (auto &r : res) {
    int cur = 0; set<int> used;
    for (size_t j = 0; j < r.path.size(); j++) {
      int v = r.path[j].first, b = r.path[j].second;
      if (T[cur].leaf) return "a context path extends another context's path";
      if (!used.insert(v).second) return "repeated vertex on a path";
      if (T[cur].vertex == -1) T[cur].vertex = v;
      else if (T[cur].vertex != v) return "two paths branch on different states at the same node";
      if (T[cur].child[b] == -1) { T[cur].child[b] = (int)T.size(); T.push_back(Trie()); }
      cur = T[cur].child[b];
    }
    if (T[cur].leaf || T[cur].vertex != -1) return "a context path is a prefix of another (or repeated)";
    T[cur].leaf = true;
  }
  for (auto &t : T) if (!t.leaf && (t.child[0] == -1 || t.child[1] == -1)) return "incomplete cover: a branch has a missing side";
  return "";
}

int main(int argc, char **argv) {
  if (argc != 7 && argc != 8) { fprintf(stderr, "usage: balcheck CATALOG.json BUDGET K THREADS FILE_PATTERN OUT.tsv [ID,ID,...]\n"); return 2; }
  vector<int> ids;  // optional subset mode (pilot checks): only these contexts, no cover check
  if (argc == 8) { string l = argv[7]; size_t p0 = 0; while (p0 <= l.size()) { size_t q = l.find(',', p0); if (q == string::npos) q = l.size(); ids.push_back(atoi(l.substr(p0, q - p0).c_str())); p0 = q + 1; } }
  if (const char *lp = getenv("BALCHECK_LEMMA_PATHS")) {
    string L = lp; size_t a = 0;
    while (a < L.size()) { size_t e = L.find(';', a); if (e == string::npos) e = L.size();
      string one = L.substr(a, e - a); vector<pair<int,int>> path; size_t c = 0;
      while (c < one.size()) { size_t f = one.find(',', c); if (f == string::npos) f = one.size();
        string lit = one.substr(c, f - c); size_t m = lit.find(':'); if (m == string::npos) { fprintf(stderr, "bad lemma path\n"); return 2; }
        int v = atoi(lit.substr(0, m).c_str()), b = atoi(lit.substr(m + 1).c_str());
        if (v < 0 || v >= NS || (b != 0 && b != 1)) { fprintf(stderr, "bad lemma literal\n"); return 2; }
        path.push_back({v, b}); c = f + 1; }
      if (path.empty()) { fprintf(stderr, "empty lemma path\n"); return 2; }
      LEMMA.push_back(path); a = e + 1; }
  }
  int B = atoi(argv[2]), K = atoi(argv[3]), TH = atoi(argv[4]); string pat = argv[5], outf = argv[6];
  if (B < 0 || B > NS || K < 1 || TH < 1 || TH > 16 || pat.find("%d") == string::npos) { fprintf(stderr, "bad arguments\n"); return 2; }
  try { read_catalog(argv[1]); } catch (exception &e) { fprintf(stderr, "catalog: %s\n", e.what()); return 2; }
  vector<CtxResult> res(ids.empty() ? K : (int)ids.size()); atomic<int> next(0); mutex mu; int doneN = 0;
  auto work = [&]() {
    for (;;) {
      int t = next++; if (t >= (ids.empty() ? K : (int)ids.size())) break; int k = ids.empty() ? t : ids[t];
      char fn[4096]; snprintf(fn, sizeof fn, pat.c_str(), k);
      res[ids.empty() ? k : t] = check_file(fn, k, B);
      lock_guard<mutex> g(mu); doneN++;
      if (doneN % 256 == 0) { fprintf(stderr, "checked %d/%d\n", doneN, K); fflush(stderr); }
    }
  };
  vector<thread> ths; for (int t = 0; t < TH; t++) ths.emplace_back(work); for (auto &t : ths) t.join();
  FILE *o = fopen(outf.c_str(), "w"); if (!o) { fprintf(stderr, "cannot write %s\n", outf.c_str()); return 2; }
  fprintf(o, "ctx\tok\tnodes\tleaves\tmin_margin\terror\n");
  long long N = 0, L = 0, bad = 0; i128 gm = -1;
  for (auto &r : res) {
    fprintf(o, "%d\t%d\t%lld\t%lld\t%lld\t%s\n", r.k, r.ok ? 1 : 0, r.nodes, r.leaves, (long long)r.minm, r.err.c_str());
    if (!r.ok) bad++; else { N += r.nodes; L += r.leaves; if (gm < 0 || r.minm < gm) gm = r.minm; }
  }
  fclose(o);
  string cov = !ids.empty() ? "not checked (subset mode)" : bad ? "not checked (failed files)" : cover_check(res);
  bool ok = bad == 0 && (cov.empty() || !ids.empty());
  printf("{\"verdict\": \"%s\", \"budget\": %d, \"contexts\": %d, \"failed\": %lld, \"nodes\": %lld, \"leaves\": %lld, \"min_margin\": %lld, \"rows\": %zu, \"cover\": \"%s\"}\n",
         ok ? (ids.empty() ? "EXACT TREE (balcheck)" : "FILES OK (subset mode, no cover check)") : "NOT CONFIRMED", B, K, bad, N, L, (long long)gm, ROWS.size(), (cov.empty() ? (LEMMA.empty() ? string("complete") : "complete with " + to_string(LEMMA.size()) + " lemma path(s) " + string(getenv("BALCHECK_LEMMA_PATHS"))) : cov).c_str());
  return ok ? 0 : 1;
}
