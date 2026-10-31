/* Exhaustive test for k points in convex position, from an orientation table.
 * stdin: n k, then for each i<j<l (lexicographic) the sign +1/-1 of chi(i,j,l).
 * A set is in convex position iff no point is inside a triangle of three others.
 * Backtracking over increasing index sets; prints the first convex k-set found or "none". */
#include <stdio.h>
#include <stdlib.h>
static int n, K, S[64][64][64], ch[64];
static int inside(int d, int a, int b, int c) { int o = S[a][b][d]; return o == S[b][c][d] && o == S[c][a][d]; }
static int ok(int p, int t) { /* chosen ch[0..t-1] plus p in convex position, given ch convex */
  for (int a = 0; a < t; a++) for (int b = a + 1; b < t; b++) for (int c = b + 1; c < t; c++) {
    int A = ch[a], B = ch[b], C = ch[c];
    if (inside(p, A, B, C) || inside(A, B, C, p) || inside(B, A, C, p) || inside(C, A, B, p)) return 0; }
  return 1; }
static int rec(int t, int from) {
  if (t == K) return 1;
  for (int p = from; p <= n - (K - t); p++) if (ok(p, t)) { ch[t] = p; if (rec(t + 1, p + 1)) return 1; }
  return 0; }
int main(void) {
  if (scanf("%d %d", &n, &K) != 2) return 2;
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) for (int l = j + 1; l < n; l++) {
    int s; if (scanf("%d", &s) != 1 || (s != 1 && s != -1)) return 2;
    S[i][j][l] = S[j][l][i] = S[l][i][j] = s; S[j][i][l] = S[i][l][j] = S[l][j][i] = -s; }
  if (rec(0, 0)) { printf("gon"); for (int i = 0; i < K; i++) printf(" %d", ch[i]); printf("\n"); }
  else printf("none\n");
  return 0; }
