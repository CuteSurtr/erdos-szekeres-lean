#!/bin/bash
# safety net: periodic sync and kill of the lanes at END
END=$(date -u -d '2026-10-25 11:16:09' +%s)
while [ $(date +%s) -lt $END ]; do
  sleep 60
  last=$(cat /opt/work/lastsync 2>/dev/null || echo 0)
  if [ $(( $(date +%s) - last )) -ge 1500 ]; then /opt/work/sync.sh progress >/dev/null 2>&1 && date +%s > /opt/work/lastsync; fi
done
for p in $(cat /opt/work/lane_pgids); do kill -TERM -- -$p 2>/dev/null; done
sleep 10
for p in $(cat /opt/work/lane_pgids); do kill -KILL -- -$p 2>/dev/null; done
echo "killed at END $(date -u '+%F %T')" >> /opt/work/watchdog.log
