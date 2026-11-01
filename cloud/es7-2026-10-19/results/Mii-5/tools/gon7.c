/* Brute-force checks on an abstract signotope given as X(i,j,k), i<j<k, N<=40 points.
   input (stdin): N, then C(N,3) values 0/1 in lexicographic triple order (1 = ccw).
   Checks: signotope axiom (every 4-subset: the sequence X(jkl),X(ikl),X(ijl),X(ijk) has at most
   one sign change) and counts subsets in convex position of each size (no point inside the
   triangle of three others, using chirotope signs), by DFS over hereditary convex sets.
   Prints axiom violations and the maximum convex-position size found (stops counting at 8). */
#include <stdio.h>
#include <stdlib.h>
static int N, X[41][41][41];
static int chi(int a, int b, int c) { /* sign of ordered triple, any order */
  int s = 1, t;
  if (a > b) { t = a; a = b; b = t; s = -s; }
  if (b > c) { t = b; b = c; c = t; s = -s; }
  if (a > b) { t = a; a = b; b = t; s = -s; }
  return X[a][b][c] ? s : -s;
}
static int inside(int d, int a, int b, int c) {
  int o = chi(a, b, c);
  return chi(a, b, d) == o && chi(b, c, d) == o && chi(c, a, d) == o;
}
static long long cnt[9]; static int S[9];
static int ok_add(int n, int p) { /* S[0..n-1] convex, check S+p convex */
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) {
    for (int k = j + 1; k < n; k++) if (inside(p, S[i], S[j], S[k])) return 0;
    for (int l = 0; l < n; l++) if (l != i && l != j && inside(S[l], p, S[i], S[j])) return 0;
  }
  return 1;
}
static void dfs(int n, int from) {
  cnt[n]++;
  if (n == 8) return;
  for (int p = from; p <= N; p++) if (ok_add(n, p)) { S[n] = p; dfs(n + 1, p + 1); }
}
int main(void) {
  if (scanf("%d", &N) != 1) return 1;
  for (int i = 1; i <= N; i++) for (int j = i + 1; j <= N; j++) for (int k = j + 1; k <= N; k++) {
    int v; if (scanf("%d", &v) != 1) return 1; X[i][j][k] = v; }
  long long bad = 0;
  for (int i = 1; i <= N; i++) for (int j = i + 1; j <= N; j++) for (int k = j + 1; k <= N; k++) for (int l = k + 1; l <= N; l++) {
    int s[4] = {X[j][k][l], X[i][k][l], X[i][j][l], X[i][j][k]}, ch = 0;
    for (int t = 0; t < 3; t++) ch += s[t] != s[t + 1];
    if (ch > 1) bad++;
  }
  dfs(0, 1);
  printf("{\"N\": %d, \"signotope_axiom_violations\": %lld", N, bad);
  for (int k = 3; k <= 8; k++) printf(", \"convex_%d\": %lld", k, cnt[k]);
  printf("}\n");
  return 0;
}
