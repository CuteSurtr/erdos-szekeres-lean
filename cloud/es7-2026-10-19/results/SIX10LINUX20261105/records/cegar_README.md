# cegar/: the sixfold 10-layer cube CEGAR rebuilt on Linux (5 Nov 2026, night)

Question: is the largest 6-fold octagon-free set in general position 54 or 60 points? 60 points = 10 nested hexagons.
This directory rebuilds the SIX10CEGAR lanes (results/SIX10CEGAR) on this machine without the off-machine base formula
(current.cnf, 9.2M clauses), replacing the missing GP / determinant-identity blocks by lazy refinement, and runs one
lane per phase-order cube until 04:40 KST.

DRAFT - final numbers are in the "Results" section at the end (filled in at hand-off).

## Rigor labels

* **exact computation**: an exact checker (integer / rational arithmetic, stdlib Python) accepted the object.
* **written argument**: a proof sketch in this README or in the tool docstrings (not refereed).
* **evidence only**: numerical results, rates, solver behaviour.

## The formula (all clause files are DIMACS lines over the encoder's variables)

| part | file | clauses | status |
|---|---|---|---|
| encoder A | `base/encA_6_8_10.cnf` = `python3 C7UPPER/gen.py 6 8 10` | 1,609,785 (58,626 vars) | written proof (gen.py docstring); count matches |
| SIX10CEGAR re-verified cuts | `base/cuts_verified.clauses` (copy) | 10,608 | exact computation (SIX10CEGAR audit) |
| model0090 face cut | `base/cut_model0090_sparse.clauses` (copy) | 1 | exact computation (SIX10REFINE) |
| lazy GP clauses | `shared/gp.clauses` + `shared/gp_relations.tsv` | grows | exact (re-checked by `tools/check_gp_file.py`) + GP identity |
| new cuts | `shared/cuts.clauses` + `shared/cuts_provenance.tsv` | grows | each accepted by an exact checker before it was appended |
| inbox | `inbox/*.clauses` (+ checker logs) | grows | other agents' certified cuts; `linfam_*` = my lin image families |
| **assumptions** | `shared/blocked.clauses` + `shared/blocked_models.tsv` | grows | hard models; NEVER mixed with cuts; any UNSAT using them is conditional |

Cubes (`cubes.txt`, identical to SIX10CEGAR/tools/cubes.txt): Y(1,2) = 5711 plus the 12 consistent phase orders of
layers 1-4, passed as solver assumptions.

SHA-256: encA `ff10dafb...79ed`, cuts_verified `15af5987...6cad` (= SIX10CEGAR), cut_model0090 `8acfca54...bfbf4`,
gp_table.npy lits `fae3b210...a6b3` (see `base/gp_table.npy.json`).

## Lazy Grassmann-Pluecker refinement (replaces the missing GP blocks)

`tools/gp.py`: all 3-term GP relations [abc][ade] - [abd][ace] + [abe][acd] = 0, rotation-reduced to pivot a = vertex 0
of its layer: 10 * C(59,4) = 4,551,260 relations, stored as int16 bracket literals (`base/gp_table.npy`, 55 MB). A model
violates a relation iff the three terms have the same strict sign (impossible in general position: written argument in
gp.py). For each violated relation (up to 4000 per round) all 16 forbidden sign patterns become clauses (tautologies
dropped). Scan time 0.03 s per model.

**Validation (exact computation, `tools/validate_gp.py`, `validation/gp_60/validate_gp.json`)** on 60 random REAL sixfold
configurations with exact integer oblique seeds (uniform, geometric multi-scale 10^7..10^2.5, and random-scale):
* general position checked exactly; E.o literal semantics checked for all 205,320 ordered triples of each
  configuration (12,319,200 checks);
* GP table reports 0 violated relations on every real configuration;
* 180 mutants (1, 3 or 20 flipped orbit variables) give 2,279,386 violated relations; 563,312 generated clauses were
  tested against the real configuration: all satisfied; every model clause is falsified by its mutant;
* cross-check with the independent C checker `ROTREFINE20261104/m6_gpcheck.c` on the full 60^3 table: anchored count
  = 6 x rotation-reduced count (21,276 = 6 x 3,546 and 35,388 = 6 x 5,898).
* The GP clause file is re-checked by an independent stdlib checker (`tools/check_gp_file.py`, recomputes the brackets
  with E.o; negative test: one corrupted literal is caught).

