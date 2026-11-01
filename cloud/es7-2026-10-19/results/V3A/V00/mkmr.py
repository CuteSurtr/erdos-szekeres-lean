import json, sys
acc = set()
for i, l in enumerate(open(sys.argv[1])):
    f = l.rstrip("\n").split("\t")
    if i and f[-1] == "ACCEPTED": acc.add(f[0])
lines = open(sys.argv[2]).read().splitlines()
assert all(json.dumps(json.loads(l)) == l for l in lines), "roundtrip"
out = []; cases = set(); dropped = 0
for l in lines:
    r = json.loads(l)
    if r["case"] in acc: dropped += 1; continue
    r["idx"] = len(out); out.append(json.dumps(r)); cases.add(r["case"])
open(sys.argv[3], "w").write("".join(x + "\n" for x in out))
print("accepted cases", len(acc), "dropped records", dropped, "n", len(out), "cases", len(cases))
