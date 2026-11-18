# BAEK973: the demand-7 lemma for row 973 (Baek block), 15 Nov 2026

Stage record written 05:45-05:59 KST from the outputs of the formulation agent (`baek973`, 05:01-05:40) and the
refutation agent (`baek973-refute`). Work files are in `/home/jay/research/data/roadmap-20261115/baek973/` and
`.../baek973-refute/`. **Nothing here is CERTIFIED.** Labels follow the house table: PROVED / CERTIFIED / EXACT TREE
/ COMPUTED / HEURISTIC; "EXACT" below means an exact integer recount.

## 1. Headline

- **Lemma 973' (demand 7) is OPEN.** It was neither proved nor refuted.
- **The planned certificate route is obstructed (COMPUTED; one SAT model re-checked clause by clause).**
  - In the pinned coupled encoder, 20 of the 42 witness F6 patterns leave a 22-owner support `F6 \ H` that is
    **SAT**. So do 17 of 65 seeded random allowed patterns.
  - The coupled CNF is monotone under sub-supports. So no coupled row with support inside F6 can kill those
    patterns, and `h(F6) >= 7` cannot be derived from F6-only rows of this encoder.
- **Rows 1165 and 2315 behave the same way (COMPUTED).** Many SAT supports were found there too. "All nine Baek rows
  at demand 7" is therefore out of reach of F-only coupled rows of this encoder.
- **Refutation search: not refuted** (COMPUTED, own exact-integer code; confidence 0.6). No real residual point set
  in the project's records has more than one owner in F6.
- **What demand 7 would buy (EXACT arithmetic).**
  - Row 973 alone gives only `h(F) >= 19`, which removes nothing new.
  - All nine rows at 7 give `h(F) >= 21`. Only slice (21,14) of budget 35 would then remain, and closing it would
    give **ES(8) <= 307**. That is a hypothetical chain: nothing toward it is in hand.

## 2. Statement

Let `source-2650.json.gz` be `/home/jay/research/data/es308-20261114/inputs/source-2650.json.gz`; its decompressed
sha256 starts `e800d5f8` and ends `82f6`.

- **Residual configurations** are as in VERIFY309N20261113 §(c): planar point sets in general position with
  distinct x, no convex 8-gon, no 6-cap and no junction (no point that ends a 6-cup and starts a 5-cap).
- **Owner state** of v: `(f1, f2, f3, f4, 0)` with `f_c(v) = max{ d2(u,v) : u < v, d1(u,v) >= c }`.
- **F6** = {states with f1 = 6} = the labels `(6,6,a,b,0)` with `0 <= b <= a <= 6`. These are the 28 states of
  source-2650 with indices between 91 and 153, and they form exactly the support of row 973. Today's row 973 has
  demand 6.

**Lemma 973' (demand 7, unconditional).** Every residual configuration occupies at most 21 of the 28 states of F6.
Equivalently, `|H ∩ F6| >= 7`, where H is the set of unoccupied states.

- **Relation to THEORY310N L9.** 973' *implies* L9, which assumes attainment. The formulation's wording "strictly
  stronger than L9" was corrected by the refutation agent to "implies L9".
- **Status:** OPEN. The geometric L9 is also still OPEN.

## 3. Planned certificate and its size (design:upper:3, steps 2-4)

The plan had two parts:

1. certified demand-1 coupled rows `(T_i, 1)` with `T_i ⊆ F6`, built from the pinned `coupled.py` with the full
   octagon clauses via `cut34_v4` (CaDiCaL LRAT plus cake_lpr `s VERIFIED UNSAT`);
2. an exact check that every 22-subset of F6 contains one of the `T_i`.

The largest single instance is `T = F6 \ H`, with 22 owners. In `gen22.json` it has 10,934 variables, 1,950,615
clauses, 33,279,712 literals and 198.6 MB of DIMACS. The model-checked support in §5 has 1,950,736 clauses, because
the state-dependent clauses depend on H.

## 4. What all nine Baek rows at demand 7 would give (EXACT, re-checked on source-2650 by the refutation agent)

The nine Baek rows are 973, 1165, 1167, 1171, 1175, 1179, 1183, 1186 and 2315: 28-state rows of demand 6.

- **Coverage.** Together they cover the 84 F-states exactly 3 times, and `|Lo| = 70`.
- **Today:** `3h(F) >= 9*6 = 54`, so `h(F) >= 18`.
- **Row 973 at 7:** `3h(F) >= 55`, so `h(F) >= 19`. This removes only (18,17), which is already EXACT TREE.
- **All nine at 7:** `3h(F) >= 63`, so `h(F) >= 21`.
  - The budget-35 slices are `(t, 35-t)`, and `h(Lo) >= 14` (from N66 <= 56) forces `h(F) <= 21`.
  - So (18,17), (19,16) and (20,15) all vanish by arithmetic. (18,17) and (19,16) are EXACT TREE already in any
    case.
  - Only **(21,14)** would remain.
