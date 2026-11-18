# V11 notes: skip list for the (20,15) frontier finder (track S1, 15 Nov 2026 evening)

**Status 20:25 KST: implemented and tested end to end in a separate namespace; NOT switched live.** The live loop
`esr-lo-b35s20v10c` and its files (packet `runs/b35s20/bb`, inputs `b35s20-v143…`, its cut folders) were not touched;
every file named below as new was created by this track. Labels: the test numbers are COMPUTED (counts from finder
logs and receipts); the throughput comparison is HEURISTIC (one short test at 1.5 CPUs against the live 4-thread
rounds). No bound and no tree is claimed; (20,15) is not closed and ES(8) ≤ 307 is not reached.

**Summary.**
- **The change is selection only.** The frontier finder now passes fastbb2 the open contexts minus those recorded too
  big at or above its cap. An optional extra worker attempts the recorded contexts with a higher cap. fastbb2, the
  ctx files, the witness checks, the cut/certify/append path and the trusted replays are unchanged (§1-§2, exact diffs
  included).
- **Test 1** (copy of the live packet at 19:10; 1 frontier thread plus 1 extra-worker thread, 150 % CPU in all):
  in 47.3 + 11.9 min the frontier attempted none of the 75 recorded contexts, closed 31 contexts (30-32 per hour on about 0.75 CPU) and found one witness. That witness went through an unchanged round: 8 of 8 rows CERTIFIED (test rows) and appended as `b35s20-v601`, and the next slice re-read the updated record. The extra worker **closed 6 of the recorded contexts** (167k-261k nodes), which every v10 round had re-attempted at 150,000 nodes without closing them. Two others went over 300k and were recorded at that cap. Memory peak 648 MB.
