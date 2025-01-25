import csv
import numpy
import math

# Used python csv docs to reference how to parse csvs
# https://docs.python.org/3/library/csv.html

def read_from_file(file_path):
    x = numpy.array([])
    y = numpy.array([])
    with open(file_path, 'r') as csv_file:
        reader = csv.reader(csv_file)

        # Used for skip the first line in CSV with the column header names
        # https://stackoverflow.com/questions/14674275/skip-first-linefield-in-loop-using-csv-file
        next(reader)

        for row in reader:
            x = numpy.append(x, float(row[0]))
            y = numpy.append(y, float(row[1]))
    return x, y

