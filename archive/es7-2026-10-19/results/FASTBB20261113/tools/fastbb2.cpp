// fastbb.cpp -- compiled exact LP branch-and-bound that FINDS omission trees (13 Nov 2026, track FASTBB).
//
// It is a drop-in finder for experiments/omission-final313-2026-10-11/search/pbb_strong.py:
// same question (is there a 0/1 hole vector with at most BUDGET holes, state 0 occupied, satisfying
// every row "sum of h over support >= rhs"?), same output files (master.json, ctx-N.json.gz with
// node types branch / weighted / over_budget / context), so that assemble.py and
// scripts/omission_tree.check_tree replay its trees unchanged.  Nothing here is trusted: the LP
// (a hand-written bounded dual simplex in double precision) only proposes row weights; a leaf is
// written only if its integer margin (the margin() formula of pbb_strong.py) is positive in exact
// 128-bit integer arithmetic, and the Python replay re-checks everything in unbounded integers.
//
// Build:  g++ -std=c++20 -O3 -march=native -fopenmp-simd -pthread -o fastbb fastbb.cpp -lz
#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cctype>
#include <cerrno>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <map>
#include <memory>
#include <mutex>
#include <string>
#include <thread>
#include <vector>
#include <fcntl.h>
#include <signal.h>
#include <sys/stat.h>
#include <unistd.h>
#include <zlib.h>

typedef long long i64;
typedef __int128 i128;
static const int MAXN = 192;  // at most 192 states (three 64-bit words)
static const int NW = 3;

static double nowSec() {
  using namespace std::chrono;
  return duration<double>(steady_clock::now().time_since_epoch()).count();
}
[[noreturn]] static void fatal(const char* msg) {
  fprintf(stderr, "FATAL: %s\n", msg);
  fflush(stderr);
  _exit(2);
}

struct Mask {
  uint64_t w[NW];
  Mask() { for (int i = 0; i < NW; i++) w[i] = 0; }
  inline bool test(int i) const { return (w[i >> 6] >> (i & 63)) & 1ULL; }
  inline void set(int i) { w[i >> 6] |= 1ULL << (i & 63); }
  inline void clr(int i) { w[i >> 6] &= ~(1ULL << (i & 63)); }
  inline int count() const { int c = 0; for (int i = 0; i < NW; i++) c += __builtin_popcountll(w[i]); return c; }
};
static inline int popand(const Mask& a, const Mask& b) {
  int c = 0;
  for (int i = 0; i < NW; i++) c += __builtin_popcountll(a.w[i] & b.w[i]);
  return c;
}

// ------------------------------------------------------------------ problem
struct Problem {
  int N = 0, R = 0, baseRows = 0, budget = 0, stride = 0;
  std::string source, extra, sourceSha, extraSha;
  std::vector<int> dem, rsz, rstart;
  std::vector<uint8_t> ridx;
  std::vector<Mask> mask;
  std::vector<int> cstart, cidx, cdeg;
  std::vector<double> rnorm;
  // ---- slice mode (track G2, phase 2): rows baseRows (capF: h(F) >= t) and baseRows+1 (capL: h(Lo) >= b)
  // with t + b = budget.  The score LP is  phi = min h(Lo)  s.t. every row except capF/capL, the node's
  // fixings and the side constraint h(F) <= t (LP constraint index n + R, normal -1 on F, rhs -t).
  bool slice = false;
  int capF = -1, capL = -1, sliceT = 0, sliceB = 0;
  Mask Fm, Lm;
  std::vector<int> Fidx;
  bool setupSlice() {
    if (baseRows + 1 >= R) return false;
    capF = baseRows; capL = baseRows + 1;
    Fm = mask[capF]; Lm = mask[capL];
    Mask both, all;
    for (int i = 0; i < NW; i++) { both.w[i] = Fm.w[i] & Lm.w[i]; all.w[i] = Fm.w[i] | Lm.w[i]; }
    if (both.count() != 0 || all.count() != N) return false;      // F and Lo partition the states
    sliceT = dem[capF]; sliceB = dem[capL];
    if (sliceT + sliceB != budget || sliceT <= 0 || sliceB <= 0) return false;
    Fidx.clear();
    for (int i = 0; i < N; i++) if (Fm.test(i)) Fidx.push_back(i);
    rnorm.resize(R + 1);
    rnorm[R] = 1.0 / std::sqrt((double)Fidx.size());
    slice = true;
    return true;
  }

  bool load(const char* path) {
    FILE* f = fopen(path, "r");
    if (!f) return false;
    char key[64], val[8192];
    int ver = 0;
    if (fscanf(f, "%63s %d", key, &ver) != 2 || strcmp(key, "FASTBB-ROWS") != 0 || ver != 1) { fclose(f); return false; }
    while (fscanf(f, "%63s %8191s", key, val) == 2) {
      if (!strcmp(key, "source")) source = val;
      else if (!strcmp(key, "source_sha256")) sourceSha = val;
      else if (!strcmp(key, "extra")) extra = val;
      else if (!strcmp(key, "extra_sha256")) extraSha = val;
      else if (!strcmp(key, "states")) N = atoi(val);
      else if (!strcmp(key, "base_rows")) baseRows = atoi(val);
      else if (!strcmp(key, "rows")) { R = atoi(val); break; }
      else { fclose(f); return false; }
    }
    if (N <= 0 || N > MAXN || R <= 0) { fclose(f); return false; }
    dem.resize(R); rsz.resize(R); rstart.assign(R + 1, 0); mask.assign(R, Mask());
    std::vector<int> deg(N, 0);
    for (int r = 0; r < R; r++) {
      int d, k;
      if (fscanf(f, "%d %d", &d, &k) != 2 || k < 0 || k > N || d < 0 || d > k) { fclose(f); return false; }
      dem[r] = d; rsz[r] = k; rstart[r] = (int)ridx.size();
      for (int t = 0; t < k; t++) {
        int i;
        if (fscanf(f, "%d", &i) != 1 || i < 0 || i >= N || mask[r].test(i)) { fclose(f); return false; }
        mask[r].set(i); ridx.push_back((uint8_t)i); deg[i]++;
      }
    }
    rstart[R] = (int)ridx.size();
    fclose(f);
    cstart.assign(N + 1, 0);
    for (int i = 0; i < N; i++) cstart[i + 1] = cstart[i] + deg[i];
    cidx.resize(ridx.size());
    std::vector<int> fill(cstart.begin(), cstart.end() - 1);
    for (int r = 0; r < R; r++)
      for (int t = rstart[r]; t < rstart[r + 1]; t++) cidx[fill[ridx[t]]++] = r;
    cdeg = deg;
    rnorm.resize(R);
    for (int r = 0; r < R; r++) rnorm[r] = rsz[r] ? 1.0 / std::sqrt((double)rsz[r]) : 0.0;
    stride = (N + 7) & ~7;
    return true;
  }
  // FNV-1a over the first `upto` rows: used to check on resume that rows were only appended.
  uint64_t prefixHash(int upto) const {
    uint64_t hsh = 1469598103934665603ULL;
    auto mix = [&](uint64_t x) { for (int b = 0; b < 4; b++) { hsh ^= (x >> (8 * b)) & 255; hsh *= 1099511628211ULL; } };
    mix((uint64_t)N);
    for (int r = 0; r < upto && r < R; r++) {
      mix((uint64_t)dem[r]); mix((uint64_t)rsz[r]);
      for (int t = rstart[r]; t < rstart[r + 1]; t++) mix(ridx[t]);
    }
    return hsh;
  }
};

// The margin() formula of pbb_strong.py / omission_tree.leaf_margin, in exact 128-bit integers,
// computed from the masks alone (no incremental state).  Weights are bounded by 2^40 and there are
// at most a few thousand rows, so nothing can overflow.  Returns -1 for malformed input.
static i128 marginExact(const Problem& P, const Mask& M, const Mask& O, i64 cap,
                        const std::vector<std::pair<int, i64>>& w) {
  if (cap < 0 || cap > (1LL << 40)) return -1;
  i128 lower = 0;
  i128 loads[MAXN];
  for (int i = 0; i < P.N; i++) loads[i] = 0;
  int prev = -1;
  for (const auto& pr : w) {
    int r = pr.first;
    i64 wt = pr.second;
    if (r <= prev || r >= P.R || wt < 0 || wt > (1LL << 40)) return -1;  // rows distinct and increasing
    prev = r;
    int d = P.dem[r] - popand(P.mask[r], M);
    if (d > 0) lower += (i128)wt * d;
    for (int t = P.rstart[r]; t < P.rstart[r + 1]; t++) loads[P.ridx[t]] += wt;
  }
  i128 excess = 0;
  for (int i = 0; i < P.N; i++)
    if (!M.test(i) && !O.test(i) && loads[i] > cap) excess += loads[i] - cap;
  return lower - (i128)cap * (P.budget - M.count()) - excess;
}

static bool verifyWitness(const Problem& P, const Mask& H) {
  if (H.count() > P.budget || H.test(0)) return false;
  for (int r = 0; r < P.R; r++)
    if (popand(P.mask[r], H) < P.dem[r]) return false;
  return true;
}

// ------------------------------------------------------------------ certificate storage
static inline void putVar(std::vector<uint8_t>& a, uint64_t x) {
  while (x >= 128) { a.push_back((uint8_t)(x | 128)); x >>= 7; }
  a.push_back((uint8_t)x);
}
static inline uint64_t getVar(const uint8_t*& p) {
  uint64_t x = 0; int s = 0;
  while (*p & 128) { x |= (uint64_t)(*p++ & 127) << s; s += 7; }
  x |= (uint64_t)(*p++) << s;
  return x;
}
struct CertStore {
  std::vector<uint8_t> arena;
  std::vector<size_t> off;
  int add(i64 cap, const std::vector<std::pair<int, i64>>& w) {
    off.push_back(arena.size());
    putVar(arena, (uint64_t)cap); putVar(arena, w.size());
    int prev = 0;
    for (const auto& pr : w) { putVar(arena, (uint64_t)(pr.first - prev)); prev = pr.first; putVar(arena, (uint64_t)pr.second); }
    return (int)off.size() - 1;
  }
  void get(int id, i64& cap, std::vector<std::pair<int, i64>>& w) const {
    const uint8_t* p = arena.data() + off[id];
    cap = (i64)getVar(p);
    size_t k = getVar(p);
    w.resize(k);
    int prev = 0;
    for (size_t t = 0; t < k; t++) { prev += (int)getVar(p); w[t].first = prev; w[t].second = (i64)getVar(p); }
  }
  void clear() { arena.clear(); off.clear(); }
};
struct NodeRec { int a, b, c; };  // a>=0 branch(vertex a, zero b, one c); -1 weighted(cert b); -2 over_budget; -3 context b; -4 pending

struct Cert {
  i64 cap = 0;
  std::vector<std::pair<int, i64>> w;   // (row, weight), rows increasing
  std::vector<std::pair<int, i64>> ex;  // (state, load - cap) where positive
  std::vector<i64> load;                // dense loads
  i64 maxEx = 0;
  int id = -1;                          // index in the tree's CertStore once it has been used as a leaf
};

// ------------------------------------------------------------------ options, statistics
struct Opt {
  int ktop = 200, dtop = 8, kmid = 4, dmid = 12, klow = 2, rel = 8;  // candidates verified per node, by number of fixed states
  int poolSize = 48, useAnc = 1, cutoff = 1, sbIter = 100, maxIter = 20000, refac = 200;
  int deadpick = 1;                      // slice rule: a strong-branching candidate with a dead child is taken at once
  int known = 0;                         // slice rule: 1 = a child closed by a known vector (pool/ancestor) counts as dead
  int forced = 1;                        // slice rule: branch on a forced row (rem == avail > 0) before any LP (pbb_strong)
  int stdFallback = 1;                   // slice rule: if phi's dual gives no leaf at a dead node, solve the standard LP
  int selfcheck = 0;
  int fullp = 8, sek = 8, candMax = 64;  // pricing: full pass period, steepest-edge shortlist, candidate list size
  int witnessContinue = 0;               // 0: stop at the first witness (as pbb_strong.py); 1: leave that context open, go on
  int cold = 0;                          // 1: measurement only, solve every node LP from the slack basis (no warm start)
  int adaptive = 1;                      // 1: verify candidates by strong branching until the best verified one beats the
  double sbslack = 1.0;                  //    next estimate (times sbslack); 0: classical reliability branching (--rel)
  double timeLimit = 0;
  i64 maxCtxNodes = 40000000;
};
struct Stats {
  i64 nodes = 0, over = 0, rowLeaves = 0, poolLeaves = 0, ancLeaves = 0, cachedLeaves = 0, lpLeaves = 0, infLeaves = 0;
  i64 lps = 0, nodeLps = 0, trials = 0, iters = 0, refac = 0, resets = 0;
  i64 certFail = 0, rayFail = 0, iterLimit = 0, intNoWit = 0, bothClosed = 0, fullPasses = 0;
  i64 forcedBr = 0, deadPicks = 0, knownPicks = 0, phiLeaves = 0, stdTried = 0, stdLeaves = 0, completions = 0;
  void add(const Stats& o) {
    fullPasses += o.fullPasses;
    forcedBr += o.forcedBr; deadPicks += o.deadPicks; knownPicks += o.knownPicks; phiLeaves += o.phiLeaves;
    stdTried += o.stdTried; stdLeaves += o.stdLeaves; completions += o.completions;
    nodes += o.nodes; over += o.over; rowLeaves += o.rowLeaves; poolLeaves += o.poolLeaves; ancLeaves += o.ancLeaves;
    cachedLeaves += o.cachedLeaves; lpLeaves += o.lpLeaves; infLeaves += o.infLeaves; lps += o.lps; nodeLps += o.nodeLps;
    trials += o.trials; iters += o.iters; refac += o.refac; resets += o.resets; certFail += o.certFail; rayFail += o.rayFail;
    iterLimit += o.iterLimit; intNoWit += o.intNoWit; bothClosed += o.bothClosed;
  }
};

static std::atomic<bool> gStop(false);
static std::atomic<i64> gNodes(0);
static double gDeadline = 0;

