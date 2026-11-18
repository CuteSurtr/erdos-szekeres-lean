// Exact integer, single-threaded adversarial Delta instrument. No external libraries.
// Native NO_DELTA_COMPUTED is NOT a certificate. See README.md and runner.py.
#include <algorithm>
#include <array>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <deque>
#include <filesystem>
#include <fstream>
#include <functional>
#include <iostream>
#include <limits>
#include <random>
#include <sstream>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

using I = int64_t;
using Wide = __int128_t;
using Mask = uint64_t;
using Clock = std::chrono::steady_clock;
constexpr I BOUND = 1000000000000000LL;
constexpr int MAX_POINTS = 64;
struct Point { I x, y; bool operator<(const Point& q) const { return x != q.x ? x < q.x : y < q.y; } };
using Points = std::vector<Point>;
int count(Mask x) { return __builtin_popcountll(x); }
int first(Mask x) { if (!x) throw std::logic_error("first(0)"); return __builtin_ctzll(x); }
Mask bit(int i) { return Mask(1) << i; }
Mask universe(int m) { if(m<0||m>64)throw std::invalid_argument("bad_point_count");return m == 64 ? ~Mask(0) : (bit(m) - 1); }
Wide det(const Point& p, const Point& q, const Point& r) {
    // With |coordinate| <= BOUND, |det| <= 8*10^30 < 2^103 < 2^127.
    // Promote BEFORE subtracting; no int64 multiplication is used in geometry.
    return (Wide(q.x)-p.x)*(Wide(r.y)-p.y) - (Wide(q.y)-p.y)*(Wide(r.x)-p.x);
}
Wide floor_div(Wide a, Wide b) {
    if (b <= 0) throw std::logic_error("nonpositive denominator");
    Wide q = a / b; return q - (a % b < 0);
}
bool coordinate(Wide v) { return -Wide(BOUND) <= v && v <= Wide(BOUND); }
struct Limit : std::runtime_error { using std::runtime_error::runtime_error; };
struct Budget {
    Clock::time_point until;
    uint64_t nodes = 0, max_nodes, ticks = 0;
    void check() const { if (Clock::now() >= until) throw Limit("time_limit"); }
    void tick() { if ((++ticks & 2047) == 0) check(); }
    void node() { check(); if (nodes >= max_nodes) throw Limit("node_limit"); ++nodes; }
};
struct Config {
    std::string command, input, out, mode = "lower";
    int a = 5, n = 8, time_ms = 2000, rounds = 10000, cache = 20000, bank = 32;
    int restart = 128, min_size = 0, minimize_ms = 5000;
    uint64_t node_limit = 2000000, clause_limit = 1000000, seed = 1, steps = 1000000;
    double seconds = 0;
    int max_delta = -1;
    bool detail = false, min_delta = false, private_witnesses = false;
};

struct Chains {
    int m;
    std::vector<int> cap, cup;
    std::vector<Mask> cap_path, cup_path;
    explicit Chains(int size) : m(size), cap(m*m), cup(m*m), cap_path(m*m), cup_path(m*m) {}
};
struct Geometry {
    Points p;
    int m;
    Mask all;
    std::vector<Mask> cap_next, cup_next;
    std::string key;
    explicit Geometry(Points points, Budget& b) : p(std::move(points)), m(int(p.size())),
        all(universe(m)), cap_next(m*m), cup_next(m*m) {
        if (m > MAX_POINTS) throw std::invalid_argument("more_than_64_points");
        std::sort(p.begin(), p.end());
        for (int i=0; i<m; ++i) {
            if (!coordinate(p[i].x) || !coordinate(p[i].y)) throw std::invalid_argument("coordinate_bound");
            if (i && p[i-1].x == p[i].x) throw std::invalid_argument("duplicate_x");
        }
        key.push_back(char(m));
        unsigned packed=0, used=0;
        for (int i=0; i<m; ++i) for (int j=i+1; j<m; ++j) for (int k=j+1; k<m; ++k) {
            b.tick(); Wide z=det(p[i],p[j],p[k]);
            if (!z) throw std::invalid_argument("collinear_triple");
            (z < 0 ? cap_next : cup_next)[i*m+j] |= bit(k);
            if (z>0) packed |= 1U << used;
            if (++used==8) { key.push_back(char(packed)); packed=used=0; }
        }
        if (used) key.push_back(char(packed));
    }
    // Suffix DP: a chain starting with edge (i,j), ending at fixed v.
    // Edge-successor masks make the inner recurrence use only the required turns.
    Chains chains(Mask allowed, Budget& b, bool do_cap=true, bool do_cup=true) const {
        Chains out(m);
        std::vector<int> dc(m*m), du(m*m);
        std::vector<Mask> pc(m*m), pu(m*m);
        for (int v=1; v<m; ++v) if (allowed & bit(v)) {
            std::fill(dc.begin(),dc.end(),0); std::fill(du.begin(),du.end(),0);
            Mask upto = v==63 ? ~Mask(0) : bit(v+1)-1;
            for (int i=v-1; i>=0; --i) if (allowed & bit(i)) {
                int bestc=0, bestu=0; Mask bc=0, bu=0;
                for (int j=i+1; j<=v; ++j) if (allowed & bit(j)) {
                    int ij=i*m+j;
                    if (j==v) {
                        dc[ij]=du[ij]=2; pc[ij]=pu[ij]=bit(i)|bit(j);
                    } else {
                        if (do_cap) for (Mask ks=cap_next[ij]&allowed&upto; ks; ks&=ks-1) {
                            b.tick(); int jk=j*m+first(ks);
                            if (dc[jk] && dc[jk]+1>dc[ij]) { dc[ij]=dc[jk]+1; pc[ij]=bit(i)|pc[jk]; }
                        }
                        if (do_cup) for (Mask ks=cup_next[ij]&allowed&upto; ks; ks&=ks-1) {
                            b.tick(); int jk=j*m+first(ks);
                            if (du[jk] && du[jk]+1>du[ij]) { du[ij]=du[jk]+1; pu[ij]=bit(i)|pu[jk]; }
                        }
                    }
                    if (dc[ij]>bestc) { bestc=dc[ij]; bc=pc[ij]; }
                    if (du[ij]>bestu) { bestu=du[ij]; bu=pu[ij]; }
                }
                int iv=i*m+v;
                out.cap[iv]=bestc; out.cup[iv]=bestu;
                out.cap_path[iv]=bc; out.cup_path[iv]=bu;
            }
        }
        return out;
    }
    std::vector<Mask> caps(int length, uint64_t limit, Budget& b) const {
        std::vector<Mask> out;
        std::function<void(int,int,Mask,int)> visit=[&](int i,int j,Mask ch,int size) {
            b.tick();
            if (size==length) {
                if (out.size()>=limit) throw Limit("clause_limit");
                out.push_back(ch); return;
            }
            if (m-j-1 < length-size) return;
            for (Mask ks=cap_next[i*m+j]; ks; ks&=ks-1) {
                int k=first(ks); visit(j,k,ch|bit(k),size+1);
            }
        };
        for (int i=0; i<m; ++i) for (int j=i+1; j<m; ++j) visit(i,j,bit(i)|bit(j),2);
        return out;
    }
};

