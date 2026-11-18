# D6_12_NOTE: the d6_12 weak-Δ count (15 November 2026, 13:22-13:35 KST, team track T5)

**Status: resolved. d6_12 has exactly 486 weak Δs (EXACT, own exhaustive recount; the main session's code and the
round-6 verifier's own output file give the same number).** The range "494 to 12,176" in ROUND6.md §2 statement 12 is a
summary error: it leaves out d6_12. The correct range over the 12 AT_n realizations is **486 to 12,176**. Nothing else
changes. Weak D still holds on every set, and the AT_n refutations do not use this count.

**Independent verification: CONFIRMED** by verifier V3 at 13:30:59. Its claim was `d6-12-correction`, its verdict is in
`/home/jay/research/data/roadmap-20261115/pm1115/claims/d6-12-correction.verdict.json`, and its write-up is
[VERIFY_D6_12.md](VERIFY_D6_12.md).
- V3 used its own exact code, with a geometric point-in-triangle convexity test (`pm1115/v3/d6-12-correction/v3_wd_count.py`).
- It reproduces 486 and the per-set counts of all 12 sets (minimum 486, maximum 12,176).
- It also reproduces the d6_12 variants 660, 32, 486 and 631.
- It found the wrong text at all four places listed below.
- V3's caveat: the cause in §2 fits the data, but how the error arose cannot be verified.

## 1. Statement

- Set: `round6/atn/d6_12_real.json`, 12 integer points, n = 6. Its 220 triple signs equal the abstract model
  `delta/probe1/inputs/d6_12.json`.
- Weak Δ (ROUND6.md "Definitions"): A ⊆ S is 4-cap-free and meets every gon, a gon being a convex (n − 1)-gon of S.
- Under this definition d6_12 has **486** weak Δs.
- The published sentence "The weak-Δ counts are 494 to 12,176 per set" appears in three places, all from the same
  source [corrected 15 Nov pm (C1 issue 17): four files, as line 14 counts; the third item covers two copies, the repo
  ROUND6.md and `round6/writeup/ROUND6.md`]:
  - `round6/vatn/VERIFY_ATN.md` line 136, the verifier's prose for statement 12, written 08:48;
  - `round6/writeup/ROUND6.tmpl.md` line 172, copied from it;
  - ROUND6.md line 193, statement 12, the same text in the repo copy and in `round6/writeup/`.

## 2. Cause

- **Same definition, same file, no bug.** The verifier's own output `round6/vatn/out/d6_12.json` (vcheck.py, written
  08:40) already says `"weak_S": 486`. The main session's `at_own_check.py` (09:09) says 486. This recount says 486.
- **Same input.** The main session hashed the same d6_12_real.json, `f97741da…`, as the atn author's SHA256SUMS. There
  is only one realization and one sign table of d6_12. (`scratchpad-snapshot-20261115/dr/d6_12.real.json` is
  byte-identical to the sign table, despite its name.)
- **Where 494 came from (an inference that fits the data, not verifiable).** 494 is the count of d6_11, m11_3 and
  m11_5, the smallest of the other eleven sets. Most likely the verifier left out d6_12, the only 12-point set, when it
  summarised its out files at 08:48. ROUND6.md then copied the sentence.
- **No other definition gives 494 for d6_12.** See the table below. The x-mirror leaves the count unchanged, and no
  variant (subsets of U, maximal sets only, the empty set, the y-mirror) gives 494. Counting the empty set changes
  nothing, because S has 55 gons.

## 3. Method

My own script, `/home/jay/research/data/roadmap-20261115/pm1115/t5/wd_recount.py`, shares no code with
`at_own_check.py` or `vcheck.py`.
- It works from the triple signs only: exact integer orientations for the real sets, the sign string for the abstract
  model.
- **4-caps.** Every one of the four triples is a cap.
- **Convex position, two methods asserted equal on every (n − 1)- and n-subset of every set:**
  - primary: split by the chord from the leftmost to the rightmost point; the points above must form a cap chain with
    the two ends, the points below a cup chain;
  - cross-check: no point of any 4-subset lies inside the triangle of the other three.
- **Enumeration.** All 2^|W| subsets of W are enumerated as bitmasks, including the empty set.
- **Self-test, run first.**
  - Three fixed configurations: a kite, a point inside a triangle, and a 4-cap.
  - 30 random 8-point integer sets. On each, the bitmask count equals a literal set-based count, and the x-mirror sign
    rule equals the signs of the reflected coordinates.
- All runs were single-thread foreground runs of under 2 s. No unit was started.

## 4. Results (EXACT)

**d6_12, under each candidate definition.** S has 12 points, 68 four-caps, 0 five-caps, 55 gons and no convex hexagon.
U = S − r has 46 gons.

| definition | count |
|---|---|
| **weak Δs of S: A ⊆ S, 4-cap-free, meets every gon of S (the ROUND6 definition)** | **486** |
| ... of these, containing r | 34 |
| ... containing both rightmost points u and r | 0 |
| ... inclusion-maximal only | 32 |
| ... is the empty set among them? | no (S has 55 gons) |
| weak Δs of U: A ⊆ U, meets every gon of U | 660 (maximal: 13) |
| A ⊆ U meeting every gon of S | 452 |
| A ⊆ S meeting only the gons of U | 694 |
| x-mirror (x → −x; caps stay caps) | 486 |
| y-mirror (y → −y; caps ↔ cups, i.e. 4-cup-free) | 631 |
| abstract model `delta/probe1/inputs/d6_12.json` (same 220 signs) | 486 |

