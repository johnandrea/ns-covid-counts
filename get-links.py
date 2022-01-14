#!/usr/local/bin/python3

# params:
# html file on stdin
# 1 = file of already handled urls

import sys
from bs4 import BeautifulSoup


def get_already_handled( filename ):
    result = []
    with open( filename ) as inf:
         for link in inf:
             if link:
                result.append( link.strip() )
    return result


if len( sys.argv ) < 2:
   print( 'missing params: alreadyfile', file=sys.stderr )
   sys.exit( 1 )

already = get_already_handled( sys.argv[1] )

data = ''
for line in sys.stdin:
    line = line.strip()
    if line:
       data += ' ' + line

soup = BeautifulSoup( data.replace('  ',' ').strip(), 'html.parser' )

# get all the links on this page
# but skip any with french labels

french_words = ['nouveaux', 'La dose de rappel']

for link in soup.findAll('a'):
    href = link.get('href')
    if href:
       if href not in already:

          text = link.text.lower()

          ok = True
          for word in french_words:
              if word.lower() in text:
                 ok = False
                 break

          if ok:
             # in mid Jan the link labels became less specific
             #if 'covid' in text and '?id=' in href:
             if '?id=' in href:
                print( href )
