1. **More rungs** (straightforward, about ×2.2 per rung): N = 37, 36, 35 … with `--nosig` and rows; each
   also lowers the colouring-model bound. Split by the number r of occupied states with f₁ = 5
   (`cube_n.sh`, `cube_cover.py`): the two cases r ≤ 13 and r ≥ 14 at N = 36 are the first example.
   Budget: a `--nosig` rung needs about 1.1 GB for CaDiCaL and a 2.6 GB heap for cake_lpr
   (LRAT 2.2 GB at N = 38).
2. **Where does the colouring model stop?** Its maximum is between 27 and @@COLMAX@@. `colhunt.sh` searches
   for colourings with 28, 30, 33 vertices (only a few minutes were spent). Below that maximum + 1 the
   ladder needs signotope packets (`--sigmax 1`, or lazy refinement with `refine.py`: add the packets of
   all 4-sets inside the occupied set of a spurious solution and repeat; prepared, not needed today).
3. **Structure instead of counting.** Ideas that were not tried:
   - *mirror information*: exact "starts a 6-cup" / "starts a 4-cap" variables (start ranks with
     successor witnesses) and the four mirrored rows (at most 25 points do not start a 6-cup, …), or a
     full two-sided model (incoming and outgoing state of every owner, both injective);
   - *internal catalogs*: give the owners with f₁ ≤ 4 their states inside T (35-state catalog, where
     the (5,6) theorem takes one minute) and the owners with f₁ = 5 their states inside R (Baek's
     catalog), coupled to the 56-state model, so that the solver can use the structure of
     near-extremal T and R instead of the bare counts 25 and 16;
   - *trade-off lemmas* "r points end a 6-cup ⟹ at most 26 − r points do not", proved for one r at a
     time (each is a slice of the 27-point problem; r = 16, 15, … may be easy).
4. **Octagons.** The same generator with G = 8 gives the (4,6)-gon catalog for N(8, 5, 7)
   (`owner.py 3 5 8 N`; no row applies, the trivial bound is 56, ETV value 41). By ETVTHY20261113 §2.1,
   N5 ≤ 22 + N(8,5,7); only N(8,5,7) ≤ 42 would beat the current N5 ≤ 65, i.e. 14 holes. Not run.
5. **Stretch (7; 6, 6)**: `owner.py 4 4 7 31` (70 states, 39 holes needed). Not run: by §6.3 it is
   harder than (7; 5, 7). The colouring question for it (is there a 31-vertex colouring with no 6-cap
   path, no 6-cup path and no weak heptagon?) is a cheap first step (`--nosig`).
6. **Lean / audit.** The owner-model soundness argument (§2) is short and uses only Growth, state
   separation, Lemma R, corner attainment and exact predecessors; the (5,6) certificate has 1.75 M
   clauses (0.61 M without signotope packets) and a 321 MB LRAT proof, so a Lean check along the lines
   of ES(8) ≤ 310 looks feasible. Until then every geometric statement here is "CNF certified +
   written argument".

**Resumable state.** Nothing is running. All generators are deterministic; every certified CNF is
reproduced by the command in the ladder table (flags, N) and matches the recorded SHA-256.
W keeps: `run/*.cnf` and `*.names.pkl` of the certified rungs, the four LRAT files of §5.1, the logs
(`run/*.log`, `run/ladder_*.log`, `run/cubes.log`), and `readme_parts/` + `mk_readme.py`.
