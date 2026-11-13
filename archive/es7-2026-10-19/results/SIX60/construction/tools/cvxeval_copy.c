/* cvxeval.c -- fast float evaluator for the sixfold search (evidence only; exact checks are done elsewhere).

   Counts convex k-gons (k = 3..KMAX, KMAX = 8) of a planar point set given in double coordinates; orientation signs
   are computed in long double.  Every convex polygon is counted once, at its lowest vertex a (minimum (y, x)); the
   other vertices are higher, sorted by angle around a (comparator = orientation table), and a chain DP over pairs
   (i, j) of consecutive vertices counts chains a -> ... -> ord[i] -> ord[j] with L vertices (L <= KMAX).  Chains
   longer than KMAX are dropped: every convex polygon with > KMAX vertices contains convex KMAX-subsets, which are
   counted on their own, so count[KMAX] = 0 iff there is no convex KMAX-subset.

   API (ctypes):
     int cvx_count(int n, const double *x, const double *y, unsigned long long *cnt, unsigned long long abort_above)
         cnt[k] for k = 0..KMAX (k < 3 unused).  If abort_above > 0 and the running count of KMAX-gons exceeds it,
         the computation stops early and returns 1 (counts partial); otherwise returns 0.
     int six_points(int t, const double *lr, const double *th, double *x, double *y)
         layer i: 6 points exp(lr[i]) * e^{i (th[i] + k pi/3)}, k = 0..5; point id 6 i + k.
     int cvx_eval6(int t, const double *lr, const double *th, unsigned long long *cnt, unsigned long long abort_above)
         six_points + cvx_count.
     int min_orient(int n, x, y, double *out) : smallest |orient|/(|ab||ac|) over triples (a sine), for diagnostics.
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <stdint.h>

#define KMAX 8
#define NMAX 64
typedef unsigned long long u64;

static int orient_ld(long double ax, long double ay, long double bx, long double by, long double cx, long double cy) {
  long double d = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax);
  return d > 0 ? 1 : (d < 0 ? -1 : 0);
}

int six_points(int t, const double *lr, const double *th, double *x, double *y) {
  for (int i = 0; i < t; i++) {
    long double r = expl((long double)lr[i]);
    for (int k = 0; k < 6; k++) {
      long double a = (long double)th[i] + k * (3.14159265358979323846264338327950288L / 3.0L);
      x[6 * i + k] = (double)(r * cosl(a));
      y[6 * i + k] = (double)(r * sinl(a));
    }
  }
  return 6 * t;
}

static __thread signed char O[NMAX * NMAX * NMAX];
static __thread u64 D[NMAX * NMAX * (KMAX - 2)];

int cvx_count(int n, const double *x, const double *y, u64 *cnt, u64 abort_above) {
  if (n > NMAX) return -1;
  for (int k = 0; k <= KMAX; k++) cnt[k] = 0;
  /* orientation table */
  for (int a = 0; a < n; a++) {
    O[(a * n + a) * n + a] = 0;
    for (int b = a + 1; b < n; b++) {
      O[(a * n + b) * n + a] = O[(a * n + a) * n + b] = O[(b * n + a) * n + a] = 0;
      O[(b * n + b) * n + a] = O[(b * n + a) * n + b] = O[(a * n + b) * n + b] = 0;
      for (int c = b + 1; c < n; c++) {
        int s = orient_ld(x[a], y[a], x[b], y[b], x[c], y[c]);
        O[(a * n + b) * n + c] = s; O[(b * n + c) * n + a] = s; O[(c * n + a) * n + b] = s;
        O[(b * n + a) * n + c] = -s; O[(a * n + c) * n + b] = -s; O[(c * n + b) * n + a] = -s;
      }
    }
  }
  /* lexicographic (y, x) order */
  int rk[NMAX], idx[NMAX];
  for (int i = 0; i < n; i++) idx[i] = i;
  for (int i = 1; i < n; i++) {   /* insertion sort */
    int v = idx[i], j = i - 1;
    while (j >= 0 && (y[idx[j]] > y[v] || (y[idx[j]] == y[v] && x[idx[j]] > x[v]))) { idx[j + 1] = idx[j]; j--; }
    idx[j + 1] = v;
  }
  for (int i = 0; i < n; i++) rk[idx[i]] = i;
  int ord[NMAX];
  const int W = KMAX - 2;   /* slots for L = 3..KMAX */
  for (int r = 0; r < n - 2; r++) {
    int a = idx[r];
    int u = 0;
    for (int s = r + 1; s < n; s++) ord[u++] = idx[s];
    /* sort by angle around a: x before y iff orient(a, x, y) > 0 */
    for (int i = 1; i < u; i++) {
      int v = ord[i], j = i - 1;
      const signed char *Oa = O + (size_t)a * n * n;
      while (j >= 0 && Oa[ord[j] * n + v] < 0) { ord[j + 1] = ord[j]; j--; }
      ord[j + 1] = v;
    }
    for (int j = 1; j < u; j++) {
      int oj = ord[j];
      for (int i = 0; i < j; i++) {
        int oi = ord[i];
        u64 *d = D + ((size_t)i * NMAX + j) * W;
        d[0] = 1; for (int L = 1; L < W; L++) d[L] = 0;
        const signed char *Oij = O + ((size_t)oi * n + oj) * n;   /* orient(oi, oj, h) = orient(h, oi, oj) */
        for (int h = 0; h < i; h++) {
          if (Oij[ord[h]] > 0) {
            const u64 *e = D + ((size_t)h * NMAX + i) * W;
            for (int L = 0; L < W - 1; L++) d[L + 1] += e[L];
          }
        }
        if (Oij[a] > 0) for (int L = 0; L < W; L++) cnt[L + 3] += d[L];
      }
    }
    if (abort_above && cnt[KMAX] > abort_above) return 1;
  }
  return 0;
}

int cvx_eval6(int t, const double *lr, const double *th, u64 *cnt, u64 abort_above) {
  double x[NMAX], y[NMAX];
  int n = six_points(t, lr, th, x, y);
  return cvx_count(n, x, y, cnt, abort_above);
}

double min_sine(int n, const double *x, const double *y) {
  double best = 1e300;
  for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) {
    long double ux = x[b] - x[a], uy = y[b] - y[a], vx = x[c] - x[a], vy = y[c] - y[a];
    long double d = ux * vy - uy * vx;
    long double s = fabsl(d) / (sqrtl(ux * ux + uy * uy) * sqrtl(vx * vx + vy * vy));
    if ((double)s < best) best = (double)s;
  }
  return best;
}

#ifdef MAIN
#include <time.h>
int main(int argc, char **argv) {
  /* read "x y" lines from stdin; print counts */
  static double x[NMAX], y[NMAX]; int n = 0;
  while (n < NMAX && scanf("%lf %lf", &x[n], &y[n]) == 2) n++;
  u64 cnt[KMAX + 1];
  int reps = argc > 1 ? atoi(argv[1]) : 1;
  clock_t c0 = clock();
  for (int r = 0; r < reps; r++) cvx_count(n, x, y, cnt, 0);
  double el = (double)(clock() - c0) / CLOCKS_PER_SEC / reps;
  printf("n=%d", n);
  for (int k = 3; k <= KMAX; k++) printf(" c%d=%llu", k, cnt[k]);
  printf("  time/eval=%.3f ms\n", el * 1e3);
  return 0;
}
#endif
