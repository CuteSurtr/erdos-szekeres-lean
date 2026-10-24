/* sigverify: read N and X(i,j,k) (lex order of i<j<k, 1-based points) as 0/1 from stdin.
   Checks signotope axioms (every 4-tuple: <=1 sign change in abc,abd,acd,bcd) and counts
   K-subsets in convex position, where p is inside triangle abc iff chi(a,b,p)=chi(b,c,p)=chi(c,a,p)
   (alternating extension of X).  usage: sigverify K < x.txt   prints violations and K-gon count (capped). */
#include <stdio.h>
#include <stdlib.h>
int N, K; static signed char X[64][64][64]; static unsigned char in[64][64][64][64/8+1];
long cnt = 0, cap = 1000000; int S[16];
static int chi(int a,int b,int c){return X[a][b][c];}
static int inside(int p,int a,int b,int c){int s1=chi(a,b,p),s2=chi(b,c,p),s3=chi(c,a,p);return s1==s2&&s2==s3;}
static int ok_add(int n,int q){ /* S[0..n-1] convex; adding q keeps convex? */
  for(int i=0;i<n;i++)for(int j=i+1;j<n;j++)for(int k=j+1;k<n;k++){
    if(inside(q,S[i],S[j],S[k]))return 0;}
  for(int p=0;p<n;p++)for(int i=0;i<n;i++)if(i!=p)for(int j=i+1;j<n;j++)if(j!=p){
    if(inside(S[p],S[i],S[j],q))return 0;}
  return 1;}
static void dfs(int n,int start){ if(cnt>=cap)return; if(n==K){cnt++; if(cnt==1){printf("first gon:");for(int i=0;i<K;i++)printf(" %d",S[i]);printf("\n");}return;}
  for(int q=start;q<=N-(K-n);q++){ if(ok_add(n,q)){S[n]=q;dfs(n+1,q+1);} } }
int main(int argc,char**argv){K=atoi(argv[1]); if(scanf("%d",&N)!=1)return 1;
  for(int i=0;i<N;i++)for(int j=i+1;j<N;j++)for(int k=j+1;k<N;k++){int v;if(scanf("%d",&v)!=1)return 1;int s=v?1:-1;
    X[i][j][k]=s;X[j][k][i]=s;X[k][i][j]=s;X[j][i][k]=-s;X[i][k][j]=-s;X[k][j][i]=-s;}
  long viol=0;
  for(int a=0;a<N;a++)for(int b=a+1;b<N;b++)for(int c=b+1;c<N;c++)for(int d=c+1;d<N;d++){
    int s[4]={X[a][b][c],X[a][b][d],X[a][c][d],X[b][c][d]};int ch=0;for(int t=0;t<3;t++)if(s[t]!=s[t+1])ch++;
    if(ch>1)viol++;}
  printf("signotope_violations %ld\n",viol);
  dfs(0,0); printf("convex_%d_subsets %ld%s\n",K,cnt,cnt>=cap?" (capped)":"");
  return 0;}
