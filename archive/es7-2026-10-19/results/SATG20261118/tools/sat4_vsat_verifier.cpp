// vsat.cpp -- independent exact checker for n-gon saturation of planar integer point sets.
// Written 21 Nov 2026 by the REBUILD verifier of D-satg-descents. Shares no code with the worker's
// satcheck/satcheck_big, the record's satcells/check_cells.py, or VX2's vx2sat.
//
// Definitions (DDSZ; record SATG20261118 sec. 2): S (general position) is K-gon-saturated iff S has no K points
// in convex position and every q not on any line through two points of S is a vertex of a convex K-gon of S+q.
//
// Usage:
//   vsat check <points> <K> [samples.txt] [lemma]   rebuild path; optional replay of concrete samples with
//                                                   set comparison; optional sector-by-sector lemma check
//   vsat brute <points> <K>                         plain brute force over all K- and (K-1)-subsets
//
// Exactness: |coordinates| < 2^28 (asserted). Then coordinate differences < 2^29, crosses < 2^59, fraction
// comparisons < 2^119, vertex numerators < 2^89: all fit in signed __int128. Replay samples are bounded at
// run time (|QX|,|QY| < 2^80, 0 < QD < 2^50, so each orientation value < 2^112).
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;
typedef __int128 i128;
typedef unsigned __int128 u128;

static int n, K, L, W;
static vector<ll> X, Y;
static vector<int8_t> OT;            // OT[(i*n+j)*n+k] = sign of orient(s_i,s_j,s_k)
static vector<int> LID;              // LID[i*n+j] = line index of {i,j}
static vector<pair<int,int>> LN;     // line index -> (i,j), i<j, lexicographic

[[noreturn]] static void die(const string& s) { printf("CHECK_FAILED %s\n", s.c_str()); fflush(stdout); exit(2); }
static inline int sg(i128 v) { return (v > 0) - (v < 0); }
static inline int ot(int i, int j, int k) { return OT[((size_t)i * n + j) * n + k]; }

static void readPoints(const char* path) {
  ifstream f(path);
  if (!f) die("cannot open points file");
  string tok; vector<ll> v;
  while (f >> tok) {
    size_t p = 0; if (tok[0] == '-' || tok[0] == '+') p = 1;
    if (p >= tok.size() || tok.size() - p > 12) die("bad token " + tok);
    for (size_t q = p; q < tok.size(); q++) if (!isdigit((unsigned char)tok[q])) die("bad token " + tok);
    v.push_back(stoll(tok));
  }
  if (v.size() % 2) die("odd number of integers");
  n = v.size() / 2;
  if (n < 3 || n > 64) die("n out of range");
  for (int i = 0; i < n; i++) {
    X.push_back(v[2 * i]); Y.push_back(v[2 * i + 1]);
    if (llabs(X[i]) >= (1LL << 28) || llabs(Y[i]) >= (1LL << 28)) die("coordinate too large");
  }
}

static void buildBasics() {
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++)
    if (X[i] == X[j] && Y[i] == Y[j]) die("repeated point");
  OT.assign((size_t)n * n * n, 0);
  for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) for (int k = 0; k < n; k++) {
    i128 c = (i128)(X[j] - X[i]) * (Y[k] - Y[i]) - (i128)(Y[j] - Y[i]) * (X[k] - X[i]);
    OT[((size_t)i * n + j) * n + k] = sg(c);
  }
  long coll = 0;
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) for (int k = j + 1; k < n; k++) if (ot(i, j, k) == 0) coll++;
  printf("A.general_position collinear_triples=%ld (of C(%d,3))\n", coll, n);
  if (coll) die("not in general position");
  LID.assign(n * n, -1);
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) { LID[i * n + j] = LID[j * n + i] = LN.size(); LN.push_back({i, j}); }
  L = LN.size(); W = (L + 63) / 64;
}

