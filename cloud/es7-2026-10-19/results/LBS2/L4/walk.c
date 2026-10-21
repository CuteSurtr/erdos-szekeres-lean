/*
 * walk.c -- random walk of a 32-point set that keeps it in general position
 * with no 7 points in convex position (strategy walk32; idea as in
 * results/LBS/L2/lbs.c, own code).
 *
 * The base set is translated to be centred and each axis is multiplied by an
 * integer factor so that the coordinates fill about 2^25 (a positive
 * diagonal affine map: the order type is unchanged).  A move displaces one
 * point by a Gaussian step of r * (distance to its nearest neighbour), r
 * log-uniform in [RMIN, 1], rounded to integers, and is accepted iff all
 * coordinates stay below 2^26 in absolute value, no three points become
 * collinear and the largest convex subset stays <= 6.  All geometric tests
 * are exact (int64 coordinates, __int128 orientations).
 *
 * The convex-subset test is the anchor DP (anchor = lowest point, others
 * sorted by angle, chains with left turns).  Only subsets through the moved
 * point can change, but the full DP is cheap enough (about 1 ms).
 *
 * usage: walk BASEFILE SEED NSNAP STEPS RMIN OUTPREFIX
 *   writes OUTPREFIX_k.txt after every STEPS accepted moves, k = 1..NSNAP
 */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 40
typedef long long ll;
typedef unsigned long long u64;
static int N;
static ll X[MAXN], Y[MAXN];
static const ll LIM = 1LL << 26;

static u64 rs;
static u64 rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static double urand(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static double grand(void) {
    double u = urand() + 1e-300, v = urand();
    return sqrt(-2 * log(u)) * cos(2 * M_PI * v);
}
static int orient(int a, int b, int c) {
    __int128 v = (__int128)(X[b] - X[a]) * (Y[c] - Y[a]) - (__int128)(Y[b] - Y[a]) * (X[c] - X[a]);
    return (v > 0) - (v < 0);
}
static int gp_point(int p) {
    for (int a = 0; a < N; a++) if (a != p)
        for (int b = a + 1; b < N; b++) if (b != p && orient(a, b, p) == 0) return 0;
    return 1;
}
static int anchor_p;
static int cmp_ang(const void *u, const void *v) {
    int a = *(const int *)u, b = *(const int *)v;
    return orient(anchor_p, a, b) > 0 ? -1 : 1;
}
/* largest convex subset, capped: returns as soon as >= cap is found */
static int largest_convex(int cap) {
    int best = 2;
    static int q[MAXN], ch[MAXN][MAXN];
    for (int p = 0; p < N; p++) {
        int m = 0;
        for (int i = 0; i < N; i++)
            if (Y[i] > Y[p] || (Y[i] == Y[p] && X[i] > X[p])) q[m++] = i;
        anchor_p = p;
        qsort(q, m, sizeof(int), cmp_ang);
        for (int i = 0; i < m; i++)
            for (int j = 0; j < i; j++) {
                int v = 3;
                for (int k = 0; k < j; k++)
                    if (ch[k][j] + 1 > v && orient(q[k], q[j], q[i]) > 0) v = ch[k][j] + 1;
                ch[j][i] = v;
                if (v > best && orient(q[j], q[i], p) > 0) { best = v; if (best >= cap) return best; }
            }
    }
    return best;
}
static void dump(const char *path) {
    FILE *f = fopen(path, "w");
    for (int i = 0; i < N; i++) fprintf(f, "%lld %lld\n", X[i], Y[i]);
    fclose(f);
}
int main(int argc, char **argv) {
    if (argc != 7) { fprintf(stderr, "usage\n"); return 1; }
    FILE *f = fopen(argv[1], "r");
    ll x, y;
    N = 0;
    while (fscanf(f, "%lld %lld", &x, &y) == 2) { X[N] = x; Y[N] = y; N++; }
    fclose(f);
    rs = 0x9E3779B97F4A7C15ULL ^ ((u64)atoll(argv[2]) * 0x2545F4914F6CDD1DULL);
    for (int i = 0; i < 20; i++) rnd();
    int nsnap = atoi(argv[3]), steps = atoi(argv[4]);
    double rmin = atof(argv[5]);
    /* centre and scale each axis by an integer factor */
    ll mnx = X[0], mxx = X[0], mny = Y[0], mxy = Y[0];
    for (int i = 0; i < N; i++) {
        if (X[i] < mnx) mnx = X[i]; if (X[i] > mxx) mxx = X[i];
        if (Y[i] < mny) mny = Y[i]; if (Y[i] > mxy) mxy = Y[i];
    }
    ll cx = (mnx + mxx) / 2, cy = (mny + mxy) / 2;
    ll hx = (mxx - mnx) / 2 + 1, hy = (mxy - mny) / 2 + 1;
    ll fx = (1LL << 25) / hx, fy = (1LL << 25) / hy;
    if (fx < 1) fx = 1; if (fy < 1) fy = 1;
    for (int i = 0; i < N; i++) { X[i] = (X[i] - cx) * fx; Y[i] = (Y[i] - cy) * fy; }
    for (int i = 0; i < N; i++) if (llabs(X[i]) >= LIM || llabs(Y[i]) >= LIM) { fprintf(stderr, "bound\n"); return 2; }
    for (int i = 0; i < N; i++) if (!gp_point(i)) { fprintf(stderr, "base not in general position\n"); return 2; }
    int lc = largest_convex(7);
    if (lc >= 7) { fprintf(stderr, "base has a convex 7-gon\n"); return 2; }
    long long tried = 0, acc = 0, rej_gp = 0, rej_k = 0;
    char path[4096];
    for (int s = 1; s <= nsnap; s++) {
        int done = 0;
        while (done < steps) {
            tried++;
            if (tried > (ll)steps * nsnap * 1000) { fprintf(stderr, "stuck\n"); return 3; }
            int p = rnd() % N;
            double d = 1e300;
            for (int i = 0; i < N; i++) if (i != p) {
                double dx = (double)(X[i] - X[p]), dy = (double)(Y[i] - Y[p]);
                double dd = sqrt(dx * dx + dy * dy);
                if (dd < d) d = dd;
            }
            double r = exp(log(rmin) * urand());
            ll nx = X[p] + llround(grand() * r * d), ny = Y[p] + llround(grand() * r * d);
            if ((nx == X[p] && ny == Y[p]) || llabs(nx) >= LIM || llabs(ny) >= LIM) continue;
            ll ox = X[p], oy = Y[p];
            X[p] = nx; Y[p] = ny;
            if (!gp_point(p)) { rej_gp++; X[p] = ox; Y[p] = oy; continue; }
            if (largest_convex(7) >= 7) { rej_k++; X[p] = ox; Y[p] = oy; continue; }
            acc++; done++;
        }
        snprintf(path, sizeof path, "%s_%d.txt", argv[6], s);
        dump(path);
    }
    fprintf(stderr, "{\"tried\": %lld, \"accepted\": %lld, \"rej_gp\": %lld, \"rej_7gon\": %lld, \"fx\": %lld, \"fy\": %lld}\n",
            tried, acc, rej_gp, rej_k, fx, fy);
    return 0;
}
