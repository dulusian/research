import pymysql
import xlrd
import xlwt
import openpyxl
from openpyxl import workbook
from openpyxl import load_workbook
from pymysql import IntegrityError

myDB = pymysql.connect(host="127.0.0.1", user="root", passwd="f9d0s-jooN", db="tweetdb")
cur = myDB.cursor()
cur.execute("SELECT * FROM winnowforwholetweet ORDER BY tweetID, gramID")
ids = cur.fetchall()
tweetID = [x[0] for x in ids]
gramID = [x[1] for x in ids]

'''
for i in range(len(tweetID)):
    print tweetID[i], gramID[i]
'''

