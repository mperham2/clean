#! /usr/bin/env python
# Read list of patients, go through dataList and retain only corresponding rows, whether user rid, date, or any other variables
# Works on Python 3 only, not Python 2

##### Parameters you can have fun playing with
headersToCompare = [] # VISCODE
compareDate = True
dateMatch = 'EXAMDATE'


import csv, re, sys
from datetime import datetime
from dateutil import parser

### Functions

def ensure_proper_format(date):
    try:
        return parser.parse(date)
    except:
        return False


def return_closest_date(dates_list, date):
    date = ensure_proper_format(date)
    dates_list = [ensure_proper_format(x) for x in dates_list if x]

    closest_date = min(dates_list, key=lambda d: abs(d - date))
    return dates_list.index(closest_date)


def csv_object(csvfile):
    try:
        check = csvfile.read(1024)
        dialect = csv.Sniffer().sniff(check, delimiters=',\t ;:.')
        csvfile.seek(0)  # Goes back to beginning
        reader = csv.reader(csvfile, dialect)
    except:
        csvfile.seek(0)  # Goes back to beginning
        reader = csv.reader(csvfile, delimiter=',')
    return reader


def find_column(header, header_string):
    for column in range(len(header)):  # For each column in the header
        if header_string.strip().lower() == header[column].strip().lower():  # If the column's header is RID
            return column
    return False


def find_column_rid(header, filename):
    column = find_column(header, 'rid')
    if column is False:
        print("No header with rid in ", filename, ". I will assume rid are in the first column.")
        column = 0  # Assuming First Column
    return column


def find_column_date(header, filename):
    column = find_column(header, dateMatch)
    if column is False:
        print("No header with date in ", filename, ". I will assume dates are in the second column.")
        column = 1  # Assuming Second Column
    return column


def bleach_rid(rid):
    rid = re.sub("[^0-9]", "", rid).lstrip('0');
    return rid


def list_rid(csvfile):
    csv_list = []
    reader = csv_object(csvfile)
    for row in reader:
        csv_list.append(row)
    return csv_list

def main(*args):

    try:
        subjectList = args[1]
        dataList = args[2]
        outputList = args[3]
    except IndexError:
        subjectList = "subjectsList.csv"
        dataList = "dataList.csv"
        outputList = "outputList.csv"

    ### Read rid
    with open(subjectList, newline='') as csvfile:
        data1 = list_rid(csvfile)
    with open(dataList, newline='') as csvfile:
        data2 = list_rid(csvfile)


    ### Determining columns
    # Determine column for rid
    data1_ridColumn = find_column_rid(data1[0], 'subjectsList.csv')
    data2_ridColumn = find_column_rid(data2[0], 'dataList.csv')

    # Determine column for date
    if compareDate:
        data1_dateColumn = find_column_date(data1[0], 'subjectsList.csv')
        data2_dateColumn = find_column_date(data2[0], 'dataList.csv')

    # Determine column for all other variables
    data1Columns = []
    data2Columns = []
    for column_header in headersToCompare:
        data1Columns.append(find_column(data1[0], column_header))
        data2Columns.append(find_column(data2[0], column_header))

    # Create a list of rid's
    data2_rids = []
    for row in data2:
        data2_rids.append(bleach_rid(row[data2_ridColumn]))


    try:
        with open(outputList, 'w', newline='') as csvfile:
            outputFile = csv.writer(csvfile)

            # Write headers to outputFile, if any
            outputFile.writerow(data1[0] + data2[0])

            # Actually compare the two lists
            for data1_row in data1:  # For each desired subject/row
                data1_rid = bleach_rid(data1_row[data1_ridColumn])

                # Ignore if row is empty, and initialize some variables
                if not data1_row:
                    continue
                desiredRow = False

                # Find rows corresponding to the given subject
                #data2_list = [row for row in data2 if bleach_rid(data1_row[data1_ridColumn]) == bleach_rid(row[data2_ridColumn])] ## Problem here for four digits numbers
                data2_list = [data2[i] for i, j in enumerate(data2_rids) if j == data1_rid]

                # Compare rows in data2 for the given desired subject and return desired row
                if not data2_list: # If no row match
                    desiredRow = False
                elif compareDate: # If comparing dates
                    dates = []
                    for row in data2_list:
                        dates.append(row[data2_dateColumn])
                    if not dates:
                        print("You might want to check out dataList.csv. There is no corresponding dates, either you picked the wrong column or there is no info.")
                    index = return_closest_date(dates, data1_row[data1_dateColumn])
                    desiredRow = data2_list[index]
                elif not headersToCompare: # If no headers besides rid and date to compare
                    desiredRow = data2_list[0]
                else: # If headers to compare
                    for data2_row in data2_list:
                        ok = 1
                        for i in range(0,len(data1Columns)):
                            if data1_row[data1Columns[i]].strip() != data2_row[data2Columns[i]].strip():
                                ok = 0
                        if ok == 1:
                            desiredRow = data2_row
                            break

                if desiredRow is not False:
                    outputFile.writerow(data1_row + desiredRow)
                else:
                    outputFile.writerow(data1_row)
    except PermissionError:
        print('Close the outputList.csv. How do you expect me to work in these conditions geez?')

# The __name___ built-in variable is set to __main__ when the program is run from command line
# That way main is run when the file is ran from command line but not when it is imported
if __name__ == '__main__':
    main(*sys.argv)