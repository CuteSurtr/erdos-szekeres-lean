// C++17, no external dependencies. Weak D(5,n) only. See SOUNDNESS.md.
#include <algorithm>
#include <array>
#include <cstdint>
#include <cstdio>
#include <fstream>
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

using Mask = uint32_t;
static int pc(Mask s) { return __builtin_popcount(s); }
static std::vector<int> vertices(Mask s) {
    std::vector<int> v;
    while (s) { v.push_back(__builtin_ctz(s)); s &= s-1; }
    return v;
}
template<class F> static void choose(Mask s, int k, F f) {
    auto rec = [&](auto&& self, Mask rem, int left, Mask out) -> void {
        if (!left) { f(out); return; }
        while (pc(rem)>=left) {
            Mask b=rem & -rem; rem ^= b;
            self(self,rem,left-1,out|b);
        }
    };
    rec(rec,s,k,0);
}
struct Options {
    int m=0,n=0;
    std::string convex="recurrence",pool="reduced",containment="witness";
    std::string out,mapfile,fix;
    bool base=false,stats=false;
};
struct Writer {
    FILE* file=nullptr;
    uint64_t clauses=0,literals=0,maxwidth=0;
    std::string phase;
    std::map<std::string,std::array<uint64_t,2>> counts;
    explicit Writer(const std::string& path) {
        if (path.empty()) return;
        file=std::fopen(path.c_str(),"wb+");
        if (!file) throw std::runtime_error("cannot open CNF output");
        std::string h(95,' '); h+='\n';
        if (std::fwrite(h.data(),1,h.size(),file)!=h.size())
            throw std::runtime_error("initial header failed");
    }
    ~Writer() { if(file) std::fclose(file); }
    void set_phase(const std::string& name) {
        phase=name;
        if (file) std::fprintf(file,"c phase %s\n",name.c_str());
    }
    void add(const std::vector<int>& c) {
        ++clauses; literals+=c.size();
        maxwidth=std::max(maxwidth,uint64_t(c.size()));
        ++counts[phase][0]; counts[phase][1]+=c.size();
        for (int x:c) if (!x) throw std::runtime_error("zero literal");
        if (file) {
            for (int x:c) std::fprintf(file,"%d ",x);
            std::fputs("0\n",file);
        }
    }
    uint64_t finish(int nv) {
        if (!file) return 0;
        if (std::ferror(file)||std::fflush(file)) throw std::runtime_error("CNF write failed");
        long bytes=std::ftell(file);
        if (bytes<0||std::fseek(file,0,SEEK_SET)) throw std::runtime_error("CNF seek failed");
        std::string h="p cnf "+std::to_string(nv)+" "+std::to_string(clauses);
        if (h.size()>95) throw std::runtime_error("header too long");
        h.resize(95,' '); h+='\n';
        if (std::fwrite(h.data(),1,h.size(),file)!=h.size()||std::fflush(file))
            throw std::runtime_error("CNF header failed");
        return uint64_t(bytes);
    }
};
struct Encoder {
    Options o;
    Writer w;
    std::ofstream mapping;
    Mask full;
    int nv=0,nt=0,amin=0,amax=0,bmax=0;
    std::vector<int> tri,Q,A,B;
    explicit Encoder(Options opt):o(opt),w(o.out),full((Mask(1)<<o.m)-1),
        tri(o.m*o.m*o.m),Q(full+1),A(full+1),B(full+1) {
        if(!o.mapfile.empty()) {
            mapping.open(o.mapfile);
            if(!mapping) throw std::runtime_error("cannot open variable map");
            mapping<<"# id kind mask; indices are zero based in increasing x order\n";
        }
        for(int i=0;i<o.m;++i) for(int j=i+1;j<o.m;++j) for(int k=j+1;k<o.m;++k)
            tri[(i*o.m+j)*o.m+k]=fresh("orientation",(Mask(1)<<i)|(Mask(1)<<j)|(Mask(1)<<k));
        nt=nv;
        amin=o.pool=="reduced"?3:0;
        amax=o.pool=="reduced"?o.m-o.n+2:o.m;
        bmax=o.pool=="reduced"?o.m-3:o.m;
    }
    int fresh(const char* kind,Mask s) {
        ++nv; if(mapping) mapping<<nv<<' '<<kind<<' '<<s<<'\n';
        return nv;
    }
    int t(int a,int b,int c) const { return tri[(a*o.m+b)*o.m+c]; }
    std::vector<int> children(Mask s,const std::vector<int>& ids,int count) const {
        std::vector<int> v;
        Mask rem=s;
        for(int i=0;i<count;++i) {
            if (!rem) throw std::runtime_error("too many selected deletions");
            // Keep the original mask: each child deletes just one vertex.
            Mask bit=rem & -rem;
            rem ^= bit;
            int id=ids[s^bit];
            if(!id) throw std::runtime_error("missing child flag");
            v.push_back(id);
        }
        return v;
    }
    void conjunction(int z,const std::vector<int>& v) {
        std::vector<int> back={z};
        for(int x:v) { w.add({-z,x}); back.push_back(-x); }
        w.add(back);
    }
    void disjunction(int z,const std::vector<int>& v) {
        std::vector<int> forward={-z};
        forward.insert(forward.end(),v.begin(),v.end()); w.add(forward);
        if(o.containment=="exact") for(int x:v) w.add({-x,z});
    }
    void geometry() {
        w.set_phase("signotope");
        choose(full,4,[&](Mask s) {
            auto p=vertices(s);
            std::array<int,4> v={t(p[0],p[1],p[2]),t(p[0],p[1],p[3]),
                                 t(p[0],p[2],p[3]),t(p[1],p[2],p[3])};
            // No alternating subsequence: exactly at most one sign change.
            for(int i=0;i<4;++i) for(int j=i+1;j<4;++j) for(int k=j+1;k<4;++k) {
                w.add({-v[i],v[j],-v[k]}); w.add({v[i],-v[j],v[k]});
            }
        });
        w.set_phase("no5cap");
        choose(full,5,[&](Mask s) {
            auto p=vertices(s);
            w.add({t(p[0],p[1],p[2]),t(p[1],p[2],p[3]),t(p[2],p[3],p[4])});
        });
        w.set_phase("convex4_equivalence");
        choose(full,4,[&](Mask s) {
            auto p=vertices(s); int z=Q[s]=fresh("convex",s);
            int a=t(p[0],p[1],p[2]),b=t(p[0],p[1],p[3]);
            int c=t(p[0],p[2],p[3]),d=t(p[1],p[2],p[3]);
            // z => a=b and c=d.
            w.add({-z,-a,b});w.add({-z,a,-b});
            w.add({-z,-c,d});w.add({-z,c,-d});
            // With the signotope axiom, convex iff a=d or b!=c.
            w.add({z,a,d});w.add({z,-a,-d});
            w.add({z,b,-c});w.add({z,-b,c});
        });
        w.set_phase("convex_larger_equivalence");
        for(int k=5;k<=o.n-1;++k) {
            if(o.convex=="direct" && k!=o.n-1) continue;
            choose(full,k,[&](Mask s) {
                int z=Q[s]=fresh("convex",s);
                std::vector<int> v;
                if(o.convex=="recurrence") v=children(s,Q,5);
                else choose(s,4,[&](Mask q){v.push_back(Q[q]);});
                conjunction(z,v);
            });
        }
        w.set_phase("no_ngon");
        choose(full,o.n,[&](Mask s) {
            std::vector<int> v;
            if(o.convex=="recurrence") v=children(s,Q,5);
            else choose(s,4,[&](Mask q){v.push_back(Q[q]);});
            for(int& x:v) x=-x;
            w.add(v);
        });
    }
    void containment() {
        w.set_phase("fourcap");
        if(amax>=4) choose(full,4,[&](Mask s) {
            auto p=vertices(s); int z=A[s]=fresh("cap_contains",s);
            int a=t(p[0],p[1],p[2]),d=t(p[1],p[2],p[3]);
            w.add({-z,-a});w.add({-z,-d});
            if(o.containment=="exact") w.add({z,a,d});
        });
        w.set_phase("cap_lattice");
        for(Mask s=0;s<=full;++s) if(pc(s)>4 && pc(s)<=amax) {
            int z=A[s]=fresh("cap_contains",s);
            disjunction(z,children(s,A,5));
        }
        w.set_phase("target_lattice");
        for(Mask s=0;s<=full;++s) {
            int k=pc(s);
            if(k==o.n-1 && k<=bmax) B[s]=Q[s];
            else if(k>o.n-1 && k<=bmax) {
                int z=B[s]=fresh("target_contains",s);
                disjunction(z,children(s,B,o.n));
            }
        }
        w.set_phase("forall_delta");
        // If the reduced interval is empty, |Delta|<=3 and |V\Delta|<n-1
        // can hold together; such a Delta works regardless of orientations.
        if(amax<amin) { w.add({}); return; }
        for(Mask d=0;d<=full;++d) if(pc(d)>=amin && pc(d)<=amax) {
            std::vector<int> c;
            if(A[d])c.push_back(A[d]);
            if(B[full^d])c.push_back(B[full^d]);
            w.add(c);
        }
    }
    void run() {
        geometry();
        if(!o.base)containment();
        w.set_phase("fixed_signs");
        if(!o.fix.empty()) {
            std::ifstream f(o.fix);std::string s,extra;f>>s;
            if(!f||int(s.size())!=nt||f>>extra) throw std::runtime_error("bad sign file length");
            for(int i=0;i<nt;++i) {
                if(s[i]!='+'&&s[i]!='-')throw std::runtime_error("bad sign character");
                w.add({s[i]=='+'?i+1:-i-1});
            }
        }
        uint64_t bytes=w.finish(nv);
        if(mapping) { mapping.flush(); if(!mapping)throw std::runtime_error("map write failed"); }
        std::cout<<"{\"label\":\"COMPUTED\",\"mode\":\"weak\",\"a\":5,\"m\":"<<o.m
          <<",\"n\":"<<o.n<<",\"convex\":\""<<o.convex<<"\",\"pool\":\""<<o.pool
          <<"\",\"containment\":\""<<o.containment<<"\",\"sym\":\"none\",\"base_only\":"
          <<(o.base?"true":"false")<<",\"fixed_signs\":"<<(!o.fix.empty()?"true":"false")
          <<",\"variables\":"<<nv<<",\"triples\":"<<nt<<",\"clauses\":"<<w.clauses
          <<",\"literals\":"<<w.literals<<",\"max_width\":"<<w.maxwidth
          <<",\"cnf_bytes\":"<<bytes<<",\"phases\":{";
        bool first=true;
        for(auto [name,c]:w.counts) {
            if(!first)std::cout<<',';
            first=false;
            std::cout<<'"'<<name<<"\":{\"clauses\":"<<c[0]<<",\"literals\":"<<c[1]<<'}';
        }
        std::cout<<"}}\n";
    }
};
int main(int argc,char**argv) {
    try {
        Options o;
        for(int i=1;i<argc;++i) {
            std::string a=argv[i];
            if(a=="--base")o.base=true;
            else if(a=="--stats")o.stats=true;
            else if(a=="--help") {
                std::cout<<"compact_cnf --m 4..16 --n 5..8 (--out FILE | --stats)\n"
                  <<" [--convex recurrence|direct] [--pool reduced|all]\n"
                  <<" [--containment witness|exact] [--map FILE] [--base] [--fix-signs FILE]\n";
                return 0;
            } else {
                if(i+1>=argc)throw std::runtime_error("missing argument");
                std::string v=argv[++i];
                if(a=="--m")o.m=std::stoi(v);else if(a=="--n")o.n=std::stoi(v);
                else if(a=="--out")o.out=v;else if(a=="--map")o.mapfile=v;
                else if(a=="--convex")o.convex=v;else if(a=="--pool")o.pool=v;
                else if(a=="--containment")o.containment=v;else if(a=="--fix-signs")o.fix=v;
                else throw std::runtime_error("unknown option: "+a);
            }
        }
        if(o.m<4||o.m>16||o.n<5||o.n>8)throw std::runtime_error("need 4<=m<=16, 5<=n<=8");
        if(o.convex!="recurrence"&&o.convex!="direct")throw std::runtime_error("bad convex mode");
        if(o.pool!="reduced"&&o.pool!="all")throw std::runtime_error("bad pool mode");
        if(o.containment!="witness"&&o.containment!="exact")throw std::runtime_error("bad containment mode");
        if(o.out.empty()==!o.stats)throw std::runtime_error("use exactly one of --out and --stats");
        Encoder(o).run();
    } catch(const std::exception& e) { std::cerr<<"ERROR: "<<e.what()<<'\n';return 1; }
}
