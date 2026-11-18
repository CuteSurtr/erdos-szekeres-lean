// General terminal-safe nonexistence, no boundary cup/complement assumptions.
#define main archived_compact_main
#include "../../compact/compact_cnf.cpp"
#undef main

int main(int argc,char**argv){
 try{
  if(argc<4||argc>5)throw std::runtime_error("usage: terminal_general m n output.cnf|--stats [fixed-signs]");
  Options o;o.m=std::stoi(argv[1]);o.n=std::stoi(argv[2]);
  if(o.n<5||o.n>8||o.m<o.n-1||o.m>20)throw std::runtime_error("bad_parameters");
  if(std::string(argv[3])!="--stats"){o.out=argv[3];o.mapfile=o.out+".map";}
  if(argc==5)o.fix=argv[4];
  Encoder e(o);e.geometry();int amax=o.m-o.n+2;
  std::vector<int> cap(e.full+1),A(e.full+1),B(e.full+1);
  e.w.set_phase("terminal_fourcap_equivalence");
  choose(e.full,4,[&](Mask s){
   int z=cap[s]=e.fresh("terminal_fourcap",s);std::vector<int> signs;
   choose(s,3,[&](Mask t){auto p=vertices(t);signs.push_back(-e.t(p[0],p[1],p[2]));});
   e.conjunction(z,signs);
  });
  e.w.set_phase("terminal_bad_triple_equivalence");
  choose(e.full,3,[&](Mask s){
   auto p=vertices(s);int a=p[0],b=p[1],c=p[2];
   int z=e.fresh("terminal_bad_triple",s);if(amax>=3)A[s]=z;
   std::vector<int> row={-e.t(a,b,c)};
   for(int u=0;u<b;++u)for(int v=u+1;v<b;++v){
    Mask q=(Mask(1)<<u)|(Mask(1)<<v)|(Mask(1)<<b)|(Mask(1)<<c);
    if(!cap[q])throw std::runtime_error("missing_fourcap");row.push_back(-cap[q]);
   }
   e.conjunction(z,row);
  });
  e.w.set_phase("bad_triple_containment");
  for(Mask s=0;s<=e.full;++s)if(pc(s)>=4&&pc(s)<=amax){
   int z=A[s]=e.fresh("bad_contains",s);e.disjunction(z,e.children(s,A,4));
  }
  e.w.set_phase("target_containment");
  for(Mask s=0;s<=e.full;++s){
   int k=pc(s);
   if(k==o.n-1)B[s]=e.Q[s];
   else if(k>o.n-1){int z=B[s]=e.fresh("target_contains",s);e.disjunction(z,e.children(s,B,o.n));}
  }
  e.w.set_phase("forall_terminal_delta");
  for(Mask s=0;s<=e.full;++s)if(pc(s)<=amax){
   std::vector<int> row;if(A[s])row.push_back(A[s]);if(B[e.full^s])row.push_back(B[e.full^s]);e.w.add(row);
  }
  e.w.set_phase("fixed_signs");
  if(!o.fix.empty()){
   std::ifstream f(o.fix);std::string signs,extra;f>>signs;
   if(!f||int(signs.size())!=e.nt||f>>extra)throw std::runtime_error("bad_sign_file");
   for(int i=0;i<e.nt;++i){if(signs[i]!='+'&&signs[i]!='-')throw std::runtime_error("bad_sign");e.w.add({signs[i]=='+'?i+1:-i-1});}
  }
  auto bytes=e.w.finish(e.nv);if(e.mapping){e.mapping.flush();if(!e.mapping)throw std::runtime_error("map_write");}
  std::cout<<"{\"m\":"<<o.m<<",\"n\":"<<o.n<<",\"amax\":"<<amax<<",\"variables\":"<<e.nv
   <<",\"clauses\":"<<e.w.clauses<<",\"literals\":"<<e.w.literals<<",\"bytes\":"<<bytes
   <<",\"fixed_signs\":"<<(!o.fix.empty()?"true":"false")<<",\"phases\":{";
  bool first=true;for(auto [name,c]:e.w.counts){if(!first)std::cout<<',';first=false;std::cout<<'"'<<name<<"\":{\"clauses\":"<<c[0]<<",\"literals\":"<<c[1]<<'}';}
  std::cout<<"}}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
