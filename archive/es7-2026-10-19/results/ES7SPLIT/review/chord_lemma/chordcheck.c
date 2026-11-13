/* Independent exhaustive check of the hexagon chord lemma and its m=1 corollary.
 * (Written from scratch for the independent check; shares no code with tools/ of this result.)
 *
 * Input on stdin: n x_1 y_1 ... x_n y_n   (integers, n <= 64)
 * Exact integer arithmetic (coordinates must have |x|,|y| < 2^28 so that products fit in int64).
 *
 * 1. Verifies general position and enumerates ALL subsets in convex position by incremental
 *    extension (a set is in convex position iff no point is inside a triangle of three others);
 *    reports counts of convex k-sets for k=3..8.  A heptagon-free set must have zero convex 7-sets.
 *    (This is a brute-force check, independent of any dynamic program.)
 * 2. For EVERY convex hexagon H (ccw h0..h5), every i in 0..5 and m in {1,2,3}:
 *      a=h_i, b=h_{i+m+1}, R(i,m) = { p : p strictly on the dropped side of line ab,
 *                                      orient(h_{i-1},h_i,p)>0, orient(h_{i+m+1},h_{i+m+2},p)>0 }
 *    computes by a DP the largest Q subset of S cap R with {a,b} u Q in convex position, and checks
 *    it equals m (it is >= m because the dropped vertices qualify; the lemma says <= m).
 *    The DP answer is cross-checked by brute force over all subsets of size m+1 (and m) of R.
 * 3. For m=1 (chord h_{j-1}h_{j+1}): checks S cap R(j-1,1) == {h_j} u (S cap open ear triangle)
 *    u {p outside H whose visible-edge set is exactly {e_{j-1}, e_j}}, and that S cap R(j-1,1) is
 *    pairwise nested w.r.t. the chord (exactly one of p in int T(a,b,q), q in int T(a,b,p)).
 * 4. For every empty convex hexagon (6-hole) checks that every other point sees a contiguous chain
 *    of >= 2 edges; for the hull (if it is a hexagon) reports ear sizes and nesting.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef long long ll;
static int n;
static ll X[64], Y[64];
static signed char O[64][64][64];

static ll orient_raw(int a, int b, int c) {
    return (X[b] - X[a]) * (Y[c] - Y[a]) - (Y[b] - Y[a]) * (X[c] - X[a]);
}

/* p strictly inside triangle abc (general position) */
static int inside(int p, int a, int b, int c) {
    int o = O[a][b][c];
    return O[a][b][p] == o && O[b][c][p] == o && O[c][a][p] == o;
}

static long long cnt[10];
static int sub[10];
static long long nhex = 0, nhole = 0, viol_lemma = 0, viol_dp = 0, viol_cor = 0, viol_nest = 0, viol_hole = 0;
static int maxchain[4], minchain[4] = {0, 99, 99, 99}, maxR[4];
static long long hept = 0;

/* is sub[0..k-1] u {new = sub[k-1]} still in convex position, given sub[0..k-2] is */
static int convex_with_new(int k) {
    int p = sub[k - 1];
    for (int i = 0; i < k - 1; i++)
        for (int j = i + 1; j < k - 1; j++)
            for (int l = j + 1; l < k - 1; l++)
                if (inside(p, sub[i], sub[j], sub[l])) return 0;
    for (int i = 0; i < k - 1; i++)
        for (int j = i + 1; j < k - 1; j++)
            for (int l = 0; l < k - 1; l++) {
                if (l == i || l == j) continue;
                if (inside(sub[l], sub[i], sub[j], p)) return 0;
            }
    return 1;
}

static int convex_set(const int *q, int k) {
    for (int i = 0; i < k; i++)
        for (int j = i + 1; j < k; j++)
            for (int l = j + 1; l < k; l++)
                for (int t = 0; t < k; t++) {
                    if (t == i || t == j || t == l) continue;
                    if (inside(q[t], q[i], q[j], q[l])) return 0;
                }
    return 1;
}

/* largest chain via DP: R[0..r-1] all strictly right of a->b */
static int dp_chain(int a, int b, int *R, int r) {
    int q[64];
    memcpy(q, R, sizeof(int) * r);
    /* insertion sort by angle around a: q before q' iff orient(a,q,q') > 0 */
    for (int i = 1; i < r; i++) {
        int v = q[i], j = i - 1;
        while (j >= 0 && O[a][v][q[j]] > 0) { q[j + 1] = q[j]; j--; }
        q[j + 1] = v;
    }
    for (int i = 0; i + 1 < r; i++)
        if (O[a][q[i]][q[i + 1]] <= 0) { fprintf(stderr, "sort error\n"); exit(2); }
    static int f[64][64];
    int best = r >= 1 ? 1 : 0;
    for (int k = 0; k < r; k++)
        for (int j = 0; j < k; j++) {
            int v = 2;
            for (int i = 0; i < j; i++)
                if (O[q[i]][q[j]][q[k]] > 0 && f[i][j] + 1 > v) v = f[i][j] + 1;
            f[j][k] = v;
            if (O[q[j]][q[k]][b] > 0 && v > best) best = v;
        }
    return best;
}

