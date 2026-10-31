# C3W3S task: σ-cube closure of mirror-kept two-orbit s = 1 roots, from the end of the list

Your prompt gives these values: V (your machine name, S0, S1, ...), j (your shard), N (the number of σ machines), H (your time budget in hours) and Z (the commit of this file). Replace {V}, {j}, {N}, {H} and {Z} by those values; follow everything else exactly.

This is part of the search for a counterexample to ES(7) = 33 (a 3-fold-symmetric 33-point set in general position with no 7 points in convex position). Every SAT answer is a candidate counterexample.

General rules: exactly as in `results/C3W3/TASK.md` (paths under `cloud/es7-2026-10-19/`), with `results/C3W3S/{V}/` as your only directory and the fallback branch `es7-fallback-c3w3s-{V}` (lower case): commit identity CuteSurtr <133225877+CuteSurtr@users.noreply.github.com> (check `git var GIT_AUTHOR_IDENT` and `GIT_COMMITTER_IDENT`), `env.txt` committed at once, plain commit messages with no AI co-author or attribution trailers, `git pull --rebase --autostash` before every push, progress pushed at least every 25 minutes, the last 12 minutes for the README, no CNF or proof files, no file over 50 MB, and do not end your turn while work is running (wait in the foreground with bounded until-loops of at most 10 minutes per tool call). An UNSAT counts only with both checkers (lrat-check E2 `c VERIFIED` and cake_lpr exactly `s VERIFIED UNSAT`).

## Why

The σ-cube pilot (`results/C3SIG/G0`, `G1`, `G3`) closed 15 of 15 hard two-orbit s = 1 nodes with 8 σ-cubes each at about 0.07–0.12 of the layer-split cost. The machines `results/C3W3/C0` to `C17` work through `results/C3W3/lists/C_s1two.tsv` from the top with the layer split. You take its mirror-kept rows from the bottom with σ-cubes, so that the two meet as late as possible. Your records will be composed with the σ-cube support of `results/C3U` (which reads the record formats of `close_node.py` and `sigma_cubes.py`).

## Steps

1. Tools and base CNF exactly as step 1 of `results/C3WAVE2/TASK.md` (C3-S tools at commit 132398c used unmodified, CaDiCaL c6073042, cake_lpr a36874a8, lrat-check 2e3b2dc with the E2 patch and its sanity check, base CNF header `p cnf 168399 4154921`, sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`); copy `results/C3PLAN/scripts/sigma_cubes.py` into the tools directory unmodified. Record everything in `tools.txt`.
2. Your roots: the rows of `results/C3W3/lists/C_s1two.tsv` with `h6m_kept` = yes, sorted by decreasing row number; take those at positions ≡ {j} (mod {N}) of that order. Write them to `roots.tsv`.
3. Before each root R, `git pull` and skip R if a C machine has reached it: if any record in `results/C3W3/C*/out.jsonl` has node R or a node starting with `R_`, or a `results/C3W3/C*/driver*.log*` file has a line `=== ROOT R start` without a matching end line. Log every skip.
4. For each root R not skipped, keep 3 solver processes busy (CaDiCaL is single-threaded):
   a. Direct attempt: `close_node.py BASE out_direct.jsonl 300 R` (cap 300 s). If it certifies R, R is closed.
   b. Otherwise: `sigma_cubes.py BASE out_sigma.jsonl R 3 300 3` (8 cubes on the 3 smallest free residues).
   c. Refine every open cube C on the next 3 free residues: the 8 cubes on the 6 smallest free residues of R that extend C, with a small driver of your own that imports `sigma_cubes` unmodified and calls its `run((base, R, bits6, vals6, 300))`, 3 at a time, appending the returned records to `out_sigma.jsonl` in the same format.
   d. Anything still open after step c is left for the next wave; record it.
   Any SAT: stop everything, commit the model and the solver output, report it first. Any `PROOF NOT ACCEPTED` or uncertified UNSAT: re-check that CNF alone (one job); if both checkers then accept, record both results in `recheck.jsonl` and continue, otherwise stop and report.
5. Every 25 minutes and at the end, commit `out_direct.jsonl`, `out_sigma.jsonl`, `recheck.jsonl` (if any), `roots.tsv`, the skip log and a driver log tail.

README.md and final message: tools and base check; per root: closed directly / closed at σ level 1 / closed at σ level 2 / open (which cubes) / skipped, with solve and check seconds; totals; any SAT, proof rejection or memory problem.
