#! /usr/bin/env python

# TODO: I need to make this more of a useable script and less like
# something written in the heat of the moment.

import logging, os, sys, time
from lap.data.db import DB
from lap.data.tables import TABLEDEFS
from lap import settings
from lap import TRACE
import MySQLdb

def timef(f, *args, **kwargs):
    start = time.time()
    result = f(*args, **kwargs)
    end = time.time()
    return (end-start, result)

def timeproc(task, f, *args, **kwargs):
    logging.info('Starting task %r', task)
    (time, result) = timef(f, *args, **kwargs)
    logging.info('Finished %r in %s seconds', task, time)

#logging.getLogger().setLevel(logging.INFO)
logging.getLogger().setLevel(logging.WARNING)

try:
    datadir = sys.argv[-1]
    #project = os.path.split(datadir)[1].upper()
    project = os.path.basename(datadir)
    dbconnect = settings.locale.connect
    #dbconnect = {'user': 'ODBC', } #'password': 'green'}

    logging.info('Data from %r', datadir)
    logging.info('Database %s', project)

    if '-c' in sys.argv or '--clean' in sys.argv:
        db = DB()
        db.connect(**dbconnect)
        #timeproc('cleaning', db.dropDB, dbconnect['user'], project)
        timeproc('cleaning', db.dropDB, project)

    db = DB()

    timeproc('importing', db.importCSV, project, datadir, dbconnect=dbconnect)

    #logging.info('Granting SELECT access to lap')

    # The user account "lap" is assumed
    #conn = MySQLdb.connect(**dbconnect)
    #cursor = conn.cursor()
    #cursor.execute(
    #    "GRANT SELECT ON %s.* TO lap@localhost IDENTIFIED BY 'lap';" %
    #        (project,)
    #    )
    #conn.commit()

finally:
    logging.shutdown()

