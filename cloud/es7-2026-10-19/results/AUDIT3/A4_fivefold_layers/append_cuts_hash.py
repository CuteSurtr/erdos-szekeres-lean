# stream base CNF + one clause per cut (own implementation) into sha256 without writing the file
import hashlib, json, sys
base, cuts = sys.argv[1], sys.argv[2]
cl = [json.loads(l)["clause"] for l in open(cuts)]
h = hashlib.sha256()
with open(base, "rb") as f:
    while True:
        line = f.readline()
        if line.startswith(b"p cnf"):
            _, _, nv, nc = line.split()
            h.update(f"p cnf {int(nv)} {int(nc) + len(cl)}\n".encode()); break
        h.update(line)
    while True:
        b = f.read(1 << 22)
        if not b: break
        h.update(b)
for c in cl:
    h.update((" ".join(map(str, c)) + " 0\n").encode())
print("base+cuts sha256:", h.hexdigest(), "cuts:", len(cl), "header clauses:", int(nc) + len(cl))
