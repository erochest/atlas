
"""\
usage: %prog [options] [data file] <[data file]...>

Checks all the data files on the command-line and makes sure that every line
has the correct number of items.
"""

import csv, glob, os, sys
from ericr import app

class ChkCsvApp(app.Application):
    USAGE = __doc__

    OPTIONS = (
        app.make_option('-c', '--count', action='store', type='int',
                        default=10, dest='count',
                        help='The count of items that should be on each line.'),
        app.make_option('-v', '--verbose', action='count', dest='verbose',
                        default=2, help='Request more status output.'),
        )

    def main(self):
        self.setLoggingLevelFromCount(self.opts.verbose)

        count = self.opts.count
        for pattern in self.args:
            for filename in glob.glob(pattern):
                if (os.path.basename(filename).startswith('_') or
                    not os.path.isfile(filename)):
                    continue
                self.info('Checking "%s"', filename)
                for (i, row) in enumerate(csv.reader(file(filename, 'rb'))):
                    if len(row) != count:
                        self.error('%s:%s:%s', filename, i, len(row))

        self.info('done')

if __name__ == '__main__':
    sys.exit(ChkCsvApp.run())

