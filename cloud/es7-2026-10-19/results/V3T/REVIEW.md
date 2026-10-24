# V3T review of `verify/v3/v3_manifest.py` and `verify/v3/v3_check.py` (base commit 8f98073)

The acceptance rule (`verify/v3/README.md`): a wave case is accepted only if (1) every leaf of the
union of all shards' strictly parsed `leaves.icnf` is re-solved from a CNF rebuilt here as
F + case cube + leaf, with the case part pinned by `cnf_sha256` in `results/Mii-S/cases.jsonl`, and
cake_lpr prints `s VERIFIED UNSAT`; and (2) the cover CNF {case cube units} + {¬leaf} is UNSAT with
a cake_lpr-verified proof.

Labels: **BUG** = can accept something that is not proved. **RISK** = liveness or a trap for the
operator; cannot by itself make an unproved leaf, cover or case look accepted. **NOTE** = checked and
fine, or informational. Line numbers refer to 8f98073.

## BUGs (both fixed, see `verify/v3/CHANGES.md`)

### BUG-1: fixed work paths are shared between concurrent v3_check.py processes
`v3_check.py:134,152` used `WORK/leaf-<idx>` and `WORK/cover-<case>`, and `solve_check`
(`:95-112`) writes `f.cnf`, runs CaDiCaL into `p.lrat`, runs cake_lpr on the two paths, then
`rmtree`s the directory. The paths are unique only inside one process. Two processes with the same
`--work` (the default `/opt/work/v3` is shared by everyone) and overlapping idx values collide:
sub-manifests are renumbered 0..n-1 (as this task prescribes), and two shards of manifests built at
different commits also overlap. Process B can overwrite `f.cnf`/`p.lrat` while A is between
CaDiCaL and cake_lpr, so cake_lpr verifies B's CNF and proof and A records `VERIFIED` for its own
leaf (whose `cnf_sha256` is computed from memory, not from the file that was checked). A's or B's
`rmtree` can also delete the other's files mid-run. The README's "Each job uses its own work
directory" holds only inside one process.
**Fix 1** (commit "uses a unique work directory per job"): each call makes its own directory with
`tempfile.mkdtemp(prefix="leaf-<idx>." / "cover-<case>.", dir=WORK)`.

### BUG-2: resume and output identify a leaf only by its manifest index
On start, every record in OUT with a final verdict adds `(kind, key)` to `done` (`:77-85`); `key`
is the manifest idx for a leaf and the case name for a cover; `leaf_job`/`cover_job` skip anything
in `done` (`:117`, `:141`). Leaf records carried no literals. So:
- rerunning into an existing OUT with a different manifest (rebuilt at a newer commit, where new
  leaves shift every idx, or a differently renumbered sub-manifest) skips leaf k of the new
  manifest because a different leaf had idx k before; that leaf is never solved, yet OUT contains a
  `VERIFIED` record with key k;
- a cover record of an older leaf set is kept for a case whose leaf set has changed (for example a
  leaf removed after a dir was rejected), so the cover verdict no longer belongs to the leaves that
  were checked;
- records from different machines can only be joined to leaves by idx, i.e. only if every machine
  used byte-identical manifests, which nothing checks.