struct StopEx {};
struct WitnessEx {};
struct TooBigEx {};

static const double TOLP = 1e-7;    // primal feasibility
static const double TOLD = 1e-9;    // dual feasibility (Harris)
static const double PIVTOL = 1e-7;  // smallest pivot
static const double TOLI = 1e-7;    // integrality
enum { ST_OPT = 0, ST_INFEAS = 1, ST_CUT = 2, ST_LIMIT = 3 };

static const i64 CAPS[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 24, 28, 30, 32, 36, 40, 42, 48, 56, 60,
                           64, 72, 84, 90, 100, 120, 128, 168, 180, 240, 256, 360, 420, 504, 720, 840, 1000, 1260, 1680,
                           2520, 5040, 10000, 27720, 100000, 1000000, 10000000};
static const int NCAPS = sizeof(CAPS) / sizeof(CAPS[0]);

struct LPSlot {
  std::vector<double> Binv;
  int cons[MAXN];
  double lam[MAXN];
  uint8_t up[MAXN];
  int nUpd = 0;
  uint64_t stamp = 0;
};

struct Decision {
  int kind = 2;            // 0 over_budget, 1 weighted leaf, 2 branch, 3 witness
  int certId = -1;
  int var = -1, c0 = -1, c1 = -1;  // branch variable; cert ids of children already known to be leaves
  double g = 0, hv = 0;
  bool lpOpt = false, slotSaved = false, ancPushed = false;
  bool tv[2] = {false, false};  // the LP state at the end of the strong-branching trial of child b is kept
};

// ------------------------------------------------------------------ worker: state, LP, search
struct Worker {
  const Problem& P;
  const Opt& opt;
  int n, R, stride;
  // --- node state (incremental)
  Mask M, O;
  int nM = 0;
  std::vector<int16_t> rem, avail;  // rem[r] = demand - |support & missing|, avail[r] = |support & free|
  // --- LP: dual simplex in "row basis" form.  The basis is a set of n active constraints: bound
  // constraints of nonbasic states and tight rows.  Binv[j*stride+p] is the inverse of the matrix
  // whose p-th row is the normal of the p-th active constraint.
  double* Binv = nullptr;
  int cons[MAXN], posVar[MAXN];
  std::vector<int> posRow;
  double lam[MAXN], lo[MAXN], hi[MAXN], beta[MAXN], h[MAXN], alpha[MAXN + 8];
  double costStd[MAXN], costPhi[MAXN];
  double* cost = costStd;
  int mode = 0;          // 0: standard LP (min sum h, all rows); 1: score LP phi of the slice (see Problem)
  int SIDE = 0;          // row index of the side constraint h(F) <= t in the LP (= R)
  double alphaS = 0;     // multiplier of the side constraint in the last extractDual() / Farkas ray
  LPSlot modeSave;       // basis of the score LP while the standard LP is solved as a fallback
  uint8_t up[MAXN];
  int nUpd = 0;
  uint64_t stamp = 0, stampCounter = 0;
  std::vector<double> viol, work;
  bool needRefac = false;
  std::vector<int> cand;       // rows violated at the last full pricing pass (hints, revalidated each time)
  std::vector<double> candV;
  int sinceFull = 0;
  double abuf[8][MAXN + 8];
  std::vector<std::unique_ptr<LPSlot>> slots;
  std::vector<std::unique_ptr<LPSlot>> tslots;  // 4 per depth: trial end states, [best0, best1, cur0, cur1]
  LPSlot* trialSave = nullptr;                  // where trial() stores the end state of an open child
  bool trialSaved = false;
  // --- dual solution of the last extractDual()
  std::vector<std::pair<int, double>> ys;
  double dload[MAXN];
  double gBound = 0;
  Cert lastCert;
  // --- certificate pool and ancestor vectors
  std::vector<std::unique_ptr<Cert>> pool;
  std::vector<i64> poolM, ancM;
  std::vector<Cert*> anc;
  std::vector<std::unique_ptr<Cert>> ancStore;
  // --- pseudo-costs
  double psum[2][MAXN];
  int pcnt[2][MAXN];
  // --- tree under construction
  std::vector<NodeRec> nodes;
  CertStore store;
  Stats st;
  std::vector<int> witness;

  Worker(const Problem& p, const Opt& o) : P(p), opt(o), n(p.N), R(p.R), stride(p.stride) {
    Binv = (double*)aligned_alloc(64, sizeof(double) * (size_t)stride * MAXN);
    posRow.assign(R + 1, -1);
    viol.assign(R + 8, 0.0);
    work.assign((size_t)2 * MAXN * MAXN, 0.0);
    slots.resize(MAXN + 4);
    tslots.resize(4 * (MAXN + 4));
    ancStore.resize(MAXN + 4);
    for (auto& a : ancStore) a.reset(new Cert());
    SIDE = R;
    // deterministic cost perturbation 1 + 1e-7*(1+u_j), u_j in [0,1): breaks ties in the ratio test
    uint64_t x = 0x9E3779B97F4A7C15ULL;
    for (int j = 0; j < MAXN; j++) {
      x ^= x << 13; x ^= x >> 7; x ^= x << 17;
      double pert = 1e-7 * (1.0 + (double)(x >> 11) / 9007199254740992.0);
      costStd[j] = 1.0 + pert;
      costPhi[j] = (j < n && P.slice && P.Lm.test(j) ? 1.0 : 0.0) + pert;
    }
    mode = P.slice ? 1 : 0;
    cost = mode ? costPhi : costStd;
    for (int d = 0; d < 2; d++) for (int j = 0; j < MAXN; j++) { psum[d][j] = 0; pcnt[d][j] = 0; }
    for (int p = 0; p < MAXN; p++) cons[p] = p;  // so that lpReset can clear posRow
    resetState();
    lpReset();
  }
  ~Worker() { free(Binv); }

  // ---------------- state
  inline bool isFree(int i) const { return !M.test(i) && !O.test(i); }
  void resetState() {
    M = Mask(); O = Mask(); nM = 0;
    rem.assign(R + 8, 0); avail.assign(R + 8, 0);
    for (int r = 0; r < R; r++) { rem[r] = (int16_t)P.dem[r]; avail[r] = (int16_t)P.rsz[r]; }
  }
  inline void fix(int v, int missing) {
    const int* c = &P.cidx[P.cstart[v]];
    int k = P.cstart[v + 1] - P.cstart[v];
    if (missing) { M.set(v); nM++; for (int t = 0; t < k; t++) { rem[c[t]]--; avail[c[t]]--; } }
    else { O.set(v); for (int t = 0; t < k; t++) avail[c[t]]--; }
  }
  inline void unfix(int v, int missing) {
    const int* c = &P.cidx[P.cstart[v]];
    int k = P.cstart[v + 1] - P.cstart[v];
    if (missing) { M.clr(v); nM--; for (int t = 0; t < k; t++) { rem[c[t]]++; avail[c[t]]++; } }
    else { O.clr(v); for (int t = 0; t < k; t++) avail[c[t]]++; }
  }
  void setState(const Mask& m, const Mask& o) {
    resetState();
    for (int i = 0; i < n; i++) { if (o.test(i)) fix(i, 0); else if (m.test(i)) fix(i, 1); }
  }
  void selfCheck() const {
    for (int r = 0; r < R; r++) {
      int rm = P.dem[r] - popand(P.mask[r], M);
      Mask fr; for (int i = 0; i < NW; i++) fr.w[i] = P.mask[r].w[i] & ~M.w[i] & ~O.w[i];
      if (rm != rem[r] || fr.count() != avail[r]) fatal("selfcheck: incremental row counts are wrong");
    }
    if (nM != M.count()) fatal("selfcheck: nM");
  }

