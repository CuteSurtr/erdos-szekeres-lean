# LAUNCH_PLAN: the s35_20 campaign (tag 3520), from the s3520-gate (22 Nov 2026, 22:40 KST)

**Status: PLAN ONLY. The campaign is not launched.** Every cost, time and size below is **HEURISTIC** (projected
from the gate's measurements on this machine). Lean has checked only what `README.md` §1 says (the gate unit and its
controls). Launching is a main-session decision; items marked **owner decision** need the owner's OK.

## 1. What the gate measured on s35_20 itself (machine loaded at 26–28 of 28 threads)

| quantity | value | source |
|---|---|---|
| pre-pass, streamed, all 8,080 contexts (32 GB of gz) | 453.5 s wall, anon + shmem ≤ 155 MB | `logs/pre3520.{out,err,mem}` |
| exporter, largest context (ctx-4274 = unit 2080: 320,422 leaves, 57 modules) | 100.8 s; anon + shmem **705 MB** | `logs/exp4274.*` |
| exporter, unit 161 (47,865 leaves) / unit 1793 (19,035) | 15.6 s, 166 MB / 6.7 s, 103 MB | `controls/v3-3520_u*` |
| exporter rate | 0.000315–0.00035 s per leaf | the three units |
| exporter, 21 units in one process (2060–2080, 1,075,337 leaves) | 5:42 wall; anon + shmem **1,189 MB** (at ctx-4274, the last unit) | `logs/multi3520.*` |
| chunk compile CPU (user + sys) per leaf | unit 2080 **0.0126**, unit 161 0.0125, unit 1793 0.0116; all 68 modules 0.0125; per module 0.0112–0.0142 | `logs/calib_gate.out` |
| chunk compile anon + shmem peak | ≤ **748 MB** (C208024, 7,999 leaves); about 300 MB + leaves / 18; RSS ≤ 3.76 GB (mapped oleans) | `logs/RS3520_*.mem`, `*.log` |
| source / olean bytes per leaf | 816–856 / 1,103–1,153 (all: 821 / 1,108) | `logs/calib_gate.out` |
| import cost (Root/Final/specialisation model) | baseline (RS.Cat3520 + CompactChecker.Path) 213–229 MB; + 57 chunk modules 233–236 MB; + 387 chunk modules (2.43 GB of oleans) 255 MB; the unit sub-root (57 imports, 61 joins, `#print axioms`) 272 MB | `controls/rootmem/*.mem` |

For comparison (res-slices-fv README): s35_19 0.0109 s per leaf and 888 + 1,177 B per leaf at the start of its run;
s34_19 0.0123 s; s35_18 0.0133 s. s35_20 has larger digits (K = 2^24, J = 2^37: one weight is 10,000,000) and a
13-level catalog trie (4,642 rows).

## 2. Cost and wall time (HEURISTIC)

