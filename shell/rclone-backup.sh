#!/bin/sh
RcloneConfig="1drive"  # Rclone设置
RclonePath="/Backup/docker-pile"  # Rclone路径
BackupPath="/data/*"  # 备份路径
ZipName="docker-pile-$(date +%F-%H-%M).7z"  # 压缩文件名
ZipPath="/root/backup_tmp"  # 压缩文件路径

# 压缩文件
7za a -t7z -r "$ZipPath/$ZipName" "$BackupPath"

echo "开始上传..."
## retries是指上传失败以后重试的次数，Buffer-size是缓存，这里可以调小一点，512M为示例
if ! rclone copy --retries=1 --buffer-size=512M "$ZipPath/$ZipName" "$RcloneConfig:$RclonePath"; then
    echo "上传失败!"
    exit 1
fi
echo "上传文件成功, 删除本地备份"