#! /usr/bin/env python

from lap import settings
from urllib import quote_plus, urlencode
import cgi, cgitb, csv, gd, glob, os, re, sys

DATADIR = settings.locale.old_data
BASEOLD = settings.locale.baseold
BASECGI = settings.locale.basecgi

class CounterSet:
    def __init__(self):
        self.occur = 0
        self.set = {}

    def __lshift__(self, data): self.set[data] = True
    def __iter__(self): return iter(self.set)
    def __contains__(self, data): return data in self.set
    def __len__(self): return len(self.set)
    def __delitem__(self, item): del self.set[item]

    def __isub__(self, other):
        for item in other:
            if item in self:
                del self[item]
        return self

    def __sub__(self, other):
        result = CounterSet()
        result.occur = self.occur
        for item in self:
            if item not in other:
                result << item
        return result

    def __iadd__(self, other):
        for item in other:
            self << item
        return self

    def __add__(self, other):
        result = CounterSet()
        result.occur = self.occur + other.occur
        for item in self:
            result << item
        for item in other:
            result << item
        return result

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

def community(infid):
    match = re.match(r'[a-zA-Z]+\d+(?:G(?=[A-Z]))?', infid)
    if match:
        return match.group(0)
    else:
        return infid

def make_map(filename, exclusive, props, image_filename, item):
    hit = CounterSet()
    miss = CounterSet()
    nr = CounterSet()

    item_lower = item.lower()
    for row in csv.reader(file(filename, 'rb')):
        item = row[0].lower()
        comm = community(row[1])

        if ((exclusive and item_lower == item) or
            (not exclusive and item.find(item_lower) != -1)):
            hit.occur += 1
            hit << comm

        elif item in ('-0-', 'nr', 'na'):
            nr.occur += 1
            nr << comm

        else:
            miss.occur += 1
            miss << comm

    coords_file = props['map.coords']
    coords = {}
    for line in file(coords_file):
        (infid, xy) = line.strip().split(':')
        coords[infid] = tuple(map(int, xy.split(',')))

    img = gd.image(props['map.image'])

    black = img.colorAllocate((0, 0, 0))
    red = img.colorAllocate((255, 0, 0))

    for h in hit:
        (x, y) = coords[h]
        img.filledRectangle((x-3, y-3), (x+4, y+4), red)
        img.rectangle((x-3, y-3), (x+4, y+4), black)

    for m in (miss-hit):
        (x, y) = coords[m]
        img.rectangle((x-3, y-3), (x+3, y+3), black)

    for n in (nr-(hit+miss)):
        (x, y) = coords[n]
        img.line((x-3, y-3), (x+4, y+4), black)
        img.line((x-3, y+4), (x+4, y-3), black)

    (line_width, line_height) = gd.fontstrsize(gd.gdFontLarge, 'M')
    x = int(props['map.text.x'])
    y = int(props['map.text.y'])

    img.filledRectangle((x, y+4), (x+7, y+11), red)
    img.rectangle((x, y+4), (x+7, y+11), black)
    img.string(gd.gdFontLarge, (x+17, y), item, black)
    y += line_height
    img.string(gd.gdFontLarge, (x+27, y), 'Occurrences (%d)' % hit.occur,
               black)
    y += line_height
    img.string(gd.gdFontLarge, (x+27, y), 'Communities (%d)' % len(hit),
               black)

    y += line_height
    img.rectangle((x, y+4), (x+7, y+11), black)
    img.string(gd.gdFontLarge, (x+17, y), 'Other Reseponses', black)
    y += line_height
    img.string(gd.gdFontLarge, (x+27, y), 'Occurrences (%d)' % miss.occur,
               black)
    y += line_height
    img.string(gd.gdFontLarge, (x+27, y), 'Communities (%d)' % len(miss),
               black)

    y += line_height
    img.line((x, y+4), (x+7, y+11), black)
    img.line((x, y+11), (x+7, y+4), black)
    img.string(gd.gdFontLarge, (x+17, y), 'No Response', black)
    y += line_height
    img.string(gd.gdFontLarge, (x+27, y), 'Occurrences (%d)' % nr.occur,
               black)
    y += line_height
    img.string(gd.gdFontLarge, (x+27, y), 'Communities (%d)' % len(nr),
               black)

    img.writePng(image_filename)

    return True

def make_page(project, item, table_name, image_url, short_file, note_file):
    print 'Content-Type: text/html'
    print
    print '<html>\n<head>'
    print '<title>', project.upper(), 'mapping for', repr(item), 'in', \
        repr(table_name), '</title>\n</head>\n<body>'
    print '<p align="center"><img src="%s"></p>' % image_url

    print '<p>Links:</p>'
    q = {
        'project': project, 'for': item, 'in': 'c*',
        'ling': '%s:%s' % (table_name, short_file), 'lingstyle': 'plain',
        'file': short_file,
        }
    q = urlencode(q)
    print '<ul><li><a href="%s/lingsearch.py?%s">Search for %r in all files' \
        '</a></li>' % (BASECGI, q, item)
    print '<li><a href="%s/browse.py?%s">Browse the %r database' \
        '</a></li>' % (BASECGI, q, table_name)
    print '<li><a href="%s/rawdata.py?%s">Browse the raw data for the %r ' \
        'database</a></li>' % (BASECGI, q, table_name)
    if os.path.exists(note_file):
        print '<li><a href="%s/headnotes.py?%s">View notes for the %r ' \
            'database</a></li>' % (BASECGI, q, table_name)
    print '<li><a href="%s/%s/maps.html">Back to Mapping</a></li></ul>' % (
        BASEOLD, project)
    print '</body></html>'

def error_page(project):
    print 'Content-Type: text/html'
    print
    print '<html><head><title>Mapping Error</title></head>'
    print '<body><p><b><a href="%s/%s/maps.html">Back to Mapping</a>' \
        '</b></p></body></html>' % (BASEOLD, project)

def main():
    cgitb.enable()
    fs = cgi.FieldStorage()
    project = fs.getfirst('project')
    short_file = fs.getfirst('file')
    esc_file = quote_plus(short_file)
    filename = os.path.join(DATADIR, project, short_file)
    note_file = os.path.join(
        DATADIR, project, 'headnotes',
        'headnote_%s.txt' % os.path.splitext(short_file)[1])
    table_name = fs.getfirst('table')
    dot_table = table_name.replace(' ', '-')
    item = fs.getfirst('search') or fs.getfirst('item')
    exclusive = not fs.getfirst('search')
    item_filename = re.sub(r'\W', '-', item)

    props = read_properties(os.path.join(DATADIR, project+'.properties'))
    map_cache = props['map.cache']

    if exclusive:
        suffix = 'ex.png'
    else:
        suffix = 'in.png'
    image_filename = '%s%s.%s.%s' % (map_cache, dot_table, item_filename,
                                     suffix)
    base_url = '.'.join((dot_table, item_filename, suffix))
    image_url = '/'.join((BASEOLD, project, 'img', 'cache', base_url))

    if item and (os.path.exists(image_filename) or
                 make_map(filename, exclusive, props, image_filename, item)):
        make_page(project, item, table_name, image_url, short_file, note_file)
    else:
        error_page(project)

