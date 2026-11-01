/* Auditor A5: stream a DIMACS CNF and evaluate up to 64 assignments in parallel.
   usage: evalcnf CNF MASKS L OUT [EXTRA]
     MASKS: binary, (nv+1) little-endian uint64; bit j of entry v = value of variable v in assignment j.
     L: number of assignments (1..64).
     OUT: text file; one line per falsified clause: "<clause index (1-based)> <hex mask of falsifying assignments> lits..."
     EXTRA (optional): a second text file of extra clauses ("l1 l2 ... 0" per line), evaluated after the CNF
                       (their indices continue the numbering).
   Prints per-assignment falsified counts. Reads the CNF in 16 MB chunks (constant memory). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

static uint64_t *mask; static long nv_file;
static long nclauses = 0, nfals_lines = 0;
static long cnt[64];
static uint64_t ALL;
static FILE *out;
static int lits[4096]; static int nl = 0;

static void finish_clause(void) {
  uint64_t m = 0;
  for (int i = 0; i < nl; i++) {
    int l = lits[i]; long v = l > 0 ? l : -l;
    if (v > nv_file) { fprintf(stderr, "variable %ld out of range\n", v); exit(2); }
    m |= (l > 0) ? mask[v] : ~mask[v];
  }
  nclauses++;
  uint64_t f = ALL & ~m;
  if (f) {
    for (int j = 0; j < 64; j++) if (f >> j & 1) cnt[j]++;
    fprintf(out, "%ld %llx", nclauses, (unsigned long long)f);
    for (int i = 0; i < nl; i++) fprintf(out, " %d", lits[i]);
    fprintf(out, "\n");
    nfals_lines++;
  }
  nl = 0;
}

static void process(FILE *fp) {
  static char buf[1 << 24];
  int in_comment = 0, at_line_start = 1, neg = 0, innum = 0; long num = 0;
  size_t n;
  while ((n = fread(buf, 1, sizeof buf, fp)) > 0) {
    for (size_t i = 0; i < n; i++) {
      char ch = buf[i];
      if (in_comment) { if (ch == '\n') { in_comment = 0; at_line_start = 1; } continue; }
      if (at_line_start && (ch == 'c' || ch == 'p')) { in_comment = 1; continue; }
      if (ch == '-') { neg = 1; innum = 1; num = 0; at_line_start = 0; continue; }
      if (ch >= '0' && ch <= '9') { num = num * 10 + (ch - '0'); innum = 1; at_line_start = 0; continue; }
      if (innum) {
        long v = neg ? -num : num;
        if (v == 0) finish_clause(); else { if (nl >= 4096) { fprintf(stderr, "clause too long\n"); exit(2); } lits[nl++] = (int)v; }
        innum = 0; neg = 0; num = 0;
      }
      if (ch == '\n') at_line_start = 1;
    }
  }
  if (innum) { long v = neg ? -num : num; if (v == 0) finish_clause(); else lits[nl++] = (int)v; }
  if (nl) { fprintf(stderr, "unterminated clause\n"); exit(2); }
}

int main(int argc, char **argv) {
  if (argc < 5) { fprintf(stderr, "usage: evalcnf CNF MASKS L OUT [EXTRA]\n"); return 1; }
  FILE *mf = fopen(argv[2], "rb"); if (!mf) { perror("masks"); return 1; }
  fseek(mf, 0, SEEK_END); long sz = ftell(mf); fseek(mf, 0, SEEK_SET);
  nv_file = sz / 8 - 1;
  mask = malloc(sz); if (fread(mask, 1, sz, mf) != (size_t)sz) { fprintf(stderr, "short read\n"); return 1; } fclose(mf);
  int L = atoi(argv[3]); ALL = (L == 64) ? ~0ULL : ((1ULL << L) - 1);
  out = fopen(argv[4], "w");
  FILE *fp = fopen(argv[1], "r"); if (!fp) { perror("cnf"); return 1; }
  process(fp); fclose(fp);
  long base_clauses = nclauses;
  if (argc > 5) { FILE *e = fopen(argv[5], "r"); if (!e) { perror("extra"); return 1; } process(e); fclose(e); }
  fclose(out);
  printf("clauses %ld (cnf %ld, extra %ld); falsified-clause lines %ld\n", nclauses, base_clauses, nclauses - base_clauses, nfals_lines);
  for (int j = 0; j < L; j++) printf("assignment %d falsified %ld\n", j, cnt[j]);
  return 0;
}
