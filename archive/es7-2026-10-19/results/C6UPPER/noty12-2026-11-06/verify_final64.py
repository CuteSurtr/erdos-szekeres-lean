#!/usr/bin/env python3
"""verify_final64.py : post-run gate for the claim "the encoder-B base formula B_m6K8t11.cnf is UNSAT" (6 November 2026).

Run after noty12.py has finished. Stdlib only, explicit checks (no assert). It re-establishes everything from the files:
 (1) tool binaries still have the hashes used (cadical 4acf5860..., cake_lpr c14ff498...);
 (2) base CNF sha = 479e31a9... (recorded, C6UPPER/SHA256SUMS.txt) and meta sha = 68b43494... (recorded); the six Y values
     are distinct ints in 1..nv;
 (3) every cube file (32 n*.cnf here, 32 c*.cnf in the replay) is, byte for byte, header "p cnf nv nc+6" + the exact base body
     + 6 unit lines matching -?[1-9][0-9]* 0 (raw bytes, ASCII); the units are (+-Y12, pattern on Y13,Y14,Y23,Y24,Y34); the
     file name spells the pattern; the sign pattern key is taken from the units themselves;
 (4) the 64 keys on the six variables are pairwise distinct (so all 2^6: every assignment satisfies the units of a cube);
 (5) certification: each n-cube has exactly one row in this job's results.tsv with verdict ACCEPTED, cake_line exactly
     's VERIFIED UNSAT' and cnf_sha256 = the file's current sha; its .cake.log contains exactly that s-line and no other s-line;
     its proof .lrat.zst has the recorded zst sha and decompresses (zstd -dc) to bytes whose sha256 is the recorded proof sha;
     each c-cube's sha equals the cnf_sha256 of exactly one ACCEPTED encoder-B replay row with that cake line (the replay's own
     zst/proof binding is recorded in C6UPPER/replay-2026-11-06);
 (6) cubes.sha256 written at preparation equals the current n-cube hashes (no file changed during the run).
Prints one 'PASS' line at the end, or 'FAIL: ...' and exits 1. Use --no-zstd to skip the (slow) decompression check.
"""
import sys, os, re, json, hashlib, subprocess

W = os.path.dirname(os.path.abspath(__file__))
REPLAY = '/path/to/data/c6upper-replay-20261106'
R = '/path/to/repo/cloud/es7-2026-10-19/results'
BASE, META = REPLAY + '/B/B_m6K8t11.cnf', R + '/C6UPPER/encb/B_m6K8t11.meta.json'
BASE_SHA = '479e31a9e8d58d752c86b9abf02fb799c10615a7e61a88f132c49734674f37fc'
TOOLS = {'/usr/bin/cadical': '4acf586001aa286dff6e1a390a273023c3160f0175aba2693e3e6a0065089e70',
         '/path/to/tools/cake_lpr/cake_lpr': 'c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54'}
UNIT = re.compile(rb'-?[1-9][0-9]* 0')
OKLINE = 's VERIFIED UNSAT'


def check(cond, msg):
    if not cond:
        print('FAIL: %s' % msg); sys.exit(1)


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()


def recorded_meta_sha():
    for l in open(R + '/C6UPPER/SHA256SUMS.txt'):
        f = l.split()
        if len(f) == 2 and f[1].endswith('B_m6K8t11.meta.json'): return f[0]
    return None


def rows(path, header_cols):
    lines = open(path).read().split('\n')
    check(lines[0].split('\t') == header_cols, '%s: unexpected header' % path)
    return [l.split('\t') for l in lines[1:] if l]