// Independent validation recurrence: forward DP using raw __int128 determinants,
// with neither successor masks nor paths from Geometry::chains.
Chains forward(const Points& p, Mask allowed, Budget& budget) {
    int m=int(p.size()); Chains out(m); std::vector<int> dc(m*m),du(m*m);
    for (int s=0; s<m; ++s) if (allowed&bit(s)) {
        std::fill(dc.begin(),dc.end(),0); std::fill(du.begin(),du.end(),0);
        for (int j=s+1; j<m; ++j) if (allowed&bit(j)) {
            dc[s*m+j]=du[s*m+j]=2;
            int bc=2,bu=2;
            for (int i=s+1; i<j; ++i) if (allowed&bit(i)) {
                for (int h=s; h<i; ++h) if (allowed&bit(h)) {
                    budget.tick(); Wide d=det(p[h],p[i],p[j]);
                    if (d<0 && dc[h*m+i]) dc[i*m+j]=std::max(dc[i*m+j],dc[h*m+i]+1);
                    if (d>0 && du[h*m+i]) du[i*m+j]=std::max(du[i*m+j],du[h*m+i]+1);
                }
                bc=std::max(bc,dc[i*m+j]); bu=std::max(bu,du[i*m+j]);
            }
            out.cap[s*m+j]=bc; out.cup[s*m+j]=bu;
        }
    }
    return out;
}
struct Witness { Mask clause, cap, cup; bool positive; };
struct Result {
    std::string status="UNKNOWN", reason;
    Points p;
    Mask delta=0;
    int maxcap=0, maxcup=0, maxgon=0, saturated=0, hard_pairs=0, rounds=0;
    uint64_t nodes=0;
    double milliseconds=0;
    bool verified=false, deletion_minimal=false;
    int tau_lower=0,tau_upper=-1;
    bool tau_exact=false,private_complete=false,optimization_unknown=false;
    Mask private_points=0;
    std::vector<Mask> caps, positive, negative;
    std::vector<Witness> witnesses;
    std::vector<Witness> private_cups;
    std::vector<int> capB,cupB;
};
void summarize(const Chains& c, Result& r, int n, int a) {
    int m=c.m; r.maxcap=r.maxcup=r.maxgon=std::min(m,2);
    Mask starts=0,ends=0;
    for(int u=0;u<m;++u) for(int v=u+1;v<m;++v) {
        int z=u*m+v;
        r.maxcap=std::max(r.maxcap,c.cap[z]); r.maxcup=std::max(r.maxcup,c.cup[z]);
        r.maxgon=std::max(r.maxgon,c.cap[z]+c.cup[z]-2);
        if(c.cap[z]>=a-1) { starts|=bit(u); ends|=bit(v); }
    }
    for(int u=0;u<m;++u) for(int v=u+1;v<m;++v) if(c.cap[u*m+v]+c.cup[u*m+v]==n+1) {
        ++r.saturated;
        if((ends&bit(u)) && (starts&bit(v))) ++r.hard_pairs;
    }
}

