/* maxconv_b.c -- second, independent exact method (method B): cap + cup decomposition.
 *
 * Arithmetic: GNU MP (arbitrary precision), no size limit on the coordinates.
 * Order: points sorted lexicographically by (x, y).  This is the x-order of the sheared copy
 * (x + eps*y, y) for every small eps > 0; the shear preserves all orientations, so the copy has the same
 * convex subsets and distinct abscissae.
 * Fact used (Lemma 2 of the notes): a set with distinct abscissae, first point a and last point b, is in convex
 * position iff it is the union of a cap from a to b and a cup from a to b (sharing only a and b).  Conversely
 * every cap from a to b and every cup from a to b together form a set in convex position.  Hence
 *      largest convex subset = max_{a<b} ( CAP(a,b) + CUP(a,b) - 2 ),
 * CAP(a,b) / CUP(a,b) = longest cap / cup with first point a and last point b, computed by the DP
 *      L[h][i] = longest cap from a ending with (h, i);  L[a][i] = 2;
 *      L[h][i] = 1 + max { L[g][h] : a <= g < h, orient(g,h,i) < 0 }  (cup: > 0).
 * Cost O(n^4/24) table look-ups; orientation signs precomputed exactly (O(n^3/6) GMP evaluations).
 * Also reports the longest cap and the longest cup of the whole set (in this x-order) and the number of
 * collinear triples.
 * Usage: maxconv_b FILE
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <gmp.h>

static int n;
static mpz_t *PX, *PY;

typedef struct { mpz_t x, y; } MP;

static int cmp_mp(const void *a, const void *b) {
    const MP *p = a, *q = b;
    int c = mpz_cmp(p->x, q->x);
    if (c) return c;
    return mpz_cmp(p->y, q->y);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s FILE\n", argv[0]); return 2; }
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror(argv[1]); return 2; }
    int cap = 1024;
    MP *pts = malloc(sizeof(MP) * cap);
    char line[4096], bx[2048], by[2048];
    n = 0;
    while (fgets(line, sizeof line, f)) {
        char *s = line;
        while (*s == ' ' || *s == '\t') s++;
        if (*s == '#' || *s == '\n' || *s == 0) continue;
        if (sscanf(s, "%2047s %2047s", bx, by) != 2) { fprintf(stderr, "bad line\n"); return 2; }
        if (n == cap) { cap *= 2; pts = realloc(pts, sizeof(MP) * cap); }
        mpz_init_set_str(pts[n].x, bx, 10);
        mpz_init_set_str(pts[n].y, by, 10);
        n++;
    }
    fclose(f);
    qsort(pts, n, sizeof(MP), cmp_mp);
    for (int i = 0; i + 1 < n; i++)
        if (!mpz_cmp(pts[i].x, pts[i + 1].x) && !mpz_cmp(pts[i].y, pts[i + 1].y)) {
            printf("duplicate point\n"); return 1;
        }
    PX = malloc(sizeof(mpz_t) * n); PY = malloc(sizeof(mpz_t) * n);
    for (int i = 0; i < n; i++) { mpz_init_set(PX[i], pts[i].x); mpz_init_set(PY[i], pts[i].y); }

    /* orientation signs: O[(i,j)][h] = sign orient(P_h, P_i, P_j) for h < i < j.
       offset of pair (i,j): off[i][j], contiguous array of length i. */
    long long total = 0;
    long long *off = malloc(sizeof(long long) * (size_t)n * n);
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) { off[(size_t)i * n + j] = total; total += i; }
    signed char *O = malloc(total > 0 ? total : 1);
    if (!O) { fprintf(stderr, "out of memory\n"); return 2; }
    mpz_t t1, t2, a1, a2, b1, b2;
    mpz_inits(t1, t2, a1, a2, b1, b2, NULL);
    long long coll = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {
            signed char *row = O + off[(size_t)i * n + j];
            for (int h = 0; h < i; h++) {
                /* orient(h,i,j) = (xi-xh)(yj-yh) - (yi-yh)(xj-xh) */
                mpz_sub(a1, PX[i], PX[h]); mpz_sub(b1, PY[j], PY[h]);
                mpz_sub(a2, PY[i], PY[h]); mpz_sub(b2, PX[j], PX[h]);
                mpz_mul(t1, a1, b1); mpz_mul(t2, a2, b2);
                int c = mpz_cmp(t1, t2);
                row[h] = (c > 0) ? 1 : (c < 0 ? -1 : 0);
                if (c == 0) coll++;
            }
        }
    printf("file %s: n = %d, collinear triples = %lld\n", argv[1], n, coll);
    if (coll) { printf("NOT IN GENERAL POSITION\n"); return 1; }

    /* DP */
    short *CA = malloc(sizeof(short) * (size_t)n * n);   /* CA[i*n+h] = longest cap from a ending (h,i), 0 = none */
    short *CU = malloc(sizeof(short) * (size_t)n * n);
    int best = (n >= 2) ? 2 : n, ba = -1, bb = -1, bcap = 0, bcup = 0;
    int longcap = (n >= 2) ? 2 : n, longcup = longcap;
    for (int a = 0; a < n; a++) {
        for (int i = a + 1; i < n; i++) {
            short *rowA = CA + (size_t)i * n, *rowU = CU + (size_t)i * n;
            rowA[a] = 2; rowU[a] = 2;
            for (int h = a + 1; h < i; h++) {
                const signed char *o = O + off[(size_t)h * n + i];   /* o[g] = sign orient(g,h,i) */
                const short *pA = CA + (size_t)h * n, *pU = CU + (size_t)h * n;
                short mA = 0, mU = 0;
                for (int g = a; g < h; g++) {
                    if (o[g] < 0) { if (pA[g] > mA) mA = pA[g]; }
                    else { if (pU[g] > mU) mU = pU[g]; }
                }
                rowA[h] = mA ? mA + 1 : 0;
                rowU[h] = mU ? mU + 1 : 0;
            }
            int cmax = 0, umax = 0;
            for (int h = a; h < i; h++) {
                if (rowA[h] > cmax) cmax = rowA[h];
                if (rowU[h] > umax) umax = rowU[h];
            }
            if (cmax > longcap) longcap = cmax;
            if (umax > longcup) longcup = umax;
            if (cmax + umax - 2 > best) { best = cmax + umax - 2; ba = a; bb = i; bcap = cmax; bcup = umax; }
        }
    }
    printf("longest cap = %d, longest cup = %d (x-order = lexicographic (x,y))\n", longcap, longcup);
    printf("LARGEST SUBSET IN CONVEX POSITION (method B, cap+cup DP, GMP): %d", best);
    if (ba >= 0) {
        gmp_printf("   [attained with first point (%Zd,%Zd), last point (%Zd,%Zd), cap %d + cup %d]",
                   PX[ba], PY[ba], PX[bb], PY[bb], bcap, bcup);
    }
    printf("\n");
    return 0;
}
