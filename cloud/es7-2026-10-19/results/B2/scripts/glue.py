#!/usr/bin/env python3
"""ETV gluing of a rung model into a larger signotope, by "deep below" composition.

compose(A, B, order): A deep below B (every point of B above every line through two points
of A and vice versa), with x-interleaving given by `order` (a string over {A, B}). For a
mixed triple in x-order:
    one A point, two B points: cup (ccw, +1) iff the A point is the middle one, else cap;
    two A points, one B point: cap (cw, -1) iff the B point is the middle one, else cup.
(These are the orientations of a point set with A squeezed far below B.)
By the lemma "a mixed subset is convex iff its A-part is a cup and its B-part is a cap":

  rung (7,5,7), S with no 5-cap, no 7-gon:            6-cap deep below-left of S.
  rung (7,5,6), S with no 5-cap, no 6-cup, no 7-gon:   5-cap C deep below-left of S -> T;
          point p deep below T, leftmost -> T'; point q deep above T', rightmost.
  rung (7,6,6), S with no 6-cap, no 6-cup, no 7-gon:   point p deep below S, leftmost;
          point q deep above, rightmost.
The output is checked separately by brute force (sigcheckB with k = 7); nothing here is
trusted beyond that check.

usage: glue.py rung N model.txt out.txt     (rung in 757, 756, 766; model = literal list)
"""
import itertools, sys


def read_model(path, N):
    nX = N * (N - 1) * (N - 2) // 6
    val = {}
    for tok in open(path).read().split():
        try:
            l = int(tok)
        except ValueError:
            continue
        if l and abs(l) <= nX:
            val[abs(l)] = 1 if l > 0 else -1
    sig = {}
    for n, t in enumerate(itertools.combinations(range(N), 3)):
        sig[t] = val[n + 1]
    return sig


def const_sig(n, s):
    return {t: s for t in itertools.combinations(range(n), 3)}


def compose(A, nA, B, nB, order):
    assert order.count("A") == nA and order.count("B") == nB
    lab, ia, ib = [], 0, 0
    for c in order:
        if c == "A":
            lab.append(("A", ia)); ia += 1
        else:
            lab.append(("B", ib)); ib += 1
    n = nA + nB
    sig = {}
    for t in itertools.combinations(range(n), 3):
        L = [lab[x] for x in t]
        kinds = [x[0] for x in L]
        if kinds.count("A") == 3:
            sig[t] = A[tuple(x[1] for x in L)]
        elif kinds.count("B") == 3:
            sig[t] = B[tuple(x[1] for x in L)]
        elif kinds.count("A") == 1:
            sig[t] = +1 if kinds[1] == "A" else -1
        else:
            sig[t] = -1 if kinds[1] == "B" else +1
    return sig, n


def write_model(sig, n, path):
    lits = []
    for idx, t in enumerate(itertools.combinations(range(n), 3)):
        lits.append(idx + 1 if sig[t] > 0 else -(idx + 1))
    open(path, "w").write(" ".join(map(str, lits)) + "\n")


def main():
    rung, N, inp, outp = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    S = read_model(inp, N)
    if rung == "757":
        G, n = compose(const_sig(6, -1), 6, S, N, "A" * 6 + "B" * N)
    elif rung == "756":
        T, nT = compose(const_sig(5, -1), 5, S, N, "A" * 5 + "B" * N)
        T2, nT2 = compose(const_sig(1, -1), 1, T, nT, "A" + "B" * nT)
        G, n = compose(T2, nT2, const_sig(1, -1), 1, "A" * nT2 + "B")
    elif rung == "766":
        T2, nT2 = compose(const_sig(1, -1), 1, S, N, "A" + "B" * N)
        G, n = compose(T2, nT2, const_sig(1, -1), 1, "A" * nT2 + "B")
    else:
        raise SystemExit("unknown rung")
    write_model(G, n, outp)
    print(n)


if __name__ == "__main__":
    main()
