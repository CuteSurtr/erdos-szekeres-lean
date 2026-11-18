// Structured terminal obstruction: low_split(L, an (n-4)-cup).
// SAT is only an abstract candidate; a real claim needs exact coordinates.
// UNSAT is only a restricted theorem after independent projection audit.
#define main archived_compact_main
#include "../../compact/compact_cnf.cpp"
#undef main

int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::runtime_error("left_m n output.cnf|--stats");
        Options o;
        o.m = std::stoi(argv[1]);
        o.n = std::stoi(argv[2]);
        if (o.n < 6 || o.n > 8 || o.m < o.n - 1 || o.m > 16)
            throw std::runtime_error("domain");
        if (std::string(argv[3]) != "--stats") {
            o.out = argv[3];
            o.mapfile = o.out + ".map";
        }
        Encoder e(o);
        e.geometry();
        e.w.set_phase("left_has_no_fourcap");
        choose(e.full, 4, [&](Mask s) {
            std::vector<int> row;
            choose(s, 3, [&](Mask t) {
                auto v = vertices(t);
                row.push_back(e.t(v[0], v[1], v[2]));
            });
            e.w.add(row);
        });
        std::vector<int> ends(o.m);
        e.w.set_phase("ends_three_cap_equivalence");
        for (int b = 0; b < o.m; ++b) {
            int z = ends[b] = e.fresh("ends_three_cap", Mask(1) << b);
            std::vector<int> row = {-z};
            for (int a = 0; a < b; ++a) for (int c = a + 1; c < b; ++c) {
                int t = e.t(a, c, b);
                row.push_back(-t);
                e.w.add({z, t});
            }
            e.w.add(row);
        }
        e.w.set_phase("no_covered_cup_transversal");
        int limit = o.m - o.n + 2;
        for (Mask s = 0; s <= e.full; ++s) if (pc(s) <= limit) {
            std::vector<int> row;
            choose(s, 3, [&](Mask t) {
                auto v = vertices(t);
                row.push_back(-e.t(v[0], v[1], v[2]));
            });
            auto v = vertices(s);
            for (size_t j = 1; j < v.size(); ++j) row.push_back(-ends[v[j]]);
            choose(e.full ^ s, o.n - 1, [&](Mask q) {
                if (!e.Q[q]) throw std::runtime_error("missing target");
                row.push_back(e.Q[q]);
            });
            e.w.add(row);
        }
        e.w.set_phase("no_small_blue_two_cup_partition");
        for (Mask s = 0; s <= e.full; ++s)
            if (pc(s) <= o.n - 1 && pc(e.full ^ s) <= o.n - 2) {
                std::vector<int> row;
                for (Mask part : {s, e.full ^ s}) choose(part, 3, [&](Mask t) {
                    auto v = vertices(t);
                    row.push_back(-e.t(v[0], v[1], v[2]));
                });
                e.w.add(row);
            }
        auto bytes = e.w.finish(e.nv);
        if (e.mapping) {
            e.mapping.flush();
            if (!e.mapping) throw std::runtime_error("map write");
        }
        std::cout << "{\"label\":\"COMPUTED structured formula\",\"left_m\":" << o.m
                  << ",\"right_m\":" << o.n - 4 << ",\"n\":" << o.n
                  << ",\"full_m\":" << o.m + o.n - 4 << ",\"variables\":" << e.nv
                  << ",\"clauses\":" << e.w.clauses << ",\"literals\":" << e.w.literals
                  << ",\"bytes\":" << bytes << ",\"phases\":{";
        bool first = true;
        for (auto [name, count] : e.w.counts) {
            if (!first) std::cout << ',';
            first = false;
            std::cout << '"' << name << "\":{\"clauses\":" << count[0]
                      << ",\"literals\":" << count[1] << '}';
        }
        std::cout << "}}\n";
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }
}
