/* lbs.c - heuristic search for 33 points with few convex 7-gons.
   Strategy c3coords: points in Eisenstein coordinates (a,b) = a + b*w, w = exp(2 pi i/3).
   Rotation by 120 degrees about the origin is exact: (a,b) -> (-b, a-b).
   The map (a,b) -> (a - b/2, b*sqrt3/2) is linear with positive determinant, so
   orientation signs in (a,b) equal the Euclidean ones.
   Each restart: simulated annealing over 11 orbit representatives (3-fold symmetric),
   then simulated annealing over all 33 points (symmetry broken).
   Count of convex k-gons: for each lowest vertex p, angular sort, DP over chains.
   usage: lbs seed seconds outprefix [R] [symsteps] [freesteps] [w] [initfile]
   with initfile (sets in the _near.txt format) each restart starts the free phase
   from a random c7 = 3 set of that file instead of running the symmetric phase.
   acceptance energy is c7 + w*c6 (w = 0: pure c7). */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define N 33
#define K 11
typedef long long ll;
static ll A[N], B[N];
static signed char O[N][N][N];

static uint64_t rs;
static inline uint64_t rnd(void){ rs ^= rs<<13; rs ^= rs>>7; rs ^= rs<<17; return rs; }
static inline double urand(void){ return (rnd()>>11)*(1.0/9007199254740992.0); }

static inline int orient3(int i,int j,int k){
  ll v=(A[j]-A[i])*(B[k]-B[i])-(B[j]-B[i])*(A[k]-A[i]);
  return v>0?1:(v<0?-1:0);
}
/* recompute orientations involving q; return 0 if some triple with q is collinear */
static int update_point(int q){
  int ok=1;
  for(int j=0;j<N;j++){ if(j==q) continue;
    for(int k=j+1;k<N;k++){ if(k==q) continue;
      int s=orient3(q,j,k); if(!s) ok=0;
      O[q][j][k]=O[j][k][q]=O[k][q][j]=s;
      O[q][k][j]=O[k][j][q]=O[j][q][k]=-s; } }
  return ok;
}
static int full_table(void){ int ok=1; for(int q=0;q<N;q++) if(!update_point(q)) ok=0; return ok; }

static inline int lower(int i,int p){ return B[i]>B[p] || (B[i]==B[p] && A[i]>A[p]); }

/* counts convex 6-gons and 7-gons */
static void count(ll *c6, ll *c7){
  static uint32_t dp[N][N], nx[N][N];
  int s[N]; ll t6=0,t7=0;
  for(int p=0;p<N;p++){
    int m=0;
    for(int i=0;i<N;i++) if(i!=p && lower(i,p)){
      int x=m++; while(x>0 && O[p][i][s[x-1]]>0){ s[x]=s[x-1]; x--; } s[x]=i; }
    if(m<5) continue;   /* 6-gons need 5 points above p (fixed: was m<6, which missed at most one 6-gon) */
    for(int i=0;i<m;i++) for(int j=0;j<m;j++) dp[i][j]=(i<j);
    for(int len=3;len<=6;len++){ /* dp holds chains with len vertices (incl p) ending i->j */
      for(int i=0;i<m;i++) memset(nx[i],0,sizeof(uint32_t)*m);
      for(int i=0;i<m;i++) for(int j=i+1;j<m;j++){ uint32_t v=dp[i][j]; if(!v) continue;
        signed char *o=O[s[i]][s[j]];
        for(int k=j+1;k<m;k++) if(o[s[k]]>0) nx[j][k]+=v; }
      for(int i=0;i<m;i++) memcpy(dp[i],nx[i],sizeof(uint32_t)*m);
      if(len==5){ /* dp now = 6-vertex chains */
        for(int i=0;i<m;i++) for(int j=i+1;j<m;j++) if(dp[i][j] && O[s[i]][s[j]][p]>0) t6+=dp[i][j]; }
    }
    for(int i=0;i<m;i++) for(int j=i+1;j<m;j++) if(dp[i][j] && O[s[i]][s[j]][p]>0) t7+=dp[i][j];
  }
  *c6=t6; *c7=t7;
}

