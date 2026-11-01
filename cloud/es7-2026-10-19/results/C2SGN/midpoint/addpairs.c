/* Random search (exploratory): add antipodal pairs (x,y), (-x,-y) to a centrally symmetric base set so that the result
   stays in general position and has no K points in convex position. Stage s adds one pair to each survivor of stage
   s-1. Largest convex subset: exact O(n^4) chain DP with every point as the lowest vertex (integer arithmetic).
   usage: addpairs BASE.txt K PAIRS TRIALS_PER_SET BOX SEED   (prints each successful final set, one point per line)
   TRIALS_PER_SET = 0: every integer pair with |x|, |y| <= BOX instead of random ones. */
#include <stdio.h>
#include <stdlib.h>
typedef long long ll;
#define MAXN 64
static int n; static ll X[MAXN], Y[MAXN]; static long long gpfail, hist[MAXN];
static ll cr(int o, int a, int b) { return (X[a] - X[o]) * (Y[b] - Y[o]) - (Y[a] - Y[o]) * (X[b] - X[o]); }
static int largest_convex(void) {
  static int q[MAXN], dp[MAXN][MAXN]; int best = 2;
  for (int p = 0; p < n; p++) {
    int m = 0;
    for (int i = 0; i < n; i++) if (i != p && (Y[i] > Y[p] || (Y[i] == Y[p] && X[i] > X[p]))) q[m++] = i;
    for (int i = 1; i < m; i++) { int v = q[i], j = i; while (j > 0 && cr(p, v, q[j - 1]) > 0) { q[j] = q[j - 1]; j--; } q[j] = v; }
    for (int j = 0; j < m; j++)
      for (int i = 0; i < j; i++) {
        dp[i][j] = cr(p, q[i], q[j]) > 0 ? 3 : 0;
        if (!dp[i][j]) continue;
        for (int k = 0; k < i; k++) if (dp[k][i] && cr(q[k], q[i], q[j]) > 0 && dp[k][i] + 1 > dp[i][j]) dp[i][j] = dp[k][i] + 1;
        if (cr(q[i], q[j], p) > 0 && dp[i][j] > best) best = dp[i][j];
      }
  }
  return best;
}
static int general_position_new(int a) {          /* points a, a+1 are new: no three collinear involving them */
  for (int t = a; t < a + 2; t++)
    for (int i = 0; i < n; i++) if (i != t)
      for (int j = i + 1; j < n; j++) if (j != t && cr(t, i, j) == 0) return 0;
  return 1;
}
int main(int argc, char **argv) {
  if (argc < 7) return 1;
  FILE *f = fopen(argv[1], "r"); if (!f) { fprintf(stderr, "cannot open %s\n", argv[1]); return 1; }
  int K = atoi(argv[2]), P = atoi(argv[3]), T = atoi(argv[4]); ll B = atoll(argv[5]);
  srand(atoi(argv[6]));
  static ll SX[20000][MAXN / 2 * 2], SY[20000][MAXN / 2 * 2]; int ns = 1, n0 = 0;
  while (fscanf(f, "%lld %lld", &X[n0], &Y[n0]) == 2) n0++;
  for (int i = 0; i < n0; i++) { SX[0][i] = X[i]; SY[0][i] = Y[i]; }
  int cur = n0; n = n0; for (int i = 0; i < n0; i++) { X[i] = SX[0][i]; Y[i] = SY[0][i]; } fprintf(stderr, "base: %d points, largest convex subset %d\n", n0, largest_convex());
  for (int s = 0; s < P; s++) {
    static ll NX[20000][MAXN], NY[20000][MAXN]; int nn = 0;
    for (int e = 0; e < ns && nn < 20000; e++)
      for (long t = 0; (T ? t < T : t < (2 * B + 1) * (2 * B + 1)) && nn < 20000; t++) {
        for (int i = 0; i < cur; i++) { X[i] = SX[e][i]; Y[i] = SY[e][i]; }
        ll x, y;
        if (T) { x = (ll)(rand() % (2 * B + 1)) - B; y = (ll)(rand() % (2 * B + 1)) - B; }
        else { x = t / (2 * B + 1) - B; y = t % (2 * B + 1) - B; if (x < 0 || (x == 0 && y <= 0)) continue; }   /* each pair once */
        if (x == 0 && y == 0) continue;
        X[cur] = x; Y[cur] = y; X[cur + 1] = -x; Y[cur + 1] = -y; n = cur + 2;
        if (!general_position_new(cur)) { gpfail++; continue; }
        { int L = largest_convex(); hist[L]++; if (L >= K) continue; }
        for (int i = 0; i < n; i++) { NX[nn][i] = X[i]; NY[nn][i] = Y[i]; }
        nn++;
      }
    fprintf(stderr, "  rejected (collinear) %lld; largest convex subset histogram:", gpfail); for (int L = 0; L < MAXN; L++) if (hist[L]) fprintf(stderr, " %d:%lld", L, hist[L]); fprintf(stderr, "\n"); gpfail = 0; for (int L = 0; L < MAXN; L++) hist[L] = 0;
    fprintf(stderr, "stage %d: %d sets of %d points without a convex %d-gon\n", s + 1, nn, cur + 2, K);
    cur += 2; ns = nn;
    for (int e = 0; e < ns; e++) for (int i = 0; i < cur; i++) { SX[e][i] = NX[e][i]; SY[e][i] = NY[e][i]; }
    if (!ns) break;
  }
  for (int e = 0; e < ns && e < 5; e++) { printf("# set %d\n", e); for (int i = 0; i < cur; i++) printf("%lld %lld\n", SX[e][i], SY[e][i]); }
  return 0;
}
