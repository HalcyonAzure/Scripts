FROM ubuntu:latest

# Replace the default software source with Tsinghua's
RUN sed -i 's/archive.ubuntu.com/mirrors.cloud.tencent.com/g' /etc/apt/sources.list
RUN sed -i 's/security.ubuntu.com/mirrors.cloud.tencent.com/g' /etc/apt/sources.list

# Install OpenJDK 17
RUN apt-get update && apt-get install -y openjdk-17-jdk openssh-server

# Create the /run/sshd directory and set the correct permissions
RUN mkdir -p /run/sshd && chmod 0755 /run/sshd

# Open port 22 for SSH, 25565 for minecraft
EXPOSE 22
EXPOSE 25565

# Set /minecraft as a mount point
VOLUME /minecraft

# Start the SSH service and run the Minecraft server
CMD ["/usr/sbin/sshd", "-D"]
