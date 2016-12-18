import csv, re, codecs

class Csvo(object):
    def __init__(self, file):
        # create self.sheet as a DictReader object
        self.file = file
        self.table = []
        with open(file) as csvfile:
            sheet = csv.DictReader(csvfile)
            for row in sheet:
                self.table.append(row)

    def csvencoding(self):
        ## identify encoding and return in UTF-8
        for row in self.table:
            i = 0
            for key, value in row.iteritems():
                try:
                    self.table[i][key] = value.encode("utf8")
                except:
                    pass
                i+=1

        return self.csvprint()

    def beginspaceclean(self, text):
        ## remove leading and trailing spaces and multiple spaces
        return re.sub('^\s+','', text)

    def newlinebeginspaceclean(self, text):
        ## remove leading and trailing spaces and multiple spaces
        return re.sub('\n\s+','', text)

    def newlineendspaceclean(self, text):
        ## remove leading and trailing spaces and multiple spaces
        return re.sub('\s+\n','', text)

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

    def listrepl(self,matchobj):
        return m.group(1)

    def listreturnclean(self, text):
        return re.sub("(\d\))(\n)",self.listrepl, text)

    def cleancsv(self):
        self.csvencoding()
        i = 0
        for row in self.table:
            for key,val in row.iteritems():
                print key, val
                self.table[i][key]=self.beginspaceclean(val)
                self.table[i][key]==self.newlinebeginspaceclean(val)
                self.table[i][key]==self.newlineendspaceclean(val)
                self.table[i][key]==self.endspaceclean(val)
                self.table[i][key]==self.xtraspaceclean(val)
                self.table[i][key]==self.begreturnclean(val)
                self.table[i][key]==self.innerreturnclean(val)
                self.table[i][key]==self.listreturnclean(val)
                print key, self.table[i][key]
            i+=1
        return self.table

    def csvprint(self):
        print str(len(self.table)) + " rows"
        for row in self.table:
            print ' | '.join('{}: {}'.format(key, value) for key, value in row.items())

    def csvout(self):
        self.csvencoding()
        self.cleancsv()
        outfile = str(self.file).replace('.csv', '_out.csv')
        with open(outfile, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
            csvwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
        pass

    def __str__(self):
        return "\n".join(str(self.table).replace("[","").replace("]","").replace("{","").replace("}","").split(", "))



test1 = Csvo('test2.csv')
test1.csvprint()
test1.csvencoding()
test1.cleancsv()

