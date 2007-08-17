#!D:/Python23/python.exe
#!/usr/local/bin/python

# For some reason these aren't getting passed through correctly w/fcgi,
# so I'm setting them here, even for cgi.
import os, sys
#sys.path.append('/mnt/mydocs/atlas/lap')
sys.path.append('e:/atlas/lap')
os.environ['ATLASSITE_TARGET'] = 'DEVEL'

from jon import modpy
from lap.web.handlers import Handler

def handler(modpy_req):
    return modpy.Request(Handler).process(modpy_req)

