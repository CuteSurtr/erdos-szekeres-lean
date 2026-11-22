# combined (part 1): one end theorem per bound (ES(8) ≤ 304, 303, 302), everything Lean-checked plugged in

Item `combined`, slot `lcb`, track `ag` (units `esr-ag-lcb-<job>`; ag budget 8,000 MB shared with one other agent).
Work directory, the only place this agent writes: `/home/jay/research/data/formalize-20261122/combined`. Nothing in
the git repository is edited; no git writes; no lake, no lean-lsp. Lean only with the bare
`/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1`, read-only LEAN_PATH, `-o` only into `out/`.

<!-- STATUS -->
- 22 Nov 21:55 KST: **part 1 DONE** (M0-M6). Nothing of this slot is running. Not reviewed yet.
- 21:33-21:52 M5 audit passed (`esr-ag-lcb-audit2` after adding the 311 route record as a pin source; `audit3` with
  the final tool; `audit4` with the start marker moved to 21:05:00, §5): closure
  13,635 modules, one provider each, 13,635/13,635 hashes equal their pins (only `RS.Lib`'s olean has no earlier
  pin), E304Z part identical to fv304-audit's (digest `fa02576e…`), 3,464 companions identical; 0 files newer than
  the start marker in the read-only stores.
- 21:30 ES302 recompiled with the `n66Bound_mono` guard; negative control `BadSwap` rejected as expected.
- 21:20-21:30 M4: `Combined.ES304` compiled (9:25 wall, anon+shmem peak 520 MB).
- 21:19-21:20 M1-M3: links (230; 229 equal earlier pins), `Combined.Residual`, `Combined.ES303`, `Combined.ES302`.
- ~21:15 orientation done; plan and memory rule written before the first unit (21:19:14).
<!-- /STATUS -->

| M | content | state |
|---|---|---|
| M0 | orientation, plan, memory rule | done |
| M1 | `links/` (file-level symlinks), `tools/env.sh` (LEAN_PATH), two-roots check + negative control | done |
| M2 | `Combined.Residual` | done |
| M3 | `Combined.ES303`, `Combined.ES302` | done |
| M4 | `Combined.ES304` (imports `E304Z.Final`) | done |
| M5 | import audit (union closure, one provider each, sha256 vs pins, companions, mtimes, read-only stores) | done |
| M6 | Lean negative control, `Switch3519.lean` template, REMAINS.md, final README | done |
| next | s35_19 switch when `RS.s35_19` is accepted (§9); part 2: plug in N66 | open |

## 1. Headline

Four end theorems compile with axioms exactly `[propext, Classical.choice, Quot.sound]`, each enforced by
`#guard_msgs`. Their hypotheses are exactly the inputs that are not Lean-checked yet (REMAINS.md has the list with
labels and evidence):

| bound | Lean theorem | label (es-research §2) |
|---|---|---|
| ResidualBound 118 | `Combined.residual_bound_118` | Lean-checked modulo `N66Bound 55`, the 2,025 row-text verdicts `RowsTextUnsat rowsP/Q/U/A` with trust items E1-E6, and the slices `s35_19`, `s35_20` |
| ES(8) ≤ 304 | `Combined.es304` | Lean-checked modulo the same: `N66Bound 55`, the 2,025 row verdicts (E1-E6), `s35_19`, `s35_20` |
| ES(8) ≤ 303 | `Combined.es303` | Lean-checked modulo `ExcludesHoleBudgetZZsF 68` (the budget-68 tree) and the same four |
| ES(8) ≤ 302 | `Combined.es302` | Lean-checked modulo `ExcludesHoleBudgetZZsN 16 69`, `N66Bound 54` and the same row verdicts and slices. **Not a bound claim**: the budget-69 tree does not exist yet |

**No bound and no record label changes.** ES(8) ≤ 304 and ≤ 303 stay as the records state them (computer-assisted,
unrefereed); what changed is how much of each is inside one Lean theorem. Not reviewed yet.

