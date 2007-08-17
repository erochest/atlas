
'''Provides basic objects for data sets and rows.
'''

__all__ = [
    'DataSet',
    'DataRow',
    ]

import fcsv as _fcsv
import sys as _sys
from types import DictType as _DictType
from types import StringType as _StringType
from UserList import UserList as _UserList
from weakref import ref as _ref
from operator import setitem as _setitem

_commanl = ',\n'

class DataRow:
    '''Contains a data row.'''
    def __init__(self, data=None, dataset=None):
        '''Initializes a data row with data and a dataset, from which
        it gets the fields and other important information and to
        which it keeps a weak reference.

        In many ways, this is supposed to look like a non-mutable
        list, except you can index it also on field names (if the
        dataset is provided).

        >>> row = DataRow(('Eric', 'Rochester', 31))
        >>> row.fields = ('fname', 'lname', 'age')
        >>> row[0]
        'Eric'
        >>> row['age']
        31

        '''
        if data:
            self.data = tuple(data)
        else:
            self.data = ()

        if dataset:
            self.dataset = _ref(dataset)
            self.fields = dataset.fields
        else:
            self.dataset = lambda: None
            self.fields = ()

    def reset(self, data):
        '''Resets the data in with data.'''
        self.data = data

    def copy(self):
        '''Copies the DataRow\'s data and dataset into a new object.'''
        return self.__class__(self.data, self.dataset)

    def index(self, i):
        '''Returns the index of i. If i is a string, it returns the
        index of the fieldname; if it is an integer, it returns the
        integer.
        >>> row = DataRow(('a', 'b', 'c', 'd'))
        >>> row.fields = ('first_col', 'second_col', 'third_col', 'fourth_col')
        >>> row.index(1)
        1
        >>> row.index('second_col')
        1
        >>> row.index('Not a column')
        Traceback (most recent call last):
            ...
        ValueError: list.index(x): x not in list
        '''

        if isinstance(i, _StringType):
            return list(self.fields).index(i)
        else:
            return i

    def dict(self):
        '''Returns a dictionary mapping field names to values.
        >>> row = DataRow(('Eric', 'Rochester', 31))
        >>> row.fields = ('FirstName', 'LastName', 'Age')
        >>> row.dict() == {'FirstName': 'Eric', 'LastName': 'Rochester', 'Age': 31}
        1
        '''
        d = {}
        [ _setitem(d, key, value)
          for (key, value) in zip(self.fields, self.data) ]
        return d

    def tuple(self):
        '''Returns the data as a tuple.
        >>> row = DataRow(['Eric', 'Rochester', 31])
        >>> row.tuple()
        ('Eric', 'Rochester', 31)
        '''
        return self.data

    def csv(self):
        '''Returns the data as a comma-separated value
        >>> row = DataRow(('Eric', 'Rochester', 'July 1, 1970', 31))
        >>> row.csv()
        'Eric,Rochester,"July 1, 1970",31'
        '''
        return _fcsv.join(map(str, self.data))

    def zip(self):
        '''Returns a list of tuple of (field, value).
        >>> row = DataRow(('Eric', 'Rochester', 'July 1, 1970', 31))
        >>> row.fields = ('FirstName', 'LastName', 'DOB', 'Age')
        >>> row.zip()
        [('FirstName', 'Eric'), ('LastName', 'Rochester'), ('DOB', 'July 1, 1970'), ('Age', 31)]
        '''
        return zip(self.fields, self.data)

    def pp(self, out=_sys.stdout):
        '''This pretty prints the data to out. Right now, it just
        prints it.'''
        print >>out, self.data

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self.data)

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        return self.data[self.index(i)]

class DataSet:
    '''This contains a dataset. In many ways, it is supposed to look
    like a tuple, except that it is mutable using append and
    extend. When you get a row, it is always the same DataRow object,
    but the data in it has been changed. Thus, if you try to store the
    rows and you retrieve them, they will all have the same values as
    the last one to be retrieved. Use the DataRow.copy method to get
    new DataRow objects or only store the DataRow.data attribute.'''

    def __init__(self, data=None, fields=(), source=None, rowclass=DataRow):
        '''Initializes a new DataSet.

        data is the data (usually a list of tuples or tuple of tuples);
        fields is a tuple of field names;
        source is the data source; and
        rowclass is the class used to hold row objects.
        '''

        if data:
            self.data = list(data)
        else:
            self.data = []

        self.source = source
        self.fields = fields
        self.rowclass = rowclass
        self._row = None

    def __len__(self):
        return len(self.data)

    def row(self, data):
        '''Returns a row object containing data.'''
        if not self._row:
            self._row = self.rowclass(data, self)
        else:
            self._row.reset(data)
        return self._row

    def dict(self, indexfield):
        '''Returns a dictionary for easily looking up a row of data
        using the value of the indexfield, which can be either an
        integer or string.'''
        if isinstance(indexfield, _StringType):
            indexfield = list(self.fields).index(indexfield)
        d = {}
        for datum in self.data:
            d[ datum[indexfield] ] = datum
        return d

    def fromDict(self, dict, default=None):
        '''Returns a tuple derived from pulling the values out of
        dict.
        >>> set = DataSet(fields=('fname', 'lname', 'age'))
        >>> set.fromDict({'fname': 'Eric', 'lname': 'Rochester'})
        ('Eric', 'Rochester', None)
        '''
        f = list(self.fields)
        l = [default] * len(f)
        for key, value in dict.items():
            try:
                l[f.index(key)] = value
            except ValueError:
                pass
        return tuple(l)

    def pp(self, out=_sys.stdout):
        '''This pretty prints the data to out. This just prints the
        field names and the data, one row per line.'''
        print >>out, self.__str__()

    def getdata(self, item):
        '''Tries to intellegently get the data from item.

        If item is a dictionary, it passes it through DataSet.fromDict;
        if item is a DataRow, it returns item.data;
        otherwise, it returns item.
        '''
        if isinstance(item, _DictType):
            item = self.fromDict(item)
        elif isinstance(item, DataRow):
            item = item.data
        return item

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def __str__(self):
        out = [ repr(self.fields) ]
        out.extend([repr(line) for line in self.data])
        return '[\n%s\n]' % _commanl.join(out)

    def __getitem__(self, i):
        return self.row(self.data[i])

    def __getslice__(self, i, j):
        return self.__class__(self.data[i:j], self.fields, self.source,
                              self.rowclass)

    def append(self, item):
        '''Appends item to self.data (nothing fancy).'''
        self.data.append(item)
    def extend(self, items):
        '''Extends self.data with items (nothing fancy).'''
        self.data.extend(items)
    __iadd__ = extend

