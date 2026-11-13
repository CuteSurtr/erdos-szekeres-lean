/* Heuristic realizer for a signotope: find integer points with orient(p_i,p_j,p_k) = sigma_ijk
 * for every triple. Floating point is used only to search; the final integer points are checked
 * exactly with __int128 orientations (and should be re-checked independently in Python).
 * usage: realize N file.sig seed restarts iters out.txt */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>

static int N, T, MODE = 0, DECAY = 0;
static double smargin = 0.02;
static int ti[70000], tj[70000], tk[70000], ts[70000];

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
    if (argc != 7) { fprintf(stderr, "usage: realize N file.sig seed restarts iters out.txt\n"); return 2; }
    N = atoi(argv[1]);
    if (getenv("REALIZE_DECAY")) DECAY = atoi(getenv("REALIZE_DECAY"));
    if (getenv("REALIZE_MODE")) MODE = atoi(getenv("REALIZE_MODE"));
    if (getenv("REALIZE_SMARGIN")) smargin = atof(getenv("REALIZE_SMARGIN"));
    FILE *f = fopen(argv[2], "r");
    unsigned long long seed = strtoull(argv[3], 0, 10) * 2654435761ULL + 12345;
    int restarts = atoi(argv[4]);
    long iters = atol(argv[5]);
    int a, b, c, s;
    T = 0;
    while (fscanf(f, "%d %d %d %d", &a, &b, &c, &s) == 4) { ti[T] = a - 1; tj[T] = b - 1; tk[T] = c - 1; ts[T] = s; T++; }
    fclose(f);
    double *x = malloc(sizeof(double) * N), *y = malloc(sizeof(double) * N);
    double *gx = malloc(sizeof(double) * N), *gy = malloc(sizeof(double) * N);
    double *mx = calloc(N, sizeof(double)), *my = calloc(N, sizeof(double));
    double *vx = calloc(N, sizeof(double)), *vy = calloc(N, sizeof(double));
    long long *X = malloc(sizeof(long long) * N), *Y = malloc(sizeof(long long) * N);
    int bestviol = 1 << 30;
    for (int r = 0; r < restarts; r++) {
        for (int i = 0; i < N; i++) { x[i] = -1 + 2.0 * (i + urand(&seed) * 0.5) / N; y[i] = 2 * urand(&seed) - 1; }
        memset(mx, 0, sizeof(double) * N); memset(my, 0, sizeof(double) * N);
        memset(vx, 0, sizeof(double) * N); memset(vy, 0, sizeof(double) * N);
        double lr = 2e-3, b1 = 0.9, b2 = 0.999, margin = 1e-3;
        int viol = T;
        for (long it = 1; it <= iters; it++) {
            memset(gx, 0, sizeof(double) * N); memset(gy, 0, sizeof(double) * N);
            viol = 0;
            for (int t = 0; t < T; t++) {
                int i = ti[t], j = tj[t], k = tk[t];
                double ux = x[j] - x[i], uy = y[j] - y[i], vx_ = x[k] - x[i], vy_ = y[k] - y[i];
                double d = ux * vy_ - uy * vx_;
                double sd = ts[t] * d;
                if (sd <= 0) viol++;
                if (MODE == 0) {
                    if (sd < margin) {
                        double w = -2.0 * (margin - sd) * ts[t]; /* dL/dd */
                        gx[i] += w * (y[j] - y[k]); gy[i] += w * (x[k] - x[j]);
                        gx[j] += w * (y[k] - y[i]); gy[j] += w * (x[i] - x[k]);
                        gx[k] += w * (y[i] - y[j]); gy[k] += w * (x[j] - x[i]);
                    }
                } else {
                    /* scale-invariant: f = d / (|u| |v|) = sine of the angle at p_i */
                    double a2 = ux * ux + uy * uy + 1e-300, b2 = vx_ * vx_ + vy_ * vy_ + 1e-300;
                    double ab = sqrt(a2 * b2);
                    double fsd = sd / ab;
                    if (fsd < smargin) {
                        double w = -2.0 * (smargin - fsd) * ts[t]; /* dL/df */
                        double f = d / ab;
                        /* df/dpj = (dd/dpj - f*ab*(u/a2))/ab ; df/dpk = (dd/dpk - f*ab*(v/b2))/ab */
                        double gjx = ((vy_) - f * ab * ux / a2) / ab, gjy = ((-vx_) - f * ab * uy / a2) / ab;
                        double gkx = ((-uy) - f * ab * vx_ / b2) / ab, gky = ((ux) - f * ab * vy_ / b2) / ab;
                        gx[j] += w * gjx; gy[j] += w * gjy;
                        gx[k] += w * gkx; gy[k] += w * gky;
                        gx[i] -= w * (gjx + gkx); gy[i] -= w * (gjy + gky);
                    }
                }
            }
            if (viol == 0) {
                /* try exact rounding at increasing scales */
                int ok = 0;
                for (int sc = 16; sc <= 44 && !ok; sc += 2) {
                    double S = ldexp(1.0, sc);
                    for (int i = 0; i < N; i++) { X[i] = llround(x[i] * S); Y[i] = llround(y[i] * S); }
                    if (exact_check(X, Y) == 0) ok = 1;
                }
                if (ok) {
                    FILE *o = fopen(argv[6], "w");
                    for (int i = 0; i < N; i++) fprintf(o, "%lld %lld\n", X[i], Y[i]);
                    fclose(o);
                    printf("REALIZED restart=%d iter=%ld; exact integer check passed (all %d triples)\n", r, it, T);
                    return 0;
                }
            }
            double c1 = 1 - pow(b1, (double)it), c2 = 1 - pow(b2, (double)it);
            for (int i = 0; i < N; i++) {
                mx[i] = b1 * mx[i] + (1 - b1) * gx[i]; vx[i] = b2 * vx[i] + (1 - b2) * gx[i] * gx[i];
                my[i] = b1 * my[i] + (1 - b1) * gy[i]; vy[i] = b2 * vy[i] + (1 - b2) * gy[i] * gy[i];
                x[i] -= lr * (mx[i] / c1) / (sqrt(vx[i] / c2) + 1e-12);
                y[i] -= lr * (my[i] / c1) / (sqrt(vy[i] / c2) + 1e-12);
                if (x[i] > 1) x[i] = 1; if (x[i] < -1) x[i] = -1;
                if (y[i] > 1) y[i] = 1; if (y[i] < -1) y[i] = -1;
            }
            if (it % 20000 == 0) { lr *= 0.7; if (lr < 1e-5) lr = 1e-5; if (DECAY) { margin *= 0.3; if (margin < 1e-12) margin = 1e-12; } }
        }
        if (viol < bestviol) bestviol = viol;
        printf("restart %d: final violated triples %d (best so far %d)\n", r, viol, bestviol);
        fflush(stdout);
    }
    printf("NOT REALIZED: best violated-triple count %d of %d\n", bestviol, T);
    return 1;
}
