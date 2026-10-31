#!/usr/bin/env python3
"""C3AUDIT2: own check of the H6M corollary on the option level and of the column h6m_kept.
(1) For m = 7, 9, 11 and every H6(a, s): the layer-2 options (one orbit r, or two orbits {r1, r2}
    with both sigma values, residues not in {0, a}), phi maps options to options, phi is an
    involution, key is injective, and keep(O) := key(O) <= key(phi(O)) keeps exactly one option of
    every phi-pair (both of a self-mirror one): O or phi(O) is kept, and both only if O = phi(O).
(2) For every row of the given lists: parse the node name, recompute keep(L2) and compare with
    column h6m_kept.  key(O) = sorted tuple of (r, -1 if one orbit else sigma), as h3_layer2_kept.
usage: check_kept.py LIST.tsv ...   (prints a JSON summary)"""
import csv
import itertools
import json
import sys


def options(m, a):
    rem = [r for r in range(1, m) if r != a]
    out = [((r, None),) for r in rem]
    for r1, r2 in itertools.combinations(rem, 2):
        for g1 in (0, 1):
            for g2 in (0, 1):
                out.append(((r1, g1), (r2, g2)))
    return out


def phi(O, m, a, s):
    return tuple(sorted(((a - r) % m, None if g is None else g ^ int(r < a) ^ int(s == 0)) for r, g in O))


def key(O):
    return tuple(sorted((r, -1 if g is None else g) for r, g in O))


def keep(O, m, a, s):
    return key(O) <= key(phi(O, m, a, s))


def option_level():
    rows = []
    for m in (7, 9, 11):
        for a in range(1, m // 2 + 1):
            for s in (0, 1):
                opts = options(m, a)
                S = set(opts)
                assert len(S) == len(opts)
                assert len({key(o) for o in opts}) == len(opts), "key injective"
                for o in opts:
                    p = phi(o, m, a, s)
                    assert p in S, ("phi leaves the options", m, a, s, o, p)
                    assert phi(p, m, a, s) == o, "involution"
                    ko, kp = keep(o, m, a, s), keep(p, m, a, s)
                    assert ko or kp, "pair uncovered"
                    assert not (ko and kp) or o == p, "both kept"
                kept = [o for o in opts if keep(o, m, a, s)]
                rows.append({"m": m, "a": a, "s": s, "options": len(opts), "kept": len(kept),
                             "kept_one": sum(len(o) == 1 for o in kept), "kept_two": sum(len(o) == 2 for o in kept),
                             "self": sum(phi(o, m, a, s) == o for o in opts)})
    return rows


def parse(name):
    lays = []
    for lay in name.split("_"):
        L = []
        for tok in lay.split("-"):
            if "s" in tok:
                r, g = tok.split("s")
                L.append((int(r), int(g)))
            else:
                L.append((int(tok), None))
        lays.append(tuple(L))
    return lays


def main():
    out = {"option_level": option_level(), "lists": {}}
    for path in sys.argv[1:]:
        st = {"rows": 0, "agree": 0, "disagree": [], "names": 0}
        names = set()
        with open(path) as f:
            for row in csv.DictReader(f, delimiter="\t"):
                st["rows"] += 1
                lays = parse(row["node"])
                assert len(lays) == 2 and lays[0][0] == (0, 0) and len(lays[0]) == 2, row["node"]
                a, s = lays[0][1]
                assert 1 <= a <= 5 and row["stratum"].startswith(f"H6({a},{s})/"), row
                O = tuple(sorted(lays[1]))
                assert O in set(options(11, a)), row["node"]
                want = "yes" if keep(O, 11, a, s) else "no"
                names.add(row["node"])
                if row["h6m_kept"] == want:
                    st["agree"] += 1
                else:
                    st["disagree"].append((row["node"], row["h6m_kept"], want))
        st["names"] = len(names)
        out["lists"][path] = st
    print(json.dumps(out))


if __name__ == "__main__":
    main()
