/* Float (long double) counter of convex K-gons, for search only (certification is exact and separate).
   Anchor DP as in K9SEARCH/tools/anneal8.c: anchor = lowest (y, then x) vertex; chains in angular order.
   long long countk(int n, const double *X, const double *Y, int K, double *mindet)
   Also returns the minimum scale-free |orientation| in *mindet. */
#include <stdlib.h>
#include <string.h>
#include <math.h>
#define NMAX 200
#define KMAX 12
static signed char O[NMAX][NMAX][NMAX];
static long long cnt[NMAX][NMAX][KMAX + 1];

long long countk(int n, const double *X, const double *Y, int K, double *mindet) {
  if (n > NMAX || K > KMAX) return -1;
  double md = 1e300;
  for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) {
    long double d = ((long double)X[b] - X[a]) * ((long double)Y[c] - Y[a]) - ((long double)Y[b] - Y[a]) * ((long double)X[c] - X[a]);
    long double ab = hypotl(X[b] - X[a], Y[b] - Y[a]), ac = hypotl(X[c] - X[a], Y[c] - Y[a]), bc = hypotl(X[c] - X[b], Y[c] - Y[b]);
    long double mx = ab > ac ? ab : ac; if (bc > mx) mx = bc;
    double rd = (double)(fabsl(d) / (mx * mx)); if (rd < md) md = rd;
    signed char s = d > 0 ? 1 : -1;
    O[a][b][c] = O[b][c][a] = O[c][a][b] = s; O[b][a][c] = O[a][c][b] = O[c][b][a] = -s;
  }
  *mindet = md;
  long long total = 0;
  int q[NMAX]; double ang[NMAX];
  for (int p = 0; p < n; p++) {
    int r = 0;
    for (int i = 0; i < n; i++) if (i != p && (Y[i] > Y[p] || (Y[i] == Y[p] && X[i] > X[p]))) { q[r] = i; ang[r] = atan2(Y[i] - Y[p], X[i] - X[p]); r++; }
    if (r < K - 1) continue;
    for (int i = 1; i < r; i++) { int t = q[i]; double a = ang[i]; int j = i - 1; while (j >= 0 && ang[j] > a) { q[j + 1] = q[j]; ang[j + 1] = ang[j]; j--; } q[j + 1] = t; ang[j + 1] = a; }
    for (int i = 0; i < r; i++) for (int j = i + 1; j < r; j++) { memset(cnt[i][j], 0, sizeof(long long) * (K + 1)); cnt[i][j][3] = 1; }
    for (int j = 1; j < r; j++) {
      int qj = q[j];
      for (int i = 0; i < j; i++) {
        long long *c = cnt[i][j]; int qi = q[i];
        if (c[K] && O[qi][qj][p] > 0) total += c[K];
        int any = 0; for (int l = 3; l < K; l++) if (c[l]) { any = 1; break; }
        if (!any) continue;
        for (int k = j + 1; k < r; k++) if (O[qi][qj][q[k]] > 0) {
          long long *d = cnt[j][k];
          for (int l = 3; l < K; l++) d[l + 1] += c[l];
        }
      }
    }
  }
  return total;
}
