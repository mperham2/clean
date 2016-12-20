import csv, re, codecs

class Csvo(object):
    def __init__(self, file, header=False):
        self.file = file
        self.header = header
        self.table = []

        with open(file, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, dialect='excel')
            print spamreader
            for row in spamreader:
                self.table.append(row) #x.strip() for x in row.split(','))

    def csvencoding(self):
        ## identify encoding and return in UTF-8
        print "csvencoding"
        for i, row in enumerate(self.table):
            for j, item in enumerate(row):
                self.table[i][j]=item.encode("utf8")
        return

    def spaceclean(self, text):
        return text.strip()

    def newlinebeginspaceclean(self, text):
        ## remove leading and trailing spaces and multiple spaces
        return re.sub('\n\s+','', text)

    def newlineendspaceclean(self, text):
        ## remove leading and trailing spaces and multiple spaces
        return re.sub('\s+\n','', text)

    def returnbeginspaceclean(self, text):
        ## remove leading and trailing spaces and multiple spaces
        return re.sub('\r\s+','', text)

    def returnendspaceclean(self, text):
        ## remove leading and trailing spaces and multiple spaces
        return re.sub('\s+\r','', text)

    def endspaceclean(self, text):
        ## remove leading and trailing spaces and multiple spaces
        return re.sub('\s+$','', text)

    def xtraspaceclean(self, text):
        return re.sub("\s{2,}", " ", text)

    def begreturnclean(self, text):
        ## remove multiple carriage returns
        ## remove returns on blank lines
        return re.sub("^\n+", "", text)

    def innerreturnclean(self, text):
        ## remove multiple carriage returns
        ## remove returns on blank lines
        return re.sub("\n{2,}", "\n", text)

    def listrepl(self,m):
        return m.group(1)

    def listreturncleanreturn(self, text):
        return re.sub("(\d\))(\n|\r)",self.listrepl, text)

    def listaddret(self,m):
        return m.group(1) + "\r" + m.group(2)

    def listreturncleanlist(self, text):
        return re.sub("(\w)(\d\))",self.listaddret, text)

    def cleancsv(self):
        self.csvencoding()
        print "cleancsv"
        for i, row in enumerate(self.table):
            for j, item in enumerate(row):
                item=re.sub("\s{2,}", " ", item.strip())
                item=re.sub("\r|\n", "", item)
                item=self.listreturncleanreturn(item)
                item=self.listreturncleanlist(item)
                self.table[i][j]=item
        print self.table
        return self.table

    def csvprint(self):
        print str(len(self.table)) + " rows"
        for row in self.table:
            print ' | '.join(row)

    def csvout(self):
        self.cleancsv()
        outfile = str(self.file).replace('.csv', '_out.csv')

        with open(outfile, 'w') as csvfile:
            if self.header:
                print self.table
                fieldnames = self.table[0]
                print "fieldnames:" + str(fieldnames)
            csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in self.table:
                csvwriter.writerow(row)
        return

    def __str__(self):
        return "\n".join(str(self.table).replace("[","").replace("]","").replace("{","").replace("}","").split(", "))



test1 = Csvo('test2.csv', True)
#test1.csvprint()
#test1.csvencoding()
#test1.cleancsv()
test1.csvout()

