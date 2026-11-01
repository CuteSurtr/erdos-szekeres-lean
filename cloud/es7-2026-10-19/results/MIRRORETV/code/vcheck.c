/* vcheck.c -- independent exact checker (written from scratch for an independent review).
 *
 * Input: text file, '#' lines ignored, other lines "x y" or "x y b" (b = block index) [--bxy: "b x y"].
 * Coordinates are parsed into __int128; we require |x| < 2^30 and |y| < 2^90 so that every orientation
 * determinant (products of differences) fits in a signed 128-bit integer with margin.
 *
 * Checks:
 *   distinct points; general position (all triples, orient != 0);
 *   mirror symmetry  (--mir y : (x,y)->(x,-y) ;  --mir x : (x,y)->(-x,y) ; default none);
 *   block hypotheses of the block lemma (if blocks given, with --k K): per block distinct x, longest cap <= b+1,
 *       longest cup <= K-1-b, (A) for all i<j, (C) for all h<i<j;
 *   largest convex subset, by two different algorithms:
 *       ALG1: lexicographic-order cap+cup dynamic program, O(n^3) (two-pointer over slope-sorted edges);
 *       ALG2: angular dynamic program around the lowest vertex, O(n^4)  (optional, --alg2);
 *   witness polygon from ALG1 re-checked by an O(w^4) triangle-containment test.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

typedef __int128 i128;
typedef struct { i128 x, y; int b; } P;

static P *pt; static int n;

static i128 parse128(const char **s) {
    while (**s && isspace((unsigned char)**s)) (*s)++;
    int neg = 0; if (**s == '-') { neg = 1; (*s)++; } else if (**s == '+') (*s)++;
    if (!isdigit((unsigned char)**s)) { fprintf(stderr, "parse error\n"); exit(2); }
    i128 v = 0; int digits = 0;
    while (isdigit((unsigned char)**s)) { v = v * 10 + (**s - '0'); (*s)++; if (++digits > 36) { fprintf(stderr, "number too long\n"); exit(2);} }
    return neg ? -v : v;
}
static i128 ab(i128 v) { return v < 0 ? -v : v; }
static void pr128(i128 v, char *buf) {
    char t[64]; int k = 0, neg = v < 0; unsigned __int128 u = neg ? (unsigned __int128)(-v) : (unsigned __int128)v;
    if (u == 0) t[k++] = '0';
    while (u) { t[k++] = '0' + (int)(u % 10); u /= 10; }
    int m = 0; if (neg) buf[m++] = '-';
    while (k) buf[m++] = t[--k];
    buf[m] = 0;
}
static inline int sgn(i128 v) { return (v > 0) - (v < 0); }
static inline i128 orient(const P *a, const P *b, const P *c) {
    return (b->x - a->x) * (c->y - a->y) - (b->y - a->y) * (c->x - a->x);
}
static inline i128 cross(i128 ux, i128 uy, i128 vx, i128 vy) { return ux * vy - uy * vx; }

static int lexcmp(const void *A, const void *B) {
    const P *a = A, *b = B;
    if (a->x != b->x) return a->x < b->x ? -1 : 1;
    if (a->y != b->y) return a->y < b->y ? -1 : 1;
    return 0;
}

/* ---------- ALG1: cap+cup DP in lexicographic order ---------- */
/* sort context */
static int g_m;  /* middle index */
static int cmp_in_desc(const void *A, const void *B) { /* h before h' iff slope(h->m) > slope(h'->m) */
    int h1 = *(const int *)A, h2 = *(const int *)B; const P *m = &pt[g_m];
    i128 c = cross(m->x - pt[h2].x, m->y - pt[h2].y, m->x - pt[h1].x, m->y - pt[h1].y); /* >0 iff slope(h1)>slope(h2) */
    return c > 0 ? -1 : (c < 0 ? 1 : 0);
}
static int cmp_out_desc(const void *A, const void *B) { /* j before j' iff slope(m->j) > slope(m->j') */
    int j1 = *(const int *)A, j2 = *(const int *)B; const P *m = &pt[g_m];
    i128 c = cross(pt[j2].x - m->x, pt[j2].y - m->y, pt[j1].x - m->x, pt[j1].y - m->y); /* >0 iff slope(j1)>slope(j2) */
    return c > 0 ? -1 : (c < 0 ? 1 : 0);
}

static int **IN, **OUT; static int *nin, *nout;
static short *F, *Gc; static int *predF, *predG;  /* n*n */

/* compute chain DP from start a. type=+1 cap (orient<0 turns), type=-1 cup (orient>0 turns).
 * T[i*n+j] = longest chain from a with last edge (i,j), 0 = undefined. pred optional. */
