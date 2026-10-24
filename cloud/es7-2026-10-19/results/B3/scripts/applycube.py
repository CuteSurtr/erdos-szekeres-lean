import sys
cnf, cube, out = sys.argv[1], sys.argv[2], sys.argv[3]
lits = [int(x) for x in cube.split()[1:] if x != '0' and x!='a']
lines = open(cnf).read().split('\n', 1)
h = lines[0].split(); nv, nc = int(h[2]), int(h[3])
with open(out, 'w') as f:
    f.write(f"p cnf {nv} {nc+len(lits)}\n"); f.write(lines[1])
    if not lines[1].endswith('\n'): f.write('\n')
    for l in lits: f.write(f"{l} 0\n")
