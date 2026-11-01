/* Order-type invariants from an exact orientation table (2026-11-01).
 *
 * Input: file written by orient.py: "OT1 n\n" then n^3 signed bytes T[i][j][k] (+1 ccw, -1 cw).
 * Output (stdout, key=value lines):
 *   convex[j]   number of j-subsets in convex position, all j (DFS over increasing index; incremental hull)
 *   holes[j]    number of empty convex j-gons (no point of the set inside the hull)
 *   tri_in[j]   number of triangles with exactly j points of the set inside
 *   jedge[j]    number of unordered pairs whose line has j points on one side and n-2-j on the other (j <= (n-2)/2)
 *   layers      sizes of the convex layers (onion peeling)
 *   canon       lexicographically least triple-sign string over all labelings "extreme point p first, the others
 *               in angular order around p" for both orientations (the order type up to reflection);
 *               written to FILE.canon; aut_plus = number of orientation-preserving automorphisms;
 *               mirror = 1 iff an orientation-reversing automorphism exists.
 * Only orientation signs are used (coordinate-free).
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int n;
static signed char *T;
#define O(a,b,c) T[((a)*n+(b))*n+(c)]

static long long convex_cnt[80], hole_cnt[80];
static unsigned char *empty3; /* empty3[(a*n+b)*n+c] = 1 iff triangle abc has no point inside */
#define E3(a,b,c) empty3[((a)*n+(b))*n+(c)]

static int poly[80], plen;
static int CAP = 1000; /* stop extending beyond this size (env INVCAP) */

/* DFS: current polygon poly[0..plen-1] ccw, all indices < next; mode 0: convex, 1: holes */
static void dfs(int start, int mode) {
    long long *cnt = mode ? hole_cnt : convex_cnt;
    for (int x = start; x < n; x++) {
        if (plen == 0) {
            poly[0] = x; plen = 1; cnt[1]++;
            dfs(x + 1, mode);
            plen = 0;
            continue;
        }
        if (plen == 1) {
            poly[1] = x; plen = 2; cnt[2]++;
            dfs(x + 1, mode);
            plen = 1;
            continue;
        }
        int vis = -1, nvis = 0;
        if (plen == 2) {
            int a = poly[0], b = poly[1];
            if (mode && !E3(a, b, x)) continue;
            int save0 = poly[0], save1 = poly[1];
            if (O(a, b, x) > 0) { poly[2] = x; }
            else { poly[0] = b; poly[1] = a; poly[2] = x; }
            plen = 3; cnt[3]++;
            dfs(x + 1, mode);
            plen = 2; poly[0] = save0; poly[1] = save1;
            continue;
        }
        for (int i = 0; i < plen; i++) {
            int a = poly[i], b = poly[(i + 1) % plen];
            if (O(a, b, x) < 0) { nvis++; vis = i; if (nvis > 1) break; }
        }
        if (nvis != 1) continue;
        if (plen >= CAP) { cnt[plen + 1]++; continue; }
        if (mode && !E3(poly[vis], poly[(vis + 1) % plen], x)) continue;
        /* insert x after position vis */
        for (int i = plen; i > vis + 1; i--) poly[i] = poly[i - 1];
        poly[vis + 1] = x; plen++;
        cnt[plen]++;
        dfs(x + 1, mode);
        for (int i = vis + 1; i < plen - 1; i++) poly[i] = poly[i + 1];
        plen--;
    }
}

static int inside(int d, int a, int b, int c) { /* d strictly inside triangle abc */
    int s = O(a, b, c);
    return O(a, b, d) == s && O(b, c, d) == s && O(c, a, d) == s;
}