Compared with `FV4A.forces_304_of_slices_rows_n66` (the previous best Lean form of 304): the four `BlockValid`
hypotheses are replaced by their per-row CNF verdicts (res118-rowblocks), and four of the six slices
(`s33_18`, `s34_18`, `s35_18`, `s34_19`) are discharged by the compact-checker theorems of res-slices-fv.
`RS.s34_19`'s own review is still pending (REMAINS.md).

## 2. Statement (`src/Combined/*.lean`, as printed by `#check` in `logs/*.log`)

```lean
theorem Combined.residual_bound_118 (n66 : OmissionZRow.N66Bound 55)
    (hP : RowGeo.RowsTextUnsat Res118.rowsP) (hQ : RowGeo.RowsTextUnsat Res118.rowsQ)
    (hU : RowGeo.RowsTextUnsat Res118.rowsU) (hA : RowGeo.RowsTextUnsat Res118.rowsA)
    (s35_19 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsU) 35 19)
    (s35_20 : Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ ++ Res118.rowsA) 35 20) :
    ErdosSzekeres.Omission.Partition.ResidualBound 118
theorem Combined.es304 (n66 …) (hP …) (hQ …) (hU …) (hA …) (s35_19 …) (s35_20 …) : ErdosSzekeres.ForcesConvexNGon 304 8
theorem Combined.es303 (tree68 : OmissionBalancedZZsF.ExcludesHoleBudgetZZsF 68) (n66 : OmissionZRow.N66Bound 55)
    (hP …) (hQ …) (hU …) (hA …) (s35_19 …) (s35_20 …) : ErdosSzekeres.ForcesConvexNGon 303 8
theorem Combined.n66Bound_mono {a b : ℕ} (hab : a ≤ b) (h : OmissionZRow.N66Bound a) : OmissionZRow.N66Bound b
theorem Combined.es302 (tree69 : OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69) (n54 : OmissionZRow.N66Bound 54)
    (hP …) (hQ …) (hU …) (hA …) (s35_19 …) (s35_20 …) : ErdosSzekeres.ForcesConvexNGon 302 8
```

(`…` = the same types as in `residual_bound_118`.) Proofs, one line each:
- `residual_bound_118 := RowGeo.residual_bound_118_of_texts n66 hP hQ hU hA RS.s33_18 RS.s34_18 RS.s34_19 RS.s35_18 s35_19 s35_20`;
- `es304 := E304Z.Final.forces_304_of_n66_res n66 (residual_bound_118 …)`;
- `es303 := OmissionBalancedZZsF.composition_303_zzsf tree68 n66 (residual_bound_118 …)`;
- `es302 := OmissionBalancedZZsN.composition_302_n54 tree69 n54 (residual_bound_118 (n66Bound_mono (by norm_num) n54) …)`.

`RowGeo.RowsTextUnsat rows` (res118-rowblocks) = every `EncB.parseDimacsBytes` parse of the UTF-8 bytes of
`RowEnc.rowText s` (what `rowprint row B I` writes) is unsatisfiable, for every `s ∈ rows`: the meaning of the
cake_lpr verdicts on the 2,025 certified row files.

## 3. Model and soundness

- The kernel checks the four compositions; every piece they use was kernel-checked when its module compiled:
  FV304 (`E304Z.Final`, closing audit fv304-audit), res118-rowblocks (`RowGeo.Blocks`), res-slices-fv
  (`RS.Final3318/3418/3518/3419`), Res118, and the comp-audit rebuilds of `BalancedBudgetsZZs(N)`.
- An import trusts the .olean bytes. The audit (§5) therefore fixes which bytes were imported, from which root, and
  that each equals a hash recorded earlier.
- That each `RS.*` theorem has exactly Res118's binder type is checked here by Lean: `Combined.residual_bound_118`
  passes them as Res118's arguments. The control (§6) shows a swapped slice is rejected.
