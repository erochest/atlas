
'''
This contains a class and some accessories to convert from one data
source to another. It is not very smart, but it is sufficient to
convert from CSV to MySQL.

It contains these things:
    Copier: the main object that handles the conversions;
    FieldConversions: a dictionary with mappings of field names to
        conversion functions;
    fromStrings: a function that converts a list of data (in strings)
        to an appropriate database format; and
    getConstant: a function that returns the constant value of a string
        code.

For usage on the class and the functions, see it, but using
FieldConversion is fairly simple:

>>> FieldConversions["auxiliary"]("Y")
1
>>> FieldConversions["infid"]("1162")
1162
'''


__all__ = [
    'Copier',
    'FieldConversions',
    'fromStrings',
    'getConstant',
    ]

from atlas import constants as _constants
from atlas.csv import CsvSource as _CsvSource
from atlas.utils import toInt as _toInt
from atlas.utils import bool as _bool
from atlas import tables as _tables
import os as _os


def getConstant(field, value, consts=_constants, default=(lambda x: x)):
    '''Returns constant value (usually an integer) of a string
    code. This is mainly used as a utility function in
    FieldConversion.
    >>> getConstant("auxiliary", "Y", default=_toInt)
    1
    '''
    if not hasattr(consts, field):
        return default(value)
    fieldconst = getattr(consts, field)
    if not hasattr(fieldconst, value):
        return default(value)
    return getattr(fieldconst, value)

FieldConversions = {
    # INFORMANTS
    'infid': _toInt, 'comid': _toInt, 'informid': str, 'oldnumber': str,
    'auxiliary': lambda x: getConstant('auxiliary', x, default=_bool),
    'fwid': _toInt, 'wsid': _toInt, 'yearint': _toInt,
    'inftype': lambda x: getConstant('inftype', x, default=_toInt),
    'generation': lambda x: getConstant('generation', x, default=_toInt),
    'cultivation': lambda x: getConstant('cultivation', x, default=_toInt),
    'sex': lambda x: getConstant('sex', x, default=_toInt),
    'age': _toInt,
    'education': lambda x: getConstant('education', x, default=_toInt),
    'occupation': lambda x: getConstant('occupation', x, default=_toInt),
    'race': lambda x: getConstant('race', x, default=_toInt),
    'latitude': float, 'longitude': float,
    # COMMUNITIES
    'comtype': lambda x: getConstant('comtype', x, default=_toInt),
    'comcode': str, 'comname': str, 'state': str, 'x': _toInt, 'y': _toInt,
    # FIELDWORKERS
    'fwcode': str, 'fwname': str,
    # WORKSHEETS
    'wscode': str, 'wsname': str,
    # TABLES
    'itemname': str, 'tablename': str,
    'tabletype': lambda x: getConstant('tabletype', x, default=_toInt),
    'page': _toInt, 'subpage': str, 'itemno': _toInt, 'subitemno': str,
    'notes': str,
    # ITEM
    'item': str, 'infid': _toInt,
    'gramflag': lambda x: getConstant('gramflag', x, default=_toInt),
    'doubtflag': lambda x: getConstant('doubtflag', x, default=_bool),
    'comments': str, 'comtext': str, 'phonetic': str, 'projectid': str,
    'itemid': _toInt,
    # PAGE
    'page': _toInt, 'subpage': str, 'itemno': _toInt, 'subitemno': str,
}

def fromStrings(fields, data):
    '''Given lists of field names and data in strings, returns the
    data with appropriate conversions.
    >>> fromStrings(("infid", "sex"), ("1162", "F"))
    (1162, 0)
    '''
    data = list(data)
    for i in range(len(data)):
        data[i] = FieldConversions.get(fields[i], lambda x: x)(data[i])
    return tuple(data)

