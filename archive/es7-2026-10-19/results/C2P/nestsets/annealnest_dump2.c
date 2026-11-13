/* annealnest: simulated annealing for point sets with a prescribed symmetry and no K points in convex position, as in
   results/SYMMAX/annealg.c, plus a penalty NW * ((|hull| - 4) + (|second layer| - 4)), so that a zero-cost set has a
   parallelogram hull and a parallelogram second layer (nested parallelograms).
   G = 2: the half-turn (a, b) -> (-a, -b) in ordinary integer coordinates (all sets of this folder). G = 4: the
   quarter-turn. G = 3 or 6: integer coordinates in the Eisenstein basis (1, w), w = e^{2 pi i/3}, an affine image of the
   plane, so convex position is unchanged. G = M: the mirror (a, b) -> (-a, b).
   m orbits plus F fixed points: the centre (0 or 1) for rotations, points on the axis a = 0 (0..2) for the mirror.
   Cost: the exact number of convex K-gons (dynamic program anchored at the lowest vertex) plus the penalty. Each move
   changes one orbit representative, keeping all points distinct and without collinear triples.
   usage: annealnest G m F K seed seconds box nestweight [dumpfile]
   With dumpfile, each new overall best set is written to it (a line '# cost C', then one point per line). */
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef long long ll;
static int n, m, C, K, G, s;
static ll X[128], Y[128], RA[70], RB[70];
static int act[128];
static unsigned long long rs;
static double urand(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (rs >> 11) * (1.0 / 9007199254740992.0); }
static ll irand(ll lo, ll hi) { return lo + (ll)(urand() * (double)(hi - lo + 1)); }
static int orient(int i, int j, int l) {
  __int128 v = (__int128)(X[j] - X[i]) * (Y[l] - Y[i]) - (__int128)(Y[j] - Y[i]) * (X[l] - X[i]);
  return (v > 0) - (v < 0);
}
static void rot(ll *a, ll *b) {
  ll x = *a, y = *b;
  if (G == 3) { *a = -y; *b = x - y; }        /* times w */
  else if (G == 6) { *a = x - y; *b = x; }    /* times 1 + w = e^{i pi/3} */
  else if (G == 4) { *a = -y; *b = x; }
  else if (G == 2) { *a = -x; *b = -y; }
  else { *a = -x; *b = y; }                   /* mirror */
}
static void place(int r) {
  if (r >= m) { X[s * m + (r - m)] = 0; Y[s * m + (r - m)] = RB[r]; return; }   /* fixed point on the mirror axis */
  ll a = RA[r], b = RB[r];
  for (int t = 0; t < s; t++) { X[r + t * m] = a; Y[r + t * m] = b; rot(&a, &b); }
}
static int ok_orbit(int r) {   /* the points of orbit r: distinct from all others and no collinear triple with them */
  int P[8], np = 0;
  if (r >= m) { P[np++] = s * m + (r - m); }
  else {
    if (G == 'M' ? RA[r] == 0 : (RA[r] == 0 && RB[r] == 0)) return 0;
    for (int t = 0; t < s; t++) P[np++] = r + t * m;
  }
  for (int i = 0; i < np; i++) for (int j = i + 1; j < np; j++) if (X[P[i]] == X[P[j]] && Y[P[i]] == Y[P[j]]) return 0;
  for (int q = 0; q < np; q++) for (int i2 = q + 1; i2 < np; i2++) for (int j2 = i2 + 1; j2 < np; j2++) if (orient(P[q], P[i2], P[j2]) == 0) return 0;
  for (int s0 = 0; s0 < np; s0++)
    for (int i = 0; i < n; i++) if (i != P[s0] && act[i]) {
      int skip = 0; for (int q = 0; q < np; q++) if (P[q] == i) skip = 1;
      if (skip) continue;
      if (X[i] == X[P[s0]] && Y[i] == Y[P[s0]]) return 0;
      for (int j = i + 1; j < n; j++) if (j != P[s0] && act[j] && orient(P[s0], i, j) == 0) return 0;
    }
  return 1;
}
static int ord[128]; static int anc;
static int cmpang(const void *p, const void *q) { int i = *(const int *)p, j = *(const int *)q; return orient(anc, i, j) > 0 ? -1 : 1; }
static double D[128][128][10];
static double NW; static const char *DUMP = 0; static ll BX[128], BY[128];   /* weight of the nested-parallelogram penalty */
static int hullmark(int *in, int *mark) {   /* marks the convex hull vertices of the active points flagged in in[] */
  int idx[128], k = 0, H[260], h = 0;
  for (int i = 0; i < n; i++) if (in[i]) idx[k++] = i;
  for (int a = 1; a < k; a++) { int v = idx[a], b = a; while (b > 0 && (X[idx[b-1]] > X[v] || (X[idx[b-1]] == X[v] && Y[idx[b-1]] > Y[v]))) { idx[b] = idx[b-1]; b--; } idx[b] = v; }
  if (k < 3) { for (int i = 0; i < k; i++) mark[idx[i]] = 1; return k; }
  for (int i = 0; i < k; i++) { while (h >= 2 && orient(H[h-2], H[h-1], idx[i]) <= 0) h--; H[h++] = idx[i]; }
  for (int i = k - 2, lo = h + 1; i >= 0; i--) { while (h >= lo && orient(H[h-2], H[h-1], idx[i]) <= 0) h--; H[h++] = idx[i]; }
  h--; for (int i = 0; i < h; i++) mark[H[i]] = 1;
  return h;
}
static double nest_penalty(void) {
  int in[128], m1[128] = {0}, m2[128] = {0};
  for (int i = 0; i < n; i++) in[i] = act[i];
  int h1 = hullmark(in, m1);
  for (int i = 0; i < n; i++) in[i] = act[i] && !m1[i];
  int h2 = hullmark(in, m2);
  return NW * ((h1 - 4) + (h2 - 4));
}
static double count_k(void) {
  double total = 0;
  for (int a = 0; a < n; a++) {
    int u = 0;
    for (int p = 0; p < n; p++) if (Y[p] > Y[a] || (Y[p] == Y[a] && X[p] > X[a])) ord[u++] = p;
    if (u < K - 1) continue;
    anc = a; qsort(ord, u, sizeof(int), cmpang);
    for (int j = 0; j < u; j++)
      for (int i = 0; i < j; i++) {
        double *d = D[i][j];
        for (int L = 0; L <= K; L++) d[L] = 0;
        d[3] = 1;   /* a, ord[i], ord[j] */
        for (int h = 0; h < i; h++)
          if (orient(ord[h], ord[i], ord[j]) > 0) { double *e = D[h][i]; for (int L = 3; L < K; L++) d[L + 1] += e[L]; }
        if (orient(ord[i], ord[j], a) > 0) total += d[K];
      }
  }
  return total + (NW > 0 ? nest_penalty() : 0);
}
int main(int argc, char **argv) {
  if (argc < 9) { fprintf(stderr, "usage: annealnest G m F K seed seconds box nestweight\n"); return 1; }
  NW = atof(argv[8]); if (argc > 9) DUMP = argv[9];
  G = argv[1][0] == 'M' ? 'M' : atoi(argv[1]); s = G == 'M' ? 2 : G;
  m = atoi(argv[2]); C = atoi(argv[3]); K = atoi(argv[4]); rs = 0x9E3779B97F4A7C15ULL ^ (unsigned long long)atoll(argv[5]) * 2654435761ULL;
  double secs = atof(argv[6]); ll B = atoll(argv[7]);
  n = s * m + C;
  int nrep = m + (G == 'M' ? C : 0);          /* mirror axis points are moved like representatives */
  if (G != 'M' && C) { X[n - 1] = 0; Y[n - 1] = 0; }
  for (int i = 0; i < 20; i++) urand();
  time_t t0 = time(NULL);
  double bestall = 1e300; long long it = 0;
  while (difftime(time(NULL), t0) < secs) {
    /* random start */
    for (int i = 0; i < n; i++) act[i] = (G != 'M' && C && i == n - 1);
    for (int r = 0; r < nrep; r++) {
      if (r < m) for (int t = 0; t < s; t++) act[r + t * m] = 1; else act[s * m + (r - m)] = 1;
      do { RA[r] = r < m ? irand(-B, B) : 0; RB[r] = irand(-B, B); place(r); } while (!ok_orbit(r));
    }
    double cost = count_k(), best = cost, T = cost > 0 ? cost * 0.02 + 1 : 1;
    for (int q = 0; q < n; q++) { BX[q] = X[q]; BY[q] = Y[q]; }
    long long since = 0;
    while (cost > 0 && since < 200000 && difftime(time(NULL), t0) < secs) {
      it++; since++;
      int r = (int)irand(0, nrep - 1); ll oa = RA[r], ob = RB[r];
      double sc = urand() < 0.1 ? (double)B : (double)B * pow(10.0, -3.0 * urand());
      if (r < m) RA[r] = oa + (ll)llround((urand() * 2 - 1) * sc);
      RB[r] = ob + (ll)llround((urand() * 2 - 1) * sc);
      place(r);
      if (!ok_orbit(r)) { RA[r] = oa; RB[r] = ob; place(r); continue; }
      double nc = count_k();
      if (nc <= cost || urand() < exp(-(nc - cost) / T)) { if (nc < best) { best = nc; since = 0; for (int q = 0; q < n; q++) { BX[q] = X[q]; BY[q] = Y[q]; } } cost = nc; }
      else { RA[r] = oa; RB[r] = ob; place(r); }
      T *= 0.99995; if (T < 0.05) T = 0.05;
    }
    if (best < bestall) { bestall = best; fprintf(stderr, "[%.0fs] restart best %.0f (overall %.0f), iters %lld\n", difftime(time(NULL), t0), best, bestall, it); }
    if (best <= bestall && DUMP && best < 1e300) {   /* the best state of this restart is an overall best: save it */
      FILE *g = fopen(DUMP, "w"); if (g) { fprintf(g, "# cost %.0f\n", best); for (int i = 0; i < n; i++) fprintf(g, "%lld %lld\n", BX[i], BY[i]); fclose(g); }
    }
    if (cost == 0) {
      printf("FOUND G=%c m=%d F=%d K=%d n=%d\n", G == 'M' ? 'M' : '0' + G, m, C, K, n);
      for (int i = 0; i < n; i++) printf("%lld %lld\n", X[i], Y[i]);
      fflush(stdout); return 0;
    }
  }
  printf("NOTFOUND best %.0f\n", bestall); return 2;
}
