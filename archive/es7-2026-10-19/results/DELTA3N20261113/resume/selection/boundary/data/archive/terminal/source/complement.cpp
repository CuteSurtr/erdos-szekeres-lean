// Counterexamples to the cup-complement sufficient condition.
#define main archived_compact_main
#include "../../compact/compact_cnf.cpp"
#undef main

int main(int argc,char**argv){
 try{
  if(argc!=4)throw std::runtime_error("usage: complement n old|root output.cnf");
  int n=std::stoi(argv[1]);std::string mode=argv[2];
  if(n<5||n>8||(mode!="old"&&mode!="root"))throw std::runtime_error("bad parameters");
  Options o;o.n=n;o.m=2*n-3+(mode=="root");o.out=argv[3];o.mapfile=o.out+".map";
  Encoder e(o);e.geometry();Mask old=(Mask(1)<<(2*n-3))-1;
  std::vector<int> cups;
  e.w.set_phase("cup_equivalence");
  choose(old,n-2,[&](Mask s){
   int z=e.fresh("cup",s);cups.push_back(z);std::vector<int> signs;
   choose(s,3,[&](Mask t){auto p=vertices(t);signs.push_back(e.t(p[0],p[1],p[2]));});
   e.conjunction(z,signs);
  });
  e.w.set_phase("some_long_cup");e.w.add(cups);
  e.w.set_phase("no_longer_cup");
  choose(old,n-1,[&](Mask s){
   std::vector<int> row;
   choose(s,3,[&](Mask t){auto p=vertices(t);row.push_back(-e.t(p[0],p[1],p[2]));});
   e.w.add(row);
  });
  e.w.set_phase("convex_complements");
  size_t index=0;
  choose(old,n-2,[&](Mask s){
   int q=e.Q[old^s];if(!q)throw std::runtime_error("missing complement flag");
   e.w.add({-cups.at(index++),q});
  });
  auto bytes=e.w.finish(e.nv);e.mapping.flush();if(!e.mapping)throw std::runtime_error("map write");
  std::cout<<"{\"mode\":\""<<mode<<"\",\"n\":"<<n<<",\"m\":"<<o.m
   <<",\"old_m\":"<<2*n-3<<",\"variables\":"<<e.nv<<",\"clauses\":"<<e.w.clauses
   <<",\"literals\":"<<e.w.literals<<",\"bytes\":"<<bytes<<"}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
