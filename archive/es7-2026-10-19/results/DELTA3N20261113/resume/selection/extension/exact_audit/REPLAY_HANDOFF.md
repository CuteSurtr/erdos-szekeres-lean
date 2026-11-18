# Pending independent replay

The formula/augmentation audit is complete. No certificate was available
at its handoff. The parent job is `nov13c-vfy-delta6-finite13`, output
`/home/jay/research/data/delta3-codex-20261113/extension/finite13-b/`.
Its `proof.blrat` is currently being written. Do not replay a moving proof
or interpret its existence as an UNSAT result.

Before an independent replay:

1. Confirm the parent solve has completed UNSAT and the proof is retained.
   Record the solver and parent cake logs separately from our own result.
2. Check `input.cnf` hashes to
   `3ec4b75d9076b6f257fed83f3cbb17b8372a43f53f1c0fc8d30730e4c5d35b87`.
   A different formula needs its own scope review.
3. Coordinate the replay's CPU, AS, cake heap/stack, MemoryMax and deadline.
   Current authorization here is only one CPU, AS300 MiB and <=20 seconds.
   The parent solve's larger allocation is not automatically a reservation
   for this independent checker. Check shared CPU/memory and active guard.
4. Stream SHA-256 over the stable CNF, proof and cake binary before replay.
   Use a bounded systemd user unit for a long replay, with CPUQuota,
   MemoryMax, MemorySwapMax=0 and RuntimeMaxSec. Preserve full command,
   stdout/stderr, resource accounting and failure cases in this directory.
5. Accept only a line exactly equal to `s VERIFIED UNSAT` in the fresh
   cake_lpr output. Exit zero alone is insufficient. Hash inputs again
   afterward, compare, and preserve the proof (compressed) after replay.

No independent replay or certification is represented by the current
`PROVED / COMPUTED` formula-audit labels. The geometric base remains the
explicit dependency at `../audit/VERIFY_EXTENSION.md`.
