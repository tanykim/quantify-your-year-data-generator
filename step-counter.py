import xml.etree.ElementTree as ET
from datetime import datetime
from datetime import timedelta
import _setup
import _savedatasets

# read xml files exported from iOS Health app
tree = ET.parse('data/apple_health_export/export.xml')
root = tree.getroot()

YEAR = _setup.YEAR

def generate_data_by_date(apple_data_type, dataset_name, data_type):

    date_dict = dict()
    for child in root:
        attr = child.attrib

        # fild the matching data type
        if child.tag == 'Record' and attr['type'] == apple_data_type:

            start_date = datetime.strptime(attr['startDate'], '%Y-%m-%d %H:%M:%S %z')
            end_date = datetime.strptime(attr['endDate'], '%Y-%m-%d %H:%M:%S %z')

            #check year
            if start_date.year == YEAR:

                # step count & date
                count = int(attr['value'])
                date = datetime.strftime(start_date, '%-m/%-d/%Y')

                # check start and end date if count happens over two or more days
                if datetime.isocalendar(start_date) != datetime.isocalendar(end_date):
                    # split the count in proportion to duration of before and after midnight
                    midnight = datetime.strftime(datetime.date(end_date), '%Y-%m-%d %H:%M:%S')
                    midnight_time = datetime.strptime(midnight, '%Y-%m-%d %H:%M:%S')
                    till_midnight = (midnight_time - start_date.replace(tzinfo=None)).seconds
                    from_midnight = (end_date.replace(tzinfo=None) - midnight_time).seconds

                    in_the_middle = 0
                    mid_date_count = (end_date - start_date).days - 1
                    # more than one day gap, second of the middle days
                    if mid_date_count > 0:
                        in_the_middle = 60 * 60 * 24 * mid_date_count

                    count_before_midnight = round(till_midnight / (till_midnight + in_the_middle + from_midnight) * count)
                    count_after_midnight = round(from_midnight / (till_midnight + in_the_middle + from_midnight) * count)

                    # add count to start and end date
                    date_dict[date] = date_dict[date] + count_before_midnight if date in date_dict.keys() else count_before_midnight

                    if end_date.year == YEAR:
                        next_date = datetime.strftime(end_date, '%-m/%-d/%Y')
                        date_dict[next_date] = date_dict[next_date] + count_after_midnight if next_date in date_dict.keys() else count_after_midnight

                    # add count to the dates evenly distributed to the dates in the middle
                    for i in range(mid_date_count):
                        count_in_a_mid_day = round((count - count_before_midnight - count_after_midnight) / mid_date_count)
                        mid_datetime = start_date + timedelta(days=(i + 1))
                        mid_date = datetime.strftime(mid_datetime, '%-m/%-d/%Y')
                        if mid_datetime.year == YEAR:
                            date_dict[mid_date] = date_dict[mid_date]  + count_in_a_mid_day if mid_date in date_dict.keys() else count_in_a_mid_day

                else:
                    date_dict[date] = date_dict[date] + count if date in date_dict.keys() else count

    # convert dict to array
    data_of_year = []
    for d in date_dict:
        data_of_year.append(dict(date=d, value=date_dict[d]))
    # sort by date; often date isn't ordered in the original data
    data_of_year = sorted(data_of_year, key=lambda i: datetime.strptime(i['date'], '%m/%d/%Y').timestamp())
    # save data as json
    _savedatasets.save_dataset(data_of_year, _setup.NAME, dataset_name, data_type)

generate_data_by_date('HKQuantityTypeIdentifierStepCount', 'steps', 'steps')
generate_data_by_date('HKQuantityTypeIdentifierFlightsClimbed', 'flights-climbed', 'floors')