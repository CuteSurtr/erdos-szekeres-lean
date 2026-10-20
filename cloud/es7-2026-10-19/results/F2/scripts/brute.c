/* Brute-force check of x-sorted signotope models (one line of C(N,3) '0'/'1' chars per model,
 * lexicographic triples, '1' = ccw).  For each model prints:
 *   index axiom_violations max_cap max_cup largest_convex_subset_capped(>=K means a K-gon exists)
 * The convex-subset search is exhaustive over all subsets (DFS, pruned only by 4-point convexity,
 * which is exact by Caratheodory), stopping once size KMAX is reached.
 * usage: brute N KMAX < models */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MX 40
static int N, KMAX; static signed char O[MX][MX][MX];
static int chi(int a,int b,int c){ return O[a][b][c]; }
static int intri(int p,int u,int v,int w){ int s=chi(u,v,w); return chi(u,v,p)==s && chi(v,w,p)==s && chi(w,u,p)==s; }
static int conv4(int a,int b,int c,int d){ return !(intri(a,b,c,d)||intri(b,a,c,d)||intri(c,a,b,d)||intri(d,a,b,c)); }
static int best, cur[MX];
static void dfs(int k,int start){ if(k>best)best=k; if(best>=KMAX)return;
  for(int e=start;e<N;e++){ int ok=1;
    for(int i=0;i<k&&ok;i++)for(int j=i+1;j<k&&ok;j++)for(int l=j+1;l<k&&ok;l++) if(!conv4(cur[i],cur[j],cur[l],e)) ok=0;
    if(!ok)continue; cur[k]=e; dfs(k+1,e+1); if(best>=KMAX)return; } }
int main(int argc,char**argv){ N=atoi(argv[1]); KMAX=atoi(argv[2]);
  int nx=N*(N-1)*(N-2)/6; char*line=malloc(nx+16); long idx=0;
  while(fgets(line,nx+16,stdin)){ if((int)strlen(line)<nx) continue; int v=0;
    for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)for(int k=j+1;k<N;k++){ int s=line[v++]=='1'?1:-1;
      O[i][j][k]=O[j][k][i]=O[k][i][j]=s; O[j][i][k]=O[i][k][j]=O[k][j][i]=-s; }
    long ax=0;
    for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)for(int k=j+1;k<N;k++)for(int l=k+1;l<N;l++){
      int s[4]={O[i][j][k],O[i][j][l],O[i][k][l],O[j][k][l]}; int ch=0; for(int t=0;t<3;t++) if(s[t]!=s[t+1]) ch++; if(ch>1) ax++; }
    int cup[MX][MX], cap[MX][MX], mcup=2, mcap=2;
    for(int j=0;j<N;j++)for(int k=j+1;k<N;k++){ cup[j][k]=cap[j][k]=2;
      for(int i=0;i<j;i++){ if(O[i][j][k]>0){ if(cup[i][j]+1>cup[j][k]) cup[j][k]=cup[i][j]+1; }
                           else { if(cap[i][j]+1>cap[j][k]) cap[j][k]=cap[i][j]+1; } }
      if(cup[j][k]>mcup)mcup=cup[j][k]; if(cap[j][k]>mcap)mcap=cap[j][k]; }
    best=0; dfs(0,0);
    printf("%ld %ld %d %d %d\n", idx++, ax, mcap, mcup, best); }
  return 0; }
