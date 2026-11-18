// Nonexistence of a weak Delta protected by ambient terminal pairs along cups.
// Independent audit required before any finite theorem is claimed.
#define main archived_compact_main
#include "../../compact/compact_cnf.cpp"
#undef main
int main(int argc,char**argv){try{
 if(argc<4||argc>5)throw std::runtime_error("usage: cup_terminal_general m n output.cnf|--stats [fixed-signs]");
 Options o;o.m=std::stoi(argv[1]);o.n=std::stoi(argv[2]);
 if(o.n<5||o.n>8||o.m<o.n-1||o.m>20)throw std::runtime_error("bad_parameters");
 if(std::string(argv[3])!="--stats"){o.out=argv[3];o.mapfile=o.out+".map";}
 if(argc==5)o.fix=argv[4];
 Encoder e(o);e.geometry();int amax=o.m-o.n+2;
 std::vector<int> cap(e.full+1),cup(e.full+1),A(e.full+1),B(e.full+1),end4(o.m*o.m),covered(o.m*o.m);
 auto exact_or=[&](int z,const std::vector<int>&xs){std::vector<int>r={-z};r.insert(r.end(),xs.begin(),xs.end());e.w.add(r);for(int x:xs)e.w.add({-x,z});};
 e.w.set_phase("fourcap_and_fourcup_equivalence");
 choose(e.full,4,[&](Mask s){
  int z=cap[s]=e.fresh("terminal_fourcap",s),w=cup[s]=e.fresh("terminal_fourcup",s);std::vector<int>neg,pos;
  choose(s,3,[&](Mask t){auto p=vertices(t);int v=e.t(p[0],p[1],p[2]);neg.push_back(-v);pos.push_back(v);});
  e.conjunction(z,neg);e.conjunction(w,pos);
 });
 e.w.set_phase("ambient_terminal_pair_equivalence");
 for(int b=0;b<o.m;++b)for(int c=b+1;c<o.m;++c){
  Mask pair=(Mask(1)<<b)|(Mask(1)<<c);int z=end4[b*o.m+c]=e.fresh("end_fourcap",pair);std::vector<int>xs;
  for(int u=0;u<b;++u)for(int v=u+1;v<b;++v)xs.push_back(cap[pair|(Mask(1)<<u)|(Mask(1)<<v)]);
  exact_or(z,xs);
 }
 std::map<std::pair<int,int>,int>support_cache;
 e.w.set_phase("cup_domination_equivalence");
 for(int b=0;b<o.m;++b)for(int c=b+1;c<o.m;++c){
  Mask pair=(Mask(1)<<b)|(Mask(1)<<c);std::vector<int>xs={end4[b*o.m+c]};
  for(int u=b;u<o.m;++u)for(int v=std::max(c,u+1);v<o.m;++v){
   if((u==b&&v==c)||u<2||v<3)continue;
   Mask s=pair|(Mask(1)<<u)|(Mask(1)<<v);int cp=0;
   if(pc(s)==3){auto p=vertices(s);cp=e.t(p[0],p[1],p[2]);}
   else if(pc(s)==4)cp=cup[s];else throw std::runtime_error("cup_union_size");
   auto key=std::make_pair(end4[u*o.m+v],cp);int z;
   auto it=support_cache.find(key);
   if(it!=support_cache.end())z=it->second;
   else{std::string kind="cup_support_"+std::to_string(u)+"_"+std::to_string(v);z=e.fresh(kind.c_str(),s);e.conjunction(z,{key.first,key.second});support_cache[key]=z;}
   xs.push_back(z);
  }
  int z=covered[b*o.m+c]=e.fresh("covered_pair",pair);exact_or(z,xs);
 }
 e.w.set_phase("uncovered_cap_triple_equivalence");
 choose(e.full,3,[&](Mask s){auto p=vertices(s);int z=e.fresh("uncovered_cap_triple",s);if(amax>=3)A[s]=z;e.conjunction(z,{-e.t(p[0],p[1],p[2]),-covered[p[1]*o.m+p[2]]});});
 e.w.set_phase("bad_triple_or_fourcap_containment");
 for(Mask s=0;s<=e.full;++s)if(pc(s)>=4&&pc(s)<=amax){
  int z=A[s]=e.fresh("bad_contains",s);auto xs=e.children(s,A,pc(s)==4?4:5);if(pc(s)==4)xs.push_back(cap[s]);e.disjunction(z,xs);
 }
 e.w.set_phase("target_containment");
 for(Mask s=0;s<=e.full;++s){int k=pc(s);if(k==o.n-1)B[s]=e.Q[s];else if(k>o.n-1){int z=B[s]=e.fresh("target_contains",s);e.disjunction(z,e.children(s,B,o.n));}}
 e.w.set_phase("forall_cup_protected_delta");
 for(Mask s=0;s<=e.full;++s)if(pc(s)<=amax){std::vector<int>row;if(A[s])row.push_back(A[s]);if(B[e.full^s])row.push_back(B[e.full^s]);e.w.add(row);}
 e.w.set_phase("fixed_signs");
 if(!o.fix.empty()){
  std::ifstream f(o.fix);std::string signs,extra;f>>signs;if(!f||int(signs.size())!=e.nt||f>>extra)throw std::runtime_error("bad_sign_file");
  for(int i=0;i<e.nt;++i){if(signs[i]!='+'&&signs[i]!='-')throw std::runtime_error("bad_sign");e.w.add({signs[i]=='+'?i+1:-i-1});}
 }
 auto bytes=e.w.finish(e.nv);if(e.mapping){e.mapping.flush();if(!e.mapping)throw std::runtime_error("map_write");}
 std::cout<<"{\"m\":"<<o.m<<",\"n\":"<<o.n<<",\"amax\":"<<amax<<",\"variables\":"<<e.nv<<",\"clauses\":"<<e.w.clauses<<",\"literals\":"<<e.w.literals<<",\"bytes\":"<<bytes<<",\"fixed_signs\":"<<(!o.fix.empty()?"true":"false")<<",\"phases\":{";
 bool first=true;for(auto [name,c]:e.w.counts){if(!first)std::cout<<',';first=false;std::cout<<'"'<<name<<"\":{\"clauses\":"<<c[0]<<",\"literals\":"<<c[1]<<'}';}std::cout<<"}}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}}
