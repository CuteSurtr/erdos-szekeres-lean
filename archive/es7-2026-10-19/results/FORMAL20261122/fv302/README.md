# fv302 (mirror): the Lean check of the ES(8) <= 302 budget-69 tree (FV302)

Mirror of the small files of the work dir `~/research/data/fv302-20261124` (25 Nov 2026; updated 20:45 KST).
**Status: ACCEPTED 25 Nov 20:13** (result.json written 20:13:32; corrected 21:10 from "~20:40") by the pre-registered items 1-4 of `PLAN.md` (log at the end of PLAN.md;
`acceptance/`: fv2a.py, result.json, step files, closure302.tsv, Audit302.lean and its log). **The budget-69 tree
`OmissionBalancedZZsN.ExcludesHoleBudgetZZsN 16 69` is Lean-checked** (`E302ZZ.Final.excludes_69`, standard axioms),
and `E302ZZ.Final.forces_302_of_n54_res : N66Bound 54 → ResidualBound 118 → ForcesConvexNGon 302 8`.
- `joins/`: the generated join sources (S_*, P_*, Root, Final, FinalTest); `logs/`: Root.log, Final.log, run.tsv,
  driver.log; `regen-test/`: the regeneration test of the chunk sources (83 contexts, 137 modules byte-identical);
  `receipts/fv302_chunk_sources_20261125.tsv`: path, size and sha256 (= manifest) of the 32,953 chunk sources
  (78.06 GiB; columns named as `verify-20261124/delete_proofs.py` reads them), before their guarded deletion.
- `src/CompactChecker/FcatZZs16.lean`, `BridgeZZs16.lean`: the new Lean modules (catalog with the Z-row and Z*-row at
  16; the bridge `zzsn16_of_root` from the Root statement to `ExcludesHoleBudgetZZsN 16 69`).
- `tools/`: exporter (export302.py, sha256 6ae42d7a... = pins-launch.sha256), joins (root302.py), driver (drive302.py),
  compile wrapper (lean302.sh), axiom audit (axiom_audit.py), watcher, context and catalog generators.
- `data/contexts302.jsonl` (sha256 5ac946fe..., 32,618 contexts) and `data/fcatzzs16-source.json` (6d83b0f1...): the
  inputs. The certificate itself (bal186-20261119/zrow/b69zs54/files, 32,618 files) stays in the data dir.
- Not mirrored: the generated chunk sources export/src/E302ZZ/C*.lean (84 GB = 78.06 GiB; regenerable byte for byte
  by export302.py, test of 25 Nov in `regen-test/`: 83 contexts / 137 modules identical), the oleans and the module
  logs. The join sources (S_*, P_*, Root, Final, FinalTest) are mirrored in `joins/`.
- **Deleted 25 Nov 2026, done 20:29:26** (manifest time; corrected 21:10 from "~21:40") (owner rule of 25 Nov "delete what has already been formalized"; advisor-checked;
  receipts pushed in c8e052d39): the 32,953 generated chunk sources `export/src/E302ZZ/C*.lean` (83.82 GB) by
  `verify-20261124/delete_proofs.py` (dry run and execute: every file re-hashed = receipt, 0 problems, 0 bindings;
  manifest `verify-20261124/manifest_deletions.txt`). Kept: the 38 join sources, all 32,618 `export/ctx` manifests,
  the oleans, the logs, the certificate files and the exporter. Free disk 1,031.4 -> 1,115.3 GB.
- Regeneration dependency: the byte-identical regeneration was shown with Python 3.13.18 (the venv
  `~/research/data/six10-linux-20261105/venv.disk`, python -I) running tools/export302.py (sha256 6ae42d7a…) on
  data/contexts302.jsonl and the certificate files `bal186-20261119/zrow/b69zs54/files` (kept); another interpreter
  version is untested.
