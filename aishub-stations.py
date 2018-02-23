#!/usr/bin/python
# -*- coding: utf-8 -*-

import json, re, numpy
import urllib.request
import pymysql.cursors
from pymysql.converters import escape_string

# Read settings from json file
with open('settings.json', 'r') as jsonf:
	SETTINGS = json.load(jsonf)

class AIShubStations:
    def __init__ (self, url_index, url_station):
        self.URL_INDEX = url_index
        self.URL_STATION = url_station

    def get_index_page_data (self, page_n):
        # Get station IDs from one index page

        # Build regex
        re_ids = re.compile('<tr data-key="(\\d+)">')

        page_text = urllib.request.urlopen(self.URL_INDEX % page_n).read().decode("utf-8")

        int_ids = []
        for this_id in re_ids.findall(page_text):
            int_ids.append(int(this_id))

        return sorted(int_ids)

    def get_index_ids (self):
        # Get IDs of all AIShub stations (from all possible index pages)

        # This will contain all station ids
        all_ids = []

        old_ids = None
        new_ids = []
        page_id = 0
        were_done = False

        while not were_done:
            page_id += 1

            old_ids = new_ids[:]
            new_ids = self.get_index_page_data(page_id)

            if numpy.array_equal(old_ids, new_ids):
                # page_id does not contain any new station IDs
                were_done = True
            else:
                # we have new station IDs
                all_ids = all_ids + new_ids

        return sorted(all_ids)

    def get_station_data (self, station_id):
        # Get data of a given station

        station_data = {
            "id": int(station_id),
            "name": None,
            "uptime": None,
            "latitude": None,
            "longitude": None,
        }

        page_text = urllib.request.urlopen(self.URL_STATION % station_id).read().decode("utf-8")

        re_station_name = re.compile('<li><a href="'+(self.URL_STATION % station_id)+'">(.+)</a></li>')
        match_station = re_station_name.search(page_text)
        if match_station:
            station_data['name'] = match_station.group(1)

        re_uptime = re.compile('<span id="uptime">(\d+)</span>')
        match_uptime = re_uptime.search(page_text)
        if match_uptime:
            station_data['uptime'] = int(match_uptime.group(1))

        re_lat = re.compile('"lat":"(.+?)"')
        match_lat = re_lat.search(page_text)
        if match_lat:
            station_data['latitude'] = match_lat.group(1)

        re_lon = re.compile('"lon":"(.+?)"')
        match_lon = re_lon.search(page_text)
        if match_lon:
            station_data['longitude'] = match_lon.group(1)

        return station_data

aishubstations = AIShubStations(SETTINGS['stations']['url_index'], SETTINGS['stations']['url_station'])

# Get station IDs
station_ids = aishubstations.get_index_ids()

# Open database connection
db = pymysql.connect(host=SETTINGS['database']['host'],
	user=SETTINGS['database']['user'],
	password=SETTINGS['database']['password'],
	db=SETTINGS['database']['db'],
	charset='utf8mb4',
    cursorclass=pymysql.cursors.SSCursor    # Using unbuffered cursor
    )

sql = 'INSERT INTO `stations` SET `station_id`=%s, `name`=%s, `uptime`=%s, `latitude`=%s, `longitude`=%s'
cursor = db.cursor()

# Get data for each station and write that to the database
for this_station_id in station_ids:
    station_data = aishubstations.get_station_data(this_station_id)

    cursor.execute(sql, (station_data['id'], station_data['name'], station_data['uptime'], station_data['latitude'], station_data['longitude']))
    db.commit()

db.close()
