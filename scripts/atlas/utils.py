
'''This provides a number of useful functions and classes.
'''

__all__ = [
    'bool',
    'toInt',
    'Set',
    ]

from types import StringType as _StringType

def bool(value):
    '''This takes a value and returns true (1) if the value is a string
    beginning with 'Y' or 'T' (in either case). Otherwise, it returns the
    value itself.

    >>> bool('true')
    1
    >>> bool('no')
    0
    >>> bool('YES')
    1
    >>> bool(1)
    1
    >>> bool(range(3))
    [0, 1, 2]
    '''
    if isinstance(value, _StringType):
        value = value.lower()
        return value.startswith('y') or value.startswith('t')
    else:
        return value

def toInt(value, default=-1):
    '''Tries to coerce value to an integer (using int). If it is unable to
    do so, it returns default, which defaults to -1.
    >>> toInt(3)
    3
    >>> toInt('4')
    4
    >>> toInt('nope')
    -1
    >>> print toInt('no go', None)
    None
    '''
    try:
        return int(value)
    except:
        return default

class Set:
    '''This provides some basic set operations. It doesn't pretend to be
    either full-featured or fast. It's just something I hacked together while
    writing this package.

    >>> set = Set('a', 'z', 'c', 'e')
    >>> set
    ['a', 'c', 'e', 'z']
    >>> set.extend(['b', 'm', 'e'])
    >>> set
    ['a', 'b', 'c', 'e', 'm', 'z']
    >>> 'y' in set
    0
    >>> 'z' in set
    1
    >>> set.append('y')
    >>> set
    ['a', 'b', 'c', 'e', 'm', 'y', 'z']
    '''
    def __init__(self, *data):
        self.data = {}
        self.extend(data)
    def extend(self, data):
        '''Takes a sequence and adds each element of the sequence to the set.
        >>> set = Set()
        >>> set.extend((0, 42, 9, 42))
        >>> set
        [0, 9, 42]
        '''
        for datum in data:
            self.data[datum] = 1
    def __getitem__(self, item):
        return self.data.get(item, 0)
    def __contains__(self, item):
        return self.data.get(item, 0)
    def append(self, data):
        '''Takes one item and adds it to the set.
        >>> set = Set()
        >>> set.append('Betty')
        >>> set
        ['Betty']
        '''
        self.data[data] = 1
    def __repr__(self):
        k = self.data.keys()
        k.sort()
        return repr(k)


