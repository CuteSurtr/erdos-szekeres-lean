# ES(8) <= 310 compact check: operator runbook (written 6 Nov 2026)

**ES(8) <= 310 is NOT proved.** The statement may be written as "Lean-checked, compact, unrefereed" only after
every gate in section C passes and `logs/es310/final310-compact.json` says `"verified": true` with mode `real`.

Everything in sections A2-A4 and B needs the user's go-ahead first: the freeze, the transient scopes
(every compile and the exporter run in their own `systemd-run --user --scope`), the job counts and the
memory caps. Nothing here touches the campaign's files, its unit `es8-b64-campaign` or `c6upper-noty12`.

```
D=/path/to/repo/experiments/omission-compact-checker-2026-11-05
C=/path/to/data/es8-b64-pilot-20261105
SRC=/path/to/repo/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json
OUT=$D/build/es310/full
K=16      # per-word k (calibration E5: k=16 recommended, k=8 the conservative choice; user decision)
cd $D
```

## Exit codes (all scripts)

| script | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| `export_es310.py` | ok | refused: the run (`refused`) or some contexts (`refused_ctx`; the others were exported) | ALERT: inputs of exported contexts changed (`ALERT-changed-inputs.txt`, latched) | some `--ctx` context not ready (never with `--all-closed`) | lock held: retry later | a context exported by another exporter sha256 (`stale_exporter`) |
| `merge_es310.py` | ok | refused | ALERT | - | lock held: retry later | - |
| `coverage_es310.py` | PASS | FAIL | usage / environment | - | lock held: retry later | - |
| `drive_es310.py` | everything selected done | some module's last verdict not ok | - | work left undone (STOP file, or `--mem-wait-max`: nothing ran and memory blocked) | - | WITNESS file in the campaign |
| `assemble_final310.sh` | VERIFIED (real mode) / TEST ONLY (test modes) | refused / FAILED | usage | - | - | - |

What to do on each non-zero code:
- **4**: run the same command again later (another export, merge or coverage holds `OUT/.export.lock`).
- **exporter 1 with only `refused_ctx`**: the other contexts were exported. Read the reason in the last line of
  `$OUT/export-runs.jsonl`. "the tree file is damaged" means a broken gz behind a result older than 600 s: tell
  the user; do not delete or rewrite anything in C. Every later cycle will exit 1 until that is resolved.
- **exporter 1 with `refused`**, **2 (ALERT)**, **5**, **coverage 1**, **driver 1**: stop the cycle and tell the
  user. Never delete `ALERT-changed-inputs.txt` or any export file without the user. Exit 5 after the freeze
  means `export_es310.py` changed: that must not happen.
- **driver 5 / any WITNESS file**: `touch $OUT/STOP`, run nothing more, keep every file, tell the user.
- A warning `code_changed` (exporter, merge) or "campaign code: run_context.py ..." (coverage) means
  `run_context.py` or `pbb_strong.py` was edited. It is recorded only (every leaf is replayed by the exporter
  and checked by Lean); report it to the user, no action needed.

## Never during the run (from now until the assembly is done; ops review item 1)

- No `lake build`, `lake update`, `lake clean`, no lean-lsp `lean_build`, no editor build in the repository.
- No edit to `CompactChecker/*.lean`, `lean-toolchain`, `lake-manifest.json`, or to any frozen script
  (`export_es310.py`, `merge_es310.py`, `drive_es310.py`, `coverage_es310.py`, `export_es311.py`,
  `shapes_es311.py`, `assemble_final310.sh`, `assembly/Final310Compact.lean`).
- No `git checkout main` (it deletes CompactChecker sources and the 311 scripts that exist only on this
  branch), no `git clean -x` (it deletes `build/`). Do P1 work in a separate worktree without building.
- Never write into, rebuild or delete `build/es311`, `build/CompactChecker`, `build/ext`, `build/chain311` or
  any `.lake` directory. The E311R side is reused from `build/es311/full` and is never recompiled.

## A. While the campaign runs: incremental export, partial coverage, compile of closed contexts

### A1. Once, before the first real export (user decisions: k, the freeze)

