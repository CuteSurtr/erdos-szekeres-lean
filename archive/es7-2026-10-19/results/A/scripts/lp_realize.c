/* Fixed-x / fixed-y alternating LP realizer for an x-sorted signotope (floating point search
 * only; every claimed realization must be re-checked exactly, see realize_models.py).
 *
 * Orientation O(i,j,k) = x_i(y_j-y_k) + x_j(y_k-y_i) + x_k(y_i-y_j) is linear in y for fixed x
 * and linear in x for fixed y. Each LP maximises the worst normalised margin t:
 *     s_r * (a_r . v) >= t * ||a_r||   for every triple r (sign s_r from the signotope),
 *     v_{i+1} - v_i  >= t * sqrt(2)     (x-LP only: keep the x-order of the labels),
 *     -1 <= v_i <= 1,  -1 <= t <= 1.
 * With v = u - 1, t = tau - 1 (u, tau >= 0) every right-hand side is >= 0 (a_r . 1 = 0), so the
 * origin is a feasible basis and a plain primal simplex on a condensed (Tucker) tableau works:
 * rows = constraints (basic slacks), columns = the n+1 structural variables.
 *
 * Each LP is restricted to a trust region of half-width rho around the current point (rho doubles
 * every round, starting at 0.02 in coordinates normalised to [-1,1]), so a solution stays near the
 * original coordinates and cannot collapse to a degenerate (all-collinear) point.
 *
 * usage: lp_realize ROUNDS < input   input: n, sign string, x_1..x_n (increasing), y_1..y_n where
 *        a y given as '?' marks a new point (free in the first y-LP)
 * output: lines "round k ... yLP t=..." / "xLP t=...", then "BEST t", "X ...", "Y ..." (%.17g). */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int n, m, ncol;
static double *T;          /* m x ncol tableau alpha */
static double *beta, *d;   /* rhs, reduced objective */
static int *basic, *nonb;  /* variable ids: 0..ncol-1 structural, ncol+i slack of row i */

/* max c.z s.t. G z <= h, z >= 0 with h >= 0. G is m x ncol row-major. Returns status. */
static int simplex(const double *G, const double *h, const double *c, double *z, double *obj) {
    memcpy(T, G, sizeof(double) * m * ncol);
    memcpy(beta, h, sizeof(double) * m);
    memcpy(d, c, sizeof(double) * ncol);
    for (int i = 0; i < m; i++) basic[i] = ncol + i;
    for (int j = 0; j < ncol; j++) nonb[j] = j;
    double f = 0;
    int it;
    for (it = 0; it < 20000; it++) {
        int jj = -1;
        double best = 1e-11;
        if (it < 10000) {
            for (int j = 0; j < ncol; j++) if (d[j] > best) { best = d[j]; jj = j; }
        } else { /* Bland's rule as an anti-cycling fallback */
            int bid = 1 << 30;
            for (int j = 0; j < ncol; j++) if (d[j] > 1e-11 && nonb[j] < bid) { bid = nonb[j]; jj = j; }
        }
        if (jj < 0) break;
        int r = -1;
        double rmin = 1e300, amax = 0;
        for (int i = 0; i < m; i++) {
            double a = T[i * ncol + jj];
            if (a > 1e-12) {
                double q = beta[i] / a;
                if (q < rmin - 1e-14 || (q <= rmin + 1e-14 && a > amax)) { rmin = q; amax = a; r = i; }
            }
        }
        if (r < 0) return 2; /* unbounded (cannot happen with the box) */
        double p = T[r * ncol + jj];
        double *Tr = T + r * ncol;
        beta[r] /= p;
        for (int k = 0; k < ncol; k++) if (k != jj) Tr[k] /= p;
        Tr[jj] = 1.0 / p;
        for (int i = 0; i < m; i++) {
            if (i == r) continue;
            double *Ti = T + i * ncol;
            double a = Ti[jj];
            if (a == 0) continue;
            beta[i] -= a * beta[r];
            if (beta[i] < 0 && beta[i] > -1e-13) beta[i] = 0;
            for (int k = 0; k < ncol; k++) if (k != jj) Ti[k] -= a * Tr[k];
            Ti[jj] = -a / p;
        }
        double dj = d[jj];
        f += dj * beta[r];
        for (int k = 0; k < ncol; k++) if (k != jj) d[k] -= dj * Tr[k];
        d[jj] = -dj / p;
        int tmp = basic[r]; basic[r] = nonb[jj]; nonb[jj] = tmp;
    }
    for (int j = 0; j < ncol; j++) z[j] = 0;
    for (int i = 0; i < m; i++) if (basic[i] < ncol) z[basic[i]] = beta[i];
    *obj = f;
    return it >= 20000 ? 1 : 0;
}

