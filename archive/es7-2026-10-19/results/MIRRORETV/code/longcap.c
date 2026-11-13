/* longcap.c -- longest cap and longest cup of a point set with distinct abscissae (exact, 128-bit).
 * L[h][i] = longest cap ending with (h,i) = 1 + max{ L[g][h] : g < h, orient(g,h,i) < 0 } (2 if none);
 * same for cups with orient > 0.  O(n^3/6) orientation evaluations; |coordinates| < 2^61 required.
 * Usage: longcap FILE
 */
#include <stdio.h>
#include <stdlib.h>
typedef __int128 i128;
typedef long long ll;
static int cmpx(const void *a, const void *b) {
    const ll *p = a, *q = b;
    return (p[0] > q[0]) - (p[0] < q[0]);
}
int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror(argv[1]); return 2; }
    int cap = 1024, n = 0;
    ll *P = malloc(sizeof(ll) * 2 * cap);
    ll a, b;
    while (fscanf(f, "%lld %lld", &a, &b) == 2) {
        if (a >= (1LL << 61) || a <= -(1LL << 61) || b >= (1LL << 61) || b <= -(1LL << 61)) { printf("too large\n"); return 2; }
        if (n == cap) { cap *= 2; P = realloc(P, sizeof(ll) * 2 * cap); }
        P[2 * n] = a; P[2 * n + 1] = b; n++;
    }
    fclose(f);
    qsort(P, n, 2 * sizeof(ll), cmpx);
    for (int i = 0; i + 1 < n; i++) if (P[2 * i] == P[2 * i + 2]) { printf("abscissae not distinct\n"); return 1; }
    short *LA = malloc(sizeof(short) * (size_t)n * n), *LU = malloc(sizeof(short) * (size_t)n * n);
    int bestA = n >= 2 ? 2 : n, bestU = bestA;
    long long coll = 0;
    for (int i = 0; i < n; i++)
        for (int h = 0; h < i; h++) {
            int mA = 1, mU = 1;
            ll hx = P[2 * h], hy = P[2 * h + 1], ix = P[2 * i], iy = P[2 * i + 1];
            for (int g = 0; g < h; g++) {
                ll gx = P[2 * g], gy = P[2 * g + 1];
                i128 o = (i128)(hx - gx) * (iy - gy) - (i128)(hy - gy) * (ix - gx);
                if (o < 0) { if (LA[(size_t)h * n + g] > mA) mA = LA[(size_t)h * n + g]; }
                else if (o > 0) { if (LU[(size_t)h * n + g] > mU) mU = LU[(size_t)h * n + g]; }
                else coll++;
            }
            LA[(size_t)i * n + h] = mA + 1; LU[(size_t)i * n + h] = mU + 1;
            if (mA + 1 > bestA) bestA = mA + 1;
            if (mU + 1 > bestU) bestU = mU + 1;
        }
    printf("file %s: n = %d, collinear triples %lld, longest cap %d, longest cup %d\n", argv[1], n, coll, bestA, bestU);
    return 0;
}
