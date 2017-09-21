
'''This provides some classes to check the consistency of data kept in
CSV format. This is provided since the data source does not provide type
checking and some of the other useful checks that data bases do.

This is easy to integrate into a script or or an interactive session by
doing this:

    import atlas.data.CsvTest
    datadir = './LAMSAS'
    atlas.data.CsvTest.test(datadir)

At which point it prints out a bunch of information about possible
problems.
'''

__all__ = [
    'CsvTest',
    'test'
    ]

from atlas import csv
from atlas.tables import TableNames
from atlas.utils import Set
import os
from types import StringType
import sys

_datadir = './LAMSAS'

_nullSet = Set('-0-', 'NA', 'na')
_boolSet = Set('Y', 'y', 'N', 'n')

_fwSet = Set('L', 'M', 'P', 'S', 'Rr', 'U', 'Rt', 'O', 'B')
_wsSet = Set('S', 'M', 'P', 'C', 'E')
_inftypeSet = Set('I', 'II', 'III')
_genSet = Set('A', 'B')
_sexSet = Set('F', 'M')
_occupSet = Set('P', 'F', 'M', 'R', 'C', 'O', 'H', 'S', 'W', 'K', 'L',
                'U', 'G')
_raceSet = Set('B', 'W')
_comtypeSet = Set('R', 'U')
_gramSet = Set('N', 'V', 'M', 'C', 'A', 'B', 'J', 'P', 'X', 'D', 'R', 'T',
               'S', 'E', 'Q', 'O', 'K')
_tableSet = Set('g', 'l', 'p')

def convert(func, value):
    try:
        return func(value)
    except:
        return None

def isNull(value):
    return not value or value in _nullSet
def isInt(value):
    return isNull(value) or convert(int, value) != None
def isString(value):
    return isinstance(value, StringType)
def inSet(value, set):
    return isNull(value) or value in set

_infCheck = [
    (isInt, 'Serial is not an integer: '),
    (isInt, 'Community number is not an integer: '),
    (isString, 'Informant ID is not a string: '),
    (isString, 'Old informant ID is not a string: '),
    (lambda v: inSet(v, _boolSet), 'Auxiliary is not a boolean: '),
    (lambda v: inSet(v, _fwSet), 'Field worker is invalid: '),
    (lambda v: inSet(v, _wsSet), 'Work sheet is invalid: '),
    (isInt, 'Year is not an integer: '),
    (lambda v: inSet(v, _inftypeSet), 'Informant type is invalid: '),
    (lambda v: inSet(v, _genSet), 'Generation is invalid: '),
    (lambda v: inSet(v, _boolSet), 'Cultivation is invalid: '),
    (lambda v: inSet(v, _sexSet), 'Sex is invalid: '),
    (isInt, 'Age is not an integer: '),
    (isInt, 'Education is not an integer: '),
    (lambda v: inSet(v, _occupSet), 'Occupation is invalid: '),
    (lambda v: inSet(v, _raceSet), 'Race is invalid: '),
    (lambda v: inSet(v, _comtypeSet), 'Community type is invalid: '),
    (isString, 'Community name is not a string: '),
    (isString, 'State is not a string: '),
    ]

_tablesCheck = [
    (isString, 'Item name is not a string: '),
    (isString, 'Table name is not a string: '),
    (lambda v: inSet(v, _tableSet), 'Table type is invalid: '),
    (isInt, 'Page is not an integer: '),
    (isString, 'Subpage is not a string: '),
    (isInt, 'Item number is not an integer: '),
    (isString, 'Subitem number is not a string: '),
    (isString, 'Notes is not a string: '),
    ]

_itemCheck = [
    (isString, 'Item is not a string: '),
    (isString, 'Informant ID is not a string: '),
    (isString, 'Old informant ID is not a string: '),
    (lambda v: inSet(v, _gramSet), 'Grammar flag is invalid: '),
    (lambda v: inSet(v, _boolSet), 'Doubt flag is invalid: '),
    (isString, 'Comments is not a string: '),
    (isString, 'Comment text is not a string: '),
    (isString, 'Phonetic data is not a string: '),
    (isString, 'Project code is not a string: '),
    (isInt, 'Serial is not an integer: '),
    ]

_pageCheck = _itemCheck + [
    (isString, 'Page number is not a string: '),
    (isString, 'Line number is not a string: '),
    ]

class CsvTest:
    def __init__(self, datadir, out=sys.stderr):
        self.source = csv.CsvSource(datadir, 'null')
        self.datadir = datadir
        self.out = out
        self.softspace = 0

    def _assert(self, test, value, filename, lineno, msg):
        if not test:
            self.write('ERROR (%s:%04d): %s (%s)\n' %
                       (filename, lineno, msg, value))

    def write(self, msg):
        self.out.write(msg)
    def writelines(self, msg):
        self.out.writelines(msg)
    def flush(self):
        self.out.flush()
    def close(self):
        self.out.close()

    def checkFile(self, ds, linelen, checks):
        lineno = 1
        filename = os.path.basename(ds.filename)
        for line in ds:
            csv = line.csv()
            self._assert(len(line) == linelen,
                         line,
                         filename,
                         lineno,
                         'Incorrect line length: '+csv)
            for (value, (func, msg)) in zip(line, checks):
                self._assert(func(value.strip()),
                             value,
                             filename,
                             lineno,
                             msg+csv)
            lineno += 1

    def run(self):
        self.checkInformants()
        self.checkTables()
        self.checkPages()
        self.checkItems()

    def checkInformants(self):
        source = self.source
        filename = os.path.join(self.datadir, TableNames.INFORMANTS)
        if not os.path.isfile(filename):
            self.write('Informants file (%s) is not a file!  Skipping.\n' %
                       filename)
            return
        self.write('Checking informants...\n')
        self.checkFile(source.loadFile(filename), 19, _infCheck)

    def checkTables(self):
        source = self.source
        filename = os.path.join(self.datadir, TableNames.TABLES)
        if not os.path.isfile(filename):
            self.write('Tables file (%s) is not a file!  Skipping.\n' %
                       filename)
            return
        self.write('Checking tables...\n')
        self.checkFile(source.loadFile(filename), 8, _tablesCheck)

    def checkPages(self):
        source = self.source
        files = [ os.path.join(self.datadir, fn)
                  for fn in os.listdir(self.datadir)
                  if fn.lower().startswith('_page') ]
        for file in files:
            if not os.path.isfile(file):
                self.write('Page file (%s) is not a file!  Skipping.\n' %
                           file)
                continue
            self.write('Checking %s...\n' % file)
            self.checkFile(source.loadFile(file), 12, _pageCheck)

    def checkItems(self):
        source = self.source
        files = [ os.path.join(self.datadir, fn)
                  for fn in os.listdir(self.datadir)
                  if not fn.startswith('_') ]
        for file in files:
            if not os.path.isfile(file):
                self.write('Data file (%s) is not a file!  Skipping.\n' %
                           file)
                continue
            self.write('Checking %s...\n' % file)
            self.checkFile(source.loadFile(file), 10, _itemCheck)

def test(datadir, out=sys.stderr):
    t = CsvTest(datadir, out)
    t.run()
    t.write('Done!\n')

if __name__ == '__main__':
    import sys
    test(*sys.argv[1:])