static int N3;
static int *ti, *tj, *tk, *ts;

static double min_margin(const double *x, const double *y) {
    double mn = 1e300;
    for (int r = 0; r < N3; r++) {
        int i = ti[r], j = tj[r], k = tk[r];
        double a0 = x[k] - x[j], a1 = -(x[k] - x[i]), a2 = x[j] - x[i];
        double o = a0 * y[i] + a1 * y[j] + a2 * y[k];
        double w = sqrt(a0 * a0 + a1 * a1 + a2 * a2);
        double v = ts[r] * o / w;
        if (v < mn) mn = v;
    }
    return mn;
}

/* LP in y (which=0, x fixed) or in x (which=1, y fixed), restricted to the box
 * lo_i <= v_i <= hi_i (a trust region around the current point). With v = u + lo and
 * t = tau + tlow, where tlow is below every row margin at v = lo, all right-hand sides are >= 0
 * and the origin is a feasible basis. Result written to out; returns the LP value of t. */
static double solve_lp(int which, const double *x, const double *y, const double *lo, const double *hi,
                       double *out) {
    int extra = which ? n - 1 : 0;
    m = N3 + n + extra + 1;
    ncol = n + 1;
    double *G = calloc((size_t)m * ncol, sizeof(double)), *h = calloc(m, sizeof(double));
    double *c = calloc(ncol, sizeof(double)), *z = calloc(ncol, sizeof(double));
    double *W = calloc(m, sizeof(double)), *L = calloc(m, sizeof(double)); /* row weight, margin at lo */
    int row = 0;
    for (int r = 0; r < N3; r++, row++) {
        int i = ti[r], j = tj[r], k = tk[r];
        double a[3];
        if (!which) { a[0] = x[k] - x[j]; a[1] = -(x[k] - x[i]); a[2] = x[j] - x[i]; }
        else { a[0] = y[j] - y[k]; a[1] = y[k] - y[i]; a[2] = y[i] - y[j]; }
        double w = sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2]);
        if (w == 0) w = 1e-300;
        G[row * ncol + i] = -ts[r] * a[0];
        G[row * ncol + j] = -ts[r] * a[1];
        G[row * ncol + k] = -ts[r] * a[2];
        G[row * ncol + n] = w;
        W[row] = w;
        L[row] = ts[r] * (a[0] * lo[i] + a[1] * lo[j] + a[2] * lo[k]); /* s * a.lo */
    }
    int box0 = row;
    for (int i = 0; i < n; i++, row++) { G[row * ncol + i] = 1; h[row] = hi[i] - lo[i]; W[row] = 0; }
    int ord0 = row;
    for (int i = 0; i + 1 < n && which; i++, row++) {
        double w = sqrt(2.0);
        G[row * ncol + i] = 1; G[row * ncol + i + 1] = -1; G[row * ncol + n] = w;
        W[row] = w; L[row] = lo[i + 1] - lo[i];
    }
    double tlow = 1e300;
    for (int q = 0; q < box0; q++) if (L[q] / W[q] < tlow) tlow = L[q] / W[q];
    for (int q = ord0; q < row; q++) if (L[q] / W[q] < tlow) tlow = L[q] / W[q];
    tlow -= 1e-9;
    for (int q = 0; q < box0; q++) h[q] = L[q] - tlow * W[q];
    for (int q = ord0; q < row; q++) h[q] = L[q] - tlow * W[q];
    G[row * ncol + n] = 1; h[row] = 1.0 - tlow; row++; /* t <= 1 */
    c[n] = 1;
    double obj;
    simplex(G, h, c, z, &obj);
    for (int i = 0; i < n; i++) out[i] = z[i] + lo[i];
    double t = z[n] + tlow;
    free(G); free(h); free(c); free(z); free(W); free(L);
    return t;
}

