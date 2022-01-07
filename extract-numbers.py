#!/usr/bin/python3

# Copyright 2022 (c) John Andrea
# Released under MIT License.
# No support implied.
#
# v1.0

import sys
import re
from word2number import w2n

# There are 40 people in hospital with five in ICU
full_phrase = re.compile( r'.*there are (.*) people in hospital with (.*) in icu' )

# Of those, 34 people are in hospital, including 4 in ICU.
shorter_phrase = re.compile( r'.*of those, (.*) people are in hospital, including (.*) in icu' )


def get_numbers( m ):
    # given a regex match, return exit status option
    # if matched, the print the two numbers

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
       print( 'didnt convert:', data )

    return result


input = ''

for line in sys.stdin:
    input += ' ' + line.strip().lower()

text = input.replace( '  ', ' ' ).replace( '  ', ' ' ).strip()

status = 0

m = full_phrase.match( text )
if m:
  status = get_numbers( m )

else:
  m = shorter_phrase.match( text )
  if m:
    status = get_numbers( m )

  else:
    # didn't match, return failure so that the input file will not be removed
    status = 1

sys.exit( status )
