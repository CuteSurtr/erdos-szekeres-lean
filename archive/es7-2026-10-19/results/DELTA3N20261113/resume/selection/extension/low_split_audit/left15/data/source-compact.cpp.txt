// Same structured predicate as low_split_cnf.cpp; exact containment lattices.
#define main archived_compact_main
#include "../../compact/compact_cnf.cpp"
#undef main

int main(int argc, char** argv) {
    try {
        if (argc != 4) throw std::runtime_error("left_m n output.cnf|--stats");
        Options o;
        o.m = std::stoi(argv[1]); o.n = std::stoi(argv[2]);
        if (o.n < 6 || o.n > 8 || o.m < o.n - 1 || o.m > 16)
            throw std::runtime_error("domain");
        if (std::string(argv[3]) != "--stats") {
            o.out = argv[3]; o.mapfile = o.out + ".map";
        }
        Encoder e(o);
        e.geometry();
        auto exact_or = [&](int z, const std::vector<int>& literals) {
            e.disjunction(z, literals);
            for (int literal : literals) e.w.add({z, -literal});
        };
        e.w.set_phase("left_has_no_fourcap");
        choose(e.full, 4, [&](Mask s) {
            std::vector<int> row;
            choose(s, 3, [&](Mask t) {
                auto v = vertices(t); row.push_back(e.t(v[0], v[1], v[2]));
            });
            e.w.add(row);
        });
        std::vector<int> ends(o.m), D(e.full + 1), T(e.full + 1);
        e.w.set_phase("ends_three_cap_equivalence");
        for (int b = 0; b < o.m; ++b) {
            int z = ends[b] = e.fresh("ends_three_cap", Mask(1) << b);
            std::vector<int> literals;
            for (int a = 0; a < b; ++a) for (int c = a + 1; c < b; ++c)
                literals.push_back(-e.t(a, c, b));
            exact_or(z, literals);
        }
        e.w.set_phase("bad_pair_or_cap_exact_containment");
        choose(e.full, 2, [&](Mask s) {
            auto v = vertices(s); D[s] = -ends[v[1]];
        });
        choose(e.full, 3, [&](Mask s) {
            auto v = vertices(s);
            int z = D[s] = e.fresh("bad_pair_or_cap_contains", s);
            exact_or(z, {-e.t(v[0], v[1], v[2]), -ends[v[1]], -ends[v[2]]});
        });
        int limit = o.m - o.n + 2;
        for (Mask s = 0; s <= e.full; ++s) if (pc(s) >= 4 && pc(s) <= limit) {
            int z = D[s] = e.fresh("bad_pair_or_cap_contains", s);
            exact_or(z, e.children(s, D, 4));
        }
        e.w.set_phase("target_exact_containment");
        for (Mask s = 0; s <= e.full; ++s) {
            if (pc(s) == o.n - 1) T[s] = e.Q[s];
            else if (pc(s) > o.n - 1) {
                int z = T[s] = e.fresh("target_contains", s);
                exact_or(z, e.children(s, T, o.n));
            }
        }
        e.w.set_phase("no_covered_cup_transversal");
        for (Mask s = 0; s <= e.full; ++s) if (pc(s) <= limit) {
            std::vector<int> row;
            if (D[s]) row.push_back(D[s]);
            if (T[e.full ^ s]) row.push_back(T[e.full ^ s]);
            e.w.add(row);
        }
        e.w.set_phase("no_small_blue_two_cup_partition");
        for (Mask s = 0; s <= e.full; ++s)
            if (pc(s) <= o.n - 1 && pc(e.full ^ s) <= o.n - 2) {
                std::vector<int> row;
                for (Mask part : {s, e.full ^ s}) choose(part, 3, [&](Mask t) {
                    auto v = vertices(t); row.push_back(-e.t(v[0], v[1], v[2]));
                });
                e.w.add(row);
            }
        auto bytes = e.w.finish(e.nv);
        if (e.mapping) { e.mapping.flush(); if (!e.mapping) throw std::runtime_error("map write"); }
        std::cout << "{\"label\":\"COMPUTED structured compact formula\",\"left_m\":" << o.m
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
        std::cerr << error.what() << '\n'; return 1;
    }
}
