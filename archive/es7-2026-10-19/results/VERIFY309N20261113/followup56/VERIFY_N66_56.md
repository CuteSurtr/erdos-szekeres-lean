# Independent follow-up: N66 ≤ 56

**INDEPENDENTLY CONFIRMED: N66 ≤ 56, with written soundness and CERTIFIED
propositional components.** The retained main LRAT passed a fresh cake_lpr
replay. Independent code reconstructed its CNF bytes and recognized every
clause. All row justifications pass; the four additional supporting CNFs
now have fresh CaDiCaL 2.1.3 proofs accepted by cake_lpr. The parent reviewed
the argument and collected all four receipts, with no pending row obligations.
This is not a Lean proof. A separate fresh solve of the main trimmed formula
ended UNKNOWN at 600 seconds and is not evidence for this verdict.

## Statement and canonical model (PROVED, written)

Let S have distinct x-coordinates, general position, no 6-cap, no 6-cup,
and no convex octagon. For u<v label the pair by the largest ending-cap
and ending-cup sizes, each minus one. Both coordinates are in 1..4.
The incoming labels at v generate a down-set I(v) of the 4×4 box.
The state-separation argument gives d(u,v) in I(v) minus I(u), hence distinct
points have distinct states. There are 70 states; occupancy selectors count
points exactly, and the first two states are occupied for |S|≥2.

For occupied owners, assign pair orders to x-order, thresholds to their exact
labels, and orientations to determinant signs. Rank attainment bounds each
label coordinate by the corresponding source height plus one. This gives the
refined-domain exclusions. Coordinate growth on cap/cup triples, the
six-order bounding-box test, and the four-point signotope property justify
the pair/triple/packet clauses, exactly as in the prior independent audit.

Assign each k-chain atom to the existence of its indicated cap/cup, and each
endpoint atom to the existence of a 5-cap/5-cup on those endpoints. Consecutive
slopes justify extension. A 5-cap and 5-cup on the same endpoints have their
three internal points strictly above and below the common chord. Each chain
is strictly convex, and their union is a convex octagon, so the endpoint
exclusion holds. Negative occupancy guards satisfy clauses involving missing
owners. The fixed units and an at-most-13 counter on the remaining 68 hole
literals therefore have a canonical extension whenever |S|≥57. Sets of size
at most one already satisfy the proposed bound.

The counter encoder remains the same shared installed PySAT sequential
counter as in the prior independent audit; its implementation was not
reproved here. All geometric enumeration and the symmetry clauses are
independent of the original N66 encoder/checker programs.

## Mirror symmetry breaking (PROVED, written; COMPUTED checks)

Reflect by ρ(x,y)=(x,−y). It preserves x-order and convex polygons, exchanges
caps/cups and their longest ending lengths, and consequently transposes every
incoming diagram. Thus τ is an involution of the 70 states and
Occ(ρS)=τ Occ(S); both fixed states stay fixed and the hole count is unchanged.

The saved list consists of 27 distinct nontrivial τ-orbits, each written as
an ordered pair (s_j,t_j); the other 16 states are τ-fixed. Among the occupancy
vectors x and x∘τ, choose the one whose first unequal listed pair is (0,1).
If every listed pair is equal, either vector is allowed. Such a choice always
exists because reflection exchanges the two entries of every listed pair.

Let e_j mean that the first j pairs agree. The full encoding has, for each
pair, the comparator clause

```
¬e_(j−1) ∨ ¬x_sj ∨ x_tj
```

and, except at the final pair, the two implications

```
¬e_(j−1) ∨ ¬x_sj ∨ ¬x_tj ∨ e_j
¬e_(j−1) ∨  x_sj ∨  x_tj ∨ e_j.
```

Omit the prefix literal at the first pair. With each e_j assigned its intended
prefix-equality meaning, the implications always hold and the comparator
holds exactly when an equal prefix does not end with an unequal (1,0) pair.
These one-direction implications suffice; reverse implications are unnecessary
for existence of the canonical extension. There are 27 comparators and
52 propagation clauses. The trimmed formula retains exactly **56 of these
79** clauses, all independently recognized with their actual variable IDs.

**Reflection closure of the trimmed formula is not required.** Every geometric
clause and every justified row holds for every real set in the class. It holds
for S and ρS separately, even if the chosen collection of rows or lazy
quadruples is not closed under τ. Choose the real set satisfying the full
lexicographic condition, extend its canonical assignment, then restrict to
the trimmed clause subset. The counter is invariant because reflection
preserves the number of holes. A sub-CNF of these clauses cannot refute both
representatives of a real counterexample merely by this symmetry breaking.

