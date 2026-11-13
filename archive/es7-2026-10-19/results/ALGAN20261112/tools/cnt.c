// Independent check: m-fold cyclotomic .pts (m=4 or 6) -> exact lattice coords,
// distinctness, general position, m-fold invariance, and counts of convex k-subsets
// k=3..9 (9 = ">=9") by a lowest-point angular counting DP (not DFS).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef __int128 i128; typedef long long ll;
#define MAXN 200
int n,m; ll A[MAXN],B[MAXN]; signed char *O;
#define OR(a,b,c) O[((a)*n+(b))*n+(c)]
static int sgn(i128 v){return v>0?1:(v<0?-1:0);}
int P,idx[MAXN],cntS;
int cmp(const void*x,const void*y){int a=*(int*)x,b=*(int*)y;return OR(P,a,b)>0?-1:1;}
int main(int argc,char**argv){
  FILE*f=fopen(argv[1],"r"); char line[4096]; m=atoi(argv[2]); n=0;
  while(fgets(line,sizeof line,f)){ if(line[0]=='#'||line[0]=='\n')continue;
    ll w[16]; int k=0; char*s=line; char*e;
    while(k<m){ ll v=strtoll(s,&e,10); if(e==s)break; w[k++]=v; s=e;}
    if(k!=m){fprintf(stderr,"bad row\n");return 2;}
    ll a=0,b=0;
    for(int j=0;j<m;j++){ int r=j%m; ll ba,bb;
      if(m==4){ int t[4][2]={{1,0},{0,1},{-1,0},{0,-1}}; ba=t[r][0]; bb=t[r][1]; }
      else if(m==6){ int t[6][2]={{1,0},{0,1},{-1,1},{-1,0},{0,-1},{1,-1}}; ba=t[r][0]; bb=t[r][1]; }
      else {fprintf(stderr,"m unsupported\n");return 2;}
      a+=w[j]*ba; b+=w[j]*bb; }
    A[n]=a;B[n]=b;n++; }
  printf("n=%d\n",n);
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++) if(A[i]==A[j]&&B[i]==B[j]){printf("DUPLICATE %d %d\n",i,j);return 1;}
  // invariance under rotation by 2pi/m
  int inv=1;
  for(int i=0;i<n;i++){ ll a2,b2; if(m==4){a2=-B[i];b2=A[i];} else {a2=-B[i];b2=A[i]+B[i];}
    int found=0; for(int j=0;j<n;j++) if(A[j]==a2&&B[j]==b2){found=1;break;} if(!found)inv=0; }
  printf("invariant_under_rotation=%d\n",inv);
  O=malloc((size_t)n*n*n); int coll=0;
  for(int a=0;a<n;a++)for(int b=0;b<n;b++)for(int c=0;c<n;c++){
    i128 v=(i128)(A[b]-A[a])*(B[c]-B[a])-(i128)(B[b]-B[a])*(A[c]-A[a]);
    OR(a,b,c)=sgn(v); if(a<b&&b<c&&v==0)coll++; }
  printf("collinear_triples=%d\n",coll); if(coll)return 1;
  // counting DP
  static double tot[10]; memset(tot,0,sizeof tot);
  static ll cnt[MAXN][MAXN][10];
  for(P=0;P<n;P++){
    cntS=0; for(int q=0;q<n;q++) if(q!=P && (B[q]>B[P] || (B[q]==B[P]&&A[q]>A[P]))) idx[cntS++]=q;
    qsort(idx,cntS,sizeof(int),cmp);
    for(int i=0;i<cntS;i++)for(int j=0;j<cntS;j++)memset(cnt[i][j],0,sizeof cnt[i][j]);
    for(int i=0;i<cntS;i++)for(int j=i+1;j<cntS;j++) cnt[i][j][3]=1;
    for(int j=0;j<cntS;j++){ // process edges (i,j) in increasing j; extend to l>j
      for(int i=0;i<j;i++){ ll*c=cnt[i][j];
        int vi=idx[i],vj=idx[j];
        // close
        if(OR(vi,vj,P)>0) for(int L=3;L<=9;L++) tot[L]+=c[L];
        for(int l=j+1;l<cntS;l++){ int vl=idx[l]; if(OR(vi,vj,vl)>0){ ll*d=cnt[j][l];
            for(int L=3;L<=8;L++) d[L+1]+=c[L]; d[9]+=c[9]; } } } }
  }
  for(int L=3;L<=9;L++) printf("convex_%d%s=%.0f\n",L,L==9?"+":"",tot[L]);
  return 0; }
