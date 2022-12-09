# 使用说明

该镜像的作用是将局域网内的某个设备IP和端口，通过Docker的形式以宿主机对应的端口进行转发

使用方法：

在运行容器的时候设定`REMOTE_PORT`和`REMOTE_HOST`两个变量，可参考如下`docker-compose.yaml`

```yaml
# 以forward为镜像，REMOTE_PORT和REMOTE_HOST为变量，将本地的端口映射到远程的端口上
# 完成这个docker-compose
version: '3'
services:
  forward:
    build: .
    network_mode: host
    environment:
      - REMOTE_PORT=5001,6690
      - REMOTE_HOST=10.0.5.249
```

就是将局域网内`10.0.5.249`的`5001`和`6690`端口转发到宿主机上
