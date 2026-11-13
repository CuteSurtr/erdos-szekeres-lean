/* Count k-subsets in convex position (default k = 7) of a planar point set in general position.
 * usage: count7 FILE [k]     FILE: first line n, then n lines "x y" (integers, |x|,|y| < 2^30 so that every
 * orientation is exact in 64-bit arithmetic; checked).  Depth-first search over convex subsets: a set is in convex
 * position iff all its 4-subsets are, so a new point is added only if every 4-set it forms with 3 chosen points is
 * convex.  Prints the count (and the subsets when there are at most 50).
 */
#include <stdio.h>
#include <stdlib.h>

#define MAXN 64
static long long X[MAXN], Y[MAXN];
static int n, K;
static unsigned char conv4[MAXN][MAXN][MAXN][MAXN];
static int cur[16];
static long long count = 0;

static int sgn(long long v) { return (v > 0) - (v < 0); }
static int orient(int a, int b, int c) {
    long long v = (X[b] - X[a]) * (Y[c] - Y[a]) - (Y[b] - Y[a]) * (X[c] - X[a]);
    return sgn(v);
}
static int inside(int q, int a, int b, int d) {
    int s1 = orient(a, b, q), s2 = orient(b, d, q), s3 = orient(d, a, q);
    return s1 == s2 && s2 == s3 && s1 != 0;
}

static void dfs(int depth, int start) {
    if (depth == K) {
        count++;
        if (count <= 50) {
            printf("convex:");
            for (int i = 0; i < K; i++) printf(" %d", cur[i]);
            printf("\n");
        }
        return;
    }
    for (int p = start; p < n; p++) {
        int ok = 1;
        for (int i = 0; i < depth && ok; i++)
            for (int j = i + 1; j < depth && ok; j++)
                for (int k = j + 1; k < depth && ok; k++)
                    if (!conv4[cur[i]][cur[j]][cur[k]][p]) ok = 0;
        if (!ok) continue;
        cur[depth] = p;
        dfs(depth + 1, p + 1);
    }
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: count7 FILE [k]\n"); return 2; }
    K = argc > 2 ? atoi(argv[2]) : 7;
    FILE *f = fopen(argv[1], "r");
    if (!f || fscanf(f, "%d", &n) != 1 || n > MAXN) { fprintf(stderr, "bad input\n"); return 2; }
    for (int i = 0; i < n; i++) {
        if (fscanf(f, "%lld %lld", &X[i], &Y[i]) != 2) { fprintf(stderr, "bad point\n"); return 2; }
        if (llabs(X[i]) >= (1LL << 30) || llabs(Y[i]) >= (1LL << 30)) { fprintf(stderr, "coordinate too large\n"); return 2; }
    }
    for (int a = 0; a < n; a++)
        for (int b = a + 1; b < n; b++)
            for (int c = b + 1; c < n; c++) {
                if (orient(a, b, c) == 0) { fprintf(stderr, "collinear %d %d %d\n", a, b, c); return 3; }
                for (int d = c + 1; d < n; d++) {
                    int cv = !(inside(a, b, c, d) || inside(b, a, c, d) || inside(c, a, b, d) || inside(d, a, b, c));
                    int idx[4] = {a, b, c, d};
                    /* store for every ordering of the first three (the last index is the newest point) */
                    for (int x = 0; x < 4; x++) for (int y = 0; y < 4; y++) for (int z = 0; z < 4; z++) for (int w = 0; w < 4; w++)
                        if (x != y && x != z && x != w && y != z && y != w && z != w)
                            conv4[idx[x]][idx[y]][idx[z]][idx[w]] = (unsigned char)cv;
                }
            }
    if (K <= 3) { printf("count %d\n", 0); return 0; }
    dfs(0, 0);
    printf("count %lld\n", count);
    return 0;
}
