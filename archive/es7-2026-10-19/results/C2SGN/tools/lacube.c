/* lacube: a small lookahead cuber. Builds a binary decision tree over variables 1..NCAND of a CNF. At each node every
   free candidate is tried both ways with unit propagation; a literal whose opposite fails is added to the node (it is
   implied); the branching variable maximises nT*nF + nT + nF (implied assignments). Leaves at depth DEPTH, and nodes
   refuted by the lookahead, are printed as cubes "a lits 0", so the leaves cover the formula.
   usage: lacube CNF NCAND DEPTH [PREFIX_CUBE_LITS...] > cubes */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int nv, nc, *lits, *cst, *cln, **w, *wn, *wc, *trail, tn, qh, ncand, dmax, cube[4096], cn;
static signed char *val;
static long nodes, leaves, refuted;
#define LI(l) ((l) > 0 ? 2 * (l) : 2 * (-(l)) + 1)
static inline int value(int l) { int v = val[abs(l)]; return l > 0 ? v : -v; }
static void watch(int l, int c) { int i = LI(l); if (wn[i] == wc[i]) { wc[i] = wc[i] ? 2 * wc[i] : 4; w[i] = realloc(w[i], wc[i] * sizeof(int)); } w[i][wn[i]++] = c; }
static void assign(int l) { val[abs(l)] = l > 0 ? 1 : -1; trail[tn++] = l; }
static void back(int to) { while (tn > to) val[abs(trail[--tn])] = 0; qh = tn; }
static int prop(void) {
  while (qh < tn) {
    int fl = -trail[qh++], i = LI(fl), *ws = w[i], n = wn[i], j = 0, k;
    for (k = 0; k < n; k++) {
      int c = ws[k], *cl = lits + cst[c], len = cln[c];
      if (cl[0] == fl) { cl[0] = cl[1]; cl[1] = fl; }
      if (value(cl[0]) == 1) { ws[j++] = c; continue; }
      int moved = 0;
      for (int m = 2; m < len; m++) if (value(cl[m]) != -1) { int t = cl[1]; cl[1] = cl[m]; cl[m] = t; watch(cl[1], c); moved = 1; break; }
      if (moved) continue;
      ws[j++] = c;
      if (value(cl[0]) == -1) { for (k++; k < n; k++) ws[j++] = ws[k]; wn[i] = j; return 0; }
      assign(cl[0]);
    }
    wn[i] = j;
  }
  return 1;
}
static void emit(void) { printf("a"); for (int i = 0; i < cn; i++) printf(" %d", cube[i]); printf(" 0\n"); leaves++; }
static void node(int depth) {
  int base = tn, cn0 = cn, best, v; double bs;
  nodes++;
again:
  best = 0; bs = -1;
  for (v = 1; v <= ncand; v++) {
    if (val[v]) continue;
    int t0 = tn, okT, okF, nT, nF;
    assign(v); okT = prop(); nT = tn - t0; back(t0);
    assign(-v); okF = prop(); nF = tn - t0; back(t0);
    if (!okT && !okF) { emit(); refuted++; cn = cn0; back(base); return; }
    if (!okT || !okF) { int l = okT ? v : -v; cube[cn++] = l; assign(l); if (!prop()) { emit(); refuted++; cn = cn0; back(base); return; } goto again; }
    double s = (double)nT * nF + nT + nF;
    if (s > bs) { bs = s; best = v; }
  }
  if (depth >= dmax || !best) { emit(); cn = cn0; back(base); return; }
  for (int pol = 1; pol >= -1; pol -= 2) {
    int t0 = tn, l = pol * best;
    cube[cn++] = l; assign(l);
    if (prop()) node(depth + 1); else { emit(); refuted++; }
    cn--; back(t0);
  }
  cn = cn0; back(base);
}
int main(int argc, char **argv) {
  FILE *f = fopen(argv[1], "r"); ncand = atoi(argv[2]); dmax = atoi(argv[3]);
  char buf[1 << 16]; int cap = 1 << 24, n = 0, x, c = 0; lits = malloc(cap * sizeof(int));
  while (fgets(buf, sizeof buf, f)) { if (buf[0] == 'p') { sscanf(buf, "p cnf %d %d", &nv, &nc); break; } }
  cst = malloc((nc + 1) * sizeof(int)); cln = calloc(nc + 1, sizeof(int)); cst[0] = 0;
  while (fscanf(f, "%d", &x) == 1) { if (n == cap) { cap *= 2; lits = realloc(lits, cap * sizeof(int)); } if (x) { lits[n++] = x; cln[c]++; } else { c++; cst[c] = n; } }
  fclose(f);
  val = calloc(nv + 1, 1); trail = malloc((nv + 1) * sizeof(int)); w = calloc(2 * nv + 2, sizeof(int *)); wn = calloc(2 * nv + 2, sizeof(int)); wc = calloc(2 * nv + 2, sizeof(int));
  int units[1 << 16], nu = 0;
  for (int i = 0; i < c; i++) { if (cln[i] == 1) units[nu++] = lits[cst[i]]; else { watch(lits[cst[i]], i); watch(lits[cst[i] + 1], i); } }
  for (int i = 0; i < nu; i++) { if (value(units[i]) == -1) { fprintf(stderr, "root conflict\n"); return 20; } if (!value(units[i])) assign(units[i]); }
  for (int i = 4; i < argc; i++) { int l = atoi(argv[i]); cube[cn++] = l; if (value(l) == -1) { emit(); return 0; } if (!value(l)) assign(l); }
  if (!prop()) { fprintf(stderr, "root/prefix refuted by propagation\n"); emit(); return 0; }
  fprintf(stderr, "clauses %d vars %d root assigned %d\n", c, nv, tn);
  node(0);
  fprintf(stderr, "nodes %ld leaves %ld refuted %ld\n", nodes, leaves, refuted);
  return 0;
}
