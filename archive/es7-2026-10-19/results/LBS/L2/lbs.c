/*
 * lbs.c -- heuristic search for 33 points in general position with few
 * (ideally zero) 7-point subsets in convex position.  Strategy extend32:
 * start from a 32-point set with no convex 7-gon (a realization of the
 * Erdos-Szekeres construction, optionally moved around by a random walk
 * that keeps it 7-gon free), add a 33rd point at many candidate positions,
 * keep the best, then anneal all 33 points.
 *
 * Exactness: coordinates are int64 with |c| < 2^40; orientations use
 * __int128, so no overflow.  Floating point is used only for proposals and
 * the Metropolis acceptance test, never for a geometric decision.
 *
 * Counting: a convex polygon is counted once, at its lowest vertex a (least
 * (y, x)).  The other points above a are sorted by angle around a; a convex
 * k-gon with anchor a is an increasing chain q_1 < ... < q_{k-1} with a left
 * turn at every q_2..q_{k-2} (turns at a, q_1 and q_{k-1} are automatic).
 * h[j][i] = number of chains ending with q_j, q_i; one DP level per vertex.
 * The number of K-gons through a point p is the same DP restricted to chains
 * that contain p (anchor p, or anchors below p with p forced into the chain);
 * a move of p changes the count by through(p, new) - through(p, old).
 *
 * Usage:
 *   lbs count FILE                     counts of convex k-gons, k = 3..7
 *   lbs run SEED SECONDS OUTPREFIX BASEFILE...   main search loop
 */
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAXN 34
#define K 7
typedef long long ll;
typedef unsigned long long u64;

static const ll LIM = 1LL << 40;
static int N;
static ll X[MAXN], Y[MAXN];
static signed char O[MAXN][MAXN][MAXN];

