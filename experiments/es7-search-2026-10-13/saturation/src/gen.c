/*
 * gen.c -- generator of K-gon-free point sets for the ES(7) saturation search.
 *
 * Reuses the exact counter, RNG and move proposals of cgon.c verbatim
 * (gen_core.h = cgon.c up to mode_count, with COORD_LIMIT lowered to 2^26 so
 * that every emitted set satisfies the |c| < 2^27 bound asserted by sat.c).
 *
 * Every emitted set is re-checked from scratch (general position, fresh
 * orientation table, exact K-gon count) before it is written.
 *
 * Output: one line per set:
 *   tag E canon canonm n x1 y1 ... xn yn
 * canon  = lexicographically minimal orientation signature over the labelings
 *          (hull vertex h, others in ccw angular order around h): an exact
 *          order-type invariant (orientation preserving);
 * canonm = min(canon, canon of the mirror image): order type up to reflection.
 * Signatures are hex of the packed bits [orient(L_i,L_j,L_k) > 0], i<j<k.
 *
 * Modes:
 *   gen walk K N seed nstarts init iters T0 T1 walkmoves emitevery out
 *      per start: init (file or random:R), anneal (as cgon, raw=0, mu=0) until
 *      E=0, then a random walk through K-gon-free configurations (proposal
 *      accepted iff the K-gon count stays 0); emit the first K-gon-free state
 *      and every `emitevery` accepted walk moves.
 *   gen near K N seed nstarts init iters T0 T1 walkmoves emitevery out
 *      anneal N points; walk with E <= 1; at every emission with E == 1 the
 *      unique K-gon's vertices are found (points whose removal gives E=0) and
 *      the K subsets of size N-1 are emitted (all K-gon-free). E == 0 states
 *      are emitted whole with tag ZERO (would be a counterexample candidate).
 *   gen canon < lines "n x1 y1 ..."  : print "canon canonm" per line
 */
#include "gen_core.h"

static int EMIT_N;
static unsigned char sigbuf[2][(MAXN * MAXN * MAXN) / 48 + 64];

static int nbytes_sig(int n) {
    long t = (long)n * (n - 1) * (n - 2) / 6;
    return (int)((t + 7) / 8);
}

/* signature for orientation sign s (+1 or -1); result into out (nb bytes) */
static void canon_sig(int s, unsigned char *out) {
    int nb = nbytes_sig(N);
    static unsigned char cur[(MAXN * MAXN * MAXN) / 48 + 64];
    int have = 0;
    int lab[MAXN];
    for (int h = 0; h < N; h++) {
        int start = -1;
        for (int a = 0; a < N && start < 0; a++) {
            if (a == h) continue;
            int ok = 1;
            for (int b = 0; b < N && ok; b++)
                if (b != h && b != a && s * O[h][a][b] <= 0) ok = 0;
            if (ok) start = a;
        }
        if (start < 0) continue; /* h not extreme */
        int m = 0;
        for (int b = 0; b < N; b++) if (b != h) lab[1 + m++] = b;
        lab[0] = h;
        for (int i = 2; i < N; i++) { /* insertion sort, b before c iff s*O[h][b][c] > 0 */
            int v = lab[i], t = i - 1;
            while (t >= 1 && s * O[h][v][lab[t]] > 0) { lab[t + 1] = lab[t]; t--; }
            lab[t + 1] = v;
        }
        if (lab[1] != start) { fprintf(stderr, "BUG canon start\n"); exit(3); }
        memset(cur, 0, nb);
        long bit = 0;
        for (int i = 0; i < N; i++)
            for (int j = i + 1; j < N; j++)
                for (int k = j + 1; k < N; k++, bit++)
                    if (s * O[lab[i]][lab[j]][lab[k]] > 0) cur[bit >> 3] |= (unsigned char)(0x80 >> (bit & 7));
        if (!have || memcmp(cur, out, nb) < 0) { memcpy(out, cur, nb); have = 1; }
    }
    if (!have) { fprintf(stderr, "BUG no hull vertex\n"); exit(3); }
}