  // ---------------- LP basics
  inline double* brow(int j) { return Binv + (size_t)j * stride; }
  void lpReset() {  // identity basis: every state nonbasic at its lower bound (always dual feasible)
    for (int p = 0; p < n; p++) if (cons[p] >= n) posRow[cons[p] - n] = -1;
    memset(Binv, 0, sizeof(double) * (size_t)stride * n);
    for (int j = 0; j < n; j++) { cons[j] = j; posVar[j] = j; lam[j] = cost[j]; up[j] = 0; brow(j)[j] = 1.0; }
    nUpd = 0; stamp = ++stampCounter; st.resets++;
  }
  void lpSave(LPSlot& s) {
    if (s.Binv.empty()) s.Binv.resize((size_t)stride * n);
    memcpy(s.Binv.data(), Binv, sizeof(double) * (size_t)stride * n);
    memcpy(s.cons, cons, sizeof(int) * n); memcpy(s.lam, lam, sizeof(double) * n); memcpy(s.up, up, n);
    s.nUpd = nUpd; s.stamp = stamp;
  }
  void lpRestore(const LPSlot& s) {
    for (int p = 0; p < n; p++) if (cons[p] >= n) posRow[cons[p] - n] = -1;
    memcpy(Binv, s.Binv.data(), sizeof(double) * (size_t)stride * n);
    memcpy(cons, s.cons, sizeof(int) * n); memcpy(lam, s.lam, sizeof(double) * n); memcpy(up, s.up, n);
    for (int j = 0; j < n; j++) posVar[j] = -1;
    for (int p = 0; p < n; p++) { int c = cons[p]; if (c < n) posVar[c] = p; else posRow[c - n] = p; }
    nUpd = s.nUpd; stamp = s.stamp;
  }
  LPSlot& slot(int depth) {
    if (!slots[depth]) slots[depth].reset(new LPSlot());
    return *slots[depth];
  }
  LPSlot& tslot(int depth, int k) {
    if (!tslots[4 * depth + k]) tslots[4 * depth + k].reset(new LPSlot());
    return *tslots[4 * depth + k];
  }
  inline bool phiExcluded(int r) const { return mode == 1 && (r == P.capF || r == P.capL); }
  inline double cutThr() const { return mode == 1 ? (double)P.sliceB : (double)P.budget; }
  void computeBetaH() {
    for (int p = 0; p < n; p++) {
      int c = cons[p];
      beta[p] = c < n ? (up[c] ? hi[c] : lo[c]) : (c - n == SIDE ? -(double)P.sliceT : (double)P.dem[c - n]);
    }
    for (int j = 0; j < n; j++) {
      int pj = posVar[j];
      if (pj >= 0) { h[j] = beta[pj]; continue; }
      const double* row = brow(j);
      double s = 0;
#pragma omp simd reduction(+ : s)
      for (int p = 0; p < n; p++) s += row[p] * beta[p];
      h[j] = s;
    }
  }
  void lpSetBounds() {
    for (int j = 0; j < n; j++) {
      if (M.test(j)) lo[j] = hi[j] = 1.0;
      else if (O.test(j)) lo[j] = hi[j] = 0.0;
      else { lo[j] = 0.0; hi[j] = 1.0; }
      int pj = posVar[j];
      if (pj >= 0) up[j] = lam[pj] < 0;
    }
    computeBetaH();
  }
  // Recompute the inverse from the basis.  Nonbasic states contribute unit rows, so only the
  // k x k block (tight rows) x (floating states) is inverted.
  bool refactor() {
    st.refac++;
    int F[MAXN], RP[MAXN], colOf[MAXN];
    int k = 0, kr = 0;
    for (int j = 0; j < n; j++) { colOf[j] = -1; if (posVar[j] < 0) { colOf[j] = k; F[k++] = j; } }
    for (int p = 0; p < n; p++) if (cons[p] >= n) RP[kr++] = p;
    if (kr != k) return false;
    int w2 = 2 * k;
    double* W = work.data();
    std::fill(W, W + (size_t)k * w2, 0.0);
    for (int i = 0; i < k; i++) {
      int r = cons[RP[i]] - n;
      if (r == SIDE) { for (int j : P.Fidx) { int c = colOf[j]; if (c >= 0) W[(size_t)i * w2 + c] = -1.0; } }
      else for (int t = P.rstart[r]; t < P.rstart[r + 1]; t++) { int c = colOf[P.ridx[t]]; if (c >= 0) W[(size_t)i * w2 + c] = 1.0; }
      W[(size_t)i * w2 + k + i] = 1.0;
    }
    for (int c = 0; c < k; c++) {
      int piv = -1; double best = 1e-9;
      for (int i = c; i < k; i++) { double a = std::fabs(W[(size_t)i * w2 + c]); if (a > best) { best = a; piv = i; } }
      if (piv < 0) return false;
      if (piv != c) for (int t = 0; t < w2; t++) std::swap(W[(size_t)piv * w2 + t], W[(size_t)c * w2 + t]);
      double* rc = W + (size_t)c * w2;
      double inv = 1.0 / rc[c];
      for (int t = 0; t < w2; t++) rc[t] *= inv;
      for (int i = 0; i < k; i++) {
        if (i == c) continue;
        double* ri = W + (size_t)i * w2;
        double f = ri[c];
        if (f == 0.0) continue;
        for (int t = 0; t < w2; t++) ri[t] -= f * rc[t];
      }
    }
    memset(Binv, 0, sizeof(double) * (size_t)stride * n);
    for (int j = 0; j < n; j++) if (posVar[j] >= 0) brow(j)[posVar[j]] = 1.0;
    for (int c = 0; c < k; c++) { double* row = brow(F[c]); for (int i = 0; i < k; i++) row[RP[i]] = W[(size_t)c * w2 + k + i]; }
    for (int i = 0; i < k; i++) {
      int r = cons[RP[i]] - n;
      if (r == SIDE) {  // coefficient -1 on F
        for (int j : P.Fidx) {
          int pj = posVar[j];
          if (pj < 0) continue;
          for (int c = 0; c < k; c++) brow(F[c])[pj] += W[(size_t)c * w2 + k + i];
        }
        continue;
      }
      for (int t = P.rstart[r]; t < P.rstart[r + 1]; t++) {
        int pj = posVar[P.ridx[t]];
        if (pj < 0) continue;
        for (int c = 0; c < k; c++) brow(F[c])[pj] -= W[(size_t)c * w2 + k + i];
      }
    }
    for (int p = 0; p < n; p++) lam[p] = 0;
    for (int j = 0; j < n; j++) { const double* row = brow(j); double cj = cost[j]; for (int p = 0; p < n; p++) lam[p] += cj * row[p]; }
    for (int p = 0; p < n; p++) if (cons[p] >= n && lam[p] < -1e-6) return false;
    nUpd = 0; stamp = ++stampCounter;
    return true;
  }
  // Full pricing pass: violation of every row at the current point, column by column.
  void fullPass() {
    st.fullPasses++;
    double* v = viol.data();
    const int16_t* rm = rem.data();
    for (int r = 0; r < R; r++) v[r] = rm[r];
    for (int j = 0; j < n; j++) {
      double x = h[j];
      if (M.test(j)) {
        if (x != 1.0) { double dlt = 1.0 - x; for (int t = P.cstart[j]; t < P.cstart[j + 1]; t++) v[P.cidx[t]] += dlt; }
      } else if (x != 0.0) {
        for (int t = P.cstart[j]; t < P.cstart[j + 1]; t++) v[P.cidx[t]] -= x;
      }
    }
    if (mode == 1) {  // side constraint -h(F) >= -t: violation h(F) - t
      double s = -(double)P.sliceT;
      for (int j : P.Fidx) s += h[j];
      v[SIDE] = s;
    } else v[SIDE] = 0.0;
    for (int p = 0; p < n; p++) if (cons[p] >= n && std::fabs(v[cons[p] - n]) > 1e-6) needRefac = true;
    cand.clear(); candV.clear();
    for (int r = 0; r < R; r++) if (v[r] > TOLP && posRow[r] < 0 && !phiExcluded(r)) { cand.push_back(r); candV.push_back(v[r]); }
    if (mode == 1 && v[SIDE] > TOLP && posRow[SIDE] < 0) { cand.push_back(SIDE); candV.push_back(v[SIDE]); }
    if ((int)cand.size() > opt.candMax) {
      std::vector<std::pair<double, int>> tmp(cand.size());
      for (size_t i = 0; i < cand.size(); i++) tmp[i] = {-candV[i] * P.rnorm[cand[i]], cand[i]};
      std::nth_element(tmp.begin(), tmp.begin() + opt.candMax, tmp.end());
      cand.resize(opt.candMax); candV.resize(opt.candMax);
      for (int i = 0; i < opt.candMax; i++) { cand[i] = tmp[i].second; candV[i] = v[tmp[i].second]; }
    }
  }
  void computeAlpha(int q, double* a) {  // (normal of constraint q) expressed in the basis rows
    if (q - n == SIDE) {
      for (int p = 0; p < n; p++) a[p] = 0;
      for (int j : P.Fidx) {
        int pj = posVar[j];
        if (pj >= 0) { a[pj] -= 1.0; continue; }
        const double* row = brow(j);
        for (int p = 0; p < n; p++) a[p] -= row[p];
      }
      return;
    }
    if (q >= n) {
      for (int p = 0; p < n; p++) a[p] = 0;
      int r = q - n;
      for (int t = P.rstart[r]; t < P.rstart[r + 1]; t++) {
        int j = P.ridx[t], pj = posVar[j];
        if (pj >= 0) { a[pj] += 1.0; continue; }
        const double* row = brow(j);
        for (int p = 0; p < n; p++) a[p] += row[p];
      }
    } else {
      const double* row = brow(q);
      for (int p = 0; p < n; p++) a[p] = row[p];
    }
  }
  // Entering constraint: candidate rows (revalidated) and violated bounds of floating states; a full
  // pass every opt.fullp iterations and always before optimality is declared.  Among the opt.sek
  // largest scaled violations the one with the best steepest-edge ratio delta^2/(1+|alpha|^2) is
  // taken.  Fills alpha[] for the chosen constraint.  Returns -1 if the point is primal feasible.
  int price(int& sigma, double& delta) {
    int nv = 0;
    for (size_t i = 0; i < cand.size(); i++) {
      int r = cand[i];
      if (posRow[r] >= 0) continue;
      double a;
      if (r == SIDE) {
        if (mode != 1) continue;
        a = -(double)P.sliceT;
        for (int j : P.Fidx) a += h[j];
      } else {
        if (phiExcluded(r)) continue;
        a = P.dem[r];
        for (int t = P.rstart[r]; t < P.rstart[r + 1]; t++) a -= h[P.ridx[t]];
      }
      if (a > TOLP) { cand[nv] = r; candV[nv] = a; nv++; }
    }
    cand.resize(nv); candV.resize(nv);
    struct C { double score, delta; int q, sigma; };
    C top[8];
    int nt = 0, T = std::max(1, std::min(8, opt.sek));
    auto offer = [&](double score, double dl, int q, int sg) {
      if (nt < T) { top[nt++] = {score, dl, q, sg}; return; }
      int w = 0;
      for (int t = 1; t < T; t++) if (top[t].score < top[w].score) w = t;
      if (score > top[w].score) top[w] = {score, dl, q, sg};
    };
    int nbv = 0;
    for (int j = 0; j < n; j++) {
      if (posVar[j] >= 0) continue;
      if (h[j] < lo[j] - TOLP) { offer(lo[j] - h[j], lo[j] - h[j], j, 1); nbv++; }
      else if (h[j] > hi[j] + TOLP) { offer(h[j] - hi[j], h[j] - hi[j], j, -1); nbv++; }
    }
    needRefac = false;
    if (nv + nbv == 0 || sinceFull >= opt.fullp || (nv < 2 && sinceFull >= 2)) {
      fullPass();
      sinceFull = 0;
      nv = (int)cand.size();
    }
    sinceFull++;
    for (int i = 0; i < nv; i++) offer(candV[i] * P.rnorm[cand[i]], candV[i], n + cand[i], 1);
    if (nt == 0) return -1;
    int bt = 0;
    if (nt > 1) {
      double bestScore = -1;
      for (int t = 0; t < nt; t++) {
        double* a = abuf[t];
        computeAlpha(top[t].q, a);
        double nrm = 1.0;
        for (int p = 0; p < n; p++) nrm += a[p] * a[p];
        double sc = top[t].delta * top[t].delta / nrm;
        if (sc > bestScore) { bestScore = sc; bt = t; }
      }
      memcpy(alpha, abuf[bt], sizeof(double) * n);
    } else computeAlpha(top[0].q, alpha);
    sigma = top[bt].sigma; delta = top[bt].delta;
    return top[bt].q;
  }
  // Bounded dual simplex from the current basis for the current node state.  With cutoff, stops as
  // soon as a dual vector with an exactly positive integer margin is found (lastCert).
  int lpSolve(bool cutoff, int maxIter) {
    st.lps++;
    lpSetBounds();
    sinceFull = opt.fullp;
    const double thr = cutThr();
    double nextTry = thr + 1e-6;
    int refTries = 0;
    struct BP { double theta, absa; int p; bool isRow; };
    BP bp[MAXN];
    for (int it = 0;; it++) {
      if (cutoff) {
        double zp = 0;
        for (int p = 0; p < n; p++) zp += lam[p] * beta[p];
        if (zp > nextTry) {
          extractDual();
          if (gBound > thr + 1e-7 && makeCert(lastCert)) return ST_CUT;
          nextTry = std::max(zp, thr) + 0.02;
        }
      }
      int sigma = 1; double delta = 0;
      int q = price(sigma, delta);
      if (needRefac && refTries < 3) {
        refTries++;
        if (!refactor()) lpReset();
        lpSetBounds();
        continue;
      }
      if (q < 0) return ST_OPT;
      if (it >= maxIter) return ST_LIMIT;
      st.iters++;
      // ratio test with bound flipping: lam_p(theta) = lam_p - theta*sigma*alpha_p
      int nb = 0;
      for (int p = 0; p < n; p++) {
        double a = sigma * alpha[p];
        if (std::fabs(a) <= PIVTOL) continue;
        int c = cons[p];
        if (c >= n) { if (a > 0) bp[nb++] = {std::max(lam[p], 0.0) / a, a, p, true}; }
        else {
          if (lo[c] == hi[c]) continue;  // fixed state: its multiplier is free
          if (!up[c]) { if (a > 0) bp[nb++] = {std::max(lam[p], 0.0) / a, a, p, false}; }
          else if (a < 0) bp[nb++] = {std::max(-lam[p], 0.0) / (-a), -a, p, false};
        }
      }
      std::sort(bp, bp + nb, [](const BP& x, const BP& y) { return x.theta < y.theta || (x.theta == y.theta && x.absa > y.absa); });
      double slope = delta;
      int k = 0;
      for (; k < nb; k++) {
        if (bp[k].isRow) break;
        if (slope - bp[k].absa > 1e-9) { slope -= bp[k].absa; continue; }  // flip this boxed state and go on
        break;
      }
      if (k == nb) {  // dual unbounded: the node LP is infeasible; Farkas weights on rows
        ys.clear();
        if (q >= n) ys.push_back({q - n, 1.0});
        for (int p = 0; p < n; p++) if (cons[p] >= n) { double yv = -sigma * alpha[p]; if (yv > 1e-9) ys.push_back({cons[p] - n, yv}); }
        std::sort(ys.begin(), ys.end());
        return ST_INFEAS;
      }
      double thMax = 1e300;
      for (int i = k; i < nb; i++) { double t = bp[i].theta + TOLD / bp[i].absa; if (t < thMax) thMax = t; }
      int sel = k;
      for (int i = k; i < nb; i++) if (bp[i].theta <= thMax && bp[i].absa > bp[sel].absa) sel = i;
      int L = bp[sel].p;
      double theta = bp[sel].theta, aL = alpha[L], stp = sigma * theta;
      for (int p = 0; p < n; p++) lam[p] -= stp * alpha[p];
      lam[L] = stp;
      for (int t = 0; t < k; t++) up[cons[bp[t].p]] ^= 1;
      int cold = cons[L];
      if (cold < n) posVar[cold] = -1; else posRow[cold - n] = -1;
      double inv = 1.0 / aL;
      for (int j = 0; j < n; j++) {
        double* row = brow(j);
        double f = row[L];
        if (f == 0.0) continue;
        f *= inv;
        for (int p = 0; p < n; p++) row[p] -= f * alpha[p];
        row[L] = f;
      }
      cons[L] = q;
      if (q < n) {
        posVar[q] = L; up[q] = sigma < 0;
        double* row = brow(q);
        for (int p = 0; p < n; p++) row[p] = 0.0;
        row[L] = 1.0;
      } else posRow[q - n] = L;
      stamp = ++stampCounter;
      if (++nUpd >= opt.refac) { if (!refactor()) lpReset(); lpSetBounds(); }
      else computeBetaH();
    }
  }
  // Dual solution without the cost perturbation: row multipliers y >= 0, loads, and the dual bound
  // g = sum y*rem + |missing| - sum over free of max(0, load-1)  (a valid lower bound for any y >= 0).
  //
  // Score LP (mode 1): costs c = 1 on Lo, 0 on F; side multiplier alpha >= 0 on h(F) <= t.  For any y >= 0,
  // alpha >= 0 the Lagrangian bound is
  //   g_phi = sum y*rem+ + |M & Lo| + alpha*(|M & F| - t) - sum over free of max(0, load_i - c'_i),
  // c'_i = alpha on F and 1 on Lo.  It converts into a dual vector of the standard LP (see stdFromPhi) whose
  // bound exceeds the budget exactly when g_phi exceeds b = budget - t.
  void extractDual() {
    double lam0[MAXN];
    for (int p = 0; p < n; p++) lam0[p] = 0;
    for (int j = 0; j < n; j++) {
      double cj = mode == 1 ? (P.Lm.test(j) ? 1.0 : 0.0) : 1.0;
      if (cj == 0.0) continue;
      int pj = posVar[j];
      if (pj >= 0) { lam0[pj] += cj; continue; }
      const double* row = brow(j);
      for (int p = 0; p < n; p++) lam0[p] += row[p];
    }
    ys.clear();
    alphaS = 0;
    for (int p = 0; p < n; p++) {
      if (cons[p] < n || lam0[p] <= 1e-9) continue;
      if (cons[p] - n == SIDE) alphaS = lam0[p];
      else ys.push_back({cons[p] - n, lam0[p]});
    }
    std::sort(ys.begin(), ys.end());
    for (int i = 0; i < n; i++) dload[i] = 0;
    double g = 0;
    if (mode == 1) {
      int mF = popand(M, P.Fm);
      g = (nM - mF) + alphaS * (mF - P.sliceT);
    } else g = nM;
    for (const auto& pr : ys) {
      int r = pr.first;
      if (rem[r] > 0) g += pr.second * rem[r];
      for (int t = P.rstart[r]; t < P.rstart[r + 1]; t++) dload[P.ridx[t]] += pr.second;
    }
    if (mode == 1) {
      for (int i = 0; i < n; i++) {
        if (!isFree(i)) continue;
        double ci = P.Fm.test(i) ? alphaS : 1.0;
        if (dload[i] > ci) g -= dload[i] - ci;
      }
    } else
      for (int i = 0; i < n; i++) if (isFree(i) && dload[i] > 1.0) g -= dload[i] - 1.0;
    gBound = g;
  }
  // The standard-LP dual vector of a score-LP dual (y, alpha) (LO33N §3; proof in the README):
  //   alpha <= 1: y + (1 - alpha) on capF;    alpha > 1: y/alpha + (1 - 1/alpha) on capL.
  // Its standard bound is >= g_phi + t (resp. budget + (g_phi - b)/alpha).  For a Farkas ray of the score LP
  // (ray = true) with alpha > 0 the vector is y/alpha + 1 on capL (bound >= budget + g0/alpha).
  void stdFromPhi(const std::vector<std::pair<int, double>>& y, double alpha, bool ray, std::vector<std::pair<int, double>>& out) const {
    out.clear();
    if (ray) {
      for (const auto& pr : y) out.push_back({pr.first, pr.second / alpha});
      out.push_back({P.capL, 1.0});
    } else if (alpha <= 1.0) {
      out = y;
      if (1.0 - alpha > 1e-12) out.push_back({P.capF, 1.0 - alpha});
    } else {
      for (const auto& pr : y) out.push_back({pr.first, pr.second / alpha});
      out.push_back({P.capL, 1.0 - 1.0 / alpha});
    }
    std::sort(out.begin(), out.end());
  }

