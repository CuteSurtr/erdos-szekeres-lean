# VERIFY_N66LE55_FINAL_VN: final independent check of claim n66-le55-cubes-1118 (verifier VN, 18 November 2026, 08:17–08:32 KST)

**Verdict: CONFIRMED at the claimed label.** N66 ≤ 55 is CERTIFIED per cube: each of the 132 leaves has a trimmed
cube CNF that cake_lpr accepted with the exact line `s VERIFIED UNSAT`. The cover of the 2^14 split is exactly
complete, and every trimmed CNF is a subset of the one base CNF F_c plus that cube's own unit clauses. Soundness rests
on the written (PROVED) arguments of the model and of the symmetry breaking (parent README §2, §6.3, §6.7), the
same trust base as N66 ≤ 56. The result is not Lean-checked and not refereed.

**File names.** The claim names `VERIFY_N66LE55_FINAL.md` and `claims/n66-le55-cubes-1118.verdict.json`. Both
already hold verifier VS's verdict (04:30–04:34, CONFIRMED), and VS still holds the claim lock. VN left them
untouched and wrote this file and `claims/n66-le55-cubes-1118.verdict-VN.json` instead. VN read only the headline of
VS's verdict and none of VS's code.

All computations below use VN's own code, written from cubes20261115/README.md §2 and §6 and parent README §6.7. No
code of the driver, P307V, AN or VB was reused. Work folder
V = `/home/jay/research/data/roadmap-20261115/pm1115/vn1118/`. Inputs were only read. Other tracks' files and the
lock were not touched.

## 1. Acceptance and cover (`V/vn_check.py meta` → `V/vn_meta.json`)

**Acceptance.** VN applied these rules to every directory `p2/c14/<id>/it*` (176 directories, all `it1`). A directory
is accepted when all of the following hold:
- `cake.out` contains exactly one non-empty line, `s VERIFIED UNSAT`;
- `cake.err` (the `/usr/bin/time -v` log) has no `s ` line and exit status 0;
- cert.json has ALL_OK, the cake line, budget 14, W_size 70, holes_at_least 15 and bound 55;
- verify.json has ALL_OK, the cake line, budget 14, 0 unclassified clauses, and trim hashes equal to cert.json;
- layout.json has W = range(70) and L = 14;
- layout.json has the same sb_pairs, sel = [988541, 988610], vars, rows_file (`mono/rows_1832.json`) and
  activated_quadruples (660,810) as the F_c layout `p2/b14h2/it1/layout.json`, and its clause count is
  |F_c| + |cube|;
- the sb_pairs in cert.json and verify.json equal the F_c layout's list;
- the cube is the same in cert.json, verify.json, layout.json and the directory name (first 6 letters = states
  25 12 16 29 17 37, then `_<state><h|o>`; o = occupied = +sel_s, h = hole = −sel_s, sel_s = 988541 + s);
- the trim.cnf SHA-256, recomputed, equals cert.json.

| result | count |
|---|---|
| accepted | **132** |
| rejected | **0** |
| directories without cert.json | 44, all split parents (each has accepted descendants) |
| cube sizes 6 / 7 / 8 / 9 / 10 / 11 / 12 | 38 / 31 / 27 / 26 / 7 / 1 / 2 |

**Exact cover.** VN enumerated every assignment of the 14 states that appear in the accepted cubes: 12, 16, 17, 23,
25, 29, 37, 39, 40, 44, 45, 46, 49 and 52. Of the **16,384 assignments, 0 are uncovered and 0 are covered twice**,
and Σ 2^−|c| = 1 exactly (Fraction). The 132 cubes therefore partition the split, and the cover is **COMPLETE**.

## 2. Four-check coverage (same script; table rows parsed per column header)

A row passes when its cake column is exactly `` `s VERIFIED UNSAT` ``, every check column (hashes, 2, 3, 4 families,
"= cert.json kinds", 4 rows) starts with `yes`, and its verdict is PASS where that column exists.

A row is current when:
- for VB rows: both 12-hex hash prefixes (trim.cnf and LRAT stream) equal today's cert.json;
- for U1 rows (which carry no hashes): cert.json time is no later than 15 Nov 18:23, when U1 stopped.

| record | rows | accepted cubes passing and current |
|---|---|---|
| VERIFY_N66CUBES.md (U1) | 76 | 76 |
| VERIFY_N66CUBES_EV.md (VB) | 23 | 23 |
| VERIFY_N66CUBES_1116.md (VB) | 6 | 6 |
| VERIFY_N66CUBES_1118.md (VB) | 27 | 27 |
| VERIFY_N66CUBES_1118_ALL.md (VB, one pass over all cubes, 05:13) | 132 | 132 |

The four records are disjoint and their union is the 132 accepted cubes. **Every cube has the four checks; none is
missing.** No row fails, no row is stale, and no id is outside the accepted set. VN audited these records as records
only and did not re-run their steps 2–4.

## 3. Uniformity and soundness (`V/vn_check.py cnf` → `V/vn_cnf.json`; unit `esr-mainv-vn-cnf`, 2 min 28 s, 733 MB peak)

**F_c.** F_c = `W/p2/b14h2/it1/cert.cnf`:
- its recomputed SHA-256 is **`14f43bf4ac4306bc415298b88afd1ca77af022a00d7468fd9fce2dffe9e8cbf3`**, equal to the
  claim and to the F_c layout's `cnf_sha256`;
- its header is `p cnf 1647808 9436582`;
- it has 9,436,582 lines, each one complete clause.

