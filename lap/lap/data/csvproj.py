

__version__ = '0.0'
__all__ = [
    'identity',
    'lamcour',
    'community',
    'Informant',
    'Community',
    'FieldWorker',
    'WorkSheet',
    'Target',
    'Response',
    'CSVProject',
    ]


import csv
import os
import re
import sets
import sys

from lap.data import values


re_community = re.compile(
    r'''
        (?P<community>
            [a-zA-Z]+\d+
            (?:
                G
                (?=[A-Z])
            )?
        )
    ''',
    re.VERBOSE,
    )


def identity(obj):
    return obj


def lamcour(string, encoding='lap.data.lamcour', errors='strict'):
    return unicode(string, encoding, errors)


def community(informid, re=re_community):
    match = re.match(informid)
    if match:
        return match.group('community')
    else:
        return None


class DataItemFactory(object):
    """A caching data item factory. """

    def __init__(self, klass, idkey):
        self.klass = klass
        self.idkey = idkey
        self.cache = {}

    def __call__(self, **args):
        try:
            key = args[self.idkey]
        except KeyError:
            return self.klass(**args)
        else:
            inst = self.cache.get(key, None)
            if inst is None:
                inst = self.cache[key] = self.klass(**args)
            return inst

    def __get__(self, key):
        return self.cache[key]

    def get_cached(self):
        return self.cache.itervalues()


class DataItem(object):
    """
    This uses a borg pattern to cache values.

    """

    _fields_ = {}

    _table_ = None
    _valid_fields_ = sets.Set()

    def __init__(self, **args):
        data = args.copy()
        self.norm_data(data)
        for (key, value) in data.items():
            data[key] = self.__value(key, value)
        self.__dict__['_data_'] = data

    def norm_data(self, data):
        pass

    def __value(self, name, value):
        try:
            converter = self._fields_[name]
        except KeyError:
            raise TypeError('Invalid attribute: %s' % name)
        try:
            value = converter(value)
        except:
            pass
        return value

    def __repr__(self):
        buffer = []
        for item in self._data_.items():
            buffer.append('%s=%r' % item)
        return '%s(%s)' % (self.__class__.__name__, ', '.join(buffer))

    def __contains__(self, name):
        return name in self._data_

    def __getitem__(self, name):
        return self._data_[name]
    def __setitem__(self, name, value):
        self._data_[name] = value
    def __delitem__(self, name):
        del self._data_[name]
    def __iter__(self):
        return iter(self._data_)
    def keys(self):
        return self._data_.keys()
    def items(self):
        return self._data_.items()

    def __getattr__(self, name):
        return self._data_[name]
    def __setattr__(self, name, value):
        if name in self._fields_:
            self._data_[name] = value
        else:
            raise TypeError('Invalid attribute: %s' % name)
    def __delattr__(self, name):
        del self._data_[name]

    def insert_sql(self, cursor):
        fields = [ k for k in self if k in self._valid_fields_ ]
        values = dict([ (k, self[k]) for k in fields ])
        self.norm_fields(fields, values)
        fields.sort()
        params = ', '.join([ '%%(%s)s' % k for k in fields ])
        fields = ', '.join(fields)
        sql = 'INSERT INTO %s (%s) VALUES (%s)' % (self._table_, fields, params)
        cursor.execute(sql, values)

    def norm_fields(self, fields, values):
        pass


class _Informant(DataItem):
    _fields_ = {
        'projid': int,
        'infid': int,
        'infid_old': int,
        'community': identity,
        'informid': str,
        'oldnumber': str,
        'auxiliary': str,
        'field_worker': identity,
        'work_sheet': identity,
        'year': int,
        'inftype': str,
        'generation': str,
        'cultivation': str,
        'sex': str,
        'age': int,
        'education': int,
        'occupation': str,
        'race': str,
        'latitude': float,
        'longitude': float,
        }
    _table_ = 'Informants'
    _valid_fields_ = sets.Set('infid projid comid informid oldnumber '
                              'auxiliary fwid wsid yearinterviewed inftype '
                              'generation cultivation sex age education '
                              'occupation race latitude longitude'.split())

    def norm_data(self, data):
        if 'comid' in data:
            data['community'] = Community(
                comid=data['comid'],
                name=data['community'],
                state=data['state'],
                type=data['comtype'],
                code=data['informid'],
                )
            del data['comid']
            del data['state']
            del data['comtype']
        if 'field_worker' in data:
            data['field_worker'] = FieldWorker(code=data['field_worker'])
        if 'work_sheet' in data:
            data['work_sheet'] = WorkSheet(code=data['work_sheet'])

    def norm_fields(self, fields, values):
        if 'year' in self:
            fields.append('yearinterviewed')
            values['yearinterviewed'] = self.year
        if 'community' in self and 'comid' in self.community:
            fields.append('comid')
            values['comid'] = self.community.comid
        if 'field_worker' in self and 'fwid' in self.field_worker:
            fields.append('fwid')
            values['fwid'] = self.field_worker.fwid
        if 'work_sheet' in self and 'wsid' in self.work_sheet:
            fields.append('wsid')
            values['wsid'] = self.work_sheet.wsid


