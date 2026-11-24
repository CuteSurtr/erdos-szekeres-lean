# Launch note for the s35_20 campaign (main session, 24 Nov 2026, about 01:30 KST)

**Owner decision (24 Nov, about 01:25):** "Run the Lean campaign" for s35_20. This supersedes the "Not now" of 23 Nov
about 01:05. Chunk sources are kept (owner, 23 Nov: "No, keep sources"). The owner also asked to "fully utilize this pc".

This note applies the four required fixes of `review/VERIFY_s35_20-gate.md` without editing any frozen or hashed
file (LAUNCH_PLAN.md, README.md and the tools keep their hashes):

1. **FVR_JOBS counts the exporter.** drive_v3 counts every active esr-fvr-* unit, the exporter included. The launch
   below uses `FVR_JOBS=4`: the exporter plus 3 chunk compiles while the export runs (about 11 h), then 4 compiles.
   More than 3 compiles is the owner's call; the owner's "fully utilize this pc" is taken as that OK. N is to be raised
   (driver stop, restart with a larger FVR_JOBS and FVR_MEM; running units are adopted) only after the proof re-checks
   (`esr-vfy-all`) end, because of the esr memory total and the yield guard's 33,000 MB threshold.
2. **FVR_CEST wording (LAUNCH_PLAN §3).** The estimate 450 + leaves/20 exceeds every measured module by at least 97 MB
   (C208057: estimate 677, measured 580), not "at least 100 MB". "Levels off after about 12 units" is not shown: maxrss
   is a high-water mark and still rose 546 -> 618 MB over units 13-20. "<= 37 %" is 37.4 %.
3. **Audit deadline (LAUNCH_PLAN §8).** The `audit.py 3520` unit reads about 100 GB of sources and 135 GB of oleans:
   give it a deadline of several hours (e.g. RuntimeMaxSec 21600), not the 3600 s of the 3519 example.
4. **Acceptance item 3 of the gate** (a whole standard axiom line in every chunk log) was met only through re-prints
   for C208014 and C208053 (profiler output split them); the re-prints show the standard axioms. The pre-registration
   README hash was re-verified by the reviewer from the worker's transcript (`review/logs/README_at_prereg_sed.md`).

**FVR_JOINMEM.** LAUNCH_PLAN §3 asks to check the s35_19 Root's anon peak first: run.tsv `root3519` peak_mb = 916
(anon + shmem, sampled), above the 0.5 GB threshold, so the plan's rule gives FVR_JOINMEM >= (0.22 + (0.916 - 0.22) x
15) / 0.8 = 13.3 GB. Launch value: `FVR_JOINMEM=14000` as a placeholder (a x15 extrapolation from one point; re-derive
it before the Root starts, e.g. from the exporter's final closure size), with the memory guard's fvr track raised to
16,000 MB (guard `esr-memguard-1124b`). `FVR_JOINEST=3000` <= FVR_MEM (default 5,200), so the Root can be admitted.

**Pre-launch checks done (24 Nov 01:20-01:30):** s35_19 accepted (res-slices-fv README update of 23 Nov 16:30);
`data/tools-frozen.sha256` OK; the three v3 tools copied into res-slices-fv/tools with equal hashes; no 3520 state in
res-slices-fv (no export/3520, no olean/RS3520, no 3520 entry in tries.json; only the prebuilt Cat3520*, Bridge3520 and
FinalTest3520 oleans); baseline hashes of olean/RS/*.olean in `res-slices-fv/data/olean_RS_baseline_20261124.sha256`
(45 files); disk 878 GB free; the driver enforces YIELD and the Tctl gate per launch.

**Command:**

```bash
D=/home/jay/research/data/formalize-20261122/res-slices-fv; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
systemd-run --user --unit=esr-fvr-drv --collect -p CPUQuota=20% -p MemoryMax=1000M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=691200 --nice=10 --setenv=FVR_JOBS=4 --setenv=FVR_CEST=450,20 --setenv=FVR_EXPMEM=3000 \
  --setenv=FVR_EXPEST=1500 --setenv=FVR_JOINMEM=14000 --setenv=FVR_JOINEST=3000 --setenv=FVR_JOINRT=43200 \
  --working-directory=$D $PY -I -B $D/tools/drive_v3.py
```

**First-hour checks:** slices 3318-3519 skipped and olean/RS unchanged against the baseline; the pre-pass gives
119,054,033 leaves and the gate's context digest, context 4782 absent; the exporter near 1.2 GB; the first chunk logs
`lean_rc=0` with compiles under about 750 MB; unit 161's modules byte-identical to the gate's copies.

## 24 Nov 04:55: the 9 axiom ALERTs of s35_20 are log interleaving (no axiom problem)
drive_v3 flagged 9 of 452 compiled modules ("axiom lines are not the standard three"; all lean_rc 0): C002901,
C002914, C003011, C003206, C003602, C003704, C005602, C005903, C006702. In each log the profiler's stderr message
".olean serialization took N ms" is printed inside a `#print axioms` line (e.g. "[p.olean serialization took 140ms
/ropext, Classical.choice, Quot.sound]"). `fv302-20261124/tools/axiom_audit.py` removes exactly that fragment and
then requires every axiom line to end with "depends on axioms: [propext, Classical.choice, Quot.sound]", lean_rc=0 and
no sorryAx/ofReduceBool: the 9 logs pass (13 axiom lines), the corrupted FV302 control log fails (as it must). The
driver is unchanged (an axiom ALERT only logs). Decisive at the end: `#print axioms` of the slice's final theorem
(transitive over all imports) and axiom_audit.py over every module log.

## 24 Nov 05:00: determinism, unit 161
The campaign's export of unit 161 equals the gate's: its 8 modules (C016101-C016108) are byte-identical (cmp), and
ctx-0161.json differs only in "seconds" (15.6 vs 10.7). Units 1793 and 2080 are not exported yet (exporter near
unit 1,269); compare them when they are.

## 24 Nov: restarts of the driver (resumable; it adopts running units)
- 06:13 FVR_JOBS=6 (after the K9/c6upper re-check freed its 2 threads); 08:48 FVR_JOBS=10 with FVR_MEM=8000 (s35_20
  has about 60 % of the remaining compile work of s35_20 + FV302; memory is not binding, heat is: Tctl 83-85 C). The
  current restart command = the launch command above with `--setenv=FVR_JOBS=10 --setenv=FVR_MEM=8000`. Progress at
  08:48: 2,946 units exported, 1,267 modules compiled (6,992,739 leaves), all lean_rc 0; exporter restarts are the
  FVR_EXPSTOP=3600 cycle (exp_tries 40).
- Export complete (about 10:06; noticed 14:50): 3,212 manifests = skeleton.json "units" 3,212; leaves 119,054,033 =
  the pre-registered total (skeleton total_leaves); 21,495 modules. At 14:50: 4,043 modules compiled (22,393,597
  leaves, 18.8 %), all lean_rc 0; 734 leaves/s over the last 2 h at 10 jobs (HEURISTIC: chunks done about 26 Nov 03:30,
  then the Root join).
- 17:3x FVR_JOBS=13, FVR_MEM=10000 (the M(16) run ended 17:29:54; its 3 lanes and the re-checker freed). Restart command = launch command with these two values.
