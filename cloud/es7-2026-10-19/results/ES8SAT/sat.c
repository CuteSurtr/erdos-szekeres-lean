/*
 * Exact saturation test: can a point p be added to a planar point set S
 * (general position) without creating K points in convex position?
 *
 * The order type of S + {p} depends only on the face of the arrangement of
 * the C(N,2) lines through pairs of S that contains p.  Every face has a
 * vertex of the arrangement on its boundary (there are non-parallel lines),
 * and near a vertex v every face incident to v is one of the angular sectors
 * between consecutive lines through v.  We therefore test, symbolically,
 *   p = v + eps * d   (eps -> 0+),
 * for
 *   - v in S: d = r_i + r_{i+1} for every pair of angularly consecutive rays
 *     r_i, r_{i+1} from v towards / away from the other points of S;
 *   - v = line(a,b) /\ line(c,d), {a,b} and {c,d} disjoint, not parallel:
 *     d = +-(b-a) +-(d-c) (all four sign choices).  When more than two lines
 *     pass through v, the pair of lines bounding each sector is among the
 *     enumerated pairs, so every sector is still covered; directions that
 *     happen to be parallel to a further line through v are detected and
 *     skipped as invalid (p would lie on a line).
 * sign orient(a,b,p) = sign orient(a,b,v) if nonzero, else sign cross(b-a,d).
 *
 * All arithmetic is exact: int64 for S-only predicates, __int128 for vertex
 * predicates, with magnitude bounds asserted at load time.
 *
 * Coverage is checked independently: distinct sign vectors of valid
 * candidates are counted (128-bit hashes; hashing can only merge, never
 * split faces) and compared with the face count from Euler's relation
 *   F = 1 + L + sum_v (m_v - 1)
 * computed from exact, gcd-normalised vertex coordinates.
 *
 * usage: sat MODE pointsfile K [options]
 *   MODE = sat   : full saturation run
 *   MODE = test  : read extra integer points "x y" from stdin, print the size
 *                  of the largest convex polygon through each (for brute-force
 *                  comparison)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

typedef __int128 i128;
typedef long long i64;
typedef unsigned long long u64;

#define MAXN 64
#define MAXL (MAXN * (MAXN - 1) / 2)
#define MAXK 66

static int N, K;
static i64 PX[MAXN], PY[MAXN];
static int NL;
static int la[MAXL], lb[MAXL];
static i64 LA[MAXL], LB[MAXL], LC[MAXL];
static int lid[MAXN][MAXN];
static u64 LT[MAXN][MAXN]; /* bit k set iff orient(k,x,y) > 0 */
static signed char O3s[MAXN][MAXN][MAXN];

static signed char sg[MAXN][MAXN]; /* sign orient(a,b,p) */

static void die(const char *m) { fprintf(stderr, "FATAL: %s\n", m); exit(2); }

static inline int sgn128(i128 v) { return (v > 0) - (v < 0); }
static inline int sgn64(i64 v) { return (v > 0) - (v < 0); }

static i64 orient64(int a, int b, int c) {
    return (PX[b] - PX[a]) * (PY[c] - PY[a]) - (PY[b] - PY[a]) * (PX[c] - PX[a]);
}

static void load(const char *path) {
    FILE *f = fopen(path, "r");
    if (!f) die("cannot open points");
    N = 0;
    i64 x, y;
    while (fscanf(f, "%lld %lld", &x, &y) == 2) {
        if (N >= MAXN) die("too many points");
        PX[N] = x; PY[N] = y; N++;
    }
    fclose(f);
    /* magnitude bound: |coord| < 2^27 => all intermediate values < 2^120 */
    for (int i = 0; i < N; i++)
        if (PX[i] >= (1LL << 27) || PX[i] <= -(1LL << 27) || PY[i] >= (1LL << 27) || PY[i] <= -(1LL << 27))
            die("coordinate bound 2^27 exceeded");
    for (int a = 0; a < N; a++)
        for (int b = 0; b < N; b++)
            for (int c = 0; c < N; c++) {
                if (a == b || b == c || a == c) { O3s[a][b][c] = 0; continue; }
                O3s[a][b][c] = (signed char)sgn64(orient64(a, b, c));
                if (O3s[a][b][c] == 0) die("S not in general position");
            }
    NL = 0;
    for (int a = 0; a < N; a++)
        for (int b = a + 1; b < N; b++) {
            la[NL] = a; lb[NL] = b;
            LA[NL] = PX[b] - PX[a];
            LB[NL] = -(PY[b] - PY[a]);
            LC[NL] = PX[a] * PY[b] - PY[a] * PX[b];
            lid[a][b] = lid[b][a] = NL;
            NL++;
        }
    for (int x = 0; x < N; x++)
        for (int y = 0; y < N; y++) {
            u64 m = 0;
            if (x != y)
                for (int k = 0; k < N; k++)
                    if (k != x && k != y && O3s[k][x][y] > 0) m |= 1ULL << k;
            LT[x][y] = m;
        }
}

