/* verify.c - independent exact check of a point file (columns a b u v; uses u v only).
   Checks: 33 distinct points, no three collinear (128-bit cross products),
   then enumerates all C(33,7) subsets and computes the number of hull vertices
   of each (a point is not a hull vertex iff it lies in a triangle of 3 others).
   Also enumerates all 6-subsets. Prints the hull-size distributions and the first 12 convex 7-gons (point indices). */
#include <stdio.h>
#include <stdlib.h>
typedef long long ll; typedef __int128 L;
#define N 33
static ll u[N],v[N]; static signed char O[N][N][N];
static int sg(int i,int j,int k){ L x=(L)(u[j]-u[i])*(v[k]-v[i])-(L)(v[j]-v[i])*(u[k]-u[i]); return x>0?1:(x<0?-1:0); }
static int intri(int p,int a,int b,int c){ int s1=O[a][b][p],s2=O[b][c][p],s3=O[c][a][p]; return s1==s2&&s2==s3; }
static int hull(int *s,int n){ int h=0;
  for(int x=0;x<n;x++){ int in=0;
    for(int a=0;a<n&&!in;a++) for(int b=a+1;b<n&&!in;b++) for(int c=b+1;c<n&&!in;c++){
      if(a==x||b==x||c==x) continue;
      if(intri(s[x],s[a],s[b],s[c])) in=1; }
    if(!in) h++; } return h; }
int main(int argc,char**argv){
  FILE *f=fopen(argv[1],"r"); char line[1024]; int n=0;
  while(fgets(line,sizeof line,f)){ if(line[0]=='#') continue; ll a,b,uu,vv;
    if(sscanf(line,"%lld %lld %lld %lld",&a,&b,&uu,&vv)==4){ if(n>=N){n++;break;} u[n]=uu; v[n]=vv; n++; } }
  if(n!=N){ printf("ERROR: %d points\n",n); return 1; }
  for(int i=0;i<N;i++) for(int j=i+1;j<N;j++) if(u[i]==u[j]&&v[i]==v[j]){ printf("ERROR: duplicate\n"); return 1; }
  int col=0;
  for(int i=0;i<N;i++) for(int j=0;j<N;j++) for(int k=0;k<N;k++){ if(i==j||j==k||i==k) continue; O[i][j][k]=sg(i,j,k); if(i<j&&j<k&&!O[i][j][k]) col++; }
  printf("collinear_triples %d\n",col); if(col) return 1;
  ll d7[8]={0},d6[7]={0}; int s[7];
  for(s[0]=0;s[0]<N;s[0]++) for(s[1]=s[0]+1;s[1]<N;s[1]++) for(s[2]=s[1]+1;s[2]<N;s[2]++)
  for(s[3]=s[2]+1;s[3]<N;s[3]++) for(s[4]=s[3]+1;s[4]<N;s[4]++) for(s[5]=s[4]+1;s[5]<N;s[5]++){
    d6[hull(s,6)]++;
    for(s[6]=s[5]+1;s[6]<N;s[6]++){ int h=hull(s,7); d7[h]++;
      if(h==7 && d7[7]<=12){ printf("convex7gon"); for(int t=0;t<7;t++) printf(" %d",s[t]); printf("\n"); } } }
  printf("6-subsets hull-size distribution:"); for(int h=3;h<=6;h++) printf(" h%d=%lld",h,d6[h]); printf("\n");
  printf("7-subsets hull-size distribution:"); for(int h=3;h<=7;h++) printf(" h%d=%lld",h,d7[h]); printf("\n");
  printf("convex6 %lld\nconvex7 %lld\nsix_plus_one %lld\n",d6[6],d7[7],d7[6]);
  return 0; }
