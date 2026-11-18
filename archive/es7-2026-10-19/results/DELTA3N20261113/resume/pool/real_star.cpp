// Exact integer finder for a maximal four-cap-free subset missing a hexagon.
// Sampling is HEURISTIC; any reported coordinate witness needs independent audit.
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <numeric>
#include <random>
#include <stdexcept>
#include <vector>
using M=uint64_t;
struct P{long long x,y;};
static int sgn(const std::vector<P>&p,int a,int b,int c){
 __int128 d=(__int128(p[b].x)-p[a].x)*(p[c].y-p[a].y)-(__int128(p[b].y)-p[a].y)*(p[c].x-p[a].x);
 return(d>0)-(d<0);
}
static void js(M a){std::cout<<'[';bool first=true;for(int i=0;i<63;++i)if(a>>i&1){if(!first)std::cout<<',';first=false;std::cout<<i;}std::cout<<']';}
int main(int argc,char**argv){
 try{
  if(argc!=2)throw std::runtime_error("input pool required");
  std::ifstream in(argv[1]);std::string magic;int version,count;in>>magic>>version>>count;
  if(magic!="D3POOL"||version!=1)throw std::runtime_error("bad pool");
  std::mt19937_64 rng(20261114);auto start=std::chrono::steady_clock::now();
  for(int z=0;z<count;++z){
   int m;in>>m;if(m<6||m>40)throw std::runtime_error("size");std::vector<P>p(m);
   for(auto&q:p){in>>q.x>>q.y;if(std::abs(q.x)>1000000000000000LL||std::abs(q.y)>1000000000000000LL)throw std::runtime_error("coordinate bound");}
   std::vector<M>caps,gons;std::vector<std::vector<M>>incident(m);
   for(int a=0;a<m;++a)for(int b=a+1;b<m;++b)for(int c=b+1;c<m;++c){
    if(!sgn(p,a,b,c))throw std::runtime_error("collinear");
    for(int d=c+1;d<m;++d)if(sgn(p,a,b,c)<0&&sgn(p,b,c,d)<0){
     M k=(M(1)<<a)|(M(1)<<b)|(M(1)<<c)|(M(1)<<d);caps.push_back(k);
     for(int i:{a,b,c,d})incident[i].push_back(k^(M(1)<<i));
    }
   }
   std::vector<int>v;
   auto choose=[&](auto&&self,int next)->void{
    if(v.size()==6){
     std::vector<int>lo,hi;
     for(int i:v){while(lo.size()>1&&sgn(p,lo[lo.size()-2],lo.back(),i)<0)lo.pop_back();lo.push_back(i);}
     for(auto it=v.rbegin();it!=v.rend();++it){int i=*it;while(hi.size()>1&&sgn(p,hi[hi.size()-2],hi.back(),i)<0)hi.pop_back();hi.push_back(i);}
     if(lo.size()+hi.size()-2==6){M g=0;for(int i:v)g|=M(1)<<i;gons.push_back(g);}return;
    }
    for(int i=next;i<=m-int(6-v.size());++i){v.push_back(i);self(self,i+1);v.pop_back();}
   };choose(choose,0);
   std::vector<int>order(m);std::iota(order.begin(),order.end(),0);
   for(int trial=0;trial<2000;++trial){
    if(std::chrono::duration<double>(std::chrono::steady_clock::now()-start).count()>15){std::cout<<"{\"status\":\"TIME_LIMIT\"}\n";return 0;}
    std::shuffle(order.begin(),order.end(),rng);M red=0;
    for(int i:order){bool blocked=false;for(M a:incident[i])if((red&a)==a){blocked=true;break;}if(!blocked)red|=M(1)<<i;}
    for(M h:gons)if(!(h&red)){
     std::cout<<"{\"status\":\"COORDINATE_CANDIDATE\",\"pool_index\":"<<z<<",\"trial\":"<<trial<<",\"m\":"<<m<<",\"n\":7,\"red\":";js(red);
     std::cout<<",\"blue_target\":";js(h);std::cout<<",\"P\":[";
     for(int i=0;i<m;++i){if(i)std::cout<<',';std::cout<<'['<<p[i].x<<','<<p[i].y<<']';}std::cout<<"]}\n";return 0;
    }
   }
   std::cout<<"{\"status\":\"NO_HIT_IN_SAMPLE\",\"pool_index\":"<<z<<",\"m\":"<<m<<",\"trials\":2000,\"fourcaps\":"<<caps.size()<<",\"hexagons\":"<<gons.size()<<"}\n";
  }
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
