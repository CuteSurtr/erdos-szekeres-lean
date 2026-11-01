/* maxconv_a.c -- exact verification of a planar integer point set (method A).
 *
 * Input: file with one "x y" (decimal integers, |x|,|y| < 2^61) per line; lines starting with '#' ignored.
 * Checks (all exact, 128-bit integer arithmetic; the coordinate bound guarantees no overflow:
 *   differences < 2^62, products < 2^124, cross products < 2^125):
 *   - all points distinct;
 *   - general position: orient(p,q,r) != 0 for all C(n,3) triples (explicit triple loop);
 *   - mirror symmetry under (x,y) -> (x,-y) (reports yes/no and the number of points on y = 0);
 *   - the largest subset in convex position, by the angular edge-sorted dynamic program:
 *       sort all n(n-1) directed edges by direction angle in [0, 2pi) (exact comparisons);
 *       for each anchor p (= lowest vertex in (y,x)-lexicographic order) keep best[v] = largest number of
 *       vertices of a chain p -> ... -> v whose edge directions strictly increase; scanning the edges in
 *       angular order, edge (u,v) gives best[v] >= best[u] + 1, and an edge (u,p) closes a convex polygon
 *       with best[u] vertices.  O(n^2) per anchor, O(n^3) in total.
 *     A witness polygon of maximum size is reconstructed and re-checked independently (every edge has all
 *     other witness vertices strictly on its left).
 * Usage: maxconv_a FILE [-q]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef __int128 i128;
typedef long long ll;

static int n;
static ll *X, *Y;

static int parse_ll(const char **s, ll *out) {
    const char *p = *s;
    while (*p == ' ' || *p == '\t' || *p == ',') p++;
    int neg = 0;
    if (*p == '-') { neg = 1; p++; } else if (*p == '+') p++;
    if (*p < '0' || *p > '9') return 0;
    i128 v = 0;
    while (*p >= '0' && *p <= '9') {
        v = v * 10 + (*p - '0');
        if (v >= ((i128)1 << 61)) { fprintf(stderr, "coordinate too large\n"); exit(2); }
        p++;
    }
    *out = (ll)(neg ? -v : v);
    *s = p;
    return 1;
}

static void read_points(const char *fn) {
    FILE *f = fopen(fn, "r");
    if (!f) { perror(fn); exit(2); }
    int cap = 1024;
    X = malloc(sizeof(ll) * cap); Y = malloc(sizeof(ll) * cap);
    char line[512];
    n = 0;
    while (fgets(line, sizeof line, f)) {
        const char *s = line;
        while (*s == ' ' || *s == '\t') s++;
        if (*s == '#' || *s == '\n' || *s == 0) continue;
        ll a, b;
        if (!parse_ll(&s, &a) || !parse_ll(&s, &b)) { fprintf(stderr, "bad line: %s", line); exit(2); }
        if (n == cap) { cap *= 2; X = realloc(X, sizeof(ll) * cap); Y = realloc(Y, sizeof(ll) * cap); }
        X[n] = a; Y[n] = b; n++;
    }
    fclose(f);
}

static inline i128 orient3(int a, int b, int c) {
    return (i128)(X[b] - X[a]) * (Y[c] - Y[a]) - (i128)(Y[b] - Y[a]) * (X[c] - X[a]);
}

/* ---- edges: directed edge u->v encoded as e = u*n + v; differences computed on the fly ---- */
static inline int half_of(ll dx, ll dy) { return (dy > 0 || (dy == 0 && dx > 0)) ? 0 : 1; }

static int cmp_edge(const void *a, const void *b) {
    unsigned e = *(const unsigned *)a, f = *(const unsigned *)b;
    int eu = e / n, ev = e % n, fu = f / n, fv = f % n;
    ll edx = X[ev] - X[eu], edy = Y[ev] - Y[eu], fdx = X[fv] - X[fu], fdy = Y[fv] - Y[fu];
    int he = half_of(edx, edy), hf = half_of(fdx, fdy);
    if (he != hf) return he - hf;
    i128 c = (i128)edx * fdy - (i128)edy * fdx;
    if (c > 0) return -1;
    if (c < 0) return 1;
    return (e < f) ? -1 : (e > f);
}

static int lower(int a, int b) { /* a strictly lower than b in (y, x) lexicographic order */
    return (Y[a] < Y[b]) || (Y[a] == Y[b] && X[a] < X[b]);
}

