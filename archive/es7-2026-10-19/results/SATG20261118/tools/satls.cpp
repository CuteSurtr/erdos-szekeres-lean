// satls.cpp (track SAT2, 18 Nov 2026): FINDER ONLY. Local search for small K-gon-saturated sets.
// Objective = number of open cells of the arrangement of all lines through 2 points of S whose sample q is NOT a
// vertex of a convex K-gon of S+q (long double samples: heuristic). Exact proof of any hit: vx1118 satcells + check_cells.py.
// One sample per cell: every cell bounded below (w.r.t. a generic "up" u) has a unique lowest vertex v and lies in one of
// the k_v-1 upper sectors at v; the L+1 cells unbounded below are sampled on a far line. So #samples = Euler count.
// Usage: satls eval  pts K                     -> prints valid, cells, fails
//        satls scan  pts K                     -> fails of S minus each point
//        satls search pts K outdir seed secs [drop] [T]  -> local search (descends after each hit)
#include <bits/stdc++.h>
using namespace std;
typedef long long ll; typedef long double ld;

int K, n; vector<ll> X, Y; vector<signed char> O3;
const ld UX = 0.31907671, UY = 0.94772957;  // generic up direction (unit up to rounding)
mt19937_64 rng(1);

static inline ll orient(int a, int b, int c) { return (X[b]-X[a])*(Y[c]-Y[a]) - (Y[b]-Y[a])*(X[c]-X[a]); }
static inline int o3(int a, int b, int c) { return O3[((size_t)a*n+b)*n+c]; }

struct Ev { bool valid = false; long cells = 0, fails = 0; vector<pair<ld,ld>> fq; };

vector<array<int,4>> caps;  // {a,b,p,r}: q fits between a=t_i and b=t_{i+1} iff orient(a,b,q)<0, orient(p,a,q)>0, orient(b,r,q)>0
typedef bitset<128> BS;
bool kfree;
vector<int> chainv;
void dfs(int p0, const vector<int>& cand, int start) {
  int m = chainv.size();
  if (m == K) { kfree = false; return; }
  if (m == K - 1) {  // convex (K-1)-gon t[0..m-1], CCW
    for (int i = 0; i < m; i++) {
      int tm = chainv[(i+m-1)%m], ti = chainv[i], t1 = chainv[(i+1)%m], t2 = chainv[(i+2)%m];
      caps.push_back({ti, t1, tm, t2});
    }
  }
  for (int idx = start; idx < (int)cand.size() && kfree; idx++) {
    int b = cand[idx];
    if (m >= 2 && (o3(chainv[m-2], chainv[m-1], b) <= 0 || o3(chainv[m-1], b, p0) <= 0)) continue;
    chainv.push_back(b); dfs(p0, cand, idx + 1); chainv.pop_back();
  }
}

