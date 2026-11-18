// One-thread, exact-coordinate finder for weak Delta containing the rightmost
// point. Includes the previous instrument; negative finder verdicts need LRAT.
#define main archived_search_main
#include "../../search/delta_search.cpp"
#undef main

Result rooted(const Points& points,const Config& c) {
    auto start=Clock::now();
    Budget b{start+std::chrono::milliseconds(c.time_ms),0,c.node_limit,0};
    Result r; r.p=points;
    try {
        Geometry g(points,b);r.p=g.p;
        Chains a=g.chains(g.all,b);summarize(a,r,c.n,5);
        if(r.maxcap>=5||r.maxgon>=c.n) {
            r.status="INVALID";r.reason="geometric_premise";
        } else {
            Chains direct=forward(g.p,g.all,b);
            if(direct.cap!=a.cap||direct.cup!=a.cup)throw std::logic_error("premise_crosscheck");
            r.caps=g.caps(4,c.clause_limit,b);r.negative=r.caps;
            if(!g.m)throw std::invalid_argument("empty_rooted_set");
            Mask root=bit(g.m-1);
            r.positive.push_back(root);
            std::unordered_set<Mask> seen{root};
            for(;;) {
                b.check();if(++r.rounds>c.rounds)throw Limit("round_limit");
                Solver sat(r.positive,r.negative,b,-1,g.all);
                if(!sat.solve()){r.status="NO_ROOTED_DELTA_COMPUTED";r.reason="exhaustive_DPLL";break;}
                r.delta=sat.model;
                if(!(r.delta&root))throw std::logic_error("missing_root");
                Mask rest=g.all&~r.delta;Chains q=g.chains(rest,b);bool added=false;
                for(int u=0;u<g.m;++u)if(rest&bit(u))for(int v=u+1;v<g.m;++v)if(rest&bit(v)) {
                    int z=u*g.m+v;
                    if(q.cap[z]+q.cup[z]-2>=c.n-1) {
                        Mask hit=q.cap_path[z]|q.cup_path[z];
                        if(count(hit)!=c.n-1)throw std::logic_error("wrong_polygon_size");
                        if(seen.insert(hit).second){
                            r.positive.push_back(hit);
                            r.witnesses.push_back({hit,q.cap_path[z],q.cup_path[z],true});added=true;
                        }
                    }
                }
                if(!added) {
                    if(!check_delta(g.p,r.delta,c,direct,b))throw std::logic_error("model_crosscheck");
                    r.status="OK";r.verified=true;break;
                }
            }
        }
    }catch(const Limit& e){r.status="UNKNOWN";r.reason=e.what();}
     catch(const std::invalid_argument& e){r.status="INVALID_INPUT";r.reason=e.what();}
    r.nodes=b.nodes;r.milliseconds=std::chrono::duration<double,std::milli>(Clock::now()-start).count();
    return r;
}

int main(int argc,char**argv) {
    try {
        if(argc!=5)throw std::runtime_error("usage: rooted n pool out per_case_ms");
        Config c;c.n=std::stoi(argv[1]);c.mode="weak";c.out=argv[3];c.time_ms=std::stoi(argv[4]);
        std::filesystem::create_directories(c.out);
        std::ifstream f(argv[2]);std::string magic;int version,k;
        if(!(f>>magic>>version>>k)||magic!="D3POOL"||version!=1)throw std::runtime_error("bad_pool");
        for(int i=0;i<k;++i){
            Points p=read_points(f);auto r=rooted(p,c);
            std::cout<<"{\"pool_index\":"<<i<<",\"result\":";report(std::cout,r,c);std::cout<<"}"<<std::endl;
            if(r.status=="NO_ROOTED_DELTA_COMPUTED")save(r,c,"candidate-"+std::to_string(i));
        }
        std::string extra;if(f>>extra)throw std::runtime_error("trailing_pool_input");
    }catch(const std::exception&e){std::cerr<<e.what()<<'\n';return 1;}
}
