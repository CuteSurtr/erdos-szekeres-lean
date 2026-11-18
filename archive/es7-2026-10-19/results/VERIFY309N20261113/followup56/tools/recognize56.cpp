// Independent family recognizer, adapted mathematically from audit_mono.py.
// No original N66 encoder/checker code is called. Only quads actually appearing
// in the trimmed input need enumeration; each candidate is compared exactly.
#include <algorithm>
#include <array>
#include <fstream>
#include <iostream>
#include <numeric>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
void require(bool x, const string& s) { if (!x) throw runtime_error(s); }
struct Hash {
    size_t operator()(const vector<int>& v) const {
        size_t h=1469598103934665603ull;
        for (int x:v) { h^=static_cast<unsigned>(x); h*=1099511628211ull; }
        return h;
    }
};
struct Entry { int copies=0, family=-1; };
unordered_map<vector<int>,Entry,Hash> wanted;
unordered_set<unsigned> quadkeys;
vector<array<int,4>> states;
unsigned cells[70], plain[70][70], refined[70][70];
int lo[70][70][2], hi[70][70][2], pairid[70][70];
int ori[70][70][70], chainid[70][70][70], endpointid[70][70];
int firstsel, top;
constexpr int TRUE_LIT=2000000000;
vector<string> names={"threshold","empty","domain","forced_sign","transitivity",
    "growth","chain_start","end_exclusion","end_implication","packet","chain_step",
    "fixed","row","counter","sb"};
