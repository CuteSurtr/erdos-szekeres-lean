# V2G task: tree-shaped kernel cover proof and the final instantiation of V2-L

Your prompt gives two values: H (your time budget in hours) and Z (the commit of this file). Below, replace {H} and {Z} by those values. Everything else in this file is to be followed exactly.

General rules:
- Start: `git fetch origin es7-cloud && git checkout es7-cloud`. Before your first commit, set the commit identity of the repository owner: `git config user.name CuteSurtr && git config user.email 133225877+CuteSurtr@users.noreply.github.com`, and check that `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` both start with `CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>` (if not, unset GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_COMMITTER_NAME and GIT_COMMITTER_EMAIL for your git commands). Every commit you make must have that author and committer. Record the environment (`uname -a; nproc; free -g || true; df -h /opt || true; date -u`) into `cloud/es7-2026-10-19/results/V2-L/logs/tree_env.txt`, then commit and push it at once.
- Time budget: {H} hours of wall time. Commit and push progress at least every 30 minutes. Use the last 15 minutes to update `results/V2-L/README.md`, push, and report.
- Do not end your turn while work is running. ScheduleWakeup does not fire in this environment, and a session that ends its turn may not be woken by background notifications. Keep the session active: wait in the foreground with bounded until-loops (at most 10 minutes per tool call) that return on progress, commit, then wait again.
- Commit only to branch es7-cloud, and only inside `cloud/es7-2026-10-19/results/V2-L/`. Use plain commit messages with no AI co-author or attribution trailers. Run `git pull --rebase --autostash` before every push, and retry the push until it succeeds (many machines push to this branch). If a push still fails after 10 tries, push to branch `es7-fallback-v2g` and say so.
- Never commit files over 50 MB. Use all 4 cores. Memory is 15 GB with no swap: run at most two Lean processes at a time, and watch peak RSS.
- Never write `sorry` or `admit` in any Lean file, not even temporarily. Do not add `axiom` declarations, `native_decide`, `implemented_by` or `extern`. Do not change or remove existing theorems or definitions of H, H3, V1-L or V2-L; only add new files and new declarations (and the new imports they need).

## Background

Paths are under `cloud/es7-2026-10-19/`. Read `results/V2-L/README.md` first, then `results/V2-L/FINAL_TASK.md` and `results/V2-L/logs/final_kernel_cover_trial.log`.

V2-L proves the mirror statement from solver certificates. `V2L.CaseCertificates leaves` asks, for each of the 450 cases, `Mir.coverCheck (leaves p.1) = true` and a per-leaf UNSAT fact. A previous run (V2F) found that `decide +kernel` on `coverCheck` of one flat leaf list does not fit in 15 GB beyond about 2,600 leaves (U_L8 was killed at 13.5 GB). The final data has about 75,000 leaves, and U_L2 alone has over 22,000. A split of the flat check by `restrictPath` failed in the same way.

The leaves are not an arbitrary list, though: they come from a tree. For each wave case, `march_cu CASE -d 7` gave the top cubes. Each cube was either closed (CaDiCaL UNSAT, cake_lpr `s VERIFIED UNSAT`: an `"UNSAT"` record whose `cake_lpr` field is that exact line) or split by `march_cu` (split depth 6) into children `cube + sub` (a `"SPLIT"` record with `"subs"`), recursively. At commit 9639cfb45 the union over all wave directories has 897 split nodes and no node with two different SPLIT records. The top-cube set of every case, and the `subs` list of every split node, is a combinatorial cover by itself (`coverCheck` true in a Python transcription). Each of these lists has at most 128 cubes of at most 7 literals. So a cover proof that follows the tree needs only small kernel checks.

## Design (follow it unless it fails; if you must deviate, explain why in the README)