/* ---------------- convex K-gon through p (uses sg only) ---------------- */

static int cache[64][MAXK];
static int ncache = 0;
#define CACHE_MAX 64

static int check_Q(const int *Q, int k) {
    /* Q = q1..q_{k-1}: p,q1,...,q_{k-1} convex (ccw) iff
       q_i strictly left of p->q1 for i>=2, consecutive ccw around p,
       and left turns at q2..q_{k-2} (verified when Q was created). */
    for (int i = 0; i + 1 < k - 1; i++)
        if (sg[Q[i]][Q[i + 1]] <= 0) return 0;
    for (int i = 2; i < k - 1; i++)
        if (sg[Q[0]][Q[i]] <= 0) return 0;
    return 1;
}

static int verify_Q_full(const int *Q, int k) {
    /* independent re-check of convex position of {p} + Q:
       every consecutive triple of the closed polygon p,q1,...,q_{k-1} turns
       left, and the polygon winds once (q's sorted inside a half-plane). */
    if (!check_Q(Q, k)) return 0;
    for (int i = 1; i + 1 < k - 1; i++)
        if (O3s[Q[i - 1]][Q[i]][Q[i + 1]] <= 0) return 0;
    /* distinctness */
    for (int i = 0; i < k - 1; i++)
        for (int j = i + 1; j < k - 1; j++)
            if (Q[i] == Q[j]) return 0;
    return 1;
}

static int cyc[MAXN];
static int find_poly(int target, int *outQ) {
    /* exists convex polygon with `target` vertices, one of them p? */
    int hp[MAXN], hm[MAXN], np = 0, nm = 0;
    for (int q = 1; q < N; q++) {
        if (sg[0][q] > 0) hp[np++] = q; else hm[nm++] = q;
    }
    /* insertion sort, a before b iff sg[a][b] > 0 (ccw within half-plane) */
    for (int i = 1; i < np; i++) {
        int x = hp[i], j = i - 1;
        while (j >= 0 && sg[x][hp[j]] > 0) { hp[j + 1] = hp[j]; j--; }
        hp[j + 1] = x;
    }
    for (int i = 1; i < nm; i++) {
        int x = hm[i], j = i - 1;
        while (j >= 0 && sg[x][hm[j]] > 0) { hm[j + 1] = hm[j]; j--; }
        hm[j + 1] = x;
    }
    int c = 0;
    cyc[c++] = 0;
    for (int i = 0; i < np; i++) cyc[c++] = hp[i];
    for (int i = 0; i < nm; i++) cyc[c++] = hm[i];
    /* sanity: sortedness inside each half */
    for (int i = 0; i + 1 < np; i++) if (sg[hp[i]][hp[i + 1]] <= 0) die("sort hp");
    for (int i = 0; i + 1 < nm; i++) if (sg[hm[i]][hm[i + 1]] <= 0) die("sort hm");

    static u64 Bl[MAXN][MAXK];
    static unsigned char pr[MAXN][MAXN];
    int H[MAXN], posH[MAXN];
    int need = target - 1; /* number of q's */
    if (need < 2) return 1;
    for (int t = 0; t < N; t++) {
        int q1 = cyc[t];
        int m = 0, tot = 0;
        for (int u = 1; u < N; u++) {
            int x = cyc[(t + u) % N];
            if (sg[q1][x] > 0) H[m++] = x; else break;
        }
        for (int x = 0; x < N; x++) if (x != q1 && sg[q1][x] > 0) tot++;
        if (tot != m) die("half-plane arc not contiguous");
        if (m < need - 1) continue;
        for (int i = 0; i < N; i++) posH[i] = -1;
        for (int i = 0; i < m; i++) posH[H[i]] = i;
        for (int j = 0; j < m; j++) {
            for (int l = 0; l <= need; l++) Bl[j][l] = 0;
            for (int l = 1; l <= 2; l++) Bl[j][l] |= 1ULL << q1;
            if (need == 2) {
                outQ[0] = q1; outQ[1] = H[j];
                return 1;
            }
            for (int i = 0; i < j; i++) {
                u64 lt = LT[H[i]][H[j]];
                int best = 0;
                for (int l = need - 1; l >= 2; l--)
                    if (Bl[i][l] & lt) { best = l; break; }
                if (!best) continue;
                int len = best + 1;
                pr[i][j] = (unsigned char)__builtin_ctzll(Bl[i][best] & lt);
                for (int l = 1; l <= len; l++) Bl[j][l] |= 1ULL << H[i];
                if (len >= need) {
                    /* reconstruct backwards */
                    int seq[MAXK], s = 0;
                    int cur = j, prv = i;
                    seq[s++] = H[cur];
                    seq[s++] = H[prv];
                    int pk = pr[prv][cur];
                    while (pk != q1) {
                        seq[s++] = pk;
                        if (s > need) die("reconstruct overflow");
                        int ppos = posH[pk];
                        if (ppos < 0) die("reconstruct posH");
                        int nk = pr[ppos][prv];
                        cur = prv; prv = ppos; pk = nk;
                    }
                    seq[s++] = q1;
                    if (s != need) die("reconstruct length");
                    for (int r = 0; r < s; r++) outQ[r] = seq[s - 1 - r];
                    if (!verify_Q_full(outQ, target)) die("reconstructed polygon fails verification");
                    return 1;
                }
            }
        }
    }
    return 0;
}

