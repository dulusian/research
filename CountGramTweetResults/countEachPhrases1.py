from nltk import RegexpTokenizer
import pymysql
from nltk.util import ngrams

#This line is for connecting python to mysql
myDB = pymysql.connect(host="127.0.0.1", user="root", passwd="f9d0s-jooN", db="tweetdb")

#Location of the file in my computer
cur = myDB.cursor()

tokenizer = RegexpTokenizer(r'\w+')
myGram = []
cur.execute("SELECT tweets FROM tweetphrases")
myDB.commit()
tweetPhrases = cur.fetchall()
idGram = []

cur.execute("SELECT gram FROM ngram")
row = cur.fetchone()
while row is not None:
    (fetched,) = row
    myGram.append(fetched)
    row = cur.fetchone()

cur.execute("SELECT gram_id FROM ngram")
idRow = cur.fetchone()
while idRow is not None:
    (ids,) = idRow
    idGram.append(ids)
    idRow = cur.fetchone()
file = open("C:/UMD/Research/CountGramTweetResults/CountGramTweet-1.txt", 'at')

for w in range(10001, 20000):
    dbWord = []
    word_tokens = tokenizer.tokenize(str(tweetPhrases[w]))
    tokens = []
    for tok in word_tokens:
        tokens.append(tok)
    for ngram in ngrams(tokens, 1):
        dbWord.append(' '.join(str(i) for i in ngram))
    for ngram in ngrams(tokens, 2):
        dbWord.append(' '.join(str(i) for i in ngram))
    for ngram in ngrams(tokens, 3):
        dbWord.append(' '.join(str(i) for i in ngram))
    for ngram in ngrams(tokens, 4):
        dbWord.append(' '.join(str(i) for i in ngram))
    counter = []
    for j in range(len(myGram)):
        for db in range(len(dbWord)):
            if str(myGram[j]) == str(dbWord[db]):
                counter.append(idGram[j])
    distinctWordList = set(counter)
    for i in distinctWordList:
        file.write(str(w + 1))
        file.write(",")
        file.write(str(i))
        file.write(",")
        file.write(str(counter.count(i)))
        file.write("\n")
