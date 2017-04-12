# for full code see streaming

import twitter
from twitter import *
import json
from collections import Counter
import datetime
import matplotlib.pyplot as plt
import sys
import tweepy
import csv
import datetime
import nltk
nltk.data.path.append('./nltk_data/')
import codecs
from sklearn.svm import LinearSVC, SVC
import io
import re
import unicodedata
from os import path
from PIL import Image
from wordcloud import WordCloud, ImageColorGenerator
'''reload(sys)
sys.setdefaultencoding('utf8')'''

consumer_key = "Xo5faElN0vMkCCaworESnFcnS"
consumer_secret = "kWRNlmqeGANOnKbWFyOYcW79JA3JncjRYEWtsabnnRFSYYW15K"
access_key = "807076865152143360-Mpfe2eKAdZoUsNoN019XRXupV8vKmiH"
access_secret = "NBPV1SC8ejObpiDuN84kJ24i9ZHOkNuwSzSy0JjDyou2N"

def read_tweets(fname):
    tweets=[]
    with open(fname, 'r') as f:
        next(f)
        for row in f:
            array=row.split(',')
            tweets.append([array[1:],array[0]])
    f.close()
    return tweets

def extract_features(document):
    document_words = set(document)
    features = {}
    for word in document_words:
      features['contains({})'.format(word)] = True
    return features

def preprocess_tweets(t):
    line=[]
    #for t in tweet:
    t = t.lower()
    t = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',t)
    t = re.sub(r'@([^\s]+)', r'\1', t)
    t = re.sub('[\s]+', ' ', t)
    t = re.sub(r'#([^\s]+)', r'\1', t)
    t = t.strip('\'"')
    '''line.append(t)
    line=''.join(line)'''
    return t

def classify_tweet(tweet, classifier):
    return(classifier.classify(extract_features(nltk.word_tokenize(tweet))))

#text="RT @DaljeetKSandhu: Panchkula police on Sunday night held five peoples for allegedly drinking in public places @HTPunjab https://t.co/d068w"

def main_fun(channel, ent):
    entities = []
    for e in ent:
        entities.append(e.lower())
    print(entities)
    #entities = [e.lower for e in entities]
    #nbm=dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    print("########### step-1 ############")
    
    auth = twitter.oauth.OAuth(access_key, access_secret, consumer_key, consumer_secret)
    twitter_api = twitter.Twitter(auth=auth)
    q = channel

    search_results = twitter_api.search.tweets(q=q, count=100)
    print("########### step-2 ############")
    #print(len(search_results))
    statuses = search_results['statuses']
    
    tweets = []
    train_tweets = read_tweets('data files/train_refined.csv')
    for tweet,sentiment in train_tweets:
        tweet=','.join(tweet)
        words_filtered = [e for e in tweet.split()]
        tweets.append((words_filtered,sentiment))

    feature_set = []
    feature_set = [(extract_features(word_list), sentiment) for (word_list,sentiment) in tweets]
    
    cutoff=int(len(feature_set)*3/4)
    train_feats = feature_set[:cutoff]
    test_feats = feature_set[cutoff:]
    MEclassifier = nltk.classify.maxent.MaxentClassifier.train(train_feats, 'GIS', trace=0, encoding=None, labels=None, gaussian_prior_sigma=0, max_iter = 5)
    print(nltk.classify.accuracy(MEclassifier, test_feats))
    
    allTweets = []
    forWordCloud = []
    
    if (entities[0]=='' and entities[1]=='' and entities[2]==''):
        print("case:1")
        for tweet in statuses:
            text = tweet['text']
            tw = text
            processed = "".join([ch for ch in text if ord(ch)<= 128])
            processed = preprocess_tweets(processed)
            sentiment = int(classify_tweet(processed, MEclassifier))
            date = tweet['created_at']
            allTweets.append(text+"   ,   "+date+"   ,   "+str(sentiment)+"<br><br>")
            forWordCloud.append((processed, sentiment))
    else:
        print("case:2")
        for tweet in statuses:
            text = tweet['text']
            tw = text
            processed = "".join([ch for ch in text if ord(ch)<= 128])
            processed = preprocess_tweets(processed)
            for user_mention in tweet['entities']['user_mentions']:
                scr_name = user_mention['screen_name']
                name = user_mention['name']
                scr_name = (unicodedata.normalize('NFKD', scr_name).encode('ascii','ignore')).lower()
                name = (unicodedata.normalize('NFKD', name).encode('ascii','ignore')).lower()
                if(scr_name in entities or name in entities) or any(len(e)>0 and e in processed for e in entities):
                    sentiment = int(classify_tweet(processed, MEclassifier))
                    date = tweet['created_at']
                    allTweets.append(text+"   ,   "+date+"   ,   "+str(sentiment)+"<br><br>")
                    forWordCloud.append((processed, sentiment))
                    
    #print(allTweets)
    ################### Wordcloud ####################
    pos_tweets = []
    neg_tweets = []
    neutral_tweets = []
    for (tw,sentiment) in forWordCloud:
        if sentiment==1:
            pos_tweets.append(tw)
        elif sentiment==-1:
            neg_tweets.append(tw)
        else:
            neutral_tweets.append(tw)

    word_string_pos = pos_tweets
    word_string_pos = ''.join(word_string_pos)
    
    wordlist = []
    all_words = word_string_pos.split()
    for word in all_words:
        if word not in STOPWORDS:
            wordlist.append(word)
    wordlist = nltk.FreqDist(wordlist)  #(word,frequency)
    word_string_pos = (",").join(wordlist)

    ############## negative word string ###############

    word_string_neg = neg_tweets
    word_string_neg = ''.join(word_string_neg)
    
    wordlist = []
    all_words = word_string_neg.split()
    for word in all_words:
        #if word not in STOPWORDS:
        wordlist.append(word)
    wordlist = nltk.FreqDist(wordlist)  #(word,frequency)
    word_string_neg = (",").join(wordlist)
    print(len(allTweets))
    return(allTweets, word_string_pos, word_string_neg)
    
'''
arr =['','','']
main_fun('times of india', arr)
'''