cert.json and verify.json have no F_c-hash field, so VN established the base by byte comparison, on **all 132
cubes** rather than only 3:
- **cert.cnf = F_c with exactly the cube's unit clauses inserted after the fixed units `988541 0` and `988542 0`**, in
  the order of the cube field;
- the header's clause count is 9,436,582 + |cube|;
- every other byte is identical to F_c;
- the cert.cnf SHA-256 equals cert.json `full_cnf_sha256`.

132 of 132 pass. All 132 therefore carry the same F_c, the same 79 SB clauses of the 27 pairs, the same rows and the
same counter, and L = 14 and W = range(70) as in §1.

**trim.cnf ⊆ F_c ∪ units(c), on all 132.** Every one of the 18,699,830 trim.cnf clause lines is a verbatim F_c line
or one of that cube's own unit clauses (976 such lines). There are 0 other lines, and every trim header's clause count
equals its line count. A cake_lpr verdict on trim.cnf therefore refutes F_c ∧ c directly.

**Symmetry breaking (parent §6.7) applies unchanged.** The SB clauses are part of F_c, and the cubes only add unit
clauses on the state variables sel_s, which are the x_s of §6.7. Suppose some set of the class had at most 14 holes:
- §6.7 gives a set with at most 14 holes whose occupancy x satisfies LEX for the one fixed pair list;
- x, with the e_j set to their meaning, satisfies F_c, which is a subset of F_full (README §2);
- x restricted to the 14 split states lies in exactly one cube c (§1);
- so x satisfies F_c ∧ c ⊇ trim(c), contradicting cake_lpr.

No cube is dropped as the mirror of another: the cover in §1 is complete without any symmetry. All cubes use the same
pair list, as §2 of the cube README requires.

## 4. Spot checks: fresh cake_lpr (`V/run_cake.sh`; unit `esr-mainv-vn-cake`, 90 % CPU, MemoryMax 2700M, 08:23:05–08:24:00)

The trimmed LRAT was streamed `zstd -dc trim.lrat.zst | tee -p FIFO | sha256sum` and checked with
`~/.local/bin/cake_lpr --CML_HEAP_SIZE=2000 trim.cnf FIFO`. The second cube was drawn at random with
`shuf --random-source=/dev/urandom` (recorded in `V/random_pick.txt`).

| cube | stdout | trim.cnf SHA-256 (= cert.json) | LRAT stream SHA-256 (= cert.json) | LRAT bytes | wall / max RSS |
|---|---|---|---|---|---|
| `hooooo` (largest proof) | exactly `s VERIFIED UNSAT`, exit 0 | `f507ed18861f84dfcee0f67792798292966c6454b3ca25a3572abf135c9051d6` yes | `f984be8c75833c94da688527741838a96e6fc1d8a9dbd397861e9107156820a6` yes | 2,014,536,363 | 50.6 s / 2,053,508 kB |
| `oooooo_40o_52h_46o_44h` (random) | exactly `s VERIFIED UNSAT`, exit 0 | `76d527e6d1631b8517f56b96b3135081b711ed1195827df314e94066e58de889` yes | `07d01b2a86854cd947996ce6d87ad3385d243d8f0c33c566ec748810de80a798` yes | 198,410,204 | 4.5 s / 2,051,444 kB |

Outputs are in `V/cake/`. Peak RSS was 76 % of MemoryMax.

## 5. Controls (`V/vn_controls.py` → `V/vn_controls.json`)

Every tampering below was caught:
- dropping one cube leaves 256 = 2^(14−6) assignments uncovered;
- duplicating it covers 256 assignments twice;
- an untouched copy of `hhhhhh` is accepted;
- an extra `s VERIFIED SAT` line in cake.out, one added trim.cnf line, a flipped cube literal (caught three ways), a
  wrong directory name, a dropped SB pair and verify ALL_OK = false are each rejected;
- one literal's sign flipped in a trim clause, or a foreign state unit added, gives trim_other = 1 and not ok.

## 6. Code (SHA-256)

| file | SHA-256 |
|---|---|
| `V/vn_check.py` | `62697b4e8308dc6877b9068a546c03463f99adcc066edbbf1ed4f0d953eba901` |
| `V/vn_controls.py` | `26c83b5a49836378f9e87b7a9a39bba2eadc64d3264daaea0fbdb1d7b95d3cc6` |
| `V/run_cake.sh` | `4bc7b35a7cf0b18bc4b7d5ff8ff496ea8fdad809293a78e40493b9241ec058fc` |

Python is `~/research/data/six10-linux-20261105/venv.disk/bin/python -I`.

## 7. Not checked by VN

- **Fresh cake_lpr on the other 130 cubes.** Their evidence is the driver's cake.out together with the fresh runs that
  U1 and VB recorded (audited in §2 as records). VN also did not hash the LRAT stream of those 130 cubes.
- **The content of F_c.** VN did not regenerate F_c or classify its clauses, so F_c ⊆ F_full rests on the critic's
  audit (cube README §2), p2_verify ALL_OK and U1/VB step 4.
- **The rows and their justification** (rows_1832, template_cert66).
- **The model:** the 70-state catalog, the hole-to-point bound N66 ≤ 69 − L, §6.3, and τ of §2.8.
- **The SB self-tests of §6.7.** VN read the proof but did not re-run them.
- **Lean.** None of this is Lean-checked.

Units: `esr-mainv-vn-cake` and `esr-mainv-vn-cnf` were the only units, run one after the other (90 % CPU each, never
together). Both had ended by 08:30:22. Nothing is committed.
