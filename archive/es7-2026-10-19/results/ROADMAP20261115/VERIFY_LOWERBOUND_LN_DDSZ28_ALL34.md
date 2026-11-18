# VERIFY_LOWERBOUND_LN_DDSZ28_ALL34: claim `lb-ln-ddsz28-all34` (verifier VB, 18 Nov 2026, 02:31-02:58 KST)

**Verdict: CONFIRMED.** Every part checked with own code written from the definitions, and with a fresh cake_lpr run:

- (a) **CERTIFIED count, re-run:** cake_lpr (heap 400 MB) on `blocking.cnf` with the kept LRAT, streamed from
  `blocking.lrat.zst` through a FIFO, printed exactly one line, `s VERIFIED UNSAT`. The CNF hash and the stream hash
  are the claim's. Own checks of the CNF: `blocking.cnf` = d28_h.cnf, clause for clause in the same order, followed
  by 34 clauses, which are in order the negations of m0000..m0033 on all 378 variables. All 34 models satisfy C,
  they are pairwise distinct, and m0000 = `d28_h.model`.
- **C is the stated encoding:** an own encoder of `l1enc S 7` (the definitions of ABSAT8_INDEPENDENT §3: R2 rotation,
  AC acyclicity and OCT chain clauses of every convex 6-gon of S) gives the same clause multiset as d28_h.cnf: 30,108
  clauses, namely 18,200 R2, 3,276 AC and 8,632 distinct OCT chains, with 0 differences either way.
- (b) **EXACT:** each of the 34 models is a uniform acyclic chirotope extension. All 102,375 three-term
  Grassmann–Plücker relations through p hold, as does acyclicity on the 3,276 four-sets through p. The x-positions
  where the x-sorted 29-point sign function is a signotope are exactly the claimed ones: 44 in all; 26 models have 1,
  6 have 2 and 2 have 3; the positions are 8 (6 times), 9 (11), 16 (2), 17 (11) and 18 (14).
- (c) **EXACT:** each of the 44 realizations m<k>_t<tt>_Sp.txt has
  - no collinear triple;
  - the labelled order type of S on its first 28 lines (3,276 of 3,276 signs);
  - p's 378 signs equal to the model;
  - S′ strictly increasing in x, with exactly t old points left of p;
  - no convex 7-gon: a C++ brute force over all 1,560,780 seven-subsets finds 0, while there are 23,747-24,473 convex
    6-sets, so the largest convex subset has 6 points.

Not checked: the search narrative (realize_sig.py, enum_ext.py). They only found the objects, and the claim's evidence
does not rest on them.

## 1. Statement checked

The claim says that all abstract one-point extensions of the 28-point DDSZ-type order type S = `agl/ddsz/d28_h.txt` are
realizable. In full:

- (a) C = `l1enc S 7` has exactly 34 models (CERTIFIED).
- (b) Each model is a uniform acyclic chirotope on 29 elements with 1-3 valid x-positions, 44 in all (EXACT).
- (c) Each of the 44 (model, position) pairs has an integer realization (EXACT):
  - 29 points in general position;
  - the first 28 points have the labelled order type of S;
  - p's signs are the model;
  - there is no convex 7-gon.

Definitions as in the claim:
- orient(a,b,c) = sign det(b−a, c−a);
- X(a,b) = [orient(a,b,p) > 0] is variable 1 + lexrank(a,b) among a<b<28;
- convex k-gon = k points in convex position;
- signotope = every 4-subset i<j<k<l of the x-sorted points has a sign sequence (ijk, ijl, ikl, jkl) with at most one
  change.

## 2. Method (own code, `W = /home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/lb-ln-ddsz28-all34/`)

- `vb_all34.py` (Python, exact integers) does the following.
  - **E, own encoder.**
    - R2: for each point a, take u_x = ε_x(x−a) in the half-open upper half-plane, sorted by exact cross products.
      For every i and k ≥ i+2, emit the two clauses (¬S_i ∨ S_{i+1} ∨ ¬S_k) and (S_i ∨ ¬S_{i+1} ∨ S_k), where S_x is
      the literal "ε_x·orient(a,x,p) > 0".
    - AC: for every triangle, p lies on the third vertex's side of at least one edge.
    - OCT: enumerate the convex 6-sets of S incrementally from the 4-point test (20,183 of them, and 0 convex
      7-sets in S). Put each in ccw order around its leftmost vertex. For each cyclic chain (q_{i−1}, q_i, q_{i+1},
      q_{i+2}), emit ¬sees(q_i,q_{i+1}) ∨ sees(q_{i−1},q_i) ∨ sees(q_{i+1},q_{i+2}), where sees(x,y) = orient(x,y,p) < 0;
      chains are deduplicated.
    - Compare with d28_h.cnf as sorted clause multisets.
  - **A.** blocking.cnf prefix and tail; the models satisfy C and the own CNF; distinctness; model 0.
  - **B.** χ on 29 elements: real signs on S, the model on the triples through p, alternating. For every 5-set
    through p and every pivot, the three GP products are not all equal. For every triple of S, the four λ-signs of
    {a,b,c,p} are not all equal (acyclicity). For every t = 0..28, test the signotope property on the 4-subsets through
    p; the 4-subsets of S are monotone since S is x-sorted, and this is also checked.
  - **C.** The exact part of (c) for the 44 files.
