// Independent fixed-coordinate verifier. No finder or earlier checker imported.
// Convexity: four-point triangle containment + the all-four-subsets criterion.
#include <algorithm>
#include <array>
#include <cctype>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>
using Mask = uint32_t;
using I = __int128_t;
struct Point { int64_t x, y; };
struct Failure : std::runtime_error { using std::runtime_error::runtime_error; };
static void need(bool b, const std::string& s) { if (!b) throw Failure(s); }
static int pc(Mask m) { return __builtin_popcount(m); }
static Mask bit(int i) { return Mask(1) << i; }
static std::vector<int> indices(Mask s) {
  std::vector<int> a;
  while (s) { int i=__builtin_ctz(s); a.push_back(i); s &= s-1; }
  return a;
}
template<class F> static void choose(int n, int k, F fn) {
  if (k>n) return;
  if (k==0) { fn(0); return; }
  const Mask end=bit(n);
  for (Mask s=bit(k)-1; s<end;) {
    fn(s);
    Mask t=s & -s, u=s+t;
    s=u | (((s^u)>>2)/t);
  }
}
static uint64_t binom(int n,int k) {
  uint64_t r=1;
  for(int i=1;i<=k;++i) r=r*(n-i+1)/i;
  return r;
}
static I det(Point a,Point b,Point c) {
  // Cast BEFORE subtraction. |coordinates|<=2^40 gives |det|<=2^83.
  return (I(b.x)-a.x)*(I(c.y)-a.y)-(I(b.y)-a.y)*(I(c.x)-a.x);
}
static std::string decimal(I x) {
  if(x==0) return "0";
  bool neg=x<0; if(neg) x=-x;
  std::string s;
  while(x) { s.push_back(char('0'+x%10)); x/=10; }
  if(neg) s.push_back('-');
  std::reverse(s.begin(),s.end()); return s;
}
static std::vector<Point> read_points(const std::string& file) {
  std::ifstream in(file); need(bool(in),"cannot open points: "+file);
  int n,target; need(bool(in>>n>>target),"invalid point header");
  need(n>=1 && n<=23 && target==7,"requires 1..23 points and target 7");
  std::vector<Point> p(n);
  constexpr int64_t bound=int64_t(1)<<40;
  for(int i=0;i<n;++i) {
    need(bool(in>>p[i].x>>p[i].y),"missing/noninteger coordinate");
    need(p[i].x>=-bound && p[i].x<=bound && p[i].y>=-bound && p[i].y<=bound,
         "coordinate_bound");
    need(i==0 || p[i-1].x<p[i].x,"x_order");
  }
  std::string tail; need(!(in>>tail),"extra point data"); return p;
}
struct Geometry {
  enum { CAP4=1,CAP5=2,SIX=4,SEVEN=8,NONCONVEX4=16 };
  std::vector<Point> p;
  int n; Mask full;
  std::vector<uint8_t> flags;
  std::vector<Mask> c4,c5,g6,g7,non4;
  std::array<std::array<Mask,23>,23> cap_pre{};
  std::array<std::array<std::vector<Mask>,23>,23> uv;
  uint64_t triples=0,cap_triples=0,convex_four=0;
  I min_abs_det=0,max_abs_det=0;
  explicit Geometry(std::vector<Point> a):p(std::move(a)),n(int(p.size())),full(bit(n)-1),flags(bit(n),0) {
    for(int a=0;a<n;++a) for(int b=a+1;b<n;++b) for(int c=b+1;c<n;++c) {
      I d=det(p[a],p[b],p[c]);
      need(d!=0,"collinear triple="+std::to_string(a)+","+std::to_string(b)+","+std::to_string(c));
      ++triples;
      I ad=d<0 ? -d:d;
      if(min_abs_det==0 || ad<min_abs_det) min_abs_det=ad;
      max_abs_det=std::max(max_abs_det,ad);
      if(d<0) { cap_pre[b][c]|=bit(a); ++cap_triples; }
    }
    choose(n,4,[&](Mask s) {
      if(!convex_direct(s)) { flags[s]|=NONCONVEX4; non4.push_back(s); }
      else ++convex_four;
      if(cap_direct(s)) {
        flags[s]|=CAP4; c4.push_back(s); auto a=indices(s);
        uv[a[2]][a[3]].push_back(bit(a[0])|bit(a[1]));
      }
    });
    choose(n,5,[&](Mask s) { if(cap_direct(s)) { flags[s]|=CAP5; c5.push_back(s); } });
    upward();
    choose(n,6,[&](Mask s) { if(!(flags[s]&NONCONVEX4)) { flags[s]|=SIX; g6.push_back(s); } });
    choose(n,7,[&](Mask s) { if(!(flags[s]&NONCONVEX4)) { flags[s]|=SEVEN; g7.push_back(s); } });
    upward();
  }
  bool cap_direct(Mask s) const {
    auto a=indices(s);
    for(size_t i=0;i<a.size();++i) for(size_t j=i+1;j<a.size();++j) for(size_t k=j+1;k<a.size();++k)
      if(det(p[a[i]],p[a[j]],p[a[k]])>=0) return false;
    return true;
  }
  bool inside(int q,int a,int b,int c) const {
    I x=det(p[a],p[b],p[q]),y=det(p[b],p[c],p[q]),z=det(p[c],p[a],p[q]);
    return (x>0 && y>0 && z>0)||(x<0 && y<0 && z<0);
  }
  bool convex_direct(Mask s) const {
    // No vertex lies in a triangle of other selected points.
    auto a=indices(s);
    for(int q:a) for(size_t i=0;i<a.size();++i) if(a[i]!=q)
      for(size_t j=i+1;j<a.size();++j) if(a[j]!=q)
        for(size_t k=j+1;k<a.size();++k) if(a[k]!=q)
          if(inside(q,a[i],a[j],a[k])) return false;
    return true;
  }
  bool convex_support(Mask s) const {
    // Independent control: count supporting edges, with degree 2 at EVERY vertex.
    auto a=indices(s); if(a.size()<3) return true;
    int degree[23]={},edges=0;
    for(size_t i=0;i<a.size();++i) for(size_t j=i+1;j<a.size();++j) {
      bool pos=false,neg=false;
      for(int k:a) if(k!=a[i] && k!=a[j]) {
        I d=det(p[a[i]],p[a[j]],p[k]); pos|=d>0; neg|=d<0;
      }
      if(pos!=neg) { ++degree[a[i]]; ++degree[a[j]]; ++edges; }
    }
    if(edges!=int(a.size())) return false;
    for(int i:a) if(degree[i]!=2) return false;
    return true;
  }
  void upward() {
    // After dimension j, flags[S] includes all seeds obtained by dropping
    // any subset of processed bits. At completion it is the OR over T subset S.
    for(Mask b=1;b<=full;b<<=1)
      for(Mask start=0;start<=full;start+=2*b)
        for(Mask j=0;j<b;++j) flags[start+b+j]|=flags[start+j];
  }
  bool supported(Mask w,int b,int c) const {
    for(Mask q:uv[b][c]) if((w&q)==q) return true;
    return false;
  }
  Mask unsafe(Mask w,Mask a,uint64_t* pair_checks=nullptr,uint64_t* triple_checks=nullptr) const {
    for(Mask cs=a;cs;cs&=cs-1) {
      int c=__builtin_ctz(cs);
      for(Mask bs=a&(bit(c)-1);bs;bs&=bs-1) {
        int b=__builtin_ctz(bs); Mask pre=a&cap_pre[b][c];
        if(!pre) continue;
        if(pair_checks) ++*pair_checks;
        if(triple_checks) *triple_checks+=pc(pre);
        if(!supported(w,b,c)) return (pre&-pre)|bit(b)|bit(c);
      }
    }
    return 0;
  }
  std::string witness_error(Mask w,Mask a,uint64_t* pairs=nullptr,uint64_t* triples_out=nullptr) const {
    if(w>full || a>full || (a&~w)) return "A_not_subset_W";
    if(flags[a]&CAP4) {
      for(Mask q:c4) if((q&a)==q) return "four_cap="+std::to_string(q);
    }
    if(flags[w&~a]&SIX) {
      for(Mask q:g6) if((q&(w&~a))==q) return "unhit_hexagon="+std::to_string(q);
    }
    Mask q=unsafe(w,a,pairs,triples_out);
    if(q) return "unsupported_cap_triple="+std::to_string(q);
    return "";
  }
  void ambient() const {
    need(c5.empty(),"ambient_five_cap="+(c5.empty()?std::string("none"):std::to_string(c5[0])));
    need(g7.empty(),"ambient_heptagon="+(g7.empty()?std::string("none"):std::to_string(g7[0])));
  }
  void print() const {
    std::cout << "{\"n\":"<<n<<",\"triples_checked\":"<<triples
      <<",\"cap_triples\":"<<cap_triples<<",\"convex_four\":"<<convex_four
      <<",\"nonconvex_four\":"<<non4.size()<<",\"four_caps\":"<<c4.size()
      <<",\"five_caps\":"<<c5.size()<<",\"convex_six\":"<<g6.size()
      <<",\"convex_seven\":"<<g7.size()<<",\"min_abs_det\":\""<<decimal(min_abs_det)
      <<"\",\"max_abs_det\":\""<<decimal(max_abs_det)<<"\"}";
  }
};
struct Row { uint64_t w,m,result,a,nodes; };
static Row parse_row(const std::string& s) {
  size_t i=0; unsigned seen=0; uint64_t val[5]={};
  auto space=[&] { while(i<s.size() && (s[i]==' '||s[i]=='\t'||s[i]=='\r'||s[i]=='\n')) ++i; };
  auto tok=[&](char c) { space(); need(i<s.size()&&s[i]==c,"json_expected_token"); ++i; };
  tok('{');
  for(int entry=0;entry<5;++entry) {
    if(entry) tok(',');
    tok('"'); size_t start=i;
    while(i<s.size() && s[i]!='"') ++i;
    need(i<s.size(),"json_unterminated_key"); std::string key=s.substr(start,i-start); ++i;
    int k=key=="W"?0:key=="m"?1:key=="result"?2:key=="A"?3:key=="nodes"?4:-1;
    need(k>=0,"json_unknown_key"); need(!(seen&bit(k)),"json_duplicate_key"); seen|=bit(k); tok(':'); space();
    need(i<s.size() && s[i]>='0' && s[i]<='9',"json_unsigned_integer_required");
    bool leading_zero=s[i]=='0'; start=i; uint64_t v=0;
    while(i<s.size()&&s[i]>='0'&&s[i]<='9') {
      unsigned d=s[i++]-'0'; need(v<=(std::numeric_limits<uint64_t>::max()-d)/10,"json_integer_overflow"); v=v*10+d;
    }
    need(!leading_zero || i-start==1,"json_leading_zero"); val[k]=v;
  }
  tok('}'); space(); need(i==s.size() && seen==31,"json_trailing_data");
  return {val[0],val[1],val[2],val[3],val[4]};
}
struct Coverage {
  int n,lo,hi; std::vector<uint8_t> seen; uint64_t rows=0,counts[24]={};
  Coverage(int n_,int lo_,int hi_):n(n_),lo(lo_),hi(hi_),seen((bit(n)+7)/8,0) {
    need(lo>=0 && lo<=hi && hi<=n,"invalid_size_range");
  }
  void add(const Row& r) {
    need(r.w<bit(n),"W_out_of_range");
    need(r.m>=uint64_t(lo) && r.m<=uint64_t(hi),"m_out_of_range");
    need(pc(Mask(r.w))==int(r.m),"m_popcount_mismatch");
    need(r.result==1,"result_not_one");
    need(r.a<bit(n) && (r.a&~r.w)==0,"A_not_subset_W");
    uint8_t b=uint8_t(1u<<(r.w&7));
    need(!(seen[r.w>>3]&b),"duplicate_W="+std::to_string(r.w));
    seen[r.w>>3]|=b; ++rows; ++counts[r.m];
  }
  void finish() const {
    // Enumerate the entire universe independently of the input order.
    uint64_t expected=0;
    for(Mask w=0;w<bit(n);++w) {
      bool wanted=pc(w)>=lo && pc(w)<=hi;
      bool got=(seen[w>>3]>>(w&7))&1;
      need(wanted==got,"coverage_mismatch_W="+std::to_string(w));
      expected+=wanted;
    }
    need(rows==expected,"row_count_mismatch");
    for(int m=lo;m<=hi;++m) need(counts[m]==binom(n,m),"binomial_count_mismatch");
  }
};
static void stream(Geometry& g,const std::string& path,int lo,int hi) {
  Coverage coverage(g.n,lo,hi); std::ifstream in(path); need(bool(in),"cannot open rows");
  uint64_t pairs=0,triples=0,nodes_max=0,a_sizes[24]={};
  char line[512]; uint64_t lineno=0;
  while(in.getline(line,sizeof(line))) {
    ++lineno;
    try {
      Row r=parse_row(line); coverage.add(r);
      std::string e=g.witness_error(Mask(r.w),Mask(r.a),&pairs,&triples);
      need(e.empty(),e); ++a_sizes[pc(Mask(r.a))]; nodes_max=std::max(nodes_max,r.nodes);
    } catch(const Failure& e) {
      std::cerr<<"failure_row="<<lineno<<" raw="<<line<<"\n";
      throw;
    }
    if(lineno%500000==0) std::cerr<<"checked_rows="<<lineno<<"\n";
  }
  need(in.eof() && !in.bad(),"read_error_or_row_exceeds_511_bytes");
  coverage.finish();
  std::cout<<"{\"kind\":\"subset_stream\",\"label\":\"COMPUTED\",\"status\":\"PASS\",\"geometry\":";
  g.print();
  std::cout<<",\"rows\":"<<coverage.rows<<",\"by_size\":{";
  for(int m=lo;m<=hi;++m) { if(m>lo) std::cout<<","; std::cout<<"\""<<m<<"\":"<<coverage.counts[m]; }
  std::cout<<"},\"A_size_histogram\":{"; bool first=true;
  for(int k=0;k<=g.n;++k) if(a_sizes[k]) { if(!first) std::cout<<","; first=false; std::cout<<"\""<<k<<"\":"<<a_sizes[k]; }
  std::cout<<"},\"terminal_pair_obligations\":"<<pairs<<",\"cap_triples_covered\":"<<triples
    <<",\"max_finder_nodes_metadata_only\":"<<nodes_max
    <<",\"coverage_every_mask_exactly_once\":true,\"extra_rows\":0,\"unknown_rows\":0}\n";
}
static void mapped18(Geometry& g,const std::string& path) {
  auto small=read_points(path); need(small.size()==18,"mapped_fixture_not_18");
  std::vector<int> ix; Mask w=0;
  for(Point p:small) {
    int found=-1;
    for(int i=0;i<g.n;++i) if(g.p[i].x==p.x && g.p[i].y==p.y) { need(found==-1,"ambiguous_mapping"); found=i; }
    need(found>=0,"18_point_missing_from_ambient"); ix.push_back(found); w|=bit(found);
  }
  need(pc(w)==18,"duplicate_mapping");
  uint64_t ordinary=0,safe=0,minsize=19,badtriples=0,n4=0,n6=0;
  for(Mask a=w;;a=(a-1)&w) {
    if(!(g.flags[a]&Geometry::CAP4) && !(g.flags[w&~a]&Geometry::SIX)) {
      ++ordinary; minsize=std::min(minsize,uint64_t(pc(a)));
      if(g.unsafe(w,a)==0) ++safe;
    }
    if(a==0) break;
  }
  for(Mask q:g.c4) n4+=(q&w)==q;
  for(Mask q:g.g6) n6+=(q&w)==q;
  for(int b=0;b<g.n;++b) if(w&bit(b)) for(int c=b+1;c<g.n;++c) if((w&bit(c))&&!g.supported(w,b,c))
    badtriples+=pc(w&g.cap_pre[b][c]);
  need(safe==0,"mapped_18_has_terminal_safe_selection");
  std::cout<<"{\"kind\":\"mapped_18\",\"label\":\"COMPUTED\",\"status\":\"PASS\",\"W\":"<<w<<",\"indices\":[";
  for(size_t i=0;i<ix.size();++i) { if(i) std::cout<<","; std::cout<<ix[i]; }
  std::cout<<"],\"selections_enumerated\":262144,\"ordinary_weak_Deltas\":"<<ordinary
    <<",\"terminal_safe_Deltas\":"<<safe<<",\"minimum_ordinary_size\":"<<minsize
    <<",\"four_caps\":"<<n4<<",\"hexagons\":"<<n6<<",\"bad_triples\":"<<badtriples<<"}\n";
}
template<class F> static void expect_fail(F f,const std::string& prefix) {
  bool failed=false;
  try { f(); } catch(const Failure& e) { failed=true; need(std::string(e.what()).find(prefix)==0,"wrong_control_failure: "+std::string(e.what())); }
  need(failed,"negative_control_accepted: "+prefix);
}
static void controls(Geometry& real) {
  unsigned parse_bad=0,coverage_bad=0; uint64_t small_sets=0,closure_queries=0,support_tests=0;
  Row good=parse_row(" { \"nodes\":9, \"A\":1, \"result\":1, \"m\":2, \"W\":3 } ");
  need(good.w==3 && good.a==1,"reordered_parser_control");
  std::vector<std::string> bad={"", "{}", "{\"W\":3,\"m\":2,\"result\":1,\"A\":1}",
    "{\"W\":3,\"W\":2,\"result\":1,\"A\":1,\"nodes\":1}",
    "{\"W\":03,\"m\":2,\"result\":1,\"A\":1,\"nodes\":1}",
    "{\"W\":-3,\"m\":2,\"result\":1,\"A\":1,\"nodes\":1}",
    "{\"W\":3.0,\"m\":2,\"result\":1,\"A\":1,\"nodes\":1}",
    "{\"W\":3,\"m\":2,\"result\":1,\"A\":1,\"nodes\":18446744073709551616}",
    "{\"W\":3,\"m\":2,\"result\":1,\"A\":1,\"nodes\":1,\"extra\":0}",
    "{\"W\":3,\"m\":2,\"result\":1,\"A\":1,\"nodes\":1} trailing"};
  for(const auto& s:bad) { expect_fail([&]{parse_row(s);},"json_"); ++parse_bad; }
  auto mutation=[&](Row r,const std::string& err) { expect_fail([&]{Coverage c(4,2,2); c.add(r);},err); ++coverage_bad; };
  mutation({16,2,1,0,0},"W_out_of_range"); mutation({3,3,1,0,0},"m_out_of_range");
  mutation({1,2,1,0,0},"m_popcount"); mutation({3,2,0,0,0},"result_not_one");
  mutation({3,2,1,4,0},"A_not_subset_W");
  expect_fail([&]{Coverage c(4,2,2);c.add(good);c.add(good);},"duplicate_W"); ++coverage_bad;
  expect_fail([&]{Coverage c(4,2,2);c.add(good);c.finish();},"coverage_mismatch"); ++coverage_bad;
  Coverage full(4,0,4); for(Mask w=0;w<16;++w) full.add({w,uint64_t(pc(w)),1,0,0}); full.finish();
  std::vector<int> perm={0,1,2,3,4,5};
  do {
    std::vector<Point> p; for(int i=0;i<6;++i) p.push_back({i,perm[i]});
    bool gp=true; for(int a=0;a<6;++a) for(int b=a+1;b<6;++b) for(int c=b+1;c<6;++c) gp&=det(p[a],p[b],p[c])!=0;
    if(!gp) continue;
    Geometry h(p); ++small_sets;
    for(Mask s=0;s<=h.full;++s) {
      bool c4=false,c5=false,g6=false,n4=false;
      for(Mask q:h.c4) c4|=(q&s)==q;
      for(Mask q:h.c5) c5|=(q&s)==q;
      for(Mask q:h.g6) g6|=(q&s)==q;
      for(Mask q:h.non4) n4|=(q&s)==q;
      need(bool(h.flags[s]&1)==c4 && bool(h.flags[s]&2)==c5 && bool(h.flags[s]&4)==g6 && bool(h.flags[s]&16)==n4,"closure_control");
      need(h.convex_direct(s)==h.convex_support(s),"supporting_edge_control"); ++closure_queries;
      for(int b=0;b<6;++b) if(s&bit(b)) for(int c=b+1;c<6;++c) if(s&bit(c)) {
        bool direct=false;
        for(int u=0;u<b;++u) if(s&bit(u)) for(int v=u+1;v<b;++v) if(s&bit(v))
          direct |= det(h.p[u],h.p[v],h.p[b])<0 && det(h.p[v],h.p[b],h.p[c])<0;
        need(direct==h.supported(s,b,c),"terminal_support_control"); ++support_tests;
      }
    }
  } while(std::next_permutation(perm.begin(),perm.end()));
  // Convex and cap sign controls use large coordinates, including the admitted boundary.
  const int64_t B=int64_t(1)<<40;
  need(det({-B,-B},{B,-B},{-B,B})==I(4)*B*B,"large_exact_arithmetic");
  for(int sign:{-1,1}) {
    std::vector<Point> p; for(int i=0;i<7;++i) p.push_back({i,sign*i*i}); Geometry h(p);
    need(h.g7.size()==1 && h.g6.size()==7,"parabola_convexity");
    need(h.c5.size()==(sign<0?21u:0u),"parabola_cap_orientation");
    expect_fail([&]{h.ambient();},sign<0?"ambient_five_cap":"ambient_heptagon");
  }
  uint64_t real_support=0;
  for(int k:{4,6,7}) choose(real.n,k,[&](Mask s) {
    need(real.convex_support(s)==!(real.flags[s]&Geometry::NONCONVEX4),"real_supporting_edges"); ++real_support;
  });
  // Real positive row and three distinct semantic defects, all independently built.
  need(real.witness_error(131071,33326).empty(),"real_positive_row");
  need(real.witness_error(131071,0).find("unhit_hexagon=")==0,"unhit_hexagon_control");
  need(real.witness_error(real.full,real.c4.at(0)).find("four_cap=")==0,"four_cap_control");
  Mask w18=0,a18=0; for(int i:{2,3,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22}) w18|=bit(i);
  for(int i:{2,9,10,11,12}) a18|=bit(i);
  need(real.witness_error(w18,a18).find("unsupported_cap_triple=")==0,"unsafe_terminal_control");
  std::cout<<"{\"kind\":\"controls\",\"status\":\"PASS\",\"parser_rejections\":"<<parse_bad
    <<",\"coverage_rejections\":"<<coverage_bad<<",\"general_position_grid_sets\":"<<small_sets
    <<",\"closure_and_convexity_controls\":"<<closure_queries<<",\"terminal_support_controls\":"<<support_tests
    <<",\"real_supporting_edge_crosschecks\":"<<real_support
    <<",\"real_semantic_rejections\":3,\"real_positive_rows\":1,\"large_exact_arithmetic\":true}\n";
}
int main(int argc,char** argv) {
  try {
    need(argc>=3,"usage: audit MODE POINTS [ROWS LO HI WITNESS18]");
    Geometry g(read_points(argv[2])); g.ambient();
    std::string mode=argv[1];
    if(mode=="run") {
      need(argc==7,"run requires ROWS LO HI WITNESS18");
      stream(g,argv[3],std::stoi(argv[4]),std::stoi(argv[5])); mapped18(g,argv[6]);
    } else if(mode=="controls") { need(argc==3,"controls args"); controls(g); }
    else if(mode=="geometry") { g.print(); std::cout<<"\n"; }
    else need(false,"unknown_mode");
    return 0;
  } catch(const std::exception& e) { std::cerr<<"FAIL: "<<e.what()<<"\n"; return 1; }
}
