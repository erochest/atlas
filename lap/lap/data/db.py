
"""
To create the database:

    drop database lap;
    create database lap;
    grant all privileges on lap.* to w_lap@localhost identified by 'laplace';

"""


__version__ = '0.0'
__all__ = [
    'DB',
    ]


import logging
from operator import setitem
import os
import sys

import MySQLdb
#import sqlite

from lap import TRACE
from lap import settings
from lap.data.csvproj import community, CSVProject, Informant, Community, \
    FieldWorker, WorkSheet, Target
from lap.data.phonetics import simplify
from lap.data.tables import TABLEDEFS, INDEXDEFS
from lap.data import values


LOG_NAME = 'lap.data.db'

COMMA = ', '
SPACE = ' '
AND = ' AND '


class DB:
    ENCODING = 'utf-8'

    def __init__(self):
        self.conn = self._cursor = None
        self.log = logging.getLogger(LOG_NAME)

    def trace(self, msg, *args, **kwargs):
        self.log.log(TRACE, msg, *args, **kwargs)

    def connect(self, **kwargs):
        self.trace('connect(**%r)', kwargs)
        self.conn = MySQLdb.connect(**kwargs)
        #dbname = kwargs['db'] + '.sqlite3'
        #self.newdb = not os.path.exists(dbname)
        #self.conn = sqlite.connect(dbname)

    def _unicode(self, u, d=None):
        return self.conn.literal(u.encode(self.ENCODING))

    def cursor(self):
        if self._cursor is None:
            self._cursor = self.conn.cursor()
        return self._cursor

    def execute(self, sql, args=None):
        self.trace('execute(%r, ...)', sql)
        self.log.debug('SQL: %r, %r', sql, args)
        if args:
            for (key, value) in args.items():
                if isinstance(value, unicode):
                    args[key] = value.encode('utf-8')
        cursor = self.cursor()
        try:
            if args: r = cursor.execute(sql, args)
            else: r = cursor.execute(sql)
        except:
            self.log.error('Error on SQL statement: %r, %r', sql, args)
            raise
        else:
            return r

    def queryrow(self, sql, args=None):
        self.trace('queryrow(%r, ...)', sql)
        self.log.debug('SQL: %r, %r', sql, args)
        if args:
            for (key, value) in args.items():
                if isinstance(value, unicode):
                    args[key] = value.encode('utf-8')
        cursor = self.cursor()
        try:
            if args: cursor.execute(sql, args)
            else: cursor.execute(sql)
            r = cursor.fetchone()
        except:
            self.log.error('Error on SQL statement: %r, %r', sql, args)
            raise
        else:
            return r

    def command(self, cmd):
        self.trace('command(%r)', cmd)
        self.log.debug('COMMAND: %r', cmd)
        os.system(cmd)

    def close(self):
        self.trace('close()')
        self.conn.close()

    def dropDB(self, name):
        self.trace('dropDB(%r)', name)
        for table, indices in INDEXDEFS.items():
            for name in indices:
                self.execute('DROP INDEX %s ON %s;' % (name, table))
        for name in TABLEDEFS:
            self.execute('DROP TABLE %s IF EXISTS;' % name)

    def createTable(self, name, fields, keys):
        self.trace('createTable(%r, ...)', name)
        fields = [ SPACE.join(fieldDef) for fieldDef in fields ] + \
                 [ 'KEY %s (%s)' % (field, field) for field in keys ]
        fields = COMMA.join(fields)
        self.execute('CREATE TABLE IF NOT EXISTS %s (%s);' % (name, fields))
        #for field in keys:
        #    self.execute('CREATE INDEX %s_%s_index ON %s (%s);' %
        #                 (name, field, name, field))

    def create(self):
        self.trace('create()')
        #if not self.newdb:
        #    return
        for (name, cols) in TABLEDEFS.items():
            self.createTable(name, cols, INDEXDEFS.get(name, ()))

    def insert(self, table, data):
        self.trace('insert(%r, ...)', table)
        fields = data[0].keys()
        fields.sort()
        valueDefs = [ '%%(%s)s' % f for f in fields ]
        sql = 'INSERT INTO %s (%s) VALUES (%s);' % \
              (table, COMMA.join(fields), COMMA.join(valueDefs))
        for row in data:
            self.execute(sql, row)

    def select(self, table, fields, where='', whereValues=None,
               orderby=''):
        self.trace('select(%r, ...)', table)
        fields = COMMA.join(fields)
        if where:
            where = ' WHERE %s' % where
        if orderby:
            orderby = ' ORDER BY %s' % COMMA.join(orderby)
        sql = 'SELECT %s FROM %s%s%s;' % (fields, table, where, orderby)
        self.execute(sql, whereValues)
        result = self.cursor().fetchall()
        return result

    def commit(self):
        self.trace('commit()')
        self.conn.commit()

    def rollback(self):
        self.trace('rollback()')
        self.conn.rollback()

    def last_insert_id(self):
        return self.queryrow('SELECT LAST_INSERT_ID()')[0]
        #return self.queryrow('SELECT LAST_INSERT_ROWID()')[0]

    def importCSV(self, project, datadir='.', headnotedir='headwords',
                  dbconnect={}):
        """
        A long, nasty piece of code follows.
        Beware all who enter here!

        """

        self.trace('importCSV(%r, ...)', project)
        csv = CSVProject(datadir, headnotedir)
        self.connect(**dbconnect)
        try:
            try:
                self.create()
                proj_info = settings.meta.projects[project]
                self.insert(
                    'Projects',
                    [{'name': proj_info.name,
                      'long_name': proj_info.description}],
                    )
                projid = self.last_insert_id()
                # processing informants
                infs = list(csv.informants())
                # add data
                cursor = self.cursor()
                for fw in FieldWorker.get_cached():
                    fw.projid = projid
                    fw.insert_sql(cursor)
                    fw.fwid = self.last_insert_id()
                for ws in WorkSheet.get_cached():
                    ws.projid = projid
                    ws.insert_sql(cursor)
                    ws.wsid = self.last_insert_id()
                # processing latlong
                csvll = {}
                for ll in csv.latlong():
                    csvll[ll['infid']] = ll
                for i in infs:
                    ll = csvll[str(i.infid)]
                    i.latitude = ll['latitude']
                    i.longitude = ll['longitude']
                # processing xy & reindexing communities
                coms2 = {}
                for c in Community.get_cached():
                    coms2.setdefault(c['code'], []).append(c)
                for xy in csv.xy():
                    if xy['comcode'] in coms2:
                        for c in coms2[xy['comcode']]:
                            c.x = xy['x']
                            c.y = xy['y']
                # inserting more data
                for c in Community.get_cached():
                    c.projid = projid
                    del c.comid
                    c.insert_sql(cursor)
                    c.comid = self.last_insert_id()
                    #print 'c.comid =', id(c._data_), c.name, c.comid
                informids = {}
                for i in infs:
                    i.infid_old = i.infid
                    del i.infid
                    i.projid = projid
                    i.insert_sql(cursor)
                    i.infid = self.last_insert_id()
                    informids[i.informid] = i
                # processing targets & responses
                for target in csv.tables():
                    if 'targetid' in target:
                        continue
                    note = csv.headnote(target.table)
                    if note:
                        target.notes = note.encode('utf-8')
                    target.projid = projid
                    target.insert_sql(cursor)
                    target.targetid = self.last_insert_id()
                    self.log.info('Reading data table %r', target.table)
                    resps = []
                    for line in csv.data(target.table):
                        phonetic = unicode(line['phonetic'], 'lap.data.lamcour')
                        #phonetic = line['phonetic']
                        r = {
                            'item': line['item'],
                            'projid': projid,
                            'infid': informids[line['informid']].infid,
                            'gramflag': line['gramflag'],
                            'doubtflag': line['doubtflag'],
                            'commenttext': line['comment_text'],
                            'commentcodes': line['comment_codes'],
                            #'phonetic': phonetic.encode('utf-8'),
                            #'simplephone': simplify(phonetic).encode('utf-8'),
                            'phonetic': phonetic,
                            'simplephone': simplify(phonetic),
                            'targetid': target.targetid,
                            }
                        resps.append(r)
                    if resps:
                        self.insert('Responses', resps)
            except:
                self.rollback()
                raise
            else:
                self.commit()
        finally:
            self.close()



