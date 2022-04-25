#!/bin/bash
/usr/bin/tar cvzf "/root/backup/docker-$(date +%F).tar.gz" --exclude='Downloads*' --exclude='bak*' --exclude='log*' /data
/usr/bin/rclone sync --cache-chunk-size=16M --transfers=16 "/root/backup" "1drive:/backup/docker" --progress
find /root/backup -mtime +30 -name "*.zip" -exec rm -rf {} \;
echo "BACKUP DATE:" "$(date +"%Y-%m-%d %H:%M:%S") ">> /var/log/backup.log