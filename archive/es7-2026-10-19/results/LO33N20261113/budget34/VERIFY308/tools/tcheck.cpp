// tcheck.cpp -- independent exact checker for budget-34 branch-and-bound certificate trees (ES(8) <= 308 packets).
// Written from the written task specification only; no project checker/finder code was read or used.
//
// usage: tcheck ROWS.txt PACKET_DIR THREADS OUT_PREFIX EXPECT_SOURCE EXPECT_EXTRA
//   ROWS.txt  : produced by prep_rows.py ("R" then R lines "d k s_1..s_k")
//   writes OUT_PREFIX.contexts.tsv, OUT_PREFIX.rowsused.txt, OUT_PREFIX.summary.json ; exit 0 iff every check passed.
//
// Leaf rule (soundness argued in README): weighted leaf (c, {(r,w_r)}) at missing set M, occupied set O is valid iff
//   margin = sum_r w_r*max(0, d_r - |S_r & M|) - c*(34-|M|) - sum_{i not in M u O} max(0, load_i - c) >= 1,
//   load_i = sum_{r : i in S_r} w_r.  All arithmetic in __int128 from int64 inputs (no overflow possible, see README).
#include <atomic>
#include <climits>
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <dirent.h>
#include <map>
#include <mutex>
#include <set>
#include <stdexcept>
#include <string>
#include <sys/stat.h>
#include <thread>
#include <vector>
#include <algorithm>
#include <zlib.h>
using namespace std;
typedef long long ll;
typedef __int128 i128;
static const int NS = 154, B = 34;

struct BS {
  uint64_t w[3] = {0, 0, 0};
  bool has(int i) const { return (w[i >> 6] >> (i & 63)) & 1; }
  void set(int i) { w[i >> 6] |= 1ULL << (i & 63); }
  int cnt() const { return __builtin_popcountll(w[0]) + __builtin_popcountll(w[1]) + __builtin_popcountll(w[2]); }
  int andcnt(const BS& o) const {
    return __builtin_popcountll(w[0] & o.w[0]) + __builtin_popcountll(w[1] & o.w[1]) + __builtin_popcountll(w[2] & o.w[2]);
  }
  bool operator==(const BS& o) const { return w[0] == o.w[0] && w[1] == o.w[1] && w[2] == o.w[2]; }
};
static string bsstr(const BS& b) {
  string s = "{";
  for (int i = 0; i < NS; i++) if (b.has(i)) { if (s.size() > 1) s += ","; s += to_string(i); }
  return s + "}";
}
static string i128s(i128 v) {
  if (v == 0) return "0";
  bool neg = v < 0; string s;
  while (v != 0) { int dgt = (int)(v % 10); if (dgt < 0) dgt = -dgt; s += char('0' + dgt); v /= 10; }
  if (neg) s += '-';
  return string(s.rbegin(), s.rend());
}

struct Row { int d; vector<int> s; BS bs; };
static vector<Row> rows;

enum { T_NONE = 0, T_BRANCH, T_WEIGHTED, T_OVER, T_CONTEXT, T_PENDING };
enum { K_TYPE = 1, K_VERTEX = 2, K_ZERO = 4, K_ONE = 8, K_CAP = 16, K_WEIGHTS = 32, K_CONTEXT = 64, K_UNKNOWN = 128 };
struct Node { int type = T_NONE; int keys = 0; ll vertex = 0, zero = 0, one = 0, cap = 0, ctx = 0; size_t woff = 0, wcnt = 0; };
struct Tree {
  vector<Node> nodes; vector<pair<ll, ll>> W;
  set<string> keys; map<string, ll> ints; map<string, string> strs; vector<ll> missing, occupied; vector<string> unknown;
};

