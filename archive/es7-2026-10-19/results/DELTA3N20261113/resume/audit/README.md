# Independent continuation audit: final readiness

**Required reviews complete.** All writes were confined to this directory
and `/home/jay/research/data/delta3-codex-20261113/resume/audit`. No parent
files, jobs or units were changed; no git operation, installation, email,
long job or proof-checker run was performed.

| Item | Independent outcome | Report |
|---|---|---|
| Original lazy pool | Geometry, complete input suffixes and final exports checked; two operational bugs reproduced. Both m16 runs finished UNKNOWN. | [VERIFY_POOL.md](VERIFY_POOL.md) |
| Pool v2 fixes | Limited diff review confirms empty-array shapes, positive-batch validation and startup provenance. Parent's rerun counts are explicitly attributed; the full suite was not repeated. | [V2 follow-up](VERIFY_POOL.md#follow-up-v2-fix-review) |
| Maximal-set family and real star | New family sound; all 48,226 generated clauses satisfy a canonical real assignment. Exact 12-point witness refutes the maximality shortcut; Delta={8} still works. | [VERIFY_MAXIMAL.md](VERIFY_MAXIMAL.md) |
| Compact encoder | Written equivalences/range reduction confirmed; fresh build matches both scheduled m16 CNFs; independent integer controls and 3,392 projected clause queries pass. | [VERIFY_COMPACT.md](VERIFY_COMPACT.md) |
| Extension embedding and weak-n8 lemma | All-gap canonical argument confirmed; 268 insertion-pattern controls; full rebuilt certificate CNF matches; five-insertion weak-n8 lemma valid under its stated premises. | [VERIFY_EMBEDDING.md](VERIFY_EMBEDDING.md) |

The exact real negative result is **COMPUTED by independent integer
enumeration**, not an LRAT certificate or a weak-Delta counterexample.
It has 25 four-caps, zero five-caps/heptagons, 54 hexagons and 1,526 working
weak Deltas. Its supplied red set is maximal and misses a hexagon.

Pending boundaries are explicit: the parent's tiny-pool and one-insertion
cake acceptance logs and matching hashes were checked, but those proofs
were not independently replayed here. No outcome or certificate from the
active compact frontier searches is audited by these reports. Any future
SAT candidate or UNSAT proof needs the corresponding result checks. The
parent's new five-point transversal probe is outside the requested scope.

All independent controls used AS400 MiB and one CPU/thread, with external
deadlines of at most 20 seconds (eight seconds for the initial real-star
check). The longest actual combined compile/control invocation was 5.023
seconds. No additional search or control is queued by this audit.

`results/` retains small evidence, input snapshots and provenance; generated
large CNFs/binaries remain in assigned scratch. `SHA256SUMS` hashes the
completed audit files. The original pool copies also retain their detailed
source-path manifest at [results/MANIFEST.json](results/MANIFEST.json).