/* brute force: does R contain s points that with a,b are in convex position */
static int exists_conv(int a, int b, int *R, int r, int s) {
    int idx[8];
    int q[8];
    if (s > r) return 0;
    for (int i = 0; i < s; i++) idx[i] = i;
    while (1) {
        q[0] = a; q[1] = b;
        for (int i = 0; i < s; i++) q[2 + i] = R[idx[i]];
        if (convex_set(q, s + 2)) return 1;
        int t = s - 1;
        while (t >= 0 && idx[t] == r - s + t) t--;
        if (t < 0) break;
        idx[t]++;
        for (int u = t + 1; u < s; u++) idx[u] = idx[u - 1] + 1;
    }
    return 0;
}

static int brute_check = 1;
static long long brute_every = 1;

static void process_hexagon(void) {
    int h[6];
    /* ccw order: start at lowest (y,x), sort others by angle */
    int s0 = 0;
    for (int i = 1; i < 6; i++) {
        int p = sub[i], c = sub[s0];
        if (Y[p] < Y[c] || (Y[p] == Y[c] && X[p] < X[c])) s0 = i;
    }
    h[0] = sub[s0];
    int k = 1;
    for (int i = 0; i < 6; i++) if (i != s0) h[k++] = sub[i];
    for (int i = 2; i < 6; i++) {
        int v = h[i], j = i - 1;
        while (j >= 1 && O[h[0]][v][h[j]] > 0) { h[j + 1] = h[j]; j--; }
        h[j + 1] = v;
    }
    for (int i = 0; i < 6; i++)
        if (O[h[i]][h[(i + 1) % 6]][h[(i + 2) % 6]] <= 0) { fprintf(stderr, "hexagon order error\n"); exit(2); }
    nhex++;
    /* emptiness */
    int empty = 1;
    for (int p = 0; p < n && empty; p++) {
        int isv = 0;
        for (int t = 0; t < 6; t++) if (h[t] == p) isv = 1;
        if (isv) continue;
        int in = 1;
        for (int t = 0; t < 6; t++) if (O[h[t]][h[(t + 1) % 6]][p] <= 0) in = 0;
        if (in) empty = 0;
    }
    if (empty) {
        nhole++;
        for (int p = 0; p < n; p++) {
            int isv = 0;
            for (int t = 0; t < 6; t++) if (h[t] == p) isv = 1;
            if (isv) continue;
            int vis[6], nv = 0;
            for (int t = 0; t < 6; t++) { vis[t] = O[h[t]][h[(t + 1) % 6]][p] < 0; nv += vis[t]; }
            /* contiguity: number of 0->1 transitions cyclically must be 1 */
            int tr = 0;
            for (int t = 0; t < 6; t++) if (!vis[t] && vis[(t + 1) % 6]) tr++;
            if (nv < 2 || nv > 5 || tr != 1) viol_hole++;
        }
    }
    for (int i = 0; i < 6; i++)
        for (int m = 1; m <= 3; m++) {
            int a = h[i], b = h[(i + m + 1) % 6], hm1 = h[(i + 5) % 6], hb1 = h[(i + m + 2) % 6];
            int d = h[(i + 1) % 6];
            int side = O[a][b][d];
            if (side >= 0) { fprintf(stderr, "side error\n"); exit(2); }
            int R[64], r = 0;
            for (int p = 0; p < n; p++) {
                if (p == a || p == b) continue;
                if (O[a][b][p] == side && O[hm1][a][p] > 0 && O[b][hb1][p] > 0) R[r++] = p;
            }
            /* dropped vertices must be in R, kept ones not */
            for (int t = 1; t <= m; t++) {
                int dv = h[(i + t) % 6], found = 0;
                for (int u = 0; u < r; u++) if (R[u] == dv) found = 1;
                if (!found) { fprintf(stderr, "dropped vertex not in R\n"); exit(2); }
            }
            int c = dp_chain(a, b, R, r);
            if (c > maxchain[m]) maxchain[m] = c;
            if (c < minchain[m]) minchain[m] = c;
            if (r > maxR[m]) maxR[m] = r;
            if (c != m) viol_lemma++;
            if (brute_check && (nhex % brute_every == 0)) {
                int e1 = exists_conv(a, b, R, r, m + 1);
                int e0 = exists_conv(a, b, R, r, m);
                if (e1 != (c >= m + 1) || e0 != (c >= m)) viol_dp++;
            }
            if (m == 1) {
                /* corollary: j = i+1 */
                int j = (i + 1) % 6;
                int hj = h[j];
                int ejm1a = h[(j + 5) % 6], ejm1b = h[j];  /* e_{j-1} = h_{j-1} -> h_j */
                int eja = h[j], ejb = h[(j + 1) % 6];       /* e_j = h_j -> h_{j+1} */
                (void)ejm1a; (void)ejm1b; (void)eja; (void)ejb;
                for (int p = 0; p < n; p++) {
                    if (p == a || p == b) continue;
                    int inR = 0;
                    for (int u = 0; u < r; u++) if (R[u] == p) inR = 1;
                    int isv = 0;
                    for (int t = 0; t < 6; t++) if (h[t] == p) isv = 1;
                    int inE = 0;
                    if (p == hj) inE = 1;
                    else if (!isv) {
                        int inear = inside(p, h[(j + 5) % 6], hj, h[(j + 1) % 6]);
                        int vis[6], nv = 0;
                        for (int t = 0; t < 6; t++) { vis[t] = O[h[t]][h[(t + 1) % 6]][p] < 0; nv += vis[t]; }
                        int exact2 = (nv == 2 && vis[(j + 5) % 6] && vis[j]);
                        if (inear || exact2) inE = 1;
                    }
                    if (inR != inE) viol_cor++;
                }
                for (int u = 0; u < r; u++)
                    for (int v = u + 1; v < r; v++) {
                        int p = R[u], q = R[v];
                        int pq = inside(p, a, b, q), qp = inside(q, a, b, p);
                        if (pq + qp != 1) viol_nest++;
                    }
            }
        }
}