- `bf.cpp` (C++, `__int128` determinants; VB's 16 Nov brute force with a kmax argument) counts, for every file, the
  k-subsets (k = 4..7) all of whose 4-subsets are convex, by full enumeration.
- `vb_count.py` is a COMPUTED cross-check only. Enumerating all models of C with pysat (CaDiCaL 1.5.3 and Glucose 4,
  blocking on all 378 variables) gives 34 models with each solver, equal as a set to m0000..m0033.
- `run.sh` ran the cake_lpr re-run, bf on all 44 files and vb_all34 in one unit, `esr-agv-vb-all34` (95 %, 1500M,
  under `vb1118/unit.lock`). vb_all34 was then re-run in the foreground (8 s) after a file-name fix: the files use
  two-digit t, `t08`, `t09`. The first run had found only 27 of the 44 files.

## 3. Results

| check | result |
|---|---|
| S: collinear triples; x strictly increasing | 0; yes |
| own encoder vs d28_h.cnf (`p cnf 378 30108`) | equal as multisets: R2 18,200 + AC 3,276 + OCT 8,632 = 30,108; 0 / 0 differences |
| models: complete, satisfy C, satisfy own CNF, pairwise distinct, m0000 = d28_h.model | 34/34, 34, 34, yes, yes |
| blocking.cnf (`p cnf 378 30142`) = C in the same order + negations of m0000..m0033 in order | yes |
| fresh cake_lpr, heap 400 MB: stdout | exactly `s VERIFIED UNSAT` (1 line); CNF SHA-256 `5b092707…`, LRAT stream SHA-256 `54059812cb70c34a004c7da4af2237da4abe6ad2775112cd9cabd376f7bee966`, 72,876 bytes (= the claim's certify.jsonl); max RSS 59 MB |
| GP relations through p (102,375 per model) / acyclicity (3,276 per model) | 0 / 0 violations in all 34 models |
| valid x-positions | 44, equal to the claim's per model (models.jsonl `valid` and `verify` keys) |
| realizations: files, exact part OK | 44 / 44 (largest abs coordinate 22,343,147) |
| bf: collinear, convex 7-subsets, convex 6-subsets | 0, 0 of 1,560,780, 23,747-24,473 (each of the 44) |
| pysat model enumeration (COMPUTED) | 34 = listed set (both solvers) |

## 4. Controls

- **bf.** A convex heptagon gives k7 = 1 (`ctrl_hept.txt`), and 10 points on a parabola give every k-subset convex.
  The same counts as on 16 Nov for `m0000_t18_Sp.txt`: 15,625 / 31,582 / 24,125 / 0.
- **Negative controls** (perturbed copies in `W/ctrl/enum`, `ctrl/summary.txt`):
  - model 5 with variable 100 flipped: it violates C (33 of 34 satisfy), the blocking tail no longer matches, and it
    has 422 GP and 3 acyclicity violations and no valid position;
  - two lines of S′ swapped in m0000_t18: 26 triple signs differ and the x-order breaks;
  - p moved by (+7, −11) in m0001_t16: 1 p-sign differs and the x-position changes.
  - Each was flagged.

## 5. Reading and limits

- Under the claim's definition (abstract one-point extension = model of the ABSAT CNF C), the statement is fully
  checked.
- The broader reading, "every uniform acyclic one-element extension of S without a convex 7-gon is a model of C",
  needs the soundness of C for abstract extensions:
  - R2 is a three-term GP relation at pivot a;
  - AC is acyclicity on {a,b,c,p};
  - OCT uses the realizability of uniform acyclic rank-3 oriented matroids on at most 8 elements (ABSAT8_INDEPENDENT
    §3, "abstract reading", a remark not checked here or there).
- Nothing about ES(7) follows (29 < 32), as the claim says.

## 6. Files (W as above)

| file | SHA-256 |
|---|---|
| `vb_all34.py` | `08146c0f153c5155ad106a41d60f0c5ec3e5167a89ce57bd2d673ee6e9f8ed9c` |
| `bf.cpp` / `bf` | `f51fcf89b1bc73a9c53fd5ba5748a05d04b24927ea80d85ba83859e404f2e2db` / `fb160872d7263779d49007f29eda24fa96c97e96096f544d650dca8f8c892ff3` |
| `vb_count.py` | `03426ccb10417bf96e3b710b70fa2f958cb29bc1274bba7ff3fdcb2f1988b54b` |
| `run.sh` | `1c0f7146246bb12a450ba7c0625c4dfecd5a58771edfb2baadec48eb6f6b6c19` |
| `vb_all34.json` (all results) | `ca14274ed5d16de1dd5fccfe7a4e35b8398b86df803b159788037ad01f2c5e0a` |
| `bf_all.out` | `5befc59b5a15fd6ee3f619c0ed4551313fac6d76441f6ddf1f6cfa88ebec7d0d` |
| `cake/rerun.jsonl`, `cake/blocking.cake.out` | `105f245b4f12933dbc25592be9c2ebc887a16644e3fe4d759fbb90e2816219d9` |
| inputs: d28_h.txt / d28_h.cnf / d28_h.model / blocking.cnf / models.jsonl | `726c3a9e…` / `79fd77b6…` / `cb0ce33a…` / `5b092707…` / `34a2b1a0…` (full hashes in `vb_all34.json` → `inputs`) |

Re-run:

```bash
W=/home/jay/research/data/roadmap-20261115/pm1115/vb1118/claims/lb-ln-ddsz28-all34; cd $W
bash run.sh    # about 10 s; one cake_lpr at heap 400 MB
```
