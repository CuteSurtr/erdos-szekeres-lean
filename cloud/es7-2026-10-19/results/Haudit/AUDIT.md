# Haudit: adversarial audit of the mirror sub-case (ii) hull split (results/Mii-S)

Branch `es7-cloud`, base commit d5917a1 (pulled again during the run). Environment: `env.txt`
(4 cores, 15 GB). All paths are under `cloud/es7-2026-10-19/`. The scripts I wrote are in
`results/Haudit/scripts/`. The geometric test, the cube generator and the cover checker are my
own code and import nothing from Mii-S.

Labels: **BUG** breaks soundness. **RISK** could break soundness and is not verified either way.
**NOTE** is informational.

## Findings

### BUG-1: `close_march.py` counts a leaf as closed even when cake_lpr rejects its proof
`results/Mii-S/scripts/close_march.py:46-50` sets `r["status"] = "UNSAT"` whenever CaDiCaL
exits with 20. It stores the cake_lpr line in `r["cake_lpr"]` (line 49) but never tests it.
Line 75 writes every record with `status == "UNSAT"` into `leaves.icnf`.

- shard_plan.md §3a says a case is complete when `cover_check OUT/leaves.icnf` prints
  `s COVERED`. A leaf whose proof failed or crashed in cake_lpr (empty output, OOM,
  `s NOT VERIFIED`) therefore still counts as closed.
- Reproduced: I ran close_march.py on case U2_L with a stub `cake_lpr` that prints
  `s NOT VERIFIED`. The record was `{"cake_lpr": "s NOT VERIFIED", "status": "UNSAT"}`,
  `leaves.icnf` was `a 0`, and covercheck.py printed `s COVERED 1`.
- Impact today: none. All 172 closed cases are `method: direct`, and I re-verified each of
  them (task 5). None of the 36 WAVE1 drivers keeps this behaviour when it writes leaves.icnf
  (see RISK-3). The Mii-S script and the shard plan still describe the unsound procedure.
- Fix: write a leaf only if `r["cake_lpr"] == "s VERIFIED UNSAT"`.

### RISK-1: a truncated last line in a cube file is read as a larger cube
`results/Mii-S/scripts/covercheck.py:13` parses `l.split()[1:-1]` and never checks that the
last token is `0`. If a VM dies while rewriting leaves.icnf, a line such as `a -5 -7 -9`
(the `0` and newline lost) becomes the cube `[-5,-7]`, which claims more than was proved.

- Reproduced with `trunc_example.icnf` (`a 5 0`, `a -5 7 0`, `a -5 -7 -9`). covercheck.py says
  `s COVERED`, but the true leaves do not cover `-5 -7 9`.
- My own checker had the same parse at first. It now rejects any line that does not end in
  ` 0\n`.
- Exposure: drivers that rewrite leaves.icnf periodically without an atomic rename (W10, W19,
  W30, W32, W35, per the driver review). H3's Lean `cover_check` parser was not inspected.
- Fix: reject malformed lines in every cover checker, and write leaves.icnf via tmp + rename.

### RISK-2: the Lean step that composes the certificate argument is not written yet
shard_plan.md §5.1 needs the lemma `not_dimacsSatisfiable_of_blocked`. It is "not yet written".
Until it exists, the propositional chain root → up:U → cases is checked only by cake_lpr on CNF
files that Python built (`cover.py`). I independently confirmed that those files have the
intended content (task 2). The step from them to `cubeCnf F P ++ blocks` in Lean is still open.

### RISK-3: the wave runs on 36 unreviewed forks of the driver
The committed `close_march.py` has no `--top`/`--shard`/`--nshards`, so passing those flags
would make argparse exit with an error. Every WAVE1 VM runs its own modified driver. A read-only
review (subagent; findings I spot-checked are marked) found:

- (a) every driver that writes leaves.icnf requires the exact line `s VERIFIED UNSAT`.
  W22:104 is the exception: its final pass trusts `status == "UNSAT"` alone.
- (b) non-unique scratch names `s_k` in a shared directory. Spot-checked in W01: `WORK`
  defaults to `/tmp/close_march_work` (line 15) and `k` restarts at 1 in each process
  (lines 42-44). Two concurrent processes can then check cube Y's CNF and record the verdict
  for cube X. Also reported for W04, W14, W15, W18, W20, W29 and W34.
- (c) no driver checks that old records in a reused leaves.jsonl belong to the current case
  or top file. The Mii-S original has the same issue: `leaves.jsonl` is opened in append mode
  (line 22), and line 75 ignores the recorded `case_sha256`.
- (d) only W34 and W35 assert the case CNF sha.

