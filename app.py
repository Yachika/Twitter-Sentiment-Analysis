from flask import Flask, render_template, request, json
from flask import jsonify
import os
import json
import urllib2
from subprocess import Popen, PIPE
#import posTagging
#import bring_graph
#import bring_tweets
#import make_wordcloud
import all_in_one

app = Flask(__name__)
 
@app.route("/")
def main():
    return render_template('all_in_one_click.html')

@app.route('/fetch_graph', methods=['GET','POST'])
def fetch_graph():
    legend = 'AAP Data'
    print("Reached app")
    labels,values1,values2,values3 = count_sentiments.elections()
    return jsonify({'var1': legend, 'var2': labels, 'var3': values1, 'var4': values2, 'var5': values3})

@app.route('/fetch_tweets', methods=['GET','POST'])
def fetch_tweets():
    #tweets = ["a,b,c", "new, car, love"]
    tweets = bring_tweets.main_fun()
    #return("hello")
    return json.dumps(tweets)

@app.route('/fetch_wc', methods=['GET','POST'])
def fetch_wc():
    party_name = request.form['party_name']
    print(party_name)
    pos_words, neg_words = make_wordcloud.main_fun(party_name)
    return jsonify({'var1': pos_words, 'var2': neg_words})

@app.route('/fetch_data', methods=['GET','POST'])
def fetch_data():
    channel = request.form['channel'].encode('utf-8')
    e1 = request.form['entity1'].encode('utf-8')
    e2 = request.form['entity2'].encode('utf-8')
    e3 = request.form['entity3'].encode('utf-8')
    print(channel,e1,e2,e3)
    tweets, pos_words, neg_words = all_in_one.main_fun(channel,[e1,e2,e3])
    print(tweets)
    print("####### pos #######")
    print(pos_words)
    print("####### neg #######")
    print(neg_words)
    if(len(tweets)==0):
        return "0"
    else:
        #return json.dumps(tweets)
        return jsonify({'var1': tweets, 'var2': pos_words, 'var3': neg_words})

@app.route('/home', methods=['GET','POST'])
def home():
    return render_template('home.html')

@app.route('/docs', methods=['GET','POST'])
def about():
    print("hello")
    return render_template('docs.html')

@app.route('/demo', methods=['GET','POST'])
def demo():
    return render_template('demo.html')

@app.route('/contact', methods=['GET','POST'])
def contact():
    return render_template('contact.html')

@app.route('/extract', methods=['POST'])
def extract():
    keyword=request.form['input']
    print keyword
    tweets.get_all_tweets(keyword)
    return json.dumps("Done")

@app.route('/process', methods=['POST'])
def process():
    text=request.form['input']    
    return json.dumps(posTagging.processText(text))

@app.route('/targets', methods=['POST'])
def targets():
    print("####### hello #######")
    txtUrl=request.form['type']
    content=request.form['input']
    btn=request.form['btn']
    tar1=request.form['target1']
    tar2=request.form['target2']
    tar3=request.form['target3']
    tarArray=[]
    if(tar1!=""):
      tarArray.append(tar1)
    if(tar2!=""):
      tarArray.append(tar2)
    if(tar3!=""):
      tarArray.append(tar3)

    print tarArray
      
    try:
        if content=="":
            result="Please input some Text or URL"
        else:
            if(txtUrl=="text"):
                result=serveRequestText.targeted(content,tarArray)
            else:
                result=serveRequestUrl.targeted(content,tarArray)

    except:
        result="Sorry!!! Cann't display results"
    return json.dumps(result)

@app.route('/categorization', methods=['POST'])
def categorization():
    print("####### hello #######")
    txtUrl=request.form['type']
    content=request.form['input']
    btn=request.form['btn']
    niche=request.form['radioBtn']
    print txtUrl,",",content,",",btn,",",niche

    try:
        if content=="":
            result="Please input some Text"
        else:
            if(txtUrl=="url"):
              result="This function works with text. So try giving text"
            else:
                result=repustatText.categorize(content,niche)

    except:
        result="Sorry!!! Cann't display results"
    print result
    return json.dumps(result)

@app.route('/doAnal', methods=['POST'])
def doAnal():
    print("####### hello #######")
    txtUrl=request.form['type']
    content=request.form['input']
    btn=request.form['btn']
    print "btn:",btn
    posTags=""

    try:
        if(btn=="sentiment"):
            if txtUrl=='text':
                print("Yes")
                result=repustateT.sentiment(content)
                print result
            else:
                result=serveRequestURL.sentiment(content)
                print result
                    
        elif(btn=="emotion"):
            if txtUrl=='text':
                result=serveRequestText.emotion(content)
                print result
            else:
                result=serveRequestURL.emotion(content)
                print result
                    
        elif(btn=="entity"):
            if txtUrl=='text':
                result=serveRequestText.entity(content)
                print result
            else:
                result=serveRequestURL.entity(content)
                print result
                    
        elif(btn=="concept"):
            if txtUrl=='text':
                result=serveRequestText.concept(content)
                print result
            else:
                result=serveRequestURL.concept(content)
                print result
                    
        elif(btn=="author"):
            if txtUrl=='text':
                result="This function works with URL. So, try giving URL"
                print result
            else:
                result=serveRequestURL.author(content)
                print result

        elif(btn=="feeds"):
            if txtUrl=='text':
                result="This function works with URL. So, try giving URL"
                print result
            else:
                result=serveRequestURL.feeds(content)
                print result

        elif(btn=="pos"):
            print "***************"
            if txtUrl=='url':
                result="This function works with text. So, try giving text"
                print result
            else:
                text = nltk.word_tokenize(content)
                posTags = nltk.pos_tag(text)
                print posTags
                result=json.dumps(posTags)
                print result

        elif(btn=="taxonomy"):
            if txtUrl=='text':
                result=serveRequestText.taxonomy(content)
                print result
            else:
                result=serveRequestURL.taxonomy(content)
                print result

        elif(btn=="keyword"):
            if txtUrl=='text':
                result=serveRequestText.keyword(content)
                print result
            else:
                result=serveRequestURL.keyword(content)
                print result

        elif(btn=="textb"):
            if txtUrl=='text':
                result="This function works with URL. So, try giving URL"
                print result
            else:
                result=serveRequestURL.text(content)
                print result

        elif(btn=="targeted"):
            if txtUrl=='text':
                result=serveRequestText.targeted(content)
                print result
            else:
                result=serveRequestURL.targeted(content)
                print result

        elif(btn=="relation"):
            if txtUrl=='text':
                result=serveRequestText.relation(content)
                print "result:  ",result
            else:
                result=serveRequestURL.relation(content)

        elif(btn=="typedRel"):
            if txtUrl=='text':
                result=serveRequestText.typedRel(content)
                print result
            else:
                result=serveRequestURL.typedRel(content)
                print result

        for element in result:
            if 'status' in element:
                del element['status']
        #result=JSON.parse(result)
        #txt=""
        '''for x in result:
            if(x!="status" or x!="usage" or x!="totalTransactions"):
                txt += response[x]
                txt+="\n"'''
    except:
        result="Sorry!!! Cann't display results"
    return json.dumps(result)
    '''a="a"
    b="b"
    c="c"
    result={a:"hello",b:"world",c:"god bless u"}'''
    

if __name__=="__main__":
    app.run()

