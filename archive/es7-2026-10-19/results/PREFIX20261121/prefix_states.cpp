// Enumerate possible occupied-state sets of the first eight points in x-order.
// Orient the first triple as a cup. Reflecting all y-coordinates achieves this.
#include <algorithm>
#include <array>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <map>
#include <numeric>
#include <stdexcept>
#include <vector>

constexpr int limit = 8;
using Shape = std::array<int, 5>;
using Pattern = std::array<unsigned char, limit>;
using Bits = std::uint32_t;

int pair_id(int i, int j) { return j * (j - 1) / 2 + i; }
Bits bit(int i) { return Bits{1} << i; }

class Prefixes {
    std::map<Shape, int> index;
    std::array<Bits, limit> signs{};
    int cap[limit][limit]{}, cup[limit][limit]{};
    Pattern order{};
    std::array<std::map<Pattern, unsigned>, limit + 1> patterns;
    std::array<unsigned, limit + 1> balanced{};

    void extend(int k, Bits incoming) {
        signs[k] = incoming;
        Shape f{};
        for (int j = 0; j < k; ++j) {
            int a = 1, b = 1;
            for (int i = 0; i < j; ++i) {
                if (incoming & bit(pair_id(i,j))) b = std::max(b, cup[i][j] + 1);
                else a = std::max(a, cap[i][j] + 1);
            }
            if (a > 5 || b > 5) return;
            cap[j][k] = a;
            cup[j][k] = b;
            for (int t = 0; t < a; ++t) f[t] = std::max(f[t], b);
        }
        order[k] = static_cast<unsigned char>(index.at(f));
        Pattern key{};
        std::copy_n(order.begin(), k+1, key.begin());
        std::sort(key.begin(), key.begin()+k+1);
        if (std::adjacent_find(key.begin(),key.begin()+k+1) != key.begin()+k+1)
            throw std::runtime_error("repeated owner state");
        ++patterns[k+1][key];
        ++balanced[k+1];
        if (k+1 < limit) next(k+1);
    }

    void next(int k) {
        int m = k * (k-1) / 2;
        Bits all = bit(m)-1;
        std::array<Bits, 28> above{}, below{};
        for (int i = 0; i < m; ++i) above[i] = bit(i);
        // For i<j<h<k, the four signs ijh, ijk, ihk, jhk change at most once.
        for (int h = 2; h < k; ++h)
            for (int j = 1; j < h; ++j)
                for (int i = 0; i < j; ++i) {
                    int a = pair_id(i,j), b = pair_id(i,h), c = pair_id(j,h);
                    if (signs[h] & bit(a)) std::swap(a,c);
                    above[a] |= bit(b);
                    above[b] |= bit(c);
                }
        for (int mid = 0; mid < m; ++mid)
            for (int i = 0; i < m; ++i)
                if (above[i] & bit(mid)) above[i] |= above[mid];
        for (int i = 0; i < m; ++i)
            for (int j = 0; j < m; ++j)
                if (above[i] & bit(j)) below[j] |= bit(i);
        auto assign = [&](auto&& self, Bits yes, Bits no) -> void {
            Bits free = all & ~(yes | no);
            if (!free) { extend(k,yes); return; }
            int i = __builtin_ctz(free);
            if (!(no & above[i])) self(self,yes | above[i], no);
            if (!(yes & below[i])) self(self,yes, no | below[i]);
        };
        assign(assign, k == 2 ? bit(0) : 0, 0);
    }

public:
    void run(std::ostream& out) {
        std::vector<Shape> states;
        for (int a = 0; a <= 5; ++a)
          for (int b = 0; b <= a; ++b)
            for (int c = 0; c <= b; ++c)
              for (int d = 0; d <= c; ++d)
                for (int e = 0; e <= d; ++e) states.push_back({a,b,c,d,e});
        auto area=[](const Shape& f){return std::accumulate(f.begin(),f.end(),0);};
        std::stable_sort(states.begin(), states.end(), [&](const Shape& a, const Shape& b) {
            return area(a) < area(b);
        });
        for (int j=0; j<int(states.size()); ++j) index[states[j]]=j;
        if (index.size()!=252) throw std::runtime_error("catalog order");
        next(0);
        for (int k=1; k<=limit; ++k) {
            std::cerr << k << ' ' << balanced[k] << ' ' << patterns[k].size() << '\n';
            for (const auto& entry : patterns[k]) {
                out << k << ' ' << entry.second;
                for (int j=0; j<k; ++j) out << ' ' << int(entry.first[j]);
                out << '\n';
            }
        }
    }
};

int main() {
    Prefixes p;
    p.run(std::cout);
    return std::cout ? 0 : 1;
}
