/* evalbig.c -- auditor A3: evaluate a zcnf.py mirror CNF (streamed on stdin) on up to 64 exact configurations at
 * once (one bit per configuration).
 *   conf file (from mkconf.py): "N NP nX C", then per configuration a line of nX '0'/'1' (triple-class variables,
 *   already checked against the map in exact arithmetic) and a line of C(N,3) '+'/'-' (chi of sorted point triples).
 * Convexity variables are numbered independently: canonical (S <= sorted(sigma S)) subsets of the N points of sizes
 * 4..K-1 in lexicographic order, after the nX class variables.  Their values are the actual convex-position values,
 * computed by counting hull edges (pairs with all other points strictly on one side); for 4-sets also by the
 * triangle criterion, for 5- and 6-sets also by "all 4-subsets convex", and the methods must agree.
 * Every clause is evaluated.  A violated clause is accepted only if it consists of negated 6-set variables and equals
 * the K-clause {-conv(canon(S - i))} of a canonical 7-set S that is in convex position (direct edge count) in every
 * configuration where the clause is violated.  Finally, per configuration, the number of violated clauses must equal
 * the number of canonical 7-sets in convex position (enumerated directly).
 * usage: zstd -dc X.cnf.zst | evalbig CONF K                                                                        */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef uint64_t u64;
static int N, NP, nX, C, K;
static u64 ALL;
static u64 *chipos;
static int tidx[48][48][48];
static long long binom[64][64];
static u64 *vmask;          /* per variable, bit j = value in configuration j */
static long nvar;           /* computed number of variables */
static long *rankvar[8];    /* rankvar[r][lexrank] = conv variable of the canonical r-set, 0 if not canonical */
static unsigned char *v6set; /* conv variable (6-sets) -> its canonical 6-set */
static long v6lo, v6hi;
static long nconv[8];

static inline int sigma(int i) { return i >= NP ? i : (i ^ 1); }

static inline u64 orient(int a, int b, int c) {
    int inv = (a > b) + (a > c) + (b > c);
    int x = a, y = b, z = c, t;
    if (x > y) { t = x; x = y; y = t; }
    if (y > z) { t = y; y = z; z = t; }
    if (x > y) { t = x; x = y; y = t; }
    u64 m = chipos[tidx[x][y][z]];
    return (inv & 1) ? (~m & ALL) : m;
}

static u64 convex_edges(const int *S, int n) {
    u64 c[6] = {0, 0, 0, 0, 0, 0};
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++) {
            u64 allp = ALL, alln = ALL;
            for (int k = 0; k < n; k++) {
                if (k == i || k == j) continue;
                u64 m = orient(S[i], S[j], S[k]);
                allp &= m;
                alln &= ~m;
            }
            u64 carry = (allp | alln) & ALL;
            for (int b = 0; b < 6 && carry; b++) { u64 nb = c[b] ^ carry; carry &= c[b]; c[b] = nb; }
        }
    u64 eq = ALL;
    for (int b = 0; b < 6; b++) eq &= ((n >> b) & 1) ? c[b] : ~c[b];
    return eq & ALL;
}

static u64 convex_tri4(const int *S) { /* 4 points: convex iff no point inside the triangle of the others */
    u64 nonconv = 0;
    for (int d = 0; d < 4; d++) {
        int o[3], k = 0;
        for (int i = 0; i < 4; i++) if (i != d) o[k++] = S[i];
        u64 m1 = orient(o[0], o[1], S[d]), m2 = orient(o[1], o[2], S[d]), m3 = orient(o[2], o[0], S[d]);
        nonconv |= (m1 & m2 & m3) | (~m1 & ~m2 & ~m3);
    }
    return ~nonconv & ALL;
}

static long lexrank(const int *S, int r) {
    long rank = 0;
    int prev = -1;
    for (int i = 0; i < r; i++) {
        for (int j = prev + 1; j < S[i]; j++) rank += binom[N - 1 - j][r - 1 - i];
        prev = S[i];
    }
    return rank;
}