Shard selection (`i % nshards == shard` over the 128 `a` lines) is consistent everywhere. The
top-cube sha agrees within each case. My own `march_cu U_L11 -d 7` reproduced W19's top file
byte for byte (sha 55715882…). At the time of the review all 61 committed leaves.icnf were
empty, so no committed result is affected yet. Before the wave cases are accepted:

- re-check each leaf's proof against the CNF rebuilt from F + case + leaf;
- run the cover check on the union of all shards' leaves;
- reject malformed lines.

### NOTE-1: close_march.py liveness and completeness
None of these can produce a false claim:

- If march_cu refutes a sub-formula outright it writes `a 0`, so the child equals its parent
  (line 58) and the driver re-solves it forever.
- Exceptions in worker threads are swallowed. The affected cube disappears and the cover check
  then fails.
- Any CaDiCaL exit code other than 10 or 20 (crash, OOM) is treated as a timeout and the cube
  is split.

### NOTE-2: march_cu at 705b60c6 keeps its refuted branches
`cube.c` `printDecisionNode` writes every non-internal node, refuted ones included, and
`printUNSAT` writes `a 0`. So the "march drops refuted branches" pitfall does not apply to this
commit; it applies to other builds. Every top file in WAVE1 has 128 cubes of depth 7 and 0
refuted. The cover check does not rely on this anyway (mutation tests below).

### NOTE-3: 56 of the 450 cases are vacuous
These are the cases with 2 ∈ U or 3 ∈ L. Their cubes contain ¬X(1,2,3) and so contradict
F's y-flip unit. This matches the normal form: after the flip, point 2 lies below chord 1–3.
The geometric tests never produced them, as expected.

### NOTE-4: symmetry handling is clean
- The y-flip unit X(1,2,3) appears once, as the last clause of F (`mirgen.py --yflip-unit`).
  No cube adds a flip.
- The mirror identification is the orbit substitution X(34−k,34−j,34−i) = **+**X(i,j,k).
  It is applied uniformly in F (mirgen.py `sub`) and in the cubes (`hullsplit.rep`).
- Geometrically, the + sign held on all 5,456 triples of every one of 15,900 sets.
- No case assumes a symmetry that it is not closed under.

### NOTE-5: the full-F check on 7-gon-free sets is vacuous at n = 33
No sampled 33-point set is 7-gon-free, as ES(7) = 33 predicts. Instead, for 1,000 sets I
extended the orientation assignment by the least model of F's cup/cap auxiliaries. Every one of
the 1,034,377 violated F clauses had a real convex 7-gon as its witness, checked exactly. So no
clause of F excluded a set except through a real 7-gon.

### NOTE-6: an error in my own first run
The first geometric run used `np.gcd` on Python ints when clearing denominators. It overflowed
in the projective-map path (`xequal`). Such a set would at worst be analysed as some other
valid symmetric set, and any asymmetry is flagged. I fixed it (`math.lcm`) and re-ran 1,000
degenerate sets (seed 505) and the 4,500 targeted sets with the fix.

## What was checked, and how

### Task 1: tools and hashes
- CaDiCaL c6073042 (3.0.1).
- march_cu from CnC 705b60c6, built with `-O3 -fno-strict-aliasing -Wall -DNDEBUG -fcommon`.
- cake_lpr a36874a8. `cake_lpr.S` sha256 2f3af32d…72b7d4a. `example.cnf/lpr` gives
  `s VERIFIED UNSAT`. A hand-made bogus proof is rejected.
- `make_cnfs.sh` regenerates F with sha256 69c1dc8f…ffff932d. Its header says 47002 vars and
  515121 clauses, which matches the clause count. The file ends with a newline.
- `hullsplit.py cubes` regenerates cases.icnf (6b6f0946…6db742, identical).
- cases.jsonl and cases.icnf list the same 450 (U,L), and the set equals the note's set.
  All 450 case-CNF sha256 recorded in cases.jsonl equal my rebuild (F + units).
- `verify/ii_wave1.json`:
  - assigns exactly the 278 open cases;
  - the shards of each split case are complete (0..k−1);
  - the case shas match cases.jsonl.

### Task 2: code review against soundness.md
- My own `mycube.py` implements the note: hull order, (a)–(c), orbit map with sign +, labels
  2..16. It equals all 450 cubes as sets (`t2_cubes.py`). No cube is self-contradictory, and
  UP(U) ⊆ cube(U,L) for all 450.
- Counts: 121 = 1 + 15 + 105 values of U. 450 = 120 (|U|=0) + 225 (|U|=1) + 105 (|U|=2). No
  obligation is empty, and every case appears in the up:U obligation of exactly its own U.
