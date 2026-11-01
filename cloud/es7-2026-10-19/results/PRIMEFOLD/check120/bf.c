/*
 * bf.c -- brute-force count of k-subsets in convex position (k = 3..K) from an orientation
 * table, for small n.  Criterion (Caratheodory, general position): a set is in convex position
 * iff no point lies strictly inside a triangle spanned by three other points of the set.
 * Usage: bf OTAB K
 */
#include <stdio.h>
#include <stdlib.h>

static int n, K;
static signed char *T;
#define OR(a, b, c) T[((size_t)(a) * n + (b)) * n + (c)]
static unsigned long long cnt[64];
static int sel[64];

static int inside(int p, int a, int b, int c) {
    int s1 = OR(a, b, p), s2 = OR(b, c, p), s3 = OR(c, a, p);
    return (s1 == s2 && s2 == s3);
}

static int convex_position(int k) {
    for (int ip = 0; ip < k; ip++) {
        int p = sel[ip];
        for (int ia = 0; ia < k; ia++) if (ia != ip)
            for (int ib = ia + 1; ib < k; ib++) if (ib != ip)
                for (int ic = ib + 1; ic < k; ic++) if (ic != ip)
                    if (inside(p, sel[ia], sel[ib], sel[ic])) return 0;
    }
    return 1;
}

static void rec(int start, int k) {
    if (k >= 3 && convex_position(k)) cnt[k]++;
    if (k == K) return;
    for (int x = start; x < n; x++) { sel[k] = x; rec(x + 1, k + 1); }
}

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "rb");
    if (!f || fscanf(f, "%d", &n) != 1 || fgetc(f) != '\n') { fprintf(stderr, "bad table\n"); return 2; }
    K = atoi(argv[2]);
    size_t N = (size_t)n * n * n;
    T = malloc(N);
    if (fread(T, 1, N, f) != N) { fprintf(stderr, "short\n"); return 2; }
    fclose(f);
    rec(0, 0);
    for (int k = 3; k <= K; k++) printf("bf convex %2d-gons: %llu\n", k, cnt[k]);
    return 0;
}
