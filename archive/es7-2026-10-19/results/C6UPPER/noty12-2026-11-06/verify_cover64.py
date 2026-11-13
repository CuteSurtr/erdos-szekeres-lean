#!/usr/bin/env python3
"""verify_cover64.py BASE.cnf META.json NEWDIR REPLAYCUBEDIR REPLAY_RESULTS.tsv : stdlib-only check that the 64 cubes
cover the encoder-B base formula.
(1) every cube file (n*.cnf in NEWDIR, c*.cnf in REPLAYCUBEDIR) = header(nv, nc+6) + exact body of BASE + 6 unit clauses;
(2) the first unit is -Y(1,2) for n-cubes and +Y(1,2) for c-cubes, the other five are one sign pattern on
    Y(1,3),Y(1,4),Y(2,3),Y(2,4),Y(3,4) in this order, and the file name spells the pattern;
(3) every c-cube's SHA-256 equals the cnf_sha256 of an ACCEPTED encoder-B row for that cube in the replay results;
(4) the 64 sign patterns on (Y(1,2), Y(1,3), ..., Y(3,4)) are pairwise distinct, so they are all 2^6 of them.
Then: if all 64 cubes are UNSAT, BASE is UNSAT (every assignment satisfies the units of exactly one cube)."""
import sys, json, os, hashlib


def check(cond, msg):
    """explicit check (not `assert`), so that `python3 -O` cannot skip it"""
    if not cond:
        sys.exit('FAIL: %s' % msg)


base, meta, newdir, repdir, reptsv = sys.argv[1:6]
Y = json.load(open(meta))['Y']
y12 = Y['1,2']; cv = [Y[k] for k in ('1,3', '1,4', '2,3', '2,4', '3,4')]
raw = open(base, 'rb').read()
hdr, body = raw.split(b'\n', 1)
p, c, nv, nc = hdr.split(); nc = int(nc)
check((p, c) == (b'p', b'cnf'), 'base header')
check(body.endswith(b'\n'), 'base body must end with a newline')
print('base sha256', hashlib.sha256(raw).hexdigest(), 'nv', int(nv), 'nc', nc)

accepted = {}
for l in open(reptsv):
    f = l.rstrip('\n').split('\t')
    if len(f) > 8 and f[0] == 'B' and f[8] == 'ACCEPTED' and f[9] == 's VERIFIED UNSAT':
        accepted[f[1]] = f[2]
check(len(accepted) == 32, 'replay has %d accepted encoder-B rows, want 32' % len(accepted))

seen = {}
for d, prefix, sign in ((newdir, 'n', -1), (repdir, 'c', +1)):
    names = sorted(f for f in os.listdir(d) if f.startswith(prefix) and f.endswith('.cnf'))
    check(len(names) == 32, '%s: %d %s*.cnf files, want 32' % (d, len(names), prefix))
    for f in names:
        r = open(os.path.join(d, f), 'rb').read()
        h, rest = r.split(b'\n', 1)
        check(rest.startswith(body), '%s: body differs from base' % f)
        tail = rest[len(body):].decode().split('\n')
        check(tail[-1] == '', '%s: no final newline' % f)
        lines = tail[:-1]
        check(len(lines) == 6, '%s: %d unit lines' % (f, len(lines)))
        units = []
        for l in lines:
            t = l.split(' ')
            check(len(t) == 2 and t[1] == '0' and t[0].lstrip('-').isdigit(), '%s: bad unit line %r' % (f, l))
            units.append(int(t[0]))
        check(h.split(b' ') == [b'p', b'cnf', nv, str(nc + 6).encode()], '%s: header %r' % (f, h))
        check(units[0] == sign * y12, '%s: first unit %d' % (f, units[0]))
        check([abs(u) for u in units[1:]] == cv, '%s: pattern variables' % f)
        bits = tuple(1 if u > 0 else 0 for u in units[1:])
        check(f == prefix + ''.join(map(str, bits)) + '.cnf', '%s: name does not match pattern' % f)
        if prefix == 'c':
            got = hashlib.sha256(r).hexdigest()
            check(accepted.get(f[:-4]) == got, '%s: sha %s is not an accepted replay row' % (f, got))
        key = (1 if sign > 0 else 0,) + bits
        check(key not in seen, '%s: duplicate pattern with %s' % (f, seen.get(key)))
        seen[key] = f
check(len(seen) == 64, len(seen))
print('OK: 32 n-cubes (base + -Y(1,2) + pattern) and 32 replayed c-cubes (hashes = accepted rows); '
      '64 distinct patterns on 6 variables; cover complete')
