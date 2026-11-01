/* es_dp.c -- largest subset in convex position, from the exact orientation table written by es_orient.
   Written from scratch for the R11 check (no code shared with sym_cvx.c).
   Method 1 (primary, no symmetry used): every convex polygon has a unique lowest vertex a in the exact (y,x) order;
     all its other vertices are strictly above a in that order, i.e. in the half-open upper half-plane at a, hence they
     are sorted by angle around a with comparator orient(a,x,y) > 0.  DP over chains a, q_i1, ..., q_im (increasing
     angle) with all interior turns left; the turns at a, q_i1, q_im are then automatically left and the closed polygon
     is convex (star-shaped from a, all turns left).  L[i][j] = 1 + max{L[k][i] : k<i, orient(q_k,q_i,q_j)>0}, else 3.
   Method 2: farthest-from-origin anchoring with the p-fold symmetry: one anchor per layer (sector-0 point), candidates
     = all other points with radius <= anchor radius (incl. same layer and centre); they lie strictly inside the
     tangent half-plane at the anchor.  Any convex polygon is rotated so its farthest vertex is a sector-0 point.
   Method 3 (subsets): Method 1 and 2 (no symmetry, all anchors) restricted to a subset vs brute-force DFS over all
     convex subsets (convex position <=> no point inside a triangle of three others; general position checked).
   usage: es_dp prefix [nsub subsize seed]  */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <time.h>

static int p, t, C, n;
static int *yrank, *lrank;
static uint8_t *OT;      /* OT bit (a*n+b)*n+c set iff orient(a,b,c) > 0 */
static inline int OPOS(int a, int b, int c) { uint64_t id = ((uint64_t)a * n + b) * n + c; return (OT[id >> 3] >> (id & 7)) & 1; }
static void die(const char *m) { fprintf(stderr, "FATAL: %s\n", m); exit(3); }
static inline uint64_t c3(uint64_t k) { return k * (k - 1) * (k - 2) / 6; }
static inline uint64_t c2(uint64_t k) { return k * (k - 1) / 2; }
static int layer(int x) { return x < p * t ? x / p : -1; }
static int sector(int x) { return x < p * t ? x % p : -1; }

static uint16_t *Lm; static int16_t *Fm, *Lst; static int maxu;
static int dp_core(int a, const int *cand, int u, int *wit, int *wlen) {
  if (u == 0) { if (wit) { wit[0] = a; *wlen = 1; } return 1; }
  if (u == 1) { if (wit) { wit[0] = a; wit[1] = cand[0]; *wlen = 2; } return 2; }
  int best = 3, bi = 0, bj = 1;
  static int cnt[1100], pos[1100];
  for (int j = 0; j < u; j++) {
    int cj = cand[j];
    for (int i = 0; i < j; i++) {
      int ci = cand[i]; const int16_t *lst = Lst + (size_t)i * u; int v = 3, fr = -1;
      for (int s = 0; s < i; s++) { int k = lst[s]; if (OPOS(cand[k], ci, cj)) { v = Lm[(size_t)k * u + i] + 1; fr = k; break; } }
      Lm[(size_t)i * u + j] = (uint16_t)v; Fm[(size_t)i * u + j] = (int16_t)fr;
      if (v > best) { best = v; bi = i; bj = j; }
    }
    /* list for column j: k<j sorted by Lm[k][j] descending (counting sort) */
    int mx = 0; for (int k = 0; k < j; k++) { int v = Lm[(size_t)k * u + j]; if (v > mx) mx = v; }
    if (mx >= 1100) die("value overflow");
    for (int v = 0; v <= mx; v++) cnt[v] = 0;
    for (int k = 0; k < j; k++) cnt[Lm[(size_t)k * u + j]]++;
    int acc = 0; for (int v = mx; v >= 0; v--) { pos[v] = acc; acc += cnt[v]; }
    int16_t *lj = Lst + (size_t)j * u;
    for (int k = 0; k < j; k++) lj[pos[Lm[(size_t)k * u + j]]++] = (int16_t)k;
  }
  if (wit) {
    int tmp[2048], len = 0, i = bi, j = bj;
    tmp[len++] = cand[j];
    while (i >= 0) { tmp[len++] = cand[i]; int f = Fm[(size_t)i * u + j]; j = i; i = f; }
    tmp[len++] = a;
    for (int q = 0; q < len; q++) wit[q] = tmp[len - 1 - q];
    *wlen = len;
  }
  return best;
}
static int g_anchor;
static void msort_ang(int *a, int len, int *tmp) {
  if (len < 2) return;
  int m = len / 2; msort_ang(a, m, tmp); msort_ang(a + m, len - m, tmp);
  int i = 0, j = m, k = 0;
  while (i < m && j < len) tmp[k++] = OPOS(g_anchor, a[i], a[j]) ? a[i++] : a[j++];
  while (i < m) tmp[k++] = a[i++]; while (j < len) tmp[k++] = a[j++];
  memcpy(a, tmp, sizeof(int) * len);
}
static void sort_check(int a, int *cand, int u, int *tmp) {
  g_anchor = a; msort_ang(cand, u, tmp);
  for (int i = 0; i + 1 < u; i++) if (!OPOS(a, cand[i], cand[i + 1])) die("angular order not consistent");
  if (u >= 2 && !OPOS(a, cand[0], cand[u - 1])) die("angular span >= 180 degrees");
}
/* convex position check of a list (general position assumed): no point inside a triangle of three others */
static int in_tri(int x, int a, int b, int c) { int o1 = OPOS(a, b, x), o2 = OPOS(b, c, x), o3 = OPOS(c, a, x); return o1 == o2 && o2 == o3; }
static int convex_position(const int *w, int len) {
  for (int x = 0; x < len; x++) for (int a = 0; a < len; a++) for (int b = a + 1; b < len; b++) for (int c = b + 1; c < len; c++) {
    if (x == a || x == b || x == c) continue;
    if (in_tri(w[x], w[a], w[b], w[c])) return 0;
  }
  return 1;
}
static int all_left(const int *w, int len) { for (int q = 0; q < len; q++) if (!OPOS(w[q], w[(q + 1) % len], w[(q + 2) % len])) return 0; return 1; }

