# C3PLAN: what it would take to close the 3-fold class

Task: `TASK.md` (commit 3d83517), time budget H = 1.25 h, one 4-core VM (`env.txt`), 00:44–01:59 UTC
on 2026-10-21. Paths below are relative to `cloud/es7-2026-10-19/`. "core-s" / "core-h" are summed
per-node solve + check seconds from the `out.jsonl` records. These are not wall clock: the waves
ran 3 jobs on 4 cores, so each number is a little inflated.

Data snapshot: all `results/C3WAVE1/*/out.jsonl` and `results/C3WAVE2/*/out.jsonl` as of the last pull
(01:10 UTC, branch es7-cloud at 3691ba2b). Wave 2 was still running then (until about 02:00 UTC), so its rows will grow.

## 1. Measured cost so far

`stats.tsv` (one row per depth-2 root, 1,630 rows) is made by `scripts/stats.py`. A root counts as
closed when every leaf of its tree is certified. That means a record with `certified: true` (lrat-check
E2 `c VERIFIED` and cake_lpr `s VERIFIED UNSAT`), or a split record whose `tree_children` are all closed.
**No SATISFIABLE record exists** in any wave record.

| top case | layer 2 | roots | closed | partial | untouched | core-h spent (solve + check) |
|---|---|---|---|---|---|---|
| H3 | one | 5 | 0 | 0 | 5 | 0.0 |
| H3 | two | 95 | 0 | 0 | 95 | 0.0 |
| H6(1,0) | one | 9 | 9 | 0 | 0 | 11.6 |
| H6(1,0) | two | 144 | 144 | 0 | 0 | 3.1 |
| H6(1,1) | one | 9 | 0 | 9 | 0 | 55.5 |
| H6(1,1) | two | 144 | 103 | 36 | 5 | 164.9 |
| H6(2,0) | one | 9 | 1 | 5 | 3 | 7.9 |
| H6(2,0) | two | 144 | 68 | 0 | 76 | 1.5 |
| H6(2,1) | one | 9 | 0 | 1 | 8 | 4.5 |
| H6(2,1) | two | 144 | 10 | 12 | 122 | 8.9 |
| H6(3,0) | one | 9 | 0 | 1 | 8 | 0.5 |
| H6(3,0) | two | 144 | 2 | 0 | 142 | 0.0 |
| H6(3,1) | one | 9 | 0 | 0 | 9 | 0.0 |
| H6(3,1) | two | 144 | 0 | 0 | 144 | 0.0 |
| H6(4,0) | one | 9 | 0 | 0 | 9 | 0.0 |
| H6(4,0) | two | 144 | 0 | 0 | 144 | 0.0 |
| H6(4,1) | one | 9 | 0 | 0 | 9 | 0.0 |
| H6(4,1) | two | 144 | 0 | 0 | 144 | 0.0 |
| H6(5,0) | one | 9 | 0 | 0 | 9 | 0.0 |
| H6(5,0) | two | 144 | 0 | 0 | 144 | 0.0 |
| H6(5,1) | one | 9 | 0 | 0 | 9 | 0.0 |
| H6(5,1) | two | 144 | 0 | 0 | 144 | 0.0 |
| **all** | | 1630 | 337 | 64 | 1229 | 258.5 |

Per-node buckets (all wave records; `scripts/estimate.py` prints them as `c_b`;
s = σ_a of the top case, l2 = layer-2 type, d = depth, o = orbits in the newest layer):

