// All x-order embeddings of a fixed signotope into a larger Delta instance.
// Inherited universal encoder is deliberately unchanged; see MODEL.md.
#define main delta_encoder_original_main
#include "../../encoder/delta_cnf.cpp"
#undef main
#include <sstream>

static std::string read_signs(const std::string& path, int count) {
    std::ifstream f(path);
    std::string s, extra;
    if (!(f >> s) || (f >> extra) || int(s.size()) != count ||
        s.find_first_not_of("+-") != std::string::npos)
        throw std::runtime_error("bad sign file: "+path);
    return s;
}

int main(int argc, char** argv) {
    try {
        Options o;
        o.pool="lattice"; o.sym="none";
        int old_m=15, added=-1;
        std::string old_path, fixed;
        bool embedding_only=false;
        for (int i=1; i<argc; ++i) {
            std::string s=argv[i];
            if (s=="--base-only") o.base=true;
            else if (s=="--embedding-only") embedding_only=true;
            else if (s=="--stats") o.stats=true;
            else if (s=="--help") {
                std::cout << "extension_cnf --old-signs FILE --add 0..5 --n 5..8\n"
                  "  --out CNF | --stats\n"
                  "  [--old-size 15] [--mode cup|weak] [--fixed-positions CSV]\n"
                  "  [--base-only | --embedding-only] [--pin-signs FILE]\n"
                  "Default: full counterexample search, all insertion gaps.\n";
                return 0;
            } else {
                if (i+1==argc) throw std::runtime_error("missing option value");
                std::string v=argv[++i];
                if (s=="--old-size") old_m=std::stoi(v);
                else if (s=="--add") added=std::stoi(v);
                else if (s=="--n") o.n=std::stoi(v);
                else if (s=="--mode") o.mode=v;
                else if (s=="--old-signs") old_path=v;
                else if (s=="--fixed-positions") fixed=v;
                else if (s=="--pin-signs") o.fix=v;
                else if (s=="--out") o.out=v;
                else throw std::runtime_error("unknown option: "+s);
            }
        }
        o.m=old_m+added;
        if (old_m<3 || added<0 || added>5 || o.m<4 || o.m>20 || o.n<5 || o.n>8)
            throw std::runtime_error("bad size: old>=3, add=0..5, total=4..20, n=5..8");
        if (o.mode!="cup" && o.mode!="weak") throw std::runtime_error("bad mode");
        if (o.out.empty()==!o.stats) throw std::runtime_error("choose --out or --stats");
        if (old_path.empty()) throw std::runtime_error("require --old-signs");
        if (embedding_only && o.base) throw std::runtime_error("choose only one partial mode");
        const std::string signs=read_signs(old_path,old_m*(old_m-1)*(old_m-2)/6);
        std::vector<int> positions;
        if (!fixed.empty()) {
            std::stringstream ss(fixed); std::string item;
            while (std::getline(ss,item,',')) positions.push_back(std::stoi(item));
            if (int(positions.size())!=old_m) throw std::runtime_error("wrong position count");
            for (int i=0; i<old_m; ++i)
                if (positions[i]<i || positions[i]>i+added ||
                    (i && positions[i]<=positions[i-1]))
                    throw std::runtime_error("positions must be an increasing embedding");
        }
        if (embedding_only) o.base=true; // Allocate only orientation variables.
        Encoder e(o);
        if (!embedding_only) e.base();
        if (!o.base) {
            e.cap_nodes(); e.endpoint_nodes(); e.seeds(); e.target_nodes(); e.pool();
        }
        e.restrictions(); // Only optional full-sign pins; no mirror or cube.
        const int universal_nv=e.nv;
        std::vector<std::vector<int>> at(old_m,std::vector<int>(added+1));
        for (auto& row:at) for (int& x:row) x=++e.nv;
        e.w.phase="embedding_one_hot";
        for (const auto& row:at) {
            e.w.add(row);
            for (int a=0; a<=added; ++a) for (int b=a+1; b<=added; ++b)
                e.w.add({-row[a],-row[b]});
        }
        e.w.phase="embedding_order";
        for (int i=0; i+1<old_m; ++i)
            for (int a=1; a<=added; ++a) for (int b=0; b<a; ++b)
                e.w.add({-at[i][a],-at[i+1][b]});
        e.w.phase="old_orientation";
        int idx=0;
        for (int i=0; i<old_m; ++i) for (int j=i+1; j<old_m; ++j)
          for (int k=j+1; k<old_m; ++k) {
            const int sign=signs[idx++]=='+'?1:-1;
            for (int a=0; a<=added; ++a) for (int b=a; b<=added; ++b)
              for (int c=b; c<=added; ++c)
                e.w.add({-at[i][a],-at[j][b],-at[k][c],sign*e.t(i+a,j+b,k+c)});
          }
        e.w.phase="fixed_positions";
        for (int i=0; i<int(positions.size()); ++i) e.w.add({at[i][positions[i]-i]});
        const uint64_t bytes=e.w.finish(e.nv);
        std::cout << "{\"label\":\"COMPUTED\",\"m\":" << o.m << ",\"n\":" << o.n
          << ",\"old_m\":" << old_m << ",\"added\":" << added
          << ",\"mode\":\"" << o.mode << "\",\"scope\":\""
          << (embedding_only?"embedding_only":o.base?"base_only":"counterexample")
          << "\",\"all_gaps\":" << (positions.empty()?"true":"false")
          << ",\"variables\":" << e.nv << ",\"universal_variables\":" << universal_nv
          << ",\"triples\":" << e.nt << ",\"clauses\":" << e.w.clauses
          << ",\"literals\":" << e.w.literals << ",\"cnf_bytes\":" << bytes
          << ",\"selector_ids\":[";
        for (int i=0; i<old_m; ++i) {
            if (i) std::cout << ',';
            std::cout << '[';
            for (int d=0; d<=added; ++d) { if (d) std::cout << ','; std::cout << at[i][d]; }
            std::cout << ']';
        }
        std::cout << "],\"phases\":{";
        bool first=true;
        for (const auto& [name,c]:e.w.counts) {
            if (!first) std::cout << ',';
            first=false;
            std::cout << '"' << name << "\":{\"clauses\":" << c[0]
                << ",\"literals\":" << c[1] << '}';
        }
        std::cout << "}}\n";
    } catch (const std::exception& e) { std::cerr << "ERROR: " << e.what() << '\n'; return 1; }
}