struct Parser {
  const char *base, *p, *e;
  [[noreturn]] void fail(const string& m) { throw runtime_error("JSON: " + m + " at byte " + to_string(p - base)); }
  void ws() { while (p < e && (*p == ' ' || *p == '\n' || *p == '\r' || *p == '\t')) p++; }
  bool peek(char c) { ws(); return p < e && *p == c; }
  void expect(char c) { ws(); if (p >= e || *p != c) fail(string("expected '") + c + "'"); p++; }
  ll integer() {
    ws(); bool neg = false;
    if (p < e && *p == '-') { neg = true; p++; }
    if (p >= e || *p < '0' || *p > '9') fail("expected integer");
    if (*p == '0' && p + 1 < e && p[1] >= '0' && p[1] <= '9') fail("leading zero");
    unsigned __int128 v = 0;
    while (p < e && *p >= '0' && *p <= '9') { v = v * 10 + (*p - '0'); if (v > (unsigned __int128)LLONG_MAX + 1) fail("integer overflow"); p++; }
    if (p < e && (*p == '.' || *p == 'e' || *p == 'E')) fail("non-integer number");
    if (!neg && v > (unsigned __int128)LLONG_MAX) fail("integer overflow");
    return neg ? (ll)(-(i128)v) : (ll)v;
  }
  string str() {
    expect('"'); string s;
    while (true) {
      if (p >= e) fail("unterminated string");
      char c = *p++;
      if (c == '"') return s;
      if ((unsigned char)c < 0x20) fail("control char in string");
      if (c == '\\') {
        if (p >= e) fail("bad escape");
        char x = *p++;
        switch (x) {
          case '"': s += '"'; break; case '\\': s += '\\'; break; case '/': s += '/'; break;
          case 'b': s += '\b'; break; case 'f': s += '\f'; break; case 'n': s += '\n'; break;
          case 'r': s += '\r'; break; case 't': s += '\t'; break;
          case 'u': if (e - p < 4) fail("bad \\u"); s += "\\u"; s.append(p, 4); p += 4; break;  // kept verbatim
          default: fail("bad escape");
        }
      } else s += c;
    }
  }
  void lit(const char* w) { size_t n = strlen(w); if ((size_t)(e - p) < n || memcmp(p, w, n)) fail("bad literal"); p += n; }
  void skip() {  // any JSON value
    ws(); if (p >= e) fail("unexpected end");
    char c = *p;
    if (c == '{') { p++; if (peek('}')) { p++; return; } while (true) { str(); expect(':'); skip(); if (peek(',')) { p++; continue; } expect('}'); return; } }
    if (c == '[') { p++; if (peek(']')) { p++; return; } while (true) { skip(); if (peek(',')) { p++; continue; } expect(']'); return; } }
    if (c == '"') { str(); return; }
    if (c == 't') { lit("true"); return; } if (c == 'f') { lit("false"); return; } if (c == 'n') { lit("null"); return; }
    if (c == '-' || (c >= '0' && c <= '9')) { p++; while (p < e && (isdigit((unsigned char)*p) || *p == '.' || *p == 'e' || *p == 'E' || *p == '+' || *p == '-')) p++; return; }
    fail("bad value");
  }
  vector<ll> intarray() {
    vector<ll> v; expect('[');
    if (peek(']')) { p++; return v; }
    while (true) { v.push_back(integer()); if (peek(',')) { p++; continue; } expect(']'); return v; }
  }
  void node(Tree& t) {
    Node n; n.woff = t.W.size(); expect('{');
    if (!peek('}')) while (true) {
      string k = str(); expect(':'); int bit;
      if (k == "type") {
        bit = K_TYPE; string ty = str();
        n.type = ty == "branch" ? T_BRANCH : ty == "weighted" ? T_WEIGHTED : ty == "over_budget" ? T_OVER
               : ty == "context" ? T_CONTEXT : ty == "pending" ? T_PENDING : -1;
        if (n.type < 0) fail("unknown node type '" + ty + "'");
      } else if (k == "vertex") { bit = K_VERTEX; n.vertex = integer(); }
      else if (k == "zero") { bit = K_ZERO; n.zero = integer(); }
      else if (k == "one") { bit = K_ONE; n.one = integer(); }
      else if (k == "capacity") { bit = K_CAP; n.cap = integer(); }
      else if (k == "context") { bit = K_CONTEXT; n.ctx = integer(); }
      else if (k == "weights") {
        bit = K_WEIGHTS; expect('[');
        if (peek(']')) p++;
        else while (true) {
          expect('['); ll r = integer(); expect(','); ll w = integer(); expect(']');
          t.W.push_back({r, w});
          if (peek(',')) { p++; continue; } expect(']'); break;
        }
      } else { bit = K_UNKNOWN; skip(); }
      if (bit != K_UNKNOWN && (n.keys & bit)) fail("duplicate key '" + k + "' in node");
      n.keys |= bit;
      if (peek(',')) { p++; continue; } expect('}'); break;
    } else p++;
    n.wcnt = t.W.size() - n.woff;
    int need = n.type == T_BRANCH ? (K_TYPE | K_VERTEX | K_ZERO | K_ONE) : n.type == T_WEIGHTED ? (K_TYPE | K_CAP | K_WEIGHTS)
             : n.type == T_OVER ? K_TYPE : n.type == T_CONTEXT ? (K_TYPE | K_CONTEXT) : -1;
    if (n.type == T_NONE) fail("node without type");
    if (need >= 0 && n.keys != need) fail("node " + to_string(t.nodes.size()) + " has wrong key set (mask " + to_string(n.keys) + ")");
    t.nodes.push_back(n);
  }
  // top-level object; allowed keys depend on master/context
  void top(Tree& t, bool ctx) {
    expect('{');
    if (!peek('}')) while (true) {
      string k = str(); expect(':');
      if (t.keys.count(k)) fail("duplicate top-level key '" + k + "'");
      t.keys.insert(k);
      if (k == "nodes") { expect('['); if (peek(']')) p++; else while (true) { node(t); if (peek(',')) { p++; continue; } expect(']'); break; } }
      else if (k == "root" || (k == "context" && ctx) || (!ctx && (k == "budget" || k == "contexts" || k == "master_leaves"))) t.ints[k] = integer();
      else if (!ctx && (k == "source" || k == "extra")) t.strs[k] = str();
      else if (ctx && k == "missing") t.missing = intarray();
      else if (ctx && k == "occupied") t.occupied = intarray();
      else { t.unknown.push_back(k); skip(); }
      if (peek(',')) { p++; continue; } expect('}'); break;
    } else p++;
    ws(); if (p != e) fail("trailing data after top-level value");
  }
};

