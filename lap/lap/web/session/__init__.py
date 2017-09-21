

"""
This code is taken from Titus Brown's code published at:
    http://issola.caltech.edu/~t/transfer/sql_example/

With slight changes to formatting and naming.

"""


__version__ = '$Id:$'
__all__ = [
    'db',
    'session',
    'sqlpublish',
    'SqlSessionPublisher',
    'get_user_by_name',
    ]


from sqlpublish import SqlSessionPublisher
from db import get_user_by_name