**Fix 2**: leaf records carry `"lits"`, cover records carry `"leaves_sha256"` (sha256 of the JSON
list of the case's leaves in manifest order), and a record is reused on resume only if kind, key,
case and lits / leaves_sha256 all match. The aggregation in this task (`accepted.tsv`) also joins
leaf records to manifest leaves by (case, lits) and recomputes each leaf's `cnf_sha256`.

## RISKs (not fixed; no change made)

- **RISK-1 (v3_check, no validation of manifest records).** v3_check trusts the manifest: it does
  not re-check that `lits` are non-zero, distinct, non-contradictory ints. A hand-edited manifest
  with literal `0` writes the line `0 0` (an empty clause) into the leaf CNF. In the cases I tried
  the clause count then disagrees with the header and CaDiCaL refuses the file (REJECTED), but the
  safety comes from the header count, not from a check. Manifests built by v3_manifest.py cannot
  contain `0` (strict regex). Operator rule: only feed manifests produced by v3_manifest.py, or
  sub-manifests that copy its records unchanged (this task's sub-manifests do).
- **RISK-2 (liveness: cake_lpr has no timeout).** `subprocess.run([cake, ...])` (`:109`) has no
  timeout; a hung check blocks a worker forever. CaDiCaL has `--cap` and is killed on timeout.
- **RISK-3 (liveness: transient failures become permanent).** Any CaDiCaL exit code other than 10,
  20 or timeout (OOM kill -9, disk full, crash) and any cake_lpr failure (heap exhausted, crash) is
  recorded as `REJECTED`, and REJECTED records are in `done`, so a rerun never retries them. This is
  conservative (never accepts), but the records must be removed by hand before a rerun.
- **RISK-4 (liveness: exceptions and leftovers).** An exception in a job (e.g. ENOSPC while writing
  `f.cnf`) is re-raised at `f.result()` and ends the run after the pool drains; `solve_check` has no
  `finally`, so its work directory (CNF + partial proof) is left behind.
- **RISK-5 (memory/disk with 4 proofs at once).** Each job holds a ~10 MB CNF and a text LRAT proof
  (U_L11 leaves: ~30 MB, W19 reported 0.94 GB for 32 leaves). Four CaDiCaL processes on F use well
  under 1 GB each. Large proofs (minutes of solving) can reach several GB each in text LRAT, and
  cake_lpr needs memory proportional to the proof; with 15 GB RAM and ~29 GB free disk this is fine
  for the leaves seen so far, but a few 300 s leaves at once could exhaust either (→ RISK-3).
- **RISK-6 (manifest: directory depth).** v3_manifest.py only looks at `WAVE/<vm>/<dir>/leaves.icnf`.
  All 270 current leaves.icnf are at that depth; a VM that nests deeper is silently ignored. This
  can only make a cover fail, never pass.

- **RISK-7 (operator: OUT inside a git checkout).** OUT is held open in append mode for the whole
  run. If OUT is a tracked file of the checkout and `git pull --rebase --autostash` (or any checkout)
  rewrites it, the process keeps appending to the old, now deleted inode and the file in the tree
  stops growing. This happened in this task at 08:00Z: I recovered the records from
  `/proc/<pid>/fd/3`, stopped the run and resumed it with OUT outside the repository
  (`/opt/work/out/`), copying OUT into `results/V3T/` only at commit time. It loses records, it
  cannot add any; resume then re-checks the lost ones.

## NOTEs (checked, sound)

- **Case cube pinned.** v3_check rebuilds every case CNF as header `p cnf nv nc+|cube|`, F's body
  unchanged, cube units sorted by |lit|, and compares with `cnf_sha256` of the same row of
  cases.jsonl (zip order of cases.jsonl and the `a` lines of cases.icnf). Any change of F, of a cube,
  of the order of the two files, or of the construction stops the run (mutations M3, M5). The leaf
  CNF uses exactly these cube units, then the extra leaf literals; the header count is
  `nc + len(cube) + len(extra)`, which is the number of unit lines written. Leaf literals already in
  the cube are dropped (duplicates would be harmless).
- **Base F pinned** by its sha256 before anything else (M3). The header/body split assumes the header
  is the first line, which the sha pins.
- **Verdict source.** A leaf/cover is VERIFIED only if the first line of cake_lpr's stdout that
  starts with `s ` is exactly `s VERIFIED UNSAT`, and cake_lpr is only run when CaDiCaL exited 20.
  With no `s ` line the stored text is the output tail and cannot equal that line. cake_lpr checks
  the CNF file on disk; with Fix 1 that file is private to the job.
- **Shortcuts without a proof.** A leaf that contains the negation of a case-cube literal is
  recorded VERIFIED without solving (its CNF contains a unit and its negation: trivially UNSAT). A
  cover with the empty cube as a leaf is recorded VERIFIED without solving (the clause ¬(empty) is
  the empty clause). Both are propositionally sound; the second is only meaningful together with
  that empty leaf's own VERIFIED verdict, which the acceptance rule requires. A literal above F's
  variable count is REJECTED.
- **Cover CNF.** `{x} for x in cube` + `{¬l : l in leaf}` for every leaf of the case in the
  manifest; header `p cnf max(nv, max|lit|) #clauses` is exact. F is not included, which only makes
  the requirement stronger. The leaves used are exactly the manifest's leaves of that case, i.e. the
  ones whose leaf records the acceptance rule requires.
- **Sharding.** Leaves by idx mod N, covers by position of the case in the sorted case list mod N;
  every leaf and every case falls in exactly one shard. Acceptance must combine all N outputs.
- **Resume parse.** A truncated last line of OUT does not parse and is ignored (re-run). TIMEOUT is
  not final and is retried.
- **Concurrency inside one process.** Output lines are written under a lock and flushed. Several
  processes appending to one OUT is not protected (write one OUT per process).
- **Manifest strict parse.** Each non-blank, non-comment line must match
  `^a( -?[1-9][0-9]*)* 0\n$` (single spaces, no CR, no 0 inside, ends with ` 0` and newline); a file
  whose last byte is not a newline is rejected; a leaf with a repeated or contradictory literal is
  rejected. Any problem rejects the whole directory (M2). Literal range is checked later by v3_check.
- **Case assignment.** case_sha256 values in leaves.jsonl must be a single value present in
  cases.jsonl and must agree with the name rule when both exist. I checked the name rule against
  all 450 names: the only prefix pairs are `U2_L`/`U2_L3`-style (digit follows → excluded) and
  `U_L2`/`U_L2-3`-style (`-digit` follows → excluded), so `U_L4-s1` → U_L4, `U_L11_s0of4` → U_L11,
  `U_L2.s01` → U_L2, `U_L2-9` → U_L2-9. A directory rejected for any reason contributes no leaves;
  the case's cover then has to hold without it.
- **Merge across VMs.** Leaves are keyed by frozenset of literals per case, so equal leaves from
  different directories or with literals in a different order collapse to one record with all
  source paths (M6). idx is deterministic for a given checkout (cases sorted by name, leaves sorted
  by their sorted literal list).
- **No use of open.icnf or the VMs' own verdicts.** Nothing in either script trusts a VM's
  `status`, `covercheck.txt` or README; acceptance rests only on the two checks above.
- **leaf `cnf_sha256`** is computed from the bytes given to CaDiCaL/cake_lpr (with Fix 1, the file
  is private) and can be recomputed from the manifest by anyone; the aggregation here does so.
