// satcells.cpp -- vx1118, 18 Nov 2026. Independent, SAT-free, exhaustive exact check of geometric K-gon saturation.
//
// S: integer points (|coords| < 2^25). Claim: (a) S in general position, no K points in convex position;
// (b) every p with S+p in general position (p on no line through two points of S) is a vertex of a convex K-gon of S+p.
//
// (b) is decided on every open cell (2-face) of the arrangement of the C(n,2) lines through pairs of S: inside one
// open cell all signs orient(s_i,s_j,p) are constant, so the order type of S+p is constant.
//   cells:  every cell has a vertex of the arrangement on its boundary (>= 2 line directions) and looks like one of the
//           2k angular sectors between consecutive lines at that vertex (k lines through it). Each sector's sign vector
//           is exact: sign L(v) for lines not through v, sign(grad L . w) for lines through v, w = r1 + r2 strictly
//           inside the sector. Sign vectors are deduplicated; their number must equal the face count
//           F = 1 + L + sum_v (k_v - 1) (insertion argument / Euler), computed from the exact vertex multiplicities.
//   sample: q = v + w / (D M) with M chosen so no line not through v changes sign; then every orientation (s_i,s_j,q)
//           is re-evaluated from q's coordinates with GMP and must equal the cell's sign vector (and be nonzero).
//   test:   method 1: cap regions of the convex (K-1)-gons T of S (q beyond edge t_i t_{i+1}, inside both neighbouring
//           edge lines); the witness T+q is then re-checked definitionally (every 4-subset in convex position).
//           method 2: exact O(N^4) DP for the largest convex subset of S+q (lex-lowest vertex, angular order).
//           The two methods must agree on every cell. Failing cells are re-checked against every convex (K-1)-gon and,
//           for the first few, against every (K-1)-subset of S (brute force, definitional).
// Output: one line per cell "QX QY QD P t_1 .. t_{K-1}" (witness, CCW, q inserted after t_i...) or "QX QY QD F".
// The trusted replay of that file is check_cells.py (separate code, Python big integers).
//
// Build: g++ -O2 -std=c++17 -o satcells satcells.cpp -lgmpxx -lgmp
// Run:   ./satcells points.txt K samples_out.txt
#include <bits/stdc++.h>
#include <gmpxx.h>
using namespace std;
typedef long long ll;
typedef __int128 LL;

static int n, K, L, W;
static vector<ll> X, Y;
static vector<int8_t> O3;          // O3[(i*n+j)*n+k] = sign orient(s_i, s_j, s_k)
static vector<int> LID, LI, LJ;    // line l <-> pair LI[l] < LJ[l]
static vector<LL> LA, LB, LC;      // L_l(p) = A px + B py + C = orient(s_i, s_j, p)

static int sg(LL v) { return (v > 0) - (v < 0); }
static LL ab(LL v) { return v < 0 ? -v : v; }
static LL gcd128(LL a, LL b) { a = ab(a); b = ab(b); while (b) { LL t = a % b; a = b; b = t; } return a; }
static string s128(LL v) {
  if (v == 0) return "0";
  bool neg = v < 0; unsigned __int128 u = neg ? -(unsigned __int128)v : (unsigned __int128)v; string s;
  while (u) { s += char('0' + int(u % 10)); u /= 10; }
  if (neg) s += '-';
  reverse(s.begin(), s.end()); return s;
}
static mpz_class Z(LL v) { return mpz_class(s128(v)); }
[[noreturn]] static void die(const string& m) { fflush(stdout); fprintf(stderr, "FATAL: %s\n", m.c_str()); exit(2); }