// Complete DPLL on monotone clauses. T/F are disjoint assignments; every leaf
// returned SAT is completed by assigning all remaining variables false.
class Solver {
    const std::vector<Mask>& pos;
    const std::vector<Mask>& neg;
    Budget& b;
    int max_true;
    Mask all;
public:
    Mask model=0;
    Solver(const std::vector<Mask>& p,const std::vector<Mask>& n,Budget& budget,int bound,Mask universe):pos(p),neg(n),b(budget),max_true(bound),all(universe){}
    bool solve(Mask t=0,Mask f=0) {
        b.node();
        for (;;) {
            Mask ot=t,of=f;
            if(max_true>=0) {
                if(count(t)>max_true)return false;
                if(count(t)==max_true)f|=all&~t;
            }
            for(Mask c:neg) {
                b.tick(); if(c&f) continue; Mask rem=c&~t;
                if(!rem) return false;
                if(!(rem&(rem-1))) f|=rem;
            }
            for(Mask c:pos) {
                b.tick(); if(c&t) continue; Mask rem=c&~f;
                if(!rem) return false;
                if(!(rem&(rem-1))) t|=rem;
            }
            if(t&f) return false;
            if(t==ot && f==of) break;
        }
        Mask choice=0; int width=65;
        for(Mask c:pos) if(!(c&t)) {
            b.tick(); Mask rem=c&~f; int w=count(rem);
            if(w<width) {width=w;choice=rem;}
        }
        if(!choice) { model=t; return true; }
        // Pick a high-degree variable from the shortest unsatisfied hit clause.
        std::array<unsigned,64> degree{};
        for(Mask c:pos) if(!(c&t)) for(Mask q=c&choice; q; q&=q-1) { b.tick(); ++degree[first(q)]; }
        int best=first(choice);
        for(Mask q=choice; q; q&=q-1) if(degree[first(q)]>degree[best]) best=first(q);
        Mask x=bit(best);
        return solve(t|x,f) || solve(t,f|x);
    }
};

bool check_delta(const Points& p, Mask d, const Config& c, const Chains& original, Budget& budget) {
    int m=int(p.size()); Mask all=universe(m);
    Chains in=forward(p,d,budget), rest=forward(p,all&~d,budget);
    for(int u=0;u<m;++u) for(int v=u+1;v<m;++v) {
        int z=u*m+v;
        if(in.cap[z]>=c.a-1) return false;
        if((d&bit(u)) || (d&bit(v))) continue;
        if(c.mode=="lower" && original.cap[z]+rest.cup[z]>c.n) return false;
        if(c.mode=="upper" && rest.cap[z]+original.cup[z]>c.n) return false;
        if(c.mode=="ends" && original.cap[z]+original.cup[z]==c.n+1) return false;
        if((c.mode=="weak" || c.mode=="strong") && rest.cap[z]+rest.cup[z]-2>=c.n-1) return false;
    }
    if(c.mode=="strong") for(int u=0;u<m;++u) for(int v=u+1;v<m;++v)
        if((d&bit(u)) && (d&bit(v)) && in.cap[u*m+v]+in.cup[u*m+v]-2>=c.n-1) return false;
    return true;
}

Result evaluate_bound(const Points& points,const Config& c,Clock::time_point global) {
    auto start=Clock::now(); Budget b{std::min(global,start+std::chrono::milliseconds(c.time_ms)),0,c.node_limit,0};
    Result r; r.p=points;
    try {
        b.check(); Geometry g(points,b); r.p=g.p;
        Chains a=g.chains(g.all,b); summarize(a,r,c.n,c.a);
        if(c.detail) { r.capB=a.cap; r.cupB=a.cup; }
        if(r.maxcap>=c.a || r.maxgon>=c.n) {
            r.status="INVALID"; r.reason=r.maxcap>=c.a ? "contains_a_cap" : "contains_n_gon";
        } else {
            // Premises checked by an independent recurrence before an exact verdict.
            Chains direct=forward(g.p,g.all,b);
            if(direct.cap!=a.cap || direct.cup!=a.cup) throw std::logic_error("geometry_crosscheck");
            r.caps=g.caps(c.a-1,c.clause_limit,b); r.negative=r.caps;
            std::unordered_set<Mask> pos_seen,neg_seen(r.caps.begin(),r.caps.end());
            auto add=[&](Mask clause,Mask upper,Mask lower,bool positive) {
                auto& seen=positive?pos_seen:neg_seen;
                if(seen.count(clause)) return false;
                if(r.negative.size()+r.positive.size()>=c.clause_limit) throw Limit("clause_limit");
                seen.insert(clause); (positive?r.positive:r.negative).push_back(clause);
                r.witnesses.push_back({clause,upper,lower,positive}); return true;
            };
            for(int u=0;u<g.m;++u) for(int v=u+1;v<g.m;++v) {
                int z=u*g.m+v;
                if(a.cap[z]+a.cup[z]!=c.n+1) continue;
                Mask hit=c.mode=="lower" ? a.cup_path[z] : c.mode=="upper" ? a.cap_path[z] :
                    c.mode=="ends" ? bit(u)|bit(v) : a.cap_path[z]|a.cup_path[z];
                add(hit,a.cap_path[z],a.cup_path[z],true);
            }
            for(;;) {
                b.check(); if(r.rounds>=c.rounds) throw Limit("round_limit"); ++r.rounds;
                Solver sat(r.positive,r.negative,b,c.max_delta,g.all);
                if(!sat.solve()) { r.status=c.max_delta<0?"NO_DELTA_COMPUTED":"NO_DELTA_WITHIN_BOUND"; r.reason="exhaustive_DPLL"; break; }
                r.delta=sat.model;
                for(Mask x:r.negative) if((x&r.delta)==x) throw std::logic_error("bad_SAT_negative");
                for(Mask x:r.positive) if(!(x&r.delta)) throw std::logic_error("bad_SAT_positive");
                Mask rest=g.all&~r.delta; bool added=false;
                if(c.mode!="ends") {
                    Chains q=g.chains(rest,b,c.mode!="lower",c.mode!="upper");
                    for(int u=0;u<g.m;++u) if(rest&bit(u)) for(int v=u+1;v<g.m;++v) if(rest&bit(v)) {
                        b.tick(); int z=u*g.m+v;
                        if(c.mode=="lower" && a.cap[z]+q.cup[z]>c.n)
                            added|=add(q.cup_path[z],a.cap_path[z],q.cup_path[z],true);
                        if(c.mode=="upper" && q.cap[z]+a.cup[z]>c.n)
                            added|=add(q.cap_path[z],q.cap_path[z],a.cup_path[z],true);
                        if((c.mode=="weak" || c.mode=="strong") && q.cap[z]+q.cup[z]-2>=c.n-1)
                            added|=add(q.cap_path[z]|q.cup_path[z],q.cap_path[z],q.cup_path[z],true);
                    }
                }
                if(c.mode=="strong") {
                    Chains q=g.chains(r.delta,b);
                    for(int u=0;u<g.m;++u) for(int v=u+1;v<g.m;++v) if((r.delta&bit(u)) && (r.delta&bit(v))) {
                        int z=u*g.m+v;
                        if(q.cap[z]+q.cup[z]-2>=c.n-1)
                            added|=add(q.cap_path[z]|q.cup_path[z],q.cap_path[z],q.cup_path[z],false);
                    }
                }
                if(!added) {
                    if(!check_delta(g.p,r.delta,c,direct,b)) throw std::logic_error("final_Delta_crosscheck");
                    if(c.max_delta>=0 && count(r.delta)>c.max_delta)throw std::logic_error("cardinality_crosscheck");
                    r.status="OK"; r.verified=true;r.tau_upper=count(r.delta); break;
                }
            }
        }
    } catch(const Limit& e) {r.status="UNKNOWN";r.reason=e.what();}
      catch(const std::invalid_argument& e) {r.status="INVALID_INPUT";r.reason=e.what();}
    r.nodes=b.nodes;
    r.milliseconds=std::chrono::duration<double,std::milli>(Clock::now()-start).count();
    return r;
}

