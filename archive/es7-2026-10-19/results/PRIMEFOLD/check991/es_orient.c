/* es_orient.c -- independent exact orientation table for a p-fold symmetric point set with points in Z[zeta_p].
   Written from scratch for the R11 refutation check (no code shared with sym_cvx.c).

   Sign method (no transcendental functions, no floating point in any decision):
     z = sum_k c_k zeta^k,  theta = 2 pi / p,  t = 2 cos theta = zeta + zeta^{-1}.
     Im z = sum_{k=1..h} w_k sin(k theta),  w_k = c_k - c_{p-k}   ->   Im z = sin(theta) * sum_k w_k U_{k-1}(t)
     (U_n Chebyshev 2nd kind written as an integer polynomial in t: U_0=1, U_1=t, U_{n+1}=t U_n - U_{n-1}).
     2 Re z = sum_{k=0..h} v_k V_k(t), v_0 = c_0, v_k = c_k + c_{p-k}, V_0=2, V_1=t, V_{n+1}=t V_n - V_{n-1}, reduced mod m.
     m(x) = 1 + sum_{k=1..h} V_k(x) is monic of degree h and vanishes at 2cos(2 pi k/p), k=1..h (from Phi_p(zeta^k)=0),
     which are h distinct reals, so m = prod (x - 2cos(2 pi k/p)) and t is its LARGEST root.
     t is isolated by exact bisection on dyadic rationals (sign of m evaluated exactly in integers); the rightmost of the
     h sign-change intervals of a fine grid on [-2,2] is the start (h sign changes found => one root per interval).
     Fixed point: T_d = floor(2^B lo^d), U_d = ceil(2^B hi^d) for t in (lo,hi) => 2^B t^d in (T_d, U_d); a polynomial
     q(t) = sum q_d t^d is decided when |sum q_d T_d| > sum |q_d| (U_d - T_d).  Escalating B; exact zero iff q == 0
     (Im/Re z = 0 iff the corresponding coefficient vector vanishes, by irreducibility of Phi_p).
   Orientation(i,j,k) = cross(P_j - P_i, P_k - P_i) = X(i,j) + X(j,k) - X(i,k) (i<j<k), X(a,b) = Im(conj(P_a) P_b).
   Fast path: per pair, S(a,b) = sum_d q_d(a,b) T_d at B0 with error e(a,b) <= sum |q_d| E_d; triple decided when
   |S(i,j)+S(j,k)-S(i,k)| > 3 max_e.  Otherwise: full recomputation from conj(P_j-P_i)(P_k-P_i) with escalation.
   usage: es_orient points.pts outprefix
   outputs: outprefix.signs (bit idx = C(k,3)+C(j,2)+i set iff orient(i,j,k) > 0, i<j<k), outprefix.meta */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <gmp.h>

#define MAXP 23
static int p, h, t, C, n;
static mpz_t **P;                 /* P[i][0..p-1] */
static long mpol[MAXP + 1];       /* m(x), monic degree h */
static long Umat[MAXP][MAXP];     /* Umat[d][k-1] = coef of t^d in U_{k-1}(t), k=1..h */
static long Vmat[MAXP][MAXP + 1]; /* Vmat[d][k] = coef of t^d in (V_k mod m), k=0..h */
#define NLEV 4
static int LEVB[NLEV] = {320, 1280, 5120, 20480};
static mpz_t TT[NLEV][MAXP], EE[NLEV][MAXP];
static int lev_ready[NLEV];
static long glo_X, ghi_X; static int g_bits;  /* coarse isolating interval [glo_X, ghi_X] / 2^g_bits */

static void die(const char *m) { fprintf(stderr, "FATAL: %s\n", m); exit(3); }

/* sign of 2^{hM} m(X / 2^M) */
static int msign(const mpz_t X, int M) {
  mpz_t acc, tmp; mpz_init_set_si(acc, mpol[h]); mpz_init(tmp);
  for (int d = h - 1; d >= 0; d--) {
    mpz_mul(acc, acc, X);
    mpz_set_si(tmp, mpol[d]); mpz_mul_2exp(tmp, tmp, (mp_bitcnt_t)M * (h - d));
    mpz_add(acc, acc, tmp);
  }
  int s = mpz_sgn(acc); mpz_clear(acc); mpz_clear(tmp); return s;
}

