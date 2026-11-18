# PROVED: the cup/complement lemma is false for every n>=6

1. **Status.** Written explicit counterexample family, finalized 14 November
   2026. The proposed sufficient selection condition fails for every n>=6.
   Every member nevertheless has a two-point terminal-safe weak Delta.
   This is neither a weak-Delta refutation nor a numerical ES bound.
2. **Statement.** For each n>=6 there are 2n-3 real points, in general
   position with distinct x-coordinates, with no five-cap, no convex
   n-gon, maximum cup length n-2, and a convex complement to every maximum
   cup. See [theory.md](theory.md), Sections 1–5, for integer coordinates
   and the full proof.
3. **Model and soundness.** Three cup blocks have sizes n-3,3,n-3. Ten
   explicit triple-sign patterns prove all premises and classify every
   maximum cup and every target polygon. Exact inequalities establish
   those signs for the displayed integer formula. No solver is used in
   the proof. The parent reviewed the slope/table/classification argument;
   no Lean proof or external peer review is claimed.
4. **Method.** The parent's n6/n8 fixtures suggested the three-block
   pattern. A simpler uniform construction gives exactly six maximum
   cups, with one-point exchange graph two disjoint triangles. Every
   complementary polygon has upper/lower chain sizes (3,n-2). Thus even
   that restricted chain type cannot rescue the proposed lemma.
5. **Other written results.** Section 6 records the parent's stronger
   full-S cup localization. Section 7 gives the exact pair obstruction
   to augmenting a cup by q and the root, without asserting q exists.
   Section 8 proves the reduction from the boundary class to all old
   sizes <=2n-3. It gives rooted extension when old U is (5,n)-valid and
   S=U+{r} remains five-cap-free, with r rightmost; S need not avoid
   n-gons. The parent's separate finite certificates for n=6,7,8 do not
   prove this terminal-safe existence statement for general n.
6. **Controls.** [data/controls.json](data/controls.json) records exact
   integer checks at n=6,7,8 of the new formula: signs, general position,
   six maximum cups, six convex complements, six target polygons, no
   longer cup/five-cap/n-gon, the exchange graph, and minimum Delta size
   two. All passed. These fixed-instance controls are COMPUTED, separate
   from the written all-n proof. One CPU (affinity0), RLIMIT_AS400MiB,
   external timeout20s, research venv; completed within one second.
   The parent's separate `check_models.inspect` also passed at n=6,7,8:
   [parametric_parent.json](../data/parametric_parent.json), SHA-256
   `36f6093c437db8c99476735f45b2e5fe400340398a3936adafb3881f03c4829d`.
   No long job, installation, SAT run or certificate replay in this track.
7. **Files and hashes.** This README, `theory.md`, `tools/controls.py`, and
   `data/controls.json`; [SHA256SUMS](SHA256SUMS) pins these files. The
   control JSON also pins its generating script. Scratch:
   `/home/jay/research/data/delta3-codex-20261113/boundary/theory/`.
8. **Limits and failures.** The attempted unqualified lemma is refuted,
   including the upper-chain-three subclass. No existence theorem for
   one-point augmentation or general terminal-safe selection is claimed.
   No control failed; no UNKNOWN result is used. The proof assumes real
   planar points in general position and distinct x-coordinates. No
   literature-priority claim is made. Parent encoder/certificate review
   remains a separate responsibility; it is pending at this freeze.
9. **Reproduce.** From the repository root, after checking current shared
   resource use, run the bounded command below. Compare stdout with
   `data/controls.json`; the output is deterministic.

```bash
bash -c 'ulimit -v 409600; exec timeout 20s taskset -c 0 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/boundary/theory/tools/controls.py'
```

Only `boundary/theory/` and its assigned scratch directory were written.
No git operation, proof deletion, prior-record/shared-manifest change,
repository-root README/math edit or external action was performed.
Track complete and frozen; further changes require a new assigned task.