`tail56.py` recomputes τ, checks all pairs/orbits, checks all eight local
prefix transition cases and 112 first-difference representatives, and writes
the symmetry clauses without importing `p2_sb.py`. The real-point controls in
`data/real.json` cover 32 sets including reflections, 216,800 row evaluations
and 1,264 full symmetry-clause evaluations, with zero violations. They see
64 states and 2,622 tight rows. The determinant/chain/owner computations are
exact integers and do not import the original encoders. These fixtures have
at least 20 holes and do not test satisfiability of the budget-13 counter.

## Trimmed CNF (COMPUTED exact checks)

`recognize56.cpp` is new C++ code based on the independently authored
`../tools/audit_mono.py` argument. It rebuilds the 70 profiles, cells, refined
domains, plain-domain bounding boxes, pair/triple IDs, chain IDs and endpoint
IDs. It enumerates all relevant families, restricting quadruple work to
supports that actually appear in the trimmed file. Every comparison is an
exact normalized literal-vector comparison, not a hash-only membership test.

It recognizes **319,611 clauses, 319,610 distinct**, with no unknown clauses.
The duplicate is an order-transitivity clause. Independent chain numbering
ends at variable 1,647,026; counter numbering ends at 1,647,741; symmetry
allocation ends at header variable 1,647,767. The largest used variable is
1,647,761.

| Family | Distinct retained clauses |
|---|---:|
| Threshold | 1,088 |
| Empty domain | 1,550 |
| Excluded label | 31,129 |
| Forced sign | 6,544 |
| Order transitivity | 4,092 |
| Growth | 51,132 |
| Chain start | 8,016 |
| Endpoint exclusion | 691 |
| Chain-to-end implication | 9,482 |
| Signotope packet | 151,935 |
| Chain extension | 45,917 |
| Fixed units | 2 |
| Row clauses | 6,775 |
| Counter clauses | 1,201 |
| Symmetry clauses | 56 |

`reconstruct56.py` streams the 319,611 distinct original clause IDs through
the 9,201,530-clause untrimmed CNF and independently writes the trimmed header
and bytes. It obtains exactly 21,301,437 bytes and SHA-256
`8d4b9099cf045ca72ba5ac56e8ecea00a73a44652d5a9f3d100f63f1f10bc151`.
The original CNF digest is also reproduced:
`1e44f104135e01b8532313b36079800109a8acb6d3c032f58e0fd5c1c36b78ea`.
This is byte reconstruction from the original CNF plus independent semantic
recognition, not a claim to have freshly generated all original CNF bytes.
No LRAT is read by this worker's reconstruction.

Three deliberately corrupted clauses (a positive occupancy guard, a reversed
counter auxiliary sign, and a reversed comparator sign) are all rejected by
the recognizer; `data/negative.json` retains the exact mutations. Its first
compile failed on the C++ name collision `ends`; the renamed version builds
cleanly with `-Wall -Wextra -Werror`. Both compile logs are preserved.

## Rows and independent certificate obligations

`model.py` and `rows56.py` adapt the prior independently authored `rows66.py`.
They rebuild the diagrams/domains/τ/six-order test and recheck the exact
used-row and justification multisets. They additionally validate test indices,
octagon subsets, template identifiers, recursive justification depth, inherited
CNF definitions and the corresponding prior receipts. No original encoder
or original row checker is imported.

All **6,775** row justifications pass: 3,229 transported, 3,303 mirror,
192 direct cores, **51 cycles**. All 51 cycle orders have eight distinct states
and pass all 56 ordered triple tests, totaling **2,856** tests. The tests force
each ordered triple of present owners to have positive orientation (or rule
out coexistence). All eight owners would then be in convex position in the
listed cyclic order, contradicting the octagon exclusion. This proves the
demand-one cycle rows. They are not being inferred from the previous audit's
50-cycle count.

Transport tests are checked on both the original core and its injective image.
Static clauses depend only on owner count; listed octagon clauses are sound
under any injective image. An excluded-label test with an empty domain is
implied by its empty-order clause. Thus the template's certified UNSAT, once
available, establishes the transported row. Mirror rows follow by applying
the row to ρS and transposing back.

Recursive justifications require 417 templates and 207 cores, **624 distinct
CNFs**. Of these, **620** have identical definitions and hashes in the completed
N66≤57 independent audit, with matching certificate receipts (and direct
cake-log checks for its fresh certificates). Four are new:

| Index | Kind / owners | Full CNF clauses | Independently regenerated SHA-256 |
|---|---|---:|---|
| 0 | template `7ced42669e0b1c5d`, 18 | 681,494 | `95ab056c2e9f65578259b8b642347e9455d49ae1de829576784878237d0dbfb4` |
| 1 | core, 26 | 3,258,947 | `b3d0aeccad06d4cbb66753d7bbd2727f3d780d6d1a6c21f64f19d32e73b650a0` |
| 2 | core, 20 | 1,074,233 | `47f4a984a7b45dd7994e2a3f4a1c072a37d507c867d5a618233315293313afe7` |
| 3 | core, 24 | 2,327,050 | `37245215fbb71b02849d8051bed05dc0c63d6acbe35c989870967a9eb829f4fe` |

The generator is the prior independent `coupled66_independent.py`, copied here
with only its import changed from `rows66` to `model`. All four fresh full-CNF
hashes match. No original static cache is used. Each generation completed
within 13 seconds and below 31 MB RSS. Original `p2_template_cert66.py` deletes
its per-row CNFs and LRATs, so its metadata does not supply retained proofs
for these four new independent obligations. `new_rows56.py certify` retained
every full/sub proof, selected a sub-CNF using full-proof hints, solved it
again and required cake's literal success line. Selection is not a trusted
proof check: every selected clause must belong to the independently generated
full CNF and the new subproof must pass cake.

## Main proof replay and completed row checks

The parent-owned `replay_existing.py` freshly hashed and replayed the original
8,025,950,354-byte LRAT. Its SHA-256 is
`ff79c2ef3805255b18917dc0769c5088cca0ee8106c5eefb78b8f212fa487296`.
I read its `replay_existing/result.json`, `cake.out`, and `cake.time` directly.
`cake.out` contains exactly **`s VERIFIED UNSAT`**. This is a fresh independent
checker invocation on the retained proof, not a fresh main SAT solve.

Exact checker arguments:

```text
/home/jay/.local/bin/cake_lpr --CML_HEAP_SIZE=3200 --CML_STACK_SIZE=32 \
  /home/jay/research/data/n66-20261113/p2/b13g/it1/trim.cnf \
  /home/jay/research/data/n66-20261113/p2/b13g/it1/trim.lrat
```

The parent supplied 1 CPU, AS 3600 MiB, MemoryMax 4600M, no swap and a
600-second unit limit. Cake took 204.02 wall seconds; hashing plus replay
took 210.841 seconds. Maximum RSS was 3,286,916 KiB, with zero swaps.
The older original run's 2,000 MB-heap failure and subsequent 3,200 MB-heap
success remain recorded in `cake_attempts.json`; that failure is not discarded.

The four row obligations completed in `nov13c-vfy-n66-56-newrows`, using one
CPU, AS700MiB, MemoryMax1000M, no swap, a 2200-second unit deadline, and an
explicit heap512/stack32 checker. Every stage finished; no timeout or failed
stage was recorded. The independently regenerated full formulas were solved,
original-clause subformulas selected, then freshly solved and certified:

| Index | Selected clauses | Selected CNF SHA-256 | Fresh LRAT SHA-256 |
|---|---:|---|---|
| 0 | 81,543 | `0a766b42f2a8856eea404c937567adc05fc1fbe58ae3e271b74e67fcb9c7c11d` | `00af5d8b4769a2dc3da73269c31342dd8e8bb1302f38adfcf0049a9625643790` |
| 1 | 396,215 | `e7de6747d4f94102ebab9b9ca68ae7a6ba956f04eb6d4fd868eb76c21715c53c` | `7361355a999d981fc6832040ec4b89ce4363663988a2199684989bb29e416111` |
| 2 | 2,173 | `98cb4cacf44282d1fd24349ddab19dc4d38c69a9de723ef1e314c3761ff94988` | `9bc74d2d5601e3d9eee509f7e2aec28518d6d494207a308445f93544ef9d20f2` |
| 3 | 299,555 | `866d51e5941d2eb30927b71ba6ae8ca59481ccb672efa237f0284827509630f4` | `775f2cb3def6de5f5770c2eae5fc75710083071a6ec027e390c07cd8358940c0` |

`tools/collect56.py` inspected all exact cake success lines and recomputed
the selected CNF/proof hashes. `data/audit_status.json` reports
INDEPENDENTLY CONFIRMED, four fresh certificates and zero pending obligations.
Both plain and compressed proofs are retained in scratch; all eight full/sub
compressed row proofs passed decompression/hash comparison. The extra main
solve in `nov13c-vfy-n66-56-fresh` ended UNKNOWN after 600.053 seconds of
solver wall time. Its 4,294,290,101-byte incomplete trace is retained, with
roundtrip-checked zstd copy and hashes in `data/fresh_main/result.json`.
It supplies no new certificate. Main-bound confirmation uses the freshly
accepted retained LRAT, not a fresh second proof. This is not a
literature-priority assessment.