Result evaluate(const Points& points,const Config& c,Clock::time_point global=Clock::time_point::max()) {
    auto start=Clock::now();auto end=std::min(global,start+std::chrono::milliseconds(c.time_ms));
    Result r=evaluate_bound(points,c,end);
    if(r.status!="OK")return r;
    if(c.min_delta) {
        int lo=0,hi=count(r.delta);uint64_t total_nodes=r.nodes;int total_rounds=r.rounds;
        while(lo<hi) {
            Config bounded=c;bounded.max_delta=(lo+hi)/2;
            Result q=evaluate_bound(points,bounded,end);total_nodes+=q.nodes;total_rounds+=q.rounds;
            if(q.status=="OK"){hi=count(q.delta);r=std::move(q);}
            else if(q.status=="NO_DELTA_WITHIN_BOUND")lo=bounded.max_delta+1;
            else if(q.status=="UNKNOWN"){r.optimization_unknown=true;break;}
            else throw std::logic_error("cardinality_probe_bad_status");
        }
        r.tau_lower=lo;r.tau_upper=hi;r.tau_exact=(lo==hi);r.nodes=total_nodes;r.rounds=total_rounds;
    }
    if(c.private_witnesses && c.mode=="lower") {
        Budget b{end,0,c.node_limit,0};
        try {
            Geometry g(r.p,b);Chains original=g.chains(g.all,b);
            for(Mask d=r.delta;d;d&=d-1) {
                b.check();Mask singleton=bit(first(d)),rest=g.all&~(r.delta&~singleton);
                Chains q=g.chains(rest,b,false,true);bool found=false;
                for(int u=0;u<g.m && !found;++u)if(rest&bit(u))for(int v=u+1;v<g.m && !found;++v)if(rest&bit(v)) {
                    int z=u*g.m+v;
                    if(original.cap[z]+q.cup[z]>c.n) {
                        if((q.cup_path[z]&r.delta)!=singleton)throw std::logic_error("bad_private_cup");
                        r.private_points|=singleton;r.private_cups.push_back({singleton,original.cap_path[z],q.cup_path[z],true});found=true;
                    }
                }
            }
            r.private_complete=true;
        }catch(const Limit&){r.private_complete=false;}
    }
    r.milliseconds=std::chrono::duration<double,std::milli>(Clock::now()-start).count();return r;
}

