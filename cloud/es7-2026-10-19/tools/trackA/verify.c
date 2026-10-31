/*
 * Independent verifier for the saturation result of sat.c.
 *
 * Different face enumeration: every face F has an edge e on its boundary,
 * lying on a line l, and e has an endpoint vertex v (every line meets some
 * other line).  For every line l, every distinct vertex v on l, both
 * directions +-u along l and both normals +-n, the symbolic point
 *     p = v + delta * (+-u) + delta^2 * (+-n),   delta -> 0+
 * is tested; sign orient(c,d,p) is the first nonzero of
 *     orient(c,d,v),  cross(d-c, +-u),  cross(d-c, +-n).
 * These points are always valid (off every line).
 *
 * Different K-gon test: a certificate list of (K-1)-subsets Q of S (produced
 * by sat.c, but re-validated here: distinct, in convex position by the
 * "no point in a triangle" criterion, re-sorted counter-clockwise).  For a
 * convex polygon Q and a point p in general position, Q + {p} is in convex
 * position iff exactly one edge of Q is visible from p (p strictly right of
 * the directed edge).
 *
 * Different face count: F = E - V + 1 with E = sum over lines of
 * (#distinct vertices on the line + 1) and V = sum over lines and vertices
 * on the line of 1/m_v (m_v = number of lines through v), all computed by
 * exact per-line sorting of intersection parameters.
 *
 * usage: verify points K certfile [uncoveredfile]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef __int128 i128;
typedef long long i64;
typedef unsigned long long u64;

#define MAXN 64
#define MAXL (MAXN * (MAXN - 1) / 2)

static int N, K, NL;
static i64 X0[MAXN], Y0[MAXN];
static int ea[MAXL], eb[MAXL];
static signed char s[MAXN][MAXN];

static void fail(const char *m) { fprintf(stderr, "FATAL: %s\n", m); exit(2); }
static i64 orient(int a, int b, int c) {
    return (X0[b] - X0[a]) * (Y0[c] - Y0[a]) - (Y0[b] - Y0[a]) * (X0[c] - X0[a]);
}
static int sign128(i128 v) { return v > 0 ? 1 : (v < 0 ? -1 : 0); }

static int *cert; static int ncert;

static int in_tri(int x, int a, int b, int c) {
    i64 s1 = orient(a, b, x), s2 = orient(b, c, x), s3 = orient(c, a, x);
    return (s1 > 0 && s2 > 0 && s3 > 0) || (s1 < 0 && s2 < 0 && s3 < 0);
}

static void load_certs(const char *path) {
    FILE *f = fopen(path, "r");
    if (!f) fail("cert file");
    int cap = 1024; cert = malloc(sizeof(int) * cap * (K - 1)); ncert = 0;
    for (;;) {
        int q[70], ok = 1;
        for (int i = 0; i < K - 1; i++) if (fscanf(f, "%d", &q[i]) != 1) { ok = 0; break; }
        if (!ok) break;
        for (int i = 0; i < K - 1; i++) {
            if (q[i] < 0 || q[i] >= N) fail("cert index");
            for (int j = 0; j < i; j++) if (q[i] == q[j]) fail("cert repeated index");
        }
        /* convex position of Q (independent criterion) */
        for (int x = 0; x < K - 1; x++)
            for (int a = 0; a < K - 1; a++) for (int b = a + 1; b < K - 1; b++) for (int c = b + 1; c < K - 1; c++)
                if (x != a && x != b && x != c && in_tri(q[x], q[a], q[b], q[c])) fail("cert not convex");
        /* ccw order: lowest point (y, then x) first, others by angle */
        int lo = 0;
        for (int i = 1; i < K - 1; i++)
            if (Y0[q[i]] < Y0[q[lo]] || (Y0[q[i]] == Y0[q[lo]] && X0[q[i]] < X0[q[lo]])) lo = i;
        int t = q[0]; q[0] = q[lo]; q[lo] = t;
        for (int i = 2; i < K - 1; i++) {
            int x = q[i], j = i - 1;
            while (j >= 1 && orient(q[0], x, q[j]) > 0) { q[j + 1] = q[j]; j--; }
            q[j + 1] = x;
        }
        for (int i = 0; i < K - 1; i++)
            if (orient(q[i], q[(i + 1) % (K - 1)], q[(i + 2) % (K - 1)]) <= 0) fail("cert ccw order");
        if (ncert == cap) { cap *= 2; cert = realloc(cert, sizeof(int) * cap * (K - 1)); }
        memcpy(cert + (size_t)ncert * (K - 1), q, sizeof(int) * (K - 1));
        ncert++;
    }
    fclose(f);
}

