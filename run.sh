#!/bin/bash

url="https://novascotia.ca/news/search/?dept=180"
prov="ns"

date

here=${0%/*}

cd $here
mkdir failed 2>/dev/null
mkdir data 2>/dev/null

already=$here/already.dat
touch $already

top=data/top-data.html
links=data/data.links
tsv=data/data.tsv
data=data/data.html

echo getting top page
if wget -k -nv -O $top $url
then
  if ./get-links.py $already <$top >$links
  then

    echo
    echo getting pages

    # append to tsv output because of multiple links
    echo -n >$tsv

    cat $links |
    while read link; do

       echo
       echo getting release

       if wget -nv -O $data "$link"
       then

          if ./page-to-tsv.py <$data >>$tsv
          then
             echo $link >>$already
          else

            if grep -i hospital $data >/dev/null
            then
              # maybe, because it contains that word, just the pattern changed
              sleep 1
              now=$(date '+%Y%m%d-%H%M%S')
              echo saving to failed location
              cp $data failed/$now.html
              echo $link > failed/$now.link

            else
              echo failed tsv, no hospital word
            fi
          fi

       else
          # to try again later, check against "already" list
          echo getting data page failed
          now=$(date '+%Y%m%d')
          echo saving link to failed
          echo $link >> failed/$now.links
       fi
    
    done

    if $here/common/run.sh $prov $here/data
    then
      :
    else
      echo failed database
      # why did this fail? and how can it be recovered
      now=$(date '+%Y%m%d')
      cp $tsv failed/$now.tsv      
    fi

  else
     echo link collection failed
  fi
else
  echo wget failed
fi

date
