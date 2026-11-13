# Verbatim copy of the CNF construction embedded in p2/tools/lrat_ext.sh
import sys, json
enc, core, out = sys.argv[1], sys.argv[2], sys.argv[3]; extra = sys.argv[4:]
units = json.load(open(core))
nv = None; body = []
with open(enc) as f:
    hdr = f.readline().split(); nv = int(hdr[2]); ncl = int(hdr[3])
ext = []
for e in extra:
    for line in open(e):
        if line.strip() and line[0] not in 'pc': ext.append(line if line.endswith('\n') else line + '\n')
with open(out, 'w') as g:
    g.write('p cnf %d %d\n' % (nv, ncl + len(ext) + len(units)))
    with open(enc) as f:
        f.readline()
        while True:
            b = f.read(1 << 24)
            if not b: break
            g.write(b)
    g.writelines(ext)
    for u in units: g.write('%d 0\n' % u)