// ---------- convex subsets ----------
static inline bool inTri(int z, int a, int b, int c) {  // z strictly inside triangle abc (general position)
  int s = ot(a, b, c);
  return ot(a, b, z) == s && ot(b, c, z) == s && ot(c, a, z) == s;
}
static vector<ll> convCount;
static vector<vector<int>> polys;   // all convex (K-1)-subsets, later put in CCW order
static ll kgons = 0;
static bool extendsConvex(const vector<int>& cur, int j) {
  int m = cur.size();
  for (int x = 0; x < m; x++) for (int y = x + 1; y < m; y++) for (int z = y + 1; z < m; z++) {
    int a = cur[x], b = cur[y], c = cur[z];
    if (inTri(j, a, b, c) || inTri(a, j, b, c) || inTri(b, j, a, c) || inTri(c, j, a, b)) return false;
  }
  return true;
}
static void dfs(vector<int>& cur, int start) {
  int m = cur.size();
  convCount[m]++;
  if (m == K - 1) polys.push_back(cur);
  if (m == K) { kgons++; return; }
  for (int j = start; j < n; j++) if (extendsConvex(cur, j)) { cur.push_back(j); dfs(cur, j + 1); cur.pop_back(); }
}
static void orderCCW(vector<int>& P) {
  int v0 = P[0];
  for (int v : P) if (X[v] < X[v0] || (X[v] == X[v0] && Y[v] < Y[v0])) v0 = v;
  vector<int> rest; for (int v : P) if (v != v0) rest.push_back(v);
  sort(rest.begin(), rest.end(), [&](int a, int b) { return ot(v0, a, b) > 0; });
  P.clear(); P.push_back(v0); for (int v : rest) P.push_back(v);
  int m = P.size();
  for (int e = 0; e < m; e++) if (ot(P[e], P[(e + 1) % m], P[(e + 2) % m]) <= 0) die("polygon not convex after ordering");
}

// ---------- sign vectors ----------
struct VecSet {
  int W; vector<uint64_t> data; vector<int32_t> tab; size_t mask; int cnt = 0;
  void init(int w, size_t expect) { W = w; size_t s = 1; while (s < 4 * expect + 16) s <<= 1; tab.assign(s, -1); mask = s - 1; data.reserve(expect * w); }
  static uint64_t h(const uint64_t* v, int W) { uint64_t x = 0x9E3779B97F4A7C15ULL; for (int i = 0; i < W; i++) { x ^= v[i]; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; } return x; }
  void grow() {
    size_t s = tab.size() * 2; tab.assign(s, -1); mask = s - 1;
    for (int id = 0; id < cnt; id++) { size_t p = h(&data[(size_t)id * W], W) & mask; while (tab[p] >= 0) p = (p + 1) & mask; tab[p] = id; }
  }
  int find(const uint64_t* v) const {
    size_t p = h(v, W) & mask;
    while (tab[p] >= 0) { if (memcmp(&data[(size_t)tab[p] * W], v, 8 * W) == 0) return tab[p]; p = (p + 1) & mask; }
    return -1;
  }
  int insert(const uint64_t* v, bool& isNew) {
    if ((size_t)(cnt + 1) * 2 > tab.size()) grow();
    size_t p = h(v, W) & mask;
    while (tab[p] >= 0) { if (memcmp(&data[(size_t)tab[p] * W], v, 8 * W) == 0) { isNew = false; return tab[p]; } p = (p + 1) & mask; }
    tab[p] = cnt; data.insert(data.end(), v, v + W); isNew = true; return cnt++;
  }
  const uint64_t* at(int id) const { return &data[(size_t)id * W]; }
};
static inline int bitOf(const uint64_t* v, int m) { return (v[m >> 6] >> (m & 63)) & 1; }
// sign of orient(s_a, s_b, q) for the cell with sign vector v (bit m = 1 iff orient(s_i,s_j,q) > 0, (i,j)=LN[m], i<j)
static inline int sq(const uint64_t* v, int a, int b) { int s = bitOf(v, LID[a * n + b]) ? 1 : -1; return a < b ? s : -s; }
// generic orientation over S + q, index n = q
static inline int og(const uint64_t* v, int i, int j, int k) {
  if (i == n) return sq(v, j, k);
  if (j == n) return sq(v, k, i);
  if (k == n) return sq(v, i, j);
  return ot(i, j, k);
}
static bool convexPositionG(const uint64_t* v, const vector<int>& T) {  // 4-point test over S + q
  int m = T.size();
  for (int zi = 0; zi < m; zi++) {
    int z = T[zi];
    for (int x = 0; x < m; x++) if (x != zi) for (int y = x + 1; y < m; y++) if (y != zi) for (int w = y + 1; w < m; w++) if (w != zi) {
      int a = T[x], b = T[y], c = T[w];
      int s = og(v, a, b, c);
      if (og(v, a, b, z) == s && og(v, b, c, z) == s && og(v, c, a, z) == s) return false;
    }
  }
  return true;
}