static int cmp_int(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

static void canon(const int *S, int r, int *out) {
    int T[16];
    for (int i = 0; i < r; i++) T[i] = sigma(S[i]);
    qsort(T, r, sizeof(int), cmp_int);
    int less = 0; /* T < S ? */
    for (int i = 0; i < r; i++) { if (T[i] != S[i]) { less = T[i] < S[i]; break; } }
    memcpy(out, less ? T : S, r * sizeof(int));
}

static int is_canon(const int *S, int r) {
    int T[16];
    canon(S, r, T);
    return memcmp(T, S, r * sizeof(int)) == 0;
}

static long var_of_set(const int *S, int r) { /* S sorted */
    int T[16];
    canon(S, r, T);
    return rankvar[r][lexrank(T, r)];
}

static int next_comb(int *S, int r) {
    int i = r - 1;
    while (i >= 0 && S[i] == N - r + i) i--;
    if (i < 0) return 0;
    S[i]++;
    for (int j = i + 1; j < r; j++) S[j] = S[j - 1] + 1;
    return 1;
}

static long nviol[64], ncvx7[64];
static long unexplained = 0, explained = 0, ktype_clauses = 0;

static void violation(const long *lits, int n, u64 viol) {
    for (int j = 0; j < C; j++) if ((viol >> j) & 1) nviol[j]++;
    long vs[64];
    for (int i = 0; i < n; i++) {
        if (lits[i] > 0 || -lits[i] < v6lo || -lits[i] > v6hi) goto bad;
        vs[i] = -lits[i];
    }
    /* sort + dedup clause variables */
    for (int i = 1; i < n; i++) for (int k = i; k > 0 && vs[k - 1] > vs[k]; k--) { long t = vs[k]; vs[k] = vs[k - 1]; vs[k - 1] = t; }
    int nu = 0;
    for (int i = 0; i < n; i++) if (nu == 0 || vs[nu - 1] != vs[i]) vs[nu++] = vs[i];
    {
        const unsigned char *c6 = v6set + 6 * (vs[0] - v6lo);
        int D[2][6];
        for (int i = 0; i < 6; i++) D[0][i] = c6[i];
        for (int i = 0; i < 6; i++) D[1][i] = sigma(c6[i]);
        qsort(D[1], 6, sizeof(int), cmp_int);
        for (int d = 0; d < 2; d++)
            for (int p = 0; p < N; p++) {
                int in = 0;
                for (int i = 0; i < 6; i++) if (D[d][i] == p) in = 1;
                if (in) continue;
                int S[7], k = 0, ins = 0;
                for (int i = 0; i < 6; i++) { if (!ins && p < D[d][i]) { S[k++] = p; ins = 1; } S[k++] = D[d][i]; }
                if (!ins) S[k++] = p;
                if (!is_canon(S, 7)) continue;
                long ws[7];
                for (int i = 0; i < 7; i++) {
                    int Q[6], q = 0;
                    for (int jj = 0; jj < 7; jj++) if (jj != i) Q[q++] = S[jj];
                    ws[i] = var_of_set(Q, 6);
                }
                for (int i = 1; i < 7; i++) for (int kk = i; kk > 0 && ws[kk - 1] > ws[kk]; kk--) { long t = ws[kk]; ws[kk] = ws[kk - 1]; ws[kk - 1] = t; }
                int nw = 0;
                for (int i = 0; i < 7; i++) if (nw == 0 || ws[nw - 1] != ws[i]) ws[nw++] = ws[i];
                if (nw != nu) continue;
                int same = 1;
                for (int i = 0; i < nu; i++) if (ws[i] != vs[i]) same = 0;
                if (!same) continue;
                u64 m7 = convex_edges(S, 7);
                if ((viol & ~m7) == 0) { explained++; return; }
            }
    }
bad:
    unexplained++;
    if (unexplained <= 20) {
        fprintf(stderr, "UNEXPLAINED violated clause (configs %016llx):", (unsigned long long)viol);
        for (int i = 0; i < n; i++) fprintf(stderr, " %ld", lits[i]);
        fprintf(stderr, "\n");
    }
}

#define BUFSZ (1 << 24)
int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: evalbig CONF K < cnf\n"); return 2; }
    K = atoi(argv[2]);
    if (K != 7) { fprintf(stderr, "K must be 7\n"); return 2; }
    for (int n = 0; n < 64; n++) { binom[n][0] = 1; for (int k = 1; k <= n; k++) binom[n][k] = binom[n - 1][k - 1] + (k <= n - 1 ? binom[n - 1][k] : 0); }
    FILE *cf = fopen(argv[1], "r");
    if (!cf || fscanf(cf, "%d %d %d %d", &N, &NP, &nX, &C) != 4 || N > 47 || C > 64 || C < 1) { fprintf(stderr, "bad conf\n"); return 2; }
    ALL = (C == 64) ? ~0ULL : ((1ULL << C) - 1);
    long ntri = binom[N][3];
    chipos = calloc(ntri, sizeof(u64));
    { long t = 0; for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) for (int c = b + 1; c < N; c++) tidx[a][b][c] = t++; }
    char *line = malloc(1 << 20);
    u64 *xm = calloc(nX + 1, sizeof(u64));
    for (int j = 0; j < C; j++) {
        if (fscanf(cf, "%s", line) != 1 || (long)strlen(line) != nX) { fprintf(stderr, "bad X line\n"); return 2; }
        for (int v = 1; v <= nX; v++) if (line[v - 1] == '1') xm[v] |= 1ULL << j;
        if (fscanf(cf, "%s", line) != 1 || (long)strlen(line) != ntri) { fprintf(stderr, "bad chi line\n"); return 2; }
        for (long t = 0; t < ntri; t++) if (line[t] == '+') chipos[t] |= 1ULL << j;
    }
    fclose(cf);
    /* conv variables */
    long nv_alloc = nX + 1;
    for (int r = 4; r < K; r++) nv_alloc += binom[N][r];
    vmask = calloc(nv_alloc + 1, sizeof(u64));
    for (int v = 1; v <= nX; v++) vmask[v] = xm[v];
    nvar = nX;
    long mism_tri = 0, mism_car = 0;
    for (int r = 4; r < K; r++) {
        rankvar[r] = calloc(binom[N][r], sizeof(long));
        if (r == 6) { v6lo = nvar + 1; v6set = malloc(6 * binom[N][6]); }
        int S[16];
        for (int i = 0; i < r; i++) S[i] = i;
        long rk = 0;
        do {
            if (lexrank(S, r) != rk) { fprintf(stderr, "lexrank bug\n"); return 3; }
            if (is_canon(S, r)) {
                long v = ++nvar;
                rankvar[r][rk] = v;
                nconv[r]++;
                u64 m = convex_edges(S, r);
                if (r == 4 && m != convex_tri4(S)) mism_tri++;
                if (r >= 5) { /* all (r-1)-subsets convex (via their variables, already computed) */
                    u64 a = ALL;
                    for (int i = 0; i < r; i++) {
                        int Q[16], q = 0;
                        for (int jj = 0; jj < r; jj++) if (jj != i) Q[q++] = S[jj];
                        a &= vmask[var_of_set(Q, r - 1)];
                    }
                    if (a != m) mism_car++;
                }
                vmask[v] = m;
                if (r == 6) for (int i = 0; i < 6; i++) v6set[6 * (v - v6lo) + i] = (unsigned char)S[i];
            }
            rk++;
        } while (next_comb(S, r));
    }
    v6hi = nvar;
    fprintf(stderr, "conv vars: 4:%ld 5:%ld 6:%ld total vars %ld; convexity method mismatches: tri4 %ld, caratheodory %ld\n",
            nconv[4], nconv[5], nconv[6], nvar, mism_tri, mism_car);
    /* stream the CNF */
    static char buf[BUFSZ];
    size_t len = 0, pos = 0;
    int eof = 0;
    long nv_hdr = -1, nc_hdr = -1, nclauses = 0, maxlit_bad = 0;
    long lits[64];
    int nl = 0, atline = 1;
