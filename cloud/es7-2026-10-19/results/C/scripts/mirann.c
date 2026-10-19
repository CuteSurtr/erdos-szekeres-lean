/*
 * mirann.c -- mirror-preserving simulated annealing for convex k-gon-free point sets,
 * with an exact axis scan.  Task C, Part 3.
 *
 * State: P "representative" points (x_r, y_r) with x_r > 0, mirrored to (-x_r, y_r), plus
 * A in {0,1} axis points (0, y0).  N = 2P + A.  Energy = exact number of convex K-gons
 * (DP of tools/trackA/cgon.c; every geometric decision is an exact __int128 orientation sign).
 * A move relocates one representative (and so its mirror image) or the axis point (y only).
 *
 * Axis scan (exact): for a K-gon-free mirror set with A = 0, every line through two of its
 * points meets the axis x = 0 in a rational t = (y1 x2 - y2 x1)/(x2 - x1) (pairs with x1 = x2
 * are vertical and miss the axis; a mirror pair gives t = y).  On each open interval between
 * consecutive values, and beyond the extremes, the order type of the set plus (0,t) is
 * constant, so testing one rational t per interval decides exactly whether some axis point
 * can be added without creating a convex K-gon.  Orientations with the rational point are
 * signs of (ax*by - ay*bx)*d + n*(bx - ax) for t = n/d, d > 0, computed in __int128.
 *
 * usage:
 *   mirann anneal K P A iters T0 T1 seed runs outprefix [init-file]
 *       `runs` independent annealing runs from random starts (or from init-file, a list of
 *       N points "x y" in the internal order: rep, mirror, rep, mirror, ..., axis).
 *       For A = 0 every K-gon-free set found is axis-scanned.  For A = 1, whenever the
 *       2P pair points alone are K-gon free, they are axis-scanned as well.
 *   mirann scan K < pts      exact axis scan of a mirror-symmetric set (A = 0) read from stdin
 *   mirann count K < pts     exact convex k-gon counts
 */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MAXN 72
typedef long long ll;
typedef unsigned long long u64;
typedef __int128 i128;

static const ll COORD_LIMIT = (1LL << 26);
static int N;
static ll X[MAXN], Y[MAXN];
static signed char O[MAXN][MAXN][MAXN];
static int RANK[MAXN];          /* position in the (y, x) order; anchor = lowest vertex */

static int sgn128(i128 v) { return (v > 0) - (v < 0); }
static int orient3(ll ax, ll ay, ll bx, ll by, ll cx, ll cy) {
    return sgn128((i128)(bx - ax) * (cy - ay) - (i128)(by - ay) * (cx - ax));
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
                O[i][j][k] = (i == j || j == k || i == k) ? 0 : orient3(X[i], Y[i], X[j], Y[j], X[k], Y[k]);
}
static void build_rank_int(void) {
    for (int a = 0; a < N; a++) {
        int r = 0;
        for (int b = 0; b < N; b++)
            if (b != a && (Y[b] < Y[a] || (Y[b] == Y[a] && X[b] < X[a]))) r++;
        RANK[a] = r;
    }
}
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
/* general position for the points in mv[] (already placed): every triple containing one of them */
static int gp_moved(const int *mv, int nm) {
    for (int t = 0; t < nm; t++) {
        int p = mv[t];
        if (!in_range(X[p], Y[p])) return 0;
        for (int i = 0; i < N; i++) {
            if (i == p) continue;
            if (X[i] == X[p] && Y[i] == Y[p]) return 0;
            for (int j = i + 1; j < N; j++) {
                if (j == p) continue;
                if (orient3(X[p], Y[p], X[i], Y[i], X[j], Y[j]) == 0) return 0;
            }
        }
    }
    return 1;
}

/* counts[k] = number of convex k-subsets, k = 3..K (cgon.c DP; the anchor is the lowest
 * vertex in the RANK order, points above it are sorted by angle using O only). */
