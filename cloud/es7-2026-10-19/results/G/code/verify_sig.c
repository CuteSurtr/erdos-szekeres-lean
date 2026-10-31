/* Brute-force checker for an abstract signotope given as a SAT model / literal list.
 * usage: verify_sig N K file
 * file: whitespace-separated signed integers (a DIMACS model with or without "v"/"s" lines is
 * fine; tokens that are not integers are skipped). Variable X(i,j,k), i<j<k, is number
 * 1..C(N,3) in lexicographic order; positive = counterclockwise.
 * Prints one JSON line:
 *   axiom_violations : quadruples i<j<k<l whose sign sequence (ijk,ijl,ikl,jkl) changes twice
 *   hull_frame_ok    : X(1,i,j) = + for all 1<i<j
 *   convex_K         : number of K-subsets in convex position (no point inside a triangle of
 *                      three others; orientation extended to all ordered triples by parity)
 *   hull_size        : number of points not inside any triangle of other points
 * Independent of the CNF encoding (does not use caps/cups). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int N, K;
static signed char S[64][64][64];
static unsigned char conv4[64][64][64][64];

static int inside(int d, int a, int b, int c) {
    int o = S[a][b][d];
    return o == S[b][c][d] && o == S[c][a][d];
}

int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage: verify_sig N K file\n"); return 2; }
    N = atoi(argv[1]); K = atoi(argv[2]);
    if (N < 4 || N > 63 || K < 4 || K > 16) { fprintf(stderr, "bad N/K\n"); return 2; }
    long nX = (long)N * (N - 1) * (N - 2) / 6;
    signed char *val = calloc(nX + 1, 1);
    FILE *f = fopen(argv[3], "r");
    if (!f) { perror("open"); return 2; }
    char tok[256];
    while (fscanf(f, "%255s", tok) == 1) {
        char *end; long x = strtol(tok, &end, 10);
        if (*end || end == tok || x == 0) continue;
        long v = labs(x);
        if (v <= nX) val[v] = x > 0 ? 1 : -1;
    }
    fclose(f);
    long idx = 0;
    for (int i = 1; i <= N; i++) for (int j = i + 1; j <= N; j++) for (int k = j + 1; k <= N; k++) {
        int s = val[++idx];
        if (s == 0) { fprintf(stderr, "missing value for var %ld\n", idx); return 2; }
        S[i][j][k] = s; S[j][k][i] = s; S[k][i][j] = s;
        S[j][i][k] = -s; S[i][k][j] = -s; S[k][j][i] = -s;
    }
    long badq = 0;
    for (int a = 1; a <= N; a++) for (int b = a + 1; b <= N; b++) for (int c = b + 1; c <= N; c++) for (int d = c + 1; d <= N; d++) {
        int q[4] = {S[a][b][c], S[a][b][d], S[a][c][d], S[b][c][d]};
        int ch = (q[0] != q[1]) + (q[1] != q[2]) + (q[2] != q[3]);
        if (ch > 1) badq++;
        conv4[a][b][c][d] = !(inside(a, b, c, d) || inside(b, a, c, d) || inside(c, a, b, d) || inside(d, a, b, c));
    }
    int frame = 1;
    for (int i = 2; i <= N; i++) for (int j = i + 1; j <= N; j++) if (S[1][i][j] != 1) frame = 0;
    /* hull */
    int hull = 0; char ext[64]; memset(ext, 0, sizeof ext);
    for (int d = 1; d <= N; d++) {
        int in = 0;
        for (int a = 1; a <= N && !in; a++) if (a != d) for (int b = a + 1; b <= N && !in; b++) if (b != d)
            for (int c = b + 1; c <= N && !in; c++) if (c != d) if (inside(d, a, b, c)) in = 1;
        if (!in) { hull++; ext[d] = 1; }
    }
    /* convex K-subsets */
    int id[20]; long long convex = 0; int first[20]; int have_first = 0;
    for (int t = 0; t < K; t++) id[t] = t + 1;
    while (1) {
        int ok = 1;
        for (int p = 0; p < K && ok; p++) for (int q = p + 1; q < K && ok; q++) for (int r = q + 1; r < K && ok; r++) for (int u = r + 1; u < K && ok; u++)
            if (!conv4[id[p]][id[q]][id[r]][id[u]]) ok = 0;
        if (ok) { convex++; if (!have_first) { have_first = 1; memcpy(first, id, sizeof id); } }
        int t = K - 1;
        while (t >= 0 && id[t] == N - K + 1 + t) t--;
        if (t < 0) break;
        id[t]++;
        for (int u = t + 1; u < K; u++) id[u] = id[u - 1] + 1;
    }
    printf("{\"N\": %d, \"K\": %d, \"axiom_violations\": %ld, \"hull_frame_ok\": %s, \"convex_K\": %lld, \"hull_size\": %d, \"extreme\": [",
           N, K, badq, frame ? "true" : "false", convex, hull);
    int firstp = 1;
    for (int d = 1; d <= N; d++) if (ext[d]) { printf(firstp ? "%d" : ", %d", d); firstp = 0; }
    printf("]");
    if (have_first) { printf(", \"first_convex\": ["); for (int t = 0; t < K; t++) printf(t ? ", %d" : "%d", first[t]); printf("]"); }
    printf("}\n");
    return 0;
}
