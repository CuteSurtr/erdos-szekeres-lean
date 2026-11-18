// Phase 2 (13 Nov 2026): trim a text LRAT proof to the derivation cone of the empty clause.
// usage: p2_lrat_trim <cnf> <lrat> <out.cnf> <out.lrat> <out.used>
// Pass 1 (backward over the LRAT file, block reads from the end): mark the empty clause and, for every marked
//   addition line, all its hints.  Only a bitset over clause ids is kept in memory.
// Pass 2 (forward): new ids = rank among marked ids (original clauses first, in CNF order, then learned clauses in
//   proof order).  out.cnf = the marked original clauses in CNF order (same variable count); out.lrat = the marked
//   addition lines with renumbered ids and hints, and the deletion lines restricted to marked ids (renumbered).
//   out.used = the original clause ids (1-based, CNF order) that are marked, one per line.
// Nothing here is trusted: cake_lpr checks out.lrat against out.cnf.
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <string>
#include <vector>
#include <algorithm>
using namespace std;
typedef long long ll;

static vector<uint64_t> bits;
static inline void mark(ll id) {
  if (id <= 0) { fprintf(stderr, "bad id %lld\n", id); exit(3); }
  size_t w = (size_t)id >> 6;
  if (w >= bits.size()) bits.resize(max(w + 1, bits.size() * 2), 0);
  bits[w] |= (1ULL << (id & 63));
}
static inline bool marked(ll id) {
  size_t w = (size_t)id >> 6;
  return w < bits.size() && (bits[w] >> (id & 63)) & 1ULL;
}
static vector<uint32_t> cum;  // cum[w] = number of marked ids in words < w
static inline ll rnk(ll id) {  // number of marked ids <= id (id must be marked)
  size_t w = (size_t)id >> 6; uint64_t m = bits[w] & ((id & 63) == 63 ? ~0ULL : ((1ULL << ((id & 63) + 1)) - 1));
  return (ll)cum[w] + __builtin_popcountll(m);
}

// parse integers of a line [p, e)
static inline const char* nexttok(const char* p, const char* e) { while (p < e && (*p == ' ' || *p == '\t' || *p == '\r')) ++p; return p; }

static ll empty_id = -1; static ll n_lines = 0, n_add = 0, n_marked_add = 0;
// process one LRAT line in the backward pass
static void back_line(const char* p, const char* e) {
  p = nexttok(p, e); if (p >= e) return;
  char* q; ll id = strtoll(p, &q, 10); p = q; p = nexttok(p, e);
  if (p < e && *p == 'd') return;  // deletion
  n_add++;
  // literals until 0
  ll lits = 0;
  while (true) { p = nexttok(p, e); if (p >= e) { fprintf(stderr, "truncated line id %lld\n", id); exit(4); }
    ll x = strtoll(p, &q, 10); p = q; if (x == 0) break; lits++; }
  if (lits == 0 && empty_id < 0) { empty_id = id; mark(id); }
  if (!marked(id)) return;
  n_marked_add++;
  while (true) { p = nexttok(p, e); if (p >= e) { fprintf(stderr, "truncated hints id %lld\n", id); exit(4); }
    ll x = strtoll(p, &q, 10); p = q; if (x == 0) break; mark(x < 0 ? -x : x); }
}

