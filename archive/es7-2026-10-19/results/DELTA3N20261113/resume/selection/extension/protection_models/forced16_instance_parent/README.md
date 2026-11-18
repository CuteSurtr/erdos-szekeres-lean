# Fresh parent replay of the fixed product certificate — PASS

**PROVED in Lean, conditional algebraic statement:** the fixed 387 strict
product inequalities in 560 positive variables are incompatible. All
338 frozen modules compiled again in a new directory. The parent also
compared all 354 exact axiom lists with the frozen manifest, checked their
module locations, and independently matched the literal Lean tables to
the raw signs and certificate without importing the generator.

The transcription comparison covers all 560 lexicographic triples, all
560 signs, and every label, slot, factor index and positive weight in all
387 rows. The Lean row blocks verify their sign/parity metadata; the
column blocks verify weighted cancellation. The final product theorem
uses only `propext`, `Classical.choice`, and `Quot.sound`.

The successful fresh checks total **169.426 seconds**, with maximum
process RSS **763884 KiB** and zero reported process swap. The named unit
was `nov13c-vfy-delta6-f16-instance-parent`, started at08:17:08 KST,
CPUQuota100%, MemoryMax1300M, MemorySwapMax0, RuntimeMaxSec600. Each Lean
child had one CPU affinity, `-j1 -M500`, AS3GiB, a950MiB RSS guard and an
18-second deadline. All modules finished before the08:23 status check.

The exact command and per-file receipts are retained in
[data/logs](data/logs); [data/result.json](data/result.json) contains the
source hashes, dependency manifest hash, axiom comparison, transcription
result, times and fresh compiled-module comparisons. The source packet
and its two frozen generic algebra dependencies were not edited.

The bounded replay command is documented in the
[frozen source packet](../forced16_instance_lean/README.md). The parent
collection command, from the repository root, was:

```bash
/usr/bin/timeout 30 /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/protection_models/forced16_instance_parent/collect.py
```

Its output was `PASS`, 338 modules, 354 axiom reports, all raw labels,
slots, factors and weights matching. The first collection attempt
incorrectly treated the manifest's list of axiom records as a dictionary;
it stopped at that comparison. The corrected collector explicitly builds
the dictionary, rejects duplicate theorem names, compares exact lists and
checks module attribution. No Lean source or proof changed for that fix.

**Boundary:** this is not yet a Lean theorem that actual real coordinates
cannot realize the fixed sign table. The coordinate-to-product bridge and
Mathlib real-number adapter remain unfinished. The complete real
nonrealizability result is the independently replayed
[written exact algebraic proof](../forced16_realization/VERIFY_FORCED16.md).
The fresh Lean result formalizes its finite certificate and conditional
product contradiction. It makes no claim about other sign models or the
general Delta conjecture.
