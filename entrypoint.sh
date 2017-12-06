#! /bin/bash
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
