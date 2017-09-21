
'''This modules provides enumerations of and definitions for the tables used
in Lingusitic Atlas databases.
escTable escapes a string to make it an easy-to-use table name;
asTable escapes a table name for WHERE clauses;
TableNames is a struct containing the names of the database tables;
TableFields is a struct containing field specifications for each table;
FieldDescriptions is a dictionary containing long descriptions of the
    fields;
FieldLenthds is a dictionary containing the approximate maximum length of
    fields for display purposes; and
FieldTables is a dictionary mapping fields to the primary tables.
'''


__all__ = [
    'escTable',
    'asTable',
    'TableNames',
    'TableFields',
    'FieldDescriptions',
    'FieldLengths',
]

import re as _re
from atlas.utils import bool as _bool
from atlas.utils import toInt as _toInt

def escTable(itemname, esc='_', sub=_re.compile(r'\W').sub):
    '''Returns the name with all the non-alpha-numeric characters changed to
    underscores. For example,

    >>> escTable("Today\'s the best day of my life!")
    'Today_s_the_best_day_of_my_life_'
    '''
    return sub(esc, itemname) + '_'

def asTable(tablename):

    '''Returns a version of the tablename that is safe for Access (and
    maybe other databases) to use in WHERE clauses.
    >>> asTable('_informants_')
    'informants_'
    '''
    if tablename[0] == '_':
        return tablename[1:]
    else:
        return tablename

class TableNames:
    INFORMANTS = '_informants_'
    COMMUNITIES = '_communities_'
    WORKSHEETS = '_worksheets_'
    FIELDWORKERS = '_fieldworkers_'
    TABLES = '_tables_'
    PAGE = '_page%03d_'

class TableFields:
    INFORMANTS = (
        ('infid', 'integer'),
        ('comid', 'integer'),
        ('informid', 'text'),
        ('oldnumber', 'text'),
        ('auxiliary', 'integer'),
        ('fwid', 'integer'),
        ('wsid', 'integer'),
        ('yearint', 'integer'),
        ('inftype', 'integer'),
        ('generation', 'integer'),
        ('cultivation', 'integer'),
        ('sex', 'integer'),
        ('age', 'integer'),
        ('education', 'integer'),
        ('occupation', 'integer'),
        ('race', 'integer'),
        ('latitude', 'float'),
        ('longitude', 'float'),
    )
    COMMUNITIES=(
        ('comid', 'integer'),
        ('comtype', 'integer'),
        ('comname', 'text'),
        ('state', 'text'),
        ('comcode', 'text'),
        ('x', 'integer'),
        ('y', 'integer'),
    )
    FIELDWORKERS=(
        ('fwid', 'integer'),
        ('fwcode', 'text'),
        ('fwname', 'text'),
    )
    WORKSHEETS=(
        ('wsid', 'integer'),
        ('wscode', 'text'),
        ('wsname', 'text'),
    )
    TABLES=(
        ('itemname', 'text'),
        ('tablename', 'text'),
        ('tabletype', 'integer'),
        ('page', 'integer'),
        ('subpage', 'text'),
        ('itemno', 'integer'),
        ('subitemno', 'text'),
        ('notes', 'blob'),
    )
    ITEM=(
        ('item', 'text'),
        ('infid', 'integer'),
        ('gramflag', 'integer'),
        ('doubtflag', 'integer'),
        ('comtext', 'text'),
        ('comments', 'text'),
        ('phonetic', 'blob'),
        ('simplephone', 'blob'),
        ('projectid', 'text'),
        ('itemid', 'integer'),
    )
    PAGE=(
        ('item', 'text'),
        ('infid', 'integer'),
        ('gramflag', 'integer'),
        ('doubtflag', 'integer'),
        ('comtext', 'text'),
        ('comments', 'text'),
        ('phonetic', 'blob'),
        ('projectid', 'text'),
        ('itemid', 'integer'),
        ('page', 'integer'),
        ('subpage', 'text'),
        ('itemno', 'integer'),
        ('subitemno', 'text'),
    )

