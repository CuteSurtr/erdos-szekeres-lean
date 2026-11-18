// Independent streaming encoder for D(5,n), weak / cup-side / cap-side.
// Build: g++ -std=c++17 -O2 -Wall -Wextra -pedantic delta_cnf.cpp -o delta_cnf
// Semantics and proof obligations are documented in DESIGN.md.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <functional>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = uint32_t;
static int size(Mask s) { return __builtin_popcount(s); }
static std::vector<int> vertices(Mask s) {
    std::vector<int> r;
    while (s) { int p=__builtin_ctz(s); r.push_back(p); s &= s-1; }
    return r;
}
template<class F> static void choose(Mask s, int k, F f) {
    // Recursive enumeration, no vector of subsets or clauses.
    auto rec = [&](auto&& self, Mask rem, int left, Mask out) -> void {
        if (!left) { f(out); return; }
        while (size(rem)>=left) {
            Mask bit=rem & (~rem+1); rem ^= bit;
            self(self,rem,left-1,out|bit);
        }
    };
    rec(rec,s,k,0);
}
struct Writer {
    FILE* file=nullptr;
    uint64_t clauses=0, literals=0, maxwidth=0;
    std::string phase;
    std::map<std::string,std::array<uint64_t,2>> counts;
    explicit Writer(const std::string& path) {
        if (!path.empty()) {
            file=std::fopen(path.c_str(),"wb+");
            if (!file) throw std::runtime_error("cannot open output");
            std::string pad(95,' '); pad+='\n';
            if (std::fwrite(pad.data(),1,pad.size(),file)!=pad.size())
                throw std::runtime_error("header write failed");
        }
    }
    ~Writer() { if(file) std::fclose(file); }
    void add(const std::vector<int>& c) {
        ++clauses; literals+=c.size(); maxwidth=std::max(maxwidth,uint64_t(c.size()));
        ++counts[phase][0]; counts[phase][1]+=c.size();
        if(file) {
            for(int x:c) {
                if(!x) throw std::runtime_error("zero used as literal");
                std::fprintf(file,"%d ",x);
            }
            std::fputs("0\n",file);
        }
    }
    uint64_t finish(int nv) {
        if (!file) return 0;
        if (std::ferror(file) || std::fflush(file)) throw std::runtime_error("CNF write failed");
        long bytes=std::ftell(file);
        if(bytes<0 || std::fseek(file,0,SEEK_SET)) throw std::runtime_error("seek failed");
        std::string h="p cnf "+std::to_string(nv)+" "+std::to_string(clauses);
        if(h.size()>95) throw std::runtime_error("header overflow");
        h.resize(95,' '); h+='\n';
        if(std::fwrite(h.data(),1,h.size(),file)!=h.size() || std::fflush(file))
            throw std::runtime_error("header rewrite failed");
        return uint64_t(bytes);
    }
};
struct Options {
    int m=0,n=0;
    std::string mode="cup",pool="lattice",sym="none",out,fix,cube;
    bool base=false,stats=false;
};
struct Encoder {
    Options o;
    Writer w;
    int nv=0,nt=0,lower=0,upper=0;
    Mask full=0;
    std::vector<int> tri,A,B,seed,q4,cup;
    std::map<std::array<int,3>,int> H;
    std::map<std::array<int,3>,std::vector<int>> supports;
    std::vector<std::array<int,3>> triples;
    explicit Encoder(Options x):o(x),w(o.out) {
        full=(Mask(1)<<o.m)-1;
        tri.resize(o.m*o.m*o.m);
        for(int i=0;i<o.m;++i) for(int j=i+1;j<o.m;++j) for(int k=j+1;k<o.m;++k) {
            tri[(i*o.m+j)*o.m+k]=++nv; triples.push_back({i,j,k});
        }
        nt=nv;
        if(!o.base) {
            A.resize(full+1); B.resize(full+1); seed.resize(full+1);
            q4.resize(full+1); cup.resize(full+1);
            lower=o.mode=="weak"?o.n-1:o.mode=="cup"?o.n-3:2;
            upper=o.mode=="cap"?4:o.n-1;
            for(Mask s=0;s<=full;++s)
                if(size(s)==4 || (o.pool=="lattice" && size(s)>4)) A[s]=++nv;
        }
    }
    int t(int i,int j,int k) const { return tri[(i*o.m+j)*o.m+k]; }
    std::vector<int> chain(Mask s, bool positive) const {
        auto v=vertices(s); std::vector<int> r;
        for(size_t i=2;i<v.size();++i) r.push_back((positive?1:-1)*t(v[i-2],v[i-1],v[i]));
        return r;
    }
    void imply(int var,const std::vector<int>& lits) {
        for(int l:lits) w.add({-var,l});
    }
    void base() {
        w.phase="signotope";
        choose(full,4,[&](Mask s) {
            auto v=vertices(s);
            std::array<int,4> q={t(v[0],v[1],v[2]),t(v[0],v[1],v[3]),t(v[0],v[2],v[3]),t(v[1],v[2],v[3])};
            // Forbid precisely the eight sign vectors with >=2 changes.
            for(int b=0;b<16;++b) {
                int changes=0;
                for(int i=1;i<4;++i) changes+=(((b>>i)^(b>>(i-1)))&1);
                if(changes<2) continue;
                std::vector<int> c;
                for(int i=0;i<4;++i)c.push_back((b&(1<<i))?-q[i]:q[i]);
                w.add(c);
            }
        });
        w.phase="no5cap";
        choose(full,5,[&](Mask s){w.add(chain(s,true));});
        w.phase="no_ngon";
        choose(full,o.n,[&](Mask s) {
            auto v=vertices(s); Mask ends=(Mask(1)<<v.front())|(Mask(1)<<v.back());
            Mask inner=s^ends;
            for(int r=0;r<=2;++r) choose(inner,r,[&](Mask u) {
                auto c=chain(u|ends,true); auto d=chain((inner^u)|ends,false);
                c.insert(c.end(),d.begin(),d.end()); w.add(c);
            });
        });
    }
    void cap_nodes() {
        w.phase="fourcap";
        choose(full,4,[&](Mask s){imply(A[s],chain(s,false));});
        if(o.pool!="lattice") return;
        w.phase="cap_lattice";
        for(Mask s=0;s<=full;++s) if(size(s)>4) {
            std::vector<int> c={-A[s]}; Mask rem=s;
            for(int i=0;i<5;++i) { Mask b=rem&(~rem+1); rem^=b; c.push_back(A[s^b]); }
            w.add(c);
        }
    }
    int endpoint(int u,int v,int k) const {
        auto it=H.find({u,v,k}); return it==H.end()?0:it->second;
    }
    void endpoint_nodes() {
        w.phase="endpoint_support";
        if(o.mode=="cup") {
            for(int u=0;u<o.m;++u) for(int v=u+2;v<o.m;++v) {
                std::vector<int> c;
                int h=H[{u,v,3}]=++nv; c.push_back(-h);
                for(int x=u+1;x<v;++x) c.push_back(-t(u,x,v));
                w.add(c);
                if(v-u<3) continue;
                h=H[{u,v,4}]=++nv; c={-h};
                for(int x=u+1;x<v;++x) for(int y=x+1;y<v;++y)
                    c.push_back(A[(Mask(1)<<u)|(Mask(1)<<x)|(Mask(1)<<y)|(Mask(1)<<v)]);
                w.add(c);
            }
        } else if(o.mode=="cap") {
            for(int k=o.n-3;k<=o.n-1;++k) choose(full,k,[&](Mask s) {
                auto v=vertices(s); int z=cup[s]=++nv; imply(z,chain(s,true));
                supports[{v.front(),v.back(),k}].push_back(z);
            });
            for(auto& [key,values]:supports) {
                int h=H[key]=++nv; std::vector<int> c={-h};
                c.insert(c.end(),values.begin(),values.end()); w.add(c);
            }
        }
    }
    void seeds() {
        w.phase="target_seeds";
        if(o.mode=="weak") {
            choose(full,4,[&](Mask s) {
                auto p=vertices(s); int z=q4[s]=++nv;
                int a=t(p[0],p[1],p[2]),b=t(p[0],p[1],p[3]);
                int c=t(p[0],p[2],p[3]),d=t(p[1],p[2],p[3]);
                w.add({-z,-a,b});w.add({-z,a,-b});w.add({-z,-c,d});w.add({-z,c,-d});
            });
            choose(full,o.n-1,[&](Mask s) {
                int z=seed[s]=++nv;
                choose(s,4,[&](Mask q){w.add({-z,q4[q]});});
            });
        } else {
            for(int k=lower;k<=upper;++k) choose(full,k,[&](Mask s) {
                auto p=vertices(s); int u=p.front(),v=p.back(),other=o.n+1-k;
                // There must be room for all n-1 distinct vertices.
                if(v-u+1<o.n-1) return;
                int h=other==2?0:endpoint(u,v,other);
                if(other!=2 && !h) return;
                int z=seed[s]=++nv;
                imply(z,chain(s,o.mode=="cup"));
                if(h) w.add({-z,h});
            });
        }
    }
    void target_nodes() {
        if(o.pool!="lattice") return;
        w.phase="target_lattice";
        for(Mask s=0;s<=full;++s) if(size(s)>=lower) {
            std::vector<int> rhs; if(seed[s])rhs.push_back(seed[s]);
            Mask rem=s;
            for(int i=0;i<std::min(size(s),upper+1);++i) {
                Mask bit=rem&(~rem+1); rem^=bit;
                if(B[s^bit])rhs.push_back(B[s^bit]);
            }
            // 0 is a compile-time false constant, never an unconstrained variable.
            // Reuse a single child; allocate only genuine OR nodes.
            if(rhs.empty()) B[s]=0;
            else if(rhs.size()==1) B[s]=rhs[0];
            else {
                B[s]=++nv; rhs.insert(rhs.begin(),-B[s]); w.add(rhs);
            }
        }
    }
    void pool() {
        w.phase="forall_delta";
        for(Mask d=0;d<=full;++d) {
            std::vector<int> c;
            if(o.pool=="lattice") {
                if(A[d])c.push_back(A[d]);
                if(B[full^d])c.push_back(B[full^d]);
            } else {
                choose(d,4,[&](Mask s){c.push_back(A[s]);});
                for(int k=lower;k<=upper;++k)
                    choose(full^d,k,[&](Mask s){if(seed[s])c.push_back(seed[s]);});
            }
            w.add(c); // An empty clause is intentional, not skipped.
        }
    }
    void restrictions() {
        w.phase="mirror";
        if(o.sym=="mirror") {
            std::vector<std::array<int,2>> pairs;
            for(auto q:triples) {
                int x=t(q[0],q[1],q[2]);
                int y=t(o.m-1-q[2],o.m-1-q[1],o.m-1-q[0]);
                if(x<y)pairs.push_back({x,y});
            }
            if(!pairs.empty()) {
                int e=++nv; w.add({e});
                for(size_t i=0;i<pairs.size();++i) {
                    int x=pairs[i][0],y=pairs[i][1];
                    w.add({-e,-x,y});
                    if(i+1<pairs.size()) {
                        int f=++nv;
                        w.add({-e,x,y,f}); w.add({-e,-x,-y,f}); e=f;
                    }
                }
            }
        }
        w.phase="cube";
        if(o.cube.size()>triples.size()) throw std::runtime_error("cube too long");
        for(size_t i=0;i<o.cube.size();++i) {
            char c=o.cube[i]; if(c!='0'&&c!='1')throw std::runtime_error("cube must be a bit string");
            w.add({(c=='1'?1:-1)*int(i+1)});
        }
        w.phase="fixed_signs";
        if(!o.fix.empty()) {
            std::ifstream f(o.fix); std::string s; f>>s;
            if(s.size()!=triples.size()) throw std::runtime_error("wrong sign-string length");
            for(size_t i=0;i<s.size();++i) {
                if(s[i]!='+' && s[i]!='-')throw std::runtime_error("bad sign character");
                w.add({(s[i]=='+'?1:-1)*int(i+1)});
            }
        }
    }
    void run() {
        base();
        if(!o.base) {cap_nodes();endpoint_nodes();seeds();target_nodes();pool();}
        restrictions();
        uint64_t bytes=w.finish(nv);
        std::cout<<"{\"label\":\"COMPUTED\",\"a\":5,\"n\":"<<o.n<<",\"m\":"<<o.m
          <<",\"mode\":\""<<o.mode<<"\",\"pool\":\""<<o.pool<<"\",\"sym\":\""<<o.sym
          <<"\",\"cube\":\""<<o.cube<<"\",\"base_only\":"<<(o.base?"true":"false")
          <<",\"variables\":"<<nv<<",\"triples\":"<<nt<<",\"clauses\":"<<w.clauses
          <<",\"literals\":"<<w.literals<<",\"max_width\":"<<w.maxwidth<<",\"cnf_bytes\":"<<bytes
          <<",\"phases\":{";
        bool first=true;
        for(auto [name,c]:w.counts) { if(!first)std::cout<<',';first=false;
            std::cout<<'"'<<name<<"\":{\"clauses\":"<<c[0]<<",\"literals\":"<<c[1]<<'}'; }
        std::cout<<"}}\n";
    }
};
int main(int argc,char**argv) {
    try {
        Options o;
        for(int i=1;i<argc;++i) {
            std::string s=argv[i];
            if(s=="--base")o.base=true;
            else if(s=="--stats")o.stats=true;
            else if(s=="--help") {
                std::cout<<"delta_cnf --n 5..8 --m 4..20 --mode weak|cup|cap --out FILE\n"
                  <<"  [--pool lattice|flat] [--sym none|mirror] [--cube BITPREFIX]\n"
                  <<"  [--fix-signs FILE] [--base] [--stats (no file)]\n"; return 0;
            } else {
                if(i+1==argc)throw std::runtime_error("missing option value");
                std::string v=argv[++i];
                if(s=="--m")o.m=std::stoi(v);else if(s=="--n")o.n=std::stoi(v);
                else if(s=="--mode")o.mode=v;else if(s=="--pool")o.pool=v;
                else if(s=="--sym")o.sym=v;else if(s=="--out")o.out=v;
                else if(s=="--fix-signs")o.fix=v;else if(s=="--cube")o.cube=v;
                else throw std::runtime_error("unknown option: "+s);
            }
        }
        if(o.m<4||o.m>20||o.n<5||o.n>8)throw std::runtime_error("require 4<=m<=20, 5<=n<=8");
        if(o.mode!="cup"&&o.mode!="cap"&&o.mode!="weak")throw std::runtime_error("bad mode");
        if(o.pool!="lattice"&&o.pool!="flat")throw std::runtime_error("bad pool");
        if(o.sym!="none"&&o.sym!="mirror")throw std::runtime_error("bad symmetry");
        if(o.out.empty()&&!o.stats)throw std::runtime_error("specify --out or --stats");
        if(!o.out.empty()&&o.stats)throw std::runtime_error("--stats and --out are exclusive");
        Encoder(o).run();
    } catch(const std::exception& e) {std::cerr<<"ERROR: "<<e.what()<<'\n';return 1;}
}