static void parse_text(const string& txt, Tree& t, bool ctx) {
  Parser P; P.base = P.p = txt.data(); P.e = txt.data() + txt.size(); P.top(t, ctx);
}
static bool read_file(const string& path, bool gz, string& out, string& err) {
  if (!gz) {
    FILE* f = fopen(path.c_str(), "rb"); if (!f) { err = "cannot open " + path; return false; }
    char buf[1 << 16]; size_t n; while ((n = fread(buf, 1, sizeof buf, f)) > 0) out.append(buf, n);
    bool ok = !ferror(f); fclose(f); if (!ok) err = "read error " + path; return ok;
  }
  gzFile g = gzopen(path.c_str(), "rb"); if (!g) { err = "cannot gzopen " + path; return false; }
  gzbuffer(g, 1 << 17);
  vector<char> buf(1 << 20); int n;
  while ((n = gzread(g, buf.data(), (unsigned)buf.size())) > 0) out.append(buf.data(), n);
  int ec = 0; const char* m = gzerror(g, &ec);
  bool ok = (n == 0 && (ec == Z_OK || ec == Z_STREAM_END));
  if (!ok) err = string("gzip error in ") + path + ": " + (m ? m : "?");
  if (gzclose(g) != Z_OK && ok) { ok = false; err = "gzclose error " + path; }
  return ok;
}

struct Stats {
  ll nodes = 0, leaves = 0, weighted = 0, over = 0, pending = 0, placeholders = 0, nerr = 0, maxrow = -1;
  bool hasmin = false; i128 minmargin = 0; ll minmargin_count = 0;
  vector<string> errs;
  void err(const string& m) { nerr++; if (errs.size() < 12) errs.push_back(m); }
  void margin(i128 m) { if (!hasmin || m < minmargin) { minmargin = m; minmargin_count = 0; hasmin = true; } if (m == minmargin) minmargin_count++; }
};
struct Placeholder { ll id; BS M, O; };
struct Scratch { vector<unsigned> stamp; unsigned cur = 0; vector<char> used; };

