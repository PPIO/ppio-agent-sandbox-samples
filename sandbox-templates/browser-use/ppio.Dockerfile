FROM ubuntu:22.04

# Set non-interactive mode
ENV DEBIAN_FRONTEND=noninteractive

# Install packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unzip \
    net-tools \
    bash \
    ca-certificates \
    libglib2.0-0 \
    libdbus-1-3 \
    libx11-6 \
    libxcb1 \
    libexpat1 \
    libfontconfig1 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libdrm2 \
    libgbm1 \
    libasound2 \
    # Chinese language and font support: \
    locales \
    language-pack-zh-hans \
    language-pack-zh-hant \
    fonts-wqy-zenhei \
    fonts-wqy-microhei \
    fonts-arphic-ukai \
    fonts-arphic-uming \
    fonts-noto \
    fonts-noto-cjk \
    fonts-noto-color-emoji \
    fonts-liberation \
    fonts-dejavu-core \
    # Chinese input method (fcitx): \
    fcitx \
    fcitx-googlepinyin \
    fcitx-module-cloudpinyin \
    fcitx-sunpinyin \
    fcitx-config-gtk \
    fcitx-frontend-gtk2 \
    fcitx-frontend-gtk3 \
    fcitx-ui-classic \
    && rm -rf /var/lib/apt/lists/*

# Set input method environment variables
ENV \
    INPUT_METHOD=fcitx \
    GTK_IM_MODULE=fcitx \
    QT_IM_MODULE=fcitx \
    XMODIFIERS=@im=fcitx \
    SDL_IM_MODULE=fcitx

# Set working directory
WORKDIR /app

# Copy scripts directory
COPY scripts/ /app/scripts/

# Set script permissions
RUN chmod +x /app/scripts/*.sh

# Download Chromium
RUN cd /app/scripts && bash ./update.sh

# Copy pre-compiled WebSocket proxy binary
COPY reverse-proxy /app/reverse-proxy
RUN chmod +x /app/reverse-proxy

# Create browser-use directory
RUN mkdir -p /app/.browser-use

# Copy startup script
COPY start-up.sh /app/.browser-use/start-up.sh

# Set startup script permissions
RUN chmod +x /app/.browser-use/start-up.sh

# Create user data directory
RUN mkdir -p /app/user-data-dir

# Configure input method
RUN mkdir -p /root/.config/fcitx && \
    echo "[Hotkey]" > /root/.config/fcitx/config && \
    echo "TriggerKey=CTRL_SPACE" >> /root/.config/fcitx/config && \
    echo "SwitchKey=Alt_Shift_L" >> /root/.config/fcitx/config && \
    echo "[Program]" >> /root/.config/fcitx/config && \
    echo "DelayStart=0" >> /root/.config/fcitx/config && \
    echo "ShareStateAmongWindow=No" >> /root/.config/fcitx/config && \
    echo "[Output]" >> /root/.config/fcitx/config && \
    echo "HalfPuncAfterNumber=True" >> /root/.config/fcitx/config && \
    echo "RemindModeDisablePaging=True" >> /root/.config/fcitx/config && \
    echo "SendTextWhenSwitchEng=True" >> /root/.config/fcitx/config && \
    echo "CandidateWordNumber=5" >> /root/.config/fcitx/config && \
    echo "PhraseTips=True" >> /root/.config/fcitx/config && \
    echo "DontCommitPreeditWhenUnfocus=False" >> /root/.config/fcitx/config

# Set input method environment in system environment
RUN echo "INPUT_METHOD=fcitx" >> /etc/environment && \
    echo "GTK_IM_MODULE=fcitx" >> /etc/environment && \
    echo "QT_IM_MODULE=fcitx" >> /etc/environment && \
    echo "XMODIFIERS=@im=fcitx" >> /etc/environment && \
    echo "SDL_IM_MODULE=fcitx" >> /etc/environment
