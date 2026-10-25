#!/bin/bash
while [ $(date +%s) -lt 1792921586 ]; do
  if grep -q "SAT FOUND" /opt/work/driver*.log 2>/dev/null; then break; fi
  sleep 10; done
for k in 0 1 2; do p=$(cat /opt/work/lane$k.pid); kill -TERM -- -$p 2>/dev/null; done
echo "=== WATCHDOG KILL $(date -u +%FT%TZ)" >> /opt/work/watchdog.log