long long generated[15]={}, unique_used[15]={}, occurrences[15]={};
unsigned quadkey(const vector<int>& q) { unsigned k=0; for (int a:q) k=k*70+a; return k; }
int before(int a,int b) { return a<b?pairid[a][b]:-pairid[b][a]; }
int ge(int t,int a,int b,int k) {
    if (k==1) return TRUE_LIT;
    if (k==5) return -TRUE_LIT;
    return pairid[min(a,b)][max(a,b)]+(t==0?1:4)+k-2;
}
void emit(int fam, vector<int> v, initializer_list<int> owners={}) {
    ++generated[fam];
    if (find(v.begin(),v.end(),TRUE_LIT)!=v.end()) return;
    v.erase(remove(v.begin(),v.end(),-TRUE_LIT),v.end());
    for (int a:owners) v.push_back(-firstsel-a);
    sort(v.begin(),v.end());
    v.erase(unique(v.begin(),v.end()),v.end());
    for (int a:v) if (binary_search(v.begin(),v.end(),-a)) return;
    auto p=wanted.find(v);
    if (p!=wanted.end() && p->second.family<0) {
        p->second.family=fam; ++unique_used[fam]; occurrences[fam]+=p->second.copies;
    }
}
bool positive(int a,int b,int c) {
    array<int,3> q={0,1,2}; int own[3]={a,b,c};
    do {
        int x=own[q[0]], y=own[q[1]], z=own[q[2]];
        if (!plain[x][y]||!plain[y][z]||!plain[x][z]) continue;
        int axis=((q[0]>q[1])+(q[0]>q[2])+(q[1]>q[2]))%2;
        if (hi[y][z][axis]>lo[x][y][axis]) return false;
    } while(next_permutation(q.begin(),q.end()));
    return true;
}
void catalog() {
    for(int a=0;a<=4;++a) for(int b=0;b<=a;++b)
    for(int c=0;c<=b;++c) for(int d=0;d<=c;++d) states.push_back({a,b,c,d});
    sort(states.begin(),states.end(),[](auto a,auto b) {
        int sa=accumulate(a.begin(),a.end(),0), sb=accumulate(b.begin(),b.end(),0);
        return sa==sb?a<b:sa<sb;
    });
    require(states.size()==70,"catalog size");
    for(int s=0;s<70;++s) for(int a=1;a<=4;++a)
    for(int b=1;b<=states[s][a-1];++b) cells[s]|=1u<<((a-1)*4+b-1);
    for(int s=0;s<70;++s) for(int t=0;t<70;++t) {
        plain[s][t]=cells[t]&~cells[s];
        int cap=0; for(int h:states[s]) cap+=h>0;
        lo[s][t][0]=lo[s][t][1]=5;
        for(int a=1;a<=4;++a) for(int b=1;b<=4;++b) {
            unsigned bit=1u<<((a-1)*4+b-1);
            if (!(plain[s][t]&bit)) continue;
            lo[s][t][0]=min(lo[s][t][0],a); lo[s][t][1]=min(lo[s][t][1],b);
            hi[s][t][0]=max(hi[s][t][0],a); hi[s][t][1]=max(hi[s][t][1],b);
            if(a<=cap+1 && b<=states[s][0]+1) refined[s][t]|=bit;
        }
    }
    int n=0;
    for(int a=0;a<70;++a) for(int b=a+1;b<70;++b) pairid[a][b]=1+7*n++;
    top=7*n;
    for(int a=0;a<70;++a) for(int b=a+1;b<70;++b) for(int c=b+1;c<70;++c) {
        ++top; array<int,3> q={a,b,c};
        do {
            int parity=((q[0]>q[1])+(q[0]>q[2])+(q[1]>q[2]))%2;
            ori[q[0]][q[1]][q[2]]=parity?-top:top;
        } while(next_permutation(q.begin(),q.end()));
    }
    top+=70*69*68*67/24;
    firstsel=top+1; top+=70;
}
void pairs_and_triples() {
    for(int a=0;a<70;++a) for(int b=a+1;b<70;++b) {
        for(int t=0;t<2;++t) for(int k=2;k<=3;++k)
            emit(0,{-ge(t,a,b,k+1),ge(t,a,b,k)},{a,b});
        for(int r=0;r<2;++r) {
            int u=r?b:a,v=r?a:b;
            if (!refined[u][v]) { emit(1,{-before(u,v)},{u,v}); continue; }
            for(int x=1;x<=4;++x) for(int y=1;y<=4;++y)
            if (!(refined[u][v]&(1u<<((x-1)*4+y-1))))
                emit(2,{-before(u,v),-ge(0,a,b,x),ge(0,a,b,x+1),
                    -ge(1,a,b,y),ge(1,a,b,y+1)},{u,v});
        }
    }
    for(int a=0;a<70;++a) for(int b=a+1;b<70;++b) for(int c=b+1;c<70;++c) {
        if(positive(a,b,c)) emit(3,{ori[a][b][c]},{a,b,c});
        else if(positive(a,c,b)) emit(3,{-ori[a][b][c]},{a,b,c});
    }
    for(int a=0;a<70;++a) for(int b=0;b<70;++b) for(int c=0;c<70;++c) {
        if(a==b||a==c||b==c||!refined[a][b]||!refined[b][c]) continue;
        emit(4,{-before(a,b),-before(b,c),before(a,c)},{a,b,c});
        if(!refined[a][c]) continue;
        chainid[a][b][c]=top+1; top+=6;
        for(int t=0;t<2;++t) {
            int o=t?-ori[a][b][c]:ori[a][b][c];
            for(int k=1;k<=4;++k)
                emit(5,{-before(a,b),-before(b,c),o,-ge(t,a,b,k),ge(t,b,c,k+1)},{a,b,c});
            emit(6,{-before(a,b),-before(b,c),o,chainid[a][b][c]+t},{a,b,c});
        }
    }
    for(int a=0;a<70;++a) for(int b=0;b<70;++b) for(int c=0;c<70;++c) {
        int v=chainid[a][b][c]; if(!v) continue;
        if(!endpointid[a][c]) { endpointid[a][c]=top+1; top+=2;
            emit(7,{-endpointid[a][c],-endpointid[a][c]-1},{a,c}); }
        for(int t=0;t<2;++t) emit(8,{-v-4-t,endpointid[a][c]+t},{a,b,c});
    }
}
void quads() {
    vector<int> bad;
    for(int m=0;m<16;++m) {
        int changes=0;
        for(int j=0;j<3;++j) changes+=((m>>j)&1)!=((m>>(j+1))&1);
        if(changes>1) bad.push_back(m);
    }
    require(bad.size()==8,"packet patterns");
    for(unsigned key:quadkeys) {
        array<int,4> q; for(int j=3;j>=0;--j) { q[j]=key%70; key/=70; }
        array<int,4> own=q;
        do {
            int a=q[0],b=q[1],c=q[2],d=q[3];
            if(!refined[a][b]||!refined[a][c]||!refined[a][d]||
               !refined[b][c]||!refined[b][d]||!refined[c][d]) continue;
            int signs[4]={ori[a][b][c],ori[a][b][d],ori[a][c][d],ori[b][c][d]};
            for(int bits:bad) {
                vector<int> v={-before(a,b),-before(b,c),-before(c,d)};
                for(int j=0;j<4;++j) v.push_back((bits>>j)&1?-signs[j]:signs[j]);
                emit(9,v,{own[0],own[1],own[2],own[3]});
            }
            require(chainid[a][b][c] && chainid[a][c][d],"chain allocation");
            for(int k=3;k<=4;++k) for(int t=0;t<2;++t)
                emit(10,{-chainid[a][b][c]-2*(k-3)-t,-before(c,d),t?-signs[3]:signs[3],
                    chainid[a][c][d]+2*(k-2)+t},{own[0],own[1],own[2],own[3]});
        } while(next_permutation(q.begin(),q.end()));
    }
}
int main(int argc,char**argv) { try {
    require(argc==3,"usage: recognize56 trim.cnf independent-tail.txt");
    catalog();
    ifstream f(argv[1]); require(bool(f),"open CNF");
    string s; getline(f,s); istringstream hd(s); string p,cnf; int nv,nc;
    require(bool(hd>>p>>cnf>>nv>>nc)&&p=="p"&&cnf=="cnf","header");
    long long count=0; int maxvar=0;
    while(getline(f,s)) {
        istringstream in(s); vector<int> v,owners; int l; bool zero=false,allsel=true;
        while(in>>l) { if(l==0) {zero=true;break;} v.push_back(l);
            require(abs(l)<=nv,"literal outside header"); maxvar=max(maxvar,abs(l));
            if(l<=-firstsel && l>-firstsel-70) owners.push_back(-l-firstsel);
            else allsel=false;
        }
        string rest; require(zero&&!(in>>rest),"bad clause line");
        sort(v.begin(),v.end()); require(adjacent_find(v.begin(),v.end())==v.end(),"duplicate literal");
        for(int x:v) require(!binary_search(v.begin(),v.end(),-x),"tautology");
        wanted[v].copies++; ++count;
        if(owners.size()==4 && !allsel) {sort(owners.begin(),owners.end());quadkeys.insert(quadkey(owners));}
    }
    require(count==nc,"clause count");
    pairs_and_triples(); quads();
    ifstream tail(argv[2]); require(bool(tail),"open independent tail");
    string meta; int mt,ct,tv,s0,s1;
    require(bool(tail>>meta>>mt>>ct>>tv>>s0>>s1)&&meta=="meta","tail header");
    require(top==mt&&firstsel==s0&&firstsel+69==s1&&nv==tv,"independent numbering mismatch");
    string name;
    while(tail>>name) {
        auto n=find(names.begin(),names.end(),name); require(n!=names.end(),"tail family");
        int fam=n-names.begin(); require(fam>=11,"invalid tail family");
        vector<int> v; int l; bool zero=false;
        while(tail>>l) {if(l==0){zero=true;break;}v.push_back(l);}
        require(zero,"tail terminator"); emit(fam,v);
    }
    long long unknown=0;
    for(const auto& [v,e]:wanted) if(e.family<0) {
        if(unknown<5) {cerr<<"unrecognized:";for(int x:v)cerr<<' '<<x;cerr<<'\n';}
        unknown+=e.copies;
    }
    cout<<"{\"label\":\"COMPUTED\",\"clauses\":"<<nc<<",\"distinct\":"<<wanted.size()
        <<",\"mono_top\":"<<top<<",\"header_vars\":"<<nv<<",\"max_var\":"<<maxvar
        <<",\"quad_supports_checked\":"<<quadkeys.size()<<",\"unrecognized\":"<<unknown<<",\"families\":{";
    for(int j=0;j<15;++j) {
        if(j)cout<<',';
        cout<<'"'<<names[j]<<"\":{\"distinct\":"<<unique_used[j]<<",\"occurrences\":"
            <<occurrences[j]<<",\"generated_candidates\":"<<generated[j]<<'}';
    }
    cout<<"}}\n"; return unknown?1:0;
} catch(const exception& e) {cerr<<e.what()<<'\n';return 2;} }
