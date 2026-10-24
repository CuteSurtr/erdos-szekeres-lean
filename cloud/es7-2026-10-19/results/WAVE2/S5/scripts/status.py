import glob, os, sys
cases = sys.argv[1].split()
for c in cases:
    st = []
    for d in glob.glob(f"results/WAVE1/*/{c}") + glob.glob(f"results/WAVE2/*/{c}"):
        if "/WAVE2/S5/" in d: continue
        lv = os.path.join(d, "leaves.icnf"); op = os.path.join(d, "open.icnf")
        nl = sum(1 for l in open(lv) if l.startswith("a")) if os.path.exists(lv) else 0
        no = sum(1 for l in open(op) if l.startswith("a")) if os.path.exists(op) else None
        closed = nl > 0 and no == 0
        started = os.path.exists(os.path.join(d, "top.icnf")) or nl > 0
        st.append((d, "CLOSED" if closed else ("STARTED" if started else "EMPTY"), nl, no))
    print(c, st)