  // ---------------- certificates
  inline i64 certMargin(const Cert& c) const {  // exact (64-bit is enough: weights <= 1e12, <= 200 rows)
    i64 lower = 0;
    for (const auto& pr : c.w) { int x = rem[pr.first]; if (x > 0) lower += pr.second * x; }
    i64 exs = 0;
    for (const auto& e : c.ex) if (isFree(e.first)) exs += e.second;
    return lower - c.cap * (i64)(P.budget - nM) - exs;
  }
  bool buildCert(const std::vector<std::pair<int, double>>& y, double scale, i64 cap, Cert& c) {
    c.w.clear(); c.ex.clear(); c.cap = cap; c.id = -1; c.maxEx = 0;
    for (const auto& pr : y) {
      if (rem[pr.first] <= 0) continue;  // a satisfied row adds load and no bound
      double x = scale * pr.second;
      if (!(x < 1e12)) return false;
      i64 w = llround(x);
      if (w > 0) c.w.push_back({pr.first, w});
    }
    if (c.w.empty() || c.w.size() > 250) return false;
    c.load.assign(n, 0);
    for (const auto& pr : c.w) { int r = pr.first; for (int t = P.rstart[r]; t < P.rstart[r + 1]; t++) c.load[P.ridx[t]] += pr.second; }
    for (int i = 0; i < n; i++) if (c.load[i] > cap) { c.ex.push_back({i, c.load[i] - cap}); c.maxEx = std::max(c.maxEx, c.load[i] - cap); }
    return true;
  }
  static bool exactAt(const std::vector<std::pair<int, double>>& y, i64 cap) {
    for (const auto& pr : y) { double x = cap * pr.second; if (std::fabs(x - std::nearbyint(x)) > 1e-6) return false; }
    return true;
  }
  // Integer weights for the dual vector ys at the current node: first the smallest capacity that
  // represents ys exactly, then the smallest capacity whose rounding still has a positive margin.
  bool makeCertFrom(const std::vector<std::pair<int, double>>& y, Cert& c) {
    for (int t = 0; t < NCAPS; t++) {
      if (!exactAt(y, CAPS[t])) continue;
      if (buildCert(y, (double)CAPS[t], CAPS[t], c) && certMargin(c) > 0) return true;
      break;
    }
    for (int t = 0; t < NCAPS; t++)
      if (buildCert(y, (double)CAPS[t], CAPS[t], c) && certMargin(c) > 0) return true;
    return false;
  }
  std::vector<std::pair<int, double>> ysStd;  // scratch: converted dual vector
  bool makeCert(Cert& c) {  // from the dual of the last extractDual() (converted in mode 1)
    if (mode == 1) { stdFromPhi(ys, alphaS, false, ysStd); return makeCertFrom(ysStd, c); }
    return makeCertFrom(ys, c);
  }
  bool makeRayCertFrom(const std::vector<std::pair<int, double>>& y, Cert& c) {  // capacity 0 (infeasibility)
    static const double SC[] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 24, 30, 36, 40, 48, 60, 72, 84, 120,
                                168, 180, 240, 360, 420, 720, 840, 1260, 2520, 5040, 27720};
    for (double s : SC) if (buildCert(y, s, 0, c) && certMargin(c) > 0) return true;
    double mx = 0;
    for (const auto& pr : y) mx = std::max(mx, pr.second);
    if (mx <= 0) return false;
    static const double SC2[] = {1e3, 1e4, 1e5, 1e6, 1e7, 1e9};
    for (double s : SC2) if (buildCert(y, s / mx, 0, c) && certMargin(c) > 0) return true;
    return false;
  }
  bool makeRayCert(Cert& c) {  // ys holds a Farkas ray of the current LP
    if (mode != 1) return makeRayCertFrom(ys, c);
    double alpha = 0;
    std::vector<std::pair<int, double>> y;
    for (const auto& pr : ys) { if (pr.first == SIDE) alpha += pr.second; else y.push_back(pr); }
    if (alpha > 1e-9) {
      stdFromPhi(y, alpha, true, ysStd);
      if (makeCertFrom(ysStd, c)) return true;
    }
    return makeRayCertFrom(y, c);
  }
  // The dual vector of an open node, kept for its descendants (reduced-cost fixing in tree form).
  bool makeOpenVec(Cert& c) {
    const std::vector<std::pair<int, double>>* y = &ys;
    if (mode == 1) { stdFromPhi(ys, alphaS, false, ysStd); y = &ysStd; }
    i64 cap = 100000;
    for (int t = 0; t < NCAPS; t++) if (exactAt(*y, CAPS[t])) { cap = CAPS[t]; break; }
    return buildCert(*y, (double)cap, cap, c);
  }
  // Standard LP (min sum h over ALL rows) from the slack basis, used only when the score LP's dual gives no
  // leaf at a node it declares dead.  The score-LP basis is saved and restored.
  bool stdLeaf(Cert& c) {
    st.stdTried++;
    lpSave(modeSave);
    mode = 0; cost = costStd; cand.clear(); candV.clear();
    lpReset();
    int s = lpSolve(true, opt.maxIter);
    bool ok = false;
    if (s == ST_CUT) ok = true, c = lastCert;
    else if (s == ST_INFEAS) ok = makeRayCert(c);
    else if (s == ST_OPT) { extractDual(); ok = gBound > P.budget + 1e-7 && makeCert(c); }
    mode = 1; cost = costPhi; cand.clear(); candV.clear();
    lpRestore(modeSave);
    lpSetBounds();   // primal values h of the restored score-LP basis
    extractDual();   // and its dual (ys, alphaS, gBound) again
    if (ok) st.stdLeaves++;
    return ok;
  }
  // Authoritative acceptance of a leaf: exact margin from the masks, then store.
  int internChecked(Cert& c) {
    if (marginExact(P, M, O, c.cap, c.w) <= 0) fatal("internal error: a certificate failed the exact margin check");
    if (c.id < 0) c.id = store.add(c.cap, c.w);
    return c.id;
  }
  int cacheChild(int j, int b, Cert* c) {
    fix(j, b);
    bool ok = marginExact(P, M, O, c->cap, c->w) > 0;
    unfix(j, b);
    if (!ok) return -1;
    if (c->id < 0) c->id = store.add(c->cap, c->w);
    return c->id;
  }
  Cert* pushPool(const Cert& c) {
    pool.insert(pool.begin(), std::unique_ptr<Cert>(new Cert(c)));
    return pool[0].get();
  }
  Cert* poolCheck() {
    while ((int)pool.size() > opt.poolSize) pool.pop_back();
    ancM.resize(anc.size()); poolM.resize(pool.size());
    for (int t = (int)anc.size() - 1; t >= 0; t--) {
      i64 m = certMargin(*anc[t]);
      ancM[t] = m;
      if (m > 0) { st.ancLeaves++; return anc[t]; }
    }
    for (int t = 0; t < (int)pool.size(); t++) {
      i64 m = certMargin(*pool[t]);
      poolM[t] = m;
      if (m > 0) {
        st.poolLeaves++;
        if (t > 0) std::rotate(pool.begin(), pool.begin() + t, pool.begin() + t + 1);
        return pool[0].get();
      }
    }
    return nullptr;
  }

  // ---------------- branching
  int fallbackVar() const {
    int best = -1;
    for (int i = 0; i < n; i++) if (isFree(i) && (best < 0 || P.cdeg[i] > P.cdeg[best])) best = i;
    return best;
  }
  double trial(int depth, int j, int b, double g, double x, Cert*& nc) {
    st.trials++;
    fix(j, b);
    double GMAX = P.budget + 1 - g, gain;
    int s = lpSolve(opt.cutoff, opt.sbIter);
    if (s == ST_CUT) { nc = pushPool(lastCert); gain = GMAX; }
    else if (s == ST_INFEAS) { if (makeRayCert(lastCert)) nc = pushPool(lastCert); gain = GMAX; }
    else {
      extractDual();
      if (s == ST_OPT && gBound > P.budget + 1e-7 && makeCert(lastCert)) { nc = pushPool(lastCert); gain = GMAX; }
      else gain = std::max(0.0, std::min(gBound, (double)P.budget + 1) - g);
    }
    trialSaved = false;
    if (!nc && trialSave) { lpSave(*trialSave); trialSaved = true; }
    unfix(j, b);
    lpRestore(*slots[depth]);
    double dist = b ? 1 - x : x;
    if (dist > 1e-9) { psum[b][j] += gain / dist; pcnt[b][j]++; }
    return gain;
  }
  void select(int depth, const int* frac, int nf, double g, const double* hN, Decision& d) {
    Cert* cl[2][MAXN];
    for (int t = 0; t < nf; t++) cl[0][frac[t]] = cl[1][frac[t]] = nullptr;
    // which children are already closed by a known vector (margin m <= 0 at this node)?
    auto applyCert = [&](Cert* c, i64 m) {
      if (m > 0) return;
      i64 need = -m;
      if (need >= c->cap && need >= c->maxEx) return;
      for (int t = 0; t < nf; t++) {
        int j = frac[t];
        i64 l = c->load[j];
        if (!cl[1][j] && c->cap - l > need) cl[1][j] = c;
        if (!cl[0][j] && l - c->cap > need) cl[0][j] = c;
      }
    };
    for (int t = (int)anc.size() - 1; t >= 0; t--) applyCert(anc[t], ancM[t]);
    for (int t = 0; t < (int)pool.size() && t < (int)poolM.size(); t++) applyCert(pool[t].get(), poolM[t]);
    double GMAX = P.budget + 1 - g;
    auto finish = [&](int j) {
      d.var = j;
      d.c0 = cl[0][j] ? cacheChild(j, 0, cl[0][j]) : -1;
      d.c1 = cl[1][j] ? cacheChild(j, 1, cl[1][j]) : -1;
    };
    for (int t = 0; t < nf; t++) { int j = frac[t]; if (cl[0][j] && cl[1][j]) { st.bothClosed++; finish(j); return; } }
    double avg[2];
    for (int b = 0; b < 2; b++) {
      double s = 0; int c = 0;
      for (int j = 0; j < n; j++) if (pcnt[b][j]) { s += psum[b][j] / pcnt[b][j]; c++; }
      avg[b] = c ? s / c : 1.0;
    }
    auto est = [&](int j, int b) {
      if (cl[b][j]) return GMAX;
      double unit = pcnt[b][j] ? psum[b][j] / pcnt[b][j] : avg[b];
      return std::min(GMAX, unit * (b ? 1 - hN[j] : hN[j]));
    };
    struct Cd { double score, off; int j; };
    Cd cds[MAXN];
    for (int t = 0; t < nf; t++) {
      int j = frac[t];
      cds[t] = {std::max(est(j, 0), 1e-3) * std::max(est(j, 1), 1e-3), std::fabs(hN[j] - 0.5), j};
    }
    std::sort(cds, cds + nf, [](const Cd& a, const Cd& b) {
      if (a.score != b.score) return a.score > b.score;
      if (a.off != b.off) return a.off < b.off;
      return a.j < b.j;
    });
    int nfix = nM + O.count();
    bool top = nfix < opt.dtop;
    int K = top ? opt.ktop : (nfix < opt.dmid ? opt.kmid : opt.klow);
    int nsb = 0, best = -1;
    double bestScore = -1;
    if (opt.adaptive && K > 0) {
      // Candidates in order of estimated score; each one is verified by solving both child LPs, and
      // the search stops when the best verified score is at least the next estimate.  The end states
      // of the chosen candidate's trials are kept, so its children are not solved a second time.
      bool bestValid[2] = {false, false};
      int kb = 0;  // tslot(depth, kb + b) holds the best candidate's states, tslot(depth, 2 - kb + b) is scratch
      for (int t = 0; t < nf; t++) {
        int j = cds[t].j;
        if (best >= 0) {  // near the root (fewer than dtop fixed states) always verify K candidates
          double e = std::max(est(j, 0), 1e-3) * std::max(est(j, 1), 1e-3);
          if (nsb >= K || (!top && bestScore >= opt.sbslack * e)) break;
        }
        double gn[2];
        bool curValid[2] = {false, false};
        for (int b = 0; b < 2; b++) {
          if (cl[b][j]) { gn[b] = GMAX; continue; }
          if (!d.slotSaved) { lpSave(slot(depth)); d.slotSaved = true; }
          Cert* nc = nullptr;
          trialSave = &tslot(depth, 2 - kb + b);
          gn[b] = trial(depth, j, b, g, hN[j], nc);
          trialSave = nullptr;
          curValid[b] = trialSaved;
          if (nc) { cl[b][j] = nc; applyCert(nc, certMargin(*nc)); }
        }
        nsb++;
        if (cl[0][j] && cl[1][j]) { st.bothClosed++; best = j; bestValid[0] = bestValid[1] = false; break; }
        double score = std::max(gn[0], 1e-3) * std::max(gn[1], 1e-3);
        if (score > bestScore) {
          bestScore = score; best = j;
          kb = 2 - kb;
          bestValid[0] = curValid[0]; bestValid[1] = curValid[1];
        }
      }
      finish(best);
      for (int b = 0; b < 2; b++) {
        bool keep = bestValid[b] && (b ? d.c1 < 0 : d.c0 < 0);
        d.tv[b] = keep;
        if (keep && kb != 0) std::swap(tslots[4 * depth + b], tslots[4 * depth + 2 + b]);  // best states live in slots 0,1
      }
      return;
    }
    for (int t = 0; t < nf; t++) {
      int j = cds[t].j;
      bool strong = nsb < K && std::min(pcnt[0][j], pcnt[1][j]) < opt.rel;
      double gn[2];
      for (int b = 0; b < 2; b++) {
        if (cl[b][j]) { gn[b] = GMAX; continue; }
        if (!strong) { gn[b] = est(j, b); continue; }
        if (!d.slotSaved) { lpSave(slot(depth)); d.slotSaved = true; }
        Cert* nc = nullptr;
        gn[b] = trial(depth, j, b, g, hN[j], nc);
        if (nc) { cl[b][j] = nc; applyCert(nc, certMargin(*nc)); }
      }
      if (strong) nsb++;
      if (cl[0][j] && cl[1][j]) { st.bothClosed++; best = j; break; }
      double score = std::max(gn[0], 1e-3) * std::max(gn[1], 1e-3);
      if (score > bestScore) { bestScore = score; best = j; }
    }
    finish(best);
  }

  // ---------------- slice rule (LO33N pbb_fast2: strong branching on phi, dead-child pick, leaves from phi's dual)
  // One strong-branching child: the score LP with state j fixed to b.  Returns its bound (1e30 if the child is
  // dead by infeasibility or by a certificate); dead = the child's score-LP bound exceeds b_slice.
  double trialPhi(int depth, int j, int b, Cert*& nc, bool& dead) {
    st.trials++;
    fix(j, b);
    const double thr = cutThr();
    double val;
    dead = false;
    int s = lpSolve(opt.cutoff, opt.sbIter);
    if (s == ST_CUT) { nc = pushPool(lastCert); val = 1e30; dead = true; }
    else if (s == ST_INFEAS) { if (makeRayCert(lastCert)) nc = pushPool(lastCert); val = 1e30; dead = true; }
    else {
      extractDual();
      val = gBound;
      if (gBound > thr + 1e-7) { dead = true; if (makeCert(lastCert)) nc = pushPool(lastCert); }
    }
    trialSaved = false;
    if (!nc && trialSave) { lpSave(*trialSave); trialSaved = true; }
    unfix(j, b);
    lpRestore(*slots[depth]);
    return val;
  }
  void selectSlice(int depth, const int* frac, int nf, double g, const double* hN, Decision& d) {
    const double capv = cutThr() + 1.0;
    int cs[MAXN];
    for (int t = 0; t < nf; t++) cs[t] = frac[t];
    std::sort(cs, cs + nf, [&](int a, int b) {
      double da = std::fabs(hN[a] - 0.5), db = std::fabs(hN[b] - 0.5);
      if (da != db) return da < db;
      return a < b;
    });
    Cert* cl[2][MAXN];
    for (int t = 0; t < nf; t++) cl[0][cs[t]] = cl[1][cs[t]] = nullptr;
    auto finish = [&](int j) {
      d.var = j;
      d.c0 = cl[0][j] ? cacheChild(j, 0, cl[0][j]) : -1;
      d.c1 = cl[1][j] ? cacheChild(j, 1, cl[1][j]) : -1;
    };
    if (opt.known) {  // children already closed by a known vector (margin m <= 0 here, enough room to close a child)
      auto applyCert = [&](Cert* c, i64 m) {
        if (m > 0) return;
        i64 need = -m;
        if (need >= c->cap && need >= c->maxEx) return;
        for (int t = 0; t < nf; t++) {
          int j = cs[t];
          i64 l = c->load[j];
          if (!cl[1][j] && c->cap - l > need) cl[1][j] = c;
          if (!cl[0][j] && l - c->cap > need) cl[0][j] = c;
        }
      };
      for (int t = (int)anc.size() - 1; t >= 0; t--) applyCert(anc[t], ancM[t]);
      for (int t = 0; t < (int)pool.size() && t < (int)poolM.size(); t++) applyCert(pool[t].get(), poolM[t]);
      for (int t = 0; t < nf; t++) {
        int j = cs[t];
        if (!cl[0][j] && !cl[1][j]) continue;
        finish(j);
        if (d.c0 >= 0 || d.c1 >= 0) { st.knownPicks++; return; }
        cl[0][j] = cl[1][j] = nullptr;
      }
    }
    int nfix = nM + O.count();
    int K = nfix < opt.dtop ? opt.ktop : opt.klow;
    if (K > nf) K = nf;
    if (K <= 0) { finish(cs[0]); return; }
    int best = -1, kb = 0;
    double bestScore = -1;
    bool bestValid[2] = {false, false};
    for (int t = 0; t < K; t++) {
      int j = cs[t];
      double gn[2] = {1e-3, 1e-3};
      bool curValid[2] = {false, false}, deadNow = false;
      for (int b = 0; b < 2; b++) {
        if (!d.slotSaved) { lpSave(slot(depth)); d.slotSaved = true; }
        Cert* nc = nullptr;
        bool dead = false;
        trialSave = &tslot(depth, 2 - kb + b);
        double val = trialPhi(depth, j, b, nc, dead);
        trialSave = nullptr;
        curValid[b] = trialSaved;
        if (nc) cl[b][j] = nc;
        gn[b] = std::max(std::min(val, capv) - g, 1e-3);
        if (dead && opt.deadpick) { deadNow = true; break; }
      }
      if (deadNow) {
        st.deadPicks++;
        best = j; kb = 2 - kb;
        bestValid[0] = curValid[0]; bestValid[1] = curValid[1];
        break;
      }
      double score = gn[0] * gn[1];
      if (score > bestScore) {
        bestScore = score; best = j; kb = 2 - kb;
        bestValid[0] = curValid[0]; bestValid[1] = curValid[1];
      }
    }
    finish(best);
    for (int b = 0; b < 2; b++) {
      bool keep = bestValid[b] && (b ? d.c1 < 0 : d.c0 < 0);
      d.tv[b] = keep;
      if (keep && kb != 0) std::swap(tslots[4 * depth + b], tslots[4 * depth + 2 + b]);
    }
  }
  Decision classifySlice(int depth) {
    Decision d;
    if (opt.selfcheck) selfCheck();
    if (nM > P.budget) { d.kind = 0; st.over++; return d; }
    int slack = P.budget - nM, violRow = -1, single = -1, forcedRow = -1;
    {
      const int16_t* rm = rem.data();
      const int16_t* av = avail.data();
      for (int r = 0; r < R; r++) {
        int x = rm[r];
        if (x > 0) {
          if (x > av[r]) { violRow = r; break; }
          if (x > slack && single < 0) single = r;
          if (x == av[r] && forcedRow < 0) forcedRow = r;
        }
      }
    }
    if (violRow >= 0 || single >= 0) {  // one row alone closes the node
      Cert c;
      c.cap = violRow >= 0 ? 0 : 1;
      c.w.push_back({violRow >= 0 ? violRow : single, 1});
      d.certId = internChecked(c); d.kind = 1; st.rowLeaves++;
      return d;
    }
    if (Cert* c = poolCheck()) { d.certId = internChecked(*c); d.kind = 1; return d; }
    if (opt.forced && forcedRow >= 0) {
      // pbb_strong: branch on the first free state of the first forced row; its 'occupied' child violates the row
      int v = -1;
      for (int t = P.rstart[forcedRow]; t < P.rstart[forcedRow + 1]; t++) { int i = P.ridx[t]; if (isFree(i) && (v < 0 || i < v)) v = i; }
      if (v < 0) fatal("internal error: forced row without a free state");
      d.var = v;
      Cert c; c.cap = 0; c.w.push_back({forcedRow, 1});
      d.c0 = cacheChild(v, 0, &c);
      st.forcedBr++;
      return d;
    }
    int nfree = n - nM - O.count();
    if (nfree == 0) {
      if (!verifyWitness(P, M)) fatal("internal error: full assignment is neither closed nor a witness");
      witness.clear();
      for (int i = 0; i < n; i++) if (M.test(i)) witness.push_back(i);
      d.kind = 3;
      return d;
    }
    if (opt.cold) lpReset();
    int s = lpSolve(opt.cutoff, opt.maxIter);
    st.nodeLps++;
    if (s == ST_CUT) { Cert* c = pushPool(lastCert); d.certId = internChecked(*c); d.kind = 1; st.lpLeaves++; st.phiLeaves++; return d; }
    if (s == ST_INFEAS) {
      if (makeRayCert(lastCert) || (opt.stdFallback && stdLeaf(lastCert))) {
        Cert* c = pushPool(lastCert); d.certId = internChecked(*c); d.kind = 1; st.infLeaves++; return d;
      }
      st.rayFail++; d.var = fallbackVar();
      return d;
    }
    if (s == ST_LIMIT) { st.iterLimit++; d.var = fallbackVar(); return d; }
    extractDual();
    double g = gBound;
    d.g = g;
    if (g > P.sliceB + 1e-7) {
      if (makeCert(lastCert)) { Cert* c = pushPool(lastCert); d.certId = internChecked(*c); d.kind = 1; st.lpLeaves++; st.phiLeaves++; return d; }
      if (opt.stdFallback && stdLeaf(lastCert)) { Cert* c = pushPool(lastCert); d.certId = internChecked(*c); d.kind = 1; st.lpLeaves++; return d; }
      st.certFail++;
    }
    int frac[MAXN], nf = 0;
    double hN[MAXN];
    for (int j = 0; j < n; j++) { hN[j] = h[j]; if (isFree(j) && h[j] > TOLI && h[j] < 1 - TOLI) frac[nf++] = j; }
    if (nf == 0) {
      // integral score-LP optimum: h(F) <= t and h(Lo) <= b.  Rows are covering, so adding holes on free states
      // until h(F) = t and h(Lo) = b keeps every row satisfied: a vector with exactly `budget` holes.
      Mask H = M;
      for (int j = 0; j < n; j++) if (isFree(j) && h[j] > 0.5) H.set(j);
      int needF = P.sliceT - popand(H, P.Fm), needL = P.sliceB - popand(H, P.Lm);
      for (int j = 0; j < n && (needF > 0 || needL > 0); j++) {
        if (!isFree(j) || H.test(j)) continue;
        if (P.Fm.test(j) && needF > 0) { H.set(j); needF--; }
        else if (P.Lm.test(j) && needL > 0) { H.set(j); needL--; }
      }
      if (verifyWitness(P, H)) {
        st.completions++;
        witness.clear();
        for (int i = 0; i < n; i++) if (H.test(i)) witness.push_back(i);
        d.kind = 3;
        return d;
      }
      st.intNoWit++;
      for (int j = 0; j < n; j++) if (isFree(j)) { d.var = j; break; }
      return d;
    }
    d.lpOpt = true;
    bool haveVec = false;
    Cert& av = *ancStore[depth];
    if (opt.useAnc) {
      haveVec = makeOpenVec(av);
      if (haveVec && certMargin(av) > 0) {
        Cert* c = pushPool(av);
        d.certId = internChecked(*c); d.kind = 1; st.lpLeaves++;
        return d;
      }
    }
    selectSlice(depth, frac, nf, g, hN, d);
    d.hv = hN[d.var];
    if (haveVec) { anc.push_back(&av); d.ancPushed = true; }
    return d;
  }

  // ---------------- one node
  Decision classify(int depth, int bvar, int bdir, double pg, double pdist) {
    if (P.slice) return classifySlice(depth);
    Decision d;
    if (opt.selfcheck) selfCheck();
    auto pcClosed = [&]() { if (bvar >= 0 && pdist > 1e-9) { psum[bdir][bvar] += (P.budget + 1 - pg) / pdist; pcnt[bdir][bvar]++; } };
    if (nM > P.budget) { d.kind = 0; st.over++; return d; }
    int slack = P.budget - nM, violRow = -1, single = -1;
    {
      const int16_t* rm = rem.data();
      const int16_t* av = avail.data();
      for (int r = 0; r < R; r++) {
        int x = rm[r];
        if (x > 0) {
          if (x > av[r]) { violRow = r; break; }
          if (x > slack && single < 0) single = r;
        }
      }
    }
    if (violRow >= 0 || single >= 0) {  // one row alone closes the node
      Cert c;
      c.cap = violRow >= 0 ? 0 : 1;
      c.w.push_back({violRow >= 0 ? violRow : single, 1});
      d.certId = internChecked(c); d.kind = 1; st.rowLeaves++; pcClosed();
      return d;
    }
    if (Cert* c = poolCheck()) { d.certId = internChecked(*c); d.kind = 1; pcClosed(); return d; }
    int nfree = n - nM - O.count();
    if (nfree == 0) {
      if (!verifyWitness(P, M)) fatal("internal error: full assignment is neither closed nor a witness");
      witness.clear();
      for (int i = 0; i < n; i++) if (M.test(i)) witness.push_back(i);
      d.kind = 3;
      return d;
    }
    if (opt.cold) lpReset();
    int s = lpSolve(opt.cutoff, opt.maxIter);
    st.nodeLps++;
    if (s == ST_CUT) { Cert* c = pushPool(lastCert); d.certId = internChecked(*c); d.kind = 1; st.lpLeaves++; pcClosed(); return d; }
    if (s == ST_INFEAS) {
      if (makeRayCert(lastCert)) { Cert* c = pushPool(lastCert); d.certId = internChecked(*c); d.kind = 1; st.infLeaves++; pcClosed(); return d; }
      st.rayFail++; d.var = fallbackVar();
      return d;
    }
    if (s == ST_LIMIT) { st.iterLimit++; d.var = fallbackVar(); return d; }
    extractDual();
    double g = gBound;
    d.g = g;
    if (g > P.budget + 1e-7) {
      if (makeCert(lastCert)) { Cert* c = pushPool(lastCert); d.certId = internChecked(*c); d.kind = 1; st.lpLeaves++; pcClosed(); return d; }
      st.certFail++;
    }
    if (bvar >= 0 && pdist > 1e-9) { psum[bdir][bvar] += std::max(0.0, std::min(g, (double)P.budget + 1) - pg) / pdist; pcnt[bdir][bvar]++; }
    int frac[MAXN], nf = 0;
    double hN[MAXN];
    for (int j = 0; j < n; j++) { hN[j] = h[j]; if (isFree(j) && h[j] > TOLI && h[j] < 1 - TOLI) frac[nf++] = j; }
    if (nf == 0) {
      Mask H = M;
      for (int j = 0; j < n; j++) if (isFree(j) && h[j] > 0.5) H.set(j);
      if (verifyWitness(P, H)) {
        witness.clear();
        for (int i = 0; i < n; i++) if (H.test(i)) witness.push_back(i);
        d.kind = 3;
        return d;
      }
      st.intNoWit++;
      for (int j = 0; j < n; j++) if (isFree(j)) { d.var = j; break; }
      return d;
    }
    d.lpOpt = true;
    bool haveVec = false;
    Cert& av = *ancStore[depth];
    if (opt.useAnc) {
      haveVec = makeOpenVec(av);
      if (haveVec && certMargin(av) > 0) {  // the rounded vector closes the node after all
        Cert* c = pushPool(av);
        d.certId = internChecked(*c); d.kind = 1; st.lpLeaves++;
        return d;
      }
    }
    select(depth, frac, nf, g, hN, d);
    d.hv = hN[d.var];
    if (haveVec) { anc.push_back(&av); d.ancPushed = true; }
    return d;
  }
  int pushLeaf(int certId) {
    nodes.push_back({-1, certId, 0});
    st.nodes++; st.cachedLeaves++;
    return (int)nodes.size() - 1;
  }
  int expand(int depth, int bvar, int bdir, double pg, double pdist) {
    if ((st.nodes & 1023) == 0) {
      gNodes.fetch_add(1024, std::memory_order_relaxed);
      if (gStop.load(std::memory_order_relaxed)) throw StopEx();
      if (gDeadline > 0 && nowSec() > gDeadline) { gStop.store(true); throw StopEx(); }
    }
    int idx = (int)nodes.size();
    nodes.push_back({-4, 0, 0});
    st.nodes++;
    if ((i64)nodes.size() > opt.maxCtxNodes) throw TooBigEx();
    Decision d = classify(depth, bvar, bdir, pg, pdist);
    if (d.kind == 0) { nodes[idx].a = -2; return idx; }
    if (d.kind == 1) { nodes[idx] = {-1, d.certId, 0}; return idx; }
    if (d.kind == 3) throw WitnessEx();
    int v = d.var;
    if (v < 0) fatal("internal error: no branching variable");
    bool both = d.c0 < 0 && d.c1 < 0;
    if (both && d.lpOpt && !d.slotSaved) { lpSave(slot(depth)); d.slotSaved = true; }
    int pv = d.lpOpt ? v : -1;
    int o, z;
    if (d.c1 >= 0) o = pushLeaf(d.c1);
    else {
      if (d.tv[1]) lpRestore(tslot(depth, 1));
      fix(v, 1); o = expand(depth + 1, d.tv[1] ? -1 : pv, 1, d.g, 1 - d.hv); unfix(v, 1);
    }
    if (d.c0 >= 0) z = pushLeaf(d.c0);
    else {
      if (d.tv[0]) lpRestore(tslot(depth, 0));
      else if (both && d.slotSaved && stamp != slots[depth]->stamp) lpRestore(*slots[depth]);
      fix(v, 0); z = expand(depth + 1, d.tv[0] ? -1 : pv, 0, d.g, d.hv); unfix(v, 0);
    }
    if (d.ancPushed) anc.pop_back();
    nodes[idx] = {v, z, o};
    return idx;
  }
  void resetForContext(const Worker* snap) {
    nodes.clear(); store.clear(); pool.clear(); anc.clear(); poolM.clear(); ancM.clear();
    lpReset();
    for (int b = 0; b < 2; b++) for (int j = 0; j < MAXN; j++) { psum[b][j] = snap ? snap->psum[b][j] : 0; pcnt[b][j] = snap ? snap->pcnt[b][j] : 0; }
    st = Stats();
  }
};

