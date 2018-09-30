FROM ubuntu:16.04
ENV NEXTCLOUD_VERSION "14.0.1"
ENV NEXTCLOUD_URL "https://download.nextcloud.com/server/releases"
ENV NEXTCLOUD_DB_NAME "nextcloud"
ENV NEXTCLOUD_DB_PASS "nextcloud"
ENV NEXTCLOUD_DB_USER "nextcloud"
ENV NEXTCLOUD_ADMIN_PASS "nextcloud"
ENV NEXTCLOUD_PUB_PROTO "https"
ENV NEXTCLOUD_PUB_DOMAIN "nextcloud.example.com"

RUN apt-get update \
 && apt-get install -y  \
     apache2 \
     php7.0 \
     wget \
     zip \
     sudo \
     libapache2-mod-php7.0 \
     php7.0-mysql \
     php7.0-zip \
     php7.0-dom \
     php7.0-XMLWriter \
     php7.0-XMLReader \
     php7.0-xml \
     php7.0-mb \
     php7.0-GD \
     php7.0-SimpleXML \
     php7.0-cURL \
 && a2enmod headers \
 && service apache2 stop \
 && mkdir /app \
 && mkdir /app/www \
 && mkdir /app/www/data \
 && mkdir /app/www/custom_apps

WORKDIR /app
ADD entrypoint.sh .
ADD ./files/php.ini /etc/php/7.0/apache2/php.ini

RUN wget $NEXTCLOUD_URL/nextcloud-$NEXTCLOUD_VERSION.zip \
 && unzip nextcloud-$NEXTCLOUD_VERSION.zip \
 && rm -f nextcloud-$NEXTCLOUD_VERSION.zip \
 && cp nextcloud/.htaccess /app/www/.htaccess \
 && cp nextcloud/.user.ini /app/www/.user.ini \
 && mv nextcloud/* www/ \
 && rm -fr nextcloud \
 && chmod 770 ./entrypoint.sh \
 && chmod 770 ./www/occ

ADD files/apache2.conf /etc/apache2/apache2.conf
ADD files/nextcloud.conf /etc/apache2/nextcloud.conf

ENTRYPOINT ["./entrypoint.sh"]
