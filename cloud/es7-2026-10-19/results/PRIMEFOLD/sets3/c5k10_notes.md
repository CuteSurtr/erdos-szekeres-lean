# push3/c5k10: fivefold sets without a convex 10-gon (K = 10), 2026-11-03

Working notes of the fivefold k = 10 search (3 November 2026); paths are relative to that working directory.
Session 06:22-07:35 KST (well inside the 150-minute limit), at most 3 busy processes (largest: CaDiCaL, 0.3 GB).
Status words: proven / certified / computational evidence / conjecture / refuted (as in `$S/brief/COMMON.md`).

## 0. Headline

1. **Certified: a fivefold symmetric set of 176 points in general position with no 10 points in convex position**
   (35 nested regular pentagons plus the centre). File `cert/c5k10_176pts_1orbit35.pts`, SHA-256
   `32679bde346eaef30da5421dbe8058063308e13573796d5b0e14032c56c55d64`. It is a single-orbit rotated blow-up: a regular
   pentagon whose vertices carry rotated copies of one 35-point cluster, plus the centre. The cluster is the
   Erdos-Szekeres cup-cap set X(5,6) (longest cup 4, longest cap 5, C(7,3) = 35 points), flattened so that all its
   edge directions lie within 5 degrees of the direction 54 degrees from the ccw tangent (1.5 units of pi/5), towards
   the centre.
2. **Proven (hand proof that relies on Lemma 1 of `primefold/theory/PROOFS.md`, a written proof that has not been refereed):
   one orbit of generic tiny clusters (centre optional) has at most 35 points per cluster for (m, K) = (5, 10), so at
   most 176 points.** Item 1 attains it, so 35 is exactly the single-orbit maximum. **It does not allow 51:** a fivefold
   256-point set without a convex 10-gon (51 pentagons + centre, the size that would be extremal if ES(10) = 257)
   cannot be a single-orbit tiny-cluster blow-up. In that family it needs at least two base orbits with cluster
   sizes summing to 51.
3. **No multi-orbit design above 35 cluster points per sector was found** (computational evidence only). We ran flat-cluster,
   tree-cluster and general-cluster formula searches over two and three base orbits (one four-orbit start), about 1.5 CPU-hours in total.
   Every design with 36 or more cluster points per sector stalls at a positive cost; most stall at exactly one
   rotation class of excess-1 polygons. Section 4 explains the recurring obstructions with heuristic arguments; they
   are not impossibility proofs.
4. Best certified fivefold 10-gon-free size: **176** (a lower bound for the fivefold maximum). The extremal candidate
   256 is not reached. Structural reason, as far as established: the single-orbit cap 35 < 51 (proven, item 2), and
   additional orbits run into tight polygons of the other orbits (heuristic, section 4).

## 1. Claims

