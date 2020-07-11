import pymysql
import xlrd
import collections

from string import punctuation

myDB = pymysql.connect(host="127.0.0.1", user="root", passwd="f9d0s-jooN", db="tweetdb")
cur = myDB.cursor()

#file = open('C:/UMD/Research/sparseArffWinnowed.txt','at')

fin = open('C:/UMD/Research/sparseArffWinnowed.txt','rt')
data = fin.read()
data = data.replace('109791 3', '109791 2')
data = data.replace('109791 4', '109791 2')
data = data.replace('109791 5', '109791 2')
data = data.replace('109791 6', '109791 2')

fin.close()

fin = open('C:/UMD/Research/sparseArffWinnowed.txt','wt')
fin.write(data)
fin.close()
