// LBS L1: simulated annealing over 33 integer points, minimizing the number of
// 7-point subsets in convex position (strategy "random": many restarts from
// random sets with varied temperature schedules). Moves creating three
// collinear points are rejected.
// Counting: for each bottom point p, sort points above p by angle and count
// convex chains p,a1..a6 (all left turns, closing turn at a6 checked) by DP.
// lbs2: when the count is small, half the moves pick a point lying in a convex
// 7-gon (participation = c7 - c7 without the point); runs ending with best<=3
// get a low-temperature polish phase from their best set.
// Usage: lbs2 SEED SECONDS OUTPREFIX
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <cmath>
#include <cstring>
#include <ctime>
#include <algorithm>
#include <random>
#include <chrono>
typedef long long ll;
const int N = 33;
struct P { ll x, y; };
static inline ll orient(const P&a,const P&b,const P&c){ return (b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x); }
static inline bool below(const P&a,const P&b){ return a.y<b.y || (a.y==b.y && a.x<b.x); }

// returns c7, sets c6
static ll countConvex(const P* pts, ll* c6out, int ex=-1){
  ll c7=0,c6=0;
  static thread_local int idx[N]; static thread_local ll f[N][N], g[N][N];
  static thread_local signed char L[N][N][N];
  for(int p=0;p<N;p++){ if(p==ex) continue;
    int m=0; const P& O=pts[p];
    for(int i=0;i<N;i++) if(i!=p && i!=ex && below(O,pts[i])) idx[m++]=i;
    if(m<5) continue;
    std::sort(idx,idx+m,[&](int a,int b){ return orient(O,pts[a],pts[b])>0; });
    P q[N]; for(int i=0;i<m;i++) q[i]=pts[idx[i]];
    for(int a=0;a<m;a++) for(int b=a+1;b<m;b++) for(int c=b+1;c<m;c++) L[a][b][c]= orient(q[a],q[b],q[c])>0;
    bool closeL[N][N];
    for(int a=0;a<m;a++) for(int b=a+1;b<m;b++) closeL[a][b]= orient(q[a],q[b],O)>0;
    for(int a=0;a<m;a++) for(int b=0;b<m;b++) f[a][b]= (a<b);
    // f = chains with k non-p vertices ending a->b; k=2
    for(int k=3;k<=6;k++){
      for(int b=0;b<m;b++) for(int c=0;c<m;c++) g[b][c]=0;
      for(int a=0;a<m;a++) for(int b=a+1;b<m;b++){ ll v=f[a][b]; if(!v) continue;
        for(int c=b+1;c<m;c++) if(L[a][b][c]) g[b][c]+=v; }
      memcpy(f,g,sizeof(f));
      if(k>=5){ ll s=0; for(int a=0;a<m;a++) for(int b=a+1;b<m;b++) if(f[a][b] && closeL[a][b]) s+=f[a][b];
        if(k==5) c6+=s; else c7+=s; }
    }
  }
  if(c6out) *c6out=c6; return c7;
}
static bool okPoint(const P* pts,int i,const P& q,int n=N){
  for(int a=0;a<n;a++){ if(a==i) continue; if(pts[a].x==q.x&&pts[a].y==q.y) return false;
    for(int b=a+1;b<n;b++){ if(b==i) continue; if(orient(pts[a],pts[b],q)==0) return false; } }
  return true;
}
int main(int argc,char**argv){
  unsigned seed=atoi(argv[1]); double secs=atof(argv[2]); const char* pre=argv[3];
  std::mt19937_64 rng(seed); std::uniform_real_distribution<double> U(0,1); std::normal_distribution<double> G(0,1);
  auto t0=std::chrono::steady_clock::now();
  auto el=[&]{ return std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count(); };
  char fn[512]; snprintf(fn,512,"%s.runs.txt",pre); FILE* runs=fopen(fn,"a");
  ll globalBest=-1; int run=0;
  if(argc>4){ P t[N]; ll c6; for(int i=0;i<N;i++) t[i]={ (ll)(i*i*7919%1000003), (ll)(i*104729%999983)}; 
    double s=el(); int it=0; while(el()-s<2){ countConvex(t,&c6); it++; } printf("evals/s %.1f\n",it/2.0); return 0; }
  while(el()<secs){
    run++;
    // random start
    ll R = 1LL<<(14+rng()%14); int dist=rng()%3;
    P pts[N];
    for(int i=0;i<N;i++){ P q; do{
        if(dist==0){ q={(ll)(U(rng)*R),(ll)(U(rng)*R)}; }
        else if(dist==1){ double r=sqrt(U(rng))*R/2, th=U(rng)*2*M_PI; q={(ll)(R/2+r*cos(th)),(ll)(R/2+r*sin(th))}; }
        else { q={(ll)(R/2+G(rng)*R/8),(ll)(R/2+G(rng)*R/8)}; }
      } while(!okPoint(pts,i,q,i));
      pts[i]=q; }
    ll c6; ll c7=countConvex(pts,&c6);
    double lam = (rng()%3==0)?0.0:((rng()%2)?0.001:0.01);
    double T0 = pow(10, U(rng)*2.5), T1 = 0.05+U(rng)*0.3;
    long steps = (long)(pow(10, 4.3+U(rng)*1.4));
    double cur = c7 + lam*c6; ll best7=c7; P bestP[N]; memcpy(bestP,pts,sizeof(pts));
    int hot[N]; int nh=-1; // points in some convex 7-gon, valid when nh>=0
    auto anneal=[&](long steps,double T0,double T1){
      for(long s=0;s<steps && el()<secs;s++){
        double T = T0*pow(T1/T0,(double)s/steps);
        if(c7<=12 && nh<0){ nh=0; for(int j=0;j<N;j++){ if(countConvex(pts,nullptr,j)<c7) hot[nh++]=j; } }
        int i = (c7<=12 && nh>0 && U(rng)<0.5) ? hot[rng()%nh] : (int)(rng()%N); P q;
        double u=U(rng);
        if(u<0.05) q={(ll)(U(rng)*R),(ll)(U(rng)*R)};
        else { double sc = R*pow(10,-U(rng)*3.5); q={pts[i].x+(ll)llround(G(rng)*sc), pts[i].y+(ll)llround(G(rng)*sc)}; }
        if(q.x< -(R<<1) || q.y< -(R<<1) || q.x> (R<<2) || q.y> (R<<2)) continue;
        if(!okPoint(pts,i,q)) continue;
        P old=pts[i]; pts[i]=q; ll n6; ll n7=countConvex(pts,&n6); double nv=n7+lam*n6;
        if(nv<=cur || U(rng)<exp(-(nv-cur)/T)){ cur=nv; if(n7!=c7) nh=-1; c7=n7; c6=n6;
          if(c7<best7){ best7=c7; memcpy(bestP,pts,sizeof(pts)); if(c7==0) return; } }
        else pts[i]=old;
      }
    };
    anneal(steps,T0,T1);
    if(best7>0 && best7<=3){ memcpy(pts,bestP,sizeof(pts)); c7=countConvex(pts,&c6); if(lam==0) lam=0.001; cur=c7+lam*c6; nh=-1;
      anneal(300000,0.6,0.1); }
    ll b6; ll b7=countConvex(bestP,&b6);
    fprintf(runs,"run %d R %lld dist %d T0 %.3f T1 %.3f steps %ld lam %.3f final %lld best %lld best6 %lld t %.0f\n",run,R,dist,T0,T1,steps,lam,c7,b7,b6,el()); fflush(runs);
    if(globalBest<0 || b7<globalBest){ globalBest=b7; snprintf(fn,512,"%s.best.txt",pre); FILE* o=fopen(fn,"w");
      fprintf(o,"# c7 %lld c6 %lld seed %u run %d\n",b7,b6,seed,run); for(int i=0;i<N;i++) fprintf(o,"%lld %lld\n",bestP[i].x,bestP[i].y); fclose(o); }
    if(b7==0){ fprintf(runs,"ZERO FOUND\n"); fflush(runs); return 0; }
  }
  return 0;
}
