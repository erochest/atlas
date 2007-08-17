

"""
Session-handling code.

This code maps the session dictionary to an SQL table. It should be safe to use
with any of the Quixote connection methods; in particular, it should properly
handle multiple Quixote instances running off of the same database.

"""


import random
import string
import time

from quixote import get_session_manager
from quixote.session import SessionManager
from quixote.session import Session as QuixoteSession

import db


KEYLEN = 20
KEYSEQ = xrange(KEYLEN)


class SqlQuixoteSession(object, QuixoteSession):

    def __init__(self, id):
        QuixoteSession.__init__(self, id)
        self._dirty = False

    def get_user(self):
        if not self.user:
            username = ''.join([
                random.choice(string.printable) for i in KEYSEQ
                ])
            self.set_user(db.get_user_by_name(username, True))
        return self.user

    def set_dirty(self, dirty=True):
        self._dirty = dirty

    def set_user(self, user):
        """
        Set the user! The change in user will be detected by Quixote through
        the 'is_dirty' function and saved accordingly.

        """

        if not self.user or user.id != self.user.id:
            self._dirty = True
        self.user = user

    def has_info(self):
        """Is this session worthy of storage? """
        return self.user

    def is_dirty(self):
        """
        Check to see if this session needs to be stored again, e.g., if the
        user has changed.

        """

        return self._dirty

    def _set_access_time(self, resolution):
        if self._access_time is None:
            self._access_time = time.time()
        QuixoteSession._set_access_time(self, resolution)
        self._dirty = True


class SqlTableMap:
    """Intercept dictionary requests and channel them to the SQL database. """

    def __init__(self, cxn):
        """Store the database connection. """
        self.cxn = cxn
        self.uncommitted = {}

    def get_cxn(self):
        """Return the database connection after doing a rollback. """
        cxn = self.cxn
        cxn.rollback()
        return cxn

    def keys(self):
        """Get a list of the session IDs in the database. """
        c = self.get_cxn().cursor()
        c.execute('SELECT session_id FROM user_sessions')
        return [ id for (id,) in c.fetchall() ]

    def values(self):
        """Load all of the sessions in the database. """
        c = self.get_cxn().cursor()
        c.execute('''
            SELECT user_id, session_id, remote_addr, creation_time, access_time
            FROM user_sessions
            ''')
        return [ self._create_from_db(*row) for row in c.fetchall() ]

    def items(self):
        """Get a list of the (key, value) pairs in the database. """
        d = {}
        for v in self.values():
            d[v.id] = v
        return d

    def get(self, session_id, default=None):
        """Get the given item from the database. """
        c = self.get_cxn().cursor()
        c.execute('''
            SELECT user_id, session_id, remote_addr, creation_time, access_time
            FROM user_sessions
            WHERE session_id=%s
            ''',
            (session_id,),
            )
        assert c.rowcount <= 1
        if c.rowcount == 1:
            row = c.fetchone()
            return self._create_from_db(*row)
        else:
            return default

    def __getitem__(self, session_id):
        """Get the given session from the database. """
        return self.get(session_id)

    def has_key(self, session_id):
        """Does this session exist in the database? """
        return self.get(session_id) is not None
    __contains__ = has_key

    def __setitem__(self, session_id, session):
        """Store the given session in the database. """
        self.uncommitted[session_id] = session

    def __delitem__(self, session_id):
        """Delete the given session from the database. """
        if session_id:
            if session_id in self.uncommitted:
                del self.uncommitted[session_id]
            cxn = self.get_cxn()
            c = cxn.cursor()
            c.execute('''
                    DELETE FROM user_sessions WHERE session_id=%s
                ''',
                (session_id,),
                )
            cxn.commit()

    def _save_to_db(self, session):
        """Save a given session to the database. """
        cxn = self.get_cxn()
        c = cxn.cursor()
        del self[session.id]
        c.execute('''
            INSERT INTO user_sessions
                (user_id, session_id, remote_addr, creation_time, access_time)
                VALUES (%s, %s, %s, %s, %s)
            ''',
            ( session.user.id, session.id, session.get_remote_address(),
              session.get_creation_time(), session.get_access_time(), ),
            )
        db.save_user(c, session.user)
        cxn.commit()

    def _create_from_db(self, uid, sid, addr, ctime, atime):
        """
        Create a new session from database data.

        This goes through the new-style object function __new__ rather than
        through the __init__ function.

        """

        session = SqlQuixoteSession.__new__(SqlQuixoteSession)
        session.id = sid
        session.user = db.get_user_by_id(uid)
        session._remote_address = addr
        if ctime is None:
            session._creation_time = time.time()
        else:
            session._creation_time = ctime.ticks()
        if atime is None:
            session._access_time = time.time()
        else:
            session._access_time = atime.ticks()
        return session

    def _abort_uncommitted(self, session):
        """Toss a session without committing any changes. """
        if session.id in self.uncommitted:
            del self.uncommitted[session.id]


class SqlSessionManager(SessionManager):
    """
    A session manager that uses the SqlTableMap to map sessions in an SQL
    database.

    """

    def __init__(self):
        cxn = db.get_cxn()
        SessionManager.__init__(self, SqlQuixoteSession, SqlTableMap(cxn))

    def abort_changes(self, session):
        if session:
            self.sessions._abort_uncommitted(session)

    def commit_changes(self, session):
        if session and session.has_info():
            self.sessions._save_to_db(session)


