# comp-audit: one-build audit of the 30x composition Lean files (22 Nov 2026)

Status: DONE 06:14 KST (started about 05:50). See the end of this file and AUDIT.md.

Task: rebuild the nine 30x composition files (plus Composition306) in ONE fresh olean directory with the
repo's pinned toolchain, check the library/Mathlib and chain311 olean pins, record the full import closure
(module, LEAN_PATH root, olean sha256; refuse a module provided by two roots), and print axioms of every
composition theorem. Slot `lcmp` (units esr-ag-lcmp-*). Writes only under this directory.

## Milestones
- by 05:59 (before unit_compile.sh was written at 05:59:27) orientation done: the ten sources match their record sha256 (Composition306 has no record hash; it is
  clean against git HEAD). Toolchain v4.24.0 (commit 797c613e), lean-toolchain and lake-manifest sha256 equal
  the chain311 pins. Earlier compiles of these files reported 3,087-3,709 MiB `time -v` max RSS (build_zsn.log,
  FV304 bbz.log). How much of that is shared olean mappings is not yet measured.

## Memory rule (pre-registered before the first driver run at 06:02:06 KST, so before any compile)
(Units: every MB figure in this file and in AUDIT.md is MiB, 2^20 bytes, as in systemd's MemoryMax=3500M
and memguard.sh. This note was added at 06:14; the rule itself is unchanged.)
- Each compile runs in its own unit `esr-ag-lcmp-<module>` (MemoryMax=3500M, MemorySwapMax=0, CPUQuota=100%,
  RuntimeMaxSec=7200, nice 10), one at a time. The memory guard `esr-memguard-1122b` counts anon + shmem + swap
  and stops a unit at 95 % of its limit; page cache is not counted.
- STOP and report (no further compile) if a unit's cgroup `memory.peak` >= 2,800 MB (80 % of 3500M), or its
  `memory.events` shows any `high`, `max`, `oom` or `oom_kill` event.
- `time -v` max RSS is reported beside the cgroup peak and a sampled anon peak for every compile. Max RSS over
  2,800 MB is NOT by itself a stop under this reading (the earlier 3,087-3,709 MiB figures include mapped olean
  files); if it happens it is stated first in AUDIT.md's memory section and in the open issues, so the
  orchestrator can overrule this reading.
- Pin hashing (about 6.5 GB of oleans; measured afterwards: 2.32 GiB of pinned library oleans plus the 196
  chain311 oleans) runs in the launcher, outside the compile units, so that page cache is
  not charged to them.
- Gates before each unit: no YIELD file, Tctl < 86 C, ag-track and esr-total guard usage each at least
  1,500 MB below their budgets (7,000 / 34,000 MB); poll every 60 s, give up after 30 min.
- 06:02:06 driver run 1 started: `python3 -I -B comp_audit.py` (log driver.log, state result.json). Files here:
  comp_audit.py (driver), unit_compile.sh (unit body), src/ (read-only copies), out/olean/ (the one fresh
  output dir), logs/ (one log per unit), audit/Audit.lean.
- 06:02 first real compile (LemmaZ, run 2): lean_rc 0, 9.7 s wall; cgroup memory.peak 1,057 MB, sampled anon
  peak 909 MB, no memory events (passes the pre-registered rule); `time -v` max RSS 3,765 MB (above 2,800 MB:
  FLAGGED, see the memory rule). The driver then crashed on a JSON bug (axiom sets); fixed, run 3 started
  06:03:29 with a fresh output dir. Run 1 refused on the unbuilt `Cli` root (library.json pins nothing there;
  the check now matches drive_es310.check_library).
- 06:05:51 run 3 PASSED (verdict in result.json: "audit passed"). Ten files built in one fresh dir (out/olean);
  31 theorems, all `[propext, Classical.choice, Quot.sound]`; closure 4,980 modules, every one pinned and
  provided by exactly one root; negative control refused (LemmaZ.olean). Fresh oleans are byte-identical to the
  older leanz/leanzs/fv304 copies. Memory: cgroup peaks <= 1,053 MB, anon <= 909 MB, no events; `time -v` max
  RSS 3,094-3,776 MB (FLAGGED, AUDIT.md section 6).
- 06:09:39 AUDIT.md written (the full report; record fixes 06:10 and 06:14). Independent re-check of closure.tsv: 4,980 rows, 0 bad.

## Status: DONE (06:14 KST). Read AUDIT.md.
Label: each of the 31 theorems is Lean-checked as stated; ES(8) <= 304 stays Lean-checked modulo its three
hypotheses (composition_304_z) and no new bound is claimed. Nothing is running; no unit of slot lcmp remains.