static void chain_dp(int a, int type, short *T, int *pred) {
    for (int j = a + 1; j < n; j++) { T[a * n + j] = 2; if (pred) pred[a * n + j] = -1; }
    for (int m = a + 1; m < n; m++) {
        for (int j = m + 1; j < n; j++) T[m * n + j] = 0;
        int *in = IN[m], ni = nin[m], *out = OUT[m], no = nout[m];
        if (type == 1) {
            /* in: slope desc ; out: slope desc ; admit h while slope(h,m) > slope(m,j) i.e. orient(h,m,j)<0 */
            int p = 0, best = 0, barg = -1;
            for (int q = 0; q < no; q++) {
                int j = out[q];
                while (p < ni && orient(&pt[in[p]], &pt[m], &pt[j]) < 0) {
                    int h = in[p];
                    if (h >= a && T[h * n + m] > best) { best = T[h * n + m]; barg = h; }
                    p++;
                }
                if (best > 0) { T[m * n + j] = best + 1; if (pred) pred[m * n + j] = barg; }
            }
        } else {
            /* cup: iterate in reverse (slope ascending) ; admit h while orient(h,m,j)>0 */
            int p = ni - 1, best = 0, barg = -1;
            for (int q = no - 1; q >= 0; q--) {
                int j = out[q];
                while (p >= 0 && orient(&pt[in[p]], &pt[m], &pt[j]) > 0) {
                    int h = in[p];
                    if (h >= a && T[h * n + m] > best) { best = T[h * n + m]; barg = h; }
                    p--;
                }
                if (best > 0) { T[m * n + j] = best + 1; if (pred) pred[m * n + j] = barg; }
            }
        }
    }
}

static int alg1(int *wit, int *wlen) {
    IN = malloc(n * sizeof(int *)); OUT = malloc(n * sizeof(int *));
    nin = calloc(n, sizeof(int)); nout = calloc(n, sizeof(int));
    for (int m = 0; m < n; m++) {
        IN[m] = malloc((m + 1) * sizeof(int)); OUT[m] = malloc((n - m + 1) * sizeof(int));
        for (int h = 0; h < m; h++) IN[m][nin[m]++] = h;
        for (int j = m + 1; j < n; j++) OUT[m][nout[m]++] = j;
        g_m = m;
        qsort(IN[m], nin[m], sizeof(int), cmp_in_desc);
        qsort(OUT[m], nout[m], sizeof(int), cmp_out_desc);
    }
    F = malloc((size_t)n * n * sizeof(short)); Gc = malloc((size_t)n * n * sizeof(short));
    int best = n >= 2 ? 2 : n, ba = -1, bb = -1;
    for (int a = 0; a < n; a++) {
        chain_dp(a, 1, F, NULL); chain_dp(a, -1, Gc, NULL);
        for (int b = a + 1; b < n; b++) {
            int cl = 0, ul = 0;
            for (int m = a; m < b; m++) { if (F[m * n + b] > cl) cl = F[m * n + b]; if (Gc[m * n + b] > ul) ul = Gc[m * n + b]; }
            if (cl + ul - 2 > best) { best = cl + ul - 2; ba = a; bb = b; }
        }
    }
    *wlen = 0;
    if (ba >= 0) { /* reconstruct */
        predF = malloc((size_t)n * n * sizeof(int)); predG = malloc((size_t)n * n * sizeof(int));
        chain_dp(ba, 1, F, predF); chain_dp(ba, -1, Gc, predG);
        int mc = -1, mu_ = -1, cl = 0, ul = 0;
        for (int m = ba; m < bb; m++) { if (F[m * n + bb] > cl) { cl = F[m * n + bb]; mc = m; } if (Gc[m * n + bb] > ul) { ul = Gc[m * n + bb]; mu_ = m; } }
        /* cap chain */
        int i = mc, j = bb; wit[(*wlen)++] = bb;
        while (i >= 0) { wit[(*wlen)++] = i; int h = predF[i * n + j]; j = i; i = h; }
        i = mu_; j = bb;
        while (i >= 0) { int h = predG[i * n + j]; if (i != ba) wit[(*wlen)++] = i; j = i; i = h; }
        free(predF); free(predG);
    }
    for (int m = 0; m < n; m++) { free(IN[m]); free(OUT[m]); }
    free(IN); free(OUT); free(nin); free(nout); free(F); free(Gc);
    return best;
}

/* convex position test by triangle containment (general position assumed) */
static int in_triangle(const P *a, const P *b, const P *c, const P *p) {
    int s1 = sgn(orient(a, b, p)), s2 = sgn(orient(b, c, p)), s3 = sgn(orient(c, a, p));
    return (s1 == s2 && s2 == s3 && s1 != 0);
}
static int convex_position(int *w, int L) {
    for (int t = 0; t < L; t++)
        for (int a = 0; a < L; a++) for (int b = a + 1; b < L; b++) for (int c = b + 1; c < L; c++) {
            if (a == t || b == t || c == t) continue;
            if (in_triangle(&pt[w[a]], &pt[w[b]], &pt[w[c]], &pt[w[t]])) return 0;
        }
    return 1;
}

