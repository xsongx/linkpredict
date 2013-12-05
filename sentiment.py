# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 09:05:33 2013

@author: xsongx
"""

import pickle
import os
zfile =set(os.listdir('/media/work/codingspace/UDIdata/usertweets/tweets/')) #zipfile.ZipFile('/media/work/codingspace/UDIdata/UDI-TwitterCrawl-Aug2012-Tweets.zip','r')
#fff=set(os.listdir('/media/data1/UDI-twitter/error/'))
fuser=open('/media/work/codingspace/UDIdata/alltweets.txt','w')
for ufile in zfile:
    utweet=pickle.load(open('/media/work/codingspace/UDIdata/usertweets/tweets/'+ufile,'rb'))#zfile.read(ufile)#open('/media/data1/UDI-twitter/error/'+ufile,'r').read()
    if utweet:
        usertw=[]
        try:                
            for tweet in utweet:
                twtext=tweet['Text']+tweet['Hashtags']
                twline='UID-TWID-TEXT'+'\t'+ufile+'\t'+tweet['ID']+'\t'+twtext
                usertw.append(twline)
            fuser.write('\n'.join(usertw)+'\n')
            print ufile+':'+str(len(utweet))
        except:
            ferror=open('/media/work/codingspace/UDIdata/error/'+ufile,'w')
            pickle.dump(utweet,ferror)
            ferror.close()
            print 'error:'+ufile
            pass
fuser.close()        
