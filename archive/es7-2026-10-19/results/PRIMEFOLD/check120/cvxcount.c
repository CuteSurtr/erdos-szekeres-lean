/*
 * cvxcount.c -- independent counter of k-point subsets in convex position, from an exact
 * orientation table.  Written from scratch for the C89-15 verification (does not share code
 * with the producer's cvx2.c or the earlier cvxcheck.c).
 *
 * Usage: cvxcount OTAB ORDERS K
 *   OTAB   : "n\n" followed by n^3 signed bytes, T[(a*n+b)*n+c] = orient(a,b,c) in {-1,0,+1}
 *   ORDERS : line 1 = indices sorted by exact (y,x)-lex order, line 2 = by exact (x,y)-lex order
 *   K      : count convex k-gons for k = 3..K
 *
 * Checks performed on the table first: T(a,b,c) != 0 for distinct a,b,c; T is invariant under
 * cyclic shifts and changes sign under transpositions.
 *
 * DPA ("lowest anchor"): every convex polygon is counted at its minimum vertex a in the (y,x)
 *   order.  The later points are sorted around a by the comparator  P < Q  iff  T(a,P,Q) > 0,
 *   and the program VERIFIES that T(a,P_i,P_j) = +1 for all i < j after sorting (so the
 *   comparator is a strict total order and all later points lie in a half-plane at a).
 *   A chain a, v1, ..., v_{k-1} (increasing in that order) closes to a convex polygon iff
 *   T(v_{s-1}, v_s, v_{s+1}) = +1 for s = 2..k-2 (the turns at v1, v_{k-1} and a are implied).
 *
 * DPB ("cap + cup"): every convex polygon is counted at its (min, max) pair (L, R) in the (x,y)
 *   order; it is the union of a chain L..R with all turns clockwise (T = -1) and a chain L..R
 *   with all turns counter-clockwise (T = +1), both increasing in the order.  For each (L,R) the
 *   number of k-gons is sum_{a+b-2=k} caps_a(L,R) * cups_b(L,R).
 *
 * Both DPs print the number of convex k-gons for k = 3..K; they must agree.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef unsigned long long u64;
typedef unsigned __int128 u128;

static int n;
static signed char *T;
#define OR(a, b, c) T[((size_t)(a) * n + (b)) * n + (c)]

static void die(const char *msg) { fprintf(stderr, "FATAL: %s\n", msg); exit(2); }

static u64 addchk(u64 x, u64 y) {
    u64 z = x + y;
    if (z < x) die("overflow in addition");
    return z;
}

static void read_table(const char *path) {
    FILE *f = fopen(path, "rb");
    if (!f) die("cannot open table");
    if (fscanf(f, "%d", &n) != 1) die("bad header");
    int ch = fgetc(f);
    if (ch != '\n') die("header not followed by newline");
    size_t N = (size_t)n * n * n;
    T = malloc(N);
    if (!T) die("malloc");
    if (fread(T, 1, N, f) != N) die("short table");
    if (fgetc(f) != EOF) die("trailing bytes in table");
    fclose(f);
}

static void check_table(void) {
    long bad = 0;
    for (int a = 0; a < n; a++)
        for (int b = 0; b < n; b++)
            for (int c = 0; c < n; c++) {
                int v = OR(a, b, c);
                int distinct = (a != b && b != c && a != c);
                if (distinct) {
                    if (v != 1 && v != -1) bad++;
                    if (OR(b, c, a) != v || OR(c, a, b) != v) bad++;
                    if (OR(b, a, c) != -v || OR(a, c, b) != -v || OR(c, b, a) != -v) bad++;
                } else if (v != 0) bad++;
            }
    printf("table n=%d: %ld violations (nonzero / cyclic / antisymmetric)\n", n, bad);
    if (bad) die("table check failed");
}

static void read_orders(const char *path, int *oy, int *ox) {
    FILE *f = fopen(path, "r");
    if (!f) die("cannot open orders");
    for (int i = 0; i < n; i++) if (fscanf(f, "%d", &oy[i]) != 1) die("orders line 1");
    for (int i = 0; i < n; i++) if (fscanf(f, "%d", &ox[i]) != 1) die("orders line 2");
    fclose(f);
    /* must be permutations */
    char *seen = calloc(n, 1);
    for (int i = 0; i < n; i++) { if (oy[i] < 0 || oy[i] >= n || seen[oy[i]]) die("oy not perm"); seen[oy[i]] = 1; }
    memset(seen, 0, n);
    for (int i = 0; i < n; i++) { if (ox[i] < 0 || ox[i] >= n || seen[ox[i]]) die("ox not perm"); seen[ox[i]] = 1; }
    free(seen);
}

