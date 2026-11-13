Axiom re-check of LAYERLEAN/LayerLemma.lean for preprint P1 (WRITEUP/P1/p1.tex, Section 3, "Build and axioms").

When and where: 6 November 2026, 04:59 KST (start 2026-11-05T19:59:23Z, see out.txt), on the project's Linux
workstation (32 hardware threads, about 64 GB of memory), from the repository root, with the Lean/Mathlib
dependencies already built (Lean 4.24.0, Mathlib f897ebcf; no rebuild).

Files:
  LayerLemmaAxioms.lean  LAYERLEAN/LayerLemma.lean (SHA-256 afb8542d..., the file of commit 393619a57) unchanged,
                         followed by 19 '#print axioms' lines.  Its first 1,148 lines are byte-identical to
                         LayerLemma.lean (checked with diff when this archive was made).
  run.sh                 the script that ran the check.  It was run from a session scratch directory, so its
                         paths (SCR=/sandbox/...) point to a temporary session directory that is not
                         kept; they are left as run.
  out.txt                its output: 19 lines '... depends on axioms: [propext, Classical.choice, Quot.sound]',
                         then /usr/bin/time -v (wall clock 0:23.11, maximum RSS 2,587,624 kB, exit status 0).

Not covered by the 19 lines: hullVerts_subset (a one-line lemma used inside layers_are_orbits and exists_layer,
which are covered).

To rerun from a checkout (repository root, dependencies built):
  cp cloud/es7-2026-10-19/results/LAYERLEAN/logs/axioms_recheck_20261106/LayerLemmaAxioms.lean <dir>/
  /usr/bin/time -v lake env lean <dir>/LayerLemmaAxioms.lean
or append the '#print axioms' lines at the end of LayerLemmaAxioms.lean to a copy of LAYERLEAN/LayerLemma.lean.
