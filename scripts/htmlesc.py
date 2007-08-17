
"""\
usage: htmlesc.py [options] <filename> [<filename>...]

options:
    --input-encoding=ENCODING, -i ENCODING
        The encoding of the input files (defaults to "Latin-1").

    --help, -h
        Print this help page and exit.
"""

import fileinput, getopt, glob, sys

def main(input_encoding, filenames):
    current = None
    for line in fileinput.input(filenames, inplace=True, backup='.bk'):
        if fileinput.filename() != current:
            current = fileinput.filename()
            print >>sys.stderr, 'Processing', current

        line = unicode(line, input_encoding).rstrip()
        buffer = []
        for char in line:
            oc = ord(char)
            if oc > 127:
                buffer.append(u'&#x%04x;' % oc)
            else:
                buffer.append(char)
        line = u''.join(buffer)

        print str(line)

    print >>sys.stderr, 'Done!'

def error(msg='', code=1, f=sys.stderr):
    print >>f, __doc__
    print >>f, msg
    raise SystemExit(1)

def _main():
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'i:h',
                                     ['input-encoding=', 'help'])
    except getopt.GetoptError, e:
        error(e)
    input_encoding = 'latin-1'
    for (opt, value) in opts:
        if opt in ('-i', '--input-encoding'):
            input_encoding = value
        elif opt in ('-h', '--help'):
            error(code=0, f=sys.stdout)
    files = []
    for pattern in args:
        files += glob.glob(pattern)
    main(input_encoding, files)

if __name__ == '__main__':
    _main()

