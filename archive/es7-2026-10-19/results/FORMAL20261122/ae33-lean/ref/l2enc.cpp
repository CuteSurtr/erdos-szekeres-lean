// l2enc.cpp -- joint two-point (radius-1) extension encoder (track L, 16 Nov 2026).  Built on L1's l1enc.cpp
// (orientation table, convex enumeration, R2, AC, OCT copied unchanged in substance); new: the second point, the W
// variables, the joint Grassmann-Pluecker / Radon families and the joint k-gon family.  Soundness: E72_SOUNDNESS.md.
//
// Input: base B, n points, exact integers, no three collinear.  Unknown: two new points p (index n), q (index n+1).
// Variables (true = positive orientation):
//   X(a,b) = [orient(a,b,p) > 0]  a<b in B: 1 .. N2              (N2 = n(n-1)/2, l1enc numbering)
//   Y(a,b) = [orient(a,b,q) > 0]  a<b in B: N2+1 .. 2 N2
//   W(a)   = [orient(a,p,q) > 0]  a in B:   2 N2 + 1 .. 2 N2 + n
// Families (each clause holds for every real p, q with B' + p + q in general position, B' any realization of B's
// labelled order type; OCT/JK only when B' + p + q has no convex k-gon):
//   R2X, R2Y  l1enc's rotation clauses at every a in B, for p and for q
//   ACX, ACY  l1enc's acyclicity clauses (4-point Radon condition on {a,b,c,p} and {a,b,c,q})
//   RAD       Radon condition on {a,b,p,q}: the coefficients ([b p q], -[a p q], [a b q], -[a b p]) are not all of one sign
//   GPA       3-term Grassmann-Pluecker relations with pivot a in B on {a,x,y,p,q}
//   GPP, GPQ  3-term GP relations with pivot p (resp. q) on {x,y,z,p,q}
//   OCTX, OCTY  l1enc's OCT (convex (k-1)-gons of B, k-gon through one new point)
//   JK        for every convex (k-2)-gon Q of B, every slot of p in Q (Q1 = Q + p convex, slot lemma) and every edge f
//             of Q1: NOT(p sees exactly that edge of Q  AND  q sees f and neither neighbour of f in Q1)
//   JKQ (option --jkq): the same with the roles of p and q exchanged
// Usage: l2enc B.txt k out.cnf [--jkq] [--no-k] [--allow-kgon]      prints one JSON stats line
//        l2enc B.txt k - --eval px py qx qy [--jkq]    evaluate all clauses at real p, q (exact) and print violations per family
//        l2enc --selftest
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <vector>
#include <string>
#include <algorithm>
#include <random>
#include <set>
#include <unordered_set>
#include <functional>
using namespace std;
typedef __int128 i128;
typedef long long ll;

struct P { ll x, y; };
static int n;
static vector<P> pts;
static vector<int8_t> O;
static int N2, NV;

static int orient3(const P& a, const P& b, const P& c) {
    i128 v = ((i128)b.x - a.x) * ((i128)c.y - a.y) - ((i128)b.y - a.y) * ((i128)c.x - a.x);
    return (v > 0) - (v < 0);
}
static inline int o(int a, int b, int c) { return O[((size_t)a * n + b) * n + c]; }
static inline int var(int a, int b) { return a * n - a * (a + 1) / 2 + (b - a - 1) + 1; }  // a < b
static void die(const char* m) { fprintf(stderr, "l2enc: %s\n", m); exit(1); }

static void build_table() {
    O.assign((size_t)n * n * n, 0);
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) for (int c = 0; c < n; c++)
        if (a != b && b != c && a != c) {
            int s = orient3(pts[a], pts[b], pts[c]);
            if (s == 0) die("three collinear points (or a repeated point)");
            O[((size_t)a * n + b) * n + c] = (int8_t)s;
        }
}

