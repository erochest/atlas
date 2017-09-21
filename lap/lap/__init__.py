
"""
The 'lap' package.

This is the base package for the Linguistic Atlas Projects' code. It simply
defines a new logging level, "TRACE", and sets up the logging.

Constants:

    'TRACE' -- The trace logging level to pass to the 'logging' package's 'log'
    function.

"""


__all__ = [
    'data',
    'settings',
    'TRACE',
    'trace',
    'util',
    'web',
    ]


import logging


TRACE = 5
logging.addLevelName(TRACE, 'TRACE')
logging.basicConfig()


def trace(msg, *args, **kwargs):
    """
    Output trace-level logging information.

    This is a utility function like the 'logging' package's 'critical' and
    other functions.

    Parameters:

        'msg' -- The message to output.

        '*args' -- String formatting arguments to use with 'msg'.

        '**kwargs' -- String formatting arguments to use with 'msg'.

    """

    logging.getRootLogger().log(TRACE, msg, *args, **kwargs)

