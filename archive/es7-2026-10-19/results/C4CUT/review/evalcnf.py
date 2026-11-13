"""Evaluate a symcnf CNF under the true chirotope of a labelled real point set.
Triple variables are fixed from exact orientations via the map; the remaining (conv) variables are computed as the
least model of the (then Horn) residual formula by forward chaining. Reports every falsified clause by type."""
import json
import numpy as np
from geom import det, sgn


class CNF:
    def __init__(self, path, mappath):
        with open(path, "rb") as f:
            while True:
                h = f.readline()
                if h.startswith(b"p cnf"):
                    break
            _, _, nv, nc = h.split()
            self.nv, self.nc = int(nv), int(nc)
            data = f.read()
        arr = np.fromstring(data, dtype=np.int64, sep=" ")
        z = arr == 0
        assert z.sum() == self.nc
        cid = np.cumsum(z) - z           # clause index of each entry
        self.lits = arr[~z]
        self.cid = cid[~z]
        lens = np.bincount(self.cid, minlength=self.nc)
        assert (lens > 0).all()
        self.starts = np.concatenate([[0], np.cumsum(lens)[:-1]])
        self.lens = lens
        info = json.load(open(mappath))
        self.info = info
        self.X = info["X_vars"]
        self.triples = info["triples"]
        self.var = np.abs(self.lits)
        self.neg = self.lits < 0
        istrip = self.var <= self.X
        # clause classes
        self.all_trip = np.logical_and.reduceat(istrip, self.starts)
        self.npos_conv = np.add.reduceat((~istrip) & (~self.neg), self.starts)
        self.nneg_conv = np.add.reduceat((~istrip) & self.neg, self.starts)
        assert (self.npos_conv <= 1).all(), "non-Horn residual clause"

    def evaluate(self, lab, K=7):
        val = np.zeros(self.nv + 1, dtype=bool)
        seen = {}
        incons = 0
        for i, j, k, v, s in self.triples:
            x = sgn(det(lab[i], lab[j], lab[k]))
            assert x != 0
            b = (x * s) > 0
            if v in seen and seen[v] != b:
                incons += 1
            seen[v] = b
            val[v] = b
        assert len(seen) == self.X
        rounds = 0
        while True:
            rounds += 1
            lt = val[self.var] ^ self.neg
            sat = np.logical_or.reduceat(lt, self.starts)
            unsat = ~sat
            # heads of unsatisfied Horn clauses
            m = unsat[self.cid] & (~self.neg) & (self.var > self.X)
            newv = np.unique(self.var[m])
            if len(newv) == 0:
                break
            val[newv] = True
        res = {"symmetry_inconsistencies": incons, "rounds": rounds,
               "violated_total": int(unsat.sum()),
               "violated_triple_only": int((unsat & self.all_trip).sum()),
               "violated_Kset": int((unsat & (self.npos_conv == 0) & (self.nneg_conv == K) & (self.lens == K)).sum()),
               "conv_true": int(val[self.X + 1:].sum())}
        res["violated_other"] = res["violated_total"] - res["violated_triple_only"] - res["violated_Kset"]
        self.last_unsat = np.nonzero(unsat)[0]
        return res
