#! /usr/bin/env python

from lap import settings
import cgi, cgitb, csv, os
from urllib import quote_plus, urlencode

DATADIR = settings.locale.old_data
BASEOLD = settings.locale.baseold
BASECGI = settings.locale.basecgi

LINGPLAIN_FORMAT = '%-6s %-6s %-6s %-30s %-30s'
LINGPLAIN_LENS = (6, 6, 6, 30, 30)
LINGPLAIN_INDICES = (9, 1, 2, 0, 7)
INFPLAIN_FORMAT = '%-6s %-3s %-10s %-5s %-2s %-4s %-3s %-3s %-4s %-3s %-4s ' \
    '%-4s %-5s'
INFPLAIN_LENS = (6, 3, 10, 5, 2, 4, 3, 3, 4, 3, 4, 4, 5)
INFPLAIN_INDICES = (2, 8, 17, 16, 6, 7, 11, 12, 15, 9, 10, 13, 14)

INFFANCY_FORMAT = '''\
<tr><th colspan="2">Informant ID</th>
<td colspan="2">
<a href="%(basecgi)s/infprofile.py?project=%(project)s&informid=%(data2)s">
%(data2)s</a></td>
<th colspan="2">Informant Type</th><td colspan="2">%(data8)s</td></tr>
<tr><th>Community</th><td colspan="2">%(data17)s</td>
<th colspan="2">Community Type</th><td>%(data16)s</td>
<th>Worksheet</th><td>%(data6)s</td></tr>
<tr><th>Year</th><td>%(data7)s</td><th>Sex</th><td>%(data11)s</td>
<th>Age</th><td>%(data12)s</td><th>Race</th><td>%(data15)s</td></tr>
<tr><th>Generation</th><td>%(data9)s</td>
<th>Cultivation</th><td>%(data10)s</td> <th>Education</th><td>%(data13)s</td>
<th>Occupation</th><td>%(data14)s</td></tr>
<tr><td colspan="8">
<img src="%(baseold)s/img/pixel.gif" height="10" width="0"></td></tr>
'''

LINGFANCY_FORMAT = '''\
<tr><th>Record No.</th><td>%(data9)s</td>
<th>Informant ID</th><td>
<a href="%(basecgi)s/infprofile.py?project=%(project)s&informid=%(data1)s">
%(data1)s</a></td>
<th>Old ID</th><td>%(data2)s</td>
<th>Gram. Category</th><td>%(data3)s</td></tr>
<tr><th>Std. Orthography</th> <td colspan="7">%(data0)s</td></tr>
<tr><th>Pronunciation</th>
<td colspan="7"><font face="LAMCOUR, LAMSAS Courier, monospace">%(data7)s
</font></td></tr>
<tr><th>Doubt</th><td>%(data4)s</td> <th>Comment</th><td>%(data6)s</td>
<th>Comtext</th><td colspan="3">%(data5)s</td></tr>
<tr><td colspan="8">
<img src="%(baseold)s/img/pixel.gif" height="10" width="0"></td></tr>
'''

def infplain_writer(row, fmt=INFPLAIN_FORMAT, lens=INFPLAIN_LENS,
                    indices=INFPLAIN_INDICES, **ignore):
    data = [ str(row[i])[:length] for (i, length) in zip(indices, lens) ]
    print fmt % tuple(data)

def inffancy_writer(row, **var_dict):
    for i in range(len(row)):
        var_dict['data%d' % i] = row[i]
    print INFFANCY_FORMAT % var_dict

def lingplain_writer(row, fmt=LINGPLAIN_FORMAT, lens=LINGPLAIN_LENS,
                     indices=LINGPLAIN_INDICES, **ignore):
    data = [ str(row[i])[:length] for (i, length) in zip(indices, lens) ]
    print fmt % tuple(data)

def lingfancy_writer(row, **var_dict):
    for i in range(len(row)):
        var_dict['data%d' % i] = row[i]
    print LINGFANCY_FORMAT % var_dict

