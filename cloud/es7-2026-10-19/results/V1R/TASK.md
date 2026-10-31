# V1R task: a second from-scratch check of the 1,198 sub-case (i) leaves, with per-leaf hashes

Your prompt gives these values: V (your machine name, R0 to R3), j (your shard), H (your time budget in hours) and Z (the commit of this file). Replace {V}, {j}, {H} and {Z} by those values; follow everything else exactly.

General rules:
- Start: `git fetch origin es7-cloud && git checkout es7-cloud`. Before your first commit run `git config user.name CuteSurtr && git config user.email 133225877+CuteSurtr@users.noreply.github.com` and check that `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` both start with `CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>` (if not, unset GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_COMMITTER_NAME and GIT_COMMITTER_EMAIL for your git commands). Record the environment (`uname -a; nproc; free -g || true; date -u`) into `cloud/es7-2026-10-19/results/V1R/{V}/env.txt`, then commit and push it at once.
- Time budget: {H} hours of wall time. Commit and push at least every 25 minutes. Use the last 10 minutes to finish `results/V1R/{V}/README.md`, push, and report. Do not end your turn while work is running: ScheduleWakeup does not fire here, so run the solver loop with `setsid nohup` and wait in the foreground with bounded until-loops (at most 10 minutes per tool call).
- Commit only to branch es7-cloud and only inside `cloud/es7-2026-10-19/results/V1R/{V}/`, with plain commit messages and no AI co-author or attribution trailers. Run `git pull --rebase --autostash` before every push and retry until it succeeds; after 10 failures push to branch `es7-fallback-v1r-{V}` (lower case) and say so. Never commit CNF or proof files or files over 50 MB.
- Write your own builder and checker driver; do not reuse the scripts of `results/V1-0` to `V1-3`, `results/V1-L` or `verify/v3`.

## Why

Sub-case (i) of the mirror class (the axis point is a hull vertex) rests on 1,198 leaf facts: `V1L.hullVertexLine_of_leaves` / the hypothesis `h1` of `V2L.mirrorExclusionLine_final` says `¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c)` for every cube c of `V1L.hullLeaves`. The cake_lpr records of `results/V1-0` to `V1-3` carry no per-leaf CNF hash (`results/AUDIT2/A1/REPORT.md`, finding 1), and, unlike sub-case (ii), these leaves had no independent second check.

## Steps

1. Build CaDiCaL 3.0.1 (commit c60730422e758ef1cebe7aeddf2dda31c996bf04) and cake_lpr (a36874a8b750b43fe4b385b8ddbf5b033e46a3fa, `make cake_lpr`; its example must print `s VERIFIED UNSAT`) from source. Record them in `tools.txt`.
2. Generate the sub-case (i) CNF `hm33k7.sub.cnf` as the repository does (find the generator through `results/H3/README.md`, `results/C/README.md` and `verify/README.md`); its sha256 must be `bfbc2d6096e4099ba751130d421eca9da18b72559991103cc2d4b4bc0d92757d`. Check that `verify/hull_leaves.icnf` has sha256 `cc11270a57ebe85ad1d5c83b15da0a3439521cc7ebd50432f16c223a1b2478b6`. If either check fails, stop and report.
3. Your leaves: the cubes of `verify/hull_leaves.icnf` with 0-based line index i ≡ {j} (mod 4).
4. For each leaf, write the CNF exactly as the Lean term `cubeCnf (hullCnf 33 7) c` lists its clauses: header `p cnf NV NC+|c|`, the body of `hm33k7.sub.cnf` unchanged, then one unit clause per literal of c in the order of the file. Record its sha256. Solve with `cadical --lrat=true --no-binary` (text LRAT), then run cake_lpr on the CNF and the proof. A leaf counts as verified only if CaDiCaL exits 20 and a line of cake_lpr's output is exactly `s VERIFIED UNSAT`. Record the proof's sha256 before deleting it. Run up to 3 leaves in parallel.
5. Write one JSON line per leaf to `results/V1R/{V}/out.jsonl`: i, cube, cnf_sha256, solver_exit, solve_s, proof_bytes, proof_sha256, cake_lpr (the exact line or the output tail), check_s. Compare with the records of `results/V1-0` to `V1-3` (same i, same cube) and list any difference.
6. If any leaf is SAT or not verified, re-run it alone; if it still fails, say so first in the README and the final message.

README.md and final message: tools, the two input hashes, the number of leaves verified out of your share, total solve and check time, the largest leaf, and every difference from the earlier records.
