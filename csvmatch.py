""" csvmatch.py
    A module to compare two lists of csvs and match up rows
    from each based on a scoring of similarity.
    The input takes 7 arguments:
    dataList1 is the name of the first csv file
    datalist2 is the name of the second csv file
    outputList is the name of the output file
    data1col1 is the column number in the data1 set to compare first
    data2col1 is the column number in the data2 set to compare first
    data1col2 is the column number in the data1 set to compare second
    data2col2 is the column number in the data2 set to compare second
    The match will be based on a weighted score matching primary and secondary columns
    this will be done with the aid of stringscore 0.1.0
"""

import csv, pprint, sys
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz

# csv_object generates a csv reader object for subsequent copying of contents
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

# list_rid generates a list of the rows in a reader object
def list_rid(csvfile):
    csv_list = []
    reader = csv_object(csvfile)
    for row in reader:
        csv_list.append(row)
    return csv_list

def lose_headers(csvdata):
    return csvdata[1:]

def convertdates(csvdata, datecolumn):
    for row in csvdata:
        #print(row[datecolumn-1])
        try:
            row[datecolumn-1]=datetime.strptime(row[datecolumn-1], "%m/%d/%y %H:%M")
        except:
            print("NOPE, fucked up!!")
    return csvdata
    

# generates scores for each item in data1col1 compared to data1col2 (2x2 matrix)
def generate_scores(headers, csvdata1, csvdata2, d1colnum, d2colnum):
    allscores = []
    # reset the data column numbers so they fit with python's default zero-index
    d1col, d2col = int(d1colnum)-1, int(d2colnum)-1
    if headers:
        data1 = csvdata1[1:]
        data2 = csvdata2[1:]
    else:
        data1 = csvdata1[:]
        data2 = csvdata[:]
    # iterate over rows in data file 1
    for row in data1:
        # get the item in the row for to be matched
        item = row[d1col]
        itemscores = []
        # iterate over the rows in data file 2 to find the best match
        for rowcompare in data2:
            # compare the corresponding item in compare row to item in primary row
            # generate a list of scores: primary item <--> compare item in every row
            score = fuzz.ratio(item, rowcompare[d2col])
            itemscores.append(score)
        # generate a row for comparison scores in an "allscores" list
        allscores.append(itemscores)
    return allscores

def datescore(csvdata1, csvdata2, datecol1, datecol2, daylimit):
    # assumes headerless data
    datescores = []
    daylimit = timedelta(days=daylimit)
    optimal_delta = timedelta(days=3)
    for row_data1 in csvdata1:
        singledatescores=[]
        for row_data2 in csvdata2:
            td = row_data1[datecol1-1] - row_data2[datecol2-1]
            if td > daylimit:
                singledatescores.append(0)
            elif td < optimal_delta:
                singledatescores.append(100)
            else:
                datescore = 100*(td-optimal_delta)/(daylimit-optimal_delta)
                singledatescores.append(datescore)
        datescores.append(singledatescores)
    return datescores


def weightscores(scoremat1, scoremat2, datescores, weight1, weight2, dateweight):
    # normalize the weights
    scoreweight1 = weight1 / (weight1 + weight2 + dateweight)
    scoreweight2 = weight2 / (weight1 + weight2 + dateweight)
    scoreweight3 = dateweight / (weight1 + weight2 + dateweight)
    scoremat=[]
    tempmat_outer = zip(scoremat1, scoremat2, datescores)
    for row in tempmat_outer:
        temprow = zip(row[0], row[1], row[2])
        scorerow = []
        for cell in temprow:
            scorerow.append((scoreweight1*cell[0]+
                             scoreweight2*cell[1]+
                             scoreweight3*cell[2]))
        scoremat.append(scorerow)           
    return scoremat

def sortscores(scoremat):
    # sort the scores, searching for the highest score per row
    # output a list of 2-item lists matching the rows from the two data sets
    match_list = []
    checklist = []
    for mat1idx, row in enumerate(scoremat):
        max_value = max(row)
        max2_index = row.index(max_value)
        
        # if max index is already in the matchlist, find the second closest match
        if max2_index in checklist:
            second_max = 0
            for score in row:
                if score > second_max and score < max_value and (row.index(score) not in checklist):
                    second_max = score
            max2_index = row.index(second_max)

        match_list.append([mat1idx, max2_index])
        checklist.append(max2_index)
    return match_list

def makecsvoutdata(match_list, headers, csvdata1, csvdata2):
    outdata = []
    indxbump = 0
    if headers:
        headerline = csvdata1[0]+csvdata2[0]
        outdata.append(headerline)
        indxbump = 1
    for matchrow in match_list:
        linefirst = csvdata1[matchrow[0]+indxbump]
        linesecond = csvdata2[matchrow[1]+indxbump]
        line = linefirst + linesecond
        outdata.append(line)
    return outdata

def writecsv(outdata, outputList):
    with open(outputList, 'w') as csvfile:
        for row in outdata:
            outline = ''
            for item in row:
                outline = outline + str(item) + ","
            outline = outline + "\n"
            csvfile.writelines(outline)
    return outputList

# main gets the arguments and calls the appropriate functions in order
def main(*args):
    # read arguments from input
    try:

        # use if calling from script
        dataList1 = args[0]  # name of csv 1
        dataList2 = args[1]  # name of csv 2
        outputList = args[2] # name of output file
        headers = args[3]    # boolean if there are headers
        data1col1 = args[4]  # first column for first match in csv 1
        data2col1 = args[5]  # first column for first match in csv 2
        data1col2 = args[6]  # second column for second match in csv 1
        data2col2 = args[7]  # second column for second match in csv 2
        is_datecol = args[8] # boolean if using dates
        datecol1 = args[9]   # column number for dates in data1
        datecol2 = args[10]  # column number for dates in data2
        

    except IndexError:
        print("There was an error with the file names")
        dataList1  = "test.csv"
        dataList2 = "test2.csv"
        outputList = "outputList.csv"

    ### Read rid -- this uses python3 syntax, specifically the "newline" argument
    with open(dataList1 , newline='') as csvfile:
        data1 = list_rid(csvfile)
    with open(dataList2, newline='') as csvfile:
        data2 = list_rid(csvfile)

    ### work without headers
    if headers:
        nhdata1 = lose_headers(data1)
        nhdata2 = lose_headers(data2)
    else:
        nhdata1 = data1[:]
        nhdata2 = data2[:]
    
    ### Read and convert dates
    if is_datecol:
        nhdata1 = convertdates(nhdata1, datecol1)
        nhdata2 = convertdates(nhdata2, datecol2)   

    ### start the scoring protocol
    col1scores = generate_scores(headers, data1, data2, data1col1, data2col1)
    col2scores = generate_scores(headers, data1, data2, data1col2, data2col2)
    datescores = datescore(nhdata1, nhdata2, datecol1, datecol2, daylimit=30)
    pprint.pprint(datescores)
    weightedmat = weightscores(col1scores, col2scores, datescores, 1, 3, 20)
    matchlist = sortscores(weightedmat)
    print(matchlist)
    outdata = makecsvoutdata(matchlist, headers, data1, data2)
    #pprint.pprint(outdata)
    writecsv(outdata, outputList)

if __name__=='__main__':
    #main(*sys.argv)
    main("test.csv", "test2.csv", "test_out.csv", True, 1,1,2,2,1,4,4)