class Copier:
    '''Handles the grunt work of converting from one data source to
    another. The only methods that you need to worry about are these:
        Copier(fromSrc, toSrc) and
        copier.run(latlongFile=None, xyFile=None, hwdir=None).
    '''

    def __init__(self, fromSrc, toSrc, verbose=0):
        '''Initializes the Copier object to transfer data from fromSrc
        to toSrc. Naturally, verbose determines whether to output
        status information.'''
        self.fromSrc = fromSrc
        self.toSrc = toSrc
        self.csvf = isinstance(fromSrc, _CsvSource)
        self.verbose = verbose

    def status(self, msg):
        '''If verbose messages are selected, prints msg to STDOUT.'''
        if self.verbose:
            print msg

    def close(self):
        '''Closes the data sources, committing changes to toSrc.'''
        try:
            self.toSrc.commit()
            self.toSrc.close()
        except:
            pass
        if hasattr(self.fromSrc, 'closed') and not self.fromSrc.closed:
            self.fromSrc.close()
    __del__ = close

    def base(self, latlongFile=None, xyFile=None):
        '''Transfers base. latlongFile is the data file containing the
        latitude and longitude information, and xyFile is the file
        containing the image x and y data, neither of which are
        included in the data returned from atlas.db.DbSource
        objects.'''

        fromSrc = self.fromSrc
        toSrc = self.toSrc
        transWrap = self._transWrap
        if (self.csvf and latlongFile and xyFile and
            _os.path.exists(latlongFile) and _os.path.exists(xyFile)):
            self.status('Grafting latitudes and longitudes onto informants...')
            fromSrc.loadLatLong(latlongFile)
            self.status('Grafting picture coordinates onto communities...')
            fromSrc.loadXY(xyFile)
        self.status('Setting up basic tables...')
        toSrc.createBaseTables()
        self.status('Transfering basic table data...')
        transWrap('getInformants', 'informants')
        transWrap('getCommunities', 'communities')
        transWrap('getFieldWorkers', 'field workers')
        transWrap('getWorkSheets', 'work sheets')

    def _transWrap(self, methname, desc):
        '''Wraps transfering the datasets returned by methname from
        each data source. desc is a description printed using status.
        '''
        self.status('Transfering %s...' % desc)
        self.transSet(getattr(self.fromSrc, methname)(),
                      getattr(self.toSrc, methname)())

    def transSet(self, fromSet, toSet):
        '''Transfers the data in fromSet to toSet, converting
        appropriately if the source is a CSV source.'''
        if self.csvf:
            fs = fromStrings
            data = [ fs(row.fields, row.data) for row in fromSet ]
        else:
            data = fromSet.data[:]
        toSet.extend(data, fromSet.fields)
        toSet.source.commit()

    def transItem(self, itemargs, count=0, total=0):
        '''Transfers the item from fromSrc to toSrc. itemargs is a
        sequence of the arguments to be passed to
        atlas.data.DataSource.createDataTable. hwdir is the directory
        containing the headword notes files. count and total are for
        correctly keeping track of how many out of how many have been
        done for status reports.'''

        self.status('Transfering item "%s" (%03d/%03d)...' %
                    ( itemargs[0], count, total ))
        fromSrc = self.fromSrc
        fromItem = fromSrc.getItem(itemargs[0])
        if len(fromItem) == 0:
            self.status('Empty data set, skipping...')
            return
        toSrc = self.toSrc
        toSrc.createDataTable(*itemargs)
        toSrc.commit()
        self.transSet(fromItem, toSrc.getItem(itemargs[0]))
        if self.csvf:
            del fromSrc._cache[itemargs[1]]

    def _coerced(self, dict,
                 fields=[f[0] for f in _tables.TableFields.TABLES],
                 convd=FieldConversions):
        '''Returns the data in dict (a dictionary containing data from
        a row from TABLES) converted appropriately.'''
        data = []
        for field in fields:
            data.append(convd.get(field, lambda x: x)(dict[field]))
        return tuple(data)

    def transfer(self, hwdir=None):
        '''Transfers all the data items in fromSrc to toSrc, with
        hwdir being the directory containing the headword notes
        files.'''
        fromSrc = self.fromSrc
        coerced = self._coerced
        if hwdir:
            fromSrc.loadHeadNotes(hwdir)
        tables = fromSrc.getTables()
        ttotal = len(tables)
        tcount = 1
        for table in tables:
            self.transItem(coerced(table.dict()), tcount, ttotal)
            tcount += 1

    def run(self, latlongFile=None, xyFile=None, hwdir=None):
        '''My main method. Attempts the entire conversion from fromSrc
        to toSrc. latlongFile and xyFile are passed to Copier.base,
        and hwdir is passed to Copier.transfer.'''
        try:
            self.base(latlongFile, xyFile)
            self.status('Attempting transfers...')
            self.transfer(hwdir)

        finally:
            self.close()

