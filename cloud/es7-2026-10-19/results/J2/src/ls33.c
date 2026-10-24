/*
 * ls33.c -- batch short local search for PatternBoost (task J2).
 * Reuses gen_core.h (exact __int128 orientations, exact convex k-gon DP count,
 * multi-scale move proposals) from tools/trackA.
 *
 * usage: ls33 K iters T0 T1 seed < sets > out
 *   input lines:  n x1 y1 ... xn yn   (integers; rescaled into |c| < 2^25 if needed,
 *                 duplicate/collinear points are nudged until general position)
 *   output lines: E0 Ebest c6best n x1 y1 ... (best state seen, E = #convex K-gons)
 * Annealing: energy log(1+E_K), Metropolis, temperature T0 -> T1 geometric;
 * stops early if E reaches 0.  The best state is the lexicographic minimum of
 * (E_K, E_{K-1}) over visited states (ties in E_K broken by fewer (K-1)-gons).  Every output set is re-verified from scratch.
 */
#include "gen_core.h"

/* 1 iff (x,y) is in range and in general position with points 0..p-1 */
static int prefix_ok(int p, ll x, ll y) {
    if (!in_range(x, y)) return 0;
    for (int i = 0; i < p; i++) {
        if (X[i] == x && Y[i] == y) return 0;
        for (int j = i + 1; j < p; j++)
            if (orient3(x, y, X[i], Y[i], X[j], Y[j]) == 0) return 0;
    }
    return 1;
}

static void fix_gp(void) {
    for (int p = 0; p < N; p++) {
        int tries = 0;
        while (!prefix_ok(p, X[p], Y[p])) {
            ll r = 3 + tries / 50;                 /* growing nudge radius */
            ll nx = X[p] + (ll)(rnd() % (uint64_t)(2 * r + 1)) - r;
            ll ny = Y[p] + (ll)(rnd() % (uint64_t)(2 * r + 1)) - r;
            if (in_range(nx, ny)) { X[p] = nx; Y[p] = ny; }
            else { X[p] /= 2; Y[p] /= 2; }
            if (++tries > 1000000) { fprintf(stderr, "cannot fix gp\n"); exit(3); }
        }
    }
}

int main(int argc, char **argv) {
    if (argc < 6) { fprintf(stderr, "usage\n"); return 2; }
    int K = atoi(argv[1]); long iters = atol(argv[2]);
    double T0 = atof(argv[3]), T1 = atof(argv[4]);
    seed_rng((uint64_t)atoll(argv[5]));
    int n;
    static ll BX[MAXN], BY[MAXN];
    while (scanf("%d", &n) == 1) {
        N = n;
        ll mx = 0, x0 = 0, x1 = 0, y0 = 0, y1 = 0;
        for (int i = 0; i < n; i++) {
            if (scanf("%lld %lld", &X[i], &Y[i]) != 2) return 2;
            if (!i || X[i] < x0) x0 = X[i]; if (!i || X[i] > x1) x1 = X[i];
            if (!i || Y[i] < y0) y0 = Y[i]; if (!i || Y[i] > y1) y1 = Y[i];
        }
        for (int i = 0; i < n; i++) {         /* translation keeps the order type */
            X[i] -= (x0 + x1) / 2; Y[i] -= (y0 + y1) / 2;
            if (llabs(X[i]) > mx) mx = llabs(X[i]);
            if (llabs(Y[i]) > mx) mx = llabs(Y[i]);
        }
        if (mx >= (1LL << 26)) {               /* lossy: only for oversized inputs */
            int sh = 0; while ((mx >> sh) >= (1LL << 26)) sh++;
            for (int i = 0; i < n; i++) { X[i] >>= sh; Y[i] >>= sh; }
        }
        fix_gp();
        if (!general_position_all()) { fprintf(stderr, "BUG gp\n"); return 3; }
        build_orients();
        u64 cc[MAXN + 1];
        count_kgons(K, cc);
        u64 E = cc[K], E0 = E, Eb = E, Hb = cc[K - 1];
        memcpy(BX, X, sizeof(ll) * N); memcpy(BY, Y, sizeof(ll) * N);
        for (long it = 0; it < iters && Eb > 0; it++) {
            double T = T0 * pow(T1 / T0, (double)it / (double)iters);
            int p = (int)(rnd() % (uint64_t)N);
            ll nx, ny;
            propose(p, &nx, &ny);
            if (!candidate_ok(p, nx, ny)) continue;
            ll ox = X[p], oy = Y[p];
            X[p] = nx; Y[p] = ny;
            set_point_orients(p);
            count_kgons(K, cc);
            u64 E2 = cc[K];
            double dE = log1p((double)E2) - log1p((double)E);
            if (E2 <= E || urand() < exp(-dE / T)) {
                E = E2;
                if (E < Eb || (E == Eb && cc[K - 1] < Hb)) { Eb = E; Hb = cc[K - 1]; memcpy(BX, X, sizeof(ll) * N); memcpy(BY, Y, sizeof(ll) * N); }
            } else { X[p] = ox; Y[p] = oy; set_point_orients(p); }
        }
        memcpy(X, BX, sizeof(ll) * N); memcpy(Y, BY, sizeof(ll) * N);
        if (!general_position_all()) { fprintf(stderr, "BUG gp out\n"); return 3; }
        build_orients();
        u64 c[MAXN + 1];
        count_kgons(K, c);
        if (c[K] != Eb || c[K - 1] != Hb) { fprintf(stderr, "BUG recount %llu %llu\n", c[K], Eb); return 3; }
        printf("%llu %llu %llu %d", E0, Eb, c[K - 1], N);
        for (int i = 0; i < N; i++) printf(" %lld %lld", X[i], Y[i]);
        printf("\n");
        fflush(stdout);
    }
    return 0;
}