1. `V2L/Tree.lean` (new): a tree certificate and its soundness.
   - A tree type, for example
     ```lean
     inductive CTree where
       | leaf : CTree
       | node : List (List Int × CTree) → CTree
     ```
     with `CTree.leaves : CTree → List (List Int)` (`leaf ↦ [[]]`; `node kids ↦` for each `(s, t)` in `kids`, in order, the list `t.leaves.map (s ++ ·)`, concatenated) and `CTree.check : CTree → Bool` (`leaf ↦ true`; `node kids ↦ Mir.coverCheck (kids.map Prod.fst) && every child tree checks`).
   - Both must reduce in the kernel: structural recursion only (no well-founded recursion, no `partial`). If structural recursion over the nested inductive is not accepted, use a fuel argument (recursion on a `Nat` depth bound), as `Mir.coverAux` does.
   - Soundness: `theorem CTree.covers_of_check {t : CTree} (h : t.check = true) : Mir.Covers t.leaves`, from `Mir.covers_of_coverCheck` and the composition fact: if `CubeSat ν s` and `CubeSat ν l` then `CubeSat ν (s ++ l)`.
2. `V2L/TreeMain.lean` (new): the main statements with tree certificates, reusing the existing proofs.
   ```lean
   def CaseCertificatesT (tree : List Nat × List Nat → CTree) : Prop :=
     ∀ p ∈ caseTable, (tree p.1).check = true ∧
       ∀ l ∈ (tree p.1).leaves, ¬DimacsSatisfiable (cubeCnf (cubeCnf (interiorCnf 33 7) p.2) l)
   def InteriorCertificatesT (tree) : Prop := RootCertificate ∧ UpCertificates ∧ CaseCertificatesT tree
   theorem interiorCnf_unsat_of_certificatesT : InteriorCertificatesT tree → ¬DimacsSatisfiable (interiorCnf 33 7)
   theorem axisInteriorLine_of_certificatesT   -- same conclusion as axisInteriorLine_of_certificates
   theorem mirrorExclusionLine_of_certificatesT -- same hypotheses h1 for sub-case (i), conclusion MirrorExclusionLine
   ```
   The only change from the existing proofs is the cover step: `CTree.covers_of_check` replaces `Mir.covers_of_coverCheck`, followed by `Mir.not_dimacsSatisfiable_of_cover` as before (or prove `InteriorCertificates`-style facts from the tree and reuse the existing theorems directly, if that is simpler).
3. The data, from the final commit. Wait for `results/FINAL/READY.json` on origin/es7-cloud (check every 5 minutes after `git fetch`; do steps 1, 2 and 5a meanwhile, testing on the current branch head). It names a commit Zf at which no wave case has an open cube, and the sha256 and line count of the acceptance manifest there. `git worktree add /opt/fin Zf`, R=/opt/fin/cloud/es7-2026-10-19/results.
   - Write `scripts/gen_trees.py R OUTDIR`. For each of the 450 cases (`R/Mii-S/cases.jsonl`, in `caseSpecs` order): a case that `Mii-S` closed directly, or for which some wave directory closed the empty cube, gets `leaf`. Otherwise read every `<vm>/<dir>` under `WAVE1` to `WAVE4` that belongs to the case (the `case_sha256` of its `leaves.jsonl` first record, as `assemble_leaves.py` does; skip `tasks` and anything else): the top cubes (`top.icnf` lines `a ... 0`), the SPLIT records (`cube`, `subs`) and the closed cubes (`"status": "UNSAT"` with `cake_lpr` exactly `s VERIFIED UNSAT`, by their exact literal sequence). The root children are the top cubes that are not `parent + sub` of a SPLIT record. A node whose literal sequence was closed is a `leaf`; otherwise it must have a SPLIT record, and its children are `(sub, subtree of parent + sub)` in the recorded order. Stop and report if any node is neither (an open cube), if two SPLIT records of one cube differ, or if any check below fails.
   - Keep every literal sequence exactly as recorded (the per-leaf files the solvers checked are "case file + leaf units" in recorded order, and the leaf of a split child is recorded as `parent + sub`), so that `(tree p.1).leaves` reproduces the recorded leaf cubes exactly.
   - Write the trees as Lean data in `V2L/Trees/` (one module per case or per chunk; split large cases into one definition per root child so that no single term is huge; the packed literal encoding of `V2L/Data.lean` may be reused) and a table `V2L.treeOf : List Nat × List Nat → CTree`. Also write `OUTDIR/status.json` with, per case, the number of leaves, split nodes and depth.