static void check_weighted(const Tree& t, const Node& x, const BS& M, const BS& O, Stats& s, Scratch& sc, ll at) {
  s.weighted++; s.leaves++;
  ll R = (ll)rows.size();
  if (x.cap < 0) { s.err("node " + to_string(at) + ": negative capacity"); return; }
  if (++sc.cur == 0) { fill(sc.stamp.begin(), sc.stamp.end(), 0); sc.cur = 1; }
  int m = M.cnt();
  i128 D = 0, load[NS]; for (int i = 0; i < NS; i++) load[i] = 0;
  for (size_t k = 0; k < x.wcnt; k++) {
    ll r = t.W[x.woff + k].first, w = t.W[x.woff + k].second;
    if (r < 0 || r >= R) { s.err("node " + to_string(at) + ": row index out of range " + to_string(r)); return; }
    if (w < 0) { s.err("node " + to_string(at) + ": negative weight"); return; }
    if (sc.stamp[r] == sc.cur) { s.err("node " + to_string(at) + ": duplicate row " + to_string(r)); return; }
    sc.stamp[r] = sc.cur;
    if (w == 0) continue;
    if (r > s.maxrow) s.maxrow = r;
    sc.used[r] = 1;
    const Row& row = rows[r];
    int def = row.d - row.bs.andcnt(M);
    if (def > 0) D += (i128)w * def;
    for (int i : row.s) load[i] += w;
  }
  i128 ex = 0;
  for (int i = 0; i < NS; i++) if (!M.has(i) && !O.has(i) && load[i] > x.cap) ex += load[i] - x.cap;
  i128 margin = D - (i128)x.cap * (B - m) - ex;
  s.margin(margin);
  if (margin < 1) s.err("node " + to_string(at) + ": margin " + i128s(margin) + " < 1 at M=" + bsstr(M));
}

// Walk the tree from its root; every node must be reached exactly once.
static void walk(const Tree& t, ll root, BS M0, BS O0, bool allow_ctx, Stats& s, Scratch& sc, vector<Placeholder>* ph) {
  ll n = (ll)t.nodes.size();
  s.nodes += n;
  if (root < 0 || root >= n) { s.err("root out of range"); return; }
  vector<char> seen(n, 0);
  struct F { ll v; BS M, O; };
  vector<F> st; st.push_back({root, M0, O0});
  while (!st.empty()) {
    F f = st.back(); st.pop_back();
    if (seen[f.v]) { s.err("node " + to_string(f.v) + " reached twice"); continue; }
    seen[f.v] = 1;
    const Node& x = t.nodes[f.v];
    switch (x.type) {
      case T_BRANCH: {
        ll v = x.vertex;
        if (v < 0 || v >= NS) { s.err("node " + to_string(f.v) + ": vertex out of range"); break; }
        if (f.M.has((int)v) || f.O.has((int)v)) { s.err("node " + to_string(f.v) + ": branch vertex already fixed"); break; }
        if (x.zero < 0 || x.zero >= n || x.one < 0 || x.one >= n) { s.err("node " + to_string(f.v) + ": child out of range"); break; }
        F z = f, o = f; z.v = x.zero; z.O.set((int)v); o.v = x.one; o.M.set((int)v);
        st.push_back(o); st.push_back(z);
        break;
      }
      case T_WEIGHTED: check_weighted(t, x, f.M, f.O, s, sc, f.v); break;
      case T_OVER:
        s.over++; s.leaves++;
        if (!(f.M.cnt() > B)) s.err("node " + to_string(f.v) + ": over_budget leaf with |M|=" + to_string(f.M.cnt()));
        break;
      case T_CONTEXT:
        s.placeholders++;
        if (!allow_ctx || !ph) s.err("node " + to_string(f.v) + ": context node not allowed here");
        else if (x.ctx < 0) s.err("node " + to_string(f.v) + ": negative context id");
        else ph->push_back({x.ctx, f.M, f.O});
        break;
      case T_PENDING: s.pending++; s.err("node " + to_string(f.v) + ": pending leaf at M=" + bsstr(f.M)); break;
      default: s.err("node " + to_string(f.v) + ": bad type");
    }
  }
  ll unreached = 0; for (ll i = 0; i < n; i++) if (!seen[i]) unreached++;
  if (unreached) s.err(to_string(unreached) + " unreachable nodes");
}