- **Test 2** (unit test: four short runner calls on a copy of the v9 test packet's master, 64 contexts): the record/skip cycle works as specified across runs. A context recorded at the frontier cap is skipped in the next run, `--too-big-only` selects exactly the contexts recorded below its cap, and an empty selection becomes `--ctx=-1` (fastbb2 todo 0).
- **Live comparison** (same logs, read-only, COMPUTED): before their first new context, the live 4-thread rounds
  c139s1-c143s2 spent 41-54 min each re-attempting 54-75 recorded contexts. c142s1 and c143s1 closed 6 and 5 contexts
  in 57 and 55 min (1.6 and 1.4 per thread-hour). The v10c finder c143s2 (18:52-20:03) closed 43, all after minute 51.
- **Not switched live**; the switch command is in §4.

## 1. What changed (A2's proposal §5.1 and §5.2)

Problem (A2, [ANALYSIS_1115PM.md](../ANALYSIS_1115PM.md)): every finder start passes all open contexts to fastbb2,
which walks them in ID order, so each round first re-attempts every known too-big context from context 0.

New files (copies of the previous versions with the minimal change):

| file | SHA-256 | role |
|---|---|---|
| `tools/run_tree_v6.py` | `d6608ce9f4d8282468debc1fac2343d03217a29af49621dfd3bb4a2c750c0da3` | finder runner = run_tree_v5.py + skip list + optional extra worker |
| `tools/continue34_v11.py` | `81d2c9e26ef858f3bf63c9b04477bdf9ad1e38bd29151c59357412e9bc5d2d7f` | loop = continue34_v10.py, calling run_tree_v6.py; passes `--extra-cap`, `--extra-threads` |
| `tools/init_too_big_v1.py` | `2964a09386ae1eabb71afc64592bbc70a94a34576ddd488ca32895cfe8a69219` | rebuilds the initial too-big record of a packet, read-only, from its finder logs |

Unchanged and called exactly as before: `bin/fastbb2` (`39b724a2…`, built from FASTBB20261113/tools/fastbb2.cpp
`2e7e0707…`; its hash stays in every receipt's input hashes), `cut34_v4.py`, `probe35_v2.py`, `append_cuts_v2.py`,
the audit script and the trusted replays.

**run_tree_v6.py**
- Record `<packet>/TOO_BIG.txt`: one line `<context> <nodes_so_far> <tag>` per `context_too_big` event. Only v6 code
  writes it: run_tree_v6 appends the run's events after the run (frontier lines with the finder tag, extra-worker
  lines with `<tag>.x`); `init_too_big_v1.py` writes the initial file (refuses an existing one). `nodes_so_far` is
  cap + 1…3, so a line records the cap at which the attempt failed.
- Frontier mode (default): the open contexts (from the packet's `contexts.json`, no `ctx-<c>.json.gz`) minus those
  with a line whose `nodes_so_far` exceeds `--max-ctx-nodes`, passed as `--ctx=a,b,…` (fastbb2 keeps master/ID
  order). Contexts too big only at a lower cap (the night's 50k lines) stay in. An empty list is passed as `--ctx=-1`
  (`--ctx=` would mean "all contexts" to fastbb2).
- `--extra-cap=X` (> `--max-ctx-nodes`): a second fastbb2 process on the same rows, packet and slice, `--threads=
  --extra-threads`, `--max-ctx-nodes=X`, `--on-witness=continue` (asserted), on the open contexts recorded too big
  above the frontier cap and at most X. It starts once the frontier's log shows its `start` event (both processes
  rewrite `master.json`/`contexts.json` at start through the same `.tmp` name; the content is identical for the same
  rows, the stagger avoids the overlap). It is stopped with the slice (the v5 stop sequence) and when the frontier
  process ends; its context in progress is then lost, as at every v5 stop. Its log is `<tag>.x.log`.
- `--too-big-only`: standalone pass on the open contexts that have a line and none above `--max-ctx-nodes` (for a
  later high-cap pass, e.g. `--max-ctx-nodes=3000000`, when the loop is not running on the packet).
- Receipt: new fields `skip_file`, `skip_file_sha256_before`, `mode`, `open_at_start`, `selected`,
  `skipped_known_too_big`, `extra` (command, exit, log, event counts), `too_big_recorded`. `command[2]` is still the row
  file (the loop asserts it). `witnesses` now lists the distinct WITNESS events of both logs, each through the
  unchanged exact row check. `peak_sampled_rss_kib` is the maximum over both workers; the 1,200 MiB RSS/swap guard
  applies to each.
- The slice's witness grace and `--stop-witnesses` count the WITNESS lines of both logs (a witness of either worker
  starts the grace), and the outer wall guard, the RSS/swap guard and the stop sequence cover both workers.
- Without a master (`master.txt`, `contexts.json`) or with `--split-open` the runner behaves exactly as v5 (no `--ctx`,
  no record), and `--extra-cap`/`--too-big-only` are refused.

**continue34_v11.py**: the finder call names `run_tree_v6.py` and appends `--extra-cap`/`--extra-threads` when
`--extra-cap` is set. Nothing else changed.

### Exact diff, run_tree_v5.py → run_tree_v6.py

```diff
--- run_tree_v5.py	2026-11-15 05:47:22.791143760 +0900
+++ run_tree_v6.py	2026-11-15 19:07:45.612908486 +0900
@@ -1,5 +1,12 @@
 #!/usr/bin/env python3
-"""Bounded finder only. Exact replay and geometric row audit are separate."""
+"""Bounded finder only. Exact replay and geometric row audit are separate.
+
+v6 (skip list): fastbb2 gets --ctx=<open contexts minus those recorded too big above this cap> instead of every open
+context, so known too-big contexts are not re-walked at every start. Record: <packet>/TOO_BIG.txt, one line
+'<context> <nodes_so_far> <tag>' per context_too_big event (appended here after each run; initial list from
+init_too_big_v1.py). --extra-cap: one extra fastbb2 (same rows, packet, slice) on the recorded too-big contexts with
+the higher cap; its witnesses join the receipt. Selection only: ctx files, witnesses and checks are those of v5.
+"""
 import argparse
 from datetime import datetime
 import gzip
@@ -25,6 +32,10 @@
 p.add_argument('--witness-grace',type=int,default=0)  # v5: end the finder (SIGTERM; ctx files are written atomically) this many seconds after its first logged WITNESS
 p.add_argument('--stop-witnesses',type=int,default=0)  # v5: ... or once this many WITNESS events were logged
 p.add_argument('--budget',type=int,default=34,choices=[34,35])  # v4: budget; runs/b<B>s<T> when B != 34  # v2: fastbb --split-open=L on resume (rewrites that packet's master)
+p.add_argument('--skip-file',default='TOO_BIG.txt')  # v6: per-packet too-big record
+p.add_argument('--too-big-only',action='store_true')  # v6: standalone pass: only open contexts recorded too big, none of them above --max-ctx-nodes
+p.add_argument('--extra-cap',type=int,default=0)  # v6: > --max-ctx-nodes: extra fastbb2 on contexts recorded too big, none of them above this cap
+p.add_argument('--extra-threads',type=int,default=1)
 args=p.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(150<<20,1400<<20))
 W=Path('/home/jay/research/data/es308-20261114')
@@ -39,22 +50,50 @@
 cmd=[str(W/'bin/fastbb2'),'solve',str(inp/'rows.txt'),str(args.budget),str(args.threads),str(args.contexts),str(bb),
      '--slice=1',f'--on-witness={args.on_witness}',f'--time-limit={args.seconds}',
      f'--max-ctx-nodes={args.max_ctx_nodes}','--ktop=16','--dtop=8','--klow=4','--sbiter=1000']+([f'--split-open={args.split_open}'] if args.split_open else [])
+skipf=bb/args.skip_file;known={};xcmd=None;xlog=run/f'{args.tag}.x.log';sel={}  # v6: known = context -> largest nodes_so_far of its too-big attempts
+use_skip=not args.split_open and (bb/'master.txt').exists() and (bb/'contexts.json').exists()  # v6: needs the packet's existing master; split-open renumbers
+assert use_skip or not (args.too_big_only or args.extra_cap)
+assert not args.extra_cap or args.extra_cap>args.max_ctx_nodes
+if use_skip:
+    assert not xlog.exists()
+    if skipf.exists():
+        for line in skipf.read_text().splitlines():
+            if line.strip():c,n=map(int,line.split()[:2]);known[c]=max(known.get(c,0),n)
+    opn=[c['context'] for c in json.loads((bb/'contexts.json').read_text()) if not (bb/f"ctx-{c['context']}.json.gz").exists()]
+    lst=[c for c in opn if (0<known.get(c,0)<=args.max_ctx_nodes if args.too_big_only else known.get(c,0)<=args.max_ctx_nodes)]
+    xl=[c for c in opn if args.max_ctx_nodes<known.get(c,0)<=args.extra_cap]
+    cmd.append('--ctx='+(','.join(map(str,lst)) or '-1'))  # '--ctx=' (empty) would mean all contexts; -1 matches none
+    sel={'skip_file':str(skipf),'skip_file_sha256_before':sha(skipf) if skipf.exists() else None,'mode':'too-big-only' if args.too_big_only else 'frontier',
+         'open_at_start':len(opn),'selected':len(lst),'skipped_known_too_big':len(opn)-len(lst)}
+    if args.extra_cap and xl:
+        xcmd=cmd[:4]+[str(args.extra_threads)]+cmd[5:-1]+['--ctx='+','.join(map(str,xl))]
+        xcmd=[x if not x.startswith('--max-ctx-nodes=') else f'--max-ctx-nodes={args.extra_cap}' for x in xcmd]
+        assert '--on-witness=continue' in xcmd  # stop mode would end the extra worker at its first witness
 def child_limit():
     resource.setrlimit(resource.RLIMIT_AS,(1400<<20,1400<<20))
     resource.setrlimit(resource.RLIMIT_CORE,(0,0))
-start=time.monotonic();peak=0;stop=None;released=set();pos=0;nwit=0;first=None
+def halt(ch):  # v6: the v5 stop sequence, for either worker
+    if ch and ch.poll() is None:
+        ch.terminate()
+        try:ch.wait(timeout=5)
+        except subprocess.TimeoutExpired:ch.kill();ch.wait()
+start=time.monotonic();peak=0;stop=None;released=set();pos=[0,0];nwit=0;first=None;xchild=xout=None
 with log.open('x') as out:
     child=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,preexec_fn=child_limit)
     while child.poll() is None:
-        try:
-            status={line.split(':',1)[0]:line.split(':',1)[1].strip() for line in Path(f'/proc/{child.pid}/status').read_text().splitlines() if ':' in line}
+        if xcmd and xchild is None and b'"event": "start"' in log.read_bytes()[:8192]:  # v6: after the frontier worker has written master.json
+            xout=xlog.open('x');xchild=subprocess.Popen(xcmd,stdout=xout,stderr=subprocess.STDOUT,preexec_fn=child_limit)
+        for ch in [child]+[xchild]*(xchild is not None and xchild.poll() is None):  # v6: same guard for the extra worker
+          try:
+            status={line.split(':',1)[0]:line.split(':',1)[1].strip() for line in Path(f'/proc/{ch.pid}/status').read_text().splitlines() if ':' in line}
             rss=int(status.get('VmRSS','0 kB').split()[0]);swap=int(status.get('VmSwap','0 kB').split()[0]);peak=max(peak,rss)
             if rss>=1200*1024 or swap:stop='internal RSS/swap guard'
-        except (FileNotFoundError,ProcessLookupError,PermissionError):pass
+          except (FileNotFoundError,ProcessLookupError,PermissionError):pass
         if time.monotonic()-start>args.seconds+180:stop='outer wall guard'
         if args.witness_grace or args.stop_witnesses:  # v5: count complete continue-mode WITNESS lines of the log
-            with log.open('rb') as f:f.seek(pos);chunk=f.read()
-            k=chunk.rfind(b'\n')+1;pos+=k
+          for i,lg in enumerate([log,xlog][:1+(xchild is not None)]):  # v6: of both workers' logs
+            with lg.open('rb') as f:f.seek(pos[i]);chunk=f.read()
+            k=chunk.rfind(b'\n')+1;pos[i]+=k
             nwit+=sum(b'"event": "WITNESS"' in l and b'"nodes_so_far"' in l for l in chunk[:k].split(b'\n'))
             if nwit and first is None:first=time.monotonic()  # witnesses come in clusters after the too-big prefix of the context list
             if (args.witness_grace and nwit and time.monotonic()-first>=args.witness_grace) or (args.stop_witnesses and nwit>=args.stop_witnesses):
@@ -68,12 +107,13 @@
                     released.add(q.name)
                 except OSError:pass
         if stop:
-            child.terminate()
-            try:child.wait(timeout=5)
-            except subprocess.TimeoutExpired:child.kill();child.wait()
+            halt(child);halt(xchild)
             break
         time.sleep(1)
 rc=child.wait()
+halt(xchild)  # v6: the slice ends with the frontier worker; the extra worker's context in progress is lost (as at every v5 stop)
+xrc=xchild.wait() if xchild else None
+if xout:xout.close()
 after={q:sha(Path(q)) for q in before}
 assert after==before,'inputs changed during finder'
 result={'label':'COMPUTED finder result; not yet EXACT TREE','slice':args.slice,'budget':args.budget,
@@ -91,17 +131,23 @@
     assert all(len(hs&set(r['support']))>=r['rhs'] for r in rows)
     result['witness']={'holes':h,'independent_exact_row_check':'PASS','rows_checked':len(rows),
                        'scope':'abstract hole vector, not a real point set'}
-ev=[]  # v5: all JSON events of the log; every distinct WITNESS (continue mode: one per context) gets its own exact row check
-for line in log.read_text().splitlines():
+def events(lg):  # v5: all JSON events of the log; every distinct WITNESS (continue mode: one per context) gets its own exact row check
+  ev=[]
+  for line in lg.read_text().splitlines():
     try:e=json.loads(line)
     except ValueError:continue
     if isinstance(e,dict) and 'event' in e:ev.append(e)
+  return ev
+ev=events(log);xev=events(xlog) if xchild else []  # v6: and of the extra worker's log
 counts={};ws=[]
 for e in ev:counts[e['event']]=counts.get(e['event'],0)+1
 st=[e for e in ev if e['event']=='start']
 result.update(on_witness=args.on_witness,events=counts,todo=st[0]['todo'] if st else None,
               processed=counts.get('closed',0)+counts.get('context_too_big',0)+sum('nodes_so_far' in e for e in ev if e['event']=='WITNESS'))
-wev=[e for e in ev if e['event']=='WITNESS']
+xcounts={}
+for e in xev:xcounts[e['event']]=xcounts.get(e['event'],0)+1
+result.update(sel,extra={'command':xcmd,'exit':xrc,'log':str(xlog),'events':xcounts} if xchild else None)  # v6
+wev=[e for e in ev+xev if e['event']=='WITNESS']
 if wev:
     base=json.loads(gzip.decompress((W/'inputs/source-2650.json.gz').read_bytes()))
     rows=base['constraints']+json.loads((inp/'extra.json').read_text())
@@ -112,5 +158,9 @@
         assert all(len(hs&set(r['support']))>=r['rhs'] for r in rows)
         ws.append({'holes':h,'context':e.get('context'),'nodes_so_far':e.get('nodes_so_far'),'independent_exact_row_check':'PASS','rows_checked':len(rows)})
 result['witnesses']=ws
+if use_skip:  # v6: record this run's too-big contexts: frontier at --max-ctx-nodes (tag), extra worker at --extra-cap (tag.x)
+    new=[f"{e['context']} {e['nodes_so_far']} {t}\n" for t,es in ((args.tag,ev),(args.tag+'.x',xev)) for e in es if e['event']=='context_too_big']
+    with skipf.open('a') as f:f.write(''.join(new))
+    result['too_big_recorded']=len(new)
 receipt.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
```

### Exact diff, continue34_v10.py → continue34_v11.py

```diff
--- continue34_v10.py	2026-11-15 06:23:56.132911024 +0900
+++ continue34_v11.py	2026-11-15 19:08:26.255563697 +0900
@@ -9,6 +9,9 @@
 A witness already cut by a row accepted earlier in the same round gets no batch of its own.
 The independent auditor owns geometric reconstruction and exact tree replay (one audit_followup_rows_v4.py process
 per batch v<k>w<i>u). This loop only appends rows having retained literal cake acceptance lines.
+
+v11: the finder is run_tree_v6.py (skip list: contexts recorded too big at or above --max-ctx-nodes in the packet's
+TOO_BIG.txt are not re-walked; optional extra worker on them with --extra-cap). Everything else is v10.
 """
 import argparse
 import hashlib
@@ -41,6 +44,8 @@
 p.add_argument('--probe-minutes',type=float,default=6)  # v8: fixed 6
 p.add_argument('--probe-procs',type=int,default=4)
 p.add_argument('--max-ctx-nodes',type=int,default=50000)  # v10: passed to run_tree_v5 (fastbb2 --max-ctx-nodes)  # v8: fixed 4
+p.add_argument('--extra-cap',type=int,default=0)  # v11: passed to run_tree_v6 (0: no extra worker)
+p.add_argument('--extra-threads',type=int,default=1)  # v11: passed to run_tree_v6
 a=p.parse_args()
 RUN=f's{a.slice}' if a.budget==34 else f'b{a.budget}s{a.slice}'
 PK=W/f'runs/{RUN}'/a.bb;assert PK.is_dir()
@@ -81,10 +86,10 @@
     j=1
     while any((W/f'runs/{RUN}/c{version}s{j}{x}').exists() for x in ('.json','.log')):j+=1
     tag=f'c{version}s{j}'
-    if call(f'finder-{tag}',[PY,'-B',str(TOOLS/'run_tree_v5.py'),str(a.slice),f'--budget={a.budget}',f'--bb={a.bb}',f'--max-ctx-nodes={a.max_ctx_nodes}',
+    if call(f'finder-{tag}',[PY,'-B',str(TOOLS/'run_tree_v6.py'),str(a.slice),f'--budget={a.budget}',f'--bb={a.bb}',f'--max-ctx-nodes={a.max_ctx_nodes}',
                              f'--seconds={seconds}',f'--threads={a.threads}',f'--contexts={a.contexts}',f'--tag={tag}',
                              f'--input-folder={RUN}-v{version}','--on-witness=continue',
-                             f'--witness-grace={a.slice_seconds}',f'--stop-witnesses={a.max_witnesses}']):return None
+                             f'--witness-grace={a.slice_seconds}',f'--stop-witnesses={a.max_witnesses}']+([f'--extra-cap={a.extra_cap}',f'--extra-threads={a.extra_threads}'] if a.extra_cap else [])):return None
     return W/f'runs/{RUN}/{tag}.json'
 def cuts(holes,rows):return any(not set(holes)&set(x['support']) for x in rows)  # rhs-1 row violated iff no hole in it
 
```

## 2. Why it is sound

- **Only the choice of contexts changed.** A context file is still written only by fastbb2 (unchanged binary, same
  options apart from `--ctx`, `--threads` and, for the extra worker, `--max-ctx-nodes`), atomically, for a context it
  closed. Which open contexts a run attempts, in which order and in which process does not enter any context file.
- **The trusted path is unaffected.** The replays (`audit/fresh_replay_v3.py`, the C++ `tcheck_b35`) re-check the
  master and every context file from scratch with the final rows and require the context files to cover the master
  frontier. A wrong or stale TOO_BIG line can only leave a context unattempted, which the replay then reports as a
  missing file (fail-safe); it can never make a context look closed.
- **Rows.** Rows are still appended only by the unchanged `append_cuts_v2.py`, which requires the literal
  `s VERIFIED UNSAT` line and the file hashes of each row's cake_lpr run; the batch audit stays as it is. Witnesses
  (from either worker) only steer candidate selection; every witness still passes the same exact row check against the
  round's rows, and a row's validity rests on its own certificate, never on the witness.
- **Two processes on one packet** is what fastbb2's claim files are for (`ctx-N.claim`, O_CREAT|O_EXCL, stale claims of
  dead processes removed at start); the two lists are disjoint anyway. Both processes use the same input version, so
  the packet `WITNESS.json` that either may write at a natural end is valid for the round's rows, as in v5.
