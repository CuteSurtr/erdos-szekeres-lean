// Enumerate models of a CNF projected onto variables 1..nX (blocking clauses on the projection).
// usage: enum_models cnf nX max_models out.txt [time_limit_s] [conflicts_per_solve]
// Writes one line per model: the nX signed literals.  Prints a summary line:
//   ENUM models=<k> status=<EXHAUSTED|BUDGET|TIMEOUT|UNKNOWN> time=<s>
#include "cadical.hpp"
#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <vector>

int main(int argc, char **argv) {
    if (argc < 5) { std::fprintf(stderr, "usage: enum_models cnf nX max_models out.txt [time_limit_s] [conflicts]\n"); return 2; }
    int nX = std::atoi(argv[2]);
    long maxm = std::atol(argv[3]);
    double tlim = argc > 5 ? std::atof(argv[5]) : 1e18;
    long conf = argc > 6 ? std::atol(argv[6]) : -1;
    CaDiCaL::Solver s;
    s.set("quiet", 1);
    int vars = 0;
    const char *err = s.read_dimacs(argv[1], vars, 1);
    if (err) { std::fprintf(stderr, "parse error: %s\n", err); return 2; }
    FILE *out = std::fopen(argv[4], "w");
    auto t0 = std::chrono::steady_clock::now();
    long models = 0;
    const char *status = "EXHAUSTED";
    while (true) {
        double el = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
        if (el > tlim) { status = "TIMEOUT"; break; }
        if (models >= maxm) { status = "BUDGET"; break; }
        if (conf > 0) s.limit("conflicts", (int) conf);
        int res = s.solve();
        if (res == 20) { status = "EXHAUSTED"; break; }
        if (res != 10) { status = "UNKNOWN"; break; }
        models++;
        std::vector<int> block;
        for (int v = 1; v <= nX; v++) {
            int l = s.val(v) > 0 ? v : -v;
            std::fprintf(out, "%d ", l);
            block.push_back(-l);
        }
        std::fprintf(out, "\n");
        std::fflush(out);
        for (int l : block) s.add(l);
        s.add(0);
    }
    std::fclose(out);
    double el = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();
    std::printf("ENUM models=%ld status=%s time=%.2f\n", models, status, el);
    return 0;
}
