# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.209.6/containers/cpp/.devcontainer/base.Dockerfile

# [Choice] Debian / Ubuntu version (use Debian 11/9, Ubuntu 18.04/21.04 on local arm64/Apple Silicon): debian-11, debian-10, debian-9, ubuntu-21.04, ubuntu-20.04, ubuntu-18.04
ARG VARIANT="bullseye"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.9-${VARIANT}

ENV DEBIAN_FRONTEND noninteractive

# install library required to build staq
RUN apt-get update && apt-get install -y build-essential git cmake

# Install staq from source
RUN git clone https://github.com/softwareQinc/staq.git \
  && cd staq && mkdir build && cd build && \
  cmake .. && make -j8 && make install

# Setup Python Environment
RUN apt-get install -y python3 curl python3-distutils python3-dev

# Poetry
ENV POETRY_HOME=/home/vscode/.local/share/pypoetry
ENV PATH="${POETRY_HOME}/bin:${PATH}"
RUN curl -sSL https://install.python-poetry.org | python3 -

# change user to vscode
USER vscode

WORKDIR /ouqu-tp
