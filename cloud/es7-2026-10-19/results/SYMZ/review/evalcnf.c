/* evalcnf CNF ASSIGN OUT: ASSIGN = bytes, ASSIGN[v] = 1 (true) / 0 (false) for v = 1..nv (byte 0 unused).
   Streams the CNF, writes every violated clause as "index lit ... 0" to OUT, reports structural anomalies. */
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: evalcnf CNF ASSIGN OUT\n"); return 2; }
    FILE *f = fopen(argv[1], "r"), *a = fopen(argv[2], "rb"), *o = fopen(argv[3], "w");
    if (!f || !a || !o) { fprintf(stderr, "open failed\n"); return 2; }
    fseek(a, 0, SEEK_END); long na = ftell(a); fseek(a, 0, SEEK_SET);
    unsigned char *val = malloc(na);
    if (fread(val, 1, na, a) != (size_t)na) { fprintf(stderr, "read assign failed\n"); return 2; }
    long nv = na - 1, hv = -1, hc = -1, ncl = 0, nviol = 0, nlit = 0, maxvar = 0, empty = 0, zero_not_eol = 0;
    int cap = 1024, len = 0, sat = 0, linestart = 1, c;
    long *cl = malloc(sizeof(long) * cap);
    while ((c = getc_unlocked(f)) != EOF) {
        if (linestart && c == 'c') { while ((c = getc_unlocked(f)) != EOF && c != '\n'); continue; }
        if (linestart && c == 'p') {
            if (fscanf(f, " cnf %ld %ld", &hv, &hc) != 2) { fprintf(stderr, "bad header\n"); return 3; }
            while ((c = getc_unlocked(f)) != EOF && c != '\n');
            continue;
        }
        if (c == '\n') { linestart = 1; continue; }
        if (c == ' ' || c == '\t' || c == '\r') { linestart = 0; continue; }
        linestart = 0;
        int neg = 0;
        if (c == '-') { neg = 1; c = getc_unlocked(f); }
        if (c < '0' || c > '9') { fprintf(stderr, "bad char %d in clause %ld\n", c, ncl); return 3; }
        long x = 0;
        while (c >= '0' && c <= '9') { x = x * 10 + (c - '0'); c = getc_unlocked(f); }
        if (x == 0) {
            if (neg) { fprintf(stderr, "-0 literal\n"); return 3; }
            if (c != '\n' && c != EOF) zero_not_eol++;
            if (len == 0) empty++;
            if (!sat) {
                nviol++;
                fprintf(o, "%ld", ncl);
                for (int i = 0; i < len; i++) fprintf(o, " %ld", cl[i]);
                fprintf(o, " 0\n");
            }
            ncl++; len = 0; sat = 0;
            if (c == '\n') linestart = 1;
            continue;
        }
        if (c != EOF) ungetc(c, f);
        if (x > nv) { fprintf(stderr, "var %ld > assignment size %ld\n", x, nv); return 3; }
        if (x > maxvar) maxvar = x;
        if (len == cap) { cap *= 2; cl = realloc(cl, sizeof(long) * cap); }
        cl[len++] = neg ? -x : x;
        nlit++;
        if ((val[x] == 1) != neg) sat = 1;
    }
    if (len) fprintf(stderr, "trailing literals without terminator\n");
    printf("header_vars=%ld header_clauses=%ld parsed_clauses=%ld lits=%ld maxvar=%ld empty=%ld zero_not_eol=%ld violated=%ld\n",
           hv, hc, ncl, nlit, maxvar, empty, zero_not_eol, nviol);
    fclose(o);
    return 0;
}