| id | statement | status | evidence |
|---|---|---|---|
| C1 | There is a 5-fold rotationally symmetric set of 176 points in general position with no 10 points in convex position (35 pentagon layers + centre); its largest convex subset has 9 points. | certified | `cert/c5k10_176pts_1orbit35.{pts,log,ot.gz,ranks.txt}`. Points exact in Z[zeta_5] (coefficients <= 1.0e40). (1) `primefold/theory/tools/orient.py` exact table (polynomial in 2cos(2pi/5) on a 2^-400 bracket): no collinear triple; (2) `src/tab_cyclo.py` with S1's `exact.Cyclo` (separate exact code): distinct, invariant under multiplication by zeta, rows are zeta-orbits, layers nested, no zero orientation, table **byte-identical** to (1); (3) `src/dpcheck` (copy of `PRIMEFOLD/check253/dpcheck.c`): lowest-vertex DP 9, leftmost-vertex DP 9, cup+cap DP 9, witnesses checked, 0 angular-order violations; (4) `src/mydp` (anchor-pair DP written here, uses no ranks): 9, and 0 convex 10-gons counted; (5) S1 `crosscheck_decimal.py`: all 893,200 sorted triples recomputed with 160-digit decimals, 0 mismatches, min abs det 1.5e61 vs error bound 4e-68. |
| C1' | A second realisation of the same construction (tree model, `src/realize_tree.py`, scale 1e60) also has largest convex subset 9 | exact computation (one table, one DP) | `runs/tree/t1v.pts`: orient.py table, `mydp` 9, 0 convex 10-gons |
| P1 | One orbit of tiny clusters, m = 5, K = 10, centre optional (base = regular pentagon, rotated copies of a cluster C, C generic in the sense of Lemma 1, eps small enough for formula (1)): no convex 10-gon implies |C| <= 35, so at most 176 points. | proven (hand proof, sec. 3; relies on Lemma 1, a written proof that has not been refereed) | sec. 3 |
| P1' | P1 is tight: 35 is attained (C1 is such a blow-up) | certified (C1) | C1; also the formula value 9 (sec. 2) |
| F1 | Formula level (Lemma 1): flat cluster types for a single orbit. Forward window in (1,2) units: allowed iff c <= 4 and c + d <= 9; in (2,2.5): iff c + d <= 8; mirror images for (2.5,4). | proven (case check of the 6 cyclic compositions of 5 and the 4 centre polygons, sec. 3) | sec. 3; `src/formula.py demo` |
| E1 | Two-orbit flat-cluster designs with total cluster size 36..41 (all (c,d) types with c + d <= 9; inner radius 0.3..0.97 and 0.03..0.35) | computational evidence only: none found; best residual cost 5 (one rotation class of excess 1) | `runs/fd_L2a.log`, `runs/fd_T2.log` |
| E2 | Three-orbit flat designs, total 36..37 | computational evidence only: best cost 5 | `runs/fd_L3a.log`, `runs/fd_T3.log` |
| E3 | General clusters (explicit points, `src/bu10`, Lemma 1 with longest-chain DP): repairs of the flat near-misses (35+1, 20+20 points) and random starts (18+18, ...) | computational evidence only: no improvement (5, 10, 577) | `runs/gd_*.log` |
| E4 | Hierarchical tree clusters (`src/treesearch`, exact eps -> 0 recursion): inner X(5,6) under 1-2 plain outer orbits or a 2-point outer cluster (180-186 points), outer (3,6)/(4,5)/(4,4) with deep inner orbits (181-206 points), three orbits | computational evidence only: none found (sec. 4) | `runs/tree/td_*.log` |
| SAT1 | SAT relaxation of P1 (`sat/clsat_full.py 5 10 36`, the `push2/c6c5` single-orbit encoder, 26.7 MB CNF, sha256 `478d81ce...`) | inconclusive: CaDiCaL 3.0.1 returned UNKNOWN at the 600 s limit (`sat/f_m5k10n36.out`); the proof file was deleted. P1 rests on the hand proof only | `sat/` |
| H1 | Heuristic obstruction (sec. 4): (a) an orbit whose cluster has cup + cap = 9 sits inside every larger orbit in a "72-degree" position; (b) the 35-point outer orbit is saturated (its triangles of gap type (1,2,2), the triangle O a_0 a_2 and its adjacent 2-gons all sum to 9) | conjecture (heuristic argument + all searches) | sec. 4 |

Not claimed: any upper bound for multi-orbit blow-ups or for general fivefold sets; that 176 is the fivefold maximum;
novelty. In the sources inspected (`PRIMEFOLD/README.md`, `ES8SYM/README.md` incl. sets2/sets3,
`push2/c6c5/README.md`, `primefold/theory/README.md`) no fivefold set without a convex 10-gon is recorded; the only
symmetric k = 10 record there is the 9-fold 253-point set (`PRIMEFOLD/sets/k10/rule_p9_253pts.pts`). This is not a
novelty claim: no literature search was done in this session.

## 2. Construction and certification of C1

