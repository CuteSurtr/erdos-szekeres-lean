#!/usr/bin/env python3
"""Streaming version of evalcnf (for CNFs too large to load): the file is read line by line, never held in memory.
Pass 1..k: least model of the auxiliary (convexity) variables by Horn propagation in file order, repeated until a
pass adds nothing. Final pass: evaluate every clause and classify violations (T / D / K as in evalcnf)."""
import json


class StreamCNF:
    def __init__(self, path, mappath):
        self.path = path
        info = json.load(open(mappath))
        self.info = info
        self.nX = info["X_vars"]
        self.nv = info["vars"]
        self.nc = info["clauses"]
        self.triples = info["triples"]

    def triple_values(self, chi_of_labels):
        val = {}
        for a, b, c, v, s in self.triples:
            x = chi_of_labels(a, b, c)
            assert x in (1, -1)
            want = (s * x) > 0
            if v in val and val[v] != want:
                raise ValueError(f"orbit inconsistency at {(a, b, c)}")
            val[v] = want
        assert sorted(val) == list(range(1, self.nX + 1))
        return val

    def _clauses(self):
        with open(self.path) as f:
            for line in f:
                if line[0] in "cp":
                    continue
                xs = line.split()
                assert xs[-1] == "0"
                yield [int(x) for x in xs[:-1]]

    def evaluate(self, tval):
        nX = self.nX
        A = bytearray(self.nv + 1)
        for v, b in tval.items():
            A[v] = 1 if b else 0
        passes = 0
        while True:
            passes += 1
            changed = False
            for cl in self._clauses():
                heads = [l for l in cl if l > nX]
                if len(heads) != 1:
                    continue
                h = heads[0]
                if A[h]:
                    continue
                if all(not (A[abs(l)] ^ (l < 0)) for l in cl if l != h):
                    A[h] = 1
                    changed = True
            if not changed:
                break
        res = {"T": 0, "D": 0, "K": 0}
        n = 0
        for cl in self._clauses():
            n += 1
            assert sum(1 for l in cl if l > nX) <= 1, "auxiliary part not Horn"
            if any(A[abs(l)] ^ (l < 0) for l in cl):
                continue
            aux = [l for l in cl if abs(l) > nX]
            if not aux:
                res["T"] += 1
            elif any(l > 0 for l in aux):
                res["D"] += 1
            else:
                res["K"] += 1
        assert n == self.nc, (n, self.nc)
        return res, passes
