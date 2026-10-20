/*
 * n2.c -- exact arrangement-face local search for 33 points with few convex 7-gons.
 *
 * Every move relocates (or re-inserts) points into faces of the line
 * arrangement of the other points; the number of convex 7-gons a point in a
 * face creates is computed exactly by satcount.c's slot count (arr_core.inc is
 * satcount.c's code, unchanged except that results are recorded in memory).
 * After every accepted move the heptagons of the new 33-point set are
 * re-enumerated from scratch (angular DFS) and compared with the prediction
 * H(S - moved) + sum of face counts; a mismatch is fatal.
 *
 * Methods:
 *   tabu   (a) best-face relocation of one point, tabu on recently moved
 *              points and on visited order-type fingerprints
 *   lns    (b) remove k = 3..6 points chosen by structure (heptagon vertices,
 *              near-heptagon participation), re-insert greedily or by beam
 *              search over faces, late-acceptance hill climbing
 *   pen    (c) as tabu, energy H + lambda(t) * NEAR with lambda annealed to 0
 *              at 75% of the budget
 * NEAR = #(convex hexagon Q, point p of S) with p strictly inside the
 * quadrilateral (c,a,b,d) of some 4 consecutive vertices of Q: a 7-subset
 * with 6 hull vertices whose inner point sits next to hull edge ab, so that
 * pushing p across ab would make a convex 7-gon.
 *
 * Order-type fingerprint (for tabu and for counting distinct states): for
 * each point i the sorted multiset of lambda(i,j) = #points left of i->j,
 * hashed, the per-point hashes sorted and hashed; min with the mirror image
 * (lambda -> n-2-lambda).  Equal order types give equal fingerprints, so the
 * number of distinct fingerprints is a lower bound on distinct order types.
 *
 * usage: n2 METHOD init.txt cpu_seconds seed outprefix
 *   writes outprefix.best.txt (best set), outprefix.traj (trajectory),
 *   outprefix.sol.txt (only if a set with 0 heptagons is found),
 *   prints one JSON line.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>

#include "arr_core.inc"

/* ---------------- rng ---------------- */
static u64 rs = 88172645463325252ULL;
static inline u64 rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline int rndi(int n) { return (int)(rnd() % (u64)n); }
static inline double rndu(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static double cpu(void) { return (double)clock() / CLOCKS_PER_SEC; }

/* ---------------- face reservoirs (two lowest m levels) ---------------- */
typedef struct { i128 X, Y, D; i64 dx, dy; int m; i64 px, py; } Rep;
#define RES 24
static Rep resv[2][RES];
static long long rc[2];
static long long minm;
static long long pt_fail = 0;
static void record_face(long long m, i128 X, i128 Y, i128 D, i64 dx, i64 dy) {
    /* only faces with an exactly verified integer point (|c| < 2^29) are kept;
       basesg holds the face's sign vector here (set by eval_direction) */
    if (m > minm + 1) return;
    i64 px, py;
    if (m < minm) {
        if (!find_point(X, Y, D, dx, dy, &px, &py)) { pt_fail++; return; }
        if (m == minm - 1) { memcpy(resv[1], resv[0], sizeof(resv[0])); rc[1] = rc[0]; }
        else rc[1] = 0;
        rc[0] = 0; minm = m;
        CAP = (int)(minm + 2);
        Rep r = {X, Y, D, dx, dy, (int)m, px, py};
        resv[0][0] = r; rc[0] = 1;
        return;
    }
    int lv = (int)(m - minm);
    long long c = rc[lv] + 1, slot = c <= RES ? c - 1 : (long long)(rnd() % (u64)c);
    if (slot >= RES) { rc[lv] = c; return; }
    if (!find_point(X, Y, D, dx, dy, &px, &py)) { pt_fail++; return; }
    rc[lv] = c;
    Rep r = {X, Y, D, dx, dy, (int)m, px, py};
    resv[lv][slot] = r;
}

/* integer point of the face represented by r (current setup) */
static int rep_point(const Rep *r, i64 *ox, i64 *oy) {
    vertex_base(r->X, r->Y, r->D);
    for (int z = 0; z < nzl; z++) {
        int l = zl[z];
        i64 e = LA[l] * r->dy + LB[l] * r->dx;
        basesg[l] = (signed char)sgn64(e);
    }
    return find_point(r->X, r->Y, r->D, r->dx, r->dy, ox, oy);
}

static int set_pts(int n, const i64 *x, const i64 *y) {
    N = n;
    for (int i = 0; i < n; i++) { PX[i] = x[i]; PY[i] = y[i]; }
    setup();
    return !gp_fail;
}

static long long nsweeps = 0, nincomplete = 0;
static double sweep_cpu = 0;
static int sweep_v3cap = 0;
static V3 *sweep_verts = NULL;
static Par *sweep_par = NULL;
static u64 htab_sz = 0;

/* sweep the arrangement of the current setup (N points), K = 7; fills reservoirs */
static int sweep(void) {
    double t0 = cpu();
    nsweeps++;
    K = 7;
    NH = 0;
    enum_polys();
    build_slots();
    ncache = 0;
    rc[0] = rc[1] = 0;
    minm = 1LL << 40;
    CAP = 1 << 30;
    long long Fmax = 1 + NL + (long long)NL * (NL - 1) / 2;
    u64 sz = 1; while (sz < (u64)(2 * Fmax)) sz <<= 1;
    if (sz > htab_sz) { free(htab); htab = calloc(2 * sz, sizeof(u64)); htab_sz = sz; if (!htab) die("alloc htab"); }
    else memset(htab, 0, 2 * sz * sizeof(u64));
    hmask = sz - 1;
    nfaces = 0;
    for (int s = 0; s < N; s++) {
        int nr = 0;
        for (int t = 0; t < N; t++) if (t != s) {
            RX[nr] = PX[t] - PX[s]; RY[nr] = PY[t] - PY[s]; nr++;
            RX[nr] = PX[s] - PX[t]; RY[nr] = PY[s] - PY[t]; nr++;
        }
        int idx[2 * MAXN];
        for (int i = 0; i < nr; i++) idx[i] = i;
        for (int i = 1; i < nr; i++) {
            int x = idx[i], j = i - 1;
            while (j >= 0 && ray_cmp(x, idx[j]) < 0) { idx[j + 1] = idx[j]; j--; }
            idx[j + 1] = x;
        }
        vertex_base(PX[s], PY[s], 1);
        if (nzl != N - 1) die("unexpected number of lines through S point");
        for (int i = 0; i < nr; i++) {
            int r1 = idx[i], r2 = idx[(i + 1) % nr];
            i64 dx = RX[r1] + RX[r2], dy = RY[r1] + RY[r2];
            i64 c1 = RX[r1] * dy - RY[r1] * dx, c2 = dx * RY[r2] - dy * RX[r2];
            if (c1 <= 0 || c2 <= 0) die("wedge direction not strictly inside");
            eval_direction(PX[s], PY[s], 1, dx, dy, "S", s, i);
        }
    }
    int need = NL * (NL - 1) / 2 + 1;
    if (need > sweep_v3cap) {
        free(sweep_verts); free(sweep_par);
        sweep_verts = malloc(sizeof(V3) * need); sweep_par = malloc(sizeof(Par) * NL);
        sweep_v3cap = need;
    }
    V3 *verts = sweep_verts; Par *par = sweep_par;
    long long nverts = 0;
    for (int l1 = 0; l1 < NL; l1++) {
        int a = la[l1], b = lb[l1];
        int np2 = 0;
        for (int l2 = l1 + 1; l2 < NL; l2++) {
            int c = la[l2], d = lb[l2];
            if (c == a || c == b || d == a || d == b) continue;
            i64 ux = PX[b] - PX[a], uy = PY[b] - PY[a];
            i64 wx = PX[d] - PX[c], wy = PY[d] - PY[c];
            i64 D = ux * wy - uy * wx;
            if (D == 0) continue;
            i64 T = (PX[c] - PX[a]) * wy - (PY[c] - PY[a]) * wx;
            if (D < 0) { D = -D; T = -T; }
            par[np2].T = T; par[np2].D = D; par[np2].l2 = l2; np2++;
        }
        qsort(par, np2, sizeof(Par), cmpPar);
        for (int k = 0; k < np2; k++) {
            int l2 = par[k].l2, c = la[l2], d = lb[l2];
            i64 ux = PX[b] - PX[a], uy = PY[b] - PY[a];
            i64 wx = PX[d] - PX[c], wy = PY[d] - PY[c];
            i128 D = par[k].D, T = par[k].T;
            i128 X = (i128)PX[a] * D + T * ux;
            i128 Y = (i128)PY[a] * D + T * uy;
            i128 g = gcd128(gcd128(X, Y), D);
            verts[nverts].x = X / g; verts[nverts].y = Y / g; verts[nverts].d = D / g; nverts++;
            vertex_base(X, Y, D);
            for (int sx = -1; sx <= 1; sx += 2)
                for (int sy = -1; sy <= 1; sy += 2)
                    eval_direction(X, Y, D, sx * ux + sy * wx, sx * uy + sy * wy, "V", l1, l2);
        }
    }
    qsort(verts, nverts, sizeof(V3), cmpV3);
    long long sum_m1 = (long long)N * (N - 2);
    for (long long i = 0; i < nverts;) {
        long long j = i;
        while (j < nverts && cmpV3(&verts[i], &verts[j]) == 0) j++;
        long long pairs = j - i, m = 2;
        while (m * (m - 1) / 2 < pairs) m++;
        if (m * (m - 1) / 2 != pairs) die("pair count not triangular");
        sum_m1 += m - 1;
        i = j;
    }
    long long Feuler = 1 + NL + sum_m1;
    free(SL); SL = NULL; free(grp_start); grp_start = NULL;
    sweep_cpu += cpu() - t0;
    if (Feuler != nfaces) { nincomplete++; return 0; }
    return 1;
}

/* ---------------- state ---------------- */
static int NPTS;
static i64 SX[MAXN], SY[MAXN];
static long long Hcur;
static int deg[MAXN];
static unsigned char *HV = NULL; static long long HVcap = 0;
static long long verify_mismatch = 0, gp_rejects = 0;

/* exact heptagon count of (n,x,y) by angular DFS; optional store + degrees */
static long long count_hept(int n, const i64 *x, const i64 *y, int store) {
    if (!set_pts(n, x, y)) return -1;
    K = 8; NH = 0;
    enum_polys();
    if (store) {
        if ((long long)NH * 7 > HVcap) { HVcap = (long long)NH * 7 * 2 + 64; HV = realloc(HV, HVcap); }
        memcpy(HV, HEX, (size_t)NH * 7);
        memset(deg, 0, sizeof(deg));
        for (long long h = 0; h < (long long)NH * 7; h++) deg[HV[h]]++;
    }
    return NH;
}
/* NEAR count (see header); part[p] = #near pairs containing p (as any of the 7) */
static long long near_count(int n, const i64 *x, const i64 *y, long long *part) {
    if (!set_pts(n, x, y)) return -1;
    K = 7; NH = 0;
    enum_polys();
    if (part) memset(part, 0, sizeof(long long) * MAXN);
    long long cnt = 0;
    for (int h = 0; h < NH; h++) {
        const unsigned char *P = HEX + (size_t)h * 6;
        unsigned long long in = 0;
        for (int i = 0; i < 6; i++) in |= 1ULL << P[i];
        for (int p = 0; p < n; p++) {
            if (in >> p & 1) continue;
            for (int i = 0; i < 6; i++) {
                int c = P[(i + 5) % 6], a = P[i], b = P[(i + 1) % 6], d = P[(i + 2) % 6];
                if (O3s[c][a][p] > 0 && O3s[a][b][p] > 0 && O3s[b][d][p] > 0 && O3s[d][c][p] > 0) {
                    cnt++;
                    if (part) { part[p]++; for (int t = 0; t < 6; t++) part[P[t]]++; }
                    break;
                }
            }
        }
    }
    return cnt;
}
/* order-type fingerprint (setup must be current) */
static int cmpu64(const void *A, const void *B) { u64 a = *(const u64 *)A, b = *(const u64 *)B; return a < b ? -1 : a > b; }
static int cmpint(const void *A, const void *B) { return *(const int *)A - *(const int *)B; }
static u64 fp_dir(int mirror) {
    u64 ph[MAXN];
    for (int i = 0; i < N; i++) {
        int lam[MAXN], c = 0;
        for (int j = 0; j < N; j++) if (j != i) {
            int l = 0;
            for (int k = 0; k < N; k++) if (k != i && k != j && O3s[i][j][k] > 0) l++;
            lam[c++] = mirror ? N - 2 - l : l;
        }
        qsort(lam, c, sizeof(int), cmpint);
        u64 h = 0x9E3779B97F4A7C15ULL;
        for (int t = 0; t < c; t++) h = mix64(h ^ (u64)(lam[t] + 1) * 0x100000001B3ULL);
        ph[i] = h;
    }
    qsort(ph, N, sizeof(u64), cmpu64);
    u64 h = 0x243F6A8885A308D3ULL;
    for (int i = 0; i < N; i++) h = mix64(h + ph[i]);
    return h;
}
static u64 fingerprint(int n, const i64 *x, const i64 *y) {
    set_pts(n, x, y);
    u64 a = fp_dir(0), b = fp_dir(1);
    u64 r = a < b ? a : b;
    return r ? r : 1;
}
#define VBITS 22
static u64 *vis; static long long nvis = 0;
static int vis_has(u64 f) { u64 p = mix64(f) & ((1ULL << VBITS) - 1); while (vis[p]) { if (vis[p] == f) return 1; p = (p + 1) & ((1ULL << VBITS) - 1); } return 0; }
static void vis_add(u64 f) {
    if (nvis > (1LL << (VBITS - 1))) return;
    u64 p = mix64(f) & ((1ULL << VBITS) - 1);
    while (vis[p]) { if (vis[p] == f) return; p = (p + 1) & ((1ULL << VBITS) - 1); }
    vis[p] = f; nvis++;
}

/* ---------------- bookkeeping ---------------- */
static const char *outp;
static long long bestH = 1LL << 60;
static double t_le1 = -1, t_zero = -1, t_start;
static FILE *traj;
static void write_set(const char *suffix, int n, const i64 *x, const i64 *y) {
    char fn[1024]; snprintf(fn, sizeof fn, "%s.%s", outp, suffix);
    FILE *f = fopen(fn, "w");
    for (int i = 0; i < n; i++) fprintf(f, "%lld %lld\n", x[i], y[i]);
    fclose(f);
}
static void note_state(long long step) {
    double t = cpu() - t_start;
    if (Hcur < bestH) {
        bestH = Hcur;
        fprintf(traj, "%.2f %lld %lld best\n", t, step, Hcur); fflush(traj);
        write_set("best.txt", NPTS, SX, SY);
    }
    if (Hcur <= 1 && t_le1 < 0) t_le1 = t;
    if (Hcur == 0 && t_zero < 0) { t_zero = t; write_set("sol.txt", NPTS, SX, SY); }
}

/* ---------------- (a)/(c): relocation candidates ---------------- */
typedef struct { int i; i64 x, y; long long H; double E, r; } Cand;
static int cmpCand(const void *A, const void *B) {
    const Cand *a = A, *b = B;
    if (a->E != b->E) return a->E < b->E ? -1 : 1;
    return a->r < b->r ? -1 : a->r > b->r;
}
/* candidates from removing point i of S: up to t0 faces at the lowest m, t1 at the next */
static int gather(int i, Cand *out, int t0, int t1) {
    i64 tx[MAXN], ty[MAXN]; int n = 0;
    for (int j = 0; j < NPTS; j++) if (j != i) { tx[n] = SX[j]; ty[n] = SY[j]; n++; }
    set_pts(n, tx, ty);
    sweep();
    int nc = 0;
    for (int lv = 0; lv < 2; lv++) {
        int have = (int)(rc[lv] < RES ? rc[lv] : RES), take = lv ? t1 : t0, got = 0;
        int ord[RES]; for (int t = 0; t < have; t++) ord[t] = t;
        for (int t = have - 1; t > 0; t--) { int u = rndi(t + 1); int z = ord[t]; ord[t] = ord[u]; ord[u] = z; }
        for (int t = 0; t < have && got < take; t++) {
            i64 px = resv[lv][ord[t]].px, py = resv[lv][ord[t]].py;
            out[nc].i = i; out[nc].x = px; out[nc].y = py;
            out[nc].H = Hcur - deg[i] + resv[lv][ord[t]].m;
            out[nc].E = (double)out[nc].H; out[nc].r = rndu();
            nc++; got++;
        }
    }
    return nc;
}
static int tabu_until[MAXN];

static void run_tabu(double budget, int pen, long long *steps_out) {
    long long step = 0;
    double lam0 = 0;
    if (pen) { long long n0 = near_count(NPTS, SX, SY, NULL); lam0 = n0 > 0 ? 10.0 / n0 : 0; }
    static Cand cands[4096];
    while (cpu() - t_start < budget && Hcur > 0) {
        step++;
        double t = cpu() - t_start;
        double lam = pen ? lam0 * fmax(0.0, 1.0 - t / (0.75 * budget)) : 0;
        /* candidate points: up to 3 heptagon vertices (weighted by degree), 1 other */
        int C[8], nC = 0, used[MAXN] = {0};
        long long totdeg = 0;
        for (int j = 0; j < NPTS; j++) if (tabu_until[j] < step) totdeg += deg[j];
        for (int rep = 0; rep < 3 && totdeg > 0; rep++) {
            long long r = (long long)(rnd() % (u64)totdeg), acc = 0;
            for (int j = 0; j < NPTS; j++) {
                if (tabu_until[j] >= step || used[j]) continue;
                acc += deg[j];
                if (r < acc) { used[j] = 1; C[nC++] = j; totdeg -= deg[j]; break; }
            }
        }
        for (int tries = 0; tries < 100 && nC < 4; tries++) {
            int j = rndi(NPTS);
            if (!used[j] && tabu_until[j] < step) { used[j] = 1; C[nC++] = j; }
        }
        int nc = 0;
        for (int c = 0; c < nC; c++) nc += gather(C[c], cands + nc, 12, 4);
        if (nc == 0) continue;
        if (pen && lam > 0) {
            qsort(cands, nc, sizeof(Cand), cmpCand);
            int lim = nc < 8 ? nc : 8;
            for (int c = 0; c < nc; c++) {
                if (c >= lim) { cands[c].E = 1e18; continue; }
                i64 tx[MAXN], ty[MAXN];
                memcpy(tx, SX, sizeof(i64) * NPTS); memcpy(ty, SY, sizeof(i64) * NPTS);
                tx[cands[c].i] = cands[c].x; ty[cands[c].i] = cands[c].y;
                cands[c].E = cands[c].H + lam * near_count(NPTS, tx, ty, NULL);
            }
        }
        qsort(cands, nc, sizeof(Cand), cmpCand);
        int pick = -1; u64 pf = 0;
        for (int c = 0; c < nc; c++) {
            if (cands[c].E >= 1e17) break;
            i64 tx[MAXN], ty[MAXN];
            memcpy(tx, SX, sizeof(i64) * NPTS); memcpy(ty, SY, sizeof(i64) * NPTS);
            tx[cands[c].i] = cands[c].x; ty[cands[c].i] = cands[c].y;
            u64 f = fingerprint(NPTS, tx, ty);
            if (gp_fail) { gp_rejects++; continue; }
            if (vis_has(f) && cands[c].H >= bestH) continue;
            pick = c; pf = f; break;
        }
        if (pick < 0) pick = 0;
        Cand *m = &cands[pick];
        i64 ox = SX[m->i], oy = SY[m->i];
        SX[m->i] = m->x; SY[m->i] = m->y;
        long long h = count_hept(NPTS, SX, SY, 1);
        if (h < 0) { SX[m->i] = ox; SY[m->i] = oy; count_hept(NPTS, SX, SY, 1); gp_rejects++; continue; }
        if (h != m->H) { verify_mismatch++; fprintf(stderr, "MISMATCH predicted %lld got %lld\n", m->H, h); }
        Hcur = h;
        if (!pf) pf = fingerprint(NPTS, SX, SY);
        vis_add(pf);
        tabu_until[m->i] = step + 3;
        note_state(step);
        if (step % 10 == 0) { fprintf(traj, "%.2f %lld %lld cur\n", cpu() - t_start, step, Hcur); fflush(traj); }
    }
    *steps_out = step;
}

/* ---------------- (b): large-neighbourhood search with LAHC ---------------- */
typedef struct { int n; i64 x[MAXN], y[MAXN]; long long H; double r; } St;
static int cmpSt(const void *A, const void *B) {
    const St *a = A, *b = B;
    if (a->H != b->H) return a->H < b->H ? -1 : 1;
    return a->r < b->r ? -1 : a->r > b->r;
}
static long long lns_k_hist[8], lns_k_acc[8];
static void run_lns(double budget, long long *steps_out) {
    long long it = 0;
    enum { L = 20 };
    long long hist[L];
    for (int v = 0; v < L; v++) hist[v] = Hcur;
    long long part[MAXN];
    near_count(NPTS, SX, SY, part);
    static St beam[16], kids[64];
    while (cpu() - t_start < budget && Hcur > 0) {
        it++;
        int k = 3 + rndi(4);
        int rem[MAXN] = {0}, nr = 0;
        if (Hcur > 0) {
            long long hsel = (long long)(rnd() % (u64)Hcur);
            const unsigned char *P = HV + hsel * 7;
            int r = 1 + rndi(k < 3 ? k : 3);
            int ord[7] = {0, 1, 2, 3, 4, 5, 6};
            for (int t = 6; t > 0; t--) { int u = rndi(t + 1); int z = ord[t]; ord[t] = ord[u]; ord[u] = z; }
            for (int t = 0; t < r; t++) { rem[P[ord[t]]] = 1; nr++; }
        }
        while (nr < k) {
            long long tot = 0;
            for (int j = 0; j < NPTS; j++) if (!rem[j]) tot += part[j] + 1;
            long long r = (long long)(rnd() % (u64)tot), acc = 0;
            for (int j = 0; j < NPTS; j++) {
                if (rem[j]) continue;
                acc += part[j] + 1;
                if (r < acc) { rem[j] = 1; nr++; break; }
            }
        }
        St *s0 = &beam[0]; s0->n = 0;
        for (int j = 0; j < NPTS; j++) if (!rem[j]) { s0->x[s0->n] = SX[j]; s0->y[s0->n] = SY[j]; s0->n++; }
        s0->H = count_hept(s0->n, s0->x, s0->y, 0);
        int B = rndu() < 0.3 ? 3 : 1, br = B == 1 ? 1 : 3, nb = 1;
        for (int lev = 0; lev < k && nb > 0; lev++) {
            int nk = 0;
            for (int b = 0; b < nb; b++) {
                set_pts(beam[b].n, beam[b].x, beam[b].y);
                sweep();
                int got = 0;
                for (int lv = 0; lv < 2 && got < br; lv++) {
                    int have = (int)(rc[lv] < RES ? rc[lv] : RES);
                    int ord[RES]; for (int t = 0; t < have; t++) ord[t] = t;
                    for (int t = have - 1; t > 0; t--) { int u = rndi(t + 1); int z = ord[t]; ord[t] = ord[u]; ord[u] = z; }
                    for (int t = 0; t < have && got < br; t++) {
                        i64 px = resv[lv][ord[t]].px, py = resv[lv][ord[t]].py;
                        St *c = &kids[nk++];
                        *c = beam[b];
                        c->x[c->n] = px; c->y[c->n] = py; c->n++;
                        c->H = beam[b].H + resv[lv][ord[t]].m; c->r = rndu();
                        got++;
                    }
                }
            }
            qsort(kids, nk, sizeof(St), cmpSt);
            nb = nk < B ? nk : B;
            for (int b = 0; b < nb; b++) beam[b] = kids[b];
        }
        if (nb == 0 || beam[0].n != NPTS) continue;
        St *best = &beam[0];
        long long h = count_hept(best->n, best->x, best->y, 0);
        if (h < 0) { gp_rejects++; continue; }
        if (h != best->H) { verify_mismatch++; fprintf(stderr, "MISMATCH predicted %lld got %lld\n", best->H, h); }
        u64 f = fingerprint(best->n, best->x, best->y);
        int v = (int)(it % L);
        lns_k_hist[k]++;
        if (h <= hist[v] || h <= Hcur) {
            lns_k_acc[k]++;
            memcpy(SX, best->x, sizeof(i64) * NPTS); memcpy(SY, best->y, sizeof(i64) * NPTS);
            Hcur = count_hept(NPTS, SX, SY, 1);
            vis_add(f);
            near_count(NPTS, SX, SY, part);
            note_state(it);
        }
        hist[v] = Hcur;
        if (it % 10 == 0) { fprintf(traj, "%.2f %lld %lld cur\n", cpu() - t_start, it, Hcur); fflush(traj); }
    }
    *steps_out = it;
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage: n2 tabu|lns|pen init.txt cpu_seconds seed outprefix\n"); return 1; }
    const char *meth = argv[1];
    double budget = atof(argv[3]);
    rs ^= mix64((u64)atoll(argv[4]) + 12345);
    if (!rs) rs = 1;
    outp = argv[5];
    FILE *f = fopen(argv[2], "r");
    if (!f) die("cannot open init");
    NPTS = 0;
    while (NPTS < MAXN && fscanf(f, "%lld %lld", &SX[NPTS], &SY[NPTS]) == 2) NPTS++;
    fclose(f);
    {   /* exact rescale to max |c| ~ 2^28 (same order type) */
        i64 mx = 1;
        for (int i = 0; i < NPTS; i++) { i64 a = llabs(SX[i]), b = llabs(SY[i]); if (a > mx) mx = a; if (b > mx) mx = b; }
        i64 f = (1LL << 28) / mx;
        if (f >= 2) for (int i = 0; i < NPTS; i++) { SX[i] *= f; SY[i] *= f; }
    }
    vis = calloc(1ULL << VBITS, sizeof(u64));
    char fn[1024]; snprintf(fn, sizeof fn, "%s.traj", outp);
    traj = fopen(fn, "w");
    t_start = cpu();
    Hcur = count_hept(NPTS, SX, SY, 1);
    if (Hcur < 0) die("initial set not in general position");
    long long H0 = Hcur;
    long long near0 = near_count(NPTS, SX, SY, NULL);
    vis_add(fingerprint(NPTS, SX, SY));
    note_state(0);
    long long steps = 0;
    if (!strcmp(meth, "calib")) {
        for (int i = 0; i < NPTS; i++) {
            i64 tx[MAXN], ty[MAXN]; int n = 0;
            for (int j = 0; j < NPTS; j++) if (j != i) { tx[n] = SX[j]; ty[n] = SY[j]; n++; }
            set_pts(n, tx, ty);
            int ok = sweep();
            long long h32 = count_hept(n, tx, ty, 0);
            printf("del %d deg %d H(S-i) %lld complete %d faces %lld minm %lld count_min %lld count_min+1 %lld\n",
                   i, deg[i], h32, ok, nfaces, minm, rc[0], rc[1]);
        }
        return 0;
    }
    if (!strcmp(meth, "tabu")) run_tabu(budget, 0, &steps);
    else if (!strcmp(meth, "pen")) run_tabu(budget, 1, &steps);
    else if (!strcmp(meth, "lns")) run_lns(budget, &steps);
    else die("unknown method");
    long long nearf = near_count(NPTS, SX, SY, NULL);
    printf("{\"method\": \"%s\", \"init\": \"%s\", \"seed\": %s, \"budget\": %.0f, \"cpu\": %.1f, \"n\": %d, "
           "\"H0\": %lld, \"near0\": %lld, \"steps\": %lld, \"sweeps\": %lld, \"sweep_cpu\": %.1f, "
           "\"incomplete_sweeps\": %lld, \"best_H\": %lld, \"final_H\": %lld, \"final_near\": %lld, "
           "\"t_le1\": %.2f, \"t_zero\": %.2f, \"distinct_fp\": %lld, \"verify_mismatch\": %lld, "
           "\"gp_rejects\": %lld, \"face_point_fail\": %lld",
           meth, argv[2], argv[4], budget, cpu() - t_start, NPTS, H0, near0, steps, nsweeps, sweep_cpu,
           nincomplete, bestH, Hcur, nearf, t_le1, t_zero, nvis, verify_mismatch, gp_rejects, pt_fail);
    if (!strcmp(meth, "lns")) {
        printf(", \"lns_k_tried\": [");
        for (int k = 3; k <= 6; k++) printf("%s%lld", k > 3 ? ", " : "", lns_k_hist[k]);
        printf("], \"lns_k_accepted\": [");
        for (int k = 3; k <= 6; k++) printf("%s%lld", k > 3 ? ", " : "", lns_k_acc[k]);
        printf("]");
    }
    printf("}\n");
    fclose(traj);
    return 0;
}
