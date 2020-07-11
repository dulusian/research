from ast import literal_eval

import nltk
import xlrd
import pymysql
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

#This line is for connecting python to mysql
myDB = pymysql.connect(host="127.0.0.1", user="root", passwd="f9d0s-jooN", db="tweetdb")
cur = myDB.cursor()
putWordToDB = "insert into tweetphrases (tweets) values (%s);"

#Location of the file in my computer
loc = ("C:/UMD/Research/myFile.xlsx")

###########Tweets into lists#############
myWb = xlrd.open_workbook(loc)
sheet = myWb.sheet_by_index(0)
sheet.cell_value(0, 0)

tweets = []
for i in range(sheet.nrows):
    tweets.append(sheet.cell_value(i, 22))
############Tweets collected##############

#Stop words removal for unigram
ps = PorterStemmer() 
stop_words = set(stopwords.words('english')) 
tokenizer = RegexpTokenizer(r'\w+')
def elim_stop_words(word):
    word_tokens = tokenizer.tokenize(word)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []
    for w in word_tokens:
            if w not in stop_words:
                filtered_sentence.append(ps.stem(w))
    return filtered_sentence

for i in range(1, sheet.nrows - 1):
    eliminated_stop = elim_stop_words(tweets[i])
    for words in range(len(eliminated_stop)):
        dbWord = (' '.join(str(i) for i in eliminated_stop))
    cur.execute(putWordToDB, [dbWord])
myDB.commit()