**All 12 AT_n realizations: weak Δs of S, three independent codes.**

| set | n | points | 4-caps | gons | this recount | main session (`at_own_check.out`) | round-6 verifier (`vatn/out/*.json`) |
|---|---|---|---|---|---|---|---|
| d7_13 | 7 | 13 | 65 | 32 | 2,535 | 2,535 | 2,535 |
| d8_15 | 8 | 15 | 114 | 30 | 12,176 | 12,176 | 12,176 |
| d6_11 | 6 | 11 | 40 | 33 | 494 | 494 | 494 |
| **d6_12** | 6 | 12 | 68 | 55 | **486** | **486** | **486** |
| m11_1 | 6 | 11 | 39 | 34 | 507 | 507 | 507 |
| m11_2 | 6 | 11 | 42 | 36 | 526 | 526 | 526 |
| m11_3 | 6 | 11 | 40 | 33 | 494 | 494 | 494 |
| m11_5 | 6 | 11 | 39 | 34 | 494 | 494 | 494 |
| m11_6 | 6 | 11 | 40 | 33 | 557 | 557 | 557 |
| m11_7 | 6 | 11 | 37 | 33 | 570 | 570 | 570 |
| m11_8 | 6 | 11 | 40 | 33 | 507 | 507 | 507 |
| m11_10 | 6 | 11 | 38 | 33 | 570 | 570 | 570 |

- Every set has 0 five-caps, no convex n-gon, and 0 weak Δs through both rightmost points. So the AT_n refutations stand
  as recorded.
- The two AT2_6 sets have 653 weak Δs (seed1_b, the 13-point V) and 696 (seed5_b). Both lie inside the corrected range.
- **Corrected sentence for ROUND6 §2 statement 12:** "The weak-Δ counts are 486 to 12,176 per set (d6_12: 486;
  d8_15: 12,176)."
- Not rechecked here: the uniform-Δ range "34 to 600 for AT" in the same sentence. It agrees with the verifier's out
  files, where uniform_U runs from 34 (d6_12) to 600 (d8_15), but no own code checked it.

## 5. Files and hashes (SHA-256)

Work directory `/home/jay/research/data/roadmap-20261115/pm1115/t5/`:

| file | SHA-256 |
|---|---|
| `wd_recount.py` | `c46d6ae2a7a15b30340fe6ef56ea07fd50ca3970d994b7bf2dc4c145f25f533d` |
| `d6_12_recount.out` (real and abstract d6_12) | `dab57a7e410120aea60b384e2a3fd36d4cb6c5cdc3512dfb25c70ce31796b689` |
| `n6_sets_recount.out` (d6_11, eight m11, two AT2 sets) | `6f1fa7b75c5d675298543ae20f2e1442a436b54012cb095df8bb9f0bbf60b395` |
| `d7_13_recount.out` | `d8c8c50564cb37c2b91b7ab667f90107d885e39e1376431f50f145d9872096ee` |
| `d8_15_recount.out` | `e2f3d0c1e11c98b234438095721a0c6912b973228188985afcee86f157ab8cee` |
| input `round6/atn/d6_12_real.json` | `f97741da80a29f53bd640706b7b03fc639d3db16abb4f92623dcecddab559c90` |
| input `delta/probe1/inputs/d6_12.json` | `c563d726fb539843847b37b29a44556b40424549701acdea1a41e715dcaec19d` |
| verifier output `round6/vatn/out/d6_12.json` (08:40) | `32f0eccc962b9d1aa7508c2adbc924e4167b9c79d380daffbdb0b8142654a2e7` |
| `round6/vatn/VERIFY_ATN.md` (08:48) | `f992596c16d253ac1963cd464153bbb0de5ef6444f5f3f810575f20052b56d3c` |
| ROUND6.md (repo copy = `round6/writeup/ROUND6.md`) | `08192f068d87e76f94b85173f874d72e728c2f125f7c19a1b49b8c09f50e626f` [superseded 15 Nov pm (C1 issue 17): this was the hash of both copies at 13:31; the main session corrected the repo copy at 15:28, which now has SHA-256 `2b6d4e92…`, while `round6/writeup/ROUND6.md` still has `08192f06…` (checked by H1 at about 19:06)] |

## 6. What remains

- The owner may want the sentence corrected in ROUND6.md statement 12. That file is not modified here, per the rule
  that existing records are never edited. [superseded 15 Nov pm (C1 issue 17): the main session corrected the repo copy
  of ROUND6.md at 15:28 (statement 12 at line 193 and the closing section "Correction, 15 November 2026 afternoon (main
  session)"); the work copies `round6/writeup/ROUND6.md`, `round6/writeup/ROUND6.tmpl.md` and `round6/vatn/VERIFY_ATN.md`
  still say 494]
- The "unresolved" remarks in VERIFY_ATN_MAIN.md line 29 and README.md line 107 are answered by this note.
- Claim `d6-12-correction` is CONFIRMED (V3, 13:30:59). Nothing is pending on this track.

## 7. Rerun

```bash
cd /home/jay/research/data/roadmap-20261115/pm1115/t5
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python; A=../../round6/atn
$PY -I wd_recount.py 6 $A/d6_12_real.json /home/jay/research/data/roadmap-20261115/delta/probe1/inputs/d6_12.json
$PY -I wd_recount.py 7 $A/d7_13_real.json; $PY -I wd_recount.py 8 $A/d8_15_real.json   # each under 2 s
```
