FROM ubuntu:latest
ENV NEXTCLOUD_VERSION "12.0.4"
ENV NEXTCLOUD_URL "https://download.nextcloud.com/server/releases"
ENV NEXTCLOUD_DB "TODOi!!"
ENV NEXTCLOUD_DB_USR "TODO!!"
ENV NEXTCLOUD_DB_PW "TODO!!"
ENV NEXTCLOUD_DB_HOST "TODO!!"
ENV NEXTCLOUD_TRUSTED_DOMAINS "TODO!!"

RUN apt-get update \
 && apt-get install -y  apache2 php7.0 wget zip vim libapache2-mod-php7.0 \
 && service apache2 stop

RUN mkdir /app
WORKDIR /app

RUN wget $NEXTCLOUD_URL/nextcloud-$NEXTCLOUD_VERSION.zip \
 && unzip nextcloud-$NEXTCLOUD_VERSION.zip \
 && rm -f nextcloud-$NEXTCLOUD_VERSION.zip \
 && mv nextcloud www 

ADD entrypoint.sh .
RUN chmod 770 entrypoint.sh \
 && mkdir ./www/custom_apps
ADD files/apache2.conf /etc/apache2/apache2.conf
ADD files/nextcloud.conf /etc/apache2/nextcloud.conf
ADD files/nextcloud_config.php ./www/config/config.php

ENTRYPOINT ["./entrypoint.sh"]
