# Parent replay of the forced16 nonrealizability proof

**PROVED, written algebraic contradiction with exact independent replay.**
The fixed sixteen-label orientation model is not realizable by real planar
points. This third checker imports neither the finder nor either earlier
checker. It independently expands the common-label Grassmann--Pluecker
identity as a polynomial, reconstructs every bracket sign by cyclic order,
and rebuilds the strict product inequalities from raw certificate labels.

All **387** inequalities have positive integer weights. Their weighted
exponents cancel exactly for every one of the **560** absolute brackets.
In a hypothetical realization all brackets are nonzero. The unique-sign
term in each three-term identity has magnitude equal to the sum of the
other two magnitudes, hence strictly exceeds either. Multiplying the
weighted inequalities would therefore give a positive product strictly
larger than itself. This is the contradiction.

The full written proof and independently frozen discovery packet are in
[VERIFY_FORCED16.md](../forced16_realization/VERIFY_FORCED16.md).
This statement excludes arbitrary real coordinates, even without an
x-order requirement. It does not exclude other orientation models and
is not a counterexample to any real selection conjecture.

Command, from the repository root:

```sh
/usr/bin/timeout 20 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/protection_models/forced16_parent/verify.py
```

The checker applies AS150 MiB internally. [result.json](result.json)
reports **PASS**, symbolic identity zero, exact exponent cancellation,
and rejection of both an altered weight and a reversed inequality.
[reconstructed_rows.json](reconstructed_rows.json) contains its own
reconstructed factors. The positive weight sum is19,282,471,848,322,771.

| Input | SHA-256 |
|---|---|
| Orientation signs | `b21664b06887c4019d75023025b1cd80582064a0b06f53698d2a70bc8fc49067` |
| Certificate | `cfe42cec6041709b2ed7ac18ee16b13e57f091239ac19b8e5257aac46d2a326d` |
| This checker | `defc8101eb12cfa9b32ba4465a9b8b1aa9b27ccf936cc0a88c312adb44568365` |

No Lean-kernel or cake_lpr verification is claimed for this algebraic
certificate. Failed coordinate searches and heuristic solver outputs
are not premises of the proof.