void indices(std::ostream& o,Mask m) { o<<'['; bool comma=false; for(;m;m&=m-1) {if(comma)o<<',';comma=true;o<<first(m);} o<<']'; }
void points_json(std::ostream& o,const Points& p) {o<<'[';for(size_t i=0;i<p.size();++i){if(i)o<<',';o<<'['<<p[i].x<<','<<p[i].y<<']';}o<<']';}
void ints(std::ostream& o,const std::vector<int>& xs) {o<<'[';for(size_t i=0;i<xs.size();++i){if(i)o<<',';o<<xs[i];}o<<']';}
void report(std::ostream& o,const Result& r,const Config& c,bool full=false) {
    o<<"{\"label\":\"COMPUTED\",\"status\":\""<<r.status<<"\",\"reason\":\""<<r.reason
     <<"\",\"a\":"<<c.a<<",\"n\":"<<c.n<<",\"mode\":\""<<c.mode<<"\",\"m\":"<<r.p.size()
     <<",\"maxcap\":"<<r.maxcap<<",\"maxcup\":"<<r.maxcup<<",\"maxgon\":"<<r.maxgon
     <<",\"saturated\":"<<r.saturated<<",\"hard_pairs\":"<<r.hard_pairs<<",\"nodes\":"<<r.nodes
     <<",\"rounds\":"<<r.rounds<<",\"negative_clauses\":"<<r.negative.size()<<",\"positive_clauses\":"<<r.positive.size()
     <<",\"milliseconds\":"<<r.milliseconds<<",\"forward_verified\":"<<(r.verified?"true":"false")
     <<",\"one_deletion_minimal\":"<<(r.deletion_minimal?"true":"false")<<",\"Delta\":";
    if(r.status=="OK") indices(o,r.delta); else o<<"null";
    o<<",\"max_delta_bound\":"<<c.max_delta<<",\"tau_lower\":"<<r.tau_lower<<",\"tau_upper\":"<<r.tau_upper
     <<",\"tau_exact\":"<<(r.tau_exact?"true":"false")<<",\"optimization_unknown\":"<<(r.optimization_unknown?"true":"false")
     <<",\"private_complete\":"<<(r.private_complete?"true":"false")<<",\"private_points\":";indices(o,r.private_points);
    if(full || c.detail) {o<<",\"P\":";points_json(o,r.p);}
    if(c.detail) {o<<",\"capB\":";ints(o,r.capB);o<<",\"cupB\":";ints(o,r.cupB);}
    if(full) {
        o<<",\"cap_clauses\":[";
        for(size_t i=0;i<r.caps.size();++i){if(i)o<<',';indices(o,r.caps[i]);}
        o<<"],\"witness_clauses\":[";
        for(size_t i=0;i<r.witnesses.size();++i) {
            if(i)o<<',';
            const auto& w=r.witnesses[i];
            o<<"{\"positive\":"<<(w.positive?"true":"false")<<",\"clause\":";indices(o,w.clause);
            o<<",\"cap\":";indices(o,w.cap);o<<",\"cup\":";indices(o,w.cup);o<<'}';
        }
        o<<"],\"private_cups\":[";
        for(size_t i=0;i<r.private_cups.size();++i){if(i)o<<',';const auto& w=r.private_cups[i];o<<"{\"vertex\":";indices(o,w.clause);o<<",\"cap\":";indices(o,w.cap);o<<",\"cup\":";indices(o,w.cup);o<<'}';}o<<']';
    }
    o<<'}';
}
void save(const Result& r,const Config& c,const std::string& name) {
    if(c.out.empty()) return;
    std::filesystem::create_directories(c.out);
    std::string base=c.out+"/"+name;
    std::ofstream js(base+".json"),cnf(base+".cnf"),pt(base+".points");
    if(!js || !cnf || !pt) throw std::runtime_error("cannot_write_artifact");
    report(js,r,c,true);js<<'\n'; pt<<r.p.size()<<'\n';for(auto p:r.p)pt<<p.x<<' '<<p.y<<'\n';
    cnf<<"c Delta3 mode "<<c.mode<<"; one variable per x-sorted point\n";
    // A bounded DPLL verdict is not represented by this geometric CNF alone.
    // Refuse its use as an UNSAT packet; runner.py also rejects bounded packets.
    if(c.max_delta>=0)cnf<<"c WARNING: CARDINALITY BOUND OMITTED; NOT A REFUTATION INSTANCE\n";
    cnf<<"p cnf "<<r.p.size()<<' '<<r.negative.size()+r.positive.size()<<'\n';
    for(Mask q:r.negative) {for(;q;q&=q-1)cnf<<-(first(q)+1)<<' ';cnf<<"0\n";}
    for(Mask q:r.positive) {for(;q;q&=q-1)cnf<<first(q)+1<<' ';cnf<<"0\n";}
    js.flush();cnf.flush();pt.flush();if(!js||!cnf||!pt)throw std::runtime_error("artifact_write_failed");
}
Points read_points(std::istream& f) {
    int m; if(!(f>>m) || m<0 || m>64)throw std::invalid_argument("bad_point_count");
    Points p(m);for(auto& q:p)if(!(f>>q.x>>q.y))throw std::invalid_argument("bad_integer_coordinate");return p;
}
Points read_one(const std::string& path) {
    std::ifstream f(path);if(!f)throw std::invalid_argument("cannot_read_input");
    Points p=read_points(f);std::string extra;if(f>>extra)throw std::invalid_argument("trailing_input");return p;
}

Result minimize(Result best,const Config& c,Clock::time_point deadline) {
    if(best.status!="NO_DELTA_COMPUTED")throw std::invalid_argument("minimize_requires_exhaustive_failure");
    bool changed=true,unknown=false;
    while(changed) {
        changed=false;unknown=false;
        for(size_t i=0;i<best.p.size();++i) {
            if(Clock::now()>=deadline)return best;
            Points q=best.p;q.erase(q.begin()+i);Result r=evaluate(q,c,deadline);
            if(r.status=="NO_DELTA_COMPUTED") {best=std::move(r);save(best,c,"minimized");changed=true;break;}
            if(r.status=="UNKNOWN")unknown=true;
            if(r.status=="INVALID" || r.status=="INVALID_INPUT")throw std::logic_error("deletion_broke_validity");
        }
    }
    best.deletion_minimal=!unknown;return best;
}