// ---------- Euler count ----------
static i128 gcd128(i128 a, i128 b) { u128 x = a < 0 ? -(u128)a : a, y = b < 0 ? -(u128)b : b; while (y) { u128 t = x % y; x = y; y = t; } return (i128)x; }
struct V3 { i128 x, y, d; bool operator<(const V3& o) const { if (x != o.x) return x < o.x; if (y != o.y) return y < o.y; return d < o.d; } bool operator==(const V3& o) const { return x == o.x && y == o.y && d == o.d; } };
static ll F_euler = 0, V_count = 0, parallelPairs = 0, sumK = 0;
static map<ll, ll> khist;
static void eulerCount() {
  vector<V3> vs; vs.reserve((size_t)L * (L - 1) / 2);
  for (int l1 = 0; l1 < L; l1++) {
    int i = LN[l1].first, j = LN[l1].second; ll dx = X[j] - X[i], dy = Y[j] - Y[i];
    for (int l2 = l1 + 1; l2 < L; l2++) {
      int a = LN[l2].first, b = LN[l2].second; ll ex = X[b] - X[a], ey = Y[b] - Y[a];
      i128 A = (i128)ex * (Y[i] - Y[a]) - (i128)ey * (X[i] - X[a]);
      i128 B = (i128)ex * dy - (i128)ey * dx;
      if (B == 0) { if (A == 0) die("coincident lines"); parallelPairs++; continue; }
      i128 xn = (i128)X[i] * B - A * dx, yn = (i128)Y[i] * B - A * dy, d = B;
      if (d < 0) { xn = -xn; yn = -yn; d = -d; }
      i128 g = gcd128(gcd128(xn, yn), d); xn /= g; yn /= g; d /= g;
      vs.push_back({xn, yn, d});
    }
  }
  sort(vs.begin(), vs.end());
  ll sumKm1 = 0;
  for (size_t p = 0; p < vs.size();) {
    size_t q = p; while (q < vs.size() && vs[q] == vs[p]) q++;
    ll r = q - p;  // r = C(k,2) pairs meet at this vertex
    ll k = (ll)llround((1.0 + sqrt(1.0 + 8.0 * (double)r)) / 2.0);
    if (k * (k - 1) / 2 != r) die("vertex pair count is not a binomial");
    V_count++; sumKm1 += k - 1; sumK += k; khist[k]++;
    p = q;
  }
  F_euler = 1 + L + sumKm1;
  printf("C.lines=%d parallel_pairs=%lld vertices=%lld hist(k:count)=", L, parallelPairs, V_count);
  for (auto& e : khist) printf("%lld:%lld ", e.first, e.second);
  printf(" sum(k_v-1)=%lld F_euler=%lld\n", sumKm1, F_euler);
}

// ---------- rebuild: one probe on each side of every edge of every line ----------
static VecSet cells;
static ll probes = 0, sumDistinctOnLines = 0;
static void enumerateCells() {
  cells.init(W, F_euler);
  vector<uint64_t> cur(W);
  struct Cr { i128 num, den; int m; };
  vector<Cr> cr; cr.reserve(L);
  for (int l = 0; l < L; l++) {
    int i = LN[l].first, j = LN[l].second; ll dx = X[j] - X[i], dy = Y[j] - Y[i];
    fill(cur.begin(), cur.end(), 0); cr.clear();
    for (int m = 0; m < L; m++) if (m != l) {
      int a = LN[m].first, b = LN[m].second; ll ex = X[b] - X[a], ey = Y[b] - Y[a];
      // orient(s_a,s_b, s_i + t d) = A + t B
      i128 A = (i128)ex * (Y[i] - Y[a]) - (i128)ey * (X[i] - X[a]);
      i128 B = (i128)ex * dy - (i128)ey * dx;
      if (B == 0) { if (A == 0) die("coincident lines"); if (A > 0) cur[m >> 6] |= 1ULL << (m & 63); continue; }
      // crossing at t_m = -A/B; for t < t_m the sign is -sign(B)
      if (B < 0) cur[m >> 6] |= 1ULL << (m & 63);
      i128 num = -A, den = B; if (den < 0) { num = -num; den = -den; }
      cr.push_back({num, den, m});
    }
    sort(cr.begin(), cr.end(), [](const Cr& p, const Cr& q) { return p.num * q.den < q.num * p.den; });
    auto emit = [&]() {
      bool nw;
      cur[l >> 6] |= 1ULL << (l & 63); cells.insert(cur.data(), nw);
      cur[l >> 6] &= ~(1ULL << (l & 63)); cells.insert(cur.data(), nw);
      probes += 2;
      if ((ll)cells.cnt > F_euler) die("more distinct sign vectors than F_euler");
    };
    emit();
    for (size_t p = 0; p < cr.size();) {
      size_t q = p; while (q < cr.size() && cr[q].num * cr[p].den == cr[p].num * cr[q].den) q++;
      for (size_t r = p; r < q; r++) cur[cr[r].m >> 6] ^= 1ULL << (cr[r].m & 63);
      sumDistinctOnLines++;
      emit();
      p = q;
    }
  }
  printf("D.rebuild probes=%lld distinct_sign_vectors=%d F_euler=%lld  sum_l(distinct vertices on l)=%lld sum_v k_v=%lld\n",
         probes, cells.cnt, F_euler, sumDistinctOnLines, sumK);
  if ((ll)cells.cnt != F_euler) die("distinct sign vectors != F_euler");
  if (sumDistinctOnLines != sumK) die("incidence count mismatch");
}

