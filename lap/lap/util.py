
__version__ = '0.0'
__all__ = [
    'Data',
    'Singleton',
    'loadClass',
    'tmpfile',
    'pathToRoot',
    ]


import os

from quixote.directory import Directory


DOT = '.'
COMMA = ', '


class Data:
    '''A generic data struct'''

    def __init__(self, **kwargs):
        for (key, value) in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        buffer = []
        for item in self.__dict__.items():
            buffer.append('%s=%r' % item)
        return '%s(%s)' % (self.__class__.__name__, COMMA.join(buffer))


class singleton(type):
    '''
    Only one instance of each class using this as a metaclass can be created.

    This is the singleton type. When the class is defined, it creates a
    _single_inst class attribute on the class that references the class's
    single instance. Finally, whenver the class is called, it creates an
    instance of itself, if _single_inst is None, and returns the cached value
    of _single_inst.

    '''

    def __init__(cls, name, bases, dict):
        super(singleton, cls).__init__(name, bases, dict)
        cls._single_inst = None

    def __call__(cls, *args, **kwargs):
        if cls._single_inst is None:
            cls._single_inst = super(singleton, cls).__call__(*args, **kwargs)
        return cls._single_inst


class Singleton(object):
    '''
    Only one instance of each class inherited from this class can be created.

    This is the actual class to inherit from. It is a subclass of object and
    it defines singleton as its metaclass.

    '''

    __metaclass__ = singleton


try:
	from os import tmpfile
except ImportError:
	import os
	import tempfile

	class tmpfile:
		def __init__(self, filename=None, mode='wcb+', buffer=-1):
			if filename is None:
				filename = tempfile.mktemp()
			self._filename = filename
			self._file = open(filename, mode)

		def __del__(self):
			if not self._file.closed:
				self.close()

		def __getattr__(self, attr):
			return getattr(self._file, attr)

		def close(self):
			self._file.close()
			os.remove(self._filename)

		def fileobj(self):
			return self._file


def path_to_root(root, filename, sep=os.sep):
    root = os.path.normcase(os.path.abspath(root))
    filename = os.path.normcase(os.path.abspath(filename))
    if os.path.isfile(filename): filename = os.path.dirname(filename)
    path = []
    old = None
    while filename and filename != root:
        (filename, part) = os.path.split(filename)
        if filename == old: break
        old = filename
        path.append(os.pardir)
    if path: return sep.join(path)
    else: return os.curdir


class lazy_property(object):

    def __init__(self, calculate_function):
        self._calculate = calculate_function

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        value = self._calculate(obj)
        setattr(obj, self._calculate.func_name, value)
        return value


