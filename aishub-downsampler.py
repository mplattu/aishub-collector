#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import pymysql.cursors
from pymysql.converters import escape_string

# Read settings from json file
with open('settings.json', 'r') as jsonf:
	SETTINGS = json.load(jsonf)

# Open database connection (one for table `temp`, one for table `aisdata` since
# we need two cursors here.

db_temp = pymysql.connect(host=SETTINGS['database']['host'],
	user=SETTINGS['database']['user'],
	password=SETTINGS['database']['password'],
	db=SETTINGS['database']['db'],
	charset='utf8mb4',
    cursorclass=pymysql.cursors.SSCursor    # Using unbuffered cursor
    )
cursor_temp = db_temp.cursor()

db_aisdata = pymysql.connect(host=SETTINGS['database']['host'],
	user=SETTINGS['database']['user'],
	password=SETTINGS['database']['password'],
	db=SETTINGS['database']['db'],
	charset='utf8mb4',
    cursorclass=pymysql.cursors.SSCursor    # Using unbuffered cursor
    )
cursor_aisdata = db_aisdata.cursor()

# SELECT * FROM `temp` ORDER BY `mmsi`,`_writetime` ASC;
sql_select = (
    "SELECT `mmsi`,`time`,`longitude`,`latitude`,`cog`,`sog`,`heading`,"
    "`navstat`,`imo`,`name`,`callsign`,`type`,`a`,`b`,`c`,`d`,`draught`,`dest`,`eta`, `_writetime` "
    "FROM `temp` ORDER BY `mmsi`,`_writetime` ASC"
    )

cursor_temp.execute(sql_select)

previous_ship = None
previous_row = None
row_count=0

# Fetch first row
row = cursor_temp.fetchone()
while row is not None:

    if (previous_ship is not None and previous_ship != row[0]):
        # New ship, write previous row to permanent database
        row_count+=1

        sql_insert = (
    		'INSERT INTO `aisdata` SET `mmsi`=%s, `time`=%s, `longitude`=%s, `latitude`=%s, '
    	 	'`cog`=%s, `sog`=%s, `heading`=%s, `navstat`=%s, '
    		'`imo`=%s, `name`=%s, `callsign`=%s, `type`=%s, '
    		'`a`=%s, `b`=%s, `c`=%s, `d`=%s, '
    		'`draught`=%s, `dest`=%s, `eta`=%s, `_writetime`=%s'
    		)

        cursor_aisdata.execute(sql_insert, (
            previous_row[0], previous_row[1], previous_row[2], previous_row[3],
            previous_row[4], previous_row[5], previous_row[6], previous_row[7],
            previous_row[8], previous_row[9], previous_row[10], previous_row[11],
            previous_row[12], previous_row[13], previous_row[14], previous_row[15],
            previous_row[16], previous_row[17], previous_row[18], previous_row[19]
        ))

		# Commit every 100 lines
        if ((row_count % 100) == 0):
            db_aisdata.commit()

    previous_row = row
    previous_ship = row[0]
    # Fetch next row
    row = cursor_temp.fetchone()

cursor_temp.close()
cursor_aisdata.close()

# Delete all data from temp table
cursor_temp = db_temp.cursor()
sql_delete = 'DELETE FROM `temp`'
cursor_temp.execute(sql_delete)
db_temp.commit()

db_temp.close()
db_aisdata.close()