// ---------- per-cell decision ----------
struct PE { int m; int visBit; };
static vector<vector<PE>> polyEdges;
static vector<char> cellPass;
static vector<int> cellWit;
static ll nPass = 0, nFail = 0;
static void decideCells() {
  polyEdges.clear();
  for (auto& P : polys) {
    vector<PE> es; int m = P.size();
    for (int e = 0; e < m; e++) { int a = P[e], b = P[(e + 1) % m]; es.push_back({LID[a * n + b], a < b ? 0 : 1}); }
    polyEdges.push_back(es);
  }
  cellPass.assign(cells.cnt, 0); cellWit.assign(cells.cnt, -1);
  vector<int> T;
  for (int c = 0; c < cells.cnt; c++) {
    const uint64_t* v = cells.at(c);
    int wit = -1;
    for (size_t pi = 0; pi < polyEdges.size() && wit < 0; pi++) {
      int vis = 0;
      for (auto& e : polyEdges[pi]) { if (bitOf(v, e.m) == e.visBit) { if (++vis > 1) break; } }
      if (vis == 1) wit = pi;
    }
    if (wit >= 0) {  // definition-level re-check: P + q in convex position (4-point test)
      T = polys[wit]; T.push_back(n);
      if (!convexPositionG(v, T)) die("cap test and 4-point test disagree (pass)");
      cellPass[c] = 1; cellWit[c] = wit; nPass++;
    } else {         // definition-level re-check against every convex (K-1)-gon
      for (auto& P : polys) { T = P; T.push_back(n); if (convexPositionG(v, T)) die("cap test and 4-point test disagree (fail)"); }
      nFail++;
    }
  }
  printf("E.cells=%d pass(4-point verified)=%lld fail(all %zu polygons rejected by 4-point test)=%lld\n", cells.cnt, nPass, polys.size(), nFail);
}

