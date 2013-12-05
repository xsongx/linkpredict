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
user_path="/media/data3/twitter/usertweets/tweets/"
topic_models_path="/media/data3/twitter/"
user_list=os.listdir(user_path)
user_sequence=[(i,u) for i,u in enumerate(user_list)]
fuser=open('/media/data3/twitter/usersequence.pickle','w')
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
    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq <10]
    dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear only once
    dictionary.compactify() # remove gaps in id sequence after words that were removed
    dictionary.save('/media/data3/twitter/alltweets.dict')
    return dictionary
def dictionaryload(dictfile):
    dictionary = corpora.Dictionary.load(dictfile)
    return dictionary
def tweetscorpora(userfiles,dictionary):
    class MyCorpus(object):
        def __iter__(self):
            for line in usertweets(userfiles):
                # assume there's one document per line, tokens separated by whitespace
                yield dictionary.doc2bow(line.lower().split())
    twcorpora=MyCorpus()
    return twcorpora
def tweetslda(twcorpora,dictionary,top):
    twtopics = models.ldamodel.LdaModel(corpus=twcorpora, id2word=dictionary, num_topics=top, update_every=0, passes=50)
    savefile='topics_'+str(top)    
    twtopics.save(topic_models_path+savefile)
    return twtopics
#tweets_dictionary=dictionaryload(topic_models_path+'alltweets.dict')
tweets_dictionary=dictionarytweets(user_list)
tweets_corpora=tweetscorpora(user_list,tweets_dictionary)
tfidf_corpora=models.TfidfModel(tweets_corpora)
tfidf_corpora.save(topic_models_path+'tfidf.mm')
#corpora.MmCorpus.serialize(topic_models_path+'twcorpora.mm',tweets_corpora)
#topnum=set([50,60,70,80,90,100,110,120,130,140,150,160,170,180,190,200])
#for top in topnum:
#    topics=tweetslda(tfidf_corpora,tweets_dictionary)