```
mkdir -p $OUT logs/es310
bash test_export_es310.sh && bash test_coverage_es310.sh        # Python only; must end "0 failed"
./freeze_es310.sh $K                                           # fills EXPORTER/MERGE/DRIVER/COVERAGE_SHA256 in
                                                               # assemble_final310.sh; writes logs/es310/frozen-shas.txt
bash test_assemble_final310.sh                                 # again: the assembly script's sha256 changed (gate 6)
PIN=$(sed -n 's/^EXPORTER_SHA256=\([0-9a-f]\{64\}\)$/\1/p' assemble_final310.sh); echo $PIN
```
`freeze_es310.sh` refuses if any pin is already set or the record exists. After it, none of the frozen files
may change; `export_es310.py` with another sha256 makes every context "stale_exporter" (exit 5).

### A2. Each cycle (every 1-2 h; strictly in this order; stop at any exit code not listed as fine)

1. Export every closed context not yet exported (fine: 0; 4 = retry later):
   ```
   systemd-run --user --scope --quiet -p MemoryMax=4G -p MemorySwapMax=0 nice -n 19 \
     python3 -I export_es310.py --campaign $C --source $SRC --out $OUT --all-closed \
     --per-word $K --chunk-leaves 12000 --block-leaves 64 >> $OUT/export-runs.jsonl 2>> logs/es310/export-full.err
   echo "export exit $?"; tail -1 $OUT/export-runs.jsonl | cut -c1-400
   ```
   Measured on 50 contexts (ops review): 0.123 s per context + 0.735 ms per leaf, peak RSS 518 MB; the first
   run (about 480 closed contexts) takes about 25 min, later runs about 2 min per campaign hour.
2. Merge (fine: 0; 4 = retry later):
   ```
   nice -n 19 python3 -I merge_es310.py $OUT --partial >> $OUT/merge-runs.jsonl 2>> logs/es310/merge-full.err; echo "merge exit $?"
   ```
3. Partial coverage, exact exporter pin (fine: 0; 4 = retry later):
   ```
   nice -n 19 python3 -I coverage_es310.py $OUT --partial --campaign $C --jobs 2 --cache $OUT/coverage-cache.json \
     --exporter-sha256 $PIN --report logs/es310/coverage-partial-last.json > /dev/null; echo "coverage exit $?"
   ```
4. Compile the new chunks, only if no driver is running on `$OUT` (`pgrep -f 'drive_es310\.py.*es310/full'`
   prints nothing). It starts a Lean job only when Tctl < 80 C, no campaign PAUSE line is newer than 10 min,
   MemAvailable >= 15 GiB, and 60 s have passed since the last start; it never stops a running job:
   ```
   nohup python3 -I drive_es310.py $OUT --reuse build/es311/full:E311R --no-final --jobs 2 --nice 10 \
     --max-tctl 80 --start-gap 60 --memory 12G --root-memory 24G >> logs/es310/drive-full.log 2>&1 &
   ```
   Fine: exit 0 (queue done) or 3 after a STOP file. With a partial manifest there is no Root: only chunks.
   At 2 jobs it compiles about 2 CPU-h per hour against 0.8-1.0 CPU-h per hour that the campaign produces.

Pause the driver: `touch $OUT/STOP` (it starts nothing more; running compiles finish; exit 3); remove the file
before the next start. Stop it at once: `pkill -TERM -f 'drive_es310\.py.*es310/full'` (its compiles are
killed, nothing is recorded for them, exit 130; the next start cleans up).

Optional, once about 2,000 chunks are compiled (ops review item 10; user approval): one capped Lean job
(MemoryMax=24G, MemorySwapMax=0, nice 10, Tctl < 85 C) that imports the compiled chunks and prints the axioms
of each `ex0`, reading `$OUT/olean` only, to measure the import and the axiom walk at scale before the Root.

## B. After `ALL 4096 CONTEXTS CLOSED`

### B1. The campaign is finished (gate 1)
```
grep -q ' ALL 4096 CONTEXTS CLOSED$' $C/campaign/campaign.log && ! systemctl --user is-active --quiet es8-b64-campaign \
  && [ ! -e $C/campaign/WITNESS-ALERT.txt ] && ! compgen -G "$C/runs/*WITNESS*" > /dev/null && echo CAMPAIGN DONE
```
If a context failed twice, there is no such line (`campaign.py:139`): tell the user (restart of the supervisor
or a manual run is their decision). If a WITNESS file exists: stop, keep every file, tell the user.

