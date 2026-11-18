**Verdict: CONFIRMED** (claim `root6-m16-vacuous`, verifier V1, 15 November 2026, 14:27 KST). Size 16 of ROOT(6) is
vacuous: no (5,6)-valid signotope on 16 points exists, and `root6_m16.cnf` is unsatisfiable already in its base clauses.
Label: CERTIFIED (by the DELTA2N certificate, whose LRAT is gone, and by T1's kept re-certification of exactly the base
prefix of `root6_m16.cnf`, whose verdict line and LRAT hash V1 checked) plus the PROVED inheritance argument. V1's own
lemma-free re-certification: the single-CNF attempt ran out of cake_lpr heap within V1's budget (no verdict); an 8-cube
retry runs in unit `esr-agy-v1-m16cubes`, and its result is added below when it ends. [superseded 15 Nov pm (C1 issue
18; note by H1): V1 stopped the cube retry at 14:38 without a verdict, and a heap-300 cake_lpr run on the full proof
also ran out of heap; see the addendum of 14:47 below. V1's own CNF stays COMPUTED only]

# VERIFY_ROOT6_M16_VACUOUS: no 16-point (5,6)-valid signotope; ROOT(6) at 16 points is vacuous

## Claim checked (filed by T4)

`ROOT6_MAIN.md` lists |S| = 15 and 16 as open sizes of ROOT(6) and plans m = 16 by cubes (about 11 h). Size 16 is
vacuous because DELTA2N20261113 certified base(5,6,16) UNSAT (N(6,5,6) = 15 for signotopes). Hence `root6_m16.cnf` is
UNSAT in its base clauses; ROOT(6) for abstract signotopes is completely decided (true for |S| ≤ 14, CERTIFIED; false at
15, claim root6-m15-abstract); for point sets ROOT(6) can fail only on a realizable 15-point valid set; and sizes ≥ 16
are vacuous for every n = 6 statement of the program.

## What was checked

1. **The record being corrected.** `ROOT6_MAIN.md` Status: "m = 15 and 16: not run to completion", "m = 15 and 16 are
   the open sizes" (for point sets, from ES(6) = 17), extrapolation "m = 16 about 11 hours", "Next step: … m = 16 by
   cubes". The 13:12 update supersedes the m = 15 part only; the 13:37 update says "For point sets the least
   counterexample size is 15" but does not retract m = 16. So the correction is apt: m = 16 needs no run.
2. **The cited certificate.** DELTA2N `data/cnf_hashes.tsv` line 53: `eager 5 6 16 base … 560 vars, 107016 clauses,
   UNSAT, CNF b36eb295…, LRAT bfc1d82e…, s VERIFIED UNSAT, 133.2 s / 9.5 s`; README §4.1 notes: "no signotope with 16
   points avoids both a 5-cap and a convex hexagon, so N(6, 5, 6) = 15"; §10 cites the same value at the signotope level
   in the literature (not new). The LRAT was not kept, as the claim says.
3. **A kept second certificate (T1, `pm1115/t1/base16/`).** `valid56_m16.cnf` (`1a556b6e…`, `p cnf 2380 41496`) is
   **identical, comments aside, to the first 41,496 clauses of `root6_m16.cnf`** (V1's extraction `v1_prefix.py`;
   clause sets also compared). Its `cake.out` is exactly `s VERIFIED UNSAT`, the CaDiCaL log says version 2.1.3, and
   `zstd -dc valid56_m16.lrat.zst | sha256sum` = `61337761…a5a7`, the recorded LRAT hash. V1 did not re-run cake_lpr on
   it. Since these clauses are a subset of `root6_m16.cnf`, **`root6_m16.cnf` is UNSAT already in its base clauses**.
4. **The ROOT encoder.** `root6_m16.cnf` (`2208c0b0…`, `p cnf 7203 92344`) regenerates byte for byte from
   `round6/envroot/root_cnf.py 6 16` (`aef1af7a…`). Reading `root_cnf.py`: the first families are the signotope axioms
   (two 3-literal clauses per position triple of every 4-tuple: no +−+ / −+− subsequence), no 5-cap on consecutive
   triples, cv ↔ "4-set convex" (both directions), and one clause per 6-set forbidding all its 4-subsets convex; the
   prefix ends at clause 41,496 (max variable 2,380 = 560 + 1,820; clause 41,497 is the first gon flag `-2381 561`). On
   any model these families force a signotope with no 5-cap and no convex hexagon, and every valid signotope satisfies
   them with cv at its value (consecutive caps imply all-triples caps in a signotope). So base UNSAT ⟺ no valid
   16-point signotope.
5. **Inheritance (PROVED).** A subset of a (5,6)-valid signotope is (5,6)-valid, so no valid signotope has ≥ 16
   points; point sets give signotopes (convex position = every 4-subset convex), so none has ≥ 16 points either.
6. **The rest of the statement.** ROOT(6) for m = 7-14: each `round6/mainsession/root6/cert/root6_m<m>.cake.out` has
   exactly one line `s VERIFIED UNSAT`, and `root_cnf.py 6 m` regenerates every certified CNF hash (checked for
   `lrr6-certified`); m ≤ 6 trivial. m = 15: abstract counterexample (V3 CONFIRMED `root6-m15-abstract`), and since
   13:37 also a real one (V3 CONFIRMED `root6-real-15`). So ROOT(6) is decided at every size, and for point sets the
   least (indeed the only possible) counterexample size is 15. The remark about other n = 6 statements holds for every
   statement whose hypothesis requires a (5,6)-valid set of the given size (for ENV#(6), U itself must be valid, so
   |U| ≥ 16 is vacuous); the exact definition of "cup-side D(5,6)" was not looked up.

## V1's own re-certification (independent CNF, in progress)

[superseded 15 Nov pm (C1 issue 18; note by H1): no longer in progress; it ended without a cake_lpr verdict (addendum
14:47 below)]

- `v1_base_cnf.py` (SHA-256 `682fffcf856561d30442a872b27e435b65e68994240729ffcf52ae49c57be799`), written from the
  definitions without any lemma: 8 forbidden full sign patterns per 4-tuple (≥ 2 sign changes), no 5-cap as "one of
  the 10 triples is a cup", c_Q ← convex(Q) (one direction), no convex hexagon. Soundness: a valid signotope with
  c_Q = convex(Q) satisfies every clause. `v1_base_m16.cnf`: 2,380 variables, 34,216 clauses, SHA-256
  `3e67b59a288e11e618fbb613cc6f99bb02a48dbb8b05fae22f431a8eeaf78381`.
- Controls (`controls_soundness.out`, `controls_model.out`): root6_m15, the three real 13-point sets and the real
  15-point set root6_real15 satisfy the CNF of their size (0 violated clauses); an all-cap string, an all-cup string and
  a one-flip non-signotope violate it; CaDiCaL models of the m = 14 and m = 15 CNFs (SAT in seconds) decode to valid
  signotopes (0 violations, 0 five-caps, 0 convex hexagons).
- Unit `esr-agy-v1-m16cert` (CPUQuota 15 %, MemoryMax 400M, 13:42-14:28) ran `certify_cnf.sh` on `v1_base_m16.cnf`:
  CaDiCaL 2.1.3 printed `s UNSATISFIABLE` (exit 20, 348.5 s CPU; LRAT 904,430,025 bytes, SHA-256
  `e8e76e6c813a546fe32a8da6368c87da61a80ba2eac8a2e6588991487a1eb86f`, kept as `cert/v1_base_m16.lrat.zst`), but
  **cake_lpr stopped with "CakeML heap space exhausted" at heap 250 MB: no verdict**, so this run certifies nothing
  (COMPUTED only). V1's budget (400 MB) does not allow a larger heap. The unit was then stopped by V1 during its second,
  redundant job (the prefix, already certified by T1); that partial LRAT is renamed `*.PARTIAL-stopped-not-a-proof`.
- Retry with smaller proofs: unit `esr-agy-v1-m16cubes` (same limits, started 14:28) certifies the 8 cubes of
  `v1_base_m16.cnf` over the triple variables x(0,8,15), x(3,7,11), x(5,10,14) (all 8 sign combinations, so the cover is
  complete by construction; each cube CNF is the original header + 3, the original clauses verbatim and 3 unit clauses;
  `make_cubes.py`, hashes in `cubes/cubes.txt`). Result: see the addendum below.

### Addendum, 14:47 KST: V1's own certificate could not be completed within V1's budget

- The cube retry did not help: after 86 s CPU the first cube (`cube_ppp`) had 1.03 M conflicts and a 424 MB partial LRAT,
  the same rate as the full run, so the split variables do not shorten the refutation. V1 stopped the unit at 14:38; the
  partial LRAT is renamed `cert_cubes/cube_ppp.lrat.PARTIAL-stopped-not-a-proof` (not a proof).
- cake_lpr on the kept full proof at heap 300 MB (unit `esr-agy-v1-recake`, 14:39-14:43, script `recake300.sh`): CNF
  `3e67b59a…`, decompressed LRAT `e8e76e6c…` (equal to `cert/certify.jsonl`), output **"CakeML heap space exhausted."**,
  0 exact lines (`recake/recake.jsonl`). The decompressed copy was deleted; the `.zst` is kept
  (`cert/v1_base_m16.lrat.zst`, SHA-256 `652ff485ddc6eb4e9e205fc514fcf82a369c49ba88fab274114a4abe0ae824dd`).
- **So V1's lemma-free CNF is UNSAT by CaDiCaL only (COMPUTED), not CERTIFIED.** It needs a cake_lpr run with a heap above
  300 MB (T1's 953 MB proof of the prefix used 1,150 MB). The verdict above does not rest on it: it rests on the DELTA2N
  certificate plus T1's kept, hash-checked certificate of exactly the base prefix of `root6_m16.cnf`. An outside cake_lpr
  re-run of T1's `valid56_m16.lrat.zst` (heap ≥ 1,150 MB) is still to do.
- All V1 units are stopped.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/v1/root6-m16-vacuous/`)

`v1_base_cnf.py`, `v1_controls.py`, `v1_prefix.py`, `run_cert.sh`, `v1_base_m1{4,5,6}.cnf`, `root6_m16_base_prefix.cnf`,
`regen_root6_m16.cnf`, `controls_*.out`, `cert/` (CaDiCaL log, LRAT, `certify.jsonl` when done). No git action; no other
repository file written.
