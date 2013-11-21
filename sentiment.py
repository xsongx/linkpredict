# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:05:33 2013

@author: xsongx
"""
import zipfile
import sentimentstrength
import json
import pickle
import os
zfile = zipfile.ZipFile('/media/work/codingspace/UDIdata/UDI-TwitterCrawl-Aug2012-Tweets.zip','r')
procfiles=os.listdir('/media/work/codingspace/UDIdata/sentiment/')
i=0
for ufile in zfile.namelist():
    if ufile.split('/')[-1] not in procfiles:
        utweet=zfile.read(ufile)
        if utweet:
            try:
                fuser=open('/media/work/codingspace/UDIdata/sentiment/'+ufile.split('/')[-1],'wb')
                usertweets=[]
                utwlist=[tweet.strip() for tweet in utweet.split('***') if len(tweet)>1]
                for tweet in utwlist:
                    twdict={}
                    twrecord1=tweet.split('Origin:')[-1].strip()
                    tworigin=twrecord1.split('Text:')[0].strip()
                    twrecord2=twrecord1.split('Text:')[1].strip()
                    twtext=twrecord2.split('URL:')[0].strip()
                    twrecord3=twrecord2.split('URL:')[1].strip()
                    twurl=twrecord3.split('ID:')[0].strip()
                    twrecord4=twrecord3.split('ID:')[1].strip()
                    twid=twrecord4.split('Time:')[0].strip()
                    twrecord5=twrecord4.split('Time:')[1].strip()
                    twtime=twrecord5.split('RetCount:')[0].strip()
                    twrecord6=twrecord5.split('RetCount:')[1].strip()
                    twrecount=twrecord6.split('Favorite:')[0].strip()
                    twrecord7=twrecord6.split('Favorite:')[1].strip()
                    twfavorite=twrecord7.split('MentionedEntities:')[0].strip()
                    twrecord8=twrecord7.split('MentionedEntities:')[1].strip()
                    twentity=twrecord8.split('Hashtags:')[0].strip()
                    twhashtag=twrecord8.split('Hashtags:')[1].strip()
                    sentiment=sentimentstrength.RateSentiment(twtext+' '+twhashtag.replace('#',''))[:3]
                    twdict['Origin']=tworigin
                    twdict['Text']=twtext
                    twdict['URL']=twurl
                    twdict['ID']=twid
                    twdict['Time']=twtime
                    twdict['RetCount']=twrecount
                    twdict['Favorite']=twfavorite
                    twdict['MentionedEntities']=twentity
                    twdict['Hashtags']=twhashtag
                    twdict['Sentiment']=sentiment
                    usertweets.append(twdict)
                pickle.dump(usertweets,fuser)
    #            userjson=json.dumps(usertweets,indent=4)
    #            json.dump(userjson,fuser)
                fuser.close()
                i=i+1
                print str(i)+':'+ufile+':'+str(len(usertweets))
            except:
                print 'error'+utweet
                exit(0)
    else:
        print ufile+' has exist!'
        
