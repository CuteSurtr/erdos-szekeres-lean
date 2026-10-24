/* copied verbatim from results/D/src/satcount.c (lines typedef..ray/par helpers) */
typedef __int128 i128;
typedef long long i64;
typedef unsigned long long u64;

#define MAXN 64
#define MAXL (MAXN * (MAXN - 1) / 2)
#define MAXK 16
#define PT_LIMIT ((1LL << 29) - 1)
#define S_BOUND (1LL << 29)

static int N, K;
static i64 PX[MAXN], PY[MAXN];
static int NL;
static int la[MAXL], lb[MAXL];
static i64 LA[MAXL], LB[MAXL], LC[MAXL];
static int lid[MAXN][MAXN];
static signed char O3s[MAXN][MAXN][MAXN];

static void die(const char *m) { fprintf(stderr, "FATAL: %s\n", m); exit(2); }
static inline int sgn128(i128 v) { return (v > 0) - (v < 0); }
static inline int sgn64(i64 v) { return (v > 0) - (v < 0); }
static i64 orient64(int a, int b, int c) {
    return (PX[b] - PX[a]) * (PY[c] - PY[a]) - (PY[b] - PY[a]) * (PX[c] - PX[a]);
}

static int gp_fail = 0;
static void setup(void) {
    gp_fail = 0;
    for (int i = 0; i < N; i++)
        if (PX[i] >= S_BOUND || PX[i] <= -S_BOUND || PY[i] >= S_BOUND || PY[i] <= -S_BOUND)
            die("coordinate bound 2^29 exceeded");
    for (int a = 0; a < N; a++)
        for (int b = 0; b < N; b++)
            for (int c = 0; c < N; c++) {
                if (a == b || b == c || a == c) { O3s[a][b][c] = 0; continue; }
                O3s[a][b][c] = (signed char)sgn64(orient64(a, b, c));
                if (O3s[a][b][c] == 0) { gp_fail = 1; }
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
}

/* ---------------- convex (K-1)-gons of S and slots ---------------- */
static int NH = 0, HCAP = 0;
static unsigned char *HEX = NULL; /* NH x (K-1), ccw */
static int chain[MAXK];
static int qa[MAXN], qm;

static void push_hex(void) {
    if (NH == HCAP) {
        HCAP = HCAP ? 2 * HCAP : 4096;
        HEX = realloc(HEX, (size_t)HCAP * (K - 1));
        if (!HEX) die("alloc hex");
    }
    for (int i = 0; i < K - 1; i++) HEX[(size_t)NH * (K - 1) + i] = (unsigned char)chain[i];
    NH++;
}
static void dfs(int len, int lastidx) {
    if (len == K - 1) { push_hex(); return; }
    for (int l = lastidx + 1; l < qm; l++) {
        int q = qa[l];
        if (len >= 2 && O3s[chain[len - 2]][chain[len - 1]][q] <= 0) continue;
        chain[len] = q;
        dfs(len + 1, l);
    }
}
static void enum_polys(void) {
    for (int a = 0; a < N; a++) {
        qm = 0;
        for (int b = 0; b < N; b++)
            if (b != a && (PY[b] > PY[a] || (PY[b] == PY[a] && PX[b] > PX[a]))) qa[qm++] = b;
        for (int i = 1; i < qm; i++) { /* ccw angular order around a */
            int v = qa[i], t = i - 1;
            while (t >= 0 && O3s[a][v][qa[t]] > 0) { qa[t + 1] = qa[t]; t--; }
            qa[t + 1] = v;
        }
        chain[0] = a;
        dfs(1, -1);
    }
}
/* independent convex-position check of a polygon given in ccw order */
static int poly_convex_ccw(const int *h, int n) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            if (j == i || j == (i + 1) % n) continue;
            if (O3s[h[i]][h[(i + 1) % n]][h[j]] <= 0) return 0;
        }
    return 1;
}

typedef struct { uint16_t le, lc, ld; signed char se, sc, sd; uint16_t w; int hex; } Slot;
static Slot *SL = NULL;
static int NS = 0;
static int *grp_start; /* slots sorted by (le, se): group index 2*le + (se>0) */