static u64 rs;
static u64 rnd(void) {
    rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs;
}
static double urand(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static double grand(void) {
    double u = urand() + 1e-300, v = urand();
    return sqrt(-2 * log(u)) * cos(2 * M_PI * v);
}

static int orient(ll ax, ll ay, ll bx, ll by, ll cx, ll cy) {
    __int128 v = (__int128)(bx - ax) * (cy - ay) - (__int128)(by - ay) * (cx - ax);
    return (v > 0) - (v < 0);
}

/* Fill orientations involving p; return 0 if p is collinear with two others. */
static int set_orients(int p) {
    int ok = 1;
    for (int i = 0; i < N; i++) {
        if (i == p) continue;
        for (int j = i + 1; j < N; j++) {
            if (j == p) continue;
            int s = orient(X[p], Y[p], X[i], Y[i], X[j], Y[j]);
            if (!s) ok = 0;
            O[p][i][j] = s; O[i][j][p] = s; O[j][p][i] = s;
            O[p][j][i] = -s; O[j][i][p] = -s; O[i][p][j] = -s;
        }
    }
    return ok;
}

static int build_all(void) {
    int ok = 1;
    for (int p = 0; p < N; p++) {
        if (X[p] <= -LIM || X[p] >= LIM || Y[p] <= -LIM || Y[p] >= LIM) ok = 0;
        if (!set_orients(p)) ok = 0;
    }
    return ok;
}

static int below(int a, int b) { /* a is lower than b in (y, x) order */
    return Y[a] < Y[b] || (Y[a] == Y[b] && X[a] < X[b]);
}

/*
 * Add to cnt[k] (k = 3..K) the convex k-gons with anchor a.  If p >= 0 and
 * p != a, only polygons containing p are counted.
 */
static void anchor_count(int a, int p, ll *cnt) {
    int q[MAXN], m = 0;
    for (int i = 0; i < N; i++)
        if (i != a && below(a, i)) {
            int v = i, t = m++;
            while (t > 0 && O[a][v][q[t - 1]] > 0) { q[t] = q[t - 1]; t--; }
            q[t] = v;
        }
    int ip = -1;
    if (p >= 0 && p != a) {
        for (int i = 0; i < m; i++) if (q[i] == p) ip = i;
        if (ip < 0) return;
    }
    static ll h[MAXN][MAXN], g[MAXN][MAXN];
    /* level 2: chains a, q_j, q_i */
    ll c3 = 0;
    for (int i = 0; i < m; i++)
        for (int j = 0; j < i; j++) {
            ll v = 1;
            if (ip >= 0 && (j > ip || (j < ip && ip < i))) v = 0;
            h[j][i] = v;
            if (ip < 0 || i >= ip) c3 += v;
        }
    cnt[3] += c3;
    for (int lev = 3; lev < K; lev++) {
        ll c = 0;
        for (int i = 0; i < m; i++)
            for (int l = i + 1; l < m; l++) g[i][l] = 0;
        for (int i = 1; i < m; i++) {
            int qi = q[i];
            for (int j = 0; j < i; j++) {
                ll v = h[j][i];
                if (!v) continue;
                const signed char *oj = O[q[j]][qi];
                int lmax = (ip >= 0 && i < ip) ? ip + 1 : m;
                for (int l = i + 1; l < lmax; l++)
                    if (oj[q[l]] > 0) g[i][l] += v;
            }
        }
        for (int i = 0; i < m; i++)
            for (int l = i + 1; l < m; l++) {
                h[i][l] = g[i][l];
                if (ip < 0 || l >= ip) c += g[i][l];
            }
        cnt[lev + 1] += c;
    }
}

static void count_all(ll *cnt) {
    memset(cnt, 0, sizeof(ll) * (K + 1));
    for (int a = 0; a < N; a++) anchor_count(a, -1, cnt);
}

static void count_through(int p, ll *cnt) {
    memset(cnt, 0, sizeof(ll) * (K + 1));
    for (int a = 0; a < N; a++)
        if (a == p || below(a, p)) anchor_count(a, p, cnt);
}

static int read_points(const char *fn, ll *xs, ll *ys) {
    FILE *f = fopen(fn, "r");
    if (!f) { perror(fn); exit(2); }
    int n = 0;
    while (n < MAXN && fscanf(f, "%lld %lld", &xs[n], &ys[n]) == 2) n++;
    fclose(f);
    return n;
}

static void write_points(const char *fn) {
    FILE *f = fopen(fn, "w");
    for (int i = 0; i < N; i++) fprintf(f, "%lld %lld\n", X[i], Y[i]);
    fclose(f);
}

static double now(void) {
    struct timespec t; clock_gettime(CLOCK_MONOTONIC, &t);
    return t.tv_sec + 1e-9 * t.tv_nsec;
}

static ll xspan, yspan;
static void spans(void) {
    ll x0 = X[0], x1 = X[0], y0 = Y[0], y1 = Y[0];
    for (int i = 1; i < N; i++) {
        if (X[i] < x0) x0 = X[i];
        if (X[i] > x1) x1 = X[i];
        if (Y[i] < y0) y0 = Y[i];
        if (Y[i] > y1) y1 = Y[i];
    }
    xspan = x1 - x0 + 1; yspan = y1 - y0 + 1;
}

static ll logstep(ll span) { /* signed step, log-uniform magnitude in [1, span] */
    double mag = exp(urand() * log((double)span));
    ll s = (ll)mag;
    if (s < 1) s = 1;
    return (rnd() & 1) ? s : -s;
}

/* Propose a new position for point p. */
static void propose(int p, ll *nx, ll *ny) {
    double r = urand();
    if (r < 0.7) {           /* local move at a random scale */
        *nx = X[p]; *ny = Y[p];
        int ax = rnd() % 3;
        if (ax != 1) *nx += logstep(xspan);
        if (ax != 0) *ny += logstep(yspan);
    } else if (r < 0.9) {    /* jump next to another point */
        int q = rnd() % N;
        *nx = X[q] + logstep(xspan / 4 + 1);
        *ny = Y[q] + logstep(yspan / 4 + 1);
    } else {                 /* anywhere near the bounding box */
        int q = rnd() % N;
        *nx = X[q] + (ll)(grand() * xspan);
        *ny = Y[q] + (ll)(grand() * yspan);
    }
}

static int try_move(int p, ll nx, ll ny) {
    if (nx <= -LIM || nx >= LIM || ny <= -LIM || ny >= LIM) return 0;
    X[p] = nx; Y[p] = ny;
    return set_orients(p);
}

static double energy_of(const ll *c, double mu) { return c[7] + mu * c[6]; }

/* One annealing pass. Returns best c7; best configuration in bx, by. */
static ll anneal(long iters, double T0, double T1, double mu, ll *bx, ll *by,
                 ll *bestc6, long *accepted) {
    ll cur[K + 1]; count_all(cur);
    ll best = cur[7]; *bestc6 = cur[6];
    memcpy(bx, X, sizeof(ll) * N); memcpy(by, Y, sizeof(ll) * N);
    *accepted = 0;
    for (long it = 0; it < iters && best > 0; it++) {
        double T = T0 * pow(T1 / T0, (double)it / iters);
        int p = rnd() % N;
        ll ox = X[p], oy = Y[p], nx, ny;
        ll before[K + 1], after[K + 1];
        count_through(p, before);
        propose(p, &nx, &ny);
        if (!try_move(p, nx, ny)) { X[p] = ox; Y[p] = oy; set_orients(p); continue; }
        count_through(p, after);
        double dE = energy_of(after, mu) - energy_of(before, mu);
        if (dE <= 0 || urand() < exp(-dE / T)) {
            for (int k = 3; k <= K; k++) cur[k] += after[k] - before[k];
            (*accepted)++;
            if (cur[7] < best || (cur[7] == best && cur[6] < *bestc6)) {
                best = cur[7]; *bestc6 = cur[6];
                memcpy(bx, X, sizeof(ll) * N); memcpy(by, Y, sizeof(ll) * N);
            }
            if ((it & 4095) == 0) spans();
        } else {
            X[p] = ox; Y[p] = oy; set_orients(p);
        }
    }
    return best;
}

/* Random walk on 32 points that keeps the set free of convex 7-gons. */
static long neutral_walk(long steps) {
    long acc = 0;
    for (long it = 0; it < steps; it++) {
        int p = rnd() % N;
        ll ox = X[p], oy = Y[p], nx, ny;
        propose(p, &nx, &ny);
        if (try_move(p, nx, ny)) {
            ll c[K + 1]; count_through(p, c);
            if (c[7] == 0) { acc++; continue; }
        }
        X[p] = ox; Y[p] = oy; set_orients(p);
    }
    return acc;
}

int main(int argc, char **argv) {
    if (argc >= 3 && !strcmp(argv[1], "count")) {
        N = read_points(argv[2], X, Y);
        int gp = build_all();
        ll c[K + 1]; count_all(c);
        printf("N=%d general_position=%d", N, gp);
        for (int k = 3; k <= K; k++) printf(" c%d=%lld", k, c[k]);
        printf("\n");
        /* self-check of the incremental count */
        for (int p = 0; p < N; p++) {
            ll t[K + 1], r[K + 1];
            count_through(p, t);
            ll sx = X[p], sy = Y[p];
            int last = N - 1;
            X[p] = X[last]; Y[p] = Y[last]; N--; build_all(); count_all(r);
            N++; X[p] = sx; Y[p] = sy; X[last] = X[last]; build_all();
            for (int k = 3; k <= K; k++)
                if (r[k] + t[k] != c[k]) { printf("SELFCHECK FAIL p=%d k=%d\n", p, k); return 1; }
            /* restore order: the swap above overwrote p with the last point */
            (void)sy;
        }
        printf("selfcheck ok\n");
        return 0;
    }
    if (argc < 6 || strcmp(argv[1], "run")) {
        fprintf(stderr, "usage: lbs count FILE | lbs run SEED SECONDS OUTPREFIX BASE...\n");
        return 2;
    }
    u64 seed = strtoull(argv[2], 0, 10);
    rs = seed * 0x9E3779B97F4A7C15ULL + 12345;
    double deadline = now() + atof(argv[3]);
    const char *pre = argv[4];
    int nbase = argc - 5;
    char fn[512];
    snprintf(fn, sizeof fn, "%s.log", pre);
    FILE *lg = fopen(fn, "a");
    snprintf(fn, sizeof fn, "%s.sets", pre);
    FILE *sets = fopen(fn, "a");
    ll gbest = 1LL << 60;
    for (int run = 0; now() < deadline; run++) {
        int b = rnd() % nbase;
        N = read_points(argv[5 + b], X, Y);
        if (N != 32 || !build_all()) { fprintf(stderr, "bad base %s\n", argv[5 + b]); return 2; }
        ll c[K + 1]; count_all(c);
        if (c[7]) { fprintf(stderr, "base has 7-gons\n"); return 2; }
        spans();
        static const long walks[] = {0, 1000, 10000, 50000};
        long wl = walks[rnd() % 4];
        long wacc = neutral_walk(wl);
        spans();
        /* add the 33rd point */
        N = 33;
        int ncand = 4000, valid = 0;
        ll emin = 1LL << 60, nmin = 0, ex = 0, ey = 0;
        ll hist[8] = {0};
        for (int t = 0; t < ncand; t++) {
            ll nx, ny;
            propose(rnd() % 32, &nx, &ny);
            if (!try_move(32, nx, ny)) continue;
            valid++;
            ll tc[K + 1]; count_through(32, tc);
            hist[tc[7] < 7 ? tc[7] : 7]++;
            if (tc[7] < emin || (tc[7] == emin && rnd() % (nmin + 1) == 0)) {
                if (tc[7] < emin) nmin = 0;
                emin = tc[7]; ex = nx; ey = ny;
            }
            if (tc[7] == emin) nmin++;
        }
        X[32] = ex; Y[32] = ey;
        if (!build_all()) { fprintf(stderr, "internal: extension not in GP\n"); return 3; }
        spans();
        static const double T0s[] = {0.3, 0.6, 1.0, 2.0, 4.0};
        static const double mus[] = {0, 0, 0.002, 0.01, 0.05};
        double T0 = T0s[rnd() % 5], T1 = 0.05 + 0.1 * urand(), mu = mus[rnd() % 5];
        long iters = (rnd() & 1) ? 100000 : 300000;
        ll bx[MAXN], by[MAXN], bc6; long acc;
        double t0 = now();
        ll best = anneal(iters, T0, T1, mu, bx, by, &bc6, &acc);
        ll fin[K + 1]; count_all(fin);
        memcpy(X, bx, sizeof X); memcpy(Y, by, sizeof Y);
        if (!build_all()) { fprintf(stderr, "internal: best not in GP\n"); return 3; }
        ll chk[K + 1]; count_all(chk);
        if (chk[7] != best) { fprintf(stderr, "internal: count mismatch\n"); return 3; }
        fprintf(lg, "run=%d base=%d walk=%ld walkacc=%ld ext_valid=%d ext_min=%lld ext_nmin=%lld "
                "ext_hist=%lld,%lld,%lld,%lld,%lld,%lld,%lld,%lld T0=%.2f T1=%.3f mu=%.3f iters=%ld "
                "acc=%ld final=%lld best=%lld best_c6=%lld secs=%.1f\n",
                run, b, wl, wacc, valid, emin, nmin, hist[0], hist[1], hist[2], hist[3], hist[4],
                hist[5], hist[6], hist[7], T0, T1, mu, iters, acc, fin[7], best, bc6, now() - t0);
        fflush(lg);
        if (best <= 1) {
            fprintf(sets, "seed=%llu run=%d c7=%lld c6=%lld", (unsigned long long)seed, run, best, bc6);
            for (int i = 0; i < N; i++) fprintf(sets, " %lld,%lld", X[i], Y[i]);
            fprintf(sets, "\n"); fflush(sets);
        }
        if (best < gbest || best == 0) {
            gbest = best;
            snprintf(fn, sizeof fn, "%s.best.txt", pre);
            write_points(fn);
        }
        if (best == 0) {
            snprintf(fn, sizeof fn, "%s.ZERO.txt", pre);
            write_points(fn);
            fprintf(lg, "ZERO FOUND run=%d\n", run); fflush(lg);
            return 0;
        }
    }
    fclose(lg); fclose(sets);
    return 0;
}
