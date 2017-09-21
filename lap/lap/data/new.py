
"""
This takes the data from the data files and integrates them into the data
stored in the data directory. The information from the table file is necessary
to extract the items from the files. All data files use CSV.

Table File
==========

This contains these fields, which are exactly the same as those in the
"_tables_" file in the data directory:

    target, filename, type, page, subpage, item, subitem, notes

For table files, however, the "filename" field is the name of the file the data
is being import *from*.

Data Directory
==============

Here is where the data will go. It must also contain a file named "_tables_",
which contains information about the data tables. The tables created from the
new data will be added to this file, which has these fields:

    target, filename, type, page, subpage, item, subitem, notes

Here, the "filename" field refers to the name of the file the data is being
imported *to*. However, the system assigns this name, based on the value of
"target."

Data Files
==========

These contain the data to be integrated. The fields in these are those used by
the Atlas Editor application:

    response, informant id, old informant id, grammar flag, doubt flag,
        textual comments, comment codes, phonetic item, project label,
        serial number, item, page

"""


import copy
import csv
import logging
import re
import sys
import warnings

from lap.record import Record
from lap.util import Data


# constants
TABLE_FILE = '_tables_'


# the fields -- a convenient holder for the data contained herein
Fields = Data(
    table=( 'target', 'filename', 'type', 'page', 'subpage', 'item',
            'subitem', 'notes', ),
    data=( 'response', 'informantId', 'oldId', 'grammarFlag', 'doubtFlag',
           'textComments', 'commentCodes', 'phonetics', 'project',
           'serial', ),
    edit=( 'response', 'informantId', 'oldId', 'grammarFlag', 'doubtFlag',
           'textComments', 'commentCodes', 'phonetics', 'project', 'serial',
           'item', 'page', ),
    )


# struct classes
class Table(Record):
    target = None
    filename = None
    type = 'p'
    page = None
    subpage = ''
    item = None
    subitem = ''
    notes = ''


class Data(Record):
    response = None
    informantId = None
    oldId = None
    grammarFlag = ''
    doubtFlag = 'N'
    textComments = ''
    commentCodes = ''
    phonetics = None
    project = None
    serial = None


class Edit(Record):
    response = None
    informantId = None
    oldId = None
    grammarFlag = ''
    doubtFlag = 'N'
    textComments = ''
    commentCodes = ''
    phonetics = None
    project = None
    serial = None
    item = None
    page = None


class NewInfo(Record):
    file = None
    writer = None
    table = None


class BaseReader(csv.DictReader):
    def __init__(self, csvfile, **kwargs):
        kwargs.setdefault('fieldnames', self._fields)
        csv.DictReader.__init__(self, **kwargs)

    def next(self):
        data = csv.DictReader.next(self)
        return self._cls(data)


class BaseWriter(csv.DictWriter):
    def __init__(self, csvfile, **kwargs):
        kwargs.setdefault('fieldnames', self._fields)
        csv.DictWriter.__init__(self, **kwargs)

    def _get_state(self, row):
        try:
            state = row.__getstate__
        except AttributeError:
            state = lambda: row
        return state()

    def writerow(self, row):
        csv.DictWriter.writerow(self, self._get_state(row))

    def writerows(self, rows):
        rows = ( self._get_state(row) for row in rows )
        csv.DictWriter.writerows(self, rows)


# reader/writer for the table file
class TableReader(BaseReader):
    _cls = Table
    _fields = Fields.table


class TableWriter(BaseWriter):
    _fields = Fields.table


# reader/writer for the final data files found in data directory
class DataReader(BaseReader):
    _cls = Data
    _fields = Fields.data


class DataWriter(BaseWriter):
    _fields = Fields.data

    def __init__(self, csvfile):
        BaseWriter.__init__(self, csvfile, extrasaction='ignore')


# reader/writer for the new data files from the Atlas Editor
class EditReader(BaseReader):
    _cls = Edit
    _fields = Fields.edit


class EditWriter(BaseWriter):
    _fields = Fields.edit