static ll R=100000;
static void rot(ll a,ll b,ll *ra,ll *rb){ *ra=-b; *rb=a-b; }
static void set_orbit(int r,ll a,ll b){
  A[r]=a; B[r]=b; rot(A[r],B[r],&A[r+K],&B[r+K]); rot(A[r+K],B[r+K],&A[r+2*K],&B[r+2*K]); }
static int distinct_ok(void){
  for(int i=0;i<N;i++){ if(A[i]==0&&B[i]==0) return 0;
    for(int j=i+1;j<N;j++) if(A[i]==A[j]&&B[i]==B[j]) return 0; } return 1; }
static ll rcoord(void){ return (ll)(rnd()%(2*R+1))-R; }

static void save(const char *fn,ll c7,ll c6,int sym){
  char tmp[512]; snprintf(tmp,sizeof tmp,"%s.tmp",fn);
  FILE *f=fopen(tmp,"w"); if(!f) return;
  fprintf(f,"# c7 %lld c6 %lld sym %d\n# columns: a b (Eisenstein a+b*w) u v (integer affine image u=2a-b, v=b)\n",c7,c6,sym);
  for(int i=0;i<N;i++) fprintf(f,"%lld %lld %lld %lld\n",A[i],B[i],2*A[i]-B[i],B[i]);
  fclose(f); rename(tmp,fn);
}
static double now(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec+1e-9*t.tv_nsec; }

