#! /usr/bin/env python

"""\
usage: bs.py [options]

options:

    -t TARGET, --target=TARGET
        the value for the ATLASSITE_TARGET environment variable (defaults to
        "DEVEL").

    -d DIRECTORY, --dir=DIRECTORY
        The subdirectory to process (defaults to all subdirectories).

    -h, --help
        print this screen

"""

import getopt, os, sys

BUILDSITE = 'scripts/buildsite.py'

def main(target, directory):
    """
    Build the atlas site.

    This runs the script %r with 'PYTHONPATH' set to the current directory and
    the target and base directory set.

    Parameters:

        'target' -- The value for the environment variable 'ATLASSITE_TARGET'.
        This should be one of 'DEVEL', 'DEVEL_TEST', 'DEPLOY_TEST', or
        'DEPLOY'.

        'directory' -- The base directory for the atlas site.

    """ % BUILDSITE

    cmd = [
        'PYTHONPATH=%s' % os.getcwd(),
        'ATLASSITE_TARGET=%s' % target,
        sys.executable,
        BUILDSITE,
        directory,
        ]
    cmd = ' '.join(cmd)
    print 'Running', repr(cmd)
    os.system(cmd)

def _main():
    """Parse command-line arguements and call 'main'."""
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 't:d:h',
                                     ['target=', 'dir=', 'help'])
    except getopt.GetoptError, e:
        print >>sys.stderr, __doc__
        print >>sys.stderr, e
        raise SystemExit(1)

    target = 'DEVEL'
    directory = ''
    for (opt, value) in opts:
        if opt in ('-t', '--target'):
            target = value
        elif opt in ('-d', '--dir'):
            directory = value
        elif opt in ('-h', '--help'):
            print __doc__
            raise SystemExit(0)

    main(target, directory)

if __name__ == '__main__':
    _main()

