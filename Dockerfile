FROM ubuntu:latest
ENV NEXTCLOUD_VERSION "12.0.4"
ENV NEXTCLOUD_URL "https://download.nextcloud.com/server/releases"

RUN mkdir /app
WORKDIR /app

RUN apt-get update \
 && apt-get install -y  apache2 php7.0 wget zip

RUN wget $NEXTCLOUD_URL/nextcloud-$NEXTCLOUD_VERSION.zip \
 && unzip nextcloud-$NEXTCLOUD_VERSION.zip \
 && rm -f nextcloud-$NEXTCLOUD_VERSION.zip
