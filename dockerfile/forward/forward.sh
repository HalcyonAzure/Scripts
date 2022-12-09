#!/bin/sh

# 从$REMOTE_PORT中读取需要转发的端口字符串，用逗号隔开，例如：'22,80,443'，然后使用socat转发$REMOTE_HOST上对应的端口
for port in $(echo $REMOTE_PORT | sed "s/,/ /g")
do
    socat TCP-LISTEN:$port,fork TCP:$REMOTE_HOST:$port &
done

# 等待所有的socat进程结束
wait