static void put_hex(FILE *f, const unsigned char *b, int nb) {
    static const char *H = "0123456789abcdef";
    for (int i = 0; i < nb; i++) { fputc(H[b[i] >> 4], f); fputc(H[b[i] & 15], f); }
}

/* current global set (X,Y,N) -> line; verifies from scratch */
static void emit(FILE *f, const char *tag, int K, long *emitted) {
    if (!general_position_all()) { fprintf(stderr, "BUG emit: not general position\n"); exit(3); }
    build_orients();
    u64 E = count_k(K);
    int nb = nbytes_sig(N);
    canon_sig(1, sigbuf[0]);
    canon_sig(-1, sigbuf[1]);
    unsigned char *m = memcmp(sigbuf[0], sigbuf[1], nb) <= 0 ? sigbuf[0] : sigbuf[1];
    fprintf(f, "%s %llu ", tag, E);
    put_hex(f, sigbuf[0], nb); fputc(' ', f);
    put_hex(f, m, nb);
    fprintf(f, " %d", N);
    for (int i = 0; i < N; i++) fprintf(f, " %lld %lld", X[i], Y[i]);
    fputc('\n', f);
    (*emitted)++;
}

static void init_set(const char *init, int n) {
    if (strncmp(init, "random:", 7) == 0) {
        ll range = atoll(init + 7);
        N = 0;
        while (N < n) {
            ll x = (ll)(rnd() % (uint64_t)range), y = (ll)(rnd() % (uint64_t)range);
            if (candidate_ok(N, x, y)) { X[N] = x; Y[N] = y; N++; }
        }
    } else {
        FILE *f = fopen(init, "r");
        if (!f) { perror(init); exit(2); }
        read_points(f);
        fclose(f);
        if (N != n) { fprintf(stderr, "init has %d points, expected %d\n", N, n); exit(2); }
    }
    if (!general_position_all()) { fprintf(stderr, "init not in general position\n"); exit(2); }
    build_orients();
}

/* anneal (log energy, as cgon raw=0 mu=0) until E <= target; leaves the
 * current state at the first state reaching E <= target; returns final E */
static u64 anneal_to(int K, long iters, double T0, double T1, u64 target) {
    u64 E = count_k(K);
    for (long it = 0; it < iters && E > target; it++) {
        double T = T0 * pow(T1 / T0, (double)it / (double)iters);
        int p = (int)(rnd() % (uint64_t)N);
        ll nx, ny;
        propose(p, &nx, &ny);
        if (!candidate_ok(p, nx, ny)) continue;
        ll ox = X[p], oy = Y[p];
        X[p] = nx; Y[p] = ny;
        set_point_orients(p);
        u64 E2 = count_k(K);
        double dE = log1p((double)E2) - log1p((double)E);
        if (E2 <= E || urand() < exp(-dE / T)) E = E2;
        else { X[p] = ox; Y[p] = oy; set_point_orients(p); }
    }
    return E;
}

/* one walk step; accepted iff new count <= emax; returns 1 if accepted */
static int walk_step(int K, u64 emax, u64 *E) {
    int p = (int)(rnd() % (uint64_t)N);
    ll nx, ny;
    propose(p, &nx, &ny);
    if (!candidate_ok(p, nx, ny)) return 0;
    ll ox = X[p], oy = Y[p];
    X[p] = nx; Y[p] = ny;
    set_point_orients(p);
    u64 E2 = count_k(K);
    if (E2 <= emax) { *E = E2; return 1; }
    X[p] = ox; Y[p] = oy; set_point_orients(p);
    return 0;
}

static void emit_subsets(FILE *f, int K, long *emitted, int start_id) {
    /* current set has exactly one K-gon: emit S \ {v} for its K vertices */
    ll SX[MAXN], SY[MAXN];
    int n0 = N;
    memcpy(SX, X, sizeof X); memcpy(SY, Y, sizeof Y);
    int found = 0;
    for (int p = 0; p < n0; p++) {
        N = 0;
        for (int i = 0; i < n0; i++) if (i != p) { X[N] = SX[i]; Y[N] = SY[i]; N++; }
        build_orients();
        if (count_k(K) == 0) {
            char tag[64];
            snprintf(tag, sizeof tag, "NEAR%d_drop%d", start_id, p);
            emit(f, tag, K, emitted);
            found++;
        }
    }
    N = n0; memcpy(X, SX, sizeof X); memcpy(Y, SY, sizeof Y);
    build_orients();
    if (found != K) { fprintf(stderr, "BUG: E=1 but %d removable vertices\n", found); exit(3); }
}

