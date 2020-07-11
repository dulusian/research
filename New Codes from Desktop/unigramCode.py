from string import punctuation
from nltk.stem.snowball import SnowballStemmer
import xlrd
import pymysql
from nltk.stem import WordNetLemmatizer

from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

#This line is for connecting python to mysql
myDB = pymysql.connect(host="127.0.0.1", user="root", passwd="f9d0s-jooN", db="tweetdb")
cur = myDB.cursor()
putWordToDB = "insert into unigram (uniword) values (%s);"

#Location of the file in my computer
loc = ("C:/UMD/Research/myFile.xlsx")

###########Tweets into lists#############
myWb = xlrd.open_workbook(loc)
sheet = myWb.sheet_by_index(0)
sheet.cell_value(0, 0)

tweets = []
for i in range(sheet.nrows):
#for i in range(1,11):
    tweets.append(sheet.cell_value(i, 22))
    #print sheet.cell_value(2,22)
############Tweets collected##############

#Stop words removal for unigram
ps = SnowballStemmer("english")
lm = WordNetLemmatizer()
cachedStopWords = stopwords.words("english")

stop_words = list(stopwords.words('english'))
regexTokenizer = RegexpTokenizer(r'\w+')
punctuations = list(punctuation)
def tokenizeIntoList(sentence):
    word_tokens = word_tokenize(sentence)
    #word_tokens = sentence.split(' ')
    word_tokens[0] = ''.join(c for c in word_tokens[0] if c not in '\'')
    word_tokens[len(word_tokens) - 1] = ''.join(c for c in word_tokens[len(word_tokens) - 1] if c not in '\'')
    #print word_tokens
    for i in range(len(word_tokens)):
        wordToChange = word_tokens[i]
        if '\u2019' in wordToChange:
            word_tokens[i] = wordToChange.replace('\u2019', "'")
            temp = word_tokens[i]
            for j in range(len(stop_words)):
                if temp == stop_words[j]:
                    temp = ''
                    word_tokens[i] = temp
        if '\u201c' in wordToChange:
            word_tokens[i] = wordToChange.replace('\u201c', "'")
            temp = word_tokens[i]
            for j in range(len(stop_words)):
                if temp == stop_words[j]:
                    temp = ''
                    word_tokens[i] = temp
        if '\u201d' in wordToChange:
            word_tokens[i] = wordToChange.replace('\u201d', "'")
            temp = word_tokens[i]
            for j in range(len(stop_words)):
                if temp == stop_words[j]:
                    temp = ''
                    word_tokens[i] = temp
        if '\n' in wordToChange:
            word_tokens[i] = wordToChange.replace('\n', " ")
        if 'http' in wordToChange:
            word_tokens[i] = ""
        if 'was' == wordToChange:
            word_tokens[i] = 'is'
        if 'were' == wordToChange:
            word_tokens[i] = 'are'
        if 'would' == wordToChange:
            word_tokens[i] = 'will'
        if 'could' == wordToChange:
            word_tokens[i] = 'can'
        if 'had' == wordToChange:
            word_tokens[i] = 'have'
        if 'amp' in wordToChange:
            word_tokens[i] = ""
        if "because" in wordToChange:
            #print 'It is in'
            word_tokens[i] = ''
        if 'becaus' == wordToChange:
            word_tokens[i] = ''
        try:
            if '#' == wordToChange:
                word_tokens[i+1] = ''
            if '@' == wordToChange:
                word_tokens[i+1] = ''
        except IndexError:
            print 'not working on ', i+1
        for char in word_tokens[i]:
            if char in punctuations:
                word_tokens[i] = ''
        if 'because' == wordToChange:
            word_tokens[i] = ''
        if wordToChange in cachedStopWords:
            word_tokens[i] = ''
        if wordToChange in punctuations:
            word_tokens[i] = ''
            wordToChange = str(word_tokens[i])
            word_tokens[i] = lm.lemmatize(wordToChange.lower())
            # wordToChange = en.verb.present(word_tokens[i])
        # word_tokens = ([word for word in word_tokens if word.lower() not in cachedStopWords])
        # word_tokens = ([word for word in word_tokens if word not in punctuations])
    word_tokens = ([ps.stem(word) for word in word_tokens if word != "becaus"])
    for i in range(len(word_tokens)):
        if word_tokens[i] == 'becaus':
            word_tokens[i] = ''
    return word_tokens

def ngramWithoutStopPunct(tokens):
    oneWordList = []
    actualWordList = []
    for i in range(len(tokens)):
        j = 0
        while j < len(stop_words) and stop_words[j] != tokens[i] and tokens[i] != "":
            j = j + 1
            #print ps.stem(tokenized[i].lower()), "Stemmed"
        if j == len(stop_words):
            #print tokenized[i], " appended"
            oneWordList.append(i)
    for i in range(len(oneWordList)):
        actualWordList.append(tokens[oneWordList[i]])
    one_word = (' '.join(str(i) for i in actualWordList))
    regexed = regexTokenizer.tokenize(one_word)
    for i in regexed:
        cur.execute(putWordToDB, [i])


for i in range(1, sheet.nrows - 1):
#for i in range(0, 30):
    tokenizedList = tokenizeIntoList(tweets[i])
    ngramWithoutStopWords = ngramWithoutStopPunct(tokenizedList)

myDB.commit()