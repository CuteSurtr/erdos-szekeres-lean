/* Independent enumerator of all subsets in convex position, from an orientation table.
   Input file: n on the first line, then a string of C(n,3) characters '+'/'-' for triples i<j<k in
   lexicographic order. A set (general position) is convex iff every 4-subset is convex (Caratheodory).
   DFS adds points in increasing index order, checking only the new 4-subsets. Prints counts by size and max. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n;
static signed char *O;          /* O[i*n*n+j*n+k] full antisymmetric table */
static unsigned char *Q4;       /* Q4 for sorted quadruple: 1 if convex */
static long long cnt[256];
static int maxsz = 0;
static int cur[256];
static long long cap_size = 0;  /* optional: stop exploring beyond this size (0 = none) */
#define OR(i,j,k) O[((size_t)(i)*n+(j))*n+(k)]
static int intri(int a,int b,int c,int x){int s1=OR(a,b,x),s2=OR(b,c,x),s3=OR(c,a,x);return s1==s2&&s2==s3;}
static int quadconvex(int a,int b,int c,int d){
  return !(intri(b,c,d,a)||intri(a,c,d,b)||intri(a,b,d,c)||intri(a,b,c,d));}
static size_t qidx(int a,int b,int c,int d){return (((size_t)a*n+b)*n+c)*n+d;}
static void dfs(int sz,int start){
  cnt[sz]++; if(sz>maxsz)maxsz=sz;
  for(int r=start;r<n;r++){
    int ok=1;
    for(int x=0;x<sz&&ok;x++)for(int y=x+1;y<sz&&ok;y++)for(int z=y+1;z<sz&&ok;z++)
      if(!Q4[qidx(cur[x],cur[y],cur[z],r)])ok=0;
    if(ok){cur[sz]=r;dfs(sz+1,r+1);}
  }
}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); if(!f){perror("open");return 1;}
  if(fscanf(f,"%d",&n)!=1)return 1;
  O=calloc((size_t)n*n*n,1);
  int c; size_t cntc=0;
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++){
    do{c=fgetc(f);}while(c=='\n'||c=='\r'||c==' ');
    if(c!='+'&&c!='-'){fprintf(stderr,"bad char\n");return 1;}
    int s=(c=='+')?1:-1; cntc++;
    OR(i,j,k)=s;OR(j,k,i)=s;OR(k,i,j)=s;OR(j,i,k)=-s;OR(i,k,j)=-s;OR(k,j,i)=-s;
  }
  fclose(f);
  Q4=calloc((size_t)n*n*n*n,1);
  for(int a=0;a<n;a++)for(int b=a+1;b<n;b++)for(int cc=b+1;cc<n;cc++)for(int d=cc+1;d<n;d++)
    Q4[qidx(a,b,cc,d)]=quadconvex(a,b,cc,d);
  dfs(0,0);
  printf("n=%d triples=%zu max_convex=%d\n",n,cntc,maxsz);
  for(int s=3;s<=maxsz;s++)printf("convex %d-subsets: %lld\n",s,cnt[s]);
  return 0;
}