- **Row versions.** The rows are append-only (A2 checked v100-v142; `append_cuts_v2.py` asserts the prefix), so a
  context closed on an older version stays valid for the final replay, as before.
- **Unchanged ctx format, master, witness files** (`WITNESS.json.r<k>w<i>` written by the loop, `witness-ctx-<c>.json`
  by fastbb2), snapshots, cut/certify/append path and resume rule.

What the skip list does give up (progress, not soundness): a context recorded too big at the frontier cap is never
retried by the frontier at that cap, even if later rows would shrink it (A2: 14 of 86 such retries closed, all just
under the cap). These contexts must all be closed by the extra worker or a later `--too-big-only` pass before the
final replay can pass.

## 3. Test (separate namespace)

All test files are new and sit in the test namespace; nothing was written into the live packet, the live inputs or the
live cut folders. `W=/home/jay/research/data/es308-20261114`; `PY` and `T` as in §4. Work files of this track:
`/home/jay/research/data/roadmap-20261115/pm1115/s1/` (`copy_packet.py` `3b0b25b4…`, `measure.py` `056c5d59…`,
`unit_v6.sh`, the saved diffs, the claim JSONs, `render.py`, the section files of these notes).

### 3.1 Test 1: a copy of the live packet, run by the v11 loop

- **Inputs** `W/inputs/b35s20-v600`: byte copy of `b35s20-v143` (`rows.txt` `e8584de6…`, `extra.json` `3313ff96…`,
  4,179 rows), made read-only. It has no `manifest.json` (the tools do not read it; the v9 test's `b35s20-v500` had none
  either). `b35s20-v610` (test 2) likewise.