| s / l2 / d / o | attempted | certified | timeouts | mean solve s | mean check s (certified) |
|---|---|---|---|---|---|
| s0/one/3/1 | 131 | 128 | 0 | 76.7 | 39.4 |
| s0/one/3/2 | 1530 | 1526 | 0 | 16.7 | 20.5 |
| s0/two/2/2 | 214 | 214 | 0 | 45.6 | 32.2 |
| s1/one/3/1 | 80 | 0 | 80 | 300.1 | 0.0 |
| s1/one/3/2 | 794 | 783 | 11 | 123.8 | 33.2 |
| s1/one/4/1 | 189 | 189 | 0 | 50.8 | 28.2 |
| s1/one/4/2 | 797 | 795 | 0 | 41.2 | 25.4 |
| s1/two/2/2 | 161 | 84 | 77 | 190.2 | 35.4 |
| s1/two/3/2 | 2639 | 2638 | 0 | 30.6 | 25.7 |
| s1/two/4/1 | 2097 | 2083 | 0 | 6.7 | 15.8 |
| s1/two/4/2 | 19462 | 19462 | 0 | 5.5 | 14.9 |

**Which roots are hard and what they share** (`stats.tsv`; `scripts/estimate.py`):

"Partial" mixes two things. Wave-1 roots ran until the wave ended. A wave-2 root got only a
10-minute slice with 3 jobs (`results/C3WAVE2/README.md`), so a wave-2 partial root may simply have
run out of time. "Hard" below means that nodes timed out at their cap.

- **The top-case bit s = σ_a decides it.** No s = 0 node has ever timed out (bucket table: 0
  timeouts in every s0 bucket). Every measured two-orbit s = 0 root is closed (H6(1,0) 144,
  H6(2,0) 68, H6(3,0) 2), at depth 2, for a mean of 78 core-s per root. One-orbit s = 0
  roots cost about 4,600 core-s each (9 closed H6(1,0) roots, 120 depth-3 leaves each). The 6
  partial one-orbit s = 0 roots (`0s0-2s0_{3,6,7,9,10}`, `0s0-3s0_5`) are wave-2 slices that ran out
  of time with 3–100 untried depth-3 nodes and no timeout. Every root with timeouts is an s = 1 root.
  C3-S points the same way: H6(4,0) had 139 of 144 two-orbit depth-2 children closing at 300 s
  (`results/C3-S/README.md`, Measurements 7).
- **One-orbit layer 2 under s = 1 is the hardest stratum.** None of the 10 (0 closed) measured roots
  (all 9 of H6(1,1), plus `0s0-2s1_1`) is closed. The wave-1 ones (`0s0-1s1_{2,3,4,6,7,10}`,
  `0s0-2s1_1`) have spent 9,000–41,000 core-s each and still have 375–4,299 open nodes
  (`0s0-1s1_4`: 1,329 at depth 4 and 2,970 at depth 5). Their depth-3
  single-orbit children (single below single) timed out at 300 s **80 times out of 80**.
  That is 6.7 core-h of pure timeouts that a pre-split would have avoided (bucket s1/one/3/1).
- **Two-orbit layer 2 under s = 1 is bimodal.** Of 161 measured roots, 113 are closed and 48 partial. The closed ones cost median 122 and mean 3834 core-s, max 16390.
  When a two-orbit s = 1 root times out at 300 s, its layer split produces 7 pre-split single
  children plus 84 two-orbit children, then 462 depth-4 leaves: **546 certified nodes, about
  6,000–6,500 s solve plus about 9,600 s check per root** (`0s0-1s1_2s1-9s1`, `0s0-1s1_3s1-4s0`,
  `0s0-1s1_4s0-6s1` in `stats.tsv`).
  Mixed layer-2 σ (01, 10) is open somewhat more often than equal σ (00, 11):
  38 of 80 mixed vs 10 of 81 equal still open (`stats.tsv`, column l2sigma).
- **Checking costs as much as solving.** Over all records, solve 122.9 core-h and check 135.6 core-h. At depth 4 a node takes
  about 5.5 s to solve and 15 s to check. Most of the 15 s is fixed work per node: the 4.15M-clause
  base CNF is written, hashed and parsed by both checkers. Deep layer trees therefore pay mostly
  for this overhead.
- **H3 (100 roots) and H6(a, ·) for a = 4, 5 have no wave records at all**, and a = 3 has only 3
  roots. Both waves take roots in name order, which puts the H6 roots first, and wave 2 had not
  reached these at the snapshot.

