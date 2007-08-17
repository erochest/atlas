#! /usr/bin/env python

from lap import settings
from urllib import urlencode
import cgi, cgitb, csv, glob, os, sys

DATADIR = settings.locale.old_data
BASEOLD = settings.locale.baseold
BASECGI = settings.locale.basecgi

FORMAT = '%-6s %-6s %-6s %-30s %-30s'
LENGTHS = (6, 6, 6, 30, 30)
INDICES = (9, 1, 2, 0, 7)

def read_properties(filename):
    props = {}
    for line in file(filename):
        try:
            (prop, value) = line.split('=', 1)
        except ValueError:
            continue
        else:
            props[prop] = value.strip()
    return props

def write_row(row, fmt=FORMAT, lens=LENGTHS, indices=INDICES):
    data = [ str(row[i])[:length] for (i, length) in zip(indices, lens) ]
    print fmt % tuple(data)

def main():
    cgitb.enable()
    fs = cgi.FieldStorage()
    project = fs.getfirst('project')
    for_ = fs.getfirst('for')
    in_ = fs.getfirst('in')
    props = read_properties(os.path.join(DATADIR, project+'.properties'))

    print 'Content-Type: text/html'
    print

    print '<html>\n<head>'
    print '<title>', project.upper(), 'Lingusitic Databases Search for', \
        repr(for_), '</title>'
    print '</head>\n<body>'

    print '<h2>', project.upper(), 'Linguistic Databases Search<br>'
    print 'for', repr(for_), '</h2>'
    print '<p>Links:</p>'
    print '<ul><li><a href="%s/fields.html">Explanation of the fields.' \
        '</a></li>' % BASEOLD
    print '<li><a href="%s/%s/lingsearch.html">Back to Linguistic Database ' \
        'Search</a></li></ul>' % (BASEOLD, project)
    print

    tables = dict([
        (os.path.normpath(os.path.join(DATADIR, project, props[key])), key[:-6])
        for key in props
        if key.endswith('.table')
        ])

    hits = {}
    for_lower = for_.lower()
    for filename in glob.glob(os.path.join(DATADIR, project, in_+'.asc')):
        filename = os.path.normpath(filename)
        for data in csv.reader(file(filename, 'rb')):
            if data[0].lower().find(for_lower) != -1:
                hits.setdefault(filename, []).append(data)
    files = [ f for f in hits if f in tables ]
    if not files:
        print '</p>No matches found</p>\n</body>\n</html>'
        return
    files.sort()

    print '<p><b>', repr(for_), 'found in', len(files), \
        'file(s):</b></p>\n<ol>'
    for filename in files:
        tables[filename] = tables[filename].replace('.', ' ')
        print '<li><a href="#%s">%s</a></li>' % (
            tables[filename], tables[filename])
    print '</ol>\n<hr>'

    notetmpl = os.path.join(DATADIR, project, 'headnotes', 'headnote_')
    for filename in files:
        short_file = os.path.basename(filename)
        note_file = '%s%s.txt' % (notetmpl, os.path.splitext(short_file)[1])
        print '<b><a name="%s">%s</a></b>' % (
            tables[filename], tables[filename])
        q = {'project': project,
             # for browse.py
             'ling': '%s:%s' % (tables[filename], short_file),
             'lingstyle': 'plain',
             # for map.py
             'file': short_file, 'table': tables[filename], 'search': for_,
             }
        q = urlencode(q)
        sys.stdout.write('<i><a href="%s/browse.py?%s">(full listing)</a> ' %
                         (BASECGI, q))
        sys.stdout.write('<a href="%s/map.py?%s">(map)</a> ' % (BASECGI, q))
        if os.path.exists(note_file):
            sys.stdout.write('<a href="%s/headnotes.py?%s">(notes)</a> ' %
                             (BASECGI, q))
        sys.stdout.write('</i><br>\n<pre>\n')
        print '<a href="%s/fields.html#serial">Serial</a> ' \
            '<a href="%s/fields.html#informid">Inf#</a>   ' \
            '<a href="%s/fields.html#oldnumbe">Old#</a>   ' \
            '<a href="%s/fields.html#item">Item</a>                           ' \
            '<a href="%s/fields.html#phnitem">Phonetics</a>' % (
            BASEOLD, BASEOLD, BASEOLD, BASEOLD, BASEOLD)

        for hit in hits[filename]:
            write_row(hit)

        print
        print '</pre>\n<hr>'

    print '</body>\n</html>'