#define GETC() (pos < len ? buf[pos++] : (eof ? -1 : (len = fread(buf, 1, BUFSZ, stdin), pos = 0, len == 0 ? (eof = 1, -1) : buf[pos++])))
    int ch;
    long hist_len[65] = {0};
    for (;;) {
        ch = GETC();
        if (ch < 0) break;
        if (atline && (ch == 'c' || ch == 'p')) {
            char hl[256]; int k = 0; hl[k++] = (char)ch;
            while ((ch = GETC()) >= 0 && ch != '\n') if (k < 255) hl[k++] = (char)ch;
            hl[k] = 0;
            if (hl[0] == 'p') { if (sscanf(hl, "p cnf %ld %ld", &nv_hdr, &nc_hdr) != 2) { fprintf(stderr, "bad header\n"); return 2; }
                if (nv_hdr != nvar) { fprintf(stderr, "VARIABLE COUNT MISMATCH header %ld computed %ld\n", nv_hdr, nvar); return 4; } }
            atline = 1;
            continue;
        }
        if (ch == '\n') { atline = 1; continue; }
        if (ch == ' ' || ch == '\t' || ch == '\r') { atline = 0; continue; }
        atline = 0;
        int neg = 0;
        long x = 0;
        if (ch == '-') { neg = 1; ch = GETC(); }
        if (ch < '0' || ch > '9') { fprintf(stderr, "parse error\n"); return 2; }
        while (ch >= '0' && ch <= '9') { x = 10 * x + (ch - '0'); ch = GETC(); }
        if (ch == '\n') atline = 1;
        if (x == 0) {
            nclauses++;
            hist_len[nl < 64 ? nl : 64]++;
            u64 sat = 0;
            int allneg6 = 1;
            for (int i = 0; i < nl; i++) {
                long v = lits[i] > 0 ? lits[i] : -lits[i];
                sat |= lits[i] > 0 ? vmask[v] : ~vmask[v];
                if (!(lits[i] < 0 && v >= v6lo && v <= v6hi)) allneg6 = 0;
            }
            if (allneg6 && nl > 0) ktype_clauses++;
            u64 viol = ~sat & ALL;
            if (viol) violation(lits, nl, viol);
            nl = 0;
        } else {
            if (x > nv_hdr) maxlit_bad++;
            if (nl >= 64) { fprintf(stderr, "clause too long\n"); return 2; }
            lits[nl++] = neg ? -x : x;
        }
    }
    if (nl != 0) { fprintf(stderr, "unterminated clause\n"); return 2; }
    /* direct count of canonical convex 7-sets */
    long ncanon7 = 0;
    {
        int S[7];
        for (int i = 0; i < 7; i++) S[i] = i;
        do {
            if (!is_canon(S, 7)) continue;
            ncanon7++;
            u64 m = convex_edges(S, 7);
            while (m) { int j = __builtin_ctzll(m); ncvx7[j]++; m &= m - 1; }
        } while (next_comb(S, 7));
    }
    int countfail = 0;
    long tv = 0, tc = 0;
    for (int j = 0; j < C; j++) { if (nviol[j] != ncvx7[j]) countfail++; tv += nviol[j]; tc += ncvx7[j]; }
    printf("header vars %ld clauses %ld; parsed clauses %ld; literal>nv %ld\n", nv_hdr, nc_hdr, nclauses, maxlit_bad);
    printf("clause length histogram:");
    for (int i = 0; i <= 64; i++) if (hist_len[i]) printf(" %d:%ld", i, hist_len[i]);
    printf("\nK-type clauses (all literals negated 6-set variables): %ld; canonical 7-sets: %ld\n", ktype_clauses, ncanon7);
    printf("convexity method mismatches: tri4 %ld caratheodory %ld\n", mism_tri, mism_car);
    printf("violated clause instances: %ld (explained clause events %ld, unexplained %ld)\n", tv, explained, unexplained);
    printf("canonical convex 7-sets summed over configurations: %ld; per-configuration count mismatches: %d\n", tc, countfail);
    printf("per configuration (violated / convex7):");
    for (int j = 0; j < C; j++) printf(" %ld/%ld", nviol[j], ncvx7[j]);
    printf("\n");
    int ok = (nclauses == nc_hdr) && maxlit_bad == 0 && unexplained == 0 && countfail == 0 && mism_tri == 0 && mism_car == 0
             && ktype_clauses == ncanon7;
    printf("RESULT %s\n", ok ? "PASS" : "FAIL");
    return ok ? 0 : 1;
}
