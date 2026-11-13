/* Exact limit order type of a stacked configuration + convex polygon DP, all in C.
   Point i = eps^e[i] * (x[i], y[i]), integers |x|,|y| < 2^62, eps a symbolic infinitesimal.
   orient(a,b,c) = cr(a,b) + cr(b,c) + cr(c,a), cr(eps^e1 z1, eps^e2 z2) = eps^(e1+e2) (x1 y2 - y1 x2);
   sign = sign of the lowest-order nonzero coefficient (exact, __int128; |coefficient| <= 3 * 2 * 2^124 < 2^127).
   Returns maxlen (largest convex subset), cnt[L] = #convex L-gons (L <= kmax), *nzero = #triples with sign 0.
   The DP is that of cvxdp.c (anchor = lowest point in (y, x) order, angular sort by orientation).
   Build: gcc -O2 -shared -fPIC -o libstackeval.so stackeval.c */
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define NMAX 160
typedef __int128 i128;

static int lowsign3(int ea, i128 va, int eb, i128 vb, int ec, i128 vc) {
    /* terms (exponent, value): return sign of lowest exponent group with nonzero sum */
    int es[3] = {ea, eb, ec}; i128 vs[3] = {va, vb, vc};
    int done[3] = {0, 0, 0};
    for (int it = 0; it < 3; it++) {
        int emin = 1 << 30;
        for (int i = 0; i < 3; i++) if (!done[i] && es[i] < emin) emin = es[i];
        if (emin == (1 << 30)) break;
        i128 s = 0;
        for (int i = 0; i < 3; i++) if (!done[i] && es[i] == emin) { s += vs[i]; done[i] = 1; }
        if (s > 0) return 1;
        if (s < 0) return -1;
    }
    return 0;
}

static int cmp1(int ea, int64_t a, int eb, int64_t b) {
    /* sign of eps^ea a - eps^eb b */
    if (ea == eb) return (a > b) - (a < b);
    if (ea < eb) { if (a) return (a > 0) ? 1 : -1; return (b > 0) ? -1 : (b < 0 ? 1 : 0); }
    if (b) return (b > 0) ? -1 : 1;
    return (a > 0) - (a < 0);
}

static const int *GE; static const int64_t *GX, *GY;
static int cmp_low(const void *pa, const void *pb) {
    int a = *(const int *)pa, b = *(const int *)pb;
    int c = cmp1(GE[a], GY[a], GE[b], GY[b]);
    if (!c) c = cmp1(GE[a], GX[a], GE[b], GX[b]);
    return c;
}

static signed char *GS; static int GN; static int GP;
static int cmp_ang(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    signed char s = GS[(size_t)GP * GN * GN + (size_t)x * GN + y];
    return s > 0 ? -1 : 1;
}

int stack_eval(int n, const int *e, const int64_t *x, const int64_t *y, int64_t *cnt, int kmax, int *nzero) {
    static signed char S[NMAX * NMAX * NMAX];
    static int rank[NMAX], ord[NMAX], U[NMAX];
    static int64_t c[2][NMAX][NMAX];
    static int best[NMAX][NMAX];
    if (n > NMAX || kmax > 12) return -1;
    int nz = 0;
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) for (int k = j + 1; k < n; k++) {
        i128 cij = (i128)x[i] * y[j] - (i128)y[i] * x[j];
        i128 cjk = (i128)x[j] * y[k] - (i128)y[j] * x[k];
        i128 cki = (i128)x[k] * y[i] - (i128)y[k] * x[i];
        int s = lowsign3(e[i] + e[j], cij, e[j] + e[k], cjk, e[k] + e[i], cki);
        if (!s) nz++;
        S[(size_t)i * n * n + j * n + k] = S[(size_t)j * n * n + k * n + i] = S[(size_t)k * n * n + i * n + j] = (signed char)s;
        S[(size_t)j * n * n + i * n + k] = S[(size_t)i * n * n + k * n + j] = S[(size_t)k * n * n + j * n + i] = (signed char)(-s);
    }
    *nzero = nz;
    if (nz) return 0;
    GE = e; GX = x; GY = y;
    for (int i = 0; i < n; i++) ord[i] = i;
    qsort(ord, n, sizeof(int), cmp_low);
    for (int i = 0; i < n; i++) rank[ord[i]] = i;
    for (int L = 0; L <= kmax; L++) cnt[L] = 0;
    GS = S; GN = n;
    int maxlen = 0;
    for (int p = 0; p < n; p++) {
        int m = 0;
        for (int q = 0; q < n; q++) if (rank[q] > rank[p]) U[m++] = q;
        if (m < 2) { if (m + 1 > maxlen) maxlen = m + 1; continue; }
        GP = p; qsort(U, m, sizeof(int), cmp_ang);
        for (int j = 0; j < m; j++) for (int i = 0; i < j; i++) best[i][j] = 3;
        for (int j = 0; j < m; j++)
            for (int i = 0; i < j; i++) {
                int bij = best[i][j];
                for (int k = j + 1; k < m; k++)
                    if (S[(size_t)U[i] * n * n + (size_t)U[j] * n + U[k]] > 0 && bij + 1 > best[j][k]) best[j][k] = bij + 1;
            }
        for (int j = 0; j < m; j++) for (int i = 0; i < j; i++)
            if (S[(size_t)U[i] * n * n + (size_t)U[j] * n + p] > 0 && best[i][j] > maxlen) maxlen = best[i][j];
        int cur = 0;
        memset(c[cur], 0, sizeof(c[cur]));
        for (int j = 0; j < m; j++) for (int i = 0; i < j; i++) c[cur][i][j] = 1;
        for (int L = 3; L <= kmax; L++) {
            int64_t tot = 0;
            for (int j = 0; j < m; j++) for (int i = 0; i < j; i++)
                if (c[cur][i][j] && S[(size_t)U[i] * n * n + (size_t)U[j] * n + p] > 0) tot += c[cur][i][j];
            cnt[L] += tot;
            if (L == kmax) break;
            int nx = 1 - cur;
            memset(c[nx], 0, sizeof(c[nx]));
            int any = 0;
            for (int j = 0; j < m; j++) for (int i = 0; i < j; i++) {
                int64_t v = c[cur][i][j];
                if (!v) continue;
                for (int k = j + 1; k < m; k++)
                    if (S[(size_t)U[i] * n * n + (size_t)U[j] * n + U[k]] > 0) { c[nx][j][k] += v; any = 1; }
            }
            cur = nx;
            if (!any) break;
        }
    }
    return maxlen;
}
