#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using Pt=array<long long,2>;using Pair=array<int,2>;
static signed char s[60][60][60];
static int rankcap[60][60];
void pairout(ostream&o,Pair p){o<<'['<<p[0]<<','<<p[1]<<']';}

bool endpoint_reference(const vector<Pt>&P,Pair p,Pair q){
 if(p==q)return true;
 array<int,4>ids={p[0],p[1],q[0],q[1]};sort(ids.begin(),ids.end());int k=unique(ids.begin(),ids.end())-ids.begin();
 __int128 dxP=P[p[1]][0]-P[p[0]][0],dyP=P[p[1]][1]-P[p[0]][1];
 __int128 dxQ=P[q[1]][0]-P[q[0]][0],dyQ=P[q[1]][1]-P[q[0]][1];
 vector<int>signs;
 for(int j=0;j<k;j++){
  __int128 x=P[ids[j]][0];
  // For |coordinates|<=1e12, magnitude <=24*(1e12)^3<2^127.
  __int128 d=((__int128)P[q[0]][1]*dxQ+dyQ*(x-P[q[0]][0]))*dxP
             -((__int128)P[p[0]][1]*dxP+dyP*(x-P[p[0]][0]))*dxQ;
  signs.push_back(d>0?1:d<0?-1:0);
 }
 if(signs.back()<0)return false;
 for(int j=0;j+1<k;j++)if(signs[j]<=0&&(signs[j]<0||signs.back()>0))return true;
 return false;
}

bool prototype(Pair p,Pair q){
 int b=p[0],c=p[1],u=q[0],v=q[1];
 if(v<c)return false;
 if(p==q)return true;
 if(v>c&&s[b][c][v]<=0)return false;
 if(u>b&&s[b][u][v]<=0)return false;
 if(u<b&&s[u][b][c]>=0)return false;
 return true;
}
int main(int argc,char**argv){
 try{
  if(argc!=3)throw runtime_error("usage: check input output");
  ifstream in(argv[1]);ifstream old(argv[2]);if(old.good())throw runtime_error("output exists");ofstream out(argv[2]);
  string magic;int total;in>>magic>>total;if(magic!="CUPCOMPARE1")throw runtime_error("input magic");
  for(int index=0;index<total;index++){
   string name;int n,m;in>>name>>n>>m;vector<Pt>P(m);for(auto&p:P)in>>p[0]>>p[1];
   if(!in||m>60||m<4)throw runtime_error("input");
   for(int i=0;i<m;i++){
    if(i&&P[i-1][0]>=P[i][0])throw runtime_error("x order");
    for(auto c:P[i])if(c< -1000000000000LL||c>1000000000000LL)throw runtime_error("coordinate bound");
   }
   for(int a=0;a<m;a++)for(int b=a+1;b<m;b++)for(int c=b+1;c<m;c++){
    __int128 d=(__int128)(P[b][0]-P[a][0])*(P[c][1]-P[a][1])-(__int128)(P[b][1]-P[a][1])*(P[c][0]-P[a][0]);if(!d)throw runtime_error("collinear");int z=d>0?1:-1;
    s[a][b][c]=s[b][c][a]=s[c][a][b]=z;s[a][c][b]=s[c][b][a]=s[b][a][c]=-z;
   }
   int maxcap=2;
   for(int b=0;b<m;b++)for(int c=b+1;c<m;c++){
    rankcap[b][c]=2;for(int a=0;a<b;a++)if(s[a][b][c]<0)rankcap[b][c]=max(rankcap[b][c],rankcap[a][b]+1);maxcap=max(maxcap,rankcap[b][c]);
   }
   if(maxcap>=5)throw runtime_error("fivecap");
   vector<Pair>pairs,ambient;
   for(int b=0;b<m;b++)for(int c=b+1;c<m;c++)pairs.push_back({b,c});
   bool E[60][60]={};
   for(int a=0;a<m;a++)for(int b=a+1;b<m;b++)for(int c=b+1;c<m;c++)for(int d=c+1;d<m;d++)
    if(s[a][b][c]<0&&s[a][b][d]<0&&s[a][c][d]<0&&s[b][c][d]<0)E[c][d]=true;
   for(auto p:pairs)if(E[p[0]][p[1]])ambient.push_back(p);
   long long tested=0,terminaltested=0,mismatch=0,trues=0;int protectedpairs=0,protectedterminal=0;
   out<<"{\"name\":\""<<name<<"\",\"m\":"<<m<<",\"n\":"<<n<<",\"mismatches\":[";
   for(auto p:pairs){
    bool any=false;bool terminal=rankcap[p[0]][p[1]]>=3;
    for(auto q:ambient){bool a=prototype(p,q),b=endpoint_reference(P,p,q);tested++;terminaltested+=terminal;trues+=a;any|=a;
     if(a!=b){if(mismatch++)out<<',';out<<"{\"query\":";pairout(out,p);out<<",\"support\":";pairout(out,q);out<<",\"prototype\":"<<(a?"true":"false")<<",\"endpoint\":"<<(b?"true":"false")<<'}';}
    }
    protectedpairs+=any;protectedterminal+=any&&terminal;
   }
   out<<"],\"query_support_comparisons\":"<<tested<<",\"cap_terminal_comparisons\":"<<terminaltested<<",\"true_support_predicates\":"<<trues<<",\"protected_pairs\":"<<protectedpairs<<",\"protected_cap_terminal_pairs\":"<<protectedterminal<<",\"mismatch_count\":"<<mismatch<<"}\n";
  }
 }catch(const exception&e){cerr<<e.what()<<'\n';return 2;}
}