- **Packet** `W/runs/b35s20/bb-v11test`: `copy_packet.py` (per-file atomic copy, source opened read-only) of the live
  packet's `master.txt`, `master.json`, `contexts.json` and its 998 ctx files at 19:10 (5.9 GB; `master.txt` and
  `contexts.json` byte-identical to the live ones; no claim or tmp files copied).
- **Record** `bb-v11test/TOO_BIG.txt` (`08a7a1f8…`): `init_too_big_v1.py W/runs/b35s20/bb <that file>` over the live
  packet's 45 receipted finder logs (newest receipt c143s1, 18:39:42): 3,270 lines from 43 logs, 232 contexts, **75 open
  contexts recorded above 150,000 nodes**. Cross-check with A2's list of 72 (16:47): the same except 1044 (closed since)
  and 1040, 1046, 1061, 1066 (recorded by c142s1/c143s1).
- **Unit** `esr-ags-v11test` (19:11:30; CPUQuota 150 %, MemoryMax 1500M, MemorySwapMax 0, RuntimeMaxSec 5700, nice
  10, single-thread BLAS):

  ```bash
  $PY -B $T/continue34_v11.py --deadline=2026-11-15T20:35:00+09:00 --start-version=600 --slice=20 --budget=35 \
    --bb=bb-v11test --threads=1 --max-ctx-nodes=150000 --slice-seconds=300 --max-witnesses=12 --accept-per-witness=8 \
    --probe-minutes=6 --probe-procs=1 --extra-cap=300000 --extra-threads=1 --out=continuation-b35s20v11test
  ```

  Test-only deviations from the live line: 1 frontier thread, grace 300 s, 1 probe process. The two fastbb2 processes
  shared the 1.5 CPUs (about 0.75 each).

