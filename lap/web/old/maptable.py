#! /usr/bin/env python

from lap import settings
from urllib import urlencode
import cgi, cgitb, csv, glob, os, sys

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

def main():
    cgitb.enable()
    fs = cgi.FieldStorage()
    project = fs.getfirst('project')
    alpha_sort = fs.getfirst('sort') == 'alpha'
    singles = fs.getfirst('singles')
    (table, short_file) = fs.getfirst('table', ':').split(':')
    filename = os.path.join(DATADIR, project, short_file)

    formats = {
        'project_upper': project.upper(),
        'project': project,
        'table': table,
        'short_file': short_file,
        'baseold': BASEOLD,
        'basecgi': BASECGI,
        }

    print '''\
Content-Type: text/html

<html>
<head>
<title>%(project_upper)s< Linguistic Map Creation -- %(table)s</title>
</head>
<body bgcolor="#FFFFFF" text="#000000" link="#5672AC" vlink="#82CACC"
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
              <a href="%(baseold)s/index.html"><img src="%(baseold)s/img/homemenuoff.gif"
		alt="Home Page" height="30" width="125"
		border="0"></a><br>
              <a href="%(baseold)s/%(project)s/index.html"><img src="%(baseold)s/%(project)s/img/%(project)smenuoff.gif" alt="%(project_upper)s" height="30" width="125" border="0"></a><br>
              <a href="%(baseold)s/%(project)s/information.html"><img src="%(baseold)s/img/infomenuoff.gif" alt="Information" height="30" width="125" border="0"></a><br>
              <a href="%(baseold)s/%(project)s/browse.html"><img src="%(baseold)s/img/browsemenuoff.gif" alt="Browse" height="30" width="125" border="0"></a><br>
              <a href="%(baseold)s/%(project)s/search.html"><img src="%(baseold)s/img/searchmenuoff.gif" alt="Search" height="30" width="125" border="0"></a><br>
              <img src="%(baseold)s/img/mapsmenuoff.gif" alt="Maps" height="30" width="125" border="0">
</td>
	  <td width="18"></td>
	  <td width="372">

<img src="%(baseold)s/%(project)s/img/maps.gif" height="33" width="67" border="0">

<p><b>Instructions:</b><br>You can generate the map for either a
specific response or for all the responses that include a search
string. For the first, merely select the desired response from the
drop-down menu; for the second, enter the search string in the entry
box.</p>

<form action="%(basecgi)s/map.py" method="get">
''' % formats

    itemcounts = {}
    for data in csv.reader(file(filename, 'rb')):
        itemcounts[data[0]] = itemcounts.get(data[0], 0) + 1
    try: del itemcounts['NR']
    except KeyError: pass
    try: del itemcounts['NA']
    except KeyError: pass
    try: del itemcounts['-0-']
    except KeyError: pass

    if alpha_sort:
        items = itemcounts.keys()
        items.sort()
    else:
        items = [ (value, key) for (key, value) in itemcounts.items() ]
        items.sort()
        items = [ key for (value, key) in items ]

    print '<p><b>Items in', repr(table), '</b></p>'
    print '<blockquote><select name="item">'
    for item in items:
        if singles or itemcounts[item] > 1:
            print '<option value="%s">%s (%d)</option>' % (
                item, item, itemcounts[item])
    print '</select></blockquote>'

    print '''\
<p><b>Please enter the search string:</b></p>
<blockquote><input name="search" type="text"></blockquote>

<input type="hidden" name="project" value="%(project)s">
<input type="hidden" name="file" value="%(short_file)s">
<input type="hidden" name="table" value="%(table)s">

<p align="right"><input type="submit">&nbsp;<input type="reset"></p>
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
''' % formats

