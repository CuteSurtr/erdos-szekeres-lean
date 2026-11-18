# Δ-route SAT probes and certificates, 15 November 2026 evening (track D1, 19:00-22:40 KST)

**Final status, 22:15 KST. All D1 units are stopped (none active at 22:14).**
- **C1(6) is CERTIFIED at 15 points and therefore holds for every signotope** (claim `d1-c1six`, **CONFIRMED by VB at
  19:34** with its own cake_lpr re-run at heap 2,000 MB). With C2(6) (`p1-c2six`, CERTIFIED) both halves of P1's
  Proposition R hold at n = 6.
- **LR(7) at 16 is reduced to four CNFs** (case split on β(r), α(l); claim `d1-lr7m16-split`, PROVED, **CONFIRMED by VB
  at 21:16**). **None of the four has a verdict**: C1(7) at 16 stopped at 7.4 M conflicts (3,267 CPU-s), the three core
  cubes K1, K2, K3 reached their wall limits at 6.5 M, 5.7 M and 5.6 M conflicts (4,405, 3,156, 3,156 CPU-s; 50 % CPU).
  So LR(7) at 16 and weak D(5,7) at 16 remain OPEN.
- **C1(7) at 15: no verdict** after 20.3 M conflicts and 11,241 CPU-s (wall limit 22:13), i.e. already more search than
  LR(7) at 15 needed (15.7 M conflicts, 7,839 CPU-s, on T1's flat encoder; C1(7) used T3's compact encoder, so the
  comparison crosses encoders): the one-sided C1(7) CNF was not easier than LR(7) (HEURISTIC). C2(7) and TWO-ENV#(7) were not run (CPU budget); their CNFs are ready.
- LR(7) at 16, SAT mode with phases from R7's real 16-point near-miss: no model in 32 min (UNKNOWN, proves nothing).
- Weak D(5,7) and weak D(5,8) remain OPEN. No ES bound changes. LR(7) for |S| ≤ 15 is CERTIFIED by the main session's
  cake_lpr run of 19:04 on T1's proof (`round6/mainsession/lrr7m15cake/`, not D1's work).