FieldDescriptions = {
    # INFORMANTS
    'infid': 'Informant ID Number',
    'informid': 'Informant ID',
    'oldnumber': 'Old Informant ID',
    'auxiliary': 'Auxiliary Informant',
    'yearint': 'Year Interviewed',
    'inftype': 'Type of Informant',
    'generation': 'Generation',
    'cultivation': 'Cultivated',
    'sex': 'Sex',
    'age': 'Age',
    'education': 'Education',
    'occupation': 'Occupation',
    'race': 'Race',
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    # COMMUNITIES
    'comid': 'Community ID',
    'comcode': 'Community code',
    'comtype': 'Type of Community',
    'comname': 'Community Name',
    'state': 'State',
    'x': 'X Location on Map (in Pixels)',
    'y': 'Y Location on Map (in Pixels)',
    # FIELDWORKERS
    'fwid': 'Field Worker ID',
    'fwcode': 'Field Worker Code',
    'fwname': 'Field Worker',
    # WORKSHEETS
    'wsid': 'Work Sheet ID',
    'wscode': 'Work Sheet Code',
    'wsname': 'Work Sheet',
    # TABLES
    'itemname': 'Item',
    'tablename': 'Database Table',
    'tabletype': 'Type of data',
    'page': 'Page',
    'subpage': 'Subpage',
    'itemno': 'Item Number',
    'subitemno': 'Subitem Number',
    'notes': 'Notes',
    # ITEM
    'item': 'Item',
    'gramflag': 'Grammatical Category',
    'doubtflag': 'Doubtful Response',
    'comments': 'Comment Codes',
    'comtext': 'Long Comments',
    'phonetic': 'Phonetic Transcription',
    'simplephone': 'Simplified Phonetic Transcription',
    'projectid': 'Project ID',
    'itemid': 'Item ID',
}

FieldLengths = {
    # INFORMANTS
    'infid': 5,
    'informid': 6,
    'oldnumber': 6,
    'auxiliary': 3,
    'yearint': 4,
    'inftype': 4,
    'generation': 3,
    'cultivation': 4,
    'sex': 3,
    'age': 3,
    'education': 2,
    'occupation': 3,
    'race': 4,
    'latitude': 8,
    'longitude': 8,
    # COMMUNITIES
    'comid': 5,
    'comcode': 6,
    'comtype': 4,
    'comname': 10,
    'state': 2,
    'x': 4,
    'y': 4,
    # FIELDWORKERS
    'fwcode': 2,
    'fwname': 10,
    # WORKSHEETS
    'wscode': 2,
    'wsname': 10,
    # TABLES
    'itemname': 10,
    'tablename': 10,
    'tabletype': 1,
    'page': 4,
    'subpage': 4,
    'itemno': 4,
    'subitemno': 4,
    'notes': 20,
    # ITEM
    'item': 20,
    'gramflag': 4,
    'doubtflag': 1,
    'comments': 20,
    'comtext': 20,
    'phonetic': 20,
    'simplephone': 20,
    'projectid': 4,
    'itemid': 6,
}

FieldTables = {
    'infid': 'INFORMANTS',
    'informid': 'INFORMANTS',
    'oldnumber': 'INFORMANTS',
    'auxiliary': 'INFORMANTS',
    'yearint': 'INFORMANTS',
    'inftype': 'INFORMANTS',
    'generation': 'INFORMANTS',
    'cultivation': 'INFORMANTS',
    'sex': 'INFORMANTS',
    'age': 'INFORMANTS',
    'education': 'INFORMANTS',
    'occupation': 'INFORMANTS',
    'race': 'INFORMANTS',
    'latitude': 'INFORMANTS',
    'longitude': 'INFORMANTS',

    'comid': 'COMMUNITIES',
    'comcode': 'COMMUNITIES',
    'comtype': 'COMMUNITIES',
    'comname': 'COMMUNITIES',
    'state': 'COMMUNITIES',
    'x': 'COMMUNITIES',
    'y': 'COMMUNITIES',

    'fwid': 'FIELDWORKERS',
    'fwcode': 'FIELDWORKERS',
    'fwname': 'FIELDWORKERS',

    'wsid': 'WORKSHEETS',
    'wscode': 'WORKSHEETS',
    'wsname': 'WORKSHEETS',

    'itemname': 'TABLES',
    'tablename': 'TABLES',
    'tabletype': 'TABLES',
    'page': 'TABLES',
    'subpage': 'TABLES',
    'itemno': 'TABLES',
    'subitemno': 'TABLES',
    'notes': 'TABLES',

    'item': 'ITEM',
    'gramflag': 'ITEM',
    'doubtflag': 'ITEM',
    'comments': 'ITEM',
    'comtext': 'ITEM',
    'phonetic': 'ITEM',
    'simplephone': 'ITEM',
    'projectid': 'ITEM',
    'itemid': 'ITEM',
    }

