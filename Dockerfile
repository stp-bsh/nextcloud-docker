FROM ubuntu:latest
ENV NEXTCLOUD_VERSION "12.0.4"
ENV NEXTCLOUD_URL "https://download.nextcloud.com/server/releases"

RUN mkdir /app
WORKDIR /app
ADD entrypoint.sh .

RUN apt-get update \
 && apt-get install -y  apache2 php7.0 wget zip vim libapache2-mod-php7.0 \
 && a2enmod php7.0

RUN wget $NEXTCLOUD_URL/nextcloud-$NEXTCLOUD_VERSION.zip \
 && unzip nextcloud-$NEXTCLOUD_VERSION.zip \
 && rm -f nextcloud-$NEXTCLOUD_VERSION.zip \
 && mv nextcloud www \
 && chmod 770 entrypoint.sh

ADD files/apache2.conf /etc/apache2/apache2.conf
ADD files/nextcloud.conf /etc/apache2/nextcloud.conf


ENTRYPOINT ["./entrypoint.sh"]
