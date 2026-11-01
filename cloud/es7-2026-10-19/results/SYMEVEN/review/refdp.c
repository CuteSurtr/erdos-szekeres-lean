/* Referee's C port of rg.py's DPs, driven by an exact orientation-sign table computed in Python.
   Input (binary, little endian): int32 N; int32 yrank[N] (rank of each point in (y,x) lexicographic order);
   int8 sign[N][N][N] for points sorted by x (sign of orient(P_i,P_j,P_l)).
   Output: largest convex subset by (1) cup+cap DP and (2) angular DP around the lowest vertex, and
   (3) number of convex subsets of each size (cup x cap counting DP). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

static int N;
static int8_t *S;
static int *yr;
#define SG(i,j,l) S[((size_t)(i)*N + (j))*N + (l)]

static int max_cupcap(void) {
    int best = N < 2 ? N : 2;
    int *cup = malloc(sizeof(int) * N * N), *cap = malloc(sizeof(int) * N * N);
    for (int a = 0; a < N; a++) {
        memset(cup, 0, sizeof(int) * N * N); memset(cap, 0, sizeof(int) * N * N);
        for (int j = a + 1; j < N; j++) { cup[a * N + j] = 2; cap[a * N + j] = 2; }
        for (int i = a + 1; i < N; i++)
            for (int j = i + 1; j < N; j++) {
                int bc = 0, bk = 0;
                for (int h = a; h < i; h++) {
                    int s = SG(h, i, j);
                    int v = cup[h * N + i];
                    if (v && s > 0 && v + 1 > bc) bc = v + 1;
                    v = cap[h * N + i];
                    if (v && s < 0 && v + 1 > bk) bk = v + 1;
                }
                cup[i * N + j] = bc; cap[i * N + j] = bk;
            }
        for (int b = a + 1; b < N; b++) {
            int lc = 0, lk = 0;
            for (int i = a; i < b; i++) {
                if (cup[i * N + b] > lc) lc = cup[i * N + b];
                if (cap[i * N + b] > lk) lk = cap[i * N + b];
            }
            if (lc + lk - 2 > best) best = lc + lk - 2;
        }
    }
    free(cup); free(cap);
    return best;
}

static int g_p;
static int cmp_ang(const void *x, const void *y) {
    int q1 = *(const int *)x, q2 = *(const int *)y;
    int s = SG(g_p, q1, q2);          /* q1 before q2 iff orient(p,q1,q2) > 0 */
    return -s;
}

static int max_angular(void) {
    int best = N < 2 ? N : 2;
    int *above = malloc(sizeof(int) * N);
    int *f = malloc(sizeof(int) * N * N);
    for (int p = 0; p < N; p++) {
        int m = 0;
        for (int q = 0; q < N; q++) if (yr[q] > yr[p]) above[m++] = q;
        if (m < 2) continue;
        g_p = p;
        qsort(above, m, sizeof(int), cmp_ang);
        for (int i = 0; i < m; i++) for (int j = 0; j < m; j++) f[i * m + j] = (i < j) ? 3 : 0;
        for (int j = 0; j < m; j++)
            for (int i = 0; i < j; i++) {
                int fij = f[i * m + j];
                for (int l = j + 1; l < m; l++)
                    if (fij + 1 > f[j * m + l] && SG(above[i], above[j], above[l]) > 0) f[j * m + l] = fij + 1;
            }
        for (int i = 0; i < m * m; i++) if (f[i] > best) best = f[i];
    }
    free(above); free(f);
    return best;
}

#define ML 24
static void count_cupcap(uint64_t *tot) {
    uint64_t *cup = malloc(sizeof(uint64_t) * N * N * ML), *cap = malloc(sizeof(uint64_t) * N * N * ML);
    uint64_t CU[ML], CA[ML];
    for (int a = 0; a < N; a++) {
        memset(cup, 0, sizeof(uint64_t) * N * N * ML); memset(cap, 0, sizeof(uint64_t) * N * N * ML);
        for (int j = a + 1; j < N; j++) { cup[((size_t)a * N + j) * ML + 2] = 1; cap[((size_t)a * N + j) * ML + 2] = 1; }
        for (int i = a + 1; i < N; i++)
            for (int j = i + 1; j < N; j++) {
                uint64_t *dc = cup + ((size_t)i * N + j) * ML, *dk = cap + ((size_t)i * N + j) * ML;
                for (int h = a; h < i; h++) {
                    int s = SG(h, i, j);
                    if (s > 0) { uint64_t *src = cup + ((size_t)h * N + i) * ML; for (int L = 2; L < ML - 1; L++) dc[L + 1] += src[L]; }
                    else if (s < 0) { uint64_t *src = cap + ((size_t)h * N + i) * ML; for (int L = 2; L < ML - 1; L++) dk[L + 1] += src[L]; }
                }
            }
        for (int b = a + 1; b < N; b++) {
            memset(CU, 0, sizeof CU); memset(CA, 0, sizeof CA);
            for (int i = a; i < b; i++)
                for (int L = 2; L < ML; L++) { CU[L] += cup[((size_t)i * N + b) * ML + L]; CA[L] += cap[((size_t)i * N + b) * ML + L]; }
            for (int L1 = 2; L1 < ML; L1++) if (CU[L1])
                for (int L2 = 2; L2 < ML; L2++) if (CA[L2]) {
                    int s = L1 + L2 - 2;
                    if (s >= 3 && s < 2 * ML) tot[s] += CU[L1] * CA[L2];
                }
        }
    }
    free(cup); free(cap);
}

int main(int argc, char **argv) {
    FILE *fp = fopen(argv[1], "rb");
    if (!fp) { perror("open"); return 1; }
    int32_t n32; if (fread(&n32, 4, 1, fp) != 1) return 1; N = n32;
    yr = malloc(sizeof(int) * N);
    for (int i = 0; i < N; i++) { int32_t v; if (fread(&v, 4, 1, fp) != 1) return 1; yr[i] = v; }
    S = malloc((size_t)N * N * N);
    if (fread(S, 1, (size_t)N * N * N, fp) != (size_t)N * N * N) return 1;
    fclose(fp);
    int doc = argc > 2 && atoi(argv[2]);
    printf("N=%d max_cupcap=%d max_angular=%d", N, max_cupcap(), max_angular());
    if (doc) {
        uint64_t tot[2 * ML]; memset(tot, 0, sizeof tot);
        count_cupcap(tot);
        printf(" counts:");
        for (int s = 3; s < 2 * ML; s++) if (tot[s]) printf(" %d:%llu", s, (unsigned long long)tot[s]);
    }
    printf("\n");
    return 0;
}