struct Entry { Points p; Mask delta,focus; double score; int tau_lower,tau_upper; bool tau_exact; uint64_t nodes; };
double score(const Result& r) {
    return 30.0*r.p.size()+100*r.tau_lower+2*count(r.private_points)+0.6*r.saturated+3*r.hard_pairs+5*std::log1p(double(r.nodes))+3*std::log1p(double(r.positive.size()));
}
Entry entry(const Result& r) { return {r.p,r.delta,r.private_points?r.private_points:r.delta,score(r),r.tau_lower,r.tau_upper,r.tau_exact,r.nodes}; }
class Search {
    const Config& c;
    std::mt19937_64 rng;
    std::vector<Entry> bank;
    std::unordered_set<std::string> seen;
    std::deque<std::string> fifo;
    Clock::time_point until;
    uint64_t tried=0, unique=0, duplicate=0, invalid=0, unknown=0, accepted=0, seed_tested=0;
    uint64_t optimization_unknown=0;
    double best_score=-std::numeric_limits<double>::infinity();
    std::array<uint64_t,7> proposed{},valid_move{};
    int pick(int n) {return int(rng()%unsigned(n));}
    void remember(const std::string& key) {
        if(c.cache==0)return;
        if(seen.insert(key).second)fifo.push_back(key);
        while(fifo.size()>size_t(c.cache)){seen.erase(fifo.front());fifo.pop_front();}
    }
    void insert(const Result& r) {
        Entry e=entry(r);
        if(r.optimization_unknown)++optimization_unknown;
        if(e.score>best_score) {
            best_score=e.score;save(r,c,"best");
            std::ofstream log(c.out+"/improvements.jsonl",std::ios::app);
            if(!log)throw std::runtime_error("cannot_save_improvements");
            report(log,r,c);log<<'\n';log.flush();if(!log)throw std::runtime_error("improvement_write_failed");
        }
        if(bank.size()<size_t(c.bank))bank.push_back(e);
        else {
            // Keep elites and use one quarter of the slots as a diversity reservoir.
            int elite=std::max(1,3*c.bank/4),worst=0;
            for(int i=1;i<elite;++i)if(bank[i].score<bank[worst].score)worst=i;
            if(e.score>bank[worst].score)bank[worst]=e;
            else bank[elite+pick(c.bank-elite)]=e;
        }
    }
    void pending(const Result& r) {
        std::ofstream f(c.out+"/pending.jsonl",std::ios::app); if(!f)throw std::runtime_error("cannot_save_pending");
        Config compact=c;compact.detail=true;report(f,r,compact);f<<'\n';f.flush();if(!f)throw std::runtime_error("pending_write_failed");
    }
    // Exact vertical wall crossing, keeping x fixed. Integer rounding can cross
    // several nearby walls; all resulting triples and premises are revalidated.
    bool wall(const Points& p,int v,int direction,I& target) {
        bool found=false;Wide nearest=0;
        for(int i=0;i<int(p.size());++i)if(i!=v)for(int j=i+1;j<int(p.size());++j)if(j!=v) {
            Wide den=Wide(p[j].x)-p[i].x;
            Wide num=Wide(p[i].y)*den+(Wide(p[j].y)-p[i].y)*(Wide(p[v].x)-p[i].x);
            Wide side=num-Wide(p[v].y)*den;
            if((direction>0 && side<0)||(direction<0 && side>0))continue;
            Wide y=direction>0?floor_div(num,den)+1:-floor_div(-num,den)-1;
            Wide distance=direction*(y-p[v].y);
            if(distance>0 && coordinate(y) && (!found || distance<nearest)) {found=true;nearest=distance;target=I(y);}
        }
        return found;
    }
    Points mutate(const Entry& e,int kind) {
        Points p=e.p;int m=int(p.size());if(m<2)return p;
        int v=pick(m);
        if(e.focus && pick(4)!=0){Mask d=e.focus;int k=pick(count(d));while(k--)d&=d-1;v=first(d);}
        auto set=[&](int i,Wide x,Wide y){if(!coordinate(x)||!coordinate(y))return false;p[i]={I(x),I(y)};return true;};
        int direction=pick(2)?1:-1;I target=0;
        if(kind==0) { // nearest order-type wall, biased to the current Delta
            if(!wall(p,v,direction,target))return {};
            p[v].y=target;
        } else if(kind==1) { // inflate a point into a small cap/cup cluster
            if(m>=64)return {};
            for(int i=0;i<m;++i)if(!set(i,Wide(p[i].x)*4,Wide(p[i].y)*4))return {};
            Wide x=Wide(p[v].x)+1,y=Wide(p[v].y)+direction*(1+pick(8));
            if(!coordinate(x)||!coordinate(y))return {};
            p.push_back({I(x),I(y)});
        } else if(kind==2) { // translate a whole contiguous block across a wall
            if(!wall(p,v,direction,target))return {};
            Wide shift=Wide(target)-p[v].y;int radius=1+pick(std::max(1,m/5));
            int lo=std::max(0,v-radius),hi=std::min(m,v+radius+1);
            for(int i=lo;i<hi;++i)if(!set(i,p[i].x,Wide(p[i].y)+shift))return {};
        } else if(kind==3) { // positive-determinant shear changes the sweep direction
            int q=1+pick(32),s=direction*(1+pick(8));
            for(int i=0;i<m;++i)if(!set(i,Wide(q)*p[i].x+Wide(s)*p[i].y,p[i].y))return {};
        } else if(kind==4) { // bend across all scales, changing many orientations
            Wide span=Wide(p.back().x)-p.front().x;
            Wide divisor=std::max(Wide(1),span*(1+pick(128)));
            I center=p[v].x;
            for(int i=0;i<m;++i){Wide dx=Wide(p[i].x)-center;if(!set(i,p[i].x,Wide(p[i].y)+direction*dx*dx/divisor))return {};}
        } else if(kind==5) { // delete a conflict-region point; later cluster moves regrow
            int floor=c.min_size?c.min_size:c.n-1;
            if(m<=floor)return {};
            p.erase(p.begin()+v);
        } else { // graft an affine image of an elite's block into this block
            if(bank.empty())return {};
            const Points& donor=bank[pick(int(bank.size()))].p;
            int width=std::min({2+pick(6),m,int(donor.size())});
            if(width<2)return {};
            int lo=pick(m-width+1),src=pick(int(donor.size())-width+1);
            Wide sw=Wide(donor[src+width-1].x)-donor[src].x,tw=Wide(p[lo+width-1].x)-p[lo].x;
            I x0=p[lo].x,y0=p[lo].y;
            for(int k=0;k<width;++k) {
                Wide x=Wide(x0)+(Wide(donor[src+k].x)-donor[src].x)*tw/sw;
                Wide y=Wide(y0)+(Wide(donor[src+k].y)-donor[src].y)*tw/sw;
                if(!set(lo+k,x,y))return {};
            }
        }
        std::sort(p.begin(),p.end());return p;
    }
    bool failure(Result& r) {
        if(r.status!="NO_DELTA_COMPUTED")return false;
        save(r,c,"failure");report(std::cout,r,c);std::cout<<std::endl;
        auto md=std::min(until,Clock::now()+std::chrono::milliseconds(c.minimize_ms));
        Result small=minimize(r,c,md);save(small,c,"minimized");report(std::cout,small,c);std::cout<<std::endl;return true;
    }
    void stats(const char* status) {
        std::cout<<"{\"label\":\"HEURISTIC\",\"status\":\""<<status<<"\",\"seed\":"<<c.seed
          <<",\"seed_tested\":"<<seed_tested<<",\"proposals\":"<<tried<<",\"novel_tested\":"<<unique
          <<",\"duplicate_order_types\":"<<duplicate<<",\"invalid\":"<<invalid<<",\"unknown\":"<<unknown
          <<",\"optimization_unknown\":"<<optimization_unknown
          <<",\"accepted\":"<<accepted<<",\"move_proposals\":[";
        for(int i=0;i<7;++i){if(i)std::cout<<',';std::cout<<proposed[i];}std::cout<<"],\"move_OK\":[";
        for(int i=0;i<7;++i){if(i)std::cout<<',';std::cout<<valid_move[i];}std::cout<<"]}"<<std::endl;
    }
public:
    explicit Search(const Config& cfg):c(cfg),rng(c.seed),until(Clock::now()+std::chrono::duration_cast<Clock::duration>(std::chrono::duration<double>(c.seconds))){}
    int run() {
        std::filesystem::create_directories(c.out);
        std::ifstream f(c.input);std::string magic;int version,k;
        if(!(f>>magic>>version>>k)||magic!="D3POOL"||version!=1||k<1||k>4096)throw std::invalid_argument("bad_pool_header");
        std::vector<Points> seeds;for(int i=0;i<k;++i)seeds.push_back(read_points(f));
        std::string extra;if(f>>extra)throw std::invalid_argument("trailing_pool_input");
        // Large seeds first, but each scheduled run can supply a different pool.
        std::shuffle(seeds.begin(),seeds.end(),rng);
        std::stable_sort(seeds.begin(),seeds.end(),[](const Points& x,const Points& y){return x.size()>y.size();});
        for(const Points& p:seeds) {
            if(Clock::now()>=until)break;
            Budget b{until,0,c.node_limit,0};std::string key;
            try {Geometry g(p,b);key=g.key;}catch(const Limit&){break;}catch(const std::invalid_argument&){++invalid;continue;}
            if(seen.count(key)){++duplicate;continue;}
            Result r=evaluate(p,c,until);++seed_tested;
            if(failure(r)){stats("FAILURE_COMPUTED");return 10;}
            if(r.status=="OK"){insert(r);remember(key);}
            else if(r.status=="UNKNOWN"){++unknown;pending(r);}
            else {++invalid;remember(key);}
            if(bank.size()>=size_t(c.bank))break;
        }
        if(bank.empty()){stats("NO_VALID_SEED");return 20;}
        Entry current=bank.front();auto nextlog=Clock::now()+std::chrono::seconds(5);
        for(;tried<c.steps && Clock::now()<until;++tried) {
            if(tried && tried%unsigned(c.restart)==0)current=bank[pick(int(bank.size()))];
            int kind=int(tried%7);++proposed[kind];Points p=mutate(current,kind);
            if(p.empty()){++invalid;continue;}
            Budget b{until,0,c.node_limit,0};std::string key;
            try{Geometry g(p,b);key=g.key;p=g.p;}catch(const Limit&){break;}catch(const std::invalid_argument&){++invalid;continue;}
            if(seen.count(key)){++duplicate;continue;}
            Result r=evaluate(p,c,until);++unique;
            if(failure(r)){stats("FAILURE_COMPUTED");return 10;}
            if(r.status=="UNKNOWN"){++unknown;pending(r);continue;}
            remember(key);
            if(r.status!="OK"){++invalid;continue;}
            ++valid_move[kind];insert(r);double s=score(r);
            // Accept some lower-size/lower-pressure states to escape extremal cells.
            if(s>=current.score || pick(8)==0){current=entry(r);++accepted;}
            if(Clock::now()>=nextlog){stats("RUNNING");nextlog=Clock::now()+std::chrono::seconds(5);}
        }
        std::ofstream elites(c.out+"/elite.jsonl");if(!elites)throw std::runtime_error("cannot_save_elites");
        for(const auto& e:bank){elites<<"{\"label\":\"HEURISTIC\",\"score\":"<<e.score<<",\"tau_lower\":"<<e.tau_lower
          <<",\"tau_upper\":"<<e.tau_upper<<",\"tau_exact\":"<<(e.tau_exact?"true":"false")<<",\"nodes\":"<<e.nodes
          <<",\"Delta\":";indices(elites,e.delta);elites<<",\"P\":";points_json(elites,e.p);elites<<"}\n";}
        elites.flush();if(!elites)throw std::runtime_error("elite_write_failed");
        stats("SEARCH_FINISHED");return unknown?20:0;
    }
};

