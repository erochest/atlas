
'''This contains an object that writes out message to a file-like
object.
'''

import atlas.debug as _debug
from mx import DateTime as _DateTime
import types as _types


class FileLog:
    '''This logs its output to a file-like object. You can either
    initialize with this object or with a string, which assumes is a
    file name to be opened, and it writes the logs to this.
    >>> import sys
    >>> log = FileLog(sys.stdout)
    >>> log('So long, and thanks for all the fish.')
    So long, and thanks for all the fish.
    '''

    def __init__(self, file, register=1):
        if isinstance(file, _types.StringType):
            file = open(file, 'a')
        self.write = file.write
        if register:
            _debug.log = self

    def __repr__(self):
        return '<%s>' % self.__class__.__name__

    def dump(self, obj):
        '''Dumps an object to the file.
        >>> import sys
        >>> class AClass:
        ...   def __init__(self, data):
        ...      self.data = data
        >>> a = AClass(42)
        >>> log = FileLog(sys.stdout)
        >>> log.dump(a)
        Instance of AClass:
        \tdata = 42
        '''
        write = self.write
        if isinstance(obj, _types.InstanceType):
            write('Instance of %s:\n' % obj.__class__.__name__)
            for attr in dir(obj):
                write('\t%s = %s\n' % (attr, getattr(obj, attr)))
        else:
            write('%s\n' % obj)

    def timestamp(self):
        '''This writes a time stamp to the log.'''
        write = self.write
        write(str(_DateTime.now()))
        write('\n')

    def log(self, *msg):
        '''Dumps the objects in msg to the log.'''
        map(self.dump, msg)

    __call__ = log
