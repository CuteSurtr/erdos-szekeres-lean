# Fivefold orientation-split pilot, 4 November 2026

**Exact computation:** the 13-layer base regenerated with SHA-256 `d7bbb74395b2799ecaa0bbaf9850842c205f059c7db20667e91d457e7e37928e`, matching the recorded instance. The 11-layer comparison base regenerated with SHA-256 `4d9a193e0f5c15f306f2166fcd6c814d675117cc113192f3604c4c9fb2723bf0`. The archive manifest records raw and compressed hashes and verified decompression round trips for both bases and each pilot cube.

## Attack and soundness

**Written proof (reviewed, not refereed):** retain the existing reflection unit `H(1)` and the phase-order cube `d111111`, namely `psi_1<psi_2<psi_3<psi_4`. The common units are `8803,8737,8738,8739,8748,8749,8758`. Split on one actual orientation variable instead of another layer-phase comparison:

`v=2009 = [orient((1,0),(2,0),(3,0)) > 0]`.

For any formula `F`, the two formulas `F and v` and `F and not v` cover every model of `F`. Thus no geometric assumption is added globally and no further symmetry claim is needed. Only this one phase-order cube is piloted; the remaining twenty-three consistent four-layer phase orders are not covered by these runs. An UNSAT result in this pilot would require a retained LRAT proof checked by both checkers before becoming a certificate.

**Exact computation:** geometric-family unit propagation under the common cube fixed 1,675 variables. Among three-layer triples supported on layers 0–3, 74 orientation variables remained unset by that propagation. After removing clauses already satisfied by these values, variable 2009 appeared positively 383 times and negatively 383 times, the highest minimum of the two counts. This is a deterministic balanced-occurrence heuristic, not a lookahead cuber or a claim that full unit propagation cannot fix the variable. The next candidate, 2219, represents `orient((1,0),(2,4),(3,4))` and has 363 occurrences of each sign; it was scored but not used in the initial binary split.

## Exact test on the certified 56-point set

**Exact computation:** `m5_pilot.py` reads `ES8SYM/sets3/c5_56pts_11layers_centre.pts`, checks the 56 points are distinct and invariant under multiplication by `zeta_5`, removes the single centre, and checks all 26,235 triple determinants of the remaining 55 points are nonzero. It checks strict nesting and compares each point and phase with exact cyclotomic signs. No floating-point arithmetic participates in these decisions.

The arithmetic uses integer coefficient vectors modulo `zeta_5^5=1` and `1+zeta_5+...+zeta_5^4=0`. For a real expression `A+B sqrt(5)`, equal-sign terms are immediate; opposite-sign terms are compared by `A^2` and `5B^2`. This is the sign argument in `SYMMAX/verify5.py`; that file is not imported because its top level writes output files. Orientations use `Im(conj(q-p)(r-p))`.

**Written proof (reviewed, not refereed):** multiplying all points by the conjugate of one outer-orbit representative is a rotation followed by a positive scaling, so it preserves orientations. It sends that representative to the positive real axis. Exact cross-product signs identify each inner representative in the sector `(1,zeta_5)`. The boundary at angle `pi/5` is `-zeta_5^3`. Multiplication by `-zeta_5^2` subtracts `pi/5` for points in the upper half-sector, putting their folded phase in `(0,pi/5)`. The sign of the cross product of two folded representatives is then exactly their strict phase order.

**Exact computation:** direct determinants of each canonical triple assign the orientation variables. Independent generic Horn closure from `tests/adversarial.py` then validates all 1,630,243 clauses of the freshly generated eleven-layer base. The identical check is repeated after exact complex conjugation.

| Set | Geometry violations | Chain violations | `H(1)` | `d111111` | Sign of triple `(5,10,15)` |
|---|---:|---:|---|---|---|
| Original 55 noncentral points | 0 | 0 | true | true | positive |
| Exact mirror | 0 | 0 | false | false | negative |

**Exact computation:** the same geometric triple has variable 1424 in the eleven-layer formula, not variable 2009; the test maps by point triple rather than reusing a variable number across dimensions. Each tested configuration has a unique sign branch. The original lies in the positive branch of the piloted phase-order cube. Its mirror verifies the reflection toggle and the opposite sign before symmetry normalization; it is not an example satisfying the negative branch together with the common `H(1)` and `d111111` assumptions. A split branch is not asserted to hold for every real configuration.

