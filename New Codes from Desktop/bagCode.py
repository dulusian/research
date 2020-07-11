import pymysql


#This line is for connecting python to mysql
myDB = pymysql.connect(host="127.0.0.1", user="root", passwd="f9d0s-jooN", db="tweetdb")

#Location of the file in my computer
cur = myDB.cursor()

wordsToDB = "insert into ngram (gram) values (%s);"
####UNIGRAM INTO N-GRAM####
cur.execute("SELECT DISTINCT uniword FROM unigram")
words = cur.fetchall()
for word in words:
	cur.execute(wordsToDB, [word])

####BIGRAM INTO N-GRAM####
cur.execute("SELECT DISTINCT biword FROM bigram")
words = cur.fetchall()
for word in words:
	cur.execute(wordsToDB, [word])

####TRIGRAM INTO N-GRAM####
cur.execute("SELECT DISTINCT triword FROM trigram")
words = cur.fetchall()
for word in words:
	cur.execute(wordsToDB, [word])

####QUADRAGRAM INTO N-GRAM####
cur.execute("SELECT DISTINCT quadraword FROM quadragram")
words = cur.fetchall()
for word in words:
	cur.execute(wordsToDB, [word])

myDB.commit()