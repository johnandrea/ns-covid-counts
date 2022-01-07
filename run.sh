#!/bin/bash

# Copyright 2022 (c) John Andrea
# Released under MIT License.
# No support implied.
#
# v1.0

table="canada"
subselect="(select id from province_names where name='Nova Scotia')"
where="where name_id=$subselect"
noerror="on conflict do nothing"
q="'"

export PGPASSWORD="PASSWORD"

here=${0%/*}

already=$here/already.dat

datadir=$here/data
archive=$here/archive

touch $already
mkdir -p $datadir 2>/dev/null
mkdir -p $archive 2>/dev/null

tmpfile=$here/tmp.tmp

# produce body of web press releases
# named with the date and time of the release  date underscore time .body.txt

$here/get-text.py $already $datadir

ls -1 "$datadir" | grep body.txt |
while read file; do
   echo checking for counts in $file

   infile="$datadir/$file"

   # the prase "people in hospital" is needed

   if cat $infile | tr '\n' ' ' | grep -i "in  *hospital" >/dev/null
   then

      date=$(echo $file | cut -f1 -d_)
      outfile="$here/counts.tmp"

      # failure could mean that the sentence pattern did not match
      # look at the data file for the sentence

      if $here/extract-numbers.py  <$infile  >$outfile
      then

         # must have two numbers separated by a space
         # 123 455   or  3 72   or  82 7
         # but if it doesn't still could be a problem with the sentence

         cat $outfile |
         tr '\t' ' ' |
         tr -s ' ' | sed 's/^ //' | sed 's/ $//' |
         grep "[0-9] [0-9]" >$tmpfile

         # take the 'tail' because the province wide numbers seem to be listed last

         if [ -s "$tmpfile" ]; then
            first=$(tail -1 $tmpfile | cut -f1 -d" ")
            second=$(tail -1 $tmpfile | cut -f2 -d" ")

            insert=$here/latest.insert
            sql=$here/$file.sql
            err=$here/$file.err

            echo "\\c covid19" >$sql
            echo "insert into $table (datatime,name_id) values ($q$date$q,$subselect) $noerror;" >>$sql
            echo "update $table set hospital=$first,icu=$second $where and datatime=$q$date$q;" >>$sql

            # leave a copy of the sql right here for checking format, etc
            cp $sql $here/latest.sql

            if /usr/bin/psql -U DBUSER -d covid19 -f $sql >$insert 2>$err
            then
              # all done with the web page
              mv $sql $archive
              mv $infile $archive
              rm -f $err
            else
              if [ -a $err ]; then
                if [ -s $err ]; then
                  echo check $err
                else
                  rm -f $err
                fi
              fi
            fi

            cat $insert

          fi

          # leave a non-unique copy of the numbers right here for checking
          mv $tmpfile $here/latest.counts
      fi

      rm -f $outfile
   else

     echo no word hospital
     rm -f $infile
   fi

done
