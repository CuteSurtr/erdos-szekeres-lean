/* Independent exact checker (no dynamic program, no shared code with geom.py).
   usage: enum_convex POINTS.txt [ORIENT_FILE] [MODE]
     POINTS.txt : "x y" integer pairs, |coordinate| < 2^62 (orientations computed here with __int128;
                  every product is bounded by (2^63)^2 = 2^126, so no overflow).
     ORIENT_FILE: optional table written by verify_set.py; every sign is compared with ours.
     MODE       : "C2" (default) checks P = -P and origin not in P; "M" checks (x,y)->(-x,y); "none" skips.
   Then it enumerates EVERY subset in convex position: for each point a taken as the lowest vertex (least (y,x)),
   the other vertices lie strictly above a in (y,x) order; they are visited in counterclockwise angular order around
   a by a depth-first search that only appends a vertex making a left turn, and a chain a,v1..vr is counted as an
   (r+1)-gon iff the closing turns (v_{r-1},v_r,a) and (v_r,a,v_1) are left turns.  Prints the number of convex
   j-gons for every j and the largest j.  Exits 0 iff general position (and symmetry) hold. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef __int128 i128;
static long long X[1024], Y[1024];
static int n;
static signed char *O;
#define OR(a, b, c) O[((size_t)(a) * n + (b)) * n + (c)]
static long long cnt[64];
static int maxsz = 0;
static int up[1024], m, A;

static int sgn128(i128 v) { return (v > 0) - (v < 0); }

static void dfs(int first, int p2, int p1, int len) {
  /* chain: A, ..., up[p2], up[p1] (len vertices including A), p2 < p1 indices in angular order */
  int prev2 = up[p2], prev = up[p1];
  if (OR(prev2, prev, A) > 0 && OR(prev, A, first) > 0) {
    cnt[len]++;
    if (len > maxsz) maxsz = len;
  }
  for (int t = p1 + 1; t < m; t++)
    if (OR(prev2, prev, up[t]) > 0) dfs(first, p1, t, len + 1);
}

int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "r");
  if (!f) return 2;
  char line[512];
  while (fgets(line, sizeof line, f)) {
    if (line[0] == '#' || line[0] == '\n') continue;
    if (sscanf(line, "%lld %lld", &X[n], &Y[n]) == 2) n++;
  }
  fclose(f);
  for (int i = 0; i < n; i++)
    if (llabs(X[i]) >= (1LL << 62) || llabs(Y[i]) >= (1LL << 62)) { printf("coordinate too large\n"); return 2; }
  O = malloc((size_t)n * n * n);
  long long coll = 0;
  for (int a = 0; a < n; a++)
    for (int b = 0; b < n; b++)
      for (int c = 0; c < n; c++) {
        if (a == b || b == c || a == c) { OR(a, b, c) = 0; continue; }
        i128 v = (i128)(X[b] - X[a]) * (Y[c] - Y[a]) - (i128)(Y[b] - Y[a]) * (X[c] - X[a]);
        OR(a, b, c) = (signed char)sgn128(v);
        if (v == 0 && a < b && b < c) coll++;
      }
  int ok = 1, dup = 0;
  for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) if (X[i] == X[j] && Y[i] == Y[j]) dup++;
  printf("n=%d duplicates=%d collinear_triples=%lld\n", n, dup, coll);
  if (dup || coll) ok = 0;
  const char *mode = argc > 3 ? argv[3] : "C2";
  if (strcmp(mode, "none") != 0) {
    int sym = 1, origin = 0;
    for (int i = 0; i < n; i++) {
      long long tx = strcmp(mode, "M") == 0 ? -X[i] : -X[i], ty = strcmp(mode, "M") == 0 ? Y[i] : -Y[i];
      int found = 0;
      for (int j = 0; j < n; j++) if (X[j] == tx && Y[j] == ty) found = 1;
      if (!found) sym = 0;
      if (X[i] == 0 && Y[i] == 0) origin = 1;
    }
    printf("symmetry(%s)=%d origin_in_set=%d\n", mode, sym, origin);
    if (!sym || (strcmp(mode, "C2") == 0 && origin)) ok = 0;
  }
  if (argc > 2 && strcmp(argv[2], "-") != 0) {
    FILE *g = fopen(argv[2], "r");
    int nn; long long mism = 0;
    if (!g || fscanf(g, "%d", &nn) != 1 || nn != n) { printf("orient file mismatch in n\n"); return 2; }
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) for (int c = 0; c < n; c++) {
      int v; if (fscanf(g, "%d", &v) != 1) { printf("orient file short\n"); return 2; }
      if (v != OR(a, b, c)) mism++;
    }
    fclose(g);
    printf("orientation signs differing from %s: %lld\n", argv[2], mism);
    if (mism) ok = 0;
  }
  for (A = 0; A < n; A++) {
    m = 0;
    for (int i = 0; i < n; i++)
      if (Y[i] > Y[A] || (Y[i] == Y[A] && X[i] > X[A])) up[m++] = i;
    /* sort up[] counterclockwise around A (all in the upper half-plane w.r.t. (y,x) order: total order) */
    for (int i = 1; i < m; i++) {
      int v = up[i], j = i - 1;
      while (j >= 0 && OR(A, v, up[j]) > 0) { up[j + 1] = up[j]; j--; }
      up[j + 1] = v;
    }
    for (int t = 0; t < m; t++) {
      int v1 = up[t];
      /* chain A, v1: extend */
      for (int s = t + 1; s < m; s++) {
        int v2 = up[s];
        if (OR(A, v1, v2) > 0) dfs(v1, t, s, 3);
      }
    }
  }
  for (int j = 3; j < 64; j++) if (cnt[j]) printf("convex %d-gons: %lld\n", j, cnt[j]);
  printf("largest convex subset: %d\n", maxsz);
  return ok ? 0 : 1;
}
