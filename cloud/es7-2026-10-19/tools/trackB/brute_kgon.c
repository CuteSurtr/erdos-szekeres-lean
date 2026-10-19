/* Method C: brute force over ALL K-subsets of a signotope (no pruning).
 * Input file: lines "i j k s" (1<=i<j<k<=N, s=+1/-1), as written by sigcheck.py (*.sig).
 * A K-subset is in convex position iff none of its points lies inside a triangle of three
 * others (d inside abc iff O(a,b,d)=O(b,c,d)=O(c,a,d), O extended by permutation parity).
 * Also re-checks the signotope axiom on every quadruple.
 * usage: brute_kgon N K file.sig */
#include <stdio.h>
#include <stdlib.h>

static int N, K;
static signed char S[64][64][64]; /* orientation for every ordered distinct triple */

static int inside(int d, int a, int b, int c) {
    int o = S[a][b][d];
    return o == S[b][c][d] && o == S[c][a][d];
}

int main(int argc, char **argv) {
    if (argc != 4) { fprintf(stderr, "usage\n"); return 2; }
    N = atoi(argv[1]); K = atoi(argv[2]);
    FILE *f = fopen(argv[3], "r");
    int i, j, k, s, cnt = 0;
    while (fscanf(f, "%d %d %d %d", &i, &j, &k, &s) == 4) {
        if (!(1 <= i && i < j && j < k && k <= N) || (s != 1 && s != -1)) { fprintf(stderr, "bad line\n"); return 2; }
        S[i][j][k] = s; S[j][k][i] = s; S[k][i][j] = s;
        S[j][i][k] = -s; S[i][k][j] = -s; S[k][j][i] = -s;
        cnt++;
    }
    long expect = (long)N * (N - 1) * (N - 2) / 6;
    if (cnt != expect) { fprintf(stderr, "expected %ld triples, got %d\n", expect, cnt); return 2; }
    /* signotope axiom */
    long badq = 0;
    for (int a = 1; a <= N; a++) for (int b = a + 1; b <= N; b++) for (int c = b + 1; c <= N; c++) for (int d = c + 1; d <= N; d++) {
        int q[4] = {S[a][b][c], S[a][b][d], S[a][c][d], S[b][c][d]};
        int ch = (q[0] != q[1]) + (q[1] != q[2]) + (q[2] != q[3]);
        if (ch > 1) badq++;
    }
    /* convex 4-subsets table: conv4[a][b][c][d] for a<b<c<d */
    static unsigned char conv4[64][64][64][64];
    for (int a = 1; a <= N; a++) for (int b = a + 1; b <= N; b++) for (int c = b + 1; c <= N; c++) for (int d = c + 1; d <= N; d++) {
        int ok = !(inside(a, b, c, d) || inside(b, a, c, d) || inside(c, a, b, d) || inside(d, a, b, c));
        conv4[a][b][c][d] = ok;
    }
    /* enumerate all K-subsets */
    int idx[16];
    long long total = 0, convex = 0;
    for (int t = 0; t < K; t++) idx[t] = t + 1;
    long long first_print = 0;
    while (1) {
        total++;
        int ok = 1;
        for (int p = 0; p < K && ok; p++) for (int q = p + 1; q < K && ok; q++) for (int r = q + 1; r < K && ok; r++) for (int u = r + 1; u < K && ok; u++)
            if (!conv4[idx[p]][idx[q]][idx[r]][idx[u]]) ok = 0;
        if (ok) {
            convex++;
            if (first_print < 5) { first_print++; printf("convex subset:"); for (int t = 0; t < K; t++) printf(" %d", idx[t]); printf("\n"); }
        }
        int t = K - 1;
        while (t >= 0 && idx[t] == N - K + 1 + t) t--;
        if (t < 0) break;
        idx[t]++;
        for (int u = t + 1; u < K; u++) idx[u] = idx[u - 1] + 1;
    }
    printf("N=%d K=%d signotope_violations=%ld K-subsets=%lld convex_K_subsets=%lld\n", N, K, badq, total, convex);
    return 0;
}
