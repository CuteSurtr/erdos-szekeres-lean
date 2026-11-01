#!/usr/bin/env python3
"""Chunked streaming evaluator (numpy) for large symcnf CNFs (audit A4). The file is read in ~16 MB pieces cut at line
boundaries; never held whole in memory. Least model of the auxiliary variables by repeated passes (each pass
propagates the Horn clauses chunk by chunk) until a pass adds nothing; then a final pass classifies the violated
clauses as T (no auxiliary variable), D (one positive auxiliary literal) or K (only negative auxiliary literals)."""
import json, warnings
import numpy as np

warnings.simplefilter("ignore", DeprecationWarning)


class ChunkCNF:
    def __init__(self, path, mappath, chunk=1 << 24):
        self.path, self.chunk = path, chunk
        info = json.load(open(mappath))
        self.nX, self.nv, self.nc = info["X_vars"], info["vars"], info["clauses"]
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

    def _chunks(self):
        with open(self.path, "rb") as f:
            while True:
                pos = f.tell()
                line = f.readline()
                if not line:
                    return
                if line[:1] in (b"c", b"p"):
                    continue
                f.seek(pos)
                break
            rem = b""
            while True:
                b = f.read(self.chunk)
                if not b:
                    if rem.strip():
                        yield np.fromstring(rem, dtype=np.int64, sep=" ")
                    return
                b = rem + b
                cut = b.rfind(b"\n") + 1
                rem = b[cut:]
                if cut:
                    yield np.fromstring(b[:cut], dtype=np.int64, sep=" ")

    @staticmethod
    def _split(arr):
        zeros = np.flatnonzero(arr == 0)
        starts = np.concatenate([[0], zeros[:-1] + 1])
        lens = zeros - starts
        mask = np.ones(len(arr), bool)
        mask[zeros] = False
        lits = arr[mask]
        cstarts = np.concatenate([[0], np.cumsum(lens)[:-1]])
        cid = np.repeat(np.arange(len(lens)), lens)
        return lits, cstarts, lens, cid

    def evaluate(self, tval):
        nX = self.nX
        A = np.zeros(self.nv + 1, bool)
        for v, b in tval.items():
            A[v] = b
        passes = 0
        while True:
            passes += 1
            changed = False
            for arr in self._chunks():
                lits, cst, lens, cid = self._split(arr)
                v = np.abs(lits)
                posaux = lits > nX
                npos = np.add.reduceat(posaux.astype(np.int64), cst)
                assert (npos <= 1).all(), "not Horn"
                isD = npos == 1
                lt = A[v] ^ (lits < 0)
                body = isD[cid] & ~posaux
                bt = np.zeros(len(lens), np.int64)
                np.add.at(bt, cid[body], lt[body].astype(np.int64))
                hidx = np.flatnonzero(isD[cid] & posaux)
                fire = bt[cid[hidx]] == 0
                hv = v[hidx[fire]]
                if hv.size and not A[hv].all():
                    A[hv] = True
                    changed = True
            if not changed:
                break
        res = {"T": 0, "D": 0, "K": 0}
        n = 0
        for arr in self._chunks():
            lits, cst, lens, cid = self._split(arr)
            n += len(lens)
            v = np.abs(lits)
            aux = v > nX
            lt = A[v] ^ (lits < 0)
            sat = np.add.reduceat(lt.astype(np.int64), cst) > 0
            naux = np.add.reduceat(aux.astype(np.int64), cst)
            npos = np.add.reduceat((lits > nX).astype(np.int64), cst)
            bad = ~sat
            res["T"] += int((bad & (naux == 0)).sum())
            res["D"] += int((bad & (npos == 1)).sum())
            res["K"] += int((bad & (naux > 0) & (npos == 0)).sum())
        assert n == self.nc, (n, self.nc)
        return res, passes
