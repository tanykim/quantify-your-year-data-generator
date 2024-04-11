#!/usr/bin/env python3

import xml.etree.ElementTree as ET

print("Start parse.")

export = ET.parse('../data/apple_health_export-2023/export.xml')
export_root = export.getroot()

print("Finding swimming...")

# Print swimming

filename = "swimming.csv"
print("Writing " + filename + "...")

wo_attributes = ['startDate', 'endDate', 'duration']

with open(filename, 'w') as output_file:
  # Header
  output_file.write(','.join(wo_attributes) + ',distance,unit,calories' + "\n")

  # Records
  for workout in export_root.findall('Workout'):
    if workout.get('workoutActivityType') == 'HKWorkoutActivityTypeSwimming':
      for att in wo_attributes:
        value = workout.get(att)
        if value is None:
          value = "NULL" # Catch null values
        output_file.write(value + ",")
      for stats in workout.findall('WorkoutStatistics'):
        if stats.get('type') == 'HKQuantityTypeIdentifierDistanceSwimming':
          output_file.write(stats.get('sum') + "," + stats.get('unit') + ',')
        if stats.get('type') == 'HKQuantityTypeIdentifierActiveEnergyBurned':
          output_file.write(stats.get('sum'))

      output_file.write("\n")

print("Done.")
