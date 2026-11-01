#!/bin/bash
# stop close_tree at END (close_tree checks --hours only between levels)
while [ $(date +%s) -lt 1792858570 ]; do sleep 10; done
kt(){ for c in $(pgrep -P $1); do kt $c; done; kill -TERM $1 2>/dev/null; }
for P in $(pgrep -f "^python3 close_tree.py" | sort -n | head -1); do kt $P; done
echo "watchdog: stopped close_tree at $(date -u +%T)" >> /opt/work/driver.log
