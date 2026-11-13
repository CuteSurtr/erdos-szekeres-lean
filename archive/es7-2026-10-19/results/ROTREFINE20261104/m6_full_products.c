/* Exact directed product-vertex cycle test. No floating-point operations.
 * Input: n,width,selected-count,anchor-count; selected points; anchors;
 * n^3 signed canonical bracket IDs, where the sign is the model orientation.
 * One phase-zero anchor per selected orbit covers all GP identities by rotation.
 * Duplicate edges are retained and counted, so edges == 2 * identities.
 */
#include <stdint.h>
#include <inttypes.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

typedef struct { uint32_t to,next,packed; } Edge;
static void fail(const char *s){fprintf(stderr,"%s\n",s);exit(2);}
static void *allocate(size_t n,size_t w){void *p=calloc(n,w);if(!p)fail("allocation failed");return p;}
static uint64_t choose4(uint64_t n){return n<4?0:n*(n-1)*(n-2)*(n-3)/24;}
static uint32_t product(int x,int y,uint32_t width){uint32_t a=(uint32_t)abs(x),b=(uint32_t)abs(y);return a<b?a*width+b:b*width+a;}
static int sign(int x){return x>0?1:-1;}
static uint32_t pack(int a,int b,int c,int d,int e,int j){return (uint32_t)a|((uint32_t)b<<6)|((uint32_t)c<<12)|((uint32_t)d<<18)|((uint32_t)e<<24)|((uint32_t)j<<30);}

