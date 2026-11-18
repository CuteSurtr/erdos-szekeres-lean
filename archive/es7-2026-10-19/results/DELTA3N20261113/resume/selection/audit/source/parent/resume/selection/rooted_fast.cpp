// Specialized rooted counterexample encoder.  Geometric base unchanged.
// Forbidden subsets of the old selected points are old four-caps and triples
// which become four-caps with the rightmost root. See ROOTED_FAST.md.
#define main archived_compact_main
#include "../compact/compact_cnf.cpp"
#undef main

int main(int argc,char**argv){
 try{
  if(argc!=4)throw std::runtime_error("usage: rooted_fast m n output.cnf");
  Options o;o.m=std::stoi(argv[1]);o.n=std::stoi(argv[2]);o.out=argv[3];o.mapfile=o.out+".map";
  if(o.n<5||o.n>8||o.m<o.n+1||o.m>16)throw std::runtime_error("bad_parameters");
  Encoder e(o);e.geometry();int r=o.m-1;Mask old=(Mask(1)<<r)-1;
  int amax=o.m-o.n+1,bmax=o.m-3;
  std::vector<int>A(old+1),B(old+1);
  e.w.set_phase("root_blocker3");
  if(amax>=3)choose(old,3,[&](Mask s){
   auto p=vertices(s);int z=A[s]=e.fresh("root_bad_contains",s);
   e.w.add({-z,-e.t(p[0],p[1],p[2])});
   e.w.add({-z,-e.t(p[1],p[2],r)});
  });
  e.w.set_phase("root_blocker4");
  if(amax>=4)choose(old,4,[&](Mask s){
   auto p=vertices(s);int c=e.fresh("old_fourcap",s);
   e.w.add({-c,-e.t(p[0],p[1],p[2])});e.w.add({-c,-e.t(p[1],p[2],p[3])});
   int z=A[s]=e.fresh("root_bad_contains",s);
   auto row=e.children(s,A,4);row.push_back(c);row.insert(row.begin(),-z);e.w.add(row);
  });
  e.w.set_phase("root_bad_lattice");
  for(Mask s=0;s<=old;++s)if(pc(s)>4&&pc(s)<=amax){
   int z=A[s]=e.fresh("root_bad_contains",s);auto row=e.children(s,A,5);
   row.insert(row.begin(),-z);e.w.add(row);
  }
  e.w.set_phase("old_target_lattice");
  for(Mask s=0;s<=old;++s){
   int k=pc(s);
   if(k==o.n-1&&k<=bmax)B[s]=e.Q[s];
   else if(k>o.n-1&&k<=bmax){
    int z=B[s]=e.fresh("old_target_contains",s);auto row=e.children(s,B,o.n);
    row.insert(row.begin(),-z);e.w.add(row);
   }
  }
  e.w.set_phase("forall_rooted_delta");
  for(Mask s=0;s<=old;++s)if(pc(s)>=2&&pc(s)<=amax){
   std::vector<int> row;if(A[s])row.push_back(A[s]);if(B[old^s])row.push_back(B[old^s]);e.w.add(row);
  }
  auto bytes=e.w.finish(e.nv);e.mapping.flush();if(!e.mapping)throw std::runtime_error("map_write");
  std::cout<<"{\"m\":"<<o.m<<",\"n\":"<<o.n<<",\"root\":"<<r
   <<",\"variables\":"<<e.nv<<",\"clauses\":"<<e.w.clauses
   <<",\"literals\":"<<e.w.literals<<",\"bytes\":"<<bytes<<"}\n";
 }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
