# fv302 (mirror): the Lean check of the ES(8) <= 302 budget-69 tree (FV302)

Mirror of the small files of the work dir `~/research/data/fv302-20261124` (25 Nov 2026 16:40 KST). **Status: the
campaign is running and NOT accepted**; acceptance is pre-registered in `PLAN.md` ("Pre-registration", items 1-4).
- `src/CompactChecker/FcatZZs16.lean`, `BridgeZZs16.lean`: the new Lean modules (catalog with the Z-row and Z*-row at
  16; the bridge `zzsn16_of_root` from the Root statement to `ExcludesHoleBudgetZZsN 16 69`).
- `tools/`: exporter (export302.py, sha256 6ae42d7a... = pins-launch.sha256), joins (root302.py), driver (drive302.py),
  compile wrapper (lean302.sh), axiom audit (axiom_audit.py), watcher, context and catalog generators.
- `data/contexts302.jsonl` (sha256 5ac946fe..., 32,618 contexts) and `data/fcatzzs16-source.json` (6d83b0f1...): the
  inputs. The certificate itself (bal186-20261119/zrow/b69zs54/files, 32,618 files) stays in the data dir.
- Not mirrored: the generated chunk sources export/src/E302ZZ/C*.lean (84 GB; regenerable byte for byte by
  export302.py, test of 25 Nov: 83 contexts / 137 modules identical, cleanup-20261125/fv302-regen), the join sources
  (mirrored once Root and Final exist), oleans and logs.
