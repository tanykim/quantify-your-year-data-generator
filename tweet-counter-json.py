import json
from datetime import datetime
import pytz
import _setup
import _savedatasets

# set timezone and year
DEFAULT_TIMEZONE = pytz.timezone(_setup.DEFAULT_TIMEZONE)
YEAR = _setup.YEAR

data_of_year = []

def add_date(date):
    # append older data to the beginning of the array
    data_of_year.insert(0, dict(date=date, value=1))

def get_tweet_info(d):
    date = d.strftime('%-m/%-d/%-Y')
    if len(data_of_year) == 0:
        add_date(date)
    else:
        if data_of_year[0]['date'] == date:
            data_of_year[0]['value'] += 1
        else:
            add_date(date)

# collect data first
tweets = []
# remove the variable name in tweet.js and tweet-part2.js and save them as JSON
for file_name in ['tweet', 'tweet-part1']:
    with open('data/' + file_name + '.json') as file:
        data = json.load(file)
        for d in data:
            tweet = d['tweet']
            utc_date = datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S %z %Y')
            date = utc_date.astimezone(DEFAULT_TIMEZONE)
            if int(date.year) == YEAR:
                tweets.append(dict(date=date, id=tweet['id_str'], text=tweet['full_text']))

# sort by date desc
for tweet in sorted(tweets, key=lambda x: x['id'], reverse=True):
    # if '체육관' in tweet['text'] or '운동' in tweet['text    ']:
    #     print (tweet['date'], tweet['text'])
    get_tweet_info(tweet['date'])

# save dataset
_savedatasets.save_dataset(data_of_year, _setup.TWITTER, 'twitter', 'twitter')