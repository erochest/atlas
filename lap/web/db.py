

__all__ = [
    'connect',
    ]


import MySQLdb
import MySQLdb.cursors

from lap import settings


def connect():
    return MySQLdb.connect(
        cursorclass=MySQLdb.cursors.DictCursor,
        **settings.locale.connect
        )


