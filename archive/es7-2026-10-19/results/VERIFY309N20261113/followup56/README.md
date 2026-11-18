# Follow-up audit of N66 ≤ 56

**INDEPENDENTLY CONFIRMED — N66 ≤ 56**, with written soundness and CERTIFIED
propositional components. This follow-up audits the 23:43 KST
certificate in `/home/jay/research/data/n66-20261113/p2/b13g/it1`.
It strengthens the completed N66 ≤ 57 audit and supports the two-slice ES309 chain.
The detailed written argument is in [VERIFY_N66_56.md](VERIFY_N66_56.md).
`data/audit_status.json` records four fresh additional row certificates,
zero pending obligations and no failed or unknown row stages.

The claimed result is that every point set with no 6-cap, no 6-cup and no
convex octagon has at most 56 points. The certificate excludes at most 13
holes in the 70-state model. Its trimmed CNF has 319,611 clauses, including
6,775 row clauses and 56 symmetry-breaking clauses. Unlike the prior
N66 ≤ 57 instance, it uses mirror lexicographic symmetry breaking.

## Model, method and result

The mirror map transposes states and preserves hole count. Either a real set
or its reflection satisfies the full lexicographic condition. Assigning
prefix-equality auxiliaries satisfies all 79 full symmetry clauses, hence
the 56 retained clauses. Every other clause family is valid for either real
set separately; the trimmed formula need not itself be reflection-closed.
The full written soundness argument and trust boundary are in the audit.

The independent C++ recognizer accounts for every clause: 319,611 occurrences,
319,610 distinct, zero unknowns. Its new code rebuilds state geometry and
chain numbering; only the installed PySAT sequential counter is shared with
the earlier audit. Original clause IDs reconstruct the trimmed bytes exactly,
with SHA-256:
`8d4b9099cf045ca72ba5ac56e8ecea00a73a44652d5a9f3d100f63f1f10bc151`.
This is reconstruction from the untrimmed CNF plus independent semantic
recognition, not fresh generation of all original CNF bytes.

All 6,775 row justifications pass: 3,229 transported, 3,303 mirror,
192 direct cores, 51 cycles. All 2,856 cycle triple tests pass.
Of 624 required template/core CNFs, 620 match prior independently checked
definitions and hashes. All four new full CNFs independently regenerate to
their claimed hashes; all four now have fresh accepted LRAT proofs.

The parent rehashed the 8,025,950,354-byte LRAT and replayed it with cake_lpr.
Its SHA-256 is:
`ff79c2ef3805255b18917dc0769c5088cca0ee8106c5eefb78b8f212fa487296`.
I directly inspected the new log's exact `s VERIFIED UNSAT` line. Cake used
heap 3200 MB, stack 32 MB, 204.02 wall seconds and 3,286,916 KiB maximum RSS;
hashing plus replay took 210.841 seconds. A separate fresh main SAT solve
ended UNKNOWN after its 600-second budget; the confirmed verdict rests on
the accepted retained-proof replay. This fresh attempt did not produce a
second certified main proof. Its logs and partial-trace hashes are archived
under `data/fresh_main/`; plain and roundtrip-checked compressed traces remain
in scratch. The additional four row proofs also have verified compressed
roundtrips in `data/new_rows_roundtrips.json`.

## Controls and preserved failures

Exact-integer controls on 32 real sets including reflections give 216,800 row
evaluations and 1,264 full symmetry-clause evaluations with zero violations.
They cover 64 states and 2,622 tight row evaluations. Their point counts are
8–50, so they do not constitute positive controls for the budget-13 counter.
The recognizer rejects three deliberate corruptions, one each in geometry,
counter and symmetry clauses.

The original failed 2,000 MB cake attempt (212.3 seconds), subsequent original
3,200 MB success, and all small probe logs are retained. An initial C++ compile
failed because a variable name collided with `std::ends`; it was renamed,
and the successful compile and failed log are both retained. No mathematical
counterexample or unknown clause was found. Future row failures/timeouts
remain in per-attempt logs and are never promoted to certificates.

## Artifacts and remaining work

`data/` holds row coverage, cycle orders, new and inherited certificate
inventories, clause counts, controls, hashes and small log snapshots.
`SHA256SUMS` pins the small record. `tools/` contains all new/adapted audit code.
Scratch contains the reconstructed trim, four independently generated full
row CNFs, all probe logs and the parent's main replay. No proof is deleted.

Indices 0–3 in `data/new_certificates.json` (one template and three cores)
completed sequentially in a parent-scheduled 1-CPU unit with AS700MiB,
MemoryMax1000M, MemorySwapMax0 and RuntimeMaxSec2200. To reproduce their
certificate driver in an appropriately scheduled unit:

```bash
prlimit --as=734003200 bash /home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/VERIFY309N20261113/followup56/tools/certify_four56.sh
```

Each full/sub solve has a 180-second deadline; cake has a 120-second deadline
with **explicit heap512/stack32**. It must print exactly `s VERIFIED UNSAT`.
Raw proofs are retained and zstd copies use one thread. Working RSS is expected
below approximately 600 MiB; the AS limit is a fail-safe, not permission to
approach the unit's memory limit. The driver launches no units itself and
does not raise caps or retry with more memory.

The evidence collector was rerun after those jobs and confirmed full coverage.
To refresh its small evidence inventory:

```bash
timeout -k 2s 25s prlimit --as=380000000 --cpu=25 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B cloud/es7-2026-10-19/results/VERIFY309N20261113/followup56/tools/collect56.py
```

The collector checks the literal cake lines and selected-CNF/LRAT hashes;
it reports pending obligations unless all four are covered. It does not scan
the large main proof. Parent review is complete; the ES309 record now includes
the simpler chain using N66 ≤ 56 and the two previously checked Lean-row trees.

## Scope and resources

All new record files are confined to this directory. Scratch:
`/home/jay/research/data/verify309-codex-20261113/followup56`.
The repository `es-research` skill and the user's tighter worker limits
apply: one thread, at most 30 seconds per probe, address-space limit below
400 MB (C++ compilation up to 500 MB). The parent schedules all long work.
This worker launched no units or jobs over 30 seconds and performed no
third-party installation, git action, earlier report edit, root README edit,
or math.md edit. Parent-scheduled proof work is reported separately.

Labels: PROVED means a written argument; COMPUTED means exact finite
checks; CERTIFIED requires the literal cake_lpr success line for the
identified CNF/LRAT pair. This follow-up is not Lean-checked.
