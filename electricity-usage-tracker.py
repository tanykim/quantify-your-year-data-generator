import csv
from datetime import datetime
import _setup
import _savedatasets

YEAR = _setup.YEAR

day_dict = dict()

# Remove first few lines to start with the column heading
with open('data/pge_electric_interval_data.csv', newline='') as csvfile:
    for row in csv.DictReader(csvfile):
        date = row['DATE']
        # to keep the accuracy, multiply 100 as int
        usage = int(float(row['USAGE']) * 100)
        day_dict[date] = day_dict[date] + usage if date in day_dict.keys() else usage

data_of_year = []
for day in day_dict:
    day_p = datetime.strptime(day, '%m/%d/%y')
    day_formatted = datetime.strftime(day_p, '%-m/%-d/%Y')
    # divide by 100 to get the sum as float format
    data_of_year.append(dict(date=day_formatted, value=day_dict[day] / 100))

# save datasets
_savedatasets.save_dataset(data_of_year, _setup.PLACE, 'electricity-usage', 'electricity')