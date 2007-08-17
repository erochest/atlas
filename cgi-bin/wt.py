#! D:\Python23\python.exe
#!/usr/local/bin/python

# For some reason these aren't getting passed through correctly w/fcgi,
# so I'm setting them here, even for cgi.
import os, sys
#sys.path.append('/mnt/mydocs/atlas/lap')
sys.path.append('e:/atlas/lap')
os.environ['ATLASSITE_TARGET'] = 'DEVEL'

from jon import cgi
from lap.web.handlers import Handler

# the magical incantation necessary to output images
if sys.platform == 'win32':
    import msvcrt
    msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)

cgi.CGIRequest(Handler).process()

