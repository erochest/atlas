#! /usr/bin/env python

"""\
usage: timedb.py [old|new] [dbname]

"""

import sys, time, MySQLdb

def timetask(msg, f, *args, **kwargs):
    (result, time) = timef(f, *args, **kwargs)
    print msg, 'accomplished in', time, 'seconds'

class SimpleQuery:
    def __init__(self, sql):
        self.sql = sql

    def __iter__(self):
        return iter([ (self.sql, None) ])

class Query:
    def __init__(self, sql, params):
        self.sql = sql
        self.params = params

    def __iter__(self):
        return iter([ (self.sql, p) for p in self.params ])

class DBTimer:
    def __init__(self, user, db, queries, n=100):
        self.user = user
        self.db = db
        self.queries = queries
        self.n = n
        self.conn = MySQLdb.connect(user=user, db=db, unicode='utf-8')
        self.conn.converter[unicode] = self._unicode
        self.timings = []

    def _unicode(self, u, d=None):
        return self.conn.literal(u.encode('utf-8'))

    def close(self):
        self.conn.close()

    def timef(self, f, *args, **kwargs):
        start = time.time()
        f(*args, **kwargs)
        end = time.time()
        return end - start

    def exec_fetch(self, cursor, sql, params):
        cursor.execute(sql, params)
        cursor.fetchall()

    def time(self):
        # prep to get the memory allocated
        cursor = self.conn.cursor()
        timef = self.timef
        ef = self.exec_fetch
        try:
            print 'Warming up...'
            for i in range(self.n/10):
                for q in self.queries:
                    for (sql, params) in q:
                        timef(ef, cursor, sql, params)
            print 'Timing...'
            self.timings = timings = [None] * self.n
            for i in range(self.n):
                for q in self.queries:
                    for (sql, params) in q:
                        timings[i] = timef(ef, cursor, sql, params)
        finally:
            self.close()

    def report(self):
        total = 0.0
        for t in self.timings:
            #print t
            total += t
        #print
        print 'n =', len(self.timings)
        print 'x =', total / float(len(self.timings))
        print

sq = SimpleQuery
q = Query

QUERIES = {
    'new': [
        sq('select * from Informants;'),
        q('select * from Informants where auxiliary=%s;', [('Y',)]),
        q('select infid, comid, informid, sex, age from Informants where auxiliary=%s;', [('Y',)]),
        q('select * from Informants where sex=%s;', [('F',)]),
        sq('select * from Communities;'),
        sq('select * from Informants, Communities where Informants.comid=Communities.comid;'),
        q('select * from Informants, Communities where Informants.comid=Communities.comid and Informants.sex=%s;', [('F',)]),
        q('select infid, Informants.comid, state from Informants, Communities where Informants.comid=Communities.comid and Informants.sex=%s;', [('F',)]),
        q('select infid, Informants.comid, state from Informants, Communities where Informants.comid=Communities.comid and Communities.state=%s;', [('NC',)]),
        sq('select * from FieldWorkers;'),
        sq('select * from WorkSheets;'),
        sq('select * from Targets;'),
        q('select * from Responses, Informants, Targets where Targets.target=%s and Targets.targetid=Responses.targetid and Informants.infid=Responses.infid;', [('dragonfly',)]),
        q('select x, y from Communities, Targets, Responses, Informants where Informants.comid=Communities.comid and Targets.target=%s and Targets.targetid=Responses.targetid and Informants.infid=Responses.infid;', [('dragonfly',)]),
        q('select * from Responses, Informants, Targets where Targets.target=%s and Targets.targetid=Responses.targetid and Informants.infid=Responses.infid and Responses.item=%s;', [('dragonfly', u'snake doctor')]),
        ],

    'old': [
        sq('select * from _informants_;'),
        q('select * from _informants_ where auxiliary=%s;', [('Y',)]),
        q('select infid, comid, informid, sex, age from _informants_ where auxiliary=%s;', [('Y',)]),
        q('select * from _informants_ where sex=%s;', [('F',)]),
        sq('select * from _communities_;'),
        sq('select * from _informants_, _communities_ where _informants_.comid=_communities_.comid;'),
        q('select * from _informants_, _communities_ where _informants_.comid=_communities_.comid and _informants_.sex=%s;', [('F',)]),
        q('select infid, _informants_.comid, state from _informants_, _communities_ where _informants_.comid=_communities_.comid and _informants_.sex=%s;', [('F',)]),
        q('select infid, _informants_.comid, state from _informants_, _communities_ where _informants_.comid=_communities_.comid and _communities_.state=%s;', [('NC',)]),
        sq('select * from _fieldworkers_;'),
        sq('select * from _worksheets_;'),
        sq('select * from _tables_;'),
        sq('select * from dragonfly_, _informants_ where _informants_.infid=dragonfly_.infid;'),
        sq('select x, y from _communities_, dragonfly_, _informants_ where _informants_.comid=_communities_.comid and _informants_.infid=dragonfly_.infid;'),
        q('select * from dragonfly_, _informants_ where _informants_.infid=dragonfly_.infid and dragonfly_.item=%s;', [(u'snake doctor',)]),
        ],
    }

def main(target, dbname):
    queries = QUERIES[target]
    dbtimer = DBTimer('root', dbname, queries)
    dbtimer.time()
    dbtimer.report()

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print __doc__
        raise SystemExit()
    (target, dbname) = sys.argv[1:]
    main(target, dbname)

