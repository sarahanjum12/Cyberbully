# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 20:46:50 2024

@author: prath
"""


from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import sys
import time
from transformers import pipeline, BlipProcessor, BlipForConditionalGeneration
from PIL import Image 
import base64
from models import ToxicRemover
from Regexes import RegexHero
from Whisper import whisperCall, distilled_student_sentiment_classifier, VoiceOutput
import threading

import requests

Chats = []



app = Flask(__name__)
CORS(app)
print("Starting this app")

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")

def delayTime(t):
    tstart = time.time()
    while(time.time() - tstart < t):
        pass
 
@app.route("/")
def hello():
    print('Hello', file=sys.stdout)
    return "Hello I'm under the water"

@app.route("/sendMessage", methods = ['POST'])
def sendMessage():
    Req = request.json
    tim = time.time()
    Req['Time'] = tim
    imgstring = Req['Image']
    #print(imgstring)
    outString = ""
    if(imgstring != ""):
        imgstring = imgstring[imgstring.find(",") + 1:]
        image = base64.b64decode(imgstring)
        
        filename = 'some_image{0}.png'.format(tim)
        with open(filename, 'wb') as f:
            f.write(image)
        
        #BLIP Side of the Code
        raw_image = Image.open(filename).convert('RGB')
        text = "a photography of"
        inputs = processor(raw_image, text, return_tensors="pt")
        out = model.generate(**inputs)
        outString = processor.decode(out[0], skip_special_tokens=True)
    print(outString, file = sys.stdout)
    Req['Image'] = ""
    
    #Do the sentiment analysis now
    Ans = distilled_student_sentiment_classifier(Req['message'].lower() + " " + outString)[0]
    
    #Appending the request to the rest of the code
    LessTox = ToxicRemover(Req['message'].lower())
    Req['Neg'] = Ans[2]['score']
    Req['Better'] = LessTox
    Chats.append(Req)
    #print(Req)
    return {"Status": "Success", "Toxics": Ans}

@app.route("/deleteChat", methods = ['POST'])
def deleteChat():
    Req = request.json
    print(Req)
    Chats = []
    return {"Status": "Success"}
    

@app.route("/getUpdates", methods = ['POST'])
def getUpdates():
    Updates = []
    tim = request.json['lastFetch']
    print("Last Fetch Time: {0}".format(tim), file = sys.stdout)
    if(tim == ''):
        tim = -1
    tim = float(tim)
    timNew = time.time()
    for chat in Chats:
        if(float(chat['Time']) > tim):
            Updates.append({'Time': timNew, 'User': chat['UserName'], 'Value': chat['message']})
    return {'UpdateTime': timNew,'Updates': Chats, 'Voice': VoiceOutput}

@app.route("/extension", methods = ['POST'])
def extension():
    Req = request.json
    htmlDat = Req['Title']
    newHtmlDat = RegexHero(htmlDat)
    return {"Title": newHtmlDat}

@app.route("/voiceMessage", methods=['POST'])
def voiceMessage():
    #threading.Thread(whisperCall, args=["C:\\Simple\\recorded_audio.wav",])
    whisperCall("C:\\Simple\\recorded_audio.wav")
    return {"Status": "Success"}
    

if __name__ == "__main__":
    app.run(debug = False, port = 5050)