typedef struct { uint32_t key; int hex; } KH;
static int cmpKH(const void *A, const void *B) {
    const KH *a = A, *b = B;
    if (a->key != b->key) return a->key < b->key ? -1 : 1;
    return a->hex - b->hex;
}
static int cmpSlot(const void *A, const void *B) {
    const Slot *a = A, *b = B;
    int ga = 2 * a->le + (a->se > 0), gb = 2 * b->le + (b->se > 0);
    return ga - gb;
}
static inline int need_sign(int x, int y, int want) { /* orient(x,y,p) == want  <=>  basesg[lid] == ret */
    return x < y ? want : -want;
}
static void build_slots(void) {
    int k1 = K - 1;
    KH *arr = malloc(sizeof(KH) * (size_t)NH * k1 + 1);
    if (!arr) die("alloc kh");
    size_t na = 0;
    for (int h = 0; h < NH; h++) {
        const unsigned char *P = HEX + (size_t)h * k1;
        int hv[MAXK];
        for (int i = 0; i < k1; i++) hv[i] = P[i];
        if (!poly_convex_ccw(hv, k1)) die("enumerated polygon not convex");
        for (int i = 0; i < k1; i++) {
            int c = P[(i - 1 + k1) % k1], a = P[i], b = P[(i + 1) % k1], d = P[(i + 2) % k1];
            if (k1 == 3) d = c; /* triangle: neighbours share the third vertex */
            arr[na].key = ((uint32_t)c << 18) | ((uint32_t)a << 12) | ((uint32_t)b << 6) | (uint32_t)d;
            arr[na].hex = h;
            na++;
        }
    }
    qsort(arr, na, sizeof(KH), cmpKH);
    SL = malloc(sizeof(Slot) * (na + 1));
    NS = 0;
    for (size_t i = 0; i < na;) {
        size_t j = i;
        while (j < na && arr[j].key == arr[i].key) j++;
        int c = (arr[i].key >> 18) & 63, a = (arr[i].key >> 12) & 63, b = (arr[i].key >> 6) & 63, d = arr[i].key & 63;
        Slot s;
        s.le = (uint16_t)lid[a][b]; s.se = (signed char)need_sign(a, b, -1);
        s.lc = (uint16_t)lid[c][a]; s.sc = (signed char)need_sign(c, a, +1);
        s.ld = (uint16_t)lid[b][d]; s.sd = (signed char)need_sign(b, d, +1);
        if (j - i > 65535) die("slot weight overflow");
        s.w = (uint16_t)(j - i);
        s.hex = arr[i].hex;
        SL[NS++] = s;
        i = j;
    }
    free(arr);
    qsort(SL, NS, sizeof(Slot), cmpSlot);
    grp_start = calloc(2 * NL + 1, sizeof(int));
    int g = 0;
    for (int i = 0; i <= NS; i++) {
        int gi = i < NS ? 2 * SL[i].le + (SL[i].se > 0) : 2 * NL;
        while (g <= gi) grp_start[g++] = i;
    }
}

/* ---------------- counting for one sign vector ---------------- */
static signed char basesg[MAXL]; /* orient(la,lb,p) */
static int CAP = 3;
#define CACHE_MAX 64
static int cache[CACHE_MAX], ncache = 0;
static long long n_full = 0, n_cache_res = 0;

static inline int slot_ok(const Slot *s) {
    return basesg[s->le] == s->se && basesg[s->lc] == s->sc && basesg[s->ld] == s->sd;
}
static void cache_put(int si) {
    for (int c = 0; c < ncache; c++) if (cache[c] == si) {
        memmove(cache + 1, cache, sizeof(int) * c);
        cache[0] = si;
        return;
    }
    int c = ncache < CACHE_MAX ? ncache : CACHE_MAX - 1;
    memmove(cache + 1, cache, sizeof(int) * c);
    cache[0] = si;
    if (ncache < CACHE_MAX) ncache++;
}
/* exact count, capped at cap (cap <= 0: uncapped); *one = a satisfied slot */
static long long count_m(int cap, int *one) {
    long long m = 0;
    *one = -1;
    if (cap > 0) {
        for (int c = 0; c < ncache; c++) {
            int si = cache[c];
            if (slot_ok(&SL[si])) {
                m += SL[si].w;
                if (*one < 0) *one = si;
                if (m >= cap) {
                    if (c > 0) { memmove(cache + 1, cache, sizeof(int) * c); cache[0] = si; }
                    n_cache_res++;
                    return m;
                }
            }
        }
        m = 0; *one = -1;
    }
    n_full++;
    int found[CACHE_MAX], nf = 0;
    for (int l = 0; l < NL; l++) {
        int g = 2 * l + (basesg[l] > 0);
        for (int i = grp_start[g]; i < grp_start[g + 1]; i++) {
            const Slot *s = &SL[i];
            if (basesg[s->lc] == s->sc && basesg[s->ld] == s->sd) {
                m += s->w;
                if (*one < 0) *one = i;
                if (nf < CACHE_MAX) found[nf++] = i;
                if (cap > 0 && m >= cap) goto done;
            }
        }
    }
done:
    for (int i = nf - 1; i >= 0; i--) cache_put(found[i]);
    return m;
}

