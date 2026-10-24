/*
 * hornchk.c -- encoder-independent clause checker for the mirror CNFs (Task Caudit).
 *
 * usage: hornchk <cnf> <nX>  < assignments
 * Each stdin line: "<id> <bits>" with bits a string of nX chars '0'/'1', the value of
 * orientation variables 1..nX.  Variables > nX are auxiliary.
 *
 * Clauses are classified structurally, without knowing how the encoder numbers or means its
 * auxiliaries:
 *   X     -- only orientation variables;
 *   HORN  -- exactly one positive auxiliary literal (an implication with that head);
 *   FORB  -- auxiliary variables present, none positive (a "forbidding" clause);
 *   OTHER -- two or more positive auxiliary literals (reported; the analysis needs none).
 * Given the orientations, the auxiliary part is Horn, so the CNF has a model extending them
 * iff every X clause holds and the least auxiliary model (forward chaining of HORN clauses)
 * satisfies every FORB clause.  Output per line:
 *   <id> xviol=<n> firstx=<clause#> forbviol=<n> firstforb=<clause#> auxtrue=<n>
 * (clause numbers are 1-based positions in the file, -1 if none).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int nv, nc, nX;
static int *cstart, *lits, *kind;  /* 0 X, 1 HORN, 2 FORB, 3 OTHER */
static int *head;                    /* HORN head var */
static int *occs, *ostart;           /* for each aux var: HORN clauses where it is a body literal */

int main(int argc, char **argv) {
  if (argc < 3) { fprintf(stderr, "usage\n"); return 1; }
  FILE *f = fopen(argv[1], "r"); nX = atoi(argv[2]);
  char buf[1 << 16];
  int cap = 1 << 22, n = 0, ci = 0;
  lits = malloc(sizeof(int) * cap);
  while (fgets(buf, sizeof buf, f)) {
    if (buf[0] == 'c') continue;
    if (buf[0] == 'p') { sscanf(buf, "p cnf %d %d", &nv, &nc); cstart = malloc(sizeof(int) * (nc + 1)); continue; }
    char *s = buf; int l, off;
    int any = 0;
    while (sscanf(s, "%d%n", &l, &off) == 1) {
      s += off;
      if (l == 0) { cstart[++ci] = n; any = 0; break; }
      if (!any && ci < nc) { if (n == 0 || cstart[ci] != n) {} any = 1; }
      if (n >= cap) { cap *= 2; lits = realloc(lits, sizeof(int) * cap); }
      lits[n++] = l;
    }
  }
  cstart[0] = 0;
  if (ci != nc) { fprintf(stderr, "clause count %d != header %d\n", ci, nc); return 1; }
  kind = calloc(nc, sizeof(int)); head = calloc(nc, sizeof(int));
  int cnt[4] = {0, 0, 0, 0};
  int *nocc = calloc(nv + 2, sizeof(int));
  for (int c = 0; c < nc; c++) {
    int pa = 0, aa = 0, h = 0;
    for (int t = cstart[c]; t < cstart[c + 1]; t++) {
      int l = lits[t], v = abs(l);
      if (v > nX) { aa++; if (l > 0) { pa++; h = v; } }
    }
    kind[c] = aa == 0 ? 0 : pa == 1 ? 1 : pa == 0 ? 2 : 3;
    head[c] = h; cnt[kind[c]]++;
    if (kind[c] == 1)
      for (int t = cstart[c]; t < cstart[c + 1]; t++) if (lits[t] < -nX) nocc[-lits[t]]++;
  }
  fprintf(stderr, "clauses: X=%d HORN=%d FORB=%d OTHER=%d\n", cnt[0], cnt[1], cnt[2], cnt[3]);
  ostart = calloc(nv + 2, sizeof(int));
  for (int v = 1; v <= nv; v++) ostart[v + 1] = ostart[v] + nocc[v];
  occs = malloc(sizeof(int) * (ostart[nv + 1] + 1));
  int *fill = calloc(nv + 2, sizeof(int));
  for (int c = 0; c < nc; c++) if (kind[c] == 1)
    for (int t = cstart[c]; t < cstart[c + 1]; t++) if (lits[t] < -nX) { int v = -lits[t]; occs[ostart[v] + fill[v]++] = c; }
  char *val = malloc(nv + 2); int *need = malloc(sizeof(int) * nc); int *queue = malloc(sizeof(int) * (nv + 2));
  static char line[1 << 20]; char id[256];
  while (fgets(line, sizeof line, stdin)) {
    char *bits;
    if (sscanf(line, "%255s", id) != 1) continue;
    bits = strchr(line, ' '); if (!bits) continue; bits++;
    if ((int)strspn(bits, "01") != nX) { printf("%s ERROR bad length %d\n", id, (int)strspn(bits, "01")); continue; }
    memset(val, 0, nv + 2);
    for (int v = 1; v <= nX; v++) val[v] = bits[v - 1] == '1';
    int xv = 0, fx = -1, fv = 0, ff = -1, qh = 0, qt = 0, aux = 0;
    for (int c = 0; c < nc; c++) {
      if (kind[c] == 0) {
        int sat = 0;
        for (int t = cstart[c]; t < cstart[c + 1]; t++) { int l = lits[t]; if ((l > 0) == val[abs(l)]) { sat = 1; break; } }
        if (!sat) { xv++; if (fx < 0) fx = c + 1; }
      } else if (kind[c] == 1) {
        int dead = 0, nb = 0;
        for (int t = cstart[c]; t < cstart[c + 1]; t++) {
          int l = lits[t], v = abs(l);
          if (v <= nX) { if ((l > 0) == val[v]) dead = 1; }  /* body condition false: clause satisfied */
          else if (l < 0) nb++;
        }
        need[c] = dead ? -1 : nb;
        if (!dead && nb == 0 && !val[head[c]]) { val[head[c]] = 1; queue[qt++] = head[c]; }
      }
    }
    while (qh < qt) {
      int v = queue[qh++]; aux++;
      for (int o = ostart[v]; o < ostart[v + 1]; o++) {
        int c = occs[o];
        if (need[c] > 0 && --need[c] == 0 && !val[head[c]]) { val[head[c]] = 1; queue[qt++] = head[c]; }
      }
    }
    for (int c = 0; c < nc; c++) if (kind[c] == 2 || kind[c] == 3) {
      int sat = 0;
      for (int t = cstart[c]; t < cstart[c + 1]; t++) { int l = lits[t]; if ((l > 0) == val[abs(l)]) { sat = 1; break; } }
      if (!sat) { fv++; if (ff < 0) ff = c + 1; }
    }
    printf("%s xviol=%d firstx=%d forbviol=%d firstforb=%d auxtrue=%d\n", id, xv, fx, fv, ff, aux);
    fflush(stdout);
  }
  return 0;
}
