# Terminal n5 closure audit — PASS

**CERTIFIED finite components; PROVED all-size deduction:** every finite
real x-ordered GP set with no five-cap and no convex pentagon admits a
terminal-safe weak Delta for n=5. Complete formula/map audits and three
fresh independent cake replays PASS. The written argument and exact scope
are in [VERIFY_TERMINAL5.md](VERIFY_TERMINAL5.md).

| Case | Variables | Clauses | Replay |
|---|---:|---:|---|
| terminal m7 | 204 | 1,143 | `s VERIFIED UNSAT` |
| terminal m8 | 471 | 2,440 | `s VERIFIED UNSAT` |
| pure base m9 | 210 | 2,268 | `s VERIFIED UNSAT` |

For m<=6 a cup of size max(0,m-3) suffices; the needed cup triple at m6
exists by no-five-cap. Separate certificates handle7,8. The pure geometric
base excludes9 and, by heredity of its premises, every larger size. No
monotonicity of terminal selection is used. The withdrawn noncap-four-set
shortcut is explicitly refuted by a real7 control and is not used.

Current sources match the accepted generic audit. Its independent checker
functions were reused read-only as authorized; the n5/m9 base was separately
rebuilt. Both mapped terminal inputs equal their solver inputs byte-for-byte.
All streamed pre/post hashes are stable. Exact canonical real controls and
all105 four-subset triangle checks pass. Source snapshots, maps, inputs,
compressed proofs, commands, stdout/stderr and hashes are retained in data.

All jobs used one CPU, AS300 MiB, wall20/CPU19; cake heap128/stack32.
Each completed below0.05s, at most22,284KiB RSS. No owned job remains active.
No re-solve or larger heap was used. Writes only here and scratch
`/home/jay/research/data/delta3-codex-20261113/extension/terminal5-audit/`.

No obligation remains for this stated n5 closure. No n7 or novelty claim is
made. Executed reproduction commands are in data/formula.command.sh and
data/replays.command.sh; use fresh output paths to preserve this packet.
