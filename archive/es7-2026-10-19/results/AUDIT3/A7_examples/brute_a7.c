/* A7 audit: exhaustive enumeration of all k-subsets (and (k-1)-subsets) of a point set, given its exact orientation
   table (binary: int32 n, then n*n*n int8 signs, O[(a*n+b)*n+c] = sign of orient(a,b,c)).
   Each subset is tested by two different criteria:
     TRI : in convex position iff no point lies strictly inside a triangle of three others;
     WRAP: in convex position iff every point q has another point r with all remaining points strictly left of q->r.
   usage: brute_a7 ORIENT.bin k */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

static int n;
static int8_t *O;
#define OR(a, b, c) O[((size_t)(a) * n + (b)) * n + (c)]

static int conv_tri(const int *s, int k) {
    for (int t = 0; t < k; t++) {
        int q = s[t];
        for (int a = 0; a < k; a++) {
            if (a == t) continue;
            for (int b = a + 1; b < k; b++) {
                if (b == t) continue;
                for (int c = b + 1; c < k; c++) {
                    if (c == t) continue;
                    int x = s[a], y = s[b], z = s[c];
                    int o1 = OR(x, y, q), o2 = OR(y, z, q), o3 = OR(z, x, q);
                    if ((o1 > 0 && o2 > 0 && o3 > 0) || (o1 < 0 && o2 < 0 && o3 < 0)) return 0;
                }
            }
        }
    }
    return 1;
}

static int conv_wrap(const int *s, int k) {
    for (int t = 0; t < k; t++) {
        int q = s[t], ok = 0;
        for (int u = 0; u < k && !ok; u++) {
            if (u == t) continue;
            int r = s[u], all = 1;
            for (int v = 0; v < k; v++) {
                if (v == t || v == u) continue;
                if (OR(q, r, s[v]) <= 0) { all = 0; break; }
            }
            if (all) ok = 1;
        }
        if (!ok) return 0;
    }
    return 1;
}

static void run(int kk) {
    long long total = 0, ctri = 0, cwrap = 0, disagree = 0;
    int s[64];
    if (kk > n) { printf("k=%d > n\n", kk); return; }
    for (int i = 0; i < kk; i++) s[i] = i;
    int printed = 0;
    while (1) {
        total++;
        int a = conv_tri(s, kk), b = conv_wrap(s, kk);
        ctri += a; cwrap += b;
        if (a != b) disagree++;
        if (a && kk >= 7 && printed < 3) {
            printf("  convex %d-subset:", kk);
            for (int i = 0; i < kk; i++) printf(" %d", s[i]);
            printf("\n");
            printed++;
        }
        int i = kk - 1;
        while (i >= 0 && s[i] == n - kk + i) i--;
        if (i < 0) break;
        s[i]++;
        for (int j = i + 1; j < kk; j++) s[j] = s[j - 1] + 1;
    }
    printf("k=%d subsets=%lld convex_TRI=%lld convex_WRAP=%lld disagreements=%lld\n", kk, total, ctri, cwrap, disagree);
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: brute_a7 ORIENT.bin k\n"); return 2; }
    FILE *f = fopen(argv[1], "rb");
    if (!f) { perror("open"); return 2; }
    int32_t nn;
    if (fread(&nn, 4, 1, f) != 1) return 2;
    n = nn;
    size_t sz = (size_t)n * n * n;
    O = malloc(sz);
    if (fread(O, 1, sz, f) != sz) { fprintf(stderr, "short read\n"); return 2; }
    fclose(f);
    int k = atoi(argv[2]);
    /* sanity of the table: nonzero on distinct triples, alternating */
    long long bad = 0, zero = 0;
    for (int a = 0; a < n; a++)
        for (int b = 0; b < n; b++)
            for (int c = 0; c < n; c++) {
                if (a == b || b == c || a == c) continue;
                int v = OR(a, b, c);
                if (v == 0) zero++;
                if (OR(b, c, a) != v || OR(c, a, b) != v || OR(b, a, c) != -v || OR(a, c, b) != -v || OR(c, b, a) != -v) bad++;
            }
    printf("n=%d table: zero_entries_on_distinct_triples=%lld alternation_violations=%lld\n", n, zero, bad);
    run(k);
    run(k - 1);
    return 0;
}
