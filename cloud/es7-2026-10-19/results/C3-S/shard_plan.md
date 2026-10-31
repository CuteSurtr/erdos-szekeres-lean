# Shard plan: 3-fold class, m = 11 (33 points), k = 7, by hull and convex-layer cases

Status: NOT closed. This is a deterministic recipe. The cost numbers are measured on one 4-core
VM (`env.txt`) and are rough (see "Expected cost").

## 1. Exact inputs

- Generator commit: `fc55d53` on branch `es7-cloud`. Directory
  `cloud/es7-2026-10-19/results/C3-S/tools/`, which imports `../../C3a/c3cnf.py` (unchanged since
  `0473a37`). Python 3.11, no randomness in any generator.
- Base CNF: `python3 tools/gen_case.py 11 7 none -o base.cnf`
  - `p cnf 168399 4154921`
  - sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`. This is
    byte-identical to C3a's chain CNF.
- Node CNF: base.cnf with the header clause count increased by u, and the node's u unit clauses
  (`hullcase.layer_clauses`, one `lit 0` line each) appended at the end. `gen_case.py 11 7 NODE`
  writes the same file (checked: identical sha256 for all 11 top cases).
- Top cases (depth 1) and their CNF sha256:

  | case | node name | units | CNF sha256 |
  |---|---|---|---|
  | H3 | `0s0` | 93 | `b6904b38881548aab08d1808374948652371bacdfd00e8a20f5031d887279475` |
  | H6a1s0 | `0s0-1s0` | 187 | `5d8f9a3028033d2bd632b454dc0681f3107ec162406986965b91da23b1aae14c` |
  | H6a1s1 | `0s0-1s1` | 187 | `441cf1c15c22882d17284c7f31c89752c14ecddf5ed7506c0d56ed100e565b56` |
  | H6a2s0 | `0s0-2s0` | 187 | `d4c130ec7dbe629ecac16058b2f3c042e7b8607247cacf84f66c111ff47d158c` |
  | H6a2s1 | `0s0-2s1` | 187 | `c4ba0989ba2f9b77185330250a4ff731fe11de0b5211cb42560845bc7cb510ce` |
  | H6a3s0 | `0s0-3s0` | 187 | `0e75b381a3980c7151860aec4f771c0b52ea0a6fe139ad0d834dd192ef5c7473` |
  | H6a3s1 | `0s0-3s1` | 187 | `b2507797af30ea3fd11024de2b4b8ed3febdd5e39326ca2c8256deefbc0c9940` |
  | H6a4s0 | `0s0-4s0` | 187 | `64d6a08f91f59aeb49a853dd7ea5be60792dfacb3042f23ee66c8d618a26dece` |
  | H6a4s1 | `0s0-4s1` | 187 | `7a2554c4c0ffcf4de41b4ebed6d10a1f0e3a6050c11994cac88ebc6b0dc08ec4` |
  | H6a5s0 | `0s0-5s0` | 187 | `eb9f971b4c3c611a0315171b73d358daa9a13c3db8e8f7e5542d6a78ba490a9e` |
  | H6a5s1 | `0s0-5s1` | 187 | `3b632d7936e433b054382d294ad7b30909c0627971b0afd0704221a5f9626777` |

- Every depth-2 node (1,630 of them: 100 below H3 after the mirror reduction, 153 below each H6
  case), with its unit count and CNF sha256, is listed in `manifest_depth2.tsv`.
  The sha256 of the sorted list of the 1,630 names joined by `\n` is
  `5412782cb766088d63fa9342afaaddcf057baee69b82b82bba69e5754fef6b7e`.
- Tools: CaDiCaL 3.0.1 (commit c6073042), cake_lpr (from the repository's `cake_lpr.S`),
  drat-trim lrat-check (2e3b2dc) + `results/E2/tools/lrat-check-E2.patch`.

## 2. Work units and commands

The shards are the depth-2 nodes, sorted by name. Machine i of N (0-based) takes the nodes whose
index is congruent to i mod N, and runs, with J = number of cores:

```
cd cloud/es7-2026-10-19/results/C3-S/tools
python3 gen_case.py 11 7 none -o /work/base.cnf          # check the sha256 above
python3 close_tree.py /work/base.cnf /work/out_$i.jsonl SHARD --shard $i --nshards $N \
        --jobs $J --caps 300,300,600 --cadopts=--sat --split-singles
