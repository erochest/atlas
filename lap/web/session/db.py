

"""
Code for getting a db connection and finding/creating users.

"""


from cPickle import dumps, loads
import sys

import MySQLdb

from lap import settings
from lap.web import query, views


__first = True
def get_cxn():
    global __first
    _cxn = MySQLdb.connect(**settings.locale.connect)
    if __first:
        c = _cxn.cursor()
        try:
            try:
                c.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTO_INCREMENT,
                        username VARCHAR(25) UNIQUE NOT NULL,
                        target VARCHAR(100) DEFAULT NULL,
                        map BOOL DEFAULT 0,
                        field_list MEDIUMTEXT,
                        table_list MEDIUMTEXT,
                        where_clause MEDIUMTEXT,
                        fullphone BOOL,
                        nrhidden BOOL,
                        page INTEGER DEFAULT 1,
                        pagelen INTEGER DEFAULT 25,
                        view TEXT,
                        sort TEXT
                        )
                    ''')
                c.execute('''
                    CREATE TABLE IF NOT EXISTS user_sessions (
                        user_id INTEGER,
                        session_id VARCHAR(25) UNIQUE NOT NULL,
                        remote_addr VARCHAR(50) NOT NULL,
                        creation_time TIMESTAMP DEFAULT NULL,
                        access_time TIMESTAMP DEFAULT NULL
                        )
                    ''')
            except:
                _cxn.rollback()
                raise
            else:
                _cxn.commit()
        finally:
            c.close()
        __first = False
    return _cxn


class User(object):
    """Simple class for holding id/username together. """

    def __init__(self, id, username, target=None, map=None, field_list=None,
                 table_list=None, where_clause=None, fullphone=None,
                 nrhidden=None, page=1, pagelen=25, view='minimal',
                 sort='Informants.infid'):
        self.id = id
        self.username = username
        self.map = map
        self.target = target
        self.view = view
        self._fields = field_list
        self._tables = table_list
        self._where = where_clause
        self.fullphone = fullphone
        self.nrhidden = nrhidden
        self.page = page
        self.pagelen = pagelen
        self.sort = sort

    def _get_fields(self):
        if self._fields is None:
            return list(views.VIEWS[self._view])
        return loads(self._fields)
    def _set_fields(self, fields):
        if fields is None:
            self._fields = None
        else:
            self._fields = dumps(fields, 0)
    fields = property(_get_fields, _set_fields)

    def _get_tables(self):
        if self._tables is None:
            return ['Informants', 'Communities']
        return loads(self._tables)
    def _set_tables(self, tables):
        if tables is None:
            self._tables = None
        else:
            self._tables = dumps(tables, 0)
    tables = property(_get_tables, _set_tables)

    def _get_where(self):
        if self._where is None:
            return query.EQ(('Informants', 'comid'), ('Communities', 'comid'))
        return loads(self._where)
    def _set_where(self, where):
        if where is None:
            self._where = None
        else:
            self._where = dumps(where, 0)
    where = property(_get_where, _set_where)

    def _get_view(self):
        return self._view
    def _set_view(self, view):
        if view is None: view = 'minimal'
        fields = list(views.VIEWS[view])
        if self.target:
            for (field, index) in views.RESPONSE_VIEWS[view]:
                fields.insert(index, field)
        self.fields = fields
        self._view = view
    view = property(_get_view, _set_view)

    def reset(self):
        self.target = None
        self._fields = None
        self._tables = None
        self._where = None
        self.fullphone = 0
        self.nrhidden = 0
        self.map = 0
        self.page = 1

    def reset_all(self):
        pass


def get_user_by_name(username, create=True):
    """Find id for existing username, and optionally create. """
    cxn = get_cxn()
    c = cxn.cursor()
    c.execute('''
            SELECT id, username, target, map, field_list, table_list,
                where_clause, fullphone, nrhidden, page, pagelen, view, sort
            FROM users
            WHERE username=%s
        ''',
        (username,))
    assert c.rowcount <= 1
    if c.rowcount == 1:
        user = User(*c.fetchone())
    elif create:
        c.execute('INSERT INTO users (username) VALUES (%s)', (username,))
        c.execute('SELECT LAST_INSERT_ID()')
        cxn.commit()
        (id,) = c.fetchone()
        user = User(id, username)
    else:
        user = None
    return user


def get_user_by_id(user_id):
    """Get User object for given user_id. """
    cxn = get_cxn()
    c = cxn.cursor()
    c.execute('''
            SELECT id, username, target, map, field_list, table_list,
                where_clause, fullphone, nrhidden, page, pagelen, view, sort
            FROM users
            WHERE id=%s
        ''',
        (user_id,),
        )
    if c.rowcount:
        return User(*c.fetchone())
    else:
        return None


def save_user(cursor, user):
    if user is None:
        return
    cursor.execute('''
            UPDATE users
            SET username=%s, target=%s, map=%s, field_list=%s,
                table_list=%s, where_clause=%s, fullphone=%s, nrhidden=%s,
                page=%s, pagelen=%s, view=%s, sort=%s
            WHERE id=%s
        ''',
        (user.username, user.target, user.map, user._fields, user._tables,
         user._where, user.fullphone, user.nrhidden, user.page, user.pagelen,
         user.view, user.sort,
         user.id),
        )


