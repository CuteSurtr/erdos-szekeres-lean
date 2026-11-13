/* Local nonlinear realizer seeded from given coordinates (floating-point search only; every
 * claimed realization must be re-checked exactly by realize_models.py).
 *
 * Same loss as tools/trackB/realize.c MODE 1 (scale-invariant: the sine of the angle at p_i,
 * hinge at SMARGIN), Adam steps, but the start is the given configuration: old points at their
 * (normalised) original coordinates, new points ('?' y) at their given x and a y drawn per restart.
 * Restart r > 0 also jitters every coordinate by 1e-3 * r. The x-order is kept by sorting checks:
 * a step that breaks the x-order of the labels is undone for that coordinate.
 *
 * usage: nl_realize RESTARTS ITERS SEED < input   (input as lp_realize: n, signs, x..., y... or '?')
 * output: "restart r viol v", then "BEST viol", "X ...", "Y ..." (%.17g) of the best configuration.
 */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int n, N3;
static int *ti, *tj, *tk, *ts;

static double urand(unsigned long long *s) {
    *s ^= *s << 13; *s ^= *s >> 7; *s ^= *s << 17;
    return (double)(*s >> 11) / 9007199254740992.0;
}

static int count_viol(const double *x, const double *y) {
    int v = 0;
    for (int r = 0; r < N3; r++) {
        int i = ti[r], j = tj[r], k = tk[r];
        double d = (x[j] - x[i]) * (y[k] - y[i]) - (y[j] - y[i]) * (x[k] - x[i]);
        if (ts[r] * d <= 0) v++;
    }
    return v;
}

int main(int argc, char **argv) {
    int restarts = argc > 1 ? atoi(argv[1]) : 4;
    long iters = argc > 2 ? atol(argv[2]) : 20000;
    unsigned long long seed = (argc > 3 ? strtoull(argv[3], 0, 10) : 1) * 2654435761ULL + 12345;
    double smargin = 0.01;
    if (scanf("%d", &n) != 1) return 2;
    static char sg[70000];
    if (scanf("%69999s", sg) != 1) return 2;
    N3 = n * (n - 1) * (n - 2) / 6;
    if ((int)strlen(sg) != N3) return 2;
    ti = malloc(sizeof(int) * N3); tj = malloc(sizeof(int) * N3); tk = malloc(sizeof(int) * N3); ts = malloc(sizeof(int) * N3);
    int r = 0;
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) for (int k = j + 1; k < n; k++, r++) {
        ti[r] = i; tj[r] = j; tk[r] = k; ts[r] = sg[r] == '+' ? 1 : -1;
    }
    double x0[200], y0[200];
    int isnew[200];
    for (int i = 0; i < n; i++) if (scanf("%lf", &x0[i]) != 1) return 2;
    for (int i = 0; i < n; i++) {
        char buf[64];
        if (scanf("%63s", buf) != 1) return 2;
        if (buf[0] == '?') { isnew[i] = 1; y0[i] = 0; } else { isnew[i] = 0; y0[i] = atof(buf); }
    }
    double xlo = x0[0], xhi = x0[n - 1];
    for (int i = 0; i < n; i++) x0[i] = -1 + 2 * (x0[i] - xlo) / (xhi - xlo);
    double ylo = 1e300, yhi = -1e300;
    for (int i = 0; i < n; i++) if (!isnew[i]) { if (y0[i] < ylo) ylo = y0[i]; if (y0[i] > yhi) yhi = y0[i]; }
    for (int i = 0; i < n; i++) y0[i] = isnew[i] ? 0 : (yhi > ylo ? -1 + 2 * (y0[i] - ylo) / (yhi - ylo) : 0);
    double x[200], y[200], gx[200], gy[200], mx[200], my[200], vx[200], vy[200], bx[200], by[200];
    int bestviol = 1 << 30;
    for (int rs = 0; rs < restarts; rs++) {
        for (int i = 0; i < n; i++) {
            x[i] = x0[i]; y[i] = y0[i];
            if (isnew[i]) y[i] = 2 * urand(&seed) - 1;
            if (rs > 0) { y[i] += 1e-3 * rs * (2 * urand(&seed) - 1); }
            mx[i] = my[i] = vx[i] = vy[i] = 0;
        }
        double lr = 1e-3, b1 = 0.9, b2 = 0.999;
        int viol = count_viol(x, y);
        for (long it = 1; it <= iters && viol > 0; it++) {
            memset(gx, 0, sizeof(double) * n); memset(gy, 0, sizeof(double) * n);
            for (int t = 0; t < N3; t++) {
                int i = ti[t], j = tj[t], k = tk[t];
                double ux = x[j] - x[i], uy = y[j] - y[i], vx_ = x[k] - x[i], vy_ = y[k] - y[i];
                double dd = ux * vy_ - uy * vx_;
                double a2 = ux * ux + uy * uy + 1e-300, b2_ = vx_ * vx_ + vy_ * vy_ + 1e-300;
                double ab = sqrt(a2 * b2_);
                double f = dd / ab, fsd = ts[t] * f;
                if (fsd < smargin) {
                    double w = -2.0 * (smargin - fsd) * ts[t];
                    double gjx = ((vy_) - f * ab * ux / a2) / ab, gjy = ((-vx_) - f * ab * uy / a2) / ab;
                    double gkx = ((-uy) - f * ab * vx_ / b2_) / ab, gky = ((ux) - f * ab * vy_ / b2_) / ab;
                    gx[j] += w * gjx; gy[j] += w * gjy;
                    gx[k] += w * gkx; gy[k] += w * gky;
                    gx[i] -= w * (gjx + gkx); gy[i] -= w * (gjy + gky);
                }
            }
            double c1 = 1 - pow(b1, (double)it), c2 = 1 - pow(b2, (double)it);
            for (int i = 0; i < n; i++) {
                mx[i] = b1 * mx[i] + (1 - b1) * gx[i]; vx[i] = b2 * vx[i] + (1 - b2) * gx[i] * gx[i];
                my[i] = b1 * my[i] + (1 - b1) * gy[i]; vy[i] = b2 * vy[i] + (1 - b2) * gy[i] * gy[i];
                double nx = x[i] - lr * (mx[i] / c1) / (sqrt(vx[i] / c2) + 1e-12);
                double ny = y[i] - lr * (my[i] / c1) / (sqrt(vy[i] / c2) + 1e-12);
                if ((i == 0 || nx > x[i - 1]) && (i == n - 1 || nx < x[i + 1])) x[i] = nx;
                y[i] = ny;
            }
            if (it % 200 == 0) viol = count_viol(x, y);
            if (it % 10000 == 0) { lr *= 0.7; if (lr < 1e-6) lr = 1e-6; }
        }
        viol = count_viol(x, y);
        printf("restart %d viol %d\n", rs, viol);
        if (viol < bestviol) { bestviol = viol; memcpy(bx, x, sizeof(double) * n); memcpy(by, y, sizeof(double) * n); }
        if (viol == 0) break;
    }
    printf("BEST %d\nX", bestviol);
    for (int i = 0; i < n; i++) printf(" %.17g", bx[i]);
    printf("\nY");
    for (int i = 0; i < n; i++) printf(" %.17g", by[i]);
    printf("\n");
    return 0;
}