size_t ncaps; double tdfs;
Ev evaluate(bool wantfail, bool cellsToo = true) {
  Ev e; n = X.size(); auto t0 = chrono::steady_clock::now();
  O3.assign((size_t)n*n*n, 0);
  for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) for (int c = 0; c < n; c++) {
    ll v = orient(a, b, c); O3[((size_t)a*n+b)*n+c] = (v > 0) - (v < 0);
    if (a < b && b < c && v == 0) return e;  // not in general position
  }
  caps.clear(); kfree = true;
  for (int p0 = 0; p0 < n && kfree; p0++) {
    vector<int> cand;
    for (int j = 0; j < n; j++) if (Y[j] > Y[p0] || (Y[j] == Y[p0] && X[j] > X[p0])) cand.push_back(j);
    sort(cand.begin(), cand.end(), [&](int a, int b) { return o3(p0, a, b) > 0; });
    chainv.assign(1, p0); dfs(p0, cand, 0);
  }
  if (!kfree) return e;
  e.valid = true; ncaps = caps.size(); tdfs = chrono::duration<double>(chrono::steady_clock::now() - t0).count();
  if (!cellsToo) return e;
  // lines a<b; g_l(p) = orient(a,b,p), gradient . w = cross(D_l, w)
  vector<int> la, lb; for (int a = 0; a < n; a++) for (int b = a+1; b < n; b++) { la.push_back(a); lb.push_back(b); }
  int L = la.size();
  vector<ll> DX(L), DY(L); for (int l = 0; l < L; l++) { DX[l] = X[lb[l]]-X[la[l]]; DY[l] = Y[lb[l]]-Y[la[l]]; }
  if (n > 128) { fprintf(stderr, "n > 128\n"); exit(2); }
  vector<BS> Pm((size_t)n*n), Rm((size_t)n*n*n);  // Pm[ab] = predecessors p; Rm[ab*n+p] = successors r
  for (auto& c : caps) { size_t ab = (size_t)c[0]*n + c[1]; Pm[ab].set(c[2]); Rm[ab*n + c[2]].set(c[3]); }
  vector<int> edges; for (int ab = 0; ab < n*n; ab++) if (Pm[ab].any()) edges.push_back(ab);
  vector<signed char> s((size_t)n*n), sg(L); vector<BS> lft(n), rgt(n);  // lft[a] = {p: orient(p,a,q)>0}, rgt[b] = {r: orient(b,r,q)>0}
  auto setS = [&](int l, int g) {
    int a = la[l], b = lb[l]; sg[l] = g; s[a*n+b] = g; s[b*n+a] = -g;
    rgt[a].reset(b); lft[b].reset(a); rgt[b].reset(a); lft[a].reset(b);
    if (g > 0) { rgt[a].set(b); lft[b].set(a); } else if (g < 0) { rgt[b].set(a); lft[a].set(b); }
  };
  size_t hint = 0;
  auto covered = [&]() {
    size_t C = edges.size();
    for (size_t t = 0; t < C; t++) {
      size_t c = hint + t; if (c >= C) c -= C;
      int ab = edges[c], a = ab / n, b = ab % n;
      if (s[ab] >= 0) continue;
      BS m = Pm[ab] & lft[a];
      for (size_t p = m._Find_first(); p < 128; p = m._Find_next(p))
        if ((Rm[(size_t)ab*n + p] & rgt[b]).any()) { hint = c; return true; }
    }
    return false;
  };
  vector<array<ld,4>> fv;  // failing cells: vertex + sector direction (sample made later)
  auto fail = [&](ld vx, ld vy, ld wx, ld wy) {
    e.fails++;
    if (wantfail) { if (fv.size() < 2000) fv.push_back({vx, vy, wx, wy}); else { size_t r = rng() % e.fails; if (r < 2000) fv[r] = {vx, vy, wx, wy}; } }
  };
  auto sgn = [](__int128 v) { return (int)((v > 0) - (v < 0)); };
  auto up = [](ll dx, ll dy) { return dy > 0 || (dy == 0 && dx > 0); };  // u = (eps, 1)
  // bounded-below cells: each has a unique lowest vertex v and lies in one of its k_v - 1 upper sectors
  struct EvT { __int128 num, den; int l; };
  vector<EvT> ev; vector<signed char> before(L);
  for (int l1 = 0; l1 < L; l1++) {
    int a = la[l1];
    ev.clear();
    for (int l = 0; l < L; l++) {
      if (l == l1) continue;
      __int128 den = (__int128)DX[l1]*DY[l] - (__int128)DY[l1]*DX[l];
      if (den == 0) { setS(l, sgn((__int128)DX[l]*(Y[a]-Y[la[l]]) - (__int128)DY[l]*(X[a]-X[la[l]]))); continue; }
      __int128 num = (__int128)(X[la[l]]-X[a])*DY[l] - (__int128)(Y[la[l]]-Y[a])*DX[l];
      if (den < 0) { den = -den; num = -num; }
      ev.push_back({num, den, l});
      setS(l, -sgn((__int128)DX[l]*DY[l1] - (__int128)DY[l]*DX[l1]));  // sign at t -> -infinity along l1
    }
    sort(ev.begin(), ev.end(), [](const EvT& p, const EvT& q) { return p.num*q.den < q.num*p.den; });
    for (size_t i = 0; i < ev.size(); ) {
      size_t j = i; while (j < ev.size() && ev[j].num*ev[i].den == ev[i].num*ev[j].den) j++;
      int mn = l1; for (size_t k = i; k < j; k++) { mn = min(mn, ev[k].l); before[ev[k].l] = sg[ev[k].l]; }
      if (mn == l1) {
        vector<pair<ll,ll>> d; vector<int> ls;
        ls.push_back(l1); for (size_t k = i; k < j; k++) ls.push_back(ev[k].l);
        for (int l : ls) { ll dx = DX[l], dy = DY[l]; if (!up(dx, dy)) { dx = -dx; dy = -dy; } d.push_back({dx, dy}); }
        sort(d.begin(), d.end(), [](const pair<ll,ll>& p, const pair<ll,ll>& q) { return (__int128)p.first*q.second - (__int128)p.second*q.first > 0; });
        ld t = (ld)ev[i].num / (ld)ev[i].den, vx = X[a] + t*DX[l1], vy = Y[a] + t*DY[l1];
        for (size_t k = 0; k + 1 < d.size(); k++) {
          ll wx = d[k].first + d[k+1].first, wy = d[k].second + d[k+1].second;
          for (int l : ls) setS(l, sgn((__int128)DX[l]*wy - (__int128)DY[l]*wx));
          e.cells++;
          if (!covered()) fail(vx, vy, wx, wy);
        }
      }
      for (size_t k = i; k < j; k++) setS(ev[k].l, -before[ev[k].l]);
      i = j;
    }
  }
  // L+1 cells unbounded below (numeric far line, u tilted by 2^-30 so that "up" agrees with (eps, 1))
  {
    const ld th = ldexpl(1.0L, -30), UX = sinl(th), UY = cosl(th), PX = UY, PY = -UX;
    ld hmin = 1e300L;
    for (int l1 = 0; l1 < L; l1++) for (int l2 = l1+1; l2 < L; l2++) {
      __int128 den = (__int128)DX[l1]*DY[l2] - (__int128)DY[l1]*DX[l2]; if (den == 0) continue;
      __int128 num = (__int128)(X[la[l2]]-X[la[l1]])*DY[l2] - (__int128)(Y[la[l2]]-Y[la[l1]])*DX[l2];
      ld t = (ld)num / (ld)den; hmin = min(hmin, (X[la[l1]] + t*DX[l1])*UX + (Y[la[l1]] + t*DY[l1])*UY);
    }
    ld H0 = hmin - 1 - fabsl(hmin);
    vector<ld> ss;
    for (int l = 0; l < L; l++) {
      ld g0 = DX[l]*(H0*UY - Y[la[l]]) - DY[l]*(H0*UX - X[la[l]]), g1 = DX[l]*PY - DY[l]*PX;
      ss.push_back(-g0 / g1);
    }
    sort(ss.begin(), ss.end());
    auto farq = [&](ld sp) {
      ld qx = H0*UX + sp*PX, qy = H0*UY + sp*PY;
      for (int l = 0; l < L; l++) { ld v = DX[l]*(qy - Y[la[l]]) - DY[l]*(qx - X[la[l]]); setS(l, (v > 0) - (v < 0)); }
      e.cells++; if (!covered()) { e.fails++; if (wantfail && fv.size() < 2000) fv.push_back({qx, qy, 0, 0}); }
    };
    farq(ss[0] - 1); for (int i = 0; i + 1 < L; i++) farq((ss[i] + ss[i+1]) / 2); farq(ss[L-1] + 1);
  }
  // sample points for the kept failing cells: half way to the first other line along the sector direction
  for (auto& f : fv) {
    if (f[2] == 0 && f[3] == 0) { e.fq.push_back({f[0], f[1]}); continue; }
    ld tmin = 1e300L;
    for (int l = 0; l < L; l++) {
      ld gv = DX[l]*(f[1] - Y[la[l]]) - DY[l]*(f[0] - X[la[l]]), gw = DX[l]*f[3] - DY[l]*f[2];
      if (fabsl(gv) < 1e-9L * (fabsl(DX[l]) + fabsl(DY[l]))) continue;  // a line through the vertex
      if (gw != 0) { ld t = -gv / gw; if (t > 0 && t < tmin) tmin = t; }
    }
    if (tmin > 1e200L) tmin = 2;
    e.fq.push_back({f[0] + tmin/2*f[2], f[1] + tmin/2*f[3]});
  }
  return e;
}

