/*
 * canon.c -- order-type signature of integer point sets (|c| < 2^30).
 *
 * Same signature as gen.c's canon mode (copied), but with exact __int128
 * orientations and a 2^30 coordinate bound instead of 2^26:
 *   canon  = lexicographically minimal packed bits [orient(L_i,L_j,L_k) > 0],
 *            i<j<k, over labelings L = (hull vertex h, others in ccw angular
 *            order around h);
 *   canonm = min(canon, canon of the mirror image).
 * Input: lines "n x1 y1 ... xn yn".  Output per line: "canon canonm" in hex,
 * or NOT_GENERAL_POSITION.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXN 70
typedef long long ll;
static int N;
static ll X[MAXN], Y[MAXN];
static signed char O[MAXN][MAXN][MAXN];
static unsigned char sigbuf[2][(MAXN * MAXN * MAXN) / 48 + 64];

static int orient3(int a, int b, int c) {
    __int128 v = (__int128)(X[b] - X[a]) * (Y[c] - Y[a]) - (__int128)(Y[b] - Y[a]) * (X[c] - X[a]);
    return (v > 0) - (v < 0);
}
static int nbytes_sig(int n) {
    long t = (long)n * (n - 1) * (n - 2) / 6;
    return (int)((t + 7) / 8);
}
static void canon_sig(int s, unsigned char *out) {
    int nb = nbytes_sig(N);
    static unsigned char cur[(MAXN * MAXN * MAXN) / 48 + 64];
    int have = 0;
    int lab[MAXN];
    for (int h = 0; h < N; h++) {
        int start = -1;
        for (int a = 0; a < N && start < 0; a++) {
            if (a == h) continue;
            int ok = 1;
            for (int b = 0; b < N && ok; b++)
                if (b != h && b != a && s * O[h][a][b] <= 0) ok = 0;
            if (ok) start = a;
        }
        if (start < 0) continue;
        int m = 0;
        for (int b = 0; b < N; b++) if (b != h) lab[1 + m++] = b;
        lab[0] = h;
        for (int i = 2; i < N; i++) {
            int v = lab[i], t = i - 1;
            while (t >= 1 && s * O[h][v][lab[t]] > 0) { lab[t + 1] = lab[t]; t--; }
            lab[t + 1] = v;
        }
        if (lab[1] != start) { fprintf(stderr, "BUG canon start\n"); exit(3); }
        memset(cur, 0, nb);
        long bit = 0;
        for (int i = 0; i < N; i++)
            for (int j = i + 1; j < N; j++)
                for (int k = j + 1; k < N; k++, bit++)
                    if (s * O[lab[i]][lab[j]][lab[k]] > 0) cur[bit >> 3] |= (unsigned char)(0x80 >> (bit & 7));
        if (!have || memcmp(cur, out, nb) < 0) { memcpy(out, cur, nb); have = 1; }
    }
    if (!have) { fprintf(stderr, "BUG no hull vertex\n"); exit(3); }
}
static void put_hex(FILE *f, const unsigned char *b, int nb) {
    static const char *H = "0123456789abcdef";
    for (int i = 0; i < nb; i++) { fputc(H[b[i] >> 4], f); fputc(H[b[i] & 15], f); }
}
int main(void) {
    int n;
    while (scanf("%d", &n) == 1) {
        if (n < 3 || n > MAXN) { fprintf(stderr, "bad n\n"); return 2; }
        N = n;
        for (int i = 0; i < n; i++) if (scanf("%lld %lld", &X[i], &Y[i]) != 2) return 2;
        int gp = 1;
        for (int i = 0; i < n; i++)
            if (X[i] >= (1LL << 30) || X[i] <= -(1LL << 30) || Y[i] >= (1LL << 30) || Y[i] <= -(1LL << 30)) gp = 0;
        for (int i = 0; i < n && gp; i++)
            for (int j = 0; j < n && gp; j++)
                for (int k = 0; k < n; k++) {
                    if (i == j || j == k || i == k) { O[i][j][k] = 0; continue; }
                    O[i][j][k] = (signed char)orient3(i, j, k);
                    if (!O[i][j][k]) { gp = 0; break; }
                }
        if (!gp) { printf("NOT_GENERAL_POSITION\n"); fflush(stdout); continue; }
        int nb = nbytes_sig(N);
        canon_sig(1, sigbuf[0]);
        canon_sig(-1, sigbuf[1]);
        unsigned char *m = memcmp(sigbuf[0], sigbuf[1], nb) <= 0 ? sigbuf[0] : sigbuf[1];
        put_hex(stdout, sigbuf[0], nb); putchar(' '); put_hex(stdout, m, nb); putchar('\n');
        fflush(stdout);
    }
    return 0;
}
