#!/bin/sh

ATLASDIR=~/projects/atlas

echo Resetting the database
mysql -p -u root < $ATLASDIR/lap/resetdb.sql
#if [ -f lap.sqlite3 ]; then
#	rm lap.sqlite3;
#fi

echo Importing AFAM
ATLASSITE_TARGET=DEVEL PYTHONPATH=$ATLASDIR/lap \
	python2.4 $ATLASDIR/lap/scripts/csv2db.py \
	$ATLASDIR/data/afam

echo Importing LAMSAS
ATLASSITE_TARGET=DEVEL PYTHONPATH=$ATLASDIR/lap \
	python2.4 $ATLASDIR/lap/scripts/csv2db.py \
	$ATLASDIR/data/lamsas