// ------------------------------------------------------------------ output
static void jsonStr(std::string& out, const std::string& s) {
  out += '"';
  for (char ch : s) { if (ch == '"' || ch == '\\') out += '\\'; out += ch; }
  out += '"';
}
static void appendNode(std::string& out, const NodeRec& nd, const CertStore& cs, std::vector<std::pair<int, i64>>& tmp) {
  char buf[96];
  if (nd.a >= 0) { snprintf(buf, sizeof buf, "{\"type\":\"branch\",\"vertex\":%d,\"zero\":%d,\"one\":%d}", nd.a, nd.b, nd.c); out += buf; }
  else if (nd.a == -1) {
    i64 cap;
    cs.get(nd.b, cap, tmp);
    snprintf(buf, sizeof buf, "{\"type\":\"weighted\",\"capacity\":%lld,\"weights\":[", cap);
    out += buf;
    for (size_t t = 0; t < tmp.size(); t++) { snprintf(buf, sizeof buf, "%s[%d,%lld]", t ? "," : "", tmp[t].first, tmp[t].second); out += buf; }
    out += "]}";
  } else if (nd.a == -2) out += "{\"type\":\"over_budget\"}";
  else if (nd.a == -3) { snprintf(buf, sizeof buf, "{\"type\":\"context\",\"context\":%d}", nd.b); out += buf; }
  else out += "{\"type\":\"pending\"}";
}
static void appendList(std::string& out, const Mask& m, int n) {
  out += '[';
  bool first = true;
  char buf[16];
  for (int i = 0; i < n; i++) if (m.test(i)) { snprintf(buf, sizeof buf, "%s%d", first ? "" : ",", i); out += buf; first = false; }
  out += ']';
}
static bool writeCtxFile(const std::string& path, int cid, const Mask& M, const Mask& O, int n,
                         const std::vector<NodeRec>& nodes, const CertStore& cs) {
  std::string tmpPath = path + ".tmp";
  gzFile gz = gzopen(tmpPath.c_str(), "wb6");
  if (!gz) return false;
  std::string out;
  std::vector<std::pair<int, i64>> tmp;
  char buf[64];
  snprintf(buf, sizeof buf, "{\"context\":%d,\"missing\":", cid);
  out += buf; appendList(out, M, n); out += ",\"occupied\":"; appendList(out, O, n); out += ",\"root\":0,\"nodes\":[";
  bool ok = true;
  for (size_t i = 0; i < nodes.size(); i++) {
    if (i) out += ',';
    appendNode(out, nodes[i], cs, tmp);
    if (out.size() > (1u << 20)) { if (gzwrite(gz, out.data(), (unsigned)out.size()) != (int)out.size()) ok = false; out.clear(); }
  }
  out += "]}";
  if (gzwrite(gz, out.data(), (unsigned)out.size()) != (int)out.size()) ok = false;
  if (gzclose(gz) != Z_OK) ok = false;
  if (!ok) return false;
  return rename(tmpPath.c_str(), path.c_str()) == 0;
}

