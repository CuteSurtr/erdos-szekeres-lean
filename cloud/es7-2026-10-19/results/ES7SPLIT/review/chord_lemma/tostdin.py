import sys
pts = []
for line in open(sys.argv[1]):
    f = line.split()
    if len(f) >= 2:
        pts.append((int(f[0]), int(f[1])))
print(len(pts), " ".join(f"{x} {y}" for x, y in pts))