4. Cross-check with the acceptance manifest, as `FINAL_TASK.md` step 4 describes (verify/v3 at bdf319c, `v3_jsonl_leaves.py` for WAVE1..WAVE4, `v3_manifest.py`; sha256 and line count must equal READY.json). Check, case by case, that every leaf of the tree (as a literal sequence, compared with the manifest's `lits`) is a manifest leaf of that case; the cases with tree `leaf` contribute the single empty leaf and are checked against Mii-S (direct) or the wave record of the empty cube. Record in `logs/tree_crosscheck.log` the per-case counts on both sides, the number of manifest leaves not in the trees (allowed; report it) and the number of tree leaves not in the manifest (must be 0; otherwise stop and report them).
5. Kernel checks.
   a. While waiting for READY.json, measure: build the trees at the current head for a few large closed cases (U_L8, U4_L, U_L7) and prove `(treeOf s).check = true` by `decide +kernel`; record wall time and peak RSS in `logs/tree_kernel_trial.log`.
   b. On the final data: one theorem per case, `theorem check_k : (treeOf s_k).check = true := by decide +kernel`, in separate modules built by lake (at most two in parallel if memory requires). Then combine them, without re-evaluating, into `theorem treeOf_check : ∀ p ∈ caseTable, (treeOf p.1).check = true` (for example via a table of (spec, tree) pairs and a conjunction of the per-case theorems). Record per-case and total kernel time and peak RSS in `logs/tree_kernel.log`.
   c. `V2L/FinalTree.lean`: state and prove the instantiated theorem, with the leaf UNSAT facts as hypotheses:
      ```lean
      theorem V2L.mirrorExclusionLine_final
          (h1 : ∀ c ∈ V1L.hullLeaves, ¬DimacsSatisfiable (cubeCnf (hullCnf 33 7) c))
          (hroot : RootCertificate) (hup : UpCertificates)
          (hleaves : ∀ p ∈ caseTable, ∀ l ∈ (treeOf p.1).leaves,
            ¬DimacsSatisfiable (cubeCnf (cubeCnf (interiorCnf 33 7) p.2) l)) :
          MirrorExclusionLine
      ```
      Add `import V2L.FinalTree` (and the other new modules) to `V2L.lean` and run `lake build`. The previous run (V2F) may have added `V2L/Final.lean` (the flat `decide +kernel` cover check) and its import; if that module cannot be built in 15 GB, remove only its import line from `V2L.lean`, leave the file, and say so.
6. Audit: add to `V2L/Audit.lean` `#guard_msgs` checks of `#print axioms` for `V2L.CTree.covers_of_check`, `V2L.treeOf_check`, `V2L.mirrorExclusionLine_certificatesT` (whatever the final names are) and `V2L.mirrorExclusionLine_final`, with the messages Lean actually prints; the main theorems must use only `propext`, `Classical.choice` and `Quot.sound`. Rebuild, rerun the forbidden-word grep of `logs/grep_forbidden.log` over all Lean files of V2-L, and save the outputs in `logs/tree_print_axioms.log` and `logs/tree_grep_forbidden.log`.
7. Commit the new Lean files (data modules too if each is under 50 MB; otherwise commit their sha256 and how to regenerate them), `scripts/gen_trees.py`, the status file and the logs. Add a README section "Tree certificates" with: Zf, the number of trees, leaves and split nodes, the cross-check, the kernel times and peak memory, the axioms, and the exact statement of `mirrorExclusionLine_final`. Say plainly which hypotheses remain (the cake_lpr verdicts of the root, the 121 up obligations, sub-case (i)'s leaves and every tree leaf) and where those verdicts are recorded.

README update and final message: Zf, the number of leaves in the Lean data, the cross-check result, the kernel time and peak memory of the tree checks, the axioms of the main theorems, and anything that failed.
