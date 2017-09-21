
"""\
usage: update_old.py [options]

This program takes all the HTML files in the directory structure ROOTDIR
and turns them into jon.wt templates for use with the LAP site. This
involves:
    1. Turning absolute URLs into URLs using parameters. E.g.,
       "/cgi-bin/infprofile.pl" -> "$$basecgi$$/infprofile.pl"
       "/img/pixel.gif" -> "$$baseold$$/img/pixel.gif"

    2. Outputting the fixed HTML file as a *.tmpl file and creating a
       corresponding *.tmpl.py file in the ../wt directory.

options:
    --rootdir=ROOTDIR, -r ROOTDIR
        The name of the root directory of the old Atlas web site.

    --verbose, -v
        Enable progress reports.

    --debug, -d
        Enable debugging error handling.

    --help, -h
        Print this message.

"""

from __future__ import generators
import getopt, os, re, sys, mx.Tidy, xml.dom.minidom
from xml.sax.saxutils import escape, quoteattr

DOCTYPE = "<!doctype html public '-//W3C//DTD HTML 4.0 Transitional//EN'>"
CODE = '\n'.join((
    '',
    '',
    'from lap.web.templates import OldTemplate',
    '',
    'class main(OldTemplate):',
    '    pass',
    '',
    '',
    ))

VERBOSE = False
def report(str, *args):
    if VERBOSE:
        print str % args

class Task:
    def __str__(self):
        return self.__class__.__name__

    def __call__(self, arg):
        raise NotImplementedError('%s.__call__' % self.__class__.__name__)

class TaskProcessor(Task):
    def __init__(self, *tasks):
        self.tasks = tasks

    def __call__(self, arg):
        for task in self.tasks:
            #report('TASK: %s', task)
            arg = task(arg)
        return arg

class FileTask(Task):
    def __init__(self, mode='r'):
        self.mode = mode
    def __call__(self, filename):
        return file(filename, self.mode).read()

class RemoveTask(Task):
    def __init__(self, string):
        self.string = string
    def __call__(self, input):
        return input.replace(self.string, '')

class StripTask(Task):
    def __call__(self, input):
        return input.strip()

class TidyTask(Task):
    def __init__(self, **options):
        self.options = options

    def __call__(self, input):
        (nerrors, nwarnings, outputdata, errordata) = mx.Tidy.tidy(
            input,
            **self.options
            )
        report('\tTidied: %d errors, %d warnings', nerrors,nwarnings)
        if nerrors > 0:
            f = file('tidy-errors.txt', 'a')
            try:
                f.write('Tidy errors:\n')
                f.write(errordata)
                f.write('\n')
            finally:
                f.close()
        return outputdata

class DOMTask(Task):
    def __call__(self, string):
        report('\tParsing %r to DOM.', string[:15])
        try:
            return xml.dom.minidom.parseString(string)
        except:
            print >>sys.stderr, 'ERROR: Writing output to dom-error.xml'
            file('dom-error.xml', 'wc').write(string)
            raise

class Visitor:
    def visit(self, obj):
        raise NotImplementedError('%s.visit' % self.__class__.__name__)

class DOMVisitor:
    def __init__(self):
        self.result = None

    def visit(self, obj):
        nodeType = obj.nodeType
        if nodeType == obj.ELEMENT_NODE:
            self.visit_element(obj)
        elif nodeType == obj.ATTRIBUTE_NODE:
            self.visit_attribute(obj)
        elif nodeType == obj.TEXT_NODE:
            self.visit_text(obj)
        elif nodeType == obj.CDATA_SECTION_NODE:
            self.visit_cdata_section(obj)
        elif nodeType == obj.ENTITY_NODE:
            self.visit_entity(obj)
        elif nodeType == obj.PROCESSING_INSTRUCTION_NODE:
            self.visit_pi(obj)
        elif nodeType == obj.COMMENT_NODE:
            self.visit_comment(obj)
        elif nodeType == obj.DOCUMENT_NODE:
            self.visit_document(obj)
        elif nodeType == obj.DOCUMENT_TYPE_NODE:
            self.visit_doctype(obj)
        elif nodeType == obj.NOTATION_NODE:
            self.visit_notation(obj)

    def visit_element(self, obj): pass
    def visit_attribute(self, obj): pass
    def visit_text(self, obj): pass
    def visit_cdata_section(self, obj): pass
    def visit_entity(self, obj): pass
    def visit_pi(self, obj): pass
    def visit_comment(self, obj): pass
    def visit_document(self, obj): pass
    def visit_doctype(self, obj): pass
    def visit_notation(self, obj): pass

class ReplaceVisitor(DOMVisitor):
    attributes = ('BACKGROUND', 'HREF', 'SRC', 'USEMAP', 'CLASSID',
                  'CODEBASE', 'DATA', 'CITE', 'ACTION', 'LONGDESC', 'PROFILE',
                  'FOR', )

    def visit(self, obj):
        DOMVisitor.visit(self, obj)
        self.result = obj

    def _replace(self, node, attr):
        value = node.getAttribute(attr)
        if not value:
            return
        #report('\tVisiting attribute %r on %r', attr, node)
        if value.startswith(u'/cgi-bin/'):
            value = value.replace(u'/cgi-bin', u'$$basecgi$$')
        elif value.startswith(u'/'):
            value = u'$$baseold$$' + value
        elif value.startswith(u'infprofile.pl'):
            value = u'$$basecgi$$/' + value
        node.setAttribute(attr, value)

    def visit_element(self, obj):
        for attr in self.attributes:
            self._replace(obj, attr)
            #self._replace(obj, attr.lower())
        for child in obj.childNodes:
            self.visit(child)

    def visit_document(self, obj):
        self.visit(obj.documentElement)

