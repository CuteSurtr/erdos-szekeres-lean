/* Search for 5-fold symmetric point sets with no K points in convex position. A point is an element of Z[z], z = e^{2 pi i/5},
   stored as 5 integer coefficients of 1, z, ..., z^4 (normalised so that c4 = 0); the rotation by 72 degrees is
   multiplication by z (a cyclic shift). Orientation is exact: cross(u, v) = Im(conj(u) v), and for w = sum w_j z^j,
   Im(w) / sin 72 = ((2(w1 - w4) - (w2 - w3)) + (w2 - w3) sqrt5) / 2, whose sign is decided with integers.
   usage: anneal5 m C K seed seconds box   (m orbits of 5 points, plus the centre if C = 1) */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
typedef long long ll;
static int n, m, C, K;
static ll P[128][5]; static double FY[128], FX[128];
static ll REP[32][5];
static unsigned long long rs;
static double urand(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (rs >> 11) * (1.0 / 9007199254740992.0); }
static ll irand(ll lo, ll hi) { return lo + (ll)(urand() * (double)(hi - lo + 1)); }
static int sgn_ab(ll A, ll B) {   /* sign of A + B sqrt5 */
  if (A >= 0 && B >= 0) return (A > 0 || B > 0);
  if (A <= 0 && B <= 0) return -(A < 0 || B < 0);
  __int128 a2 = (__int128)A * A, b2 = (__int128)5 * B * B;
  if (A > 0) return a2 > b2 ? 1 : (a2 < b2 ? -1 : 0);
  return b2 > a2 ? 1 : (b2 < a2 ? -1 : 0);
}
static int orient(int i, int j, int l) {
  ll u[5], v[5], w[5] = {0, 0, 0, 0, 0};
  for (int t = 0; t < 5; t++) { u[t] = P[j][t] - P[i][t]; v[t] = P[l][t] - P[i][t]; }
  for (int a = 0; a < 5; a++) if (u[a]) for (int b = 0; b < 5; b++) w[((5 - a) % 5 + b) % 5] += u[a] * v[b];   /* conj(u) v */
  return sgn_ab(2 * (w[1] - w[4]) - (w[2] - w[3]), w[2] - w[3]);
}
static void setxy(int i) {
  FX[i] = 0; FY[i] = 0;
  for (int t = 0; t < 5; t++) { FX[i] += P[i][t] * cos(2 * M_PI * t / 5); FY[i] += P[i][t] * sin(2 * M_PI * t / 5); }
}
static void place(int r) {
  ll c[5]; for (int t = 0; t < 5; t++) c[t] = REP[r][t];
  for (int k = 0; k < 5; k++) {
    int idx = r + k * m; ll c4 = c[4];
    for (int t = 0; t < 5; t++) P[idx][t] = c[t] - c4;   /* normalise */
    setxy(idx);
    ll nc[5]; for (int t = 0; t < 5; t++) nc[(t + 1) % 5] = c[t]; for (int t = 0; t < 5; t++) c[t] = nc[t];
  }
}
static int act[128];
static int same(int i, int j) { for (int t = 0; t < 5; t++) if (P[i][t] != P[j][t]) return 0; return 1; }
static int ok_orbit(int r) {
  int Q[5]; for (int k = 0; k < 5; k++) Q[k] = r + k * m;
  int zero = 1; for (int t = 0; t < 5; t++) if (P[Q[0]][t]) zero = 0;
  if (zero) return 0;
  for (int a = 0; a < 5; a++) for (int b = a + 1; b < 5; b++) for (int c = b + 1; c < 5; c++) if (orient(Q[a], Q[b], Q[c]) == 0) return 0;
  for (int s0 = 0; s0 < 5; s0++)
    for (int i = 0; i < n; i++) if (act[i]) {
      int skip = 0; for (int q = 0; q < 5; q++) if (Q[q] == i) skip = 1;
      if (skip) continue;
      if (same(i, Q[s0])) return 0;
      for (int j = i + 1; j < n; j++) if (act[j]) {
        int sk = 0; for (int q = 0; q < 5; q++) if (Q[q] == j) sk = 1;
        if (!sk && orient(Q[s0], i, j) == 0) return 0;
      }
      for (int q = 0; q < 5; q++) if (q != s0 && orient(Q[s0], Q[q], i) == 0) return 0;
    }
  return 1;
}
static int ord[128]; static int anc;
static int cmpang(const void *p, const void *q) { int i = *(const int *)p, j = *(const int *)q; return orient(anc, i, j) > 0 ? -1 : 1; }
static double D[128][128][10];
static double count_k(void) {
  double total = 0;
  for (int a = 0; a < n; a++) {
    int u = 0;
    for (int p = 0; p < n; p++) if (FY[p] > FY[a] || (FY[p] == FY[a] && FX[p] > FX[a])) ord[u++] = p;
    if (u < K - 1) continue;
    anc = a; qsort(ord, u, sizeof(int), cmpang);
    for (int j = 0; j < u; j++)
      for (int i = 0; i < j; i++) {
        double *d = D[i][j];
        for (int L = 0; L <= K; L++) d[L] = 0;
        d[3] = 1;
        for (int h = 0; h < i; h++)
          if (orient(ord[h], ord[i], ord[j]) > 0) { double *e = D[h][i]; for (int L = 3; L < K; L++) d[L + 1] += e[L]; }
        if (orient(ord[i], ord[j], a) > 0) total += d[K];
      }
  }
  return total;
}
int main(int argc, char **argv) {
  if (argc < 7) { fprintf(stderr, "usage: anneal5 m C K seed seconds box\n"); return 1; }
  m = atoi(argv[1]); C = atoi(argv[2]); K = atoi(argv[3]); rs = 0x9E3779B97F4A7C15ULL ^ (unsigned long long)atoll(argv[4]) * 2654435761ULL;
  double secs = atof(argv[5]); ll B = atoll(argv[6]);
  n = 5 * m + C;
  if (C) { for (int t = 0; t < 5; t++) P[n - 1][t] = 0; setxy(n - 1); }
  for (int i = 0; i < 20; i++) urand();
  time_t t0 = time(NULL); double bestall = 1e300; long long it = 0;
  while (difftime(time(NULL), t0) < secs) {
    for (int i = 0; i < n; i++) act[i] = (C && i == n - 1);
    for (int r = 0; r < m; r++) {
      for (int k = 0; k < 5; k++) act[r + k * m] = 1;
      do { for (int t = 0; t < 4; t++) REP[r][t] = irand(-B, B); REP[r][4] = 0; place(r); } while (!ok_orbit(r));
    }
    double cost = count_k(), best = cost, T = cost > 0 ? cost * 0.02 + 1 : 1; long long since = 0;
    while (cost > 0 && since < 200000 && difftime(time(NULL), t0) < secs) {
      it++; since++;
      int r = (int)irand(0, m - 1); ll old[5]; for (int t = 0; t < 5; t++) old[t] = REP[r][t];
      double sc = urand() < 0.1 ? (double)B : (double)B * pow(10.0, -3.0 * urand());
      for (int t = 0; t < 4; t++) REP[r][t] = old[t] + (ll)llround((urand() * 2 - 1) * sc);
      place(r);
      if (!ok_orbit(r)) { for (int t = 0; t < 5; t++) REP[r][t] = old[t]; place(r); continue; }
      double nc = count_k();
      if (nc <= cost || urand() < exp(-(nc - cost) / T)) { if (nc < best) { best = nc; since = 0; } cost = nc; }
      else { for (int t = 0; t < 5; t++) REP[r][t] = old[t]; place(r); }
      T *= 0.99995; if (T < 0.05) T = 0.05;
    }
    if (best < bestall) { bestall = best; fprintf(stderr, "[%.0fs] restart best %.0f (overall %.0f), iters %lld\n", difftime(time(NULL), t0), best, bestall, it); }
    if (cost == 0) {
      printf("FOUND G=5 m=%d C=%d K=%d n=%d\n", m, C, K, n);
      for (int i = 0; i < n; i++) printf("%lld %lld %lld %lld\n", P[i][0], P[i][1], P[i][2], P[i][3]);
      fflush(stdout); return 0;
    }
  }
  printf("NOTFOUND best %.0f\n", bestall); return 2;
}