/* ---------- ALG2: angular DP around the lowest vertex ---------- */
static const P *g_anchor;
static int cmp_ang(const void *A, const void *B) {
    const P *p = *(P * const *)A, *q = *(P * const *)B;
    i128 c = cross(p->x - g_anchor->x, p->y - g_anchor->y, q->x - g_anchor->x, q->y - g_anchor->y);
    return c > 0 ? -1 : (c < 0 ? 1 : 0);
}
static int alg2(void) {
    int best = n >= 2 ? 2 : n;
    P **cand = malloc(n * sizeof(P *));
    short *f = malloc((size_t)n * n * sizeof(short));
    for (int a = 0; a < n; a++) {
        int m = 0; const P *A = &pt[a];
        for (int i = 0; i < n; i++) {
            if (i == a) continue;
            if (pt[i].y > A->y || (pt[i].y == A->y && pt[i].x > A->x)) cand[m++] = &pt[i];
        }
        if (m + 1 <= best) continue;
        g_anchor = A; qsort(cand, m, sizeof(P *), cmp_ang);
        for (int j = 0; j < m; j++) for (int i = 0; i < j; i++) {
            int v = 3;
            for (int h = 0; h < i; h++) if (f[h * n + i] + 1 > v && orient(cand[h], cand[i], cand[j]) > 0) v = f[h * n + i] + 1;
            f[i * n + j] = v;
            if (v > best && orient(cand[i], cand[j], A) > 0) best = v;
        }
    }
    free(cand); free(f);
    return best;
}