/* ---------------- face hashing ---------------- */
static u64 *htab = NULL;
static u64 hmask;
static long long nfaces = 0;
static inline u64 mix64(u64 z) {
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}
static int face_insert(const u64 *bits, int nw) { /* 1 if new */
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
        if (e[0] == 0) { e[0] = h1; e[1] = h2; nfaces++; return 1; }
        if (e[0] == h1 && e[1] == h2) return 0;
        pos = (pos + 1) & hmask;
    }
}

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
static void print128(FILE *f, i128 v) {
    char buf[64]; int i = 63; buf[i] = 0;
    int neg = v < 0;
    unsigned __int128 u = neg ? -(unsigned __int128)v : (unsigned __int128)v;
    if (u == 0) buf[--i] = '0';
    while (u) { buf[--i] = '0' + (int)(u % 10); u /= 10; }
    if (neg) buf[--i] = '-';
    fputs(buf + i, f);
}

/* ---------------- integer point inside a face ---------------- */
static long long n_pt_ok = 0, n_pt_fail = 0;
static int point_in_face(i64 x, i64 y) {
    if (x > PT_LIMIT || x < -PT_LIMIT || y > PT_LIMIT || y < -PT_LIMIT) return 0;
    for (int l = 0; l < NL; l++) {
        i128 v = (i128)LA[l] * y + (i128)LB[l] * x + (i128)LC[l];
        if (sgn128(v) != basesg[l]) return 0;
    }
    return 1;
}
typedef struct { double x, y; } P2;
static int clip(P2 *in, int n, P2 *out, double A, double B, double C, int s) {
    /* keep s*(A*y + B*x + C) >= 0 */
    int m = 0;
    for (int i = 0; i < n; i++) {
        P2 p = in[i], q = in[(i + 1) % n];
        double fp = s * (A * p.y + B * p.x + C), fq = s * (A * q.y + B * q.x + C);
        if (fp >= 0) out[m++] = p;
        if ((fp >= 0) != (fq >= 0)) {
            double t = fp / (fp - fq);
            out[m].x = p.x + t * (q.x - p.x);
            out[m].y = p.y + t * (q.y - p.y);
            m++;
        }
    }
    return m;
}
static double last_area = 0;
static int find_point(i128 X, i128 Y, i128 D, i64 dx, i64 dy, i64 *ox, i64 *oy) {
    static P2 b1[2 * MAXL + 8], b2[2 * MAXL + 8];
    double L = (double)PT_LIMIT;
    int n = 4;
    b1[0].x = -L; b1[0].y = -L; b1[1].x = L; b1[1].y = -L; b1[2].x = L; b1[2].y = L; b1[3].x = -L; b1[3].y = L;
    P2 *in = b1, *out = b2;
    for (int l = 0; l < NL && n > 0; l++) {
        n = clip(in, n, out, (double)LA[l], (double)LB[l], (double)LC[l], basesg[l]);
        P2 *t = in; in = out; out = t;
    }
    double vx = (double)X / (double)D, vy = (double)Y / (double)D;
    double cx = vx, cy = vy;
    double minx = vx, maxx = vx, miny = vy, maxy = vy;
    last_area = 0;
    if (n >= 3) {
        double A2 = 0, sx = 0, sy = 0;
        minx = maxx = in[0].x; miny = maxy = in[0].y;
        for (int i = 0; i < n; i++) {
            P2 p = in[i], q = in[(i + 1) % n];
            double cr = p.x * q.y - q.x * p.y;
            A2 += cr; sx += (p.x + q.x) * cr; sy += (p.y + q.y) * cr;
            if (p.x < minx) minx = p.x; if (p.x > maxx) maxx = p.x;
            if (p.y < miny) miny = p.y; if (p.y > maxy) maxy = p.y;
        }
        last_area = fabs(A2) / 2;
        if (fabs(A2) > 0) { cx = sx / (3 * A2); cy = sy / (3 * A2); }
        else {
            cx = 0; cy = 0;
            for (int i = 0; i < n; i++) { cx += in[i].x; cy += in[i].y; }
            cx /= n; cy /= n;
        }
    }
    /* 1. rounded centroid and small neighbourhood */
    for (int r = 0; r <= 2; r++)
        for (int ix = -r; ix <= r; ix++)
            for (int iy = -r; iy <= r; iy++) {
                if (abs(ix) != r && abs(iy) != r) continue;
                i64 x = (i64)llround(cx) + ix, y = (i64)llround(cy) + iy;
                if (point_in_face(x, y)) { *ox = x; *oy = y; return 1; }
            }
    /* 2. points along the symbolic ray from v, and toward the centroid */
    double dl = sqrt((double)dx * dx + (double)dy * dy);
    for (int e = 0; e < 60; e++) {
        double t = ldexp(1.0, 30 - e) / dl;
        i64 x = (i64)llround(vx + t * dx), y = (i64)llround(vy + t * dy);
        if (point_in_face(x, y)) { *ox = x; *oy = y; return 1; }
    }
    for (int e = 1; e < 12; e++) {
        double t = ldexp(1.0, -e);
        i64 x = (i64)llround(vx + t * (cx - vx)), y = (i64)llround(vy + t * (cy - vy));
        if (point_in_face(x, y)) { *ox = x; *oy = y; return 1; }
    }
    /* 3. lattice points of a small bounding box */
    if (n >= 3 && (maxx - minx + 1) * (maxy - miny + 1) <= 20000.0) {
        for (i64 x = (i64)floor(minx); x <= (i64)ceil(maxx); x++)
            for (i64 y = (i64)floor(miny); y <= (i64)ceil(maxy); y++)
                if (point_in_face(x, y)) { *ox = x; *oy = y; return 1; }
    }
    return 0;
}