int main(int argc, char** argv) {
  if (argc != 6) { fprintf(stderr, "usage: %s cnf lrat out.cnf out.lrat out.used\n", argv[0]); return 1; }
  // CNF header
  FILE* fc = fopen(argv[1], "r"); if (!fc) { perror("cnf"); return 1; }
  ll nv = -1, nc = -1; { char line[4096];
    while (fgets(line, sizeof line, fc)) { if (line[0] == 'c') continue; if (sscanf(line, "p cnf %lld %lld", &nv, &nc) == 2) break; } }
  if (nc < 0) { fprintf(stderr, "no header\n"); return 1; }
  // Pass 1: backward
  FILE* fl = fopen(argv[2], "rb"); if (!fl) { perror("lrat"); return 1; }
  fseeko(fl, 0, SEEK_END); off_t size = ftello(fl);
  const size_t BS = getenv("P2_BS") ? (size_t)atoll(getenv("P2_BS")) : (size_t)(1 << 26); vector<char> blk; string carry;  // carry = start of a line that continues into the next block
  off_t pos = size;
  while (pos > 0) {
    size_t len = (size_t)min<off_t>(BS, pos); pos -= len;
    size_t tot = len + carry.size();
    blk.resize(tot + 1); blk[tot] = '\n';  // sentinel: strtoll must not read past the last line of the block
    fseeko(fl, pos, SEEK_SET); if (fread(blk.data(), 1, len, fl) != len) { perror("read"); return 1; }
    memcpy(blk.data() + len, carry.data(), carry.size());
    // lines: split by '\n'; the first partial line (before the first '\n') is carried unless pos == 0
    size_t end = tot;
    // strip trailing newline(s)
    while (true) {
      // find last '\n' before end
      size_t i = end; while (i > 0 && blk[i - 1] != '\n') --i;
      if (i == 0) { // no newline: [0,end) is a partial line
        if (pos == 0) { if (end > 0) { back_line(blk.data(), blk.data() + end); n_lines++; } carry.clear(); }
        else carry.assign(blk.data(), end);
        break;
      }
      if (end > i) { back_line(blk.data() + i, blk.data() + end); n_lines++; }
      end = i - 1;  // position of '\n'
    }
  }
  if (empty_id < 0) { fprintf(stderr, "no empty clause in proof\n"); return 2; }
  // rank structure
  cum.assign(bits.size() + 1, 0);
  for (size_t w = 0; w < bits.size(); ++w) cum[w + 1] = cum[w] + __builtin_popcountll(bits[w]);
  ll n_orig_marked = 0;
  for (ll i = 1; i <= nc; ++i) if (marked(i)) n_orig_marked++;
  // Pass 2a: trimmed CNF + used ids
  FILE* oc = fopen(argv[3], "w"); FILE* ou = fopen(argv[5], "w"); if (!oc || !ou) { perror("out"); return 1; }
  fprintf(oc, "p cnf %lld %lld\n", nv, n_orig_marked);
  { rewind(fc); char* line = nullptr; size_t cap = 0; ssize_t r; ll cid = 0; bool hdr = false;
    while ((r = getline(&line, &cap, fc)) > 0) {
      if (line[0] == 'c') continue;
      if (!hdr && line[0] == 'p') { hdr = true; continue; }
      // a clause per line (our writers put exactly one clause per line)
      const char* p = line; while (*p == ' ' || *p == '\t') ++p; if (*p == '\n' || *p == 0) continue;
      ++cid; if (marked(cid)) { fputs(line, oc); fprintf(ou, "%lld\n", cid); }
    }
    free(line);
    if (cid != nc) { fprintf(stderr, "clause count %lld != header %lld (one clause per line expected)\n", cid, nc); return 5; } }
  fclose(oc); fclose(ou);
  // Pass 2b: trimmed LRAT
  FILE* ol = fopen(argv[4], "w"); if (!ol) { perror("out lrat"); return 1; }
  static char obuf[1 << 22]; setvbuf(ol, obuf, _IOFBF, sizeof obuf);
  rewind(fl);
  { char* line = nullptr; size_t cap = 0; ssize_t r; ll last_new = n_orig_marked; bool done = false; vector<ll> keep;
    while (!done && (r = getline(&line, &cap, fl)) > 0) {
      const char* p = line; const char* e = line + r; char* q;
      p = nexttok(p, e); if (p >= e || *p == '\n') continue;
      ll id = strtoll(p, &q, 10); p = q; p = nexttok(p, e);
      if (p < e && *p == 'd') {
        ++p; keep.clear();
        while (true) { p = nexttok(p, e); if (p >= e || *p == '\n') break; ll x = strtoll(p, &q, 10); p = q; if (x == 0) break; if (marked(x)) keep.push_back(rnk(x)); }
        if (!keep.empty()) { fprintf(ol, "%lld d", last_new); for (ll x : keep) fprintf(ol, " %lld", x); fputs(" 0\n", ol); }
        continue;
      }
      if (!marked(id)) continue;
      ll nid = rnk(id); last_new = nid;
      fprintf(ol, "%lld", nid);
      while (true) { p = nexttok(p, e); ll x = strtoll(p, &q, 10); p = q; fprintf(ol, " %lld", x); if (x == 0) break; }
      while (true) { p = nexttok(p, e); ll x = strtoll(p, &q, 10); p = q;
        if (x == 0) { fputs(" 0\n", ol); break; }
        ll a = x < 0 ? -x : x; if (!marked(a)) { fprintf(stderr, "unmarked hint %lld in marked line %lld\n", a, id); return 6; }
        fprintf(ol, " %lld", x < 0 ? -rnk(a) : rnk(a)); }
      if (id == empty_id) done = true;
    }
    free(line); }
  fclose(ol); fclose(fl); fclose(fc);
  fprintf(stdout, "{\"lrat_lines\": %lld, \"additions\": %lld, \"marked_additions\": %lld, \"empty_id\": %lld, \"originals\": %lld, \"marked_originals\": %lld, \"marked_total\": %lld}\n",
          n_lines, n_add, n_marked_add, empty_id, nc, n_orig_marked, (ll)cum[bits.size()]);
  return 0;
}
