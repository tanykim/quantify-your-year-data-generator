from datetime import datetime
import pytz
import json
import _setup
import _savedatasets

# load piano practice file
# this file was generated with IFTTT
# save start time: https://ifttt.com/applets/92183169d-if-you-say-i-am-playing-the-piano-then-add-row-to-tanyoung-kim-s-google-drive-spreadsheet
# save end time: https://ifttt.com/applets/92183383d-if-you-say-i-m-done-with-the-piano-then-add-row-to-tanyoung-kim-s-google-drive-spreadsheet
# then convert this spreadsheet to JSON format using this https://www.npmjs.com/package/google-spreadsheet-to-json
# run the following script:
# $ gsjson 1zFSHMbYUnu9cm3pU4rxPcfHPnRBhBiXKnM0OiUTJ6RQ data/piano-2019.json -b -l

YEAR = _setup.YEAR
data_of_year = []

def add_date(date, duration):
    data_of_year.append(dict(date=date, value=duration))

def add_duration(date, duration):
    if len(data_of_year) == 0:
        add_date(date, duration)
    else:
        if data_of_year[len(data_of_year) - 1]['date'] == date:
            data_of_year[len(data_of_year) - 1]['value'] += duration
        else:
            add_date(date, duration)

with open('data/piano.json') as file:
    data = json.load(file)

    for i in range(len(data) - 1):
        d = data[i]
        # if the first start time isn't recorded
        # in case there's no start or stop time recorded, set it to 20 minutes
        diff_in_min = 20
        if i == 0 and d[1] == 'stop':
            t = datetime.strptime(d[0], '%B %d, %Y at %I:%M%p')
            add_duration(datetime.strftime(t, '%-m/%-d/%Y'), diff_in_min)
        # find start time first
        elif d[1] == 'start':
            start_time = datetime.strptime(d[0], '%B %d, %Y at %I:%M%p')
            # end time should come in the next element
            end = data[i + 1]
            if end[1] == 'stop':
                end_time = datetime.strptime(end[0], '%B %d, %Y at %I:%M%p')
                # duration in minute
                diff_in_min = int((end_time - start_time).seconds / 60)
                date = datetime.strftime(start_time, '%-m/%-d/%Y')
                add_duration(date, diff_in_min)

# save datasets
_savedatasets.save_dataset(data_of_year, 'tanyoung', 'piano_practice', 'piano')