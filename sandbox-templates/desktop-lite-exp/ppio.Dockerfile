# PPIO Sandbox Desktop Lite Template
#
# This Dockerfile contains the commands to create a computer use sandbox on PPIO Sandbox.
# If you want to make your own template based on this one, make your changes

FROM ubuntu:22.04

# Environment variables:

ENV \
    # Avoid system prompts: \
    DEBIAN_FRONTEND=noninteractive \
    DEBIAN_PRIORITY=high \
    # Pip settings: \
    PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Basic system utilities:

RUN yes | unminimize && \
    apt-get update && \
    # Install apt-utils to avoid debconf warnings: \
    apt-get install -y apt-utils && \
    # X window server:
    apt-get install -y xserver-xorg xorg x11-xserver-utils xvfb x11-utils xauth && \
    # XFCE desktop environment:
    apt-get install -y xfce4 xfce4-goodies && \
    # Basic system utilities:
    apt-get install -y util-linux sudo curl git wget && \
    # Pip will be used to install Python packages:
    apt-get install -y python3-pip && \
    # Clean up apt cache to reduce image size:
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Streaming server:

RUN apt-get update && \
    # VNC: \
    apt-get install -y x11vnc && \
    # NoVNC: \
    git clone --branch e2b-desktop https://github.com/e2b-dev/noVNC.git /opt/noVNC && \
    ln -s /opt/noVNC/vnc.html /opt/noVNC/index.html && \
    # Websockify: \
    apt-get install -y net-tools netcat && \
    pip install numpy && \
    git clone --branch v0.12.0 https://github.com/novnc/websockify /opt/noVNC/utils/websockify && \
    # Clean up apt cache: \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create XFCE configuration directories
RUN mkdir -p /home/user/.config/xfce4/xfconf/xfce-perchannel-xml/

# Copy configuration files
COPY ./wallpaper.png /usr/share/backgrounds/xfce/wallpaper.png
COPY ./xfce4-desktop.xml /home/user/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml
