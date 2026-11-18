# Fifteen-point terminal model audit — COMPLETE

**Confirmed real fifteen-point terminal obstruction.** Exact coordinate,
clause, auxiliary and full subset checks pass. The fixed membership CNF is
**CERTIFIED by independent cake_lpr replay**. The general CNF is a checked
SAT model. Full scope: [VERIFY_MODEL15.md](VERIFY_MODEL15.md).
Started 14 November 2026, 05:24 KST; completed about 05:34 KST.
This disjoint track audits the SAT model at `terminal7-a/m15` and leaves
the completed `../audit/` and `../cardinality/` records unchanged.

## Statement and model

The supplied fifteen-point real (5,7)-valid set has **no terminal-safe weak
Delta**. It nevertheless has 4,805 ordinary weak Deltas, including four
triples, and every point belongs to an ordinary weak Delta of size at most
four. No ordinary/rooted weak-Delta conjecture, ES bound or ambient-size
minimality statement is inferred.

## Method and results

`model.py` streams all 64,718 assigned variables and 182,697 clauses and
reconstructs the complete map and formula. Exact flags and one-way witness
semantics pass, including allowed false internal containment flags. The
canonical assignment independently satisfies every clause.

`gp.py` checks all 15,015 necessary five-label sign relations. Subsequent
`geometry.py` replay matches all 455 signs to exact coordinates, enumerates
48 four-caps, 78 bad triples and 187 six-targets, and excludes every five-cap,
seven-gon and terminal-safe Delta among all 32,768 selections. Maximum
cap/cup/convex sizes are (4,6,6).

`membership.py` reconstructs all 313 fixed-coordinate membership clauses,
checks every assignment, and independently replays the fresh binary LRAT.
Cake with heap128/stack32 printed exactly `s VERIFIED UNSAT`; all hashes and
the retained proof's compressed roundtrip match. The generic SAT run's
partial LRAT is not treated as an UNSAT proof.

## Controls, files and remaining work

Own code, frozen coordinates/signs, receipts, the small membership CNF and
retained raw/compressed proof, `data/inputs.json` and scoped `SHA256SUMS`
pin the evidence. Scratch is
`/home/jay/research/data/delta3-codex-20261113/extension/model15_audit/`.
No parent checker is imported. The preliminary GP-only realizability
UNKNOWN remains in its original receipt; exact coordinates subsequently
resolve it. The audit is complete. The parent's restriction and uniform/cup
checks are separate, and global minimality is unclaimed.

## Resources and resume

Every job used one CPU, AS400 MiB, external 20 seconds and 18 CPU seconds.
Largest observed semantic-check RSS was 21,504 KiB; cake used 7,916 KiB.
No long unit was required. No jobs remain running or queued. Prior audit
and cardinality manifests verify unchanged, and no shared manifest changed.

From the repository root, after checking resources:

```sh
audit=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/model15_audit
py=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
timeout 20s env PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  prlimit --as=419430400 --cpu=18 "$py" -B "$audit/geometry.py" \
  "$audit/data/real15.coordinates.json" real15-recheck
timeout 20s prlimit --as=419430400 --cpu=18 "$HOME/.local/bin/cake_lpr" \
  --CML_HEAP_SIZE=128 --CML_STACK_SIZE=32 \
  "$audit/data/certificate/witness.terminal.cnf" "$audit/data/certificate/fresh.blrat"
```

Receipt tags must be fresh; scripts refuse to overwrite outputs. Model/map
reconstruction uses the retained original scratch inputs with recorded
hashes. A later larger replay needs coordinated resources. No proof deletion,
git mutation, install, external action or frozen-scope edits are authorized
by these commands.
