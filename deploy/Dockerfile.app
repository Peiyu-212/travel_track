##### Build Image
FROM python:3.12-slim-bullseye AS builder
LABEL maintainer Peiyu Jhong@wistron.com
ARG TZ=Asia/Taipei

RUN echo "deb http://opensource.nchc.org.tw/debian/ bullseye main" > /etc/apt/sources.list \
  && echo "deb http://opensource.nchc.org.tw/debian/ bullseye-updates main" >> /etc/apt/sources.list \
  && echo "deb http://opensource.nchc.org.tw/debian/ bullseye-proposed-updates main" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends\
  build-essential \
  libldap2-dev \
  #=2.4.47+dfsg-3+deb10u4 \
  libsasl2-dev \
  vim
RUN apt-get install -y wget \
  unzip \
  cron \
  && apt-get purge -y --auto-remove \
  && rm -rf /var/lib/apt/lists/*

RUN pip install psycopg2-binary==2.8.6

RUN ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime \
  && echo ${TZ} > /etc/timezone \
  && dpkg-reconfigure -f noninteractive tzdata

### Copy the Project
COPY ./backend /backend
COPY ./.env /.env
COPY ./backend/compose/local.txt /backend/requirements.txt

WORKDIR /backend


RUN pip install --upgrade pip
RUN pip install -r /backend/requirements.txt


COPY ./deploy/uwsgi.ini /etc/uwsgi/uwsgi.ini
RUN mkdir -p  /log \
  && chown -R www-data:www-data /log \
  && chown -R www-data:www-data /var/tmp/

### Start uWSGI on container startup
CMD ["/usr/local/bin/uwsgi", "--ini", "/etc/uwsgi/uwsgi.ini"]
