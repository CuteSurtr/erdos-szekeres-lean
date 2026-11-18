**Verdict: CONFIRMED** (claim `lb-e1-octdel65`, filed by track E1; verifier VS, 15 November 2026, 19:15-19:40 KST).
The labels hold as claimed: CERTIFIED computation (56/56 deletion CNFs, plus the SMQH CNF) with PROVED soundness and
order-type invariance (computer-assisted, unrefereed); the identity and order-type facts are EXACT. Every CNF was
rebuilt by VS's own encoder, written from the definitions, and every LRAT was re-checked by a fresh cake_lpr run.

# VERIFY_LOWERBOUND_E1_OCTDEL65: octagon-vertex deletions of the seven one-octagon 65-point sets

## Claim checked

T is one of `experiments/es8-lower-bound-search-2026-10-11/anneal/init_w8p_1..4.txt` and `init_v8p_1..3.txt`, and v is
one of its 8 octagon vertices. For every realization S′ of the labelled order type of T − v, and every p with S′ + p in
general position, S′ + p has a convex octagon through p. Corollary: no octagon-free 65-point set in general position
contains a 64-point subset with the order type of T − v, for any of the 65 points v of T. Side facts (EXACT): the 7
deletions of point 64 have witness(8)'s order type; the 49 other deletions form 8 order types, none of them witness(8)'s;
the SMQH crossed file without its comment line is byte-identical to the certified `c2_64points_k8_bb.txt`.

## Checks and results (all with VS's own code; exact integer arithmetic, `__int128` orientations)

| # | check | result |
|---|---|---|
| 1 | SHA-256 of the 7 repo files = `agl/sets8/` copies; 65 lines each; no three collinear points | 7/7 equal; general position holds |
| 2 | convex 8-subsets of each T (own backtracking enumerator: a set is convex iff each 4-subset is, 4-point test "no point in the triangle of the other three") | exactly **1** in each set: {0..6, 64} for `init_w8p_1..4` and `init_v8p_3`, {57..63, 64} for `init_v8p_1,2`. No convex 9-set, since a 9-gon would contain 9 octagons |
| 3 | T − v built by deleting line v (file order kept), compared with `agl/sets8/init_*_d<v>.txt` | 56/56 byte-identical; names equal `names_del8.txt` |
| 4 | **own encoder** `vs_oct cmp` (R2, AC, OCT families of ABSAT8_INDEPENDENT §3, written from the text, not from `l1enc.cpp`) vs each `cnf8/<name>.cnf.zst`, compared as sets of 3-literal clauses; header and counts checked | **57/57 EQUAL** (56 deletions + SMQH): no missing or extra clause, no duplicate, header `p cnf 2016 <count>` exact, no convex octagon in T − v. Example `init_w8p_1_d0`: R2 242,048 + AC 41,664 + OCT 144,247 = 427,959 clauses from 3,846,106 convex heptagons |
| 5 | SHA-256 of each decompressed CNF and LRAT vs `cert8/certify.jsonl` | 57/57 equal (20 distinct CNFs, 20 distinct LRATs) |
| 6 | filer's `cert8/<name>.cake.out`: lines matching `^s VERIFIED UNSAT$`; CaDiCaL logs | exactly 1 in 57/57; every log says `Version 2.1.3` and has one `s UNSATISFIABLE` |
| 7 | **fresh cake_lpr** (`~/.local/bin/cake_lpr --CML_HEAP_SIZE=200`) on each CNF + LRAT, in unit `esr-agv-vs-oct65` | exactly one `s VERIFIED UNSAT` line in **57/57**; peak RSS 208 MB |
| 8 | canonical order types (own code: minimum over hull vertices h, and over orientation for the reflection-closed form, of the sign string after labelling h → 0 and the rest by angle around h) | the 7 `*_d64` deletions, `w8.txt` and `v8_1..3.txt` share one class (witness(8)); the 49 other deletions fall into **8 classes** (sizes 7,7,7,7,7,7,6,1; `init_w8p_2_d6` is alone), none equal to witness(8)'s. The partition is the same with and without identifying mirror images |
| 9 | SMQH: `SYMEVEN/lit/smqh_crossed_k8_64points.txt` minus line 1 vs `pm1115/l1/sets/c2_64points_k8_bb.txt` and `lower8/probe1/absat/sets/c2_64points_k8_bb.txt` | byte-identical to both; its CNF and LRAT hashes equal the c2_64points_k8_bb row of ABSAT8_INDEPENDENT §5 (`e0688763…`, `8dc6438b…`) |

