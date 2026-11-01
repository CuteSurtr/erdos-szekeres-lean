/* cvxcheck.c -- two independent exact checks on an orientation table (no coordinates used).
   Input file: n, then n*n*n signs (-1/0/1) of orient(a,b,c) (as written by otab2txt.py).
   (1) DFS: counts all k-subsets in convex position for k = 3..K, extending index-increasing subsets one point at a time;
       a set is in convex position iff every 4-subset is (no point inside the triangle of three others).
   (2) DP: largest subset in convex position, anchored at the minimum-index vertex a and its CCW successor b:
       all other vertices c satisfy orient(a,b,c) > 0, so the angular order around a is the total order orient(a,x,y) > 0.
   Also checks the table: antisymmetry and no zero on distinct triples.
   usage: cvxcheck table K   */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static signed char *O; static int n, K;
#define OR(a,b,c) O[((size_t)(a)*n+(b))*n+(c)]
static long long cnt[16];
static int S[16];
static int in_tri(int x, int a, int b, int c) {  /* x strictly inside triangle abc */
  int o1 = OR(a, b, x), o2 = OR(b, c, x), o3 = OR(c, a, x);
  return o1 == o2 && o2 == o3;
}
static int convex4(int a, int b, int c, int d) {
  return !in_tri(d, a, b, c) && !in_tri(c, a, b, d) && !in_tri(b, a, c, d) && !in_tri(a, b, c, d);
}
static void dfs(int s, int start) {
  /* S[0..s-1] in convex position */
  if (s >= 3) cnt[s]++;
  if (s == K) return;
  for (int x = start; x < n; x++) {
    int ok = 1;
    for (int i = 0; i < s && ok; i++) for (int j = i + 1; j < s && ok; j++) for (int l = j + 1; l < s && ok; l++)
      if (!convex4(S[i], S[j], S[l], x)) ok = 0;
    if (!ok) continue;
    S[s] = x; dfs(s + 1, x + 1);
  }
}
static int *ord, *D;
static int g_a;
static int cmp(const void *p, const void *q) { int x = *(const int *)p, y = *(const int *)q; return OR(g_a, x, y) > 0 ? -1 : 1; }
int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: cvxcheck table K\n"); return 1; }
  FILE *f = fopen(argv[1], "r"); K = atoi(argv[2]);
  if (!f || fscanf(f, "%d", &n) != 1) return 1;
  O = malloc((size_t)n * n * n);
  for (size_t i = 0; i < (size_t)n * n * n; i++) { int v; if (fscanf(f, "%d", &v) != 1) return 1; O[i] = (signed char)v; }
  fclose(f);
  long bad = 0;
  for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) for (int c = 0; c < n; c++) {
    if (a == b || b == c || a == c) continue;
    int v = OR(a, b, c);
    if (v == 0) bad++;
    if (OR(b, c, a) != v || OR(b, a, c) != -v) bad++;
  }
  printf("table n=%d: %ld antisymmetry/zero violations\n", n, bad);
  dfs(0, 0);
  for (int k = 3; k <= K; k++) printf("convex %d-subsets: %lld\n", k, cnt[k]);
  /* DP */
  ord = malloc(sizeof(int) * n); D = malloc(sizeof(int) * n * n);
  int best = 2;
  for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) {
    int u = 0; ord[u++] = b;
    for (int c = a + 1; c < n; c++) if (c != b && OR(a, b, c) > 0) ord[u++] = c;
    g_a = a; qsort(ord + 1, u - 1, sizeof(int), cmp);   /* b is first: every c is left of a->b */
    /* D[i*n+j] = max vertices of convex chain a -> b=ord[0] -> ... -> ord[i] -> ord[j] (left turns), 0 if none */
    for (int j = 1; j < u; j++) {
      for (int i = 0; i < j; i++) {
        int v = 0;
        if (i == 0) v = 3;   /* a, b, ord[j]: left turn since ord[j] left of a->b */
        else {
          for (int h = 0; h < i; h++) {
            int dv = D[h * n + i];
            if (dv && OR(ord[h], ord[i], ord[j]) > 0 && dv + 1 > v) v = dv + 1;
          }
        }
        /* chain must also turn left at ord[i] relative to its predecessor: ensured by the h-loop; for i=0 the turn at b
           is (a, b, ord[j]) > 0 by selection */
        D[i * n + j] = v;
        if (v && OR(ord[i], ord[j], a) > 0 && OR(ord[j], a, b) > 0 && v > best) best = v;
      }
    }
  }
  printf("DP largest convex subset: %d\n", best);
  return 0;
}
