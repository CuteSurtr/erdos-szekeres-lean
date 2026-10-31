// geomcount: count, for r = 4..Kmax, the orbits (under a given permutation group) of r-subsets
// of a planar point set that are in convex position.  Purely geometric and independent of the
// CNF generators: convex position is tested by computing the convex hull of the subset with
// Andrew's monotone chain on the exact integer coordinates (a subset is in convex position iff
// every point is a strict hull vertex).  Subsets of convex sets are convex, so a DFS over
// convex subsets is exhaustive.
// Also reports the number of collinear triples (must be 0) and the largest convex subset size.
//
// input (stdin): n g Kmax / n lines "x y" (integers) / g lines with a permutation of 0..n-1
// output: one line "collinear=<c> maxconv=<m> orbits4=<..> ... orbitsKmax=<..>"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
typedef __int128 i128;
static int n, g, Kmax;
static ll X[64], Y[64];
static int G[16][64];
static i128 stabsum[16];
static long long cnt[16];
static int maxconv = 0;

static i128 cross(int o, int a, int b) {
  return (i128)(X[a] - X[o]) * (Y[b] - Y[o]) - (i128)(Y[a] - Y[o]) * (X[b] - X[o]);
}
static int cmpidx(const void *pa, const void *pb) {
  int a = *(const int *)pa, b = *(const int *)pb;
  if (X[a] != X[b]) return X[a] < X[b] ? -1 : 1;
  if (Y[a] != Y[b]) return Y[a] < Y[b] ? -1 : 1;
  return 0;
}
// number of strict hull vertices of the subset
static int hullsize(const int *S, int k) {
  int P[16], H[40];
  memcpy(P, S, sizeof(int) * k);
  qsort(P, k, sizeof(int), cmpidx);
  int h = 0;
  for (int i = 0; i < k; i++) {
    while (h >= 2 && cross(H[h - 2], H[h - 1], P[i]) <= 0) h--;
    H[h++] = P[i];
  }
  for (int i = k - 2, t = h + 1; i >= 0; i--) {
    while (h >= t && cross(H[h - 2], H[h - 1], P[i]) <= 0) h--;
    H[h++] = P[i];
  }
  return h - 1;
}
static int cur[16];
static void dfs(int k, int startidx, unsigned long long mask) {
  if (k > maxconv) maxconv = k;
  if (k >= 4) {
    // stabilizer size
    int stab = 0;
    for (int j = 0; j < g; j++) {
      unsigned long long im = 0;
      for (int i = 0; i < k; i++) im |= 1ULL << G[j][cur[i]];
      if (im == mask) stab++;
    }
    stabsum[k] += stab;
    cnt[k]++;
  }
  if (k == Kmax) return;
  for (int p = startidx; p < n; p++) {
    cur[k] = p;
    if (k + 1 < 4 || hullsize(cur, k + 1) == k + 1) dfs(k + 1, p + 1, mask | (1ULL << p));
  }
}
int main(void) {
  if (scanf("%d %d %d", &n, &g, &Kmax) != 3) return 2;
  if (n > 63 || g > 16 || Kmax > 15) return 2;
  for (int i = 0; i < n; i++) if (scanf("%lld %lld", &X[i], &Y[i]) != 2) return 2;
  for (int j = 0; j < g; j++) for (int i = 0; i < n; i++) if (scanf("%d", &G[j][i]) != 1) return 2;
  long coll = 0;
  for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++)
    if (cross(a, b, c) == 0) coll++;
  dfs(0, 0, 0);
  printf("collinear=%ld maxconv=%d", coll, maxconv);
  for (int r = 4; r <= Kmax; r++) {
    if (stabsum[r] % g) { printf(" orbits%d=NONINTEGER", r); continue; }
    printf(" orbits%d=%lld", r, (long long)(stabsum[r] / g));
  }
  for (int r = 4; r <= Kmax; r++) printf(" subsets%d=%lld", r, cnt[r]);
  printf("\n");
  return 0;
}