Config parse(int argc,char** argv) {
    if(argc<2)throw std::invalid_argument("command: check | search | minimize");
    Config c;c.command=argv[1];
    for(int i=2;i<argc;++i) {
        std::string s=argv[i];if(s=="--detail"){c.detail=true;continue;}
        if(s=="--min-delta"){c.min_delta=true;continue;}if(s=="--private-witnesses"){c.private_witnesses=true;continue;}
        if(i+1==argc)throw std::invalid_argument("option_missing_value");
        std::string v=argv[++i];
        // Numeric parsing must consume the whole token; negative unsigned values rejected.
        auto number=[&](){size_t end=0;if(v.empty()||v[0]=='-')throw std::invalid_argument("bad_unsigned_option");auto x=std::stoull(v,&end);if(end!=v.size())throw std::invalid_argument("bad_numeric_option");return x;};
        auto small=[&](){auto x=number();if(x>unsigned(std::numeric_limits<int>::max()))throw std::invalid_argument("option_overflow");return int(x);};
        if(s=="--input")c.input=v;else if(s=="--out")c.out=v;else if(s=="--mode")c.mode=v;
        else if(s=="--a")c.a=small();else if(s=="--n")c.n=small();else if(s=="--time-ms")c.time_ms=small();
        else if(s=="--node-limit")c.node_limit=number();else if(s=="--clause-limit")c.clause_limit=number();
        else if(s=="--round-limit")c.rounds=small();else if(s=="--seed")c.seed=number();else if(s=="--steps")c.steps=number();
        else if(s=="--cache")c.cache=small();else if(s=="--bank")c.bank=small();else if(s=="--restart")c.restart=small();
        else if(s=="--min-size")c.min_size=small();else if(s=="--minimize-ms")c.minimize_ms=small();
        else if(s=="--max-delta")c.max_delta=small();
        else if(s=="--seconds"){size_t end=0;c.seconds=std::stod(v,&end);if(end!=v.size()||!std::isfinite(c.seconds))throw std::invalid_argument("bad_seconds");}
        else throw std::invalid_argument("unknown_option");
    }
    if(c.input.empty()||c.a<4||c.a>8||c.n<c.a||c.n>12||c.bank<2||c.bank>256||c.restart<1||c.min_size>64)
        throw std::invalid_argument("bad_configuration");
    if(c.mode!="lower"&&c.mode!="upper"&&c.mode!="ends"&&c.mode!="weak"&&c.mode!="strong")throw std::invalid_argument("bad_mode");
    if(c.command=="search"&&(c.seconds<=0||c.out.empty()))throw std::invalid_argument("search_requires_seconds_and_out");
    if(c.max_delta>=0&&(c.command!="check"||c.min_delta))throw std::invalid_argument("bound_is_check_only");
    return c;
}
int main(int argc,char** argv) {
    try {
        Config c=parse(argc,argv);
        if(c.command=="search")return Search(c).run();
        if(c.command!="check"&&c.command!="minimize")throw std::invalid_argument("unknown_command");
        Result r=evaluate(read_one(c.input),c);
        if(c.command=="minimize") {
            if(r.status!="NO_DELTA_COMPUTED"){report(std::cout,r,c);std::cout<<std::endl;return 20;}
            save(r,c,"failure");r=minimize(std::move(r),c,Clock::now()+std::chrono::milliseconds(c.minimize_ms));
        }
        save(r,c,c.command=="minimize"?"minimized":"check");report(std::cout,r,c);std::cout<<std::endl;
        return r.status=="OK"?0:r.status=="NO_DELTA_COMPUTED"?10:r.status=="NO_DELTA_WITHIN_BOUND"?11:r.status=="UNKNOWN"?20:r.status=="INVALID"?30:31;
    } catch(const std::exception& e) {
        std::cerr<<"ERROR: "<<e.what()<<'\n';return 2;
    }
}
