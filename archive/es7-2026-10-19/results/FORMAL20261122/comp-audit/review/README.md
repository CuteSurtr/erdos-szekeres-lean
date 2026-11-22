# comp-audit review (statement fidelity), 22 Nov 2026

Reviewer slot `lrev` (units `esr-ag-lrev-<job>`). Writes only under this directory.
Task: independent statement-fidelity review of the comp-audit worker result
(`/home/jay/research/data/formalize-20261122/comp-audit/AUDIT.md`), plus one axiom re-run on the worker's olean output.
Output: `VERIFY_comp-audit_fidelity.md` (here).

## Milestones
- 06:15 started; read SKILL.md, LEAN_STATUS.md, the worker's README and AUDIT.md.
- 06:20-06:35 read the ten sources (worker `src/`), the library definitions (Definitions, Realization, Partition,
  PopulationBounds, Subsets, CycleGeometry, ProjectiveTransfer), the chain311 row sources (BalancedProof/Catalog,
  BalancedCoverCutsV2), the records ES304/ES305/ES303/ES306/ES307/N66N and the bridge model, check_tree
  (`scripts/omission_tree.py` 35cb3050...) and the balcheck2 header. Worker files re-hashed: all equal AUDIT.md section 10.
  ES303 README is being edited live; sha256 at 06:31:40 was a5ed27da...fc9f.

## Pre-registered rules (written 06:40, before the compile)

Verdict rule per theorem (keys = the 31 names of the worker's theorems.json):
- **confirmed** iff all four hold:
  1. the statement in the loaded environment (`#check @`, `#print` of every definition it unfolds to) says what the
     written result says, with no extra binder and no weakening;
  2. every hypothesis equals, or follows by a Lean-checked one-line implication (Review.lean section D), the statement
     that existing evidence or a concrete planned pipeline of a record certifies; for tree hypotheses the row sets are
     bound by MY dump of the rows from the oleans compared with MY parser to the checkers' row inputs, and their
     hashes are recorded; N66Bound and ResidualBound are checked for form against the record's stated class only (their
     proofs are not re-derived here);
  3. non-vacuity is shown (exact computation on the dumped rows plus reasoning);
  4. my re-run prints exactly `[propext, Classical.choice, Quot.sound]`.
- **not_confirmed** if any of 1-4 is not established, including a hypothesis with no existing or planned evidence.
- **refuted** only for a statement or hypothesis form that contradicts the written result or the evidence, or a
  non-standard axiom.

Memory reading (single compile, so no later compile depends on it): judged by the unit's cgroup `memory.peak` (must stay
below 2,800 MiB = 80 % of MemoryMax=3500M) and `memory.events` (no high/max/oom/oom_kill). `time -v` max RSS is reported
as well; it is expected near 3.1 GiB because it counts the shared, file-backed olean mappings (the worker saw
3,094-3,776 MiB with cgroup peaks of 313-1,053 MiB). An RSS above 2,800 MiB is FLAGGED, not a stop. The closure oleans
are re-hashed from the shell just before the start (independent closure check; it also keeps their pages in cache).
- 06:39:55 the one unit esr-ag-lrev-axioms started (gate: no YIELD, Tctl 78.4 C; closure pre-check 4,980 modules, 0 bad).
  By 06:40 the log held sections A-E (46 axiom lines, no error) and the ROW dump up to row 2,623 (stdout is
  block-buffered). The CUT dump then made no progress for 14 min: `BalancedCoverCutsV2.support` is a 446-entry `![...]`
  vector, and evaluating it through the generic compiled `Fin.cons`/`Fin.induction` looks exponential in the index
  (my diagnosis, not measured further). 06:54:40 snapshot: cgroup memory.peak 318 MiB, anon 240 MiB, no memory event,
  swap 0 (pre_stop_snapshot.txt). 06:55 I sent SIGTERM to the lean process (my own unit) to end the compile; the
  buffered rows 2,624-2,684 and the CUT/Z/CAT dumps are lost, so those bindings fall back to a source-level check
  bound to the oleans by the chain311 build record (weaker; labelled so in the VERIFY file). No second compile.
- 06:54:49 unit ended (lean_rc 143 after my SIGTERM; time -v max RSS 3,189 MiB = FLAGGED; cgroup memory.peak 318 MiB,
  anon peak 241 MiB, memory.events all 0, swap 0; user 875.5 s). Worker oleans unchanged (before = after). Closure
  post-check: my compile's module list = closure.tsv, 4,980 modules, same order. 46/46 axiom lines are exactly
  [propext, Classical.choice, Quot.sound]; no error or warning message (no "Review.lean:" line).
- 06:56 rows_compare.py: olean dump rows 0-2,623 = source rows; all 3,131 Lean rows = balanced-v2-source.json in order;
  catalog = JSON states; Z/Z* = zrow.json/zstar.json/zzs_rows*.json; balz*.rows consistent; all file hashes = records;
  non-vacuity vectors satisfy every row. 06:57: b68zs/steps.log shows balcheck2 EXACT TREE at 06:21:29 and ES303
  README (a5ed27da...) now states "ES(8) <= 303 ESTABLISHED"; noted, not re-checked.
- 07:00 writing VERIFY_comp-audit_fidelity.md.
- 07:03-07:05 tree-evidence pins verified (b67 against ES304 §4, b68zs against ES303 §6 with README a5ed27da... and
  steps.log 1c5d73cb..., b66 masters against ES305 §7; the b66 check outputs are not pinned there). VERIFY updated.
- DONE 07:08. No esr-ag-lrev-* unit remains. Result: VERIFY_comp-audit_fidelity.md (26 confirmed, 5 not_confirmed,
  0 refuted; Composition306 docstring refuted; memory reading flagged).
