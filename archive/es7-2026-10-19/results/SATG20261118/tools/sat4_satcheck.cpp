// satcheck.cpp -- fresh exact checker for K-gon saturation (worker satg, 21 Nov 2026). Shares no code with the
// record's satcells.cpp / check_cells.py / vx2sat.cpp or with the finder sat3ls8.cpp.
//
// Usage: satcheck points.txt K
//
// (A) input: distinct integer points, |x|,|y| < 2^30 (so every product below fits in __int128: coordinate
//     differences < 2^31, cross products < 2^63, cross-multiplied comparisons < 2^126).
// (B) general position: orient(a,b,c) != 0 for all triples.
// (C) convex subsets of S: (C1) enumeration of all subsets in convex position, grown in increasing index order with
//     the "exactly one visible edge" test (hereditary, so complete); counts per size; must find no K-subset;
//     (C2) O(n^4) DP over the lowest vertex: largest convex subset; C1 and C2 must both give K-1.
// (D) cells: every open cell of the arrangement of the L = C(n,2) lines touches an edge (an open segment or ray of
//     a line between consecutive distinct crossing points). For each line l = (i,j), parametrise P_i + t (P_j - P_i);
//     the crossing parameter of another line m is t_m = num_m / den_m (exact). The sign of orient(m, P_i + t D) is
//     den_m (t - t_m), so on the k-th edge it is sign(den_m) * (+1 if t_m lies at or before the edge's left end,
//     else -1); parallel lines have a constant sign. Points just off the edge's interior on side s of l lie in one
//     open cell whose sign vector is (those signs; s for l). All cells are met; equal sign vectors = same cell
//     (a sign vector defines an intersection of open half-planes, which is convex). Distinct vectors are counted
//     and must equal the Euler count F = 1 + L + sum_v (k_v - 1) (vertices counted once, from their lowest line).
// (E) per cell, q is abstract: the chirotope of S + q is O3 on S and the cell's sign vector for triples (a,b,q).
//     Pass: a convex (K-1)-gon P of S from (C1) with exactly one edge visible from q, VERIFIED by the 4-point test
//     on P + q (no point inside the triangle of three others). Fail: no polygon works; every failing cell is then
//     re-decided by an independent DP (convex chains anchored at q, all first vertices) that must find no K-gon.
// Verdict SATURATED iff (A)-(D) hold, every cell passes with a verified witness, and no check disagrees.
#include <bits/stdc++.h>
using namespace std;
typedef long long ll; typedef __int128 i128;

int n, K, L; vector<ll> X, Y; vector<signed char> O3; vector<int> LI;  // LI[a*n+b] = line index of {a,b}
static inline int sg(i128 v) { return (v > 0) - (v < 0); }
static inline int orS(int a, int b, int c) {
  return sg((i128)(X[b] - X[a]) * (Y[c] - Y[a]) - (i128)(Y[b] - Y[a]) * (X[c] - X[a]));
}
static inline int o3(int a, int b, int c) { return O3[((size_t)a * n + b) * n + c]; }

// chirotope of S + q (q = index n) for one cell: bits[l] = 1 iff orient(a,b,q) > 0 for line l = {a<b}
struct Chi {
  const vector<uint64_t>* bits;
  int sq(int a, int b) const {  // sign of orient(a,b,q), a != b in S
    int l = LI[a * n + b]; int s = ((*bits)[l >> 6] >> (l & 63)) & 1 ? 1 : -1;
    return a < b ? s : -s;
  }
  int operator()(int a, int b, int c) const {
    if (a == n) return sq(b, c);      // orient(q,b,c) = orient(b,c,q)
    if (b == n) return sq(c, a);      // orient(a,q,c) = orient(c,a,q)
    if (c == n) return sq(a, b);
    return o3(a, b, c);
  }
};

template <class F> bool inConvexPosition4(const vector<int>& P, const F& chi) {  // 4-point test
  int m = P.size();
  for (int a = 0; a < m; a++) for (int b = a + 1; b < m; b++) for (int c = b + 1; c < m; c++) {
    int s = chi(P[a], P[b], P[c]); if (s == 0) return false;
    for (int d = 0; d < m; d++) if (d != a && d != b && d != c)
      if (chi(P[a], P[b], P[d]) == s && chi(P[b], P[c], P[d]) == s && chi(P[c], P[a], P[d]) == s) return false;
  }
  return true;
}

