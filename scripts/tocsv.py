
"""\
usage: %prog [options] [data file] <[data file]...>

This reads in all the data files using fcsv and writes them back out using the
now-standard csv.
"""

import csv, fcsv, glob, os, sys
from ericr import app

class ToCsvApp(app.Application):
    USAGE = __doc__

    OPTIONS = (
        app.make_option('-v', '--verbose', action='count', dest='verbose',
                        default=2, help='Request more status output.'),
        )

    def main(self):
        self.setLoggingLevelFromCount(self.opts.verbose)

        for pattern in self.args:
            for filename in glob.glob(pattern):
                if os.path.isfile(filename):
                    self.info('Processing "%s"', filename)
                    self.convert(filename)

        self.info('done')

    def convert(filename):
        # read in the data
        f = file(filename)
        data = [ fcsv.split(line) for line in f ]
        f.close()

        # write it back out
        f = file(filename, 'wb')
        csv.writer(f).writerows(data)
        f.close()

    convert = staticmethod(convert)


if __name__ == '__main__':
    sys.exit(ToCsvApp.run())

