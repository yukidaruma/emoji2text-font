FROM python:3.13.6-bookworm

RUN apt-get update && apt-get install -y \
    fontforge \
    fonttools \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash user
USER user