static bool setof(const vector<ll>& v, BS& b, string& why) {
  for (ll x : v) { if (x < 0 || x >= NS) { why = "entry out of range"; return false; } if (b.has((int)x)) { why = "duplicate entry"; return false; } b.set((int)x); }
  return true;
}

struct CtxResult { ll id; string file; Stats s; bool done = false; };

int main(int argc, char** argv) {
  if (argc != 7) { fprintf(stderr, "usage: tcheck ROWS.txt PACKET_DIR THREADS OUT_PREFIX EXPECT_SOURCE EXPECT_EXTRA\n"); return 2; }
  string rowsf = argv[1], dir = argv[2], outp = argv[4], expsrc = argv[5], expextra = argv[6];
  int threads = atoi(argv[3]); if (threads < 1 || threads > 8) { fprintf(stderr, "threads 1..8\n"); return 2; }
  vector<string> fatal;
  { // rows
    FILE* f = fopen(rowsf.c_str(), "r"); if (!f) { fprintf(stderr, "no rows\n"); return 2; }
    long R; if (fscanf(f, "%ld", &R) != 1 || R <= 0) { fprintf(stderr, "bad rows\n"); return 2; }
    rows.resize(R);
    for (long r = 0; r < R; r++) {
      int d, k; if (fscanf(f, "%d %d", &d, &k) != 2 || k < 0 || k > NS || d < 0 || d > k) { fprintf(stderr, "bad row %ld\n", r); return 2; }
      rows[r].d = d;
      for (int j = 0; j < k; j++) { int i; if (fscanf(f, "%d", &i) != 1 || i < 0 || i >= NS || rows[r].bs.has(i)) { fprintf(stderr, "bad support row %ld\n", r); return 2; } rows[r].s.push_back(i); rows[r].bs.set(i); }
    }
    int extra; if (fscanf(f, "%d", &extra) == 1) { fprintf(stderr, "trailing data in rows file\n"); return 2; }
    fclose(f);
  }
  Stats ms; vector<Placeholder> ph; Tree mt;
  Scratch msc; msc.stamp.assign(rows.size(), 0); msc.used.assign(rows.size(), 0);
  try {
    string txt, err;
    if (!read_file(dir + "/master.json", false, txt, err)) throw runtime_error(err);
    parse_text(txt, mt, false);
  } catch (exception& ex) { fatal.push_back(string("master: ") + ex.what()); }
  if (fatal.empty()) {
    for (auto& k : mt.unknown) fatal.push_back("master: unknown top-level key " + k);
    for (const char* k : {"source", "extra"}) if (!mt.strs.count(k)) fatal.push_back(string("master: missing ") + k);
    for (const char* k : {"root", "budget", "contexts", "master_leaves"}) if (!mt.ints.count(k)) fatal.push_back(string("master: missing ") + k);
    if (mt.keys.count("nodes") == 0) fatal.push_back("master: missing nodes");
  }
  if (fatal.empty()) {
    if (mt.strs["source"] != expsrc) fatal.push_back("master: source field differs from the catalog used");
    if (mt.strs["extra"] != expextra) fatal.push_back("master: extra field differs from the extra.json used");
    if (mt.ints["budget"] != B) fatal.push_back("master: budget != 34");
    BS M0, O0; O0.set(0);
    walk(mt, mt.ints["root"], M0, O0, true, ms, msc, &ph);
    if ((ll)ph.size() != mt.ints["contexts"]) fatal.push_back("master: contexts field " + to_string(mt.ints["contexts"]) + " != placeholders " + to_string(ph.size()));
  }
  // placeholder ids distinct; ctx files == ids
  map<ll, size_t> idx;
  for (size_t i = 0; i < ph.size(); i++) { if (idx.count(ph[i].id)) fatal.push_back("duplicate context id " + to_string(ph[i].id)); idx[ph[i].id] = i; }
  set<ll> files; ll badnames = 0;
  if (DIR* dp = opendir(dir.c_str())) {
    while (dirent* de = readdir(dp)) {
      string nm = de->d_name; if (nm.rfind("ctx-", 0) != 0) continue;
      const string suf = ".json.gz"; bool ok = nm.size() > 4 + suf.size() && nm.compare(nm.size() - suf.size(), suf.size(), suf) == 0;
      string num = ok ? nm.substr(4, nm.size() - 4 - suf.size()) : "";
      ok = ok && !num.empty() && num.size() < 18 && all_of(num.begin(), num.end(), ::isdigit) && !(num.size() > 1 && num[0] == '0');
      if (!ok) { badnames++; fatal.push_back("unexpected ctx-like file " + nm); continue; }
      files.insert(stoll(num));
    }
    closedir(dp);
  } else fatal.push_back("cannot list dir");
  ll missingf = 0, extraf = 0;
  for (auto& kv : idx) if (!files.count(kv.first)) { missingf++; if (missingf <= 5) fatal.push_back("missing ctx file for id " + to_string(kv.first)); }
  for (ll id : files) if (!idx.count(id)) { extraf++; if (extraf <= 5) fatal.push_back("ctx file without placeholder: " + to_string(id)); }
  // contexts in parallel, largest files first
  vector<CtxResult> res(ph.size());
  vector<pair<ll, size_t>> order;
  for (size_t i = 0; i < ph.size(); i++) {
    res[i].id = ph[i].id; res[i].file = dir + "/ctx-" + to_string(ph[i].id) + ".json.gz";
    struct stat sb; ll sz = stat(res[i].file.c_str(), &sb) == 0 ? (ll)sb.st_size : 0;
    order.push_back({-sz, i});
  }
  sort(order.begin(), order.end());
  atomic<size_t> next(0); mutex mu; vector<char> used(rows.size(), 0);
  auto worker = [&]() {
    Scratch sc; sc.stamp.assign(rows.size(), 0); sc.used.assign(rows.size(), 0);
    while (true) {
      size_t k = next++; if (k >= order.size()) break;
      size_t i = order[k].second; CtxResult& cr = res[i]; const Placeholder& P = ph[i];
      try {
        string txt, err; Tree t;
        if (!files.count(P.id)) throw runtime_error("file missing");
        if (!read_file(cr.file, true, txt, err)) throw runtime_error(err);
        parse_text(txt, t, true); string().swap(txt);
        for (auto& u : t.unknown) cr.s.err("unknown top-level key " + u);
        for (const char* key : {"context", "missing", "occupied", "root", "nodes"}) if (!t.keys.count(key)) cr.s.err(string("missing key ") + key);
        if (t.ints.count("context") && t.ints["context"] != P.id) cr.s.err("context field " + to_string(t.ints["context"]) + " != placeholder id");
        BS M, O; string why;
        if (!setof(t.missing, M, why)) cr.s.err("missing list: " + why);
        if (!setof(t.occupied, O, why)) cr.s.err("occupied list: " + why);
        if (!(M == P.M)) cr.s.err("missing set " + bsstr(M) + " != placeholder M " + bsstr(P.M));
        if (!(O == P.O)) cr.s.err("occupied set " + bsstr(O) + " != placeholder O " + bsstr(P.O));
        if (cr.s.nerr == 0 && t.ints.count("root")) walk(t, t.ints["root"], P.M, P.O, false, cr.s, sc, nullptr);
      } catch (exception& ex) { cr.s.err(ex.what()); }
      cr.done = true;
    }
    lock_guard<mutex> lk(mu); for (size_t r = 0; r < used.size(); r++) used[r] |= sc.used[r];
  };
  { // contexts are checked even after a master problem, so the report shows everything
    vector<thread> th; for (int k = 0; k < threads; k++) th.emplace_back(worker); for (auto& x : th) x.join();
  }
  for (size_t r = 0; r < used.size(); r++) used[r] |= msc.used[r];
  // aggregate
  Stats tot = ms; ll ctx_nodes = 0, ctx_leaves = 0, bad_ctx = 0;
  FILE* ft = fopen((outp + ".contexts.tsv").c_str(), "w");
  fprintf(ft, "context\tnodes\tleaves\tweighted\tover_budget\tmin_margin\tmin_margin_count\tmax_row\terrors\tfirst_error\n");
  for (auto& cr : res) {
    Stats& s = cr.s;
    fprintf(ft, "%lld\t%lld\t%lld\t%lld\t%lld\t%s\t%lld\t%lld\t%lld\t%s\n", cr.id, s.nodes, s.leaves, s.weighted, s.over,
            s.hasmin ? i128s(s.minmargin).c_str() : "NA", s.minmargin_count, s.maxrow, s.nerr, s.errs.empty() ? "" : s.errs[0].c_str());
    ctx_nodes += s.nodes; ctx_leaves += s.leaves;
    tot.nodes += s.nodes; tot.leaves += s.leaves; tot.weighted += s.weighted; tot.over += s.over; tot.pending += s.pending;
    tot.nerr += s.nerr; tot.maxrow = max(tot.maxrow, s.maxrow);
    if (s.hasmin) { if (!tot.hasmin || s.minmargin < tot.minmargin) { tot.minmargin = s.minmargin; tot.minmargin_count = 0; tot.hasmin = true; } if (s.minmargin == tot.minmargin) tot.minmargin_count += s.minmargin_count; }
    if (s.nerr) { bad_ctx++; if (fatal.size() < 40) fatal.push_back("ctx " + to_string(cr.id) + ": " + (s.errs.empty() ? "?" : s.errs[0])); }
    if (!cr.done) fatal.push_back("ctx not processed");
  }
  fclose(ft);
  for (auto& e : ms.errs) fatal.push_back("master tree: " + e);
  FILE* fu = fopen((outp + ".rowsused.txt").c_str(), "w"); ll nused = 0;
  for (size_t r = 0; r < used.size(); r++) if (used[r]) { fprintf(fu, "%zu\n", r); nused++; }
  fclose(fu);
  bool ok = fatal.empty() && tot.nerr == 0 && tot.pending == 0;
  FILE* fs = fopen((outp + ".summary.json").c_str(), "w");
  auto esc = [](const string& s) { string o; for (char c : s) { if (c == '"' || c == '\\') o += '\\'; if ((unsigned char)c >= 0x20) o += c; } return o; };
  fprintf(fs, "{\n \"packet\": \"%s\",\n \"verdict\": \"%s\",\n \"rows\": %zu,\n \"contexts\": %zu,\n \"ctx_files\": %zu,\n"
              " \"master_nodes\": %lld,\n \"master_leaves_counted\": %lld,\n \"master_leaves_field\": %lld,\n \"master_contexts_field\": %lld,\n"
              " \"context_nodes\": %lld,\n \"context_leaves\": %lld,\n \"total_nodes\": %lld,\n \"total_leaves\": %lld,\n"
              " \"weighted_leaves\": %lld,\n \"over_budget_leaves\": %lld,\n \"pending_leaves\": %lld,\n \"min_margin\": \"%s\",\n"
              " \"min_margin_leaf_count\": %lld,\n \"max_row_positive_weight\": %lld,\n \"rows_used_positive_weight\": %lld,\n"
              " \"contexts_with_errors\": %lld,\n \"error_count\": %lld,\n \"problems\": [",
          esc(dir).c_str(), ok ? "EXACT TREE" : "NOT CONFIRMED", rows.size(), ph.size(), files.size(), ms.nodes, ms.leaves,
          mt.ints.count("master_leaves") ? mt.ints["master_leaves"] : -1, mt.ints.count("contexts") ? mt.ints["contexts"] : -1,
          ctx_nodes, ctx_leaves, tot.nodes, tot.leaves, tot.weighted, tot.over, tot.pending, tot.hasmin ? i128s(tot.minmargin).c_str() : "NA",
          tot.minmargin_count, tot.maxrow, nused, bad_ctx, tot.nerr + (ll)fatal.size());
  for (size_t i = 0; i < fatal.size(); i++) fprintf(fs, "%s\n  \"%s\"", i ? "," : "", esc(fatal[i]).c_str());
  fprintf(fs, "]\n}\n");
  fclose(fs);
  FILE* in = fopen((outp + ".summary.json").c_str(), "r"); int c; while ((c = fgetc(in)) != EOF) putchar(c); fclose(in);
  return ok ? 0 : 1;
}