## 2. Total cost of the C3 class with the current method

Method: `close_tree.py`, caps 300/300/600, `--split-singles`, CaDiCaL `--sat`, dual check.
Model (`scripts/estimate.py`, full description in its docstring):
- A closed root costs what it actually spent.
- A partial root costs what it spent plus, for each open node, the mean cost c_b of its bucket
  (low 0.5 c_b, high 3 c_b, because open nodes are the harder ones).
- A stratum without data borrows the per-root costs of the measured strata with the same
  (s, layer-2 type). The s-dependence is strong and the a-dependence is weak in the data we have.
- H3 takes the C3-S Knuth walks (`results/C3-S/README.md` "Measurements" 6: median 446, lowest 218,
  heaviest 6.8·10^5 solve core-h for the whole H3 stratum), × 1.27 for checking.

| stratum | roots | measured(closed/partial) | per_root_core_h(low/mid/high) | stratum_core_h(low/mid/high) | source |
|---|---|---|---|---|---|
| H3/one | 5 | 0/0 | 2.77/5.66/8636.00 | 14/28/43180 | C3-S Knuth walks (H3 stratum, 100 roots) |
| H3/two | 95 | 0/0 | 2.77/5.66/8636.00 | 263/538/820420 | C3-S Knuth walks (H3 stratum, 100 roots) |
| H6(1,0)/one | 9 | 9/0 | 1.29/1.29/1.29 | 12/12/12 | own roots |
| H6(1,0)/two | 144 | 144/0 | 0.02/0.02/0.02 | 3/3/3 | own roots |
| H6(1,1)/one | 9 | 0/9 | 16.49/26.81/68.10 | 148/241/613 | own roots |
| H6(1,1)/two | 144 | 103/36 | 1.55/1.91/3.35 | 223/275/483 | own roots |
| H6(2,0)/one | 9 | 1/5 | 1.46/1.60/2.17 | 13/14/20 | own roots |
| H6(2,0)/two | 144 | 68/0 | 0.02/0.02/0.02 | 3/3/3 | own roots |
| H6(2,1)/one | 9 | 0/1 | 11.70/18.85/47.46 | 105/170/427 | own roots |
| H6(2,1)/two | 144 | 10/12 | 1.30/2.20/5.80 | 188/317/835 | own roots |
| H6(3,0)/one | 9 | 0/1 | 1.00/1.51/3.58 | 9/14/32 | own roots |
| H6(3,0)/two | 144 | 2/0 | 0.02/0.02/0.02 | 3/3/3 | own roots |
| H6(3,1)/one | 9 | 0/0 | 16.01/26.02/66.04 | 144/234/594 | borrowed: all measured s1/one roots |
| H6(3,1)/two | 144 | 0/0 | 1.51/1.95/3.69 | 218/281/531 | borrowed: all measured s1/two roots |
| H6(4,0)/one | 9 | 0/0 | 1.33/1.42/1.76 | 12/13/16 | borrowed: all measured s0/one roots |
| H6(4,0)/two | 144 | 0/0 | 0.02/0.02/0.02 | 3/3/3 | borrowed: all measured s0/two roots |
| H6(4,1)/one | 9 | 0/0 | 16.01/26.02/66.04 | 144/234/594 | borrowed: all measured s1/one roots |
| H6(4,1)/two | 144 | 0/0 | 1.51/1.95/3.69 | 218/281/531 | borrowed: all measured s1/two roots |
| H6(5,0)/one | 9 | 0/0 | 1.33/1.42/1.76 | 12/13/16 | borrowed: all measured s0/one roots |
| H6(5,0)/two | 144 | 0/0 | 0.02/0.02/0.02 | 3/3/3 | borrowed: all measured s0/two roots |
| H6(5,1)/one | 9 | 0/0 | 16.01/26.02/66.04 | 144/234/594 | borrowed: all measured s1/one roots |
| H6(5,1)/two | 144 | 0/0 | 1.51/1.95/3.69 | 218/281/531 | borrowed: all measured s1/two roots |

