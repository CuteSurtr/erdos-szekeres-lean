/*
 * cgon.c -- exact counting of convex k-gons in planar integer point sets,
 * plus simulated annealing to minimise the number of convex k-gons.
 *
 * Exactness: every geometric decision is an orientation sign computed with
 * __int128 from int64 coordinates bounded by |c| < 2^30 (checked on input and
 * on every move), so the determinant (< 2^63 in magnitude) cannot overflow.
 * No floating point is used in any geometric decision; floats only appear in
 * the annealing acceptance probability and the random move generator.
 *
 * Counting algorithm (per anchor a = lowest vertex of the polygon):
 *   points above a are sorted by angle around a; a convex polygon with lowest
 *   vertex a is a chain a, q_{i1}, ..., q_{i(k-1)} with i1 < ... < i(k-1) and a
 *   left turn at every q.  The turns at a and at the last vertex (back to a)
 *   are automatically convex.  For an inner vertex q_j, incoming directions
 *   (q_j - q_i, i<j, or q_j - a) and outgoing directions (q_l - q_j, l>j) all
 *   lie in the closed half-plane left of line a->q_j, so "left turn" is a
 *   comparison of angles there; with both lists sorted this is a prefix, and
 *   each DP level costs O(m^2) per anchor after O(m^2 log m)-ish sorting.
 *
 * Modes:
 *   cgon count K < pts            print #convex k-gons for k=3..K (K<=N) and max k
 *   cgon anneal K N iters T0 T1 seed init out [fixed]
 *        init = file of points or "random:<range>"; minimises #convex K-gons
 *        fixed (optional) = number of leading points that are never moved
 *   cgon addpoint K tries seed < pts   add one point to the set at many
 *        candidate positions; report histogram of #convex K-gons created
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MAXN 128
typedef long long ll;
typedef unsigned long long u64;

static const ll COORD_LIMIT = (1LL << 26); /* gen.c: sat.c requires |c| < 2^27 */

static int N;
static ll X[MAXN], Y[MAXN];
static signed char O[MAXN][MAXN][MAXN];

static int orient3(ll ax, ll ay, ll bx, ll by, ll cx, ll cy) {
    __int128 v = (__int128)(bx - ax) * (cy - ay) - (__int128)(by - ay) * (cx - ax);
    return (v > 0) - (v < 0);
}

static int in_range(ll x, ll y) {
    return x > -COORD_LIMIT && x < COORD_LIMIT && y > -COORD_LIMIT && y < COORD_LIMIT;
}

static void set_point_orients(int p) {
    for (int i = 0; i < N; i++) {
        if (i == p) continue;
        for (int j = 0; j < N; j++) {
            if (j == p || j == i) continue;
            int s = orient3(X[p], Y[p], X[i], Y[i], X[j], Y[j]);
            O[p][i][j] = s; O[i][j][p] = s; O[j][p][i] = s;
        }
    }
}

static void build_orients(void) {
    for (int i = 0; i < N; i++)
        for (int j = 0; j < N; j++)
            for (int k = 0; k < N; k++)
                O[i][j][k] = (i == j || j == k || i == k) ? 0
                    : orient3(X[i], Y[i], X[j], Y[j], X[k], Y[k]);
}

/* 1 iff the whole set is in general position (no repeated points, no collinear triple). */
static int general_position_all(void) {
    for (int i = 0; i < N; i++) {
        if (!in_range(X[i], Y[i])) return 0;
        for (int j = i + 1; j < N; j++) {
            if (X[i] == X[j] && Y[i] == Y[j]) return 0;
            for (int k = j + 1; k < N; k++)
                if (orient3(X[i], Y[i], X[j], Y[j], X[k], Y[k]) == 0) return 0;
        }
    }
    return 1;
}

/* 1 iff placing point p at (x,y) keeps general position. */
static int candidate_ok(int p, ll x, ll y) {
    if (!in_range(x, y)) return 0;
    for (int i = 0; i < N; i++) {
        if (i == p) continue;
        if (X[i] == x && Y[i] == y) return 0;
        for (int j = i + 1; j < N; j++) {
            if (j == p) continue;
            if (orient3(x, y, X[i], Y[i], X[j], Y[j]) == 0) return 0;
        }
    }
    return 1;
}

/* counts[k] = number of k-subsets in convex position, k = 3..K.
 * Returns the largest k <= K with counts[k] > 0 (or min(N,2)).
 * Requires general position and N <= 66 when K is large (uint64 range). */
