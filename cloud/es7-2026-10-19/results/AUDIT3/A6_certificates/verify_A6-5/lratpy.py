#!/usr/bin/env python3
"""Small, strict, independent LRAT checker (RUP steps only), written for the A6-5 check so that the c3hex proofs are
accepted by a second checker other than drat-trim's lrat-check (cake_lpr may not be run in this audit).

Semantics checked:
  * the DIMACS formula: header 'p cnf V M', exactly M clauses, every literal in 1..V; clause ids 1..M in file order;
  * each addition line 'id l1 .. lk 0 h1 .. hn 0': id strictly larger than every id used so far, every literal in 1..V
    (no extension variables), every hint positive (a negative hint = RAT step -> reported as unsupported, rejected);
    RUP: start from the assignment that falsifies l1..lk; walk the hints in order; each hint must name a live clause;
    under the current assignment the clause must have no true literal and at most one unassigned literal; with one
    unassigned literal it is made true; with none the step ends in a conflict, which must happen at the last hint
    (strict, as lrat-check does: extra hints after the conflict are rejected);
  * each deletion line 'id d i1 .. in 0': every deleted id must be live (deleted clauses can no longer be used);
  * the result is accepted only if an addition of the empty clause was verified.
Usage: python3 -I lratpy.py FORMULA.cnf PROOF.lrat
"""
import sys

def die(msg):
    print("s REJECTED:", msg)
    sys.exit(1)

def main():
    cnf, prf = sys.argv[1], sys.argv[2]
    db = {}
    nv = nc = None
    cur = []
    nid = 0
    with open(cnf) as f:
        for line in f:
            if not line.strip() or line[0] == "c":
                continue
            if line[0] == "p":
                t = line.split()
                if nv is not None or t[:2] != ["p", "cnf"] or len(t) != 4:
                    die("bad header " + line.strip())
                nv, nc = int(t[2]), int(t[3])
                continue
            if nv is None:
                die("clause before header")
            for x in map(int, line.split()):
                if x == 0:
                    nid += 1
                    db[nid] = tuple(cur)
                    cur = []
                else:
                    if not (1 <= abs(x) <= nv):
                        die(f"literal {x} out of range in formula")
                    cur.append(x)
    if cur:
        die("unterminated last clause in formula")
    if nid != nc:
        die(f"header says {nc} clauses, file has {nid}")
    print(f"c formula: {nv} variables, {nc} clauses")

    val = [0] * (nv + 1)  # 0 unassigned, +1 true, -1 false (for the variable)
    last_id = nc
    n_add = n_del = n_hint = 0
    empty_ok = False
    with open(prf) as f:
        for lineno, line in enumerate(f, 1):
            t = line.split()
            if not t or t[0] == "c":
                continue
            sid = int(t[0])
            if t[1] == "d":
                ids = list(map(int, t[2:]))
                if ids[-1] != 0:
                    die(f"line {lineno}: deletion not terminated by 0")
                for i in ids[:-1]:
                    if i not in db:
                        die(f"line {lineno}: deleting id {i} which is not live")
                    del db[i]
                    n_del += 1
                continue
            nums = list(map(int, t[1:]))
            try:
                z = nums.index(0)
            except ValueError:
                die(f"line {lineno}: no 0 after literals")
            lits = nums[:z]
            hints = nums[z + 1:]
            if not hints or hints[-1] != 0:
                die(f"line {lineno}: hints not terminated by 0")
            hints = hints[:-1]
            if 0 in hints:
                die(f"line {lineno}: stray 0 in hints")
            if sid <= last_id:
                die(f"line {lineno}: id {sid} not larger than previous id {last_id}")
            if sid in db:
                die(f"line {lineno}: id {sid} reused")
            for x in lits:
                if not (1 <= abs(x) <= nv):
                    die(f"line {lineno}: literal {x} out of range (extension variables not supported)")
            if any(h < 0 for h in hints):
                die(f"line {lineno}: negative hint (RAT step) -- unsupported by this checker")
            # RUP check
            trail = []
            taut = False
            for x in lits:
                v = abs(x)
                want = -1 if x > 0 else 1   # falsify x
                if val[v] == 0:
                    val[v] = want
                    trail.append(v)
                elif val[v] != want:
                    taut = True              # lemma contains x and -x: trivially implied
            ok = taut
            if not taut:
                for k, h in enumerate(hints):
                    c = db.get(h)
                    if c is None:
                        for v in trail: val[v] = 0
                        die(f"line {lineno}: hint {h} is not a live clause")
                    unassigned = None
                    nun = 0
                    for x in c:
                        s = val[abs(x)]
                        if s == 0:
                            nun += 1
                            unassigned = x
                            if nun > 1:
                                break
                        elif (s > 0) == (x > 0):
                            for v in trail: val[v] = 0
                            die(f"line {lineno}: hint {h} has a true literal")
                    if nun > 1:
                        for v in trail: val[v] = 0
                        die(f"line {lineno}: hint {h} is not unit (>1 unassigned literals)")
                    if nun == 1:
                        v = abs(unassigned)
                        val[v] = 1 if unassigned > 0 else -1
                        trail.append(v)
                    else:  # conflict
                        if k != len(hints) - 1:
                            for v in trail: val[v] = 0
                            die(f"line {lineno}: conflict at hint {k + 1} of {len(hints)} (extra hints)")
                        ok = True
                        break
            for v in trail:
                val[v] = 0
            if not ok:
                die(f"line {lineno}: hints exhausted without conflict (lemma id {sid})")
            db[sid] = tuple(lits)
            last_id = sid
            n_add += 1
            n_hint += len(hints)
            if not lits:
                empty_ok = True
                print(f"c empty clause verified at line {lineno}, id {sid}")
                break
    print(f"c additions {n_add}, deletions {n_del}, hints {n_hint}")
    if not empty_ok:
        die("no empty clause derived")
    print("s VERIFIED (RUP-only LRAT, independent Python checker)")

if __name__ == "__main__":
    main()