int main(int argc,char**argv){
  if(argc<4){ fprintf(stderr,"usage\n"); return 1; }
  uint64_t seed=strtoull(argv[1],0,10); double secs=atof(argv[2]); const char *pre=argv[3];
  if(argc>4) R=atoll(argv[4]);
  ll S1= argc>5? atoll(argv[5]):40000, S2= argc>6? atoll(argv[6]):20000; double W= argc>7? atof(argv[7]):0;
  rs=seed*0x9E3779B97F4A7C15ULL+12345; for(int i=0;i<20;i++) rnd();
  char fbest[512], fbsym[512], flog[512], fnear[512];
  snprintf(fbest,512,"%s_best.txt",pre); snprintf(fbsym,512,"%s_bestsym.txt",pre); snprintf(flog,512,"%s_runs.tsv",pre); snprintf(fnear,512,"%s_near.txt",pre);
  FILE *lg=fopen(flog,"a"); setvbuf(lg,0,_IOLBF,0);
  fprintf(lg,"#W %g S1 %lld S2 %lld\n#restart\tR\tT0",W,S1,S2); fprintf(lg,"\tsym_final\tsym_best\tsym_best_c6\tfree_final\tfree_best\tfree_best_c6\tevals\tsecs\n");
  static ll IA[400][N], IB[400][N]; int ni=0;
  if(argc>8){ FILE *fi=fopen(argv[8],"r"); char ln[512]; int k=-1, use=0; ll c7i;
    while(fi && fgets(ln,sizeof ln,fi)){
      if(ln[0]=='#'){ use = sscanf(ln,"# restart %*d c7 %lld",&c7i)==1 && c7i==3 && ni<400; if(use){ k=0; ni++; } continue; }
      if(use && k<N && sscanf(ln,"%lld %lld",&IA[ni-1][k],&IB[ni-1][k])==2) k++; }
    if(fi) fclose(fi);
    fprintf(lg,"# %d initial sets\n",ni); S1=0; }
  double t0=now(); ll gbest=1LL<<60, gbsym=1LL<<60; ll Abest[N],Bbest[N];
  for(int rest=0; now()-t0<secs; rest++){
    double rt=now(); ll evals=0;
    /* random symmetric start in general position */
    if(ni){ int x=rnd()%ni; memcpy(A,IA[x],sizeof A); memcpy(B,IB[x],sizeof B); full_table(); }
    else do{ for(int r=0;r<K;r++) set_orbit(r,rcoord(),rcoord()); }while(!distinct_ok()||!full_table());
    ll c6,c7; count(&c6,&c7); evals++;
    double T0=pow(10.0,0.3+1.2*urand()), T1=0.05;   /* temperatures in units of c7 */
    ll bc7=c7,bc6=c6; memcpy(Abest,A,sizeof A); memcpy(Bbest,B,sizeof B);
    for(ll st=0; st<S1; st++){
      double fr=(double)st/S1, T=T0*pow(T1/T0,fr);
      int r=rnd()%K; ll oa=A[r],ob=B[r];
      double sig = R*pow(10.0,-urand()*(1.0+4.0*fr)); if(sig<1) sig=1;
      ll na=oa+(ll)llround(sig*(2*urand()-1)), nb=ob+(ll)llround(sig*(2*urand()-1));
      if(na>R||na<-R||nb>R||nb<-R) continue;
      ll sv[3][2]; for(int t=0;t<3;t++){ sv[t][0]=A[r+t*K]; sv[t][1]=B[r+t*K]; }
      set_orbit(r,na,nb);
      int ok=distinct_ok(); if(ok){ for(int t=0;t<3;t++) if(!update_point(r+t*K)) ok=0; }
      ll n6,n7;
      if(ok){ count(&n6,&n7); evals++; }
      if(ok && (n7+W*n6<=c7+W*c6 || urand()<exp(-((n7-c7)+W*(n6-c6))/T))){ c7=n7; c6=n6;
        if(c7<bc7||(c7==bc7&&c6<bc6)){ bc7=c7; bc6=c6; memcpy(Abest,A,sizeof A); memcpy(Bbest,B,sizeof B); }
      } else { for(int t=0;t<3;t++){ A[r+t*K]=sv[t][0]; B[r+t*K]=sv[t][1]; } for(int t=0;t<3;t++) update_point(r+t*K); }
      if(c7==0) break;
    }
    ll symfinal=c7, symb=bc7, symb6=bc6;
    memcpy(A,Abest,sizeof A); memcpy(B,Bbest,sizeof B); full_table(); count(&c6,&c7);
    if(symb<gbsym){ gbsym=symb; save(fbsym,c7,c6,1); }
    if(symb<gbest){ gbest=symb; save(fbest,c7,c6,1); }
    /* symmetry broken phase */
    double T0f=1.0+2.0*urand();
    for(ll st=0; st<S2 && c7>0; st++){
      double fr=(double)st/S2, T=T0f*pow(T1/T0f,fr);
      int q=rnd()%N; ll oa=A[q],ob=B[q];
      double sig = R*pow(10.0,-1.0-urand()*(1.0+3.0*fr)); if(sig<1) sig=1;
      ll na=oa+(ll)llround(sig*(2*urand()-1)), nb=ob+(ll)llround(sig*(2*urand()-1));
      A[q]=na; B[q]=nb;
      int ok=1; for(int i=0;i<N;i++) if(i!=q&&A[i]==na&&B[i]==nb) ok=0;
      if(ok) ok=update_point(q);
      ll n6,n7; if(ok){ count(&n6,&n7); evals++; }
      if(ok && (n7+W*n6<=c7+W*c6 || urand()<exp(-((n7-c7)+W*(n6-c6))/T))){ c7=n7; c6=n6;
        if(c7<bc7||(c7==bc7&&c6<bc6)){ bc7=c7; bc6=c6; memcpy(Abest,A,sizeof A); memcpy(Bbest,B,sizeof B); }
      } else { A[q]=oa; B[q]=ob; update_point(q); }
    }
    ll ffinal=c7;
    if(bc7<=6){ FILE *fn=fopen(fnear,"a");
      if(fn){ fprintf(fn,"# restart %d c7 %lld c6 %lld symbest %lld\n",rest,bc7,bc6,symb);
        for(int i=0;i<N;i++) fprintf(fn,"%lld %lld %lld %lld\n",Abest[i],Bbest[i],2*Abest[i]-Bbest[i],Bbest[i]);
        fclose(fn); } }
    if(bc7<gbest){ memcpy(A,Abest,sizeof A); memcpy(B,Bbest,sizeof B); full_table(); count(&c6,&c7); gbest=c7; save(fbest,c7,c6,0); }
    fprintf(lg,"%d\t%lld\t%.2f\t%lld\t%lld\t%lld\t%lld\t%lld\t%lld\t%lld\t%.1f\n",rest,R,T0,symfinal,symb,symb6,ffinal,bc7,bc6,evals,now()-rt);
    if(gbest==0){ fprintf(lg,"# ZERO FOUND\n"); fclose(lg); return 7; }
  }
  fclose(lg); return 0;
}
