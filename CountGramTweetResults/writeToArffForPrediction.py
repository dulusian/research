import pymysql
import xlrd
import collections

from string import punctuation

myDB = pymysql.connect(host="127.0.0.1", user="root", passwd="f9d0s-jooN", db="tweetdb")
cur = myDB.cursor()

file = open('C:/UMD/Research/sparseArff.txt','at')
'''
fin = open('C:/UMD/Research/sparseArff.txt','rt')
data = fin.read()
data = data.replace('109791 6', '109791 2')
fin.close()

fin = open('C:/UMD/Research/sparseArff.txt','wt')
fin.write(data)
fin.close()
'''
#########Adding gram ID to arff file############
punctuations = list(punctuation)
counter = 1

cur.execute("SELECT gram FROM ngram")
words = cur.fetchall()

'''
for line in fin:
    for golbang in line:
        if '@' in golbang:
            fout.write(line.replace('@','%'))
'''
file.write('@RELATION classification\n')
file.write("@ATTRIBUTE 0_AVOID_INDEX NUMERIC\n")

for word in words:
    file.write('@ATTRIBUTE')
    file.write(' ')
    file.write(str(counter))
    file.write('_')
    word = ''.join(c for c in word if c not in punctuation)
    splitted = str(word)
    splitted = '_'.join(splitted.split(" "))
    file.write(splitted)
    file.write(' ')
    file.write('NUMERIC\n')
    counter = counter + 1
'''
for word in range(1, 109794):
    word = str(word)
    word = ''.join(c for c in word if c not in punctuation)
    file.write('@ATTRIBUTE')
    file.write(' ')
    file.write('ngram')
    file.write(word)
    file.write(' ')
    file.write('NUMERIC\n')
'''

#####Adding class to arff file#######
winnowedLoc = ("C:/UMD/Research/CountGramTweetResults/countGram.xlsx")
#gramIDLoc = ("C:/UMD/Research/CountGramTweetResults/gramID.xlsx")

winnowedWB = xlrd.open_workbook(winnowedLoc)
#gramWB = xlrd.open_workbook(gramIDLoc)

winnowedSheet = winnowedWB.sheet_by_index(0)
tempSheet = winnowedWB.sheet_by_index(0)
winnowedSheet.cell_value(0, 0)
tempSheet.cell_value(0,0)

tweetIDS = []
for i in range(1, winnowedSheet.nrows):
    val = int(winnowedSheet.cell_value(i, 0))
    if val not in tweetIDS:
        tweetIDS.append(val)
indexForTweetID = 0

topicNumTracker = 0
sorterForGram = {}
sorterForTopic = {}
file.write('@ATTRIBUTE class {1,2,3,4,5,6}\n')
file.write('@DATA\n')
file.write('{')
for i in range(1, winnowedSheet.nrows):
    tweetID = int(winnowedSheet.cell_value(i,0))
    #topicNumber = int(winnowedSheet.cell_value(i, 1))
    gramID = int(winnowedSheet.cell_value(i, 1))
    gramCount = int(winnowedSheet.cell_value(i,2))
    if tweetID != tweetIDS[indexForTweetID]:
        od = collections.OrderedDict(sorted(sorterForGram.items()))
        for num in od:
            file.write(' ')
            file.write(str(num))
            file.write(' ')
            file.write(str(od[num]))
            file.write(',')
        file.write(' 109791')
        file.write(' ')
#        file.write('\'topic')
        file.write('?')
        file.write('}\n')
        file.write('{')

        indexForTweetID = indexForTweetID + 1
        sorterForGram = {}
        od = {}
        sorterForGram[gramID] = gramCount
        #topicNumTracker = topicNumber


    else:
        #print 'gramID: ', gramID, 'gramCount: ', gramCount
        sorterForGram[gramID] = gramCount
        #topicNumTracker = topicNumber
