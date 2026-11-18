#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using Mask = uint64_t;
using Point = array<long long,2>;

// Exact integer encoder; input: m n, then m sorted x y pairs.
// This executable does no SAT solving or certification.
int main(int argc,char**argv) {
  if(argc!=3) { cerr<<"usage: encode input.points output-prefix\n"; return 2; }
  ifstream in(argv[1]); int m,n; in>>m>>n;
  if(!in || m<0 || m>60 || n<4 || n>12) return 2;
  vector<Point> p(m); for(auto &q:p) in>>q[0]>>q[1];
  if(!in) return 2;
  // Bounding coordinates by 1e15 makes every determinant fit in signed 128 bits.
  for(int i=0;i<m;i++) {
    for(auto q:p[i]) if(q < -1000000000000000LL || q>1000000000000000LL) return 2;
    if(i && p[i-1][0]>=p[i][0]) return 2;
  }
  int s[60][60][60]={};
  for(int a=0;a<m;a++) for(int b=a+1;b<m;b++) for(int c=b+1;c<m;c++) {
    __int128 d=(__int128)(p[b][0]-p[a][0])*(p[c][1]-p[a][1])
              -(__int128)(p[b][1]-p[a][1])*(p[c][0]-p[a][0]);
    if(!d) {cerr<<"collinear "<<a<<" "<<b<<" "<<c<<"\n"; return 3;}
    s[a][b][c]=(d>0?1:-1);
  }
  int h[60][60]={}; int maxcap=0;
  for(int b=0;b<m;b++) for(int c=b+1;c<m;c++) {
    h[b][c]=2;
    for(int a=0;a<b;a++) if(s[a][b][c]<0) h[b][c]=max(h[b][c],1+h[a][b]);
    maxcap=max(maxcap,h[b][c]);
  }
  // For each fixed first vertex, longest cap/cup ending in an ordered pair.
  int maxgon=min(m,2);
  for(int first=0;first<m;first++) {
    int d[2][60][60]={}, best[2][60]={};
    for(int j=first+1;j<m;j++) for(int t=0;t<2;t++) d[t][first][j]=best[t][j]=2;
    for(int b=first+1;b<m;b++) for(int c=b+1;c<m;c++) for(int a=first;a<b;a++) {
      int t=s[a][b][c]>0;
      if(d[t][a][b]) d[t][b][c]=max(d[t][b][c],1+d[t][a][b]);
      best[t][c]=max(best[t][c],d[t][b][c]);
    }
    for(int j=first+1;j<m;j++) maxgon=max(maxgon,best[0][j]+best[1][j]-2);
  }
  ofstream geo(string(argv[2])+".geometry.json");
  geo<<"{\n\"label\":\"COMPUTED\",\"m\":"<<m<<",\"n\":"<<n
     <<",\"maxcap\":"<<maxcap<<",\"maxgon\":"<<maxgon<<",\"valid\":"
     <<((maxcap<5 && maxgon<n)?"true":"false");
  if(maxcap>=5 || maxgon>=n) {geo<<"}\n"; return 4;}
  vector<Mask> caps4,bad3,good3;
  for(int a=0;a<m;a++) for(int b=a+1;b<m;b++) for(int c=b+1;c<m;c++) if(s[a][b][c]<0) {
    auto z=(Mask(1)<<a)|(Mask(1)<<b)|(Mask(1)<<c);
    (h[b][c]==3?bad3:good3).push_back(z);
    for(int e=c+1;e<m;e++) if(s[b][c][e]<0) caps4.push_back(z|(Mask(1)<<e));
  }
  using ChainLists = array<vector<Mask>,13>;
  vector<vector<ChainLists>> cup(m,vector<ChainLists>(m)),cap(m,vector<ChainLists>(m));
  auto fill=[&](int sign,int bound,auto &store) {
    function<void(int,int,int,int,Mask)> rec=[&](int first,int a,int b,int len,Mask z) {
      store[first][b][len].push_back(z);
      if(len==bound) return;
      for(int c=b+1;c<m;c++) if(s[a][b][c]==sign) rec(first,b,c,len+1,z|(Mask(1)<<c));
    };
    for(int a=0;a<m;a++) for(int b=a+1;b<m;b++) rec(a,a,b,2,(Mask(1)<<a)|(Mask(1)<<b));
  };
  fill(-1,4,cap); fill(1,n-1,cup);
  set<Mask> polygons;
  for(int a=0;a<m;a++) for(int b=a+1;b<m;b++) for(int clen=2;clen<=4;clen++) {
    int ulen=n+1-clen;
    if(ulen<2 || ulen>n-1) continue;
    for(auto c:cap[a][b][clen]) for(auto u:cup[a][b][ulen]) polygons.insert(c|u);
  }
  auto arr=[&](string key,const auto &zs) {
    geo<<",\n\""<<key<<"\":["; bool comma=false;
    for(Mask z:zs) {if(comma) geo<<",";comma=true;geo<<"[";bool c=false;
      for(int i=0;i<m;i++) if(z&(Mask(1)<<i)) {if(c)geo<<",";c=true;geo<<i;} geo<<"]";}
    geo<<"]";
  };
  arr("fourcaps",caps4); arr("rank3_triples",bad3); arr("rank4_triples",good3); arr("polygons",polygons);
  geo<<",\n\"terminal_ranks\":["; bool comma=false;
  for(int b=0;b<m;b++) for(int c=b+1;c<m;c++) {if(comma)geo<<",";comma=true;geo<<"["<<b<<","<<c<<","<<h[b][c]<<"]";}
  geo<<"]}\n";
  for(bool strong:{false,true}) {
    ofstream cnf(string(argv[2])+(strong?".terminal.cnf":".weak.cnf"));
    cnf<<"c x_i iff point i-1 belongs to A; whole polygon hit\n";
    cnf<<"p cnf "<<m<<" "<<caps4.size()+polygons.size()+(strong?bad3.size():0)<<"\n";
    auto clauses=[&](const auto &zs,int sign) {for(auto z:zs) {for(int i=0;i<m;i++) if(z&(Mask(1)<<i)) cnf<<sign*(i+1)<<" ";cnf<<"0\n";}};
    clauses(caps4,-1); if(strong) clauses(bad3,-1); clauses(polygons,1);
  }
  cout<<"m="<<m<<" n="<<n<<" cap4="<<caps4.size()<<" bad3="<<bad3.size()<<" good3="<<good3.size()<<" polygons="<<polygons.size()<<"\n";
}
