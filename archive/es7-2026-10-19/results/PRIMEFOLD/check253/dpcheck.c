/* dpcheck.c -- largest subset in convex position, from an exact orientation table (written from scratch).
   Inputs: ranks.txt ("n", then n lines "yrank xrank": exact lexicographic (y,x) and (x,y) ranks),
           orient_upper.bin (n^3 bytes; entry [i][j][k], i<j<k: 1 = ccw, 255 = cw), optional subset file.
   Methods:
     M1y: anchor = lowest vertex in (y,x)-lex order; other vertices sorted by angle around it (orient), DP on last edge.
     M1x: same with anchor = leftmost vertex in (x,y)-lex order.
     M2 : (x,y)-lex leftmost l and rightmost r; polygon = cup (left turns) + cap (right turns) from l to r;
          size = bestcup(l,r) + bestcap(l,r) - 2.
   For every anchor of M1 the sorted candidate list is checked to be a strict total order under orient
   (orient(a, c_i, c_j) = +1 for all i<j), which also cross-checks the exact rank arrays against the table.
   Witness polygons are checked: every consecutive turn left, and no vertex inside a triangle of three others.
   usage: dpcheck ranks.txt orient_upper.bin [subset.txt]   prints the three maxima and witnesses */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int n;
static signed char *T;
static int *yrank, *xrank;
#define O(a, b, c) T[((size_t)(a) * n + (size_t)(b)) * n + (size_t)(c)]

static int g_anchor;
static int cmp_angle(const void *x, const void *y) {
  int a = *(const int *)x, b = *(const int *)y;
  if (a == b) return 0;
  return O(g_anchor, a, b) > 0 ? -1 : 1;
}
static int *g_rank;
static int cmp_rank(const void *x, const void *y) {
  int a = *(const int *)x, b = *(const int *)y;
  return g_rank[a] - g_rank[b];
}

static int in_triangle(int x, int a, int b, int c) {
  int o1 = O(a, b, x), o2 = O(b, c, x), o3 = O(c, a, x);
  return o1 == o2 && o2 == o3;
}
static int check_convex_polygon(const int *w, int len) {
  /* consecutive left turns */
  for (int q = 0; q < len; q++) if (O(w[q], w[(q + 1) % len], w[(q + 2) % len]) != 1) return 0;
  /* convex position: no vertex in a triangle of three others */
  for (int x = 0; x < len; x++)
    for (int i = 0; i < len; i++) for (int j = i + 1; j < len; j++) for (int k = j + 1; k < len; k++) {
      if (x == i || x == j || x == k) continue;
      if (in_triangle(w[x], w[i], w[j], w[k])) return 0;
    }
  return 1;
}

static long order_violations = 0;

/* M1: anchor = rank-minimal vertex (rank = yrank or xrank) */
static int method1(const int *S, int m, int *rank, int *wit, int *wlen) {
  int best = m < 2 ? m : 2;
  *wlen = 0;
  int *cand = malloc(sizeof(int) * m);
  int *D = malloc(sizeof(int) * (size_t)m * m);
  int *F = malloc(sizeof(int) * (size_t)m * m);
  for (int ai = 0; ai < m; ai++) {
    int a = S[ai], u = 0;
    for (int xi = 0; xi < m; xi++) { int x = S[xi]; if (x != a && rank[x] > rank[a]) cand[u++] = x; }
    if (u < 2) continue;
    g_anchor = a; qsort(cand, u, sizeof(int), cmp_angle);
    for (int i = 0; i < u; i++) for (int j = i + 1; j < u; j++) if (O(a, cand[i], cand[j]) != 1) order_violations++;
    for (int j = 0; j < u; j++) for (int i = 0; i < j; i++) {
      int v = 3, fr = -1;
      for (int h = 0; h < i; h++) {
        int dv = D[(size_t)h * u + i] + 1;
        if (dv > v && O(cand[h], cand[i], cand[j]) == 1) { v = dv; fr = h; }
      }
      D[(size_t)i * u + j] = v; F[(size_t)i * u + j] = fr;
      if (v > best) {
        best = v;
        int tmp[256], len = 0, ii = i, jj = j;
        tmp[len++] = cand[jj];
        while (ii >= 0) { tmp[len++] = cand[ii]; int f = F[(size_t)ii * u + jj]; jj = ii; ii = f; }
        tmp[len++] = a;
        for (int q = 0; q < len; q++) wit[q] = tmp[len - 1 - q];
        *wlen = len;
      }
    }
  }
  free(cand); free(D); free(F);
  return best;
}