static void setup_polys(void) {
  long V[MAXP + 2][MAXP + 2], U[MAXP + 2][MAXP + 2];
  memset(V, 0, sizeof V); memset(U, 0, sizeof U);
  V[0][0] = 2; V[1][1] = 1;
  for (int k = 1; k < h; k++) for (int d = 0; d <= h; d++) V[k + 1][d] = (d ? V[k][d - 1] : 0) - V[k - 1][d];
  U[0][0] = 1; U[1][1] = 1;
  for (int k = 1; k < h; k++) for (int d = 0; d <= h; d++) U[k + 1][d] = (d ? U[k][d - 1] : 0) - U[k - 1][d];
  memset(mpol, 0, sizeof mpol); mpol[0] = 1;
  for (int k = 1; k <= h; k++) for (int d = 0; d <= h; d++) mpol[d] += V[k][d];
  if (mpol[h] != 1) die("m not monic");
  /* reduce V_k mod m (only V_h has degree h) */
  for (int k = 0; k <= h; k++) {
    long r[MAXP + 2]; for (int d = 0; d <= h; d++) r[d] = V[k][d];
    if (r[h]) { long c = r[h]; for (int d = 0; d <= h; d++) r[d] -= c * mpol[d]; }
    if (r[h]) die("reduction failed");
    for (int d = 0; d < h; d++) Vmat[d][k] = r[d];
  }
  for (int k = 1; k <= h; k++) for (int d = 0; d < h; d++) Umat[d][k - 1] = U[k - 1][d];
  /* check x^h m(x + 1/x) == Phi_p(x) = 1 + x + ... + x^{p-1} exactly (polynomial identity) */
  {
    /* expand sum_d mpol[d] (x^2+1)^d x^{h-d} */
    long res[2 * MAXP + 2]; memset(res, 0, sizeof res);
    for (int d = 0; d <= h; d++) {
      long bin[2 * MAXP + 2]; memset(bin, 0, sizeof bin); bin[0] = 1;       /* (x^2+1)^d */
      for (int e = 0; e < d; e++) { for (int q = 2 * MAXP; q >= 2; q--) bin[q] += bin[q - 2]; }
      for (int q = 0; q <= 2 * d; q++) res[q + h - d] += mpol[d] * bin[q];
    }
    for (int q = 0; q <= 2 * h; q++) if (res[q] != 1) die("x^h m(x+1/x) != Phi_p");
  }
  printf("m(x) = "); for (int d = h; d >= 0; d--) printf("%+ld x^%d ", mpol[d], d); printf("  [checked x^h m(x+1/x) = Phi_p(x)]\n");
  /* grid sign changes on [-2,2] */
  int g = 14; long N = 1L << g; int prev = 0, changes = 0; long lastX = 0;
  mpz_t X; mpz_init(X);
  for (long i = 0; i <= 4 * N; i++) {
    long Xv = -2 * N + i; mpz_set_si(X, Xv);
    int s = msign(X, g); if (s == 0) die("m has a dyadic root on the grid");
    if (i > 0 && s != prev) { changes++; lastX = Xv - 1; }
    prev = s;
  }
  if (changes != h) die("wrong number of sign changes of m on [-2,2]");
  glo_X = lastX; ghi_X = lastX + 1; g_bits = g;
  printf("m has %d sign changes on a 2^-%d grid of [-2,2]; largest root t in [%ld, %ld]/2^%d = [%.9f, %.9f]; 2cos(2pi/p) = %.9f (double, info only)\n",
         changes, g, glo_X, ghi_X, g, (double)glo_X / N, (double)ghi_X / N, 2 * cos(2 * M_PI / p));
  mpz_clear(X);
}