**Slice 1, `c600s1` (19:11:30-19:58:47, 47.3 min; receipt `W/runs/b35s20/c600s1.json`).**
- Frontier (cap 150,000): `open_at_start` 7,067, `selected` 6,992, `skipped_known_too_big` 75. It closed 25 contexts
  (1069, 1074-1094, 1096-1098; 1,705,939 nodes in 2,779 s of context time) and logged one WITNESS (context 1095 at
  35,404 nodes; exact row check PASS over 4,179 rows). It had no too-big event, and none of its events names one of the 75
  recorded contexts (checked against `TOO_BIG.txt`). The first three, 1069, 1074 and 1075, are the contexts live c143s1
  had left in progress at its time limit; all three closed (148,975, 97,313 and 34,657 nodes).
- Extra worker (cap 300,000, `c600s1.x.log`): todo 75; it **closed 6 of the recorded contexts**: 0, 33, 51, 80, 81 and 97
  (167,479-261,085 nodes; 1,224,414 nodes in 2,048 s). Contexts 0 and 33 alone account for 22 too-big attempts in the live
  logs c134s1-c143s2. Context 96 was too big at 300,000 and was recorded as `96 300001 c600s1.x`.
- The slice ended 300 s after the witness (`stop_reason` "witness slice complete (1 witnesses logged)"). Both workers were
  stopped. The receipt has the new fields as specified, `too_big_recorded` 1, and `contexts_saved` 1,029 = 998 + 25 + 6.
