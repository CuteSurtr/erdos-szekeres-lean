/* enumk.c -- list all convex K-gons (float coordinates, long double signs); evidence/diagnostics only.
   int enum_k(int n, const double *x, const double *y, int K, int *out, int maxout)
   writes up to maxout polygons (K indices each, ccw from the lowest vertex) and returns the total number found. */
#include <stdlib.h>
#include <string.h>
#define NMAX 64
static signed char O[NMAX * NMAX * NMAX];
static int n_, K_, ord_[NMAX], u_, a_, chain_[16], *out_, maxout_; static long found_;
static int orient_ld(long double ax, long double ay, long double bx, long double by, long double cx, long double cy) {
  long double d = (bx - ax) * (cy - ay) - (by - ay) * (cx - ax); return d > 0 ? 1 : (d < 0 ? -1 : 0); }
#define OR(a,b,c) O[((a) * n_ + (b)) * n_ + (c)]
static void dfs(int len, int lasti) {
  /* chain_[0] = a, chain_[1..len-1] = ord indices (as point ids) */
  if (len == K_) {
    if (OR(chain_[len - 2], chain_[len - 1], a_) > 0 && OR(chain_[len - 1], a_, chain_[1]) > 0) {
      if (found_ < maxout_) memcpy(out_ + found_ * K_, chain_, sizeof(int) * K_);
      found_++;
    }
    return;
  }
  for (int j = lasti + 1; j < u_; j++) {
    int q = ord_[j];
    if (len >= 2 && OR(chain_[len - 2], chain_[len - 1], q) <= 0) continue;
    chain_[len] = q; dfs(len + 1, j);
  }
}
int enum_k(int n, const double *x, const double *y, int K, int *out, int maxout) {
  n_ = n; K_ = K; out_ = out; maxout_ = maxout; found_ = 0;
  for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) for (int c = 0; c < n; c++)
    OR(a, b, c) = (a == b || b == c || a == c) ? 0 : orient_ld(x[a], y[a], x[b], y[b], x[c], y[c]);
  for (int a = 0; a < n; a++) {
    u_ = 0;
    for (int c = 0; c < n; c++) if (y[c] > y[a] || (y[c] == y[a] && x[c] > x[a])) ord_[u_++] = c;
    for (int i = 1; i < u_; i++) { int v = ord_[i], j = i - 1; while (j >= 0 && OR(a, ord_[j], v) < 0) { ord_[j + 1] = ord_[j]; j--; } ord_[j + 1] = v; }
    a_ = a; chain_[0] = a; dfs(1, -1);
  }
  return (int)found_;
}
