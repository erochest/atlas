

'''Overwrites the table definitions in atlas.tables to make them more specific
to Jet tables. To use this, simply import it before anything else.

>>> import atlas.jet
>>> import atlas.tables
>>> atlas.tables.TableFields.INFORMANTS[0]
('infid', 'smallint', 'not null', 'primary key')
'''

import atlas.tables

class JetFields:
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
        ('notes', 'text'),
    )
    ITEM=(
        ('item', 'text'),
        ('infid', 'integer'),
        ('gramflag', 'integer'),
        ('doubtflag', 'integer'),
        ('comtext', 'text'),
        ('comments', 'text'),
        ('phonetic', 'text'),
        ('simplephone', 'text'),
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
        ('phonetic', 'text'),
        ('projectid', 'text'),
        ('itemid', 'integer'),
        ('page', 'integer'),
        ('subpage', 'text'),
        ('itemno', 'integer'),
        ('subitemno', 'text'),
    )

atlas.tables.TableFields = JetFields

