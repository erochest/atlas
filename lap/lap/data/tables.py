

__version__ = '0.0'
__all__ = [
    'TableNames',
    'FieldDescriptions',
    'FieldLengths',
    ]


from lap.util import Data


TableNames = Data(
    PROJECTS='Projects',
    INFORMANTS='Informants',
    COMMUNITIES='Communities',
    WORKSHEETS='WorkSheets',
    FIELDWORKERS='FieldWorkers',
    TARGETS='Targets',
    RESPONSES='Responses',
    )


TABLEDEFS = {
    'Projects': (
        ('projid', 'integer primary key auto_increment'),
        ('name', 'varchar(10)'),
        ('long_name', 'varchar(100)'),
        ),
    'Informants': (
        ('infid', 'integer primary key auto_increment'),
        ('projid', 'integer'),
        ('comid', 'integer'),
        ('informid', 'varchar(10)'),
        ('oldnumber', 'varchar(10)'),
        ('auxiliary', 'char(1)'),
        ('fwid', 'integer'),
        ('wsid', 'integer'),
        ('yearinterviewed', 'year'),
        ('inftype', 'varchar(3)'),
        ('generation', 'char(1)'),
        ('cultivation', 'char(1)'),
        ('sex', 'char(1)'),
        ('age', 'integer'),
        ('education', 'char(1)'),
        ('occupation', 'char(1)'),
        ('race', 'char(1)'),
        ('latitude', 'float'),
        ('longitude', 'float'),
        ),
    'Communities': (
        ('comid', 'integer primary key auto_increment'),
        ('projid', 'integer'),
        ('type', 'char(1)'),
        ('name', 'varchar(30)'),
        ('state', 'char(2)'),
        ('code', 'varchar(10)'),
        ('x', 'integer'),
        ('y', 'integer'),
        ),
    'FieldWorkers': (
        ('fwid', 'integer primary key auto_increment'),
        ('projid', 'integer'),
        ('code', 'varchar(3)'),
        ('name', 'varchar(30)'),
        ),
    'WorkSheets': (
        ('wsid', 'integer primary key auto_increment'),
        ('projid', 'integer'),
        ('code', 'varchar(3)'),
        ('name', 'varchar(30)'),
        ),
    'Targets': (
        ('targetid', 'integer primary key auto_increment'),
        ('projid', 'integer'),
        ('target', 'varchar(50)'),
        ('type', 'char(1)'),
        ('page', 'integer'),
        ('subpage', 'varchar(1)'),
        ('item', 'integer'),
        ('subitem', 'varchar(1)'),
        ('notes', 'text'),
        ),
    'Responses': (
        ('responseid', 'integer primary key auto_increment'),
        ('projid', 'integer'),
        ('item', 'varchar(100)'),
        ('infid', 'integer'),
        ('gramflag', 'varchar(4)'),
        ('doubtflag', 'varchar(4)'),
        ('commenttext', 'blob'),
        ('commentcodes', 'varchar(50)'),
        ('phonetic', 'varchar(255)'),
        ('simplephone', 'varchar(255)'),
        ('targetid', 'integer'),
        ),
    }

INDEXDEFS = {
    'Informants': ( 'projid', 'comid', 'informid', 'fwid', 'wsid',
                    'yearinterviewed', 'inftype', 'generation', 'cultivation',
                    'sex', 'age', 'education', 'occupation', 'race', ),
    'Communities': ( 'projid', 'type', 'state', 'code', ),
    'Targets': ( 'projid', 'target', 'type', 'page', 'item', ),
    'Responses': ( 'projid', 'infid', 'gramflag', 'doubtflag', 'phonetic',
                   'simplephone', 'targetid', ),
    }

FieldDescriptions = {
    # INFORMANTS
    'Informants.infid': 'Informant ID Number',
    'Informants.informid': 'Informant ID',
    'Informants.oldnumber': 'Old Informant ID',
    'Informants.auxiliary': 'Auxiliary Informant',
    'Informants.yearinterviewed': 'Year Interviewed',
    'Informants.inftype': 'Type of Informant',
    'Informants.generation': 'Generation',
    'Informants.cultivation': 'Cultivated',
    'Informants.sex': 'Sex',
    'Informants.age': 'Age',
    'Informants.education': 'Education',
    'Informants.occupation': 'Occupation',
    'Informants.race': 'Race',
    'Informants.latitude': 'Latitude',
    'Informants.longitude': 'Longitude',
    # COMMUNITIES
    'Communities.comid': 'Community ID',
    'Communities.code': 'Community code',
    'Communities.type': 'Type of Community',
    'Communities.name': 'Community Name',
    'Communities.state': 'State',
    'Communities.x': 'X Location on Map (in Pixels)',
    'Communities.y': 'Y Location on Map (in Pixels)',
    # FIELDWORKERS
    'FieldWorkers.fwid': 'Field Worker ID',
    'FieldWorkers.code': 'Field Worker Code',
    'FieldWorkers.name': 'Field Worker',
    # WORKSHEETS
    'WorkSheets.wsid': 'Work Sheet ID',
    'WorkSheets.code': 'Work Sheet Code',
    'WorkSheets.name': 'Work Sheet',
    # TARGETS
    'Targets.targetid': 'Target ID',
    'Targets.target': 'Target Item',
    'Targets.type': 'Type of data',
    'Targets.page': 'Page',
    'Targets.subpage': 'Subpage',
    'Targets.item': 'Item Number',
    'Targets.subitem': 'Subitem Number',
    'Targets.notes': 'Notes',
    # RESPONSE
    'Responses.item': 'Item',
    'Responses.gramflag': 'Grammatical Category',
    'Responses.doubtflag': 'Doubtful Response',
    'Responses.commenttext': 'Long Comments',
    'Responses.commentcodes': 'Comment Codes',
    'Responses.phonetic': 'Phonetic Transcription',
    'Responses.simplephone': 'Simplified Phonetic Transcription',
    'Responses.responseid': 'Response ID',
    }

FieldLengths = {
    # INFORMANTS
    'Informants.infid': 5,
    'Informants.informid': 6,
    'Informants.oldnumber': 6,
    'Informants.auxiliary': 3,
    'Informants.yearinterviewed': 4,
    'Informants.inftype': 4,
    'Informants.generation': 3,
    'Informants.cultivation': 4,
    'Informants.sex': 3,
    'Informants.age': 3,
    'Informants.education': 2,
    'Informants.occupation': 3,
    'Informants.race': 4,
    'Informants.latitude': 16,
    'Informants.longitude': 16,
    # COMMUNITIES
    'Communities.comid': 5,
    'Communities.code': 6,
    'Communities.type': 4,
    'Communities.name': 10,
    'Communities.state': 2,
    'Communities.x': 4,
    'Communities.y': 4,
    # FIELDWORKERS
    'FieldWorkers.fwcode': 2,
    'FieldWorkers.name': 10,
    # WORKSHEETS
    'WorkSheets.wscode': 2,
    'WorkSheets.name': 10,
    # TARGETS
    'Targets.target': 10,
    'Targets.type': 1,
    'Targets.page': 4,
    'Targets.subpage': 4,
    'Targets.item': 4,
    'Targets.subitem': 4,
    'Targets.notes': 20,
    # RESPONSES
    'Responses.item': 20,
    'Responses.gramflag': 4,
    'Responses.doubtflag': 1,
    'Responses.commenttext': 20,
    'Responses.commentcodes': 20,
    'Responses.phonetic': 20,
    'Responses.simplephone': 20,
    'Responses.responseid': 6,
    }

