FROM python:3.9-slim

WORKDIR /usr/app/src

ARG LANG='en_us.UTF-8'

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-utils \
        locales \
        python3-pip \
        python3-yaml \
        rsyslog systemd systemd-cron sudo \
    && apt-get clean

RUN pip3 install --upgrade pip

RUN pip3 install streamlit

RUN pip3 install pymongo

RUN pip3 install datetime

RUN pip3 install configparser


COPY / ./

CMD ["streamlit","run","app.py"]