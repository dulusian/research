select *, count(one_word)
From unigram
group by one_word
