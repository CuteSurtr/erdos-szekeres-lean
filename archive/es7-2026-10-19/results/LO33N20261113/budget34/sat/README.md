# COMPUTED: v1–v4 SAT; final v5 remains unexcluded

Independent finite-row SAT sidecar, 14 November 2026. No improved ES(8)
bound is established by this track. Four parent-supplied abstract hole
vectors were independently verified against every row and every CNF clause.
The fourth also satisfies all 6,829 additional provisional size9 rows.

## 1. Statement

There are 154 Boolean holes, with h[0]=0 and sum(h)<=34. The base consists
of 2,650 source inequalities h(S)>=d. F consists of the84 profiles whose
first height is at least5; Lo contains the other70. The initial combined
model has h(F)>=19 and h(Lo)>=14. Later models restrict to slice20 with
h(F)>=20 and h(Lo)>=14, forcing total34. Old capacity rows were discarded.
The parent owns the completed slice19 exact tree and coupled-row proof audits.

An abstract hole assignment is not a real point configuration or an ES
lower-bound example. These finite SAT witnesses show limitations of the
specified row systems only.

## 2. Model and soundness

DIMACS variable i+1 is h[i]. Prefix counters have semantics
q(i,j) iff the first i inputs contain at least j true entries, with
q(i,0)=true and q(i,j)=false for j>i. Each recurrence
q(i,j) iff q(i-1,j) OR (x[i] AND q(i-1,j-1)) is encoded by four clauses.
Writing its variables y,a,x,b, these are
(!a OR y), (!x OR !b OR y), (!y OR a OR x), (!y OR a OR b).
Constants are simplified. Complete local truth tables establish equivalence;
induction gives exact prefix meanings and a unique auxiliary extension.
Requiring q(n,d) expresses a lower bound; forbidding q(n,35) expresses
sum<=34. Demand-one rows use their direct positive disjunction.

The combined <=34 satisfiability question equals the union of exact slices
(19,15) and(20,14): capacity minima give total>=33, and a33-hole solution
can gain a nonzero-index hole without violating any lower-bound row.
This padding argument uses no budget33 checker or exclusion certificate.

## 3. Method

The emitter independently validates JSON supports, indices, demands and the
154-profile universe. State order was separately compared with the Lean
catalog. No finder/checker code or old budget33 helper was imported.
A separate streamed audit rebuilds counter indices from raw supports and
checks every actual clause group by truth table. A separate witness checker
recomputes all support sums in integers and evaluates every CNF clause.
The CP-SAT protobuf text is also independently parsed and compared, including
all coefficients, domains, capacities, budget and separate optional hints.

CaDiCaL2.1.3 ran with LRAT output. No target UNSAT result was accepted.
Only cake_lpr's complete line `s VERIFIED UNSAT` can certify such a result.
The local wrapper follows that protocol while retaining both raw and
compressed proofs; the stock wrapper would delete the raw trace.
CP-SAT statuses alone are never exclusion certificates.

## 4. Results

| Frozen model | Coupled rows | Total rows | CNF clauses | Independently checked result |
|---|---:|---:|---:|---|
| v1 combined |812|3464|283115|SAT, witness1|
| v2 slice20 |819|3471|283381|SAT, witness2|
| v3 slice20 |956|3608|283518|SAT, witness3|
| v4 slice20 |966|3618|283528|SAT, witness4|
| final v5 slice20 |971|3623|283533|Encoding audited; no surviving witness or exclusion here|

Every checked witness has h[0]=0 and(F,Lo,total)=(20,14,34).
The full154-bit vectors, all row counts/margins, and CNF hashes are in
[data/witness-v1.json](data/witness-v1.json),
[data/witness-v2.json](data/witness-v2.json),
[data/witness-v3.json](data/witness-v3.json), and
[data/witness-v4.json](data/witness-v4.json). Complete auxiliary assignments
remain in W/sat/parent-witness-1 through parent-witness-4.

Witness4 also passes every one of the6,829 distinct provisional size9 rows
outside the base/v4 pool, obtained from the three supplied killtools data
files. Thus adding the entire supplied size9 candidate family to v4 still
leaves a34-hole SAT model. This is an exact finite-model observation, not
certification of those candidate rows. Final v5 excludes witness4 with its
five additional13-state rows. See
[data/provisional-nine-sat-witness.json](data/provisional-nine-sat-witness.json)
and [the final v5 check](data/v4-witness-final-v5-check.json).

