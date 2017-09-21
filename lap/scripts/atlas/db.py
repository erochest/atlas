
'''Wraps ODBC object as provided by the mxODBC package. You need to
provide the Connection object to the DbSource constructor, and the
rest of the wrapping should take of itself.
'''

__all__ = [
    'DbRow',
    'DbSet',
    'DbSource',
    'ParamsMixin',
]

from atlas import constants as _constants
from atlas import tables as _tables
from atlas.data import DataRow as _DataRow
from atlas.data import DataSet as _DataSet

_space = ' '
_comma = ', '


class ParamsMixin:
    '''Methods for creating a parameter list based upon the database
    module\'s paramstyle attribute.'''

    def paramlist(self, style, fields):
        '''Returns a list of parameter entries suitable for SQL INSERT
        statements based upon style and fields.

        >>> params = ParamsMixin()
        >>> fields = (\'fname\', \'lname\', \'age\', \'dob\')
        >>> params.paramlist(\'qmark\', fields)
        \'?, ?, ?, ?\'
        >>> params.paramlist(\'numeric\', fields)
        \':1, :2, :3, :4\'
        >>> params.paramlist(\'named\', fields)
        \':fname, :lname, :age, :dob\'
        >>> params.paramlist(\'format\', fields)
        \'%s, %s, %s, %s\'
        >>> params.paramlist(\'pyformat\', fields)
        \'%(fname)s, %(lname)s, %(age)s, %(dob)s\'
        '''
        if style == 'qmark':
            return _comma.join(['?'] * len(fields))
        elif style == 'numeric':
            return _comma.join([(':%d' % (n+1)) for n in range(len(fields))])
        elif style == 'named':
            return _comma.join([(':%s' % f) for f in fields])
        elif style == 'format':
            return _comma.join(['%s'] * len(fields))
        elif style == 'pyformat':
            return _comma.join([('%%(%s)s' % f) for f in fields])

    def paramwhere(self, style, field, pos=1, op='='):
        '''Returns a list of parameter entries suitable for SQL WHERE
        clauses based upon style, field, position, and operation (op).
        >>> params = ParamsMixin()
        >>> params.paramwhere(\'qmark\', \'fname\', op=\'<\')
        \'fname<?\'
        >>> params.paramwhere(\'numeric\', \'fname\', 3)
        \'fname=:3\'
        >>> params.paramwhere(\'named\', \'fname\')
        \'fname=:fname\'
        >>> params.paramwhere(\'format\', \'fname\')
        \'fname=%s\'
        >>> params.paramwhere(\'pyformat\', \'fname\')
        \'fname=%(fname)s\'
        '''
        if style == 'qmark':
            return '%s%s?' % (field, op)
        elif style == 'numeric':
            return '%s%s:%d' % (field, op, pos)
        elif style == 'named':
            return '%s%s:%s' % (field, op, field)
        elif style == 'format':
            return '%s%s%%s' % (field, op)
        elif style == 'pyformat':
            return '%s%s%%(%s)s' % (field, op, field)

class DbRow (_DataRow):
    '''This merely renames atlas.data.DataRow.'''
    pass

class DbSet (_DataSet, ParamsMixin):
    '''This extends atlas.data.DataSet and mixes in ParamsMixin.'''
    def __init__(self, source, cursor=None, table='', paramstyle='qmark'):
        '''Initializes the DbSet.

        source is the DbSource;
        cursor is the cursor that created this DbSet;
        table is the table name;
        paramstyle is the paramstyle attribute of the database module.
        '''
        data = fields = ()
        if cursor:
            try:
                data = cursor.fetchall()
                fields = tuple([ d[0] for d in cursor.description ])
            except:
                pass
        _DataSet.__init__(self, data, fields, source, DbRow)
        self.table = table
        self.param = paramstyle

    def __getslice__(self, i, j):
        slice = self.__class__(self.source, table=self.table)
        slice.data = self.data[i:j]
        slice.fields = self.fields
        return slice

    def execute(self, query, params=None):
        '''Execute query with params.'''
        #print 'executing query:', query
        #print 'with parameters:', params
        #print
        return self.source.execute(query, params)

    def insert(self, data, fields=None):
        '''Insert data into this dataset. If the field 'id' is in
        fields, it is removed.'''
        fields = fields or self.fields
        try:
            fields = list(fields[:])
            fields.remove('id')
        except ValueError:
            pass
        cmd = '''\
INSERT INTO %s (%s)
VALUES (%s)''' % ( self.table,
                   _comma.join(fields),
                   self.paramlist(self.param, fields), )
        data = map(self.getdata, data)
        for d in data:
            self.execute(cmd, d)

    def append(self, item, fields=None):
        '''Appends item onto the data.'''
        self.insert([self.getdata(item)], fields)
        _DataSet.append(self, item)

    def extend(self, items, fields=None):
        '''Extends data with items.'''
        self.insert(map(self.getdata, items), fields)
        _DataSet.extend(self, items)

    __iadd__ = extend