// ---------- replay of concrete samples ----------
static bool parse128(const string& s, i128& out) {
  size_t p = 0; bool neg = false;
  if (p < s.size() && (s[p] == '-' || s[p] == '+')) { neg = s[p] == '-'; p++; }
  if (p >= s.size() || s.size() - p > 30) return false;
  i128 v = 0; for (; p < s.size(); p++) { if (!isdigit((unsigned char)s[p])) return false; v = v * 10 + (s[p] - '0'); }
  out = neg ? -v : v; return true;
}
static void replay(const char* path) {
  ifstream f(path); if (!f) die("cannot open samples");
  VecSet seen; seen.init(W, F_euler);
  const i128 QB = (i128)1 << 80, DB = (i128)1 << 50;
  ll ns = 0, onLine = 0, dup = 0, badFmt = 0, wpass = 0, wbad = 0, tagF = 0, notInRebuild = 0, verdictDiff = 0;
  string line; vector<uint64_t> v(W); vector<int> T;
  while (getline(f, line)) {
    if (line.empty()) continue;
    istringstream is(line); string a, b, c, tag; is >> a >> b >> c >> tag;
    i128 QX, QY, QD;
    ns++;
    if (!parse128(a, QX) || !parse128(b, QY) || !parse128(c, QD) || QD <= 0 || QD >= DB || QX >= QB || -QX >= QB || QY >= QB || -QY >= QB) { badFmt++; continue; }
    fill(v.begin(), v.end(), 0); bool zero = false;
    for (int m = 0; m < L; m++) {
      int i = LN[m].first, j = LN[m].second;
      i128 PX = QX - (i128)X[i] * QD, PY = QY - (i128)Y[i] * QD;          // QD*(q - s_i)
      i128 val = (i128)(X[j] - X[i]) * PY - (i128)(Y[j] - Y[i]) * PX;      // QD*orient(s_i,s_j,q), QD>0
      if (val == 0) { zero = true; break; }
      if (val > 0) v[m >> 6] |= 1ULL << (m & 63);
    }
    if (zero) { onLine++; continue; }
    bool nw; seen.insert(v.data(), nw); if (!nw) dup++;
    int cid = cells.find(v.data()); if (cid < 0) notInRebuild++;
    if (tag == "P") {
      T.clear(); string t; bool ok = true;
      for (int r = 0; r < K - 1; r++) { if (!(is >> t)) { ok = false; break; } i128 tv; if (!parse128(t, tv) || tv < 0 || tv >= n) { ok = false; break; } T.push_back((int)tv); }
      if (ok) { vector<int> s2 = T; sort(s2.begin(), s2.end()); if (unique(s2.begin(), s2.end()) != s2.end()) ok = false; }
      if (ok) { T.push_back(n); ok = convexPositionG(v.data(), T); }
      if (ok) wpass++; else wbad++;
      if (cid >= 0 && !cellPass[cid]) verdictDiff++;
    } else if (tag == "F") { tagF++; if (cid >= 0 && cellPass[cid]) verdictDiff++; }
    else badFmt++;
  }
  bool ok = badFmt == 0 && onLine == 0 && dup == 0 && wbad == 0 && notInRebuild == 0 && ns == F_euler && seen.cnt == F_euler;
  printf("R.replay samples=%lld distinct=%d F_euler=%lld on_line=%lld duplicate=%lld bad_format=%lld witness_verified=%lld witness_bad=%lld tagF=%lld not_in_rebuild_set=%lld verdict_differs=%lld -> %s\n",
         ns, seen.cnt, F_euler, onLine, dup, badFmt, wpass, wbad, tagF, notInRebuild, verdictDiff,
         ok ? (tagF == 0 && wpass == F_euler ? "REPLAY_SATURATED (sets equal)" : "REPLAY_NOT_SATURATED") : "REPLAY_REJECTED");
}

// ---------- lemma: sector-by-sector check ----------
static void lemmaCheck() {
  ll sectors = 0, critUncov = 0, cellFailSect = 0, mism = 0, missing = 0;
  vector<char> adj(cells.cnt, 0);
  vector<uint64_t> v(W);
  for (int p = 0; p < n; p++) {
    vector<pair<ll, ll>> dirs;
    for (int x = 0; x < n; x++) if (x != p) { dirs.push_back({X[x] - X[p], Y[x] - Y[p]}); dirs.push_back({X[p] - X[x], Y[p] - Y[x]}); }
    auto half = [](const pair<ll, ll>& d) { return (d.second > 0 || (d.second == 0 && d.first > 0)) ? 0 : 1; };
    sort(dirs.begin(), dirs.end(), [&](const pair<ll, ll>& a, const pair<ll, ll>& b) {
      int ha = half(a), hb = half(b); if (ha != hb) return ha < hb;
      return (i128)a.first * b.second - (i128)a.second * b.first > 0; });
    vector<int> mine; for (size_t pi = 0; pi < polys.size(); pi++) for (int u : polys[pi]) if (u == p) { mine.push_back(pi); break; }
    int D = dirs.size();
    for (int k = 0; k < D; k++) {
      auto d1 = dirs[k], d2 = dirs[(k + 1) % D];
      if ((i128)d1.first * d2.second - (i128)d1.second * d2.first <= 0) die("sector angle not in (0,pi)");
      ll ux = d1.first + d2.first, uy = d1.second + d2.second;
      fill(v.begin(), v.end(), 0);
      for (int m = 0; m < L; m++) {
        int a = LN[m].first, b = LN[m].second; int s;
        if (a == p || b == p) { i128 c = (i128)(X[b] - X[a]) * uy - (i128)(Y[b] - Y[a]) * ux; s = sg(c); if (!s) die("sector direction on a line"); }
        else s = ot(a, b, p);
        if (s > 0) v[m >> 6] |= 1ULL << (m & 63);
      }
      sectors++;
      int cid = cells.find(v.data());
      if (cid < 0) { missing++; continue; }
      adj[cid] = 1;
      bool crit = false;
      for (int pi : mine) {
        int side = 0; bool okp = true;
        for (int w : polys[pi]) if (w != p) {
          int s = sg((i128)ux * (Y[w] - Y[p]) - (i128)uy * (X[w] - X[p]));
          if (s == 0) die("polygon vertex on sector line");
          if (side == 0) side = s; else if (s != side) { okp = false; break; }
        }
        if (okp) { crit = true; break; }
      }
      if (!crit) critUncov++;
      if (!cellPass[cid]) cellFailSect++;
      if (crit != (bool)cellPass[cid]) mism++;
    }
  }
  ll failAdj = 0, failNonAdj = 0;
  for (int c = 0; c < cells.cnt; c++) if (!cellPass[c]) { if (adj[c]) failAdj++; else failNonAdj++; }
  printf("G.lemma sectors=%lld missing_in_cell_map=%lld criterion_uncovered=%lld failing_(cell,point)_pairs=%lld mismatches=%lld failing_cells_adjacent=%lld failing_cells_not_adjacent=%lld\n",
         sectors, missing, critUncov, cellFailSect, mism, failAdj, failNonAdj);
}

