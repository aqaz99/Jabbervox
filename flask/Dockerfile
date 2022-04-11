FROM ubuntu:20.04

# For tzdata
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=America/California

RUN apt-get update -y && \
    apt-get install -y python3-pip python-dev \
    ffmpeg

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

CMD [ "python3", "app.py"]