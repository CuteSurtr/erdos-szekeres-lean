#!/bin/bash
while [ $(date +%s) -lt 1792921594 ]; do sleep 20; done
for k in 0 1 2; do P=$(cat /opt/work/lane$k.pid); kill -TERM -- -$P 2>/dev/null; done
sleep 5; for k in 0 1 2; do P=$(cat /opt/work/lane$k.pid); kill -KILL -- -$P 2>/dev/null; done
echo "killed $(date -u)" > /opt/work/killed.txt
