# Verification record — 2026-10-05

Proof checkpoint: `0407d69d70b12eae6c66fe8808de464264330984`.
The subsequent cleanup changes documentation, ignore rules and audit-output
recording; it does not change the finished geometric proofs.

## Main library

- `lake build --wfail`: **passed**, 3,194 build jobs (including dependencies).
- `python3 scripts/check_axioms.py`: **passed**, 201 named theorem roots.
- Python suite with the existing optional Z3/HiGHS environment: **41 tests passed**.
  The standard-library-only CI run skips 13 solver-dependent tests.
- Lean successfully resolved all **75 declarations** checked from the paper map
  (74 project-qualified names and Mathlib's `convexHull_mono`).

The [complete, unabridged axiom output](validation/axiom-audit-2026-10-05.txt)
contains these main results:

```text
'ErdosSzekeres.Suk.theorem2016' depends on axioms: [propext, Classical.choice, Quot.sound]
'ErdosSzekeres.HMPT.theorem2020' depends on axioms: [propext, Classical.choice, Quot.sound]
Axiom audit passed for 201 theorems: only standard Lean axioms.
```

`#print axioms` reports transitive axiom dependencies of each named result.
The allowlist is exactly `propext`, `Classical.choice`, and `Quot.sound`.
It excludes `sorryAx`, custom theorem assumptions declared as axioms, and
native-evaluation axioms. This records Lean verification of the stated
propositions; it does not expand them to the unformalized parts of the papers.
See [PAPER_MAP.md](PAPER_MAP.md) for those scope distinctions.

## Placeholder and repository checks

A source scan covered **all 102 tracked `.lean` files**, including finished
Suk/HMPT modules, adapted prerequisites, the audit, and standalone experiments.
There were **zero occurrences** of the tokens `sorry`, `admit`, `sorryAx` and
`native_decide`, and zero lines declaring an `axiom` or `constant`. Thus there
is no `sorry` anywhere in the maintained finished results. Failed local probes
inside the ignored cache are not maintained results and are not included in
this statement. The transitive axiom check independently covers the dependencies
of both completed final theorems.

The Git index contained **zero** files under `.cache/`, `.lake/`, or `.elan/`,
and zero compiled Lean objects, native objects/libraries, trace files or Python
bytecode. `git check-ignore` confirmed that representative toolchain and build
outputs are ignored. The committed generated `.lean` catalog is proof input,
not a compiled build artifact. Third-party licenses and modifications are
identified in [THIRD_PARTY.md](THIRD_PARTY.md).

[Source manifest](validation/source-manifest-2026-10-05.json) records SHA-256
hashes of every maintained Lean source, the toolchain/dependency pins, the audit
script, the audit output and validation logs. Its combined source digest is
`d73423332422742791949c5dc190e90ce7a0a181a62d839c88df9211db3b65cf`.
Logs of the full build and Python run remain in the ignored cache; their hashes
are recorded, while the requested full axiom output is committed above.

To reproduce the main audit, after building:

```sh
python3 scripts/check_axioms.py --output /tmp/erdos-axiom-audit.txt
```

For this Mac's workspace-local toolchain:

```sh
ELAN_HOME="$PWD/.elan" .elan/bin/lake build --wfail
ELAN_HOME="$PWD/.elan" python3 scripts/check_axioms.py \
  --lake "$PWD/.elan/bin/lake" --output /tmp/erdos-axiom-audit.txt
```

## Separate certificate checkpoint

The [chunked catalog and leaf](../experiments/omission-chunked-2026-10-05/README.md)
were checked separately, with both Lean processes exiting zero. Their saved
profiler and axiom output are in the directory's `validation.json`. They are
not part of the default-library build or its 201-root audit. Their conclusions
certify the 2,685 balanced row encodings and a single conditional leaf only.
The two complete omission trees and their geometric transfer remain unproved
in Lean. Certificate work stopped after this checkpoint was pushed.
