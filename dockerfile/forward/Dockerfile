FROM alpine

# 使用腾讯云内网镜像源，以Alpine作为基础镜像，安装socat工具以便于后面执行一个脚本来将局域网内的端口映射到外网
RUN echo "https://mirrors.cloud.tencent.com/alpine/v3.12/main/" > /etc/apk/repositories && \
    echo "https://mirrors.cloud.tencent.com/alpine/v3.12/community/" >> /etc/apk/repositories 

RUN apk update && \
    apk add socat

# 将当前目录下的脚本文件映射到容器内的 /socat-forward.sh
COPY forward.sh /forward.sh

# 容器启动时执行脚本
CMD ["/forward.sh"]