static void make_level(int L) {
  if (lev_ready[L]) return;
  int B = LEVB[L], M = B + 64;
  mpz_t lo, hi, mid; mpz_init_set_si(lo, glo_X); mpz_init_set_si(hi, ghi_X); mpz_init(mid);
  mpz_mul_2exp(lo, lo, M - g_bits); mpz_mul_2exp(hi, hi, M - g_bits);
  int slo = msign(lo, M), shi = msign(hi, M);
  if (slo == 0 || shi == 0 || slo == shi) die("bad isolating interval");
  mpz_t w; mpz_init(w);
  for (;;) {
    mpz_sub(w, hi, lo); if (mpz_cmp_ui(w, 1) <= 0) break;
    mpz_add(mid, lo, hi); mpz_fdiv_q_2exp(mid, mid, 1);
    int s = msign(mid, M); if (s == 0) die("dyadic root");
    if (s == slo) mpz_set(lo, mid); else mpz_set(hi, mid);
  }
  if (mpz_sgn(lo) <= 0) die("t not positive");
  /* T_d = floor(lo^d 2^B / 2^{dM}), U_d = ceil(hi^d 2^B / 2^{dM}) */
  mpz_t pl, ph, Ud; mpz_init_set_ui(pl, 1); mpz_init_set_ui(ph, 1); mpz_init(Ud);
  for (int d = 0; d < h + 1 && d < MAXP; d++) {
    mpz_init(TT[L][d]); mpz_init(EE[L][d]);
    if (d == 0) { mpz_set_ui(TT[L][0], 1); mpz_mul_2exp(TT[L][0], TT[L][0], B); mpz_set_ui(EE[L][0], 0); }
    else {
      mpz_mul(pl, pl, lo); mpz_mul(ph, ph, hi);
      long sh = (long)d * M - B;    /* > 0 */
      mpz_fdiv_q_2exp(TT[L][d], pl, sh);
      mpz_cdiv_q_2exp(Ud, ph, sh);
      mpz_sub(EE[L][d], Ud, TT[L][d]);
    }
  }
  if (L == 0) { printf("level 0: B=%d, E_d =", B); for (int d = 0; d < h; d++) gmp_printf(" %Zd", EE[L][d]); printf("\n"); }
  mpz_clear(lo); mpz_clear(hi); mpz_clear(mid); mpz_clear(w); mpz_clear(pl); mpz_clear(ph); mpz_clear(Ud);
  lev_ready[L] = 1;
}