- **If (21,14) were closed:** together with the closed budget <= 34 (the ES(8) <= 308 chain) this gives
  `h(C) >= 36`, `|R| <= 118` and `|S| <= 1 + 187 + 118 = 306`. The threshold is 307, so **ES(8) <= 307**
  (computer-assisted, unrefereed, hypothetical). The bridge is `budget34/bridge` line 94, shifted by one.
- **Cost of (21,14) is unknown.** The figure of about 3.6e5 nodes (design:upper:3's paired dive) is HEURISTIC and
  depends on the options used. Under fastbb2's default options the critic's paired dive went the wrong way: 7.1e11
  nodes against a base of 2.6e10.

## 5. Pilot (COMPUTED only; at most 1 thread and 1.5 GB per unit)

The pilot ran as four units, `esr-agx-r2-b973{,b,c,d}`, each with CPUQuota=100%, MemoryMax=1500M, MemorySwapMax=0
and RuntimeMaxSec. CaDiCaL children ran under RLIMIT_AS 1300M. No such unit was active at 05:43.

- **Encoder identity.**
  - `gen_stream.py` overrides only `CNF.add` of the pinned `coupled.py`. The sha256 pins of coupled.py
    (`959072b1…`) and common.py (`4b74ae77…`) are asserted in every script.
  - Its output is byte-identical to the pinned in-memory build at n=12 and n=17.
  - The fast split, static(22) + dynamic(S), has the same clause multiset as the pinned build at n=14.
- **First 22-owner run.** Witness pattern `H = [91,101,131,133,138,139]`: UNSAT in 0.65 s (0.61 s of it parsing),
  261 conflicts, 85 MB RSS. Its 19-owner prefix is SAT.
- **42 distinct witness F6 patterns.** All of them are allowed by the 13 inner rows of the b35s20-v132 union.
  **20 SAT, 22 UNSAT.**
- **65 seeded random allowed patterns:** **17 SAT, 48 UNSAT.**
  - The SAT fraction is 0.26 (Wilson interval 0.17-0.38).
  - That suggests about 25k-56k of the 148,628 allowed patterns survive (HEURISTIC). The count 148,628 is EXACT,
    recomputed in `corestats.py`.
- **Model check.** The CaDiCaL model for `H = [91,111,119,127,138,139]` satisfies all 1,950,736 clauses of the
  pinned-order build. This was checked by the pilot's own loop. The CNF sha256 starts `c9c3d4d5` and ends `d7d4d9`.
- **Why one SAT support is fatal to the route** (written argument by the pilot agent, not independently checked).
  - `CNF(T')` embeds in `CNF(T)` for `T' ⊆ T`.
  - Every clause family is local to the pairs, triples, quads or 8-sets of owners. State-dependent clauses depend
    only on the states involved. Sorted supports keep index order, so before-signs and orientation parities match.
  - Hence SAT(`F6 \ H`) implies that no row `(T,1)` with `T ⊆ F6 \ H` is UNSAT.
  - Consequence by the same argument: the hole vector whose occupied set is exactly `F6 \ H` violates no demand-1
    row of the pinned encoder of any support. That vector has 132 holes, far outside the budget-35 slices.
    Unconditional 973' is therefore not derivable from pinned rows. A conditional, in-slice version that uses
    rows reaching outside F6 is not ruled out.
- **Block images** (5 minutes each).
  - **Row 1165:** 5 inner rows, 337,869 allowed patterns. 14 of 32 witness-tight patterns are SAT; 43 of 291 random
    allowed patterns are SAT.
  - **Row 2315:** 13 inner rows, 150,630 allowed patterns. 100 of 325 random allowed patterns are SAT.
  - Rows 1167-1186 were not tested.
- **By-product: 19 candidate cores.**
  - Deletion-minimizing the 22 UNSAT witness supports gave 19 distinct F6-only cores of 11-17 states: nine of size
    11, seven of 13, and one each of 15, 16 and 17.
  - Together they kill exactly the 22 UNSAT witness patterns and 30,647 of the 148,628 allowed patterns (20.6 %).
  - They are in `cores_candidates.json`, in `cut34_v4 certify` format. They are COMPUTED only: not certified, not
    audited, and not appended to any input.

## 6. Cost estimate (measured rates)

| step | measured |
|---|---|
| one 22-owner test through the pipe | about 1.0 s (median 1.0, max 1.29, over 107 tests) |
| pinned streamed build at n=22 | 13.4 s |
| one deletion minimization | 15-30 s |
| exhaustive survivor list for row 973 | about 148,628 x 1 s, roughly 41 CPU-h in Python; much less in C++ with incremental solving (not built) |
| certifying the 19 cores with cake_lpr | not measured |

The original L9-by-cores plan was estimated at 5-30 CPU-h by the designer and about 200 CPU-h by the critics. It is
moot on this encoder: roughly a quarter of the allowed patterns have SAT supports. The size of the instances and the
solve rate are not the obstacle.

## 7. Refutation search (verdict: not refuted, confidence 0.6, no fatal errors)

The refutation agent used its own exact-integer code, `baek973-refute/f6occ.py`.

- **57-point residual chart** (`theory310-20261113/residual57_points.json`).
  - It was recomputed as in class: polygon 7, cap 5, cup 7, 0 junctions, 57 distinct states.
  - It has exactly one F6 owner, state (6,6,6,6,0). The other 56 owners have `f1 <= 5`.
- **Subsets of that chart** have at most one F6 owner. f1 = 6 needs a 7-cup inside the subset, and then its endpoint
  already has f1 = 6 in the full chart.
- **VERIFY309N's own generator** gives residual sets of at most 16 points.
- **The ETV and N66 sets** have no 6-cup, so they have no F6 owner.
- **ES8SLACK and the budget34 audit** contain only Boolean hole vectors and abstract signotopes, no point sets.
- **Agreement with ES8SLACK C15.** The pinned-encoder obstruction agrees with C15: an independent encoder also has
  22-owner abstract models for row 973.
- **Conclusion.** A proof of 973' must use realizability (geometry beyond the coupled relaxation) or the occupancy
  outside F6. The SAT models are not shown to be realizable, so they do not refute the geometric lemma.

## 8. Files and hashes (sha256, work directory `/home/jay/research/data/roadmap-20261115/`)

```
71e790aa19918c5df3826631cb1f8e3275c784d6cb180d49a4aaa83906214074  baek973/gen_stream.py
39c621e62820a86af27bc10ba5c0c88fe74d7e8ec39b59debf953e42f58fbfe2  baek973/pilot2.py
545e6c9be6263f6900b68ee26368dae9d87d787c2a29c38e8b3c151c68ac58b0  baek973/pilot3.py
dc004c38d4a2487b78a41c46187cc88c12d01445bb941d7c5ba68955cc6d13b4  baek973/pilot4.py
3fcee33575ad1f5318913edea2d36962d47d9a697cc00bd7a3cc37a43a294d6b  baek973/pilot2.jsonl
3cb073448fa0fe41a95e80f65cd926505789a3ee200f54d06dab340d4d080987  baek973/pilot3.jsonl
d37b94e7ddcb5489f73862bbe917ca71666a052e4f372995896c81c66e7afd1c  baek973/cores.jsonl
2f484da83b7b5d6d5cc33092e1fca2f60ca176e9312e869a6ffa162826c34843  baek973/cores_candidates.json
48cc475153415e815816e26494029a058909772288019faab5a9bf43cd70e8a3  baek973/satw1.modelcheck.json
dd0cd2f0aa918f1d517d8c3f87623cc0f5c01fcff6b7d74a6fb079b6e1c75ff8  baek973/verify.jsonl
509ea72d898f18dd9cf89932639dc20ba6574020f1afa601f647e6baa8713e23  baek973/witness_f6_patterns.json
692097a78068c6a6b14b27a79a3617400ec68e9c543b7bf5c8b407484b75e711  baek973-refute/f6occ.py
```

Also in the work directory: `baek973/README.md`, the pilot notes; `gen22.json`, the 22-owner instance statistics;
and `corestats.py`, `modelcheck.py`, `pilot.sh` and `run3.sh`. The work directory is outside the repository and
nothing has been copied in.

## 9. What remains

- **Certification.** Nothing is CERTIFIED. If the 20.6 % cut is wanted, certify the 19 candidate cores with
  `cut34_v4 certify` and cake_lpr. An independent audit needs a witness-free copy of `audit_followup_rows_v4.py`.
- **Re-checks.**
  - Only one SAT model was re-checked.
  - The fast static+dynamic split was matched against the pinned build only at n=14 (clause multiset). The
    streamed builder was matched byte for byte at n=12 and n=17.
- **Realizability.** Test whether any SAT 22-owner model is realized by a real point set (exact integers). A real
  realization would refute geometric 973'. Otherwise look for a stronger encoder.
- **A conditional, in-slice demand-7 lemma** for the budget-35 slices, using rows whose supports leave F6. The
  unconditional route is closed for this encoder (§5).
- **Rows not tested.** Rows 1167-1186 were not tested. The survivor counts for 973, 1165 and 2315 are sampling
  extrapolations.
- **Literature.** No literature check was made for the Baek-saturation observation.

## 10. Resume commands (one thread, 1.5 GB, with a deadline)

```bash
cd /home/jay/research/data/roadmap-20261115/baek973
P=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
# model check of the SAT support (writes satw1.modelcheck.json)
$P -B modelcheck.py '[91, 111, 119, 127, 138, 139]' satw1
# block-image sampling until END (epoch seconds) for the listed rows
systemd-run --user --unit=esr-agx-r2-b973e -p CPUQuota=100% -p MemoryMax=1500M -p MemorySwapMax=0 \
  -p RuntimeMaxSec=3600 --nice=10 --working-directory=$PWD \
  $P -B pilot3.py $(date -d '+55 min' +%s) 1165,2315
# pilot2.py / pilot4.py take the same END argument (witness/random sampling, core minimization)
```