// chi(i,j,k) over elements 0..n+1 (n = p, n+1 = q): returns CP (const +), -CP (const -), or a signed literal +-v meaning
// "orient(i,j,k) > 0  iff  literal true".
static const int CP = 1 << 29;  // constant marker (never a variable number)
static int chi(int i, int j, int k) {
    int a[3] = {i, j, k}, s = 1;
    for (int x = 0; x < 3; x++) for (int y = 0; y < 2 - x; y++) if (a[y] > a[y + 1]) { swap(a[y], a[y + 1]); s = -s; }
    if (a[0] == a[1] || a[1] == a[2]) die("chi: repeated element");
    if (a[2] < n) return CP * s * o(a[0], a[1], a[2]);
    if (a[1] < n) {  // (a,b,new)
        int v = var(a[0], a[1]) + (a[2] == n ? 0 : N2);
        return s * v;
    }
    if (a[0] < n && a[1] == n && a[2] == n + 1) return s * (2 * N2 + 1 + a[0]);
    die("chi: bad triple"); return 0;
}

// ---- convex polygon enumeration (l1enc's), plus a list of the (k-2)-gons ----
static vector<ll> cnt;
static int kmax, kq, kj;
static vector<uint64_t> chainbits;
static int chain[64 + 2];
static vector<int> cand;
static vector<vector<int>> polys;  // convex kj-gons, ccw

static void mark_chains(int m) {
    for (int i = 0; i < m; i++) {
        int a = chain[(i + m - 1) % m], b = chain[i], c = chain[(i + 1) % m], d = chain[(i + 2) % m];
        size_t key = (((size_t)a * n + b) * n + c) * n + d;
        chainbits[key >> 6] |= 1ULL << (key & 63);
    }
}
static void dfs(int depth, int lastidx) {
    int v = chain[0], w = chain[depth - 1], u = chain[depth - 2];
    for (int t = lastidx + 1; t < (int)cand.size(); t++) {
        int x = cand[t];
        if (depth >= 2 && o(u, w, x) <= 0) continue;
        if (o(w, x, v) <= 0) continue;
        chain[depth] = x;
        int m = depth + 1;
        cnt[m]++;
        if (m == kq) mark_chains(m);
        if (m == kj) polys.push_back(vector<int>(chain, chain + m));
        if (m < kmax) dfs(depth + 1, t);
    }
}
static void enumerate_convex() {
    cnt.assign(kmax + 1, 0);
    polys.clear();
    for (int v = 0; v < n; v++) {
        cand.clear();
        for (int x = 0; x < n; x++)
            if (x != v && (pts[x].y > pts[v].y || (pts[x].y == pts[v].y && pts[x].x > pts[v].x))) cand.push_back(x);
        sort(cand.begin(), cand.end(), [&](int p1, int p2) { return o(v, p1, p2) > 0; });
        chain[0] = v;
        for (int t = 0; t < (int)cand.size(); t++) { chain[1] = cand[t]; if (kmax >= 3) dfs(2, t); }
    }
}

// ---- clause store, by family ----
enum Fam { R2X, R2Y, ACX, ACY, RAD, GPA, GPP, GPQ, OCTX, OCTY, JK, JKQ, NFAM };
static const char* famname[NFAM] = {"r2x", "r2y", "acx", "acy", "rad", "gpa", "gpp", "gpq", "octx", "octy", "jk", "jkq"};
static vector<int> lits;
static vector<int> famof;  // family per clause
static vector<ll> famcnt(NFAM, 0);
static void addc(const vector<int>& c, int fam) {
    for (int l : c) lits.push_back(l);
    lits.push_back(0); famof.push_back(fam); famcnt[fam]++;
}

