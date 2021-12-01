FROM ubuntu

ENV DEBIAN_FRONTEND noninteractive
# install library required to build staq
RUN apt-get update && apt-get install -y build-essential git cmake

# Install staq from source
RUN git clone https://github.com/softwareQinc/staq.git \
  && cd staq && mkdir build && cd build && \
  cmake .. && make -j8 && make install

# Setup Poetry Environment
RUN apt-get install -y python3 curl python3-distutils python3-dev
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
ENV PATH $PATH:/root/.poetry/bin

WORKDIR /ouqu-tp
