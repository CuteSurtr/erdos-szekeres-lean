/* Heuristic realizer for a rotationally symmetric chirotope.
 * Points: orbit representatives q_0..q_{t-1} (free), point (o,r) = R^r q_o with R = rotation by
 * 2*pi/m about the origin; optional centre at the origin (index m*t).  Floating point is used
 * only to search (Adam on a scale-invariant hinge loss over all required triple signs).  When
 * every sign is satisfied, all points are rounded to integers at increasing scales and ALL
 * triples are re-checked exactly with __int128; the integer point set (no longer exactly
 * symmetric, but a genuine point set) is written out.  Re-check it independently in Python.
 * usage: symrealize P m has_center file.sig seed restarts iters out.txt
 *   file.sig: lines "a b c s" with 0-based indices a<b<c over all P points, s = +1/-1 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

static int P, M, HASC, T, NORB, NT;
static int *ti, *tj, *tk, *ts;
static double smargin = 0.02;

static double urand(unsigned long long *s) {
    *s ^= *s << 13; *s ^= *s >> 7; *s ^= *s << 17;
    return (double)(*s >> 11) / 9007199254740992.0;
}

static int exact_check(long long *X, long long *Y) {
    int bad = 0;
    for (int t = 0; t < T; t++) {
        int i = ti[t], j = tj[t], k = tk[t];
        __int128 d = (__int128)(X[j] - X[i]) * (Y[k] - Y[i]) - (__int128)(Y[j] - Y[i]) * (X[k] - X[i]);
        int sg = d > 0 ? 1 : (d < 0 ? -1 : 0);
        if (sg != ts[t]) bad++;
    }
    return bad;
}

int main(int argc, char **argv) {
    if (argc != 9) { fprintf(stderr, "usage: symrealize P m has_center file.sig seed restarts iters out.txt\n"); return 2; }
    P = atoi(argv[1]); M = atoi(argv[2]); HASC = atoi(argv[3]);
    NORB = P - HASC; NT = NORB / M;
    if (NT * M != NORB) { fprintf(stderr, "bad P/m\n"); return 2; }
    if (getenv("REALIZE_SMARGIN")) smargin = atof(getenv("REALIZE_SMARGIN"));
    FILE *f = fopen(argv[4], "r");
    if (!f) { fprintf(stderr, "cannot open %s\n", argv[4]); return 2; }
    int cap = 1 << 16; ti = malloc(cap * sizeof(int)); tj = malloc(cap * sizeof(int)); tk = malloc(cap * sizeof(int)); ts = malloc(cap * sizeof(int));
    int a, b, c, s; T = 0;
    while (fscanf(f, "%d %d %d %d", &a, &b, &c, &s) == 4) {
        if (T == cap) { cap *= 2; ti = realloc(ti, cap * sizeof(int)); tj = realloc(tj, cap * sizeof(int)); tk = realloc(tk, cap * sizeof(int)); ts = realloc(ts, cap * sizeof(int)); }
        ti[T] = a; tj[T] = b; tk[T] = c; ts[T] = s; T++;
    }
    fclose(f);
    unsigned long long seed = strtoull(argv[5], 0, 10) * 2654435761ULL + 12345;
    int restarts = atoi(argv[6]);
    long iters = atol(argv[7]);
    double *qx = malloc(sizeof(double) * NT), *qy = malloc(sizeof(double) * NT);
    double *gqx = malloc(sizeof(double) * NT), *gqy = malloc(sizeof(double) * NT);
    double *mx = calloc(NT, sizeof(double)), *my = calloc(NT, sizeof(double));
    double *vx = calloc(NT, sizeof(double)), *vy = calloc(NT, sizeof(double));
    double *x = malloc(sizeof(double) * P), *y = malloc(sizeof(double) * P);
    double *gx = malloc(sizeof(double) * P), *gy = malloc(sizeof(double) * P);
    long long *X = malloc(sizeof(long long) * P), *Y = malloc(sizeof(long long) * P);
    double *cr = malloc(sizeof(double) * M), *sr = malloc(sizeof(double) * M);
    for (int r = 0; r < M; r++) { cr[r] = cos(2 * M_PI * r / M); sr[r] = sin(2 * M_PI * r / M); }
    int bestviol = 1 << 30;
    for (int rs = 0; rs < restarts; rs++) {
        for (int o = 0; o < NT; o++) { double rad = 0.2 + 0.8 * urand(&seed), an = 2 * M_PI * urand(&seed); qx[o] = rad * cos(an); qy[o] = rad * sin(an); }
        memset(mx, 0, sizeof(double) * NT); memset(my, 0, sizeof(double) * NT);
        memset(vx, 0, sizeof(double) * NT); memset(vy, 0, sizeof(double) * NT);
        double lr = 2e-3, b1 = 0.9, b2 = 0.999;
        int viol = T;
        for (long it = 1; it <= iters; it++) {
            for (int o = 0; o < NT; o++) for (int r = 0; r < M; r++) {
                int i = o * M + r;
                x[i] = cr[r] * qx[o] - sr[r] * qy[o];
                y[i] = sr[r] * qx[o] + cr[r] * qy[o];
            }
            if (HASC) { x[P - 1] = 0; y[P - 1] = 0; }
            memset(gx, 0, sizeof(double) * P); memset(gy, 0, sizeof(double) * P);
            viol = 0;
            for (int t = 0; t < T; t++) {
                int i = ti[t], j = tj[t], k = tk[t];
                double ux = x[j] - x[i], uy = y[j] - y[i], vx_ = x[k] - x[i], vy_ = y[k] - y[i];
                double d = ux * vy_ - uy * vx_;
                double sd = ts[t] * d;
                if (sd <= 0) viol++;
                double a2 = ux * ux + uy * uy + 1e-300, b2_ = vx_ * vx_ + vy_ * vy_ + 1e-300;
                double ab = sqrt(a2 * b2_);
                double fsd = sd / ab;
                if (fsd < smargin) {
                    double w = -2.0 * (smargin - fsd) * ts[t];
                    double fv = d / ab;
                    double gjx = ((vy_) - fv * ab * ux / a2) / ab, gjy = ((-vx_) - fv * ab * uy / a2) / ab;
                    double gkx = ((-uy) - fv * ab * vx_ / b2_) / ab, gky = ((ux) - fv * ab * vy_ / b2_) / ab;
                    gx[j] += w * gjx; gy[j] += w * gjy;
                    gx[k] += w * gkx; gy[k] += w * gky;
                    gx[i] -= w * (gjx + gkx); gy[i] -= w * (gjy + gky);
                }
            }
            if (viol == 0) {
                int ok = 0;
                for (int sc = 16; sc <= 44 && !ok; sc += 2) {
                    double S = ldexp(1.0, sc);
                    for (int i = 0; i < P; i++) { X[i] = llround(x[i] * S); Y[i] = llround(y[i] * S); }
                    if (exact_check(X, Y) == 0) ok = 1;
                }
                if (ok) {
                    FILE *o = fopen(argv[8], "w");
                    for (int i = 0; i < P; i++) fprintf(o, "%lld %lld\n", X[i], Y[i]);
                    fclose(o);
                    printf("REALIZED restart=%d iter=%ld; exact integer check passed (all %d triples)\n", rs, it, T);
                    return 0;
                }
            }
            /* chain rule to representatives: grad_q += R^{-r} grad_point */
            memset(gqx, 0, sizeof(double) * NT); memset(gqy, 0, sizeof(double) * NT);
            for (int o = 0; o < NT; o++) for (int r = 0; r < M; r++) {
                int i = o * M + r;
                gqx[o] += cr[r] * gx[i] + sr[r] * gy[i];
                gqy[o] += -sr[r] * gx[i] + cr[r] * gy[i];
            }
            double c1 = 1 - pow(b1, (double)it), c2 = 1 - pow(b2, (double)it);
            for (int o = 0; o < NT; o++) {
                mx[o] = b1 * mx[o] + (1 - b1) * gqx[o]; vx[o] = b2 * vx[o] + (1 - b2) * gqx[o] * gqx[o];
                my[o] = b1 * my[o] + (1 - b1) * gqy[o]; vy[o] = b2 * vy[o] + (1 - b2) * gqy[o] * gqy[o];
                qx[o] -= lr * (mx[o] / c1) / (sqrt(vx[o] / c2) + 1e-12);
                qy[o] -= lr * (my[o] / c1) / (sqrt(vy[o] / c2) + 1e-12);
                double rad = sqrt(qx[o] * qx[o] + qy[o] * qy[o]);
                if (rad > 1) { qx[o] /= rad; qy[o] /= rad; }
                if (rad < 0.02) { qx[o] *= 0.02 / rad; qy[o] *= 0.02 / rad; }
            }
            if (it % 20000 == 0) { lr *= 0.7; if (lr < 1e-5) lr = 1e-5; }
        }
        if (viol < bestviol) bestviol = viol;
        printf("restart %d: final violated triples %d (best so far %d)\n", rs, viol, bestviol);
        fflush(stdout);
    }
    printf("NOT REALIZED: best violated-triple count %d of %d\n", bestviol, T);
    return 1;
}
