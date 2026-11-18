#!/usr/bin/env python3
"""Release research proof cache before nominal unit watermarks are reached.

No file is deleted/truncated. Fixed input paths only; runs in a bounded
nov13c-vfy unit. This complements, and does not replace, the memory guard.
"""
import json
import os
from pathlib import Path
import resource
import time

resource.setrlimit(resource.RLIMIT_AS, (40 << 20, 40 << 20))
ROOT = Path('/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice')
W = Path('/home/jay/research/data/delta3-codex-20261113/extension')
E = Path(__file__).resolve().parent
PAIRS = [('allcuts14', 'allcuts14-a'), ('nosixcup14', 'nosixcup14-a'),
         ('low16', 'low16-n7-a'), ('longcup16', 'low16-longcup-a')]
started = time.monotonic()
peaks = {}
with (E/'data/cache-watch.jsonl').open('a', buffering=1) as log:
    while time.monotonic()-started < 2400:
        for short, folder in PAIRS:
            cg = ROOT/f'nov13c-vfy-delta6-{short}.service'
            try:
                current = int((cg/'memory.current').read_text())
                high = int((cg/'memory.high').read_text())
            except (FileNotFoundError, ValueError):
                continue
            peaks[short] = max(peaks.get(short,0),current)
            if current < high * .55:
                continue
            released = []
            for name in ['input.cnf', 'proof.blrat', 'proof.blrat.zst']:
                p = W/folder/name
                try:
                    fd = os.open(p,os.O_RDONLY)
                except FileNotFoundError:
                    continue
                try:
                    size = os.fstat(fd).st_size
                    upto = max(0,size-(32<<20))
                    if upto:
                        os.fsync(fd)
                        os.posix_fadvise(fd,0,upto,os.POSIX_FADV_DONTNEED)
                        released.append([name,upto])
                finally:
                    os.close(fd)
            log.write(json.dumps({'wall_time':time.time(),'unit':short,
                'current_before':current,'memory_high':high,'released':released})+'\n')
        time.sleep(.25)
    log.write(json.dumps({'finished':True,'sampled_peaks':peaks})+'\n')
