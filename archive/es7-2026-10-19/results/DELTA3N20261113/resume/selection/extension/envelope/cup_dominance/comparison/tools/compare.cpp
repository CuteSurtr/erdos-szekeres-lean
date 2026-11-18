#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>
using namespace std;
using Pt=array<long long,2>;using Pair=array<int,2>;
static signed char s[60][60][60];
static int rankcap[60][60];

bool cup(Pair p,Pair q){
 array<int,4>a={p[0],p[1],q[0],q[1]};sort(a.begin(),a.end());int k=unique(a.begin(),a.end())-a.begin();
 for(int i=0;i<k;i++)for(int j=i+1;j<k;j++)for(int t=j+1;t<k;t++)if(s[a[i]][a[j]][a[t]]<=0)return false;
 return true;
}
vector<int> signs(Pair p,Pair q){
 array<int,4>a={p[0],p[1],q[0],q[1]};sort(a.begin(),a.end());int k=unique(a.begin(),a.end())-a.begin();vector<int>r;
 for(int j=0;j<k;j++){
  int z=a[j];bool inP=z==p[0]||z==p[1],inQ=z==q[0]||z==q[1];
  r.push_back(inP&&inQ?0:inP?-s[q[0]][q[1]][z]:s[p[0]][p[1]][z]);
 }return r;
}
bool forced(Pair p,Pair q){
 if(p==q)return true;
 auto z=signs(p,q);if(z.back()<0)return false;
 for(size_t i=0;i+1<z.size();i++)if(z[i]<=0&&(z[i]<0||z.back()>0))return true;
 return false;
}
void pairout(ostream&o,Pair p){o<<'['<<p[0]<<','<<p[1]<<']';}
int main(int argc,char**argv){
 try{
  if(argc!=5)throw runtime_error("usage: compare input output first last");
  ifstream in(argv[1]);ifstream old(argv[2]);if(old.good())throw runtime_error("output exists");
  ofstream out(argv[2]);string magic;int total;in>>magic>>total;if(magic!="CUPCOMPARE1")throw runtime_error("input magic");
  int first=stoi(argv[3]),last=stoi(argv[4]);
  for(int index=0;index<total;index++){
   string name;int n,m;in>>name>>n>>m;if(!in||m<4||m>60)throw runtime_error("input size");
   vector<Pt>P(m);for(auto&p:P)in>>p[0]>>p[1];if(!in)throw runtime_error("input coordinates");
   if(index<first||index>=last)continue;
   for(int i=0;i<m;i++){
    if(i&&P[i-1][0]>=P[i][0])throw runtime_error("x order");
    for(auto c:P[i])if(c< -1000000000000000LL||c>1000000000000000LL)throw runtime_error("coordinate bound");
   }
   for(int a=0;a<m;a++)for(int b=a+1;b<m;b++)for(int c=b+1;c<m;c++){
    __int128 d=(__int128)(P[b][0]-P[a][0])*(P[c][1]-P[a][1])-(__int128)(P[b][1]-P[a][1])*(P[c][0]-P[a][0]);
    if(!d)throw runtime_error("collinear");
    int z=d>0?1:-1;
    s[a][b][c]=s[b][c][a]=s[c][a][b]=z;s[b][a][c]=s[a][c][b]=s[c][b][a]=-z;
   }
   int maxcap=2;
   for(int b=0;b<m;b++)for(int c=b+1;c<m;c++){
    rankcap[b][c]=2;for(int a=0;a<b;a++)if(s[a][b][c]<0)rankcap[b][c]=max(rankcap[b][c],1+rankcap[a][b]);
    maxcap=max(maxcap,rankcap[b][c]);
   }
   if(maxcap>=5)throw runtime_error("fivecap premise fails");
   vector<Pair>pairs;int id[60][60];
   for(int b=0;b<m;b++)for(int c=b+1;c<m;c++){id[b][c]=pairs.size();pairs.push_back({b,c});}
   int k=pairs.size();vector<char>end(k),terminal(k),one(k),closure(k),force(k);vector<int>next(k,-1),oneW(k,-1),forceW(k,-1);vector<array<int,4>>witness(k);
   for(int j=0;j<k;j++)terminal[j]=rankcap[pairs[j][0]][pairs[j][1]]>=3;
   for(int a=0;a<m;a++)for(int b=a+1;b<m;b++)for(int c=b+1;c<m;c++)if(s[a][b][c]<0)for(int d=c+1;d<m;d++)if(s[b][c][d]<0){int j=id[c][d];if(!end[j])witness[j]={a,b,c,d};end[j]=1;}
   vector<int>ambient;for(int i=0;i<k;i++)if(end[i])ambient.push_back(i);
   for(int i=k-1;i>=0;i--){
    Pair p=pairs[i];
    if(end[i]){one[i]=closure[i]=force[i]=1;oneW[i]=forceW[i]=i;continue;}
    for(int j:ambient){
     Pair q=pairs[j];
     if(q[0]>=p[0]&&q[1]>=p[1]&&cup(p,q)){one[i]=1;oneW[i]=j;}
     if(forced(p,q)){
      if(q[1]<p[1])throw runtime_error("forced late query would make fivecap");
      force[i]=1;forceW[i]=j;
     }
    }
    if(one[i]){closure[i]=1;next[i]=oneW[i];}
    else for(int j=k-1;j>i;j--)if(closure[j]&&pairs[j][0]>=p[0]&&pairs[j][1]>=p[1]&&cup(p,pairs[j])){closure[i]=1;next[i]=j;break;}
    if(one[i]&&!force[i])throw runtime_error("cup must imply forced dominance");
   }
   int a1=0,ac=0,af=0,t1=0,tc=0,tf=0;
   for(int i=0;i<k;i++){a1+=one[i];ac+=closure[i];af+=force[i];if(terminal[i]){t1+=one[i];tc+=closure[i];tf+=force[i];}}
   out<<"{\"name\":\""<<name<<"\",\"n\":"<<n<<",\"m\":"<<m<<",\"maxcap\":"<<maxcap<<",\"pairs\":"<<k<<",\"ambient_pairs\":"<<ambient.size()<<",\"direct_cup\":"<<a1<<",\"cup_closure\":"<<ac<<",\"endpoint_forced\":"<<af<<",\"direct_cup_cap_terminal\":"<<t1<<",\"cup_closure_cap_terminal\":"<<tc<<",\"endpoint_forced_cap_terminal\":"<<tf;
   auto capout=[&](int j){auto w=witness[j];out<<'['<<w[0]<<','<<w[1]<<','<<w[2]<<','<<w[3]<<']';};
   out<<",\"closure_added\":[";bool comma=false;
   for(int i=0;i<k;i++)if(closure[i]&&!one[i]){
    if(comma)out<<',';
    comma=true;out<<"{\"pair\":";pairout(out,pairs[i]);out<<",\"cap_terminal\":"<<(terminal[i]?"true":"false")<<",\"path\":[";int j=i;pairout(out,pairs[j]);
    while(!end[j]){int oldj=j;j=next[j];if(j<=oldj||j>=k||!cup(pairs[oldj],pairs[j]))throw runtime_error("bad path");out<<',';pairout(out,pairs[j]);}
    out<<"],\"ambient_fourcap\":";capout(j);out<<'}';
   }out<<']';
   out<<",\"forced_added\":[";comma=false;
   for(int i=0;i<k;i++)if(force[i]&&!one[i]){
    if(comma)out<<',';
    comma=true;int j=forceW[i];out<<"{\"pair\":";pairout(out,pairs[i]);out<<",\"cap_terminal\":"<<(terminal[i]?"true":"false")<<",\"support\":";pairout(out,pairs[j]);out<<",\"ambient_fourcap\":";capout(j);out<<",\"endpoint_difference_signs\":[";auto z=signs(pairs[i],pairs[j]);for(size_t t=0;t<z.size();t++){if(t)out<<',';out<<z[t];}out<<"]}";
   }out<<']';
   if(name=="relation-control"){
    bool ab=cup({0,3},{1,4}),bc=cup({1,4},{2,5}),acup=cup({0,3},{2,5});
    if(!ab||!bc||acup||end[id[2][5]])throw runtime_error("relation control");
    out<<",\"raw_relation_nontransitive_control\":true";
   }
   out<<"}\n";out.flush();
  }
  string trailing;if(in>>trailing)throw runtime_error("trailing input");
 }catch(const exception&e){cerr<<e.what()<<'\n';return 2;}
}
