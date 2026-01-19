# PPIO Sandbox Desktop V2 Beta Template
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

# Desktop environment:

RUN yes | unminimize && \
    apt-get update && \
    # Install apt-utils to avoid debconf warnings: \
    apt-get install -y apt-utils && \
    # Install locales and Chinese language support: \
    apt-get install -y locales language-pack-zh-hans language-pack-zh-hant && \
    # Generate Chinese UTF8 locales: \
    locale-gen zh_CN.UTF-8 && \
    update-locale LANG=zh_CN.UTF-8 LC_ALL=zh_CN.UTF-8 && \
    # Install Chinese fonts: \
    apt-get install -y fonts-wqy-zenhei fonts-wqy-microhei fonts-arphic-ukai fonts-arphic-uming && \
    # Install additional fonts for better terminal UTF-8 support: \
    apt-get install -y fonts-noto fonts-noto-cjk fonts-noto-color-emoji fonts-liberation fonts-dejavu-core && \
    # Install Chinese input method (fcitx): \
    apt-get install -y fcitx fcitx-googlepinyin fcitx-module-cloudpinyin fcitx-sunpinyin fcitx-config-gtk fcitx-frontend-gtk2 fcitx-frontend-gtk3 fcitx-ui-classic && \
    # X window server:
    apt-get install -y xserver-xorg xorg x11-xserver-utils xvfb x11-utils xauth && \
    # XFCE desktop environment:
    apt-get install -y xfce4 xfce4-goodies && \ 
    # Basic system utilities:
    apt-get install -y util-linux sudo curl git wget && \
    # Pip will be used to install Python packages:
    apt-get install -y python3-pip && \ 
    # Tools used by the desktop SDK:
    apt-get install -y xdotool scrot ffmpeg && \
    # Additional tools for UTF-8 support:
    apt-get install -y xclip xsel ibus ibus-gtk ibus-gtk3 && \
    # Clean up apt cache to reduce image size:
    apt-get clean && rm -rf /var/lib/apt/lists/*



# Set locale environment variables after locale generation
ENV \
    LANG=zh_CN.UTF-8 \
    LANGUAGE=zh_CN:zh:en_US:en \
    LC_ALL=zh_CN.UTF-8 \
    LC_CTYPE=zh_CN.UTF-8

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

# User applications:

# ~ Make your changes to this template BELOW this line ~

# Set the default terminal
RUN ln -sf /usr/bin/xfce4-terminal.wrapper /etc/alternatives/x-terminal-emulator

# Install standard apps and Firefox
RUN apt-get update && \
    # Install standard apps: \
    apt-get install -y x11-apps libreoffice xpdf gedit xpaint tint2 galculator pcmanfm && \
    # Install Firefox: \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:mozillateam/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends firefox-esr && \
    # Set Firefox as default browser: \
    update-alternatives --set x-www-browser /usr/bin/firefox-esr && \
    # Clean up apt cache: \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Node.js 20.19.3 using nvm
# Create user directory and set up environment
RUN mkdir -p /home/user /home/user/.nvm && \
    export NVM_DIR="/home/user/.nvm" && \
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash && \
    [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && \
    nvm install 20.19.3 && \
    nvm alias default 20.19.3 && \
    npm install -g npm@latest yarn typescript && \
    chown -R 1000:1000 /home/user

# Install VS Code and additional tools
RUN apt-get update && \
    # Install VS Code: \
    apt-get install -y apt-transport-https && \
    wget -qO- https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    add-apt-repository -y "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" && \
    apt-get update && \
    apt-get install -y code && \
    # Install additional tools: \
    apt-get install -y libgtk-3-bin && \
    update-desktop-database /usr/share/applications/ && \
    # Clean up apt cache: \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Create VS Code and XFCE configuration directories
RUN mkdir -p /home/user/.config/Code/User \
             /home/user/.config/xfce4/xfconf/xfce-perchannel-xml/ \
             /home/user/.config/xfce4/terminal

# Copy configuration files
COPY ./settings.json /home/user/.config/Code/User/settings.json
COPY ./wallpaper.png /usr/share/backgrounds/xfce/wallpaper.png
COPY ./xfce4-desktop.xml /home/user/.config/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml

# Copy firefox policies
COPY firefox-policies.json /usr/lib/firefox-esr/distribution/policies.json
COPY firefox-autoconfig.js /usr/lib/firefox-esr/defaults/pref/autoconfig.js
COPY firefox.cfg /usr/lib/firefox-esr/firefox.cfg

# Configure system environment and terminal settings
RUN echo "[Configuration]" > /home/user/.config/xfce4/terminal/terminalrc && \
    echo "FontName=Noto Sans Mono CJK SC 12" >> /home/user/.config/xfce4/terminal/terminalrc && \
    # Configure Chinese language and input method globally: \
    echo "LANG=zh_CN.UTF-8" >> /etc/environment && \
    echo "LC_ALL=zh_CN.UTF-8" >> /etc/environment && \
    echo "LC_CTYPE=zh_CN.UTF-8" >> /etc/environment && \
    echo "INPUT_METHOD=fcitx" >> /etc/environment && \
    echo "GTK_IM_MODULE=fcitx" >> /etc/environment && \
    echo "QT_IM_MODULE=fcitx" >> /etc/environment && \
    echo "XMODIFIERS=@im=fcitx" >> /etc/environment && \
    echo "SDL_IM_MODULE=fcitx" >> /etc/environment && \
    echo "TERM=xterm-256color" >> /etc/environment && \
    echo "FCITX_SOCKET=/tmp/fcitx-socket" >> /etc/environment

# Create autostart configuration and wrapper scripts
RUN mkdir -p /etc/xdg/autostart && \
    echo "[Desktop Entry]" > /etc/xdg/autostart/fcitx.desktop && \
    echo "Name=Fcitx" >> /etc/xdg/autostart/fcitx.desktop && \
    echo "Exec=fcitx" >> /etc/xdg/autostart/fcitx.desktop && \
    echo "Terminal=false" >> /etc/xdg/autostart/fcitx.desktop && \
    echo "Type=Application" >> /etc/xdg/autostart/fcitx.desktop && \
    echo "Categories=System;Utility;" >> /etc/xdg/autostart/fcitx.desktop && \
    echo "StartupNotify=false" >> /etc/xdg/autostart/fcitx.desktop && \
    echo "NoDisplay=true" >> /etc/xdg/autostart/fcitx.desktop && \
    # Create UTF-8 xdotool wrapper that preserves --delay parameter: \
    echo '#!/bin/bash' > /usr/local/bin/xdotool-utf8 && \
    echo '# UTF-8 wrapper with proper environment and --delay support' >> /usr/local/bin/xdotool-utf8 && \
    echo 'export LANG=zh_CN.UTF-8' >> /usr/local/bin/xdotool-utf8 && \
    echo 'export LC_ALL=zh_CN.UTF-8' >> /usr/local/bin/xdotool-utf8 && \
    echo 'export LC_CTYPE=zh_CN.UTF-8' >> /usr/local/bin/xdotool-utf8 && \
    echo 'if [ "$1" = "type" ]; then' >> /usr/local/bin/xdotool-utf8 && \
    echo '    shift' >> /usr/local/bin/xdotool-utf8 && \
    echo '    # Extract --delay parameter if present' >> /usr/local/bin/xdotool-utf8 && \
    echo '    delay_param=""' >> /usr/local/bin/xdotool-utf8 && \
    echo '    if [ "$1" = "--delay" ]; then' >> /usr/local/bin/xdotool-utf8 && \
    echo '        delay_param="--delay $2"' >> /usr/local/bin/xdotool-utf8 && \
    echo '        shift 2' >> /usr/local/bin/xdotool-utf8 && \
    echo '    fi' >> /usr/local/bin/xdotool-utf8 && \
    echo '    # Use printf and --file for UTF-8 support, preserving delay' >> /usr/local/bin/xdotool-utf8 && \
    echo '    printf "%s" "$*" | /usr/bin/xdotool-original type $delay_param --file -' >> /usr/local/bin/xdotool-utf8 && \
    echo 'else' >> /usr/local/bin/xdotool-utf8 && \
    echo '    /usr/bin/xdotool-original "$@"' >> /usr/local/bin/xdotool-utf8 && \
    echo 'fi' >> /usr/local/bin/xdotool-utf8 && \
    chmod +x /usr/local/bin/xdotool-utf8 && \
    # Create comprehensive xdotool override system: \
    mv /usr/bin/xdotool /usr/bin/xdotool-original && \
    ln -s /usr/local/bin/xdotool-utf8 /usr/bin/xdotool && \
    # Also create symlink in /usr/local/bin for redundancy: \
    ln -sf /usr/local/bin/xdotool-utf8 /usr/local/bin/xdotool && \
    # Create terminal wrapper for UTF-8 support: \
    echo '#!/bin/bash' > /usr/local/bin/terminal-utf8 && \
    echo 'export LANG=zh_CN.UTF-8' >> /usr/local/bin/terminal-utf8 && \
    echo 'export LC_ALL=zh_CN.UTF-8' >> /usr/local/bin/terminal-utf8 && \
    echo 'export LC_CTYPE=zh_CN.UTF-8' >> /usr/local/bin/terminal-utf8 && \
    echo 'export TERM=xterm-256color' >> /usr/local/bin/terminal-utf8 && \
    echo 'exec /usr/bin/xfce4-terminal "$@"' >> /usr/local/bin/terminal-utf8 && \
    chmod +x /usr/local/bin/terminal-utf8

# Configure bash profile and set file permissions
RUN echo 'export LANG=zh_CN.UTF-8' >> /home/user/.bashrc && \
    echo 'export LC_ALL=zh_CN.UTF-8' >> /home/user/.bashrc && \
    echo 'export LC_CTYPE=zh_CN.UTF-8' >> /home/user/.bashrc && \
    echo 'export TERM=xterm-256color' >> /home/user/.bashrc && \
    echo 'export INPUT_METHOD=fcitx' >> /home/user/.bashrc && \
    echo 'export GTK_IM_MODULE=fcitx' >> /home/user/.bashrc && \
    echo 'export QT_IM_MODULE=fcitx' >> /home/user/.bashrc && \
    echo 'export XMODIFIERS=@im=fcitx' >> /home/user/.bashrc && \
    echo 'export SDL_IM_MODULE=fcitx' >> /home/user/.bashrc && \
    echo 'alias terminal="terminal-utf8"' >> /home/user/.bashrc && \
    echo 'alias xfce4-terminal="terminal-utf8"' >> /home/user/.bashrc && \
    # Create Firefox wrapper for better input method support: \
    echo '#!/bin/bash' > /usr/local/bin/firefox-utf8 && \
    echo 'export LANG=zh_CN.UTF-8' >> /usr/local/bin/firefox-utf8 && \
    echo 'export LC_ALL=zh_CN.UTF-8' >> /usr/local/bin/firefox-utf8 && \
    echo 'export LC_CTYPE=zh_CN.UTF-8' >> /usr/local/bin/firefox-utf8 && \
    echo 'export INPUT_METHOD=fcitx' >> /usr/local/bin/firefox-utf8 && \
    echo 'export GTK_IM_MODULE=fcitx' >> /usr/local/bin/firefox-utf8 && \
    echo 'export QT_IM_MODULE=fcitx' >> /usr/local/bin/firefox-utf8 && \
    echo 'export XMODIFIERS=@im=fcitx' >> /usr/local/bin/firefox-utf8 && \
    echo 'export SDL_IM_MODULE=fcitx' >> /usr/local/bin/firefox-utf8 && \
    echo 'exec /usr/bin/firefox-esr "$@"' >> /usr/local/bin/firefox-utf8 && \
    chmod +x /usr/local/bin/firefox-utf8 && \
    # Create alias for Firefox with UTF-8 support: \
    echo 'alias firefox="firefox-utf8"' >> /home/user/.bashrc && \
    echo 'alias firefox-esr="firefox-utf8"' >> /home/user/.bashrc && \
    # Node.js environment configuration (nvm will manage npm global packages): \
    # nvm configuration: \
    echo 'export NVM_DIR="$HOME/.nvm"' >> /home/user/.bashrc && \
    echo '[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"' >> /home/user/.bashrc && \
    echo '[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"' >> /home/user/.bashrc && \
    # Create fcitx configuration directory and default config: \
    mkdir -p /home/user/.config/fcitx && \
    echo "[Hotkey]" > /home/user/.config/fcitx/config && \
    echo "TriggerKey=CTRL_SPACE" >> /home/user/.config/fcitx/config && \
    echo "SwitchKey=Alt_Shift_L" >> /home/user/.config/fcitx/config && \
    echo "[Program]" >> /home/user/.config/fcitx/config && \
    echo "DelayStart=0" >> /home/user/.config/fcitx/config && \
    echo "ShareStateAmongWindow=No" >> /home/user/.config/fcitx/config && \
    echo "[Output]" >> /home/user/.config/fcitx/config && \
    echo "HalfPuncAfterNumber=True" >> /home/user/.config/fcitx/config && \
    echo "RemindModeDisablePaging=True" >> /home/user/.config/fcitx/config && \
    echo "SendTextWhenSwitchEng=True" >> /home/user/.config/fcitx/config && \
    echo "CandidateWordNumber=5" >> /home/user/.config/fcitx/config && \
    echo "PhraseTips=True" >> /home/user/.config/fcitx/config && \
    echo "DontCommitPreeditWhenUnfocus=False" >> /home/user/.config/fcitx/config && \
    # Set proper ownership of all user files: \
    chown -R 1000:1000 /home/user