// R2 for new point "which" (0 = p, 1 = q): l1enc's emit_R2 with the variable offset
static void emit_R2(int which) {
    int off = which ? N2 : 0;
    for (int a = 0; a < n; a++) {
        struct E { int x, eps; ll ux, uy; };
        vector<E> e;
        for (int x = 0; x < n; x++) {
            if (x == a) continue;
            ll dx = pts[x].x - pts[a].x, dy = pts[x].y - pts[a].y;
            int eps = (dy > 0 || (dy == 0 && dx > 0)) ? 1 : -1;
            e.push_back({x, eps, eps * dx, eps * dy});
        }
        auto cr = [](const E& p, const E& q) { i128 v = (i128)p.ux * q.uy - (i128)p.uy * q.ux; return (v > 0) - (v < 0); };
        sort(e.begin(), e.end(), [&](const E& p, const E& q) { return cr(p, q) > 0; });
        int m = e.size();
        vector<int> S(m);
        for (int i = 0; i < m; i++) {
            int x = e[i].x, lp = a < x ? var(a, x) + off : -(var(x, a) + off);  // "orient(a,x,new) > 0"
            S[i] = e[i].eps > 0 ? lp : -lp;
        }
        for (int i = 0; i + 2 < m; i++)
            for (int k = i + 2; k < m; k++) {
                if (cr(e[i], e[i + 1]) <= 0 || cr(e[i + 1], e[k]) <= 0 || cr(e[i], e[k]) <= 0) die("R2 cone check failed");
                addc({-S[i], S[i + 1], -S[k]}, which ? R2Y : R2X);
                addc({S[i], -S[i + 1], S[k]}, which ? R2Y : R2X);
            }
    }
}
static void emit_AC(int which) {
    int nw = n + which;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) {
        int s = o(a, b, c);
        // p on the side of the third vertex for at least one edge: literal "s*orient(x,y,new) > 0"
        int l1 = chi(a, b, nw), l2 = chi(b, c, nw), l3 = chi(c, a, nw);
        addc({s > 0 ? l1 : -l1, s > 0 ? l2 : -l2, s > 0 ? l3 : -l3}, which ? ACY : ACX);
    }
}

// generic: forbid every assignment of the unknowns in the given sign terms for which pred(values) is true.
// terms: list of chi-values (const +-2 or signed literal); pred gets the +-1 values in order.
template <class F> static vector<vector<int>> forbid_terms(const vector<int>& t, F pred) {
    vector<vector<int>> out;
    vector<int> vars;
    for (int x : t) if (x != CP && x != -CP) { int v = abs(x); if (find(vars.begin(), vars.end(), v) == vars.end()) vars.push_back(v); }
    int m = vars.size();
    auto values = [&](int mask) {
        vector<int> val(t.size());
        for (size_t r = 0; r < t.size(); r++) {
            int x = t[r];
            if (x == CP) val[r] = 1; else if (x == -CP) val[r] = -1;
            else { int idx = find(vars.begin(), vars.end(), abs(x)) - vars.begin(); val[r] = ((x > 0) == (((mask >> idx) & 1) == 1)) ? 1 : -1; }
        }
        return val;
    };
    for (int mask = 0; mask < (1 << m); mask++) {
        if (!pred(values(mask))) continue;
        // shorten: drop a variable if the clause stays implied (every completion of the kept part is forbidden)
        vector<int> keep(m, 1);
        for (int d = 0; d < m; d++) {
            keep[d] = 0;
            vector<int> fidx; for (int e2 = 0; e2 < m; e2++) if (!keep[e2]) fidx.push_back(e2);
            bool allbad = true;
            for (int fm = 0; fm < (1 << fidx.size()) && allbad; fm++) {
                int mm = mask;
                for (size_t r = 0; r < fidx.size(); r++) { if ((fm >> r) & 1) mm |= 1 << fidx[r]; else mm &= ~(1 << fidx[r]); }
                if (!pred(values(mm))) allbad = false;
            }
            if (!allbad) keep[d] = 1;
        }
        vector<int> c;
        for (int d = 0; d < m; d++) if (keep[d]) c.push_back(((mask >> d) & 1) ? -vars[d] : vars[d]);
        sort(c.begin(), c.end());
        if (c.empty()) die("forbid_terms: constant violation (base not in general position?)");
        out.push_back(c);
    }
    return out;
}

static unordered_set<string> seen;  // dedupe for the GP, RAD and JK families
static void addc_d(const vector<int>& c, int fam) {
    string key((const char*)c.data(), c.size() * sizeof(int)); key += (char)fam;
    if (seen.insert(key).second) addc(c, fam);
}
static void emit_gp(int e, int f, int g, int h, int i, int fam) {
    // [efg][ehi] - [efh][egi] + [efi][egh] = 0: the three terms (T1, -T2, T3) are never all of one sign
    vector<int> t = {chi(e, f, g), chi(e, h, i), chi(e, f, h), chi(e, g, i), chi(e, f, i), chi(e, g, h)};
    for (auto& c : forbid_terms(t, [](const vector<int>& v) { int T1 = v[0] * v[1], T2 = -v[2] * v[3], T3 = v[4] * v[5]; return T1 == T2 && T2 == T3; }))
        addc_d(c, fam);
}
static void emit_RAD() {
    int p = n, q = n + 1;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) {
        vector<int> t = {chi(b, p, q), chi(a, p, q), chi(a, b, q), chi(a, b, p)};
        for (auto& c : forbid_terms(t, [](const vector<int>& v) { return v[0] == -v[1] && -v[1] == v[2] && v[2] == -v[3]; })) addc_d(c, RAD);
    }
}
static void emit_GP() {
    int p = n, q = n + 1;
    for (int a = 0; a < n; a++) for (int x = 0; x < n; x++) for (int y = x + 1; y < n; y++) {
        if (x == a || y == a) continue;
        emit_gp(a, x, y, p, q, GPA);
    }
    for (int x = 0; x < n; x++) for (int y = x + 1; y < n; y++) for (int z = y + 1; z < n; z++) {
        emit_gp(p, x, y, z, q, GPP);
        emit_gp(q, x, y, z, p, GPQ);
    }
}
static void emit_OCT(int which) {
    int nw = n + which;
    size_t N4 = (size_t)n * n * n * n;
    for (size_t key = 0; key < N4; key++) {
        if (!(chainbits[key >> 6] >> (key & 63) & 1)) continue;
        int d = key % n, cc = (key / n) % n, b = (key / n / n) % n, a = key / n / n / n;
        // forbid: sees(b,c) & !sees(a,b) & !sees(c,d), sees(x,y) <=> orient(x,y,new) < 0
        addc({chi(b, cc, nw), -chi(a, b, nw), -chi(cc, d, nw)}, which ? OCTY : OCTX);
    }
}
// joint k-gon family: first new point f1 into a slot of Q, then second new point f2 onto an edge of Q1
static void emit_JK(int f1, int f2, int fam) {
    for (auto& Q : polys) {
        int m = Q.size();
        for (int i = 0; i < m; i++) {
            int qa = Q[(i + m - 1) % m], qb = Q[i], qc = Q[(i + 1) % m], qd = Q[(i + 2) % m];
            // f1 sees (qb,qc), not (qa,qb), not (qc,qd).  "sees(x,y)" literal = -chi(x,y,f)
            vector<int> c1 = {-chi(qb, qc, f1), chi(qa, qb, f1), chi(qc, qd, f1)};  // conjunction literals
            vector<int> Q1;
            for (int r = 0; r <= i; r++) Q1.push_back(Q[r]);
            Q1.push_back(f1);
            for (int r = i + 1; r < m; r++) Q1.push_back(Q[r]);
            int m1 = Q1.size();
            for (int j = 0; j < m1; j++) {
                int u = Q1[(j + m1 - 1) % m1], v = Q1[j], w = Q1[(j + 1) % m1], z = Q1[(j + 2) % m1];
                vector<int> conj = c1;
                conj.push_back(-chi(v, w, f2)); conj.push_back(chi(u, v, f2)); conj.push_back(chi(w, z, f2));
                // clause = OR of negations; constants: a false conjunct makes the clause trivially true
                vector<int> c; bool taut = false;
                for (int l : conj) {
                    if (l == CP) continue;          // conjunct always true: drop
                    if (l == -CP) { taut = true; break; }  // conjunct always false: clause satisfied
                    c.push_back(-l);
                }
                if (taut) continue;
                sort(c.begin(), c.end()); c.erase(unique(c.begin(), c.end()), c.end());
                bool tt = false;
                for (size_t r = 0; r + 1 < c.size(); r++) if (c[r] == -c[r + 1]) tt = true;
                for (size_t r = 0; r < c.size(); r++) for (size_t s2 = 0; s2 < c.size(); s2++) if (c[r] == -c[s2]) tt = true;
                if (tt) continue;
                if (c.empty()) die("empty JK clause (the base has a convex k-gon?)");
                addc_d(c, fam);
            }
        }
    }
}

static void build(int k, bool jkq, bool nok) {
    N2 = n * (n - 1) / 2; NV = 2 * N2 + n;
    build_table();
    kmax = k; kq = k - 1; kj = k - 2;
    chainbits.assign(((size_t)n * n * n * n >> 6) + 1, 0);
    enumerate_convex();
    lits.clear(); famof.clear(); famcnt.assign(NFAM, 0); seen.clear();
    emit_R2(0); emit_R2(1); emit_AC(0); emit_AC(1); emit_RAD(); emit_GP();
    if (!nok) { emit_OCT(0); emit_OCT(1); emit_JK(n, n + 1, JK); if (jkq) emit_JK(n + 1, n, JKQ); }
}

// exact evaluation at real p, q (coordinates as i128-safe 61-bit integers)
static vector<int> realassign(P p, P q) {
    vector<int> val(NV + 1, 0);
    vector<P> all = pts; all.push_back(p); all.push_back(q);
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) {
        int s1 = orient3(all[a], all[b], p), s2 = orient3(all[a], all[b], q);
        if (!s1 || !s2) return {};
        val[var(a, b)] = s1 > 0; val[N2 + var(a, b)] = s2 > 0;
    }
    for (int a = 0; a < n; a++) { int s = orient3(all[a], p, q); if (!s) return {}; val[2 * N2 + 1 + a] = s > 0; }
    return val;
}
static vector<ll> eval_viol(const vector<int>& val) {
    vector<ll> v(NFAM, 0);
    size_t s = 0, ci = 0;
    while (s < lits.size()) {
        bool sat = false;
        while (lits[s] != 0) { int l = lits[s]; if ((l > 0) == (val[abs(l)] == 1)) sat = true; s++; }
        if (!sat) v[famof[ci]]++;
        s++; ci++;
    }
    return v;
}
// brute force: is there a convex k-gon in B+p+q containing p (resp. q, both)?  returns bitmask 1: through p only,
// 2: through q only, 4: through both
static int kgon_through(P p, P q, int k) {
    vector<P> all = pts; all.push_back(p); all.push_back(q);
    int N = all.size();
    vector<int8_t> OO((size_t)N * N * N);
    for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) for (int c = 0; c < N; c++)
        if (a != b && b != c && a != c) OO[((size_t)a * N + b) * N + c] = orient3(all[a], all[b], all[c]);
    auto oo = [&](int a, int b, int c) { return OO[((size_t)a * N + b) * N + c]; };
    auto conv4 = [&](int a, int b, int c, int d) {
        int qq[4] = {a, b, c, d};
        for (int i = 0; i < 4; i++) {
            int x = qq[i], u = qq[(i + 1) % 4], v = qq[(i + 2) % 4], w = qq[(i + 3) % 4];
            int s = oo(u, v, w);
            if (oo(u, v, x) == s && oo(v, w, x) == s && oo(w, u, x) == s) return false;
        }
        return true;
    };
    int res = 0;
    vector<int> cur;
    // DFS over convex subsets that contain at least one new point; record which new points
    function<void(int)> rec = [&](int last) {
        if ((int)cur.size() == k) {
            bool hp = find(cur.begin(), cur.end(), n) != cur.end(), hq = find(cur.begin(), cur.end(), n + 1) != cur.end();
            if (hp && hq) res |= 4; else if (hp) res |= 1; else if (hq) res |= 2;
            return;
        }
        for (int x = last + 1; x < N; x++) {
            bool ok = true;
            int m = cur.size();
            for (int i = 0; i < m && ok; i++) for (int j = i + 1; j < m && ok; j++) for (int l = j + 1; l < m && ok; l++)
                if (!conv4(cur[i], cur[j], cur[l], x)) ok = false;
            if (!ok) continue;
            cur.push_back(x); rec(x); cur.pop_back();
        }
    };
    rec(-1);
    return res;
}