Initial CaDiCaL search was stopped UNKNOWN after356.34 CPU seconds.
CP-SAT attempts on the initial system, v2 and v3 stopped UNKNOWN after
159.184,241.195 and561.261 seconds when superseded by checked parent vectors.
The provisional v4 attempt with LP relaxation stopped UNKNOWN after336.428
seconds. The final sequential attempt disabled LP relaxation and ended UNKNOWN
after480.000 seconds at10:50:33. All sidecar units stopped before the10:52
freeze. Exact statuses are recorded in the final result summary.
No new long discovery run started after10:45.

## 5. Controls

The16 gate truth cases and4,606 small counter cases pass. Complete CNF audits
check every clause, including1,010,600 local truth assignments in each final
slice encoding. Six deliberate corruptions were rejected: h[0] sign,
support index, gate sign, demand off-by-one, budget33 substituted for34,
and a replaced coupled row. Original files remained unchanged.

Final v5 passes214 exact real-point controls:207 sets of sizes1–12 and7
additional sets of sizes13–14, totaling775,322 row evaluations. Orientations,
convexity checks and ranks use integers; both starting-cap and ending-cup
ranks are independently cross-checked by exhaustive subsequences. The
small real sets are not expected to meet the target34-hole budget.

The provisional enlarged system also passes the207 standard real controls
(2,162,529 row evaluations), which does not prove its added rows.
Tiny binary-LRAT positive and empty-proof negative cake_lpr controls pass.
Detailed controls are in [data/discovery-controls.json](data/discovery-controls.json)
and [data/adversarial-v3.json](data/adversarial-v3.json).

## 6. Files and hashes

W is `/home/jay/research/data/es308-20261114`; all sidecar large artifacts
are under W/sat. Source gzip SHA-256:
`8c7fe9ef5264182524095d46ef50ed6bc691cab425efa965756d1870112241aa`.
Final extracted pool971 SHA-256:
`83d5f6e90b6bc1e1b04b07861ec2b12306b862b38b27ea4fd5f733d2391dac60`.
Final v5 CNF SHA-256:
`ebbc3dcf79fe48eee83204dce1f6d60356a8a0264c836ddbd8a3def51b6c53b1`.
It has77,286 variables,283,533 clauses and760,539 literals, estimating
108.80–181.33 MiB initial CaDiCaL storage before search/proof overhead.

The1,301,098,496-byte partial LRAT is retained raw and compressed. It is
not an UNSAT certificate. Raw SHA-256:
`8da5df70602b6315876cec15566a914ad6aa08def1cc79babdfa740fad7a0245`;
compressed SHA-256:
`25587afbcbd3bbb51fcc3a7633ad6a3c40bd59527e3b36bd00fd5e000f0a445c`.
All encoding/PB audit receipts are in[data/encoding-audits.json](data/encoding-audits.json).
The final manifest records hashes of every sidecar artifact and retained trace.

One CPU, pinned to11. Address-space reservation<=1200 MiB; CP-SAT AS<=1000
MiB. Long units have CPUQuota100%, MemoryMax1600M, MemorySwapMax0 and finite
RuntimeMaxSec<=1900. No jobs overlap except brief bounded verification on
the same CPU. The stop/freeze deadline is10:52. The final resource receipt
records stopped units and observed RSS. No git action, installation, external
message, pool modification or proof deletion was performed.

## 7. What remains

Final v5 is not excluded by this track. More finite reasoning or additional
justified rows are needed to establish the35-hole target. No geometric
realizability conclusion follows from the saved Boolean vectors.
All provenance/proof replay for coupled rows and the slice19 tree belongs
to the separate parent/auditor records.

## 8. Resume commands

Read [VERIFY_FINITE_SAT.md](VERIFY_FINITE_SAT.md) and the final result summary.
The final solver-ready CNF is W/sat/s20-v5/system.cnf. Generate a new exclusive
run directory and fresh bounded unit only in a newly authorized time window;
do not overwrite the frozen packet. The current scripts enforce the original
10:45 launch cutoff and10:51:15 solver deadline.

