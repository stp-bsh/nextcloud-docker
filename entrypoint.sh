#! /bin/bash
# TODO: add the nextcloud config.php and do the
#       replace for all important parameters"
sleep 20
if [ -z $1 ]
then
 CMD="apachectl -D FOREGROUND"
else
 if [ $1 == "debug" ]
 then
  CMD="bash"
 fi
fi
/app/www/occ maintenance:install --database "mysql" --database-host "mysql" --database-name $NEXTCLOUD_DB_NAME --database-user $NEXTCLOUD_DB_USER \
  --database-pass $NEXTCLOUD_DB_PASS --admin-pass $NEXTCLOUD_ADMIN_PASS
chown -R www-data:www-data /app
$CMD
