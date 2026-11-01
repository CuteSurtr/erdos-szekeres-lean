/* Independent line-module search by closure (written from scratch for an independent check; not derived from modules.c).
 *
 * Definition: C subset of S is a line-module if no line through two points of S\C separates two points of C.
 * Points in general position (no zero orientation for distinct indices; checked).
 *
 * Reformulation used here.  For a in S and K subset of S\{a}, call K a-closed if for every pair t != u in K, every
 * point strictly on the side of line(t,u) NOT containing a lies in K.
 *   (1) If C is a module, a in C and T = S\C, then T is a-closed (C lies on one side of each line tu, t,u in T,
 *       and a in C fixes that side; the other side has no point of C, so it is inside T).
 *   (2) If K is a-closed, |K| >= 2, then S\K is a module (each line tu, t,u in K, has all points not in K on a's
 *       side, by general position no point lies on the line).
 * cl_a(X) = smallest a-closed superset of X; computed by the obvious fixpoint (adding forced points), which never
 * adds a.  Monotone in X.
 * Detection of modules of size 2..n-5:  such a module C exists  iff  some a and some 5-set X with a notin X have
 * |cl_a(X)| <= n-2 (=> by (1), take a in C, X inside T; <= by (2)).  Search: for every a, start from cl_a({t1,t2})
 * for all pairs, and repeatedly add one point to closed sets of size <= 4.  Adding the points of a witnessing X one
 * at a time gives a chain of closed sets inside cl_a(X); the first one of size >= 5 is still <= n-2, so it is found.
 * Every a-closed K with 2 <= |K| <= 4 and |S\K| >= 2 is also reached (same argument), so all modules of size
 * n-4..n-2 are listed.
 * Mode "all" (small n validation): BFS over all a-closed sets without the size cut-off -> all modules 2..n-2.
 *
 * Input: "XT n\n" or "OT1 n\n" or "n\n" followed by n^3 signed bytes, index (i*n+j)*n+k.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
typedef unsigned __int128 u128;
#define BIT(i) (((u128)1) << (i))
static int n;
static signed char *T;
#define O(a, b, c) T[((size_t)(a) * n + (b)) * n + (c)]
static u128 Lf[128][128];
static inline int pc(u128 x) { return __builtin_popcountll((uint64_t)x) + __builtin_popcountll((uint64_t)(x >> 64)); }
static inline int ctz(u128 x) {
    uint64_t lo = (uint64_t)x;
    return lo ? __builtin_ctzll(lo) : 64 + __builtin_ctzll((uint64_t)(x >> 64));
}
static long long nclos = 0;
static u128 closure(int a, u128 K0) {
    int mem[130], cnt = 0;
    u128 K = K0, x = K0;
    nclos++;
    while (x) { mem[cnt++] = ctz(x); x &= x - 1; }
    for (int p = 0; p < cnt; p++) {
        int t = mem[p];
        for (int q = 0; q < p; q++) {
            int u = mem[q];
            u128 side = (O(u, t, a) > 0) ? Lf[t][u] : Lf[u][t];
            u128 nw = side & ~K;
            if (nw) {
                K |= nw;
                while (nw) { mem[cnt++] = ctz(nw); nw &= nw - 1; }
                if (cnt >= n - 1) return K;
            }
        }
    }
    return K;
}
/* simple open-addressing hash set of u128 */
typedef struct { u128 *v; char *used; size_t cap, cnt; } hset;
static void hinit(hset *h, size_t cap) { h->cap = cap; h->cnt = 0; h->v = calloc(cap, sizeof(u128)); h->used = calloc(cap, 1); }
static void hfree(hset *h) { free(h->v); free(h->used); }
static size_t hh(u128 x) { uint64_t a = (uint64_t)x, b = (uint64_t)(x >> 64); uint64_t z = a * 0x9E3779B97F4A7C15ULL ^ (b + 0x632BE59BD9B4E019ULL) * 0xBF58476D1CE4E5B9ULL; z ^= z >> 29; return (size_t)z; }
static int hadd(hset *h, u128 x) { /* returns 1 if newly added */
    if (2 * (h->cnt + 1) > h->cap) {
        hset g; hinit(&g, h->cap * 2);
        for (size_t i = 0; i < h->cap; i++) if (h->used[i]) hadd(&g, h->v[i]);
        hfree(h); *h = g;
    }
    size_t i = hh(x) % h->cap;
    while (h->used[i]) { if (h->v[i] == x) return 0; i = (i + 1) % h->cap; }
    h->used[i] = 1; h->v[i] = x; h->cnt++;
    return 1;
}
static int cmpu(const void *p, const void *q) { u128 a = *(const u128 *)p, b = *(const u128 *)q; return a < b ? -1 : a > b; }

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: modclose TABLE detect|all [maxprint]\n"); return 2; }
    FILE *f = fopen(argv[1], "rb");
    if (!f) return 1;
    char line[64]; if (!fgets(line, sizeof line, f)) return 1;
    char *p = line + strlen(line); while (p > line && (p[-1] == '\n' || p[-1] == ' ')) p--; *p = 0;
    char *q = strrchr(line, ' '); n = atoi(q ? q + 1 : line);
    if (n < 4 || n > 128) { fprintf(stderr, "bad n\n"); return 1; }
    T = malloc((size_t)n * n * n);
    if (fread(T, 1, (size_t)n * n * n, f) != (size_t)n * n * n) { fprintf(stderr, "short table\n"); return 1; }
    fclose(f);
    int allmode = !strcmp(argv[2], "all");
    int maxprint = argc > 3 ? atoi(argv[3]) : 100;
    /* table sanity: general position + antisymmetry */
    long bad = 0;
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) for (int k = 0; k < n; k++) {
        int s = O(i, j, k);
        int deg = (i == j || j == k || i == k);
        if (deg) { if (s) bad++; continue; }
        if (s != 1 && s != -1) bad++;
        if (O(j, i, k) != -s || O(j, k, i) != s) bad++;
    }
    if (bad) { fprintf(stderr, "table sanity failures: %ld\n", bad); return 3; }
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) {
        u128 m = 0;
        if (i != j) for (int k = 0; k < n; k++) if (k != i && k != j && O(i, j, k) > 0) m |= BIT(k);
        Lf[i][j] = m;
    }
    u128 ALL = (n == 128) ? ~(u128)0 : (BIT(n) - 1);
    hset mods; hinit(&mods, 1 << 12);       /* modules (as bitsets of C) with 2 <= |C| <= n-2 */
    long long violations = 0;
    for (int a = 0; a < n; a++) {
        hset seen; hinit(&seen, 1 << 10);
        size_t qcap = 1024, qn = 0, qh = 0; u128 *queue = malloc(qcap * sizeof(u128));
#define CLASSIFY(K) do { u128 _K = (K); int s = pc(_K); \
        if (s < n - 1) { \
            if (hadd(&seen, _K)) { \
                hadd(&mods, ALL & ~_K); \
                if (!allmode && s >= 5) violations++; \
                if (allmode || s <= 4) { if (qn == qcap) { qcap *= 2; queue = realloc(queue, qcap * sizeof(u128)); } queue[qn++] = _K; } \
            } } } while (0)
        for (int t1 = 0; t1 < n; t1++) if (t1 != a) for (int t2 = t1 + 1; t2 < n; t2++) if (t2 != a) {
            u128 K = closure(a, BIT(t1) | BIT(t2));
            CLASSIFY(K);
        }
        while (qh < qn) {
            u128 K = queue[qh++];
            for (int t = 0; t < n; t++) if (t != a && !((K >> t) & 1)) {
                u128 K2 = closure(a, K | BIT(t));
                CLASSIFY(K2);
            }
        }
        free(queue); hfree(&seen);
    }
    /* collect, sort, print */
    u128 *list = malloc((mods.cnt + 1) * sizeof(u128)); size_t L = 0;
    for (size_t i = 0; i < mods.cap; i++) if (mods.used[i]) list[L++] = mods.v[i];
    qsort(list, L, sizeof(u128), cmpu);
    int hist[130] = {0};
    for (size_t i = 0; i < L; i++) hist[pc(list[i])]++;
    printf("n=%d mode=%s closures=%lld modules(2..n-2)=%zu violations(size 2..n-5 found in detect mode)=%lld\n",
           n, allmode ? "all" : "detect", nclos, L, violations);
    printf("size_histogram:");
    for (int s = 2; s <= n - 2; s++) if (hist[s]) printf(" %d:%d", s, hist[s]);
    printf("\n");
    for (size_t i = 0; i < L && (int)i < maxprint; i++) {
        printf("module size %d complement:", pc(list[i]));
        for (int s = 0; s < n; s++) if (!((list[i] >> s) & 1)) printf(" %d", s);
        printf("\n");
    }
    return 0;
}
