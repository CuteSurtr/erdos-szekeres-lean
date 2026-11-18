// Exact cap/cup/convex-polygon analysis for planar point sets (sorted by x, distinct x).
// Orientation with __int128. All arrays row-major n*n.
#include <stdlib.h>
#include <string.h>
typedef long long ll;
typedef __int128 i128;
static int orient(const ll *x, const ll *y, int a, int b, int c){
  i128 v = (i128)(x[b]-x[a])*(y[c]-y[a]) - (i128)(y[b]-y[a])*(x[c]-x[a]);
  return v>0 ? 1 : (v<0 ? -1 : 0);
}
// returns 0 ok, -1 if collinear triple or non-increasing x
// capE[i*n+j]: longest cap ending with edge (i,j), i<j (>=2); cupE same for cups
// capS, cupS: longest starting with edge (i,j)
// capB[s*n+t], cupB: longest cap/cup from s to t (>=2 for s<t)
int analyze(int n, const ll *x, const ll *y, int *capE, int *cupE, int *capS, int *cupS, int *capB, int *cupB){
  for(int i=0;i+1<n;i++) if(x[i]>=x[i+1]) return -1;
  signed char *O = malloc((size_t)n*n*n);
  for(int a=0;a<n;a++) for(int b=a+1;b<n;b++) for(int c=b+1;c<n;c++){
    int o = orient(x,y,a,b,c); if(o==0){free(O);return -2;}
    O[((size_t)a*n+b)*n+c]=(signed char)o; }
  for(int j=0;j<n;j++) for(int i=0;i<j;i++){
    int bc=2,bu=2;
    for(int h=0;h<i;h++){ signed char o=O[((size_t)h*n+i)*n+j];
      if(o<0){ if(capE[h*n+i]+1>bc) bc=capE[h*n+i]+1; } else { if(cupE[h*n+i]+1>bu) bu=cupE[h*n+i]+1; } }
    capE[i*n+j]=bc; cupE[i*n+j]=bu; }
  for(int i=n-1;i>=0;i--) for(int j=n-1;j>i;j--){
    int bc=2,bu=2;
    for(int k=j+1;k<n;k++){ signed char o=O[((size_t)i*n+j)*n+k];
      if(o<0){ if(capS[j*n+k]+1>bc) bc=capS[j*n+k]+1; } else { if(cupS[j*n+k]+1>bu) bu=cupS[j*n+k]+1; } }
    capS[i*n+j]=bc; cupS[i*n+j]=bu; }
  if(capB){
    int *Dc = malloc(sizeof(int)*n*n), *Du = malloc(sizeof(int)*n*n);
    for(int s=0;s<n;s++){
      // D[i][j] longest chain from s ending with edge (i,j), s<=i<j; 0 if none
      for(int i=0;i<n*n;i++){Dc[i]=0;Du[i]=0;}
      for(int j=s+1;j<n;j++){ Dc[s*n+j]=2; Du[s*n+j]=2; }
      for(int j=s+1;j<n;j++) for(int i=s+1;i<j;i++){
        int bc=0,bu=0;
        for(int h=s;h<i;h++){ signed char o=O[((size_t)h*n+i)*n+j];
          if(o<0){ if(Dc[h*n+i] && Dc[h*n+i]+1>bc) bc=Dc[h*n+i]+1; } else { if(Du[h*n+i] && Du[h*n+i]+1>bu) bu=Du[h*n+i]+1; } }
        Dc[i*n+j]=bc; Du[i*n+j]=bu; }
      for(int t=0;t<n;t++){ capB[s*n+t]=0; cupB[s*n+t]=0; }
      for(int t=s+1;t<n;t++){ int bc=0,bu=0; for(int i=s;i<t;i++){ if(Dc[i*n+t]>bc) bc=Dc[i*n+t]; if(Du[i*n+t]>bu) bu=Du[i*n+t]; }
        capB[s*n+t]=bc; cupB[s*n+t]=bu; }
    }
    free(Dc); free(Du);
  }
  free(O); return 0;
}
// fast validity: returns max over (s,t) of capB+cupB-2 (largest convex polygon), and max cap, max cup
int quick(int n, const ll *x, const ll *y, int *maxcap, int *maxcup){
  int *capE=malloc(sizeof(int)*n*n),*cupE=malloc(sizeof(int)*n*n),*capS=malloc(sizeof(int)*n*n),*cupS=malloc(sizeof(int)*n*n),*capB=malloc(sizeof(int)*n*n),*cupB=malloc(sizeof(int)*n*n);
  int r = analyze(n,x,y,capE,cupE,capS,cupS,capB,cupB);
  int best=0, mc=1, mu=1;
  if(r==0){ for(int s=0;s<n;s++) for(int t=s+1;t<n;t++){ int v=capB[s*n+t]+cupB[s*n+t]-2; if(v>best) best=v; if(capB[s*n+t]>mc) mc=capB[s*n+t]; if(cupB[s*n+t]>mu) mu=cupB[s*n+t]; } }
  else best = r;
  *maxcap=mc; *maxcup=mu;
  free(capE);free(cupE);free(capS);free(cupS);free(capB);free(cupB);
  return best;
}

