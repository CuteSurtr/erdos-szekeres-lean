"""Independent exact re-verification of stored non-realizability certificates (written separately from bfp.py).
A certificate is a list of items (a, b, c, d, e, odd, other, mult).  For the Grassmann-Pluecker relation
  [abc][ade] - [abd][ace] + [abe][acd] = 0
term number 'odd' (0, 1, 2) must have the sign opposite to the two other signed terms, so that
|term_odd| > |term_other|; the certificate is valid iff all multipliers are positive integers and
sum mult * (log|term_odd| - log|term_other|) vanishes identically as a linear form in the log|bracket| variables.
usage: bfp_verify.py <file_bfp.jsonl> ..."""
import sys, json, itertools
def bracket_sign(sig_of, x, y, z):
    inv = (x > y) + (x > z) + (y > z)
    i, j, k = sorted((x, y, z))
    return sig_of[i, j, k] * (-1 if inv % 2 else 1)
def verify(n, sig, cert):
    sig_of = {t: (1 if ch == '+' else -1) for t, ch in zip(itertools.combinations(range(n), 3), sig)}
    form = {}
    for it in cert:
        a, b, c, d, e, odd, other = it['tag']; m = it['mult']
        assert type(m) is int and m > 0 and len({a, b, c, d, e}) == 5 and {odd, other} <= {0, 1, 2} and odd != other
        pairs = [((a, b, c), (a, d, e)), ((a, b, d), (a, c, e)), ((a, b, e), (a, c, d))]
        signed = [bracket_sign(sig_of, *pairs[0][0]) * bracket_sign(sig_of, *pairs[0][1]),
                  -bracket_sign(sig_of, *pairs[1][0]) * bracket_sign(sig_of, *pairs[1][1]),
                  bracket_sign(sig_of, *pairs[2][0]) * bracket_sign(sig_of, *pairs[2][1])]
        rest = [i for i in range(3) if i != odd]
        assert signed[rest[0]] == signed[rest[1]] == -signed[odd], 'the stated term is not the odd one'
        for t in pairs[odd]: form[frozenset(t)] = form.get(frozenset(t), 0) + m
        for t in pairs[other]: form[frozenset(t)] = form.get(frozenset(t), 0) - m
    assert all(v == 0 for v in form.values()), 'the combination does not cancel'
    return True
tot = ok = 0
for fn in sys.argv[1:]:
    for line in open(fn):
        d = json.loads(line)
        if d['nonrealizable_certificate'] is None: continue
        tot += 1; ok += verify(d['n'], d['sig'], d['nonrealizable_certificate'])
print(f'{ok} of {tot} stored certificates re-verified exactly by the independent checker')
