"""Re-derive the static clause blocks with the uncached builder and compare with the cached files used by
template certification.  usage: static_check.py n1 n2 ..."""
import sys, hashlib, coupled5, os
for n in map(int, sys.argv[1:]):
    cnf = coupled5.CNF(list(range(n)))
    cls = [c for c, t in zip(cnf.clauses, cnf.tags) if t is None]
    body = ''.join(' '.join(map(str, c)) + ' 0\n' for c in cls)
    nv, nc, cbody = coupled5._static(n)
    print(n, 'fresh', cnf.nv, len(cls), hashlib.sha256(body.encode()).hexdigest()[:16], 'cached', nv, nc, hashlib.sha256(cbody.encode()).hexdigest()[:16], 'MATCH' if (nv, nc, cbody) == (cnf.nv, len(cls), body) else 'DIFF')
