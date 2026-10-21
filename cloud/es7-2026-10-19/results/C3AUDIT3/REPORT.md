# C3AUDIT3: independent check of σ-cube splitting (C3U)

Task `results/C3AUDIT3/TASK.md` at 3f153540, H = 3.0. Run on 2026-10-21 from 05:37 UTC, from branch head 712efc6b,
on one cloud VM (4 cores, 15 GB; `env.txt`). I built these tools here: CaDiCaL 3.0.1 (c6073042), cake_lpr (a36874a8)
and lrat-check (drat-trim 2e3b2dc with `results/E2/tools/lrat-check-E2.patch`). As a sanity check, lrat-check rejects
`3 0 0` on {1},{−1} and accepts `3 0 1 2 0`. The m = 11 base I rebuilt has header `p cnf 168399 4154921` and sha256
`bf0e502e…dd6da`. C3U was reviewed at its final README, f710546d (finished 06:40 UTC). Its `tools/` last changed at **95cafa93**, which
is the commit the README recommends. Working notes are in `NOTES.md`.

## Verdict

| | verdict |
|---|---|
| **Specification** (`results/C3U/TASK.md` rules 1–5) | **Accept.** Rules 2 and 3 cover their parents. The units never lose a set. The depth ≥ 2 restriction is sufficient and both tools enforce it. Details below. |
| **Implementation** (`results/C3U/tools` at 95cafa93) | **Reject `compose.py` until finding 1 is fixed. Then accept with conditions.** `hullcase.py` and `close_tree.py` match the specification: my driver, written from the specification only, builds the identical tree with identical CNF hashes. `compose.py` has a soundness hole. It is not triggered by any current record, but waves must not use 95cafa93 `compose.py` as the judge. |

Conditions for accepting the implementation:
1. Fix finding 1 in `compose.py`, e.g. `if not ch: missing; return False` in the plain branch of `covered2`.
2. Re-run `tools/forge.py` and `logs/childless_real_m5k6.jsonl` against the fixed version. The childless input must
   come out not covered.
3. Correct the two false statements in `README.md` and `sigma_split.md` (finding 1).
4. Keep `--jobs ≤ 3` for m = 11 cube proofs (cake_lpr ≈ 4 GB each), as C3U says. I saw the same failure (finding 4).

## Findings, most serious first

### 1. `compose.py` covers a childless plain node vacuously — breaks soundness (latent)
- `C3U/tools/compose.py:199` (95cafa93) puts the layer name L itself into `prefixes` for every certified cube record
  `L__C`. C3T used only proper prefixes. Line 203 does the same for split records.
- `compose.py:235-241` then covers a plain node that is in `prefixes` with `for c in children(layers): ok = …`. When
  `tree_children` is empty, the loop body never runs and `ok` stays True.
- A fully layered node L′ (every residue in some layer, so no children) is a real leaf. A set S of the class can have
  exactly that layer path. If only one cube `L′__C` of it is certified, L′ is still counted as covered. Only the part
  of L′ with σ = C was refuted.
- Rule 3 generates such cube names in normal use: the layer split of a cube node whose newest layer uses the last
  free residues. So the hole is reachable from `close_tree.py` output. It does not need forged names.
- The 79a3f3c1 guard ("never vacuously covered", `compose.py:227`) covers only the cube branch, not the plain branch.
- **Evidence:** m = 5, k = 6, with real proofs. Every record is solved by CaDiCaL and accepted by both checkers, and
  the sha is re-derived (`logs/childless_real_m5k6.jsonl`, built by `tools/forge_childless.py` and
  `tools/real_childless.py`). P = `0s0_1s0-2s0`.
  - All other depth-2 nodes are certified, and so are all children of P except A = P_3.
  - A has one child, FULL = `0s0_1s0-2s0_3_4`. FULL is never solved. Only `FULL__3s0-4s0` is certified, which is one
    quarter of FULL: σ_3 and σ_4 are free in FULL, because its layers 3 and 4 are one-orbit layers.
  - **C3U compose (95cafa93): `class_covered: true`.** C3T compose on the same plain records: not covered (frontier
    `0s0_1s0-2s0_3`). My fixed composer: not covered (frontier `0s0_1s0-2s0_3_4`). See `logs/childless_compose.txt`.
