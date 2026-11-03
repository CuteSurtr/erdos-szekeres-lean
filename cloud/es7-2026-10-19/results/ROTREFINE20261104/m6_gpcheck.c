/* gpcheck: read an orientation table (n, then n*n*n signed chars, chi[a][b][c] in {-1,0,1}) from stdin;
   enumerate all 5-subsets and all 3-term Grassmann-Pluecker relations
     [abc][ade] - [abd][ace] + [abe][acd] = 0   (pivot a, the other four b<c<d<e)
   report relations whose three terms have the same sign (impossible in general position).
   output lines: a b c d e  (pivot first). Stops after MAXOUT lines. */
#include <stdio.h>
#include <stdlib.h>
#define MAXN 80
static signed char chi[MAXN][MAXN][MAXN];
int main(int argc, char **argv) {
  int n; long maxout = argc > 1 ? atol(argv[1]) : 100000; long cnt = 0, viol = 0;
  if (scanf("%d", &n) != 1) return 1;
  for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) for (int c = 0; c < n; c++) {
    int v; if (scanf("%d", &v) != 1) return 2; chi[a][b][c] = (signed char)v; }
  int q[5];
  for (q[0] = 0; q[0] < n; q[0]++) for (q[1] = q[0]+1; q[1] < n; q[1]++) for (q[2] = q[1]+1; q[2] < n; q[2]++)
  for (q[3] = q[2]+1; q[3] < n; q[3]++) for (q[4] = q[3]+1; q[4] < n; q[4]++) {
    for (int p = 0; p < 5; p++) {
      int a = q[p], o[4], k = 0;
      for (int r = 0; r < 5; r++) if (r != p) o[k++] = q[r];
      int b = o[0], c = o[1], d = o[2], e = o[3];
      int t1 = chi[a][b][c] * chi[a][d][e];
      int t2 = -chi[a][b][d] * chi[a][c][e];
      int t3 = chi[a][b][e] * chi[a][c][d];
      cnt++;
      if (t1 == t2 && t2 == t3) {
        viol++;
        if (viol <= maxout) printf("%d %d %d %d %d\n", a, b, c, d, e);
      }
    }
  }
  fprintf(stderr, "relations %ld violated %ld\n", cnt, viol);
  return 0;
}
