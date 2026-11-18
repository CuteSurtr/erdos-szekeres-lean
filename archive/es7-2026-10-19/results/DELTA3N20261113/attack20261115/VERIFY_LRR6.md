**Verdict: CONFIRMED** (claim `lrr6-certified`, verifier V1, 15 November 2026, 14:22 KST). LRR(6) holds for every
(5,6)-valid signotope, hence every point set in general position. Labels as claimed: CERTIFIED for |S| = 15 (T1's
cake_lpr run; V1 checked the verdict line, the CNF and LRAT hashes and the encoder, but did **not** re-run cake_lpr, whose
1,150 MB heap exceeds V1's 400 MB budget), PROVED for the combination with the cited CERTIFIED results.

# VERIFY_LRR6: the rooted left-or-right disjunction LRR(6)

## Claim checked (filed by T1)

LRR(6): if S is (5,6)-valid, r ends a 4-cap and l starts a 4-cap, then S − r has a weak Δ A with A + r 4-cap-free, or
S − l has a weak Δ A with A + l 4-cap-free (`PROBES_1115PM.md`, Definitions). (1) |S| = 15: `lrr6_m15.cnf` (encoder
`t3/tools/lr_cnf.py 6 15`) is UNSAT, certified. (2) |S| ≤ 14: ROOT(6) is CERTIFIED and implies LRR(6) at each size.
(3) |S| ≥ 16: no (5,6)-valid signotope exists.

## (a) Encoder soundness and the CNF

- **Reading of `lr_cnf.py`** (SHA-256 `8669a98b…5de562`, as claimed). Put every auxiliary variable at its defining
  condition: cv = convex 4-set (exact equivalence), Z_T = T convex, F_K = (abc, bcd caps), R_t = (abc, bcr caps),
  L_t = (lab, abc caps). For an LRR(6) failure S: the signotope clauses hold; "no 5-cap" with consecutive triples holds
  because in a signotope consecutive caps make every triple a cap (axiom on each 4-tuple); "no convex 6-set" holds;
  OR R and OR L hold because r ends and l starts a 4-cap. A right row for A ⊆ S − r is satisfied iff A contains a 4-cap,
  or some (a,b,c) ⊆ A has (a,b,c,r) a 4-cap (the only 4-caps of A + r through r), or A misses a convex pentagon of S − r,
  i.e. iff A is not a right-rooted weak Δ; symmetrically for left rows (4-caps through l start at l). In a failure no A
  is rooted on either side, so every row holds. Keeping only rows with |A| ≤ |W| − 4 removes clauses and keeps
  soundness. **UNSAT ⇒ LRR(6) for all signotopes on 15 points. Correct.**
- **Regeneration:** `lr_cnf.py 6 15` reproduces `t3/cnf/lrr6_m15.cnf` byte for byte, SHA-256
  `0555d770b08e2e0d5857847a8633ef40d06437a7ae7598ab18383ed265b6a1a2` (header `p cnf 6552 79293`, 31,828 rows).
- **Semantic test of the actual CNF file** (`v1_lr_eval.py`, own code). Under the canonical assignment of a valid
  15-point set, the soundness argument predicts that the violated clauses are exactly one row per rooted weak Δ with
  |A| ≤ 10 (left or right), plus OR R / OR L if a hypothesis fails. V1 computes that number independently by exhaustive
  enumeration with `v1lib` and compares:

  | set | right-rooted | left-rooted | violated clauses | match |
  |---|---|---|---|---|
  | root6_m15 (abstract) | 0 | 231 | 231 | yes |
  | t1/root6_real15 (real) | 0 | 258 | 258 | yes |
  | t1/real/m15_it10_real | 0 | 260 | 260 | yes |
  | t1/real/m15_it21_real | 0 | 220 | 220 | yes |
  | root6_real15 reflected (x → −x) | 258 | 0 | 258 | yes |
  | m15_it10_real reflected | 260 | 0 | 260 | yes |

  So both row families, the base clauses and the hypothesis clauses behave exactly as the soundness argument says, on
  real sets. (No tested set failed a hypothesis, so OR R / OR L were only tested in the satisfied state.)

## (b) The certificate (`t1/lrrcert/cert/`)

- `certify.jsonl`: CNF SHA-256 `0555d770…` (equal to the regenerated CNF), LRAT SHA-256 `625dffe5…a02f`, 3,619,946,969
  bytes, verdict `s VERIFIED UNSAT`, heap 1,150 MB.
- `lrr6_m15.cake.out` is exactly the line `s VERIFIED UNSAT`; the CaDiCaL log says `c Version 2.1.3` and `s UNSATISFIABLE`.
- `zstd -dc lrr6_m15.lrat.zst | sha256sum` = `625dffe51617b889c44edac6f5fac5c79fcdd20bd318e1e320b9bc6a1390a02f`,
  3,619,946,969 bytes: **equal**.
- **cake_lpr not re-run by V1** (budget). The proof is kept as zstd; an outside re-run is still to do. [superseded 15
  Nov pm (C1 issue 18; note by H1): done twice, by the main session (`round6/mainsession/lrr6recake/`, heap 1400,
  finished 14:21:41) and by T3 (`pm1115/t3/replay/t1_lrr6_m15.json`, heap 1500, 16:45:11); each output is exactly one
  `s VERIFIED UNSAT` line, with CNF `0555d770…` and streamed LRAT `625dffe5…` equal to the values above]

## (c) |S| ≤ 14

`ROOT6_MAIN.md` lists ROOT(6) CERTIFIED for m = 7-14 (m ≤ 6 trivial). In `round6/mainsession/root6/cert/` each
`root6_m<m>.cake.out`, m = 7..14, has exactly one line `s VERIFIED UNSAT`, and `root_cnf.py 6 m` regenerates CNFs whose
SHA-256 equal the certified `cnf_sha256` for all eight sizes. V1 read `root_cnf.py`: its base and rows are those of
`lr_cnf.py` (right side only), with the same soundness argument. ROOT(6) at m implies LRR(6) at m, since LRR's hypothesis
contains "r ends a 4-cap" and ROOT gives the right alternative. cake_lpr was not re-run on these proofs by V1.

## (d) |S| ≥ 16

- DELTA2N20261113 `data/cnf_hashes.tsv` (eager 5 6 16 base, UNSAT, `s VERIFIED UNSAT`; its LRAT was not kept).
- T1's re-certification `t1/base16/`: `valid56_m16.cnf` (`1a556b6e…`, `p cnf 2380 41496`) is **identical, comments
  aside, to the first 41,496 clauses of `root6_m16.cnf`** (the base families of `root_cnf.py`, which force a valid
  signotope); its `cake.out` is exactly `s VERIFIED UNSAT`; CaDiCaL 2.1.3; `zstd -dc | sha256sum` = `61337761…a5a7` as
  recorded. Validity passes to subsets, so no valid signotope has 16 or more points.
- V1's own lemma-free re-certification of base(5,6,16) is running for claim `root6-m16-vacuous` (see that verdict).
  [superseded 15 Nov pm (C1 issue 18; note by H1): it ended without a cake_lpr verdict (heap exhausted at 250 and
  300 MB), so it is COMPUTED only; VERIFY_ROOT6_M16_VACUOUS.md, addendum 14:47]

## Conclusion

Sizes ≤ 14 (ROOT, CERTIFIED), 15 (this CERTIFIED run) and ≥ 16 (vacuous, CERTIFIED) cover all sizes, so LRR(6) holds for
every (5,6)-valid signotope and so for every point set in general position (orientations of a point set form a
signotope; convex position is decided by 4-subsets). Weak D(5,7) and weak D(5,8) are not affected.

## Files (`/home/jay/research/data/roadmap-20261115/pm1115/v1/lrr6-certified/`)

| file | SHA-256 |
|---|---|
| v1_lr_eval.py | `a935aeb954f020133d5131948ff176f1f8e19fa49346566a8fa27651d4747a13` |
| v1_lr_eval.out | `9130ddb6a81bbcd01909fbf52a9bcdb94c8013b0674c960357a8fcfef685247a` |
| regen_lrr6_m15.cnf | `0555d770b08e2e0d5857847a8633ef40d06437a7ae7598ab18383ed265b6a1a2` |
| lrat_sha256.txt / lrat_bytes.txt | the streamed hash and size above |

Rerun (seconds): `python3 -I lr_cnf.py 6 15 | sha256sum`; `venv python -I v1_lr_eval.py <lrr6_m15.cnf> 6 <set.json>...`;
`zstd -dc lrr6_m15.lrat.zst | sha256sum`. No git action, no unit for this claim, no other repository file written.