static int count_kgons(int K, u64 *counts) {
    static int q[MAXN];
    static int incl[MAXN][MAXN + 1];
    static int posi[MAXN][MAXN + 1];
    static int outl[MAXN][MAXN];
    static int cutv[MAXN][MAXN];
    static u64 g[2][MAXN][MAXN + 1];
    static u64 P[MAXN + 2];
    for (int k = 0; k <= K; k++) counts[k] = 0;
    for (int a = 0; a < N; a++) {
        int m = 0;
        for (int b = 0; b < N; b++)
            if (b != a && (Y[b] > Y[a] || (Y[b] == Y[a] && X[b] > X[a]))) q[m++] = b;
        if (m < 2) continue;
        for (int i = 1; i < m; i++) {           /* angular sort around a */
            int v = q[i], t = i - 1;
            while (t >= 0 && O[a][v][q[t]] > 0) { q[t + 1] = q[t]; t--; }
            q[t + 1] = v;
        }
        for (int j = 0; j < m; j++) {
            int pj = q[j];
            int n_in = 1;
            incl[j][0] = -1;                     /* the anchor: relative angle 0 */
            for (int i = 0; i < j; i++) {
                int t = n_in - 1;
                while (t >= 1 && O[pj][q[i]][q[incl[j][t]]] > 0) { incl[j][t + 1] = incl[j][t]; t--; }
                incl[j][t + 1] = i;
                n_in++;
            }
            for (int t = 0; t < n_in; t++) posi[j][incl[j][t] + 1] = t;
            int n_out = 0;
            for (int l = j + 1; l < m; l++) {
                int t = n_out - 1;
                while (t >= 0 && O[pj][q[l]][q[outl[j][t]]] > 0) { outl[j][t + 1] = outl[j][t]; t--; }
                outl[j][t + 1] = l;
                n_out++;
            }
            int p = 1;                           /* anchor always precedes every outgoing */
            for (int t = 0; t < n_out; t++) {
                int l = outl[j][t];
                while (p < n_in && O[q[incl[j][p]]][pj][q[l]] > 0) p++;
                cutv[j][l] = p;
            }
        }
        int cur = 0;
        for (int j = 0; j < m; j++) {
            for (int t = 0; t <= j; t++) g[cur][j][t] = 0;
            g[cur][j][0] = 1;
        }
        for (int L = 2; L < K; L++) {
            int nx = cur ^ 1;
            for (int l = 0; l < m; l++) for (int t = 0; t <= l; t++) g[nx][l][t] = 0;
            u64 tot = 0;
            for (int j = 0; j < m; j++) {
                P[0] = 0;
                for (int t = 0; t <= j; t++) P[t + 1] = P[t] + g[cur][j][t];
                if (P[j + 1] == 0) continue;
                for (int l = j + 1; l < m; l++) {
                    u64 v = P[cutv[j][l]];
                    g[nx][l][posi[l][j + 1]] = v;
                    tot += v;
                }
            }
            counts[L + 1] += tot;
            cur = nx;
            if (tot == 0) break;
        }
    }
    int best = N < 2 ? N : 2;
    for (int k = 3; k <= K; k++) if (counts[k]) best = k;
    return best;
}

static u64 count_k(int K) {
    u64 c[MAXN + 1];
    count_kgons(K, c);
    return c[K];
}

/* ---------- random numbers (xorshift128+) ---------- */
static uint64_t rs0 = 0x9E3779B97F4A7C15ULL, rs1 = 0xD1B54A32D192ED03ULL;
static uint64_t rnd(void) {
    uint64_t s1 = rs0, s0 = rs1;
    rs0 = s0; s1 ^= s1 << 23;
    rs1 = s1 ^ s0 ^ (s1 >> 17) ^ (s0 >> 26);
    return rs1 + s0;
}
static double urand(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static void seed_rng(uint64_t s) {
    rs0 ^= s * 0x9E3779B97F4A7C15ULL; rs1 ^= (s + 1) * 0xBF58476D1CE4E5B9ULL;
    for (int i = 0; i < 20; i++) rnd();
}
static ll scaled(double smax) {           /* signed integer of magnitude ~2^U(0,smax) */
    double s = urand() * smax;
    double v = (2.0 * urand() - 1.0) * pow(2.0, s);
    return (ll)llround(v);
}

static int read_points(FILE *f) {
    N = 0;
    ll x, y;
    while (fscanf(f, "%lld %lld", &x, &y) == 2) {
        if (N >= MAXN) { fprintf(stderr, "too many points\n"); exit(2); }
        if (!in_range(x, y)) { fprintf(stderr, "coordinate out of range\n"); exit(2); }
        X[N] = x; Y[N] = y; N++;
    }
    return N;
}

static void write_points(const char *path) {
    FILE *f = fopen(path, "w");
    if (!f) { perror(path); exit(2); }
    for (int i = 0; i < N; i++) fprintf(f, "%lld %lld\n", X[i], Y[i]);
    fclose(f);
}

static double log2_extent(void) {
    ll minx = X[0], maxx = X[0], miny = Y[0], maxy = Y[0];
    for (int i = 1; i < N; i++) {
        if (X[i] < minx) minx = X[i]; if (X[i] > maxx) maxx = X[i];
        if (Y[i] < miny) miny = Y[i]; if (Y[i] > maxy) maxy = Y[i];
    }
    ll e = maxx - minx; if (maxy - miny > e) e = maxy - miny;
    return log2((double)e + 2.0);
}

/* propose a new position for point p (general position is checked by caller) */
static void propose(int p, ll *nx, ll *ny) {
    double smax = log2_extent() + 1.0;
    double r = urand();
    if (r < 0.55) {                            /* multi-scale local perturbation */
        *nx = X[p] + scaled(smax); *ny = Y[p] + scaled(smax);
    } else if (r < 0.85) {                     /* jump next to another point */
        int j = (int)(rnd() % (uint64_t)N);
        *nx = X[j] + scaled(smax * 0.6); *ny = Y[j] + scaled(smax * 0.6);
    } else if (r < 0.95) {                     /* small axis-wise nudge */
        if (rnd() & 1) { *nx = X[p] + scaled(smax); *ny = Y[p]; }
        else { *nx = X[p]; *ny = Y[p] + scaled(smax); }
    } else {                                   /* anywhere in the bounding box */
        ll minx = X[0], maxx = X[0], miny = Y[0], maxy = Y[0];
        for (int i = 1; i < N; i++) {
            if (X[i] < minx) minx = X[i]; if (X[i] > maxx) maxx = X[i];
            if (Y[i] < miny) miny = Y[i]; if (Y[i] > maxy) maxy = Y[i];
        }
        *nx = minx + (ll)(urand() * (double)(maxx - minx + 1));
        *ny = miny + (ll)(urand() * (double)(maxy - miny + 1));
    }
}

