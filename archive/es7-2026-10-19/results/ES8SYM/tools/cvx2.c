/* cvx2.c -- two independent exact dynamic programmes on an exact orientation table (no coordinates used).
   Input: PREFIX.otab (first line "n", then n^3 signed bytes orient(a,b,c), a major) and PREFIX.lex (rank of each
   point in the exact (Im, Re) lexicographic order).
   DP1: every convex polygon is counted once, at its minimum-index vertex a and the vertex b following a
        counter-clockwise; the other vertices c (> a) satisfy orient(a,b,c) > 0 and are sorted by orient(a,.,.).
   DP2: every convex polygon is counted once, at its lowest vertex a (minimum lex rank); the other vertices have
        larger rank, lie in the half-plane above a and are sorted by orient(a,.,.).
   Each DP gives (i) the number of convex k-gons for k = 3..KC and (ii) the size of a largest convex subset.
   Table checks: antisymmetry under all permutations, no zero on distinct triples.
   usage: cvx2 PREFIX K        (K = forbidden size; counts printed for k = 3..K)
   exit 0 iff table OK, all counts of DP1 and DP2 agree, both maxima agree, count(K) = 0 and maximum < K. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static signed char *O; static int n, K;
#define OR(a,b,c) O[((size_t)(a)*n+(b))*n+(c)]
#define LMAX 16
typedef unsigned long long u64;
static int g_a;
static int cmpang(const void *p, const void *q) { int x = *(const int *)p, y = *(const int *)q; return OR(g_a, x, y) > 0 ? -1 : 1; }

static u64 *Dc;   /* Dc[(i*n + j)*LMAX + L] : chains ... x_i, x_j with L vertices */
static int *Dm;

/* generic chain DP on a sorted candidate list ord[0..u-1] around anchor a.  first: if >= 0, the chain must start
   a -> ord[0] (DP1: ord[0] = b); counts and max are accumulated. */
static void chain_dp(int a, int *ord, int u, int force_first, u64 *cnt, int *best) {
  for (int j = 1; j < u; j++) {
    for (int i = 0; i < j; i++) {
      u64 *d = Dc + ((size_t)i * n + j) * LMAX;
      memset(d, 0, sizeof(u64) * LMAX);
      int v = 0;
      if (OR(a, ord[i], ord[j]) <= 0) { Dm[i * n + j] = 0; continue; }   /* never for sorted lists; safety */
      if (!force_first || i == 0) { d[3] = 1; v = 3; }
      for (int h = 0; h < i; h++) {
        if (OR(ord[h], ord[i], ord[j]) <= 0) continue;
        int dv = Dm[h * n + i];
        if (dv && dv + 1 > v) v = dv + 1;
        u64 *e = Dc + ((size_t)h * n + i) * LMAX;
        for (int L = 3; L < LMAX - 1; L++) d[L + 1] += e[L];
      }
      Dm[i * n + j] = v;
      if (v && OR(ord[i], ord[j], a) > 0) {
        if (v > *best) *best = v;
        for (int L = 3; L < LMAX; L++) cnt[L] += d[L];
      }
    }
  }
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: cvx2 PREFIX K\n"); return 1; }
  char fn[4096];
  K = atoi(argv[2]);
  snprintf(fn, sizeof fn, "%s.otab", argv[1]);
  FILE *f = fopen(fn, "rb");
  if (!f || fscanf(f, "%d", &n) != 1) { fprintf(stderr, "cannot read %s\n", fn); return 1; }
  fgetc(f);
  O = malloc((size_t)n * n * n);
  if (fread(O, 1, (size_t)n * n * n, f) != (size_t)n * n * n) { fprintf(stderr, "short table\n"); return 1; }
  fclose(f);
  int *rank = malloc(sizeof(int) * n);
  snprintf(fn, sizeof fn, "%s.lex", argv[1]);
  f = fopen(fn, "r");
  for (int i = 0; i < n; i++) if (fscanf(f, "%d", &rank[i]) != 1) { fprintf(stderr, "bad lex\n"); return 1; }
  fclose(f);
  long bad = 0;
  for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) for (int c = 0; c < n; c++) {
    int v = OR(a, b, c);
    if (a == b || b == c || a == c) { if (v) bad++; continue; }
    if (v != 1 && v != -1) bad++;
    if (OR(b, c, a) != v || OR(c, a, b) != v || OR(b, a, c) != -v || OR(a, c, b) != -v || OR(c, b, a) != -v) bad++;
  }
  printf("table n=%d: %ld antisymmetry/zero violations\n", n, bad);
  Dc = malloc(sizeof(u64) * (size_t)n * n * LMAX);
  Dm = malloc(sizeof(int) * (size_t)n * n);
  int *ord = malloc(sizeof(int) * n);
  u64 c1[LMAX] = {0}, c2[LMAX] = {0};
  int best1 = 2, best2 = 2;
  /* DP1 */
  for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) {
    int u = 0; ord[u++] = b;
    for (int c = a + 1; c < n; c++) if (c != b && OR(a, b, c) > 0) ord[u++] = c;
    g_a = a; qsort(ord + 1, u - 1, sizeof(int), cmpang);
    chain_dp(a, ord, u, 1, c1, &best1);
  }
  /* DP2 */
  for (int a = 0; a < n; a++) {
    int u = 0;
    for (int c = 0; c < n; c++) if (rank[c] > rank[a]) ord[u++] = c;
    g_a = a; qsort(ord, u, sizeof(int), cmpang);
    /* sanity: sorted list must be a chain of strict left turns around a */
    for (int q = 0; q + 1 < u; q++) if (OR(a, ord[q], ord[q + 1]) <= 0) bad++;
    chain_dp(a, ord, u, 0, c2, &best2);
  }
  int agree = (best1 == best2);
  for (int L = 3; L <= K && L < LMAX; L++) {
    printf("convex %2d-gons: DP1 %llu  DP2 %llu%s\n", L, c1[L], c2[L], c1[L] == c2[L] ? "" : "  MISMATCH");
    if (c1[L] != c2[L]) agree = 0;
  }
  printf("largest convex subset: DP1 %d  DP2 %d\n", best1, best2);
  int ok = bad == 0 && agree && c1[K] == 0 && best1 < K;
  printf("%s (K=%d)\n", ok ? "CVX2 PASS" : "CVX2 FAIL", K);
  return ok ? 0 : 1;
}
