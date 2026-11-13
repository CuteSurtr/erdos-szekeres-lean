#!/usr/bin/env python3
"""Turn wave leaves.jsonl records into leaves.icnf files that v3_manifest.py can read.

Some wave drivers write leaves.icnf only at the end of their run and keep the leaf list in
leaves.jsonl until then. This script widens the set of candidate leaves; it cannot make anything
accepted on its own, because v3_check.py re-solves every leaf and checks every cover from scratch.

For every ROOT/WAVEDIR/<vm>/<dir>/leaves.jsonl, it writes OUTDIR/<vm>/<dir>/leaves.icnf with one
line "a l1 .. lk 0" per record whose "status" is "UNSAT" and whose "cube" is a list of nonzero
ints with no repeated or complementary literals, in the record's literal order. A record that has a
"cake_lpr" field other than "s VERIFIED UNSAT" is skipped. leaves.jsonl is copied next to the new
file so that v3_manifest.py can assign the directory to its case (case_sha256 and directory name).
Run v3_manifest.py with both WAVEDIR and OUTDIR (relative to ROOT); it merges and deduplicates.

usage: v3_jsonl_leaves.py ROOT WAVEDIR OUTDIR     (WAVEDIR and OUTDIR relative to ROOT)
"""
import sys, os, json, shutil


def main():
    root, wave, out = sys.argv[1], sys.argv[2], sys.argv[3]
    wroot, oroot = os.path.join(root, wave), os.path.join(root, out)
    ndirs = nleaves = nskip = 0
    for vm in sorted(os.listdir(wroot)):
        vmdir = os.path.join(wroot, vm)
        if not os.path.isdir(vmdir):
            continue
        for d in sorted(os.listdir(vmdir)):
            jf = os.path.join(vmdir, d, "leaves.jsonl")
            if not os.path.isfile(jf):
                continue
            lines = []
            for l in open(jf):
                l = l.strip()
                if not l.startswith("{"):
                    continue
                try:
                    r = json.loads(l)
                except ValueError:
                    nskip += 1
                    continue
                if r.get("status") != "UNSAT":
                    continue
                if "cake_lpr" in r and r["cake_lpr"] != "s VERIFIED UNSAT":
                    nskip += 1
                    continue
                c = r.get("cube")
                if (not isinstance(c, list) or not all(isinstance(x, int) and not isinstance(x, bool) and x != 0 for x in c)
                        or len(set(c)) != len(c) or any(-x in c for x in c)):
                    nskip += 1
                    continue
                lines.append("a " + "".join(f"{x} " for x in c) + "0\n")
            if not lines:
                continue
            od = os.path.join(oroot, vm, d)
            os.makedirs(od, exist_ok=True)
            with open(os.path.join(od, "leaves.icnf"), "w") as f:
                f.writelines(lines)
            shutil.copyfile(jf, os.path.join(od, "leaves.jsonl"))
            ndirs += 1
            nleaves += len(lines)
    print("dirs", ndirs, "leaf lines", nleaves, "skipped records", nskip)


if __name__ == "__main__":
    main()