### B2. Final export, merge, coverage, shapes
```
sleep 150                                  # every result older than 120 s
# A2 step 1 again: must exit 0, with "not_ready": {} and "refused_ctx": {} in the last export-runs.jsonl line
ls $OUT/ctx/ctx-*.json | wc -l             # 4096
nice -n 10 python3 -I merge_es310.py $OUT --complete >> $OUT/merge-runs.jsonl; echo "merge exit $?"     # writes src/E310B/Root.lean
nice -n 10 python3 -I coverage_es310.py $OUT --complete --campaign $C --jobs 8 --exporter-sha256 $PIN \
  --report logs/es310/coverage-complete.json > /dev/null; echo "coverage exit $?"                     # gate 3: 0
nice -n 10 python3 -I shapes_es311.py $OUT > logs/es310/shapes-full.json; grep '"PASS": true' logs/es310/shapes-full.json
```
Estimated: merge under 1 min, coverage about 2.5 min at `--jobs 8`, shapes about 1 min.

### B3. Compile the rest, then the Root and E310.Final (user approval of the job count)
```
python3 -I drive_es310.py $OUT --reuse build/es311/full:E311R --dry-run | head -1 | cut -c1-600
#   check: "final": "added", "reuse" with 127 modules, "library_pinned_verified": 4952, "stale_after_imports": {}
nohup python3 -I drive_es310.py $OUT --reuse build/es311/full:E311R --jobs 12 --nice 10 --max-tctl 85 \
  --start-gap 20 --memory 12G --root-memory 24G >> logs/es310/drive-full.log 2>&1 &
```
The ops review suggests `--jobs 16` (16 physical cores) after the campaign; start with 12 and watch Tctl
(the 311 run reached 95.6 C with 8 Lean jobs beside the campaign). The Root (4,096 imports, 4,095 split_pm
steps; probe: 100 s, 2.6 GB anonymous) and E310.Final each run alone under 24G; the driver waits until
MemAvailable >= 34 GiB and stops with exit 3 after `--mem-wait-max` (30 min) if it cannot start one.
Done when the driver exits 0 and a `--dry-run` shows `"to_run": 0` (gate 4).

### B4. The assembly (gates 2-6)
Close Lean editors and lean-lsp tools first (not required for the count any more, but they use memory).
```
bash assemble_final310.sh --dry-run; echo "dry exit $?"      # 0: every check passed, nothing compiled
A310_MEM=24G bash assemble_final310.sh; echo "assembly exit $?"
python3 -c 'import json; d=json.load(open("logs/es310/final310-compact.json")); print(d["verified"], d["mode"], d["statement"], d["axioms"], d["problems"])'
```
Required: last line `VERIFIED ErdosSzekeres.Omission.Compact310.forces_convex_octagon_310 :
ErdosSzekeres.ForcesConvexNGon 310 8 (standard axioms only)`, and in the JSON `"verified": true`,
`"mode": "real"`, axioms within {propext, Classical.choice, Quot.sound}, `"problems": []`. A line starting
"TEST ONLY" is never a verification.

## C. The gates (design section F, with the fixes of 6 Nov)

1. `campaign.log` says `ALL 4096 CONTEXTS CLOSED`; the unit is inactive; no WITNESS file (B1).
2. 4,096 context manifests, all by the one pinned exporter sha256 and one parameter set, min margin >= 1, no
   corrupted module; inputs re-hashed at export, merge, coverage and assembly (assembly check-run).
3. `coverage_es310.py --complete` PASS with `--exporter-sha256 $PIN` (exact), on the manifest the assembly checks.
4. `run.tsv`: every E310B chunk, `E310B.Root` and `E310.Final` ok with current stamps, unchanged `.olean`, every
   import compiled before its importer; E311R's 127 modules verified in place (driver and assembly).
5. `assemble_final310.sh` real mode: `"verified": true`; the compiled source is the pinned copy of
   `assembly/Final310Compact.lean`; every non-library `.olean` in the environment has its recorded sha256;
   statement exactly `ErdosSzekeres.ForcesConvexNGon 310 8`; one axiom line, standard axioms only.
6. The tests (`test_export_es310.sh`, `test_coverage_es310.sh`, `test_driver_es310.sh`,
   `test_assemble_final310.sh`) passed with the frozen script sha256s; the assembly checks the pins of the
   exporter, merge, driver, coverage and shapes scripts itself.
