#! /usr/bin/env python

import cgi, cgitb, os
from lap import settings

def error_page():
    print 'Content-Type: text/html'
    print
    print '<html>\n<head><title>Error</title></head>\n<body>'
    print '<p><b>Error:</b> Please supply both the project and file.</p>'
    print '</body></html>'

def main():
    cgitb.enable()
    fs = cgi.FieldStorage()
    project = fs.getfirst('project')
    filename = fs.getfirst('file')
    if not filename or not project:
        error_page()
    else:
        print 'Content-type: text/csv'
        print
        print file(os.path.join(settings.locale.old_data, project,
                                filename)).read()

