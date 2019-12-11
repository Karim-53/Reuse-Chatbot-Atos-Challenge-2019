#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

import urllib2
import wget # sehr lagsam , better use urllib2
from getExactData import * 
# from association_rule import * # replaced by seperate_functions
from seperate_functions import * # association rule mining UDF
from database import *
#import urllib
#from urllib2 import request as reqqq
import subprocess

# Flask app should start in global layout
app = Flask(__name__)
#######
link = "https://www.facebook.com/permalink.php?story_fbid=1993472214292745&id=1993440317629268"
jsonFile = "LastReq.json"
file_FACEBOOK_MEDIA =  '/home/karim/FACEBOOK_MEDIA.jpg' # ~/darknet/     # ~/myproject/
##########
#TODO: raw el python ma ye5demch ki n9oloulou what can i do with a bottle ?
# article lel optimisation fhemt menou chay https://mediatum.ub.tum.de/doc/1094637/TUM-I0412.pdf
# Evaluation of Association Rules , 9rineha w peu etre hia eli na3mlou beha el elimination bta3 el rules
# Leave 1 out cross validation hia el 7aja eli tse3edna 5ater base de donnee yesser sghira


#init
rules = ARM_train(dataset)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    #json.dump(req, jsonFile,indent=4)

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    #r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("resolvedQuery") == "FACEBOOK_MEDIA":
        return useCase_ImageRecognition(req)

    elif req.get("result").get("action") == "GiveIdea":
        result = req.get("result")
        parameters = result.get("parameters")
        lista = parameters.get("Objectnames")
        return useCase_GiveIdea(lista)

    elif req.get("result").get("action") == "interest":  # this code is just for testing the chtbot and is not part of the Reuse solution
        result = req.get("result")
        parameters = result.get("parameters")
        zone = parameters.get("Objectnames")
    
        cost = {'Andhra Bank':'6.85%', 'Allahabad Bank':'6.75%', 'Axis Bank':'6.5%', 'Bandhan bank':'7.15%', 'Bank of Maharashtra':'6.50%', 'Bank of Baroda':'6.90%', 'Bank of India':'6.60%', 'Bharatiya Mahila Bank':'7.00%', 'Canara Bank':'6.50%', 'Central Bank of India':'6.60%', 'City Union Bank':'7.10%', 'Corporation Bank':'6.75%', 'Citi Bank':'5.25%', 'DBS Bank':'6.30%', 'Dena Bank':'6.80%', 'Deutsche Bank':'6.00%', 'Dhanalakshmi Bank':'6.60%', 'DHFL Bank':'7.75%', 'Federal Bank':'6.70%', 'HDFC Bank':'5.75% to 6.75%', 'Post Office':'7.10%', 'Indian Overseas Bank':'6.75%', 'ICICI Bank':'6.25% to 6.9%', 'IDBI Bank':'6.65%', 'Indian Bank':'4.75%', 'Indusind Bank':'6.85%', 'J&K Bank':'6.75%', 'Karnataka Bank':'6.50 to 6.90%', 'Karur Vysya Bank':'6.75%', 'Kotak Mahindra Bank':'6.6%', 'Lakshmi Vilas Bank':'7.00%', 'Nainital Bank':'7.90%', 'Oriental Bank of Commerce':'6.85%', 'Punjab National Bank':'6.75%', 'Punjab and Sind Bank':'6.4% to 6.80%', 'Saraswat bank':'6.8%', 'South Indian Bank':'6% to 6.75%', 'State Bank of India':'6.75%', 'Syndicate Bank':'6.50%', 'Tamilnad Mercantile Bank Ltd':'6.90%', 'UCO bank':'6.75%', 'United Bank Of India':'6%', 'Vijaya Bank':'6.50%', 'Yes Bank':'7.10%'}
    
        speech = "The interest rate of " + zone + " is " + str(cost[zone])
        print("Response:")
        print(speech)
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": [],
            "source": "BankRates"
        }
    elif req.get("result").get("action") == "randomidea":
        speech = "you can try this: " + link
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            #"contextOut": [],
            "source": "BankRates"
        }
    else:
        
        return {}
    
def download(url,faya):
    filedata = urllib2.urlopen(url)  
    datatowrite = filedata.read()

    with open(faya, 'wb') as f:  
        f.write(datatowrite)

