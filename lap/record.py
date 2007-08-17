
"""

This is taken from a posting on comp.lang.python by Alex Martelli. Except for
some different nomenclature, (including of the data structure itself) it is
essentially unchanged. Records are similar to C structs or Pascal record types.

Here's how to use it::

    >>> class Point(Record):
    ...     x = 0.0
    ...     y = 0.0
    ...     color = 'gray'
    ...
    >>> q = Point()
    >>> print q
    Point()
    >>> p = Point(x=1.2, y=3.4)
    >>> print p
    Point(x=1.2, y=3.3999999999999999)

record is the metaclass; Record is the class to derive new records from.

"""


import warnings


class record(type):
    def __new__(cls, classname, bases, classdict):
        def __init__(self, **kw):
            for k in self.__dflts__: setattr(self, k, self.__dflts__[k])
            for k in kw: setattr(self, k, kw[k])

        def __repr__(self):
            keys = list(self.__dflts__)
            keys.sort()
            rep = [
                '%s=%r' % (k, getattr(self, k)) for k in keys
                if getattr(self, k) != self.__dflts__[k]
                ]
            return '%s(%s)' % (classname, ', '.join(rep))

        def __getstate__(self):
            return dict([
                (k, getattr(self, k)) for k in self.__dflts__
                if getattr(self, k) != self.__dflts__[k]
                ])

        def __setstate__(self, state):
            for k in self.__dflts__: setattr(self, k, self.__dflts__[k])
            for k in state: setattr(self, k, state[k])

        newdict = {
            '__slots__': [],
            '__dflts__': {},
            '__init__': __init__,
            '__repr__': __repr__,
            '__getstate__': __getstate__,
            '__setstate__': __setstate__,
            }

        for k in classdict:
            if k.startswith('__'):
                if k in newdict:
                    warnings.warn("Can't set attr %r in record %r" % (
                        k, classname))
                else:
                    newdict[k] = classdict[k]
            else:
                newdict['__slots__'].append(k)
                newdict['__dflts__'][k] = classdict[k]

        return type.__new__(cls, classname, bases, newdict)


class Record(object):
    __metaclass__ = record


def _test():
    import doctest, record
    return doctest.testmod(record)


if __name__ == '__main__':
    _test()

