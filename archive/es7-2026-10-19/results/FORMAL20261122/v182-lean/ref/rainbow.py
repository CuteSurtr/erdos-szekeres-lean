"""Own tools for edge colourings in which every 4-cycle subgraph (chords allowed) is rainbow.

Subcommands
  graph182 OUT.json            build the omission-layer graph: 3-,4-,5-subsets of {0..7} joined by
                               inclusion of consecutive sizes; prints vertex/edge/4-cycle counts.
  small NAME OUT.json          small control graphs: K4 C4 K23 K33 Q3 PETERSEN
  cnf G.json k OUT.cnf [UNITS.json] [--proper] [--symbreak]
                               DIMACS encoding (see ENCODING below); optional units fix colours.
  decode G.json k MODEL.txt OUT.json   decode a CaDiCaL model (v-lines) into a colouring.
  check G.json COL.json [--proper]     independent check of a colouring (own cycle enumeration).
  brute G.json kmax            exact rainbow chromatic number by backtracking (small graphs only).
  notes182 diamond-colors.txt G.json OUT.json   read the notes' six-colour table into a colouring.

ENCODING (soundness argument in the README): variable x(e,c) = e*k + c + 1 means "edge e has colour c".
  (1) for every edge e: x(e,0) v ... v x(e,k-1);
  (2) for every 4-cycle subgraph Z, every two distinct edges e,f of Z and every colour c:
      -x(e,c) v -x(f,c);
  (3) --proper adds (2) also for every two edges sharing an endpoint.
  A model gives a colouring by taking the least true colour of each edge; a colouring gives a model by
  x(e,c) = [colour(e) = c].  Hence: CNF satisfiable <=> such a colouring with <= k colours exists.
"""
import sys, json, itertools


def four_cycles_by_diagonals(n, edges):
    """All 4-cycle subgraphs as frozensets of 4 edge indices: for every vertex pair {a,c} (adjacent or
    not) and every pair {b,d} of common neighbours, the cycle a-b-c-d."""
    eid = {}
    for i, (u, v) in enumerate(edges):
        eid[(u, v)] = eid[(v, u)] = i
    nb = [set() for _ in range(n)]
    for u, v in edges:
        nb[u].add(v); nb[v].add(u)
    cyc = set()
    for a in range(n):
        for c in range(a + 1, n):
            com = sorted(nb[a] & nb[c])
            for b, d in itertools.combinations(com, 2):
                cyc.add(frozenset((eid[(a, b)], eid[(b, c)], eid[(c, d)], eid[(d, a)])))
    return sorted(tuple(sorted(z)) for z in cyc)


def load(path):
    g = json.load(open(path))
    return g["n"], [tuple(e) for e in g["edges"]], g


def graph182(out):
    verts = [m for m in range(256) if bin(m).count("1") in (3, 4, 5)]
    idx = {m: i for i, m in enumerate(verts)}
    edges = []
    for m in verts:
        if bin(m).count("1") == 4:
            for x in range(8):
                edges.append((idx[m], idx[m ^ (1 << x)]))     # down to a 3-set or up to a 5-set
    z = four_cycles_by_diagonals(len(verts), edges)
    sizes = {s: sum(1 for m in verts if bin(m).count("1") == s) for s in (3, 4, 5)}
    deg = [0] * len(verts)
    for u, v in edges:
        deg[u] += 1; deg[v] += 1
    print(f"vertices {len(verts)} (3-sets {sizes[3]}, 4-sets {sizes[4]}, 5-sets {sizes[5]}), edges {len(edges)}, "
          f"4-cycles {len(z)}, degrees {sorted(set(deg))}")
    json.dump({"n": len(verts), "edges": edges, "masks": verts}, open(out, "w"))


