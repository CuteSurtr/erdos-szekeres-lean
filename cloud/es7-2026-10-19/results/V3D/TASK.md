# V3D task (fourth acceptance pass of mirror sub-case (ii): the leaves still unchecked at commit 3e4dbaae3)

Your prompt gives five values: V (your machine name, for example D03; v is the same in lower case, d03), i (your shard), N (the number of shards), H (your time budget in hours) and Z (the commit of this file). Below, replace {V}, {v}, {i}, {N}, {H} and {Z} by those values. Everything else in this file is to be followed exactly.

General rules:
- Start: `git fetch origin es7-cloud && git checkout es7-cloud`. Before your first commit, set the commit identity of the repository owner: `git config user.name CuteSurtr && git config user.email 133225877+CuteSurtr@users.noreply.github.com`, and check that `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` both start with `CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>` (if not, unset GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_COMMITTER_NAME and GIT_COMMITTER_EMAIL for your git commands). Every commit you make must have that author and committer. Record the environment (`uname -a; nproc; free -g || true; df -h /opt || true; date -u`) into `cloud/es7-2026-10-19/results/V3D/{V}/env.txt`, then commit and push it at once.
- Time budget: {H} hours of wall time. Commit and push progress at least every 30 minutes. Use the last 15 minutes to write `results/V3D/{V}/README.md`, push, and report. If your shard is finished earlier, write the README then and end.
- Do not end your turn while work is running. ScheduleWakeup does not fire in this environment. Keep the session active: wait with background until-loops or Monitor that return on progress, commit, then wait again.
- Commit only to branch es7-cloud, and only inside `cloud/es7-2026-10-19/results/V3D/{V}/`. Use plain commit messages with no AI co-author or attribution trailers. Run `git pull --rebase --autostash` before every push, and retry the push until it succeeds (many machines push to this branch). If a push still fails after 10 tries, push to branch `es7-fallback-v3d-{v}` and say so.
- Never commit files over 50 MB, and never commit CNF or LRAT proof files. Use all 4 cores.
- The only trusted proof checker is cake_lpr: a claim counts only if it prints the exact line `s VERIFIED UNSAT`.

Task V3D {V}: machine {i} of {N} in the fourth pass of the from-scratch acceptance check of mirror sub-case (ii).

Background (paths under `cloud/es7-2026-10-19/`):
- Sub-case (ii) is the CNF F = `m33k7int.sub.cnf` (sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d), split into 450 hull cases (`results/Mii-S/cases.jsonl`, `results/Mii-S/cases.icnf`). The waves `results/WAVE1/` to `results/WAVE4/` close the wave cases by leaves. A leaf counts only after `verify/v3/v3_check.py` re-solves it from a CNF it builds itself (F + case cube + leaf) and cake_lpr verifies the proof. Read `verify/v3/README.md`, `verify/v3/CHANGES.md` and `results/V3T/REVIEW.md`.
- The earlier passes (`results/V3T/`, `results/V3A/`, `results/V3B/`, `results/V3C/`) check the leaves of earlier manifests. This pass checks the leaves of the manifest at commit 3e4dbaae3 that had no VERIFIED record there and that no running pass was checking: the work list `results/V3D/worklist.jsonl` (22682 records, sha256 27e02b76e005964ef7779f970b1e3da55328bdfa878541b4ad86020120e7b1d9). `results/V3D/README.md` says how it was made. The final acceptance table re-derives everything from the wave directories, so the work list only decides which leaves you check.
- Use `verify/v3/` exactly as of commit bdf319c: `git worktree add /opt/v3src bdf319c`; V3 below is `/opt/v3src/cloud/es7-2026-10-19/verify/v3`.

Steps:
1. Tools, built from source, recorded with their commits in `results/V3D/{V}/tools.txt`:
   - CaDiCaL 3.0.1 (https://github.com/arminbiere/cadical, commit c6073042) as /opt/bin/cadical;
   - cake_lpr (https://github.com/tanyongkiam/cake_lpr at a36874a8, `make cake_lpr`) as /opt/bin/cake_lpr; check that its bundled example prints `s VERIFIED UNSAT`.
   Regenerate F: `python3 tools/etv/gen_etv.py 33 7 7 7 --mirror -o m33k7.cnf`, then `python3 results/C/scripts/mirgen.py m33k7.cnf 33 --interior --yflip-unit -o /opt/work/F.cnf`, and check the sha256 above.
2. Inputs pinned at commit {Z}: `git worktree add /opt/in {Z}` and set ROOT=/opt/in/cloud/es7-2026-10-19. Check the sha256 and the line count of `$ROOT/results/V3D/worklist.jsonl` against the values above, and record them in `results/V3D/{V}/inputs.txt`.
   Cross-check the work list: `git worktree add /opt/zd 3e4dbaae3`, R2=/opt/zd/cloud/es7-2026-10-19, then `python3 $V3/v3_jsonl_leaves.py $R2 results/WAVEk jtreek` for k = 1, 2, 3, 4, and `python3 $V3/v3_manifest.py $R2 /opt/work/Mzd.jsonl /opt/work/Czd.jsonl results/WAVE1 jtree1 results/WAVE2 jtree2 results/WAVE3 jtree3 results/WAVE4 jtree4`. Its sha256 must be 9685d3c4e3c071782c9db41362a6e4bc244ee99130ef131bc7b6da58254a67a8 (70215 lines), and every work-list record's (case, lits) must occur in it. Record the result in inputs.txt. If either check fails, stop and report.
3. Run `python3 $V3/v3_check.py --root $ROOT --base /opt/work/F.cnf --manifest $ROOT/results/V3D/worklist.jsonl --shard {i} --nshards {N} --skip-covers --out /opt/work/out/out.jsonl --work /opt/work/v3w --jobs 4 --cap 1800`, started with `setsid nohup` so that it keeps running between your tool calls. Keep OUT outside the git checkout (REVIEW.md RISK-7) and copy it to `results/V3D/{V}/out.jsonl` each time you commit. The run is resumable with the same arguments.
4. A REJECTED leaf whose `cake_lpr` field is empty means the checker printed no verdict, usually because it ran out of memory while four large proofs were checked at once. After the main run (or when you stop it), re-check each such leaf alone: run v3_check.py on a one-record manifest (the record renumbered to idx 0) with `--jobs 1`, write to a separate output, and append that record to your out.jsonl with an extra field `"recheck": true`. Report both records.
5. When your time is nearly up, stop the run (records are written as jobs finish).

README.md and final message:
- the tool commits, F's sha256, the input commit and verify/v3 commit, the work-list sha256 and the cross-check result;
- leaf verdict counts (VERIFIED, REJECTED, SAT, TIMEOUT) and how many of your leaves are still unchecked;
- solve and check time (sum, median, max);
- any SAT, REJECTED or TIMEOUT with the case, the literals and the source directories. A SAT leaf would mean the case is satisfiable: report it first and commit the solver output.
