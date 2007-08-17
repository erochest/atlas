#! /usr/bin/env python

from lap import settings
import cgi, cgitb, csv, os

DATADIR = settings.locale.old_data
BASEOLD = settings.locale.baseold
BASECGI = settings.locale.basecgi

class empty:
    def get(self, value, default=None):
        return default
EMPTY = empty()
DATA_TEXT = (
    # serial, commno, informid, oldnumbe, aux,
    EMPTY, EMPTY, EMPTY, EMPTY, EMPTY,
    # fw
	{'L': 'Guy Lowman', 'M': 'Raven McDavid', 'P': 'Lee Pederson',
	 'S': 'Student', 'Rr': 'Grace Reuter', 'U': 'Gerald Udell',
	 'Rt': 'Barbara Rutledge', 'O': 'Raymond O\'Cain',
     'B': 'Bernard Bloch', 'T': 'Lorenzo Turner' },
    # ws
	{'S': 'South Atlantic', 'M': 'Middle Atlantic',
	 'P': 'Preliminary South Atlantic', 'C': 'Combined',
	 'E': 'New England' },
    # year
    EMPTY,
    # inftype
    {'I': 'Folk', 'II': 'Common', 'III': 'Cultivated' },
    #  gen
	{ 'A': 'Aged', 'B': 'Modern' },
    # cult
    EMPTY,
    # sex
	{ 'M': 'Male', 'F': 'Female' },
    # age
    EMPTY,
    # educ
	{ '0': 'None/Illiterate', '1': 'Some grade school: 1-4 years',
	  '2': 'Grade school: 5-8 years', '3': 'Some high school: 9-11 years',
	  '4': 'High school: 12 years', '5': 'Some college (also trade schools)',
	  '6': 'College graduate' },
    # occup
	{ 'P': 'Professional and Technical', 'F': 'Farmers',
	  'M': 'Managers, Officials, Proprietors', 'R': 'Clerical and Sales',
	  'C': 'Craftsmen and Foremen', 'O': 'Operatives',
	  'H': 'Private Household Workers', 'S': 'Service Workers',
	  'W': 'Farm Laborers', 'K': 'Keeping House', 'L': 'Non-Farm Laborers',
	  'U': 'Seeking Work', 'G': 'Student' },
    # race
    { 'B': 'African-American', 'W': 'White' },
    # comtype
	{ 'U': 'Urban', 'R': 'Rural' },
    # ???, ???
    EMPTY, EMPTY,
    )

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

def get_informants(filename):
    return list(csv.reader(file(filename, 'rb')))