typedef struct { ll x, y; } P2;
static int cmp_p2(const void *a, const void *b) {
    const P2 *p = a, *q = b;
    if (p->x != q->x) return p->x < q->x ? -1 : 1;
    if (p->y != q->y) return p->y < q->y ? -1 : 1;
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s FILE [-q]\n", argv[0]); return 2; }
    int quiet = (argc > 2 && !strcmp(argv[2], "-q"));
    read_points(argv[1]);
    printf("file %s: n = %d\n", argv[1], n);

    /* distinctness and mirror symmetry */
    P2 *srt = malloc(sizeof(P2) * n);
    for (int i = 0; i < n; i++) { srt[i].x = X[i]; srt[i].y = Y[i]; }
    qsort(srt, n, sizeof(P2), cmp_p2);
    int dup = 0;
    for (int i = 0; i + 1 < n; i++) if (srt[i].x == srt[i + 1].x && srt[i].y == srt[i + 1].y) dup++;
    printf("duplicate points: %d\n", dup);
    int sym = 1, axis = 0;
    for (int i = 0; i < n; i++) {
        P2 q = { X[i], -Y[i] };
        if (Y[i] == 0) axis++;
        if (!bsearch(&q, srt, n, sizeof(P2), cmp_p2)) sym = 0;
    }
    printf("mirror symmetric under (x,y)->(x,-y): %s; points on the axis y=0: %d\n", sym ? "YES" : "NO", axis);

    /* general position */
    long long coll = 0;
    for (int a = 0; a < n; a++)
        for (int b = a + 1; b < n; b++)
            for (int c = b + 1; c < n; c++)
                if (orient3(a, b, c) == 0) {
                    if (coll < 5) printf("  collinear: %d %d %d\n", a, b, c);
                    coll++;
                }
    printf("collinear triples: %lld (checked all %lld triples)\n", coll, (long long)n * (n - 1) * (n - 2) / 6);
    if (dup || coll) { printf("NOT IN GENERAL POSITION -- convex DP skipped\n"); return 1; }

    /* edges */
    if ((long long)n * n >= 4294967295LL) { fprintf(stderr, "n too large\n"); return 2; }
    long long m = (long long)n * (n - 1);
    unsigned *idx = malloc(sizeof(unsigned) * m);
    long long e = 0;
    for (int u = 0; u < n; u++)
        for (int v = 0; v < n; v++) if (u != v) idx[e++] = (unsigned)u * n + v;
    qsort(idx, m, sizeof(unsigned), cmp_edge);
    /* sanity: the sorted sequence is non-decreasing in angle (adjacent pairs) */
    long long bad = 0;
    for (long long t = 0; t + 1 < m; t++) if (cmp_edge(&idx[t], &idx[t + 1]) > 0) bad++;
    if (bad) { printf("edge sort check failed: %lld\n", bad); return 3; }
    int *SU = malloc(sizeof(int) * m), *SV = malloc(sizeof(int) * m);
    for (long long t = 0; t < m; t++) { SU[t] = idx[t] / n; SV[t] = idx[t] % n; }
    free(idx);

    int *best = malloc(sizeof(int) * n);
    unsigned char *act = malloc(n);
    int ans = (n >= 1) ? 1 : 0, ansp = -1;
    long long *hist = calloc(n + 2, sizeof(long long));
    for (int p = 0; p < n; p++) {
        for (int v = 0; v < n; v++) { act[v] = (v == p) || lower(p, v); best[v] = -1; }
        best[p] = 1;
        int loc = 1;
        for (long long t = 0; t < m; t++) {
            int u = SU[t], v = SV[t];
            if (!act[u] || !act[v]) continue;
            int bu = best[u];
            if (bu < 0) continue;
            if (v == p) { if (bu > loc) loc = bu; }
            else if (bu + 1 > best[v]) best[v] = bu + 1;
        }
        hist[loc]++;
        if (loc > ans) { ans = loc; ansp = p; }
    }
    printf("LARGEST SUBSET IN CONVEX POSITION (method A, angular DP): %d\n", ans);
    if (!quiet) {
        printf("distribution over anchors of the largest convex polygon with that lowest vertex:");
        for (int s = 0; s <= n + 1; s++) if (hist[s]) printf(" [%d]:%lld", s, hist[s]);
        printf("\n");
    }

    /* witness reconstruction for anchor ansp */
    if (ansp >= 0) {
        int p = ansp;
        int *rec_v = malloc(sizeof(int) * (m + 1)), *rec_prev = malloc(sizeof(int) * (m + 1));
        int *cur = malloc(sizeof(int) * n);
        int nrec = 0, closing = -1, loc = 1;
        for (int v = 0; v < n; v++) { act[v] = (v == p) || lower(p, v); best[v] = -1; cur[v] = -1; }
        best[p] = 1; rec_v[0] = p; rec_prev[0] = -1; cur[p] = 0; nrec = 1;
        for (long long t = 0; t < m; t++) {
            int u = SU[t], v = SV[t];
            if (!act[u] || !act[v]) continue;
            int bu = best[u];
            if (bu < 0) continue;
            if (v == p) { if (bu > loc) { loc = bu; closing = cur[u]; } }
            else if (bu + 1 > best[v]) {
                best[v] = bu + 1; rec_v[nrec] = v; rec_prev[nrec] = cur[u]; cur[v] = nrec; nrec++;
            }
        }
        int w[4096], nw = 0;
        for (int r = closing; r >= 0; r = rec_prev[r]) w[nw++] = rec_v[r];
        /* reverse to counterclockwise order starting at p */
        for (int i = 0; i < nw / 2; i++) { int tmp = w[i]; w[i] = w[nw - 1 - i]; w[nw - 1 - i] = tmp; }
        int ok = (nw == loc);
        for (int i = 0; i < nw; i++) {
            int a = w[i], b = w[(i + 1) % nw];
            for (int j = 0; j < nw; j++) if (j != i && j != (i + 1) % nw)
                if (orient3(a, b, w[j]) <= 0) ok = 0;
        }
        for (int i = 0; i < nw; i++) for (int j = i + 1; j < nw; j++) if (w[i] == w[j]) ok = 0;
        printf("witness polygon (%d vertices, counterclockwise, 0-based input line indices):", nw);
        for (int i = 0; i < nw; i++) printf(" %d", w[i]);
        printf("\nwitness coordinates:");
        for (int i = 0; i < nw; i++) printf(" (%lld,%lld)", X[w[i]], Y[w[i]]);
        printf("\nwitness re-check (all other vertices strictly left of every edge, distinct): %s\n",
               ok ? "OK" : "FAILED");
        if (!ok) return 4;
    }
    return 0;
}