Informant = DataItemFactory(_Informant, 'informid')


class _Community(DataItem):
    _fields_ = {
        'projid': int,
        'comid': int,
        'type': str,
        'name': str,
        'state': str,
        'code': str,
        'x': int,
        'y': int,
        }
    _table_ = 'Communities'
    _valid_fields_ = sets.Set('comid projid type name state code x y'.split())

    def norm_data(self, data):
        if 'code' in data:
            data['code'] = community(data['code'])


Community = DataItemFactory(_Community, 'comid')


class _FieldWorker(DataItem):
    _fields_ = {
        'fwid': int,
        'projid': int,
        'code': str,
        'name': str,
        }
    _table_ = 'FieldWorkers'
    _valid_fields_ = sets.Set('fwid projid code name'.split())

    def norm_data(self, data):
        if 'code' in data:
            data['name'] = values.FieldWorkers.get(data['code'], None)


FieldWorker = DataItemFactory(_FieldWorker, 'name')


class _WorkSheet(DataItem):
    _fields_ = {
        'wsid': int,
        'projid': int,
        'code': str,
        'name': str,
        }
    _table_ = 'WorkSheets'
    _valid_fields_ = sets.Set('wsid projid code name'.split())

    def norm_data(self, data):
        if 'code' in data:
            data['name'] = values.WorkSheets.get(data['code'], None)


WorkSheet = DataItemFactory(_WorkSheet, 'name')


class _Target(DataItem):
    _fields_ = {
        'targetid': int,
        'table': str,
        'projid': int,
        'target': str,
        'type': str,
        'page': int,
        'subpage': str,
        'item': int,
        'subitem': str,
        'notes': lamcour,
        }
    _table_ = 'Targets'
    _valid_fields_ = sets.Set('targetid projid target type page subpage '
                              'item subitem notes'.split())


Target = DataItemFactory(_Target, 'table')


class CSVProject(object):
    _filenames_ = {
        'informants': '_informants_',
        'latlong': '_latlong_',
        'tables': '_tables_',
        'xy': '_xy_',
        }

    _classes_ = {'informants': Informant, 'tables': Target}

    _fields_ = {
        'informants': (
            ('infid', int),
            ('comid', int),
            ('informid', str),
            ('oldnumber', str),
            ('auxiliary', str),
            ('field_worker', str),
            ('work_sheet', str),
            ('year', int),
            ('inftype', str),
            ('generation', str),
            ('cultivation', str),
            ('sex', str),
            ('age', int),
            ('education', int),
            ('occupation', str),
            ('race', str),
            ('comtype', str),
            ('community', str),
            ('state', str),
            ),
        'latlong': (
            ('infid', int),
            ('latitude', float),
            ('longitude', float),
            ),
        'tables': (
            ('target', str),
            ('table', str),
            ('type', str),
            ('page', int),
            ('subpage', str),
            ('item', int),
            ('subitem', str),
            ('notes', lamcour),
            ),
        'xy': (
            ('comcode', str),
            ('x', int),
            ('y', int),
            ),
        'data': (
            ('item', lamcour),
            ('informid', str),
            ('oldnumber', str),
            ('gramflag', str),
            ('doubtflag', str),
            ('comment_text', lamcour),
            ('comment_codes', lamcour),
            ('phonetic', lamcour),
            ('projectid', str),
            ('itemid', int),
            ),
        }

    def __init__(self, datadir, headnotedir='headwords'):
        self.datadir = datadir
        self.headnotedir = os.path.join(datadir, headnotedir)

    def __file1(self, f, cls):
        for row in f:
            yield cls(**row)

    def _file1(self, filename, fields, cls=None):
        f = csv.DictReader(open(filename, 'rb'), [ n for (n, _) in fields ])
        if cls is not None:
            return self.__file1(f, cls)
        else:
            return f

    def _file2(self, id):
        if id in self._filenames_:
            fn = os.path.join(self.datadir, self._filenames_[id])
            fields = self._fields_[id]
        else:
            table = self._get_tables()[id]
            fn = os.path.join(self.datadir, table[1])
            fields = self._fields_['data']
        cls = self._classes_.get(id, None)
        return self._file1(fn, fields, cls)

    def informants(self):
        return self._file2('informants')

    def latlong(self):
        return self._file2('latlong')

    def tables(self):
        return self._file2('tables')

    def xy(self):
        return self._file2('xy')

    def data(self, target):
        return self._file2(target)

    def headnote(self, filename):
        filename = os.path.join(self.headnotedir, filename)
        if os.path.exists(filename):
            f = open(filename)
            try:
                data = lamcour(f.read())
            finally:
                f.close()
            return data
        else:
            return None

    def _get_tables(self):
        try:
            tables = self._tables
        except AttributeError:
            self._tables = tables = {}
            fn = os.path.join(self.datadir, self._filenames_['tables'])
            f = open(fn)
            try:
                for data in csv.reader(f):
                    tables[data[0]] = tables[data[1]] = data
            finally:
                f.close()
        return tables


