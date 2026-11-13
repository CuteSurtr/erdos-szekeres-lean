/* Independent exact check: reads 33 points (lines "x y", '#' comments),
   checks general position (no repeated point, no three collinear) and counts
   7-subsets (and 6-subsets) in convex position by brute force: a subset is in
   convex position iff no member lies in a closed triangle of three others.
   Also prints per-point participation in convex 7-gons. Uses __int128. */
#include <stdio.h>
#include <string.h>
typedef long long ll; typedef __int128 L;
int n=0; ll X[64],Y[64];
static int sgn(int a,int b,int c){ L v=(L)(X[b]-X[a])*(Y[c]-Y[a])-(L)(Y[b]-Y[a])*(X[c]-X[a]); return v>0?1:(v<0?-1:0); }
static int intri(int p,int a,int b,int c){ int s1=sgn(a,b,p),s2=sgn(b,c,p),s3=sgn(c,a,p);
  return (s1>=0&&s2>=0&&s3>=0)||(s1<=0&&s2<=0&&s3<=0); }
static int convex(int*s,int k){ for(int i=0;i<k;i++) for(int a=0;a<k;a++) if(a!=i) for(int b=a+1;b<k;b++) if(b!=i) for(int c=b+1;c<k;c++) if(c!=i)
  if(intri(s[i],s[a],s[b],s[c])) return 0; return 1; }
long long part[64];
static ll cnt(int k,int track){ int s[8]; ll tot=0; for(int i=0;i<k;i++) s[i]=i;
  while(1){ if(convex(s,k)){ tot++; if(track) for(int i=0;i<k;i++) part[s[i]]++; }
    int i=k-1; while(i>=0 && s[i]==n-k+i) i--; if(i<0) break; s[i]++; for(int j=i+1;j<k;j++) s[j]=s[j-1]+1; }
  return tot; }
int main(int argc,char**argv){ FILE*f=fopen(argv[1],"r"); char line[256];
  while(fgets(line,256,f)){ if(line[0]=='#') continue; if(sscanf(line,"%lld %lld",&X[n],&Y[n])==2) n++; }
  int gp=1; for(int a=0;a<n;a++) for(int b=a+1;b<n;b++){ if(X[a]==X[b]&&Y[a]==Y[b]) gp=0; for(int c=b+1;c<n;c++) if(sgn(a,b,c)==0) gp=0; }
  printf("n %d general_position %s\n",n,gp?"yes":"NO");
  ll c7=cnt(7,1); printf("convex7 %lld\n",c7);
  if(argc>2){ ll c6=cnt(6,0); printf("convex6 %lld\n",c6); }
  printf("participation7:"); for(int i=0;i<n;i++) printf(" %lld",part[i]); printf("\n"); return 0; }
