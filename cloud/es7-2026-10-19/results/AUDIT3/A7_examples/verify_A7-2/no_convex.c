/* Independent brute force: count K-subsets in convex position, given an exact orientation table
   (first line N, then N*N rows of N signs o[a][b][c] in {-1,0,1}).
   A K-subset in general position is in convex position iff no point of it lies in the closed... (open, since no three
   points are collinear) triangle of three other points of it. usage: ./no_convex K < table */
#include <stdio.h>
#include <stdlib.h>
static signed char o[64][64][64];
static int N, K, idx[16];
static long long total = 0, convex = 0;
static int inside(int d, int a, int b, int c) {
  int s = o[a][b][c];
  return o[a][b][d] == s && o[b][c][d] == s && o[c][a][d] == s;
}
static int is_convex(void) {
  for (int i = 0; i < K; i++)
    for (int j = i + 1; j < K; j++)
      for (int l = j + 1; l < K; l++)
        for (int m = 0; m < K; m++) {
          if (m == i || m == j || m == l) continue;
          if (inside(idx[m], idx[i], idx[j], idx[l])) return 0;
        }
  return 1;
}
static void rec(int start, int depth) {
  if (depth == K) { total++; convex += is_convex(); return; }
  for (int v = start; v <= N - (K - depth); v++) { idx[depth] = v; rec(v + 1, depth + 1); }
}
int main(int argc, char **argv) {
  if (argc < 2) { fprintf(stderr, "usage: no_convex K < table\n"); return 1; }
  K = atoi(argv[1]);
  if (scanf("%d", &N) != 1 || N > 64) return 2;
  for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) for (int c = 0; c < N; c++) {
    int v; if (scanf("%d", &v) != 1) return 3; o[a][b][c] = (signed char)v;
  }
  /* sanity: antisymmetry of the table and no zero on distinct triples */
  long long bad = 0;
  for (int a = 0; a < N; a++) for (int b = 0; b < N; b++) for (int c = 0; c < N; c++) {
    if (a == b || b == c || a == c) continue;
    if (o[a][b][c] == 0 || o[a][b][c] != o[b][c][a] || o[a][b][c] != -o[b][a][c]) bad++;
  }
  rec(0, 0);
  printf("N=%d K=%d table_anomalies=%lld subsets=%lld convex=%lld\n", N, K, bad, total, convex);
  return 0;
}