- **Round 600 → 601 (19:58:47-19:59:13, 26 s, unchanged v10 path).** The loop wrote `WITNESS.json.r601w1` and ran pool
  selection plus probe35 (13 candidates). `cut34_v4.py certify` accepted 8 of 8 rows (13.1 s). I checked that each
  `cake.log` has exactly one `s VERIFIED UNSAT` line and that each row misses all 35 holes of the witness. The rows were
  appended by the unchanged `append_cuts_v2.py` as `W/inputs/b35s20-v601` (4,187 rows; `rows.txt` `c5c529d7…`).
  - These are **test rows** (batch `cuts-v601w1u`). They were not audited and must not be counted for (20,15).
  - Their LRATs stay in place. zstd copies, checked byte-equal after decompression, are in `pm1115/s1/lrat-v601w1u/`.

**Slice 2, `c601s1` (19:59:13-20:11:08, 11.9 min, on `b35s20-v601`; receipt `c601s1.json`).**
- Frontier: `open_at_start` 7,036, `selected` 6,967, `skipped_known_too_big` 69. That is the 75 recorded contexts minus
  the 6 the extra worker closed; they now include 96. It closed 6 contexts:
  - 1095, the slice-1 witness context, now closed with the new rows (78,565 nodes);
  - 1099, which slice 1 had left in progress;
  - 1100-1103.
- Extra worker: todo 68, because 96 is now excluded at 300,000. It spent the slice on context 100, whose slice-1 attempt had
  been lost at the slice end, and recorded 100 at 300,000 (`100 300001 c601s1.x`).
- I ended the slice at 20:11:08 by sending SIGTERM to my own frontier fastbb2 process. run_tree_v6 then stopped the extra
  worker, wrote the receipt and appended the record. The loop logged `OPEN` (no witness) and `FINISHED`, and the unit
  ended with result success.

**Resources.** Unit total: 1 h 29 min CPU over 59 min 39 s, memory peak 648.1 MB (journal; MemoryMax 1500M). The
sampled RSS peaks of the fastbb2 workers were 75 MB and 71 MB (1 thread each). Final `bb-v11test/TOO_BIG.txt`:
3,272 lines (`84cafb39…`).

### 3.2 Before and after (re-walk time per round; contexts closed per hour)

Live rounds of v10, 4 threads, cap 150,000. Read-only from the live logs with `measure.py`; COMPUTED. "Re-walk prefix" is
the time until the finder started the first never-attempted context that closed.

| finder | wall (min) | too-big attempts | of them on contexts recorded earlier | re-walk prefix (min) | closed | closed per hour | per thread-hour |
|---|---|---|---|---|---|---|---|
| c139s1 | 81.1 | 66 | 54 | 41.3 | 119 | 88.1 | 22.0 |
| c140s1 | 68.1 | 63 | 63 | 45.5 | 231 | 203.6 | 50.9 |
| c141s1 | 62.8 | 72 | 63 | 43.9 | 82 | 78.3 | 19.6 |
| c142s1 | 56.7 | 75 | 72 | 52.9 | 6 | 6.4 | 1.6 |
| c143s1 | 54.6 | 74 | 73 | 53.0 | 5 | 5.5 | 1.4 |
| c143s2 (v10c, 18:52-20:03) | 70.6 | 77 | 75 | 54.2 | 43 | 36.6 | 9.1 |

The v11 test: 1 frontier thread at about 0.75 CPU, and the extra worker on the rest of the 1.5 CPUs.

