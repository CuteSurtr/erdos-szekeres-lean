/* Independent second method: enumerate ALL subsets in convex position by adding points in increasing label
 * order, keeping the polygon in ccw cyclic order.  Q (convex, |Q| >= 3, ccw) plus v is in convex position iff
 * exactly one edge (q_i, q_{i+1}) of Q has v strictly on its right (orient < 0); then v is inserted there.
 * Input: sign file written by verify64.py (first line n, then '+'/'-' for i<j<k in lexicographic order).
 * Output: number of convex k-subsets for k = 3..KMAX.  No geometry, only the exact orientation table.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NMAX 128
#define KMAX 16
static signed char O[NMAX][NMAX][NMAX];
static int n;
static long long cnt[KMAX + 2];

static void rec(int *poly, int k, int maxlab) {
    /* poly: ccw cyclic order of k >= 3 points; try to add v > maxlab */
    int newpoly[KMAX + 2];
    for (int v = maxlab + 1; v < n; v++) {
        int vis = 0, pos = -1;
        for (int i = 0; i < k; i++) {
            int a = poly[i], b = poly[(i + 1) % k];
            if (O[a][b][v] < 0) {
                vis++;
                pos = i;
                if (vis > 1) break;
            }
        }
        if (vis != 1) continue;
        if (k + 1 > KMAX) { fprintf(stderr, "KMAX exceeded\n"); exit(2); }
        /* insert v after position pos */
        int t = 0;
        for (int i = 0; i <= pos; i++) newpoly[t++] = poly[i];
        newpoly[t++] = v;
        for (int i = pos + 1; i < k; i++) newpoly[t++] = poly[i];
        cnt[k + 1]++;
        rec(newpoly, k + 1, v);
    }
}

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "%d", &n) != 1 || n > NMAX) { fprintf(stderr, "bad n\n"); return 1; }
    int c;
    do { c = fgetc(f); } while (c == '\n' || c == '\r' || c == ' ');
    long long read = 0;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            for (int k = j + 1; k < n; k++) {
                if (read > 0) c = fgetc(f);
                read++;
                int s;
                if (c == '+') s = 1; else if (c == '-') s = -1; else { fprintf(stderr, "bad char %d\n", c); return 1; }
                O[i][j][k] = O[j][k][i] = O[k][i][j] = (signed char)s;
                O[j][i][k] = O[i][k][j] = O[k][j][i] = (signed char)(-s);
            }
    fclose(f);
    memset(cnt, 0, sizeof cnt);
    int poly[3];
    for (int a = 0; a < n; a++)
        for (int b = a + 1; b < n; b++)
            for (int v = b + 1; v < n; v++) {
                if (O[a][b][v] > 0) { poly[0] = a; poly[1] = b; poly[2] = v; }
                else { poly[0] = a; poly[1] = v; poly[2] = b; }
                cnt[3]++;
                rec(poly, 3, v);
            }
    printf("n=%d convex k-subsets:", n);
    int mx = 0;
    for (int k = 3; k <= KMAX; k++) { if (cnt[k]) mx = k; }
    for (int k = 3; k <= (mx + 1 < KMAX ? mx + 1 : KMAX); k++) printf(" %d:%lld", k, cnt[k]);
    printf("\nlargest convex subset: %d\n", mx);
    return 0;
}
