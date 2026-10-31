/* Brute-force check of signotope models on n points (x-sorted, 0-based, X(i,j,k) true = ccw = cup).
   Input: one model per line, C(n,3) chars '+'/'-' in lexicographic triple order.
   Checks: signotope axiom (monotone sign sequence on every 4-tuple), longest cap < A,
   longest cup < U, no k-subset in convex position (k = K), by exhaustive enumeration.
   Prints per line: OK or FAIL <reason>. Usage: brute26 n A U K < models */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n, A, U, K; static signed char X[40][40][40];
static int ch(int a,int b,int c){ /* orientation for any distinct a,b,c */
  int t; int s=1; if(a>b){t=a;a=b;b=t;s=-s;} if(b>c){t=b;b=c;c=t;s=-s;} if(a>b){t=a;a=b;b=t;s=-s;} return s*X[a][b][c]; }
static int sub[16];
static int chain(int len,int sgn){ /* any len-subset with all consecutive triples of sign sgn? recursive */
  /* DP: best[a][b] = longest chain ending with a<b */
  static int best[40][40]; int mx=0;
  for(int b=0;b<n;b++) for(int a=0;a<b;a++){ int v=2; for(int z=0;z<a;z++) if(X[z][a][b]==sgn && best[z][a]+1>v) v=best[z][a]+1; best[a][b]=v; if(v>mx) mx=v; }
  return mx >= len; }
/* brute chain (exhaustive subsets) to double-check DP */
static int bchain(int len,int sgn,int start,int depth){
  if(depth==len) return 1;
  for(int i=start;i<n;i++){ if(depth>=2 && X[sub[depth-2]][sub[depth-1]][i]!=sgn) continue; sub[depth]=i; if(bchain(len,sgn,i+1,depth+1)) return 1; }
  return 0; }
static unsigned char nc4[40][40][40][40];
static int convex_k(int k,int start,int depth){
  if(depth==k) return 1;
  for(int i=start;i<n;i++){ int ok=1;
    for(int a=0;a<depth&&ok;a++) for(int b=a+1;b<depth&&ok;b++) for(int c=b+1;c<depth&&ok;c++) if(nc4[sub[a]][sub[b]][sub[c]][i]) ok=0;
    if(!ok) continue; sub[depth]=i; if(convex_k(k,i+1,depth+1)) return 1; }
  return 0; }
int main(int argc,char**argv){
  n=atoi(argv[1]); A=atoi(argv[2]); U=atoi(argv[3]); K=atoi(argv[4]);
  static char line[20000]; long ln=0;
  while(fgets(line,sizeof line,stdin)){ ln++; int p=0;
    for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++){ char c=line[p++]; X[i][j][k]= c=='+'?1:-1; }
    const char*bad=NULL;
    for(int i=0;i<n&&!bad;i++)for(int j=i+1;j<n&&!bad;j++)for(int k=j+1;k<n&&!bad;k++)for(int l=k+1;l<n&&!bad;l++){
      int s[4]={X[i][j][k],X[i][j][l],X[i][k][l],X[j][k][l]}; int chg=0; for(int t=0;t<3;t++) if(s[t]!=s[t+1]) chg++;
      if(chg>1) bad="signotope";
      int q[4]={i,j,k,l}; int nonc=0;
      for(int d=0;d<4;d++){ int o[3],m=0; for(int e=0;e<4;e++) if(e!=d) o[m++]=q[e];
        int s0=ch(o[0],o[1],o[2]); if(ch(o[0],o[1],q[d])==s0&&ch(o[1],o[2],q[d])==s0&&ch(o[2],o[0],q[d])==s0) nonc=1; }
      nc4[i][j][k][l]=nonc; }
    if(!bad && bchain(A,-1,0,0)) bad="cap";
    if(!bad && bchain(U,+1,0,0)) bad="cup";
    if(!bad && (chain(A,-1)||chain(U,1))) bad="dp-mismatch";
    if(!bad && convex_k(K,0,0)) bad="kgon";
    if(bad) printf("FAIL %ld %s\n",ln,bad); else printf("OK %ld\n",ln);
  }
  return 0; }