class PrintVisitor(DOMVisitor):
    empty = ('BASEFONT', 'BR', 'AREA', 'LINK', 'IMG', 'PARAM', 'HR', 'INPUT',
             'COL', 'FRAME', 'ISINDEX', 'BASE', 'META', )

    def __init__(self, f=sys.stdout, encoding='latin1'):
        DOMVisitor.__init__(self)
        self.f = f
        self.encoding = encoding

    def attr_items(self, node):
        attributes = node.attributes
        keys = attributes.keys()
        keys.sort()
        while keys:
            key = keys.pop(0)
            attr = attributes[key]
            yield (attr.name, attr.value)
        raise StopIteration()

    def attrs(self, node):
        for i in range(node.attributes.length):
            yield node.attributes.item(i)
        StopIteration()

    def write(self, str):
        buffer = []
        for char in str:
            if ord(char) > 127:
                buffer.append(u'&#x%04x;' % ord(char))
            else:
                buffer.append(char)
        self.f.write(u''.join(buffer))

    def visit_element(self, obj):
        name = obj.tagName.lower()
        self.write(u'<%s' % name)
        for attr in self.attrs(obj):
            self.visit(attr)
        #for (attr, value) in self.attrs(obj):
        #    self.write(u' %s=%s' % (attr.lower(), quoteattr(value)))
        self.write(u'>')
        for child in obj.childNodes:
            self.visit(child)
        if obj.tagName not in self.empty:
            self.write(u'</%s>' % name)

    def visit_attribute(self, obj):
        self.write(u' %s=%s' % (obj.name.lower(), quoteattr(obj.value)))

    def visit_text(self, obj):
        self.write(escape(obj.data))

    def visit_cdata_section(self, obj):
        self.write(escape(obj))

    def visit_comment(self, obj):
        self.write(u'<!--%s-->' % obj.data)

    def visit_document(self, obj):
        self.visit(obj.documentElement)

class VisitorTask(Task):
    def __init__(self, visitor):
        self.visitor = visitor

    def __call__(self, obj):
        report('\tVisiting %s with %s', obj.__class__.__name__,
               self.visitor.__class__.__name__)
        self.visitor.visit(obj)
        return self.visitor.result

class TemplateTask(VisitorTask):
    def __init__(self, filename, visitor):
        self.filename = filename
        self.visitor = visitor

    def __call__(self, obj):
        report('\tWriting template to %r', self.filename)
        self.visitor.f = file(self.filename, 'wc')
        try:
            try:
                VisitorTask.__call__(self, obj)
            finally:
                self.visitor.f.close()
        except:
            raise
        else:
            return self.filename

class CodeTask(Task):
    def __init__(self, code, wtdir=r'wt'):
        self.code = code
        self.wtdir = wtdir

    def __call__(self, filename):
        filename = os.path.normpath(os.path.join(self.wtdir, filename))
        (path, fn) = os.path.split(filename)
        if not os.path.exists(path):
            os.makedirs(path)
        filename += '.py'
        report('\tWriting code to %r', filename)
        f = file(filename, 'wbc')
        try:
            f.write(self.code)
        finally:
            f.close()

class FileGatherTask(Task):
    def __call__(self, rootdir, ext):
        self.ext = ext
        self.filenames = []
        os.path.walk(rootdir, self.walk, None)
        return self.filenames

    def walk(self, arg, dirname, fnames):
        for filename in fnames:
            fullpath = os.path.join(dirname, filename)
            if (os.path.splitext(filename)[1] == self.ext and
                os.path.isfile(fullpath)):
                self.filenames.append(fullpath)

class UpdateTask(TaskProcessor):
    def __init__(self):
        self.tmpl = TemplateTask(None, PrintVisitor())
        self.tasks = (
            FileTask(),
            RemoveTask(DOCTYPE),
            StripTask(),
            TidyTask(numeric_entities=True, output_xml=True,
                     uppercase_attributes=True, uppercase_tags=True,
                     add_xml_decl=True),
            DOMTask(),
            VisitorTask(ReplaceVisitor()),
            self.tmpl,
            CodeTask(CODE),
            )

    def __call__(self, rootdir):
        files = FileGatherTask()
        for filename in files(rootdir, '.html'):
            (base, ext) = os.path.splitext(filename)
            self.tmpl.filename = base + '.tmpl'
            report('Updating %r', filename)
            TaskProcessor.__call__(self, filename)
        report('Done!')

def error(msg=None, code=1, f=sys.stderr):
    f.write(__doc__)
    if msg:
        f.write(str(msg))
        f.write('\n')
    raise SystemExit(code)


main = UpdateTask()

def _main():
    global VERBOSE
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'r:vdh',
                                     ('rootdir=', 'verbose', 'debug', 'help'))
    except getopt.error, e:
        error(e)
    if args:
        error('Invalid command line.')
    debug = False
    rootdir = None
    for (opt, value) in opts:
        if opt in ('--rootdir', '-r'):
            rootdir = value
        elif opt in ('--debug', '-d'):
            debug = True
        elif opt in ('--verbose', '-v'):
            VERBOSE = True
        elif opt in ('--help', '-h'):
            error(code=0, f=sys.stdout)
    if rootdir is None or not os.path.isdir(rootdir):
        error('Please specify a valid root directory.')
    try:
        main(rootdir)
    except Exception, e:
        if debug:
            raise
        else:
            error('ERROR (%s): %s' % (e.__class__.__name__, e))

if __name__ == '__main__':
    _main()

