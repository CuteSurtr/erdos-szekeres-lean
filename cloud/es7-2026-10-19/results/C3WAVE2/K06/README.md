# C3WAVE2 / K06: shard 6 of 40

**Result: no roots were run. The session could not build the solver or the checkers.**

- Done: the C3-S tools worktree (132398c) at /opt/c3s. The base CNF `gen_case.py 11 7 none` gives `p cnf 168399 4154921`, sha256 `bf0e502e…dd6da`, which matches. My roots are idx ≡ 6 (mod 40), 34 roots (`roots.tsv`).
- Blocked: the session's automatic permission policy refused to clone and compile CaDiCaL (c6073042), cake_lpr (a36874a8) and drat-trim lrat-check (2e3b2dc). It gave the reason "Code from External". Without these tools `close_tree.py` cannot run, so all 34 roots are **not reached**. No SAT, no proof rejection, no memory problem, no out.jsonl.
- To resume: run this shard again in a session that allows building those three tools. Nothing here needs to be undone.
