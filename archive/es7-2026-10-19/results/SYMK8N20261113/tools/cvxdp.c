/* Exact convex-polygon DP on a precomputed orientation sign table (no geometry inside).
   Input: n, sign table S[i*n*n+j*n+k] in {-1,+1} (all triples of distinct points; must be a chirotope of a point set),
          rank[i] = position of point i in the (y, x) lexicographic order (lowest first).
   For every anchor p, the points q with rank[q] > rank[p] lie in the closed upper half-plane of p (angles in [0, pi)),
   so they are sorted by angle around p with the comparator orient(p, a, b) > 0  <=>  a before b.
   A convex polygon with lowest vertex p is p, u_1, ..., u_{L-1} in this angular order with
   orient(u_{i-1}, u_i, u_{i+1}) > 0 for 1 < i < L-1 and orient(u_{L-2}, u_{L-1}, p) > 0
   (the turns at p and u_1 are automatic).  Each convex polygon is counted once (at its lowest vertex).
   Output: maxlen = largest convex subset size, cnt[L] = number of convex L-gons for L <= KMAX.
   Build: gcc -O2 -shared -fPIC -o libcvxdp.so cvxdp.c */
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define NMAX 160
#define KMAX 12

static const signed char *GS; static int GN; static int GP;
static int cmp_ang(const void *a, const void *b) {
    int x = *(const int *)a, y = *(const int *)b;
    signed char s = GS[(size_t)GP * GN * GN + (size_t)x * GN + y];
    return s > 0 ? -1 : 1;
}

int cvx_dp(int n, const signed char *S, const int *rank, int64_t *cnt, int kmax) {
    static int U[NMAX];
    static int64_t c[2][NMAX][NMAX];
    static int best[NMAX][NMAX];
    int maxlen = 0;
    if (n > NMAX || kmax > KMAX) return -1;
    for (int L = 0; L <= kmax; L++) cnt[L] = 0;
    GS = S; GN = n;
    for (int p = 0; p < n; p++) {
        int m = 0;
        for (int q = 0; q < n; q++) if (rank[q] > rank[p]) U[m++] = q;
        if (m < 2) { if (m + 1 > maxlen) maxlen = m + 1; continue; }
        GP = p; qsort(U, m, sizeof(int), cmp_ang);
        /* longest chains: best[i][j] = max #vertices of chain p,...,u_i,u_j */
        for (int j = 0; j < m; j++) for (int i = 0; i < j; i++) best[i][j] = 3;
        for (int j = 0; j < m; j++)
            for (int i = 0; i < j; i++) {
                int bij = best[i][j];
                for (int k = j + 1; k < m; k++)
                    if (S[(size_t)U[i] * n * n + (size_t)U[j] * n + U[k]] > 0 && bij + 1 > best[j][k]) best[j][k] = bij + 1;
            }
        for (int j = 0; j < m; j++) for (int i = 0; i < j; i++)
            if (S[(size_t)U[i] * n * n + (size_t)U[j] * n + p] > 0 && best[i][j] > maxlen) maxlen = best[i][j];
        if (maxlen < 2) maxlen = 2;
        /* counts by length */
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