def small(name, out):
    if name == "K4":
        n, E = 4, list(itertools.combinations(range(4), 2))
    elif name == "C4":
        n, E = 4, [(0, 1), (1, 2), (2, 3), (3, 0)]
    elif name == "K23":
        n, E = 5, [(a, b) for a in range(2) for b in range(2, 5)]
    elif name == "K33":
        n, E = 6, [(a, b) for a in range(3) for b in range(3, 6)]
    elif name == "Q3":
        n, E = 8, [(a, a ^ (1 << i)) for a in range(8) for i in range(3) if a < a ^ (1 << i)]
    elif name == "PETERSEN":
        n = 10
        E = [(i, (i + 1) % 5) for i in range(5)] + [(i, i + 5) for i in range(5)] + [(5 + i, 5 + (i + 2) % 5) for i in range(5)]
    else:
        raise SystemExit("unknown graph")
    json.dump({"n": n, "edges": E}, open(out, "w"))


def cnf(gpath, k, out, units=None, proper=False, symbreak=False, strong=False):
    n, E, g = load(gpath)
    x = lambda e, c: e * k + c + 1
    cls = set()
    for z in four_cycles_by_diagonals(n, E):
        for e, f in itertools.combinations(z, 2):
            for c in range(k):
                cls.add((-x(e, c), -x(f, c)))
    if proper:
        inc = [[] for _ in range(n)]
        for i, (u, v) in enumerate(E):
            inc[u].append(i); inc[v].append(i)
        for L in inc:
            for e, f in itertools.combinations(L, 2):
                for c in range(k):
                    cls.add((-x(min(e, f), c), -x(max(e, f), c)))
    clauses = [tuple(x(e, c) for c in range(k)) for e in range(len(E))]
    clauses += sorted(cls)
    if strong:
        # redundant clauses satisfied by every colouring written as indicators:
        # at most one colour per edge, and every colour on any k edges at a vertex that pairwise lie in
        # common 4-cycles (they need k distinct colours out of k)
        for e in range(len(E)):
            for c1, c2 in itertools.combinations(range(k), 2):
                clauses.append((-x(e, c1), -x(e, c2)))
        inc = [[] for _ in range(n)]
        for i, (u, v) in enumerate(E):
            inc[u].append(i); inc[v].append(i)
        for L in inc:
            if len(L) == k and all((-x(e, 0), -x(f, 0)) in cls for e, f in itertools.combinations(sorted(L), 2)):
                for c in range(k):
                    clauses.append(tuple(x(e, c) for e in L))
    if units:
        for e, c in json.load(open(units))["colour"].items():
            clauses.append((x(int(e), int(c)),))
    if symbreak:
        # the 5 edges at the first 3-set (pairwise in common 4-cycles) get colours 0..4
        masks = g["masks"]; first = next(i for i, m in enumerate(masks) if bin(m).count("1") == 3)
        star = [i for i, (u, v) in enumerate(E) if first in (u, v)]
        assert len(star) == 5 and k >= 5
        for c, e in enumerate(star):
            clauses.append((x(e, c),))
    with open(out, "w") as f:
        f.write(f"p cnf {len(E) * k} {len(clauses)}\n")
        for cl in clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")
    print(f"{out}: {len(E) * k} variables, {len(clauses)} clauses")


def decode(gpath, k, model, out):
    n, E, g = load(gpath)
    true = set()
    for line in open(model):
        if line.startswith("v"):
            true.update(int(t) for t in line.split()[1:] if int(t) > 0)
    col = {}
    for e in range(len(E)):
        cs = [c for c in range(k) if e * k + c + 1 in true]
        assert cs, f"edge {e} without colour"
        col[str(e)] = cs[0]
    json.dump({"colour": col}, open(out, "w"))


