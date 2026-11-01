/* sym_cvx.c -- exact verification of a p-fold symmetric point set in Z[zeta_p] (GMP).
   Input points file: header comment, then "p t C", then t lines of p integers (sector-0 representatives, coefficients of
   zeta^0..zeta^{p-1}); C=1 adds the centre. All points: layer*p + k = rep * zeta^k (cyclic shift), centre last.
   Trig file: "p PREC", then p lines "round(2^PREC sin(2 pi j/p)) round(2^PREC cos(2 pi j/p))".
   Checks:
     (1) every orientation sign certified nonzero (double filter with rigorous bound, else exact fixed-point evaluation
         sum_k w_k S_k with |error| <= sum |w_k|; undecided -> FAIL);
     (2) radii of layers pairwise distinct (certified), points distinct;
     (3) largest convex subset by an O(u^3) DP anchored at the farthest vertex (anchor = sector-0 point of each layer,
         candidates = points with radius <= anchor radius; they lie strictly inside the tangent half-plane);
     (4) second method on random subsets: brute-force DFS (all 4-subsets convex) vs a DP anchored at the lowest point
         (exact Im comparisons), compared with (3) restricted to the subset.
   usage: sym_cvx points trig K [nsubsets subsetsize seed]   (exit 0 iff largest convex subset < K and all checks pass) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <gmp.h>
#define MAXP 16
static int p, t, C, n, PREC;
static mpz_t **P;              /* P[i][j] */
static mpz_t Ssin[MAXP], Scos[MAXP];
static double zr[MAXP], zi[MAXP];
static signed char *T, *Tc;   /* T[(lx*n + y)*n + z], Tc[y*n+z] */
static long n_filter = 0, n_exact = 0;
static int sector(int x) { return x == p * t ? -1 : x % p; }
static int layer(int x) { return x == p * t ? -1 : x / p; }
static int rot(int x, int k) { if (x == p * t) return x; int s = (x % p + k) % p; if (s < 0) s += p; return (x / p) * p + s; }
/* certified sign of sum_k w_k * TAB_k (TAB scaled by 2^PREC, |TAB_k - exact| <= 1) */
static int cert_sign(mpz_t *w, mpz_t *TAB, mpz_t acc, mpz_t err, mpz_t tmp) {
  mpz_set_ui(acc, 0); mpz_set_ui(err, 0);
  for (int k = 0; k < p; k++) { mpz_addmul(acc, w[k], TAB[k]); mpz_abs(tmp, w[k]); mpz_add(err, err, tmp); }
  mpz_add_ui(err, err, 1);
  mpz_abs(tmp, acc);
  if (mpz_cmp(tmp, err) > 0) return mpz_sgn(acc);
  return 0;   /* undecided */
}
static mpz_t U[MAXP], V[MAXP], W[MAXP], acc, err, tmp;
static int orient_exact(int a, int b, int c) {
  for (int j = 0; j < p; j++) { mpz_sub(U[j], P[b][j], P[a][j]); mpz_sub(V[j], P[c][j], P[a][j]); }
  /* double filter */
  double ur = 0, ui = 0, vr = 0, vi = 0, u1 = 0, v1 = 0;
  for (int j = 0; j < p; j++) {
    double x = mpz_get_d(U[j]), y = mpz_get_d(V[j]);
    ur += x * zr[j]; ui += x * zi[j]; vr += y * zr[j]; vi += y * zi[j]; u1 += fabs(x); v1 += fabs(y);
  }
  double cr = ur * vi - ui * vr;                 /* Im(conj(u) v) */
  double bound = 8.0 * (p + 4) * ldexp(1.0, -52) * u1 * v1 * 1.0001 + 1e-300;
  n_filter++;
  if (fabs(cr) > bound) return cr > 0 ? 1 : -1;
  n_exact++;
  for (int k = 0; k < p; k++) {
    mpz_set_ui(W[k], 0);
    for (int j = 0; j < p; j++) mpz_addmul(W[k], U[(p - j) % p], V[((k - j) % p + p) % p]);
  }
  int s = cert_sign(W, Ssin, acc, err, tmp);
  if (s == 0) { fprintf(stderr, "UNDECIDED orientation %d %d %d\n", a, b, c); exit(3); }
  return s;
}
static int orient(int a, int b, int c) {
  if (a == p * t) { /* centre first: rotate b to sector 0 */
    if (b == p * t || c == p * t) return 0;
    int s = sector(b); return Tc[(size_t)rot(b, -s) * n + rot(c, -s)];
  }
  int s = sector(a);
  return T[((size_t)layer(a) * n + rot(b, -s)) * n + rot(c, -s)];
}
/* exact comparison of squared radii of two points: sign(|a|^2 - |b|^2) */
static int cmp_radius(int a, int b) {
  mpz_t ra[MAXP], rb[MAXP];
  for (int k = 0; k < p; k++) { mpz_init(ra[k]); mpz_init(rb[k]); }
  for (int k = 0; k < p; k++) for (int j = 0; j < p; j++) {
    mpz_addmul(ra[k], P[a][j], P[a][((j - k) % p + p) % p]);
    mpz_addmul(rb[k], P[b][j], P[b][((j - k) % p + p) % p]);
  }
  for (int k = 0; k < p; k++) mpz_sub(ra[k], ra[k], rb[k]);
  int s = cert_sign(ra, Scos, acc, err, tmp);
  int allzero = 1; for (int k = 0; k < p; k++) if (mpz_sgn(ra[k])) allzero = 0;
  for (int k = 0; k < p; k++) { mpz_clear(ra[k]); mpz_clear(rb[k]); }
  if (s == 0 && !allzero) { fprintf(stderr, "UNDECIDED radius comparison %d %d\n", a, b); exit(3); }
  return s;
}
/* exact sign of Im(b - a) */
static int cmp_im(int a, int b) {
  mpz_t d[MAXP]; for (int k = 0; k < p; k++) { mpz_init(d[k]); mpz_sub(d[k], P[b][k], P[a][k]); }
  int s = cert_sign(d, Ssin, acc, err, tmp);
  int allzero = 1; for (int k = 0; k < p; k++) if (mpz_sgn(d[k])) allzero = 0;
  for (int k = 0; k < p; k++) mpz_clear(d[k]);
  if (s == 0 && !allzero) { fprintf(stderr, "UNDECIDED Im comparison\n"); exit(3); }
  return s;
}
static int cmp_re(int a, int b) {
  mpz_t d[MAXP]; for (int k = 0; k < p; k++) { mpz_init(d[k]); mpz_sub(d[k], P[b][k], P[a][k]); }
  int s = cert_sign(d, Scos, acc, err, tmp);
  for (int k = 0; k < p; k++) mpz_clear(d[k]);
  return s;
}
/* ---------- method A: farthest-vertex anchored DP over the whole set (or a subset mask) ---------- */
static int g_anchor;
static int cmp_ang(const void *x, const void *y) { int a = *(const int *)x, b = *(const int *)y; return orient(g_anchor, a, b) > 0 ? -1 : 1; }
static int *layer_rank;   /* rank of layer radius: larger radius -> smaller rank; ties impossible (checked) */
static int dp_farthest(const char *mask, int *witness, int *wlen) {
  int best = 0; int *cand = malloc(sizeof(int) * n); short *D = malloc(sizeof(short) * (size_t)n * n);
  int *from = malloc(sizeof(int) * (size_t)n * n);
  for (int a = 0; a < n; a++) {
    if (!mask[a] || a == p * t) continue;
    int u = 0;
    for (int x = 0; x < n; x++) {
      if (x == a || !mask[x]) continue;
      if (x == p * t || layer_rank[layer(x)] >= layer_rank[layer(a)]) cand[u++] = x;   /* radius(x) <= radius(a) */
    }
    if (u + 1 > best && u >= 2) {
      g_anchor = a; qsort(cand, u, sizeof(int), cmp_ang);
      for (int j = 0; j < u; j++) for (int i = 0; i < j; i++) {
        int v = 3, fr = -1;
        for (int hh = 0; hh < i; hh++) {
          int dv = D[(size_t)hh * u + i];
          if (dv + 1 > v && orient(cand[hh], cand[i], cand[j]) > 0) { v = dv + 1; fr = hh; }
        }
        D[(size_t)i * u + j] = v; from[(size_t)i * u + j] = fr;
        if (v > best && orient(cand[i], cand[j], a) > 0) {
          best = v;
          if (witness) { /* reconstruct */
            int len = 0, ii = i, jj = j; int tmpw[64];
            tmpw[len++] = cand[jj];
            while (ii >= 0) { tmpw[len++] = cand[ii]; int f = from[(size_t)ii * u + jj]; jj = ii; ii = f; }
            tmpw[len++] = a; *wlen = len; for (int q = 0; q < len; q++) witness[q] = tmpw[len - 1 - q];
          }
        }
      }
    }
  }
  free(cand); free(D); free(from);
  return best;
}
/* ---------- method B: lowest-point anchored DP (exact (Im, Re) order) on a subset ---------- */
static int dp_lowest(int *S, int m) {
  int best = m < 2 ? m : 2; int *up = malloc(sizeof(int) * m); short *D = malloc(sizeof(short) * m * m);
  for (int ai = 0; ai < m; ai++) {
    int a = S[ai], u = 0;
    for (int xi = 0; xi < m; xi++) { int x = S[xi]; if (x == a) continue; int s = cmp_im(a, x); if (s == 0) s = cmp_re(a, x); if (s > 0) up[u++] = x; }
    g_anchor = a; qsort(up, u, sizeof(int), cmp_ang);
    for (int j = 0; j < u; j++) for (int i = 0; i < j; i++) {
      int v = 3; for (int hh = 0; hh < i; hh++) { int dv = D[hh * u + i]; if (dv + 1 > v && orient(up[hh], up[i], up[j]) > 0) v = dv + 1; }
      D[i * u + j] = v; if (v > best && orient(up[i], up[j], a) > 0) best = v;
    }
  }
  free(up); free(D); return best;
}
/* ---------- method C: brute-force DFS (subset in convex position iff no point in a triangle of three others) ---------- */
static int Sdfs[64], bestdfs; static int *Sub; static int msub;
static int in_tri(int x, int a, int b, int c) { int o1 = orient(a, b, x), o2 = orient(b, c, x), o3 = orient(c, a, x); return o1 == o2 && o2 == o3; }
static void dfs(int s, int start) {
  if (s > bestdfs) bestdfs = s;
  for (int xi = start; xi < msub; xi++) {
    int x = Sub[xi], ok = 1;
    for (int i = 0; i < s && ok; i++) for (int j = i + 1; j < s && ok; j++) for (int l = j + 1; l < s && ok; l++) {
      int a = Sdfs[i], b = Sdfs[j], c = Sdfs[l];
      if (in_tri(x, a, b, c) || in_tri(a, b, c, x) || in_tri(b, a, c, x) || in_tri(c, a, b, x)) ok = 0;
    }
    if (!ok) continue;
    Sdfs[s] = x; dfs(s + 1, xi + 1);
  }
}
static unsigned long long rs = 88172645463325252ULL;
static unsigned long long xr(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: sym_cvx points trig K [nsub subsize seed]\n"); return 1; }
  int K = atoi(argv[3]);
  FILE *f = fopen(argv[1], "r"); char line[1 << 16];
  do { if (!fgets(line, sizeof line, f)) return 1; } while (line[0] == '#');
  sscanf(line, "%d %d %d", &p, &t, &C);
  n = p * t + C;
  P = malloc(sizeof(mpz_t *) * n);
  for (int i = 0; i < n; i++) { P[i] = malloc(sizeof(mpz_t) * p); for (int j = 0; j < p; j++) mpz_init(P[i][j]); }
  for (int l = 0; l < t; l++) for (int j = 0; j < p; j++) { if (mpz_inp_str(P[l * p][j], f, 10) == 0) { fprintf(stderr, "read error\n"); return 1; } }
  fclose(f);
  for (int l = 0; l < t; l++) for (int k = 1; k < p; k++) for (int j = 0; j < p; j++) mpz_set(P[l * p + k][j], P[l * p][((j - k) % p + p) % p]);
  FILE *g = fopen(argv[2], "r"); int pp; fscanf(g, "%d %d", &pp, &PREC); if (pp != p) { fprintf(stderr, "trig table for wrong p\n"); return 1; }
  for (int j = 0; j < p; j++) { mpz_init(Ssin[j]); mpz_init(Scos[j]); mpz_inp_str(Ssin[j], g, 10); mpz_inp_str(Scos[j], g, 10); }
  fclose(g);
  for (int j = 0; j < p; j++) { zr[j] = cos(2 * M_PI * j / p); zi[j] = sin(2 * M_PI * j / p); }
  for (int j = 0; j < MAXP; j++) { mpz_init(U[j]); mpz_init(V[j]); mpz_init(W[j]); }
  mpz_init(acc); mpz_init(err); mpz_init(tmp);
  printf("p=%d t=%d centre=%d n=%d PREC=%d\n", p, t, C, n, PREC);
  /* radii: distinct layers, ranks */
  layer_rank = malloc(sizeof(int) * t);
  int distinct_ok = 1;
  for (int a = 0; a < t; a++) { layer_rank[a] = 0; for (int b = 0; b < t; b++) if (b != a) { int s = cmp_radius(b * p, a * p); if (s == 0) distinct_ok = 0; if (s > 0) layer_rank[a]++; } }
  /* points distinct: distinct radii across layers; within a layer the p rotations are distinct iff the rep is nonzero */
  for (int a = 0; a < t; a++) { int nz = 0; for (int j = 0; j < p; j++) if (mpz_sgn(P[a * p][j])) nz = 1; if (!nz) distinct_ok = 0; }
  printf("layers have pairwise distinct radii and nonzero reps: %s\n", distinct_ok ? "yes" : "NO");
  /* orientation tables */
  T = malloc((size_t)t * n * n); Tc = malloc((size_t)n * n);
  if (!T || !Tc) { fprintf(stderr, "out of memory\n"); return 1; }
  long zeros = 0;
  for (int lx = 0; lx < t; lx++) {
    int x = lx * p;
    for (int y = 0; y < n; y++) for (int z = 0; z < n; z++) T[((size_t)lx * n + y) * n + z] = 0;
    for (int y = 0; y < n; y++) for (int z = y + 1; z < n; z++) {
      if (y == x || z == x) continue;
      int o = orient_exact(x, y, z); if (o == 0) zeros++;
      T[((size_t)lx * n + y) * n + z] = o; T[((size_t)lx * n + z) * n + y] = -o;
    }
  }
  if (C) {
    int c0 = p * t;
    for (size_t i = 0; i < (size_t)n * n; i++) Tc[i] = 0;
    for (int y = 0; y < n; y++) for (int z = y + 1; z < n; z++) { if (y == c0 || z == c0) continue; int o = orient_exact(c0, y, z); Tc[(size_t)y * n + z] = o; Tc[(size_t)z * n + y] = -o; }
  }
  printf("orientation tables: %ld filter calls, %ld exact evaluations, zero orientations: %ld\n", n_filter, n_exact, zeros);
  /* consistency: cyclic symmetry orient(a,b,c) = orient(b,c,a) on random triples */
  long bad = 0;
  for (int it = 0; it < 200000; it++) {
    int a = xr() % n, b = xr() % n, c = xr() % n; if (a == b || b == c || a == c) continue;
    int o1 = orient(a, b, c), o2 = orient(b, c, a), o3 = orient(c, a, b), o4 = orient(b, a, c);
    if (o1 != o2 || o2 != o3 || o4 != -o1 || o1 == 0) bad++;
  }
  printf("random consistency check (cyclic/antisymmetric/nonzero) violations: %ld\n", bad);
  if (getenv("SAMPLE_OUT")) {
    FILE *so = fopen(getenv("SAMPLE_OUT"), "w"); long ns = getenv("SAMPLE_N") ? atol(getenv("SAMPLE_N")) : 100000;
    for (long it = 0; it < ns; it++) {
      int a = xr() % n, b = xr() % n, c = xr() % n;
      if (it % 2 == 0) { /* half the sample inside one cluster neighbourhood (same sector) for near-degenerate triples */
        int s0 = xr() % p; a = (xr() % t) * p + s0; b = (xr() % t) * p + s0; c = (xr() % t) * p + s0; }
      if (a == b || b == c || a == c) continue;
      fprintf(so, "%d %d %d %d\n", a, b, c, orient(a, b, c));
    }
    fclose(so); printf("wrote orientation sample to %s\n", getenv("SAMPLE_OUT"));
  }
  char *mask = malloc(n); memset(mask, 1, n);
  int wit[64], wl = 0;
  int best = dp_farthest(mask, wit, &wl);
  printf("method A (farthest-vertex DP, whole set): largest convex subset = %d\n", best);
  /* verify witness polygon with exact orientations: all consecutive turns left and convex position */
  int wok = 1;
  for (int q = 0; q < wl; q++) if (orient(wit[q], wit[(q + 1) % wl], wit[(q + 2) % wl]) <= 0) wok = 0;
  printf("witness polygon of size %d:", wl); for (int q = 0; q < wl; q++) printf(" %d(L%d,s%d)", wit[q], layer(wit[q]), sector(wit[q])); printf("  all turns left: %s\n", wok ? "yes" : "NO");
  int sub_ok = 1;
  if (argc >= 7) {
    int ns = atoi(argv[4]), ss = atoi(argv[5]); rs ^= (unsigned long long)atoll(argv[6]) * 0x9E3779B97F4A7C15ULL;
    Sub = malloc(sizeof(int) * n);
    const char *wl_env = getenv("SUBSET_WINDOWS"); char wbuf[256]; strncpy(wbuf, wl_env ? wl_env : "0", 255); wbuf[255] = 0;
    for (char *tok = strtok(wbuf, ","); tok; tok = strtok(NULL, ",")) {
    int win = atoi(tok);
    for (int it = 0; it < ns; it++) {
      memset(mask, 0, n); msub = 0;
      int s0 = xr() % p;
      while (msub < ss) { int x;
        if (win > 0) { int s = (s0 + (int)(xr() % win)) % p; int l = xr() % (t + 1); x = (l == t) ? (C ? p * t : 0) : l * p + s; }
        else if (msub < ss / 2) { int s = xr() % p; int l = xr() % t; x = l * p + s; } else x = xr() % n;
        if (!mask[x]) { mask[x] = 1; Sub[msub++] = x; } }
      int a1 = dp_farthest(mask, NULL, NULL);
      int a2 = dp_lowest(Sub, msub);
      bestdfs = 0; dfs(0, 0);
      int a3 = bestdfs;
      printf("  window %d subset %2d (%d points): farthest-DP %d  lowest-DP %d  brute-force DFS %d %s\n", win, it, msub, a1, a2, a3, (a1 == a2 && a2 == a3) ? "" : "MISMATCH");
      fflush(stdout);
      if (!(a1 == a2 && a2 == a3)) sub_ok = 0;
    }
    }
  }
  int ok = distinct_ok && zeros == 0 && bad == 0 && wok && sub_ok && best < K;
  printf("%s (K=%d)\n", ok ? "PASS" : "FAIL", K);
  return ok ? 0 : 2;
}