/* returns 1 if a convex K-gon through p exists (cache first, then exact DP) */
static FILE *qf = NULL;
static long long n_cache_hit = 0, n_dp_found = 0, n_dp_none = 0;
static int has_kgon(void) {
    for (int c = 0; c < ncache; c++) {
        if (check_Q(cache[c], K)) {
            if (c > 0) {
                int tmp[MAXK];
                memcpy(tmp, cache[c], sizeof(int) * (K - 1));
                memmove(cache[1], cache[0], sizeof(cache[0]) * c);
                memcpy(cache[0], tmp, sizeof(int) * (K - 1));
            }
            n_cache_hit++;
            return 1;
        }
    }
    int Q[MAXK];
    if (find_poly(K, Q)) {
        int c = ncache < CACHE_MAX ? ncache : CACHE_MAX - 1;
        memmove(cache[1], cache[0], sizeof(cache[0]) * c);
        memcpy(cache[0], Q, sizeof(int) * (K - 1));
        if (ncache < CACHE_MAX) ncache++;
        n_dp_found++;
        if (qf) { for (int r = 0; r < K - 1; r++) fprintf(qf, "%d%c", Q[r], r == K - 2 ? '\n' : ' '); }
        return 1;
    }
    n_dp_none++;
    return 0;
}

/* ---------------- face hashing ---------------- */
static u64 *htab = NULL; /* pairs (h1,h2), h1 != 0 */
static u64 hmask;
static long long nfaces = 0;
static inline u64 mix64(u64 z) {
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}
static void face_insert(const u64 *bits, int nw) {
    u64 h1 = 0x243F6A8885A308D3ULL, h2 = 0x13198A2E03707344ULL;
    for (int i = 0; i < nw; i++) {
        h1 = mix64(h1 ^ bits[i]) + (u64)i * 0x9E3779B97F4A7C15ULL;
        h2 = mix64((h2 + bits[i]) * 0xD6E8FEB86659FD93ULL) ^ ((u64)i << 17);
    }
    h1 = mix64(h1); h2 = mix64(h2 ^ 0xA0761D6478BD642FULL);
    if (h1 == 0) h1 = 1;
    u64 pos = h1 & hmask;
    for (;;) {
        u64 *e = htab + 2 * pos;
        if (e[0] == 0) { e[0] = h1; e[1] = h2; nfaces++; return; }
        if (e[0] == h1 && e[1] == h2) return;
        pos = (pos + 1) & hmask;
    }
}

