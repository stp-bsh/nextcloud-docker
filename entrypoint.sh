#! /bin/bash
sleep 10
if [ -z $1 ]
then
 CMD="apachectl -D FOREGROUND"
else
 if [ $1 == "debug" ]
 then
  CMD="bash"
 fi
fi
chown -R www-data:www-data /app

if [ ! -e /app/.is_installed ]
then
 sudo -u www-data /app/www/occ maintenance:install --database "mysql" --database-host "mysql" --database-name $NEXTCLOUD_DB_NAME --database-user $NEXTCLOUD_DB_USER \
   --database-pass $NEXTCLOUD_DB_PASS --admin-pass $NEXTCLOUD_ADMIN_PASS
fi

sudo -u www-data /app/www/occ config:system:set trusted_domains 0 --value=${NEXTCLOUD_PUB_DOMAIN}
sudo -u www-data /app/www/occ config:system:set overwrite.cli.url --value=${NEXTCLOUD_PUB_PROTO}://${NEXTCLOUD_PUB_DOMAIN}
echo "true" > /app/.is_installed
$CMD