Side finding (exact computation): 18 of the 101 old hard models violate full GP (all 15 of c11000 with 324 violated
relations each, 3 of the 8 of c10000 with 112), consistent with `inbox/altcert_gp.*` of another agent; the other 83
satisfy all 4,551,260 relations (`validation/hard_models_gp.json`).

## Lane pipeline (`tools/worker.py`)

Per cube: CaDiCaL 3.0 (PySAT `cadical300`), incremental, 1 thread, budget 2M conflicts per call. Each round: sync all
shared/inbox clause files (byte offsets, complete lines only, malformed lines rejected), solve under the cube, keep the
5,746 encoding variables of the model, then:
0. **GP** scan; violations -> GP clauses, next round (no model file).
1a. **lin2** (added 00:28): as lin below, but the LP may also use the normal-form rows (radius D_aa - D_bb, a<b;
   phase_plus/minus D_ij +- E_ij; phase_sign s*E_ij, whose Y literal goes into the clause when i >= 1) and minimises
   (reweighted, 3 passes) the weight on literal-carrying rows. Witness in facial-cert-v1 format, checked by
   `facial_snap/checker/check_facial.py` (the weighted sum is the zero form, which is NSD). Clauses 13-36 literals where
   lin gives 40-80; on two test models lin2 gave UNIT clauses (e.g. orient(z_0, z_1, -z_1) = 2 det(z_0, z_1) > 0 since
   0 = theta_0 < theta_1 < 60 deg: a fact encoder A's angular rules miss because O lies on the segment).
1. **lin** (fallback): exact nonnegative linear dependency of the signed orientation forms in the rotation-averaged lift (HiGHS LP
   picks a vertex = circuit; weights recomputed in Fractions by ROTREFINE `math_linear.exact_weights`); checker
   `tools/check_lin.py` (stdlib; sum of weighted signed (2/sqrt3)-orientation polynomials in the 20 oblique seed
   coordinates is the ZERO polynomial; model and triple bindings).
1b. **facial** (added 00:22): facial-reduction NSD certificate, `--minimize 15` then without minimization (snapshot of
   the facial agent's `certify.py` in `tools/facial_snap/`, one search-side bug fix for empty kernels, SHA256SUMS kept);
   checker `facial_snap/checker/check_facial.py` (stdlib, complete exact PSD test by symmetric elimination, no kernel
   basis). Records may include radius rows D_aa - D_bb (radii decrease), phase_plus/minus rows D_ij +- E_ij (phases
   within 60 degrees) and phase_sign rows; a phase_sign row on a pair (i,j), i >= 1, puts its Y literal into the clause.
2. **face** (SIX10REFINE model0090 face; `check_cert.py`), 3. **def** (`sdp_ext.py`; `check_def.py`), 4. **faceg** (face
   read from the lift; `check_cert_g.py`), 5. **subface** (layer subsets, 900 s cap), 6. **def-drop** (600 s budget),
   7. **minimize** face cuts (re-checked by `check_cert_g.py`).
8. Nothing works -> the model's 5,710 triple signs are **blocked as an assumption** (`shared/blocked.clauses`), with
   its distance to the 101 old hard models logged.

Worker versions (all kept in `tools/`): v1 `worker_v1.py` (00:12-00:22: GP, lin, old chain), v2 `worker_v2.py` (+facial,
00:22-00:28), v3 `worker_v3.py` (+lin2, 00:28-00:38), v4 `worker.py` (from 00:38: subface capped at 400 s and def-drop at
240 s, since 93% of the old run's subface successes came from the first three layer subsets; each child runs in its
own session and its whole subtree is killed on timeout or when the lane gets SIGTERM). Lanes were restarted by killing
their process groups; the supervisor restarted them within 30 s (logged in `logs/supervisor.log`). A restart loses at
most the model in progress (it comes back as a SAT model).

Blocked models are re-attempted in the background by `tools/resolver.py` (1 core): first it checks whether a certified
clause (cuts or inbox) already falsifies the model, else uncapped subface + all 55 one/two-layer drops; success ->
cut with method `*-offline` and a line in `shared/resolved_blocked.tsv`. (The facial agent also picks up blocked models
from `shared/blocked_models.tsv` on its own and drops certified clauses into the inbox.)

A cut is appended only after its checker exits 0 (checker output kept next to the witness: `.../check.out`) and only if
it falsifies the model. Provenance line per cut: time, cube, generation, round, model hash, method, length, witness
file, model file, checker log. Round ids are unique (`runs/<cube>/g<epoch>_<pid>/r<round>/`); nothing is overwritten.

**Why the cuts are sound (written argument).** lin: a realization makes every signed record strictly positive, so the
positive combination is > 0, but it is the zero polynomial. NSD certificates (face/def/faceg/subface/facial): same with
"<= 0 everywhere". Both are statements about all seed vectors z in R^20 (layers not used are free), so they hold for every
configuration with the sixfold rotation; facial rows other than triples are valid for the encoding's normal form
(theta_0 = 0, theta_i in (0,60), radii strictly decreasing), which every SAT model of encoder A represents.

## Image families of lin cuts (`tools/lin_family.py`, published through the inbox)

A zero polynomial stays zero under any substitution of seeds: for each lin cut with <= 16 literals, its images under
all order-preserving layer injections, with both global signs (-sum = 0 too), are generated; the batch is published to
`inbox/linfam_NNNN.clauses` only after `tools/check_lin_family.py` (stdlib, independent) re-verifies every image
(binding, positive integer weights, zero polynomial, clause = negated signs).

From 00:30 the expander also takes lin2 cuts (<= 16 literals): images under all order-preserving layer injections
(no sign negation: normal-form rows have a fixed sign; a phase_sign row moved off layer 0 gains its Y literal; an image
needing theta_j < theta_0 is dropped), batches `inbox/linfam2_NNNN.*`, checked by `tools/check_nf_family.py`.

## Normal-form forced orientations (`tools/nf_family.py`, `tools/nf_pairs.py`; published as `inbox/nfunits.*`, `inbox/nfpairs.*`)

For every orbit triple t and sign s, an LP over the normal-form rows decides whether s*(2/sqrt3)[t] + sum mu_r row_r = 0
is possible; if so, s*[t] > 0 is impossible in normal form, giving a clause (-s*var_t) OR (Y conditions). Result: 2,622
clauses (582 units, 1,368 binary, 672 of length 4); 198 of the units are not unit clauses of encoder A. Exact check:
`tools/check_nf_family.py` (stdlib, OBLIQUE coordinates, zero polynomial, row-validity rules, clause = required negated
literals; negative test with one altered weight is caught) on all 2,622, and the facial checker (different coordinates)
on 40 random ones via synthetic models: all accepted. `nf_pairs.py` does the same for pairs of triples on <= 2 layers.

## Inbox (`inbox/README.txt`)

DIMACS clause lines over vars 1..5746 ending with 0; loaded each round by every lane, only when a checker log
(`NAME.log`, `.checker.log`, `.check.log` or `.clauses.log`) exists; files may be appended to; a file that shrinks
is re-read from the start. Must be valid for every normalized configuration (phase literals included when used).

## Supervisor, deadline, monitoring

* `tools/supervisor2.sh` (pid in `pids/supervisor.pid`): restarts dead lanes (max 50 restarts per cube), starts
  `certify_cube.sh` on an UNSAT event, writes `STATUS` every ~30 s and a light snapshot every 30 min, stops all lanes at
  04:38 KST (deadline file `deadline` = 04:40 KST epoch; lanes get deadline-150 s), writes the final full snapshot and exits.
* `tools/lin_family.py` (pid `pids/aux_linfam.pid`) stops itself at 04:37:30.
* `tools/certify_cube.sh CUBE`: rebuilds the exact formula the lane had loaded (its `UNSAT_manifest.json`: base files +
  byte prefixes of gp/cuts/inbox files), EXCLUDING `blocked.clauses`, adds the cube units, runs plain
  `cadical --lrat`, then `lrat-check`; result in `cert/CUBE/record.txt` (SAT there = the lane's UNSAT was conditional on
  blocked models). Build path tested on a fake manifest (`validation/certtest`).
* `tools/status.py` (STATUS), `tools/rates.py` (per-bin rates -> `logs/rates.json`), `tools/clusters.py` (blocked-model
  clusters -> `logs/clusters.json`), `tools/snapshot.py TAG [full]` (state for resuming -> `state/`),
  `tools/resolve_blocked.py` (offline facial attempt on blocked models; success -> cut with method `facial-offline`,
  listed in `shared/resolved_blocked.tsv`; blocked.clauses stays append-only).

## Resume

`state/<latest>/` holds copies of every shared clause file (complete lines), provenance tables, `cubes.txt`,
`MANIFEST.json` (SHA-256) and `RESUME.md`; the final one also holds `formula_certified.cnf` (base + all certified clause
files, no blocked models, no cube units).

## Key finding: the 101 old hard models are excluded by elementary exact clauses

(exact computation + written argument; `validation/old_hard_models_nf_gp.json`)
* **90 of the 101** blocked hard models of SIX10CEGAR violate a normal-form forced-orientation clause of `nfunits` /
  `nfpairs`, and in all 90 the violated clause is about a triple (p, -p, q) that contains an ANTIPODAL pair of one
  layer. Written argument: orient(p, -p, q) = 2 det(p, q); with p = R^k z_i, q = R^l z_j, theta's in [0, 60) deg,
  the sign is sign sin(theta_j - theta_i + 60(l - k) deg), which is fixed for l - k = 1, 2, 4, 5 (mod 6) and equals the
  phase order Y(i,j) (or its negation) for l - k = 0, 3. Encoder A's angular rules cover only "O inside the triangle"
  and "open half-plane" triples, so these ~340 facts (198 units, 144 binary clauses with a Y literal) are missing from
  the base CNF, and the old pipeline could not see them because it ran the SDP without phase rows (`--no-phase`).
* **the other 11** (all in c11000) violate a 3-term GP relation (324 violated relations each).
* So none of the old "hard cores" was a genuine degree-2 obstruction problem; the frontier they suggested was an
  artifact. (The facial agent's certificates, which use phase rows, are consistent with this.)
* Sanity test (evidence): 0 violations of all 2.07M certified clauses (all files, incl. other agents' inbox) on random
  real normalized configurations (`tools/validate_clauses.py`); the negated nf units are violated by every
  configuration (negative control).

## Files

* `base/`: `encA_6_8_10.cnf` (+ `.json` metadata, `gen.log`), `cuts_verified.clauses`, `cut_model0090_sparse.clauses`,
  `gp_table.npy` (+ `_pts.npy`, `.json`).
* `tools/`: `worker.py` (lane, v4; `worker_v1..v3.py` earlier versions), `worker_orig.py` / `supervisor_orig.sh`
  (SIX10CEGAR originals), `supervisor2.sh` (running supervisor; `supervisor.sh` = first version, replaced at 00:14),
  `gp.py`, `validate_gp.py`, `check_gp_file.py`, `lin_cert.py`, `check_lin.py`, `lin2_cert.py`, `lin_family.py`,
  `check_lin_family.py`, `check_nf_family.py`, `check_nsd_family.py`, `nf_family.py`, `nf_pairs.py`,
  `validate_clauses.py`, `resolver.py`, `resolve_blocked.py`, `certify_cube.sh`, `status.py`, `rates.py`, `summary.py`,
  `clusters.py`, `snapshot.py`, `audit.py`, `realize_opt.py` (path-fixed copy), the SIX10CEGAR / SIX10REFINE
  certificate tools (`sdp_ext.py`, `face_*.py`, `facegen*.py`, `minimize.py`, `subface.py` (paths fixed),
  `check_cert.py`, `check_cert_g.py`, `check_def.py`, `spec_trueW.json`), `facial_snap/` (facial agent's tool
  snapshot + SHA256SUMS + note of the one patch), `cubes.txt`.
* `shared/`: `gp.clauses`, `gp_relations.tsv`, `cuts.clauses`, `cuts_provenance.tsv`, `blocked.clauses`,
  `blocked_models.tsv`, `resolved_blocked.tsv`, `events.txt`, `gp.lock`.
* `inbox/`: shared extra-cut inbox (README.txt; my files: `nfunits.*`, `nfpairs.*`, `linfam_*`, `linfam2_*`).
* `runs/<cube>/g<epoch>_<pid>/r<round>/`: model.json + every witness, checker output, SDP lift of that round.
* `logs/`: per-lane logs, supervisor, lin_family, resolver, `rates.json`, `clusters.json`, `audit.json`.
* `validation/`: GP validation (`gp_60/`), GP file re-check, certify path test, old hard models vs nf/GP,
  clause validation logs, lin vs facial comparisons, realization probe of the c01011 hard model.
* `nf/`: normal-form families (witness jsonl, clauses, checker logs).  `linfam/`: expander state.
* `state/`: snapshots (periodic every 30 min, final full one at the deadline).  `cert/`: UNSAT certification runs.
* `STATUS` (live), `deadline` (04:40 KST epoch), `pids/` (supervisor, lanes, aux jobs).
