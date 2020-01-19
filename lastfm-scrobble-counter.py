import csv
from datetime import datetime
import json
import pytz
import _setup
import _savedatasets

# set timezone and year
DEFAULT_TIMEZONE = pytz.timezone(_setup.DEFAULT_TIMEZONE)
YEAR = _setup.YEAR

data_of_year = []

def addDate(date):
    data_of_year.insert(0, dict(date=date, value=1))

def getTweetInfo(d):
    date = d.strftime('%-m/%-d/%-Y')
    if len(data_of_year) == 0:
        addDate(date)
    else:
        if data_of_year[0]['date'] == date:
            data_of_year[0]['value'] += 1
        else:
            addDate(date)

with open('data/' + _setup.LASTFM + '.csv', newline='') as csvfile:
    sheet = csv.DictReader(csvfile)
    for row in sheet:
        utc_date = datetime.strptime(row['date'], '%d %b %Y %H:%M')
        date = utc_date.astimezone(DEFAULT_TIMEZONE)
        year = int(date.year)
        if year == YEAR:
            getTweetInfo(date)
        elif year < YEAR:
            break

# save datasets
_savedatasets.save_dataset(data_of_year, _setup.LASTFM, 'lastfm', 'lastfm')