static long long scanned = 0;
static int covered(void) {
    int m = K - 1;
    for (int c = 0; c < ncert; c++) {
        int *q = cert + (size_t)c * m, vis = 0;
        scanned++;
        for (int i = 0; i < m && vis < 2; i++)
            if (s[q[i]][q[(i + 1) % m]] < 0) vis++;
        if (vis == 1) {
            if (c > 0) { /* move to front */
                int tmp[70];
                memcpy(tmp, q, sizeof(int) * m);
                memmove(cert + m, cert, sizeof(int) * (size_t)c * m);
                memcpy(cert, tmp, sizeof(int) * m);
            }
            return 1;
        }
    }
    return 0;
}

/* face hashing (FNV-style over sign bytes, two lanes) */
static u64 *tab; static u64 tmask; static long long distinct = 0;
static u64 *utab; static long long udistinct = 0;
static int insert(u64 *t, u64 h1, u64 h2) {
    if (!h1) h1 = 1;
    for (u64 i = h1 & tmask;; i = (i + 1) & tmask) {
        if (!t[2 * i]) { t[2 * i] = h1; t[2 * i + 1] = h2; return 1; }
        if (t[2 * i] == h1 && t[2 * i + 1] == h2) return 0;
    }
}

typedef struct { i64 T, D; int l2; } Ip;
static int cmpIp(const void *A, const void *B) {
    const Ip *a = A, *b = B;
    i128 l = (i128)a->T * b->D, r = (i128)b->T * a->D;
    return l < r ? -1 : (l > r ? 1 : 0);
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: verify points K certfile [uncovered]\n"); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) fail("points");
    i64 x, y; N = 0;
    while (fscanf(f, "%lld %lld", &x, &y) == 2) { X0[N] = x; Y0[N] = y; N++; }
    fclose(f);
    for (int i = 0; i < N; i++)
        if (X0[i] >= (1LL << 27) || -X0[i] >= (1LL << 27) || Y0[i] >= (1LL << 27) || -Y0[i] >= (1LL << 27))
            fail("coordinate bound");
    for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) for (int c = b + 1; c < N; c++)
        if (orient(a, b, c) == 0) fail("not in general position");
    K = atoi(argv[2]);
    load_certs(argv[3]);
    FILE *uf = argc > 4 ? fopen(argv[4], "w") : NULL;
    NL = 0;
    for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) { ea[NL] = a; eb[NL] = b; NL++; }
    u64 sz = 1; while (sz < (u64)(2 * (1 + NL + (long long)NL * NL / 2))) sz <<= 1;
    tab = calloc(2 * sz, 8); utab = calloc(2 * sz, 8); tmask = sz - 1;
    if (!tab || !utab) fail("alloc");

    long long E = 0, cnt_by_m[MAXL + 2]; memset(cnt_by_m, 0, sizeof(cnt_by_m));
    long long ncand = 0, nunc = 0;
    Ip *ip = malloc(sizeof(Ip) * NL);
    signed char base[MAXL];
    clock_t t0 = clock();
    for (int l = 0; l < NL; l++) {
        int a = ea[l], b = eb[l];
        i64 ux = X0[b] - X0[a], uy = Y0[b] - Y0[a];
        int n = 0;
        for (int l2 = 0; l2 < NL; l2++) {
            if (l2 == l) continue;
            int c = ea[l2], d = eb[l2];
            i64 wx = X0[d] - X0[c], wy = Y0[d] - Y0[c];
            i64 D = ux * wy - uy * wx;
            if (!D) continue;
            i64 T = (X0[c] - X0[a]) * wy - (Y0[c] - Y0[a]) * wx;
            if (D < 0) { D = -D; T = -T; }
            ip[n].T = T; ip[n].D = D; ip[n].l2 = l2; n++;
        }
        if (n == 0) fail("line without vertices");
        qsort(ip, n, sizeof(Ip), cmpIp);
        int kdist = 0;
        for (int i = 0; i < n;) {
            int j = i;
            while (j < n && cmpIp(&ip[i], &ip[j]) == 0) j++;
            int m = (j - i) + 1; /* lines through this vertex */
            kdist++;
            cnt_by_m[m]++;
            /* vertex v = a + (T/D) u, homogeneous (Xv, Yv, Dv) */
            i128 Dv = ip[i].D, T = ip[i].T;
            i128 Xv = (i128)X0[a] * Dv + T * ux, Yv = (i128)Y0[a] * Dv + T * uy;
            for (int l3 = 0; l3 < NL; l3++) {
                int c = ea[l3], d = eb[l3];
                /* orient(c,d,v)*Dv = (dx-cx)(Yv - cy Dv) - (dy-cy)(Xv - cx Dv) */
                i128 o = (i128)(X0[d] - X0[c]) * (Yv - (i128)Y0[c] * Dv) - (i128)(Y0[d] - Y0[c]) * (Xv - (i128)X0[c] * Dv);
                base[l3] = (signed char)sign128(o);
            }
            if (base[l] != 0) fail("vertex not on its line");
            for (int i2 = i; i2 < j; i2++) if (base[ip[i2].l2] != 0) fail("vertex not on crossing line");
            for (int su = -1; su <= 1; su += 2)
                for (int sn = -1; sn <= 1; sn += 2) {
                    i64 dux = su * ux, duy = su * uy, nx = -sn * uy, ny = sn * ux;
                    u64 h1 = 1469598103934665603ULL, h2 = 0x84222325CBF29CE4ULL;
                    for (int l3 = 0; l3 < NL; l3++) {
                        int c = ea[l3], d = eb[l3];
                        int sv = base[l3];
                        if (!sv) {
                            i64 ex = X0[d] - X0[c], ey = Y0[d] - Y0[c];
                            i64 e1 = ex * duy - ey * dux;
                            sv = (e1 > 0) - (e1 < 0);
                            if (!sv) {
                                i64 e2 = ex * ny - ey * nx;
                                sv = (e2 > 0) - (e2 < 0);
                                if (!sv) fail("degenerate perturbation");
                            }
                        }
                        s[c][d] = (signed char)sv; s[d][c] = (signed char)-sv;
                        u64 byte = (u64)(sv > 0 ? 0x2B : 0x2D);
                        h1 = (h1 ^ byte) * 1099511628211ULL;
                        h2 = (h2 ^ (byte + (u64)l3)) * 0x100000001B3ULL;
                        h2 ^= h2 >> 29;
                    }
                    ncand++;
                    insert(tab, h1, h2) ? distinct++ : 0;
                    if (!covered()) {
                        nunc++;
                        if (insert(utab, h1, h2)) {
                            udistinct++;
                            if (uf) {
                                for (int l3 = 0; l3 < NL; l3++) fputc(s[ea[l3]][eb[l3]] > 0 ? '+' : '-', uf);
                                fputc('\n', uf);
                            }
                        }
                    }
                }
            i = j;
        }
        E += kdist + 1;
        if ((l & 127) == 0)
            fprintf(stderr, "line %d/%d cand=%lld faces=%lld uncovered=%lld scanned=%lld t=%.1fs\n",
                    l, NL, ncand, distinct, nunc, scanned, (double)(clock() - t0) / CLOCKS_PER_SEC);
    }
    /* V = sum_m cnt_by_m[m] / m, must be integral for each m */
    long long V = 0;
    for (int m = 2; m <= NL + 1; m++) {
        if (cnt_by_m[m] % m) fail("vertex multiplicity count not divisible");
        V += cnt_by_m[m] / m;
    }
    long long F = E - V + 1;
    printf("{\"N\": %d, \"K\": %d, \"certificates\": %d, \"E\": %lld, \"V\": %lld, \"faces_E_minus_V_plus_1\": %lld, "
           "\"candidates\": %lld, \"distinct_faces_hit\": %lld, \"uncovered_candidates\": %lld, "
           "\"uncovered_distinct_faces\": %lld, \"cpu_seconds\": %.1f}\n",
           N, K, ncert, E, V, F, ncand, distinct, nunc, udistinct, (double)(clock() - t0) / CLOCKS_PER_SEC);
    if (uf) fclose(uf);
    return 0;
}
