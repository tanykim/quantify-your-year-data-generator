import csv
from datetime import datetime
import pytz
import _setup
import _savedatasets
import math

DEFAULT_TIMEZONE = pytz.timezone(_setup.DEFAULT_TIMEZONE)
YEAR = _setup.YEAR

data_of_year = []

current_date = '1/1/' + str(YEAR)
first_odometer_of_date = 0

for i in range(12):
    month = str(i + 1) if i >= 9 else ('0' + str(i + 1))
    # open each month's csv file
    with open('data/all_driving_data/' + str(YEAR) + '-' + month + '.csv', newline='') as csvfile:
        for row in csv.DictReader(csvfile):

            # valid rows with both date and odometer data
            if row['recordDateTime'] != '' and row['totalOdometerMeters'] != '':

                # get date in the correct timezone
                dt = datetime.strptime(row['recordDateTime'], '%Y-%m-%dT%H:%M:%S.%fZ')
                timestamp = dt.replace(tzinfo=pytz.utc).timestamp()
                dt_tz = datetime.fromtimestamp(timestamp).astimezone(pytz.utc).astimezone(DEFAULT_TIMEZONE)
                date = dt_tz.strftime('%-m/%-d/%Y')

                if current_date == '7/29/2018':
                    print(date, current_date, row['totalOdometerMeters'])
                if current_date == '7/30/2018':
                    print(date, current_date, row['totalOdometerMeters'])

                # get the very first odometer
                if first_odometer_of_date == 0 and dt_tz.year == YEAR:
                    first_odometer_of_date = int(row['totalOdometerMeters'])

                # date change
                if date != current_date and first_odometer_of_date > 0:
                    driving_distance = int(row['totalOdometerMeters']) - first_odometer_of_date

                    if date == '7/30/2018' or date == '7/31/2018':
                        print ('---', date, current_date, driving_distance)

                    if driving_distance > 0 and dt_tz.year == YEAR:
                        # meter to mile
                        data_of_year.append(dict(date=current_date, value= math.ceil(driving_distance * 0.000621371 * 100) / 100 ))

                    # reset for next day
                    current_date = date
                    first_odometer_of_date = int(row['totalOdometerMeters'])

# save datasets
_savedatasets.save_dataset(data_of_year, _setup.CAR, 'driving', 'driving')