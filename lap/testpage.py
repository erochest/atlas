
'''usage: testpage.py [url]

url is the URL relative to http://localhost/lap .
'''

import imp, os, sys
from jon import cgi, wt

docbase = r'e:\atlas\www'
htdocs = os.path.join(docbase, 'htdocs')
etc = os.path.join(docbase, 'etc')

_code_cache = {}

class Handler(wt.DebugHandler):
    url = None

    def _get_template(self):
        return self.url

    def _get_etc(self):
        return etc

    def _get_code(self):
        (dirname, filename) = os.path.split(self.url)
        return os.path.join(dirname, 'wt', filename+'.py')

    def process(self, req):
        os.environ['WT_TEMPLATE_URL'] = self.url
        self.req = req
        self.template = self._get_template()
        self.etc = self._get_etc()
        codefname = self._get_code()
        try:
            namespace = _code_cache[codefname]
        except KeyError:
            #namespace = { "wt": wt }
            #code = compile(open(codefname, "rb").read(), codefname, "exec")
            #exec code in namespace
            #del code
            #if self.cache_code:
            #    _code_cache[codefname] = namespace
            (dirname, filename) = os.path.split(codefname)
            (filename, ext) = os.path.splitext(filename)
            info = imp.find_module(filename, [dirname])
            mod = imp.load_module('wtmod', *info)
        obj = getattr(mod, 'main')(None, self)
        self.pre_request(obj)
        if obj.template_as_file:
            obj.main(open(self.template, "rb"))
        else:
            obj.main(open(self.template, "rb").read())
        self.post_request(obj)

def main(url):
    filename = os.path.join(htdocs, url)
    Handler.url = filename
    cgi.CGIRequest(Handler).process()

if __name__ == '__main__':
    if '-h' in sys.argv or '--help' in sys.argv:
        print __doc__
        raise SystemExit(0)
    if len(sys.argv) != 2:
        print >>sys.stderr, __doc__
        raise SystemExit(1)
    main(sys.argv[1])

