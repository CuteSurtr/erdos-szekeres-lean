/* Independent check (no DP): count k-subsets in convex position, given the orientation sign table.
   A subset (no three collinear) is in convex position iff no point lies inside a triangle of three others.
   Input (stdin): n, then n*n*n signs (-1/1/0) for orient(a,b,c). Usage: brute k */
#include <stdio.h>
#include <stdlib.h>
static signed char *O; static int n;
#define OR(a,b,c) O[((a)*n+(b))*n+(c)]
static int convex(const int *s, int k) {
  for (int t = 0; t < k; t++)
    for (int a = 0; a < k; a++) if (a != t)
      for (int b = a + 1; b < k; b++) if (b != t)
        for (int c = b + 1; c < k; c++) if (c != t) {
          int o1 = OR(s[a], s[b], s[t]), o2 = OR(s[b], s[c], s[t]), o3 = OR(s[c], s[a], s[t]);
          if (o1 == o2 && o2 == o3) return 0;
        }
  return 1;
}
int main(int argc, char **argv) {
  int k = atoi(argv[1]);
  if (scanf("%d", &n) != 1) return 1;
  O = malloc((size_t)n * n * n);
  for (long i = 0; i < (long)n * n * n; i++) { int v; if (scanf("%d", &v) != 1) return 1; O[i] = (signed char)v; }
  int s[16]; for (int i = 0; i < k; i++) s[i] = i;
  long long total = 0, cv = 0;
  while (1) {
    total++; cv += convex(s, k);
    int i = k - 1; while (i >= 0 && s[i] == n - k + i) i--;
    if (i < 0) break;
    s[i]++; for (int j = i + 1; j < k; j++) s[j] = s[j - 1] + 1;
  }
  printf("n=%d k=%d subsets=%lld convex=%lld\n", n, k, total, cv);
  return 0;
}
