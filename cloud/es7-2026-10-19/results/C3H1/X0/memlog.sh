#!/bin/bash
END=1792927001
while [ $(date +%s) -lt $((END+600)) ]; do
  { echo "=== $(date -u +%FT%T)"; free -m; du -sb /opt/work/ct 2>/dev/null; } >> /opt/work/mem.log
  sleep 900
done
