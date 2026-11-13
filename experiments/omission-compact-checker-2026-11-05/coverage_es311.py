#!/usr/bin/env python3
"""Independent coverage check of an export_es311.py manifest (6 November 2026).

  coverage_es311.py EXPORT_DIR/manifest-<Prefix>.json --expect-leaves 782437

Written separately from export_es311.py (it imports nothing from it). From the certificate
parts listed in the manifest it rebuilds the tree shape and checks:
  * the decompressed stream has the manifest's sha256, and every part file its sha256;
  * the leaves under the export root number --expect-leaves (782,437 for tree-63 and 437,579
    for the state-0 subtree of tree-2650-32, as counted by the review's replay_tree.py,
    cloud/es7-2026-10-19/results/ES8SLACK/review/C1_certificates/replay{63,2650}.out);
  * the subtree roots of all modules cover every leaf under the export root exactly once, and
    each module's leaf count is the sum of its subtree roots' counts;
  * every node under the export root that is not inside a subtree root is a branch listed in
    the manifest's skeleton with the tree's vertex and children;
for every written module file:
  * its sha256 is the manifest's;
  * the number of `(.leaf ` and `.overBudget` terms in it equals its leaf count;
  * every block term `b<k>` is the preorder serialization of the subtree at node k (branch
    vertices, leaf capacities), and its `chk<k>`/`ex<k>` statements carry the path of node k
    (the decisions up to the tree root, innermost first), recomputed here;
  * every subtree root `ex<s>` is stated with the path of s;
  * (6 November 2026, review fix) every line has one of the exporter's shapes (shapes_es311.py:
    no axiom, #eval, option, macro or other command);
and, if Root.lean is present, it references every subtree root exactly once, from its module, and
passes the same line-shape check.
Leaf weights are not compared: Lean checks every leaf, and any weights it accepts certify it.
"""
import argparse
import hashlib
import json
import lzma
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import shapes_es311  # noqa: E402  (line shapes only; nothing from the exporter)


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 22), b""):
            h.update(b)
    return h.hexdigest()


