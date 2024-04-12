#!/usr/bin/env python3

import xml.etree.ElementTree as ET

print("Start parse.")

export = ET.parse('../data/apple_health_export-2023/export.xml')
export_root = export.getroot()

print("Finding activity...")

# Print swimming

filename = "activity.csv"
print("Writing " + filename + "...")

wo_attributes = ['startDate', 'endDate', 'duration', 'workoutActivityType']

with open(filename, 'w') as output_file:
  # Header
  output_file.write(','.join(wo_attributes) + ',calories\n')

  # Records
  for workout in export_root.findall('Workout'):
    for att in wo_attributes:
      value = workout.get(att)
      if value is None:
        value = "NULL" # Catch null values
      output_file.write(value + ",")
    for stats in workout.findall('WorkoutStatistics'):
      if stats.get('type') == 'HKQuantityTypeIdentifierActiveEnergyBurned':
        output_file.write(stats.get('sum'))
    output_file.write("\n")

print("Done.")
