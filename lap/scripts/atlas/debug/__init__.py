
'''This contains a number of useful debugging classes, functions, and
variables. The most important of these is probably DEBUG, which
provides an application-wide constant for whether to print debugging
information. This would be used something like this:

>>> DEBUG = 1
>>> if __debug__:
...     if DEBUG:
...        assert answer == 42
Traceback (most recent call last):
    ...
NameError: name 'answer' is not defined

This package also contains a number of modules that implement
different logging classes. Upon initializing one of these, it installs
itself in the debug module as log, so you can do something like this:

>>> import atlas.debug.filelog, sys
>>> atlas.debug.filelog.FileLog(sys.stdout)
<FileLog>
>>> atlas.debug.log('Here is a message.')
Here is a message.

Beside the FileLog, which can output to any file-like object, there is
also a soaplog that implements both a client and server, but which
requires the SOAP module [FIXME: URL]. I developed this to be able to
debug WebKit program when running the OneShot adapter
(http://webware.sf.net). The client is what is called for printing
debugging information from a program. The server is started by calling
the module from the command line. As client connect as pass it
messages, it simply writes them to standard out. For example,

$ python /usr/lib/python2.1/site-packages/atlas/debug/soaplog.py

'''

__all__ = [
    'DEBUG',
    'log',
    'filelog',
    'soaplog',
    ]

DEBUG = 0
log = None

