#!/usr/bin/env python3
"""Evaluate a symcnf-style CNF on a labelled real configuration (audit A4; independent of project test code).

- Triple variables (1..X_vars) are set from exact orientations via the map file (sorted triple -> (var, sign) with
  chi(sorted) = sign * value(var)); every member of a triple orbit must give the same value (checks the symmetric
  identification against the geometry).
- The remaining variables are the encoder's auxiliary convexity variables. With the triples fixed, every clause
  containing one must be Horn in them (asserted); the least model is computed by fixpoint propagation. The CNF is
  satisfiable with these triple values iff the least model satisfies every clause, so this is a complete test.
- Clauses are classified: T = only triple variables (axioms, centre facts, normal-form units),
  D = definitional (one positive auxiliary literal), K = all-negative auxiliary clauses (the K-set clauses).
"""
import json
import numpy as np


class CNF:
    def __init__(self, path, mappath):
        with open(path) as f:
            text = []
            nv = nc = None
            for line in f:
                if line.startswith("c"):
                    continue
                if line.startswith("p"):
                    _, _, nv, nc = line.split()
                    nv, nc = int(nv), int(nc)
                    break
            rest = f.read()
        arr = np.array(rest.split(), dtype=np.int64)
        zeros = np.flatnonzero(arr == 0)
        assert len(zeros) == nc, (len(zeros), nc)
        self.nv, self.nc = nv, nc
        ends = zeros
        starts = np.concatenate([[0], zeros[:-1] + 1])
        mask = np.ones(len(arr), bool)
        mask[zeros] = False
        self.lits = arr[mask]
        # starts/ends in the compressed literal array
        lens = ends - starts
        assert (lens > 0).all(), "empty clause"
        self.starts = np.concatenate([[0], np.cumsum(lens)[:-1]])
        self.lens = lens
        self.cid = np.repeat(np.arange(nc), lens)          # clause index of each literal
        info = json.load(open(mappath))
        self.info = info
        self.nX = info["X_vars"]
        self.m, self.t, self.P = info["m"], info["t"], info["P"]
        self.center = info["center_index"]
        self.triples = info["triples"]
        v = np.abs(self.lits)
        aux = v > self.nX
        pos_aux = aux & (self.lits > 0)
        n_aux = np.add.reduceat(aux.astype(np.int64), self.starts)
        n_pos_aux = np.add.reduceat(pos_aux.astype(np.int64), self.starts)
        assert (n_pos_aux <= 1).all(), "auxiliary part is not Horn"
        self.cls = np.where(n_aux == 0, 0, np.where(n_pos_aux == 1, 1, 2))   # 0 = T, 1 = D, 2 = K
        self.head_lit = pos_aux                              # the unique positive auxiliary literal of D clauses
        self.counts = {c: int((self.cls == i).sum()) for i, c in enumerate("TDK")}

    def triple_values(self, chi_of_labels):
        """chi_of_labels(a, b, c) -> exact orientation of labelled points a < b < c; returns value array (bool) for
        variables 1..nX, or raises on an inconsistent orbit"""
        val = {}
        for a, b, c, v, s in self.triples:
            x = chi_of_labels(a, b, c)
            assert x in (1, -1), ("degenerate triple", a, b, c)
            want = (s * x) > 0
            if v in val:
                if val[v] != want:
                    raise ValueError(f"orbit inconsistency at triple {(a, b, c)} var {v}")
            else:
                val[v] = want
        assert sorted(val) == list(range(1, self.nX + 1))
        return val

    def evaluate(self, tval):
        A = np.zeros(self.nv + 1, bool)
        for v, b in tval.items():
            A[v] = b
        v = np.abs(self.lits)
        neg = self.lits < 0
        D = self.cls == 1
        Dlit = D[self.cid]
        body = Dlit & ~self.head_lit
        head_idx = np.flatnonzero(Dlit & self.head_lit)
        head_var = v[head_idx]
        head_cl = self.cid[head_idx]
        for it in range(50):
            lt = A[v] ^ neg
            # a D clause fires when every body literal is false
            body_true = np.zeros(self.nc, np.int64)
            np.add.at(body_true, self.cid[body], lt[body].astype(np.int64))
            fire = body_true[head_cl] == 0
            newv = head_var[fire]
            before = A[newv].copy()
            A[newv] = True
            if before.all():
                break
        else:
            raise RuntimeError("no fixpoint")
        lt = A[v] ^ neg
        sat = np.add.reduceat(lt.astype(np.int64), self.starts) > 0
        bad = np.flatnonzero(~sat)
        res = {"T": 0, "D": 0, "K": 0}
        for i in bad:
            res["TDK"[self.cls[i]]] += 1
        return res, bad

    def clause(self, i):
        s = self.starts[i]
        return [int(x) for x in self.lits[s:s + self.lens[i]]]
