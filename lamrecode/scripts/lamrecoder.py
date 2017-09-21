#!/usr/bin/env python


"""\
usage: %prog [options] [FILE|DIRECTORY] ...

This walks over the files and directories on the command line and recodes them
from lamcour to UTF-8.  """


from __future__ import with_statement

import atexit
import codecs
from collections import deque
from contextlib import nested
import datetime
import logging
import optparse
import os
import sys
import tempfile
import time

import lamcour


__version__ = '$Revision:$'


ERROR_HANDLERS = ('strict', 'replace', 'ignore')

LOG_FORMAT = (
    '%(asctime)s [%(levelname)s] %(name)s : %(message)s'
    )
LOG_LEVELS = {
    'very-quiet': logging.CRITICAL,
    'quiet': logging.WARNING,
    'normal': logging.INFO,
    'verbose': logging.DEBUG,
    }

if sys.platform == 'win32':
    timer = time.clock
else:
    timer = time.time


def lamrecode(inputs, in_place=False, error='replace'):
    inputs = deque( os.path.abspath(inp) for inp in inputs )
    while inputs:
        input = inputs.popleft()
        if os.path.isfile(input):
            logging.info(input)
            if in_place:
                fin = tempfile.TemporaryFile()
                with open(input, 'rb') as cp:
                    fin.writelines(cp)
                fin.seek(0)
                output = input
            else:
                fin = open(input, 'rb')
                output = input + '.utf8'
            fout = codecs.open(output, 'wb', 'utf-8', error)
            with nested(fin, fout) as (fin, fout):
                fout.writelines( lamcour.decode(line, error)[0] for line in fin )
        else:
            inputs.extend( os.path.join(input, fn) for fn in os.listdir(input) )


def parse_args(argv):
    """\
    This parses the command-line arguments in argv and returns a tuple
    containing the options and other arguments.

    """

    op = optparse.OptionParser(usage=__doc__, version='%prog '+__version__)
    op.add_option('-e', '--error', action='store', dest='error', choices=ERROR_HANDLERS,
                  default='replace',
                  help='Specify how to handle errors. Choices are "strict", "ignore", and '
                       '"replace". See http://docs.python.org/lib/string-methods.html, about the '
                       '"decode" method, for more information on the meaning of these. Default = '
                       '%default.')
    op.add_option('-i', '--in-place', action='store_true', dest='in_place',
                  help='Modify the files in place. Otherwise, the files are saved with the added '
                       'extension, ".utf8".')
    op.add_option('--log-dest', action='store', dest='log_file', default='STDOUT',
                  help='The name of the file to send log messages to. "STDOUT" will print to '
                       'the screen. Default=%default.')
    op.add_option('--log-level', action='store', dest='log_level', choices=LOG_LEVELS.keys(),
                  default='normal',
                  help='The level of logging information to output. Valid choices are '
                       '"quiet", "normal", and "verbose". Default="%default".')
    (opts, args) = op.parse_args(argv)
    if not args:
        op.error('You must specify one or more files or directories to process.')
    return (opts, args)


def setup_logging(opts):
    """\
    This sets up the logging system, based on the values in opts. Specifically,
    this looks for the log_file and log_level attributes on opts.

    """

    args = {}
    if opts.log_file == 'STDOUT':
        args['stream'] = sys.stdout
    else:
        args['filename'] = opts.log_file
    logging.basicConfig(
        level=LOG_LEVELS[opts.log_level],
        format=LOG_FORMAT,
        **args
        )
    atexit.register(logging.shutdown)


def main(argv=None):
    (opts, args) = parse_args(argv or sys.argv[1:])
    setup_logging(opts)
    try:
        start = timer()
        lamrecode(args, opts.in_place, opts.error)
        end = timer()
        logging.info('done')
        logging.info('elapsed time: %s', datetime.timedelta(seconds=end-start))
    except SystemExit:
        return 0
    except KeyboardInterrupt:
        logging.warning('KeyboardInterrupt')
        return 2
    except:
        logging.exception('ERROR')
        return 1
    else:
        return 0


if __name__ == '__main__':
    sys.exit(main())