static long n_escal[NLEV];
/* sign of sum_{d<h} q_d t^d */
static int sign_poly(mpz_t *q) {
  int allz = 1; for (int d = 0; d < h; d++) if (mpz_sgn(q[d])) allz = 0;
  if (allz) return 0;
  mpz_t S, E, a; mpz_init(S); mpz_init(E); mpz_init(a);
  for (int L = 0; L < NLEV; L++) {
    make_level(L);
    mpz_set_ui(S, 0); mpz_set_ui(E, 0);
    for (int d = 0; d < h; d++) { mpz_addmul(S, q[d], TT[L][d]); mpz_abs(a, q[d]); mpz_addmul(E, a, EE[L][d]); }
    if (mpz_cmpabs(S, E) > 0) { int s = mpz_sgn(S); n_escal[L]++; mpz_clear(S); mpz_clear(E); mpz_clear(a); return s; }
  }
  die("UNDECIDED sign at maximal precision");
  return 0;
}
/* sign of Im z, z given by p coefficients */
static int sign_im(mpz_t *c) {
  mpz_t w[MAXP], q[MAXP];
  for (int k = 0; k < h; k++) { mpz_init(w[k]); mpz_sub(w[k], c[k + 1], c[p - k - 1]); }
  for (int d = 0; d < h; d++) { mpz_init(q[d]); for (int k = 0; k < h; k++) { long a = Umat[d][k];
      if (a > 0) mpz_addmul_ui(q[d], w[k], a); else if (a < 0) mpz_submul_ui(q[d], w[k], -a); } }
  int s = sign_poly(q);
  int wz = 1; for (int k = 0; k < h; k++) if (mpz_sgn(w[k])) wz = 0;
  if ((s == 0) != wz) die("inconsistent zero test (Im)");
  for (int k = 0; k < h; k++) { mpz_clear(w[k]); mpz_clear(q[k]); }
  return s;
}
/* sign of Re z */
static int sign_re(mpz_t *c) {
  mpz_t v[MAXP + 1], q[MAXP];
  mpz_init_set(v[0], c[0]);
  for (int k = 1; k <= h; k++) { mpz_init(v[k]); mpz_add(v[k], c[k], c[p - k]); }
  for (int d = 0; d < h; d++) { mpz_init(q[d]); for (int k = 0; k <= h; k++) { long a = Vmat[d][k];
      if (a > 0) mpz_addmul_ui(q[d], v[k], a); else if (a < 0) mpz_submul_ui(q[d], v[k], -a); } }
  int s = sign_poly(q);
  /* exact zero iff z + conj z == 0 in Z[zeta] iff v_k == 2 v_0 for all k */
  int ez = 1; mpz_t tw; mpz_init(tw); mpz_mul_ui(tw, v[0], 2);
  for (int k = 1; k <= h; k++) if (mpz_cmp(v[k], tw)) ez = 0;
  if ((s == 0) != ez) die("inconsistent zero test (Re)");
  mpz_clear(tw); for (int k = 0; k <= h; k++) mpz_clear(v[k]); for (int d = 0; d < h; d++) mpz_clear(q[d]);
  return s;
}
/* coefficient vector of conj(a) * b */
static void conj_mul(mpz_t *res, mpz_t *a, mpz_t *b) {
  for (int m = 0; m < p; m++) { mpz_set_ui(res[m], 0); for (int x = 0; x < p; x++) mpz_addmul(res[m], a[x], b[(x + m) % p]); }
}
static int orient_full(int i, int j, int k) {
  mpz_t u[MAXP], v[MAXP], r[MAXP];
  for (int x = 0; x < p; x++) { mpz_init(u[x]); mpz_init(v[x]); mpz_init(r[x]); mpz_sub(u[x], P[j][x], P[i][x]); mpz_sub(v[x], P[k][x], P[i][x]); }
  conj_mul(r, u, v);
  int s = sign_im(r);
  for (int x = 0; x < p; x++) { mpz_clear(u[x]); mpz_clear(v[x]); mpz_clear(r[x]); }
  return s;
}
static int cmp_yx(int a, int b) {  /* sign of (y_a - y_b), then (x_a - x_b) */
  mpz_t d[MAXP]; for (int x = 0; x < p; x++) { mpz_init(d[x]); mpz_sub(d[x], P[a][x], P[b][x]); }
  int s = sign_im(d); if (s == 0) s = sign_re(d);
  for (int x = 0; x < p; x++) mpz_clear(d[x]);
  return s;
}
static mpz_t *R2;   /* R2[layer*p .. ] squared-radius coefficient vectors per layer */
static int cmp_rad(int la, int lb) {
  mpz_t d[MAXP]; for (int x = 0; x < p; x++) { mpz_init(d[x]); mpz_sub(d[x], R2[la * p + x], R2[lb * p + x]); }
  int s = sign_re(d);
  for (int x = 0; x < p; x++) mpz_clear(d[x]);
  return s;
}
static void msort(int *a, int len, int (*cmp)(int, int), int *tmp) {
  if (len < 2) return;
  int m = len / 2; msort(a, m, cmp, tmp); msort(a + m, len - m, cmp, tmp);
  int i = 0, j = m, k = 0;
  while (i < m && j < len) { int c = cmp(a[i], a[j]); if (c == 0) die("tie in sort"); tmp[k++] = (c < 0) ? a[i++] : a[j++]; }
  while (i < m) tmp[k++] = a[i++]; while (j < len) tmp[k++] = a[j++];
  memcpy(a, tmp, sizeof(int) * len);
}
static inline uint64_t c3(uint64_t k) { return k * (k - 1) * (k - 2) / 6; }
static inline uint64_t c2(uint64_t k) { return k * (k - 1) / 2; }

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage: es_orient points.pts outprefix\n"); return 1; }
  FILE *f = fopen(argv[1], "r"); if (!f) die("cannot open points");
  static char line[1 << 20]; int state = 0, row = 0; mpz_t *reps = NULL;
  while (fgets(line, sizeof line, f)) {
    char *s = line; while (*s == ' ' || *s == '\t') s++;
    if (*s == '#' || *s == '\n' || *s == 0) continue;
    if (state == 0) { if (sscanf(s, "%d %d %d", &p, &t, &C) != 3) die("bad header"); state = 1;
      if (p < 3 || p > MAXP || !(p & 1)) die("bad p");
      for (int d = 2; d * d <= p; d++) if (p % d == 0) die("p not prime");
      h = (p - 1) / 2; reps = malloc(sizeof(mpz_t) * t * p); continue; }
    if (row >= t) die("too many rows");
    int col = 0; char *tok = strtok(s, " \t\r\n");
    while (tok) { if (col >= p) die("too many cols"); mpz_init(reps[row * p + col]); if (mpz_set_str(reps[row * p + col], tok, 10)) die("bad integer"); col++; tok = strtok(NULL, " \t\r\n"); }
    if (col != p) die("too few cols");
    row++;
  }
  fclose(f);
  if (row != t) die("wrong number of rows");
  if (C != 0 && C != 1) die("C must be 0/1");
  n = p * t + C;
  printf("p=%d h=%d layers=%d centre=%d n=%d\n", p, h, t, C, n);
  P = malloc(sizeof(mpz_t *) * n);
  for (int i = 0; i < n; i++) { P[i] = malloc(sizeof(mpz_t) * p); for (int x = 0; x < p; x++) mpz_init(P[i][x]); }
  for (int l = 0; l < t; l++) for (int k = 0; k < p; k++) for (int x = 0; x < p; x++)
    mpz_set(P[l * p + k][x], reps[l * p + ((x - k) % p + p) % p]);   /* rep * zeta^k */
  /* magnitude */
  size_t maxbits = 0; for (int l = 0; l < t * p; l++) { size_t b = mpz_sizeinbase(reps[l], 2); if (b > maxbits) maxbits = b; }
  {
    mpz_t mx; mpz_init(mx); for (int l = 0; l < t * p; l++) if (mpz_cmpabs(reps[l], mx) > 0) mpz_abs(mx, reps[l]);
    gmp_printf("max |coefficient| = %Zd (%zu bits)\n", mx, maxbits); mpz_clear(mx);
  }
  setup_polys();
  /* distinct points: canonical form c_x - c_{p-1} */
  {
    long dup = 0; mpz_t a, b; mpz_init(a); mpz_init(b);
    for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) {
      int same = 1;
      for (int x = 0; x < p - 1 && same; x++) { mpz_sub(a, P[i][x], P[i][p - 1]); mpz_sub(b, P[j][x], P[j][p - 1]); if (mpz_cmp(a, b)) same = 0; }
      if (same) dup++;
    }
    printf("duplicate point pairs (exact, canonical basis): %ld\n", dup); mpz_clear(a); mpz_clear(b);
    if (dup) die("duplicate points");
  }
  /* layer radii */
  R2 = malloc(sizeof(mpz_t) * t * p);
  for (int l = 0; l < t; l++) { for (int x = 0; x < p; x++) mpz_init(R2[l * p + x]); conj_mul(R2 + l * p, P[l * p], P[l * p]); }
  int *lord = malloc(sizeof(int) * t), *tmpb = malloc(sizeof(int) * (n + t + 5));
  for (int l = 0; l < t; l++) lord[l] = l;
  msort(lord, t, cmp_rad, tmpb);       /* ascending radius; dies on a tie */
  int *lrank = malloc(sizeof(int) * t); for (int r = 0; r < t; r++) lrank[lord[r]] = r;
  printf("layer radii: all %d pairwise distinct (exact sort, no ties); smallest layer %d, largest layer %d\n", t, lord[0], lord[t - 1]);
  /* also: all p points of a layer have the same squared radius (exact) */
  {
    long bad = 0; mpz_t r[MAXP], d[MAXP]; for (int x = 0; x < p; x++) { mpz_init(r[x]); mpz_init(d[x]); }
    for (int l = 0; l < t; l++) for (int k = 1; k < p; k++) { conj_mul(r, P[l * p + k], P[l * p + k]);
      for (int x = 0; x < p; x++) mpz_sub(d[x], r[x], R2[l * p + x]); if (sign_re(d) != 0) bad++; }
    printf("points with radius different from their layer representative: %ld\n", bad);
    if (C) { int nz = 0; for (int x = 0; x < p; x++) if (mpz_sgn(P[n - 1][x])) nz = 1; printf("centre is the origin: %s\n", nz ? "NO" : "yes"); }
  }
  /* (y,x) order */
  int *yord = malloc(sizeof(int) * n); for (int i = 0; i < n; i++) yord[i] = i;
  msort(yord, n, cmp_yx, tmpb);
  int *yrank = malloc(sizeof(int) * n); for (int r = 0; r < n; r++) yrank[yord[r]] = r;
  printf("(y,x) order computed exactly; lowest point %d, highest %d\n", yord[0], yord[n - 1]);
  /* pair table */
  make_level(0);
  uint64_t npairs = c2(n);
  mpz_t *SP = malloc(sizeof(mpz_t) * npairs);
  mpz_t emax; mpz_init(emax);
  {
    mpz_t r[MAXP], w[MAXP], q[MAXP], e, a; mpz_init(e); mpz_init(a);
    for (int x = 0; x < p; x++) { mpz_init(r[x]); mpz_init(w[x]); mpz_init(q[x]); }
    for (int j = 1; j < n; j++) for (int i = 0; i < j; i++) {
      conj_mul(r, P[i], P[j]);
      for (int k = 0; k < h; k++) mpz_sub(w[k], r[k + 1], r[p - k - 1]);
      for (int d = 0; d < h; d++) { mpz_set_ui(q[d], 0); for (int k = 0; k < h; k++) { long c = Umat[d][k];
          if (c > 0) mpz_addmul_ui(q[d], w[k], c); else if (c < 0) mpz_submul_ui(q[d], w[k], -c); } }
      uint64_t id = c2(j) + i; mpz_init2(SP[id], LEVB[0] + 2 * maxbits + 64);
      mpz_set_ui(SP[id], 0); mpz_set_ui(e, 0);
      for (int d = 0; d < h; d++) { mpz_addmul(SP[id], q[d], TT[0][d]); mpz_abs(a, q[d]); mpz_addmul(e, a, EE[0][d]); }
      if (mpz_cmp(e, emax) > 0) mpz_set(emax, e);
    }
    for (int x = 0; x < p; x++) { mpz_clear(r[x]); mpz_clear(w[x]); mpz_clear(q[x]); }
    mpz_clear(e); mpz_clear(a);
  }
  mpz_t E3; mpz_init(E3); mpz_mul_ui(E3, emax, 3);
  printf("pair table: %llu pairs, max pair error %zu bits, triple threshold 3*emax (%zu bits)\n", (unsigned long long)npairs, mpz_sizeinbase(emax, 2), mpz_sizeinbase(E3, 2));
  fflush(stdout);
  /* all triples */
  uint64_t ntri = c3(n);
  size_t nbytes = (ntri + 7) / 8;
  uint8_t *bits = calloc(nbytes, 1); if (!bits) die("oom bits");
  long nfast = 0, nslow = 0, nzero = 0, npos = 0;
  mpz_t SD; mpz_init2(SD, LEVB[0] + 2 * maxbits + 80);
  size_t minbits = (size_t)-1; mpz_t minabs; mpz_init(minabs); int mi = -1, mj = -1, mk = -1;
  for (int k = 2; k < n; k++) {
    for (int j = 1; j < k; j++) {
      mpz_t *Sjk = &SP[c2(k) + j];
      uint64_t base_ij = c2(j), base_ik = c2(k), tb = c3(k) + c2(j);
      for (int i = 0; i < j; i++) {
        mpz_sub(SD, SP[base_ij + i], SP[base_ik + i]); mpz_add(SD, SD, *Sjk);
        int s;
        if (mpz_cmpabs(SD, E3) > 0) { s = mpz_sgn(SD); nfast++;
          size_t bsz = mpz_sizeinbase(SD, 2);
          if (bsz <= minbits) { if (bsz < minbits || mpz_cmpabs(SD, minabs) < 0) { minbits = bsz; mpz_abs(minabs, SD); mi = i; mj = j; mk = k; } }
        } else { s = orient_full(i, j, k); nslow++; if (s == 0) { nzero++; if (nzero < 20) printf("COLLINEAR triple %d %d %d\n", i, j, k); } }
        if (s > 0) { uint64_t id = tb + i; bits[id >> 3] |= (uint8_t)(1u << (id & 7)); npos++; }
      }
    }
    if (k % 100 == 0) { printf("  k=%d done (fast %ld, slow %ld, zero %ld)\n", k, nfast, nslow, nzero); fflush(stdout); }
  }
  printf("triples: %llu total, decided by pair fast path %ld, full recomputation %ld, zero (collinear) %ld, positive %ld\n",
         (unsigned long long)ntri, nfast, nslow, nzero, npos);
  printf("escalation counts by level (sign_poly calls decided at level L):"); for (int L = 0; L < NLEV; L++) printf(" %ld", n_escal[L]); printf("\n");
  {
    /* min |det| among fast-path triples: |det| = sin(theta) |Q| ~ sin(theta) |S_D| / 2^B (approximate, for info) */
    double v = mpz_get_d(minabs); double det = v / ldexp(1.0, LEVB[0]) * sin(2 * M_PI / p);
    printf("smallest |S_D| among fast-path triples: %zu bits, triple (%d,%d,%d); approx |det| = %.4e (info only)\n", minbits, mi, mj, mk, det);
  }
  /* spot check: fast path vs full recomputation on a deterministic sample */
  {
    long chk = 0, bad = 0; unsigned long long rs = 0x1234567ULL;
    for (int it = 0; it < 200000; it++) {
      rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; int a = rs % n; rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; int b = rs % n; rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; int c = rs % n;
      if (it % 2) { /* same sector, near-degenerate */ int s0 = c % p; a = (a % t) * p + s0; b = (b % t) * p + s0; c = ((c / p) % t) * p + s0; }
      if (a == b || b == c || a == c) continue;
      int x[3] = {a, b, c}; for (int u = 0; u < 3; u++) for (int v = u + 1; v < 3; v++) if (x[v] < x[u]) { int tt = x[u]; x[u] = x[v]; x[v] = tt; }
      uint64_t id = c3(x[2]) + c2(x[1]) + x[0]; int sb = (bits[id >> 3] >> (id & 7)) & 1 ? 1 : -1;
      int sf = orient_full(x[0], x[1], x[2]); chk++; if (sf != sb) bad++;
    }
    printf("spot check fast-path table vs independent full recomputation: %ld triples, %ld mismatches\n", chk, bad);
  }
  /* rotation invariance over ALL triples */
  if (t > 0) {
    long bad = 0;
    int *rot = malloc(sizeof(int) * n); for (int x = 0; x < n; x++) rot[x] = (x < p * t) ? (x / p) * p + (x % p + 1) % p : x;
    for (int k = 2; k < n; k++) for (int j = 1; j < k; j++) for (int i = 0; i < j; i++) {
      uint64_t id = c3(k) + c2(j) + i; int s = (bits[id >> 3] >> (id & 7)) & 1;
      int a = rot[i], b = rot[j], c = rot[k], par = 0;
      if (a > b) { int tt = a; a = b; b = tt; par ^= 1; } if (b > c) { int tt = b; b = c; c = tt; par ^= 1; } if (a > b) { int tt = a; a = b; b = tt; par ^= 1; }
      uint64_t id2 = c3(c) + c2(b) + a; int s2 = (bits[id2 >> 3] >> (id2 & 7)) & 1; if (par) s2 ^= 1;
      if (s != s2) bad++;
    }
    printf("rotation invariance orient(zeta a, zeta b, zeta c) = orient(a,b,c) over all %llu triples: %ld violations\n", (unsigned long long)ntri, bad);
  }
  /* write outputs */
  char fn[4096];
  snprintf(fn, sizeof fn, "%s.signs", argv[2]); FILE *o = fopen(fn, "wb"); fwrite(bits, 1, nbytes, o); fclose(o);
  snprintf(fn, sizeof fn, "%s.meta", argv[2]); o = fopen(fn, "w");
  fprintf(o, "%d %d %d %d\n", p, t, C, n);
  for (int i = 0; i < n; i++) fprintf(o, "%d%c", yrank[i], i == n - 1 ? '\n' : ' ');
  for (int l = 0; l < t; l++) fprintf(o, "%d%c", lrank[l], l == t - 1 ? '\n' : ' ');
  fclose(o);
  printf("wrote %s.signs (%zu bytes) and %s.meta\n", argv[2], nbytes, argv[2]);
  printf("RESULT general_position=%s\n", nzero == 0 ? "yes" : "NO");
  return nzero == 0 ? 0 : 2;
}
