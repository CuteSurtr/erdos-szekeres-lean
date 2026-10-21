# C3AUDIT task: adversarial review of the 3-fold class setup, before more compute goes into it

Your prompt gives two values: H (your time budget in hours) and Z (the commit of this file). Replace {H} and {Z} below by those values; follow everything else exactly.

General rules:
- Start: `git fetch origin es7-cloud && git checkout es7-cloud`. Before your first commit run `git config user.name CuteSurtr && git config user.email 133225877+CuteSurtr@users.noreply.github.com` and check that `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` both start with `CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>` (if not, unset GIT_AUTHOR_NAME, GIT_AUTHOR_EMAIL, GIT_COMMITTER_NAME and GIT_COMMITTER_EMAIL for your git commands). Record the environment (`uname -a; nproc; free -g || true; date -u`) into `cloud/es7-2026-10-19/results/C3AUDIT/env.txt`, then commit and push it at once.
- Time budget: {H} hours of wall time. Commit and push your notes at least every 30 minutes. Use the last 10 minutes to finish `results/C3AUDIT/REPORT.md`, push, and report. Do not end your turn while work is running: ScheduleWakeup does not fire here, so wait in the foreground with bounded until-loops (at most 10 minutes per tool call).
- Commit only to branch es7-cloud and only inside `cloud/es7-2026-10-19/results/C3AUDIT/`, with plain commit messages and no AI co-author or attribution trailers. Run `git pull --rebase --autostash` before every push and retry until it succeeds (about 50 machines push to this branch); after 10 failures push to branch `es7-fallback-c3audit` and say so. Never commit files over 50 MB, CNF or proof files. Never write `sorry` or `admit` in any Lean file. Do not modify anything outside your directory: if you find a bug, describe it with evidence; do not fix it in place.
- Commit hashes cited in files written before 2026-10-21 are pre-rewrite hashes; translate them with `results/FINAL/COMMIT_MAP.tsv` (old full hash → new full hash; abbreviated hashes are prefixes of the old full hash).

## The setup under review

Paths are under `cloud/es7-2026-10-19/`.
- **Symmetry reduction:** a 33-point counterexample to ES(7) = 33 (33 points in general position, no 7 in convex position) with a nontrivial symmetry has a reflection or a rotation by 120°; the class with both (D3) is excluded in `results/E` and `results/E2`. Find where each step is argued (`results/C3-S`, `results/C`, `results/C2`, `results/E`, `results/E2` and their READMEs).
- **Base encoding of the 3-fold class:** `results/C3a` (`c3cnf.py`, `validate.py`, `check_identities.py`, `controls`), `results/C3b` (`DERIVATION.md`), and `results/C3-S/tools/gen_case.py`. The base CNF `gen_case.py 11 7 none` has header `p cnf 168399 4154921` and sha256 `bf0e502ee78599400d36e0fc402a8ce79b4c41443327b4e0186902fab0cdd6da`, said to be byte-identical to C3a's chain CNF.
- **Decomposition:** `results/C3-S/soundness.md` (Lemmas 1 to 5 and the cover theorem), `results/C3-S/tools/hullcase.py`, the root manifest `manifest_depth2.tsv` (11 top cases, 1,630 depth-2 roots), and the validation tools and logs listed in `results/C3-S/README.md`.
- **Drivers and records:** `results/C3-S/tools/close_node.py`, `close_tree.py` and `compose.py`; the records `results/C3WAVE1/C*/out.jsonl` (and `results/C3WAVE2/K*/out.jsonl` as they arrive).

## What to look for

Find any reason why refuting every node of a cut of the layer tree, as `compose.py` checks it, would not imply that the 3-fold class is empty. Default to suspicion.
1. **Symmetry reduction.** Re-derive which rotation orders and which reflections are possible for 33 points with no 7 in convex position, and check the argument that leaves only a reflection and a 120° rotation. Is the point-reflection (order 2) case covered, and by what?
2. **Encoding.** Does every 3-fold-symmetric 33-point set with no convex 7-gon give a satisfying assignment of the base CNF? Check the variables, the orbit identification `R(i) = (i − m) mod n`, the σ conventions, the `sb` clause and the 7-gon clauses. Rebuild the base CNF yourself and compare the header and sha256.
3. **Decomposition.** Check Lemmas 1 to 5 line by line against `hullcase.py`: the hull orders, the layer options and `tree_children`, the a ≤ 5 renormalization for m = 11, the mirror map and `h3_layer2_kept`. Is there a configuration that no node covers (for example a layer that is not one or two orbits, or a last layer with fewer points)? If time allows, write an independent check: generate random exact-coordinate 3-fold-symmetric sets with your own code (not the repository's generator), canonicalize them with your own code, and evaluate the clauses of their node.
4. **Drivers.** Can `close_node.py` or `close_tree.py` record a node as certified unless both checkers accepted a proof of exactly that node's CNF? Does `compose.py` check the cut correctly (children lists complete, nothing counted twice, CNF sha256 recomputed)? Re-check at least 10 certified wave-1 nodes yourself: build the node CNF, solve it with CaDiCaL 3.0.1 (c6073042) producing LRAT, check it with cake_lpr (a36874a8), and compare the CNF sha256 with the record.

For each finding give the file and line, the evidence, and how serious it is (breaks soundness / weakens the trust base / cosmetic). Say plainly what you checked and found sound, and what you could not check.

`results/C3AUDIT/REPORT.md` and final message: the findings, most serious first, each with evidence; what you checked and found sound; what you could not check.