Labels: PROVED / CERTIFIED (CaDiCaL 2.1.3 LRAT, cake_lpr's exact line `s VERIFIED UNSAT`, hashes recorded) / EXACT /
COMPUTED / HEURISTIC. Nothing is rounded up. Work directory (not in Git):
`/home/jay/research/data/roadmap-20261115/pm1115/d1ev/`. Units `esr-agd-*`.

## Status table

| statement | size | CNF (SHA-256) | run | result | label | claim |
|---|---|---|---|---|---|---|
| **C1(6)**: r ends a 4-cap and a 5-cup ⟹ S has a weak Δ through r | 15 | `c1_rcup6_m15.cnf` (`078f207e…`; byte-identical to P1's file; base regenerated) | `esr-agd-c1six`, certify_cnf.sh, 19:02-19:27 | **UNSAT**: CaDiCaL 1,269 CPU-s, 4,228,926 conflicts, max RSS 194 MB; LRAT 5,559,430,678 B (`fb3b9939…`); cake_lpr heap 1200, 216 s, **exactly one line `s VERIFIED UNSAT`**; proof kept (`.zst` 1,485,329,073 B, `9a1c9eba…`) | **CERTIFIED** | `d1-c1six` (filed 19:28; VB CONFIRMED 19:34, own cake_lpr re-run, heap 2000) |
| C1(6), all sizes | all | – | – | ≤ 14: ROOT(6) CERTIFIED ≤ 14; 15: above; ≥ 16: vacuous (`root6-m16-vacuous`) | CERTIFIED (15) + citations | `d1-c1six` |
| C1(7) | 15 | `c1_rcup7_m15.cnf` (`54c59be6…`) | `esr-agd-c1sev15`, cad_cert.sh, 50 % CPU 19:03-19:08, then 100 %, CaDiCaL wall limit 11,400 s | **no verdict** at the limit (22:13:47): 20,309,313 conflicts, 11,241 CPU-s; the partial LRAT (about 47 GB, not a proof) was removed by the script | UNKNOWN | – |
| C1(7) | 16 | `c1_rcup7_m16.cnf` (`9c7a0da1…`) | `esr-agd-c1sev16`, cad_cert.sh, 100 %, 19:28-20:22 | **no verdict**: stopped by D1 at 20:22 after 7,394,835 conflicts and 3,267 CPU-s, to give the CPU to the K2/K3 cubes (C1(7) at 15 already looked as hard as LR(7) at 15, so C1(7) at 16 had little chance by 22:08); the 18.3 GB partial LRAT (not a proof) was removed | UNKNOWN | – |
| LR(7) core cube K1: LR(7) failure with β(r) ≤ 4 and α(l) ≤ 4 (case split below) | 16 | `lrK1_m16.cnf` (`0ce89610…`) | `esr-agd-lrk1`, cad_cert.sh, 50 %, 19:41-22:08 | **no verdict** at the wall limit: 6,503,107 conflicts, 4,405 CPU-s; partial LRAT removed | UNKNOWN | `d1-lr7m16-split` (reduction only) |
| LR(7) core cube K2: β(r) = 5, α(l) ≤ 4 | 16 | `lrK2_m16.cnf` (`59349034…`) | `esr-agd-lrk2`, cad_cert2.sh, 50 %, 20:22-22:08 | **no verdict**: 5,664,877 conflicts, 3,156 CPU-s; partial LRAT removed | UNKNOWN | `d1-lr7m16-split` (reduction only) |
| LR(7) core cube K3: β(r) = α(l) = 5 | 16 | `lrK3_m16.cnf` (`8bc9f335…`) | `esr-agd-lrk3`, cad_cert2.sh, 50 %, 20:22-22:08 | **no verdict**: 5,594,998 conflicts, 3,156 CPU-s; partial LRAT removed | UNKNOWN | `d1-lr7m16-split` (reduction only) |
| **Reduction** LR(7) at 16 ⟸ UNSAT of `c1_rcup7_m16`, `lrK1_m16`, `lrK2_m16`, `lrK3_m16` (section below) | 16 | – | – | case split on β(r), α(l) and the mirror image | **PROVED** | `d1-lr7m16-split` (VB CONFIRMED 21:16, own regeneration of all four CNFs) |
| LR(7), SAT mode, phases from R7's best real 16-point set `r7/lns/f4.json` (4 weak Δs through r) | 16 | `lc7_m16.cnf` (`898569a8…`, T3's `lr_compact.py 7 16`) | `esr-agd-lr16ph`, pysat CaDiCaL 1.9.5, 50 %, 19:08:43-19:41 (stopped to free the CPU for the K1 cube) | **no model** in 32 min wall (about 16 CPU-min); proves nothing | UNKNOWN | – |

**Consequence at n = 6 (PROVED combination, no new computation):** C1(6) (this record) and C2(6) (`p1-c2six`) hold for
every signotope, so by Proposition R (`p1-cupext`, PROVED) LR(6) follows for every signotope a third time, through the
reduction. (LR(6) itself was already CERTIFIED twice: `lrr6-certified`, `lr6-m15-second`.)

## Definitions

As in PROOF_LR_ATTEMPT_P1.md §0 and PROBES_1115PM.md (Definitions). (5,n)-valid = signotope with no 5-cap and no convex
n-set; gon = convex (n−1)-set; weak Δ = 4-cap-free set meeting every gon; r = m−1, l = 0; β(v) / α(v) = number of points
of a longest cup ending / starting at v.
- **C1(n):** for every (5,n)-valid S whose rightmost point r ends a 4-cap: if r ends an (n−1)-cup, S has a weak Δ
  through r.
- **C2(n):** if r ends a 4-cap, l starts a 4-cap and S has no weak Δ through r, then l starts an (n−1)-cup.
- **Prop. R** (P1, PROVED, claim `p1-cupext` CONFIRMED): C1(n) ∧ C2(n) at size m ⟹ LR(n) at size m (C2 applied to S,
  C1 to the mirror image μS, both of size m).

## CNFs and encoder review

- Base: T3's compact ROOT encoder `t3/tools/root_compact.py`. `rc6_m15.cnf` regenerated here (SHA-256 `152d8a20…`, equal
  to T3's file); `rc7_m15/16/17.cnf` used as T3 wrote them (`ab88cb34…`, `b78f5f51…`, `ec553501…`, equal to T3's
  `SHA256SUMS.final`).
