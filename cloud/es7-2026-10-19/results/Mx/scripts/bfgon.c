/* Mx brute force: largest subset in convex position, by exhaustive DFS over subsets in
   convex position, using exact integer orientation tests (coordinates |.| < 2^30).
   A set is in convex position iff no point lies in a triangle of three others.
   Input lines: n x1 y1 ... xn yn ; output: largest convex-position subset size (capped at cap). */
#include <stdio.h>
#include <stdlib.h>
typedef long long ll; typedef __int128 L;
static int n, cap, best; static ll X[64], Y[64]; static int S[64];
static int orient(int a,int b,int c){ L d=(L)(X[b]-X[a])*(Y[c]-Y[a])-(L)(Y[b]-Y[a])*(X[c]-X[a]); return d>0?1:(d<0?-1:0); }
static int intri(int p,int a,int b,int c){ int o1=orient(a,b,p),o2=orient(b,c,p),o3=orient(c,a,p); return o1==o2&&o2==o3; }
static int ok(int r,int m){ /* S[0..m-1] in convex position; can r be added? */
  for(int i=0;i<m;i++)for(int j=i+1;j<m;j++)for(int k=j+1;k<m;k++){
    if(intri(r,S[i],S[j],S[k]))return 0;
    if(intri(S[i],r,S[j],S[k])||intri(S[j],r,S[i],S[k])||intri(S[k],r,S[i],S[j]))return 0; }
  return 1; }
static void dfs(int m,int from){ if(m>best)best=m; if(best>=cap)return;
  for(int r=from;r<n;r++){ if(m+(n-r)<=best)return; if(ok(r,m)){S[m]=r;dfs(m+1,r+1); if(best>=cap)return;} } }
int main(int argc,char**argv){ cap=argc>1?atoi(argv[1]):99;
  while(scanf("%d",&n)==1){ for(int i=0;i<n;i++)scanf("%lld %lld",&X[i],&Y[i]);
    best=0; dfs(0,0); printf("%d\n",best); fflush(stdout);} return 0; }
