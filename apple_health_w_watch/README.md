# Apple health data with cleaning
This folder contains several Python scripts that generate exercise data with Apple Health data tracked via Apple Watch.

## Export your health data
Export Apple health data from iPhone, and locate it `../data/apple_health_export-2023`.

## Run scripts

1. `appple-health-activities.py` parses exercises with activity type, start and end time, duration, and calories burnt, then generates `activity.csv` file. `daily_exercise.py` generates datasets for [shades-of-exercise](https://github.com/tanykim/shades-of-exercise).
2. `apple-health-swimming.py` parses swimming data with start and end time, duration, distance, then generates `swimming.csv` file. `swimming.py` generates datasets for [quantify-your-year](https://github.com/tanykim/quantify-your-year).