struct CtxDef { int cid, node; Mask M, O; };
struct Master {
  std::vector<NodeRec> nodes;
  CertStore store;
  std::vector<CtxDef> ctxs;
  int leaves = 0, rowsAtBuild = 0;
  uint64_t hashAtBuild = 0;
};
static bool writeTextFile(const std::string& path, const std::string& content) {
  std::string tmp = path + ".tmp";
  FILE* f = fopen(tmp.c_str(), "w");
  if (!f) return false;
  bool ok = fwrite(content.data(), 1, content.size(), f) == content.size();
  ok = fclose(f) == 0 && ok;
  return ok && rename(tmp.c_str(), path.c_str()) == 0;
}
static bool writeMasterJson(const std::string& path, const Problem& P, const Master& m) {
  std::string out = "{\"source\": ";
  jsonStr(out, P.source);
  out += ", \"extra\": ";
  if (P.extra == "-") out += "null"; else jsonStr(out, P.extra);
  char buf[96];
  snprintf(buf, sizeof buf, ", \"budget\": %d, \"root\": 0, \"nodes\": [", P.budget);
  out += buf;
  std::vector<std::pair<int, i64>> tmp;
  for (size_t i = 0; i < m.nodes.size(); i++) { if (i) out += ", "; appendNode(out, m.nodes[i], m.store, tmp); }
  snprintf(buf, sizeof buf, "], \"contexts\": %d, \"master_leaves\": %d}", (int)m.ctxs.size(), m.leaves);
  out += buf;
  return writeTextFile(path, out);
}
static bool writeContextsJson(const std::string& path, const Problem& P, const Master& m) {
  std::string out = "[";
  char buf[64];
  for (size_t i = 0; i < m.ctxs.size(); i++) {
    snprintf(buf, sizeof buf, "%s\n{\"context\":%d,\"missing\":", i ? "," : "", m.ctxs[i].cid);
    out += buf; appendList(out, m.ctxs[i].M, P.N); out += ",\"occupied\":"; appendList(out, m.ctxs[i].O, P.N); out += "}";
  }
  out += "\n]\n";
  return writeTextFile(path, out);
}
// master.txt: fastbb's own copy of the master tree, so that a resumed run keeps the same contexts
// even when rows have been appended (the BFS is not repeated).
static bool saveMasterTxt(const std::string& path, const Problem& P, const Master& m, const Worker& w) {
  std::string out;
  char buf[160];
  snprintf(buf, sizeof buf, "FASTBB-MASTER 1\n%d %d %d %llu %d\n%d\n", P.N, P.budget, m.rowsAtBuild, (unsigned long long)m.hashAtBuild, m.leaves, (int)m.nodes.size());
  out += buf;
  for (const auto& nd : m.nodes) { snprintf(buf, sizeof buf, "%d %d %d\n", nd.a, nd.b, nd.c); out += buf; }
  snprintf(buf, sizeof buf, "%d\n", (int)m.store.off.size());
  out += buf;
  std::vector<std::pair<int, i64>> tmp;
  for (int id = 0; id < (int)m.store.off.size(); id++) {
    i64 cap;
    m.store.get(id, cap, tmp);
    snprintf(buf, sizeof buf, "%lld %d", cap, (int)tmp.size());
    out += buf;
    for (const auto& pr : tmp) { snprintf(buf, sizeof buf, " %d %lld", pr.first, pr.second); out += buf; }
    out += '\n';
  }
  snprintf(buf, sizeof buf, "%d\n", (int)m.ctxs.size());
  out += buf;
  for (const auto& c : m.ctxs) {
    snprintf(buf, sizeof buf, "%d %d %d", c.cid, c.node, c.M.count());
    out += buf;
    for (int i = 0; i < P.N; i++) if (c.M.test(i)) { snprintf(buf, sizeof buf, " %d", i); out += buf; }
    snprintf(buf, sizeof buf, " %d", c.O.count());
    out += buf;
    for (int i = 0; i < P.N; i++) if (c.O.test(i)) { snprintf(buf, sizeof buf, " %d", i); out += buf; }
    out += '\n';
  }
  for (int j = 0; j < P.N; j++) { snprintf(buf, sizeof buf, "%.17g %d %.17g %d\n", w.psum[0][j], w.pcnt[0][j], w.psum[1][j], w.pcnt[1][j]); out += buf; }
  return writeTextFile(path, out);
}
static int loadMasterTxt(const std::string& path, const Problem& P, Master& m, Worker& w) {  // 0 absent, 1 ok, -1 mismatch
  FILE* f = fopen(path.c_str(), "r");
  if (!f) return 0;
  char key[64];
  int ver, N, budget, nn, nc, nx;
  unsigned long long hsh;
  int ok = 1;
  if (fscanf(f, "%63s %d %d %d %d %llu %d %d", key, &ver, &N, &budget, &m.rowsAtBuild, &hsh, &m.leaves, &nn) != 8 || strcmp(key, "FASTBB-MASTER")) ok = -1;
  if (ok == 1 && (N != P.N || budget != P.budget || m.rowsAtBuild > P.R || hsh != P.prefixHash(m.rowsAtBuild))) ok = -1;
  if (ok == 1) {
    m.hashAtBuild = hsh;
    m.nodes.resize(nn);
    for (auto& nd : m.nodes) if (fscanf(f, "%d %d %d", &nd.a, &nd.b, &nd.c) != 3) ok = -1;
  }
  if (ok == 1 && fscanf(f, "%d", &nc) == 1) {
    std::vector<std::pair<int, i64>> tmp;
    for (int id = 0; id < nc && ok == 1; id++) {
      long long cap; int k;
      if (fscanf(f, "%lld %d", &cap, &k) != 2) { ok = -1; break; }
      tmp.resize(k);
      for (auto& pr : tmp) { long long wv; if (fscanf(f, "%d %lld", &pr.first, &wv) != 2) ok = -1; pr.second = wv; }
      m.store.add(cap, tmp);
    }
  } else ok = -1;
  if (ok == 1 && fscanf(f, "%d", &nx) == 1) {
    m.ctxs.resize(nx);
    for (auto& c : m.ctxs) {
      int k, i;
      if (fscanf(f, "%d %d %d", &c.cid, &c.node, &k) != 3) { ok = -1; break; }
      for (int t = 0; t < k; t++) { if (fscanf(f, "%d", &i) != 1 || i < 0 || i >= P.N) { ok = -1; break; } c.M.set(i); }
      if (ok != 1 || fscanf(f, "%d", &k) != 1) { ok = -1; break; }
      for (int t = 0; t < k; t++) { if (fscanf(f, "%d", &i) != 1 || i < 0 || i >= P.N) { ok = -1; break; } c.O.set(i); }
    }
  } else ok = -1;
  if (ok == 1) for (int j = 0; j < P.N; j++) if (fscanf(f, "%lf %d %lf %d", &w.psum[0][j], &w.pcnt[0][j], &w.psum[1][j], &w.pcnt[1][j]) != 4) ok = -1;
  fclose(f);
  return ok;
}

