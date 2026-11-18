// Fixed-realization subset finder. Native negative results are NOT certificates.
#include <algorithm>
#include <array>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <functional>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
#include <fcntl.h>
#include <unistd.h>
using M=uint32_t;using Wide=__int128_t;using Clock=std::chrono::steady_clock;
struct P{int64_t x,y;};
Wide det(P a,P b,P c){return (Wide(b.x)-a.x)*(Wide(c.y)-a.y)-(Wide(b.y)-a.y)*(Wide(c.x)-a.x);}
int pop(M z){return __builtin_popcount(z);}int first(M z){return __builtin_ctz(z);}
std::vector<int> verts(M z){std::vector<int>r;for(;z;z&=z-1)r.push_back(first(z));return r;}
template<class F>void choose(M universe,int k,F f){
 auto rec=[&](auto&&self,M rem,int left,M z)->void{if(!left){f(z);return;}while(pop(rem)>=left){M b=rem&-rem;rem^=b;self(self,rem,left-1,z|b);}};rec(rec,universe,k,0);
}
struct Stop{};struct Unknown{};
struct Solver{
 const std::vector<M>&pos;const std::vector<M>&neg;Clock::time_point end;uint64_t nodes=0,limit;M model=0;
 bool solve(M t=0,M f=0){
  if(Clock::now()>=end)throw Stop{};if(++nodes>limit)throw Unknown{};
  for(;;){M ot=t,of=f;
   for(M c:neg){if(c&f)continue;M r=c&~t;if(!r)return false;if(!(r&(r-1)))f|=r;}
   for(M c:pos){if(c&t)continue;M r=c&~f;if(!r)return false;if(!(r&(r-1)))t|=r;}
   if(t&f)return false;if(t==ot&&f==of)break;
  }
  M choice=0;int width=33;
  for(M c:pos)if(!(c&t)){M r=c&~f;if(pop(r)<width){width=pop(r);choice=r;}}
  if(!choice){model=t;return true;}
  std::array<unsigned,32>d{};
  for(M c:pos)if(!(c&t))for(M r=c&choice;r;r&=r-1)++d[first(r)];
  int v=first(choice);for(M r=choice;r;r&=r-1)if(d[first(r)]>d[v])v=first(r);
  return solve(t|(M(1)<<v),f)||solve(t,f|(M(1)<<v));
 }
};
int main(int argc,char**argv){try{
 if(argc!=8)throw std::runtime_error("input.points out.jsonl first_size last_size seconds maxcases node_limit");
 std::ifstream in(argv[1]);int m,n;in>>m>>n;if(!in||m>24||m<7||n<5||n>8)throw std::runtime_error("domain");
 std::vector<P>p(m);for(auto&q:p)in>>q.x>>q.y;if(!in)throw std::runtime_error("points");
 for(int i=0;i<m;++i){if(std::abs(p[i].x)>1000000000000000LL||std::abs(p[i].y)>1000000000000000LL||(i&&p[i-1].x>=p[i].x))throw std::runtime_error("coordinate_bound");}
 M all=(M(1)<<m)-1;int signs[24][24][24]={};
 choose(all,3,[&](M s){auto v=verts(s);auto d=det(p[v[0]],p[v[1]],p[v[2]]);if(!d)throw std::runtime_error("collinear");signs[v[0]][v[1]][v[2]]=d>0?1:-1;});
 auto iscap=[&](M s){bool good=true;choose(s,3,[&](M t){auto v=verts(t);if(signs[v[0]][v[1]][v[2]]>0)good=false;});return good;};
 auto convex=[&](M s){auto v=verts(s);std::vector<int>h;
  for(int i:v){while(h.size()>=2&&det(p[h[h.size()-2]],p[h.back()],p[i])<=0)h.pop_back();h.push_back(i);}
  size_t low=h.size();for(int j=int(v.size())-2;j>=0;--j){int i=v[j];while(h.size()>low&&det(p[h[h.size()-2]],p[h.back()],p[i])<=0)h.pop_back();h.push_back(i);}
  return h.size()==v.size()+1;
 };
 bool valid=true;choose(all,5,[&](M s){if(iscap(s))valid=false;});choose(all,n,[&](M s){if(convex(s))valid=false;});if(!valid)throw std::runtime_error("invalid_ambient");
 std::vector<M>targets,caps,triples;std::array<std::vector<M>,24*24>witness;
 choose(all,n-1,[&](M s){if(convex(s))targets.push_back(s);});
 choose(all,4,[&](M s){if(iscap(s)){caps.push_back(s);auto v=verts(s);witness[v[2]*24+v[3]].push_back(s);}});
 choose(all,3,[&](M s){if(iscap(s))triples.push_back(s);});
 FILE*out=std::fopen(argv[2],"wx");if(!out)throw std::runtime_error("output_exists_or_open_failed");
 int high=std::stoi(argv[3]),low=std::stoi(argv[4]);auto begin=Clock::now(),end=begin+std::chrono::seconds(std::stoi(argv[5]));uint64_t maxcases=std::stoull(argv[6]),node_limit=std::stoull(argv[7]),cases=0,sats=0,unsats=0,unknown=0,nodes=0;std::string stop="COMPLETE";
 auto flush=[&](){if(std::fflush(out)||::fdatasync(fileno(out)))throw std::runtime_error("flush");::posix_fadvise(fileno(out),0,0,POSIX_FADV_DONTNEED);};
 try{for(int size=high;size>=low;--size){
  if(size<0||size>m)throw std::runtime_error("size");uint64_t before=cases;
  choose(all,size,[&](M W){
   if(cases>=maxcases){stop="CASE_LIMIT";throw Stop{};}if(Clock::now()>=end){stop="DEADLINE";throw Stop{};}
   std::vector<M>pos,neg;for(M h:targets)if((h&W)==h)pos.push_back(h);
   for(M t:triples)if((t&W)==t){auto v=verts(t);bool seen=false;for(M c:witness[v[1]*24+v[2]])if((c&W)==c){seen=true;break;}if(!seen)neg.push_back(t);}
   Solver s{pos,neg,end,0,node_limit,0};int verdict=0;
   try{verdict=s.solve()?1:-1;}catch(const Unknown&){verdict=0;}
   ++cases;nodes+=s.nodes;
   if(verdict==1){++sats;M A=s.model;if(A&~W)throw std::runtime_error("outside_model");for(M c:pos)if(!(c&A))throw std::runtime_error("missed_polygon");for(M c:neg)if((c&A)==c)throw std::runtime_error("bad_terminal");for(M c:caps)if((c&A)==c)throw std::runtime_error("fourcap");}
   else if(verdict==-1)++unsats;else ++unknown;
   std::fprintf(out,"{\"W\":%u,\"m\":%d,\"result\":%d,\"A\":%u,\"nodes\":%llu}\n",W,size,verdict,s.model,(unsigned long long)s.nodes);
   if(!(cases%4096))flush();
   if(verdict==-1){stop="NEGATIVE_NEEDS_CERTIFICATION";throw Stop{};}
  });
  std::cerr<<"completed size="<<size<<" cases="<<cases-before<<" total="<<cases<<"\n";flush();
 }}catch(const Stop&){if(stop=="COMPLETE")stop="DEADLINE";}
 flush();std::fclose(out);
 std::cout<<"{\"label\":\"COMPUTED\",\"stop\":\""<<stop<<"\",\"cases\":"<<cases<<",\"SAT\":"<<sats<<",\"negative\":"<<unsats<<",\"UNKNOWN\":"<<unknown<<",\"nodes\":"<<nodes<<",\"seconds\":"<<std::chrono::duration<double>(Clock::now()-begin).count()<<",\"target_polygons\":"<<targets.size()<<",\"fourcaps\":"<<caps.size()<<"}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