// ---------- brute force ----------
static void brute() {
  vector<uint64_t> tri((size_t)n * n * n, 0);
  for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) {
    uint64_t m = 0; for (int z = 0; z < n; z++) if (z != a && z != b && z != c && inTri(z, a, b, c)) m |= 1ULL << z;
    tri[((size_t)a * n + b) * n + c] = m;
  }
  for (int k : {K - 1, K}) {
    ll total = 0, conv = 0;
    uint64_t lim = (n == 64) ? 0 : (1ULL << n);
    uint64_t s = (1ULL << k) - 1;
    int idx[64];
    while (true) {
      total++;
      int c = 0; for (uint64_t t = s; t; t &= t - 1) idx[c++] = __builtin_ctzll(t);
      bool ok = true;
      for (int x = 0; x < c && ok; x++) for (int y = x + 1; y < c && ok; y++) {
        const uint64_t* row = &tri[((size_t)idx[x] * n + idx[y]) * n];
        for (int z = y + 1; z < c; z++) if (row[idx[z]] & s) { ok = false; break; }
      }
      if (ok) conv++;
      uint64_t lo = s & -s, r = s + lo;           // Gosper's hack: next subset of the same size
      if (r == 0 || (lim && r >= lim)) break;
      s = (((r ^ s) >> 2) / lo) | r;
      if (lim && s >= lim) break;
    }
    printf("B.brute k=%d subsets=%lld convex=%lld\n", k, total, conv);
  }
}

int main(int argc, char** argv) {
  if (argc < 4) { fprintf(stderr, "usage: vsat check|brute <points> <K> [samples] [lemma]\n"); return 1; }
  string mode = argv[1]; K = atoi(argv[3]);
  readPoints(argv[2]);
  if (K < 4 || K > 12) die("K out of range");
  printf("vsat mode=%s points=%s n=%d K=%d\n", mode.c_str(), argv[2], n, K);
  buildBasics();
  if (mode == "brute") { brute(); return 0; }
  convCount.assign(K + 1, 0);
  vector<int> cur; dfs(cur, 0);
  printf("B.dfs convex k-subsets k=3..%d:", K); for (int k = 3; k <= K; k++) printf(" %lld", convCount[k]); printf("  (K-gons %lld)\n", kgons);
  for (auto& P : polys) orderCCW(P);
  bool sat = true;
  if (kgons) { printf("S contains a convex %d-gon\n", K); sat = false; }
  if (convCount[K - 1] == 0) die("no convex (K-1)-gon");
  eulerCount();
  enumerateCells();
  decideCells();
  if (nFail) sat = false;
  if (argc >= 5 && string(argv[4]) != "-") replay(argv[4]);
  if (argc >= 6 && string(argv[5]) == "lemma") lemmaCheck();
  printf("VERDICT %s n=%d K=%d cells=%d fail=%lld kgons=%lld\n", sat ? "SATURATED" : "NOT_SATURATED", n, K, cells.cnt, nFail, kgons);
  return 0;
}
