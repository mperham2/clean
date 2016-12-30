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

import csv, pprint
#from stringscore import liquidmetal
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

# generates scores for each item in data1col1 compared to data1col2 (2x2 matrix)
def generate_scores(headers, csvdata1, csvdata2, d1colnum, d2colnum):
    allscores = []
    d1col, d2col = d1colnum-1, d2colnum-1
    if headers:
        data1 = csvdata1[1:]
        data2 = csvdata2[1:]
        pprint.pprint(data1)
    else:
        data1 = csvdata1[:]
        data2 = csvdata[:]
    # iterate over rows in data file 1
    for row in data1:
        # get the item in the row for to be matched
        item = row[d1col]
        itemscores = []
        # iterate over the rows in data file 2
        for rowcompare in data2:
            # compare the corresponding item in compare row to item in primary row
            # generate a list of scores: primary item <--> compare item in every row
            score = fuzz.ratio(item, rowcompare[d2col])
            itemscores.append(score)
            print(item, rowcompare[d2col], score)
        # generate a row for comparison scores in an "allscores" list
        allscores.append(itemscores)
    return allscores

def weightscores(scoremat1, scoremat2, weight1, weight2):
    scoreweight1 = weight1 / (weight1 + weight2)
    scoreweight2 = weight2 / (weight1 + weight2)
    scoremat=[]
    # probably need matrix functionality here
    tempmat_outer = zip(scoremat1, scoremat2)
    for row in tempmat_outer:
        temprow = zip(row[0], row[1])
        scorerow = []
        for cell in temprow:
            scorerow.append((scoreweight1*cell[0]+scoreweight2*cell[1]))
        scoremat.append(scorerow)           
    return scoremat

def sortscores(scoremat):
    # sort the scores, searching for the highest score per row
    match_list = []
    for mat1idx, row in enumerate(scoremat):
        max_value = max(row)
        max2_index = row.index(max_value)
        match_list.append([mat1idx, max2_index])
    return match_list

def makecsvoutdata(matchlist, headers, csvdata1, csvdata2):
    outdata = []
    indxbump = 0
    if headers:
        headerline = csvdata1[0]+csvdata2[0]
        outdata.append(headerline)
        indxbump = 1
    for matchrow in matchlist:
        print(matchrow)
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
    '''
    idx = 0
    for arg in args:
        print("arg" + str(idx) + ": " + str(arg))
        idx+=1
        print(args[0])
        print(args[1])
    '''
    # read arguments from input
    try:
        dataList1 = args[0] # name of csv 1
        dataList2 = args[1] # name of csv 2
        outputList = args[2] # name of output file
        data1col1 = args[3] # first column for first match in csv 1
        data2col1 = args[4] # first column for first match in csv 2
        data1col2 = args[5] # second column for second match in csv 1
        data2col2 = args[6] # second column for second match in csv 2
        headers = args[7] # boolean if there are headers
    except IndexError:
        print("something didn't work")
        '''    
        dataList1  = "subjectsList.csv"
        dataList2 = "dataList.csv"
        outputList = "outputList.csv"
        '''
    ### Read rid -- this uses python3 syntax, specifically the "newline" argument
    with open(dataList1 , newline='') as csvfile:
        data1 = list_rid(csvfile)
    with open(dataList2, newline='') as csvfile:
        data2 = list_rid(csvfile)

    ### start the scoring protocol
    col1scores = generate_scores(headers, data1, data2, data1col1, data2col1)
    col2scores = generate_scores(headers, data1, data2, data1col2, data2col2)
    pprint.pprint(col1scores)
    pprint.pprint(col2scores)
    weightedmat = weightscores(col1scores, col2scores, 7, 3)
    pprint.pprint(weightedmat)
    matchlist = sortscores(weightedmat)
    pprint.pprint(matchlist)
    outdata = makecsvoutdata(matchlist, headers, data1, data2)
    print(outdata)
    writecsv(outdata, outputList)

if __name__=='__main__':
    #main(*sys.argv)
    main("test.csv", "test2.csv", "test_out.csv", 1,1,2,2, True)

