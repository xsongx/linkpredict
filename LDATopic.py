# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 21:06:03 2013

@author: xsongx
"""
import sys
sys.path.append("..")
from gensim import corpora,models, similarities
from nltk.corpus import stopwords
import os,logging
#from  topic import ascii_encoding
#from nltk.stem import PorterStemmer
import pickle

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
stopword_list=set(stopwords.words("english"))
user_path="/media/work/codingspace/UDIdata/usertweets/tweets/"
topic_models_path="/media/work/codingspace/UDIdata/"
user_list=os.listdir(user_path)
user_sequence=[(i,u) for i,u in enumerate(user_path)]
fuser=open('/media/work/codingspace/UDIdata/usersequence.pickle','w')
pickle.dump(user_sequence,fuser)
fuser.close()
def usertweets(userfiles):
    for userfile in userfiles:
        fuser=open(user_path+userfile,'rb')
        userlist=pickle.load(fuser)
        tweetlist=[u['Text'].strip()+u['Hashtags'].strip() for u in userlist if u['Text'].strip()+u['Hashtags'].strip()]
        tweets=' '.join(tweetlist)
        print userfile
        yield tweets
def dictionarytweets(userfiles):
    dictionary = corpora.Dictionary(line.lower().split() for line in usertweets(userfiles))
    # remove stop words and words that appear only once
    stop_ids = [dictionary.token2id[stopword] for stopword in stopword_list if stopword in dictionary.token2id]
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq ==1]
    dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
    dictionary.compactify() # remove gaps in id sequence after words that were removed
    dictionary.save('/media/work/codingspace/UDIdata/alltweets.dict')
    return dictionary
def tweetscorpora(userfiles,dictionary):
    class MyCorpus(object):
        def __iter__(self):
            for line in usertweets(userfiles):
                # assume there's one document per line, tokens separated by whitespace
                yield dictionary.doc2bow(line.lower().split())
    twcorpora=MyCorpus()
    return twcorpora
def tweetslda(twcorpora,dictionary):
    twtopics = models.ldamodel.LdaModel(corpus=twcorpora, id2word=dictionary, num_topics=100, update_every=0, passes=20)
    twtopics.save(topic_models_path+'topic100')
    return twtopics
tweets_dictionary=dictionarytweets(user_list)
tweets_corpora=tweetscorpora(user_list,tweets_dictionary)
corpora.MmCorpus.serialize(topic_models_path+'twcorpora.mm',tweets_corpora)
#topics=tweetslda(tweets_corpora,tweets_dictionary)   

