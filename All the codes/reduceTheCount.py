import xlrd
import pymysql


#This line is for connecting python to mysql
myDB = pymysql.connect(host="127.0.0.1", user="root", passwd="f9d0s-jooN", db="tweetdb")

#Location of the file in my computer
cur = myDB.cursor()
###########Tweets into lists#############
loc = ("C:/UMD/Research/CountGramTweetResults/CountGram(Winnowed).xlsx")

putWordToDB = "insert into countwinnowedintweet (tweetID, gramID, count) values (%s, %s, %s);"

myWb = xlrd.open_workbook(loc)
sheet = myWb.sheet_by_index(0)
sheet.cell_value(0, 0)

tweets = {}
#for i in range(sheet.nrows):
for i in range(1, sheet.nrows):
    tweetID = int(sheet.cell_value(i,0))
    gramID = int(sheet.cell_value(i, 1))
    gramCount = int(sheet.cell_value(i, 2))
    cur.execute(putWordToDB, [tweetID, gramID, gramCount])
myDB.commit()