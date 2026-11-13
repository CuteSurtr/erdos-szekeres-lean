#!/bin/bash
while true; do
  { echo "=== $(date -u +%FT%TZ)"; free -m; du -sm /opt/work/ct 2>/dev/null || echo "0 /opt/work/ct (absent)"; } >> /opt/work/mem.log
  sleep 900
done