/* ---------------- Euler face count ---------------- */
typedef struct { i128 x, y, d; } V3;
static int cmpV3(const void *A, const void *B) {
    const V3 *a = A, *b = B;
    if (a->x != b->x) return a->x < b->x ? -1 : 1;
    if (a->y != b->y) return a->y < b->y ? -1 : 1;
    if (a->d != b->d) return a->d < b->d ? -1 : 1;
    return 0;
}
static i128 gcd128(i128 a, i128 b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b) { i128 t = a % b; a = b; b = t; }
    return a;
}

/* ---------------- candidate evaluation ---------------- */
static signed char basesg[MAXL];
static int zl[MAXL], nzl;
static FILE *badf = NULL;
static long long n_cand = 0, n_invalid = 0, n_bad = 0;

static void print128(FILE *f, i128 v) {
    char buf[64]; int i = 63; buf[i] = 0;
    int neg = v < 0;
    unsigned __int128 u = neg ? -(unsigned __int128)v : (unsigned __int128)v;
    if (u == 0) buf[--i] = '0';
    while (u) { buf[--i] = '0' + (int)(u % 10); u /= 10; }
    if (neg) buf[--i] = '-';
    fputs(buf + i, f);
}

static void vertex_base(i128 X, i128 Y, i128 D) {
    nzl = 0;
    for (int l = 0; l < NL; l++) {
        i128 v = (i128)LA[l] * Y + (i128)LB[l] * X + (i128)LC[l] * D;
        int s = sgn128(v);
        basesg[l] = (signed char)s;
        if (!s) zl[nzl++] = l;
    }
}

static void eval_direction(i128 X, i128 Y, i128 D, i64 dx, i64 dy, const char *tag, int t1, int t2) {
    n_cand++;
    signed char fix[MAXL];
    for (int z = 0; z < nzl; z++) {
        int l = zl[z];
        i64 e = LA[l] * dy + LB[l] * dx; /* cross(b-a, d) */
        int s = sgn64(e);
        if (!s) { n_invalid++; return; }
        fix[z] = (signed char)s;
    }
    for (int z = 0; z < nzl; z++) basesg[zl[z]] = fix[z];
    for (int l = 0; l < NL; l++) {
        int a = la[l], b = lb[l];
        sg[a][b] = basesg[l];
        sg[b][a] = (signed char)-basesg[l];
    }
    /* face hash */
    u64 bits[(MAXL + 63) / 64];
    int nw = (NL + 63) / 64;
    memset(bits, 0, sizeof(u64) * nw);
    for (int l = 0; l < NL; l++) if (basesg[l] > 0) bits[l >> 6] |= 1ULL << (l & 63);
    face_insert(bits, nw);
    for (int z = 0; z < nzl; z++) basesg[zl[z]] = 0;

    if (!has_kgon()) {
        n_bad++;
        if (badf) {
            fprintf(badf, "%s %d %d ", tag, t1, t2);
            print128(badf, X); fputc(' ', badf);
            print128(badf, Y); fputc(' ', badf);
            print128(badf, D);
            fprintf(badf, " %lld %lld ", dx, dy);
            for (int l = 0; l < NL; l++) fputc(sg[la[l]][lb[l]] > 0 ? '+' : '-', badf);
            fputc('\n', badf);
            fflush(badf);
        }
    }
}

static int halfplane(i64 x, i64 y) { return (y > 0 || (y == 0 && x > 0)) ? 0 : 1; }
static i64 RX[2 * MAXN], RY[2 * MAXN];
static int ray_cmp(int i, int j) {
    int hi = halfplane(RX[i], RY[i]), hj = halfplane(RX[j], RY[j]);
    if (hi != hj) return hi < hj ? -1 : 1;
    i64 c = RX[i] * RY[j] - RY[i] * RX[j];
    if (c > 0) return -1;
    if (c < 0) return 1;
    die("parallel rays at S point");
    return 0;
}