```

For each node, `close_tree.py` does the following:

- writes the node CNF and records its sha256;
- runs `cadical -q -t CAP --sat --lrat --binary=false node.cnf node.lrat`;
- on UNSAT, runs `lrat-check node.cnf node.lrat` (E2 patch) and
  `cake_lpr node.cnf node.lrat` (CML_HEAP_SIZE=12000, CML_STACK_SIZE=2000);
- marks the node certified only if both print `c VERIFIED` and `s VERIFIED UNSAT`;
- deletes the CNF and the proof (both can be regenerated);
- if CaDiCaL does not decide the node within CAP, records `{"split": true}` and queues all
  children (`hullcase.tree_children`, the next convex layer).

Caps by depth below the shard root: 300 s at depth 2, 300 s at depth 3, 600 s from depth 4.
The driver can be restarted: certified and split nodes in OUT are reused. A SAT answer stops the
driver and saves the model. Decode it with `results/C3a/decode.py`, check it, and report it first.

The depth-1 nodes are never solved directly. The 11 top-case CNFs time out at 300 s, and the
depth-2 shards are their children.

`--split-singles` (used above and assumed in the cost numbers): a node whose newest layer is a
single orbit directly below a two-orbit layer (or below the top) is split at once, without trying
it. Runs of one-orbit layers are tried, or the tree explodes. One-orbit layers add only 3 hull vertices, and those nodes
almost never close at 300 s (`logs/tree_H6a4s0.jsonl`).

## 3. Composition into one certificate

1. Collect all `out_*.jsonl`.
2. Run `python3 tools/compose.py /work/base.cnf out_*.jsonl`. It does the following:
   - keeps only records with `certified: true`, `lrat_check == "c VERIFIED"` and
     `cake_lpr == "s VERIFIED UNSAT"`;
   - recomputes each node's CNF sha256 from base.cnf and the node name, and requires a match;
   - checks that the certified nodes form a cut of the layer tree. A node is covered iff it is
     certified, or all its children (`tree_children`) are covered.
   - prints `class_covered: true` exactly when the root is covered.
3. The claim then rests on:
   - (a) soundness of the base encoding (C3a/C3b validation);
   - (b) the cover lemmas in `soundness.md`: hull/layer cases, the mirror reduction under H3,
     and the completeness of `tree_children`;
   - (c) the two proof checkers.

   The per-node certificates compose by plain case analysis. No coverage proof is needed beyond
   (b), because the children of a node are an explicit enumeration, not march cubes.

If march cubes are used inside a node (optional), the C3a recipe applies to that node's CNF:
complete the cube tree, and certify coverage with an LRAT proof of the negated cubes, checked by
both checkers.

## 4. Expected cost

All numbers are single-core seconds or hours, measured on the shared 4-core VM. "Solve" is
CaDiCaL time; dual checking adds about 27% (measured: mean 27 s check per 101 s solve).

| part of the tree | how measured | solve core-hours |
|---|---|---|
| 10 H6 cases × 144 two-orbit layer-2 nodes, closed at depth 2 | H6a4s0 enumerated completely: 139/144 closed, mean 100.6 s (median 81, max 290), 5 time out at 300 s | about 40 (+11 checking) |
| the about 5 % of those pair nodes that time out, split once | assumed to cost like a one-orbit subtree below | about 130 |
| 10 × 9 one-orbit layer-2 subtrees below H6 (pre-split, children capped) | 88 Knuth walks (`kd_H6single_s51`) | 469 ± 141 (median walk 113, max 11,797) |
| H3 subtree (100 layer-2 options after the mirror reduction) | 8 Knuth walks (`kc_H3_*`, two policies) | median walk 446; policy 300k/100k: 218 and 1,681; one walk 682,760 |

**Estimate: about 1,500 core-hours (H6 ≈ 800 with checking, H3 ≈ 500–1,700), but the H3 part
is heavy-tailed and its mean over 8 walks is 86,000 ± 85,000 core-hours.** The one extreme walk
goes through nested one-orbit layers (`0s0_1_5_...`): nested triangles add only 3 hull vertices
per layer, so the tree branches about 100-fold per level with little propagation. The
estimate is not reliable until the H3 stratum has hundreds of walks. Run the H3 subtree first,
under the shard plan below, for a few hundred core-hours, then re-estimate from its own logs.

For N machines with C cores each, the expected wall time is about 1,500 / (N·C) hours if the
tail does not bite. For example, 16 machines × 32 cores gives about 3 h.
The plan is deterministic, so a second run of the same plan reproduces the same node CNFs
(sha256 in `manifest_depth2.tsv` and in the records). Solver time limits can change which nodes
are split, but they never change soundness.
