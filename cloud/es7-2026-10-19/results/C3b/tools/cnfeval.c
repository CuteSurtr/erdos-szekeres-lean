/* cnfeval: evaluate a CNF under assignments of its primary variables.
   usage: cnfeval CNF NPRIM NONKGON < assignments
   Each input line: NPRIM integers (+v or -v for v = 1..NPRIM, any order).
   Variables > NPRIM are auxiliary: they get their least model under unit propagation
   (a clause whose literals are all false except one unassigned auxiliary literal forces it;
   all auxiliaries still unassigned at the fixpoint are set false).  Then every clause is
   evaluated.  Output per line: "<falsified clauses with index < NONKGON> <falsified clauses
   with index >= NONKGON> <true auxiliaries>".                                        */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage\n"); return 2; }
  FILE *f = fopen(argv[1], "r"); int nprim = atoi(argv[2]); long nonk = atol(argv[3]);
  char line[1 << 16]; int nv = 0; long nc = 0;
  while (fgets(line, sizeof line, f)) { if (line[0] == 'p') { sscanf(line, "p cnf %d %ld", &nv, &nc); break; } }
  long cap = nc * 6 + 16, nl = 0; int *lits = malloc(sizeof(int) * cap); long *start = malloc(sizeof(long) * (nc + 1));
  long ci = 0; int x; start[0] = 0;
  while (fscanf(f, "%d", &x) == 1) {
    if (nl >= cap) { cap *= 2; lits = realloc(lits, sizeof(int) * cap); }
    if (x == 0) { ci++; start[ci] = nl; } else lits[nl++] = x;
  }
  if (ci != nc) { fprintf(stderr, "clause count %ld vs %ld\n", ci, nc); return 2; }
  signed char *val = malloc(nv + 1);
  int *buf = malloc(sizeof(int) * (nprim + 1));
  while (1) {
    int got = 0;
    for (int i = 0; i < nprim; i++) { if (scanf("%d", &buf[i]) != 1) break; got++; }
    if (got < nprim) break;
    memset(val, 0, nv + 1);
    for (int i = 0; i < nprim; i++) { int l = buf[i], v = abs(l); if (v > nprim) { fprintf(stderr, "bad prim\n"); return 2; } val[v] = l > 0 ? 1 : -1; }
    for (int v = 1; v <= nprim; v++) if (!val[v]) { fprintf(stderr, "prim %d unassigned\n", v); return 2; }
    int changed = 1;
    while (changed) {
      changed = 0;
      for (long c = 0; c < nc; c++) {
        int sat = 0, unk = 0, ul = 0;
        for (long t = start[c]; t < start[c + 1]; t++) {
          int l = lits[t], v = abs(l); int s = val[v] * (l > 0 ? 1 : -1);
          if (s > 0) { sat = 1; break; } if (s == 0) { unk++; ul = l; }
        }
        if (!sat && unk == 1 && ul > 0) { val[ul] = 1; changed = 1; }
      }
    }
    long aux = 0; for (int v = nprim + 1; v <= nv; v++) { if (!val[v]) val[v] = -1; else if (val[v] > 0) aux++; }
    long f1 = 0, f2 = 0;
    for (long c = 0; c < nc; c++) {
      int sat = 0;
      for (long t = start[c]; t < start[c + 1]; t++) { int l = lits[t]; if (val[abs(l)] * (l > 0 ? 1 : -1) > 0) { sat = 1; break; } }
      if (!sat) { if (c < nonk) f1++; else f2++; }
    }
    printf("%ld %ld %ld\n", f1, f2, aux); fflush(stdout);
  }
  return 0;
}
