
from lap.data import fcsv
import MySQLdb, sys

(project, table) = sys.argv[1:]

conn = MySQLdb.connect(user='webuser', passwd='webuser', db=project)
try:
    cursor = conn.cursor()
    try:
        cursor.execute('select * from %s;' % table)
        print fcsv.join([ d[0] for d in cursor.description ])
        for row in cursor.fetchall():
            print fcsv.join(map(str, row))
    finally:
        cursor.close()
finally:
    cursor.close()

