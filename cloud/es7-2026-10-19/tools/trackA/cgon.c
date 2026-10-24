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

static const ll COORD_LIMIT = (1LL << 30);

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

static int mode_count(int K) {
    read_points(stdin);
    if (!general_position_all()) { printf("NOT_GENERAL_POSITION\n"); return 1; }
    if (K > N) K = N;
    if (K > 66 && N > 66) { fprintf(stderr, "count range\n"); return 2; }
    build_orients();
    u64 c[MAXN + 1];
    int best = count_kgons(K, c);
    printf("N=%d", N);
    for (int k = 3; k <= K; k++) printf(" c%d=%llu", k, c[k]);
    printf(" maxconvex=%d\n", best);
    return 0;
}

static int mode_anneal(int K, int n, long iters, double T0, double T1, uint64_t seed,
                       const char *init, const char *out, int fixed, double mu, int raw) {
    seed_rng(seed);
    if (strncmp(init, "random:", 7) == 0) {
        ll range = atoll(init + 7);
        N = 0;
        while (N < n) {
            ll x = (ll)(rnd() % (uint64_t)range), y = (ll)(rnd() % (uint64_t)range);
            if (candidate_ok(N, x, y)) { X[N] = x; Y[N] = y; N++; }
        }
    } else {
        FILE *f = fopen(init, "r");
        if (!f) { perror(init); return 2; }
        read_points(f);
        fclose(f);
        if (N != n) { fprintf(stderr, "init has %d points, expected %d\n", N, n); return 2; }
    }
    if (!general_position_all()) { fprintf(stderr, "init not in general position\n"); return 2; }
    build_orients();
    u64 cc[MAXN + 1];
    count_kgons(K, cc);
    u64 E = cc[K], bestE = E, F = cc[K - 1];
    ll BX[MAXN], BY[MAXN];
    memcpy(BX, X, sizeof X); memcpy(BY, Y, sizeof Y);
    long accepted = 0, rejected_gp = 0, evals = 0;
    long dwell[4] = {0, 0, 0, 0};   /* evaluated iterations whose current E is 0,1,2,>=3 */
    long acc_at_min = 0;            /* accepted moves that land on a state with E == bestE */
    clock_t t0 = clock();
    fprintf(stderr, "start E=%llu\n", E);
    for (long it = 0; it < iters && bestE > 0; it++) {
        double T = T0 * pow(T1 / T0, (double)it / (double)iters);
        int p = fixed + (int)(rnd() % (uint64_t)(N - fixed));
        ll nx, ny;
        propose(p, &nx, &ny);
        if (!candidate_ok(p, nx, ny)) { rejected_gp++; continue; }
        ll ox = X[p], oy = Y[p];
        X[p] = nx; Y[p] = ny;
        set_point_orients(p);
        count_kgons(K, cc);
        u64 E2 = cc[K], F2 = cc[K - 1];
        double dE = (raw ? ((double)E2 - (double)E) : (log1p((double)E2) - log1p((double)E)))
                    + mu * (log1p((double)F2) - log1p((double)F));
        evals++;
        if (E2 < E || (E2 == E && dE <= 0) || urand() < exp(-dE / T)) {
            E = E2; F = F2; accepted++;
            if (E2 <= bestE) acc_at_min++;
            if (E < bestE) {
                bestE = E;
                memcpy(BX, X, sizeof X); memcpy(BY, Y, sizeof Y);
            }
        } else {
            X[p] = ox; Y[p] = oy;
            set_point_orients(p);
        }
        dwell[E >= 3 ? 3 : (int)E]++;
        if ((it & 0x3fff) == 0)
            fprintf(stderr, "it=%ld T=%.4f E=%llu F=%llu best=%llu acc=%ld gprej=%ld t=%.1fs\n", it, T, E, F, bestE,
                    accepted, rejected_gp, (double)(clock() - t0) / CLOCKS_PER_SEC);
    }
    memcpy(X, BX, sizeof X); memcpy(Y, BY, sizeof Y);
    build_orients();
    if (!general_position_all()) { fprintf(stderr, "BUG: best not in general position\n"); return 3; }
    u64 check = count_k(K);
    if (check != bestE) { fprintf(stderr, "BUG: recount mismatch\n"); return 3; }
    write_points(out);
    printf("anneal K=%d N=%d raw=%d T0=%g T1=%g mu=%.3f seed=%llu iters=%ld best=%llu accepted=%ld gprej=%ld evals=%ld dwellE0/1/2/3+=%ld/%ld/%ld/%ld acc_at_best=%ld cpu=%.1fs\n", K, N, raw, T0, T1, mu,
           (unsigned long long)seed, iters, bestE, accepted, rejected_gp, evals, dwell[0], dwell[1], dwell[2], dwell[3], acc_at_min,
           (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}

/* add one point to the set read from stdin at `tries` random candidate positions */
static int mode_addpoint(int K, long tries, uint64_t seed) {
    seed_rng(seed);
    read_points(stdin);
    if (!general_position_all()) { fprintf(stderr, "base not in general position\n"); return 2; }
    int base = N;
    N = base + 1;
    X[base] = X[0]; Y[base] = Y[0];
    build_orients();
    u64 hist[8] = {0}; /* 0,1,2,3-9,10-99,100-999,1000-9999,>=10000 */
    u64 minE = ~0ULL; ll mx = 0, my = 0; long valid = 0;
    N = base;
    double smax = log2_extent() + 2.0;
    N = base + 1;
    for (long t = 0; t < tries; t++) {
        ll x, y;
        int j = (int)(rnd() % (uint64_t)base);
        double r = urand();
        if (r < 0.7) { x = X[j] + scaled(smax); y = Y[j] + scaled(smax); }
        else { x = X[j] + scaled(smax * 0.5); y = Y[j] + scaled(smax * 0.5); }
        if (!candidate_ok(base, x, y)) continue;
        X[base] = x; Y[base] = y;
        set_point_orients(base);
        u64 e = count_k(K);
        valid++;
        int b = e == 0 ? 0 : e == 1 ? 1 : e == 2 ? 2 : e < 10 ? 3 : e < 100 ? 4 : e < 1000 ? 5 : e < 10000 ? 6 : 7;
        hist[b]++;
        if (e < minE) { minE = e; mx = x; my = y; }
    }
    printf("addpoint K=%d base=%d valid=%ld min=%llu at (%lld,%lld) hist[0,1,2,3-9,10-99,1e2-1e3,1e3-1e4,>=1e4]=",
           K, base, valid, minE, mx, my);
    for (int b = 0; b < 8; b++) printf("%llu%c", hist[b], b < 7 ? ',' : '\n');
    return 0;
}

/* single-move neighbourhood scan: for every point p, try `tries` proposed new
 * positions (same proposal distribution as the annealer) and record the
 * number of convex K-gons after that one move. */
static int mode_scan(int K, long tries, uint64_t seed, const char *zero_out) {
    seed_rng(seed);
    read_points(stdin);
    if (!general_position_all()) { fprintf(stderr, "not in general position\n"); return 2; }
    build_orients();
    u64 E0 = count_k(K);
    /* participation: #K-gons through p = E0 - E(S \ {p}) */
    int involved = 0;
    {
        ll SX[MAXN], SY[MAXN];
        memcpy(SX, X, sizeof X); memcpy(SY, Y, sizeof Y);
        int n0 = N;
        for (int p = 0; p < n0; p++) {
            N = 0;
            for (int i = 0; i < n0; i++) if (i != p) { X[N] = SX[i]; Y[N] = SY[i]; N++; }
            build_orients();
            if (count_k(K) < E0) involved++;
        }
        N = n0; memcpy(X, SX, sizeof X); memcpy(Y, SY, sizeof Y);
        build_orients();
    }
    u64 hist[8] = {0}, pmin_hist[8] = {0};
    u64 gmin = ~0ULL; long valid = 0;
    for (int p = 0; p < N; p++) {
        ll ox = X[p], oy = Y[p];
        u64 pmin = ~0ULL;
        for (long t = 0; t < tries; t++) {
            ll nx, ny;
            propose(p, &nx, &ny);
            if (!candidate_ok(p, nx, ny)) continue;
            X[p] = nx; Y[p] = ny;
            set_point_orients(p);
            u64 e = count_k(K);
            valid++;
            int b = e == 0 ? 0 : e == 1 ? 1 : e == 2 ? 2 : e < 10 ? 3 : e < 100 ? 4 : e < 1000 ? 5 : e < 10000 ? 6 : 7;
            hist[b]++;
            if (e < pmin) pmin = e;
            if (e == 0) { write_points(zero_out); fprintf(stderr, "ZERO FOUND -> %s\n", zero_out); }
            X[p] = ox; Y[p] = oy;
            set_point_orients(p);
        }
        if (pmin < gmin) gmin = pmin;
        int b = pmin == 0 ? 0 : pmin == 1 ? 1 : pmin == 2 ? 2 : pmin < 10 ? 3 : pmin < 100 ? 4 : pmin < 1000 ? 5 : pmin < 10000 ? 6 : 7;
        pmin_hist[b]++;
    }
    printf("scan K=%d N=%d E0=%llu points_in_some_Kgon=%d valid_moves=%ld min_after_one_move=%llu "
           "hist[0,1,2,3-9,10-99,1e2-1e3,1e3-1e4,>=1e4]=", K, N, E0, involved, valid, gmin);
    for (int b = 0; b < 8; b++) printf("%llu%c", hist[b], b < 7 ? ',' : ' ');
    printf("per_point_min_hist=");
    for (int b = 0; b < 8; b++) printf("%llu%c", pmin_hist[b], b < 7 ? ',' : '\n');
    return 0;
}

int main(int argc, char **argv) {
    if (argc >= 3 && !strcmp(argv[1], "count")) return mode_count(atoi(argv[2]));
    if (argc >= 6 && !strcmp(argv[1], "scan"))
        return mode_scan(atoi(argv[2]), atol(argv[3]), (uint64_t)atoll(argv[4]), argv[5]);
    if (argc >= 10 && !strcmp(argv[1], "anneal"))
        return mode_anneal(atoi(argv[2]), atoi(argv[3]), atol(argv[4]), atof(argv[5]), atof(argv[6]),
                           (uint64_t)atoll(argv[7]), argv[8], argv[9], argc >= 11 ? atoi(argv[10]) : 0,
                           argc >= 12 ? atof(argv[11]) : 0.0, argc >= 13 ? atoi(argv[12]) : 0);
    if (argc >= 5 && !strcmp(argv[1], "addpoint"))
        return mode_addpoint(atoi(argv[2]), atol(argv[3]), (uint64_t)atoll(argv[4]));
    fprintf(stderr, "usage: see header comment\n");
    return 2;
}
