# C3SIG task: σ-cube pilot on hard two-orbit nodes of the 3-fold class

Your prompt gives these values: V (your machine name, G0 to G3), j (your shard), H (your time budget in hours) and Z (the commit of this file). Replace {V}, {j}, {H} and {Z} by those values; follow everything else exactly.

General rules: exactly as in `results/C3WAVE2/TASK.md` (paths under `cloud/es7-2026-10-19/`), with `results/C3SIG/{V}/` as your only directory and the fallback branch `es7-fallback-c3sig-{V}` (lower case): commit identity CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>, `env.txt` pushed at once, plain commit messages with no AI co-author or attribution trailers, `git pull --rebase --autostash` before every push, progress pushed at least every 25 minutes, the last 12 minutes for the README, no CNF or proof files, and do not end your turn while work is running. An UNSAT counts only with both checkers (lrat-check E2 `c VERIFIED` and cake_lpr exactly `s VERIFIED UNSAT`). Any SAT: stop, commit the model and the solver output, and report it first.

## Question

`results/C3PLAN/PLAN.md` §3b and §4 step 1: is splitting a hard node on σ bits cheaper than the layer split? The nodes in `results/C3W3/lists/S_sigma_nodes.tsv` are two-orbit s = 1 roots that timed out at 300 s and were then closed by the layer split; the column `recorded_core_s` is what that cost (solve + check, summed over the subtree, from the wave records).

## Steps

1. Tools and base CNF exactly as step 1 of `results/C3WAVE2/TASK.md`; record them in `tools.txt`.
2. Your nodes: rows with row ≡ {j} (mod 4).
3. For each node, run `results/C3PLAN/scripts/sigma_cubes.py` (usage in its docstring; copy it into the tools directory, unmodified) with K = 3, cap 300 and 3 jobs. If some cubes stay open, run K = 6 with cap 300 on that node (all 64 cubes; note which of them refine the open K = 3 cubes). Keep each node within an even share of your time.
4. Record per node and K: cubes certified / open, total solve and check seconds, the largest cube time, and the comparison with `recorded_core_s`. Keep all records in `out.jsonl`.

README.md and final message: the table, the median ratio σ-cube cost / layer-split cost, the fraction of open cubes at K = 3 and K = 6, and whether PLAN.md's criterion (median below half the layer-split cost; under 20% of second-level cubes open) is met.
