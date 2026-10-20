# Shard plan: 3-fold class, m = 11 (33 points), k = 7, by hull and convex-layer cases

Status: NOT closed. This is a deterministic recipe. The cost numbers are measured on one 4-core
VM (`env.txt`) and are rough (see "Expected cost").

## 1. Exact inputs

- Generator commit: GENCOMMIT_PLACEHOLDER on branch `es7-cloud`. Directory
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

TOPCASES_PLACEHOLDER

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
        --jobs $J --caps 300,300,600 --cadopts=--sat
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

Recommended policy change (from the measurements below): do not try a node whose newest layer
is a single orbit. Split it at once. One-orbit layers add only 3 hull vertices, and those nodes
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

COST_PLACEHOLDER