static int count_kgons(int K, u64 *counts) {
    static int q[MAXN];
    static int incl[MAXN][MAXN + 1], posi[MAXN][MAXN + 1], outl[MAXN][MAXN], cutv[MAXN][MAXN];
    static u64 g[2][MAXN][MAXN + 1];
    static u64 Pf[MAXN + 2];
    for (int k = 0; k <= K; k++) counts[k] = 0;
    for (int a = 0; a < N; a++) {
        int m = 0;
        for (int b = 0; b < N; b++) if (b != a && RANK[b] > RANK[a]) q[m++] = b;
        if (m < 2) continue;
        for (int i = 1; i < m; i++) {
            int v = q[i], t = i - 1;
            while (t >= 0 && O[a][v][q[t]] > 0) { q[t + 1] = q[t]; t--; }
            q[t + 1] = v;
        }
        for (int j = 0; j < m; j++) {
            int pj = q[j], n_in = 1;
            incl[j][0] = -1;
            for (int i = 0; i < j; i++) {
                int t = n_in - 1;
                while (t >= 1 && O[pj][q[i]][q[incl[j][t]]] > 0) { incl[j][t + 1] = incl[j][t]; t--; }
                incl[j][t + 1] = i; n_in++;
            }
            for (int t = 0; t < n_in; t++) posi[j][incl[j][t] + 1] = t;
            int n_out = 0;
            for (int l = j + 1; l < m; l++) {
                int t = n_out - 1;
                while (t >= 0 && O[pj][q[l]][q[outl[j][t]]] > 0) { outl[j][t + 1] = outl[j][t]; t--; }
                outl[j][t + 1] = l; n_out++;
            }
            int p = 1;
            for (int t = 0; t < n_out; t++) {
                int l = outl[j][t];
                while (p < n_in && O[q[incl[j][p]]][pj][q[l]] > 0) p++;
                cutv[j][l] = p;
            }
        }
        int cur = 0;
        for (int j = 0; j < m; j++) { for (int t = 0; t <= j; t++) g[cur][j][t] = 0; g[cur][j][0] = 1; }
        for (int L = 2; L < K; L++) {
            int nx = cur ^ 1;
            for (int l = 0; l < m; l++) for (int t = 0; t <= l; t++) g[nx][l][t] = 0;
            u64 tot = 0;
            for (int j = 0; j < m; j++) {
                Pf[0] = 0;
                for (int t = 0; t <= j; t++) Pf[t + 1] = Pf[t] + g[cur][j][t];
                if (Pf[j + 1] == 0) continue;
                for (int l = j + 1; l < m; l++) { u64 v = Pf[cutv[j][l]]; g[nx][l][posi[l][j + 1]] = v; tot += v; }
            }
            counts[L + 1] += tot; cur = nx;
            if (tot == 0) break;
        }
    }
    int best = N < 2 ? N : 2;
    for (int k = 3; k <= K; k++) if (counts[k]) best = k;
    return best;
}
static u64 count_k(int K) { u64 c[MAXN + 1]; count_kgons(K, c); return c[K]; }

