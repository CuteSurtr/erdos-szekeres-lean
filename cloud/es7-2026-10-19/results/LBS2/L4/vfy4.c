/*
 * vfy4.c -- exact checks independent of walk.c's DP.
 *   - general position: every triple, __int128 orientation;
 *   - number of k-subsets in convex position, k = 5, 6, 7 (and >= 8 flagged), by
 *     enumerating index-increasing subsets and extending a convex set C by q only if
 *     q lies in no triangle of C and no point of C lies in a triangle (q, c1, c2)
 *     (a set in general position is convex iff no point is inside a triangle of others);
 *   - order-type hash, up to relabeling and reflection: for every hull vertex h and
 *     both orientations, label h as 0 and the others by angle around h; the canonical
 *     form is the lexicographically least sign sequence over triples i<j<k; output its
 *     64-bit FNV-1a hash.
 * usage: vfy4 FILE   -> one JSON line
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
typedef unsigned long long u64;
#define MAXN 40
static int N;
static ll X[MAXN], Y[MAXN];
static signed char O[MAXN][MAXN][MAXN];
static long long cnt[MAXN];
static int C[MAXN], csz;

static int orient(int a, int b, int c) {
    __int128 v = (__int128)(X[b] - X[a]) * (Y[c] - Y[a]) - (__int128)(Y[b] - Y[a]) * (X[c] - X[a]);
    return (v > 0) - (v < 0);
}
static int inside(int d, int a, int b, int c) {
    int s = O[a][b][c];
    return O[a][b][d] == s && O[b][c][d] == s && O[c][a][d] == s;
}
static int can_add(int q) {
    for (int i = 0; i < csz; i++)
        for (int j = i + 1; j < csz; j++) {
            for (int k = j + 1; k < csz; k++) if (inside(q, C[i], C[j], C[k])) return 0;
            for (int k = 0; k < csz; k++) if (k != i && k != j && inside(C[k], q, C[i], C[j])) return 0;
        }
    return 1;
}
static void rec(int start) {
    cnt[csz]++;
    if (csz >= 8) return;
    for (int q = start; q < N; q++)
        if (can_add(q)) { C[csz++] = q; rec(q + 1); csz--; }
}
static int hh, mir;
static int cmpang(const void *u, const void *v) {
    int a = *(const int *)u, b = *(const int *)v;
    return mir * O[hh][a][b] > 0 ? -1 : 1;
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r");
    ll x, y; N = 0;
    while (fscanf(f, "%lld %lld", &x, &y) == 2) { X[N] = x; Y[N] = y; N++; }
    fclose(f);
    ll mx = 0;
    for (int i = 0; i < N; i++) { if (llabs(X[i]) > mx) mx = llabs(X[i]); if (llabs(Y[i]) > mx) mx = llabs(Y[i]); }
    if (mx >= (1LL << 60)) { printf("{\"error\":\"coords too large\"}\n"); return 2; }
    int gp = 1;
    for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) for (int c = 0; c < N; c++) {
        O[a][b][c] = (a == b || b == c || a == c) ? 0 : orient(a, b, c);
        if (a < b && b < c && O[a][b][c] == 0) gp = 0;
    }
    if (!gp) { printf("{\"N\": %d, \"general_position\": false}\n", N); return 1; }
    csz = 0; rec(0);
    /* canonical form */
    static signed char best[MAXN * MAXN * MAXN], cur[MAXN * MAXN * MAXN];
    int have = 0, nt = 0, nhull = 0;
    for (int h = 0; h < N; h++) {
        int hull = 1;
        for (int a = 0; a < N && hull; a++) if (a != h) {
            /* h is a hull vertex iff some a has all others on one side of line h-a... use: h not inside any triangle */
        }
        for (int a = 0; a < N && hull; a++) for (int b = a + 1; b < N && hull; b++) for (int c = b + 1; c < N && hull; c++)
            if (a != h && b != h && c != h && inside(h, a, b, c)) hull = 0;
        if (!hull) continue;
        nhull++;
        for (mir = 1; mir >= -1; mir -= 2) {
            int lab[MAXN], m = 0;
            hh = h;
            for (int i = 0; i < N; i++) if (i != h) lab[m++] = i;
            qsort(lab, m, sizeof(int), cmpang);
            int L[MAXN]; L[0] = h; for (int i = 0; i < m; i++) L[i + 1] = lab[i];
            nt = 0;
            for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++) for (int k = j + 1; k < N; k++)
                cur[nt++] = mir * O[L[i]][L[j]][L[k]];
            if (!have || memcmp(cur, best, nt) < 0) { memcpy(best, cur, nt); have = 1; }
        }
    }
    u64 hsh = 1469598103934665603ULL;
    for (int i = 0; i < nt; i++) { hsh ^= (unsigned char)(best[i] + 1); hsh *= 1099511628211ULL; }
    printf("{\"N\": %d, \"general_position\": true, \"max_abs_coord\": %lld, \"hull\": %d, \"c5\": %lld, \"c6\": %lld, \"c7\": %lld, \"c8plus\": %lld, \"ot_hash\": \"%016llx\"}\n",
           N, mx, nhull, cnt[5], cnt[6], cnt[7], cnt[8], hsh);
    return 0;
}
