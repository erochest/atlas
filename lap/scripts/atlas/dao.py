
'''This module provides some extra functions for manipulating Jet databases
using DAO. This should allow you to programmatically create, delete, and
compact databases.'''

from win32com.client import Dispatch, constants
import os

_dao = None

def getDao():
    global _dao
    if _dao is None:
        _dao = Dispatch('DAO.DBEngine.36')
    return _dao

def create(filename):
    filename = os.path.normpath(filename)
    path, base = os.path.split(filename)
    fn, ext = os.path.splitext(base.lower())
    if ext == '.mdb':
        dsn = os.path.join(path, fn+'.dsn')
    else:
        dsn = os.path.join(path, base+'.dsn')
    getDao().CreateDatabase(filename, constants.dbLangGeneral)
    f = open(dsn, 'wc')
    print >>f, r'[ODBC]'
    print >>f, r'DRIVER=Microsoft Access Driver (*.mdb)'
    print >>f, r'FIL=MS Access'
    print >>f, r'DriverId=25'
    print >>f, r'DefaultDir=%s' % path
    print >>f, r'DBQ=%s' % filename
    f.close()
    return dsn

def delete(filename):
    os.remove(filename)

def compact(oldfilename, newfilename):
    oldfilename = os.path.normpath(oldfilename)
    newfilename = os.path.normpath(newfilename)
    getDao().CompactDatabase(oldfilename, newfilename, constants.dbLangGeneral)

repair = compact