// orientation in S + q; q has index n; qs[l] = sign orient(s_i, s_j, q) for line l = {i < j}
struct Orient {
  const int8_t* qs;
  int o(int a, int b, int c) const {
    if (a == n) return o(b, c, a);
    if (b == n) return o(c, a, b);
    if (c == n) return a < b ? qs[LID[a * n + b]] : -qs[LID[b * n + a]];
    return O3[((size_t)a * n + b) * n + c];
  }
  bool inTri(int p, int a, int b, int c) const { int s = o(a, b, c); return o(a, b, p) == s && o(b, c, p) == s && o(c, a, p) == s; }
  bool conv4(int a, int b, int c, int d) const { return !(inTri(d, a, b, c) || inTri(c, a, b, d) || inTri(b, a, c, d) || inTri(a, b, c, d)); }
  bool convexPos(const int* v, int m) const {  // Caratheodory: convex position <=> every 4-subset in convex position
    for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) for (int c = b + 1; c < m; c++) for (int d = c + 1; d < m; d++)
      if (!conv4(v[a], v[b], v[c], v[d])) return false;
    return true;
  }
};

// brute force: number of m-subsets of S in convex position (optionally each together with q = index n)
static ll bruteCount(int m, const Orient& O, bool withQ) {
  if (m > n) return 0;
  vector<int> c(m + 1); for (int i = 0; i < m; i++) c[i] = i;
  ll cnt = 0;
  while (true) {
    c[m] = n;
    if (O.convexPos(c.data(), withQ ? m + 1 : m)) cnt++;
    int i = m - 1; while (i >= 0 && c[i] == n - m + i) i--;
    if (i < 0) break;
    c[i]++; for (int j = i + 1; j < m; j++) c[j] = c[j - 1] + 1;
  }
  return cnt;
}

static vector<ll> dfsCnt;
static vector<vector<int>> gons;   // convex (K-1)-gons of S
static void dfs(vector<int>& cur, int start, const Orient& O) {
  int m = cur.size();
  for (int q = start; q < n; q++) {
    bool ok = true;
    for (int a = 0; a < m && ok; a++) for (int b = a + 1; b < m && ok; b++) for (int c = b + 1; c < m && ok; c++)
      if (!O.conv4(cur[a], cur[b], cur[c], q)) ok = false;
    if (!ok) continue;
    cur.push_back(q); dfsCnt[m + 1]++;
    if (m + 1 == K - 1) gons.push_back(cur);
    if (m + 1 < K) dfs(cur, q + 1, O);
    cur.pop_back();
  }
}

// method 2: size of the largest convex subset of S (N = n) or S + q (N = n + 1). upq[i] = +1 iff q is above s_i in
// (y, x) lexicographic order. Polygon counted at its lex-lowest vertex b; the others sorted by angle around b.
static int largestConvex(const Orient& O, int N, const int8_t* upq, int stopAt) {
  int best = min(N, 2);
  vector<int> U; vector<int> dp;
  for (int b = 0; b < N; b++) {
    U.clear();
    for (int i = 0; i < N; i++) {
      if (i == b) continue;
      bool above;
      if (i == n) above = upq[b] > 0;
      else if (b == n) above = upq[i] < 0;
      else above = (Y[i] > Y[b]) || (Y[i] == Y[b] && X[i] > X[b]);
      if (above) U.push_back(i);
    }
    for (size_t a = 1; a < U.size(); a++) {  // insertion sort: u before w iff orient(b, u, w) > 0
      int u = U[a]; size_t c = a;
      while (c > 0 && O.o(b, u, U[c - 1]) > 0) { U[c] = U[c - 1]; c--; }
      U[c] = u;
    }
    for (size_t a = 1; a < U.size(); a++) if (O.o(b, U[a - 1], U[a]) <= 0) die("angular sort");
    int m = U.size(); dp.assign((size_t)m * m, 0);
    for (int j = 0; j < m; j++) for (int i = 0; i < j; i++) {
      int v = 3;  // chain b -> U[i] -> U[j]
      for (int k = 0; k < i; k++) { int c = dp[k * m + i] + 1; if (c > v && O.o(U[k], U[i], U[j]) > 0) v = c; }
      dp[i * m + j] = v;
      if (v > best && O.o(U[i], U[j], b) > 0) { best = v; if (best >= stopAt) return best; }
    }
  }
  return best;
}

struct Cap { int l[3]; int8_t w[3]; int gon, edge; };

