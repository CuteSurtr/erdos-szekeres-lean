# Original compact left16 independent replay — PASS, CERTIFIED

Fresh independent replay of the original compact16 CNF/proof, whose full
instance audit is already frozen in ../left16_longcup/. No long-cup
augmentation is used. Authorized heap2800, stack32, AS3100MiB, one CPU,
nominal MemoryMax4000M, Swap0, Runtime780, checker660. Cache release is
every1s/64MiB, with an internal3100MiB/no-swap guard. No other own audit
check or compilation overlaps the replay; preparation/packaging is AS150.

On fresh acceptance, the intended closure is T7 for all admissible left
sets via explicit through15 coverage, this individual size16 result and
the separately checked capacity16 dependency. The parent's capacity
receipt is inherited evidence, not an independent Lean replay here.
All earlier audit records remain frozen; writes stay in this new packet.

AttemptA printed `s VERIFIED UNSAT` but its wrapper failed while reading
optional /proc child-IO telemetry at child exit. Source and logs are copied
unchanged into data/attemptA; the supplemental manual posthash recovery
also matches. The parent requested fresh clean retry before final closure.
RetryB catches PermissionError alongside vanished-process telemetry errors;
proof access, checker arguments, memory guard and hash validation are
unchanged. It uses new exclusive outputs and the same authorized allocation.

RetryB completed cleanly at08:17:29KST: exact `s VERIFIED UNSAT`, exit0,
134.537s checker /145.348s total, stable streamed before/after hashes for
CNF, raw proof, compressed proof and checker. Cgroup peak3010473984bytes,
zero swap; the3100MiB allocation is released. The final certificate is
data/retryB/result.json, not the failed attemptA wrapper or manual recovery.

**PROVED (written deduction from certified components and inherited checked
capacity): T7 holds for every finite real x-ordered GP left set with no
four-cap and no seven-gon.** See VERIFY_LEFT16.md for the explicit size
coverage and exact scope. This is not an end-to-end Lean formalization.