// Find a convex polygon witness with exactly k vertices (k>=3). Returns number of vertices written (k) or 0.
// Uses longest cap/cup between endpoints with back-pointers; drops interior points if longer.
int gon_witness(int n, const ll *x, const ll *y, int k, int *out){
  for(int i=0;i+1<n;i++) if(x[i]>=x[i+1]) return -1;
  if(n<k) return 0;
  signed char *O = malloc((size_t)n*n*n);
  for(int a=0;a<n;a++) for(int b=a+1;b<n;b++) for(int c=b+1;c<n;c++){ int o=orient(x,y,a,b,c); if(o==0){free(O);return -2;} O[((size_t)a*n+b)*n+c]=(signed char)o; }
  int *Dc=malloc(sizeof(int)*n*n),*Du=malloc(sizeof(int)*n*n),*Pc=malloc(sizeof(int)*n*n),*Pu=malloc(sizeof(int)*n*n);
  int found=0;
  for(int s=0;s<n && !found;s++){
    for(int i=0;i<n*n;i++){Dc[i]=0;Du[i]=0;Pc[i]=-1;Pu[i]=-1;}
    for(int j=s+1;j<n;j++){ Dc[s*n+j]=2; Du[s*n+j]=2; }
    for(int j=s+1;j<n;j++) for(int i=s+1;i<j;i++){
      int bc=0,bu=0,pc=-1,pu=-1;
      for(int h=s;h<i;h++){ signed char o=O[((size_t)h*n+i)*n+j];
        if(o<0){ if(Dc[h*n+i] && Dc[h*n+i]+1>bc){bc=Dc[h*n+i]+1;pc=h;} } else { if(Du[h*n+i] && Du[h*n+i]+1>bu){bu=Du[h*n+i]+1;pu=h;} } }
      Dc[i*n+j]=bc; Du[i*n+j]=bu; Pc[i*n+j]=pc; Pu[i*n+j]=pu; }
    for(int t=s+1;t<n && !found;t++){
      int bc=0,bi=-1,bu=0,bj=-1;
      for(int i=s;i<t;i++){ if(Dc[i*n+t]>bc){bc=Dc[i*n+t];bi=i;} if(Du[i*n+t]>bu){bu=Du[i*n+t];bj=i;} }
      if(bc+bu-2>=k){
        int capv[64],cupv[64],nc=0,nu=0;
        // reconstruct cap: chain ... bi, t
        int a=bi,b=t; capv[nc++]=t; while(1){ capv[nc++]=a; if(a==s) break; int h=Pc[a*n+b]; b=a; a=h; }
        a=bj; b=t; cupv[nu++]=t; while(1){ cupv[nu++]=a; if(a==s) break; int h=Pu[a*n+b]; b=a; a=h; }
        // capv, cupv reversed order (t ... s). interior counts nc-2, nu-2; need (nc-2)+(nu-2)+2 = k
        int needc = nc-2, needu = nu-2; int total = needc+needu+2;
        while(total>k){ if(needc>0){needc--;} else {needu--;} total--; }
        int m=0; out[m++]=s; out[m++]=t;
        for(int q=1;q<=needc;q++) out[m++]=capv[q];
        for(int q=1;q<=needu;q++) out[m++]=cupv[q];
        found=m;
      }
    }
  }
  free(O);free(Dc);free(Du);free(Pc);free(Pu);
  return found;
}
