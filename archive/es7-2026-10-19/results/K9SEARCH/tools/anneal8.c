/* 8-fold symmetric nested-orbit annealer: L layers (lr, th), point = e^lr e^{i(th + 2 pi j/8)}.
   cost = number of convex K-gons (float orientation; search only, certification is done separately, exactly).
   usage: anneal8 SEEDCFG L SECONDS RNGSEED OUTCFG [T0]
   SEEDCFG: lines "lr th" (missing layers are filled at random). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>
#define M 8
#ifndef TELE
#define TELE 0.0
#endif
#ifndef MINDET
#define MINDET 1e-9
#endif
#ifndef K
#define K 9
#endif
#define NMAX 160
static int n, L;
static double X[NMAX], Y[NMAX];
static signed char O[NMAX][NMAX][NMAX];
static double lr[32], th[32];
static unsigned long long rs;
static double urand(void){ rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return (rs >> 11) * (1.0/9007199254740992.0);}
static double grand(void){ double u=urand()+1e-300, v=urand(); return sqrt(-2*log(u))*cos(2*M_PI*v);}
static void build(void){
  n = L*M;
  for (int o=0;o<L;o++) for (int j=0;j<M;j++){ double r=exp(lr[o]), a=th[o]+2*M_PI*j/M; X[o*M+j]=r*cos(a); Y[o*M+j]=r*sin(a);} }
static double mindet;
static void otab(void){
  mindet=1e300;
  for (int a=0;a<n;a++) for (int b=a+1;b<n;b++) for (int c=b+1;c<n;c++){
    double d=(X[b]-X[a])*(Y[c]-Y[a])-(Y[b]-Y[a])*(X[c]-X[a]);
    double sc=fabs(X[a])+fabs(Y[a])+fabs(X[b])+fabs(Y[b])+fabs(X[c])+fabs(Y[c]);
    double rd=fabs(d)/(sc*sc); if (rd<mindet) mindet=rd;
    signed char s = d>0?1:-1;
    O[a][b][c]=O[b][c][a]=O[c][a][b]=s; O[b][a][c]=O[a][c][b]=O[c][b][a]=-s; } }
/* count convex K-gons: anchor = lowest (y, then x) vertex */
static long long cnt[NMAX][NMAX][K+1];
static double count_k(void){
  double total=0;
  int q[NMAX]; double ang[NMAX];
  for (int p=0;p<n;p++){
    int r=0;
    for (int i=0;i<n;i++) if (i!=p && (Y[i]>Y[p] || (Y[i]==Y[p] && X[i]>X[p]))) { q[r]=i; ang[r]=atan2(Y[i]-Y[p], X[i]-X[p]); r++; }
    if (r < K-1) continue;
    /* sort by angle */
    for (int i=1;i<r;i++){ int t=q[i]; double a=ang[i]; int j=i-1; while(j>=0 && ang[j]>a){ q[j+1]=q[j]; ang[j+1]=ang[j]; j--; } q[j+1]=t; ang[j+1]=a; }
    for (int i=0;i<r;i++) for (int j=i+1;j<r;j++){ memset(cnt[i][j],0,sizeof(long long)*(K+1)); cnt[i][j][3]=1; }
    for (int j=1;j<r;j++){
      int qj=q[j];
      for (int i=0;i<j;i++){
        long long *c=cnt[i][j]; int qi=q[i];
        /* close */
        if (c[K] && O[qi][qj][p]>0) total += c[K];
        int any=0; for (int l=3;l<K;l++) if (c[l]) { any=1; break; }
        if (!any) continue;
        for (int k=j+1;k<r;k++) if (O[qi][qj][q[k]]>0){
          long long *d=cnt[j][k];
          for (int l=3;l<K;l++) d[l+1]+=c[l];
        }
      }
    }
  }
  return total;
}
static double cost(void){ build(); otab(); double c=count_k(); if (mindet<MINDET) c += 1e6; return c; }
int main(int argc, char **argv){
  if (argc<6){ fprintf(stderr,"usage\n"); return 1; }
  L=atoi(argv[2]); double secs=atof(argv[3]); rs=strtoull(argv[4],0,10)*2654435761ULL+12345; for(int i=0;i<10;i++) urand();
  double T0 = argc>6? atof(argv[6]) : 0.5;
  int got=0; FILE *f=fopen(argv[1],"r"); char line[256];
  while (f && fgets(line,sizeof line,f)){ if(line[0]=='#') continue; double a,b; if (sscanf(line,"%lf %lf",&a,&b)==2 && got<L){ lr[got]=a; th[got]=b; got++; } }
  if (f) fclose(f);
  if (getenv("DEL")){ double c0=cost(); printf("full L=%d cost %.0f\n",L,c0); double sl[32],st[32]; memcpy(sl,lr,sizeof sl); memcpy(st,th,sizeof st);
    for (int o=0;o<L;o++){ int q=0; for (int i=0;i<L;i++) if(i!=o){ lr[q]=sl[i]; th[q]=st[i]; q++; } L--; double cc=cost(); L++; printf("del layer %d (lr %.6f) cost %.0f\n",o,sl[o],cc); memcpy(lr,sl,sizeof sl); memcpy(th,st,sizeof st);} return 0; }
  if (getenv("GRID")){ double A,B; int NA,NT; sscanf(getenv("GRID"),"%lf %lf %d %d",&A,&B,&NA,&NT); double bc=1e300;
    for (int a=0;a<NA;a++) for (int t=0;t<NT;t++){ lr[got]=A+(B-A)*(a+0.5)/NA; th[got]=2*M_PI/M*(t+0.37)/NT;
      double cc=cost(); printf("%d %d %.0f %.3g %.17g %.17g\n",a,t,cc,mindet,lr[got],th[got]); fflush(stdout);
      if (cc<bc){ bc=cc; FILE *g=fopen(argv[5],"w"); fprintf(g,"# cost %.0f L %d\n",bc,L); for(int i=0;i<L;i++) fprintf(g,"%.17g %.17g\n",lr[i],th[i]); fclose(g);} }
    return 0; }
  if (getenv("SCAN")){ /* targeted insertion scan near each existing layer */
    double sc[7]={1e-4,3e-4,1e-3,3e-3,1e-2,3e-2,1e-1}; double bc=1e300;
    for (int o=0;o<got;o++) for (int si=0;si<7;si++) for (int d=0;d<8;d++){
      lr[got]=lr[o]+sc[si]*cos(2*M_PI*d/8+0.3); th[got]=th[o]+sc[si]*sin(2*M_PI*d/8+0.3);
      double cc=cost(); printf("%d %g %d %.0f %.3g %.17g %.17g\n",o,sc[si],d,cc,mindet,lr[got],th[got]); fflush(stdout);
      if (cc<bc){ bc=cc; FILE *g=fopen(argv[5],"w"); fprintf(g,"# cost %.0f L %d\n",bc,L); for(int i=0;i<L;i++) fprintf(g,"%.17g %.17g\n",lr[i],th[i]); fclose(g);} }
    return 0; }
  double lo=1e9,hi=-1e9; for(int o=0;o<got;o++){ if(lr[o]<lo)lo=lr[o]; if(lr[o]>hi)hi=lr[o]; }
  double c=1e300;
  if (got<L){ double bl=0,bt=0; for (int tr=0;tr<40;tr++){ for (int o=got;o<L;o++){ lr[o]=lo-1+urand()*(hi-lo+1.5); th[o]=urand()*2*M_PI/M; }
      double cc=cost(); fprintf(stderr,"ins %d lr %.4f th %.4f cost %.0f\n",tr,lr[got],th[got],cc); if(cc<c){c=cc; bl=lr[got]; bt=th[got];} }
    lr[got]=bl; th[got]=bt; }
  c=cost(); double best=c; double blr[32], bth[32]; memcpy(blr,lr,sizeof lr); memcpy(bth,th,sizeof th);
  fprintf(stderr,"start cost %.0f mindet %.3g\n", c, mindet);
  time_t t0=time(0); long it=0;
  double lc = log1p(c/8);
  while (difftime(time(0),t0) < secs && best>0){
    it++; if (it%2000==0) fprintf(stderr,"status it %ld t %.0f cur %.0f best %.0f\n",it,difftime(time(0),t0),c,best);
    double frac = difftime(time(0),t0)/secs; double T = T0*(1-frac)+0.02;
    int o = (int)(urand()*L); double slr=lr[o], sth=th[o];
    double sz = pow(10, -1-3*urand());
    int mv = urand()<0.5;
    if (mv==0) lr[o] += sz*grand(); else th[o] += sz*grand();
    if (urand()<0.2){ lr[o] += sz*grand(); th[o]+=sz*grand(); }
    if (urand()<TELE){ int o2=(int)(urand()*L); if (o2!=o){ double s2=pow(10,-1.5-2.5*urand()); lr[o]=lr[o2]+s2*grand(); th[o]=th[o2]+s2*grand(); } }
    double nc=cost(); double nl=log1p(nc/8);
    if (nl<=lc || urand()<exp(-(nl-lc)/T)){ c=nc; lc=nl; if (c<best){ best=c; memcpy(blr,lr,sizeof lr); memcpy(bth,th,sizeof th);
          FILE *g=fopen(argv[5],"w"); fprintf(g,"# cost %.0f L %d\n",best,L); for(int i=0;i<L;i++) fprintf(g,"%.17g %.17g\n",blr[i],bth[i]); fclose(g);
          fprintf(stderr,"it %ld t %.0f best %.0f mindet %.3g\n", it, difftime(time(0),t0), best, mindet); } }
    else { lr[o]=slr; th[o]=sth; }
  }
  fprintf(stderr,"done it %ld best %.0f\n", it, best);
  FILE *g=fopen(argv[5],"w"); fprintf(g,"# cost %.0f L %d\n",best,L); for(int i=0;i<L;i++) fprintf(g,"%.17g %.17g\n",blr[i],bth[i]); fclose(g);
  return 0;
}
