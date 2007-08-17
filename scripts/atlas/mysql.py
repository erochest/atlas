
'''Overwrites the table definitions in atlas.tables to make them more
specific to MySQL tables. To use this, simply import it before
anything else.

>>> import atlas.mysql
>>> import atlas.tables
>>> atlas.tables.TableFields.INFORMANTS[0]
('infid', 'smallint', 'not null', 'primary key')
'''

import atlas.tables

class MySQLFields:
    INFORMANTS = (
        ('infid', 'smallint', 'not null', 'primary key'),
        ('comid', 'smallint', 'not null'),
        ('informid', 'tinytext', 'not null'),
        ('oldnumber', 'tinytext', 'not null'),
        ('auxiliary', 'tinyint', 'not null'),
        ('fwid', 'tinyint', 'not null'),
        ('wsid', 'tinyint', 'not null'),
        ('yearint', 'year', 'not null'),
        ('inftype', 'tinyint', 'not null'),
        ('generation', 'tinyint', 'not null'),
        ('cultivation', 'tinyint', 'not null'),
        ('sex', 'tinyint', 'not null'),
        ('age', 'tinyint', 'not null'),
        ('education', 'tinyint', 'not null'),
        ('occupation', 'tinyint', 'not null'),
        ('race', 'tinyint', 'not null'),
        ('latitude', 'float', 'not null'),
        ('longitude', 'float', 'not null'),
    )
    COMMUNITIES=(
        ('comid', 'smallint', 'unsigned', 'not null', 'primary key'),
        ('comtype', 'tinyint', 'not null'),
        ('comname', 'tinytext', 'not null'),
        ('state', 'tinytext', 'not null'),
        ('comcode', 'tinytext', 'not null'),
        ('x', 'smallint', 'not null'),
        ('y', 'smallint', 'not null'),
    )
    FIELDWORKERS=(
        ('fwid', 'tinyint', 'unsigned', 'not null', 'primary key'),
        ('fwcode', 'tinytext', 'not null'),
        ('fwname', 'tinytext', 'not null'),
    )
    WORKSHEETS=(
        ('wsid', 'tinyint', 'unsigned', 'not null', 'primary key'),
        ('wscode', 'tinytext', 'not null'),
        ('wsname', 'tinytext', 'not null'),
    )
    TABLES=(
        ('itemname', 'char(100)', 'not null', 'primary key'),
        ('tablename', 'tinytext', 'not null'),
        ('tabletype', 'tinyint', 'not null'),
        ('page', 'tinyint', 'not null'),
        ('subpage', 'tinytext', 'not null'),
        ('itemno', 'tinyint', 'not null'),
        ('subitemno', 'tinytext', 'not null'),
        ('notes', 'blob', 'not null'),
    )
    ITEM=(
        ('item', 'text', 'not null'),
        ('infid', 'smallint', 'not null'),
        ('gramflag', 'tinyint', 'not null'),
        ('doubtflag', 'tinyint', 'not null'),
        ('comtext', 'text', 'not null'),
        ('comments', 'tinytext', 'not null'),
        ('phonetic', 'tinyblob', 'not null'),
        ('simplephone', 'tinyblob', 'not null'),
        ('projectid', 'tinytext', 'not null'),
        ('itemid', 'smallint', 'unsigned', 'not null'),
        ('id', 'smallint', 'unsigned', 'auto_increment', 'primary key'),
    )
    PAGE=(
        ('item', 'text', 'not null'),
        ('infid', 'tinyint', 'not null'),
        ('gramflag', 'tinyint', 'not null'),
        ('doubtflag', 'tinyint', 'not null'),
        ('comtext', 'text', 'not null'),
        ('comments', 'tinytext', 'not null'),
        ('phonetic', 'tinyblob', 'not null'),
        ('simplephone', 'tinyblob', 'not null'),
        ('projectid', 'tinytext', 'not null'),
        ('itemid', 'smallint', 'unsigned', 'not null'),
        ('id', 'smallint', 'unsigned', 'auto_increment', 'primary key'),
        ('page', 'tinyint', 'not null'),
        ('subpage', 'tinytext', 'not null'),
        ('itemno', 'tinyint', 'not null'),
        ('subitemno', 'tinytext', 'not null'),
    )

atlas.tables.TableFields = MySQLFields