int main(int argc, char** argv) {
  if (argc < 4) die("usage: satcells points.txt K samples_out.txt");
  auto T0 = chrono::steady_clock::now();
  auto secs = [&]() { return chrono::duration<double>(chrono::steady_clock::now() - T0).count(); };
  K = atoi(argv[2]);
  if (K < 4) die("K >= 4");
  {
    ifstream in(argv[1]); if (!in) die("cannot read points");
    string line;
    while (getline(in, line)) {
      if (line.empty() || line[0] == '#') continue;
      istringstream ss(line); ll x, y;
      if (!(ss >> x >> y)) continue;
      X.push_back(x); Y.push_back(y);
    }
  }
  n = X.size();
  printf("input %s n=%d K=%d\n", argv[1], n, K);
  for (int i = 0; i < n; i++) if (llabs(X[i]) >= (1LL << 25) || llabs(Y[i]) >= (1LL << 25)) die("coordinate bound 2^25 violated");
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) if (X[i] == X[j] && Y[i] == Y[j]) die("repeated point");

  // ---- (a) general position, convex subsets
  O3.assign((size_t)n * n * n, 0);
  ll zeroTriples = 0;
  for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) for (int k = 0; k < n; k++) {
    LL v = (LL)(X[j] - X[i]) * (Y[k] - Y[i]) - (LL)(Y[j] - Y[i]) * (X[k] - X[i]);
    O3[((size_t)i * n + j) * n + k] = sg(v);
    if (i < j && j < k && v == 0) zeroTriples++;
  }
  printf("a.general_position collinear_triples=%lld %s\n", zeroTriples, zeroTriples ? "FAIL" : "OK");
  if (zeroTriples) die("S not in general position");
  Orient OS{nullptr};
  dfsCnt.assign(K + 2, 0); { vector<int> cur; dfs(cur, 0, OS); }
  printf("a.convex_subsets_by_size(dfs):"); for (int m = 3; m <= K; m++) printf(" %d:%lld", m, dfsCnt[m]); printf("\n");
  // SAT2 copy: SATCELLS_NO_BRUTE=1 skips the C(n,K) and C(n,K-1) brute force (infeasible for K = 9, n ~ 58); the DFS
  // count, the DP and the replay's own DP still decide (a).
  bool nb = getenv("SATCELLS_NO_BRUTE") != nullptr;
  if (nb) printf("a.bruteforce SKIPPED (SATCELLS_NO_BRUTE)\n");
  ll bfK = nb ? 0 : bruteCount(K, OS, false), bfK1 = nb ? dfsCnt[K - 1] : bruteCount(K - 1, OS, false);
  int lcS = largestConvex(OS, n, nullptr, 1 << 30);
  printf("a.bruteforce convex_%d-subsets=%lld convex_%d-subsets=%lld ; dp_largest_convex=%d ; %s  [%.1fs]\n", K, bfK, K - 1, bfK1, lcS,
         (bfK == 0 && dfsCnt[K] == 0 && bfK1 == dfsCnt[K - 1] && bfK1 > 0 && lcS == K - 1) ? "OK" : "FAIL", secs());
  if (bfK != 0 || dfsCnt[K] != 0 || bfK1 != dfsCnt[K - 1] || lcS != K - 1) die("(a) fails or methods disagree");

  // CCW order of each convex (K-1)-gon (insertion sort around its first vertex, then verify left turns)
  for (auto& g : gons) {
    int t0 = g[0];
    for (size_t a = 2; a < g.size(); a++) { int u = g[a]; size_t c = a; while (c > 1 && O3[((size_t)t0 * n + u) * n + g[c - 1]] > 0) { g[c] = g[c - 1]; c--; } g[c] = u; }
    int m = g.size();
    for (int i = 0; i < m; i++) if (O3[((size_t)g[i] * n + g[(i + 1) % m]) * n + g[(i + 2) % m]] <= 0) die("gon not CCW convex");
  }

  // ---- lines
  LID.assign(n * n, -1);
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) {
    LID[i * n + j] = LI.size(); LI.push_back(i); LJ.push_back(j);
    LA.push_back(-(LL)(Y[j] - Y[i])); LB.push_back((LL)(X[j] - X[i]));
    LC.push_back((LL)(Y[j] - Y[i]) * X[i] - (LL)(X[j] - X[i]) * Y[i]);
  }
  L = LI.size(); W = (L + 63) / 64;
  for (int l = 0; l < L; l++) for (int k = 0; k < n; k++)
    if (sg(LA[l] * X[k] + LB[l] * Y[k] + LC[l]) != O3[((size_t)LI[l] * n + LJ[l]) * n + k]) die("line form");

  // caps for method 1
  vector<Cap> caps;
  auto sigmaReq = [&](int a, int b, int r, int& l, int8_t& w) { if (a < b) { l = LID[a * n + b]; w = r; } else { l = LID[b * n + a]; w = -r; } };
  for (size_t gi = 0; gi < gons.size(); gi++) {
    const auto& g = gons[gi]; int m = g.size();
    for (int i = 0; i < m; i++) {
      int pv = g[(i - 1 + m) % m], a = g[i], b = g[(i + 1) % m], nx = g[(i + 2) % m];
      Cap c; c.gon = gi; c.edge = i;
      sigmaReq(a, b, -1, c.l[0], c.w[0]); sigmaReq(pv, a, +1, c.l[1], c.w[1]); sigmaReq(b, nx, +1, c.l[2], c.w[2]);
      caps.push_back(c);
    }
  }

  // ---- vertices of the arrangement (exact, reduced homogeneous coordinates, D > 0)
  map<array<LL, 3>, int> vmap;
  vector<array<LL, 3>> V; vector<vector<int>> VL; vector<ll> VG;
  ll parallel = 0;
  for (int l1 = 0; l1 < L; l1++) for (int l2 = l1 + 1; l2 < L; l2++) {
    LL D = LA[l1] * LB[l2] - LA[l2] * LB[l1];
    if (D == 0) {
      parallel++;
      if (sg(LA[l2] * X[LI[l1]] + LB[l2] * Y[LI[l1]] + LC[l2]) == 0) die("coincident lines");
      continue;
    }
    LL Xn = LB[l1] * LC[l2] - LB[l2] * LC[l1], Yn = LC[l1] * LA[l2] - LC[l2] * LA[l1];
    LL g = gcd128(gcd128(Xn, Yn), D); Xn /= g; Yn /= g; D /= g;
    if (D < 0) { Xn = -Xn; Yn = -Yn; D = -D; }
    array<LL, 3> key{Xn, Yn, D};
    auto it = vmap.find(key); int v;
    if (it == vmap.end()) { v = V.size(); vmap.emplace(key, v); V.push_back(key); VL.emplace_back(); VG.push_back(0); }
    else v = it->second;
    VL[v].push_back(l1); VL[v].push_back(l2); VG[v]++;
  }
  ll sumKm1 = 0, sumPairs = 0, samplesExpected = 0, atS = 0; map<int, ll> hist;
  for (size_t v = 0; v < V.size(); v++) {
    sort(VL[v].begin(), VL[v].end()); VL[v].erase(unique(VL[v].begin(), VL[v].end()), VL[v].end());
    ll k = VL[v].size();
    if (VG[v] != k * (k - 1) / 2) die("vertex multiplicity inconsistent");
    sumKm1 += k - 1; sumPairs += k * (k - 1) / 2; samplesExpected += 2 * k; hist[k]++;
    if (V[v][2] == 1) for (int i = 0; i < n; i++) if (V[v][0] == X[i] && V[v][1] == Y[i]) atS++;
  }
  ll pairsAll = (ll)L * (L - 1) / 2;
  if (sumPairs + parallel != pairsAll) die("pair count");
  ll Feuler = 1 + L + sumKm1;
  printf("b.lines=%d parallel_pairs=%lld vertices=%zu (at points of S: %lld) multiplicity_histogram:", L, parallel, V.size(), atS);
  for (auto& [k, c] : hist) printf(" k=%d:%lld", k, c);
  printf("\nb.sum_pairs_at_vertices=%lld + parallel=%lld = C(L,2)=%lld ; sum(k_v-1)=%lld ; F_euler = 1 + L + sum(k_v-1) = %lld  [%.1fs]\n",
         sumPairs, parallel, pairsAll, sumKm1, Feuler, secs());

  // ---- cells: one sign vector per angular sector at every vertex; deduplicate
  unordered_map<string, int> fmap; fmap.reserve(Feuler * 2);
  vector<uint64_t> fbits; struct Rep { int v; LL wx, wy; }; vector<Rep> reps;
  vector<LL> N(L); vector<uint64_t> base(W), bits(W);
  ll samples = 0;
  for (size_t v = 0; v < V.size(); v++) {
    LL Xv = V[v][0], Yv = V[v][1], Dv = V[v][2];
    fill(base.begin(), base.end(), 0);
    int through = 0;
    for (int l = 0; l < L; l++) {
      N[l] = LA[l] * Xv + LB[l] * Yv + LC[l] * Dv;
      if (N[l] == 0) through++; else if (N[l] > 0) base[l >> 6] |= 1ULL << (l & 63);
    }
    if (through != (int)VL[v].size()) die("lines through vertex");
    for (int l : VL[v]) if (N[l] != 0) die("vertex not on its line");
    struct Ray { LL x, y; };
    vector<Ray> R;
    for (int l : VL[v]) { R.push_back({LB[l], -LA[l]}); R.push_back({-LB[l], LA[l]}); }
    auto half = [](const Ray& r) { return (r.y > 0 || (r.y == 0 && r.x > 0)) ? 0 : 1; };
    sort(R.begin(), R.end(), [&](const Ray& a, const Ray& b) { int ha = half(a), hb = half(b); if (ha != hb) return ha < hb; return a.x * b.y - a.y * b.x > 0; });
    int m = R.size();
    for (int j = 0; j < m; j++) {
      const Ray& r1 = R[j]; const Ray& r2 = R[(j + 1) % m];
      if (r1.x * r2.y - r1.y * r2.x <= 0) die("sector not convex");
      LL wx = r1.x + r2.x, wy = r1.y + r2.y;
      bits = base;
      for (int l : VL[v]) { LL g = LA[l] * wx + LB[l] * wy; if (g == 0) die("w on a line"); if (g > 0) bits[l >> 6] |= 1ULL << (l & 63); }
      samples++;
      string key((const char*)bits.data(), W * 8);
      if (fmap.emplace(key, (int)reps.size()).second) { reps.push_back({(int)v, wx, wy}); fbits.insert(fbits.end(), bits.begin(), bits.end()); }
    }
  }
  ll F = reps.size();
  printf("b.sector_samples=%lld (expected sum 2k_v=%lld) distinct_cells=%lld F_euler=%lld %s  [%.1fs]\n", samples, samplesExpected, F, Feuler,
         (F == Feuler && samples == samplesExpected) ? "MATCH" : "MISMATCH", secs());
  if (F != Feuler) die("cell count differs from Euler count");

  // ---- explicit rational sample per cell, verified with GMP; octagon test by two methods
  FILE* out = fopen(argv[3], "w"); if (!out) die("cannot write samples");
  vector<int8_t> qs(L), upq(n);
  Orient OQ{qs.data()};
  vector<mpz_class> PX(n), PY(n); mpz_class QX, QY, QD, val, t;
  ll pass = 0, fail = 0, mismatch = 0, failBrute = 0; size_t maxBits = 0; LL maxM = 0;
  vector<int> wit(K + 1);
  for (ll f = 0; f < F; f++) {
    const Rep& rp = reps[f];
    LL Xv = V[rp.v][0], Yv = V[rp.v][1], Dv = V[rp.v][2];
    LL M = 1;
    for (int l = 0; l < L; l++) {
      LL Nl = LA[l] * Xv + LB[l] * Yv + LC[l] * Dv; if (Nl == 0) continue;
      LL g = LA[l] * rp.wx + LB[l] * rp.wy;
      if (g == 0 || sg(g) == sg(Nl)) continue;
      LL need = ab(g) / ab(Nl) + 1; if (need > M) M = need;
    }
    if (M > maxM) maxM = M;
    QX = Z(Xv) * Z(M) + Z(rp.wx); QY = Z(Yv) * Z(M) + Z(rp.wy); QD = Z(Dv) * Z(M);
    if (sgn(QD) <= 0) die("QD");
    maxBits = max({maxBits, mpz_sizeinbase(QX.get_mpz_t(), 2), mpz_sizeinbase(QY.get_mpz_t(), 2), mpz_sizeinbase(QD.get_mpz_t(), 2)});
    for (int i = 0; i < n; i++) { PX[i] = QX - QD * (long)X[i]; PY[i] = QY - QD * (long)Y[i]; }
    const uint64_t* fb = &fbits[f * W];
    for (int l = 0; l < L; l++) {  // definitional orientation of (s_i, s_j, q), q = (QX/QD, QY/QD)
      int i = LI[l], j = LJ[l];
      val = PY[i] * (long)(X[j] - X[i]) - PX[i] * (long)(Y[j] - Y[i]);
      int s = sgn(val);
      if (s == 0) die("sample on a line");
      int want = (fb[l >> 6] >> (l & 63) & 1) ? 1 : -1;
      if (s != want) die("sample sign differs from cell sign vector");
      qs[l] = s;
    }
    for (int i = 0; i < n; i++) {
      t = QD * (long)Y[i]; int c = cmp(QY, t);
      if (c == 0) { t = QD * (long)X[i]; c = cmp(QX, t); }
      if (c == 0) die("sample equals a point of S");
      upq[i] = c > 0 ? 1 : -1;
    }
    // method 1
    int found = -1;
    for (size_t c = 0; c < caps.size(); c++) {
      const Cap& cp = caps[c];
      if (qs[cp.l[0]] == cp.w[0] && qs[cp.l[1]] == cp.w[1] && qs[cp.l[2]] == cp.w[2]) { found = c; break; }
    }
    if (found >= 0) {
      const auto& g = gons[caps[found].gon];
      for (int i = 0; i < K - 1; i++) wit[i] = g[i];
      wit[K - 1] = n;
      if (!OQ.convexPos(wit.data(), K)) die("witness fails the 4-subset test");
    }
    // method 2
    int best = largestConvex(OQ, n + 1, upq.data(), K);
    bool p1 = found >= 0, p2 = best >= K;
    if (p1 != p2) { mismatch++; fprintf(stderr, "method mismatch at cell %lld\n", f); }
    fprintf(out, "%s %s %s", QX.get_str().c_str(), QY.get_str().c_str(), QD.get_str().c_str());
    if (p1) {
      const Cap& cp = caps[found]; const auto& g = gons[cp.gon];
      fprintf(out, " P");
      for (int i = 0; i < K - 1; i++) fprintf(out, " %d", g[i]);
      fprintf(out, " e%d\n", cp.edge);
      pass++;
    } else {
      fprintf(out, " F\n");
      fail++;
      for (const auto& g : gons) {  // every convex (K-1)-gon, definitional test (q first: 4-subsets with q tested first)
        wit[0] = n;
        for (int i = 0; i < K - 1; i++) wit[i + 1] = g[i];
        if (OQ.convexPos(wit.data(), K)) die("failing cell has a witness");
      }
      if (fail <= 3) { ll c = bruteCount(K - 1, OQ, true); if (c != 0) die("brute force finds a witness"); failBrute++; }
    }
    if ((f + 1) % 20000 == 0) { printf("  progress %lld/%lld pass=%lld fail=%lld [%.1fs]\n", f + 1, F, pass, fail, secs()); fflush(stdout); }
  }
  fclose(out);
  printf("b.cells=%lld pass=%lld fail=%lld method_mismatches=%lld failing_cells_bruteforced=%lld max_M=%s max_sample_bits=%zu\n",
         F, pass, fail, mismatch, failBrute, s128(maxM).c_str(), maxBits);
  printf("RESULT n=%d K=%d cells=%lld F_euler=%lld pass=%lld fail=%lld mismatch=%lld verdict=%s  [%.1fs]\n", n, K, F, Feuler, pass, fail, mismatch,
         (fail == 0 && mismatch == 0 && F == Feuler) ? "SATURATED" : (mismatch ? "ERROR" : "NOT_SATURATED"), secs());
  return mismatch ? 3 : 0;
}
