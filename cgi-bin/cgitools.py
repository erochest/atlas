#! D:\Python23\python.exe

import cgi
import re
from string import join
import sys
import traceback


__reSanitize = re.compile(r'[^\w\.#_-]')


def sanitize(str):
    return __reSanitize.sub(' ', str)

def error(msg='', b=0):
    print 'Content-type: text/html'
    print
    sys.stderr = sys.stdout

    print '''<html>
  <head><title>Error</title></head>
  <body>
    <h1>Error:</h1>
    <p>%s</p>''' % msg

    if b:
        print '    <pre>'
        traceback.print_exc()
        print '    </pre>'
    print '  </body></html>'

def getValues(map={}, cgiquery=cgi.FieldStorage()):
    for key in map.keys():
        if cgiquery.has_key(key) and cgiquery[key].value:
            map[key] = sanitize(cgiquery[key].value)
    return map

