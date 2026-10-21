/*
 * vfy.c -- independent exact check for lbs.c results.  Reads integer points,
 * checks general position (all triples, __int128 orientation computed from
 * the coordinates, no tables), and counts k-subsets in convex position for
 * k = 4..7 by enumerating subsets and computing the convex hull of each with
 * Andrew's monotone chain (a subset is convex iff all its points are hull
 * vertices).  Enumeration is pruned: a superset of a non-convex set is not
 * convex.  Also prints every convex 7-gon when there are at most 20, and the
 * points that lie in every convex 7-gon.
 * Usage: vfy FILE        (one "x y" per line, or "x,y" tokens)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
static int n;
static ll px[64], py[64];
static long long cnt[8];
static int sub[8];
static long long per[64];
static int list7[20][7], nlist;

static int sgn(ll ax, ll ay, ll bx, ll by, ll cx, ll cy) {
    __int128 v = (__int128)(bx - ax) * (cy - ay) - (__int128)(by - ay) * (cx - ax);
    return (v > 0) - (v < 0);
}

static int convex(int k) { /* all k points of sub[] are hull vertices? */
    int id[8];
    memcpy(id, sub, sizeof(int) * k);
    for (int i = 1; i < k; i++) { /* sort by (x, y) */
        int v = id[i], j = i;
        while (j > 0 && (px[id[j-1]] > px[v] || (px[id[j-1]] == px[v] && py[id[j-1]] > py[v]))) {
            id[j] = id[j-1]; j--;
        }
        id[j] = v;
    }
    int h[20], m = 0;
    for (int i = 0; i < k; i++) {
        while (m >= 2 && sgn(px[h[m-2]], py[h[m-2]], px[h[m-1]], py[h[m-1]], px[id[i]], py[id[i]]) <= 0) m--;
        h[m++] = id[i];
    }
    for (int i = k - 2, t = m + 1; i >= 0; i--) {
        while (m >= t && sgn(px[h[m-2]], py[h[m-2]], px[h[m-1]], py[h[m-1]], px[id[i]], py[id[i]]) <= 0) m--;
        h[m++] = id[i];
    }
    return m - 1 == k;
}

static void rec(int start, int k) {
    if (k >= 4) {
        if (!convex(k)) return;
        cnt[k]++;
        if (k == 7) {
            for (int i = 0; i < 7; i++) per[sub[i]]++;
            if (nlist < 20) memcpy(list7[nlist], sub, sizeof list7[0]);
            nlist++;
            return;
        }
    }
    for (int i = start; i < n; i++) { sub[k] = i; rec(i + 1, k + 1); }
}

int main(int argc, char **argv) {
    FILE *f = fopen(argv[1], "r");
    if (!f) { perror(argv[1]); return 2; }
    char tok[128];
    while (fscanf(f, "%127s", tok) == 1) {
        char *c = strchr(tok, ',');
        if (c) { if (strchr(tok, '=')) continue; px[n] = atoll(tok); py[n++] = atoll(c + 1); }
        else { px[n] = atoll(tok); if (fscanf(f, "%lld", &py[n]) != 1) return 2; n++; }
    }
    int gp = 1;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            for (int k = j + 1; k < n; k++)
                if (!sgn(px[i], py[i], px[j], py[j], px[k], py[k])) gp = 0;
    rec(0, 0);
    printf("n=%d general_position=%d c4=%lld c5=%lld c6=%lld c7=%lld\n", n, gp, cnt[4], cnt[5], cnt[6], cnt[7]);
    if (cnt[7] && cnt[7] <= 20)
        for (int t = 0; t < nlist && t < 20; t++) {
            printf("7gon:");
            for (int i = 0; i < 7; i++) printf(" %d", list7[t][i]);
            printf("\n");
        }
    if (cnt[7]) {
        printf("in_every_7gon:");
        for (int i = 0; i < n; i++) if (per[i] == cnt[7]) printf(" %d", i);
        printf("\n");
    }
    return 0;
}