static std::mutex gIo;
static void statsJson(std::string& out, const Stats& s) {
  char buf[640];
  snprintf(buf, sizeof buf,
           "\"node_lps\":%lld,\"trial_lps\":%lld,\"simplex_iters\":%lld,\"leaves_row\":%lld,\"leaves_pool\":%lld,"
           "\"leaves_ancestor\":%lld,\"leaves_cached\":%lld,\"leaves_lp\":%lld,\"leaves_infeasible\":%lld,\"over_budget\":%lld,"
           "\"both_closed\":%lld,\"refactor\":%lld,\"cert_fail\":%lld,\"ray_fail\":%lld,\"iter_limit\":%lld,\"integral_no_witness\":%lld,\"full_pricing_passes\":%lld",
           s.nodeLps, s.trials, s.iters, s.rowLeaves, s.poolLeaves, s.ancLeaves, s.cachedLeaves, s.lpLeaves, s.infLeaves, s.over,
           s.bothClosed, s.refac, s.certFail, s.rayFail, s.iterLimit, s.intNoWit, s.fullPasses);
  out += buf;
  snprintf(buf, sizeof buf, ",\"forced_branches\":%lld,\"dead_picks\":%lld,\"known_picks\":%lld,\"leaves_phi\":%lld,\"std_lp_tried\":%lld,\"std_lp_leaves\":%lld,\"completions\":%lld",
           s.forcedBr, s.deadPicks, s.knownPicks, s.phiLeaves, s.stdTried, s.stdLeaves, s.completions);
  out += buf;
}
static void printWitness(const Problem& P, const std::vector<int>& holes, int cid, const std::string& outdir) {
  Mask H;
  for (int i : holes) H.set(i);
  if ((int)holes.size() != H.count() || !verifyWitness(P, H)) fatal("internal error: witness failed the exact check");
  std::string hl = "[";
  char buf[32];
  for (size_t t = 0; t < holes.size(); t++) { snprintf(buf, sizeof buf, "%s%d", t ? ", " : "", holes[t]); hl += buf; }
  hl += "]";
  if (cid >= 0) printf("{\"event\": \"WITNESS\", \"context\": %d, \"holes\": %s}\n", cid, hl.c_str());
  else printf("{\"event\": \"WITNESS\", \"holes\": %s}\n", hl.c_str());
  fflush(stdout);
  if (!outdir.empty()) {
    std::string js = "{\"holes\": " + hl + ", \"context\": " + (cid >= 0 ? std::to_string(cid) : std::string("null")) + "}";
    writeTextFile(outdir + "/WITNESS.json", js);
  }
}

// ------------------------------------------------------------------ modes
static bool fileExists(const std::string& p) { struct stat sb; return stat(p.c_str(), &sb) == 0; }

// Claim files let several fastbb processes share one output directory (add or remove workers at any
// time): a context is taken by the process that creates ctx-N.claim; claims of dead processes are removed.
static std::string claimPath(const std::string& outdir, int cid) { return outdir + "/ctx-" + std::to_string(cid) + ".claim"; }
static bool claimCtx(const std::string& outdir, int cid) {
  int fd = open(claimPath(outdir, cid).c_str(), O_CREAT | O_EXCL | O_WRONLY, 0664);
  if (fd < 0) return false;
  char buf[32];
  int k = snprintf(buf, sizeof buf, "%d\n", (int)getpid());
  if (write(fd, buf, k) != k) { close(fd); return true; }
  close(fd);
  return true;
}
static void clearStaleClaims(const std::string& outdir, const std::vector<int>& cids) {
  for (int cid : cids) {
    std::string p = claimPath(outdir, cid);
    FILE* f = fopen(p.c_str(), "r");
    if (!f) continue;
    int pid = 0;
    if (fscanf(f, "%d", &pid) != 1) pid = 0;
    fclose(f);
    if (pid <= 0 || (kill(pid, 0) != 0 && errno == ESRCH)) unlink(p.c_str());
  }
}

static int runSolve(Problem& P, const Opt& opt, int threads, int nctx, const std::string& outdir, const std::vector<int>& only, int ctxLimit, int splitOpen) {
  mkdir(outdir.c_str(), 0775);
  double t0 = nowSec();
  // a witness left by an earlier run: still valid for the current rows?
  if (fileExists(outdir + "/WITNESS.json")) {
    FILE* f = fopen((outdir + "/WITNESS.json").c_str(), "r");
    std::string txt; int ch;
    while (f && (ch = fgetc(f)) != EOF) txt += (char)ch;
    if (f) fclose(f);
    Mask H; std::vector<int> holes;
    size_t a = txt.find('['), b = txt.find(']');
    if (a != std::string::npos && b != std::string::npos)
      for (size_t i = a + 1; i < b;) { if (isdigit((unsigned char)txt[i])) { int v = atoi(txt.c_str() + i); if (v < P.N) { H.set(v); holes.push_back(v); } while (i < b && isdigit((unsigned char)txt[i])) i++; } else i++; }
    if (!holes.empty() && verifyWitness(P, H)) { printf("{\"event\": \"old_witness_still_valid\"}\n"); printWitness(P, holes, -1, ""); return 3; }
    for (int k = 1;; k++) { std::string to = outdir + "/WITNESS.refuted-" + std::to_string(k) + ".json"; if (!fileExists(to)) { rename((outdir + "/WITNESS.json").c_str(), to.c_str()); break; } }
    printf("{\"event\": \"old_witness_refuted_by_current_rows\"}\n");
  }
  Master m;
  Worker mw(P, opt);
  int lm = loadMasterTxt(outdir + "/master.txt", P, m, mw);
  if (lm < 0) { fprintf(stderr, "master.txt in %s does not match this row file/budget (rows must only be appended)\n", outdir.c_str()); return 2; }
  struct Fr { int node; Mask M, O; };
  bool masterWitness = false;
  // one breadth-first level of the master tree: classify every frontier node, children form the next frontier
  auto expandLevel = [&](std::vector<Fr>& frontier) {
    std::vector<Fr> next;
    for (const auto& f : frontier) {
      mw.setState(f.M, f.O);
      Decision d = mw.classify(0, -1, 0, 0, 0);
      if (d.ancPushed) mw.anc.pop_back();
      if (d.kind == 0) { m.nodes[f.node] = {-2, 0, 0}; m.leaves++; }
      else if (d.kind == 1) { m.nodes[f.node] = {-1, d.certId, 0}; m.leaves++; }
      else if (d.kind == 3) { masterWitness = true; return; }
      else {
        int z = (int)m.nodes.size();
        m.nodes.push_back({-4, 0, 0}); m.nodes.push_back({-4, 0, 0});
        m.nodes[f.node] = {d.var, z, z + 1};
        Mask mo = f.O; mo.set(d.var);
        Mask mm = f.M; mm.set(d.var);
        if (d.c0 >= 0) { m.nodes[z] = {-1, d.c0, 0}; m.leaves++; } else next.push_back({z, f.M, mo});
        if (d.c1 >= 0) { m.nodes[z + 1] = {-1, d.c1, 0}; m.leaves++; } else next.push_back({z + 1, mm, f.O});
      }
    }
    frontier.swap(next);
  };
  if (lm == 0) {
    std::vector<Fr> frontier;
    m.nodes.push_back({-4, 0, 0});
    Mask o0; o0.set(0);
    frontier.push_back({0, Mask(), o0});
    mw.resetForContext(nullptr);
    while (!frontier.empty() && (int)frontier.size() < nctx && !masterWitness) expandLevel(frontier);
    if (masterWitness) { printWitness(P, mw.witness, -1, outdir); return 3; }
    for (size_t i = 0; i < frontier.size(); i++) {
      m.nodes[frontier[i].node] = {-3, (int)i, 0};
      m.ctxs.push_back({(int)i, frontier[i].node, frontier[i].M, frontier[i].O});
    }
    m.store = mw.store;
    m.rowsAtBuild = P.R; m.hashAtBuild = P.prefixHash(P.R);
    if (!saveMasterTxt(outdir + "/master.txt", P, m, mw)) { fprintf(stderr, "cannot write master.txt\n"); return 2; }
  }
  if (splitOpen > 0) {
    // Refinement: every context that is still open is replaced by its descendants splitOpen levels
    // further down (new context numbers); closed contexts and their files are untouched.
    mw.store = m.store;
    std::vector<CtxDef> keep;
    std::vector<Fr> frontier;
    int nextCid = 0;
    for (const auto& c : m.ctxs) {
      nextCid = std::max(nextCid, c.cid + 1);
      if (fileExists(outdir + "/ctx-" + std::to_string(c.cid) + ".json.gz")) keep.push_back(c);
      else frontier.push_back({c.node, c.M, c.O});
    }
    int before = (int)frontier.size();
    for (int lvl = 0; lvl < splitOpen && !frontier.empty() && !masterWitness; lvl++) expandLevel(frontier);
    if (masterWitness) { printWitness(P, mw.witness, -1, outdir); return 3; }
    for (const auto& f : frontier) { m.nodes[f.node] = {-3, nextCid, 0}; keep.push_back({nextCid, f.node, f.M, f.O}); nextCid++; }
    m.ctxs.swap(keep);
    m.store = mw.store;
    m.rowsAtBuild = P.R; m.hashAtBuild = P.prefixHash(P.R);
    if (!saveMasterTxt(outdir + "/master.txt", P, m, mw)) { fprintf(stderr, "cannot write master.txt\n"); return 2; }
    printf("{\"event\": \"split_open\", \"levels\": %d, \"open_before\": %d, \"open_after\": %d, \"contexts\": %d}\n", splitOpen, before, (int)frontier.size(), (int)m.ctxs.size());
  }
  if (!writeMasterJson(outdir + "/master.json", P, m) || !writeContextsJson(outdir + "/contexts.json", P, m)) { fprintf(stderr, "cannot write master.json\n"); return 2; }
  std::vector<int> todo;  // positions in m.ctxs
  for (size_t i = 0; i < m.ctxs.size(); i++) {
    const auto& c = m.ctxs[i];
    if (!only.empty() && std::find(only.begin(), only.end(), c.cid) == only.end()) continue;
    if (!fileExists(outdir + "/ctx-" + std::to_string(c.cid) + ".json.gz")) todo.push_back((int)i);
  }
  if (ctxLimit > 0 && (int)todo.size() > ctxLimit) todo.resize(ctxLimit);
  {
    std::vector<int> cids;
    for (const auto& c : m.ctxs) cids.push_back(c.cid);
    clearStaleClaims(outdir, cids);
  }
  std::atomic<int> skippedClaimed(0);
  {
    std::string sj; statsJson(sj, mw.st);
    printf("{\"event\": \"start\", \"contexts\": %d, \"todo\": %d, \"master_leaves\": %d, \"master_nodes\": %d, \"master_resumed\": %s, \"rows\": %d, \"states\": %d, \"budget\": %d, \"threads\": %d, \"master_seconds\": %.2f, %s}\n",
           (int)m.ctxs.size(), (int)todo.size(), m.leaves, (int)m.nodes.size(), lm == 1 ? "true" : "false", P.R, P.N, P.budget, threads, nowSec() - t0, sj.c_str());
    fflush(stdout);
  }
  if (opt.timeLimit > 0) gDeadline = nowSec() + opt.timeLimit;
  std::atomic<int> next(0);
  std::atomic<int> done(0);
  Stats total;
  i64 totalNodes = 0;
  bool haveWitness = false, tooBig = false;
  int witnessCount = 0;
  std::vector<int> witHoles; int witCtx = -1;
  double t1 = nowSec();
  FILE* logf = fopen((outdir + "/fastbb.log.jsonl").c_str(), "a");
  auto workerFn = [&]() {
    Worker w(P, opt);
    while (!gStop.load()) {
      int k = next.fetch_add(1);
      if (k >= (int)todo.size()) break;
      const CtxDef& c = m.ctxs[todo[k]];
      std::string path = outdir + "/ctx-" + std::to_string(c.cid) + ".json.gz";
      if (fileExists(path)) continue;                                     // closed meanwhile by another process
      if (!claimCtx(outdir, c.cid)) { skippedClaimed++; continue; }       // another process is working on it
      struct Release { std::string p; ~Release() { unlink(p.c_str()); } } release{claimPath(outdir, c.cid)};
      double tc = nowSec();
      w.resetForContext(&mw);
      w.setState(c.M, c.O);
      try {
        w.expand(0, -1, 0, 0, 0);
      } catch (StopEx&) {
        std::lock_guard<std::mutex> lk(gIo);
        total.add(w.st);
        printf("{\"event\": \"abandoned\", \"context\": %d, \"nodes_so_far\": %lld, \"seconds\": %.1f}\n", c.cid, w.st.nodes, nowSec() - tc);
        fflush(stdout);
        break;
      } catch (WitnessEx&) {
        std::lock_guard<std::mutex> lk(gIo);
        total.add(w.st);
        if (!haveWitness) { haveWitness = true; witHoles = w.witness; witCtx = c.cid; }
        if (opt.witnessContinue) {  // keep the other contexts going; this context stays open
          Mask H;
          for (int i : w.witness) H.set(i);
          if (!verifyWitness(P, H)) fatal("internal error: witness failed the exact check");
          std::string hl = "[";
          for (size_t t = 0; t < w.witness.size(); t++) hl += (t ? ", " : "") + std::to_string(w.witness[t]);
          hl += "]";
          printf("{\"event\": \"WITNESS\", \"context\": %d, \"holes\": %s, \"nodes_so_far\": %lld}\n", c.cid, hl.c_str(), w.st.nodes);
          fflush(stdout);
          writeTextFile(outdir + "/witness-ctx-" + std::to_string(c.cid) + ".json", "{\"holes\": " + hl + ", \"context\": " + std::to_string(c.cid) + "}");
          witnessCount++;
          continue;
        }
        gStop.store(true);
        break;
      } catch (TooBigEx&) {
        std::lock_guard<std::mutex> lk(gIo);
        total.add(w.st);
        tooBig = true;
        printf("{\"event\": \"context_too_big\", \"context\": %d, \"nodes_so_far\": %lld}\n", c.cid, w.st.nodes);
        fflush(stdout);
        continue;
      }
      if (!writeCtxFile(path, c.cid, c.M, c.O, P.N, w.nodes, w.store)) fatal("cannot write a context file");
      std::lock_guard<std::mutex> lk(gIo);
      total.add(w.st);
      totalNodes += (i64)w.nodes.size();
      int dn = ++done;
      std::string sj; statsJson(sj, w.st);
      char line[2400];
      snprintf(line, sizeof line, "{\"event\": \"closed\", \"context\": %d, \"nodes\": %lld, \"seconds\": %.2f, \"done\": %d, \"todo\": %d, \"total_nodes\": %lld, \"elapsed\": %.1f, %s}",
               c.cid, (i64)w.nodes.size(), nowSec() - tc, dn, (int)todo.size(), totalNodes, nowSec() - t1, sj.c_str());
      puts(line); fflush(stdout);
      if (logf) { fprintf(logf, "%s\n", line); fflush(logf); }
    }
  };
  std::vector<std::thread> th;
  for (int t = 0; t < threads; t++) th.emplace_back(workerFn);
  for (auto& t : th) t.join();
  if (logf) fclose(logf);
  double el = nowSec() - t1;
  std::string sj; statsJson(sj, total);
  if (haveWitness) printWitness(P, witHoles, witCtx, outdir);
  if (witnessCount) { printf("{\"event\": \"witness_contexts\", \"count\": %d}\n", witnessCount); }
  if (skippedClaimed.load()) printf("{\"event\": \"claimed_by_other_processes\", \"contexts\": %d}\n", skippedClaimed.load());
  int closedFiles = 0;
  for (const auto& c : m.ctxs) if (fileExists(outdir + "/ctx-" + std::to_string(c.cid) + ".json.gz")) closedFiles++;
  bool all = closedFiles == (int)m.ctxs.size() && !haveWitness;
  printf("{\"event\": \"%s\", \"contexts\": %d, \"contexts_closed\": %d, \"closed_now\": %d, \"todo\": %d, \"total_nodes\": %lld, \"nodes_incl_abandoned\": %lld, \"seconds\": %.1f, \"threads\": %d, %s}\n",
         all ? "DONE" : (haveWitness ? "STOPPED_ON_WITNESS" : "PARTIAL"), (int)m.ctxs.size(), closedFiles, done.load(), (int)todo.size(), totalNodes, total.nodes, el, threads, sj.c_str());
  fflush(stdout);
  if (haveWitness) return 3;
  if (tooBig) return 4;
  return all ? 0 : 5;
}

