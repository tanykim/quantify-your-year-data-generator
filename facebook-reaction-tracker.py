from datetime import datetime
import pytz
import json
import _setup
import _savedatasets

# set timezone and year
DEFAULT_TIMEZONE = pytz.timezone(_setup.DEFAULT_TIMEZONE)
YEAR = _setup.YEAR

by_date = dict()

def getTimeZonedTime(ts):
    utc = datetime.fromtimestamp(ts).astimezone(pytz.utc)
    return utc.astimezone(DEFAULT_TIMEZONE)

# load google map history data
with open('data/posts_and_comments.json') as file:
    data = json.load(file)

    # check single traces
    for i in range(len(data['reactions'])):
        trace = data['reactions'][i]

        # all data is set to UTC, convert to the timezone of the home location
        current_time = getTimeZonedTime(trace['timestamp'])

        # check only the selected year
        year = int(current_time.year)
        if year == YEAR:

            # get the format as date, as a key of dataset
            today = datetime.strftime(current_time, '%-m/%-d/%Y')

            by_date[today] = by_date[today] + 1 if today in by_date.keys() else 1

# convert dict to array
data_of_year = []
for d in by_date:
    data_of_year.insert(0, dict(date=d, value=by_date[d]))

# save datasets
_savedatasets.save_dataset(data_of_year, _setup.FACEBOOK, 'reactions-on-facebook', 'facebook')