#!/bin/bash
END=$(date -u -d '2026-10-25 11:16:09' +%s)
while [ $(date +%s) -lt $((END+300)) ]; do
  { echo "=== $(date -u '+%F %T')"; free -m; du -sh /opt/work/ct 2>/dev/null; } >> /opt/work/mem.log
  sleep 900
done
