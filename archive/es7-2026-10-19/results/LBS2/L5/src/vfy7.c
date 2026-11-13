/* LBS2 L5: independent exact check of a point set (one "x y" per line, any n <= 40).
   General position by all C(n,3) orientations in __int128; counts of k-subsets in convex
   position for k = 4..8 by depth-first extension in index order, where a set is extended by q
   only if every 4-subset containing q is in convex position (Caratheodory: a set is in convex
   position iff all its 4-subsets are). Independent of the annealer's angular DP.
   Output: "gp G c5 A c6 B c7 C c8 D maxabs M"; with "-l" also lists the convex 7-subsets. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef __int128 i128;
static int n; static long long X[64], Y[64]; static signed char O[64][64][64];
static long long cnt[10]; static int listmode; static int S[10];
static int convex4(int a,int b,int c,int d){ /* d inside abc, etc. */
  int q[4]={a,b,c,d};
  for(int i=0;i<4;i++){ int p=q[i], u=q[(i+1)%4], v=q[(i+2)%4], w=q[(i+3)%4];
    int s1=O[u][v][p], s2=O[v][w][p], s3=O[w][u][p]; if(s1==s2&&s2==s3) return 0; }
  return 1; }
static void dfs(int k,int start){
  if(k>=3) cnt[k]++;
  if(k==7 && listmode){ printf("C7"); for(int i=0;i<7;i++) printf(" %d",S[i]); printf("\n"); }
  if(k==8) return;
  for(int q=start;q<n;q++){ int ok=1;
    for(int a=0;a<k&&ok;a++) for(int b=a+1;b<k&&ok;b++) for(int c=b+1;c<k&&ok;c++) if(!convex4(S[a],S[b],S[c],q)) ok=0;
    if(ok){ S[k]=q; dfs(k+1,q+1); } } }
int main(int argc,char**argv){
  if(argc<2){ fprintf(stderr,"usage: vfy7 file [-l]\n"); return 1; }
  listmode = argc>2 && !strcmp(argv[2],"-l");
  FILE*f=fopen(argv[1],"r"); if(!f) return 1; long long x,y; n=0; long long mx=0;
  while(fscanf(f,"%lld %lld",&x,&y)==2){ if(n>=40){fprintf(stderr,"too many\n");return 1;} X[n]=x;Y[n]=y;n++;
    if(llabs(x)>mx) mx=llabs(x); if(llabs(y)>mx) mx=llabs(y);} fclose(f);
  if(mx > (1LL<<60)){ fprintf(stderr,"coords too large\n"); return 1; }
  int gp=1;
  for(int a=0;a<n;a++) for(int b=0;b<n;b++) for(int c=0;c<n;c++){
    i128 d=(i128)(X[b]-X[a])*(Y[c]-Y[a])-(i128)(Y[b]-Y[a])*(X[c]-X[a]);
    O[a][b][c]=(d>0)-(d<0); if(a!=b&&b!=c&&a!=c&&d==0) gp=0; }
  if(!gp){ printf("gp 0 n %d maxabs %lld\n",n,mx); return 0; }
  dfs(0,0);
  printf("gp 1 n %d c5 %lld c6 %lld c7 %lld c8 %lld maxabs %lld\n",n,cnt[5],cnt[6],cnt[7],cnt[8],mx);
  return 0; }
