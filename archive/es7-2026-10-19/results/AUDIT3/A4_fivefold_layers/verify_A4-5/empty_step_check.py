#!/usr/bin/env python3
"""Streaming check of the empty-clause step(s) of the archived C4CUT LRAT proof (standard library only).

Never holds the CNF or the proof in memory: both are decompressed with `zstd -dc` and read in 16 MB chunks.

Pass 1 (proof): SHA-256 and byte count of the decompressed proof; every addition line whose clause is empty
                ("<id> 0 <hints> 0"); counts of lines, deletion lines and additions with negative (RAT) hints.
Pass 2 (proof): the literal lists of every lemma used as a hint by an empty-clause step.
Pass 3 (CNF):   SHA-256 and clause count of the decompressed CNF; the original clauses used as hints.
Replay:         for each empty-clause step, unit propagation over its hints in the given order, with the semantics
                of lrat-check's checkRedundancy (skip falsified literals; two non-falsified -> FAILED; none ->
                CONFLICT; one -> make it true).

If every empty-clause step reaches CONFLICT, the patched and unpatched lrat-check builds take the same branch on
this proof (they differ only when an empty clause's RUP hints end without a conflict, E2 §2), so the recorded
"c VERIFIED" does not depend on which build produced it.

usage: empty_step_check.py PROOF.zst CNF.zst OUT.json
"""
import hashlib, json, re, subprocess, sys, time

CH = 1 << 24


def lines_of(path, hasher=None, counter=None):
    """Yield complete lines (without newline); optionally hash the raw bytes."""
    p = subprocess.Popen(["zstd", "-dc", "-q", path], stdout=subprocess.PIPE)
    carry = b""
    while True:
        b = p.stdout.read(CH)
        if not b:
            break
        if hasher is not None:
            hasher.update(b)
        if counter is not None:
            counter[0] += len(b)
        b = carry + b
        parts = b.split(b"\n")
        carry = parts.pop()
        yield from parts
    if carry:
        yield carry
    p.stdout.close()
    if p.wait() != 0:
        raise SystemExit(f"zstd failed on {path}")


def main():
    proof, cnf, out = sys.argv[1:4]
    t0 = time.time()
    res = {"proof_archive": proof, "cnf_archive": cnf}

    # ---- pass 1: proof hash, empty-clause steps, RAT hints
    h = hashlib.sha256(); nbytes = [0]
    n_lines = n_del = n_add = n_rat = 0
    empties = []          # (line_no, id, hints)
    first_id = last_id = None
    for ln, line in enumerate(lines_of(proof, h, nbytes), 1):
        n_lines = ln
        if not line:
            continue
        sp = line.find(b" ")
        if line[sp + 1:sp + 3] == b"d ":
            n_del += 1
            continue
        n_add += 1
        cid = int(line[:sp])
        if first_id is None:
            first_id = cid
        last_id = cid
        # end of the literal list: the first token "0" after the id
        if line[sp + 1:sp + 3] == b"0 ":
            k = sp + 1
        else:
            k = line.find(b" 0 ", sp)
            if k < 0:
                raise SystemExit(f"malformed line {ln}")
            k += 1
        hint_part = line[k + 2:]
        if b"-" in hint_part:
            n_rat += 1
        if k == sp + 1:  # empty clause
            toks = hint_part.split()
            assert toks[-1] == b"0", f"line {ln}: hints not 0-terminated"
            empties.append((ln, cid, [int(t) for t in toks[:-1]]))
    res.update(proof_sha256=h.hexdigest(), proof_bytes=nbytes[0], proof_lines=n_lines, addition_lines=n_add,
               deletion_lines=n_del, additions_with_negative_hints=n_rat, first_lemma_id=first_id,
               last_lemma_id=last_id,
               empty_clause_steps=[{"line": a, "id": b, "n_hints": len(c), "hints_head": c[:8], "hints_tail": c[-4:]}
                                   for a, b, c in empties])
    print(f"pass 1 done in {time.time() - t0:.0f} s: {n_lines} lines, {len(empties)} empty-clause step(s)",
          flush=True)

    need = set()
    for _, _, hs in empties:
        need.update(x for x in hs if x > 0)

    # ---- pass 3 first (CNF): needed original clauses, hash, count
    hc = hashlib.sha256(); cbytes = [0]
    orig = {}; n_cls = 0; header = None
    for line in lines_of(cnf, hc, cbytes):
        if not line or line[:1] == b"c":
            continue
        if line[:1] == b"p":
            header = line.decode(); continue
        n_cls += 1
        if n_cls in need:
            toks = line.split()
            assert toks[-1] == b"0", "clause spans lines"
            orig[n_cls] = [int(t) for t in toks[:-1]]
    res.update(cnf_sha256=hc.hexdigest(), cnf_bytes=cbytes[0], cnf_header=header, cnf_clause_lines=n_cls)
    print(f"CNF pass done at {time.time() - t0:.0f} s: {n_cls} clauses", flush=True)

    # ---- pass 2: needed lemmas
    lem = {}
    need_lem = {x for x in need if x > n_cls}
    deleted_before_use = set()
    if need_lem:
        last_empty_line = max(a for a, _, _ in empties)
        for ln, line in enumerate(lines_of(proof), 1):
            if not line:
                continue
            sp = line.find(b" ")
            if line[sp + 1:sp + 3] == b"d ":
                continue
            cid = int(line[:sp])
            if cid in need_lem:
                k = 0 if line[sp + 1:sp + 3] == b"0 " else line.find(b" 0 ", sp) - sp
                lits = line[sp + 1:sp + 1 + k].split() if k > 0 else []
                lem[cid] = [int(t) for t in lits]
            if ln > last_empty_line:
                break
    print(f"lemma pass done at {time.time() - t0:.0f} s: {len(lem)} of {len(need_lem)} hinted lemmas found",
          flush=True)

    # ---- replay
    replays = []
    for ln, cid, hs in empties:
        false = set()   # falsified literals
        status = None; at = None; detail = []
        for i, x in enumerate(hs):
            if x < 0:
                status = "RAT_HINT"; at = i; break
            cl = orig.get(x) if x <= n_cls else lem.get(x)
            if cl is None:
                status = f"MISSING_HINT {x}"; at = i; break
            if len(cl) == 0:
                status = f"HINT_IS_EMPTY_CLAUSE {x}"; at = i; break
            nf = [l for l in cl if l not in false]
            if len(nf) >= 2:
                status = f"FAILED multiple unassigned in hint {x}"; at = i; break
            if len(nf) == 0:
                status = "CONFLICT"; at = i; break
            false.add(-nf[0])
            detail.append((x, "orig" if x <= n_cls else "lemma", len(cl)))
        if status is None:
            status = "NO_CONFLICT"
        replays.append({"line": ln, "id": cid, "n_hints": len(hs), "status": status, "conflict_at_hint_index": at,
                        "hints_from_cnf": sum(1 for x in hs if 0 < x <= n_cls),
                        "hints_from_lemmas": sum(1 for x in hs if x > n_cls),
                        "units_propagated": len(false)})
    res["replays"] = replays
    res["elapsed_s"] = round(time.time() - t0, 1)
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
