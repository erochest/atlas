#! D:\Python23\python.exe

from jon import cgi
import pgdb

class Handler(cgi.DebugHandler):
    def process(self, req):
        req.set_header('Content-Type', 'text/plain')
        req.write('Greetings, Earthling!\n\n')
        conn = pgdb.connect(
            #user='apache', database='afam'
            user='lap', password='lap', database='afam', host='localhost',
            )
        req.write('Connected to database: %r\n' % conn)

cgi.CGIRequest(Handler).process()

