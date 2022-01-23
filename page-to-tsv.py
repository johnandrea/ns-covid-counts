#!/usr/local/bin/python3

# params:
# html page on stdin

import sys
import re
from bs4 import BeautifulSoup

# all cases so far have hospitalized count first, icu second

# these patterns need to stop on sentences (.), not just non-greedy strings

patterns = []

#<p>Today, January 15, Nova Scotia is reporting 58 people in hospital
# who were admitted due to COVID-19 and are receiving specialized care
# in a COVID-19 designated unit.</p> <p>Ten people are in ICU today.

pattern = 'Nova Scotia is reporting ([^\\.]+?) people in hospital'
pattern += ' who were admitted due to COVID-19 and are receiving specialized'
pattern += ' care in a COVID-19 designated unit\\.'
pattern += ' ([^\\.]+?) people are in ICU'

patterns.append( re.compile( '.*' + pattern.lower() ) )

# There are 40 people in hospital with five in ICU
pattern = 'there are ([^\\.]+) people in hospital with ([^\\.]+) in icu'

patterns.append( re.compile( '.*' + pattern.lower() ) )

# Of those, 34 people are in hospital, including 4 in ICU.
pattern = 'of those, ([^\\.]+) people are in hospital, including ([^\\.]+) in icu'

patterns.append( re.compile( '.*' + pattern.lower() ) )

#There are 59 people in hospital who were admitted due to COVID-19
# and are receiving specialized care in a COVID-19 designated unit.
# That includes seven people in ICU.

pattern = 'There are ([^\\.]+?) people in hospital who were admitted due to COVID-19'
pattern +=' and are receiving specialized care in a COVID-19 designated unit.'
pattern +=' That includes ([^\\.]+?) people in ICU.'

patterns.append( re.compile( '.*' + pattern.lower() ) )

# use these words to try and detect if the page is french
french_words = []
french_words.append( "Aujourd\'hui" )
french_words.append( "Aujourd’hui" )
french_words.append( "sont aux soins intensifs" )


def get_date( data ):

    soup = BeautifulSoup( data, 'html.parser' )

    result = None

    # <time datetime="2022-01-05T15:02:00-04:00">January 5, 2022 - 3:02 PM</time>

    for link in soup.findAll('time'):
        ref = link.get('datetime')
        parts = ref.split( 't' )
        if '20' in parts[0]:
           # use the rest of the date in case there are multiples in one day
           result = parts[0]
           break

    return result

exit_code = 1

data = ''
for line in sys.stdin:
    data += line

d = get_date( data.lower() )

if d:

   search_data = data.lower().replace('\n',' ').replace('\r',' ')
   search_data = search_data.replace('<p>', ' ' ).replace('</p>', ' ')
   search_data = re.sub(r'\s+',' ',search_data).strip()

   # skip a page which is french
   for word in french_words:
       if exit_code > 0:
          if word.lower() in search_data:
             # 'ok' on exit so that this page is ignored
             exit_code = 0

   if exit_code > 0:
      for pattern in patterns:
          m = pattern.match( search_data )
          if m:
             exit_code = 0
             print( d +'\t' + m.group(1) +'\t'+ m.group(2) )
             break

      if exit_code > 0:
         print( 'no pattern match', file=sys.stderr )
         print( 'has date:', d, file=sys.stderr )

else:
  # no, date - then maybe this isn't a file of value
  # exit ok so that link is skipped
  exit_status = 0

sys.exit( exit_code )
