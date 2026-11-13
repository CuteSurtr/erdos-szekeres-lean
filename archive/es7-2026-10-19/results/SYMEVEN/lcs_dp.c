/*
 * Largest subset in convex position, two exact O(n^4) dynamic programs (int64 coords, __int128 orientation):
 *  (A) angular DP around the lowest vertex, with witness;  (B) lower cup + upper cap DP (lexicographic order).
 * Also checks distinctness, central symmetry, origin, and general position (all triples).
 * Usage: lcs_dp POINTS_FILE
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 1024
typedef __int128 i128;
static long long X[MAXN], Y[MAXN];
static int N;

static int orient(int a, int b, int c) {
    i128 v = (i128)(X[b] - X[a]) * (i128)(Y[c] - Y[a]) - (i128)(Y[b] - Y[a]) * (i128)(X[c] - X[a]);
    return (v > 0) - (v < 0);
}
static int PIV;
static int cmp_ang(const void *u, const void *v) {
    int a = *(const int *)u, b = *(const int *)v;
    int o = orient(PIV, a, b);
    return o > 0 ? -1 : (o < 0 ? 1 : 0);
}
static int cmp_lex(const void *u, const void *v) {
    int a = *(const int *)u, b = *(const int *)v;
    if (X[a] != X[b]) return X[a] < X[b] ? -1 : 1;
    if (Y[a] != Y[b]) return Y[a] < Y[b] ? -1 : 1;
    return 0;
}
static short dp[MAXN][MAXN], par[MAXN][MAXN];

static int angular(int *wit, int *wlen) {
    int best = N < 2 ? N : 2;
    int v[MAXN];
    for (int p = 0; p < N; p++) {
        int t = 0;
        for (int q = 0; q < N; q++)
            if (Y[q] > Y[p] || (Y[q] == Y[p] && X[q] > X[p])) v[t++] = q;
        if (t + 1 <= best) continue;
        PIV = p;
        qsort(v, t, sizeof(int), cmp_ang);
        for (int j = 0; j < t; j++)
            for (int i = 0; i < j; i++) {
                int bv = 3, bp = -1;
                for (int h = 0; h < i; h++)
                    if (dp[h][i] + 1 > bv && orient(v[h], v[i], v[j]) > 0) { bv = dp[h][i] + 1; bp = h; }
                dp[i][j] = bv; par[i][j] = bp;
                if (bv > best && orient(v[i], v[j], p) > 0) {
                    best = bv;
                    int len = 0, a = i, b = j, tmp[MAXN];
                    tmp[len++] = v[j]; tmp[len++] = v[i];
                    while (par[a][b] != -1) { int hh = par[a][b]; tmp[len++] = v[hh]; b = a; a = hh; }
                    tmp[len++] = p;
                    for (int r = 0; r < len; r++) wit[r] = tmp[len - 1 - r];
                    *wlen = len;
                }
            }
    }
    return best;
}

static short Cu[MAXN][MAXN], Ca[MAXN][MAXN];
static int cupcap(void) {
    int V[MAXN];
    for (int i = 0; i < N; i++) V[i] = i;
    qsort(V, N, sizeof(int), cmp_lex);
    int best = N < 2 ? N : 2;
    for (int a = 0; a < N; a++) {
        for (int j = a + 1; j < N; j++) {
            int fu = 2, fc = 2;
            Cu[a][j] = 2; Ca[a][j] = 2;
            for (int i = a + 1; i < j; i++) {
                int bu = 0, bc = 0;
                for (int h = a; h < i; h++) {
                    int o = orient(V[h], V[i], V[j]);
                    if (o > 0) { if (Cu[h][i] > 0 && Cu[h][i] + 1 > bu) bu = Cu[h][i] + 1; }
                    else if (o < 0) { if (Ca[h][i] > 0 && Ca[h][i] + 1 > bc) bc = Ca[h][i] + 1; }
                }
                Cu[i][j] = bu; Ca[i][j] = bc;
                if (bu > fu) fu = bu;
                if (bc > fc) fc = bc;
            }
            if (fu + fc - 2 > best) best = fu + fc - 2;
        }
    }
    return best;
}

/* independent convex-position test of a witness: every point is a strict hull vertex (no point inside a
   triangle of three others) */
static int convex_position(const int *w, int len) {
    for (int a = 0; a < len; a++)
        for (int b = a + 1; b < len; b++)
            for (int c = b + 1; c < len; c++) {
                int s = orient(w[a], w[b], w[c]);
                for (int d = 0; d < len; d++) {
                    if (d == a || d == b || d == c) continue;
                    if (orient(w[a], w[b], w[d]) == s && orient(w[b], w[c], w[d]) == s &&
                        orient(w[c], w[a], w[d]) == s) return 0;
                }
            }
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s POINTS\n", argv[0]); return 1; }
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
    long long col = 0;
    for (int a = 0; a < N; a++)
        for (int b = a + 1; b < N; b++)
            for (int c = b + 1; c < N; c++)
                if (orient(a, b, c) == 0) col++;
    printf("N=%d duplicates=%d centrally_symmetric=%d origin_in_set=%d collinear_triples=%lld\n", N, dup, sym, orig, col);
    if (col || dup) { printf("not in general position; abort\n"); return 3; }
    int wit[MAXN], wl = 0;
    int A = angular(wit, &wl);
    printf("(A) angular DP: largest convex subset = %d ; witness (%d pts) convex by triangle test = %d\n",
           A, wl, convex_position(wit, wl));
    printf("    witness:");
    for (int r = 0; r < wl; r++) printf(" (%lld,%lld)", X[wit[r]], Y[wit[r]]);
    printf("\n");
    int B = cupcap();
    printf("(B) cup+cap DP: largest convex subset = %d\n", B);
    return 0;
}