| finder | wall (min) | frontier too-big attempts | on recorded contexts | first never-attempted context started at (min) | closed (frontier) | closed per hour | extra worker |
|---|---|---|---|---|---|---|---|
| c600s1 | 47.3 | 0 | 0 | 7.7 (after 3 contexts c143s1 had left in progress; all 3 closed) | 25 | 31.7 | 6 recorded contexts closed, 1 recorded at 300k |
| c601s1 | 11.9 | 0 | 0 | 2.0 (after the slice-1 witness context, which closed) | 6 | 30.2 | 1 recorded at 300k |

**Re-walk time per round (COMPUTED).**
- **Before:** 41-54 min of every live 4-thread round went to re-attempting the recorded contexts, about 2.7-3.6
  thread-hours per round at about 150,000 nodes per attempt. In c142s1, c143s1 and c143s2 that was 77-97 % of the
  finder's time.
- **After:** no attempt on a recorded context, by construction and checked in both slices' logs. The only repeats left are
  the contexts in progress at the previous stop (at most one per thread) and the witness contexts of the previous round.
  Both are real work: all five such contexts in the test (1069, 1074, 1075, 1095, 1099) closed.

**Contexts closed per hour (HEURISTIC, one short test).**
- The v11 frontier closed 30-32 contexts per hour on one thread at about 0.75 CPU, in ids 1069-1103.
- In the same id region, the live c143s2 closed 43 contexts in its last 19 min of forward work at 4 threads, about 34 per
  thread-hour. So the per-thread rate after the re-walk is about the same, as expected with the same fastbb2.
- The gain is the re-walk removed: the last three whole live rounds closed 5.5-36.6 per hour at 4 threads (c139s1-c141s1,
  with fewer recorded contexts, 78-204).
- A v11 loop at 3+1 threads should close several times more per wall-hour than c143s2, and far more than c142s1 or
  c143s1. The factor depends on the witness rate and on the region.
- The extra worker closed 6 contexts in 47 min on about 0.75 CPU. The v10 loop could never close any of them at its cap.

### 3.3 Test 2: record/skip cycle and the standalone mode (unit test)

`pm1115/s1/unit_v6.sh`, unit `esr-ags-v11unit` (20:11:21-20:14:41; CPUQuota 100 %, MemoryMax 1G; 3 min 17 s CPU,
memory peak 44.6 MB).
- Setup: packet `W/runs/b35s20/bb-v11test2` = copy of the v9 test packet's master files (64 contexts, none closed).
  Input `W/inputs/b35s20-v610` = byte copy of `b35s20-v502`. Record from the v9 test's two logs: 46 lines at
  50,001-50,003. Every step ran with `--stop-witnesses=1`, so no packet `WITNESS.json` could be written. None was.
- **u610a** (frontier, cap 20,000, 90 s): skipped the 28 contexts recorded at 50k (above this cap) and selected 36. It
  recorded 24, 28, 30 and 31 (20,001-20,003). Context 32 was abandoned at the time limit and correctly not recorded.
- **u610b** (frontier, cap 20,000, 45 s): skipped 32 = 28 + those 4. It started at 32 and recorded 32 and 33; 34 was
  abandoned.
- **u610c** (`--too-big-only`, cap 40,000, 60 s): selected exactly 24, 28, 30, 31, 32 and 33. These are the contexts
  recorded at about 20k; the 50k ones are above this cap. It recorded 24 at 40,001; 28 was abandoned.
- **u610d** (`--too-big-only`, cap 10,000): nothing selected, so the runner passed `--ctx=-1`. fastbb2 started with todo 0
  and exited 5 (PARTIAL) in 1 s.

## 4. Switching the live loop (for the main session, after review)

Not done by S1. Paths: `W=/home/jay/research/data/es308-20261114`,
`T=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LO33N20261113/budget34/tools`,
`PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python`.

1. **End the v10 loop cleanly.** Let `esr-lo-b35s20v10c` reach its deadline (22:40), or stop it while it is in a
   finder slice (`systemctl --user stop esr-lo-b35s20v10c`; the last event in `W/continuation-b35s20v10c/events.json`
   should be a `CERTIFIED_ROWS_APPENDED` or no event yet, and the newest file in that folder a `finder-c<k>s<j>.log`).
   A stop during a certify stage leaves a cut folder without `accepted.json`, which the resumed round refuses (`OPEN`).
