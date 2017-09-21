

'''Contains classes that extend those in atlas.data to handle data
kept in comma-separated-value-formatted data files. They expect a
certain directory structure [FIXME: describe].

There are three main classes: CsvSource, CsvSet, and CsvRow.
'''


__all__ = [
    'CsvRow',
    'CsvSet',
    'CsvSource',
    ]

from atlas import tables as _tables
from atlas.data import DataRow as _DataRow
from atlas.data import DataSet as _DataSet
from atlas.phonetics import simplify as _simplify
import fcsv as _fcsv
import os as _os
import re as _re
from types import IntType as _IntType
from types import StringType as _StringType


_reCom = _re.compile(
    r'''
    (?P<community>
      [a-zA-Z]+\d+
      (?:
        G
        (?=[A-Z])
      )?
    )
    ''', _re.VERBOSE)


class CsvRow (_DataRow):
    '''This is merely a renaming of atlas.data.DataRow.'''
    pass

class CsvSet (_DataSet):
    '''This extends atlas.data.DataSet by accepting a filename in the
    initializer and by setting the rowclass to default to CsvRow.'''
    def __init__(self, data=None, fields=(), source=None, rowclass=CsvRow,
                 filename=None):
        _DataSet.__init__(self, data, fields, source, rowclass)
        self.filename = filename