def read_tree(parts):
    """type, vertex, zero, one, capacity per node, by a plain incremental JSON scan."""
    dec, decoder, h = lzma.LZMADecompressor(), json.JSONDecoder(), hashlib.sha256()
    text, pos, started, nodes, done = "", 0, False, [], False
    for p in parts:
        with open(p, "rb") as f:
            for raw in iter(lambda: f.read(1 << 22), b""):
                out = dec.decompress(raw)
                h.update(out)
                text = text[pos:] + out.decode("ascii")
                pos = 0
                if not started:
                    i = text.find('"nodes":[')
                    if i < 0:
                        continue
                    header = json.loads(text[:i].rstrip()[:-1] + "}")
                    pos, started = i + len('"nodes":['), True
                while not done:
                    while pos < len(text) and text[pos] in ", \n\r\t":
                        pos += 1
                    if pos >= len(text):
                        break
                    if text[pos] == "]":
                        done = True
                        pos += 1
                        break
                    try:
                        obj, end = decoder.raw_decode(text, pos)
                    except json.JSONDecodeError:
                        break  # incomplete object; read more
                    if end == len(text):
                        break  # a number may continue in the next block
                    pos = end
                    t = obj["type"]
                    if t == "branch":
                        nodes.append(("b", obj["vertex"], obj["zero"], obj["one"], None))
                    elif t == "weighted":
                        nodes.append(("w", None, None, None, obj["capacity"]))
                    elif t == "over_budget":
                        nodes.append(("o", None, None, None, None))
                    else:
                        nodes.append(("x", None, None, None, None))
    assert dec.eof and done and text[pos:].strip() == "}", "stream did not end as expected"
    return header, nodes, h.hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest", type=Path)
    ap.add_argument("--expect-leaves", type=int, required=True)
    args = ap.parse_args()
    man = json.loads(args.manifest.read_text())
    ex = args.manifest.parent
    res = {"manifest": str(args.manifest), "checks": {}}
    ok = res["checks"]
    parts = [Path(p["file"]) for p in man["tree_parts"]]
    ok["part_sha256"] = all(sha(p) == q["sha256"] for p, q in zip(parts, man["tree_parts"]))
    header, nodes, tree_sha = read_tree(parts)
    ok["tree_sha256"] = tree_sha == man["tree_sha256"]
    ok["budget"] = header["hole_budget"] == man["budget"]
    N = len(nodes)
    # parents and edge decisions, from the tree root; every node reached once
    parent, decision = [None] * N, [None] * N
    root0 = header["root"]
    stack, reached = [root0], 0
    while stack:
        j = stack.pop()
        reached += 1
        if nodes[j][0] == "b":
            for c, x in ((nodes[j][2], 2), (nodes[j][3], 1)):
                assert parent[c] is None and c != root0, "node reached twice"
                parent[c], decision[c] = j, x
                stack.append(c)
    ok["tree_is_tree"] = reached == N

    def path(j):
        p = []
        while parent[j] is not None:
            p.append([nodes[parent[j]][1], decision[j]])
            j = parent[j]
        return p

    def leaves_below(j):
        out, st = [], [j]
        while st:
            k = st.pop()
            if nodes[k][0] == "b":
                st += [nodes[k][3], nodes[k][2]]
            else:
                out.append(k)
        return out

    def preorder(j):
        out, st = [], [j]
        while st:
            k = st.pop()
            t = nodes[k]
            if t[0] == "b":
                out.append(("split", t[1]))
                st += [t[3], t[2]]
            elif t[0] == "w":
                out.append(("leaf", t[4]))
            elif t[0] == "o":
                out.append(("over", None))
            else:
                out.append(("other", None))
        return out

    er = man["export_root"]
    all_leaves = leaves_below(er)
    ok["expected_leaves"] = len(all_leaves) == args.expect_leaves == man["total_leaves"]
    ok["base_path"] = path(er) == man["base_path"]
    cover = {}
    srs = {}
    module_counts_ok = True
    for mm in man["modules"]:
        tot = 0
        for s, c in mm["subtree_roots"]:
            lv = leaves_below(s)
            if len(lv) != c:
                module_counts_ok = False
            tot += len(lv)
            for x in lv:
                cover[x] = cover.get(x, 0) + 1
            srs[s] = mm["module"]
        if tot != mm["leaves"]:
            module_counts_ok = False
    ok["module_leaf_counts"] = module_counts_ok
    ok["every_leaf_exactly_once"] = (set(cover) == set(all_leaves) and all(v == 1 for v in cover.values()))
    ok["sum_of_module_leaves"] = sum(mm["leaves"] for mm in man["modules"]) == len(all_leaves)
    # skeleton: nodes under the export root, outside every subtree root
    inside = set()
    for s in srs:
        st = [s]
        while st:
            k = st.pop()
            inside.add(k)
            if nodes[k][0] == "b":
                st += [nodes[k][2], nodes[k][3]]
    skel = {u: (v, z, o) for u, v, z, o in man["skeleton"]}
    outside, st = [], [er]
    while st:
        k = st.pop()
        if k in inside:
            continue
        outside.append(k)
        if nodes[k][0] == "b":
            st += [nodes[k][2], nodes[k][3]]
    ok["skeleton"] = (set(outside) == set(skel) and all(
        nodes[u][0] == "b" and (nodes[u][1], nodes[u][2], nodes[u][3]) == skel[u] for u in outside))
    # module files
    written, files_ok, shapes_ok = 0, True, True
    sp = shapes_es311.side_params(man)
    detail = []
    tok = re.compile(r"\(\.split (\d+)|\(\.leaf (\d+)|\.overBudget")
    stmt = re.compile(r"^theorem (chk|ex)(\d+) : .*?\(pmask \(zerosF \d+\) (\[[^\]]*\])\)", re.M)
    for mm in man["modules"]:
        if not mm["file"]:
            continue
        written += 1
        f = ex / mm["file"]
        text = f.read_text()
        good = sha(f) == mm["sha256"]
        nleaf = text.count("(.leaf ") + text.count(".overBudget")
        good &= nleaf == mm["leaves"]
        blocks = re.findall(r"^noncomputable def b(\d+) : PTree := (.*)$", text, re.M)
        for k, term in blocks:
            got = [("split", int(a)) if a else ("leaf", int(b)) if b else ("over", None)
                   for a, b in tok.findall(term)]
            good &= got == preorder(int(k))
        for kind, k, lst in stmt.findall(text):
            pairs = [[int(a), int(b)] for a, b in re.findall(r"\((\d+), (\d+)\)", lst)]
            good &= pairs == path(int(k))
        for s, _ in mm["subtree_roots"]:
            good &= re.search(rf"^theorem ex{s} : ", text, re.M) is not None
        shape_errors = shapes_es311.check_text(text, "chunk", mm["module"], sp)
        shapes_ok &= not shape_errors
        files_ok &= good
        detail.append({"module": mm["module"], "ok": good, "leaf_terms": nleaf, "blocks": len(blocks),
                       "shape_errors": shape_errors})
    ok["module_files"] = files_ok
    ok["module_line_shapes"] = shapes_ok
    res["written_modules"] = written
    if man.get("root"):
        rt = (ex / man["root"]["file"]).read_text()
        refs = re.findall(rf"{re.escape(man['prefix'])}\.(C\d+)\.ex(\d+)", rt)
        cnt = {}
        for mod, k in refs:
            cnt[int(k)] = cnt.get(int(k), 0) + 1
            if srs.get(int(k)) != f"{man['prefix']}.{mod}":
                cnt[int(k)] = -99
        ok["root_references"] = (sha(ex / man["root"]["file"]) == man["root"]["sha256"]
                                 and set(cnt) == set(srs) and all(v == 1 for v in cnt.values()))
        res["root_shape_errors"] = shapes_es311.check_text(rt, "root", man["prefix"], sp)
        ok["root_line_shapes"] = not res["root_shape_errors"]
    res["leaves"] = len(all_leaves)
    res["modules"] = len(man["modules"])
    res["subtree_roots"] = len(srs)
    res["files"] = detail
    res["PASS"] = all(ok.values())
    print(json.dumps(res, indent=1))
    sys.exit(0 if res["PASS"] else 1)


if __name__ == "__main__":
    main()