# misc functions
def clean_target(target, regex=re.compile(r'\W')):
    """ Return the target "cleaned" so as to make a file name. """
    return regex.sub('_', target) + '_'


# load various data
def load_tables(table):
    """ Load data from a tables file. """
    table_data = {}
    for item in TableReader(open(table)):
        if item.filename not in table_data:
            table_data[item.filename] = {}
        key = (item.page, item.subpage, item.item, item.subitem)
        table_data[item.filename][key] = item
    return table_data


def new_data(tables, directory, files):
    """ The entry function for this module. """
    table_data = load_table(tables)
    new_tables = {}
    for filename in files:
        logging.info('Reading %s', filename)
        file_table = table_data[os.path.basename(filename)]
        for row in EditReader(open(filename)):
            key = (row.page, row.subpage, row.item, row.subitem)
            assert key in file_index, \
                'No index entry for page %s%s, item %s%s.' % key
            table = file_table[key]
            data_filename = clean_target(table.target)
            if data_filename not in new_tables:
                logging.info('Opening %s', data_filename)
                new_table = copy.copy(table)
                new_table.filename = data_filename
                f = open(os.path.join(directory, data_filename), 'wc')
                new_tables[data_filename] = NewInfo(
                    file=f,
                    writer=DataWriter(f),
                    table=new_table,
                    )
            new_tables[data_filename].writer.writerow(row)
    logging.info('Appending to %s', TABLE_FILE)
    table_writer = TableWriter(open(os.path.join(directory, TABLE_FILE), 'a'))
    while new_tables:
        (key, info) = new_tables.popitem()
        table_writer.writerow(info.table)
        info.file.close()
    logging.info('Finished merging new data.')


# command-line ui functions
def parse_args():
    """ Parse the command-line options. """
    import optparse
    parser = optparse.OptionParser(usage=__doc__)
    parser.add_option('-i', '--index', action='store', type='string',
                      dest='index', default=None,
                      help='The file containing information about the new '
                           'data files.')
    parser.add_option('-d', '--directory', action='store', type='string',
                      dest='directory', default=None,
                      help='The directory containing the final data files.')
    parser.add_option('-e', '--extended-help', action='store_true',
                      dest='extended_help', default=False,
                      help='Display extended help information, then exit.')
    parser.add_option('-v', '--verbose', action='store_true',
                      dest='verbose', default=False,
                      help='Display status messages.')
    return parser(sys.argv[1:])


def check_options(opts):
    """ Check the command-line arguments. """
    if opts.extended_help:
        print __doc__
        raise SystemExit(0)
    if not os.path.exists(opts.index):
        print >>sys.stderr, 'The index file', opts.index, 'does not exist.'
        raise SystemExit(1)
    if not os.path.exists(os.path.join(opts.directory, TABLE_FILE)):
        print >>sys.stderr, 'The table file', \
            os.path.join(opts.directory, TABLE_FILE), 'does not exist.'
        raise SystemExit(1)


def get_filenames(patterns):
    """ Expaned the glob patterns into a list of file names. """
    import glob
    files = []
    for pattern in patterns:
        files += glob.glob(pattern)
    return files


def check_filenames(files):
    """ Verify the list of input file names. """
    if not files:
        print >>sys.stderr, 'Please specify one or more data files to import.'
        raise SystemExit(1)
    for filename in files:
        if not os.path.exists(filename):
            print >>sys.stderr, filename, 'does not exist.'
            raise SystemExit(1)


def config_logging(verbose=False):
    """ Configure the logging system. """
    logging.basicConfig()
    logger = logging.getLogger()
    if verbose:
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.WARNING)


def main():
    """ The command-line interface to this module. """
    (opts, args) = parse_args()
    check_options(opts)
    files = get_filenames(args)
    check_filenames(files)
    config_logging(opts.verbose)
    try:
        new_data(index=opts.index, directory=opts.directory, files=files)
    finally:
        logging.shutdown()


if __name__ == '__main__':
    main()

