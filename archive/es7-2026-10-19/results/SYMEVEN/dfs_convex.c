/*
 * Exhaustive enumeration of all subsets in convex position, by size, for a planar point set in
 * general position (exact: int64 coordinates, __int128 orientation).
 * Independent of the Python code: convex position is hereditary, so a DFS over index-increasing
 * sequences that only extends convex sets visits every convex subset exactly once. Extension test:
 * for a convex set C (|C|>=3, hull in CCW order) the set C+z is convex iff exactly one hull edge has
 * z strictly on its right side.
 * Also checks: no three collinear (all triples), central symmetry, origin absent.
 * Usage: dfs_convex POINTS_FILE MAXSIZE      (lines "x y [label]", '#' comments)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define MAXN 4096
#define MAXK 32
typedef __int128 i128;
static long long X[MAXN], Y[MAXN];
static int N, K;
static unsigned long long cnt[MAXK + 2];

static int orient(int a, int b, int c) {
    i128 v = (i128)(X[b] - X[a]) * (i128)(Y[c] - Y[a]) - (i128)(Y[b] - Y[a]) * (i128)(X[c] - X[a]);
    return (v > 0) - (v < 0);
}

static void dfs(const int *hull, int h, int last) {
    int nh[MAXK + 2];
    for (int z = last + 1; z < N; z++) {
        if (h == 1) {
            nh[0] = hull[0]; nh[1] = z;
        } else if (h == 2) {
            if (orient(hull[0], hull[1], z) > 0) { nh[0] = hull[0]; nh[1] = hull[1]; nh[2] = z; }
            else { nh[0] = hull[1]; nh[1] = hull[0]; nh[2] = z; }
        } else {
            int vis = 0, at = -1;
            for (int i = 0; i < h; i++) {
                int o = orient(hull[i], hull[(i + 1) % h], z);
                if (o == 0) { fprintf(stderr, "collinear triple met in DFS\n"); exit(2); }
                if (o < 0) { vis++; at = i; if (vis > 1) break; }
            }
            if (vis != 1) continue;
            int t = 0;
            for (int i = 0; i <= at; i++) nh[t++] = hull[i];
            nh[t++] = z;
            for (int i = at + 1; i < h; i++) nh[t++] = hull[i];
        }
        cnt[h + 1]++;
        if (h + 1 < K) dfs(nh, h + 1, z);
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: %s POINTS MAXSIZE\n", argv[0]); return 1; }
    K = atoi(argv[2]);
    if (K < 3 || K > MAXK) { fprintf(stderr, "bad MAXSIZE\n"); return 1; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    char line[1024];
    while (fgets(line, sizeof line, f)) {
        if (line[0] == '#' || line[0] == '\n') continue;
        long long x, y;
        if (sscanf(line, "%lld %lld", &x, &y) != 2) continue;
        if (llabs(x) > (1LL << 60) || llabs(y) > (1LL << 60)) { fprintf(stderr, "coordinate too large\n"); return 1; }
        if (N >= MAXN) { fprintf(stderr, "too many points\n"); return 1; }
        X[N] = x; Y[N] = y; N++;
    }
    fclose(f);
    /* distinctness, symmetry, origin */
    int sym = 1, orig = 0, dup = 0;
    for (int i = 0; i < N; i++) {
        if (X[i] == 0 && Y[i] == 0) orig = 1;
        int found = 0;
        for (int j = 0; j < N; j++) {
            if (j != i && X[j] == X[i] && Y[j] == Y[i]) dup = 1;
            if (X[j] == -X[i] && Y[j] == -Y[i]) found = 1;
        }
        if (!found) sym = 0;
    }
    /* general position */
    long long col = 0;
    for (int a = 0; a < N; a++)
        for (int b = a + 1; b < N; b++)
            for (int c = b + 1; c < N; c++)
                if (orient(a, b, c) == 0) col++;
    printf("N=%d duplicates=%d centrally_symmetric=%d origin_in_set=%d collinear_triples=%lld\n",
           N, dup, sym, orig, col);
    if (col || dup) { printf("not in general position; aborting DFS\n"); return 3; }
    cnt[1] = N;
    for (int a = 0; a < N; a++) { int hl[1] = {a}; if (K > 1) dfs(hl, 1, a); }
    for (int s = 1; s <= K; s++) printf("convex subsets of size %d: %llu\n", s, cnt[s]);
    return 0;
}
