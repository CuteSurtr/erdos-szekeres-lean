// Exact unit propagation only. No variable elimination or heuristic deductions.
// Keeps every derived unit in the output and preserves all variable IDs.
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

int main(int argc,char**argv) {
    try {
        if(argc!=3) throw std::runtime_error("usage: unit_simplify INPUT.cnf OUTPUT.cnf");
        const auto started=std::chrono::steady_clock::now();
        std::ifstream in(argv[1]);
        if(!in) throw std::runtime_error("cannot open input");
        std::string line;
        int nv=0; size_t nc=0;
        while(std::getline(in,line)) {
            if(line.empty()||line[0]=='c') continue;
            if(std::sscanf(line.c_str(),"p cnf %d %zu",&nv,&nc)!=2)
                throw std::runtime_error("missing header");
            break;
        }
        if(nv<=0) throw std::runtime_error("bad variable count");
        std::vector<int> lits;
        std::vector<size_t> ends{0}; ends.reserve(nc+1);
        int x;
        while(in>>x) {
            if(x==0) ends.push_back(lits.size());
            else {
                if(std::abs(x)>nv) throw std::runtime_error("bad literal");
                lits.push_back(x);
            }
        }
        if(!in.eof() || ends.size()!=nc+1 || ends.back()!=lits.size())
            throw std::runtime_error("malformed clauses");
        std::vector<signed char> val(nv+1,0);
        bool conflict=false,changed=true;
        size_t rounds=0,units=0;
        while(changed && !conflict) {
            changed=false; ++rounds;
            for(size_t c=0;c<nc;++c) {
                size_t unknown=0; int last=0; bool satisfied=false;
                for(size_t j=ends[c];j<ends[c+1];++j) {
                    const int l=lits[j], v=val[std::abs(l)];
                    if(!v) {++unknown;last=l;}
                    else if(v==(l>0?1:-1)) {satisfied=true;break;}
                }
                if(satisfied) continue;
                if(!unknown) {conflict=true;break;}
                if(unknown==1) {
                    val[std::abs(last)]=last>0?1:-1;
                    ++units;changed=true;
                }
            }
        }
        FILE* out=std::fopen(argv[2],"wb+");
        if(!out) throw std::runtime_error("cannot open output");
        std::string pad(95,' '); pad+='\n'; std::fputs(pad.c_str(),out);
        size_t clauses=0,literals=0,remaining=0;
        if(conflict) {std::fputs("0\n",out);++clauses;}
        else {
            for(int v=1;v<=nv;++v) if(val[v]) {
                std::fprintf(out,"%d 0\n",val[v]>0?v:-v);++clauses;++literals;
            }
            for(size_t c=0;c<nc;++c) {
                bool satisfied=false;
                for(size_t j=ends[c];j<ends[c+1];++j) {
                    int l=lits[j];
                    if(val[std::abs(l)]==(l>0?1:-1)) {satisfied=true;break;}
                }
                if(satisfied) continue;
                for(size_t j=ends[c];j<ends[c+1];++j) {
                    int l=lits[j];
                    if(!val[std::abs(l)]) {std::fprintf(out,"%d ",l);++literals;}
                }
                std::fputs("0\n",out);++clauses;++remaining;
            }
        }
        if(std::ferror(out)||std::fflush(out)) throw std::runtime_error("write failure");
        const long bytes=std::ftell(out);
        if(std::fseek(out,0,SEEK_SET)) throw std::runtime_error("seek failure");
        std::string header="p cnf "+std::to_string(nv)+" "+std::to_string(clauses);
        header.resize(95,' '); header+='\n'; std::fputs(header.c_str(),out);
        if(std::fclose(out)) throw std::runtime_error("close failure");
        double seconds=std::chrono::duration<double>(std::chrono::steady_clock::now()-started).count();
        std::cout<<"{\"label\":\"COMPUTED\",\"operation\":\"unit propagation\",\"input_clauses\":"<<nc
          <<",\"input_literals\":"<<lits.size()<<",\"variables\":"<<nv<<",\"clauses\":"<<clauses
          <<",\"literals\":"<<literals<<",\"derived_units\":"<<units<<",\"remaining_clauses\":"<<remaining
          <<",\"rounds\":"<<rounds<<",\"conflict\":"<<(conflict?"true":"false")
          <<",\"cnf_bytes\":"<<bytes<<",\"seconds\":"<<seconds<<"}\n";
    } catch(const std::exception& e) {std::cerr<<"ERROR: "<<e.what()<<'\n';return 1;}
}