- `src/esflat.py`: X(a,b) by the Erdos-Szekeres recursion X(a,b) = X(a-1,b) U (X(a,b-1) shifted so that every
  connecting slope exceeds every internal slope), exact rationals; X(5,6): 35 points, longest cup 4, longest cap 5
  (checked by an exact DP). Flattening v -> delta*v with delta = tan(5 deg)/maxslope = 3.56e-7, rotation (rational
  approximation, a linear map of the cluster) so that the u axis points to local angle 144 deg (x = radial outward,
  y = ccw tangent), i.e. t = (144 - 90)/36 = 1.5 units of pi/5 from the ccw tangent.
- `src/make176.py`: base point v_0 = 1 (so the local frame is the global frame there), cluster scale eps = 1e-5,
  z = 1 + eps (x + i y), S*z rounded to w0 + w1*zeta at S = 1e40 (`src/realize5.py`; 140-digit Decimal values of
  cos 72, sin 72); orbits = exact cyclic shifts; centre 0. Rows sorted outermost layer first.
- Formula level (Lemma 1): `src/formula.py demo` and `src/bu10 eval runs/f1.cfg` (explicit 35-point cluster) both give
  value 9 (0 convex 10-subsets in the eps -> 0 limit, angular margin 0.227 rad). The certificate does not depend on
  the formula: it checks the realised point set directly.
- `src/certify5.sh FILE.pts NAME 10` runs the five checks of C1 and writes `cert/NAME.log` (24 s for 176 points).

## 3. Proofs

**Setting** (as in `push2/c6c5/README.md` sec. 3). Base = regular pentagon {v_j}, cluster at v_j = R^j(C) (C in the
frame of v_0), S = U_j (v_j + eps R^j C) (+ centre O), eps small, C generic in the sense of Lemma 1. A vertex of a
convex base polygon with gaps a (before) and b (after) (units 2pi/5) has turning arc (-a, b) in units of pi/5
measured from the ccw tangent; F(a,b) := f_C((-a, b)) = longest ccw chain of C with edge directions in that arc.
Lemma 1: mc(S) = max(mc(C), max over convex base polygons of the sum of the vertex weights) (the centre has weight 1).

**P1.** (i) The full pentagon gives 5 F(1,1) <= 9, so F(1,1) = 1: no segment of C has a direction within pi/5 of
the tangent. Sort C by the radial coordinate; every segment, oriented inwards, has direction t in (1, 4).
(ii) The 2-gon {v_0, v_1} has arcs (-4, 1) at v_0 and (-1, 4) at v_1, so F(4,1) + F(1,4) <= 9. The arc (-1,4)
contains all inward directions and no outward one (outward = inward - 5, in (-4,-1)), so F(1,4) = the longest chain
whose edges all point inwards and turn left, i.e. the longest cup g in the radial order; likewise F(4,1) = the longest
cap h. (iii) Erdos-Szekeres cups-caps theorem: |C| <= C(g+h-2, g-1) <= max_{g+h=9} C(7, g-1) = C(7,3) = 35.
Hence at most 5*35 + 1 = 176 points. The same argument with 9 replaced by K-1 is C4 of `push2/c6c5`
(m = 5, K = 8: 10 points).

**F1 (flat clusters, single orbit).** A flat cluster with forward window W (narrow) and backward window W - 5 has
F(a,b) = c if W is inside (-a,b), d if W - 5 is, 1 otherwise. The arcs of the six cyclic compositions of 5 are
(1,1,1,1,1): (-1,1) x5; (1,1,1,2): (-2,1),(-1,1),(-1,1),(-1,2); (1,1,3): (-3,1),(-1,1),(-1,3); (1,2,2): (-2,1),
(-1,2),(-2,2); (1,4): (-4,1),(-1,4); (2,3): (-3,2),(-2,3); with the centre: {O,v0}: (-2.5,2.5); {O,v0,v1}: (-2.5,1),
(-1,2.5); {O,v0,v2}: (-2.5,2),(-2,2.5); {O,v0,v1,v2}: (-2.5,1),(-1,1),(-1,2.5) (+1 for O each). For W in (1,2):
(1,2,2) gives 1 + 2c <= 9 and (2,3) gives 2c <= 9, so c <= 4, and (1,4) gives c + d <= 9; all other polygons are
then <= 9 (largest: 3 + c, 2 + c, 1 + 2c). So (c,d) = (4,5) works: 35 points. For W in (2,2.5): (1,1,3) gives
c + d + 1 <= 9. `src/formula.py` and `src/flatsearch` confirm these values numerically.

