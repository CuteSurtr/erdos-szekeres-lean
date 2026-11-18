#include <algorithm>
#include <array>
#include <cassert>
#include <cstdint>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

// Input records: name n m, followed by m integer coordinate pairs, x-increasing.
// Exhaustive real geometry and one O(m*2^m) directed min-plus transform.
struct Point { long long x,y; };
static __int128 cross(Point a,Point b,Point c) {
    return ((__int128)b.x-a.x)*((__int128)c.y-a.y)
           -((__int128)b.y-a.y)*((__int128)c.x-a.x);
}
static void ids(unsigned mask) {
    cout << '['; bool first=true;
    while(mask) { int i=__builtin_ctz(mask); mask&=mask-1;
        if(!first) cout<<','; first=false; cout<<i; }
    cout << ']';
}
int main() {
    string name; int n,m;
    while(cin>>name>>n>>m) {
        if(m<1 || m>16 || n<5 || n>10) return 2;
        vector<Point> p(m); for(auto& q:p) {
            if(!(cin>>q.x>>q.y)) return 3;
            // Bound makes all intermediate __int128 products safe.
            if(q.x < -1000000000000000LL || q.x > 1000000000000000LL ||
               q.y < -1000000000000000LL || q.y > 1000000000000000LL) return 4;
        }
        bool ordered=true; for(int i=1;i<m;++i) ordered &= p[i-1].x<p[i].x;
        int sign[16][16][16]={}; int zeros=0;
        for(int a=0;a<m;++a) for(int b=a+1;b<m;++b) for(int c=b+1;c<m;++c) {
            auto v=cross(p[a],p[b],p[c]); sign[a][b][c]=(v>0)-(v<0); zeros += !v;
        }
        unsigned N=1u<<m, all=N-1;
        vector<uint8_t> badcap(N,0), hasgon(N,0);
        vector<unsigned> caps,gons; int fivecaps=0, ngons=0;
        for(unsigned mask=0;mask<N;++mask) {
            int s=__builtin_popcount(mask);
            if(s!=4 && s!=5 && s!=n-1 && s!=n) continue;
            vector<int> v; for(int i=0;i<m;++i) if(mask>>i&1) v.push_back(i);
            if(s==4 || s==5) {
                bool cap=true; for(int i=2;i<s;++i) cap &= sign[v[i-2]][v[i-1]][v[i]]<0;
                if(cap && s==4) { caps.push_back(mask); badcap[mask]=1; }
                if(cap && s==5) ++fivecaps;
            }
            if(s==n-1 || s==n) {
                vector<int> lo,hi;
                for(int j:v) {
                    while(lo.size()>=2 && cross(p[lo[lo.size()-2]],p[lo.back()],p[j])<=0) lo.pop_back();
                    lo.push_back(j);
                    while(hi.size()>=2 && cross(p[hi[hi.size()-2]],p[hi.back()],p[j])>=0) hi.pop_back();
                    hi.push_back(j);
                }
                bool convex=int(lo.size()+hi.size())-2==s;
                if(convex && s==n-1) { gons.push_back(mask); hasgon[mask]=1; }
                if(convex && s==n) ++ngons;
            }
        }
        cout << "{\"name\":\""<<name<<"\",\"n\":"<<n<<",\"m\":"<<m
             <<",\"ordered_x\":"<<(ordered?"true":"false")<<",\"collinear_triples\":"<<zeros
             <<",\"fivecaps\":"<<fivecaps<<",\"ngons\":"<<ngons
             <<",\"fourcaps\":"<<caps.size()<<",\"targets\":"<<gons.size();
        if(!ordered || zeros || fivecaps || ngons) { cout<<",\"valid\":false}\n"; continue; }
        for(int i=0;i<m;++i) for(unsigned x=0;x<N;++x) if(x>>i&1) {
            badcap[x] |= badcap[x^(1u<<i)]; hasgon[x] |= hasgon[x^(1u<<i)];
        }
        constexpr int INF=100;
        vector<int> dist(N,INF); vector<unsigned> arg(N,all); int full=0;
        for(unsigned B=0;B<N;++B) if(!badcap[B]&&!hasgon[all^B]) {
            dist[B]=0; arg[B]=B; ++full;
        }
        for(int i=0;i<m;++i) for(unsigned x=0;x<N;++x) if(!(x>>i&1)) {
            unsigned y=x|(1u<<i), a0=arg[x],a1=arg[y]; int d0=dist[x],d1=dist[y];
            // Output bit zero pays 1 for an input bit one; bit one is free.
            if(d1+1<d0) { dist[x]=d1+1; arg[x]=a1; }
            if(d0<d1) { dist[y]=d0; arg[y]=a0; }
        }
        cout<<",\"valid\":true,\"full_deltas\":"<<full<<",\"roots\":[";
        for(int r=0;r<m;++r) {
            unsigned rb=1u<<r; array<unsigned,101> hist{}; unsigned worstA=0; int worst=-1;
            for(unsigned A=0;A<N;++A) if(!(A&rb)&&!badcap[A]&&!hasgon[all^(A|rb)]) {
                int d=dist[A|rb]; ++hist[d];
                if(d>worst || (d==worst && __builtin_popcount(A)<__builtin_popcount(worstA))) { worst=d; worstA=A; }
            }
            if(r) cout<<',';
            cout<<"{\"r\":"<<r<<",\"hist\":{"; bool first=true;
            for(int d=0;d<=INF;++d) if(hist[d]) { if(!first)cout<<','; first=false; cout<<'"'<<d<<"\":"<<hist[d]; }
            cout<<"},\"max_cost\":"<<worst<<",\"A\":"; ids(worstA);
            cout<<",\"best_B\":"; ids(arg[worstA|rb]); cout<<'}';
        }
        cout<<"]}\n"; cout.flush();
    }
}
