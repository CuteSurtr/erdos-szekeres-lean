# Independent finite-row verification

Current verified status: **confirmed SAT for frozen v1–v4, ending at the
966-coupled-row slice20 system; final v5 remains unexcluded**. This verification
does not certify any geometric realization, new coupled-row theorem,
branch-and-bound tree, or ES(8) improvement.

## Inputs and independent parsing

The compressed 2,650-row source hashes to
`8c7fe9ef5264182524095d46ef50ed6bc691cab425efa965756d1870112241aa`.
The frozen initial coupled pool hashes to
`91a4e36f31712231ed1386576d6dcbe846ddf6c1b0d4de41e225bbdb4a18bcf8`.
Our parser checks integer index ranges, unique supports and demand bounds.
The 154 profiles are exactly the nonincreasing four-tuples in [0,6] with
first height<6 or second height=6, followed by zero. Their index order was
separately compared with ResidualCatalogData.lean. F and Lo are independently
computed from the first height and have sizes 84 and 70.

The old s23 extra file contributes only entries [2:], exactly the 812
unique demand-one rows in the frozen pool. Its first two capacity rows are
not used. Both new initial slice files were separately compared with
capacities (19,15) and (20,14) plus precisely that pool.

## Translation

The counter recurrence and four-clause equivalence are written in README.
There is a direct auxiliary extension from every hole assignment using
integer prefix counts. Conversely, induction on each prefix gives exact
threshold meanings in every CNF model, so demanding the final thresholds
and prohibiting threshold 35 produces exactly the stated inequalities.
Demand-one rows are literal disjunctions. The unit -1 means h[0]=0.

`audit_translation.py` imports neither the encoder nor any finder. It reads
the DIMACS stream directly, independently traverses every raw support, and
checks each actual local clause group's complete Boolean truth table.
It checks the demand and budget output units and consumes the whole file.
Initial audit: 77,067 gates, 1,009,568 truth assignments, 283,115 clauses,
758,300 literals. All passed. This is a computational audit of the written
translation argument, not a Lean proof.

## Positive and negative controls

The encoder's local gate and small-counter controls pass 16 and 4,606 cases.
A separate exact-coordinate program generated 240 fixed-seed point sets,
retained the 207 meeting the residual hypotheses, and computed their
starting-cap and ending-cup ranks. It checked those ranks a second way by
exhaustive subsequences. Owner assignments were injective, included zero,
and satisfied all base, pool and capacity rows. These are small-set positive
controls, not evidence that abstract 34-hole assignments are realizable.

A valid tiny binary LRAT passed cake_lpr's exact `s VERIFIED UNSAT` line;
an empty proof did not. No exclusion of the research CNFs has been certified.
In particular the retained 1.30 GB interrupted LRAT is not a proof of UNSAT.

## Explicit SAT witness

The parent's finder candidate in runs/s20/bb/WITNESS.json was treated only
as input data. `extend_assignment.py` first checked its row inequalities
and used actual prefix counts to construct the auxiliary assignment.
`check_independent.py` independently re-read the rows and checked all
3,464 support sums in integers, h[0]=0, total=34, F=20, Lo=14, and every
clause of the original combined CNF. No finder code or old witness-killer
helper was imported. The full exact receipt is `data/witness-v1.json`.

The auxiliary assignment hashes to
`74c34aa87af4b33cbdeedc07d363420671477f0f320e42d134474be8f368409a`.
This proves satisfiability of the finite model even though neither our
CaDiCaL nor our interrupted CP-SAT search found the vector on its own.

## Strengthened v2

The parent extra file hashes to
`81029d946c29318905cbfa967fbcf8ac7d4513193a25e06626568abb9de3b1c9`.
Its capacity rows were checked to be exactly F>=20 and Lo>=14. Its 819
coupled rows extend the original pool by seven. All seven supports contain
zero holes in the preceding witness, so each independently excludes it.
The extracted pool hash is
`d3a819094d66a5075e23139b6844c57045fd57aba82b1f336bfde50d7063b9b8`.
The new CNF hashes to
`7d23164f451081f4d8202d7e49270478843afb021b6cfc73472b04863b4dca80`.
Its complete independent translation audit and 207 real-point controls
passed. The new geometric rows' LRAT/provenance replay belongs to the
separate auditor; it is not claimed as a fresh replay by this track.

## Limitations

SAT establishes insufficiency of a particular finite row set, not a
counterexample to ES(8)<=308. UNSAT claims require both an accepted cake_lpr
proof for the exact CNF and justified geometric input rows. Neither solver
timeouts nor CP-SAT infeasibility statuses are promoted to that label.

## Further checks at 10:28 KST

Witness2 separately passes all 3,471 v2 rows and every one of its 283,381
CNF clauses. The witness and complete per-row margins are saved in
`data/witness-v2.json`; the corresponding full CNF assignment is retained.

The v3 pool has 956 coupled rows, including the 819-row prefix. Its exact
slice20 CNF has 283,518 clauses and 760,360 literals. The same independent
translation audit passed, and the exact-coordinate controls passed all
3,608 rows. Nine new rows exclude witness2. Search is still open.

Six deliberately corrupted copies of the v3 CNF were rejected by the
independent audit: changed h[0] sign, wrong support index, wrong gate sign,
off-by-one demand output, budget33 substituted for budget34, and a replaced
coupled row. The audit does not consult the stored CNF hash to accept/reject,
so these were semantic/structural failures. The untouched original hash was
checked before and after. Negative files, failure logs and hashes remain
in W/sat/adversarial-v3; the summary is copied to the record's data directory.


## Final v4/v5 checks

The fourth parent vector passes every v4 row and all283,528 CNF clauses.
It additionally passes all6,829 distinct provisional size9 rows outside
the base/v4 pool, with minimum support sum1. Therefore the entire supplied
size9 family still admits a34-hole vector with F=20, Lo=14 and h[0]=0.
The vector is explicitly checked, not inferred from a solver status.
Final v5 rejects it on all five appended13-state supports. See the
provisional-nine SAT witness and final-v5 rejection receipts in data/.

Final v5 has971 coupled rows and3,623 total inequalities. Its77,286-variable,
283,533-clause CNF passed the complete independent translation audit.
In addition to207 standard controls, seven larger admissible real sets
(five of size13 and two of size14) passed all rows, for214 controls and
775,322 exact row evaluations in total. The other larger attempted sets
were filtered out because they contained a6-cap or convex octagon.

The native PB exports for v2, v3 and both final provisional searches were
independently parsed without importing OR-Tools. Every Boolean domain,
coefficient, support, inequality bound, h[0] constraint and global budget
was checked. The sole representation difference was term sorting inside
sums; coefficient-index pairs match exactly. The uncertified discovery
model has10,449 constraints and is not an exclusion certificate.

No further discovery job started after10:45. Solver statuses, shutdown
receipt and final file hashes are frozen separately in the final summary
and manifest. The existence of SAT witnesses for earlier pools does not
settle final v5 or ES(8)<=308.
