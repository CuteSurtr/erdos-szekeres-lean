# V3B task (second acceptance pass of mirror sub-case (ii))

Your prompt gives five values: V (your machine name, for example B03; v is the same in lower case, b03), i (your shard), N (the number of shards), H (your time budget in hours) and Z (the input commit). Below, replace {V}, {v}, {i}, {N}, {H} and {Z} by those values. Everything else in this file is to be followed exactly.

General rules:
- Start: `git fetch origin es7-cloud && git checkout es7-cloud`. Record the environment (`uname -a; nproc; free -g || true; df -h /opt || true; date -u`) into `cloud/es7-2026-10-19/results/V3B/{V}/env.txt`, then commit and push it at once.
- Time budget: {H} hours of wall time. Commit and push progress at least every 30 minutes. Use the last 15 minutes to write `results/V3B/{V}/README.md`, push, and report.
- Do not end your turn while work is running. ScheduleWakeup does not fire in this environment. Keep the session active: wait with background until-loops or Monitor that return on progress, commit, then wait again.
- Commit only to branch es7-cloud, and only inside `cloud/es7-2026-10-19/results/V3B/{V}/`. Use plain commit messages with no AI co-author or attribution trailers. Run `git pull --rebase --autostash` before every push. If a push is rejected, push to branch `claude/es7-v3b-{v}` and say so.
- Never commit files over 50 MB, and never commit CNF or LRAT proof files. Use all 4 cores.
- The only trusted proof checker is cake_lpr: a claim counts only if it prints the exact line `s VERIFIED UNSAT`.

Task V3B {V}: machine {i} of {N} in the second pass of the from-scratch acceptance check of mirror sub-case (ii).

Background (paths under `cloud/es7-2026-10-19/`):
- Sub-case (ii) is the CNF F = `m33k7int.sub.cnf` (sha256 69c1dc8f7818cbef615c1c6f65db66463294ea8054f0cec602846f27ffff932d), split into 450 hull cases (`results/Mii-S/cases.jsonl`, `results/Mii-S/cases.icnf`). The waves `results/WAVE1/` (36 separately modified drivers, `results/Haudit/AUDIT.md` RISK-3), `results/WAVE2/` and `results/WAVE3/` (one shared driver, `results/WAVE2/F2/close_march.py`) closed the 278 open cases by leaves. A leaf counts only after `verify/v3/v3_check.py` re-solves it from a CNF it builds itself (F + case cube + leaf) and cake_lpr verifies the proof. Read `verify/v3/README.md`, `verify/v3/CHANGES.md` and `results/V3T/REVIEW.md`.
- The first pass (`results/V3T/`, `results/V3A/Vxx/out.jsonl`) already verified part of the leaves. This pass checks every leaf of the manifest at commit {Z} that has no VERIFIED record yet.
- Use `verify/v3/` exactly as of commit bdf319c: `git worktree add /opt/v3src bdf319c`; V3 below is `/opt/v3src/cloud/es7-2026-10-19/verify/v3`.

Steps:
1. Tools, built from source, recorded with their commits in `results/V3B/{V}/tools.txt`:
   - CaDiCaL 3.0.1 (https://github.com/arminbiere/cadical, commit c6073042) as /opt/bin/cadical;
   - cake_lpr (https://github.com/tanyongkiam/cake_lpr at a36874a8, `make cake_lpr`) as /opt/bin/cake_lpr; check that its bundled example prints `s VERIFIED UNSAT`.
   Regenerate F: `python3 tools/etv/gen_etv.py 33 7 7 7 --mirror -o m33k7.cnf`, then `python3 results/C/scripts/mirgen.py m33k7.cnf 33 --interior --yflip-unit -o /opt/work/F.cnf`, and check the sha256 above.
2. Inputs pinned at commit {Z}: `git worktree add /opt/in {Z}` and set ROOT=/opt/in/cloud/es7-2026-10-19. Then, for each wave directory that exists at that commit:
   - `python3 $V3/v3_jsonl_leaves.py $ROOT results/WAVE1 jtree1`, `python3 $V3/v3_jsonl_leaves.py $ROOT results/WAVE2 jtree2`, `python3 $V3/v3_jsonl_leaves.py $ROOT results/WAVE3 jtree3` (the jtree directories are written under $ROOT and never committed);
   - `python3 $V3/v3_manifest.py $ROOT /opt/work/M.jsonl /opt/work/C.jsonl results/WAVE1 jtree1 results/WAVE2 jtree2 results/WAVE3 jtree3` (leave out the pairs whose wave directory does not exist).
   Record the printed counts and the sha256 of M.jsonl in `results/V3B/{V}/inputs.txt`.
3. Collect every record with `"kind": "leaf"` and `"verdict": "VERIFIED"` and a `lits` field from all JSONL files under `$ROOT/results/V3T/` and from `$ROOT/results/V3A/*/out.jsonl` (and from `$ROOT/results/V3B/*/out.jsonl` of earlier V3B machines, if any exist at {Z}). Key each by (case, the JSON text of lits). Remove from M.jsonl every record whose (case, JSON text of lits) is one of these keys, keep the rest in order, renumber idx 0..n-1, and write `/opt/work/Mt.jsonl`. Record the number of VERIFIED keys found, n, and the sha256 of Mt.jsonl in inputs.txt. All {N} machines must produce the same Mt.jsonl; the key text must be exactly `json.dumps(lits)` of the manifest's literal list.
4. Run `python3 $V3/v3_check.py --root $ROOT --base /opt/work/F.cnf --manifest /opt/work/Mt.jsonl --shard {i} --nshards {N} --skip-covers --out /opt/work/out/out.jsonl --work /opt/work/v3w --jobs 4 --cap 1800`. Keep OUT outside the git checkout (REVIEW.md RISK-7) and copy it to `results/V3B/{V}/out.jsonl` each time you commit. The run is resumable with the same arguments.
5. A REJECTED leaf whose `cake_lpr` field is empty means the checker printed no verdict, usually because it ran out of memory while four large proofs were checked at once. After the main run (or when you stop it), re-check each such leaf alone: run v3_check.py on a one-record manifest (the record renumbered to idx 0) with `--jobs 1`, write to a separate output, and append that record to your out.jsonl with an extra field `"recheck": true`. Report both records.
6. When your time is nearly up, stop the run (records are written as jobs finish).

README.md and final message:
- the tool commits, F's sha256, the input commit and verify/v3 commit, the manifest counts and sha256s;
- leaf verdict counts (VERIFIED, REJECTED, SAT, TIMEOUT) and how many of your leaves are still unchecked;
- solve and check time (sum, median, max);
- any SAT, REJECTED or TIMEOUT with the case, the literals and the source directories. A SAT leaf would mean the case is satisfiable: report it first and commit the solver output.