(`estimate.txt`, made by `scripts/estimate.py`; core-h are solve + check.)

**Result: about 3,194 core-hours (range 2,101 – 7,979) with the current method.** That is
1,065 machine-hours of the 4-core VMs used here at 3 jobs per VM (798 at 4 jobs).
The range has an unbounded tail from H3. One of the 8 H3 Knuth walks extrapolates to 6.8·10^5 solve
core-h. If that walk is representative, the total is about 869,444 core-h and the method cannot
finish H3. The upper end 7,979 uses the second-heaviest H3 walk (1,681) instead.

Where it goes (mid): s = 1 one-orbit about 1113 core-h for 45 roots, s = 1 two-orbit about
1435 core-h for 720 roots, H3 about 566 core-h (Knuth walk only), and all s = 0 strata
together about 81 core-h.

**Comparison with the C3-S Knuth walks** (`results/C3-S/README.md` "Measurements" 6, solve only).
Check is about as large as solve here, so the walk numbers should be compared with about half of
the measured totals:
- The unstratified walks gave 3,080 ± 2,417 solve core-h, and C3-S's headline was "about 1,500
  core-h if the H3 tail is mild". The measured H6 part alone is about 2,629 core-h (solve +
  check), roughly 1,249 solve, so the total sits at the upper end of the C3-S guess.
- "H6, budget 100k at depth 2: 39 ± 17": a large **underestimate** for the H6 two-orbit strata
  (measured about 1,450 core-h). The 4 walks all landed in easy s = 0 / quickly closing nodes
  and never saw the s = 1 timeouts, which cost about 15,800 core-s each.
- "H6 one-orbit subtrees from depth 3: 469 ± 141": consistent with the measured one-orbit total of
  about 1,179 core-h solve + check (about half of it solve).

## 3. Ways to make it cheaper (with evidence)

### 3a. Mirror reduction below every H6 case (sound; proof below): about 47% of the H6 roots

**Lemma H6M.** Fix a top case H6(a, s) (1 ≤ a ≤ 5, s ∈ {0, 1}, m = 11). For residues r ∉ {0, a}
define φ(r, σ) = ((a − r) mod m, σ ⊕ [r < a] ⊕ [s = 0]), with σ = None kept as None for one-orbit
layers. φ is an involution on the layer-2 options of H6(a, s). If S has a canonical labelling
(Lemma 2 of `results/C3-S/soundness.md`) in case H6(a, s) with layer path (L_1, L_2, ...), then
M(S), its mirror image in l, has a canonical labelling in the same case H6(a, s) with layer path
(L_1, φ(L_2), φ(L_3), ...).

Proof. Start as in Lemma 5 of `soundness.md`, which never uses |H| = 3 in these steps. M(S) is in
the class. With the same l and then l turned just past the line of the point now labelled n − 1
(the image of label 0), M(S) gets labels i ↦ (−i) mod n, σ'_0 = 0 and σ' = 1 − σ for every other
label. Residue r goes to residue m − r with σ'_{m−r} = 1 − σ_r. So the hull of M(S) is
{orbit 0, orbit a'} with a' = m − a ≥ 6, and σ'_{a'} = 1 − s. This labelling is valid except for
a ≤ 5. As in Lemma 2(a)(c), move label 0 to the point with label t = a' by turning l to just before
the line of label t. Every label i becomes (i − t) mod n. The lines of labels 0..t−1 are swept, and
exactly those points change side of l, so their σ flips (the same step as in Lemma 5). Then:

- The new label 0 is old label t (not swept), with σ = σ'_t = 1 − s.
- The new label a is old label a + t = m (not swept, since m ≥ t), with σ = σ'_m = 1 − σ'_0 = 1.
- For a residue r ∉ {0, a} of S: the mirrored residue is r' = m − r, and the new residue is
  ρ = (r' − t) mod m = (a − r) mod m. Its new label ρ is old label ρ + t, which is < n and ≥ t, so
  it is not swept.
  - If r < a: ρ + t = m − r = r', with σ'_{r'} = 1 − σ_r.
  - If r > a: ρ + t = 2m − r = r' + m, with σ'_{r'+m} = 1 − σ'_{r'} = σ_r.

  So σ_ρ = σ_r ⊕ [r < a].
- Finally Lemma 2(b): if the new σ_0 = 1 − s is 1, that is s = 0, apply p ↦ −p. It keeps the labels
  and flips every σ. Afterwards σ_0 = 0, the other hull residue is a ≤ 5, and
  σ_a = 1 ⊕ [s = 0] = s, so M(S) is in case H6(a, s). Every other residue r maps to
  ((a − r) mod m, σ_r ⊕ [r < a] ⊕ [s = 0]) = φ(r, σ_r).

M is affine, and relabelling and p ↦ −p do not change the point sets, so the convex layers of M(S)
are the images of those of S, and the layer path maps as stated. For a one-orbit layer, σ is not
part of the node (Lemma 3). φ is an involution: (a − (a − r)) = r, and [r < a] = [(a − r) mod m < a].
∎

**Corollary (cover).** Below each H6(a, s), keep a layer-2 option O iff key(O) ≤ key(φ(O)), as
`h3_layer2_kept` does for H3. If every kept subtree is refuted, then for any S in H6(a, s), either S or M(S)
(with the labelling above) has a kept layer 2 and satisfies the base CNF and the units of a refuted
node (Theorem of `soundness.md`), which is a contradiction. With m = 11 this keeps **81 of 153 options
in every H6 case** (5 of 9 one-orbit, 76 of 144 two-orbit; 9 self-mirror options). All 1,530 H6
roots become 810. φ maps every option to an option (`scripts/validate_mirror_h6.py` and the count
in `logs/h6_mirror_counts.txt`).

Evidence beyond the proof:
- **Exact-coordinate validation** (`scripts/validate_mirror_h6.py`, `logs/validate_mirror_h6.jsonl`).
  It adapts C3-S `validate_mirror.py`. S and M(S) are canonicalized independently, by random
  search for l plus the a ≤ m//2 rule, then σ_0 = 0. For m = 7, 9, 11, 300 hexagonal-hull sets
  each, all 10 H6 cases occur at m = 11. **0 failures over 900 sets and 3,604 layers.** The
  mutation without the σ rule fails on 162 of 900 sets.
- **Measured cost of mirror pairs**: in `stats.tsv`, for the 93 H6 root pairs (O, φ(O)) with both
  closed, the median ratio of their costs is 1.18 (`0s0-1s1_2s0-9s0` 16,390 core-s vs its image
  `0s0-1s1_3s0-10s0` 15,074). Half of the H6 work so far was spent on mirror images.
- Not yet done: integrating it into `hullcase.tree_children` and `compose.py`, and an
  independent audit. The proof should be checked by C3AUDIT before any certified node is dropped.

### 3b. Split hard two-orbit nodes on σ bits instead of on the next layer: mixed, 1 of 3 nodes 16.6× cheaper

`scripts/sigma_cubes.py` takes a node, picks the 3 smallest residues r ≠ 0 outside its layers, and
solves the 2^3 cubes σ_r ∈ {0, 1}. The cubes cover every assignment, so the node is closed iff all
cubes are UNSAT. Same CNF construction, CaDiCaL `--sat --lrat`, and both checkers as
`close_tree.py`, 3 jobs on 4 cores. Every UNSAT below was **checked by both lrat-check (E2) and
cake_lpr** (`logs/sigma_cubes.jsonl`). The three nodes are depth-2 two-orbit s = 1 roots that timed
out at 300 s in wave 1, so their layer split is measured in full:

| node | layer split (wave 1, `stats.tsv`) | 8 σ-cubes, this run |
|---|---|---|
| `0s0-1s1_2s1-9s1` | closed: 546 nodes, solve 6,249 + check 9,579 = 15,828 core-s | **closed: 8/8 certified at cap 150, solve 693 + check 260 = 953 core-s (16.6× less)** |
| `0s0-1s1_3s1-4s0` | closed: 546 nodes, 6,537 + 9,809 = 16,346 core-s | 6/8 certified at cap 150 (99–142 s each), 2 UNKNOWN; spent 1,033 + 243 = 1,276 core-s |
| `0s0-1s1_4s0-6s1` | closed: 546 nodes, 6,477 + 9,662 = 16,139 core-s | 2/8 certified at cap 120 (91 s, 119 s), 6 UNKNOWN at 120 s; spent 951 + 58 core-s |

Solver time used in all experiments: 2,677 s of the 45-minute budget (2,700 s), on 3 nodes.
On the node that closed, the gain comes mostly from cutting per-node overhead: 8 nodes instead
of 546. The other two nodes show that 3 σ bits are not always enough within 120–150 s.
The open cubes would need another level of splitting, either 3 more σ bits or the layer split below
the cube, and that level was not measured. If each open cube cost as much again as the measured
cubes, the second node would cost about 2× and the third about 1× of the layer split
(rough, not measured). **Conclusion: σ-cubes are a promising and cheap first split for a node that
times out at 300 s, but the evidence is 3 nodes with a mixed outcome.** They should be compared with
the layer split on a pilot of about 20 timed-out nodes before they become the default. A cube that
times out should fall back to the layer split (the cover stays trivially sound: a cube node's
children are its layer children with the same σ units). Nothing was measured on one-orbit roots or
on H3.

### 3c. Pre-split single-below-single at depth 3 for s = 1 (no measured downside)

All 80 such nodes timed out at 300 s and were then split anyway (bucket `s1/one/3/1`, 80 attempted,
0 certified), wasting 6.7 core-h in 7 roots. Splitting them without a solve gives the same tree for
300 s less per node. This is a one-line change to the `--split-singles` rule. The better option is
to give these nodes σ-cubes (3b) instead of a layer split: the one-orbit roots have 375–4,299 open
nodes each under layer splitting.

### 3d. Smaller items

- **Per-node check overhead**: about 15 s of check per depth-4 node regardless of solve time (bucket
  table). Fewer, larger nodes (3b) is the main fix. Removing clauses satisfied by the node units
  would not help: on `0s0-1s1_3s1-5s0_2s0-6s1_4` it drops only 4.5% of clauses (3,969,337 of
  4,154,921 remain; `scripts/reduce_node.py`, no solver run). Not pursued.
- **Solver options**: C3-S measured `--sat` about 1.4× faster, and `--unsat`, `--elim=false`,
  `--chrono=0` no better (`results/C3-S/logs/cadical_options.jsonl`). Not re-measured here.
- **march_cu** on top cases gives cubes that time out (C3-S Measurements 3). With more time, the
  next step would be march_cu below a layer node at depth 2. It was not tried here because
  σ-cubes already work on the nodes tested.
- **Encodings**: C3a chain is the fastest of those measured (C3-S Measurements 4: chain
  12.5 s / 45.7 s vs conv 69 / 129, C3b chain 20 / 52). Nothing new here.

**Combined estimate.** The mirror reduction (3a) gives 1,986 core-h mid (range 1,260 –
5,300, H3 unchanged; `scripts/estimate.py` "with H6 mirror"). σ-cubes (3b) might reduce the s = 1 tail further,
but 3 nodes with a mixed outcome do not support a number.

## 4. Plan for the next wave

Order matters more than size: close what is cheap and certain first, then measure the unknowns
(H3 and a = 3..5) before spending heavily.

0. **Before launch (one session, ~2 h, no machines): audit and implement H6M.** Add `mirror_h6` to
   `hullcase.tree_children` (same pattern as `h3_layer2_kept`, with φ above), extend `compose.py`, rerun
   `validate_mirror_h6.py` with 3,000 sets per m, and have C3AUDIT read the proof. Also add the
   σ-cube split (3b) to `close_tree.py` as `--sigma-split K`: a node that times out at depth 2 or
   at a single-below-single position is split into 2^K σ-cubes, and a cube that times out is split
   on the next K free σ bits before falling back to the layer split. `compose.py` must accept
   cube nodes. The cover argument is trivial (the cubes cover all assignments of K variables), but
   the node naming and sha256 re-derivation must be extended and tested.
1. **σ-cube pilot, 4 machines × 2 h, first.** 20 two-orbit s = 1 nodes that timed out at 300 s
   (the d2 timeouts listed by `stats.tsv`, timeout_then_split_by_depth = d2:1, with a closed layer
   subtree to compare against). Run 3 σ bits at cap 300, then the layer split under any open cube.
   If the median total cost is below half of the 546-node layer split (about 16,000 core-s), use
   σ-cubes as the first split in 3c/3d.
2. **Wave 3a: s = 0 cleanup, 10 machines × 2 h.** All untouched H6(a, 0) roots (mirror-kept only:
   about 81 per case minus those already closed), a = 2..5, caps 300/300/600. Expected about 40
   core-h of work, i.e. a few hours on 10 machines (3 jobs each). Result: **five top cases closed**
   (H6(1,0) is already fully closed). This also measures the a = 3..5 dependence.
3. **Wave 3b: H3 pilot, 10 machines × 3 h, in parallel with 3a.** 30 mirror-kept H3 roots, chosen
   at random, 3 per machine, with the σ-cube split on timeouts. This replaces the Knuth-walk number
   for H3 (the largest uncertainty) with measured per-root costs.
4. **Wave 3c: s = 1 two-orbit, 30 machines × 8 h.** The mirror-kept two-orbit roots of H6(a, 1),
   about 76 × 5 = 380, minus those closed: about 300. Budget, from the s1/two stratum mean of about
   2 core-h per root: about 600 core-h ≈ 200 machine-hours (3 jobs), less if the σ-cube pilot wins.
5. **Wave 3d: s = 1 one-orbit, 25 roots** (5 kept per a), resumed from the 7 partial roots'
   records where kept. One root per machine, 25 machines × 12 h, with σ-cubes below single layers.
   This is the stratum with the most uncertainty in H6.
6. Then H3 in full, sized from the 3b pilot.

**Total with the mirror reduction 3a** (mid): about 1,986 core-h without the σ-cube gain. With 40 machines
× 3 jobs = 120 parallel solves, that is about 17 h of wall time. Whether σ-cubes shorten this is
decided by the pilot in step 1.

**What would show the method cannot finish:**
- the H3 pilot (step 3) extrapolates to more than 10^4 core-h for H3, that is a mean above 100
  core-h per kept root over 30 roots, or more than 3 of 30 roots still open after 3 h with a
  frontier that does not shrink;
- or, in 3c/3d, σ-cubes stop closing: more than 20% of second-level cubes (6 σ bits fixed)
  time out at 600 s. The remaining free σ bits are then not enough, and the tree grows without
  closing, which is what happens to `0s0-1s1_4` under layer splitting (4,299 open nodes).
- Any SAT answer stops everything. It is a candidate counterexample and must be realized.

## Files

`README.md`, `PLAN.md` (this file), `env.txt`, `stats.tsv`, `estimate.txt` (output of estimate.py),
`scripts/stats.py`, `scripts/estimate.py`, `scripts/sigma_cubes.py`,
`scripts/validate_mirror_h6.py`, `scripts/reduce_node.py`, `logs/sigma_cubes.jsonl`,
`logs/sigma_cubes_run.log`, `logs/validate_mirror_h6.jsonl`, `logs/h6_mirror_counts.txt`.