static void rec(int start, int k) {
    cnt[k]++;
    if (k == 6) process_hexagon();
    if (k == 7) { hept++; return; }
    for (int p = start; p < n; p++) {
        sub[k] = p;
        if (k < 3 || convex_with_new(k + 1)) rec(p + 1, k + 1);
    }
}

int main(int argc, char **argv) {
    if (argc > 1 && strcmp(argv[1], "--nobrute") == 0) brute_check = 0;
    if (argc > 2 && strcmp(argv[1], "--every") == 0) brute_every = atoll(argv[2]);
    if (scanf("%d", &n) != 1 || n > 64 || n < 6) { fprintf(stderr, "bad n\n"); return 1; }
    for (int i = 0; i < n; i++) {
        if (scanf("%lld %lld", &X[i], &Y[i]) != 2) { fprintf(stderr, "bad input\n"); return 1; }
        if (X[i] > (1LL << 28) || X[i] < -(1LL << 28) || Y[i] > (1LL << 28) || Y[i] < -(1LL << 28)) {
            fprintf(stderr, "coordinate too large\n"); return 1;
        }
    }
    int gp = 1;
    for (int a = 0; a < n; a++)
        for (int b = 0; b < n; b++)
            for (int c = 0; c < n; c++) {
                ll v = orient_raw(a, b, c);
                O[a][b][c] = (v > 0) - (v < 0);
                if (a != b && b != c && a != c && v == 0) gp = 0;
            }
    if (!gp) { printf("NOT IN GENERAL POSITION\n"); return 0; }
    rec(0, 0);
    /* hull */
    int hull[64], hn = 0;
    {
        /* gift wrapping */
        int start = 0;
        for (int i = 1; i < n; i++) if (X[i] < X[start] || (X[i] == X[start] && Y[i] < Y[start])) start = i;
        int cur = start;
        do {
            hull[hn++] = cur;
            int nxt = (cur == 0) ? 1 : 0;
            for (int p = 0; p < n; p++) {
                if (p == cur) continue;
                if (O[cur][nxt][p] < 0) nxt = p; /* p is right of cur->nxt: more clockwise */
            }
            cur = nxt;
        } while (cur != start && hn < 64);
    }
    printf("n=%d gp=%d convex k-sets:", n, gp);
    for (int k = 3; k <= 7; k++) printf(" k%d=%lld", k, cnt[k]);
    printf(" | heptagons=%lld\n", hept);
    printf("hull size %d (ccw from leftmost)\n", hn);
    printf("convex hexagons=%lld 6-holes=%lld\n", nhex, nhole);
    printf("chain stats per m: ");
    for (int m = 1; m <= 3; m++) printf("m=%d [min %d max %d maxR %d] ", m, minchain[m], maxchain[m], maxR[m]);
    printf("\n");
    printf("violations: lemma(c!=m)=%lld dp-vs-brute=%lld%s corollary-region=%lld nesting=%lld hole-visibility=%lld\n",
           viol_lemma, viol_dp, brute_check ? "" : "(skipped)", viol_cor, viol_nest, viol_hole);
    if (hn == 6) {
        printf("hull ears (size,nested):");
        for (int j = 0; j < 6; j++) {
            int a = hull[(j + 5) % 6], v = hull[j], b = hull[(j + 1) % 6];
            int E[64], e = 0;
            for (int p = 0; p < n; p++)
                if (p != a && p != v && p != b && inside(p, a, v, b)) E[e++] = p;
            int nested = 1;
            for (int u = 0; u < e; u++)
                for (int w = u + 1; w < e; w++)
                    if (inside(E[u], a, E[w], b) + inside(E[w], a, E[u], b) != 1) nested = 0;
            printf(" (%d,%d)", e, nested);
        }
        printf("\n");
    }
    return 0;
}