2. **Create the live record once** (read-only over the packet's logs; refuses an existing file):

   ```bash
   cd $W && OPENBLAS_NUM_THREADS=1 $PY -B $T/init_too_big_v1.py $W/runs/b35s20/bb $W/runs/b35s20/bb/TOO_BIG.txt
   ```

   Add `--log=<tag>` for a finder that was stopped with its loop and so has no receipt (for example `--log=c144s1`
   if the v10c loop is stopped during that finder). At 19:10 this gave 3,270 lines, 75 open contexts above 150,000
   nodes (the test packet's copy is `W/runs/b35s20/bb-v11test/TOO_BIG.txt`).
3. **Resume with v11** by the ADDENDUM's rule, reading the last `round` event (version V, receipt R) of
   `W/continuation-b35s20v10c/events.json`: if round V was not appended, `--start-version=V --start-receipt=R`; if it was
   appended as V+1, `--start-version=V+1` and no receipt. State read at 20:18: v10c's round 143 (finder c143s2, 2
   witnesses) was appended at 20:03:59 as `b35s20-v144` (16 rows) and finder c144s1 then started on v144; if nothing later
   is appended, that means `--start-version=144` and no receipt. With the same 4 threads as v10c (3 frontier + 1 extra):

   ```bash
   systemd-run --user --unit=esr-lo-b35s20v11a -p CPUQuota=400% -p MemoryMax=2G -p MemorySwapMax=0 \
     -p RuntimeMaxSec=<seconds to the deadline + 600> --nice=10 --working-directory=$W \
     -E OPENBLAS_NUM_THREADS=1 -E OMP_NUM_THREADS=1 -E MKL_NUM_THREADS=1 \
     $PY -B $T/continue34_v11.py --deadline=<ISO time> --start-version=<V or V+1> [--start-receipt=<R>] \
     --slice=20 --budget=35 --bb=bb --threads=3 --max-ctx-nodes=150000 --slice-seconds=600 --max-witnesses=12 \
     --accept-per-witness=8 --probe-minutes=6 --probe-procs=4 --extra-cap=300000 --extra-threads=1 \
     --out=continuation-b35s20v11a
   ```

   Without the extra worker drop the last two options and keep `--threads=4`. Each finder slice then has the tags
   `c<k>s<j>` (frontier log and receipt) and `c<k>s<j>.x.log` (extra worker). The batch audit is unchanged (one
   `audit_followup_rows_v4.py` process per batch).
4. **Later, a high-cap pass** for the contexts recorded above the extra cap, when no loop runs on the packet (see §5):

   ```bash
   $PY -B $T/run_tree_v6.py 20 --budget=35 --bb=bb --input-folder=b35s20-v<newest> --tag=<new tag> --threads=<t> \
     --too-big-only --max-ctx-nodes=3000000 --on-witness=continue --seconds=<s>
   ```

   (as its own unit). Its witnesses are in its receipt; feed them to the loop with `--start-version=<newest>
   --start-receipt=W/runs/b35s20/<tag>.json`.

## 5. Caveats and what remains

- **Every recorded context must still be closed.** The frontier never retries a context recorded too big at its cap.
  The extra worker covers those up to its cap; the rest need the high-cap pass of §4 before the final replay can pass.
  A2's model expects about 238 contexts above 150,000 nodes in all and about 67 above 300,000 (HEURISTIC).
- **Extra worker and slices.** Its context in progress is lost at every slice end, and it restarts on its list in ID
  order, so its cap must fit inside one slice: 300,000 nodes is about 340 s at the live rate of about 885 nodes per
  thread-second (A2), and a slice that found a witness lasts at least `--slice-seconds` (600 s live). Each slice then
  finishes at least one extra-worker context (closed or recorded at the extra cap), so the worker cannot get stuck.
  A much higher cap (A2 suggested 3,000,000) belongs in the separate pass of §4, not in the loop.
- **Do not run a separate fastbb2 (for example the §4 pass) on the packet while the loop runs.** Both would rewrite
  `master.json` at start (same `.tmp` name), possibly for different row versions, and a natural-end `WITNESS.json` of an
  older version could fail run_tree's packet-witness check in the loop's finder (a crash, not a wrong result). The
  extra worker avoids this by sharing the frontier's row version and slice.
- **Records lost with a killed finder.** A finder killed without writing its receipt (loop stopped mid-slice) does not
  append its too-big events; those contexts are attempted again and recorded then, or added with
  `init_too_big_v1.py --log=<tag>` when the record is first created.
- **Fresh packet.** On a packet without a master the first run behaves as v5 and records nothing; recording starts with
  the second run. Not relevant for `runs/b35s20/bb`.
- **Final replay.** As before, `fresh_replay_v3.py` asserts that `master.json` names the replay's row version; any
  fastbb2 start on that version (for example `run_tree_v6.py … --too-big-only` with nothing left, `--ctx=-1`) rewrites it.
- **Not tested here:** the live packet itself; a natural-end `WITNESS.json` written by the extra worker; the batch audit
  of the test rows (the test namespace's rows `v60x`/`v61x` are test rows and must not be counted for (20,15), as with
  the v9 test's `v50x` rows).
- **Do not copy test ctx files into the live packet.** The contexts closed in `bb-v11test` by slice c601s1 were solved
  with `b35s20-v601`, whose rows 4,179-4,186 are the 8 test rows; in the live inputs those indices hold other rows. A
  replay would reject such files, but there is no reason to risk it. The 5.9 GB test packet and the other test files can
  be deleted later with the owner's OK; nothing was deleted by S1.
- **Claims:** `s1-v11-skiplist` CONFIRMED by VS at COMPUTED (19:47; VERIFY_V11.md), with three wording exceptions, all
  addressed here. They are: no `manifest.json` in `b35s20-v600`; the claim's "36 too-big attempts in c143s2's first 26 min"
  was a live reading and cannot be re-derived from the log; and its list of changes omitted `--too-big-only`, the both-log
  witness counting and the both-worker guards. `s1-v11-test-results` CONFIRMED by VB at COMPUTED (20:20; VERIFY_V11_VB.md),
  including a fresh cake_lpr run on the 8 test rows (8/8). VB did not re-derive the live c143s2 timings, the memory peak
  or the wall times.
