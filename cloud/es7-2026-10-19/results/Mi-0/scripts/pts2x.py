import sys, itertools
def X_of(P):
    P = sorted(P); N = len(P); out = [str(N)]
    for i, j, k in itertools.combinations(range(N), 3):
        (ax, ay), (bx, by), (cx, cy) = P[i], P[j], P[k]
        d = (bx-ax)*(cy-ay) - (by-ay)*(cx-ax); assert d != 0
        out.append("1" if d > 0 else "0")
    return " ".join(out)
if __name__ == "__main__":
    t = open(sys.argv[1]).readline().split(); n = int(t[3]); v = list(map(int, t[4:4+2*n]))
    print(X_of([(v[2*i], v[2*i+1]) for i in range(n)]))