int main(int argc,char **argv){
 if(argc<2)fail("input file required");
 FILE *f=fopen(argv[1],"r");if(!f)fail("cannot open input");
 int n,w,np,na;if(fscanf(f,"%d%d%d%d",&n,&w,&np,&na)!=4)fail("bad header");
 if(n<5||n>63||w<2||w>32767||np<5||np>n||na<1||na>np)fail("header range");
 int points[63],anchors[63],seen[63]={0};
 for(int i=0;i<np;i++){if(fscanf(f,"%d",points+i)!=1||points[i]<0||points[i]>=n||seen[points[i]]++)fail("bad selected points");if(i&&points[i-1]>=points[i])fail("points not increasing");}
 for(int i=0;i<na;i++){if(fscanf(f,"%d",anchors+i)!=1||anchors[i]<0||anchors[i]>=n||!seen[anchors[i]])fail("bad anchor");for(int j=0;j<i;j++)if(anchors[j]==anchors[i])fail("duplicate anchor");}
 int16_t *orientation=allocate((size_t)n*n*n,sizeof(*orientation));
 for(int a=0;a<n;a++)for(int b=0;b<n;b++)for(int c=0;c<n;c++){
  int v;if(fscanf(f,"%d",&v)!=1||abs(v)>=w)fail("bad bracket ID");
  if((a==b||a==c||b==c)!=(v==0))fail("zero bracket mismatch");
  orientation[(a*n+b)*n+c]=(int16_t)v;
 }
 int trailing;if(fscanf(f,"%d",&trailing)!=EOF)fail("trailing input");fclose(f);
 uint64_t identities_expected=(uint64_t)na*choose4((uint64_t)np-1),capacity=2*identities_expected;
 uint64_t nodes64=(uint64_t)w*w;if(nodes64>UINT32_MAX||capacity>=UINT32_MAX)fail("index overflow");
 uint32_t nodes=(uint32_t)nodes64,*head=allocate(nodes,sizeof(*head)),*degree=allocate(nodes,sizeof(*degree)),*queue=allocate(nodes,sizeof(*queue));
 memset(head,0xff,(size_t)nodes*sizeof(*head));Edge *edges=allocate((size_t)capacity,sizeof(*edges));
 uint32_t ne=0;uint64_t identities=0;int dump=argc>2&&!strcmp(argv[2],"--dump");
 #define O(a,b,c) orientation[((a)*n+(b))*n+(c)]
 for(int ai=0;ai<na;ai++){
  int a=anchors[ai],rest[63],nr=0;for(int i=0;i<np;i++)if(points[i]!=a)rest[nr++]=points[i];
  for(int ib=0;ib<nr-3;ib++)for(int ic=ib+1;ic<nr-2;ic++)for(int id=ic+1;id<nr-1;id++)for(int ie=id+1;ie<nr;ie++){
   int b=rest[ib],c=rest[ic],d=rest[id],e=rest[ie];
   int x[3]={O(a,b,c),O(a,b,d),O(a,b,e)},y[3]={O(a,d,e),O(a,c,e),O(a,c,d)};
   int s[3]={sign(x[0])*sign(y[0]),-sign(x[1])*sign(y[1]),sign(x[2])*sign(y[2])};
   identities++;if(s[0]==s[1]&&s[1]==s[2]){fprintf(stderr,"GP violation %d %d %d %d %d\n",a,b,c,d,e);return 2;}
   int minority=s[0]==s[1]?2:(s[0]==s[2]?1:0);uint32_t p[3];for(int k=0;k<3;k++)p[k]=product(x[k],y[k],(uint32_t)w);
   for(int j=0;j<3;j++)if(j!=minority){
    uint32_t u=p[minority],v=p[j];if(ne>=capacity)fail("edge overflow");
    edges[ne]=(Edge){v,head[u],pack(a,b,c,d,e,j)};head[u]=ne++;degree[v]++;
    if(dump)printf("edge %d %d %d %d %d %d %d %u %u\n",a,b,c,d,e,minority,j,u,v);
   }
  }
 }
 if(identities!=identities_expected||ne!=2*identities)fail("coverage count mismatch");
 uint32_t used=0,front=0,back=0;
 for(uint32_t u=0;u<nodes;u++)if(head[u]!=UINT32_MAX||degree[u]){used++;if(!degree[u])queue[back++]=u;}
 while(front<back){uint32_t u=queue[front++];for(uint32_t k=head[u];k!=UINT32_MAX;k=edges[k].next){uint32_t v=edges[k].to;if(!degree[v])fail("indegree underflow");if(!--degree[v])queue[back++]=v;}}
 uint32_t remaining=used-back;
 printf("{\"identities\":%" PRIu64 ",\"expected_identities\":%" PRIu64 ",\"edges_with_multiplicity\":%u,\"used_product_vertices\":%u,\"pruned_vertices\":%u,\"remaining_vertices\":%u,\"all_identities_covered\":true,\"acyclic\":%s,\"cycle_backward\":[",identities,identities_expected,ne,used,back,remaining,remaining?"false":"true");
 if(remaining){
  /* Every unpruned vertex has an unpruned incoming predecessor. Reuse queue. */
  uint32_t start=UINT32_MAX;for(uint32_t u=0;u<nodes;u++)if(degree[u]){start=u;for(uint32_t k=head[u];k!=UINT32_MAX;k=edges[k].next)if(degree[edges[k].to])queue[edges[k].to]=u;}
  uint32_t slow=start,fast=start;do{slow=queue[slow];fast=queue[queue[fast]];}while(slow!=fast);
  uint32_t v=slow;int comma=0;do{
   uint32_t u=queue[v],k=head[u];while(k!=UINT32_MAX&&edges[k].to!=v)k=edges[k].next;if(k==UINT32_MAX)fail("missing cycle edge");
   uint32_t z=edges[k].packed;printf("%s{\"from\":%u,\"to\":%u,\"q\":[%u,%u,%u,%u,%u],\"other\":%u}",comma?",":"",u,v,z&63,(z>>6)&63,(z>>12)&63,(z>>18)&63,(z>>24)&63,z>>30);comma=1;v=u;
  }while(v!=slow);
 }
 puts("]}");free(edges);free(queue);free(degree);free(head);free(orientation);return 0;
}