static int mode_gen(int near, int K, int n, uint64_t seed, int nstarts, const char *init, long iters,
                    double T0, double T1, long walkmoves, long emitevery, const char *out) {
    seed_rng(seed);
    FILE *f = fopen(out, "a");
    if (!f) { perror(out); return 2; }
    long emitted = 0;
    clock_t t0 = clock();
    for (int s = 0; s < nstarts; s++) {
        init_set(init, n);
        u64 target = near ? 1 : 0;
        u64 E = anneal_to(K, iters, T0, T1, target);
        if (near && E > 1) {
            /* keep annealing toward 1 from wherever we are */
            fprintf(stderr, "start %d: anneal ended at E=%llu (no emission)\n", s, E);
            continue;
        }
        if (E > target) {
            fprintf(stderr, "start %d: anneal ended at E=%llu (no emission)\n", s, E);
            continue;
        }
        char tag[64];
        long acc = 0, tried = 0;
        if (near) {
            if (E == 0) { snprintf(tag, sizeof tag, "ZERO%d", s); emit(f, tag, K, &emitted); }
            else emit_subsets(f, K, &emitted, s);
        } else {
            snprintf(tag, sizeof tag, "S%d_w0", s);
            emit(f, tag, K, &emitted);
        }
        long since = 0;
        while (acc < walkmoves && tried < walkmoves * 200) {
            tried++;
            if (walk_step(K, target, &E)) {
                acc++; since++;
                if (near && E == 0) { snprintf(tag, sizeof tag, "ZERO%d", s); emit(f, tag, K, &emitted); since = 0; continue; }
                if (since >= emitevery) {
                    since = 0;
                    if (near) emit_subsets(f, K, &emitted, s);
                    else { snprintf(tag, sizeof tag, "S%d_w%ld", s, acc); emit(f, tag, K, &emitted); }
                }
            }
        }
        fflush(f);
        fprintf(stderr, "start %d done: walk acc=%ld tried=%ld emitted_total=%ld t=%.1fs\n", s, acc, tried, emitted,
                (double)(clock() - t0) / CLOCKS_PER_SEC);
    }
    fclose(f);
    printf("gen mode=%s K=%d N=%d seed=%llu starts=%d emitted=%ld cpu=%.1fs\n", near ? "near" : "walk", K, n,
           (unsigned long long)seed, nstarts, emitted, (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}

static int mode_canon(void) {
    int n;
    while (scanf("%d", &n) == 1) {
        N = n;
        for (int i = 0; i < n; i++) if (scanf("%lld %lld", &X[i], &Y[i]) != 2) return 2;
        if (!general_position_all()) { printf("NOT_GENERAL_POSITION\n"); continue; }
        build_orients();
        int nb = nbytes_sig(N);
        canon_sig(1, sigbuf[0]);
        canon_sig(-1, sigbuf[1]);
        unsigned char *m = memcmp(sigbuf[0], sigbuf[1], nb) <= 0 ? sigbuf[0] : sigbuf[1];
        put_hex(stdout, sigbuf[0], nb); putchar(' '); put_hex(stdout, m, nb); putchar('\n');
    }
    return 0;
}

int main(int argc, char **argv) {
    (void)EMIT_N;
    if (argc >= 2 && !strcmp(argv[1], "canon")) return mode_canon();
    if (argc >= 13 && (!strcmp(argv[1], "walk") || !strcmp(argv[1], "near")))
        return mode_gen(!strcmp(argv[1], "near"), atoi(argv[2]), atoi(argv[3]), (uint64_t)atoll(argv[4]), atoi(argv[5]),
                        argv[6], atol(argv[7]), atof(argv[8]), atof(argv[9]), atol(argv[10]), atol(argv[11]), argv[12]);
    fprintf(stderr, "usage: see header\n");
    return 2;
}
