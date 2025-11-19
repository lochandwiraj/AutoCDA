FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    ca-certificates \
    wget \
    unzip && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /usr/share/kicad/symbols

RUN wget https://gitlab.com/kicad/libraries/kicad-symbols/-/archive/master/kicad-symbols-master.zip -O /tmp/symbols.zip && \
    unzip /tmp/symbols.zip -d /tmp/symbols && \
    cp /tmp/symbols/kicad-symbols-master/*.kicad_sym /usr/share/kicad/symbols/ && \
    rm -rf /tmp/symbols /tmp/symbols.zip

# Set ALL KiCad symbol search paths
ENV KICAD_SYMBOL_DIR="/usr/share/kicad/symbols"
ENV KICAD6_SYMBOL_DIR="/usr/share/kicad/symbols"
ENV KICAD7_SYMBOL_DIR="/usr/share/kicad/symbols"
ENV KICAD8_SYMBOL_DIR="/usr/share/kicad/symbols"
ENV KICAD9_SYMBOL_DIR="/usr/share/kicad/symbols"

RUN pip install skidl

RUN useradd -m -u 1000 skidl_user
USER skidl_user

WORKDIR /workspace
