// Exact coordinate geometry for the uniform-envelope search. No SAT calls.
// Input m n followed by x,y integers. Output is a single JSON packet.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstring>
#include <fstream>
#include <functional>
#include <iostream>
#include <set>
#include <stdexcept>
#include <vector>
using namespace std;
using Mask=uint64_t;
using Point=array<long long,2>;
static signed char orient[60][60][60];
static int d[2][60][60],best[2][60];
static constexpr size_t ROW_LIMIT=2000000;

int main(int argc,char**argv){
 try {
  if(argc!=2)throw runtime_error("usage: geometry input.points");
  ifstream in(argv[1]);int m,n;in>>m>>n;
  if(!in||m<2||m>60||n<4||n>12)throw runtime_error("parameters");
  vector<Point>P(m);for(auto&q:P)in>>q[0]>>q[1];
  if(!in)throw runtime_error("truncated input");
  string extra;if(in>>extra)throw runtime_error("trailing input");
  for(int a=0;a<m;a++){
   for(auto c:P[a])if(c < -1000000000000000LL || c>1000000000000000LL)throw runtime_error("coordinate bound 1e15");
   if(a&&P[a-1][0]>=P[a][0])throw runtime_error("x order");
   for(int b=a+1;b<m;b++)for(int c=b+1;c<m;c++){
    __int128 z=(__int128)(P[b][0]-P[a][0])*(P[c][1]-P[a][1])-(__int128)(P[b][1]-P[a][1])*(P[c][0]-P[a][0]);
    if(!z)throw runtime_error("collinear triple");
    orient[a][b][c]=(z>0?1:-1);
   }
  }
  int maxcap=2,maxcup=2,maxgon=2;
  for(int first=0;first<m;first++){
   memset(d,0,sizeof(d));memset(best,0,sizeof(best));
   for(int b=first+1;b<m;b++)for(int t=0;t<2;t++)d[t][first][b]=best[t][b]=2;
   for(int b=first+1;b<m;b++)for(int c=b+1;c<m;c++)for(int a=first;a<b;a++){
    int t=orient[a][b][c]>0;
    if(d[t][a][b])d[t][b][c]=max(d[t][b][c],1+d[t][a][b]);
    best[t][c]=max(best[t][c],d[t][b][c]);
   }
   for(int b=first+1;b<m;b++){
    maxcap=max(maxcap,best[0][b]);maxcup=max(maxcup,best[1][b]);
    maxgon=max(maxgon,best[0][b]+best[1][b]-2);
   }
  }
  bool valid=maxcap<5&&maxgon<n;
  cout<<"{\"m\":"<<m<<",\"n\":"<<n<<",\"maxcap\":"<<maxcap<<",\"maxcup\":"<<maxcup<<",\"maxgon\":"<<maxgon<<",\"valid\":"<<(valid?"true":"false");
  if(!valid){cout<<"}\n";return 4;}
  vector<Mask>c3,c4;
  for(int a=0;a<m;a++)for(int b=a+1;b<m;b++)for(int c=b+1;c<m;c++)if(orient[a][b][c]<0){
   Mask z=(Mask(1)<<a)|(Mask(1)<<b)|(Mask(1)<<c);c3.push_back(z);
   for(int e=c+1;e<m;e++)if(orient[b][c][e]<0)c4.push_back(z|(Mask(1)<<e));
  }
  using Lists=array<vector<Mask>,13>;
  vector<vector<Lists>>cups(m,vector<Lists>(m)),caps(m,vector<Lists>(m));
  size_t chains=0;
  auto enumerate=[&](int sign,int bound,auto&store){
   function<void(int,int,int,int,Mask)>visit=[&](int first,int a,int b,int len,Mask z){
    if(++chains>ROW_LIMIT)throw runtime_error("chain resource guard");
    store[first][b][len].push_back(z);
    if(len<bound)for(int c=b+1;c<m;c++)if(orient[a][b][c]==sign)visit(first,b,c,len+1,z|(Mask(1)<<c));
   };
   for(int a=0;a<m;a++)for(int b=a+1;b<m;b++)visit(a,a,b,2,(Mask(1)<<a)|(Mask(1)<<b));
  };
  enumerate(-1,4,caps);enumerate(1,n-1,cups);
  set<Mask>targets;
  for(int a=0;a<m;a++)for(int b=a+1;b<m;b++)for(int c=2;c<=4;c++){
   int u=n+1-c;if(u<2||u>n-1)continue;
   for(Mask x:caps[a][b][c])for(Mask y:cups[a][b][u]){
    if(__builtin_popcountll(x|y)!=n-1)throw runtime_error("chain overlap");
    targets.insert(x|y);if(targets.size()>ROW_LIMIT)throw runtime_error("target resource guard");
   }
  }
  auto rows=[&](const char*name,const auto&sets){
   cout<<",\""<<name<<"\":[";bool first=true;
   for(Mask z:sets){if(!first)cout<<",";first=false;cout<<"[";bool j=true;
    for(int i=0;i<m;i++)if(z&(Mask(1)<<i)){if(!j)cout<<",";j=false;cout<<i;}
    cout<<"]";
   }cout<<"]";
  };
  rows("caps3",c3);rows("caps4",c4);rows("targets",targets);
  cout<<",\"chains\":"<<chains<<"}\n";
 }catch(const exception&e){cerr<<e.what()<<"\n";return 2;}
}
