# Batched lazy subset constraints

The two initial m16 jobs use the frozen `batch_pool.py`. Use
`batch_pool_v2.py` for future runs: it fixes empty small-instance array
dimensions, rejects nonpositive batch sizes, and retains a startup source
snapshot/hash. The initial m16 jobs do not exercise the small-instance bugs;
their executing source is intentionally preserved unchanged. The independent
audit documents both issues and the external-deadline requirement.

**COMPUTED search method; both m16 trials ended UNKNOWN.** The n7 trial
retained 767 subset clauses after three intermediate models, and n8 retained
511 after two. Each had a 900-second solver budget. Results, exact selected
masks and event logs are archived under `data/n7m16-b128/` and
`data/n8m16-b128/`; final formulas remain in scratch with hashes.
The small n6,m8 control has a fresh accepted proof in `data/control-n6m8/`;
the saved finder result correctly remains labelled UNSAT_UNCERTIFIED because
certification was a separate step. Its successful checker log is
`data/control-n6m8/cert/cake-stack32.out`.

The input is an unconditioned weak
universal CNF from the independently audited earlier C++ encoder. Its last
2^m clauses, in integer-mask order, are the subset-failure constraints. The
driver retains every preceding clause and initially omits those final
clauses. Each SAT model is checked by exact Boolean sign semantics. All
four-subsets define convexity; a full subset zeta transform determines every
working Delta. A reproducibly sampled batch of such masks and their reversals
is added. Reversal only chooses extra masks; it imposes no orientation
symmetry restriction.

Soundness: every stage is a literal subformula of the previously justified
universal CNF. A counterexample to weak Delta has a canonical assignment
satisfying every such subformula. Therefore UNSAT of any stage excludes all
counterexamples, provided the final exported CNF is independently certified.
SAT in an incomplete pool is only an intermediate configuration. A reported
zero-Delta model requires the separate earlier model checker, and realizability
must be resolved before claiming a real point-set counterexample.

The incremental solver is only a finder. Its UNSAT result is labelled
UNSAT_UNCERTIFIED until a fresh CaDiCaL 2.1.3 LRAT run and cake_lpr acceptance.
The driver saves a plain `final.cnf`, original CNF hash, exact selected masks,
events, and limits. Its complete pool formula can be checked directly against
the original clauses; no new geometric clause family is introduced.

Planning: the existing m16 inputs have 2.16 million (n7) and 3.45 million (n8)
literals. At 150–250 bytes per literal these require roughly 0.32–0.86 GB
before buffers. Start n7 at AS900 MiB / MemoryMax1200M, n8 at AS1200 MiB /
MemoryMax1600M, with finite external deadlines. Actual memory and the shared
6-GB verifier budget must be checked before any launch. Source tests are
bounded short calls; long searches run only in parent-scheduled units.
