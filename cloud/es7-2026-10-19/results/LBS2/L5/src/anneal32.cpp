// LBS2 L5 anneal32: simulated annealing of random 32-point integer sets down to
// 0 convex 7-gons. Counting by the bottom-point angular DP (same scheme as
// results/LBS/L1/src/lbs2.cpp, rewritten for N = 32). Moves that create three
// collinear points or leave the box |coord| < 2^26 are rejected.
// When a run reaches c7 = 0 the set is written, then a random walk that keeps
// c7 = 0 writes SNAP further snapshots (every GAP accepted moves), then restart.
// With STARTFILE (one set of 32 or 33 points per line, "x,y" tokens; a random point of a
// 33-point set is dropped) every run starts from a random set of the file at lower temperature.
// Polish: a run whose best is <= 8 restarts up to 4 times from its best set at low temperature.
// Usage: anneal32 SEED SECONDS OUTFILE [STARTFILE]   (appends "seed run snap c7 c6 | x,y ..." lines)
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <algorithm>
#include <random>
#include <chrono>
#include <vector>
#include <string>
typedef long long ll;
const int N = 32;
const ll BOX = 1LL << 26;
struct P { ll x, y; };
static inline ll orient(const P&a,const P&b,const P&c){ return (b.x-a.x)*(c.y-a.y)-(b.y-a.y)*(c.x-a.x); }
static inline bool below(const P&a,const P&b){ return a.y<b.y || (a.y==b.y && a.x<b.x); }
static ll count7(const P* pts, ll* c6out, int ex=-1){
  ll c7=0,c6=0; int idx[N]; ll f[N][N], g[N][N]; static signed char L[N][N][N]; bool cl[N][N];
  for(int p=0;p<N;p++){ if(p==ex) continue;
    int m=0; const P& O=pts[p];
    for(int i=0;i<N;i++) if(i!=p && i!=ex && below(O,pts[i])) idx[m++]=i;
    if(m<5) continue;
    std::sort(idx,idx+m,[&](int a,int b){ return orient(O,pts[a],pts[b])>0; });
    P q[N]; for(int i=0;i<m;i++) q[i]=pts[idx[i]];
    for(int a=0;a<m;a++) for(int b=a+1;b<m;b++){ cl[a][b]=orient(q[a],q[b],O)>0;
      for(int c=b+1;c<m;c++) L[a][b][c]=orient(q[a],q[b],q[c])>0; }
    for(int a=0;a<m;a++) for(int b=0;b<m;b++) f[a][b]=(a<b);
    for(int k=3;k<=6;k++){
      for(int b=0;b<m;b++) for(int c=0;c<m;c++) g[b][c]=0;
      for(int a=0;a<m;a++) for(int b=a+1;b<m;b++){ ll v=f[a][b]; if(!v) continue;
        for(int c=b+1;c<m;c++) if(L[a][b][c]) g[b][c]+=v; }
      memcpy(f,g,sizeof f);
      if(k>=5){ ll s=0; for(int a=0;a<m;a++) for(int b=a+1;b<m;b++) if(f[a][b]&&cl[a][b]) s+=f[a][b];
        if(k==5) c6+=s; else c7+=s; }
    }
  }
  if(c6out) *c6out=c6; return c7;
}
static bool okPoint(const P* pts,int i,const P& q){
  if(q.x<=-BOX||q.x>=BOX||q.y<=-BOX||q.y>=BOX) return false;
  for(int a=0;a<N;a++){ if(a==i) continue; if(pts[a].x==q.x&&pts[a].y==q.y) return false;
    for(int b=a+1;b<N;b++){ if(b==i) continue; if(orient(pts[a],pts[b],q)==0) return false; } }
  return true;
}
int main(int argc,char**argv){
  if(argc<4){ fprintf(stderr,"usage: anneal32 SEED SECONDS OUTFILE\n"); return 1; }
  unsigned seed=atoi(argv[1]); double secs=atof(argv[2]); const char* out=argv[3];
  std::mt19937_64 rng(seed); std::uniform_real_distribution<double> U(0,1); std::normal_distribution<double> G(0,1);
  auto t0=std::chrono::steady_clock::now();
  auto el=[&]{ return std::chrono::duration<double>(std::chrono::steady_clock::now()-t0).count(); };
  P pts[N];
  // optional start file: one set per line, "x,y" tokens (32 or 33 points; for 33 a random point is dropped)
  std::vector<std::vector<P>> starts; int ns=0;
  if(argc>4){ FILE* sf=fopen(argv[4],"r"); char line[1<<16];
    while(sf && fgets(line,sizeof line,sf)){ std::vector<P> v; char* t=strtok(line," \n");
      while(t){ long long x,y; if(sscanf(t,"%lld,%lld",&x,&y)==2) v.push_back({x,y}); t=strtok(nullptr," \n"); }
      bool inbox=true; for(auto&p:v) if(std::llabs(p.x)>=BOX||std::llabs(p.y)>=BOX) inbox=false;
      if((v.size()==32||v.size()==33)&&inbox) starts.push_back(v); }
    if(sf) fclose(sf); ns=starts.size(); fprintf(stderr,"%d start sets\n",ns); if(!ns) return 1; }
  for(int run=0; el()<secs; run++){
    int startid=-1; double R=0; int mode=-1;
    if(ns>0){ startid=rng()%ns; std::vector<P> v=starts[startid]; if(v.size()==33) v.erase(v.begin()+rng()%33);
      for(int i=0;i<N;i++) pts[i]=v[i]; }
    else {
    // start: uniform in a box of random size, or clustered (multi-scale)
      R = std::ldexp(1.0, 14 + (int)(rng()%8)); mode=rng()%3;
    for(int i=0;i<N;i++){ P q; do{
        if(mode==0){ q.x=(ll)((2*U(rng)-1)*R); q.y=(ll)((2*U(rng)-1)*R); }
        else { double s=R*std::pow(2.0,-6*U(rng)); double cx=(2*U(rng)-1)*R, cy=(2*U(rng)-1)*R;
          q.x=(ll)(cx+s*G(rng)); q.y=(ll)(cy+s*G(rng)); }
      } while([&]{ for(int j=0;j<i;j++){ if(pts[j].x==q.x&&pts[j].y==q.y) return true;
          for(int k=j+1;k<i;k++) if(orient(pts[j],pts[k],q)==0) return true; } return false; }());
      pts[i]=q; } }
    // re-validate general position of the start
    bool gp=true; for(int a=0;a<N&&gp;a++) for(int b=a+1;b<N&&gp;b++) for(int c=b+1;c<N;c++) if(orient(pts[a],pts[b],pts[c])==0){gp=false;break;}
    if(!gp) continue;
    ll c6, c7=count7(pts,&c6), best=c7; P bestP[N]; memcpy(bestP,pts,sizeof pts);
    double T0=0.3+3*U(rng), T1=0.02+0.1*U(rng); long steps=200000+rng()%800000;
    if(ns>0){ T0=0.2+0.8*U(rng); steps=100000+rng()%300000; }
    long st=0, total=0; int phase=0;
    for(;;){
      int part[N]; int np=0; long lastp=-1000000;
      for(st=0; st<steps && c7>0 && el()<secs; st++){
        double T=T0*std::pow(T1/T0,(double)st/steps);
        if(c7<=60 && st-lastp>=400){ lastp=st; np=0; for(int j=0;j<N;j++) if(count7(pts,nullptr,j)<c7) part[np++]=j; }
        if(c7>60) np=0;
        int i=(np>0 && (rng()&1)) ? part[rng()%np] : (int)(rng()%N); P q=pts[i];
        // step size: log-uniform relative to distance to nearest other point
        ll dmin=-1; for(int j=0;j<N;j++) if(j!=i){ ll dx=pts[j].x-q.x, dy=pts[j].y-q.y; ll d=std::max(std::llabs(dx),std::llabs(dy)); if(dmin<0||d<dmin) dmin=d; }
        double s=std::max(1.0,(double)dmin*std::pow(2.0,4-12*U(rng)));
        q.x+=(ll)llround(s*G(rng)); q.y+=(ll)llround(s*G(rng));
        if(!okPoint(pts,i,q)) continue;
        P old=pts[i]; pts[i]=q; ll n6, n7=count7(pts,&n6);
        if(n7<=c7 || U(rng)<std::exp(-(double)(n7-c7)/T)){ c7=n7; c6=n6; if(c7<best){ best=c7; memcpy(bestP,pts,sizeof pts);} }
        else pts[i]=old;
      }
      total+=st;
      // polish: restart from the best set at low temperature (up to 4 phases) while best is small
      if(c7==0 || best>8 || phase>=4 || el()>=secs) break;
      phase++; memcpy(pts,bestP,sizeof pts); c7=count7(pts,&c6);
      T0=0.3+0.7*U(rng); T1=0.03+0.05*U(rng); steps=200000+rng()%300000;
    }
    FILE* lg=fopen((std::string(out)+".log").c_str(),"a");
    fprintf(lg,"seed %u run %d R %.0f mode %d T0 %.3f T1 %.3f steps %ld phases %d start %d final %lld best %lld t %.0f\n",seed,run,R,mode,T0,T1,total,phase,startid,c7,best,el()); fclose(lg);
    if(c7!=0) continue;
    // c7 = 0: write, then walk keeping c7 = 0 and write snapshots
    const int SNAP=4, GAP=1500;
    for(int snap=0; snap<=SNAP; snap++){
      if(snap>0){ int acc=0; long tries=0;
        while(acc<GAP && tries<200000 && el()<secs){ tries++;
          int i=rng()%N; P q=pts[i];
          ll dmin=-1; for(int j=0;j<N;j++) if(j!=i){ ll d=std::max(std::llabs(pts[j].x-q.x),std::llabs(pts[j].y-q.y)); if(dmin<0||d<dmin) dmin=d; }
          double s=std::max(1.0,(double)dmin*std::pow(2.0,2-10*U(rng)));
          q.x+=(ll)llround(s*G(rng)); q.y+=(ll)llround(s*G(rng));
          if(!okPoint(pts,i,q)) continue;
          P old=pts[i]; pts[i]=q; ll n6; if(count7(pts,&n6)==0){ acc++; c6=n6; } else pts[i]=old; }
        if(acc<GAP) break; }
      FILE* f=fopen(out,"a"); fprintf(f,"%u %d %d %d 0 %lld |",seed,run,startid,snap,c6);
      for(int i=0;i<N;i++) fprintf(f," %lld,%lld",pts[i].x,pts[i].y); fprintf(f,"\n"); fclose(f);
    }
  }
  return 0;
}
