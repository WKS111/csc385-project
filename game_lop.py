import csv
from ortools.linear_solver import pywraplp

# opening the CSV file
with open('BGG Top 100.csv', mode='r')as file:

    # reading the CSV file
    csvFile = csv.reader(file)

    # displaying the contents of the CSV file
    for lines in csvFile:
        print(lines[0])
