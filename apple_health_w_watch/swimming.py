import sys
sys.path.append('..')
import csv
from datetime import datetime
import json

data_of_year = dict()

# Remove first few lines to start with the column heading
with open('swimming.csv', newline='') as csv_file:
    for row in csv.DictReader(csv_file):
        raw_date = datetime.strptime(row['startDate'], '%Y-%m-%d %H:%M:%S %z')
        year = raw_date.year
        if year not in data_of_year:
            data_of_year[year] = dict()

        date = raw_date.strftime('%-m/%-d/%Y')
        raw_value = float(row['distance'])
        value = int(raw_value) if raw_value % 1 == 0 else round(raw_value, 2)

        # in case of multiple records in a day
        if date in data_of_year[year]:
            data_of_year[year][date] += value
        else:
            data_of_year[year][date] = value

# save datasets
for year in data_of_year:
    if year > 2020 or year < 2024:
        dataset = []
        for each_date in data_of_year[year]:
            dataset.append(dict(date=each_date, value=data_of_year[year][each_date]))
        json_data = json.dumps(dataset, separators=(',',':'), indent=2, ensure_ascii=False)
        fd = open('../../quantify-your-year/src/data/tanyofish-swimming-' + str(year) + '.json', 'w', encoding='utf8')
        fd.write(json_data)
        fd.close()
        print('Generated tanyofish-swimming-' + str(year) + '.json')
        # TODO: script for setting files
