// Tests a sufficient strengthening of weak Delta: every maximal four-cap-free
// subset hits all target polygons. Uses the previously audited geometric base.
#define main archived_delta_encoder_main
#include "../../encoder/delta_cnf.cpp"
#undef main

int main(int argc,char**argv) {
 try {
  if(argc!=4)throw std::runtime_error("usage: maximal_cnf m n output.cnf");
  Options o;o.m=std::stoi(argv[1]);o.n=std::stoi(argv[2]);o.out=argv[3];o.base=true;
  if(o.m<o.n || o.m>20 || o.n<5 || o.n>8)throw std::runtime_error("parameter bounds");
  Encoder e(o);e.base();
  std::vector<int> red(o.m),cap(e.full+1),quad(e.full+1);
  for(int&v:red)v=++e.nv;
  e.w.phase="red_cap_free";
  choose(e.full,4,[&](Mask s){
   auto p=vertices(s);auto c=e.chain(s,true);
   for(int i:p)c.push_back(-red[i]);
   e.w.add(c);
   int z=cap[s]=++e.nv;e.imply(z,e.chain(s,false));
  });
  e.w.phase="maximal_red";
  for(int p=0;p<o.m;++p){
   std::vector<int> clause={red[p]};
   choose(e.full^(Mask(1)<<p),3,[&](Mask s){
    int z=++e.nv;clause.push_back(z);e.w.add({-z,cap[s|(Mask(1)<<p)]});
    for(int i:vertices(s))e.w.add({-z,red[i]});
   });
   e.w.add(clause);
  }
  e.w.phase="convex_quads";
  choose(e.full,4,[&](Mask s){
   auto p=vertices(s);int z=quad[s]=++e.nv;
   int a=e.t(p[0],p[1],p[2]),b=e.t(p[0],p[1],p[3]);
   int c=e.t(p[0],p[2],p[3]),d=e.t(p[1],p[2],p[3]);
   e.w.add({-z,-a,b});e.w.add({-z,a,-b});e.w.add({-z,-c,d});e.w.add({-z,c,-d});
  });
  e.w.phase="blue_target";
  std::vector<int> some;
  choose(e.full,o.n-1,[&](Mask s){
   int z=++e.nv;some.push_back(z);
   choose(s,4,[&](Mask q){e.w.add({-z,quad[q]});});
   for(int p:vertices(s))e.w.add({-z,-red[p]});
  });
  e.w.add(some);auto bytes=e.w.finish(e.nv);
  std::cout<<"{\"label\":\"COMPUTED\",\"m\":"<<o.m<<",\"n\":"<<o.n
   <<",\"variables\":"<<e.nv<<",\"clauses\":"<<e.w.clauses
   <<",\"literals\":"<<e.w.literals<<",\"bytes\":"<<bytes<<",\"red_variables\":[";
  for(int i=0;i<o.m;++i){if(i)std::cout<<',';std::cout<<red[i];}std::cout<<"]}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