/* ---------- random numbers (xorshift128+) ---------- */
static uint64_t rs0 = 0x9E3779B97F4A7C15ULL, rs1 = 0xD1B54A32D192ED03ULL;
static uint64_t rnd(void) {
    uint64_t s1 = rs0, s0 = rs1; rs0 = s0; s1 ^= s1 << 23;
    rs1 = s1 ^ s0 ^ (s1 >> 17) ^ (s0 >> 26); return rs1 + s0;
}
static double urand(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static void seed_rng(uint64_t s) {
    rs0 ^= s * 0x9E3779B97F4A7C15ULL; rs1 ^= (s + 1) * 0xBF58476D1CE4E5B9ULL;
    for (int i = 0; i < 20; i++) rnd();
}
static ll scaled(double smax) { double s = urand() * smax; return (ll)llround((2.0 * urand() - 1.0) * pow(2.0, s)); }

/* ---------- mirror state ---------- */
static int P_, A_, K_;
static void place_rep(int r, ll x, ll y) { X[2 * r] = x; Y[2 * r] = y; X[2 * r + 1] = -x; Y[2 * r + 1] = y; }
static double log2_extent(void) {
    ll mx = 1, my0 = Y[0], my1 = Y[0];
    for (int i = 0; i < N; i++) { if (llabs(X[i]) > mx) mx = llabs(X[i]); if (Y[i] < my0) my0 = Y[i]; if (Y[i] > my1) my1 = Y[i]; }
    ll e = 2 * mx; if (my1 - my0 > e) e = my1 - my0;
    return log2((double)e + 2.0);
}
static int is_mirror_symmetric(void) {
    for (int r = 0; r < P_; r++) if (X[2 * r] <= 0 || X[2 * r + 1] != -X[2 * r] || Y[2 * r + 1] != Y[2 * r]) return 0;
    for (int i = 2 * P_; i < N; i++) if (X[i] != 0) return 0;
    return 1;
}

/* ---------- exact axis scan ---------- */
typedef struct { i128 n, d; } rat;   /* d > 0 */
static int ratcmp(const rat *a, const rat *b) { return sgn128(a->n * b->d - b->n * a->d); }
static int cmp_rat(const void *pa, const void *pb) { return ratcmp((const rat *)pa, (const rat *)pb); }
static rat TS[MAXN * MAXN];
/* Returns the minimum number of convex K-gons over all axis positions for the current
 * A = 0 set (N = 2P points); *nint = number of intervals tested; best t in *bt. */
static u64 axis_scan(int K, int *nint, rat *bt, u64 *zero_count) {
    int n0 = N, m = 0;
    for (int i = 0; i < n0; i++)
        for (int j = i + 1; j < n0; j++) {
            if (X[i] == X[j]) continue;
            rat t; t.n = (i128)Y[i] * X[j] - (i128)Y[j] * X[i]; t.d = (i128)X[j] - X[i];
            if (t.d < 0) { t.n = -t.n; t.d = -t.d; }
            TS[m++] = t;
        }
    qsort(TS, m, sizeof(rat), cmp_rat);
    int u = 0;
    for (int i = 0; i < m; i++) if (u == 0 || ratcmp(&TS[u - 1], &TS[i]) != 0) TS[u++] = TS[i];
    /* candidates: below the first, midpoints, above the last */
    u64 best = ~0ULL; *nint = 0; *zero_count = 0;
    int c = n0; N = n0 + 1; X[c] = 0; Y[c] = 0;
    for (int s = 0; s <= u; s++) {
        rat t;
        if (s == 0) { t.n = TS[0].n - TS[0].d; t.d = TS[0].d; }
        else if (s == u) { t.n = TS[u - 1].n + TS[u - 1].d; t.d = TS[u - 1].d; }
        else { t.n = TS[s - 1].n * TS[s].d + TS[s].n * TS[s - 1].d; t.d = 2 * TS[s - 1].d * TS[s].d; }
        /* orientations with q = (0, t) */
        for (int i = 0; i < n0; i++)
            for (int j = 0; j < n0; j++) {
                if (i == j) { O[c][i][j] = 0; continue; }
                /* orient(q, a, b) = (ax*by - ay*bx) + t (bx - ax) */
                i128 v = ((i128)X[i] * Y[j] - (i128)Y[i] * X[j]) * t.d + t.n * ((i128)X[j] - X[i]);
                int sg = sgn128(v);
                if (sg == 0) { fprintf(stderr, "BUG: collinear axis candidate\n"); exit(3); }
                O[c][i][j] = sg; O[i][j][c] = sg; O[j][c][i] = sg;
            }
        O[c][c][c] = 0;
        for (int i = 0; i < n0; i++) { O[c][c][i] = O[c][i][c] = O[i][c][c] = 0; }
        /* rank of q in the (y,x) order: compare t with integer y (x of q is 0) */
        for (int a = 0; a < n0; a++) {
            int r = 0;
            for (int b = 0; b < n0; b++) if (b != a && (Y[b] < Y[a] || (Y[b] == Y[a] && X[b] < X[a]))) r++;
            i128 diff = t.n - (i128)Y[a] * t.d;   /* sign(t - y_a) */
            if (diff == 0) { fprintf(stderr, "BUG: tie\n"); exit(3); }
            if (diff < 0) r++;                     /* q is below a */
            RANK[a] = r;
        }
        { int r = 0; for (int b = 0; b < n0; b++) { i128 diff = t.n - (i128)Y[b] * t.d; if (diff > 0) r++; } RANK[c] = r; }
        u64 e = count_k(K);
        (*nint)++;
        if (e == 0) (*zero_count)++;
        if (e < best) { best = e; *bt = t; }
    }
    N = n0;
    build_rank_int();
    return best;
}
static void print_i128(FILE *f, i128 v) {
    char buf[64]; int n = 0, neg = v < 0; unsigned __int128 u = neg ? -(unsigned __int128)v : (unsigned __int128)v;
    if (u == 0) buf[n++] = '0';
    while (u) { buf[n++] = '0' + (int)(u % 10); u /= 10; }
    if (neg) fputc('-', f);
    while (n) fputc(buf[--n], f);
}
static void write_points(const char *path, const char *mode, const char *tag) {
    FILE *f = fopen(path, mode); if (!f) { perror(path); exit(2); }
    fprintf(f, "%s %d", tag, N);
    for (int i = 0; i < N; i++) fprintf(f, " %lld %lld", X[i], Y[i]);
    fprintf(f, "\n"); fclose(f);
}

static int mode_anneal(int K, int P, int A, long iters, double T0, double T1, uint64_t seed, int runs,
                       const char *pre, const char *init) {
    P_ = P; A_ = A; K_ = K; N = 2 * P + A;
    seed_rng(seed);
    char fbest[512], fzero[512], fscan[512];
    snprintf(fbest, sizeof fbest, "%s.best", pre); snprintf(fzero, sizeof fzero, "%s.zero", pre);
    snprintf(fscan, sizeof fscan, "%s.scan", pre);
    u64 global_best = ~0ULL;
    for (int run = 0; run < runs; run++) {
        clock_t t0 = clock();
        if (init) {
            FILE *f = fopen(init, "r"); if (!f) { perror(init); return 2; }
            for (int i = 0; i < N; i++) if (fscanf(f, "%lld %lld", &X[i], &Y[i]) != 2) { fprintf(stderr, "short init\n"); return 2; }
            fclose(f);
            if (!is_mirror_symmetric() || !general_position_all()) { fprintf(stderr, "bad init\n"); return 2; }
        } else {
            ll R = 1 << 20;
            for (;;) {
                for (int r = 0; r < P; r++) place_rep(r, 1 + (ll)(rnd() % (uint64_t)R), (ll)(rnd() % (uint64_t)(2 * R)) - R);
                for (int i = 2 * P; i < N; i++) { X[i] = 0; Y[i] = (ll)(rnd() % (uint64_t)(2 * R)) - R; }
                if (general_position_all()) break;
            }
        }
        build_orients(); build_rank_int();
        u64 E = count_k(K), bestE = E;
        ll BX[MAXN], BY[MAXN]; memcpy(BX, X, sizeof X); memcpy(BY, Y, sizeof Y);
        long acc = 0, gprej = 0, it;
        int pairs_dirty = 1; long nscans = 0; u64 scan_min = ~0ULL;
        for (it = 0; it < iters && bestE > 0; it++) {
            double T = T0 * pow(T1 / T0, (double)it / (double)iters);
            int pick = (int)(rnd() % (uint64_t)(P + A));
            int mv[2], nm;
            ll ox[2], oy[2];
            double smax = log2_extent() + 1.0;
            if (pick < P) {
                int r = pick; mv[0] = 2 * r; mv[1] = 2 * r + 1; nm = 2;
                ox[0] = X[2 * r]; oy[0] = Y[2 * r];
                ll nx, ny; double u = urand();
                if (u < 0.6) { nx = X[2 * r] + scaled(smax); ny = Y[2 * r] + scaled(smax); }
                else if (u < 0.85) { int j = (int)(rnd() % (uint64_t)N); nx = llabs(X[j]) + scaled(smax * 0.6); ny = Y[j] + scaled(smax * 0.6); }
                else if (u < 0.95) { if (rnd() & 1) { nx = X[2 * r] + scaled(smax); ny = Y[2 * r]; } else { nx = X[2 * r]; ny = Y[2 * r] + scaled(smax); } }
                else { nx = 1 + (ll)(urand() * (double)(1LL << (int)fmin(smax, 25))); ny = Y[(int)(rnd() % (uint64_t)N)] + scaled(smax); }
                if (nx < 0) nx = -nx;
                if (nx == 0) { gprej++; continue; }
                place_rep(r, nx, ny);
                if (!gp_moved(mv, nm)) { place_rep(r, ox[0], oy[0]); gprej++; continue; }
                set_point_orients(mv[0]); set_point_orients(mv[1]);
            } else {
                int c = 2 * P; mv[0] = c; nm = 1; oy[0] = Y[c];
                ll ny = (urand() < 0.7) ? Y[c] + scaled(smax) : Y[(int)(rnd() % (uint64_t)N)] + scaled(smax * 0.5);
                Y[c] = ny;
                if (!gp_moved(mv, nm)) { Y[c] = oy[0]; gprej++; continue; }
                set_point_orients(c);
            }
            build_rank_int();
            u64 E2 = count_k(K);
            double dE = log1p((double)E2) - log1p((double)E);
            if (E2 <= E || urand() < exp(-dE / T)) {
                E = E2; acc++;
                if (E < bestE) { bestE = E; memcpy(BX, X, sizeof X); memcpy(BY, Y, sizeof Y); }
                /* A = 1: are the pair points alone K-gon free? then axis-scan them exactly */
                if (pick < P) pairs_dirty = 1;
                if (A == 1 && E <= 64 && pairs_dirty) {
                    int n1 = N, c = 2 * P; ll sx = X[c], sy = Y[c];
                    N = 2 * P; build_rank_int();
                    u64 E32 = count_k(K);
                    if (E32 == 0) {
                        int nint; rat bt; u64 zc;
                        u64 m = axis_scan(K, &nint, &bt, &zc);
                        nscans++; if (m < scan_min) scan_min = m;
                        FILE *f = fopen(fscan, "a");
                        fprintf(f, "run=%d it=%ld E33=%llu pairs_free=1 intervals=%d min_axis_E=%llu zero_intervals=%llu t=", run, it, E, nint, m, zc);
                        print_i128(f, bt.n); fprintf(f, "/"); print_i128(f, bt.d); fprintf(f, "\n"); fclose(f);
                        if (m == 0) write_points(fzero, "a", "AXIS_ZERO_BASE");
                    }
                    pairs_dirty = 0;
                    N = n1; X[c] = sx; Y[c] = sy; set_point_orients(c); build_rank_int();
                }
            } else {
                if (pick < P) { place_rep(pick, ox[0], oy[0]); set_point_orients(mv[0]); set_point_orients(mv[1]); }
                else { Y[2 * P] = oy[0]; set_point_orients(2 * P); }
                build_rank_int();
            }
        }
        memcpy(X, BX, sizeof X); memcpy(Y, BY, sizeof Y);
        build_orients(); build_rank_int();
        if (!general_position_all() || !is_mirror_symmetric()) { fprintf(stderr, "BUG: best invalid\n"); return 3; }
        u64 check = count_k(K);
        if (check != bestE) { fprintf(stderr, "BUG: recount mismatch\n"); return 3; }
        char tag[128]; snprintf(tag, sizeof tag, "K%d_P%d_A%d_seed%llu_run%d_E%llu", K, P, A, (unsigned long long)seed, run, bestE);
        write_points(fbest, "a", tag);
        double cpu = (double)(clock() - t0) / CLOCKS_PER_SEC;
        if (bestE < global_best) global_best = bestE;
        printf("run=%d K=%d P=%d A=%d seed=%llu best=%llu iters=%ld acc=%ld gprej=%ld cpu=%.1fs", run, K, P, A,
               (unsigned long long)seed, bestE, it, acc, gprej, cpu);
        if (A == 1) printf(" pair_scans=%ld pair_scan_min=%lld", nscans, nscans ? (long long)scan_min : -1LL);
        if (A == 0 && bestE == 0) {
            write_points(fzero, "a", tag);
            int nint; rat bt; u64 zc;
            u64 m = axis_scan(K, &nint, &bt, &zc);
            printf(" axis_scan_intervals=%d axis_min_E=%llu axis_zero_intervals=%llu", nint, m, zc);
            FILE *f = fopen(fscan, "a");
            fprintf(f, "%s intervals=%d min_axis_E=%llu zero_intervals=%llu t=", tag, nint, m, zc);
            print_i128(f, bt.n); fprintf(f, "/"); print_i128(f, bt.d); fprintf(f, "\n"); fclose(f);
        }
        printf("\n"); fflush(stdout);
    }
    printf("global_best=%llu\n", global_best);
    return 0;
}
static int read_points(FILE *f) {
    N = 0; ll x, y;
    while (fscanf(f, "%lld %lld", &x, &y) == 2) {
        if (N >= MAXN) { fprintf(stderr, "too many points\n"); exit(2); }
        if (!in_range(x, y)) { fprintf(stderr, "coordinate out of range\n"); exit(2); }
        X[N] = x; Y[N] = y; N++;
    }
    return N;
}
int main(int argc, char **argv) {
    if (argc >= 3 && !strcmp(argv[1], "count")) {
        int K = atoi(argv[2]); read_points(stdin);
        if (!general_position_all()) { printf("NOT_GENERAL_POSITION\n"); return 1; }
        build_orients(); build_rank_int();
        u64 c[MAXN + 1]; int best = count_kgons(K, c);
        printf("N=%d", N); for (int k = 3; k <= K; k++) printf(" c%d=%llu", k, c[k]); printf(" maxconvex=%d\n", best);
        return 0;
    }
    if (argc >= 3 && !strcmp(argv[1], "scan")) {
        int K = atoi(argv[2]); read_points(stdin);
        if (!general_position_all()) { printf("NOT_GENERAL_POSITION\n"); return 1; }
        /* the set must be mirror symmetric about x = 0 with no point on the axis */
        for (int i = 0; i < N; i++) {
            int ok = 0; if (X[i] == 0) { printf("POINT_ON_AXIS\n"); return 1; }
            for (int j = 0; j < N; j++) if (X[j] == -X[i] && Y[j] == Y[i]) ok = 1;
            if (!ok) { printf("NOT_SYMMETRIC\n"); return 1; }
        }
        build_orients(); build_rank_int();
        u64 e0 = count_k(K);
        int nint; rat bt; u64 zc;
        u64 m = axis_scan(K, &nint, &bt, &zc);
        printf("N=%d E_base=%llu intervals=%d min_axis_E=%llu zero_intervals=%llu t=", N, e0, nint, m, zc);
        print_i128(stdout, bt.n); printf("/"); print_i128(stdout, bt.d); printf("\n");
        return 0;
    }
    if (argc >= 3 && !strcmp(argv[1], "otcount")) {
        /* order-type input (any number of tables until EOF): "N  rank_0..rank_{N-1}  s_ijk for i<j<k"
         * (s = +1/-1 = orientation sign of points i,j,k; rank = position in a generic linear order
         * of the points by height, used only to pick the lowest vertex of each polygon) */
        int K = atoi(argv[2]), n;
        while (scanf("%d", &n) == 1) {
            N = n;
            for (int i = 0; i < N; i++) if (scanf("%d", &RANK[i]) != 1) return 2;
            for (int i = 0; i < N; i++) for (int j = i + 1; j < N; j++) for (int k = j + 1; k < N; k++) {
                int sg; if (scanf("%d", &sg) != 1) return 2;
                O[i][j][k] = sg; O[j][k][i] = sg; O[k][i][j] = sg; O[j][i][k] = -sg; O[i][k][j] = -sg; O[k][j][i] = -sg;
            }
            u64 c[MAXN + 1]; int best = count_kgons(K, c);
            printf("N=%d", N); for (int k = 3; k <= K; k++) printf(" c%d=%llu", k, c[k]); printf(" maxconvex=%d\n", best);
            fflush(stdout);
        }
        return 0;
    }
    if (argc >= 11 && !strcmp(argv[1], "anneal"))
        return mode_anneal(atoi(argv[2]), atoi(argv[3]), atoi(argv[4]), atol(argv[5]), atof(argv[6]), atof(argv[7]),
                           (uint64_t)atoll(argv[8]), atoi(argv[9]), argv[10], argc >= 12 ? argv[11] : NULL);
    fprintf(stderr, "usage: see header\n");
    return 2;
}
