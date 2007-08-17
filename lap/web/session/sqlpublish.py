

from quixote.publish import SessionPublisher
from session import SqlSessionManager


class SqlSessionPublisher(SessionPublisher):
    """
    Override the __init__ function to set the session manager to the
    SqlSessionManager. This is necessary because the publishers are created by
    the SCGI server handler directly, and there is no other place to set the
    session manager.

    """

    def __init__(self, package, config=None):
        SessionPublisher.__init__(self, package, config=config)
        self.set_session_manager(SqlSessionManager())


