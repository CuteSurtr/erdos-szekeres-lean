#!/bin/bash
END=1792921610
while [ $(date -u +%s) -lt $END ]; do sleep 20; done
for k in 0 1 2; do p=$(cat /opt/work/lane$k.pid); kill -TERM -- -$p 2>/dev/null && echo "=== KILLED at END $(date -u '+%F %T')" >> /opt/work/driver$k.log; done
sleep 5; for k in 0 1 2; do kill -KILL -- -$(cat /opt/work/lane$k.pid) 2>/dev/null; done
