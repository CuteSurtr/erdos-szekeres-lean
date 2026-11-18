// Sufficient weak-octagon criterion: deleting at most five points removes
// all convex hexagons. Search for a configuration where this fails.
#define main archived_compact_encoder_main
#include "../compact/compact_cnf.cpp"
#undef main
int main(int argc,char**argv){
 try{
  if(argc!=3)throw std::runtime_error("usage: transversal_cnf m output.cnf");
  Options o;o.m=std::stoi(argv[1]);o.n=8;o.out=argv[2];o.mapfile=o.out+".map";o.base=true;
  if(o.m<11||o.m>16)throw std::runtime_error("require11<=m<=16");
  Encoder e(o);e.geometry();std::vector<int>J(e.full+1);
  e.w.set_phase("hexagon_containment");
  for(Mask s=0;s<=e.full;++s){
   int k=pc(s);
   if(k==6)J[s]=e.Q[s];
   else if(k>6&&k<=o.m-5){
    int z=J[s]=e.fresh("contains_hexagon",s);
    auto v=e.children(s,J,7);v.insert(v.begin(),-z);e.w.add(v);
   }
  }
  e.w.set_phase("no_five_point_transversal");
  choose(e.full,o.m-5,[&](Mask s){e.w.add({J[s]});});
  auto bytes=e.w.finish(e.nv);
  std::cout<<"{\"m\":"<<o.m<<",\"n\":8,\"variables\":"<<e.nv
   <<",\"clauses\":"<<e.w.clauses<<",\"literals\":"<<e.w.literals<<",\"bytes\":"<<bytes<<"}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
