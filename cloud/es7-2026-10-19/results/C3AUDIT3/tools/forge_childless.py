"""forged input: a fully layered (childless) plain node L' is never proved; only one sigma cube
L'__C of it is certified.  Correct answer: not covered.  usage: forge_childless.py OUT.jsonl"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mycompose as Y
m, k = 5, 6
FAKE = {"status": "UNSATISFIABLE", "lrat_check": "c VERIFIED", "cake_lpr": "s VERIFIED UNSAT", "certified": True, "cnf_sha256": "0" * 64}
P = "0s0_1s0-2s0"; A = P + "_3"; FULL = A + "_4"
recs = []
for c in Y.layer_children(m, k, (((0, 0),),)):
    n = Y.kname(Y.key(c, ()))
    if n != P: recs.append(dict(FAKE, node=n))
for c in Y.layer_children(m, k, Y.parse(P)[0]):
    n = Y.kname(Y.key(c, ()))
    if n != A: recs.append(dict(FAKE, node=n))
assert [Y.kname(Y.key(c, ())) for c in Y.layer_children(m, k, Y.parse(A)[0])] == [FULL]
assert Y.layer_children(m, k, Y.parse(FULL)[0]) == []
recs.append(dict(FAKE, node=FULL + "__3s0-4s0"))  # one quarter of FULL only
open(sys.argv[1], "w").write("".join(json.dumps(r) + "\n" for r in recs))
print(len(recs), "records; uncovered: plain", FULL, "(only", FULL + "__3s0-4s0", "certified)")
