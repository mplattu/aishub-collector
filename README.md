# aishub-collector

AIShub collector gets data from AIShub network and stores it to the MySQL database for later use.
The script is written in Python 3.

The collector contains two scripts:
 * `aishub-collector.py` gets current data from AIShub API (see [http://www.aishub.net/api]) and stores
   it to `temp` table. You should call this script as often as you wish to get a snapshot of
   vessels in your area.
 * `aishub-downsampler.py` 1) reads the `temp` table, 2) writes the last entry of every ship to `aisdata` and
   cleans the `temp` table.

## Requirements

 * Python 3
 * `pymysql` (Debian/Ubuntu package `python3-pymysql`)

## Install

 1. Create and edit `settings.json` based on sample `settings.sample.json`. You need to fill
    your AIShub username to the AIShub URL and enter your MySQL credentials.
 1. Create MySQL database, e.g.: `mysql -u root -p <database.sql`
 1. Set `cron` to execute `aishub-collector.py` every ~2 minutes and `aishub-downsampler.py` as often
    as you wish to store the data (e.g. every 24 hours).
 1. Profit!
