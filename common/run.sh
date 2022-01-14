#!/bin/bash

oldest="2021-12-15"
#oldest="2000-01-01"

db="DBNAME"
dbuser="DBUSER"

here=${0%/*}

if [ "$2" = "" ]; then
  echo Usage: provincekey  datadir
  exit 1
fi

key="$1"
datadir="$2"
tsv=$datadir/data.tsv

if [ -d $datadir ]; then
  :
else
  echo data dir not a dir: $datadir
fi
if [ -f $tsv ]; then
  :
else
  echo tsv file not found: $tsv
  exit 1
fi

# skip if tsv is empty
if [ -s $tsv ]; then

   sql=$datadir/data.sql

   if $here/tsv-to-sql.py $db $key $oldest <$tsv >$sql
   then

     log=$datadir/insert.log
     err=$datadir/insert.err

     /usr/bin/psql -U $dbuser -d $db -f $sql >$log 2>$err

     echo
     echo lines in log
     wc -l $log

     if [ -a $err ]; then
        if [ -s $err ]; then
           echo check $err
           cat $err
        else
           rm -f $err
        fi
     fi

   else
     echo failed converting to sql
     exit 1
   fi
fi
