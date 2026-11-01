/* Brute-force checker for an x-sorted signotope given as a SAT model.
 *
 * usage: sigcheckB N a u k model.txt
 *   model.txt: whitespace-separated literals (other tokens ignored); literal +v / -v with
 *   1 <= v <= C(N,3) sets X(i,j,k) for the v-th triple of {1..N} in lexicographic order.
 *   X true = counterclockwise = cup triple (gen_etv.py and Baek-Balko convention).
 *
 * Checks, each by enumerating ALL subsets of the given size (no pruning, no SAT encoding):
 *   sig_viol  : quadruples i<j<k<l whose (ijk, ijl, ikl, jkl) has more than one sign change
 *   caps_a    : a-subsets that are caps (every consecutive triple clockwise)
 *   cups_u    : u-subsets that are cups (every consecutive triple counterclockwise)
 *   gons_cc   : k-subsets in convex position by the cap+cup definition (split the middle
 *               points by the side of the line through the two extreme points; upper part
 *               plus extremes must be a cap, lower part plus extremes a cup)
 *   gons_4pt  : k-subsets in convex position by the 4-point test (no point inside a
 *               triangle of three others, orientation extended by permutation parity)
 * Prints one JSON line. Exit code 0 iff all checks pass (sig_viol = caps_a = cups_u =
 * gons_cc = gons_4pt = 0) and all C(N,3) literals were present.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 40
static int N, A, U, K;
static signed char O3[MAXN + 1][MAXN + 1][MAXN + 1]; /* all ordered triples */
static unsigned char C4[MAXN + 1][MAXN + 1][MAXN + 1][MAXN + 1];