/* ---------------- candidate evaluation ---------------- */
static int zl[MAXL], nzl;
static FILE *ff = NULL;
static int EMIT = 1;
static long long n_cand = 0, n_invalid = 0;
static long long hist[4] = {0, 0, 0, 0};
static long long hist_full[64];

static void vertex_base(i128 X, i128 Y, i128 D) {
    nzl = 0;
    for (int l = 0; l < NL; l++) {
        i128 v = (i128)LA[l] * Y + (i128)LB[l] * X + (i128)LC[l] * D;
        int s = sgn128(v);
        basesg[l] = (signed char)s;
        if (!s) zl[nzl++] = l;
    }
}

static void report_face(long long m, int one, const char *tag, int t1, int t2, i128 X, i128 Y, i128 D, i64 dx, i64 dy) {
    i64 px = 0, py = 0;
    int ok = find_point(X, Y, D, dx, dy, &px, &py);
    if (ok) n_pt_ok++; else n_pt_fail++;
    if (!ff) return;
    fprintf(ff, "%lld %s %d %d ", m, tag, t1, t2);
    print128(ff, X); fputc(' ', ff); print128(ff, Y); fputc(' ', ff); print128(ff, D);
    fprintf(ff, " %lld %lld %d %lld %lld %.3g |", dx, dy, ok, px, py, last_area);
    if (m == 1) {
        if (one < 0 || SL[one].w != 1) die("m=1 but slot weight != 1");
        const unsigned char *P = HEX + (size_t)SL[one].hex * (K - 1);
        int a = la[SL[one].le], b = lb[SL[one].le];
        int ins = -1;
        for (int i = 0; i < K - 1; i++) {
            fprintf(ff, " %d", P[i]);
            if ((P[i] == a && P[(i + 1) % (K - 1)] == b) || (P[i] == b && P[(i + 1) % (K - 1)] == a)) ins = i;
        }
        fprintf(ff, " | %d", ins);
    } else fprintf(ff, " | -1");
    fputc('\n', ff);
}

static void record_face(long long m, i128 X, i128 Y, i128 D, i64 dx, i64 dy);
static void eval_direction(i128 X, i128 Y, i128 D, i64 dx, i64 dy, const char *tag, int t1, int t2) {
    n_cand++;
    signed char fix[MAXL];
    for (int z = 0; z < nzl; z++) {
        int l = zl[z];
        i64 e = LA[l] * dy + LB[l] * dx;
        int s = sgn64(e);
        if (!s) { n_invalid++; return; }
        fix[z] = (signed char)s;
    }
    for (int z = 0; z < nzl; z++) basesg[zl[z]] = fix[z];
    u64 bits[(MAXL + 63) / 64];
    int nw = (NL + 63) / 64;
    memset(bits, 0, sizeof(u64) * nw);
    for (int l = 0; l < NL; l++) if (basesg[l] > 0) bits[l >> 6] |= 1ULL << (l & 63);
    if (face_insert(bits, nw)) {
        int one;
        long long m = count_m(CAP, &one);
        hist[m >= 3 ? 3 : m]++;
        record_face(m, X, Y, D, dx, dy);
    }
    for (int z = 0; z < nzl; z++) basesg[zl[z]] = 0;
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