- Add-on: P1's `p1/addcup.py` (SHA-256 `0eaca59b…`; `rcup` = r ends an (n−1)-cup, `nolcup` = l starts no (n−1)-cup,
  `norcup` = r ends no (n−1)-cup). The C2 CNFs do not add "l starts a 4-cap", so an UNSAT verdict proves the stronger
  form (as for P1's C2(6)).
- **D1's review of the soundness direction (UNSAT ⟹ statement), done line by line on `root_compact.py`.** For a
  counterexample S put every variable to its defining condition: x_t = sign; cv_Q ⟺ Q convex (the four 2-literal
  clauses give cv ⟹ equalities, the four 5-literal clauses forbid ¬cv with both equalities); the 8 clauses per 4-set
  forbid the patterns +−+ and −+− in any 3 of the 4 positions (= at most one sign change, the signotope axiom); "some
  consecutive triple of every 5-set is a cup" holds because a 5-set with three consecutive caps is a 5-cap in a
  signotope; B(X) := "X ⊆ U contains a gon of U" satisfies B(X) ⟹ X convex at |X| = n−1 and B(X) ⟹ ∨ B(X−v) over the
  n smallest points of X (one of them is outside the gon); Bad(D) := "D + r contains a 4-cap" satisfies the base rule
  (abcr a 4-cap ⟹ abc, bcr caps), the 4-set rule (a 4-cap inside D, flag F_D ⟹ abc, bcd caps, or one through r using
  three points of D) and the ≥ 5 rule (one of the 5 smallest points of D is outside the 4-cap); the hypothesis
  ∨ Bad(abc) is "r ends a 4-cap"; each row Bad(D) ∨ B(U−D) holds because D + r is not a weak Δ of S (a missed gon avoids
  r, so it is a gon of U inside U − D; for |U−D| = n−2 the row is Bad(D) alone and D + r must contain a 4-cap; for
  |D| ≤ 2 the row is B(U−D) alone and D + r cannot contain a 4-cap). `addcup.py`: rcup with y_T := "T + r is a cup"
  (β(r) = n−1 gives a 5-set T, no n-cup exists); nolcup and norcup are the literal conditions. So every clause holds for
  a counterexample: UNSAT proves the statement for all signotopes with m points. The same review covers T3's
  `lr_compact.py` (both sides; BadL base: lab and abc caps ⟹ labc a 4-cap; B(X) only for X not containing both l and r,
  closed under the recursion).
- **D1's own semantic controls** (`d1ev/tools/ctl_cup.py`, uses D1's exact checker `d1ev/tools/d1check.py`; pysat
  CaDiCaL 1.5.3 with all triple variables fixed to the set's signs): base ROOT CNF SAT ⟺ (valid, r ends a 4-cap, no weak
  Δ through r); add-on alone SAT ⟺ β(r) = n−1 (rcup) resp. α(l) ≠ n−1 (nolcup); full C1 / C2 CNF ⟺ both.
  - n = 6, m = 15: 25 sets (T3's `root6_m15`, `rc6_m15_fg`, `tspm6_m15`, T1's `root6_real15` and 21 real `t1real/m15_it*`)
    × {set, mirror} = 50 instances, **0 mismatches** (base SAT 24, add_rcup SAT 26, add_nolcup SAT 24, C1 SAT 0, C2 SAT 0).
  - n = 7, m = 17: R7's and T1's real ROOT(7) sets, T3's abstract model and T3's copy `blk_t1real17` × 2 = 8 instances,
    **0 mismatches** (base SAT 4, add_rcup SAT 4 (mirrors, α(l) = 6), add_nolcup SAT 4, C1 SAT 0, C2 SAT 0).
  - Checker controls: `d1check.py` reproduces T3's counts on R7's real set (8,435 weak Δs, 0 through r, 4,316 through l),
    on `blk_t1real17` (8,195 / 0 / 4,129) and on `root6_m15` (467 weak Δs, 231 through l, 329 pentagons, 98 four-caps).
- Hashes of every CNF: `d1ev/cnf/SHA256SUMS`.

## LR(7) at 16: cost and a sound case split (plan)

- Expected cost of a direct LR(7) proof at 16 (HEURISTIC): LR(7) at 15 needed 15.7 M conflicts, 7,857 s and a 23.7 GB
  LRAT (T1); cake_lpr ran out of heap at 1,150 MB and passed at 4,500 MB (main session, 19:04). T1's m = 16 run reached
  4.5 M conflicts and 8.8 GB of LRAT in 3,782 s without a verdict. Growth factors per point in today's runs were ×4-×20,
  so m = 16 needs roughly 10-45 CPU-h and an LRAT of the order of 100 GB, whose cake_lpr check would need a heap above
  my 2.5 GB budget. Not feasible tonight as one run.