def main():
    cgitb.enable()
    fs = cgi.FieldStorage()
    project = fs.getfirst('project', '')
    informid = fs.getfirst('informid', '')
    properties = read_properties(os.path.join(DATADIR, project+'.properties'))
    infs = get_informants(
        os.path.join(DATADIR, project, properties['informant.table'])
        )
    infdata = [ i for i in infs if i[2] == informid ][0]

    var_dict = {
        'project': project, 'project_upper': project.upper(),
        'informid': informid, 'baseold': BASEOLD, 'basecgi': BASECGI,
        'options': file(os.path.join(DATADIR, project, 'options')).read(),
        }
    for i in range(len(infdata)):
        value = infdata[i]
        var_dict['data%d_raw' % i] = value
        var_dict['data%d' % i] = DATA_TEXT[i].get(value, value)

    print 'Content-Type: text/html'
    print
    print '''<html>
<head>
<title>%(project_upper)s Linguistic Informant Profile -- %(informid)s</title>
</head>
<body bgcolor="#FFFFFF" text="#000000" link="#5672AC" link="#82CACC"
      alink="#0E5EFF">
<img src="%(baseold)s/%(project)s/img/logo.gif" border="0">
<table><tbody>
<tr>
<td><img src="%(baseold)s/img/pixel.gif" height="1" width="132"></td>
<td><img src="%(baseold)s/img/pixel.gif" height="1" width="18"></td>
<td><img src="%(baseold)s/img/pixel.gif" height="1" width="372"></td>
</tr>
<tr>
<td width="132" valign="top">
<a href="%(baseold)s/index.html">
<img src="%(baseold)s/img/homemenuoff.gif" alt="Home Page" height="30"
     width="125" border="0"></a><br>
<a href="%(baseold)s/%(project)s/index.html>
<img src="%(baseold)s/%(project)s/img/%(project)smenuoff.gif"
     alt="%(project_upper)s" height="30" width="125" border="0"></a><br>
<a href="%(baseold)s/%(project)s/information.html">
<img src="%(baseold)s/img/infomenuoff.gif" alt="Information" height="30"
     width="125" border="0"></a><br>
<a href="%(baseold)s/%(project)s/browse.html">
<img src="%(baseold)s/img/browsemenuoff.gif" alt="Browse" height="30"
     width="125" border="0"></a><br>
<a href="%(baseold)s/%(project)s/search.html">
<img src="%(baseold)s/img/searchmenuoff.gif" alt="Search" height="30"
     width="125" border="0"></a><br>
<img src="%(baseold)s/img/mapsmenuoff.gif" alt="Maps" height="30" width="125"
     border="0">
</td>
<td width="18"></td>
<td width="372">

<img src="%(baseold)s/img/browse.gif" height="28" width="87" border="0">

<p><b>Informant data for record %(data0)s</b>:<br>
%(data12)s-year-old %(data15)s %(data11)s, type %(data8)s</p>

<table border="0"><tbody>
<tr><th align="right">Serial Number: </th><td>%(data0)s</td></tr>
<tr><th align="right">Community Number: </th><td>%(data1)s (%(data17)s, %(data18)s)</td></tr>
<tr><th align="right">Informant ID Number: </th><td>%(data2)s</td></tr>
<tr><th align="right">Old Informant Number: </th><td>%(data3)s</td></tr>
<tr><th align="right">Auxiliary Informants: </th><td>%(data4)s</td></tr>
<tr><th align="right">Field Worker: </th><td>%(data5)s</td></tr>
<tr><th align="right">Work Sheet: </th><td>%(data6)s</td></tr>
<tr><th align="right">Year Interviewed: </th><td>%(data7)s</td></tr>
<tr><th align="right">Type: </th><td>%(data8_raw)s (%(data8)s)</td></tr>
<tr><th align="right">Generation: </th><td>%(data9_raw)s (%(data9)s)</td></tr>
<tr><th align="right">Cultivation: </th><td>%(data10)s</td></tr>
<tr><th align="right">Sex: </th><td>%(data11)s</td></tr>
<tr><th align="right">Age (when interviewed): </th><td>%(data12)s</td></tr>
<tr><th align="right">Education: </th><td>%(data13)s</td></tr>
<tr><th align="right">Occupation: </th><td>%(data14)s</td></tr>
<tr><th align="right">Race: </th><td>%(data15)s</td></tr>
<tr><th align="right">Locality Type: </th><td>%(data16)s</td></tr>
</tbody></table>

<hr>

<p>Select the databases to see the informant's responses.</p>

<form action="%(basecgi)s/infresp.py" method="get">
<input type="hidden" name="project" value="%(project)s">
<input type="hidden" name="informid" value="%(informid)s">

<select size="10" multiple="multiple" name="tables">
<option value="c*">All files</option>
<option value="cp*">Phonetic files</option>
<option value="cg*">Grammatical files</options>
<option value="cl*">Lexical files</options>
%(options)s
</select>

<p align="right"><input type="submit"> <input type="reset"></p>

</form>
</td>
	</tr>
      </tbody>
    </table>

<table>
      <tbody>
	<tr>
	  <td><img src="%(baseold)s/img/pixel.gif" height="1" width="179"></td>
	  <td><img src="%(baseold)s/img/pixel.gif" height="1" width="178"></td>
	  <td><img src="%(baseold)s/img/pixel.gif" height="1" width="178"></td>
	</tr>
	<tr>
	  <td class="footer" align="left"><font size="-1">July 28, 1998</font></td>
	  <td class="footer" align="center"><font size="-1">Copyright &copy; 1998</font></td>
	  <td class="footer" align="right"><font size="-1"><a href="mailto:webmaster\@us.english.uga.edu">webmaster\@us.english.uga.edu</a></font></td>
	</tr>
      </tbody>
    </table>

</body>
</html>
''' % var_dict

if __name__ == '__main__':
    main()