- **Chunk compiles**: 119,054,033 leaves × 0.0116–0.0126 s = **383–417 CPU-h** (per-module extremes 0.0112–0.0142:
  370–470 CPU-h). About 20,900 chunk modules (the gate's 5,696 leaves per module).
- **Export**: 10.4–11.6 h on one thread, plus the 7.6-min pre-pass. One exporter outruns even 12 compiles: it makes
  about 3,000 leaves/s; N compiles take N / 0.0125 leaves/s (958 at N = 12).
- **Root, Final, Res118 specialisation** (each imports the whole chunk closure, about 131–137 GB of oleans, and its
  `#print axioms` walks it): FV304's Root (8,217 chunk modules, 25 GB of oleans) took 8:53 wall at 66 s CPU, its Final
  8:15. Scaled by olean bytes: about 45–50 min each, so about 2.5 h for the three. Risk: FV304's closure (25 GB)
  fit in the page cache; 3520's (about 135 GB) does not fit in 60.9 GB of RAM, so each of the three may re-read it from
  disk, possibly more than once (not measured). Hence `FVR_JOINRT=43200` in the command below.
- **Wall time** (compiles dominate; the per-leaf CPU was measured at today's load, and more threads on SMT siblings may
  raise it):

  | compile slots N | wall for the compiles | plus joins | `FVR_JOBS` while the exporter runs / after |
  |---|---|---|---|
  | 3 | 5.3–5.8 days | + 2.5 h | 4 / 3 (or 4) |
  | 6 | 2.7–2.9 days | + 2.5 h | 7 / 6 |
  | 12 | 1.3–1.4 days | + 2.5 h | 13 / 12 |

  `FVR_JOBS` counts the exporter: with `FVR_JOBS=3` only 2 compiles run during the first ~11 h.

## 3. Memory

- **Exporter**: 705 MB at the largest context in a fresh one-unit process. The campaign exporter runs hundreds of units per launch and keeps
  `code_caches` (one row-code dict per block base, bounded) across them. Measured (`logs/multi3520.*`, units
  2060–2080 in one process, 1,075,337 leaves): maxrss 124 → 618 MB over the first 20 units (it levels off after
  about 12), then **1,189 MB anon + shmem at ctx-4274** (against 705 MB fresh); unit 2080's manifest and module hashes
  were identical to the gate export. So drive v3 restarts the exporter every hour (`--stop-after` from `FVR_EXPSTOP`,
  default 3,600 s; RuntimeMaxSec `FVR_EXPRT`, default 7,200 s; about 12 of the 40 allowed launches; restarts are cheap
  because `prepass.json` is reused) and its MemoryMax default is 3000M (`FVR_EXPMEM`; 1,189 MB = 40 %), with
  `FVR_EXPEST=1500`. Growth over hundreds of units in one process was not measured.
- **Chunk compiles**: MemoryMax 2000M (v2) leaves the measured peak at ≤ 37 %. The v2 estimate 500 + leaves // 10
  (1,300 MB at 8,000 leaves) is 1.7× the measured peak; `FVR_CEST=450,20` (850 MB at 8,000 leaves) is above every
  measured module by ≥ 100 MB. Driver budget `FVR_MEM` ≥ 1,500 (exporter) + N × 850:

  | N | FVR_MEM needed (CEST 450,20) | with v2's estimate (500,10) |
  |---|---|---|
  | 3 | 4,050 (default 5,200 is enough) | 5,400 |
  | 6 | 6,600 | 9,300 |
  | 12 | 11,700 | 17,100 |

  The running memory guard (`esr-memguard-1122f`, read 21:03) has `esr 36000` with track `fvr=10000`; N = 12 does not
  fit the fvr track and N = 6 needs `FVR_MEM` above the v2 default: **owner decision** for N > 3 (threads and memory).
- **Root, Final, specialisation**: projected anon + shmem 1.3–2.1 GB (HEURISTIC: 8–14 MB per GB of imported oleans,
  from FV304's Root (429 MB) and the gate's 387-module import test, plus the 0.22 GB baseline; × 131–137 GB). Set
  `FVR_JOINMEM=4000` (≤ 55 %; these units run after every compile has finished, alone in the fvr track). Check it
  against the s35_19 Root first: its anon peak (`run.tsv` row `root3519`, 7.76 M leaves, about 9 GB of oleans) should be
  about 0.29–0.35 GB; if it is above 0.5 GB, use `FVR_JOINMEM` ≥ (0.22 + (A₃₅₁₉ − 0.22) × 15) / 0.8 GB, which may need
  an owner decision. Splitting the Root into sub-roots does not help here: Lean loads every transitively imported
  module, so the Final and the specialisation import the whole closure anyway (drive v3 therefore gives the same
  `join_mem` to all three).
- **Driver unit**: `root_slice.py` runs as a child inside the driver's cgroup, loads 3,212 manifests and writes a Root
  with about 20,900 imports and 21,000 theorems. Start the v3 driver with MemoryMax 1000M (v2 used 400M).

## 4. Disk (HEURISTIC)

- 119,054,033 leaves: sources 97–102 GB, oleans 131–137 GB, logs about 0.13 GB (6 KB per module).
- **Sources kept**: 228–239 GB at the end.
- **Each source deleted once its olean exists** (**owner decision**; the export is deterministic and every manifest
  keeps its module's sha256, so a source can be regenerated and re-hashed; `audit.py` would need a re-export mode):
  131–137 GB at the end. The exporter finishes after ~11 h, long before the compiles, so nearly all sources exist at
  once; the peak with deletion is therefore about 140 GB rather than the end state.
- Free at 22:38: 704 GB. Disk is not the binding constraint either way.

## 5. Swap-in: drive.py v3 after s35_19 has finished

Preconditions (all):
1. `res-slices-fv/driver.log` says `nothing left to run` with `s35_19` in done, and `esr-fvr-drv` is inactive.
2. The s35_19 finish recipe (res-slices-fv README §9, steps 1–5) is done and accepted: `RS.s35_19` and the five-slice
   `RS.residual_bound_118_fv` with standard axioms, audit and axlines without problems, leaf sum 7,763,206.
3. No YIELD file; Tctl below 86 °C; free disk ≥ 300 GB; the fvr track ≥ `FVR_MEM` (§3).

Commands (main session; they write only in `res-slices-fv`):

```bash
G=/home/jay/research/data/formalize-20261122/s3520-gate; D=/home/jay/research/data/formalize-20261122/res-slices-fv
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
# 1. the tools are the ones the gate checked (prints "OK" lines only)
(cd $G && grep -v '^#' data/tools-frozen.sha256 | sha256sum -c)
# 2. copy the three new tools next to the old ones; nothing in res-slices-fv/tools is replaced
cp -n $G/tools/slice_export_v3.py $G/tools/export_es310_w13l.py $G/tools/drive_v3.py $D/tools/
(cd $D/tools && sha256sum slice_export_v3.py export_es310_w13l.py drive_v3.py)   # must equal data/tools-frozen.sha256
# 3. the v3 driver (3318-3519 are done and skipped; it adopts running esr-fvr-c* units). The campaign takes days.
systemctl --user is-active esr-fvr-drv || systemd-run --user --unit=esr-fvr-drv --collect -p CPUQuota=20% \
  -p MemoryMax=1000M -p MemorySwapMax=0 -p RuntimeMaxSec=691200 --nice=10 \
  --setenv=FVR_JOBS=4 --setenv=FVR_CEST=450,20 --setenv=FVR_EXPMEM=3000 --setenv=FVR_EXPEST=1500 \
  --setenv=FVR_JOINMEM=4000 --setenv=FVR_JOINEST=3000 --setenv=FVR_JOINRT=43200 \
  --working-directory=$D $PY -I -B $D/tools/drive_v3.py
cat $D/status.json; tail $D/driver.log
```

- What v3 then does for 3520: the catalog and bridge are done (`olean/RS/Bridge3520.olean`); the exporter
  `tools/slice_export_v3.py` (unit `esr-fvr-exp3520`, MemoryMax 3000M, RuntimeMaxSec 7,200, `--stop-after 3600`, up
  to 40 launches, resumable: units whose manifest fingerprint matches are skipped) runs its pre-pass, then the units in
  order; chunk compiles start as manifests appear; then the Root (`root_slice.py`, unit `esr-fvr-r3520`), `RS.s35_20`
  (`Final3520`) and the six-slice `RS.residual_bound_118_fv`, all three with `FVR_JOINMEM`/`FVR_JOINRT`.
- To change N later: `systemctl --user stop esr-fvr-drv` (running chunk units continue and are adopted), then start it
  again with new `FVR_JOBS` / `FVR_MEM`.
- Nothing is seeded from the gate: the campaign regenerates the pre-pass and every unit. Afterwards
  `cmp` of the campaign's `export/3520/src/RS3520/C0161*`, `C1793*`, `C2080*` with the gate's copies is a free
  determinism check (expected byte-identical).

## 6. What the main session must check before launching

1. s35_19 finished and accepted (§5 preconditions 1–2).
2. The gate's acceptance in `README.md` §1: pre-pass equal to T7 (119,054,033 leaves); byte identity on 3318 and
   two 3520 units; ctx-4274 exported at 705 MB; all 57 + 8 + 3 chunk modules and `RS3520.U2080.root` with standard
   axiom lines; the corrupted chunk rejected.
3. `data/tools-frozen.sha256` matches (step 1 above).
4. The s35_19 Root's anon peak (§3) → `FVR_JOINMEM`.
5. N (threads under the 28-thread cap and `FVR_MEM` against the fvr track): **owner decision** above N = 3.
6. Disk ≥ 300 GB free (sources kept), and the owner's choice on deleting sources (not needed at 704 GB free).
7. The driver's RuntimeMaxSec (691,200 s = 8 days covers N ≥ 3) and MemoryMax 1000M.
8. YIELD absent; the thermal rule (the driver enforces it per launch).
9. Exporter memory over a launch: watch `esr-fvr-exp3520`'s anon in the first hours (gate: 1,189 MB after 21 units);
   if the memory guard stops it, the driver relaunches it (resumable); lower `FVR_EXPSTOP` if that recurs.

## 7. Break points of res-slices-fv README §8, after the gate

| # | break point | status |
|---|---|---|
| 1 | context ids with a gap at 4782 | fixed (sorted placeholder ids; the contexts digest iterates them); checked by the full pre-pass against T7 |
| 2 | exporter memory, about 12 KB per leaf | fixed: about 2 KB per leaf; 705 MB at the largest context in a fresh process, 1,189 MB after 20 other units (the reference: 903 MB at 47,865 leaves, about 5.4 GB projected at 320,422); hourly exporter restarts and MemoryMax 3000M |
| 3 | exporter deadline | `--stop-after` (control: `--stop-after 0` stops before unit 0 with exit 0 and no manifest; the rerun is byte-identical) plus per-slice `exp_rt` (7,200 s) and `exp_tries` (40); the export needs about 12 hourly launches |
| 4 | the driver hard-codes `slice_export.py` | per-slice `exporter` key (drive v3) |
| 5 | 99 modules per unit | cannot trigger: greedy packing gives at most 2 × leaves / 8,000 + 1 = 81 modules for the largest unit; it has 57 |
| 6 | sub-roots for the Root | the one-file Root of `root_slice.py` stays; `subroot.py` gives a per-unit sub-root (checked on unit 2080). Memory is set by the import closure, which sub-roots cannot shrink (§3) |
| new | the Final and the specialisation import the whole closure too | drive v3 gives them `join_mem` / `join_rt` |
| new | `root_slice.py` runs inside the driver's cgroup | driver MemoryMax 1000M |
| new | `FVR_JOBS` counts the exporter | §2 table |
| new | profiler output splits axiom lines (2 of 75 here) | expected; `axlines.py --reprint` settles them (it reports such lines as "missing", not as "split", when the split falls inside the standard text) |

## 8. Acceptance of s35_20 (pre-registered in README §3; unchanged)

`logs/RS_Final3520.log` with lean_rc 0 and `'RS.s35_20' depends on axioms: [propext, Classical.choice, Quot.sound]`;
`tools/audit.py 3520` with no problems except entries for split axiom lines, which `tools/axlines.py 3520 --reprint`
settles (a whole standard line for every `#print axioms`, from the chunk log or from the re-print). Expect many split
lines (HEURISTIC: 2 of 75 lines here, 4 of 148 modules for s34_19, 4 of 8,217 for FV304, so tens to hundreds over
about 20,900 modules); the driver logs an ALERT line for each such module (not a STOP), and `RP3520.lean` then imports
that many modules (memory as a small join unit); every unit manifest with minimum margin ≥ 1 and 0 leaf-test failures; the leaf sum
119,054,033 (= `skeleton.json` `total_leaves`). Then `RS.residual_bound_118_fv` over six slices with standard axioms:
`ResidualBound 118` **Lean-checked modulo `N66Bound 55` and `BlockValid rowsP/Q/U/A`**. Never quote it before these
checks pass.
