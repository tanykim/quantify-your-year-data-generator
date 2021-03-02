# quantify-your-year-data-generator

Various datasets generators for [Quantify Your Year project](http://tany.kim/quantify-your-year)

This repo includes dataset generators of reactions on Facebook, tweets, location history, step/floor counter, electricity usage, car odometer. Depending on the availability of your data sources, use the generators.

Each python file generates both setting and dataset json files for the front-end visualization. 


# Download this repo

Have this repo in the same location of [quantify-your-year repo](https://github.com/tanykim/quantify-your-year) like below.
```
/quantify-your-year
/quantify-your-year-data-generator

```

# Setup the basic information

Open ```_setup.local``` and replace place holders with your data. Follow the instruction in the file.
Then copy the setting to a Python file.

```
cp _setup.local _setup.py
```

# Reactions on Facebook

Count daily reactions (like, love, haha and etc) on Facebook. This requires a Facebook account.

1. Download your Facebook information 'Likes and Reactions' from privacy setting. 
2. Find ```posts_and_comments.json``` and copy under ```/data``` folder.
3. Run ```facebook-reaction-tracker.py```.


# Tweet Counter

Count daily tweets. This requires you have an active Twitter account.

1. Download the archive on your twitter account page.
2. Copy ```tweets.csv``` under ```/data``` folder.
3. Run ```tweet-counter.py```.

It looks like if you have too many tweets, csv file isn't generated. Then we will use ```tweet.js``` and ```tweet-part1.js```; 
remove the variable name and save those files as JSON. Then move those files to under ```/data``` folder, run ```tweet-counter-json.py```.

# Location History Tracker

Calculate daily time spent at a single location. This requires an active Google account. 

1. Sign in and download your Location History data from the [Google's Takeout page.](https://takeout.google.com/settings/takeout)
2. Unzip the downloaded file, you'll see ```Takeout/Location History/Location History.json```.
3. Copy ```Location History.json``` under ```/data``` folder.
4. Run ```location-history-tracker.py```.

# Step Counter & Flights Climbed Counter

Calculate daily step and flight floors counter (two kinds of dataset). You have to use iPhone and have iCloud account.  

1. On your iPhone, open Health app. Check your account setting and export health data.
2. Unzip the downloaded file, you'll see ```apple_health_export``` folder.
3. Copy the folder under ```/data``` folder.
4. Run ```step_counter.py```. This will generate two sets of files (step count and flights climbed floors). 

# Electricity Usage Tracker

Calculate the consumption or production of electricity of solar panels of a house. This requires an active account at PG and E.

1. Sign in [PG and E](https://www.pge.com) and download the usage data of the selected year. 
2. Find a csv file named like this ```pge_electric_interval_data_[your-account].csv``` and save it as ```pge_electric_interval_data.csv``` under the folder ```/data```.
3. Open the CSV file and remove the first few lines that contain meta information of the csv file. In other words, the csv file should start with the row with the column name. 
4. Run ```electricity-usage-tracker.py```.

# Driving Tracker

Track the distance of daily driving. This requires you're a member of [Metromile](https://www.metromile.com) car insurance.

1. Export your driving data.
2. Copy ```all_driving-data``` folder under ```/data```.
3. Run ```driving-tracking.py```.

# Last.fm Scrobble Counter

Count how many songs scrobbled to your Last.fm account. This requires you go to this [site](https://benjaminbenben.com/lastfm-to-csv/).

1. Enter your Last.fm username and click fetch tracks.
2. Save as ```lastfmusername.csv``` under ```/data```.
3. Open the csv file and add a column named ```date``` on the first D column.
3. Run ```lastfm-scrobble-counter.py```.
