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
            # https://math.stackexchange.com/questions/4503690/how-much-distance-is-covered-by-each-unit-of-longitude-and-latitude#:~:text=According%20to%20this%20question%20here,111.320*cos(latitude)%20km
            x = numpy.append(x, math.cos(math.radians(float(row[0]))) * 111.320)
            y = numpy.append(y, float(row[1]) * 110.574)
    return x, y

