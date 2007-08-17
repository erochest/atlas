#! /usr/bin/env python

"""\
usage: python shbang.py [-h|--help] [<directory>]

This steps through all the *.py files in the directory (or the current
directory if none is specified). If the first line of the file is a sh-bang
line (i.e., it begins with "#!"), it is replaced with a sh-bang line pointing
to the current Python executable.
"""

import fileinput, getopt, glob, os, sys

def main(argv=None):
    # argument handling
    if argv is None: argv = sys.argv
    try:
        (opts, args) = getopt.getopt(argv[1:], 'h', ['help'])
    except getopt.error, e:
        print >>sys.stderr, __doc__
        print >>sys.stderr, e
        raise SystemExit(1)

    for (opt, value) in opts:
        if opt in ('-h', '--help'):
            print __doc__
            raise SystemExit(0)

    if not args: args = [os.getcwd()]

    if len(args) != 1:
        print >>sys.stderr, __doc__
        print >>sys.stderr, 'Please specify only one directory.'
        raise SystemExit(1)

    # change a list of one directory name to a list of the python files
    # in that directory.
    args = glob.glob(os.path.join(args[0], '*.py'))

    # finally, iterate over the files
    for line in fileinput.input(args, inplace=True, backup='~'):
        if fileinput.isfirstline() and line.startswith('#!'):
            print >>sys.stderr, 'Processing:', fileinput.filename()
            print '#!', sys.executable
        else:
            print line.rstrip()

if __name__ == '__main__':
    main()
