

__all__ = [
    'DEBUG',
    'DatabasePublisher',
    'get_publisher',
    ]


import quixote
from quixote.config import Config

from lap.web.db import connect
from lap.web.session import SqlSessionPublisher


DEBUG = True


class DatabasePublisher(SqlSessionPublisher):
    def __init__(self, package, config=None):
        SqlSessionPublisher.__init__(self, package, config=config)
        self.cxn = connect()

    def cleanup(self):
        self.cxn.close()

    def start_request(self):
        SqlSessionPublisher.start_request(self)
        quixote.get_request().cxn = self.cxn


def get_publisher():
    quixote.enable_ptl()
    from lap.web.site import root
    if DEBUG:
        config = Config(display_exceptions='html')
    else:
        config = None
    return DatabasePublisher(root.index(), config)


