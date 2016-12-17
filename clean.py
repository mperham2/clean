import csv, re

class Csvo(object):
    def __init__(self, file):
        # create self.sheet as a DictReader object
        self.table = []
        with open(file) as csvfile:
            sheet = csv.DictReader(csvfile)
            for row in sheet:
                self.table.append(row)

    def csvencoding(self):
        ## identify encoding and return in UTF-8
        pass

    def spaceclean(self):
        ## remove leading and trailing spaces and multiple spaces

        pass

    def returnclean(self, text):
        ## remove multiple carriage returns
        ## remove returns on blank lines
        if 
        pass

    def csvprint(self):
        print str(len(self.table)) + " rows"
        for row in self.table:
            print ' | '.join('{}: {}'.format(key, value) for key, value in row.items())



    def __str__(self):
        return "\n".join(str(self.table).replace("[","").replace("]","").replace("{","").replace("}","").split(", "))



test1 = Csvo('test.csv')
test1.csvprint()
print test1