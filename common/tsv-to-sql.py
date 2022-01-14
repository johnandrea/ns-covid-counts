#!/usr/local/bin/python3

import sys
from word2number import w2n

# params:
# list of data tab hosp tab icu on stdin
# arg 1 = db name
# arg 2 = province name key
# arg 3 = oldest date


def is_int( s ):
    try:
       x = int( s )
       return True
    except ValueError:
       return False


def date_newer_than( since, given ):
    def make_compare( date_string ):
        parts = date_string.replace("'","").replace(' ','').split('-')
        return '%s%02d%02d' % ( parts[0], int(parts[1]), int(parts[2]) )
    return make_compare( given ) > make_compare( since )


def get_months():
    months = dict()
    months['jan'] = '01'
    months['feb'] = '02'
    months['mar'] = '03'
    months['apr'] = '04'
    months['may'] = '05'
    months['jun'] = '06'
    months['jul'] = '07'
    months['aug'] = '08'
    months['sep'] = '09'
    months['oct'] = '10'
    months['nov'] = '11'
    months['dec'] = '12'
    months['janurary'] = '01'
    months['january'] = '01'
    months['february'] = '02'
    months['febuary'] = '02'
    months['march'] = '03'
    months['april'] = '04'
    months['june'] = '06'
    months['july'] = '07'
    months['august'] = '08'
    months['september'] = '09'
    months['sept'] = '09'
    months['october'] = '10'
    months['november'] = '11'
    months['december'] = '12'
    return months


def fix_date( d, months ):
    # month might be full name
    # 2022-jan-12 => 2022-01-12
    # 2021-december-1 => 2021-12-1

    result = None

    if '-' in d or '/' in d:

       result = d.replace( ' ', '' ).replace('/','-').lower()

       # assume its close to an expected date format
       parts = result.split('-')

       if parts[1] in months:
          result = parts[0] +'-'+ months[parts[1]] +'-'+ parts[2]

       else:
          # better be numbers
          for part in parts:
              if not is_int( part ):
                 result = None
                 break

    return result


if len( sys.argv ) < 4:
   print( 'args: dbname province-key oldestdate', file=sys.stderr )
   sys.exit( 1 )

dbname = sys.argv[1]
prov_key = sys.argv[2].lower()
oldest_date = sys.argv[3]

dbtable = 'canada'
subselect = '(select id from province_names where key=\'' + prov_key + '\')'

print( '\\c ' + dbname )

months = get_months()

for line in sys.stdin:
    line = line.strip()
    if line:
       parts = line.split( '\t' )

       d = fix_date( parts[0], months )

       if d:
          if date_newer_than( oldest_date, d ):

             d = "'" + d + "'"

             insert = 'insert into ' + dbtable + ' (datatime,name_id)'
             insert += ' values(' + d + ',' + subselect + ')'
             insert += ' on conflict do nothing'

             update = 'update ' + dbtable + ' set'
             where = 'where name_id=' + subselect
             where += ' and datatime=' + d

             # sometimes field missing
             hosp = 'null'
             if len(parts) > 1:
                x = w2n.word_to_num( parts[1] )
                if x is not None:
                   hosp = x
             icu = 'null'
             if len(parts) > 2:
                x = w2n.word_to_num( parts[2] )
                if x is not None:
                   icu = x

             print( '' )
             print( insert, ';' )
             print( update, 'hospital=', hosp, where, ';' )
             print( update, 'icu=', icu, where, ';' )

       else:
          print( 'skipping bad date', parts[0], file=sys.stderr )