bool readPts(const char* f) {
  ifstream in(f); if (!in) return false; X.clear(); Y.clear(); string line;
  while (getline(in, line)) { if (line.empty() || line[0] == '#') continue; istringstream ss(line); ll x, y; if (ss >> x >> y) { X.push_back(x); Y.push_back(y); } }
  n = X.size(); return true;
}
void writePts(const string& f) { ofstream o(f); for (size_t i = 0; i < X.size(); i++) o << X[i] << " " << Y[i] << "\n"; }
void dropPt(int p) { X.erase(X.begin()+p); Y.erase(Y.begin()+p); n = X.size(); }

vector<pair<long,int>> scanDel() {  // (fails, index) over deletions, valid only
  vector<ll> X0 = X, Y0 = Y; vector<pair<long,int>> r;
  for (int p = 0; p < (int)X0.size(); p++) { X = X0; Y = Y0; dropPt(p); Ev e = evaluate(false); if (e.valid) r.push_back({e.fails, p}); }
  X = X0; Y = Y0; n = X.size(); sort(r.begin(), r.end()); return r;
}

int main(int argc, char** argv) {
  if (argc < 4) { fprintf(stderr, "usage: satls eval|scan|search pts K [outdir seed secs drop T]\n"); return 2; }
  string mode = argv[1]; K = atoi(argv[3]);
  if (!readPts(argv[2])) { fprintf(stderr, "cannot read\n"); return 2; }
  auto T0 = chrono::steady_clock::now();
  auto secs = [&]() { return chrono::duration<double>(chrono::steady_clock::now() - T0).count(); };
  if (mode == "fails") { Ev e = evaluate(true); printf("fails=%ld\n", e.fails); for (auto& q : e.fq) printf("%.3Lf %.3Lf\n", q.first, q.second); return 0; }
  if (mode == "eval") { Ev e = evaluate(false); printf("n=%d K=%d valid=%d cells=%ld fails=%ld caps=%zu dfs=%.2fs [%.2fs]\n", n, K, e.valid, e.cells, e.fails, ncaps, tdfs, secs()); return 0; }
  if (mode == "scan") { auto r = scanDel(); for (auto& x : r) printf("drop %d fails %ld\n", x.second, x.first); printf("[%.2fs]\n", secs()); return 0; }
  string out = argv[4]; rng.seed(atoll(argv[5])); double lim = atof(argv[6]);
  int drop = argc > 7 ? atoi(argv[7]) : -2; double T = argc > 8 ? atof(argv[8]) : 0.7;
  FILE* lg = fopen((out + "/log.jsonl").c_str(), "a");
  auto LOG = [&](const char* fmt, auto... a) { fprintf(lg, fmt, a...); fprintf(lg, "\n"); fflush(lg); };
  auto descend = [&](int forced) {
    int p = forced;
    if (p < 0) { auto r = scanDel(); if (r.empty()) return false; size_t k = 0; while (k + 1 < r.size() && r[k+1].first == r[0].first) k++;
      p = r[uniform_int_distribution<size_t>(0, k)(rng)].second; LOG("{\"t\":%.0f,\"scan_best\":%ld,\"n\":%d}", secs(), r[0].first, n); }
    dropPt(p); LOG("{\"t\":%.0f,\"drop\":%d,\"n\":%d}", secs(), p, n); return true;
  };
  if (mode == "multigrow") {  // repeat: random seed of 2(K-1) points in [-R,R]^2, greedy growth to saturation; keep small ones
    long R = 20000, runs = 0; int bestN = 100000; int m0 = argc > 7 ? atoi(argv[7]) : 2*(K-1);
    uniform_int_distribution<long> UC(-R, R);
    while (secs() < lim) {
      X.clear(); Y.clear(); n = 0;
      while ((int)X.size() < m0) { X.push_back(UC(rng)); Y.push_back(UC(rng)); n = X.size(); if (!evaluate(false, false).valid) { X.pop_back(); Y.pop_back(); n = X.size(); } }
      bool ok = true;
      while (ok && secs() < lim) {
        Ev e = evaluate(true); if (e.fails == 0) break;
        if ((int)X.size() >= bestN + 6) { ok = false; break; }
        shuffle(e.fq.begin(), e.fq.end(), rng);
        long bf = LONG_MAX; ll bx = 0, by = 0; int tried = 0;
        for (auto& q : e.fq) { if (tried >= 8) break; X.push_back(llround(q.first)); Y.push_back(llround(q.second)); n = X.size();
          if (evaluate(false, false).valid) { tried++; long f = evaluate(false).fails; if (f < bf) { bf = f; bx = X.back(); by = Y.back(); } }
          X.pop_back(); Y.pop_back(); n = X.size(); }
        if (!tried) { bool big = false; for (auto& x : X) { x *= 4; big |= llabs(x) >= (1LL<<23); } for (auto& y : Y) { y *= 4; big |= llabs(y) >= (1LL<<23); } if (big) ok = false; continue; }
        X.push_back(bx); Y.push_back(by); n = X.size();
      }
      runs++;
      if (!ok || secs() >= lim) continue;
      LOG("{\"t\":%.0f,\"run\":%ld,\"saturated_n\":%d}", secs(), runs, n);
      if (n <= bestN) { bestN = n; string f = out + "/found_n" + to_string(n) + "_" + to_string((long)secs()) + ".txt"; writePts(f); LOG("{\"t\":%.0f,\"FOUND\":\"%s\",\"n\":%d}", secs(), f.c_str(), n); }
    }
    return 0;
  }
  if (mode == "grow") {  // add points into failing cells (best of up to 8 valid candidates) until saturated
    drop = -1;
    while (secs() < lim) {
      Ev e = evaluate(true); if (!e.valid) { LOG("{\"error\":\"invalid grow state\"}"); return 1; }
      LOG("{\"t\":%.0f,\"grow_n\":%d,\"fails\":%ld,\"cells\":%ld}", secs(), n, e.fails, e.cells);
      if (e.fails == 0) break;
      shuffle(e.fq.begin(), e.fq.end(), rng);
      long bestf = LONG_MAX; ll bx = 0, by = 0; int tried = 0;
      for (auto& q : e.fq) {
        if (tried >= 8) break;
        ll qx = llround(q.first), qy = llround(q.second);
        X.push_back(qx); Y.push_back(qy);
        Ev v = evaluate(false, false);
        if (v.valid) { tried++; Ev w = evaluate(false); if (w.fails < bestf) { bestf = w.fails; bx = qx; by = qy; } }
        X.pop_back(); Y.pop_back(); n = X.size();
      }
      if (!tried) { for (auto& x : X) x *= 4; for (auto& y : Y) y *= 4; LOG("{\"t\":%.0f,\"scaled\":4}", secs()); continue; }
      X.push_back(bx); Y.push_back(by); n = X.size();
      writePts(out + "/grow_state.txt");
    }
  }
  if (drop != -1) descend(drop >= 0 ? drop : -1);
  Ev cur = evaluate(true); if (!cur.valid) { LOG("{\"error\":\"invalid start\"}"); return 1; }
  vector<ll> bX = X, bY = Y; long best = cur.fails; long iter = 0, lastImp = 0;
  LOG("{\"t\":%.0f,\"start_fails\":%ld,\"cells\":%ld,\"n\":%d}", secs(), cur.fails, cur.cells, n);
  normal_distribution<double> N01; uniform_real_distribution<double> U01;
  while (secs() < lim) {
    if (cur.fails == 0) {
      string f = out + "/found_n" + to_string(n) + "_" + to_string((long)secs()) + ".txt"; writePts(f);
      LOG("{\"t\":%.0f,\"FOUND\":\"%s\",\"n\":%d,\"cells\":%ld}", secs(), f.c_str(), n, cur.cells);
      if (!descend(-1)) break;
      cur = evaluate(true); bX = X; bY = Y; best = cur.fails; lastImp = iter;
      LOG("{\"t\":%.0f,\"start_fails\":%ld,\"cells\":%ld,\"n\":%d}", secs(), cur.fails, cur.cells, n);
      continue;
    }
    iter++;
    ll mnx = *min_element(X.begin(), X.end()), mxx = *max_element(X.begin(), X.end());
    ll mny = *min_element(Y.begin(), Y.end()), mxy = *max_element(Y.begin(), Y.end());
    double diam = max(mxx - mnx, mxy - mny);
    int i;
    if (U01(rng) < 0.5 && !cur.fq.empty()) {  // a point near a random failing sample
      auto q = cur.fq[uniform_int_distribution<size_t>(0, cur.fq.size()-1)(rng)];
      vector<pair<ld,int>> dd; for (int j = 0; j < n; j++) dd.push_back({(X[j]-q.first)*(X[j]-q.first) + (Y[j]-q.second)*(Y[j]-q.second), j});
      sort(dd.begin(), dd.end()); i = dd[uniform_int_distribution<int>(0, min(n, 8) - 1)(rng)].second;
    } else i = uniform_int_distribution<int>(0, n-1)(rng);
    double sc = diam * pow(10.0, -(0.5 + 3.0*U01(rng)));
    ll dx = llround(N01(rng)*sc), dy = llround(N01(rng)*sc);
    if (!dx && !dy) continue;
    ll ox = X[i], oy = Y[i]; X[i] += dx; Y[i] += dy;
    if (llabs(X[i]) >= (1LL<<24) || llabs(Y[i]) >= (1LL<<24)) { X[i] = ox; Y[i] = oy; continue; }
    Ev e = evaluate(true);
    long dl = e.valid ? e.fails - cur.fails : 1;
    if (e.valid && (dl <= 0 || U01(rng) < exp(-dl / T))) cur = e; else { X[i] = ox; Y[i] = oy; }
    if (cur.fails < best) { best = cur.fails; bX = X; bY = Y; lastImp = iter; writePts(out + "/best_n" + to_string(n) + ".txt");
      LOG("{\"t\":%.0f,\"iter\":%ld,\"best\":%ld,\"n\":%d}", secs(), iter, best, n); }
    if (iter - lastImp > 1500) {
      lastImp = iter;
      if (U01(rng) < 0.5 || cur.fq.empty()) { X = bX; Y = bY; cur = evaluate(true); LOG("{\"t\":%.0f,\"iter\":%ld,\"reset_to\":%ld}", secs(), iter, cur.fails); }
      else {  // kick: add the best of up to 8 valid points in failing cells, then delete the best other point
        vector<pair<ld,ld>> fq = cur.fq; shuffle(fq.begin(), fq.end(), rng);
        long bf = LONG_MAX; ll bx = 0, by = 0; int tried = 0;
        for (auto& q : fq) { if (tried >= 8) break; X.push_back(llround(q.first)); Y.push_back(llround(q.second));
          if (evaluate(false, false).valid) { tried++; long f = evaluate(false).fails; if (f < bf) { bf = f; bx = X.back(); by = Y.back(); } }
          X.pop_back(); Y.pop_back(); n = X.size(); }
        if (tried) {
          X.push_back(bx); Y.push_back(by); n = X.size();
          vector<ll> X0 = X, Y0 = Y; long bd = LONG_MAX; int bp = -1;
          for (int p = 0; p + 1 < (int)X0.size(); p++) { X = X0; Y = Y0; dropPt(p); Ev e2 = evaluate(false); if (e2.valid && e2.fails > 0 && e2.fails < bd) { bd = e2.fails; bp = p; }
            else if (e2.valid && e2.fails == 0) { bd = 0; bp = p; break; } }
          X = X0; Y = Y0; dropPt(bp >= 0 ? bp : (int)X0.size() - 1); cur = evaluate(true);
          LOG("{\"t\":%.0f,\"iter\":%ld,\"kick_add_fails\":%ld,\"kick_drop\":%d,\"now\":%ld}", secs(), iter, bf, bp, cur.fails);
          if (cur.fails < best) { best = cur.fails; bX = X; bY = Y; writePts(out + "/best_n" + to_string(n) + ".txt"); }
        }
      }
    }
    if (iter % 200 == 0) LOG("{\"t\":%.0f,\"iter\":%ld,\"cur\":%ld,\"best\":%ld,\"n\":%d}", secs(), iter, cur.fails, best, n);
  }
  LOG("{\"t\":%.0f,\"end\":1,\"best\":%ld,\"n\":%d}", secs(), best, n);
  return 0;
}