## 4. Searches and the recurring obstruction (computational evidence and heuristics only)

All searches evaluate Lemma 1 in the eps -> 0 limit; cost = sum over convex base subsets (|B'| >= 2) of the excess
over 9. A cost of 5 means one rotation class of polygons with excess 1. Nothing in this section is a claim about
point sets; a failed search is not impossibility.

| family (tool) | designs | runs | best residual |
|---|---|---|---|
| flat clusters, 2 orbits, inner radius 0.3..0.97 (`flatsearch`, `fdriver.py L2a`) | all (c,d) pairs with c + d <= 9, total size 36..42 (66 combinations) | 2 x 6 s each | 5 (every combination of size 36..41 tried) |
| flat, 3 orbits (`L3a`) | 100 combinations of total size 36..37 | 6 s each | 5 |
| flat, small inner radius 0.03..0.35 (`T2`, `T3`) | 11 selected two- and three-orbit combinations | 15 s each | 5 |
| general clusters, explicit points (`bu10`, `gdriver.py`) | repairs of flat near-misses 35+1, 20+20, 15+21, 1+35; random 18+18 | 90-100 s each | 5, 10, 5, 5; random 577 |
| tree clusters (`treesearch`, `tdrive.sh`) | inner X(5,6) under 1-2 plain orbits or a 2-point outer cluster (180-186 points); outer (3,6) + inner (3,5) / (4,4) (181, 206); (4,4)+(4,4) (201); three orbits (3,6)+(3,4)+(3,3) (186) and others | ~60 runs of 45-120 s | 5 (186-point three-orbit design J6, inner-X(5,6) designs), 10 (181, 201), 15 (206) |
| tree clusters, last batch | outer (3,5) + (3,5) + (3,3) (181), outer (3,5) + (3,5) + (3,4) (201), outer (3,5) + (4,4) + (3,4) (226), two 256-point-sized designs (3,6)+(4,4)+(3,4) and (4,5)+(3,4)+(3,3); J6 with radii fixed deeper (0.28, 0.09) | 2 x 80-90 s each; 3 x 60 s | 5 (181), 30 (201), 70 (226), 100 and 160 (256), 20 (J6 deep) |

**One more layer on the 176 design** (flat model, `src/addlayer_scan.sh`): a plain pentagon layer (1-point orbit) at
any of 32 radii in 0.02..5 times 72 phases (2,304 positions, with and without the centre). Minimum cost 5 in both
cases (`runs/addlayer_{1,0}.log`). So within this model the design cannot grow by one layer (computational evidence).

**Bug note.** Before 07:12 `flatsearch` charged a spurious "window cut" to one-point clusters. They have no edges, but
the code still assigned them a dummy window. Fixed, with the same version in `src/`. Re-runs of all plain-layer
two-orbit combinations with the fixed binary (`runs/fd_F11a.log`, `runs/fd_F11b.log`, both radius ranges) give the
same best cost 5, and the residual polygons printed earlier were genuine excesses, not cuts.

Calibration: the flat model reproduces the single-orbit optimum in < 0.1 s. In 5 s runs it did **not** find the
known K = 8 two-orbit solution (56 points, `push2/c6c5` C1), whose clusters are not flat. So stalls in the flat model
are weak evidence. The tree model is exact in the eps -> 0 limit for hierarchical clusters; ES sets are such trees,
and `src/realize_tree.py` realises tree designs exactly (C1' checks one realisation). Its annealer is crude: a sanity
run from a badly rotated single-orbit tree reached cost 16, not 0.

**Recurring residual polygons** (printed by `flatsearch SPEC 1 0` / `treesearch SPEC 1 0`):
1. *Inner cluster with cup + cap = 9* (for example X(5,6) on an inner orbit): the triangle {b_k, b_{k+1}, a_j} formed by an
   adjacent inner 2-gon and one point of any larger orbit sums to 4 + 5 + 1 = 10. Heuristic reason (flat clusters,
   written argument, not checked by a second person): the region of positions a for which both windows survive
   in that triangle is bounded by a line through b_k and its image under the rotation by 72 degrees through b_{k+1}.
   So on every circle about O it is an arc of polar width 72 degrees minus a term proportional to the window width.
   A 5-point orbit therefore has a point in it unless its phase lies in a gap of about the window width. For
   non-flat clusters a gap needs every maximum cap to use an edge steeper than the shallowest edge of every maximum cup.
   That fails for the Erdos-Szekeres tree X(5,6): one recursion step down, X(3,6) has longest cup 2, so every single
   edge is a maximum cup.
2. *Outer cluster X(5,6) at window 1.5 units*: saturated. Its triangles of gap type (1,2,2) and {O, a_0, a_2} sum to
   1 + 4 + 4 = 9, and its 2-gons {a_j, a_{j+2}} sum to 8. Any inner hull vertex near them adds 1: for example the
   quadrilaterals {a_j, a_{j+2}, x, y} of two inner points (4 + 4 + 1 + 1). Inner points near the outer edges create
   {a_j, a_{j+1}, x} (5 + 4 + 1). In the limit where all inner orbits shrink to a tiny fivefold configuration D at
   the centre (short argument, formula level), the triangle {O, a_0, a_2} with weights 1 + 4 + 4 forces D to have
   no 2-chain with directions in the five 36-degree turning arcs at O (rotations of each other by 72 degrees). But
   any segment has one of its two directions in one of these arcs. So D is the centre alone.
3. *Outer (3,6) with deep inner orbits* (the 186-point three-orbit design J6, cost 5): the outer adjacent 2-gon is
   tight (6 + 3) and a middle-orbit point lies in its edge triangle (6 + 3 + 1).

These suggest (conjecture H1) that fivefold tiny-cluster blow-ups gain little or nothing from extra orbits at K = 10.
In particular they do not suggest any route to 51 cluster points per sector. This is weaker than a proof: multi-orbit
designs with non-flat, non-tree clusters were explored only by the crude general-cluster annealer.

## 5. Files

- `cert/c5k10_176pts_1orbit35.pts` (the certified set: 176 rows of 5 integers w_0..w_4, point = sum w_j zeta^j,
  zeta = e^{2 pi i/5}; rows 5l..5l+4 = layer l, outermost first; centre last), `.log` (all checks), `.ot.gz` (exact
  orientation table, format b"OT1 n\n" + n^3 signed bytes), `.ranks.txt` (exact (Im,Re) and (Re,Im) ranks).
- `src/esflat.py` (ES sets, flattening), `src/realize5.py` (exact rounding into Z[zeta_5]), `src/make176.py` (C1),
  `src/certify5.sh` (pipeline), `src/tab_cyclo.py` (second exact table + structure + ranks), `src/mydp.c` (anchor-pair
  DP), `src/dpcheck_check253.c` (copy of `PRIMEFOLD/check253/dpcheck.c`), `src/ot2txt.py`.
- Search tools: `src/formula.py` (Lemma 1, Python), `src/flatsearch.c` + `src/fdriver.py` (flat clusters),
  `src/bu10.c` (copy of `push2/c6c5/bu.c` with K <= 12, clusters <= 48 points, fine moves) + `src/gdriver.py` +
  `src/spec2cfg.py`, `src/treesearch.c` + `src/tdrive.sh` (tree clusters), `src/realize_tree.py`.
- Logs: `runs/fd_*.log`, `runs/gd_*.log`, `runs/tree/td_*.log`; best configurations `runs/fd_*_r*.spec`,
  `runs/gd_*_best.cfg`, `runs/tree/*.best`.
- `SHA256SUMS.txt`.

Reproduce C1: `python3 -I src/make176.py X.pts 5 40 && src/certify5.sh X.pts NAME 10` (C programs compiled with
`cc -O2 -isysroot /Library/Developer/CommandLineTools/SDKs/MacOSX26.sdk`).