def main():
    do_zstd = '--no-zstd' not in sys.argv[1:]
    for p, want in TOOLS.items():
        check(sha(p) == want, 'tool hash changed: %s' % p)
    check(sha(BASE) == BASE_SHA, 'base sha')
    msha = recorded_meta_sha()
    check(msha is not None and sha(META) == msha, 'meta sha (recorded %s)' % msha)
    Y = json.load(open(META))['Y']
    raw = open(BASE, 'rb').read()
    hdr, body = raw.split(b'\n', 1)
    t = hdr.split(b' ')
    check(len(t) == 4 and t[:2] == [b'p', b'cnf'] and t[2].isdigit() and t[3].isdigit(), 'base header')
    nv, nc = int(t[2]), int(t[3])
    check(body.endswith(b'\n') and body.count(b'\n') == nc, 'base body: %d lines, header says %d' % (body.count(b'\n'), nc))
    keys6 = ('1,2', '1,3', '1,4', '2,3', '2,4', '3,4')
    yv = [Y[k] for k in keys6]
    check(all(type(v) is int and 1 <= v <= nv for v in yv) and len(set(yv)) == 6, 'Y values %s' % yv)
    y12, cv = yv[0], yv[1:]

    # this job's rows
    head_n = 'cube\tunits\tcnf_sha256\tcadical_rc\tsolve_s\tproof_sha256\tproof_bytes\tverdict\tcake_line\tcake_s\tzst_sha256\tdate'.split('\t')
    acc_n = {}
    for f in rows(W + '/results.tsv', head_n):
        check(len(f) == 12, 'results.tsv row width %d' % len(f))
        if f[7] == 'ACCEPTED':
            check(f[8] == OKLINE, '%s: ACCEPTED with cake line %r' % (f[0], f[8]))
            check(f[0] not in acc_n, '%s: two ACCEPTED rows' % f[0])
            acc_n[f[0]] = f
    # replay rows
    head_r = 'enc\tcube\tcnf_sha256\tcadical_rc\tsolve_s\tproof_sha256\tproof_bytes\tsame_as_archived\tverdict\tcake_line\tzst_sha256\tdate'.split('\t')
    acc_c = {}
    for f in rows(REPLAY + '/results.tsv', head_r):
        if len(f) == 12 and f[0] == 'B' and f[8] == 'ACCEPTED' and f[9] == OKLINE:
            check(f[1] not in acc_c, '%s: two accepted replay rows' % f[1])
            acc_c[f[1]] = f[2]
    check(len(acc_c) == 32, 'replay: %d accepted B rows' % len(acc_c))

    prep = {}
    for l in open(W + '/cubes.sha256'):
        h, name = l.split()
        prep[os.path.basename(name)[:-4]] = h

    seen = {}
    for d, prefix, sign in ((W + '/cubes', 'n', -1), (REPLAY + '/B/cubes', 'c', +1)):
        names = sorted(f[:-4] for f in os.listdir(d) if f.startswith(prefix) and f.endswith('.cnf'))
        check(len(names) == 32, '%s: %d %s-cubes' % (d, len(names), prefix))
        for n in names:
            p = d + '/' + n + '.cnf'
            r = open(p, 'rb').read()
            h, rest = r.split(b'\n', 1)
            check(h == b'p cnf %d %d' % (nv, nc + 6), '%s header %r' % (n, h))
            check(rest.startswith(body), '%s body' % n)
            tail = rest[len(body):]
            lines = tail.split(b'\n')
            check(len(lines) == 7 and lines[-1] == b'', '%s: tail is not 6 newline-terminated lines' % n)
            check(all(UNIT.fullmatch(l) for l in lines[:6]), '%s: bad unit line' % n)
            units = [int(l.split(b' ')[0]) for l in lines[:6]]
            check([abs(u) for u in units] == yv, '%s: unit variables %s' % (n, units))
            check(units[0] == sign * y12, '%s: first unit %d' % (n, units[0]))
            key = tuple(1 if u > 0 else 0 for u in units)
            check(n == prefix + ''.join(map(str, key[1:])), '%s: name/pattern mismatch' % n)
            check(key not in seen, '%s duplicates %s' % (n, seen.get(key)))
            seen[key] = n
            fs = hashlib.sha256(r).hexdigest()
            if prefix == 'c':
                check(acc_c.get(n) == fs, '%s: sha %s is not an accepted replay row' % (n, fs))
                continue
            check(prep.get(n) == fs, '%s: changed since preparation (cubes.sha256)' % n)
            row = acc_n.get(n)
            check(row is not None, '%s: no ACCEPTED row' % n)
            check(row[2] == fs, '%s: row cnf_sha256 %s != file %s' % (n, row[2], fs))
            check(row[1] == ' '.join(map(str, units)), '%s: row units %r' % (n, row[1]))
            clog = open(d + '/' + n + '.cake.log').read().splitlines()
            sl = [l.strip() for l in clog if l.startswith('s ')]
            check(sl == [OKLINE], '%s: cake log s-lines %r' % (n, sl))
            z = d + '/' + n + '.lrat.zst'
            check(os.path.exists(z) and sha(z) == row[10], '%s: zst missing or sha differs from the row' % n)
            check(not os.path.exists(d + '/' + n + '.lrat'), '%s: raw .lrat still present (compression incomplete?)' % n)
            if do_zstd:
                pz = subprocess.Popen(['zstd', '-dc', z], stdout=subprocess.PIPE)
                hh, nb = hashlib.sha256(), 0
                for b in iter(lambda: pz.stdout.read(1 << 22), b''): hh.update(b); nb += len(b)
                check(pz.wait() == 0, '%s: zstd -dc failed' % n)
                check(hh.hexdigest() == row[5] and str(nb) == row[6], '%s: decompressed proof sha/size differ from the row' % n)
    check(len(seen) == 64, 'patterns %d' % len(seen))
    for p, want in TOOLS.items():
        check(sha(p) == want, 'tool hash changed during check: %s' % p)
    print('PASS: tools and base/meta hashes as recorded; 64 distinct cubes (32 n-cubes certified in this run, each '
          'row = file sha, cake log exactly "%s"%s; 32 c-cubes = accepted replay rows) cover all 2^6 assignments of '
          'Y(1,2),Y(1,3),Y(1,4),Y(2,3),Y(2,4),Y(3,4): B_m6K8t11.cnf (sha %s...) is UNSAT'
          % (OKLINE, ', proof zst decompresses to the recorded proof sha' if do_zstd else '', BASE_SHA[:12]))


if __name__ == '__main__':
    main()