// Knuth-style random dives with the same node rule.  A child that is already known to be a leaf
// is counted exactly instead of being sampled, which lowers the variance.
static int runDive(Problem& P, const Opt& opt, int dives, uint64_t seed, const std::string& outPath) {
  Worker w(P, opt);
  w.resetForContext(nullptr);
  uint64_t x = seed * 0x9E3779B97F4A7C15ULL + 0x1234567ULL;
  auto rnd = [&]() { x ^= x << 13; x ^= x >> 7; x ^= x << 17; return x; };
  std::vector<double> ests; std::vector<int> depths; std::vector<std::vector<int>> wits;
  // The decisions near the root (fewer than dtop fixed states) are the expensive ones (ktop candidates);
  // a real run takes each of them once, so the dives remember them instead of recomputing them.
  std::map<std::array<uint64_t, 2 * NW>, Decision> topCache;
  double t0 = nowSec(), sum = 0;
  if (opt.timeLimit > 0) gDeadline = nowSec() + opt.timeLimit;
  for (int dv = 0; dv < dives; dv++) {
    if (gDeadline > 0 && nowSec() > gDeadline) break;
    Mask o0; o0.set(0);
    w.setState(Mask(), o0);
    w.anc.clear();
    double wgt = 1, est = 0; int depth = 0, bvar = -1, bdir = 0; double pg = 0, pdist = 0;
    for (;;) {
      Decision d;
      bool top = w.nM + w.O.count() < opt.dtop, hit = false;
      std::array<uint64_t, 2 * NW> key;
      if (top) {
        for (int i = 0; i < NW; i++) { key[i] = w.M.w[i]; key[NW + i] = w.O.w[i]; }
        auto itc = topCache.find(key);
        if (itc != topCache.end()) { d = itc->second; hit = true; }
      }
      if (!hit) {
        d = w.classify(depth, bvar, bdir, pg, pdist);
        if (top && d.kind != 3) {
          Decision c = d;
          c.tv[0] = c.tv[1] = false; c.ancPushed = false; c.slotSaved = false; c.lpOpt = false;
          topCache[key] = c;
        }
      }
      est += wgt;
      if (d.kind == 3) { wits.push_back(w.witness); break; }
      if (d.kind != 2) break;
      int v = d.var;
      if (d.c0 >= 0 && d.c1 >= 0) { est += 2 * wgt; break; }
      int b;
      if (d.c0 >= 0) { est += wgt; b = 1; }
      else if (d.c1 >= 0) { est += wgt; b = 0; }
      else { b = (int)((rnd() >> 33) & 1); wgt *= 2; }
      if (d.tv[b]) w.lpRestore(w.tslot(depth, b));
      w.fix(v, b);
      if (d.lpOpt && !d.tv[b]) { bvar = v; bdir = b; pg = d.g; pdist = b ? 1 - d.hv : d.hv; } else bvar = -1;
      depth++;
      if (depth >= MAXN) break;
    }
    ests.push_back(est); depths.push_back(depth); sum += est;
    double mu = sum / ests.size(), var = 0;
    for (double e : ests) var += (e - mu) * (e - mu);
    double se = ests.size() > 1 ? std::sqrt(var / (ests.size() - 1) / ests.size()) : 0;
    std::vector<int> sd = depths; std::sort(sd.begin(), sd.end());
    std::string out;
    char buf[512];
    snprintf(buf, sizeof buf, "{\"budget\": %d, \"rows\": %d, \"dives\": %d, \"mean_nodes\": %.6g, \"log10_mean_nodes\": %.3f, \"stderr_mean\": %.6g, \"median_depth\": %d, \"max_depth\": %d, \"witnesses\": %d, \"t\": %.1f, \"node_lps\": %lld, \"trial_lps\": %lld, \"simplex_iters\": %lld",
             P.budget, P.R, (int)ests.size(), mu, std::log10(mu), se, sd[sd.size() / 2], sd.back(), (int)wits.size(), nowSec() - t0, w.st.nodeLps, w.st.trials, w.st.iters);
    out += buf;
    if ((dv + 1) % 10 == 0 || dv + 1 == dives) { printf("%s}\n", out.c_str()); fflush(stdout); }
    out += ", \"ests\": [";
    for (size_t i = 0; i < ests.size(); i++) { snprintf(buf, sizeof buf, "%s%.0f", i ? ", " : "", ests[i]); out += buf; }
    out += "], \"depths\": [";
    for (size_t i = 0; i < depths.size(); i++) { snprintf(buf, sizeof buf, "%s%d", i ? ", " : "", depths[i]); out += buf; }
    out += "], \"witness_vectors\": [";
    for (size_t i = 0; i < wits.size(); i++) {
      out += i ? ", [" : "[";
      for (size_t t = 0; t < wits[i].size(); t++) { snprintf(buf, sizeof buf, "%s%d", t ? ", " : "", wits[i][t]); out += buf; }
      out += "]";
    }
    out += "]}\n";
    if ((dv + 1) % 10 == 0 || dv + 1 == dives || !wits.empty()) writeTextFile(outPath, out);
  }
  for (const auto& wv : wits) printWitness(P, wv, -1, "");
  return wits.empty() ? 0 : 3;
}

// Random walks that solve every LP to optimality and print (status, value, bounds) for the
// differential test against HiGHS (tools/lp_difftest.py).
static int runLpTest(Problem& P, const Opt& opt, int dives, uint64_t seed, const std::string& outPath) {
  Worker w(P, opt);
  FILE* f = fopen(outPath.c_str(), "w");
  if (!f) return 2;
  uint64_t x = seed * 0x9E3779B97F4A7C15ULL + 0x7654321ULL;
  auto rnd = [&]() { x ^= x << 13; x ^= x >> 7; x ^= x << 17; return x >> 11; };
  long cnt = 0;
  for (int dv = 0; dv < dives; dv++) {
    Mask o0; o0.set(0);
    w.setState(Mask(), o0);
    for (int depth = 0; depth < 90; depth++) {
      int s = w.lpSolve(false, 200000);
      double val = 0;
      if (s == ST_OPT) { w.extractDual(); val = w.gBound; }
      fprintf(f, "%d %.12f %d", s, val, w.nM);
      for (int i = 0; i < P.N; i++) if (w.M.test(i)) fprintf(f, " %d", i);
      fprintf(f, " %d", w.O.count());
      for (int i = 0; i < P.N; i++) if (w.O.test(i)) fprintf(f, " %d", i);
      fprintf(f, "\n");
      cnt++;
      if (s != ST_OPT) break;
      std::vector<int> fr, fre;
      for (int j = 0; j < P.N; j++) if (w.isFree(j)) { fre.push_back(j); if (w.h[j] > TOLI && w.h[j] < 1 - TOLI) fr.push_back(j); }
      if (fre.empty()) break;
      int v = (!fr.empty() && rnd() % 10 < 7) ? fr[rnd() % fr.size()] : fre[rnd() % fre.size()];
      w.fix(v, (int)(rnd() % 3 == 0));
    }
  }
  fclose(f);
  printf("{\"event\": \"lptest\", \"lps\": %ld, \"simplex_iters\": %lld, \"refactor\": %lld}\n", cnt, w.st.iters, w.st.refac);
  return 0;
}

static void usage() {
  fprintf(stderr,
          "fastbb solve ROWS BUDGET THREADS CONTEXTS OUTDIR [options]   exact branch-and-bound, resumable per context\n"
          "fastbb dive  ROWS BUDGET DIVES SEED OUT.json [options]       Knuth random-dive estimate of the tree size\n"
          "fastbb lptest ROWS BUDGET DIVES SEED OUT.txt                 LP values for the differential test\n"
          "options: --ktop=200 --dtop=8 --kmid=4 --dmid=12 --klow=2 --rel=8 --pool=48 --anc=1 --cutoff=1 --sbiter=100 --refac=200\n"
          "         --time-limit=SEC --ctx=a,b,c --ctx-limit=K --max-ctx-nodes=N --selfcheck=1\n"
          "         --on-witness=stop|continue (continue: that context stays open, the others go on)\n"
          "         --split-open=L (on resume: replace every open context by its descendants L levels down)\n"
          "         --fullp=8 --sek=8 --candmax=64 (LP pricing)\n"
          "         --adaptive=1 --sbslack=1.0 (verify candidates until the best verified score >= sbslack * next estimate;\n"
          "          at most klow/ktop candidates per node)   --adaptive=0: reliability branching with --rel\n"
          "exit codes: 0 closed, 3 WITNESS, 5 partial (time limit), 4 a context exceeded --max-ctx-nodes, 2 error\n");
}
int main(int argc, char** argv) {
  if (argc < 7) { usage(); return 2; }
  std::string mode = argv[1];
  Problem P;
  if (!P.load(argv[2])) { fprintf(stderr, "cannot read row file %s\n", argv[2]); return 2; }
  P.budget = atoi(argv[3]);
  if (P.budget < 0 || P.budget > P.N) { fprintf(stderr, "bad budget\n"); return 2; }
  Opt opt;
  std::vector<int> only;
  int ctxLimit = 0, splitOpen = 0, slice = 0;
  for (int i = 7; i < argc; i++) {
    std::string a = argv[i];
    size_t e = a.find('=');
    if (a.rfind("--", 0) != 0 || e == std::string::npos) { usage(); return 2; }
    std::string k = a.substr(2, e - 2), v = a.substr(e + 1);
    if (k == "ktop") opt.ktop = atoi(v.c_str());
    else if (k == "kmid") opt.kmid = atoi(v.c_str());
    else if (k == "dmid") opt.dmid = atoi(v.c_str());
    else if (k == "dtop") opt.dtop = atoi(v.c_str());
    else if (k == "klow") opt.klow = atoi(v.c_str());
    else if (k == "rel") opt.rel = atoi(v.c_str());
    else if (k == "pool") opt.poolSize = atoi(v.c_str());
    else if (k == "anc") opt.useAnc = atoi(v.c_str());
    else if (k == "cutoff") opt.cutoff = atoi(v.c_str());
    else if (k == "sbiter") opt.sbIter = atoi(v.c_str());
    else if (k == "refac") opt.refac = atoi(v.c_str());
    else if (k == "selfcheck") opt.selfcheck = atoi(v.c_str());
    else if (k == "on-witness") opt.witnessContinue = (v == "continue");
    else if (k == "adaptive") opt.adaptive = atoi(v.c_str());
    else if (k == "cold") opt.cold = atoi(v.c_str());
    else if (k == "sbslack") opt.sbslack = atof(v.c_str());
    else if (k == "fullp") opt.fullp = atoi(v.c_str());
    else if (k == "sek") opt.sek = atoi(v.c_str());
    else if (k == "candmax") opt.candMax = atoi(v.c_str());
    else if (k == "maxiter") opt.maxIter = atoi(v.c_str());
    else if (k == "time-limit") opt.timeLimit = atof(v.c_str());
    else if (k == "max-ctx-nodes") opt.maxCtxNodes = atoll(v.c_str());
    else if (k == "ctx-limit") ctxLimit = atoi(v.c_str());
    else if (k == "slice") slice = atoi(v.c_str());
    else if (k == "deadpick") opt.deadpick = atoi(v.c_str());
    else if (k == "known") opt.known = atoi(v.c_str());
    else if (k == "forced") opt.forced = atoi(v.c_str());
    else if (k == "stdfb") opt.stdFallback = atoi(v.c_str());
    else if (k == "split-open") splitOpen = atoi(v.c_str());
    else if (k == "ctx") { for (size_t p = 0; p < v.size();) { only.push_back(atoi(v.c_str() + p)); size_t c = v.find(',', p); if (c == std::string::npos) break; p = c + 1; } }
    else { usage(); return 2; }
  }
  if (slice) {
    if (!P.setupSlice()) { fprintf(stderr, "--slice=1: rows base_rows and base_rows+1 must be h(F) >= t and h(Lo) >= b, F/Lo a partition, t + b = budget\n"); return 2; }
    fprintf(stderr, "slice mode: t = %d (row %d, %d states), b = %d (row %d, %d states)\n", P.sliceT, P.capF, (int)P.Fidx.size(), P.sliceB, P.capL, P.Lm.count());
  }
  if (mode == "solve") return runSolve(P, opt, atoi(argv[4]), atoi(argv[5]), argv[6], only, ctxLimit, splitOpen);
  if (mode == "dive") return runDive(P, opt, atoi(argv[4]), strtoull(argv[5], nullptr, 10), argv[6]);
  if (mode == "lptest") return runLpTest(P, opt, atoi(argv[4]), strtoull(argv[5], nullptr, 10), argv[6]);
  usage();
  return 2;
}
