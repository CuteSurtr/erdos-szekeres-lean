/* Streaming DIMACS clause evaluator, written for this audit.
 *
 * usage: evalcnf CNF OUTPREFIX A1 [A2 ...]
 *   Ai: binary file of V+1 signed bytes, byte v = +1 (variable v true) or -1 (false) for v = 1..V (byte 0 unused).
 * The CNF is read once, in a fixed-size buffer (never loaded whole).  Every clause is evaluated under every
 * assignment.  For assignment i, each violated clause is written to OUTPREFIX.i.viol as
 *   <clause index, 1-based> <literals...> 0
 * Also checked: header present, clause count = header count, every literal in range, no empty clause; counts of
 * clauses with a repeated literal and of tautological clauses are reported.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXA 64
#define MAXLEN 4096
#define VIOL_CAP 3000000L

static FILE *in;
static char buf[1 << 20];
static size_t blen = 0, bpos = 0;

static int getch(void) {
    if (bpos == blen) {
        blen = fread(buf, 1, sizeof buf, in);
        bpos = 0;
        if (blen == 0) return EOF;
    }
    return (unsigned char)buf[bpos++];
}

static void skipline(void) {
    int c;
    while ((c = getch()) != EOF && c != '\n') {}
}

/* reads next integer token; returns 0 on EOF, 1 on success */
static int readint(long *out) {
    int c = getch();
    while (c == ' ' || c == '\n' || c == '\t' || c == '\r') c = getch();
    if (c == EOF) return 0;
    int neg = 0;
    if (c == '-') { neg = 1; c = getch(); }
    if (c < '0' || c > '9') { fprintf(stderr, "unexpected character %d\n", c); exit(3); }
    long v = 0;
    while (c >= '0' && c <= '9') { v = v * 10 + (c - '0'); c = getch(); }
    *out = neg ? -v : v;
    return 1;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: evalcnf CNF OUTPREFIX A1 [A2 ...]\n"); return 2; }
    in = fopen(argv[1], "rb");
    if (!in) { perror(argv[1]); return 2; }
    int na = argc - 3;
    if (na > MAXA) { fprintf(stderr, "too many assignments\n"); return 2; }
    /* header */
    long V = -1, C = -1;
    for (;;) {
        int c = getch();
        if (c == 'c') { skipline(); continue; }
        if (c == 'p') {
            char line[256]; int k = 0; int d;
            while ((d = getch()) != EOF && d != '\n' && k < 255) line[k++] = (char)d;
            line[k] = 0;
            if (sscanf(line, " cnf %ld %ld", &V, &C) != 2) { fprintf(stderr, "bad header\n"); return 2; }
            break;
        }
        fprintf(stderr, "no header\n");
        return 2;
    }
    signed char *A[MAXA];
    for (int i = 0; i < na; i++) {
        A[i] = malloc(V + 1);
        FILE *f = fopen(argv[3 + i], "rb");
        if (!f) { perror(argv[3 + i]); return 2; }
        if ((long)fread(A[i], 1, V + 1, f) != V + 1) { fprintf(stderr, "short assignment %s\n", argv[3 + i]); return 2; }
        fclose(f);
        for (long v = 1; v <= V; v++)
            if (A[i][v] != 1 && A[i][v] != -1) { fprintf(stderr, "assignment %d: variable %ld unset\n", i, v); return 2; }
    }
    FILE *out[MAXA];
    long nviol[MAXA], viol_by_len[MAXA][16];
    memset(viol_by_len, 0, sizeof viol_by_len);
    for (int i = 0; i < na; i++) {
        char name[4096];
        snprintf(name, sizeof name, "%s.%d.viol", argv[2], i);
        out[i] = fopen(name, "w");
        if (!out[i]) { perror(name); return 2; }
        nviol[i] = 0;
    }
    long lits[MAXLEN];
    long len = 0, ncl = 0, ntaut = 0, ndup = 0, lenhist[16] = {0};
    long x;
    unsigned char *mark = calloc(V + 1, 1);
    while (readint(&x)) {
        if (x != 0) {
            if (x > V || -x > V) { fprintf(stderr, "literal %ld out of range in clause %ld\n", x, ncl + 1); return 3; }
            if (len >= MAXLEN) { fprintf(stderr, "clause too long\n"); return 3; }
            lits[len++] = x;
            continue;
        }
        if (len == 0) { fprintf(stderr, "empty clause at %ld\n", ncl + 1); return 3; }
        ncl++;
        lenhist[len < 15 ? len : 15]++;
        /* repeated / complementary literals */
        int taut = 0, dup = 0;
        for (long j = 0; j < len; j++) {
            long v = lits[j] > 0 ? lits[j] : -lits[j];
            unsigned char m = lits[j] > 0 ? 1 : 2;
            if (mark[v] & m) dup = 1;
            if (mark[v] & (3 - m)) taut = 1;
            mark[v] |= m;
        }
        for (long j = 0; j < len; j++) mark[lits[j] > 0 ? lits[j] : -lits[j]] = 0;
        ntaut += taut; ndup += dup;
        for (int i = 0; i < na; i++) {
            int sat = 0;
            for (long j = 0; j < len && !sat; j++) {
                long l = lits[j];
                if (l > 0 ? A[i][l] == 1 : A[i][-l] == -1) sat = 1;
            }
            if (!sat) {
                nviol[i]++;
                viol_by_len[i][len < 15 ? len : 15]++;
                if (nviol[i] <= VIOL_CAP) {
                    fprintf(out[i], "%ld", ncl);
                    for (long j = 0; j < len; j++) fprintf(out[i], " %ld", lits[j]);
                    fprintf(out[i], " 0\n");
                }
            }
        }
        len = 0;
    }
    if (len != 0) { fprintf(stderr, "unterminated last clause\n"); return 3; }
    printf("header vars %ld clauses %ld; read %ld clauses (%s); repeated-literal clauses %ld; tautologies %ld\n",
           V, C, ncl, ncl == C ? "count OK" : "COUNT MISMATCH", ndup, ntaut);
    printf("clause length histogram:");
    for (int k = 1; k < 16; k++) if (lenhist[k]) printf(" %d:%ld", k, lenhist[k]);
    printf("\n");
    for (int i = 0; i < na; i++) {
        printf("assignment %d (%s): violated %ld", i, argv[3 + i], nviol[i]);
        for (int k = 1; k < 16; k++) if (viol_by_len[i][k]) printf(" [len %d: %ld]", k, viol_by_len[i][k]);
        printf("%s\n", nviol[i] > VIOL_CAP ? " (list truncated)" : "");
        fclose(out[i]);
    }
    return ncl == C ? 0 : 4;
}