- Trust items for the row texts (ENCBLEAN wording): E1 printer output = certified bytes (checked for all 2,025 rows
  by res118-rowblocks M9), E2 the cake_lpr verdicts, E3 cake_lpr parses as `EncB.parseDimacsBytes` (not verified),
  E4 Lean compiler/runtime of the printer, E5 kernel, Mathlib `f897ebcf` and the definitions, E6 SHA-256.

## 4. Method

LEAN_PATH (`tools/env.sh`, 17 read-only roots plus `out/`; `data/links.json` and `data/audit.json` list them):
1. FV304's 14 roots, verbatim (`/home/jay/research/data/fv304-20261120/lean_path.txt`, sha256 `65463fd5…` =
   fv304-audit's record): library, Mathlib and packages, toolchain, chain311, `leanz` (LemmaZ),
   `fv304-20261120/olean` (BalancedBudgetsZ, CompactChecker/* symlinks into `build/CompactChecker`, E304Z/*).
2. ENCBLEAN `.lake/build/lib/lean` (EncB.*).
3. `res118-rowblocks/build/olean` (RowEnc.*, RowGeo.*).
4. `combined/links`: 230 file-level symlinks (`tools/mklinks.py`). The other stores cannot be added whole: each
   duplicates modules of root 1 (`res118/olean`: CompactChecker/*, BalancedBudgetsZ; `res-slices-fv/olean`:
   CompactChecker/*; `comp-audit/out/olean`: LemmaZ, BalancedBudgetsZ; `fv304-audit/olean`: Res118/*). Linked:
   `Res118/{Rows,LemmaA,Glue,Final,Adapter}` (res118, the only store with `Adapter`, which `RS.Lib` imports);
   `RS/Lib`, `RS/{Cat,Bridge,Final}{3318,3418,3518,3419}` with the catalog parts and every chunk and Root olean of
   `RS3318/`, `RS3418/`, `RS3518/`, `RS3419/` (finished slices only; nothing of 3519/3520, `FinalTest*`, `Res118FV`);
   `FixedStatesZ`, `LemmaZStar`, `BalancedBudgetsZZs`, `BalancedBudgetsZZsN` (comp-audit).
5. `combined/out` (this build).

No n66 store is on the path. Units (`tools/start.sh` gates, `tools/unit_lean.sh` body) as in the memory rule below.

### Memory rule (pre-registered 22 Nov ~21:15, before the first unit at 21:19:14)

- Every compile in its own unit `esr-ag-lcb-<job>`: CPUQuota 100 %, MemorySwapMax 0, nice 10, one unit of this slot
  at a time. `tools/unit_lean.sh` (from fv304-audit's): `/usr/bin/time -v`, plus a sampler of the cgroup's
  anon+shmem (what `memguard.sh` counts) every 0.2 s that sends SIGTERM to lean at 80 % of MemoryMax.
- Light compiles (Residual, ES303, ES302, controls): MemoryMax 4G (stop at 3,277 MB), RuntimeMaxSec 1800.
- Heavy compile (ES304): MemoryMax 6G (stop at 4,915 MB), RuntimeMaxSec 3600.
- **Reading of "peak below 80 % of MemoryMax"** (as fv304-audit §4): the binding measure is the sampled anon+shmem.
  An `import E304Z.Final` maps about 25 GB of oleans, so `time -v` max RSS and the cgroup `memory.peak` (page cache;
  the guard turns MemoryMax into `memory.high`) exceed MemoryMax by design; `high` events are page cache and are
  reported, not a stop. Any `oom` or `oom_kill` event stops the work.
- Gates before every start: no YIELD file; Tctl < 86 °C; `cpu_free.sh esr` ≥ 1; no other `esr-ag-lcb-*` unit active;
  ag track anon + 1,500 MB ≤ 6,800 MB (85 % of 8,000). Poll 60 s, give up after 90 min (`logs/gates.log`).
- Audit units (hashing about 27 GB): MemoryMax 2G, RuntimeMaxSec 1800.

## 5. Results

| unit (KST) | job | result | wall | anon+shmem peak | cgroup peak | memory events | time -v max RSS |
|---|---|---|---|---|---|---|---|
| `links` 21:19:14 | `tools/mklinks.py` | rc 0: 230 links, 229 equal earlier pins, 1 first recorded (`RS/Lib`); no duplicate on the 18 roots; control refused | 2.5 s | not sampled | 1.2 GB | – | – |
| `res` 21:19:23 | `Combined.Residual` | lean_rc 0, guard passed | 11.3 s | 291 MB | 435 MB | none | 4.7 GB |
| `es303` 21:19:47 | `Combined.ES303` | lean_rc 0, guard passed | 11.7 s | 285 MB | 377 MB | none | 4.8 GB |
| `es302` 21:19:59 | `Combined.ES302` (first build, `n66Bound_mono` printed unguarded: standard axioms; its log was overwritten by `es302b`, figures from the unit output at the time) | lean_rc 0 | 11.2 s | 289 MB | 385 MB | none | 4.8 GB |
| `es304` 21:20:23 | `Combined.ES304` | lean_rc 0, guard passed | 9:25 (33 % CPU: page-cache bound) | **520 MB** | 6.44 GB (page cache) | high 125,913; max 0; oom 0; oom_kill 0 | 10.4 GB |
| `es302b` 21:30:10 | `Combined.ES302` with the `n66Bound_mono` guard | lean_rc 0, both guards passed | 12.4 s | 289 MB | 361 MB | none | 4.8 GB |
| `ctl` 21:30:23 | `controls/BadSwap.lean` | lean_rc 1, as expected (§6) | 2.4 s | 256 MB | 336 MB | none | 4.6 GB |
| `audit` 21:30:41 | `tools/audit.py` + `tools/readonly.sh` | passed; 2 CompactChecker modules unpinned in my sources | 48 s | not sampled | 2 GB | – | – |
| `audit2` 21:33:17 | the same with the 311 route record as a pin source | **passed**, 0 problems | 49 s | not sampled | 2 GB | – | – |
| `audit3` 21:39:21 | the same with the final `tools/audit.py` (env `MARKER` added for the switch; default unchanged) | **passed**, 0 problems; `audit.json`, `closure.tsv`, `readonly.txt` byte-identical to audit2's | 49 s | not sampled | 2 GB | – | – |
| `audit4` 21:51:31 | the same, start marker mtime moved from 21:10:00 to 21:05:00 (below) | **passed**, 0 problems; `closure.tsv` identical | 51 s | not sampled | 2 GB | – | – |

- The memory guard lifted every unit (`memguard.log`: `LIFT esr-ag-lcb-*`) and stopped none.
- **The four audit units reached a cgroup `memory.peak` of 2G = their MemoryMax (2048M).** Their anon was not
  sampled (the sampler is in `unit_lean.sh`, used for compiles only). The guard, which reads anon+shmem every 0.25 s
  and stops a unit at 95 % of its limit, did not stop them. The peak is presumably page cache from hashing about
  27 GB of oleans (the Python process holds only the 13,635-row table), but that is an inference, not a measurement.
- The ES304 cgroup peak (6,444,544,000 B) passed 6 GiB by 2 MB; it is page cache under the `memory.high` brake
  (`memory.max` lifted by the guard), anon was 520 MB.

**Import audit** (`data/audit.json`, `data/closure.tsv`): closure = union of the module lists the four modules
printed at compile time (Residual 5,320 ⊂ ES303 5,412, ES302 5,413, ES304 13,631; union **13,635**).

| pin class | modules | status |
|---|---|---|
| library.json (chain311 `library.json`, 4,952 pinned library/Mathlib oleans) | 4,952 | ok |
| chain311 `build.tsv` (last ok row) | 195 | ok |
| verified 311 assembly record `logs/es311/final311-compact.json` (CompactChecker/*, resolved into `build/CompactChecker`) | 10 | ok |
| fv304-audit `data/closure_combined.tsv` (LemmaZ, BalancedBudgetsZ, FcatZ, BridgeZ, 8,217 E304Z) | 8,221 | ok |
| `links.json` → res-slices-fv `data/audit-<TAG>.json` (3318: 5, 3418: 12, 3518: 48, 3419: 155) | 220 | ok |
| `links.json` → res118 `data/olean_sha256_after_resume.txt` | 5 | ok |
| `links.json` → comp-audit `closure.tsv` | 4 | ok |
| res118-rowblocks `data/manifest.sha256` (RowEnc/RowGeo) | 10 | ok |
| sevenfold review `oleans_before.sha256` (EncB) | 16 | ok |
| first recorded here: `RS.Lib` (`952b115c…`; its source sha256 `611be187…` is in res-slices-fv §7) | 1 | ok vs link time |
| this build: `Combined.Residual` | 1 | ok |

- Every module has exactly one providing root; every resolved file outside `out/` is older than the start marker
  `data/MARKER_START` (newest: 19:10:41 KST, `RS/Final3419`).
- **About the marker:** it was created at 21:21:51, after the first five units had started, with `touch -d` and a
  back-dated mtime: first 21:10:00 (audit, audit2, audit3), then 21:05:00 (audit4), which is before this agent's
  first write (the `mkdir` of the work directory at 21:05:26; nothing outside it was ever written). The results do
  not depend on the choice: the newest imported file is from 19:10:41.
- E304Z part: 8,217 modules, digest `fa02576ef5752c7fa509ea9f74b95feb46e4fdce9de26292b6df19c654b36c76` = fv304-audit's.
- Companions: 3,464 `.olean.server/.private` (toolchain), all equal to fv304-audit's table; digest `81fbc1d0…` =
  fv304-audit's figure in the same format.
- `data/readonly.txt` (audit4): 0 files newer than 21:05:00 in the 18 read-only stores listed there (repo `.lake` builds,
  chain311, `build/CompactChecker`, leanz, fv304 olean, ENCBLEAN, res118-rowblocks, res118, comp-audit, toolchain).
  `res-slices-fv/olean` is excluded (its driver writes 3519 files); the mtime check above covers the linked files.

## 6. Controls

- **Two-roots negative control** (`tools/mklinks.py`, `data/links.json`): appending `res118/olean` to the LEAN_PATH
  is refused; the duplicates are exactly BalancedBudgetsZ, CompactChecker/{Fast,Fast2,Packed,Path,Split,WordPack}
  and Res118/{Adapter,Final,Glue,LemmaA,Rows}.
- **Lean negative control** (`controls/BadSwap.lean`, `logs/ctl_BadSwap.log`): the proof term of
  `Combined.residual_bound_118` with `RS.s34_18` in the place of `s35_18`. Rejected: "Application type mismatch …
  `Res118.ResSliceExcludes (Res118.rowsP ++ Res118.rowsQ) 34 18` but is expected to have type … `35 18`"; lean_rc 1,
  no olean. So the slice theorems are bound to their exact (rows, B, T).
- **Guards**: every `#guard_msgs in #print axioms` fails the compile on any other axiom list; all passed.

## 7. Files and hashes (sha256)

| file | sha256 |
|---|---|
| `src/Combined/Residual.lean` | `422164559122b62e6dc25d61abe342aa254fef2d66f6d11a5057765964bee696` |
| `src/Combined/ES303.lean` | `07a1cc63012b01fc9c532068e4723f195cb223c1916dab9559599c2ede68908e` |
| `src/Combined/ES302.lean` | `5cfcb024a75751200e3c16509774706d7085290d3ba94f87b1a8b154c4829cad` |
| `src/Combined/ES304.lean` | `337e14dd9108653e5e906157e52ded6c3fa30c652ced4e7e224129f440f0a732` |
| `src/Combined/Switch3519.lean` (NOT compiled) | `02a692334a1180149801b85b1beb6c5663acd161a050195180968a55946ed761` |
| `controls/BadSwap.lean` | `78766bd89d4a2b5ddc4c15f90c73900532998d0faab6bd298137b7dc6aa43bf5` |
| `out/Combined/Residual.olean` | `cdadeb8cd48908519e9a82be6d8cd178fe2aefbfcfb8a5d0f6b35a0a8e08690d` |
| `out/Combined/ES303.olean` | `ebf1b4b3e656a8fe6fa2a323aea6fbe86265a912459919199bfefc2144ee36ae` |
| `out/Combined/ES302.olean` | `57476735e5b08c14200189ebe6d7ac8f3801c770813921f6509ac04e0875bd51` |
| `out/Combined/ES304.olean` | `fac38b7e2ce8c1fc54d308c76f19602ce44ecceceebeab33312451d547545715` |
| `logs/Residual.log` / `ES303.log` / `ES302.log` / `ES304.log` / `ctl_BadSwap.log` | `f4416933…` / `8f5dc8ff…` / `ccb74055…` / `2a71986d…` / `8dec8d8a…` |
| `data/closure.tsv` (module, root, file, sha256, pin, status) | `a93370e697eba04b05a2643bb33e54179703102dc4faac99c65406b2e831b016` |
| `data/audit.json` (audit4) | `68242ffc79bd0d8675c88fce5d1cff38dfafc24a602c6bce596c3932bf6e8279` |
| `data/links.json` | `255045a0964a3670eeb47e1f8dca1c0a9487431bbe275beeb6ac025ba6f8544a` |
| `data/readonly.txt` (audit4) | `6901248e0d01aee1cded86e3b18a801f51ee0abefcd5d906fa7dac524016d997` |
| `tools/audit.py` / `mklinks.py` / `env.sh` / `start.sh` / `unit_lean.sh` / `readonly.sh` | `e25e9252…` / `c7dfda9f…` / `95919dbf…` / `47f1bffb…` / `3f4cf21b…` / `d77b2c19…` |

The closure digest over all 13,635 sorted "module\tsha256" lines is
`20b59514c89db6dec8606d7241d3033b6b0bb4d3bba5d265a0e204f53766d675`.

## 8. What remains, findings

- **REMAINS.md**: per bound, the exact remaining hypotheses with their label and evidence.
- **s35_19**: Lean check running in res-slices-fv. When accepted, run the switch below; H-S3519 then disappears.
- **N66**: part 2. n66-rowsvalid's `RowEnc.*`/`RowGeo.*` have the same module names and namespaces as
  res118-rowblocks' (both use `namespace RowEnc`/`RowGeo`), so they can never share this LEAN_PATH. n66-l15-rows
  plans renamed modules (`N66R15*`); if it imports n66-rowsvalid's originals, part 2 needs renamed copies.
- Findings:
  1. The task text locates `composition_303_zzsf` in `Composition303.lean`; it is in `BalancedBudgetsZZs.lean`
     (`Composition303.lean` holds `composition_303 : BalancedBound 183 → ResidualBound 118 → …`).
  2. `Combined.n66Bound_mono` shows `Classical.choice` and `Quot.sound` too; presumably through `N66Bound`'s
     definition rather than the two-line proof (not tested).
  3. ES303 does not use the budget-67 tree (FV304); ES302 uses `N66Bound 54` in both halves.
  4. `RS.Lib`'s olean had no earlier hash; it is first recorded here.
  5. `time -v` max RSS (10.4 GB) and the cgroup peak (6.44 GB) of the ES304 compile exceed MemoryMax 6G as page
     cache and mapped oleans (memory rule above); anon+shmem was 520 MB. The audit units: §5.
  6. `audit-3419.json` (a pin source) lists 1 problem: C001706's axiom line split by profiler output, re-printed
     standard by res-slices-fv (§8 there). Only its hashes are used here.
- **Disclosure (task rule 4, read-only reads of files others were writing).** During orientation (about 21:12) a
  recursive `grep -rl/-rh --include=*.tsv --include=*.json --include=*.txt --include=*.sha256 "EncB/Render.olean"`
  over all of `/home/jay/research/data/formalize-20261122` read every such file there, including res-slices-fv's
  `run.tsv`, `status.json`, `tries.json` and the `export/3519` manifests that the running driver `esr-fvr-drv`
  writes, and other agents' live directories. I also read `n66-l15-rows/README.md` (another agent's live file) and
  listed `bal186-20261119/` (directory listing only; nothing under the running b69 finder was opened). All
  read-only; nothing was written, stopped or changed there. No unit other than `esr-ag-lcb-*` was touched.

## 9. Resume

```bash
W=/home/jay/research/data/formalize-20261122/combined; cd $W
tools/start.sh links 2048 900 1 /usr/bin/python3 -I -B tools/mklinks.py                  # links + two-roots check
for m in Residual ES303 ES302; do j=$(echo $m | tr A-Z a-z)
  tools/start.sh $j 4096 1800 1 /bin/bash tools/unit_lean.sh logs/$m.log out/Combined/$m.olean src src/Combined/$m.lean 3277; done
tools/start.sh es304 6144 3600 0 /bin/bash tools/unit_lean.sh logs/ES304.log out/Combined/ES304.olean src src/Combined/ES304.lean 4915
# (detached, about 10 min; wait until `systemctl --user is-active esr-ag-lcb-es304` is inactive)
tools/start.sh ctl 4096 1800 1 /bin/bash tools/unit_lean.sh logs/ctl_BadSwap.log - controls controls/BadSwap.lean 3277  # must fail
tools/start.sh audit 2048 1800 1 /bin/bash -c 'python3 -I -B tools/audit.py; rc=$?; tools/readonly.sh; exit $rc'
```

Units run with `--collect`, so the name of a finished unit can be reused; a name that is still active cannot.

### s35_19 switch (when res-slices-fv has accepted `RS.s35_19`)

1. Check its acceptance: `grep -h "'RS.s35_19' depends on axioms: \[propext, Classical.choice, Quot.sound\]"
   /home/jay/research/data/formalize-20261122/res-slices-fv/logs/RS_Final3519.log`, the log ends `lean_rc=0`, and
   `res-slices-fv/data/audit-3519.json` exists with `"problems": []`, except entries for axiom lines split by profiler
   output that `tools/axlines.py 3519` settles by re-printing (its §5.1 acceptance and §9 steps 2-3). Precedent:
   `audit-3419.json`, used here as a pin source for hashes only, keeps 1 such entry (C001706, re-printed standard,
   res-slices-fv §8).
   Only after its driver has finished 3519 (do not read files it is still writing).
2. `tools/start.sh links3519 2048 900 1 /usr/bin/python3 -I -B tools/mklinks.py 3318 3418 3518 3419 3519`
   (adds the 3519 links; pins from `audit-3519.json`).
3. `tools/start.sh sw3519 6144 3600 0 /bin/bash tools/unit_lean.sh logs/Switch3519.log out/Combined/Switch3519.olean src src/Combined/Switch3519.lean 4915`
   (heavy, about 10 min): theorems `Combined.residual_bound_118_s3519`, `es304_s3519`, `es303_s3519`,
   `es302_s3519`, each without `s35_19`, with `#guard_msgs`.
4. `touch data/MARKER_SWITCH` right after step 1 (before step 2), then
   `tools/start.sh audit3519 2048 1800 1 /bin/bash -c 'MARKER=data/MARKER_SWITCH python3 -I -B tools/audit.py logs/Residual.log logs/ES303.log logs/ES302.log logs/ES304.log logs/Switch3519.log; rc=$?; tools/readonly.sh; exit $rc'`
   (the 3519 oleans are newer than `data/MARKER_START`; the switch marker keeps the "nothing changed during the run"
   check meaningful).
5. Update REMAINS.md: drop H-S3519 from the four lists.
