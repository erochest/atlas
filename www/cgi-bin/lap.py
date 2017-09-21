#!/usr/bin/env python2.4


from quixote.server.cgi_server import run

from lap.web.publish import get_publisher


if __name__ == '__main__':
    run(get_publisher)