// largest convex polygon having `anchor` as a vertex with all other vertices in `cand`, which must lie in an open
// half-plane through the anchor and be sorted by angle (chi(anchor, c_i, c_j) > 0 for i < j); `first` >= 0 forces
// the first vertex after the anchor to be cand[first].
template <class F> int bestAnchored(int anchor, const vector<int>& c, const F& chi, int first) {
  int m = c.size(), best = 1 + (m > 0 ? 1 : 0);
  if (m < 2) return best;
  vector<int> dp((size_t)m * m, 0);  // dp[i*m+j]: vertices of a left-turning chain anchor -> ... -> c_i -> c_j
  for (int j = 0; j < m; j++) for (int i = 0; i < j; i++) {
    int v = 0;
    if (first < 0 || i == first) v = 3;
    for (int h = 0; h < i; h++) { int w = dp[(size_t)h * m + i]; if (w && w + 1 > v && chi(c[h], c[i], c[j]) > 0) v = w + 1; }
    dp[(size_t)i * m + j] = v;
    if (v && chi(c[i], c[j], anchor) > 0) best = max(best, v);
  }
  return best;
}

int main(int argc, char** argv) {
  if (argc < 3) { fprintf(stderr, "usage: satcheck points.txt K\n"); return 2; }
  K = atoi(argv[2]);
  { ifstream in(argv[1]); if (!in) { printf("VERDICT CHECK_FAILED cannot_read\n"); return 1; } string line;
    while (getline(in, line)) { if (line.empty() || line[0] == '#') continue; istringstream ss(line); ll x, y; if (ss >> x >> y) { X.push_back(x); Y.push_back(y); } } }
  n = X.size();
  printf("input %s n=%d K=%d\n", argv[1], n, K);
  auto fail = [&](const char* why) { printf("VERDICT CHECK_FAILED %s\n", why); exit(1); };
  if (n < 3 || K < 4 || n > 120) fail("size");
  for (int i = 0; i < n; i++) if (llabs(X[i]) >= (1LL << 30) || llabs(Y[i]) >= (1LL << 30)) fail("coordinate_bound");
  { set<pair<ll,ll>> s; for (int i = 0; i < n; i++) s.insert({X[i], Y[i]}); if ((int)s.size() != n) fail("repeated_point"); }
  // (B)
  O3.assign((size_t)n * n * n, 0); long coll = 0;
  for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) for (int c = 0; c < n; c++) {
    if (a == b || b == c || a == c) continue;
    int s = orS(a, b, c); O3[((size_t)a * n + b) * n + c] = s; if (s == 0 && a < b && b < c) coll++;
  }
  printf("B.collinear_triples=%ld\n", coll); if (coll) fail("not_in_general_position");
  auto chiS = [&](int a, int b, int c) { return o3(a, b, c); };
  // (C1) convex subsets by growth in increasing index order; polygons kept CCW
  vector<long> cnt(K + 1, 0); vector<vector<int>> polys;  // convex (K-1)-gons, CCW
  {
    vector<int> poly;
    function<void(int)> grow = [&](int last) {
      int m = poly.size(); cnt[m]++;
      if (m == K - 1) polys.push_back(poly);
      if (m == K) return;
      for (int z = last + 1; z < n; z++) {
        if (m < 2) { poly.push_back(z); grow(z); poly.pop_back(); continue; }
        if (m == 2) {  // triangle: make it CCW
          vector<int> save = poly; if (o3(poly[0], poly[1], z) > 0) poly = {poly[0], poly[1], z}; else poly = {poly[0], z, poly[1]};
          grow(z); poly = save; continue;
        }
        int vis = 0, at = -1;
        for (int i = 0; i < m && vis < 2; i++) if (o3(poly[i], poly[(i + 1) % m], z) < 0) { vis++; at = i; }
        if (vis != 1) continue;
        vector<int> save = poly; poly.insert(poly.begin() + at + 1, z);
        grow(z); poly = save;
      }
    };
    grow(-1);
  }
  int largest1 = 0; for (int s = 0; s <= K; s++) if (cnt[s]) largest1 = s;
  printf("C1.convex_subsets_by_size"); for (int s = 3; s <= K; s++) printf(" %d:%ld", s, cnt[s]); printf("  largest=%d%s\n", largest1, cnt[K] ? "(>=K)" : "");
  for (auto& P : polys) if (!inConvexPosition4(P, chiS)) fail("C1_polygon_not_convex");
  // (C2) DP over the lowest vertex
  int largest2 = 0;
  for (int b = 0; b < n; b++) {
    vector<int> U; for (int i = 0; i < n; i++) if (Y[i] > Y[b] || (Y[i] == Y[b] && X[i] > X[b])) U.push_back(i);
    sort(U.begin(), U.end(), [&](int i, int j) { return o3(b, i, j) > 0; });
    for (size_t t = 1; t < U.size(); t++) if (o3(b, U[t - 1], U[t]) <= 0) fail("C2_angular_sort");
    largest2 = max(largest2, bestAnchored(b, U, chiS, -1));
  }
  printf("C2.dp_largest_convex_subset=%d\n", largest2);
  if (cnt[K] || largest1 != K - 1 || largest2 != K - 1) fail("largest_convex_subset_not_K-1");
  // (D) lines and cells
  vector<int> la, lb; LI.assign((size_t)n * n, -1);
  for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) { LI[a * n + b] = LI[b * n + a] = la.size(); la.push_back(a); lb.push_back(b); }
  L = la.size(); int W = (L + 63) / 64;
  long parallel = 0, V = 0, sumk1 = 0, edges = 0;
  unordered_set<string> cells; cells.reserve(4 * (size_t)L * L / 3 + 16); vector<const string*> order;  // first-seen order (locality)
  vector<i128> num(L), den(L); vector<int> dsg(L), rank_(L), constsg(L);
  string key((size_t)W * 8, '\0');
  for (int l = 0; l < L; l++) {
    int i = la[l], j = lb[l]; ll Dx = X[j] - X[i], Dy = Y[j] - Y[i];
    vector<int> cr;
    for (int m = 0; m < L; m++) {
      if (m == l) continue;
      ll Ex = X[lb[m]] - X[la[m]], Ey = Y[lb[m]] - Y[la[m]];
      i128 d = (i128)Ex * Dy - (i128)Ey * Dx;                                            // cross(E, D)
      i128 u = (i128)Ex * (Y[la[m]] - Y[i]) - (i128)Ey * (X[la[m]] - X[i]);             // cross(E, P_a - P_i)
      if (d == 0) { constsg[m] = sg(-u); rank_[m] = -1; if (l < m) parallel++; if (constsg[m] == 0) fail("line_coincidence"); continue; }
      // f_m(t) = orient(P_a, P_c, P_i + t D) = -u + t d = d (t - u/d)
      dsg[m] = sg(d); if (d < 0) { d = -d; u = -u; } num[m] = u; den[m] = d; cr.push_back(m);
    }
    sort(cr.begin(), cr.end(), [&](int p, int q) { return num[p] * den[q] < num[q] * den[p]; });
    // groups of equal t; verify strict increase between groups
    vector<int> gstart;
    for (size_t t = 0; t < cr.size(); t++) {
      if (t == 0 || num[cr[t - 1]] * den[cr[t]] != num[cr[t]] * den[cr[t - 1]]) {
        if (t > 0 && !(num[cr[t - 1]] * den[cr[t]] < num[cr[t]] * den[cr[t - 1]])) fail("crossing_sort");
        gstart.push_back(t);
      }
      rank_[cr[t]] = gstart.size() - 1;
    }
    int G = gstart.size(); gstart.push_back(cr.size());
    for (int g = 0; g < G; g++) {
      int mn = INT_MAX; for (int t = gstart[g]; t < gstart[g + 1]; t++) mn = min(mn, cr[t]);
      if (l < mn) { V++; sumk1 += gstart[g + 1] - gstart[g]; }  // k_v - 1 = number of other lines through v
    }
    // edges k = 0..G (edge k lies after group k-1 and before group k)
    for (int k = 0; k <= G; k++) {
      edges++;
      vector<uint64_t> w(W, 0);
      for (int m = 0; m < L; m++) {
        if (m == l) continue;
        int s = rank_[m] < 0 ? constsg[m] : dsg[m] * (rank_[m] < k ? 1 : -1);
        if (s > 0) w[m >> 6] |= 1ULL << (m & 63);
      }
      for (int side = 0; side < 2; side++) {
        if (side) w[l >> 6] |= 1ULL << (l & 63); else w[l >> 6] &= ~(1ULL << (l & 63));
        memcpy(&key[0], w.data(), (size_t)W * 8); auto ins = cells.insert(key); if (ins.second) order.push_back(&*ins.first);
      }
    }
  }
  long F = 1 + L + sumk1, C = cells.size();
  printf("D.lines=%d parallel_pairs=%ld vertices=%ld sum(k_v-1)=%ld F_euler=%ld edges=%ld distinct_cells=%ld V-E+F=%ld\n",
         L, parallel, V, sumk1, F, edges, C, V - edges + F);
  if (C != F) fail("cell_count_differs_from_euler");
  // (E) per cell
  long pass = 0, nfail = 0, bad = 0, dpconf = 0; size_t hint = 0;
  vector<uint64_t> bits(W); Chi chi{&bits};
  vector<int> witness(K);
  for (const string* sp : order) {
    memcpy(bits.data(), sp->data(), (size_t)W * 8);
    bool ok = false;
    for (size_t t = 0; t < polys.size() && !ok; t++) {
      size_t pi = (hint + t) % polys.size(); const vector<int>& P = polys[pi];
      int vis = 0, m = P.size();
      for (int e = 0; e < m && vis < 2; e++) if (chi.sq(P[e], P[(e + 1) % m]) < 0) vis++;
      if (vis != 1) continue;
      for (int e = 0; e < m; e++) witness[e] = P[e];
      witness[m] = n;
      if (!inConvexPosition4(witness, chi)) { bad++; continue; }  // never expected
      ok = true; hint = pi;
    }
    if (ok) { pass++; continue; }
    nfail++;
    // independent DP: any convex K-gon through q? (anchor q, every first vertex v1)
    int best = 0;
    for (int v1 = 0; v1 < n && best < K; v1++) {
      vector<int> c; c.push_back(v1);
      for (int x = 0; x < n; x++) if (x != v1 && chi(n, v1, x) > 0) c.push_back(x);
      sort(c.begin() + 1, c.end(), [&](int a, int b) { return chi(n, a, b) > 0; });
      for (size_t t = 1; t < c.size(); t++) if (chi(n, c[t - 1], c[t]) <= 0) fail("E_angular_sort");
      best = max(best, bestAnchored(n, c, chi, 0));
    }
    if (best >= K) bad++; else dpconf++;
    if (getenv("SATCHECK_ADJ")) {  // diagnostics only: points p whose closure meets this failing cell (signs agree off p's lines)
      printf("  failing cell %ld adjacent to points:", nfail);
      for (int p = 0; p < n; p++) { bool adj = true;
        for (int l = 0; l < L && adj; l++) { if (la[l] == p || lb[l] == p) continue; if (chi.sq(la[l], lb[l]) != o3(la[l], lb[l], p)) adj = false; }
        if (adj) printf(" %d", p); }
      printf("\n");
    }
  }
  printf("E.cells=%ld pass_verified_witness=%ld fail=%ld fail_dp_confirmed=%ld bad=%ld polygons=%zu\n", C, pass, nfail, dpconf, bad, polys.size());
  if (bad) fail("disagreement");
  if (nfail) { printf("VERDICT NOT_SATURATED fails=%ld cells=%ld\n", nfail, C); return 0; }
  printf("VERDICT SATURATED cells=%ld\n", C);
  return 0;
}