int main(int argc, char **argv) {
    int rounds = argc > 1 ? atoi(argv[1]) : 6;
    if (scanf("%d", &n) != 1) return 2;
    static char sg[70000];
    if (scanf("%69999s", sg) != 1) return 2;
    N3 = n * (n - 1) * (n - 2) / 6;
    if ((int)strlen(sg) != N3) { fprintf(stderr, "bad sign string\n"); return 2; }
    ti = malloc(sizeof(int) * N3); tj = malloc(sizeof(int) * N3); tk = malloc(sizeof(int) * N3); ts = malloc(sizeof(int) * N3);
    int r = 0;
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) for (int k = j + 1; k < n; k++, r++) {
        ti[r] = i; tj[r] = j; tk[r] = k; ts[r] = sg[r] == '+' ? 1 : -1;
    }
    double *x = malloc(sizeof(double) * n), *y = malloc(sizeof(double) * n);
    double *bx = malloc(sizeof(double) * n), *by = malloc(sizeof(double) * n);
    for (int i = 0; i < n; i++) if (scanf("%lf", &x[i]) != 1) return 2;
    static int isnew[200];
    for (int i = 0; i < n; i++) {
        char buf[64];
        if (scanf("%63s", buf) != 1) return 2;
        if (buf[0] == '?') { isnew[i] = 1; y[i] = 0; } else { isnew[i] = 0; y[i] = atof(buf); }
    }
    /* normalise x to [-1,1] (positive affine map: orientations unchanged) */
    double xlo = x[0], xhi = x[n - 1];
    for (int i = 0; i < n; i++) x[i] = -1 + 2 * (x[i] - xlo) / (xhi - xlo);
    double ylo = 1e300, yhi = -1e300;
    for (int i = 0; i < n; i++) if (!isnew[i]) { if (y[i] < ylo) ylo = y[i]; if (y[i] > yhi) yhi = y[i]; }
    for (int i = 0; i < n; i++) y[i] = isnew[i] ? 0 : (yhi > ylo ? -1 + 2 * (y[i] - ylo) / (yhi - ylo) : 0);
    T = malloc(sizeof(double) * (size_t)(N3 + 2 * n + 2) * (n + 1));
    beta = malloc(sizeof(double) * (N3 + 2 * n + 2)); d = malloc(sizeof(double) * (n + 1));
    basic = malloc(sizeof(int) * (N3 + 2 * n + 2)); nonb = malloc(sizeof(int) * (n + 1));
    double best = min_margin(x, y);
    memcpy(bx, x, sizeof(double) * n); memcpy(by, y, sizeof(double) * n);
    printf("start margin %.3e\n", best);
    double *v = malloc(sizeof(double) * n), *lo = malloc(sizeof(double) * n), *hi = malloc(sizeof(double) * n);
    /* NEWMASK: points whose initial y is unknown get the full box in the first y-LP */
    double rho = 0.02;
    for (int k = 0; k < rounds; k++, rho *= 2) {
        if (rho > 2) rho = 2;
        for (int i = 0; i < n; i++) {
            double rr = (k == 0 && isnew[i]) ? 2.0 : rho;
            lo[i] = y[i] - rr; hi[i] = y[i] + rr;
        }
        double t = solve_lp(0, x, y, lo, hi, v);
        memcpy(y, v, sizeof(double) * n);
        double mm = min_margin(x, y);
        printf("round %d rho=%.3g yLP t=%.3e check=%.3e\n", k, rho, t, mm);
        if (mm > best) { best = mm; memcpy(bx, x, sizeof(double) * n); memcpy(by, y, sizeof(double) * n); }
        if (mm > 1e-9) break;
        for (int i = 0; i < n; i++) { lo[i] = x[i] - rho; hi[i] = x[i] + rho; }
        t = solve_lp(1, x, y, lo, hi, v);
        int sorted = 1;
        for (int i = 0; i + 1 < n; i++) if (!(v[i] < v[i + 1])) sorted = 0;
        if (sorted) memcpy(x, v, sizeof(double) * n);
        mm = min_margin(x, y);
        printf("round %d rho=%.3g xLP t=%.3e check=%.3e sorted=%d\n", k, rho, t, mm, sorted);
        if (mm > best) { best = mm; memcpy(bx, x, sizeof(double) * n); memcpy(by, y, sizeof(double) * n); }
        if (mm > 1e-9) break;
    }
    printf("BEST %.6e\nX", best);
    for (int i = 0; i < n; i++) printf(" %.17g", bx[i]);
    printf("\nY");
    for (int i = 0; i < n; i++) printf(" %.17g", by[i]);
    printf("\n");
    return 0;
}
