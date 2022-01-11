#!/usr/bin/python3

import re

patterns = []
patterns.append( 'some (.*) or' )     # anything between
patterns.append( 'some (.*?) or' )    # non-greedy
patterns.append( 'some ([^\.]+) or' ) # stop at first sentence

data = []
data.append( 'some thing or another.' )
data.append( 'some thing or another. and second or more.' )

print( 'expecting: thing' )
for s in data:
    print( '' )
    print( 'input:', s )

    for pattern in patterns:
        p = re.compile( '.*' + pattern )
        m = p.match( s )
        if m:
           print( pattern, '=> ', m.group(1) )
        else:
           print( pattern, '- no match' )
