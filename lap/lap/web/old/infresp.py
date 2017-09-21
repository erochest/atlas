#! /usr/bin/env python

from lap import settings
import cgi, cgitb, csv, glob, os

DATADIR = settings.locale.old_data
BASEOLD = settings.locale.baseold
BASECGI = settings.locale.basecgi

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

def get_filenames(project, tables):
    for pattern in tables:
        for filename in glob.glob(os.path.join(DATADIR, project, pattern)):
            if os.path.isfile(filename):
                yield filename
    return

def main():
    cgitb.enable()
    fs = cgi.FieldStorage()
    project = fs.getfirst('project', '')
    informid = fs.getfirst('informid', '')
    tables = fs.getlist('tables')
    props = read_properties(os.path.join(DATADIR, project+'.properties'))
    rev_props = dict(
        [ (value, key) for (key, value) in props.items() ]
        )

    print 'Content-Type: text/html'
    print
    print '<html><head>'
    print '<title>%s Responses for Informant %s</title>' % (
        project.upper(), informid)
    print '</head>'
    print '<body>'
    print '<h2>%s Responses for Informant %s</h2>' % (
        project.upper(), informid)

    for filename in get_filenames(project, tables):
        basename = os.path.basename(filename)
        if basename not in rev_props:
            continue
        title = rev_props[basename][:-6]
        title = title.replace('.', ' ')
        title = title.title()
        print '<h3>Responses to', title, '</h3>'
        print '<table border="1"><tbody>'
        lines = list(csv.reader(file(os.path.join(DATADIR, project, basename),
                                     'rb')))
        lines = [ item for item in lines if item[1] == informid ]
        for data in lines:
            print '<tr><th>Record No.</th><td>', data[9], '</td>'
            print '<th>Informant ID</th><td><a href="%s/infprofile.py?project=%s&informid=%s">%s</a></td>' % (BASECGI, project, data[1], data[1])
            print '<th>Old ID</th><td>', data[1], '</td></th>'
            print '<th>Gram. Category</th><td>', data[3], '</td></tr>'
            print '<tr><th>Std. Orthography</th>'
            print '<td colspan="7">', data[0], '</td></tr>'
            print '<tr><th>Pronunciation</th>'
            print '<td colspan="7"><font face="LAMCOUR, LAMSAS Courier, monospace">', data[7], '</font></td></tr>'
            print '<tr><th>Doubt</th><td>', data[4], '</td>'
            print '<th>Comment</th><td>', data[6], '</td>'
            print '<th>Comtext</th><td colspan="3">', data[5], '</td></tr>'
            print '<tr><td colspan="8"><img src="%s/img/pixel.gif" height="10" width="1"></td></tr>' % BASEOLD
        print '</tbody></table></body></html>'