static int o(int i, int j, int k) { return O3[i][j][k]; }
static int inside(int d, int a, int b, int c) {
  int x = O3[a][b][d];
  return x == O3[b][c][d] && x == O3[c][a][d];
}
static int is_chain(const int *s, int m, int sign) {
  for (int t = 0; t + 2 < m; t++)
    if (o(s[t], s[t + 1], s[t + 2]) != sign) return 0;
  return 1;
}
static int gon_cc(const int *s, int m) {
  int up[MAXN], lo[MAXN], nu = 0, nl = 0;
  up[nu++] = s[0]; lo[nl++] = s[0];
  for (int t = 1; t + 1 < m; t++) {
    if (o(s[0], s[t], s[m - 1]) < 0) up[nu++] = s[t]; else lo[nl++] = s[t];
  }
  up[nu++] = s[m - 1]; lo[nl++] = s[m - 1];
  return is_chain(up, nu, -1) && is_chain(lo, nl, +1);
}
static int gon_4pt(const int *s, int m) {
  for (int p = 0; p < m; p++) for (int q = p + 1; q < m; q++)
    for (int r = q + 1; r < m; r++) for (int w = r + 1; w < m; w++)
      if (!C4[s[p]][s[q]][s[r]][s[w]]) return 0;
  return 1;
}
typedef int (*pred)(const int *, int);
static int cap_p(const int *s, int m) { return is_chain(s, m, -1); }
static int cup_p(const int *s, int m) { return is_chain(s, m, +1); }
static long long count_subsets(int m, pred f, int *example) {
  if (m > N) return 0;
  int s[MAXN];
  for (int t = 0; t < m; t++) s[t] = t + 1;
  long long c = 0;
  for (;;) {
    if (f(s, m)) { if (!c && example) memcpy(example, s, sizeof(int) * m); c++; }
    int t = m - 1;
    while (t >= 0 && s[t] == N - m + 1 + t) t--;
    if (t < 0) break;
    s[t]++;
    for (int q = t + 1; q < m; q++) s[q] = s[q - 1] + 1;
  }
  return c;
}
int main(int argc, char **argv) {
  if (argc != 6) { fprintf(stderr, "usage: sigcheckB N a u k model\n"); return 2; }
  N = atoi(argv[1]); A = atoi(argv[2]); U = atoi(argv[3]); K = atoi(argv[4]);
  if (N < 3 || N > MAXN) { fprintf(stderr, "bad N\n"); return 2; }
  int nX = N * (N - 1) * (N - 2) / 6;
  int *val = calloc(nX + 1, sizeof(int));
  FILE *f = fopen(argv[5], "r");
  if (!f) { perror("model"); return 2; }
  char tok[64];
  while (fscanf(f, "%63s", tok) == 1) {
    char *end; long l = strtol(tok, &end, 10);
    if (*end || l == 0) continue;
    long v = labs(l);
    if (v <= nX) val[v] = l > 0 ? 1 : -1;
  }
  fclose(f);
  int missing = 0, idx = 0;
  for (int i = 1; i <= N; i++) for (int j = i + 1; j <= N; j++) for (int k = j + 1; k <= N; k++) {
    int s = val[++idx];
    if (!s) missing++;
    O3[i][j][k] = s; O3[j][k][i] = s; O3[k][i][j] = s;
    O3[j][i][k] = -s; O3[i][k][j] = -s; O3[k][j][i] = -s;
  }
  long long sig_viol = 0;
  for (int a = 1; a <= N; a++) for (int b = a + 1; b <= N; b++)
    for (int c = b + 1; c <= N; c++) for (int d = c + 1; d <= N; d++) {
      int q[4] = {o(a, b, c), o(a, b, d), o(a, c, d), o(b, c, d)};
      if ((q[0] != q[1]) + (q[1] != q[2]) + (q[2] != q[3]) > 1) sig_viol++;
      C4[a][b][c][d] = !(inside(a, b, c, d) || inside(b, a, c, d) || inside(c, a, b, d) || inside(d, a, b, c));
    }
  int ex_cap[MAXN], ex_cup[MAXN], ex_gon[MAXN];
  long long caps = count_subsets(A, cap_p, ex_cap);
  long long cups = count_subsets(U, cup_p, ex_cup);
  long long gcc = count_subsets(K, gon_cc, ex_gon);
  long long g4 = count_subsets(K, gon_4pt, NULL);
  /* longest cap / cup by exhaustive DP over pairs (for information) */
  static int capL[MAXN + 1][MAXN + 1], cupL[MAXN + 1][MAXN + 1];
  int maxcap = N >= 2 ? 2 : N, maxcup = maxcap;
  for (int j = 1; j <= N; j++) for (int k = j + 1; k <= N; k++) {
    capL[j][k] = cupL[j][k] = 2;
    for (int i = 1; i < j; i++) {
      if (o(i, j, k) < 0 && capL[i][j] + 1 > capL[j][k]) capL[j][k] = capL[i][j] + 1;
      if (o(i, j, k) > 0 && cupL[i][j] + 1 > cupL[j][k]) cupL[j][k] = cupL[i][j] + 1;
    }
    if (capL[j][k] > maxcap) maxcap = capL[j][k];
    if (cupL[j][k] > maxcup) maxcup = cupL[j][k];
  }
  int ok = !missing && !sig_viol && !caps && !cups && !gcc && !g4;
  printf("{\"N\": %d, \"a\": %d, \"u\": %d, \"k\": %d, \"missing\": %d, \"sig_viol\": %lld, "
         "\"caps_a\": %lld, \"cups_u\": %lld, \"gons_cc\": %lld, \"gons_4pt\": %lld, "
         "\"max_cap\": %d, \"max_cup\": %d, \"ok\": %s",
         N, A, U, K, missing, sig_viol, caps, cups, gcc, g4, maxcap, maxcup, ok ? "true" : "false");
  if (gcc) { printf(", \"gon_example\": ["); for (int t = 0; t < K; t++) printf("%s%d", t ? ", " : "", ex_gon[t]); printf("]"); }
  printf("}\n");
  return ok ? 0 : 1;
}