/* M2: cups and caps between (x,y)-lex leftmost and rightmost vertices */
static int method2(const int *S, int m, int *wit, int *wlen) {
  int best = m < 2 ? m : 2;
  *wlen = 0;
  int *g = malloc(sizeof(int) * m); memcpy(g, S, sizeof(int) * m);
  g_rank = xrank; qsort(g, m, sizeof(int), cmp_rank);
  int *cup = malloc(sizeof(int) * (size_t)m * m), *cap = malloc(sizeof(int) * (size_t)m * m);
  int *fcup = malloc(sizeof(int) * (size_t)m * m), *fcap = malloc(sizeof(int) * (size_t)m * m);
  for (int l = 0; l < m; l++) {
    /* chains start at g[l]; indices i, j in [l, m); cup[i][j] valid for l <= i < j; 0 = invalid */
    for (int j = l + 1; j < m; j++) {
      cup[(size_t)l * m + j] = 2; cap[(size_t)l * m + j] = 2; fcup[(size_t)l * m + j] = -1; fcap[(size_t)l * m + j] = -1;
      for (int i = l + 1; i < j; i++) {
        int vu = 0, fu = -1, vc = 0, fc = -1;
        for (int h = l; h < i; h++) {
          int o = O(g[h], g[i], g[j]);
          if (o == 1) { int c = cup[(size_t)h * m + i]; if (c && c + 1 > vu) { vu = c + 1; fu = h; } }
          else { int c = cap[(size_t)h * m + i]; if (c && c + 1 > vc) { vc = c + 1; fc = h; } }
        }
        cup[(size_t)i * m + j] = vu; fcup[(size_t)i * m + j] = fu;
        cap[(size_t)i * m + j] = vc; fcap[(size_t)i * m + j] = fc;
      }
      /* best cup and cap ending at j */
      int bu = 2, iu = l, bc = 2, ic = l;
      for (int i = l + 1; i < j; i++) {
        if (cup[(size_t)i * m + j] > bu) { bu = cup[(size_t)i * m + j]; iu = i; }
        if (cap[(size_t)i * m + j] > bc) { bc = cap[(size_t)i * m + j]; ic = i; }
      }
      int sz = bu + bc - 2;
      if (sz >= 3 && sz > best) {
        best = sz;
        /* reconstruct: cup chain l -> ... -> iu -> j, cap chain l -> ... -> ic -> j; polygon ccw = cup then reversed cap */
        int cu[256], lu = 0, ca[256], lc = 0;
        { int ii = iu, jj = j; cu[lu++] = j; while (ii != l) { cu[lu++] = ii; int f = fcup[(size_t)ii * m + jj]; jj = ii; ii = f; } cu[lu++] = l; }
        { int ii = ic, jj = j; ca[lc++] = j; while (ii != l) { ca[lc++] = ii; int f = fcap[(size_t)ii * m + jj]; jj = ii; ii = f; } ca[lc++] = l; }
        int len = 0;
        for (int q = lu - 1; q >= 0; q--) wit[len++] = g[cu[q]];          /* l ... j along the cup */
        for (int q = 1; q < lc - 1; q++) wit[len++] = g[ca[q]];           /* back along the cap, excluding j and l */
        *wlen = len;
      }
    }
  }
  free(g); free(cup); free(cap); free(fcup); free(fcap);
  return best;
}

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: dpcheck ranks.txt orient_upper.bin [subset.txt]\n"); return 1; }
  FILE *f = fopen(argv[1], "r"); if (!f) return 1;
  if (fscanf(f, "%d", &n) != 1) return 1;
  yrank = malloc(sizeof(int) * n); xrank = malloc(sizeof(int) * n);
  for (int i = 0; i < n; i++) if (fscanf(f, "%d %d", &yrank[i], &xrank[i]) != 2) return 1;
  fclose(f);
  /* ranks must be permutations */
  { char *sy = calloc(n, 1), *sx = calloc(n, 1);
    for (int i = 0; i < n; i++) { if (yrank[i] < 0 || yrank[i] >= n || sy[yrank[i]]++ || xrank[i] < 0 || xrank[i] >= n || sx[xrank[i]]++) { fprintf(stderr, "bad ranks\n"); return 1; } }
    free(sy); free(sx); }
  size_t N3 = (size_t)n * n * n;
  T = malloc(N3);
  f = fopen(argv[2], "rb"); if (!f || fread(T, 1, N3, f) != N3) { fprintf(stderr, "table read error\n"); return 1; }
  fclose(f);
  long bad = 0;
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) for (int k = j + 1; k < n; k++) {
    signed char s = O(i, j, k);
    if (s != 1 && s != -1) bad++;
    O(j, k, i) = s; O(k, i, j) = s; O(j, i, k) = -s; O(i, k, j) = -s; O(k, j, i) = -s;
  }
  printf("n=%d  table entries not +-1 among i<j<k: %ld\n", n, bad);
  if (bad) return 2;
  int *S = malloc(sizeof(int) * n), m = 0;
  if (argc >= 4) {
    f = fopen(argv[3], "r"); int x; while (fscanf(f, "%d", &x) == 1) S[m++] = x; fclose(f);
  } else { for (int i = 0; i < n; i++) S[m++] = i; }
  int w1[256], l1, w2[256], l2, w3[256], l3;
  int r1 = method1(S, m, yrank, w1, &l1);
  int r2 = method1(S, m, xrank, w2, &l2);
  int r3 = method2(S, m, w3, &l3);
  printf("subset size %d\n", m);
  printf("M1y (lowest-vertex anchor) max convex subset = %d  witness ok=%d :", r1, l1 == r1 && check_convex_polygon(w1, l1));
  for (int q = 0; q < l1; q++) printf(" %d", w1[q]); printf("\n");
  printf("M1x (leftmost-vertex anchor) max convex subset = %d  witness ok=%d :", r2, l2 == r2 && check_convex_polygon(w2, l2));
  for (int q = 0; q < l2; q++) printf(" %d", w2[q]); printf("\n");
  printf("M2 (cup+cap) max convex subset = %d  witness ok=%d :", r3, l3 == r3 && check_convex_polygon(w3, l3));
  for (int q = 0; q < l3; q++) printf(" %d", w3[q]); printf("\n");
  printf("angular-order violations (must be 0): %ld\n", order_violations);
  printf("RESULT %d %d %d %s\n", r1, r2, r3, (r1 == r2 && r2 == r3 && order_violations == 0) ? "AGREE" : "DISAGREE");
  return 0;
}
