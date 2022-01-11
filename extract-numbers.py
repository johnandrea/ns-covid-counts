#!/usr/bin/python3

import sys
import re
from word2number import w2n

patterns = []

# There are 40 people in hospital with five in ICU
pattern = 'there are (.+?) people in hospital with (.+?) in icu'

patterns.append( re.compile( '.*' + pattern.lower() ) )

# Of those, 34 people are in hospital, including 4 in ICU.
pattern = 'of those, (.+?) people are in hospital, including (.+?) in icu'

patterns.append( re.compile( '.*' + pattern.lower() ) )


def get_numbers( m ):
    # given a regex match, return exit status option
    # if matched, then print the two numbers

    result = 0

    first = w2n.word_to_num( m.group(1) )
    if first is not None:
       second = w2n.word_to_num( m.group(2) )
       if second is not None:
          print( first, second )
       else:
          result = 1
    else:
       result = 1
       print( 'didnt convert' )

    return result


data = ''
for line in sys.stdin:
    data += ' ' + line

text = data.lower().replace( '\t', ' ' )
text = text.replace( '\n', ' ' ).replace( '\r', ' ' )
text = text.replace( '  ', ' ' ).strip()

status = 0
found = False

for pattern in patterns:
    if not found:
       m = pattern.match( text )
       if m:
          found = True
          status = get_numbers( m )

if not found:
   # didn't match, return failure so that the input file will not be removed
   status = 1

sys.exit( status )