def main():
    cgitb.enable()
    fs = cgi.FieldStorage()
    project = fs.getfirst('project', '')
    plain = (fs.getfirst('infstyle', '') == 'plain' or
             fs.getfirst('lingstyle', '') == 'plain')
    (ling, short_file) = fs.getfirst('ling', ':').split(':')
    inf = fs.getfirst('infstyle', '')
    if inf:
        short_file = 'inf.asc'
    esc_file = quote_plus(short_file)
    data_file = os.path.join(DATADIR, project, short_file)
    note_file = os.path.join(DATADIR, 'headnotes',
                             'headnote_'+os.path.splitext(short_file)[0]+'.txt'
                             )
    if inf:
        title = '%s Informant Database' % project.upper()
    else:
        title = '%s Database for %r' % (project.upper(), ling)

    print 'Content-Type: text/html'
    print
    print '<html><head><title>', title, '</title></head></html>'
    print '<body>\n<h2>', title,
    if plain:
        print 'Plain Format</h2>'
    else:
        print 'Fancy Format</h2>'
    print '<p>Links:</p>'
    print '<ul><li><a href="%s/fields.html">Explanation of the fields' \
        '</a></li>' % BASEOLD
    if inf:
        print '<li><a href="%s/%s/infsearch.html">Search the informants' \
            '</a></li>' % (BASEOLD, project)
        print '<li><a href="%s/rawdata.py?project=%s&file=inf.asc">Examine ' \
            'the raw data file</a></li>' % (BASECGI, project)
    else:
        print '<li><a href="%s/%s/lingsearch.html">Search the databases' \
            '</a></li>' % (BASEOLD, project)
        print '<li><a href="%s/rawdata.py?project=%s&file=%s">Examine ' \
            'the raw data file</a></li>' % (BASECGI, project, esc_file)
        if os.path.exists(note_file):
            print '<li><a href="%s/headnotes.py?project=%s&file=%s">Examine ' \
                'notes about this file</a></li>' % (BASECGI, project, esc_file)
        q = {'project': project, 'sort': 'alpha',
             'table': '%s:%s' % (ling, short_file)}
        q = urlencode(q)
        print ('<li><a href="%s/maptable.py?%s">Generate a map from this '
               'database</a></li>') % (BASECGI, q)
    print '<li><a href="%s/%s/browse.html">Back to Browse</a></li>' % (
        BASEOLD, project)
    print '</ul>'

    if inf and plain:
        writer = infplain_writer
    elif inf and not plain:
        writer = inffancy_writer
    elif not inf and plain:
        writer = lingplain_writer
    else:
        writer = lingfancy_writer

    if inf and plain:
        print ('<pre>\n'
               "<a href=\"%(baseold)s/fields.html#informid\">Inf#</a>   "
               "<a href=\"%(baseold)s/fields.html#inftype\">Typ</a> " 
               "<a href=\"%(baseold)s/fields.html#comm\">Community</a>  " 
               "<a href=\"%(baseold)s/fields.html#comtype\">Local</a> " 
               "<a href=\"%(baseold)s/fields.html#ws\">WS</a> " 
               "<a href=\"%(baseold)s/fields.html#year\">Year</a> " 
               "<a href=\"%(baseold)s/fields.html#sex\">Sex</a> " 
               "<a href=\"%(baseold)s/fields.html#age\">Age</a> " 
               "<a href=\"%(baseold)s/fields.html#race\">Race</a> " 
               "<a href=\"%(baseold)s/fields.html#gen\">Gen</a> " 
               "<a href=\"%(baseold)s/fields.html#cult\">Cult</a> " 
               "<a href=\"%(baseold)s/fields.html#educ\">Educ</a> " 
               "<a href=\"%(baseold)s/fields.html#occup\">Occup</a> ") % {
               'baseold': BASEOLD }
    elif not plain:
        print '<table border="1"><tbody>'
    else:
        print ('<pre>'
               "<a href=\"%(baseold)s/fields.html#serial\">Serial</a> "
               "<a href=\"%(baseold)s/fields.html#informid\">Inf#</a>   " 
               "<a href=\"%(baseold)s/fields.html#oldnumbe\">Old#</a>   " 
               "<a href=\"%(baseold)s/fields.html#item\">Item</a>                           " 
               "<a href=\"%(baseold)s/fields.html#phnitem\">Phonetics</a>") % {
                'baseold': BASEOLD }

    kwargs = {
        'baseold': BASEOLD,
        'basecgi': BASECGI,
        'project': project,
        }

    for line in csv.reader(file(data_file, 'rb')):
        writer(line, baseold=BASEOLD, basecgi=BASECGI, project=project)

    if plain:
        print '</pre>'
    else:
        print '</tbody></table>'
    print '</body></html>'

