from datetime import datetime
import pytz
import json
import _setup
import _savedatasets

# set timezone and year
DEFAULT_TIMEZONE = pytz.timezone(_setup.DEFAULT_TIMEZONE)
YEAR = _setup.YEAR

# place, latitude, and longitude
PLACE = _setup.PLACE
LAT = _setup.LAT
LON = _setup.LON

by_date = dict()

def getTimeZonedTime(ts):
    utc = datetime.fromtimestamp(int(ts) / 1000).astimezone(pytz.utc)
    return utc.astimezone(DEFAULT_TIMEZONE)

# load google map history data
with open('data/Location History.json') as file:
    data = json.load(file)

    # check single traces
    for i in range(len(data['locations'])):
        trace = data['locations'][i]

        # all data is set to UTC, convert to the timezone of the home location
        current_time = getTimeZonedTime(trace['timestampMs'])

        # check only the selected year
        year = int(current_time.year)
        if year == YEAR:

            # get the format as date, as a key of dataset
            today = datetime.strftime(current_time, '%-m/%-d/%Y')

            # compare the lat/lon of the trace with the home location
            lat = int(trace['latitudeE7']) / 10000000
            lon = int(trace['longitudeE7']) / 10000000
            rounded_lat = round(lat * 1000)
            rounded_lon = round(lon * 1000)
            home_lat_rounded = round(LAT * 1000)
            home_lon_rounded = round(LON * 1000)

            # probably the location - some lat and log are slightly off, this could be an acceptable range
            if abs(home_lat_rounded - rounded_lat) <= 2 and abs(home_lon_rounded - rounded_lon) <= 2:
                prev_time = getTimeZonedTime(data['locations'][i + 1]['timestampMs'])

                # if different date
                if datetime.isocalendar(current_time) != datetime.isocalendar(prev_time):

                    yesterday = datetime.strftime(prev_time, '%-m/%-d/%Y')

                    # split the time span at midnight
                    midnight = datetime.strftime(datetime.date(current_time), '%Y-%m-%d %H:%M:%S')
                    midnight_time = datetime.strptime(midnight, '%Y-%m-%d %H:%M:%S')
                    till_midnight = (midnight_time - prev_time.replace(tzinfo=None)).seconds
                    from_midnight = (current_time.replace(tzinfo=None) - midnight_time).seconds

                    # accumulate time spent at home location by day
                    by_date[today] = by_date[today] + from_midnight if today in by_date.keys() else from_midnight
                    by_date[yesterday] = by_date[yesterday] + till_midnight if yesterday in by_date.keys() else till_midnight

                # same date
                else:
                    duration = (current_time - prev_time).seconds
                    by_date[today] = by_date[today] + duration if today in by_date.keys() else duration

        elif year < YEAR:
            break

# convert dict to array
data_of_year = []
for d in by_date:
    # save it as hour, record only valid points
    hour = round(by_date[d] / 60 / 60 * 10) / 10
    if hour > 0.0:
        data_of_year.insert(0, dict(date=d, value=hour))

# save datasets
_savedatasets.save_dataset(data_of_year, _setup.GOOGLE, 'time-at-' + _setup.PLACE, 'location')