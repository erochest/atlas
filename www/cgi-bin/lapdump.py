#! D:\Python23\python.exe
#!/usr/local/bin/python

import sys
sys.path.append('e:/atlas/lap')

from jon import cgi
from lap.web.templates.dump import DumpHandler

cgi.CGIRequest(DumpHandler).process()

