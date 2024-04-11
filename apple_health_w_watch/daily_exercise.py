import sys
sys.path.append('..')
import csv
from datetime import datetime
import json
from itertools import groupby

data = []

# Remove first few lines to start with the column heading
with open('activity.csv', newline='') as csv_file:
    for row in csv.DictReader(csv_file):
        raw_date = datetime.strptime(row['startDate'], '%Y-%m-%d %H:%M:%S %z')
        year = raw_date.year
        date = raw_date.strftime('%-m/%-d')
        activity_type = row['workoutActivityType'].replace('HKWorkoutActivityType', '')
        duration = int(float(row['duration']))
        calories = int(float(row['calories'])) if row['calories'] != '' else 0
        data.append(dict(
            year = year, 
            date = date, 
            activity_type = activity_type,
            duration = duration, 
            calories = calories,
        ))

data_of_year = dict()
DURATION_THRESHOLD = 20

for year, year_data in groupby(data, key=lambda x: x['year']):
    data_of_year[year] = dict(types=dict(), data=dict())
    for date, date_data in groupby(list(year_data), key=lambda x: x['date']):
        for activity, activity_data in groupby(list(date_data), key=lambda x: x['activity_type']):
            duration = 0
            calories = 0
            for d in list(activity_data):
                duration += d['duration']
                calories += d['calories']

            if duration > DURATION_THRESHOLD and calories > 0:
                data_of_year[year]['data'][date] = []
                if activity not in data_of_year[year]['types']:
                    data_of_year[year]['types'][activity] = 1
                else:
                    data_of_year[year]['types'][activity] += 1
                
                data_of_year[year]['data'][date].append(
                    dict(type = activity, note= str(duration) + ' min / ' + str(calories) + ' kcal')
                )
        


# save datasets
for year in data_of_year:
    if year < 2024:
        dataset = []
        for each_date in data_of_year[year]:
            dataset.append(dict(date=each_date, value=data_of_year[year][each_date]))
        json_data = json.dumps(dataset, separators=(',',':'), indent=2, ensure_ascii=False)
        fd = open('../../shades-of-exercise/src/data/data-' + str(year) + '.json', 'w', encoding='utf8')
        fd.write(json_data)
        fd.close()
        print('Generated exercise data - ' + str(year) + '.json')

