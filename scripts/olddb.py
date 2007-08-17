#! /usr/bin/env python

r'''Usage: csv2mysql.py --super-user=<user>:<password> --project=<name> \
        --user=<user>:<password> --clean --help

Transfers the data from the CSV files to a MySQL database.
'''


# load all the standard modules
import os, sys, getopt
#sys.path.append('/home/eric/atlas/old-modules/atlasmodule')
import lap.data.fcsv
sys.modules['fcsv'] = lap.data.fcsv

import atlas.mysql
from atlas import conversion, csv, db
import MySQLdb

colon = ':'

def error(msg=None, code=1):
    sys.stderr.write(__doc__)
    if msg:
        sys.stderr.write(msg)
    sys.exit(code)

_db = None
def getDb(super, force=0, dbname=None):
    global _db
    if force and _db:
        _db = None
    if not _db:
        superd = { 'user': super[0], }
        if len(super) == 2:
            superd['passwd'] = super[1]
        if dbname:
            superd['db'] = dbname
        _db = MySQLdb.connect(**superd)
    return _db

def getdbs(super, project):
    return db.DbSource(getDb(super, force=1, dbname=project),
                       MySQLdb.paramstyle)

def user(super, userinfo, project):
    return
    print 'Granting %s select rights on %s...' % (userinfo[0], project)
    cur = getDb(super, force=1, dbname='mysql').cursor()
    cur.execute(
        "GRANT SELECT ON %s.* " \
        "TO %s@localhost IDENTIFIED BY '%s'" % ((project,)+userinfo)
        )
    cur.close()

def hasDb(db, dbname):
    c = db.cursor()
    c.execute('SHOW DATABASES')
    dblist = c.fetchall()
    c.close()
    return (dbname,) in dblist

# actions
def clean(super, project):
    db = getDb(super, force=1)
    c = db.cursor()
    c.execute('DROP DATABASE IF EXISTS %s' % project)
    c.close()

def setup(super, project):
    connection = getDb(super, force=1)
    cur = connection.cursor()
    cur.execute('CREATE DATABASE IF NOT EXISTS %s' % project)
    cur.close()


def main():
    super = userinfo = project = cleanp = None

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            's:p:u:ch',
            [ 'super-user=', 'project=', 'user=', 'clean', 'help', ])
    except getopt.error, e:
        error('Invalid command-line argument: %s'%e)

    for opt, value in opts:
        if opt == '-s' or opt == '--super-user':
            super = tuple(value.split(colon))
        elif opt == '-u' or opt == '--user':
            userinfo = tuple(value.split(colon))
        elif opt == '-p' or opt == '--project':
            project = value
        elif opt == '-c' or opt == '--clean':
            cleanp = 1
        elif opt == '-h' or opt == '--help':
            error(None, 0)

    if not project:
        error('You must specify a project.')
    if not super:
        error('You must specify a super-user.')

    csvdir = os.path.join(os.getcwd(), project)
    if not os.path.isdir(csvdir):
        error('%s does not exist or is not a directory.'%csvdir)

    dbname = project + '_old'

    if cleanp:
        print 'Cleaning old database', dbname
        clean(super, dbname)

    print 'Loading CSV database...'
    csvs = csv.CsvSource(os.getcwd(), project)
    print 'Creating MySQL database...'
    setup(super, dbname)
    print 'Loading MySQL database...'
    dbs = getdbs(super, dbname)

    copier = conversion.Copier(csvs, dbs, 1)
    copier.run(
        os.path.join(csvdir, '_latlong_'),
        os.path.join(csvdir, '_xy_'),
        os.path.join(csvdir, 'headwords')
        )

    if userinfo:
        user(super, userinfo, project)

    print 'Done!'

if __name__ == '__main__':
    main()

