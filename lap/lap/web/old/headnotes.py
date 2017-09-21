#! /usr/bin/env python

from lap import settings
import cgi, cgitb, os, sys

newline = '\n'
empty = ''


def wrap(paragraph, width=72, indent=0):
    i = 0
    length = len(paragraph)
    effectiveWidth = width - indent
    indentStr = ' ' * indent
    buffer = []
    if (length <= effectiveWidth):
        return '%s%s' % (indentStr, paragraph)
    while ((length - i) > effectiveWidth):
        right = paragraph.rfind(' ', i, i + effectiveWidth)
        if right == -1:
            right = paragraph.find(' ', i + effectiveWidth)
            if right == -1:
                break
        buffer.append('%s%s' % (indentStr, paragraph[i:right].lstrip()))
        i = right + 1
    buffer.append('%s%s' % (indentStr, paragraph[i:].lstrip()))
    return newline.join(buffer)

def error_page():
    print 'Content-Type: text/html'
    print
    print '<html>\n<head><title>Error</title></head>\n<body>'
    print '<p><b>Error:</b> Please supply both the project and file.</p>'
    print '</body></html>'

def main():
    cgitb.enable()
    fs = cgi.FieldStorage()
    if not fs.getfirst('project') or not fs.getfirst('file'):
        error_page()
        return
    # get rid of '.asc'
    (basename, ext) = os.path.splitext(fs.getfirst('file'))
    lines = list(file(os.path.join(settings.locale.old_data, 'headnotes',
                                   'headnote_%s.txt' % basename)))

    print 'Content-type: text/html'
    print

    print '''<html>
<head>
<title>Headnote information for %(file)s in project %(project)s</title>
<style type="text/css">
.PHONE { font-family: LAMCOUR, monospace; }
</style>
</head>
<body><pre class="PHONE">
''' % fs
    print empty.join(map(wrap, lines))
    print '</pre></body></html>'

