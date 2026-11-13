import sys, time, coupled5
for n in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
    t = time.time(); nv, nc, body = coupled5._static(n); print(n, nv, nc, round(time.time() - t, 1), flush=True)