/* ---------- block hypotheses ---------- */
static int longest_chain_block(int *idx, int m, int type) { /* idx sorted by x; type +1 cap, -1 cup */
    if (m <= 2) return m;
    int best = 2; short *T = calloc((size_t)m * m, sizeof(short));
    for (int j = 1; j < m; j++) for (int i = 0; i < j; i++) {
        int v = 2;
        for (int h = 0; h < i; h++) {
            i128 o = orient(&pt[idx[h]], &pt[idx[i]], &pt[idx[j]]);
            if ((type == 1 ? o < 0 : o > 0) && T[h * m + i] + 1 > v) v = T[h * m + i] + 1;
        }
        T[i * m + j] = v; if (v > best) best = v;
    }
    free(T); return best;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: vcheck FILE [--mir x|y] [--k K] [--alg2] [--bxy] [--noalg1]\n"); return 2; }
    char mir = 0; int K = 0, doalg2 = 0, bxy = 0, doalg1 = 1;
    for (int i = 2; i < argc; i++) {
        if (!strcmp(argv[i], "--mir") && i + 1 < argc) mir = argv[++i][0];
        else if (!strcmp(argv[i], "--k") && i + 1 < argc) K = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--alg2")) doalg2 = 1;
        else if (!strcmp(argv[i], "--noalg1")) doalg1 = 0;
        else if (!strcmp(argv[i], "--bxy")) bxy = 1;
    }
    FILE *fp = fopen(argv[1], "r"); if (!fp) { perror("open"); return 2; }
    int cap = 1024; pt = malloc(cap * sizeof(P)); n = 0;
    static char line[4096]; int haveb = 0;
    while (fgets(line, sizeof line, fp)) {
        const char *s = line; while (*s && isspace((unsigned char)*s)) s++;
        if (!*s || *s == '#') continue;
        if (n == cap) { cap *= 2; pt = realloc(pt, cap * sizeof(P)); }
        P q; q.b = -1;
        if (bxy) { q.b = (int)parse128(&s); q.x = parse128(&s); q.y = parse128(&s); haveb = 1; }
        else {
            q.x = parse128(&s); q.y = parse128(&s);
            while (*s && isspace((unsigned char)*s)) s++;
            if (*s && (isdigit((unsigned char)*s) || *s == '-')) { q.b = (int)parse128(&s); haveb = 1; }
        }
        pt[n++] = q;
    }
    fclose(fp);
    i128 LX = (i128)1 << 30, LY = (i128)1 << 90;
    for (int i = 0; i < n; i++) if (ab(pt[i].x) >= LX || ab(pt[i].y) >= LY) { printf("FAIL bounds exceeded at point %d\n", i); return 1; }
    printf("file=%s n=%d\n", argv[1], n);
    /* sort lexicographically (blocks travel with points) */
    qsort(pt, n, sizeof(P), lexcmp);
    for (int i = 1; i < n; i++) if (lexcmp(&pt[i - 1], &pt[i]) == 0) { printf("FAIL duplicate point\n"); return 1; }
    printf("distinct: OK\n");
    /* general position */
    long long trip = 0;
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) for (int k = j + 1; k < n; k++) {
        trip++;
        if (orient(&pt[i], &pt[j], &pt[k]) == 0) { printf("FAIL collinear triple %d %d %d\n", i, j, k); return 1; }
    }
    printf("general position: OK (%lld triples)\n", trip);
    /* mirror */
    if (mir) {
        int axis = 0;
        for (int i = 0; i < n; i++) {
            P q = pt[i]; if (mir == 'y') q.y = -q.y; else q.x = -q.x;
            if (lexcmp(&q, &pt[i]) == 0) axis++;
            if (!bsearch(&q, pt, n, sizeof(P), lexcmp)) { printf("FAIL not mirror symmetric (point %d)\n", i); return 1; }
        }
        printf("mirror symmetric (%c): OK, axis points=%d\n", mir, axis);
    }
    /* blocks */
    if (haveb && K > 0) {
        int nb = 0; for (int i = 0; i < n; i++) if (pt[i].b + 1 > nb) nb = pt[i].b + 1;
        if (nb != K - 1) { printf("FAIL number of blocks %d != K-1=%d\n", nb, K - 1); return 1; }
        int **bl = malloc(nb * sizeof(int *)); int *bs = calloc(nb, sizeof(int));
        for (int b = 0; b < nb; b++) bl[b] = malloc(n * sizeof(int));
        for (int i = 0; i < n; i++) bl[pt[i].b][bs[pt[i].b]++] = i;  /* lex order within block */
        int ok = 1;
        for (int b = 0; b < nb; b++) {
            for (int t = 1; t < bs[b]; t++) if (pt[bl[b][t]].x == pt[bl[b][t - 1]].x) { printf("FAIL block %d repeated x\n", b); ok = 0; }
            int lc = longest_chain_block(bl[b], bs[b], 1), lu = longest_chain_block(bl[b], bs[b], -1);
            printf("block %2d size %4d longest cap %2d (<= %2d) longest cup %2d (<= %2d)\n", b, bs[b], lc, b + 1, lu, K - 1 - b);
            if (lc > b + 1 || lu > K - 1 - b) { printf("FAIL block bound\n"); ok = 0; }
        }
        long long cntA = 0, cntC = 0;
        for (int i = 0; i < nb; i++) for (int j = i + 1; j < nb; j++) {
            /* p,q in B_i (x_p<x_q), d in B_j: orient(p,q,d)<0 ; p,q in B_j, u in B_i: orient(p,q,u)>0 */
            for (int s = 0; s < bs[i]; s++) for (int t = s + 1; t < bs[i]; t++) for (int r = 0; r < bs[j]; r++) {
                cntA++; if (orient(&pt[bl[i][s]], &pt[bl[i][t]], &pt[bl[j][r]]) >= 0) { printf("FAIL (A1) %d %d\n", i, j); ok = 0; goto doneA; } }
            for (int s = 0; s < bs[j]; s++) for (int t = s + 1; t < bs[j]; t++) for (int r = 0; r < bs[i]; r++) {
                cntA++; if (orient(&pt[bl[j][s]], &pt[bl[j][t]], &pt[bl[i][r]]) <= 0) { printf("FAIL (A2) %d %d\n", i, j); ok = 0; goto doneA; } }
        }
    doneA:
        for (int h = 0; h < nb; h++) for (int i = h + 1; i < nb; i++) for (int j = i + 1; j < nb; j++)
            for (int s = 0; s < bs[h]; s++) for (int t = 0; t < bs[i]; t++) for (int r = 0; r < bs[j]; r++) {
                cntC++; if (orient(&pt[bl[j][r]], &pt[bl[h][s]], &pt[bl[i][t]]) >= 0) { printf("FAIL (C) %d %d %d\n", h, i, j); ok = 0; goto doneC; } }
    doneC:
        printf("block lemma hypotheses: %s ((A) tests %lld, (C) tests %lld)\n", ok ? "OK" : "FAIL", cntA, cntC);
    }
    if (doalg1) {
        int *wit = malloc((n + 2) * sizeof(int)), wl = 0;
        int b1 = alg1(wit, &wl);
        printf("ALG1 largest convex subset = %d\n", b1);
        if (wl) {
            int cp = convex_position(wit, wl);
            printf("witness (%d points, convex position %s):", wl, cp ? "OK" : "FAIL");
            char bx[64], by[64];
            for (int t = 0; t < wl; t++) { pr128(pt[wit[t]].x, bx); pr128(pt[wit[t]].y, by); printf(" (%s,%s)", bx, by); }
            printf("\n");
            if (wl != b1 || !cp) printf("FAIL witness mismatch\n");
        }
    }
    if (doalg2) printf("ALG2 largest convex subset = %d\n", alg2());
    return 0;
}