Extra (not in the claim): the four `init_w8p_*_d64` CNFs have SHA-256 `2d5768ff…`, the ABSAT8 `ot0000` CNF.

## Soundness (re-read)

ABSAT8_INDEPENDENT §3 was re-read: R2 (Cramer's rule on the angularly sorted, sign-normalized vectors), AC (barycentric
coordinates), OCT (visible edges of a convex heptagon form a cyclic interval; a violated chain clause makes Q + p a
convex octagon) and the order-type invariance (R2 with the same ε for S′; AC and OCT depend on orientation signs only)
are correct. The claim `absat8-l1-indep` covering this encoder is CONFIRMED. Mirror images are covered as well: reflect
the whole configuration S′ + p. For v off the octagon, T − v keeps the octagon, and convex position is an order-type
property, so the corollary holds for all 65 points.

## Controls (own)

- Enumerator: convex k-subset counts equal brute force on 12 random sets of 9-13 points, k = 4, 5, 6
  (`selftest_gons.py`, 0 mismatches).
- Canonical form: invariant under random relabelling plus integer affine maps with det 1; a reflected copy keeps only
  the reflection-closed key (`selftest_canon.py`, PASS).
- Semantic control of the clause families (`vs_canon ctrl`): in each of the 56 deletions, p = the real deleted vertex
  violates **no** R2 or AC clause, exactly one OCT clause, and lies on exactly one convex octagon (direct
  enumeration), 56/56 (`ctrl_deleted.out`). On 3 random p for `init_w8p_1_d0`: 0 R2/AC violations, and each p lies on
  1 to 1,816,431 convex octagons, consistent with its violated OCT clauses.

## Not checked

The filer's controls C1, C3, C4 and E8-1.2 (stacking order types) were not re-run. The record's statements beyond the
claim were not reviewed.

## Files (work directory `/home/jay/research/data/roadmap-20261115/pm1115/vs/lb-e1-octdel65/`)

| file | SHA-256 |
|---|---|
| `vs_oct.cpp` (encoder, enumerator, CNF comparison) | `1fac1364ad7c4f3f3c56e348a56e22cbf4fdd5e7cd15113c43645a46b18e97e8` |
| `vs_canon.cpp` (`vs_oct` plus canonical order types and the semantic control) | `5eb8f5bfdb15b6510f900b1b578226d6ad7b81a12a018bad6a8fd6560070336b` |
| `drive.sh` (hashes, line counts, encoder comparison, cake_lpr re-run) | `c94fa9c7023f6cbcf57b098eb19fb21fb2ad469d510d4b23b18b89ecb931fe97` |
| `results.tsv` (57 rows) | `94817ed05d1cad099f33173724d871eeeedb9724568939b350115e5051e24dfc` |
| `canon_keys.txt` | `66f744747c4259a60f320d2fe8705f3db55696c702ffbb06eaba2000fb8982d8` |
| `ctrl_deleted.out` | `689455f37acf1afff667f1df24abd73232f924169fbbbe326d31862461ff0631` |
| `cake/<name>.cake.out` | VS's 57 cake_lpr outputs |

Rerun: `g++ -O2 -o vs_oct vs_oct.cpp; bash drive.sh` (about 2.3 CPU-s per name). No git action and no e-mail. No
repository file other than this one was written. Nothing was deleted except VS's own decompressed copies.