/* ---------------- DPA ---------------- */
static void dpa(const int *oy, int K, u64 *cnt) {
    int *c = malloc(sizeof(int) * n);
    size_t M = (size_t)n * n;
    u64 *dp = calloc((size_t)(K + 1) * M, sizeof(u64));
    if (!c || !dp) die("malloc dpa");
    for (int k = 0; k <= K; k++) cnt[k] = 0;
    for (int pa = 0; pa < n; pa++) {
        int a = oy[pa], m = 0;
        for (int pb = pa + 1; pb < n; pb++) c[m++] = oy[pb];
        /* insertion sort by angle around a */
        for (int i = 1; i < m; i++) {
            int x = c[i], j = i - 1;
            while (j >= 0 && OR(a, x, c[j]) > 0) { c[j + 1] = c[j]; j--; }
            c[j + 1] = x;
        }
        for (int i = 0; i < m; i++)
            for (int j = i + 1; j < m; j++)
                if (OR(a, c[i], c[j]) != 1) die("DPA: angular order not a strict total order (not a half-plane)");
        /* level 3 */
#define DP(k, i, j) dp[(size_t)(k) * M + (size_t)(i) * m + (j)]
        for (int i = 0; i < m; i++)
            for (int j = i + 1; j < m; j++) DP(3, i, j) = 1;
        cnt[3] = addchk(cnt[3], (u64)m * (m - 1) / 2);
        for (int k = 4; k <= K; k++) {
            for (int j = 0; j < m; j++)
                for (int l = j + 1; l < m; l++) {
                    u64 s = 0;
                    int cj = c[j], cl = c[l];
                    for (int i = 0; i < j; i++)
                        if (OR(c[i], cj, cl) > 0) s = addchk(s, DP(k - 1, i, j));
                    DP(k, j, l) = s;
                    cnt[k] = addchk(cnt[k], s);
                }
        }
#undef DP
    }
    free(c); free(dp);
}

/* ---------------- DPB ---------------- */
static void dpb(const int *ox, int K, u64 *cnt) {
    size_t M = (size_t)n * n;
    u64 *cap = calloc((size_t)(K + 1) * M, sizeof(u64));
    u64 *cup = calloc((size_t)(K + 1) * M, sizeof(u64));
    u64 *capsR = calloc((size_t)(K + 1), sizeof(u64));
    u64 *cupsR = calloc((size_t)(K + 1), sizeof(u64));
    int *id = malloc(sizeof(int) * n);
    if (!cap || !cup || !id) die("malloc dpb");
    for (int k = 0; k <= K; k++) cnt[k] = 0;
    for (int L = 0; L < n; L++) {
        int m = n - L;               /* positions 0..m-1, position 0 is L itself */
        for (int p = 0; p < m; p++) id[p] = ox[L + p];
#define CA(k, i, j) cap[(size_t)(k) * M + (size_t)(i) * m + (j)]
#define CU(k, i, j) cup[(size_t)(k) * M + (size_t)(i) * m + (j)]
        for (int k = 2; k <= K; k++)
            for (int i = 0; i < m; i++)
                for (int j = 0; j < m; j++) { CA(k, i, j) = 0; CU(k, i, j) = 0; }
        for (int j = 1; j < m; j++) { CA(2, 0, j) = 1; CU(2, 0, j) = 1; }
        for (int k = 3; k <= K; k++) {
            for (int j = 1; j < m; j++)
                for (int l = j + 1; l < m; l++) {
                    u64 sa = 0, su = 0;
                    int pj = id[j], pl = id[l];
                    for (int i = 0; i < j; i++) {
                        int o = OR(id[i], pj, pl);
                        if (o < 0) sa = addchk(sa, CA(k - 1, i, j));
                        else if (o > 0) su = addchk(su, CU(k - 1, i, j));
                        else die("DPB: zero orientation");
                    }
                    CA(k, j, l) = sa; CU(k, j, l) = su;
                }
        }
        for (int r = 1; r < m; r++) {
            for (int k = 2; k <= K; k++) {
                u64 sa = 0, su = 0;
                for (int i = 0; i < r; i++) { sa = addchk(sa, CA(k, i, r)); su = addchk(su, CU(k, i, r)); }
                capsR[k] = sa; cupsR[k] = su;
            }
            for (int s = 3; s <= K; s++) {
                u128 tot = 0;
                for (int a = 2; a <= K; a++) {
                    int b = s + 2 - a;
                    if (b < 2 || b > K) continue;
                    tot += (u128)capsR[a] * (u128)cupsR[b];
                }
                if (tot >> 64) die("overflow in DPB product");
                cnt[s] = addchk(cnt[s], (u64)tot);
            }
        }
#undef CA
#undef CU
    }
    free(cap); free(cup); free(capsR); free(cupsR); free(id);
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: cvxcount OTAB ORDERS K\n"); return 1; }
    read_table(argv[1]);
    int K = atoi(argv[3]);
    if (K < 3 || K > 40) die("bad K");
    check_table();
    int *oy = malloc(sizeof(int) * n), *ox = malloc(sizeof(int) * n);
    read_orders(argv[2], oy, ox);
    u64 *ca = calloc(K + 1, sizeof(u64)), *cb = calloc(K + 1, sizeof(u64));
    dpa(oy, K, ca);
    dpb(ox, K, cb);
    int agree = 1, maxa = 0, maxb = 0;
    for (int k = 3; k <= K; k++) {
        printf("convex %2d-gons: DPA %llu  DPB %llu%s\n", k, ca[k], cb[k], ca[k] == cb[k] ? "" : "  MISMATCH");
        if (ca[k] != cb[k]) agree = 0;
        if (ca[k]) maxa = k;
        if (cb[k]) maxb = k;
    }
    printf("largest convex subset (<= K): DPA %d  DPB %d%s\n", maxa, maxb,
           (maxa < K && maxb < K) ? "  (K-gon count is 0, so exact)" : "  (reached K: only a lower bound)");
    printf("%s\n", agree ? "DPA == DPB" : "DPA != DPB");
    return agree ? 0 : 3;
}