/* method 1 on a subset mask (mask==NULL: all points) */
static int method1(const char *mask, int *wit, int *wlen, int verbose) {
  int *cand = malloc(sizeof(int) * n), *tmp = malloc(sizeof(int) * n), *order = malloc(sizeof(int) * n);
  int best = 0, w2[2048], l2;
  for (int x = 0; x < n; x++) order[yrank[x]] = x;   /* lowest first */
  clock_t t0 = clock();
  for (int r = 0; r < n; r++) {
    int a = order[r]; if (mask && !mask[a]) continue;
    int u = 0; for (int x = 0; x < n; x++) if (x != a && (!mask || mask[x]) && yrank[x] > yrank[a]) cand[u++] = x;
    if (u + 1 <= best) continue;
    sort_check(a, cand, u, tmp);
    int v = dp_core(a, cand, u, wit ? w2 : NULL, &l2);
    if (v > best) { best = v; if (wit) { memcpy(wit, w2, sizeof(int) * l2); *wlen = l2; } }
    if (verbose && (r % 100 == 0)) { printf("  method1 anchor rank %d (u=%d): best so far %d  [%.1fs]\n", r, u, best, (double)(clock() - t0) / CLOCKS_PER_SEC); fflush(stdout); }
  }
  free(cand); free(tmp); free(order);
  return best;
}
/* method 2: farthest-from-origin anchor; sym=1: only sector-0 anchors (requires full set) */
static int method2(const char *mask, int sym, int *wit, int *wlen, int verbose) {
  int *cand = malloc(sizeof(int) * n), *tmp = malloc(sizeof(int) * n);
  int best = 0, w2[2048], l2;
  clock_t t0 = clock();
  for (int a = 0; a < p * t; a++) {
    if (mask && !mask[a]) continue;
    if (sym && sector(a) != 0) continue;
    int u = 0;
    for (int x = 0; x < n; x++) { if (x == a || (mask && !mask[x])) continue; if (x == p * t || lrank[layer(x)] <= lrank[layer(a)]) cand[u++] = x; }
    if (u + 1 <= best) continue;
    sort_check(a, cand, u, tmp);
    int v = dp_core(a, cand, u, wit ? w2 : NULL, &l2);
    if (v > best) { best = v; if (wit) { memcpy(wit, w2, sizeof(int) * l2); *wlen = l2; } }
    if (verbose && sym && layer(a) % 10 == 0) { printf("  method2 anchor layer %d (u=%d): best so far %d  [%.1fs]\n", layer(a), u, best, (double)(clock() - t0) / CLOCKS_PER_SEC); fflush(stdout); }
  }
  free(cand); free(tmp);
  return best;
}
/* method 3: brute force DFS over convex subsets of sub[0..m-1] */
static int bf_best; static int bf_cur[64];
static void bf(const int *sub, int m, int s, int start) {
  if (s > bf_best) bf_best = s;
  for (int xi = start; xi < m; xi++) {
    int x = sub[xi], ok = 1;
    for (int a = 0; a < s && ok; a++) for (int b = a + 1; b < s && ok; b++) for (int c = b + 1; c < s && ok; c++)
      if (in_tri(x, bf_cur[a], bf_cur[b], bf_cur[c])) ok = 0;
    for (int y = 0; y < s && ok; y++) for (int b = 0; b < s && ok; b++) for (int c = b + 1; c < s && ok; c++) {
      if (b == y || c == y) continue;
      if (in_tri(bf_cur[y], x, bf_cur[b], bf_cur[c])) ok = 0;
    }
    if (!ok) continue;
    if (s >= 63) die("too deep");
    bf_cur[s] = x; bf(sub, m, s + 1, xi + 1);
  }
}
static unsigned long long rs = 0x9E3779B97F4A7C15ULL;
static unsigned long long xr(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }

int main(int argc, char **argv) {
  if (argc < 2) { fprintf(stderr, "usage: es_dp prefix [nsub subsize seed] [nosym-full]\n"); return 1; }
  char fn[4096];
  snprintf(fn, sizeof fn, "%s.meta", argv[1]); FILE *f = fopen(fn, "r"); if (!f) die("meta");
  if (fscanf(f, "%d %d %d %d", &p, &t, &C, &n) != 4) die("meta header");
  yrank = malloc(sizeof(int) * n); lrank = malloc(sizeof(int) * (t + 1));
  for (int i = 0; i < n; i++) if (fscanf(f, "%d", &yrank[i]) != 1) die("meta yrank");
  for (int l = 0; l < t; l++) if (fscanf(f, "%d", &lrank[l]) != 1) die("meta lrank");
  fclose(f);
  uint64_t ntri = c3(n); size_t nb = (ntri + 7) / 8;
  uint8_t *bits = malloc(nb); snprintf(fn, sizeof fn, "%s.signs", argv[1]); f = fopen(fn, "rb"); if (!f || fread(bits, 1, nb, f) != nb) die("signs"); fclose(f);
  uint64_t nt3 = (uint64_t)n * n * n; OT = calloc((nt3 + 7) / 8, 1); if (!OT) die("oom OT");
#define SETB(a, b, c, v) do { uint64_t id_ = ((uint64_t)(a) * n + (b)) * n + (c); if (v) OT[id_ >> 3] |= (uint8_t)(1u << (id_ & 7)); } while (0)
  for (int k = 2; k < n; k++) for (int j = 1; j < k; j++) for (int i = 0; i < j; i++) {
    uint64_t id = c3(k) + c2(j) + i; int s = (bits[id >> 3] >> (id & 7)) & 1;
    SETB(i, j, k, s); SETB(j, k, i, s); SETB(k, i, j, s);
    SETB(i, k, j, !s); SETB(k, j, i, !s); SETB(j, i, k, !s);
  }
  free(bits);
  maxu = n; Lm = malloc(sizeof(uint16_t) * (size_t)maxu * maxu); Fm = malloc(sizeof(int16_t) * (size_t)maxu * maxu); Lst = malloc(sizeof(int16_t) * (size_t)maxu * maxu);
  printf("loaded p=%d layers=%d centre=%d n=%d\n", p, t, C, n);
  /* layers: convex position of each regular p-gon, and nesting */
  {
    int okc = 1; long viol = 0, pairs_not_nested = 0;
    for (int l = 0; l < t; l++) { int w[64]; for (int k = 0; k < p; k++) w[k] = l * p + k; if (!all_left(w, p)) okc = 0; }
    for (int A = 0; A < t; A++) for (int B = 0; B < t; B++) {
      if (lrank[B] >= lrank[A]) continue;   /* B smaller radius */
      long v = 0; for (int k = 0; k < p; k++) for (int j = 0; j < p; j++) if (!OPOS(A * p + k, A * p + (k + 1) % p, B * p + j)) v++;
      viol += v; if (v) pairs_not_nested++;
    }
    printf("each layer is a convex p-gon in rotation order: %s; layer pairs (smaller layer not strictly inside larger polygon): %ld of %d, point-edge violations %ld\n",
           okc ? "yes" : "NO", pairs_not_nested, t * (t - 1) / 2, viol);
  }
  int nsub = argc >= 5 ? atoi(argv[2]) : 0, ssz = argc >= 5 ? atoi(argv[3]) : 0;
  if (argc >= 5) rs ^= (unsigned long long)atoll(argv[4]) * 0xD1B54A32D192ED03ULL;
  /* subset cross-checks first (fast) */
  char *mask = malloc(n); int *sub = malloc(sizeof(int) * n); int mism = 0;
  for (int it = 0; it < nsub; it++) {
    memset(mask, 0, n); int m = 0; int mode = it % 4; int s0 = xr() % (p ? p : 1), win = 1 + (int)(xr() % 3);
    int target = ssz < n ? ssz : n; long tries = 0;
    while (m < target) {
      int x; tries++;
      if (mode == 3 || t == 0 || tries > 20L * target) x = xr() % n;   /* fall back to uniform when the window is exhausted */
      else { int s = (s0 + (int)(xr() % (mode == 0 ? 1 : win))) % p; int l = xr() % (t + C); x = (l == t) ? p * t : l * p + s; }
      if (!mask[x]) { mask[x] = 1; sub[m++] = x; }
    }
    int r1 = method1(mask, NULL, NULL, 0), r2 = method2(mask, 0, NULL, NULL, 0);
    bf_best = 0; bf(sub, m, 0, 0); int r3 = bf_best;
    printf("  subset %2d (mode %d, %d pts): method1 %d  method2 %d  brute-force %d %s\n", it, mode, m, r1, r2, r3, (r1 == r2 && r2 == r3) ? "" : "MISMATCH");
    fflush(stdout);
    if (!(r1 == r2 && r2 == r3)) mism++;
  }
  if (nsub) printf("subset cross-checks: %d subsets, %d mismatches\n", nsub, mism);
  /* full set */
  int wit[2048], wl = 0;
  clock_t t0 = clock();
  int b2 = method2(NULL, 1, wit, &wl, 1);
  printf("METHOD2 (farthest-from-origin anchor, symmetry, %d anchors): largest convex subset = %d  [%.1fs]\n", t, b2, (double)(clock() - t0) / CLOCKS_PER_SEC);
  printf("  witness (%d):", wl); for (int q = 0; q < wl; q++) printf(" %d(L%d,s%d)", wit[q], layer(wit[q]), sector(wit[q]));
  printf("\n  witness all turns left: %s, convex position (no point in triangle of 3 others): %s\n", all_left(wit, wl) ? "yes" : "NO", convex_position(wit, wl) ? "yes" : "NO");
  fflush(stdout);
  t0 = clock();
  int b1 = method1(NULL, wit, &wl, 1);
  printf("METHOD1 (lowest-vertex anchor, all %d anchors, no symmetry): largest convex subset = %d  [%.1fs]\n", n, b1, (double)(clock() - t0) / CLOCKS_PER_SEC);
  printf("  witness (%d):", wl); for (int q = 0; q < wl; q++) printf(" %d(L%d,s%d)", wit[q], layer(wit[q]), sector(wit[q]));
  printf("\n  witness all turns left: %s, convex position: %s\n", all_left(wit, wl) ? "yes" : "NO", convex_position(wit, wl) ? "yes" : "NO");
  if (argc >= 6) {
    t0 = clock();
    int b3 = method2(NULL, 0, NULL, NULL, 0);
    printf("METHOD2' (farthest-from-origin anchor, all %d anchors, no symmetry): largest convex subset = %d  [%.1fs]\n", p * t, b3, (double)(clock() - t0) / CLOCKS_PER_SEC);
  }
  printf("RESULT largest_convex_subset method1=%d method2=%d subset_mismatches=%d\n", b1, b2, mism);
  return 0;
}