static int selftest() {
    mt19937_64 rng(2026);
    long cases = 0, withk = 0, both = 0;
    for (int trial = 0; trial < 400; trial++) {
        int k = 5 + trial % 2;  // k = 5 or 6
        n = k == 5 ? 6 + trial % 3 : 6 + trial % 5;  // pentagon-free needs n <= 8 (ES(5) = 9)
        ll R = 200 + 100 * (trial % 3);
        for (;;) {
            pts.assign(n, {0, 0});
            for (auto& z : pts) { z.x = (ll)(rng() % (2 * R + 1)) - R; z.y = (ll)(rng() % (2 * R + 1)) - R; }
            bool ok = true;
            for (int a = 0; a < n && ok; a++) for (int b = a + 1; b < n && ok; b++) for (int c = b + 1; c < n && ok; c++)
                if (orient3(pts[a], pts[b], pts[c]) == 0) ok = false;
            if (!ok) continue;
            N2 = n * (n - 1) / 2; build_table(); kmax = k; kq = k - 1; kj = k - 2;
            chainbits.assign(((size_t)n * n * n * n >> 6) + 1, 0); enumerate_convex();
            if (cnt[k] == 0) break;  // base must be k-gon-free
        }
        build(k, true, false);
        for (int s = 0; s < 40; s++) {
            P p = {(ll)(rng() % (6 * R + 1)) - 3 * R, (ll)(rng() % (6 * R + 1)) - 3 * R};
            P q = {(ll)(rng() % (6 * R + 1)) - 3 * R, (ll)(rng() % (6 * R + 1)) - 3 * R};
            vector<P> all = pts; all.push_back(p); all.push_back(q);
            bool gp = true;
            for (int a = 0; a < n + 2 && gp; a++) for (int b = a + 1; b < n + 2 && gp; b++) for (int c = b + 1; c < n + 2 && gp; c++)
                if (orient3(all[a], all[b], all[c]) == 0) gp = false;
            if (!gp) continue;
            vector<int> val = realassign(p, q);
            vector<ll> v = eval_viol(val);
            int kg = kgon_through(p, q, k);
            cases++; if (kg) withk++; if (kg & 4) both++;
            // consistency families never violated
            for (int f : {R2X, R2Y, ACX, ACY, RAD, GPA, GPP, GPQ})
                if (v[f]) {
                    printf("selftest FAIL: family %s violated by a real configuration (trial %d)\n", famname[f], trial);
                    size_t s2 = 0, ci = 0;
                    while (s2 < lits.size()) { bool sat = false; size_t st = s2; while (lits[s2] != 0) { int l = lits[s2]; if ((l > 0) == (val[abs(l)] == 1)) sat = true; s2++; }
                        if (!sat && famof[ci] == f) { printf("clause:"); for (size_t r = st; r < s2; r++) printf(" %d", lits[r]); printf("\n"); break; } s2++; ci++; }
                    printf("n=%d N2=%d\n", n, N2); return 1; }
            bool bp = kg & 1, bq = kg & 2, bb = kg & 4;
            // OCTX violated <=> k-gon through p avoiding q?  OCTX detects k-gons through p with k-1 base points.
            if ((v[OCTX] > 0) != bp) { printf("selftest FAIL octx trial %d kg=%d v=%lld\n", trial, kg, v[OCTX]); return 1; }
            if ((v[OCTY] > 0) != bq) { printf("selftest FAIL octy trial %d kg=%d v=%lld\n", trial, kg, v[OCTY]); return 1; }
            if ((v[JK] > 0) != bb) { printf("selftest FAIL jk trial %d kg=%d v=%lld\n", trial, kg, v[JK]); return 1; }
            if ((v[JKQ] > 0) != bb) { printf("selftest FAIL jkq trial %d kg=%d v=%lld\n", trial, kg, v[JKQ]); return 1; }
        }
    }
    printf("selftest OK: %ld real (p,q) configurations on 400 random k-gon-free bases (k = 5, 6; n = 6..10); "
           "%ld with a k-gon through a new point, %ld through both; consistency families never violated; "
           "OCTX/OCTY/JK/JKQ violated exactly when the brute force finds such a k-gon\n", cases, withk, both);
    return 0;
}