- **The same failure from unmodified `close_tree.py` output** (`logs/natural/`, see its README.txt): m = 5, k = 6.
  - Run A: C3U `close_tree` from `0s0` with `-c 1`, no σ-split.
  - Run B: C3U `close_tree` from `0s0_2` with `-c 1` and `--sigma-split 2`.
  - C: the 46 fully layered cube leaves that B left with 0 children, solved afterwards, all certified. A later
    `close_tree` run with those leaves as ROOT does the same.
  - On A + C, C3U compose reports a frontier of 31 nodes, and my brute force finds 36 holes. **5 fully layered plain
    nodes are counted covered** (no uncovered ancestor in C3U's frontier list), although only one σ half of each is
    certified. Example: `0s0_2_1_3s0-4s1`, where only `__1s1-3s0` is certified; brute force leaves 2 σ vectors of it
    unrefuted. My fixed composer reports a frontier of 52.
  - This is the "earlier wave split the node by layers, a later wave σ-split it" situation the task asked about: the
    layer route of `0s0_2` comes from A, the cube certificates from B and C.
- **Reach today:** the wave records at 712efc6b use at most 7 of the 11 residues, so no record is fully layered. Every
  covered/not-covered answer so far is unaffected. The hole opens once rule-3 splits below cubes reach full depth.
- **Wrong statements** (final README f710546d): `sigma_split.md:82` and `README.md:27` say the plain-node rule is "the C3T rule unchanged".
  `README.md:37` says compose "does not count such a node as covered". Both are false for plain nodes.
- My own composer had the same hole on its first version, because I followed the same specification. I fixed it
  (`tools/mycompose.py`: a node without children is covered only if certified). Every comparison below was run or
  re-run with the fixed version.

### 2. `close_tree.py` drops a timed-out childless node from the frontier — misleading, not a soundness break
`close_tree.py:194-196` (95cafa93) writes `{"split": true, "children": 0}` for a fully layered node that timed out,
and the node leaves the frontier. The run can then print `open_frontier: 0` without a proof of that node. Reproduced: run A above (C3U `close_tree`, m = 5,
k = 6, `-c 1`) prints `{"open_frontier": 0}` while 52 fully layered nodes timed out and were never refuted. Both
composers report them uncovered. This
behaviour is inherited from C3T, and the C3U README states it. `compose.py` is the judge: it catches cube nodes, and
catches plain nodes only once finding 1 is fixed. Suggestion: keep such a node on an "unsplittable" list and print it.

### 3. `close_tree.py` restart reads sigma_cubes.py records wrongly — cosmetic
`close_tree.py:115-117` marks `r["node"]` as done for every certified record. In a `sigma_cubes.py` record, `node` is
the **parent** and `cube` holds the bits. If such a file were given as `OUT`, the parent would count as closed after one
cube. This matters only if someone mixes the formats. `compose.py` reads these records correctly.

### 4. Checker memory — operational
With a parallel m = 8 run on the VM, cake_lpr printed nothing (`"none"`) for 2 of 3 m = 11 cube proofs. Re-run alone,
it accepted both. C3U hit the same failure in its test 4. The tools handle it safely: the record is not certified, and
`close_tree` stops with `PROOF NOT ACCEPTED`. Waves need the memory headroom.

## Specification review (step 1)

- **Rule 1 (CNF):** an assignment satisfies `L__C` exactly when it satisfies L and σ_r = v for every (r, v) in C. The
  σ literals are the base's (`c3cnf.sig`: σ_{r+m} = ¬s_r, σ_{r+2m} = s_r), and σ_r is defined for every S by its
  canonical labelling. So the units remove only assignments outside the cube. A certificate refutes exactly the sets in
  the cube.
- **Rule 2 cover:** the 2^K children run over all assignments of K distinct bits that are not in C, so every S in the
  parent is in exactly one child. "Smallest free" is not needed for soundness. It only fixes the names. Residue 0 (σ_0
  = 0) and the residues of layers are excluded, which is harmless.
- **Rule 3 cover and dropped options:** an S in `L__C` with a next layer O has L + O in `tree_children(L)`. At depth
  ≥ 2 there is no mirror reduction, so the child is there. O's explicit σ values are S's true values, which agree with
  C, so the child is not dropped. A dropped option would need σ_r = s ≠ v = σ_r. One-orbit layers carry no σ.
- **Depth 1:**
  - The only reductions that do not keep every set are Lemma 5 (H3 mirror: S ↦ M(S), with σ ↦ 1 − σ and r ↦ m − r),
    Lemma H6M (`--mirror-h6`, off), and the root normalizations (label 0, σ_0 = 0, a ≤ m // 2). The mirror reductions
    act only on the children of the depth-1 nodes: `hullcase.py:192` needs `layers == [[(0, 0)]]`, `:194` needs
    `len(layers) == 1`. The root normalizations act at depth 0.
  - So the mirror is applied first: S is replaced by M(S) whose layer 2 is kept. Only then are cubes considered, below
    a kept depth-2 node, and they cover all of that node.
  - Requiring ≥ 2 layers is therefore sufficient. It is enforced in `close_tree.py:188`, in `compose.py:153` (record
    → exit 1) and in `compose.py:160` (implied split not used). Rule 3 children of a cube node have ≥ 3 layers, and
    `tree_children` applies no reduction there.
  - `--split-singles` pre-splits are plain layer splits and touch no σ. With cubes they use the rule-3 children.
  - Tests: a σ-split record at `0s0` is rejected, and sigma_cubes records of `0s0` alone are not covered (forge
    05, 05b, 05c).
- **Earlier waves that split the same node by layers:** a node is covered through its σ-split **or** through its layer
  children. Both routes are complete covers, and the composer never mixes half of one with half of the other. A
  node's coverage depends only on its name, because the name fixes the CNF, so memoizing by name is sound. The one
  gap is finding 1, which is in how the plain route is explored, not in the rules.

## Own composer and tests (step 1)

- **`tools/mycompose.py`:** grown from `results/C3AUDIT/tools/mycompose.py`, whose unmodified copy is the first
  commit. Written from the specification only. It has its own name parser, tree (C3-S tree with the H3 mirror and no
  H6 mirror), rule 2/3 children, and its own re-implementation of the layer units. It re-derives every certified
  record's CNF sha256. From the repository it imports only `C3a/c3cnf.py` (variable numbering).
- **`tools/xcheck_tree.py`:** 465 comparisons with `hullcase.py` (children, units, rule-3 children, σ children) for
  (m, k) ∈ {(5,6), (6,6), (7,5), (7,6), (7,7), (9,7), (11,7)}, depth ≤ 3. 0 mismatches.
- **`tools/mydriver.py`:** my own small-instance closer, rules 1–4, with deterministic conflict limits.

  | run | instance | solves | σ-splits | nested (\|C\| = 2K) | cube layer splits | rule-3 dropped | both composers |
  |---|---|---|---|---|---|---|---|
  | t1 | m=7 k=6 K=2 | 137 | 6 | yes | 4 | 104 | covered, 126 certified |
  | t2 | m=7 k=6 K=3 | 401 | 3 | no (m ≤ 7) | 16 | 312 | covered, 381 |
  | t3 | m=6 k=6 K=2 | 316 | 15 | yes | 23 | 414 | covered, 277 |

  **t1 is identical to C3U's `sig_m7k6c300K2`:** the same 126 certified names with the same `cnf_sha256`, and the same
  11 split records (σ bits and child counts). My driver and C3U's `close_tree.py` were written independently.
- **`tools/forge.py`:** 18 cases, run on t1, t2 and t3 against C3U compose 95cafa93 and against mine. **18/18 pass
  on each.** Expected outcomes:
  - Rejected (exit 1): wrong cube `cnf_sha256`; `sigma_bits` not the smallest, reversed, or strings; σ-split record
    at depth 1, alone or with cubes; wrong `base_sha256`.
  - Not covered: a missing cube; a non-conflicting rule-3 child dropped; sigma_cubes records of a depth-1 node; an
    implied split with 3 of 4 cubes, or on non-smallest bits; a cube certified only under an unsorted name; a cake
    line that is not exact; a cube node's layer split record missing.
  - Covered: the original records; a correct implied split from sigma_cubes records.
- **Childless input** (finding 1): the one case where C3U compose and my fixed composer differ.
- **`tools/mybrute.py`:** a brute-force cover check independent of every composer and of the split records. Every
  maximal path of my tree, with every σ vector consistent with it, must be matched by a certified leaf
  (`logs/mybrute.txt`).
  - 0 holes on t1, t2, t3 and on the 4 regenerated C3U runs.
  - 1 hole on the childless input (`0s0_1s0-2s0_3_4`, 3 of its 4 σ vectors unmatched). This confirms that C3U's
    "covered" there is wrong.
- **forge.py also passes 18/18** on C3U's m = 7 c100 run (1,104 certified, 69 cube layer splits) and on its m = 8 K = 3
  run (nested K = 3) (`logs/forge_c3u_sig_m8k6c300K3.txt`).
- **Reproducibility:** I re-ran C3U's `run_small.sh sig` here with C3U's tools. The m = 6 and the three m = 7 runs give
  records equal to C3U's committed ones in node, `cnf_sha256`, `proof_sha256`, status, `sigma_bits` and children
  (`logs/regen_vs_committed.txt`). My own driver's t1 equals C3U's `sig_m7k6c300K2` (above).

## Comparison on the repository's records (step 2)

All outputs are in `logs/m11_compare.txt`. Base sha `bf0e502e…`, sha check on, records at 712efc6b (snapshot via `git archive`).

| input | mycompose | C3U compose 95cafa93 (41041780 identical) | C3T compose |
|---|---|---|---|
| C3SIG/G0..G3 `out.jsonl` | 160 cert. cube records, **20 σ-splits used**, frontier 143 | same | – |
| 116 wave files (all `out.jsonl` of C3WAVE1, C3WAVE2, C3S0, C3W3 + 5 recheck files + C04 `out_reconstructed`; not `summary*`, not `removed_records`) | 48,614 records, 48,439 nodes, sha-checked, not covered, frontier 11,492 | same | same |
| waves + C3SIG | 48,774 / 48,599, 20 σ-splits used, frontier 11,492 | same | – |
| C3U `tests/logs/m11/tree_*.jsonl` | 16 cubes, 2 σ-splits used, frontier 161 | same | – |
| C3U's 20 small-run record files, `tests/logs/small/*.jsonl` at f710546d (12 `cmp_*`, 2 `restart_*`, 6 `sig_*` including m = 8 with K = 2 and K = 3) | all covered; certified counts and `sigma_splits_used` as in C3U's table, e.g. m = 8 K = 3: 248 certified, 17 σ-splits | **identical on all 20** (`logs/c3u_small_records.txt`) | – |

The frontier of waves + C3SIG equals that of the waves alone, because the waves had already layer-closed the 20 pilot
nodes.

**Re-solved nodes.** I rebuilt each CNF with my own units and ran CaDiCaL with `--sat --lrat --binary=false`, then
lrat-check (E2) and cake_lpr.
- 3 cubes of C3U's m = 11 records (`logs/resolve_c3u_m11.jsonl`): `cnf_sha256` equal 3/3, UNSAT 3/3, **`proof_sha256`
  and `proof_bytes` equal to C3U's records 3/3**, lrat-check and cake_lpr accept 3/3. Two cake runs had to be repeated
  because of finding 4.
- 3 C3SIG/G0 cubes (`logs/resolve_sig_G0.jsonl`): `cnf_sha256` equal 3/3, UNSAT, both checkers accept, `proof_bytes`
  equal to G0's.

## What I could not check
- Lemmas 1–5, the base encoding and the symmetry reduction were taken as given (C3AUDIT's scope). The H6M lemma
  (`--mirror-h6`) was not reviewed. It stays off.
- I did not re-run C3U's `run_small.sh cmp` (C3T against C3U with `--sigma-split 0`). I did run both composers on
  its committed records: they agree, with 0 brute-force holes. The `close_tree.py` diff shows that the
  `--sigma-split 0` path gives the same cap index as C3T (splits from the root = layers from the root) and the same
  children.
- My driver did not close an m = 8 nested K = 3 tree within the budget. Instead, C3U's committed m = 8 K = 3 run
  (\|C\| up to 6) passes both composers, brute force with 0 holes, and forge.py 18/18.