- All 122 obligation CNFs from `cover.py` equal my independent construction:
  - root is F plus ¬UP(U) for each of the 121 U;
  - up:U is F, then the UP(U) units, then ¬cube(U,L) for the cases with that U, compared as
    multisets;
  - the header clause counts are correct (`t2_oblig.log`).
- Unit appending: `hullsplit.py case`, `cover.py cnf` and `close_march.write` all write the
  header with `nc + added`, then the body, then the units.
- Mutation tests (`t2_mutate.log`, on the U_L2 top file plus a 2-level tree of 149 leaves):
  - remove a leaf, flip a literal: covercheck.py and my checker both say NOT COVERED
    (3 trials each);
  - shorten a leaf, duplicate a leaf: both say COVERED.
  - Dropping a march-refuted branch could not be tested on real data, because no
    refuted cubes occur in any top file at -d 7. Removing any leaf is the same mutation and is
    rejected.
- My cover checker (`mycover.py`) turns the cubes into the CNF {¬c}, solves it with CaDiCaL and
  checks the LRAT proof with cake_lpr.

### Task 3: certificate argument from scratch (`t3_cover_lrat.jsonl`)
- All 122 obligations (root plus 121 up:U) are UNSAT and cake_lpr `s VERIFIED UNSAT`.
- Every CNF sha256 equals the one in `cover_lrat.jsonl`.
- Totals: 515 s CaDiCaL, 313 s cake_lpr, 1.02 GB of proofs (deleted).
- Largest: up: (192 s solve, 29 s check, 418 MB) and root (132 s, 22 s, 199 MB). These agree
  with the recorded 206 s and 130 s.

### Task 4: own geometric test (`geotest.py`, `t4_summary.txt`, `geo_main.jsonl`, `geo_extra.jsonl`)
15,900 accepted sets, all with exact integer arithmetic (rejections: 2,135 not in general
position, 366 with the axis point on the hull).

| kind | accepted sets | failures |
|---|---|---|
| random 4/6-vertex mirror hulls | 2,600 | 0 |
| uniform symmetric | 2,600 (428 with hull ≤ 6) | 0 |
| degenerate: axis point 1–3 units inside the hull | 1,044 | 0 |
| degenerate: hull pair at chord height ±1–3 | 174 | 0 |
| degenerate: interior point 1–3 units inside an edge | 898 | 0 |
| degenerate: x differs by 1 | 969 | 0 |
| degenerate: equal x, then projective map | 515 | 0 |
| mirrored and perturbed halves of 32-point heptagon-free sets from `inputs/distinct_K7.txt` | 2,600 | 0 |
| targeted at each of the 450 cases, 10 times each | 4,500 | 0 |

Checks on every set:
- symmetry after normal form, with the y-flip applied in 7,965 sets;
- the orbit rule +;
- all orientation-only clauses of F;
- all auxiliary-definition clauses under the least model;
- the 7-gon detector against F's forbidding clauses. The cup/cap detector was also checked
  against an independent angular-DP 7-gon search on 309 sets.
- For hulls of size ≤ 6: the case cube from my own monotone-chain hull is satisfied, no other
  of the 450 is, and the hull order matches the note.
- For hulls of size ≥ 8 (2,783 sets): no cube is satisfied.

Coverage: 394 distinct cases were hit, which is every case except the 56 vacuous ones
(NOTE-3), including all 28 non-vacuous 4-gon cases. The witness test of NOTE-5 is in
`t4_witness.jsonl`.

### Task 5: closed cases (`t5_sample32.jsonl`, `t5_all172.jsonl`)
- The sample was the 10 hardest by recorded time plus 22 at random (seed 20261020). After it
  passed I re-checked **all 172** closed cases.
- Each case CNF was rebuilt from F plus `mycube` units. All 172 sha256 match cases.jsonl. All
  are UNSAT with cake_lpr `s VERIFIED UNSAT`: 699 s solve and 445 s check in total, at most
  20 s and 11 s for a single case.
- All 172 are `method: direct`, so the leaf set is the single empty cube and the cover holds
  trivially.

## Not checked
- H3's Lean proofs (`Mir.interiorCnf_satisfiable`, `Mir.interiorTieBreak`), the Lean generator,
  and `lake exe cover_check`. These were not built.
- The 278 open cases and any WAVE1 leaves (none closed yet).
- The WAVE1 drivers beyond the read-only review in RISK-3. The scratch-dir collision is
  confirmed in W01 only. I did not check whether any VM actually ran two processes at once.
- A geometric test with an axis that is not vertical (rigid-motion step), and normal-form
  inputs whose x-coordinates are separated by the projective map at scales other than the
  ones generated.
- The layer split (`layers.py`, `cover2.py`), which is not used by the 450-case argument.
- A deliberate mutation of march output that drops a refuted branch. Real top files contain
  none, but removing any leaf is detected.