- **Case split (PROVED, elementary):** let S be a 16-point LR(7) failure (r ends a 4-cap, l starts a 4-cap, no weak Δ
  through r or l). If β(r) = 6, S satisfies the C1 CNF `c1_rcup7_m16.cnf`. If α(l) = 6, the mirror image μS (16 points;
  μ(l) is its rightmost point, ends a 4-cap, ends a 6-cup and lies in no weak Δ of μS, since μ maps caps to caps, cups
  to cups and weak Δs to weak Δs) satisfies the same CNF. Otherwise S satisfies `lrcore7_m16.cnf` = `lc7_m16.cnf` +
  addcup `norcup nolcup` (β(r) ≤ 5 and α(l) ≤ 5). So **UNSAT of `c1_rcup7_m16.cnf` and of `lrcore7_m16.cnf` proves
  LR(7) at 16**, and with weak D(5,7) ≤ 15 (CERTIFIED, DELTA2N) T4's L1 then gives weak D(5,7) at 16. Each piece can be
  split further into cubes on triple variables (a sound cover: all 2^k sign patterns of k chosen triples).
- **Second split of the core (PROVED, elementary), used tonight:** in the core β(r), α(l) ≤ 5. Cases: K1 β(r) ≤ 4,
  α(l) ≤ 4 (`lrK1_m16.cnf` = `lc7_m16` + `norcup:5 nolcup:5`); K2 β(r) = 5, α(l) ≤ 4 (`lrK2_m16.cnf` = `lc7_m16` +
  `norcup:6 rcup:5 nolcup:5`); β(r) ≤ 4, α(l) = 5 is the mirror image of K2 (μS is again a 16-point LR(7) failure, with
  β and α exchanged), so it needs no CNF; K3 β(r) = α(l) = 5 (`lrK3_m16.cnf` = `lc7_m16` + `norcup:6 nolcup:6 rcup:5
  lcup:5`). So **LR(7) at 16 ⟸ UNSAT of `c1_rcup7_m16`, `lrK1_m16`, `lrK2_m16` and `lrK3_m16`.**
- `d1ev/tools/addcup2.py` (D1) writes these blocks with an explicit cup length k (`rcup`, `lcup`, `norcup`, `nolcup`).
  Controls: its output is byte-identical (after the comment line) to P1's `addcup.py` for `c1_rcup7_m16`,
  `c2_nolcup7_m16` and `lrcore7_m16`; `ctl_cup2.py` fixes all triples of 6 known sets (15, 16, 17 points; R7's real
  ROOT(7) set, T3's abstract model, R7's real 16-point sets f4 and seed_g9, two ROOT(6) sets) and their mirrors and
  checks each block alone for k = 4, 5, 6 against the exact β(r), α(l): **144 checks, 0 mismatches** (the positive side
  of `rcup:5` / `lcup:5` is exercised by the n = 6 sets, α(l) = 5).

## Files (work directory `/home/jay/research/data/roadmap-20261115/pm1115/d1ev/`, not in Git)

- `tools/`: `d1check.py` (exact checker from the definitions: signotope axioms, 5-caps, convex sets, 4-caps, β(r),
  α(l), all weak Δs by enumeration of all 2^m subsets), `ctl_cup.py` and `ctl_cup2.py` (semantic controls),
  `addcup2.py` (cup blocks with explicit length), `phase_sat.py` (SAT mode with initial phases, pysat CaDiCaL 1.9.5),
  `cad_cert.sh` (CaDiCaL with LRAT and a wall limit, then cake_lpr under a lock, then zstd) and `cad_cert2.sh` (the
  same, but the proof is hashed and compressed before cake_lpr, which reads it through a FIFO).
- `cnf/` (all CNFs, regenerable; `cnf/SHA256SUMS`), `cert/<run>/` (CaDiCaL logs, `certify.jsonl`, cake_lpr output,
  proofs kept as `.lrat.zst`), `runs/` (controls, phase-search log), `claims/` (claim JSON as filed).

## Resume commands

