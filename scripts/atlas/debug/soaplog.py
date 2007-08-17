
'''This contains a SOAP client and server. The server is started by running
this module from the command line:

$ python /usr/lib/python2.1/site-packages/atlas/debug/soaplog.py

This starts the server, which will print any messages it receives from a client
on the console on which it\'s running.

The client is to be used within the program, like this:

>>> import atlas.debug, atlas.debug.soaplog
>>> atlas.debug.soaplog.SoapLog("http://localhost:9900")
<SoapLog>
>>> atlas.debug.log("Here is a message")

On the console running the server, then the message, "Here is a message",
should appear.

'''

import atlas.debug as _debug
from atlas.debug.filelog import FileLog as _FileLog
import SOAP as _SOAP

class SoapLog (_FileLog):
    def __init__(self, url='http://localhost:9900', register=1):
        self.url = url
        soapfile = _SOAP.SOAPProxy(url)
        _FileLog.__init__(self, soapfile, register)
        self.register = register

    def __getstate__(self):
        dict = self.__dict__.copy()
        del dict['write']
        return dict

    def __setstate__(self, dict):
        soapfile = _SOAP.SOAPProxy(dict['url'])
        dict['write'] = soapfile.write
        if dict['register']:
            _debug.log = self
        self.__dict__.update(dict)

def SoapLogServer(host='localhost', port=9900):
    import sys, atlas.debug.filelog
    server = _SOAP.SOAPServer((host, port))
    server.registerObject(sys.stdout)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print 'Closing SOAP log...'

if __name__ == '__main__':
    # FIXME: probably ought to get host and port from the cmd line
    SoapLogServer()
