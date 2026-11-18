# Restricted no-six-cup14 append audit — PASS

**COMPUTED:** all3,003 negative20-triple clauses,60,060 literals and the
unchanged exact base match independent reconstruction. **PROVED (written):**
the added family means exactly **no six-cup**, as explained in
[VERIFY_CUP_BOUND14.md](VERIFY_CUP_BOUND14.md).

The final file has32,086vars/234,616rows/683,300lits, SHA-256
`614a810468d31b194293128c0c56fcf79d92230d7712fbfcd5fb610eb4c81a34`.
All231,613 old rows remain unchanged; no cut exclusions or new variables
are added. Source/map/output hashes are stable before/after.

Boolean controls pass. A real14-point no-six-cup control with246 hexagons
satisfies every added row; a valid geometric14-point control with14
six-cups violates exactly those14 rows. Both have independently checked
terminal selectors. Full evidence and commands are in data/.

An accepted matching UNSAT proof would concern only no5cap/no6cup/no7gon
sets of size14. It would not settle unrestricted m14 or the six-cup-present
branch. No proof was replayed here. AS300/one CPU only,0.395s/25,116KiB;
no extra allocation or job remains. Old frozen packets are unchanged.

The preserved workflow is data/run.command.sh; reruns require new exclusive
output files. Proof replays remain subject to separate resource coordination.
