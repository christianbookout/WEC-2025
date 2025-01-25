import csv

# Used python csv docs to reference how to parse csvs
# https://docs.python.org/3/library/csv.html

file_path = 'coordinates2005.csv'
coordinates = [] 
with open(file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)

    # Used for skip the first line in CSV with the column header names
    # https://stackoverflow.com/questions/14674275/skip-first-linefield-in-loop-using-csv-file
    next(reader)

    for row in reader:
        coordinates.append(tuple((row[0], row[1])))
