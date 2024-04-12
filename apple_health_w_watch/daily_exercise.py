import sys
sys.path.append('..')
import csv
from datetime import datetime
import json
from itertools import groupby

data = []

# filter unused activity types
with open('activity.csv', newline='') as csv_file:
    for row in csv.DictReader(csv_file):
        activity_type = row['workoutActivityType'].replace('HKWorkoutActivityType', '')
        if activity_type != 'Walking' and activity_type != 'Cooldown' and activity_type != 'PreparationAndRecovery':
            raw_date = datetime.strptime(row['startDate'], '%Y-%m-%d %H:%M:%S %z')
            data.append(dict(
                year = raw_date.year,
                day = raw_date.strftime('%A'),
                date = raw_date.strftime('%-m/%-d'),
                activity_type = activity_type,
                duration = int(float(row['duration'])), 
                calories =  int(float(row['calories'])) if row['calories'] != '' else 0,
            ))

# generate daily exercise data
data_of_year = dict()
DURATION_THRESHOLD = 30
CALORIES_THRESHOLD = 100

for year, year_data in groupby(data, key=lambda x: x['year']):
    data_of_year[year] = dict(types=dict(), data=dict())
    for date, date_data in groupby(list(year_data), key=lambda x: x['date']):
        for activity, activity_data in groupby(list(date_data), key=lambda x: x['activity_type']):
            duration = 0
            calories = 0
            for d in list(activity_data):
                duration += d['duration']
                calories += d['calories']
            if duration > DURATION_THRESHOLD and calories > CALORIES_THRESHOLD:
                data_of_year[year]['data'][date] = []
                if activity not in data_of_year[year]['types']:
                    data_of_year[year]['types'][activity] = 1
                else:
                    data_of_year[year]['types'][activity] += 1
                
                # for each date
                data_of_year[year]['data'][date].append(
                    dict(type = activity, note= str(duration) + ' min / ' + str(calories) + ' kcal')
                )

# by day and month summary
for year in data_of_year:
    by_day = [dict() for i in range(7)]
    by_month = [dict() for i in range(12)]
    for date in data_of_year[year]['data']:
        day = int(datetime.strptime(str(year) + '/' + date, '%Y/%m/%d').strftime('%w'))
        month = int(datetime.strptime(str(year) + '/' + date, '%Y/%m/%d').strftime('%-m')) - 1
        for activity in data_of_year[year]['data'][date]:
            if activity['type'] in by_day[day]:
                by_day[day][activity['type']] += 1
            else:
                by_day[day][activity['type']] = 1
            if activity['type'] in by_month[month]:
                by_month[month][activity['type']] += 1
            else:
                by_month[month][activity['type']] = 1
    data_of_year[year]['by_day'] = by_day
    data_of_year[year]['by_month'] = by_month

# save datasets
for year in data_of_year:
    if year > 2020 and year < 2024:
        json_data = json.dumps(data_of_year[year], separators=(',',':'), indent=2, ensure_ascii=False)
        fd = open('../../shades-of-exercise/src/data/data-' + str(year) + '.json', 'w', encoding='utf8')
        fd.write(json_data)
        fd.close()
        print('Generated exercise data - ' + str(year) + '.json')

