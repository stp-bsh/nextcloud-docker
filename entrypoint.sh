#! /bin/bash
# TODO: add the nextcloud config.php and do the
#       replace for all important parameters
CMD="run"
if [ -z $1 ]
then
 CMD="apachectl -D FOREGROUND"
else
 if [ $1 == "debug" ]
 then
  CMD="bash"
 fi
fi
$CMD
