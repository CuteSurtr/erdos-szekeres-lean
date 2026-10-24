/* Brute force over ALL K-subsets of an integer point set: is any K-subset in convex position?
 * A set is in convex position iff no point lies inside the triangle of three others
 * (d inside abc iff orient(a,b,d), orient(b,c,d), orient(c,a,d) all have the same sign).
 * Orientations are computed exactly (__int128) from the integer coordinates; also checks
 * general position (no zero orientation).
 * usage: brute7 K file.pts     (file.pts: one "x y" per line)
 * prints: N, number of K-subsets in convex position (stops early at the first unless FULL=1),
 * and the number of collinear triples.  Exit 0 iff no convex K-subset and general position. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 64
static int N, K;
static long long X[MAXN], Y[MAXN];
static signed char O[MAXN][MAXN][MAXN];

int main(int argc, char **argv) {
    if (argc != 3) { fprintf(stderr, "usage: brute7 K file.pts\n"); return 2; }
    K = atoi(argv[1]);
    FILE *f = fopen(argv[2], "r");
    if (!f) { fprintf(stderr, "cannot open\n"); return 2; }
    N = 0;
    while (N < MAXN && fscanf(f, "%lld %lld", &X[N], &Y[N]) == 2) N++;
    fclose(f);
    long collinear = 0;
    for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) for (int c = 0; c < N; c++) {
        if (a == b || b == c || a == c) { O[a][b][c] = 0; continue; }
        __int128 d = (__int128)(X[b] - X[a]) * (Y[c] - Y[a]) - (__int128)(Y[b] - Y[a]) * (X[c] - X[a]);
        O[a][b][c] = d > 0 ? 1 : (d < 0 ? -1 : 0);
        if (d == 0 && a < b && b < c) collinear++;
    }
    int full = getenv("FULL") != NULL;
    long convex = 0, subsets = 0;
    int idx[MAXN];
    for (int i = 0; i < K; i++) idx[i] = i;
    while (1) {
        subsets++;
        int ok = 1;
        for (int d = 0; d < K && ok; d++) {
            int pd = idx[d];
            for (int a = 0; a < K && ok; a++) if (a != d) for (int b = a + 1; b < K && ok; b++) if (b != d) for (int c = b + 1; c < K && ok; c++) if (c != d) {
                int pa = idx[a], pb = idx[b], pc = idx[c];
                int o1 = O[pa][pb][pd], o2 = O[pb][pc][pd], o3 = O[pc][pa][pd];
                if (o1 != 0 && o1 == o2 && o2 == o3) ok = 0;   /* pd strictly inside triangle */
            }
        }
        if (ok) {
            convex++;
            if (!full) {
                printf("N=%d K=%d: convex %d-subset found:", N, K, K);
                for (int i = 0; i < K; i++) printf(" %d", idx[i]);
                printf("\n");
                break;
            }
        }
        int i = K - 1;
        while (i >= 0 && idx[i] == N - K + i) i--;
        if (i < 0) break;
        idx[i]++;
        for (int j = i + 1; j < K; j++) idx[j] = idx[j - 1] + 1;
    }
    printf("N=%d K=%d subsets_checked=%ld convex_%d_subsets=%ld collinear_triples=%ld\n", N, K, subsets, K, convex, collinear);
    return (convex == 0 && collinear == 0) ? 0 : 1;
}