## Resource bounds and reproduction

**Evidence only: experimental protocol.** One solver at a time, one core, equal 300-second real-time limits for the baseline and both split polarities. A separate guard checks active + wired + compressed memory every three seconds and terminates the current solver if total memory reaches 29,000,000,000 bytes. The solver phase has a 1,500-second overall guard. The three initial runs use no proof tracing; any solver UNSAT is therefore only a recorded solver verdict pending proof generation and checking. The script strips build-host and machine-path lines before saving logs, removes temporary raw logs, and records child cleanup.

From the results directory, set `ARCHIVE`, `SCRATCH`, and `BIN` to the intended local directories:

```sh
python3 -I C6C7REVIEW/m5_pilot.py --prepare --archive "$ARCHIVE" --scratch "$SCRATCH"
python3 -I C6C7REVIEW/m5_pilot.py --run --archive "$ARCHIVE" --scratch "$SCRATCH" --bin "$BIN" --seconds 300
```

**Exact computation:** `logs/m5_prepare.json` contains the selection, exact-set outcomes, source hashes, all cube units, and verified archive hashes. `logs/m5_generate_t11.log` and `logs/m5_generate_t13.log` contain fresh generator statistics. The completed solver measurements are in `logs/m5_runs.json`.

**Exact computation:** the executed runner is retained in the archive as `pilot_runner_executed.py`, SHA-256 `9e4d53db93a066d213aea337c6057918d23221331ddb865ce6ada3700baff19c`, matching the preparation manifest. The current script distinguishes cleanup of a completed child from completion of the whole campaign, and retains any SAT assignment separately from the shortened log. Formula construction, exact arithmetic, variable selection, solver commands, and resource guards are unchanged.

## Completed measurements and interpretation

**Evidence only: solver measurements, replayed 4 November 2026.** All three runs used the same CaDiCaL binary and a 300-second real-time limit, without proof tracing. Each reached its limit with exit code zero and UNKNOWN.

| Instance | Wall seconds | CPU seconds | Conflicts | Propagations | Peak RSS, decimal GB | Result |
|---|---:|---:|---:|---:|---:|---|
| Baseline `H1 + d111111` | 300.942 | 299.732 | 1,206,072 | 1,791,640,676 | 2.336 | UNKNOWN |
| Baseline + `2009` | 300.847 | 299.734 | 1,293,138 | 1,913,023,343 | 2.607 | UNKNOWN |
| Baseline + `-2009` | 300.766 | 299.638 | 1,334,547 | 1,955,969,205 | 2.294 | UNKNOWN |

**Evidence only:** the orientation split did not make either child tractable within the pilot budget. Larger conflict and propagation counts measure activity, not progress toward a proof; they do not establish a speedup. The two children together received twice the baseline's CPU budget, so their summed counters are not an equal-total-budget comparison. This single deterministic variable choice gives no basis for scaling the partition to a larger campaign. A subsequent experiment could compare alternative orientation triples or propagation-based lookahead scores, with the same explicit cover and exact-set checks.

**Evidence only:** the solver phase used 902.555 seconds wall time in total and 899.104 seconds CPU, with one solver at a time. The highest observed system active + wired + compressed memory was 27,436,122,112 bytes, below the 29,000,000,000-byte guard. No resource guard fired. All three solver children and the temporary idle witness watcher were reaped; no active-process record or raw scratch log remains. No SAT assignment or UNSAT proof was produced. The fivefold threshold remains open.

**Exact computation:** result-file SHA-256 is `98431ad955fff2a37f2fc7e71501cdaa5d7b8632d3ea20bc5474299bdff457a3` for `logs/m5_runs.json`. The sanitized logs have these hashes:

| Log | SHA-256 |
|---|---|
| `logs/m5_baseline.log` | `868c6ff297c91beae4f4cc3e6b59341ddbf187af6a4ae79109b2b046eee12df0` |
| `logs/m5_split_positive.log` | `517ba78d339b60a4b2687af570f21777e36623120723dbbf3653c9510a79c592` |
| `logs/m5_split_negative.log` | `6cdac1707db4b414d75f416b6bca86e789491503c7e328e9e36657bc5d894b26` |
