#! /usr/bin/env python

from lap import settings
import cgi, cgitb, csv, os, sys

DATADIR = settings.locale.old_data
BASEOLD = settings.locale.baseold
BASECGI = settings.locale.basecgi

COMMA = ', '
PLAIN_ROW = '%-6s %-3s %-10s %-5s %-2s %-4s %-3s %-3s %-4s %-3s %-4s %-4s %-5s'
PLAIN_INDICES = (2, 8, 17, 16, 6, 7, 11, 12, 15, 9, 10, 13, 14)
PLAIN_LENS = (6, 3, 10, 5, 2, 4, 3, 3, 4, 3, 4, 4, 5)

STATES = {'all': 'All States',
	      'ny' : 'New York',
	      'nj' : 'New Jersey',
	      'pa' : 'Pennsylvania',
	      'wv' : 'West Virginia',
	      'de' : 'Delaware',
	      'md' : 'Maryland',
	      'dc' : 'Washington, DC',
	      'va' : 'Virginia',
	      'nc' : 'North Carolina',
	      'sc' : 'South Carolina',
	      'ga' : 'Georgia',
	      'fl' : 'Florida'}

def get_state(state):
    return STATES[state]

PARAMS = (('state', 'all', get_state), ('ws', 'all', 'Worksheet = %s'),
          ('year', 'all', 'Year = %s'), ('inftype', 'all', 'Type = %s'),
          ('gen', 'all', 'Generation = %s'),
          ('cult', 'all', 'Cultivation = %s'), ('sex', 'all', 'Sex = %s'),
          ('lowerage', 0, 'Age from %s Years'),
          ('higherage', 120, 'Age to %s years'),
          ('educ', 'all', 'Education = %s'),
          ('occup', 'all', 'Occupation = %s'),
          ('race', 'all', 'Race = %s'),
          ('commtype', 'all', 'Locality Type = %s'), ('project', None, None), 
          ('display', 'plain', None), )

def get_params(fs):
    params = {}
    for (param, default, desc) in PARAMS:
        params[param] = fs.getfirst(param, default)
    return params

def get_description(params):
    buffer = []
    append = buffer.append
    for (param, default, desc) in PARAMS:
        if desc is None:
            continue
        value = params[param]
        if value != str(default):
            if callable(desc):
                append(desc(value))
            else:
                append(desc % value)
    return ',<br> Where ' + COMMA.join(buffer)

def plain_header():
    sys.stdout.write(
        '<pre>\n'
        "<a href=\"%s/fields.html#informid\">Inf#</a>   "
        "<a href=\"%s/fields.html#inftype\">Typ</a> "
        "<a href=\"%s/fields.html#comm\">Community</a>  "
        "<a href=\"%s/fields.html#comtype\">Local</a> "
        "<a href=\"%s/fields.html#ws\">WS</a> "
        "<a href=\"%s/fields.html#year\">Year</a> "
        "<a href=\"%s/fields.html#sex\">Sex</a> "
        "<a href=\"%s/fields.html#age\">Age</a> "
        "<a href=\"%s/fields.html#race\">Race</a> "
        "<a href=\"%s/fields.html#gen\">Gen</a> "
        "<a href=\"%s/fields.html#cult\">Cult</a> "
        "<a href=\"%s/fields.html#educ\">Educ</a> "
        "<a href=\"%s/fields.html#occup\">Occup</a> \n" %
        ((BASEOLD,) * 13)
        )

def fancy_header():
    pass

def plain_row(row):
    data = [
        str(row[i])[:length] for (i, length) in zip(PLAIN_INDICES, PLAIN_LENS)
        ]
    data = tuple(data)
    print PLAIN_ROW % data

def fancy_row(project, row):
    print '<table border="1"><tbody>'
    print '<tr><th colspan="2">Informant ID</th><td colspan="2">'
    print '<a href="infprofile.py?project=%s&informid=%s">' % (project, row[2])
    print row[2], '</a></td>'
    print '<th colspan="2">Informant Type</th><td colspan="2">', row[8], \
        '</td></tr>'
    print '<tr><th>Community</th><td colspan="2">', row[17], '</td>'
    print '<th colspan="2">Community Type</th><td>', row[16], '</td>'
    print '<th>Worksheet</th><td>', row[6], '</td></tr>'
    print '<tr><th>Year</th><td>', row[7], '</td>'
    print '<th>Sex</th><td>', row[11], '</td>'
    print '<th>Age</th><td>', row[12], '</td>'
    print '<th>Race</th><td>', row[15], '</td></tr>'
    print '<tr><th>Generation</th><td>', row[9], '</td>'
    print '<th>Cultivation</th><td>', row[10], '</td>'
    print '<th>Education</th><td>', row[13], '</td>'
    print '<th>Occupation</th><td>', row[14], '</td></tr>\n</tbody>\n</table>'

def plain_end():
    print '</pre>'

def fancy_end():
    pass

_int = int
def int(value):
    try:
        return _int(value)
    except:
        return value

def main():
    cgitb.enable()
    fs = cgi.FieldStorage()
    params = get_params(fs)
    project = params['project']
    infile = os.path.join(DATADIR, project, 'inf.asc')
    display = fs.getfirst('display', 'plain')
    desc = get_description(params);

    print 'Content-Type: text/html'
    print
    print '<html>\n<head>\n<title>', project.upper(),
    print 'Informant Information', desc, '</title>\n</head>\n'
    print '<body>'
    print '<h2>', project.upper(), 'Informant Database Search', desc, ',<br>',
    print display.title(), 'Format</h2>'

    print '<p>Links:</p>'
    print '<ul>'
    print '<li><a href="%s/fields.html">Explanation of the fields</a></li>' % \
        BASEOLD
    print '<li><a href="%s/browse.py?project=%s&infstyle=%s">List all ' \
        'informants</a></li>' % (BASECGI, project, display)
    print '<li><a href="%s/%s/search.html">Back to search</a></li>' % \
        (BASEOLD, project)
    print '</ul>'

    if display == 'plain':
        plain_header()
    else:
        fancy_header()

    for data in csv.reader(file(infile, 'rb')):
        if not data:
            continue
        if ((params['state'] == 'all' or data[-1].lower() == params['state']) and
            (params['ws'] == 'all' or data[6].lower() == params['ws']) and
            (params['year'] == 'all' or data[7] == params['year']) and
            (params['inftype'] == 'all' or data[8].lower() == params['inftype']) and
            (params['gen'] == 'all' or data[9].lower() == params['gen']) and
            (params['cult'] == 'all' or data[10].lower() == params['cult']) and
            (params['sex'] == 'all' or data[11].lower() == params['sex']) and
            (int(data[12]) >= int(params['lowerage']) and int(data[12]) <= int(params['higherage'])) and
            (params['educ'] == 'all' or data[13].lower() == params['educ']) and
            (params['occup'] == 'all' or data[14].lower() == params['occup']) and
            (params['race'] == 'all' or data[15].lower() == params['race']) and
            (params['commtype'] == 'all' or data[16].lower() == params['commtype'])):
            if display == 'plain':
                plain_row(data)
            else:
                fancy_row(project, data)

    if display == 'plain':
        plain_end()
    else:
        fancy_end()

    print '</body>\n</html>'

