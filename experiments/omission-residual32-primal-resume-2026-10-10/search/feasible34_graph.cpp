#include <array>
#include <vector>
#include <unordered_set>
#include <unordered_map>
#include <iostream>
#include <fstream>
#include <chrono>
#include <cstdint>
#include <cassert>
using namespace std;
struct Bits { array<uint64_t,3> w{}; bool operator==(Bits const& o)const{return w==o.w;} bool test(int i)const{return (w[i/64]>>(i%64))&1;} void flip(int i){w[i/64]^=1ULL<<(i%64);} int count()const{return __builtin_popcountll(w[0])+__builtin_popcountll(w[1])+__builtin_popcountll(w[2]);} };
Bits operator&(Bits a,Bits b){for(int k=0;k<3;k++)a.w[k]&=b.w[k];return a;}
struct Hash{size_t operator()(Bits const&a)const{size_t h=1469598103934665603ULL;for(auto x:a.w){h^=x;h*=1099511628211ULL;}return h;}};
void output(Bits b){cout<<'[';bool first=true;for(int i=0;i<154;i++)if(b.test(i)){if(!first)cout<<',';cout<<i;first=false;}cout<<']';}
int main(int argc,char**argv){assert(argc==4);ifstream f(argv[1]);int n,m,ns;f>>n>>m>>ns;assert(n==154&&(m==2598||m==2646));vector<Bits> rows(m);vector<int> rhs(m);for(int j=0;j<m;j++){int l;f>>rhs[j]>>l;while(l--){int i;f>>i;rows[j].flip(i);}}
vector<Bits> q;unordered_set<Bits,Hash> seen;seen.reserve(1000000);for(int k=0;k<ns;k++){Bits b;for(int j=0;j<34;j++){int i;f>>i;b.flip(i);}assert(b.count()==34&&!b.test(0));for(int j=0;j<m;j++)assert((b&rows[j]).count()>=rhs[j]);if(seen.insert(b).second)q.push_back(b);}
auto start=chrono::steady_clock::now();auto elapsed=[&](){return chrono::duration<double>(chrono::steady_clock::now()-start).count();};double budget=stod(argv[2]);size_t limit=stoull(argv[3]),head=0;uint64_t edges=0;bool found=false,bounded=false;Bits witness;unordered_map<int,Bits> near;vector<int> layer(q.size(),0);int maxdepth=0;
while(head<q.size()){
if(elapsed()>budget||q.size()>limit){bounded=true;break;}
Bits b=q[head];vector<int> holes;for(int i=1;i<n;i++)if(b.test(i))holes.push_back(i);Bits available;for(int i=1;i<n;i++)if(!b.test(i))available.flip(i);array<Bits,154> allowed;array<int,154> critical{};array<int,154> only{}; vector<int> almost;for(auto i:holes)allowed[i]=available;
for(int j=0;j<m;j++){int c=(b&rows[j]).count();assert(c>=rhs[j]);if(c==rhs[j]+1)almost.push_back(j);if(c==rhs[j]){for(int k=0;k<3;k++){uint64_t z=b.w[k]&rows[j].w[k];while(z){int i=k*64+__builtin_ctzll(z);z&=z-1;allowed[i]=allowed[i]&rows[j];critical[i]++;only[i]=j;}}}}
Bits removable;for(auto i:holes)if(critical[i]==0)removable.flip(i);
for(auto i:holes){if(!removable.test(i))continue;Bits pair=removable;pair.flip(i);array<int,154> after=critical;array<int,154> ar=only;
 for(auto j:almost)if(rows[j].test(i)){for(auto k:holes)if(rows[j].test(k)){after[k]++;ar[k]=j;}for(int k=0;k<3;k++)pair.w[k]&=~rows[j].w[k];}
 if(pair.count()){int k=0;while(!pair.w[k])k++;int j=64*k+__builtin_ctzll(pair.w[k]);witness=b;witness.flip(i);witness.flip(j);found=true;break;}
 for(auto j:holes)if(j!=i&&after[j]==1&&!near.count(ar[j])){Bits c=b;c.flip(i);c.flip(j);near[ar[j]]=c;cout<<"{\"event\":\"new_single_deficit\",\"row\":"<<ar[j]<<",\"holes\":";output(c);cout<<",\"processed\":"<<head<<",\"seconds\":"<<elapsed()<<"}"<<endl;}
}
if(found)break;
for(auto i:holes){for(int k=0;k<3;k++){uint64_t z=allowed[i].w[k];while(z){int a=k*64+__builtin_ctzll(z);z&=z-1;Bits c=b;c.flip(i);c.flip(a);edges++;if(seen.insert(c).second){q.push_back(c);layer.push_back(layer[head]+1);maxdepth=max(maxdepth,layer.back());}}}}
head++;if(head%10000==0)cout<<"{\"event\":\"progress\",\"processed\":"<<head<<",\"seen\":"<<q.size()<<",\"edges\":"<<edges<<",\"seconds\":"<<elapsed()<<",\"max_depth\":"<<maxdepth<<",\"diverse_near_models\":"<<near.size()<<"}"<<endl;
}
if(found){assert(witness.count()==32&&!witness.test(0));for(int j=0;j<m;j++)assert((witness&rows[j]).count()>=rhs[j]);}
cout<<"{\"event\":\"final\",\"processed\":"<<head<<",\"seen\":"<<q.size()<<",\"frontier\":"<<q.size()-head<<",\"edges\":"<<edges<<",\"seconds\":"<<elapsed()<<",\"component_exhausted\":"<<(!found&&!bounded?"true":"false")<<",\"witness_found\":"<<(found?"true":"false")<<",\"holes\":";output(witness);cout<<",\"max_depth\":"<<maxdepth<<",\"diverse_near_models\":"<<near.size()<<"}"<<endl;
}