/* canonical labeling */
static int cmp_p, cmp_s;
static int cmpf(const void *u, const void *v) {
    int q = *(const int *)u, r = *(const int *)v;
    if (q == r) return 0;
    return (cmp_s * O(cmp_p, q, r) > 0) ? -1 : 1;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: inv TABLE [skipconvex]\n"); return 1; }
    if (getenv("INVCAP")) CAP = atoi(getenv("INVCAP"));
    FILE *f = fopen(argv[1], "rb");
    if (!f) { perror("open"); return 1; }
    if (fscanf(f, "OT1 %d", &n) != 1) { fprintf(stderr, "bad header\n"); return 1; }
    fgetc(f);
    T = malloc((size_t)n * n * n);
    if (fread(T, 1, (size_t)n * n * n, f) != (size_t)n * n * n) { fprintf(stderr, "short\n"); return 1; }
    fclose(f);
    /* consistency */
    long bad = 0;
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) for (int c = 0; c < n; c++) {
        int s = O(a, b, c);
        if (a == b || b == c || a == c) { if (s) bad++; continue; }
        if (s != 1 && s != -1) bad++;
        if (O(b, c, a) != s || O(b, a, c) != -s) bad++;
    }
    printf("n=%d\ntable_violations=%ld\n", n, bad);
    if (bad) return 2;

    /* triangle contents and empty triangles */
    empty3 = calloc((size_t)n * n * n, 1);
    long long tri_in[80] = {0};
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) {
        int k = 0;
        for (int d = 0; d < n; d++) if (d != a && d != b && d != c && inside(d, a, b, c)) k++;
        tri_in[k]++;
        if (k == 0) {
            int p[3] = {a, b, c};
            for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) for (int l = 0; l < 3; l++)
                if (i != j && j != l && i != l) E3(p[i], p[j], p[l]) = 1;
        }
    }
    printf("tri_in=");
    for (int k = 0; k <= n - 3; k++) printf("%s%lld", k ? "," : "", tri_in[k]);
    printf("\n");

    /* j-edges */
    long long je[80] = {0};
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) {
        int L = 0;
        for (int c = 0; c < n; c++) if (c != a && c != b && O(a, b, c) > 0) L++;
        int m = L < n - 2 - L ? L : n - 2 - L;
        je[m]++;
    }
    printf("jedge=");
    for (int k = 0; k <= (n - 2) / 2; k++) printf("%s%lld", k ? "," : "", je[k]);
    printf("\n");
    if (n % 2 == 0) printf("halving_lines=%lld\n", je[(n - 2) / 2]);

    /* convex layers */
    int *alive = malloc(n * sizeof(int));
    for (int i = 0; i < n; i++) alive[i] = 1;
    int remaining = n;
    printf("layers=");
    int first = 1;
    int *hull0 = malloc(n * sizeof(int)), h0 = 0;
    while (remaining > 0) {
        int *ext = calloc(n, sizeof(int)), cnt = 0;
        for (int d = 0; d < n; d++) {
            if (!alive[d]) continue;
            int in = 0;
            for (int a = 0; a < n && !in; a++) { if (!alive[a] || a == d) continue;
                for (int b = a + 1; b < n && !in; b++) { if (!alive[b] || b == d) continue;
                    for (int c = b + 1; c < n; c++) { if (!alive[c] || c == d) continue;
                        if (inside(d, a, b, c)) { in = 1; break; } } } }
            if (!in) { ext[d] = 1; cnt++; }
        }
        if (first) { for (int d = 0; d < n; d++) if (ext[d]) hull0[h0++] = d; }
        printf("%s%d", first ? "" : ",", cnt);
        first = 0;
        for (int d = 0; d < n; d++) if (ext[d]) { alive[d] = 0; remaining--; }
        free(ext);
    }
    printf("\n");

    /* holes */
    memset(hole_cnt, 0, sizeof hole_cnt);
    plen = 0; dfs(0, 1);
    printf("holes=");
    int maxh = 0;
    for (int k = 1; k <= n; k++) if (hole_cnt[k]) maxh = k;
    for (int k = 3; k <= maxh; k++) printf("%s%lld", k > 3 ? "," : "", hole_cnt[k]);
    printf("  (j=3..%d)\n", maxh);

    if (argc < 3) {
        plen = 0; dfs(0, 0);
        int maxc = 0;
        for (int k = 1; k <= n; k++) if (convex_cnt[k]) maxc = k;
        printf("convex=");
        for (int k = 3; k <= maxc; k++) printf("%s%lld", k > 3 ? "," : "", convex_cnt[k]);
        printf("  (j=3..%d)\nmax_convex=%d\n", maxc, maxc);
    }

    /* canonical form */
    int ntrip = n * (n - 1) * (n - 2) / 6;
    char *best = NULL, *cur = malloc(ntrip + 1);
    cur[ntrip] = 0;
    int *lab = malloc(n * sizeof(int));
    char **cands = malloc(2 * h0 * sizeof(char *));
    for (int ci = 0; ci < 2 * h0; ci++) {
        int p = hull0[ci / 2], s = (ci % 2) ? -1 : 1;
        int m = 0;
        for (int q = 0; q < n; q++) if (q != p) lab[1 + m++] = q;
        lab[0] = p;
        cmp_p = p; cmp_s = s;
        qsort(lab + 1, n - 1, sizeof(int), cmpf);
        int t = 0;
        for (int i = 0; i < n; i++) for (int j = i + 1; j < n; j++) for (int k = j + 1; k < n; k++)
            cur[t++] = (s * O(lab[i], lab[j], lab[k]) > 0) ? '1' : '0';
        cands[ci] = strdup(cur);
        if (!best || strcmp(cur, best) < 0) { free(best); best = strdup(cur); }
    }
    int autp = 0, mirror = 0;
    for (int ci = 0; ci < 2 * h0; ci += 2) if (strcmp(cands[ci], cands[0]) == 0) autp++;
    for (int ci = 1; ci < 2 * h0; ci += 2) if (strcmp(cands[ci], cands[0]) == 0) mirror = 1;
    printf("hull_size=%d\naut_plus=%d\nmirror_automorphism=%d\n", h0, autp, mirror);
    char fn[4096];
    snprintf(fn, sizeof fn, "%s.canon", argv[1]);
    FILE *g = fopen(fn, "w");
    fprintf(g, "%s\n", best);
    fclose(g);
    printf("canon_written=%s\n", fn);
    return 0;
}
