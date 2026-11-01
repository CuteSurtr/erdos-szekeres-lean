# WRITEUP task: a self-contained account of the mirror-class result

Your prompt gives two values: H (your time budget in hours) and Z (the commit of this file). Replace {H} and {Z} below by those values; follow everything else exactly.

General rules:
- Start: `git fetch origin es7-cloud && git checkout es7-cloud`. Before your first commit run `git config user.name CuteSurtr && git config user.email 133225877+CuteSurtr@users.noreply.github.com` and check that `git var GIT_AUTHOR_IDENT` and `git var GIT_COMMITTER_IDENT` start with `CuteSurtr <133225877+CuteSurtr@users.noreply.github.com>`. Commit only to branch es7-cloud and only inside `cloud/es7-2026-10-19/results/WRITEUP/`, with plain commit messages and no AI co-author or attribution trailers; `git pull --rebase --autostash` before every push, retry until it succeeds (after 10 failures push to branch `es7-fallback-writeup`).
- Time budget {H} hours; commit at least every 30 minutes; do not end your turn while work is running (ScheduleWakeup does not fire here).
- Commit hashes cited in files written before 2026-10-21 are pre-rewrite hashes; translate them with `results/FINAL/COMMIT_MAP.tsv` when you cite them, and cite the new ones.

Write `results/WRITEUP/MIRROR.md`, a self-contained account (as for a mathematician who has not seen this repository) of the result:

> Every set of 33 points in the plane in general position that is invariant under a reflection contains 7 points in convex position. Equivalently, a counterexample to the Erdős–Szekeres conjecture ES(7) = 33 cannot be mirror-symmetric.

Sources (paths under `cloud/es7-2026-10-19/`): `results/V3Z/summary.md` and README, `results/V2-L/README.md` (§3–§9), `results/V1-L/` (SUMMARY and README), `results/H3/` (encoding), `results/Mii-S/` (`soundness.md`, the 450-case split), `results/Haudit/AUDIT.md`, `results/FINAL/README.md`, `verify/v3/README.md`, the symmetry reduction in the C3-S/C/E results (only reflections and 3-fold rotations are possible symmetries of a 33-point counterexample; the D3 class is excluded in `results/E`/`E2`), and the related-work notes in `docs/RELATED_WORK_2026-10-14.md` of the main repository.

Required sections:
1. Statement, and what is and is not claimed (the 3-fold rotation class is open; no counterexample is known; say "we did not find prior work", never claim priority).
2. Why only reflections and 3-fold rotations can be symmetries of a 33-point counterexample (a short proof).
3. The encoding (signotope/order-type variables, the mirror normalization, the axis point; sub-cases (i) hull vertex and (ii) interior) and its Lean soundness proof.
4. The case split of sub-case (ii) (hull pairs, 450 cases, 122 obligations) and why it is complete.
5. The solving (cube-and-conquer waves, leaves, splits) and the from-scratch acceptance (V3: every leaf re-solved from a CNF built from F, proof checked by cake_lpr; every case cover checked), with the final numbers.
6. The Lean theorems (`V1L.hullVertexLine_of_leaves`, `V2L.mirrorExclusionLine_final`, the tree certificates), their axioms, and the exact trust base (cake_lpr verdicts read as unsatisfiability of byte-identified files; DIMACS emission; the drivers' leaf recording).
7. Reproduction: commits (new hashes), tools and commands, compute used.
8. Table of all numbers with the file each comes from.

Check every number against its source file and give the path next to it. Keep it to the facts recorded in the repository; where two files disagree, say so. Also write `results/WRITEUP/NUMBERS.tsv` (number, value, source file) and a short `README.md`.
