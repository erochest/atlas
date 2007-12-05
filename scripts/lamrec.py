#!/usr/bin/env python


"""\
usage: %prog [options]
"""


from __future__ import with_statement

import atexit
import codecs
from contextlib import nested
import datetime
import logging
import optparse
import os
import sys
import tempfile
import time

import lamcour

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
from tkMessageBox import showinfo


__version__ = '$Revision:$'


DEBUG = True
ERROR_HANDLERS = ('replace', 'ignore', 'strict')

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


class DevNull(object):
    softspace = 0

    def write(self, text):
        pass


class FileBrowse(Frame):

    def __init__(self, master, get_filename):
        Frame.__init__(self, master)
        self.create_widgets()
        self.pack()
        self.get_filename = get_filename

    def get_path(self):
        return self.entry.get()
    def set_path(self, path):
        self.entry.delete(0, END)
        self.entry.insert(END, path)

    def create_widgets(self):
        self.browse = Button(self, text='Browse', command=self.on_browse)
        self.browse.pack(side=RIGHT)
        self.entry = Entry(self)
        self.entry.pack(side=RIGHT, expand=1, fill=BOTH)

    def on_browse(self):
        path = self.get_path()
        args = {'parent': self}
        if path:
            args['initialfile'] = path
        path = self.get_filename(**args)
        if path:
            self.set_path(path)


class Application(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        master = self.master
        Label(master, text='Input File').grid(row=0, column=0, sticky=N+W)
        self.input_entry = FileBrowse(master, askopenfilename)
        self.input_entry.grid(row=0, column=1, sticky=E+W)
        Label(master, text='Output File').grid(row=1, column=0, sticky=N+W)
        self.output_entry = FileBrowse(master, asksaveasfilename)
        self.output_entry.grid(row=1, column=1, sticky=E+W)
        Label(master, text='Errors').grid(row=2, column=0, sticky=N+W)
        self.error_handler = StringVar()
        self.error_handler.set('replace')
        frame = Frame(master)
        frame.grid(row=2, column=1, sticky=N+W)
        for text in ERROR_HANDLERS:
            rb = Radiobutton(frame, text=text.title(), variable=self.error_handler, value=text)
            rb.pack(side=TOP, anchor=W)
        frame = Frame(master)
        frame.grid(row=3, column=0, columnspan=2, sticky=N+E)
        button = Button(frame, text='Cancel', command=self.on_cancel, width=8)
        button.pack(side=RIGHT)
        button = Button(frame, text='OK', command=self.on_ok, width=8)
        button.pack(side=RIGHT)

    def on_ok(self):
        input_file = self.input_entry.get_path()
        output_file = self.output_entry.get_path()
        if input_file == output_file:
            fin = tempfile.TemporaryFile()
            with open(input_file, 'rb') as cp:
                fin.writelines(cp)
            fin.seek(0)
        else:
            fin = open(input_file, 'rb')
        errors = self.error_handler.get()
        fout = codecs.open(output_file, 'wb', 'utf-8', errors)
        with nested(fin, fout) as (fin, fout):
            fout.writelines( lamcour.decode(line, errors)[0] for line in fin )
        showinfo('Done', 'The file has been recoded.')

    def on_cancel(self):
        self.quit()


def setup_streams():
    if not DEBUG:
        sys.stderr = sys.stdout = DevNull()


def parse_args(argv):
    """\
    This parses the command-line arguments in argv and returns a tuple
    containing the options and other arguments.

    """

    op = optparse.OptionParser(usage=__doc__, version='%prog '+__version__)
    op.add_option('--log-dest', action='store', dest='log_file', default='STDOUT',
                  help='The name of the file to send log messages to. "STDOUT" will print to '
                       'the screen. Default=%default.')
    op.add_option('--log-level', action='store', dest='log_level', choices=LOG_LEVELS.keys(),
                  default='normal',
                  help='The level of logging information to output. Valid choices are '
                       '"quiet", "normal", and "verbose". Default="%default".')
    (opts, args) = op.parse_args(argv)
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
        root = Tk()
        app = Application(master=root)
        app.mainloop()
        logging.info('done')
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
    root.destroy()


if __name__ == '__main__':
    setup_streams()
    sys.exit(main())