```bash
D=/home/jay/research/data/roadmap-20261115/pm1115/d1ev; PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd $D; export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1
# regenerate the CNFs
$PY -I ../t3/tools/root_compact.py 6 15 > cnf/rc6_m15.cnf; $PY -I ../p1/addcup.py cnf/rc6_m15.cnf 15 6 rcup > cnf/c1_rcup6_m15.cnf
for m in 15 16 17; do $PY -I ../p1/addcup.py ../t3/cnf/rc7_m$m.cnf $m 7 rcup > cnf/c1_rcup7_m$m.cnf; $PY -I ../p1/addcup.py ../t3/cnf/rc7_m$m.cnf $m 7 nolcup > cnf/c2_nolcup7_m$m.cnf; done
$PY -I ../t3/tools/lr_compact.py 7 16 > cnf/lc7_m16.cnf
$PY -I tools/addcup2.py cnf/lc7_m16.cnf 16 norcup:5 nolcup:5 > cnf/lrK1_m16.cnf
$PY -I tools/addcup2.py cnf/lc7_m16.cnf 16 norcup:6 rcup:5 nolcup:5 > cnf/lrK2_m16.cnf
$PY -I tools/addcup2.py cnf/lc7_m16.cnf 16 norcup:6 nolcup:6 rcup:5 lcup:5 > cnf/lrK3_m16.cnf
sha256sum -c cnf/SHA256SUMS
# controls
$PY -I tools/ctl_cup.py 6 15 cnf/rc6_m15.cnf cnf/c1_rcup6_m15.cnf ../p1/c2_nolcup6_m15.cnf ../t3/models/root6_m15.json ../t3/models/t1real/*.json
$PY -I tools/ctl_cup2.py 7 ../r7/root7_real17.json ../r7/lns/f4.json ../t3/models/root6_m15.json
# a proof run as a unit (cake_lpr needs MemoryMax above the heap; cad_cert2.sh keeps the proof before cake_lpr)
systemd-run --user --unit=esr-agd-<job> -p CPUQuota=100% -p MemoryMax=2450M -p MemorySwapMax=0 -p RuntimeMaxSec=<s> \
  --nice=10 --working-directory=$D bash tools/cad_cert2.sh cnf/lrK1_m16.cnf cert/lrk1 <wall_secs> 1900
# cake_lpr re-run of a kept proof (main session's script; heap in MB)
bash /home/jay/research/data/roadmap-20261115/round6/mainsession/recake_generic.sh cnf/c1_rcup6_m15.cnf cert/c1six/c1_rcup6_m15.lrat.zst <outdir> 1500
grep -cx 's VERIFIED UNSAT' <outdir>/cake.out
```

## What remains (as of 22:15)

- **LR(7) at 16** (⟹ weak D(5,7) at 16): the four CNFs of `d1-lr7m16-split` are ready and confirmed; none is decided.
  Tonight's measurements (HEURISTIC): C1(7) at 16 had no verdict after 7.4 M conflicts, K1/K2/K3 after 5.6-6.5 M each;
  for comparison LR(7) at 15 needed 15.7 M conflicts in one run. A real attempt needs several CPU-hours per piece and,
  for certification, cake_lpr heaps above 2 GB (LRATs grew at 2-5 MB per CPU-second tonight: about 47 GB for C1(7) at 15
  after 20 M conflicts). Use `cad_cert2.sh` (proof hashed and compressed before cake_lpr) and further cubes on triple
  variables inside each piece if wall time is short.
- **C1(7) at 15** is undecided after 20.3 M conflicts (more than LR(7) at 15 needed); C1(7) and C2(7) at 15-17, the SAT-mode
  counterexample searches for C1(7)/C2(7) at 17, and TWO-ENV#(7) at 15 by cubes were not run or not finished (CPU
  budget). CNFs: `cnf/c1_rcup7_m1{5,6,7}.cnf`, `cnf/c2_nolcup7_m1{5,6,7}.cnf`; TWO-ENV#(7): T3's `t3/cnf/te7_m15.cnf`.
- Since LR(7) at 15 is CERTIFIED directly (main session, 19:04), C1(7) ∧ C2(7) at 15 would only give a second route
  to it plus evidence for the two conjectures; at 16 they are one way to LR(7) at 16, but tonight's data suggest the
  one-sided CNFs are not cheaper than the two-sided ones.
- `SHA256SUMS.final` of the work directory: 52 entries, its own SHA-256 `0741c153…` (22:14).
