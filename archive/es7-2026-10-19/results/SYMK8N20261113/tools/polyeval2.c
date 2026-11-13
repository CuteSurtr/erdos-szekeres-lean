/* Exact limit order type for points that are polynomials in a symbolic infinitesimal eps:
   point i = sum_{t} eps^{E[t]} (X[t], Y[t]) over its terms t = off[i] .. off[i+1]-1 (exponents in [-8, 8]).
   orient(a,b,c) = cr(a,b)+cr(b,c)+cr(c,a), expanded by exponent; sign of the lowest nonzero coefficient
   (__int128; callers keep |coords| <= 2^58 and <= 3 terms per point so that sums cannot overflow).
   Coordinate comparisons for the (y, x) anchor order likewise.  Then the convex-polygon DP of cvxdp.c.
   Build: gcc -O2 -shared -fPIC -o libpolyeval.so polyeval.c */
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#define NMAX 160
#define EOFF 64
#define ENUM 200
typedef __int128 i128;
static const int *GOFF, *GE; static const int64_t *GX, *GY;

static void crpoly(int a, int b, i128 *acc) {
    for (int s = GOFF[a]; s < GOFF[a + 1]; s++)
        for (int t = GOFF[b]; t < GOFF[b + 1]; t++)
            acc[GE[s] + GE[t] + EOFF] += (i128)GX[s] * GY[t] - (i128)GY[s] * GX[t];
}
static int orientp(int a, int b, int c) {
    i128 acc[ENUM]; memset(acc, 0, sizeof(acc));
    crpoly(a, b, acc); crpoly(b, c, acc); crpoly(c, a, acc);
    for (int k = 0; k < ENUM; k++) { if (acc[k] > 0) return 1; if (acc[k] < 0) return -1; }
    return 0;
}
static int cmpcoord(int a, int b, int which) {
    i128 acc[ENUM]; memset(acc, 0, sizeof(acc));
    for (int s = GOFF[a]; s < GOFF[a + 1]; s++) acc[GE[s] + EOFF + 8] += which ? GY[s] : GX[s];
    for (int s = GOFF[b]; s < GOFF[b + 1]; s++) acc[GE[s] + EOFF + 8] -= which ? GY[s] : GX[s];
    for (int k = 0; k < ENUM; k++) { if (acc[k] > 0) return 1; if (acc[k] < 0) return -1; }
    return 0;
}
static int cmp_low(const void *pa, const void *pb) {
    int a = *(const int *)pa, b = *(const int *)pb;
    int c = cmpcoord(a, b, 1);
    if (!c) c = cmpcoord(a, b, 0);
    return c;
}
static signed char *GS; static int GN; static int GP;
static int cmp_ang(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    return GS[(size_t)GP * GN * GN + (size_t)x * GN + y] > 0 ? -1 : 1;
}
int poly_eval(int n, const int *off, const int *E, const int64_t *X, const int64_t *Y, int64_t *cnt, int kmax, int *nzero) {
    static signed char S[NMAX * NMAX * NMAX];
    static int rank[NMAX], ord[NMAX], U[NMAX];
    static int64_t c[2][NMAX][NMAX];
    static int best[NMAX][NMAX];
    if (n > NMAX || kmax > 12) return -1;
    GOFF = off; GE = E; GX = X; GY = Y;
    int nz = 0;
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) for (int k = j + 1; k < n; k++) {
        int s = orientp(i, j, k);
        if (!s) nz++;
        S[(size_t)i * n * n + j * n + k] = S[(size_t)j * n * n + k * n + i] = S[(size_t)k * n * n + i * n + j] = (signed char)s;
        S[(size_t)j * n * n + i * n + k] = S[(size_t)i * n * n + k * n + j] = S[(size_t)k * n * n + j * n + i] = (signed char)(-s);
    }
    *nzero = nz;
    if (nz) return 0;
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
        for (int j = 0; j < m; j++) for (int i = 0; i < j; i++) {
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
            int nx = 1 - cur; memset(c[nx], 0, sizeof(c[nx])); int any = 0;
            for (int j = 0; j < m; j++) for (int i = 0; i < j; i++) {
                int64_t v = c[cur][i][j]; if (!v) continue;
                for (int k = j + 1; k < m; k++)
                    if (S[(size_t)U[i] * n * n + (size_t)U[j] * n + U[k]] > 0) { c[nx][j][k] += v; any = 1; }
            }
            cur = nx; if (!any) break;
        }
    }
    return maxlen;
}
