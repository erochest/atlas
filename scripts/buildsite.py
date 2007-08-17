#! /usr/bin/env python

'''\
usage: buildsite.py [-h|--help]

'''

from lap import settings
import os, sys
from jon import cgi, wt
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

if settings.meta.development:
    BaseHandler = wt.DebugHandler
else:
    BaseHandler = wt.Handler

class Request(cgi.CGIRequest):
    def __init__(self, handler_type, filename):
        self.filename = filename
        cgi.CGIRequest.__init__(self, handler_type)

    def output_headers(self):
        if self._doneHeaders:
            raise cgi.SequencingError('output_headers() called twice')
        self._doneHeaders = True

    def _init(self):
        (base, ext) = os.path.splitext(self.filename)
        output = os.path.join(settings.locale.htdocs, base+'.html')
        self.__out = file(output, 'wc')
        self.__err = sys.stderr
        self.environ = os.environ
        self.stdin = sys.stdin
        cgi.Request._init(self)

    def error(self, s):
        self.__err.write(s)

    def _write(self, s):
        if not self.aborted:
            self.__out.write(s)

    def _flush(self):
        if not self.aborted:
            self.__out.flush()

class Handler(BaseHandler):
    def _get_template(self):
        return os.path.join(settings.locale.htdocs, self.req.filename)

    def _get_code(self):
        return os.path.join(settings.locale.htdocs, 'wt',
                            self.req.filename+'.py')

    def _get_etc(self):
        return settings.locale.etc

def _accum_files(arg, dirname, names):
    names = [
        os.path.join(dirname, name)
        for name in names
        if os.path.splitext(name)[1] in arg['exts']
        ]
    names = [ name for name in names if os.path.isfile(name) ]
    arg['files'] += names

def accum_files(dirname, exts):
    # For recursive builds:
    arg = { 'exts': exts, 'files': [], }
    os.path.walk(dirname, _accum_files, arg)
    return arg['files']
    # For only handling the dirname directory (i.e., for testing):
    #import glob
    #files = []
    #for ext in exts:
    #    files += glob.glob(os.path.join(dirname, '*' + ext))
    #return files

def main(dirname, subdirs):
    os.chdir(dirname)
    if subdirs:
        files = []
        for sd in subdirs:
            files += accum_files(os.path.join('.', sd), {'.tmpl': True})
    else:
        files = accum_files('.', {'.tmpl': True})
    for filename in files:
        print >>sys.stderr, 'Processing', filename
        Request(Handler, filename).process()

if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print __doc__
        raise SystemExit(0)
    if len(sys.argv) > 1:
        subdirs = sys.argv[1:]
    else:
        subdirs = []
    main(settings.locale.htdocs, subdirs)

