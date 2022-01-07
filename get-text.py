#!/usr/bin/python3

# Copyright 2022 (c) John Andrea
# Released under MIT License.
# No support implied.
#
# v1.0

# params:
# 1 = file of already handled urls
# 2 = dir to hold output text

import sys
from bs4 import BeautifulSoup
import requests


def only_numbers( s ):
    return s.replace(':','').replace(' ','')


def get_already_handled( filename ):
    result = []
    with open( filename ) as inf:
         for link in inf:
             if link:
                result.append( link.strip() )
    return result


def add_handled( filename, data ):
    with open( filename, 'a' ) as outf:
         print( data, file=outf )


def handle_page( url, data_dir ):
    print( url )

    result = True

    print( 'getting detail page', url )
    page = requests.get( url )

    if page.status_code != 200:
      print( 'page not found; error', page.status_code, ':', url, file=sys.stderr )

    else:
      data = page.text

      soup = BeautifulSoup( data, 'html.parser' )

      # <time datetime="2022-01-05T15:02:00-04:00">January 5, 2022 - 3:02 PM</time>

      time = None
      full_time = None

      print( 'checking for time' )
      for link in soup.findAll('time'):
          text = link.text
          ref = link.get('datetime')
          parts = ref.split( 'T' )
          if '20' in parts[0]:
             time = parts[0]
             # use the rest of the date in case there are multiples in one day
             full_time = parts[0] + '_' + only_numbers( parts[1] )
             break

      if time:
         # <div id="releaseBody">

         print( 'checking for body div' )
         for div in soup.findAll('div'):
            div_id = div.get('id')
            if div_id:
               if str(div_id.lower()) == 'releasebody':
                  with open( data_dir + '/' + full_time + '.body.txt', 'w' ) as outf:
                       print( div.text, file=outf )
                       print( 'saving' )
                  break

      else:
         result = False

    return result

if len( sys.argv ) < 3:
   print( 'missing params:  alreadyfile  datadir', file=sys.stderr )
   sys.exit( 1 )

already_file = sys.argv[1]
data_dir = sys.argv[2]

base_url = 'https://novascotia.ca/news/search/'
url = base_url + '?dept=180'

french_words = ['nouveaux', 'La dose de rappel']

print( 'getting base page' )
page = requests.get( url )

if page.status_code != 200:
   print( 'page not found; error', page.status_code, ':', url, file=sys.stderr )

else:
   already = get_already_handled( already_file )

   data = page.text

   soup = BeautifulSoup( data, 'html.parser' )

   # get all the links on this pge

   print( 'checking links' )

   for link in soup.findAll('a'):
       href = link.get('href')
       if href not in already:
          text = link.text
          if 'covid' in text.lower() and '?id=' in href:

             # skip french
             ok = True
             for word in french_words:
                 if word.lower() in text.lower():
                    ok = False
                    break

             if ok:
                print( '' )
                print( href, text )
                if handle_page( base_url + href, data_dir ):
                   add_handled( already_file, href )
