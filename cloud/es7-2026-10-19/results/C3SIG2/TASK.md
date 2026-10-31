# C3SIG2 task: σ-cube pilot on one-orbit s = 1 roots and H3 roots

Your prompt gives these values: V (your machine name, G4 to G7), j (your shard), H (your time budget in hours) and Z (the commit of this file). Replace {V}, {j}, {H} and {Z} by those values; follow everything else exactly.

General rules: exactly as in `results/C3SIG/TASK.md`, with `results/C3SIG2/{V}/` as your only directory and the fallback branch `es7-fallback-c3sig2-{V}` (lower case). In particular: commit identity CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>, `env.txt` pushed at once, plain commit messages with no AI co-author or attribution trailers, `git pull --rebase --autostash` before every push, progress pushed at least every 25 minutes, the last 12 minutes for the README, no CNF or proof files, do not end your turn while work is running. An UNSAT counts only with both checkers (lrat-check E2 `c VERIFIED` and cake_lpr exactly `s VERIFIED UNSAT`). Any SAT: stop, commit the model and the solver output, and report it first.

## Question

`results/C3SIG/G0`, `G1` and `G3` closed 15 of 15 hard two-orbit s = 1 nodes with 8 σ-cubes each (K = 3, cap 300) at about 0.07–0.12 of the layer-split cost. Nothing has been measured on one-orbit roots (which explode under the layer split: `0s0-1s1_4` has 4,299 open nodes) or on H3 roots. Do σ-cubes close them, and at what cost?

## Steps

1. Tools and base CNF exactly as step 1 of `results/C3WAVE2/TASK.md`; copy `results/C3PLAN/scripts/sigma_cubes.py` into the tools directory unmodified; record everything in `tools.txt`.
2. Your nodes: rows of `results/C3SIG2/nodes.tsv` with row ≡ {j} (mod 4), in order. Give each node an even share of your time.
3. For each node, run `sigma_cubes.py BASE out.jsonl NODE 3 300 3` (K = 3, cap 300, 3 jobs). If cubes stay open and the node's share allows, refine each open cube C on the next 3 free residues: the 8 cubes on the 6 smallest free residues of the node that extend C. Do this with a small driver of your own that imports `sigma_cubes` unmodified and calls its `run((base, node, bits6, vals6, 300))` for those 8 assignments, 3 at a time, appending the returned records to `out.jsonl` in the same format (so every record has `node` = the depth-2 node and `cube` = the fixed bits). Record which cubes stay open after that.
4. Per node: cubes certified / open at each level, total solve and check seconds, the largest cube, and whether the node is closed (all 8 K = 3 cubes certified, or each open one refined into 8 certified cubes). For the partial roots, compare with `spent_core_s` and `open_nodes` (what the layer split has spent so far without closing them).

README.md and final message: the table, per stratum (one-orbit H6(a,1) and H3) the fraction of nodes closed and the median cost per closed node, the open fractions at both levels, and your judgement of whether σ-cubes at depth 2 should be the first step for these strata in the next wave.
