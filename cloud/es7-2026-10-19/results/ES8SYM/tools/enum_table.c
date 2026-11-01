/* Enumerate all subsets in convex position from an orientation table, and classify the large ones by side.
   usage: enum_table TABLE.bin SIDES.txt K
   TABLE.bin: int32 n, then n^3 int8 signs, index (a*n+b)*n+c; the point order of the table must be increasing in the
              (y, x) order of the actual points (so that "lowest vertex" = least index; written by projective_check.py).
   SIDES.txt: n integers +1/-1 (side of the tear line / mirror axis for each point).
   Prints the number of convex j-gons for every j, the largest j, and for j >= K how many polygons have all vertices
   on one side and how many have vertices on both sides. */
#include <stdio.h>
#include <stdlib.h>
static signed char *O; static int n, K, A, m, up[512], side[512], chain[64];
static long long cnt[64], oneside[64], cross[64]; static int maxsz;
#define OR(a,b,c) O[((size_t)(a)*n+(b))*n+(c)]
static void record(int len) {
  cnt[len]++; if (len > maxsz) maxsz = len;
  if (len >= K) {
    int pos = 0, neg = 0;
    for (int i = 0; i < len; i++) { if (side[chain[i]] > 0) pos = 1; else neg = 1; }
    if (pos && neg) cross[len]++; else oneside[len]++;
  }
}
static void dfs(int p2, int p1, int len) {
  int prev2 = up[p2], prev = up[p1];
  chain[len - 1] = prev;
  if (OR(prev2, prev, A) > 0 && OR(prev, A, chain[1]) > 0) record(len);
  for (int t = p1 + 1; t < m; t++) if (OR(prev2, prev, up[t]) > 0) dfs(p1, t, len + 1);
}
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "rb"); if (!f) return 2;
  if (fread(&n, 4, 1, f) != 1) return 2;
  O = malloc((size_t)n * n * n); if (fread(O, 1, (size_t)n * n * n, f) != (size_t)n * n * n) return 2; fclose(f);
  FILE *g = fopen(argv[2], "r"); for (int i = 0; i < n; i++) if (fscanf(g, "%d", &side[i]) != 1) return 2; fclose(g);
  K = atoi(argv[3]);
  for (A = 0; A < n; A++) {
    m = 0; for (int i = A + 1; i < n; i++) up[m++] = i;
    for (int i = 1; i < m; i++) { int v = up[i], j = i - 1; while (j >= 0 && OR(A, v, up[j]) > 0) { up[j + 1] = up[j]; j--; } up[j + 1] = v; }
    chain[0] = A;
    for (int t = 0; t < m; t++) { chain[1] = up[t];
      for (int s = t + 1; s < m; s++) if (OR(A, up[t], up[s]) > 0) dfs(t, s, 3); }
  }
  for (int j = 3; j < 64; j++) if (cnt[j]) {
    printf("convex %d-gons: %lld", j, cnt[j]);
    if (j >= K) printf("  (one side: %lld, crossing: %lld)", oneside[j], cross[j]);
    printf("\n");
  }
  printf("largest convex subset: %d\n", maxsz);
  return 0;
}
