/* Exhaustive count of subsets in convex position, by size, for points in general position (exact __int128).
   A set is in convex position iff no point lies strictly inside a triangle of three others (general position).
   DFS over index-increasing subsets; a new point x extends a convex set S iff for every triple {a,b,c} of S, x is not
   inside abc, and for every pair {a,b} of S and every c in S, c is not inside abx.  Input: lines "a b" (integers). */
#include <stdio.h>
#include <stdlib.h>
typedef __int128 i128; typedef long long ll;
static ll X[100], Y[100]; static int n; static long long cnt[20];
static int sgn(int o,int p,int q){ i128 v=(i128)(X[p]-X[o])*(Y[q]-Y[o])-(i128)(Y[p]-Y[o])*(X[q]-X[o]); return v>0?1:(v<0?-1:0);}
static int inside(int x,int a,int b,int c){ int s1=sgn(a,b,x),s2=sgn(b,c,x),s3=sgn(c,a,x); return (s1>0&&s2>0&&s3>0)||(s1<0&&s2<0&&s3<0);}
static int S[20];
static void dfs(int k,int start){
  cnt[k]++;
  if(k>=12) return;
  for(int x=start;x<n;x++){
    int ok=1;
    for(int i=0;i<k&&ok;i++) for(int j=i+1;j<k&&ok;j++) for(int l=j+1;l<k&&ok;l++){
      int a=S[i],b=S[j],c=S[l];
      if(inside(x,a,b,c)||inside(a,b,c,x)||inside(b,a,c,x)||inside(c,a,b,x)) ok=0; }
    if(ok){ S[k]=x; dfs(k+1,x+1);} }
}
int main(int argc,char**argv){ FILE*f=fopen(argv[1],"r"); if(!f){fprintf(stderr,"cannot open %s\n",argv[1]); return 2;} while(fscanf(f,"%lld %lld",&X[n],&Y[n])==2) n++;
  for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int c=b+1;c<n;c++) if(!sgn(a,b,c)){printf("collinear\n");return 1;}
  dfs(0,0); printf("n=%d\n",n); for(int k=3;k<20;k++) if(cnt[k]) printf("convex %d-subsets: %lld\n",k,cnt[k]);
  int mx=0; for(int k=0;k<20;k++) if(cnt[k]) mx=k; printf("largest convex subset: %d\n",mx); return 0;}