def check(gpath, cpath, proper=False):
    """Own check: walk every path a-b-c and every d adjacent to a and c (d != b): the four edges
    ab, bc, cd, da form a 4-cycle subgraph; their colours must be pairwise distinct."""
    n, E, g = load(gpath)
    col = {int(e): c for e, c in json.load(open(cpath))["colour"].items()}
    assert sorted(col) == list(range(len(E)))
    eid = {}
    for i, (u, v) in enumerate(E):
        eid[(u, v)] = eid[(v, u)] = i
    nb = [set() for _ in range(n)]
    for u, v in E:
        nb[u].add(v); nb[v].add(u)
    seen = set(); bad = 0
    for b in range(n):
        for a in nb[b]:
            for c in nb[b]:
                if a == c:
                    continue
                for d in nb[a] & nb[c]:
                    if d == b:
                        continue
                    es = (eid[(a, b)], eid[(b, c)], eid[(c, d)], eid[(d, a)])
                    seen.add(frozenset(es))
                    if len({col[e] for e in es}) != 4:
                        bad += 1
    if proper:
        for v in range(n):
            cs = [col[eid[(v, u)]] for u in nb[v]]
            if len(set(cs)) != len(cs):
                bad += 1
    k = len(set(col.values()))
    print(f"{'OK' if bad == 0 else 'FAIL'}: {n} vertices, {len(E)} edges, {len(seen)} four-cycles, "
          f"{k} colours used, violations {bad}{', proper' if proper else ''}")
    return bad == 0


def brute(gpath, kmax):
    n, E, g = load(gpath)
    nb = [set() for _ in range(n)]
    eid = {}
    for i, (u, v) in enumerate(E):
        eid[(u, v)] = eid[(v, u)] = i
        nb[u].add(v); nb[v].add(u)
    # conflict pairs straight from the definition (4-tuples of distinct vertices)
    conf = [set() for _ in E]
    for a, b, c, d in itertools.permutations(range(n), 4):
        if b in nb[a] and c in nb[b] and d in nb[c] and a in nb[d]:
            es = [eid[(a, b)], eid[(b, c)], eid[(c, d)], eid[(d, a)]]
            for e in es:
                conf[e].update(f for f in es if f != e)
    m = len(E); col = [-1] * m

    def bt(i, k, used):
        if i == m:
            return True
        for c in range(min(used + 1, k)):
            if all(col[f] != c for f in conf[i] if f < i):
                col[i] = c
                if bt(i + 1, k, max(used, c + 1)):
                    return True
        col[i] = -1
        return False
    for k in range(1, kmax + 1):
        if bt(0, k, 0):
            print(f"rainbow chromatic number = {k} (brute force)")
            return k
    print(f"> {kmax}")


def notes182(table, gpath, out):
    n, E, g = load(gpath)
    masks = g["masks"]; idx = {m: i for i, m in enumerate(masks)}
    eid = {}
    for i, (u, v) in enumerate(E):
        eid[(u, v)] = eid[(v, u)] = i
    tok = open(table).read().split()
    col = {}
    for p in range(56):
        tri, lo, up = int(tok[3 * p]), tok[3 * p + 1], tok[3 * p + 2]
        assert bin(tri).count("1") == 3
        outside = [x for x in range(8) if not tri >> x & 1]
        for pos, x in enumerate(outside):
            a = tri | (1 << x)
            col[str(eid[(idx[a], idx[tri])])] = int(lo[pos])                 # edge tri - (tri+x)
            col[str(eid[(idx[255 ^ a], idx[255 ^ tri])])] = int(up[pos])     # edge comp(tri+x) - comp(tri)
    assert len(tok) == 168 and len(col) == len(E)
    json.dump({"colour": col}, open(out, "w"))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "graph182":
        graph182(a[1])
    elif a[0] == "small":
        small(a[1], a[2])
    elif a[0] == "cnf":
        units = next((v for v in a[4:] if not v.startswith("--")), None)
        cnf(a[1], int(a[2]), a[3], units, "--proper" in a, "--symbreak" in a, "--strong" in a)
    elif a[0] == "decode":
        decode(a[1], int(a[2]), a[3], a[4])
    elif a[0] == "check":
        sys.exit(0 if check(a[1], a[2], "--proper" in a) else 1)
    elif a[0] == "brute":
        brute(a[1], int(a[2]))
    elif a[0] == "notes182":
        notes182(a[1], a[2], a[3])