class CsvSource:
    '''Provides access to a data project kept in CSV files.'''
    def __init__(self, datadir, project):

        '''Initializes data source to use data files kept in the
        project subdirectory of datadir.
        >>> source = CsvSource("/home/eric/Documents/work/atlas", "AFAM")
        >>> source
        <CsvSource AFAM>
        '''
        self.project = project
        self.datadir = datadir
        self._cache = {}
        d = _os.path.join(datadir, project)
        if not _os.path.exists(d):
            _os.makedirs(d)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.project)

    def loadinfs(self):
        '''Loads the informants, putting the data into the INFORMANTS,
        COMMUNITIES, FIELDWORKERS, and WORKSHEETS directories.'''

        infs = []
        fws = {}
        wss = {}
        coms = {}
        tnames = _tables.TableNames
        fields = _tables.TableFields
        inffile = _os.path.join(self.datadir, self.project, tnames.INFORMANTS)
        if _os.path.exists(inffile):
            for line in open(inffile).xreadlines():
                line = _fcsv.split(line)
                if not line:
                    continue
                com = coms.setdefault(line[1], tuple([line[1]]+line[-3:]) )
                fw = fws.setdefault(line[5], (len(fws), line[5], '') )
                ws = wss.setdefault(line[6], (len(wss), line[6], '') )
                infs.append(tuple(line[:1] +
                                  [com[0]] +
                                  line[2:5] +
                                  [fw[0], ws[0]] +
                                  line[7:16]))
        cache = self._cache
        fn = self.fieldnames
        cache[tnames.INFORMANTS] = CsvSet(data=infs,
                                          fields=fn(fields.INFORMANTS),
                                          source=self,
                                          filename=inffile)
        cache[tnames.COMMUNITIES] = CsvSet(data=coms.values(),
                                           fields=fn(fields.COMMUNITIES),
                                           source=self)
        cache[tnames.FIELDWORKERS] = CsvSet(data=fws.values(),
                                            fields=fn(fields.FIELDWORKERS),
                                            source=self)
        cache[tnames.WORKSHEETS] = CsvSet(data=wss.values(),
                                          fields=fn(fields.WORKSHEETS),
                                          source=self)

    def fieldnames(self, fields):
        '''Returns the field names from a table specification in
        atlas.tables.'''
        return tuple([field[0] for field in fields])

    def _getFields(self, row, fields):
        '''Returns the specified fields in row. Fields can be
        specified using either field indices or (if the row object is
        a descendent of atlas.data.DataRow) field names.
        >>> copier = Copier(None, None)
        >>> copier._getFields(("a", "b", "c", "d", "e", "f", "g"), (3, 4, 0))
        ('d', 'e', 'a')
        '''
        data = []
        for f in fields:
            data.append(row[f])
        return tuple(data)

    def _getCom(self, informid, re=_reCom):
        '''Returns the community specification from the informant ID.
        >>> copier = Copier(None, None)
        >>> copier._getCom("NC2A")
        'NC2'
        >>> copier._getCom("SC24GA")
        'SC24G'
        '''
        match = re.match(informid)
        if match: return match.group('community')
        else: return None

    def loadLatLong(self, latlongfile):
        '''Grafts the information in the latlongfile onto the
        INFORMANTS table.'''
        latlong = self.loadFile(latlongfile,
                                fields=('infid', 'latitude', 'longitude',))
        infs = self.getInformants()
        getFields = self._getFields
        llset = {}
        for row in latlong:
            llset[row['infid']] = getFields(row, ('latitude', 'longitude',))
        for i in range(len(infs)):
            row = infs[i]
            data = row.data + llset.get(row['infid'], (-1.0, -1.0,))
            infs.data[i] = data

    def loadXY(self, xyfile):
        '''Grafts the x, y image data onto the COMMUNITIES table.'''
        xy = self.loadFile(xyfile, fields=('comcode', 'x', 'y',))
        infs = self.getInformants()
        coms = self.getCommunities()
        getCom = self._getCom
        xyd = {}
        comcodes = {}
        for row in xy:
            xyd[row['comcode']] = row.data
        for row in infs:
            comcodes[row['comid']] = getCom(row['informid'])
        for i in range(len(coms)):
            row = coms[i]
            data = row.data + xyd.get(comcodes[row['comid']], ('', -1, -1))
            coms.data[i] = data

    def loadHeadNotes(self, headnotedir):
        '''Grafts entries from the headnotes directory onto the TABLES
        table.'''
        tables = self.getTables()
        for i in range(len(tables)):
            row = tables[i]
            headnotefile = _os.path.join(headnotedir, row['tablename'])
            if _os.path.exists(headnotefile):
                data = list(row.data)
                data[-1] = open(headnotefile).read()
                tables.data[i] = tuple(data)

    def loadtables(self):
        '''Loads the TABLES file.'''
        tfile = _os.path.join(self.datadir, self.project,
                              _tables.TableNames.TABLES)
        data = []
        if _os.path.exists(tfile):
            for line in open(tfile).xreadlines():
                line = _fcsv.split(line)
                if not line:
                    continue
                data.append(tuple(line))
        self._cache[_tables.TableNames.TABLES] = CsvSet(
                data=data,
                fields=self.fieldnames(_tables.TableFields.TABLES),
                source=self,
                filename=tfile
                )

    def loaditem(self, itemname):
        '''Loads the data file given in itemname, which is the
        filename of the data file. This performs some replacements on
        the data. For example, it replaces the informant information
        with just the infid.'''

        filename = _os.path.join(self.datadir, self.project, itemname)
        data = []
        if _os.path.exists(filename):
            infs = self.getInformants()
            infd = {}
            for i in infs:
                infd[i[2]] = i[0]
            for line in open(filename).xreadlines():
                line = _fcsv.split(line)
                if not line:
                    continue
                data.append(tuple(line[:1] +
                                  [infd.get(line[1], '')] +
                                  line[3:8] +
                                  [_simplify(line[7])] +
                                  line[8:]))
                                  #'blew,NY1,50,V,N,-0-,-0-,bluw,MS,1'
        self._cache[itemname] = CsvSet(
            data=data,
            fields=self.fieldnames(_tables.TableFields.ITEM),
            source=self,
            filename=filename
            )

    def loadpage(self, page):
        filename = _os.path.join(self.datadir, self.project,
                                 _tables.TableNames.PAGE%page)
        data = []
        if _os.path.exists(filename):
            infs = self.getInformants()
            infd = {}
            for i in infs:
                infd[i[2]] = i[0]
            for line in open(filename).xreadlines():
                line = _fcsv.split(line)
                if not line:
                    continue
                data.append(tuple(line[:1] +
                                  [infd.get(line[1], '')] +
                                  line[3:10] +
                                  [line[11], '', line[10], '']))
        self._cache[page] = CsvSet(
            data=data,
            fields=self.fieldnames(tables.TableFields.PAGE),
            source=self,
            filename=filename
            )

    def getTable(self, tablename, loadfunc):
        '''Get the table information, loading it into the cache with
        loadfunc if it is not already there.'''
        if not self._cache.has_key(tablename):
            loadfunc()
        return self._cache[tablename]

    def getInformants(self):
        '''Get the INFORMANTS table.'''
        return self.getTable(_tables.TableNames.INFORMANTS, self.loadinfs)
    def getCommunities(self):
        '''Get the COMMUNITIES table.'''
        return self.getTable(_tables.TableNames.COMMUNITIES, self.loadinfs)
    def getFieldWorkers(self):
        '''Get the FIELDWORKERS table.'''
        return self.getTable(_tables.TableNames.FIELDWORKERS, self.loadinfs)
    def getWorkSheets(self):
        '''Get the WORKSHEETS table.'''
        return self.getTable(_tables.TableNames.WORKSHEETS, self.loadinfs)
    def getTables(self):
        '''Get the TABLES table.'''
        return self.getTable(_tables.TableNames.TABLES, self.loadtables)

    def getItem(self, itemname):
        '''Get a data table itemname.'''
        tablename = _tables.escTable(itemname)
        return self.getTable(tablename,
                             lambda x=tablename, s=self: s.loaditem(x))
    def getPage(self, page):
        return self.getTable(_tables.TableNames.PAGE % page,
                             lambda x=page, s=self: s.loadpage(x))

    def loadFile(self, filename, fields=()):
        '''Returns a CsvSet object of the data in filename, containing
        fields fields.'''
        return CsvSet(
            data = [ tuple(_fcsv.split(line))
                     for line in open(filename).xreadlines() ],
            fields=fields,
            source=self,
            filename=filename)

    def saveFile(self, dataset):
        '''Saves the dataset.'''
        fout = open(dataset.filename, 'wc')
        for line in dataset:
            print >>fout, line.csv()
        fout.close()

    def lookup(self, dataset, field):
        '''Creates a dictionary to do indexed look-ups on field
        (either field name or field index) to the rows in dataset.'''
        dict = {}
        for row in dataset:
            dict[row[field]] = row.data
        return dict

    def saveinfs(self):
        '''Gathers information from the four winds to save the
        INFORMANTS table.'''
        infs = self.getInformants()
        coms = self.lookup(self.getCommunities(), 'comid')
        fws = self.lookup(self.getFieldWorkers(), 'fwid')
        wss = self.lookup(self.getWorkSheets(), 'wsid')
        fout = open(infs.filename, 'wc')
        for i in infs:
            i = list(i.data)
            print >>fout, _fcsv.join(i[:5] +
                                     [ fws.get(i[5], [None, ''])[1],
                                       wss.get(i[6], [None, ''])[1] ] +
                                     i[7:16] +
                                     list(coms.get(i[1], ['', '', ''])[1:]))
        fout.close()

    def savetables(self):
        '''Saves the TABLES dataset.'''
        self.saveFile(self.getTables())

    def saveitem(self, itemname):
        '''Saves an item.'''
        infs = self.lookup(self.getInformants(), 'infid')
        item = self.getItem(itemname)
        fout = open(item.filename, 'wc')
        for i in item:
            i = list(i.data)
            print >>fout, _fcsv.join(i[:1] +
                    infs.get(i[1], ['', '', '', '', ''])[2:4] +
                    i[2:])
        fout.close()

    def saveitems(self):
        '''Saves all items.'''
        tables = [ value
                   for (key, value) in _tables.TableNames.__dict__.items()
                   if not key.startswith('_') ]
        for key in self._cache.keys():
            if isinstance(key, _StringType) and key not in tables:
                self.saveitem(key)

    def savepage(self, page):
        dataset = self._cache.get(page, None)
        if dataset:
            infs = self.lookup(self.getInformants(), 'infid')
            fout = open(dataset.filename, 'wc')
            for item in dataset:
                item = list(item)
                print >>fout, _fcsv.join(
                        item[:1] +
                        infs.get(item[1], ['', '', '', '', ''])[2:4] +
                        item[2:]
                        )
            fout.close()

    def savepages(self):
        for key in self._cache.keys():
            if isinstance(key, _IntType):
                self.savepage(key)

    def commit(self):
        '''Commit changes to all open datafiles.'''
        self.saveinfs()
        self.savetables()
        self.saveitems()
        self.savepages()

    def close(self):
        '''A no-op for whatever to atlas.db.DbSource.'''
        pass

