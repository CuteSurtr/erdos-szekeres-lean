/* Independent exact brute-force checker (independent check of the 27-point witness of Proposition 8(b)).
 *
 * Usage: brute FILE [b_index]
 *   FILE: lines "x y" (integers).  b_index: index (0-based) of the designated point (default: last).
 *
 * Exact arithmetic: orientation determinants are computed with __int128 from 64-bit coordinates,
 * after checking |coordinate| < 2^30 (so every product is < 2^62 and no overflow can occur even in int64).
 *
 * Convex-position test (method A, triangle containment): a set Q in general position is in convex
 * position iff no point of Q lies strictly inside a triangle spanned by three other points of Q
 * (Caratheodory; general position excludes boundary cases).
 *
 * Reports: general position; for k = 5, 6, 7: number of k-subsets in convex position, and how many of
 * them contain the designated point b; whether b is a hull vertex (b in no triangle of other points);
 * one example convex hexagon.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 64
static long long X[MAXN], Y[MAXN];
static signed char O[MAXN][MAXN][MAXN];
static int N;

static int orient_sign(int a, int b, int c) {
    __int128 v = (__int128)(X[b] - X[a]) * (Y[c] - Y[a]) - (__int128)(Y[b] - Y[a]) * (X[c] - X[a]);
    return (v > 0) - (v < 0);
}

/* strictly inside triangle (a,b,c)?  general position assumed */
static int inside(int p, int a, int b, int c) {
    int o = O[a][b][c];
    return O[a][b][p] == o && O[b][c][p] == o && O[c][a][p] == o;
}

static int convex_position(const int *q, int k) {
    for (int i = 0; i < k; i++)
        for (int j = i + 1; j < k; j++)
            for (int l = j + 1; l < k; l++)
                for (int m = 0; m < k; m++) {
                    if (m == i || m == j || m == l) continue;
                    if (inside(q[m], q[i], q[j], q[l])) return 0;
                }
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s FILE [b_index]\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("fopen"); return 2; }
    long long x, y;
    N = 0;
    while (fscanf(f, "%lld %lld", &x, &y) == 2) {
        if (N >= MAXN) { fprintf(stderr, "too many points\n"); return 2; }
        if (llabs(x) >= (1LL << 30) || llabs(y) >= (1LL << 30)) { fprintf(stderr, "coordinate too large\n"); return 2; }
        X[N] = x; Y[N] = y; N++;
    }
    fclose(f);
    int b = (argc >= 3) ? atoi(argv[2]) : N - 1;
    printf("points: %d, designated b = index %d = (%lld, %lld)\n", N, b, X[b], Y[b]);

    /* distinctness */
    int distinct = 1;
    for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++)
        if (X[i] == X[j] && Y[i] == Y[j]) distinct = 0;
    printf("distinct: %s\n", distinct ? "yes" : "NO");

    /* orientation table + general position */
    long long zero = 0;
    for (int i = 0; i < N; i++) for (int j = 0; j < N; j++) for (int k = 0; k < N; k++) {
        O[i][j][k] = (signed char)orient_sign(i, j, k);
        if (i != j && j != k && i != k && O[i][j][k] == 0) zero++;
    }
    printf("general position: %s (collinear ordered triples: %lld)\n", zero == 0 ? "yes" : "NO", zero);

    /* b is a hull vertex iff it lies in no triangle of three other points */
    long long btri = 0;
    for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++) for (int k = j + 1; k < N; k++) {
        if (i == b || j == b || k == b) continue;
        if (inside(b, i, j, k)) btri++;
    }
    printf("b inside %lld triangles of other points -> b is %sa hull vertex\n", btri, btri == 0 ? "" : "NOT ");

    /* hull vertices overall (same criterion) */
    int nh = 0;
    for (int p = 0; p < N; p++) {
        int in = 0;
        for (int i = 0; i < N && !in; i++) for (int j = i + 1; j < N && !in; j++) for (int k = j + 1; k < N && !in; k++) {
            if (i == p || j == p || k == p) continue;
            if (inside(p, i, j, k)) in = 1;
        }
        if (!in) nh++;
    }
    printf("hull vertices (triangle criterion): %d\n", nh);

    /* enumerate k-subsets */
    for (int k = 5; k <= 7; k++) {
        int q[16];
        for (int i = 0; i < k; i++) q[i] = i;
        long long total = 0, convex = 0, convex_b = 0, total_b = 0;
        int printed = 0;
        while (1) {
            total++;
            int hasb = 0;
            for (int i = 0; i < k; i++) if (q[i] == b) hasb = 1;
            if (hasb) total_b++;
            if (convex_position(q, k)) {
                convex++;
                if (hasb) convex_b++;
                if (k == 6 && !printed) {
                    printf("example convex hexagon (indices):");
                    for (int i = 0; i < k; i++) printf(" %d", q[i]);
                    printf("  points:");
                    for (int i = 0; i < k; i++) printf(" (%lld,%lld)", X[q[i]], Y[q[i]]);
                    printf("\n");
                    printed = 1;
                }
            }
            /* next combination */
            int i = k - 1;
            while (i >= 0 && q[i] == N - k + i) i--;
            if (i < 0) break;
            q[i]++;
            for (int j = i + 1; j < k; j++) q[j] = q[j - 1] + 1;
        }
        printf("k=%d: subsets %lld, convex %lld | subsets containing b %lld, convex containing b %lld\n",
               k, total, convex, total_b, convex_b);
    }
    return 0;
}