class DbSource (ParamsMixin):
    '''Provides access to a data source from a DB API level 2
    connection object.'''
    def __init__(self, connection, paramstyle='qmark'):
        '''Initializes the DbSource with a connection object and the
        paramstyle attribute of the database module (defaults to
        \'qmark\').'''
        self.db = connection
        self.paramstyle = paramstyle

    def __del__(self):
        try:
            self.db.close()
        except:
            pass

    def execute(self, query, params=None, table=''):
        '''Executes a query (with params and table named table) on a
        new cursor object, returning a DbSet wrapping it. If the query
        does not return anything, the DbSet will be empty.'''
        #print 'Executing:', query, params
        cursor = self.db.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return DbSet(self, cursor, table, paramstyle=self.paramstyle)

    def createTable(self, tablename, fields):
        '''Create a table with fields.'''
        fields = _comma.join([_space.join(field) for field in fields])
        return self.execute('CREATE TABLE %s (%s)' % (tablename, fields),
                            table=tablename)

    def createBaseTables(self):
        '''Creates the base tables (definitions from atlas.tables.'''
        tables = _tables.TableNames
        fields = _tables.TableFields
        create = self.createTable
        create(tables.INFORMANTS, fields.INFORMANTS)
        create(tables.COMMUNITIES, fields.COMMUNITIES)
        create(tables.FIELDWORKERS, fields.FIELDWORKERS)
        create(tables.WORKSHEETS, fields.WORKSHEETS)
        create(tables.TABLES, fields.TABLES)

    def createDataTable(self, itemname, tablename, tabletype, page, subpage,
                        itemno, subitemno, notes=''):
        '''Creates a data table and inserts an entry for it into TABLES.'''
        tablename = tablename or _tables.escTable(itemname)
        self.getTables().append(( itemname, tablename, tabletype,
            page, subpage, itemno, subitemno, notes, ),
            [t[0] for t in _tables.TableFields.TABLES])
        self.createTable(tablename, _tables.TableFields.ITEM)

    def createPageTable(self, page):
        name = _tables.TableNames.PAGE % page
        self.createTable(name, _tables.TableFields.PAGE)

    def hasTable(self, tablename):
        '''Does the data source have a certain table?'''
        try:
            self.execute('SELECT * FROM %s WHERE 0=1'%tablename)
            return 1
        except:
            return 0

    def getTable(self, tablename, order_by=''):
        '''Return the DbSet for all the data and all the fields in
        tablename.'''
        if order_by:
            order_by = 'ORDER BY ' + order_by
        return self.execute('SELECT * FROM %s %s' % (tablename, order_by),
                            table=tablename)

    def getInformants(self):
        '''Return the INFORMANTS table.'''
        return self.getTable(_tables.TableNames.INFORMANTS, 'infid')
    def getCommunities(self):
        '''Return the COMMUNITIES table.'''
        return self.getTable(_tables.TableNames.COMMUNITIES, 'comid')
    def getFieldWorkers(self):
        '''Return the FIELDWORKERS table.'''
        return self.getTable(_tables.TableNames.FIELDWORKERS, 'fwid')
    def getWorkSheets(self):
        '''Return the WORKSHEETS table.'''
        return self.getTable(_tables.TableNames.WORKSHEETS, 'wsid')
    def getTables(self):
        '''Return the TABLES table.'''
        return self.getTable(_tables.TableNames.TABLES, 'itemname')

    def getItem(self, itemname):
        '''Return the table for itemname.'''
        return self.getTable(_tables.escTable(itemname), 'itemid')
    def getPage(self, page):
        return self.getTable(_tables.TableNames.PAGE % page, 'itemid')

    def __getattr__(self, attr):
        return getattr(self.db, attr)

