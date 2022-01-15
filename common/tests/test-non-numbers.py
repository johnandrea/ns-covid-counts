#!/usr/local/bin/python3

import sys
from word2number import w2n

def fix_number( given ):
    result = None
    if given == 'null':
       result = given
    elif given == '':
       result = 'null'
    else:
       try:
          result = w2n.word_to_num( given )
       except ValueError:
          print( 'non-numeric found:', given, file=sys.stderr )
    return result


def run_test( s ):
    x = fix_number( s )
    print( s, '=>', x )


run_test( '5' )
run_test( 'five' )
run_test( '' )
run_test( 'null' )
run_test( 'nothing' )
run_test( 'twenty-two' )