int main(int argc, char** argv) {
    if (argc >= 2 && !strcmp(argv[1], "--selftest")) return selftest();
    if (argc < 4) die("usage: l2enc B.txt k out.cnf [--jkq] [--no-k] [--allow-kgon] | l2enc B.txt k - --eval px py qx qy [--jkq]");
    int k = atoi(argv[2]);
    if (k < 5 || k > 12) die("k out of range");
    bool jkq = false, nok = false, allowk = false, ev = false;
    P ep = {0, 0}, eq = {0, 0};
    for (int i = 4; i < argc; i++) {
        if (!strcmp(argv[i], "--jkq")) jkq = true;
        else if (!strcmp(argv[i], "--no-k")) nok = true;
        else if (!strcmp(argv[i], "--allow-kgon")) allowk = true;
        else if (!strcmp(argv[i], "--eval") && i + 4 < argc) {
            ev = true; ep = {atoll(argv[i + 1]), atoll(argv[i + 2])}; eq = {atoll(argv[i + 3]), atoll(argv[i + 4])}; i += 4;
        } else die("unknown option");
    }
    FILE* f = fopen(argv[1], "r");
    if (!f) die("cannot open points");
    ll x, y;
    while (fscanf(f, "%lld %lld", &x, &y) == 2) {
        if (llabs(x) >= (1LL << 61) || llabs(y) >= (1LL << 61)) die("coordinate too large");
        pts.push_back({x, y});
    }
    fclose(f);
    n = pts.size();
    if (n < 4 || n > 64) die("need 4..64 points");
    build(k, jkq, nok);
    if (cnt[k] > 0 && !allowk) die("base contains a convex k-gon");
    if (ev) {
        vector<int> val = realassign(ep, eq);
        if (val.empty()) die("eval: p, q not in general position with B (an orientation is 0)");
        vector<P> all = pts; all.push_back(ep); all.push_back(eq);
        for (int a = 0; a < n + 2; a++) for (int b = a + 1; b < n + 2; b++) for (int c = b + 1; c < n + 2; c++)
            if (orient3(all[a], all[b], all[c]) == 0) die("eval: not in general position");
        vector<ll> v = eval_viol(val);
        int kg = kgon_through(ep, eq, k);
        printf("{\"eval\":true,\"kgon_through_p_only\":%d,\"kgon_through_q_only\":%d,\"kgon_through_both\":%d", kg & 1 ? 1 : 0, kg & 2 ? 1 : 0, kg & 4 ? 1 : 0);
        for (int fm = 0; fm < NFAM; fm++) printf(",\"viol_%s\":%lld", famname[fm], v[fm]);
        printf("}\n");
        return 0;
    }
    ll ncl = famof.size();
    FILE* g = fopen(argv[3], "w");
    if (!g) die("cannot open output");
    fprintf(g, "p cnf %d %lld\n", NV, ncl);
    string buf; buf.reserve(1 << 20); char tmp[24];
    for (size_t i = 0; i < lits.size(); i++) {
        if (lits[i] == 0) buf += "0\n"; else { snprintf(tmp, sizeof tmp, "%d ", lits[i]); buf += tmp; }
        if (buf.size() > (1 << 20)) { fwrite(buf.data(), 1, buf.size(), g); buf.clear(); }
    }
    fwrite(buf.data(), 1, buf.size(), g);
    if (fclose(g) != 0) die("write failed");
    printf("{\"points\":\"%s\",\"n\":%d,\"k\":%d,\"vars\":%d,\"clauses\":%lld", argv[1], n, k, NV, ncl);
    for (int fm = 0; fm < NFAM; fm++) printf(",\"%s\":%lld", famname[fm], famcnt[fm]);
    for (int m = 3; m <= k; m++) printf(",\"convex%d\":%lld", m, cnt[m]);
    printf("}\n");
    return 0;
}