typedef struct { i64 T, D; int l2; } Par;
static int cmpPar(const void *A, const void *B) {
    const Par *a = A, *b = B;
    i128 l = (i128)a->T * b->D, r = (i128)b->T * a->D;
    if (l != r) return l < r ? -1 : 1;
    return a->l2 - b->l2;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: sat MODE points K [badfile [certfile]]\n"); return 1; }
    const char *mode = argv[1];
    load(argv[2]);
    K = atoi(argv[3]);
    if (K < 3 || K > MAXK - 1) die("bad K");

    if (!strcmp(mode, "test")) {
        i64 x, y;
        while (scanf("%lld %lld", &x, &y) == 2) {
            int ok = 1;
            for (int a = 0; a < N && ok; a++)
                for (int b = a + 1; b < N; b++) {
                    i128 v = (i128)LA[lid[a][b]] * y + (i128)LB[lid[a][b]] * x + (i128)LC[lid[a][b]];
                    int s = sgn128(v);
                    if (!s) { ok = 0; break; }
                    sg[a][b] = (signed char)s; sg[b][a] = (signed char)-s;
                }
            if (!ok) { printf("degenerate\n"); continue; }
            int best = 2, Q[MAXK];
            for (int t = 3; t <= N + 1; t++) {
                if (find_poly(t, Q)) best = t; else break;
            }
            printf("%d\n", best);
        }
        return 0;
    }
    if (strcmp(mode, "sat")) die("unknown mode");
    if (argc >= 5) badf = fopen(argv[4], "w");
    if (argc >= 6) qf = fopen(argv[5], "w");

    clock_t t0 = clock();
    /* hash table sized for the worst case F <= 1 + L + L(L-1)/2 */
    long long Fmax = 1 + NL + (long long)NL * (NL - 1) / 2;
    u64 sz = 1; while (sz < (u64)(2 * Fmax)) sz <<= 1;
    htab = calloc(2 * sz, sizeof(u64));
    if (!htab) die("alloc htab");
    hmask = sz - 1;

    /* 1. vertices at points of S */
    long long cand_S = 0;
    for (int s = 0; s < N; s++) {
        int nr = 0;
        for (int t = 0; t < N; t++) if (t != s) {
            RX[nr] = PX[t] - PX[s]; RY[nr] = PY[t] - PY[s]; nr++;
            RX[nr] = PX[s] - PX[t]; RY[nr] = PY[s] - PY[t]; nr++;
        }
        int idx[2 * MAXN];
        for (int i = 0; i < nr; i++) idx[i] = i;
        for (int i = 1; i < nr; i++) {
            int x = idx[i], j = i - 1;
            while (j >= 0 && ray_cmp(x, idx[j]) < 0) { idx[j + 1] = idx[j]; j--; }
            idx[j + 1] = x;
        }
        vertex_base(PX[s], PY[s], 1);
        if (nzl != N - 1) die("unexpected number of lines through S point");
        for (int i = 0; i < nr; i++) {
            int r1 = idx[i], r2 = idx[(i + 1) % nr];
            i64 dx = RX[r1] + RX[r2], dy = RY[r1] + RY[r2];
            /* strictly inside the wedge: cross(r1,d) > 0 and cross(d,r2) > 0 */
            i64 c1 = RX[r1] * dy - RY[r1] * dx, c2 = dx * RY[r2] - dy * RX[r2];
            if (c1 <= 0 || c2 <= 0) die("wedge direction not strictly inside");
            eval_direction(PX[s], PY[s], 1, dx, dy, "S", s, i);
            cand_S++;
        }
    }
    fprintf(stderr, "S-vertex candidates: %lld, bad so far %lld, faces so far %lld\n", cand_S, n_bad, nfaces);

    /* 2. other vertices, processed line by line in order along the line */
    V3 *verts = malloc(sizeof(V3) * ((size_t)NL * (NL - 1) / 2 + 1));
    if (!verts) die("alloc verts");
    long long nverts = 0, nparallel = 0;
    Par *par = malloc(sizeof(Par) * NL);
    for (int l1 = 0; l1 < NL; l1++) {
        int a = la[l1], b = lb[l1];
        int np2 = 0;
        for (int l2 = l1 + 1; l2 < NL; l2++) {
            int c = la[l2], d = lb[l2];
            if (c == a || c == b || d == a || d == b) continue;
            i64 ux = PX[b] - PX[a], uy = PY[b] - PY[a];
            i64 wx = PX[d] - PX[c], wy = PY[d] - PY[c];
            i64 D = ux * wy - uy * wx;
            if (D == 0) { nparallel++; continue; }
            i64 T = (PX[c] - PX[a]) * wy - (PY[c] - PY[a]) * wx; /* cross(c-a, d-c) */
            if (D < 0) { D = -D; T = -T; }
            par[np2].T = T; par[np2].D = D; par[np2].l2 = l2; np2++;
        }
        qsort(par, np2, sizeof(Par), cmpPar);
        for (int k = 0; k < np2; k++) {
            int l2 = par[k].l2, c = la[l2], d = lb[l2];
            i64 ux = PX[b] - PX[a], uy = PY[b] - PY[a];
            i64 wx = PX[d] - PX[c], wy = PY[d] - PY[c];
            i128 D = par[k].D, T = par[k].T;
            i128 X = (i128)PX[a] * D + T * ux;
            i128 Y = (i128)PY[a] * D + T * uy;
            /* exactness check: v lies on both lines */
            {
                i128 e1 = (i128)LA[l1] * Y + (i128)LB[l1] * X + (i128)LC[l1] * D;
                i128 e2 = (i128)LA[l2] * Y + (i128)LB[l2] * X + (i128)LC[l2] * D;
                if (e1 != 0 || e2 != 0) die("vertex not on its lines");
            }
            i128 g = gcd128(gcd128(X, Y), D);
            verts[nverts].x = X / g; verts[nverts].y = Y / g; verts[nverts].d = D / g; nverts++;
            vertex_base(X, Y, D);
            for (int sx = -1; sx <= 1; sx += 2)
                for (int sy = -1; sy <= 1; sy += 2)
                    eval_direction(X, Y, D, sx * ux + sy * wx, sx * uy + sy * wy, "V", l1, l2);
        }
        if ((l1 & 63) == 0)
            fprintf(stderr, "line %d/%d cand=%lld bad=%lld faces=%lld hits=%lld dp=%lld t=%.1fs\n",
                    l1, NL, n_cand, n_bad, nfaces, n_cache_hit, n_dp_found,
                    (double)(clock() - t0) / CLOCKS_PER_SEC);
    }
    /* Euler count */
    qsort(verts, nverts, sizeof(V3), cmpV3);
    long long sum_m1 = (long long)N * (N - 2); /* S points: N-1 lines each */
    long long ndistinct = 0, maxm = 2;
    for (long long i = 0; i < nverts;) {
        long long j = i;
        while (j < nverts && cmpV3(&verts[i], &verts[j]) == 0) j++;
        long long pairs = j - i, m = 2;
        while (m * (m - 1) / 2 < pairs) m++;
        if (m * (m - 1) / 2 != pairs) die("pair count not triangular");
        sum_m1 += m - 1;
        if (m > maxm) maxm = m;
        ndistinct++;
        i = j;
    }
    long long Feuler = 1 + NL + sum_m1;
    double secs = (double)(clock() - t0) / CLOCKS_PER_SEC;
    printf("{\"N\": %d, \"K\": %d, \"lines\": %d, \"parallel_pairs\": %lld, "
           "\"nonS_vertex_pairs\": %lld, \"nonS_distinct_vertices\": %lld, \"max_lines_through_nonS_vertex\": %lld, "
           "\"faces_euler\": %lld, \"faces_hit_by_valid_candidates\": %lld, "
           "\"candidates\": %lld, \"invalid_candidates\": %lld, \"valid_candidates\": %lld, "
           "\"cache_hits\": %lld, \"dp_found\": %lld, \"dp_none\": %lld, \"bad_candidates\": %lld, "
           "\"cpu_seconds\": %.1f}\n",
           N, K, NL, nparallel, nverts, ndistinct, maxm, Feuler, nfaces, n_cand, n_invalid,
           n_cand - n_invalid, n_cache_hit, n_dp_found, n_dp_none, n_bad, secs);
    if (badf) fclose(badf);
    if (qf) fclose(qf);
    return 0;
}
