/*
 * cvxenum.c -- exhaustive enumeration of all subsets in convex position (third, unrelated method).
 * Subsets are grown in increasing index order (convex position is hereditary, so pruning a
 * non-convex prefix loses nothing).  The current subset is kept as a CCW convex polygon.
 * A new point x keeps convex position iff exactly one polygon edge (v_i, v_{i+1}) is visible from
 * x, i.e. orient(v_i, v_{i+1}, x) < 0 for exactly one i (x outside, and no vertex is swallowed);
 * x is then inserted between v_i and v_{i+1}.  For a 2-point "polygon" [a,b] the two directed
 * edges a->b and b->a are used, which always gives exactly one visible edge.
 * Usage: cvxenum OTAB KMAX     (counts convex k-subsets for k = 1..KMAX)
 */
#include <stdio.h>
#include <stdlib.h>

typedef unsigned long long u64;
static int n, KMAX;
static signed char *T;
#define OR(a, b, c) T[((size_t)(a) * n + (b)) * n + (c)]
static u64 cnt[64];
static int poly[64][64];   /* poly[k] = CCW polygon with k vertices at depth k */

static void rec(int k, int last) {
    /* poly[k][0..k-1] is a convex polygon in CCW order; its largest index is 'last' */
    cnt[k]++;
    if (k == KMAX) return;
    int *P = poly[k], *Q = poly[k + 1];
    for (int x = last + 1; x < n; x++) {
        int vis = 0, pos = -1;
        for (int i = 0; i < k; i++) {
            int a = P[i], b = P[(i + 1) % k];
            if (OR(a, b, x) < 0) { vis++; pos = i; if (vis > 1) break; }
        }
        if (vis != 1) continue;
        /* insert x after position pos */
        int t = 0;
        for (int i = 0; i <= pos; i++) Q[t++] = P[i];
        Q[t++] = x;
        for (int i = pos + 1; i < k; i++) Q[t++] = P[i];
        rec(k + 1, x);
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: cvxenum OTAB KMAX\n"); return 1; }
    FILE *f = fopen(argv[1], "rb");
    if (!f || fscanf(f, "%d", &n) != 1 || fgetc(f) != '\n') { fprintf(stderr, "bad table\n"); return 2; }
    KMAX = atoi(argv[2]);
    size_t N = (size_t)n * n * n;
    T = malloc(N);
    if (fread(T, 1, N, f) != N) { fprintf(stderr, "short\n"); return 2; }
    fclose(f);
    for (int a = 0; a < n; a++) {
        cnt[1]++;
        if (KMAX < 2) continue;
        for (int b = a + 1; b < n; b++) {
            poly[2][0] = a; poly[2][1] = b;
            rec(2, b);
        }
    }
    for (int k = 3; k <= KMAX; k++) printf("enum convex %2d-subsets: %llu\n", k, cnt[k]);
    fflush(stdout);
    return 0;
}
