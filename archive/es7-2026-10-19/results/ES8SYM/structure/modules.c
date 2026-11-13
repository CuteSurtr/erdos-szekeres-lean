/* Line-modules of an order type (2026-11-01).
 *
 * C subset of S is a LINE-MODULE if no line through two points of S \ C separates two points of C.
 * Nontrivial: 2 <= |C| <= n-2.  Every cluster of an (X,Y)-blow-up in the sense of Baek-Balko (SoCG 2025,
 * Definition 13) is a line-module (the triple-orientation condition handles lines through two other clusters,
 * the "almost vertical" condition handles lines through two points of one other cluster).
 *
 * Exact algorithm (orientation signs only).  Around q, list the 2(n-1) "items": each other point s (real item) and
 * its reflection 2q - s (ghost item), in circular order of direction.  A line q q' cuts this circle at the real and
 * the ghost item of q'.  For q not in C: no line q q' (q' not in C) separates C iff all real items of C lie in one gap
 * between consecutive items of points outside C.  In a module that gap contains no ghost of a point of C (the real
 * item of that point would lie in the antipodal gap), so around any outside q1 the module is a run of consecutive
 * real items.  We enumerate q1 and all such runs of length 2..n-2 and test each run around every outside point.
 * Input: OT1 table (orient.py).  n <= 64.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int n;
static signed char *T;
#define O(a,b,c) T[((a)*n+(b))*n+(c)]
/* full circular order (mod 2 pi) around q of the 2(n-1) items: real point s (code 2s) and ghost 2q-s (code 2s+1) */
static int seq[64][128];
static int cq, cr;
static int sgn_item(int q, int a, int b) { /* orient(q, item a, item b) */
    int s = O(q, a >> 1, b >> 1);
    if ((a & 1) ^ (b & 1)) s = -s;
    return s;
}
static int half(int x) { /* +1: angle in (0,pi), -1: (pi,2pi), 0: r itself, 2: ghost of r */
    if ((x >> 1) == cr) return (x & 1) ? 2 : 0;
    int s = O(cq, cr, x >> 1);
    return (x & 1) ? -s : s;
}
static int rank_half(int h) { return h == 0 ? 0 : h == 1 ? 1 : h == 2 ? 2 : 3; }
static int cmpf(const void *u, const void *v) {
    int a = *(const int *)u, b = *(const int *)v;
    if (a == b) return 0;
    int ha = rank_half(half(a)), hb = rank_half(half(b));
    if (ha != hb) return ha < hb ? -1 : 1;
    return sgn_item(cq, a, b) > 0 ? -1 : 1;
}
/* C (bitmask) unseparated by every line q q', q' outside C, iff all real items of C lie in ONE gap between
   consecutive cut items (real or ghost items of points outside C other than q). Requires >= 1 such point. */
static int ok_around(int q, uint64_t C) {
    int m = 2 * (n - 1), first = -1;
    for (int i = 0; i < m; i++) { int s = seq[q][i] >> 1; if (!((C >> s) & 1)) { first = i; break; } }
    if (first < 0) return 1;
    int gaps = 0, in_gap_has_c = 0;
    for (int t = 1; t <= m; t++) {
        int x = seq[q][(first + t) % m], s = x >> 1;
        if (!((C >> s) & 1)) { if (in_gap_has_c) gaps++; in_gap_has_c = 0; }
        else if (!(x & 1)) in_gap_has_c = 1;
    }
    return gaps <= 1;
}
static int cmpu(const void *u, const void *v) {
    uint64_t a = *(const uint64_t *)u, b = *(const uint64_t *)v;
    return a < b ? -1 : a > b;
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "rb");
    if (!f || fscanf(f, "OT1 %d", &n) != 1) { fprintf(stderr, "bad input\n"); return 1; }
    fgetc(f);
    if (n > 64) { fprintf(stderr, "n>64\n"); return 1; }
    T = malloc((size_t)n * n * n);
    if (fread(T, 1, (size_t)n * n * n, f) != (size_t)n * n * n) return 1;
    fclose(f);
    for (int q = 0; q < n; q++) {
        int m = 0;
        for (int s = 0; s < n; s++) if (s != q) { seq[q][m++] = 2 * s; seq[q][m++] = 2 * s + 1; }
        cq = q; cr = seq[q][0] >> 1;
        qsort(seq[q], m, sizeof(int), cmpf);
        for (int i = 0; i < m; i++) for (int j = i + 1; j < m; j++) {
            int a = seq[q][i], b = seq[q][j];
            if (cmpf(&a, &b) != -1) { fprintf(stderr, "order check failed q=%d\n", q); return 3; }
        }
        /* antipodal sanity: item x and its ghost are exactly n-1 positions apart */
        int pos[128];
        for (int i = 0; i < m; i++) pos[seq[q][i]] = i;
        for (int s = 0; s < n; s++) if (s != q) {
            int d = (pos[2 * s + 1] - pos[2 * s] + m) % m;
            if (d != n - 1) { fprintf(stderr, "antipodal check failed q=%d s=%d d=%d\n", q, s, d); return 4; }
        }
    }
    size_t cap = 1 << 20, cnt = 0;
    uint64_t *found = malloc(cap * sizeof(uint64_t));
    int m2 = 2 * (n - 1);
    long cand = 0;
    for (int q1 = 0; q1 < n; q1++) {
        for (int a = 0; a < m2; a++) {
            uint64_t I = 0;
            for (int L = 1; L <= n - 2; L++) {
                int x = seq[q1][(a + L - 1) % m2];
                if (x & 1) break;            /* runs of real items only */
                I |= (uint64_t)1 << (x >> 1);
                if (L < 2) continue;
                cand++;
                int ok = 1;
                for (int q = 0; q < n && ok; q++) {
                    if ((I >> q) & 1) continue;
                    if (!ok_around(q, I)) ok = 0;
                }
                if (ok) {
                    if (cnt == cap) { cap *= 2; found = realloc(found, cap * sizeof(uint64_t)); }
                    found[cnt++] = I;
                }
            }
        }
    }
    fprintf(stderr, "candidates tested: %ld\n", cand);
    qsort(found, cnt, sizeof(uint64_t), cmpu);
    size_t u = 0;
    for (size_t i = 0; i < cnt; i++) if (i == 0 || found[i] != found[i - 1]) found[u++] = found[i];
    int hist[65] = {0};
    for (size_t i = 0; i < u; i++) hist[__builtin_popcountll(found[i])]++;
    printf("n=%d nontrivial_line_modules=%zu\nsize_histogram:", n, u);
    for (int s = 2; s <= n - 2; s++) if (hist[s]) printf(" %d:%d", s, hist[s]);
    printf("\n");
    int show = argc > 2 ? atoi(argv[2]) : 40;
    for (size_t i = 0; i < u && (int)i < show; i++) {
        printf("module %zu (size %d):", i, __builtin_popcountll(found[i]));
        for (int s = 0; s < n; s++) if ((found[i] >> s) & 1) printf(" %d", s);
        printf("\n");
    }
    return 0;
}