def useCase_ImageRecognition(req):
    imgContent = "VOID"
    print("useCase_ImageRecognition")
    imgURL = req.get("originalRequest").get("data").get("message").get("attachments")[0].get("payload").get("url")
    print(imgURL)
    print('Beginning file download...')
    #urllib.request.urlretrieve(url, '~/myproject/FACEBOOK_MEDIA.jpg') # rod belek 7keyet .jpg wala .png wala je sais pas XD 
    #wget.download(imgURL, file_FACEBOOK_MEDIA)  
    download(imgURL,file_FACEBOOK_MEDIA)
    #result = subprocess.run(['~/darknet/darknet', 'detect', 'cfg/yolov3.cfg', 'yolov3.weights', file_FACEBOOK_MEDIA], stdout=subprocess.PIPE)
    #print( result.stdout )
    #imgContent = result.stdout


    #proc = subprocess.Popen(['/home/karim/darknet/darknet', 'detect', '/home/karim/darknet/cfg/yolov3.cfg', '/home/karim/darknet/yolov3.weights', file_FACEBOOK_MEDIA], stdout=subprocess.PIPE, cwd="/home/karim/darknet/")
    proc = subprocess.Popen(['/home/karim/darknet/darknet', 'detect', '/home/karim/darknet/cfg/yolov3-tiny.cfg', '/home/karim/darknet/yolov3-tiny.weights', file_FACEBOOK_MEDIA], stdout=subprocess.PIPE, cwd="/home/karim/darknet/")
    output = proc.stdout.read()
    print("*******************----------***********************\n")
    print( output )
    print("*******************----------***********************\n")
    type(output)
    lista = getExactData(output)
    if not lista:
        #print("List is empty")
        speech = "Sorry, the image is not clear enough, please try another one or enter the list of object directly." # association_rule(contenu, dataset, map)
        return {
            "speech": speech,
            "displayText": speech,
            "source": "agent"
        }

    imgContent = ", ".join(lista)

    speech = "image content: " + imgContent
    print(speech)
    return speechFormat(speech +"\n" + ListToPrediction(lista) )

def useCase_GiveIdea(lista):
    for i in range(0 , len(lista)):
            lista[i] = "".join(e for e in lista[i] if e.isalpha())

    listContent = ", ".join(lista)
    speech = "List: " + listContent

    return speechFormat(speech +"\n" + ListToPrediction(lista) )

def ListToPrediction(lista):

    # association_rule
    contenu=set(lista)
    #TODO: eliminate things we can t reuse like dog, person hhhhh
    #propositions = list()
    #print("propositions")
    #print(propositions)


    #TODO: y7ebou cross validation
    #TODO: nchoufou 3al internet how to do cross valisation fel cas bta3 el rule mining
    #TODO: est ce que bech na3mlou base de donne statique fel code python maktouba wala we will extract the data mel fb

    #todo: en fin de compte we agreeed on : na3mlou data set sghira 3al fb, extratiwha bidina , el id wel contenu (bottle , 7keya)

    return ARM_predict_sting(ARM_predict_list(contenu,ActiveUserTransactions,rules,mapping)) # ARM_predict(contenu,rules,mapping=map) # association_rule(contenu, dataset, map)
def speechFormat(speech):
    return {
        "speech": speech,
        "displayText": speech,
        "source": "agent",
        #"attachment": {
        #    "type": "audio",
        #    "payload": {
        #        "url": "https://scontent-frt3-2.xx.fbcdn.net/v/t1.0-9/55576013_2127401727312889_7534456038389448704_n.jpg?_nc_cat=109&_nc_ht=scontent-frt3-2.xx&oh=fad237e7cc29334e1de591f767f820ea&oe=5D37D0D1"
        #    }
        #}
        #"image_url":"https://scontent-frt3-2.xx.fbcdn.net/v/t1.0-9/55576013_2127401727312889_7534456038389448704_n.jpg?_nc_cat=109&_nc_ht=scontent-frt3-2.xx&oh=fad237e7cc29334e1de591f767f820ea&oe=5D37D0D1"
    }
if __name__ == '__main__':
    #test
    print("test:")
    lista = ["bottle .", "tire ?"]
    print(useCase_GiveIdea(lista))
    #run
    print("run:")
    port = int(os.getenv('PORT', 5000))
    print ("Starting app on port %d" %(port))
    app.run(debug=True, port=port, host='127.0.0.1', use_reloader=False)
