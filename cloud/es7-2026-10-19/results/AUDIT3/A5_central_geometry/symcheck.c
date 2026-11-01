/* Auditor A5: syntactic check that a literal map sigma sends every clause of a CNF into (CNF U EXTRA).
   usage: symcheck CNF SIGMA EXTRA
     SIGMA: binary int32 little-endian, entry v (v = 0..nv) = signed literal sigma(+v) (entry 0 unused).
     EXTRA: text clauses ("l1 ... 0" per line) added to the target set (here: hull clauses of another point).
   Clauses are compared as sorted sets of distinct literals, through a 128-bit hash (two independent 64-bit mixes).
   Prints the number of clauses whose image is missing and the first few of them. Memory: 16 bytes per clause. */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

typedef struct { uint64_t a, b; } H128;
static H128 *tab; static long ntab = 0, cap = 0;
static int32_t *sig; static long nv;
static int lits[4096], nl = 0;

static uint64_t mix(uint64_t x) { x ^= x >> 33; x *= 0xff51afd7ed558ccdULL; x ^= x >> 33; x *= 0xc4ceb9fe1a85ec53ULL; x ^= x >> 33; return x; }
static int cmpint(const void *p, const void *q) { int x = *(const int *)p, y = *(const int *)q; return (x > y) - (x < y); }
static int cmph(const void *p, const void *q) { const H128 *x = p, *y = q; if (x->a != y->a) return x->a < y->a ? -1 : 1; if (x->b != y->b) return x->b < y->b ? -1 : 1; return 0; }

static H128 hclause(int *c, int n) {
  qsort(c, n, sizeof(int), cmpint);
  int m = 0; for (int i = 0; i < n; i++) if (m == 0 || c[m - 1] != c[i]) c[m++] = c[i];
  H128 h = { 0x9e3779b97f4a7c15ULL ^ (uint64_t)m, 0x632be59bd9b4e019ULL + (uint64_t)m };
  for (int i = 0; i < m; i++) {
    uint64_t x = (uint64_t)(int64_t)c[i];
    h.a = mix(h.a ^ mix(x + 0x1234567ULL));
    h.b = mix(h.b + mix(x ^ 0xabcdef987ULL) * 31);
  }
  return h;
}

static int mode; /* 0 = collect, 1 = check */
static long nclauses = 0, nmiss = 0;
static void finish(void) {
  nclauses++;
  if (mode == 0) {
    if (ntab == cap) { cap = cap ? cap * 2 : (1 << 20); tab = realloc(tab, cap * sizeof(H128)); if (!tab) { fprintf(stderr, "oom\n"); exit(2); } }
    tab[ntab++] = hclause(lits, nl);
  } else {
    int img[4096];
    for (int i = 0; i < nl; i++) {
      int l = lits[i]; long v = l > 0 ? l : -l;
      if (v > nv) { fprintf(stderr, "var out of range\n"); exit(2); }
      int s = sig[v]; img[i] = l > 0 ? s : -s;
    }
    int orig[4096]; memcpy(orig, lits, nl * sizeof(int));
    H128 h = hclause(img, nl);
    if (!bsearch(&h, tab, ntab, sizeof(H128), cmph)) {
      nmiss++;
      if (nmiss <= 10) {
        printf("MISSING image of clause %ld:", nclauses);
        for (int i = 0; i < nl; i++) printf(" %d", orig[i]);
        printf("  ->");
        int c2[4096]; for (int i = 0; i < nl; i++) { int l = orig[i]; long v = l > 0 ? l : -l; c2[i] = l > 0 ? sig[v] : -sig[v]; }
        for (int i = 0; i < nl; i++) printf(" %d", c2[i]);
        printf("\n");
      }
    }
  }
  nl = 0;
}

static void process(FILE *fp) {
  static char buf[1 << 24];
  int in_comment = 0, at_line_start = 1, neg = 0, innum = 0; long num = 0; size_t n;
  while ((n = fread(buf, 1, sizeof buf, fp)) > 0) {
    for (size_t i = 0; i < n; i++) {
      char ch = buf[i];
      if (in_comment) { if (ch == '\n') { in_comment = 0; at_line_start = 1; } continue; }
      if (at_line_start && (ch == 'c' || ch == 'p')) { in_comment = 1; continue; }
      if (ch == '-') { neg = 1; innum = 1; num = 0; at_line_start = 0; continue; }
      if (ch >= '0' && ch <= '9') { num = num * 10 + (ch - '0'); innum = 1; at_line_start = 0; continue; }
      if (innum) { long v = neg ? -num : num; if (v == 0) finish(); else lits[nl++] = (int)v; innum = 0; neg = 0; num = 0; }
      if (ch == '\n') at_line_start = 1;
    }
  }
  if (innum) { long v = neg ? -num : num; if (v == 0) finish(); else lits[nl++] = (int)v; }
  if (nl) { fprintf(stderr, "unterminated clause\n"); exit(2); }
}

int main(int argc, char **argv) {
  if (argc < 4) { fprintf(stderr, "usage: symcheck CNF SIGMA EXTRA\n"); return 1; }
  FILE *sf = fopen(argv[2], "rb"); fseek(sf, 0, SEEK_END); long sz = ftell(sf); fseek(sf, 0, SEEK_SET);
  nv = sz / 4 - 1; sig = malloc(sz); if (fread(sig, 1, sz, sf) != (size_t)sz) return 1; fclose(sf);
  mode = 0;
  FILE *fp = fopen(argv[1], "r"); process(fp); fclose(fp);
  long nbase = nclauses;
  FILE *e = fopen(argv[3], "r"); process(e); fclose(e);
  long nextra = nclauses - nbase;
  qsort(tab, ntab, sizeof(H128), cmph);
  mode = 1; nclauses = 0;
  fp = fopen(argv[1], "r"); process(fp); fclose(fp);
  printf("target set: %ld base + %ld extra clauses; checked %ld images; missing %ld\n", nbase, nextra, nclauses, nmiss);
  return nmiss ? 3 : 0;
}
